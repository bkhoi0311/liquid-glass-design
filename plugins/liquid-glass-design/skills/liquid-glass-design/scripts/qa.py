#!/usr/bin/env python3
"""Liquid Glass Design — one-command quality gate.

Usage:  python3 qa.py page.html [more.html ...] [--out DIR]
Needs:  pip install playwright && playwright install chromium   (or a preinstalled Chromium)

For each page it:
  1. scrolls through the page like a visitor (so reveal/scroll effects settle),
  2. saves 3 screenshots: desktop light, desktop dark (1280 px), mobile light (390 px),
  3. reports JS errors, sideways overflow / elements past the right edge at 390 px,
     text contrast below WCAG AA (computed on solid backgrounds; text over glass or
     images is listed as "check by eye"), tap targets under 44 px, and hidden content
     (opacity < 0.1 after scrolling).
Exit code 1 if any hard failure. Read the screenshots once, fix, run once more. Do not loop.
"""
import asyncio, json, os, sys
from playwright.async_api import async_playwright

JS_AUDIT = r"""
() => {
  const W = window.__LG_W || (window.visualViewport ? window.visualViewport.width : window.innerWidth);
  const parse = s => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const mix = (fg, bg) => ({ r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1 });
  function background(el) {
    let layers = [];
    for (let n = el; n; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return { unknown: 'gradient/image behind text' };
      if ((cs.backdropFilter && cs.backdropFilter !== 'none') || (cs.webkitBackdropFilter && cs.webkitBackdropFilter !== 'none')) {
        const c = parse(cs.backgroundColor); if (!c || c.a < 0.85) return { unknown: 'text on glass' }; }
      const c = parse(cs.backgroundColor);
      if (c && c.a > 0) { layers.push(c); if (c.a >= 0.99) break; }
    }
    let bg = { r: 255, g: 255, b: 255, a: 1 };
    const rootBg = parse(getComputedStyle(document.body).backgroundColor);
    if (rootBg && rootBg.a > 0.99) bg = rootBg;
    for (let i = layers.length - 1; i >= 0; i--) bg = mix(layers[i], bg);
    return { color: bg };
  }
  const out = { contrast: [], glassText: 0, smallTargets: [], pastEdge: [], hidden: 0 };
  const seen = new Set();
  document.querySelectorAll('body *').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const r = el.getBoundingClientRect(); if (r.width === 0 || r.height === 0) return;
    if (parseFloat(cs.opacity) < 0.1 && el.textContent.trim()) out.hidden++;
    if (r.right > W + 1 && r.left < W - 1 && cs.position !== 'fixed' && !el.closest('[data-qa-scroll], .lg-scroll, table') && out.pastEdge.length < 8)
      out.pastEdge.push(`${el.tagName.toLowerCase()}.${String(el.className).split(' ')[0]} right=${Math.round(r.right)}`);
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (own && parseFloat(cs.opacity) > 0.1) {
      const fg = parse(cs.color); const b = background(el);
      if (b.unknown) { out.glassText++; }
      else if (fg) {
        const f = mix(fg, b.color); const L1 = lum(f), L2 = lum(b.color);
        const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
        const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700;
        const need = (size >= 24 || (size >= 18.66 && bold)) ? 3 : 4.5;
        const key = el.tagName + el.className + cs.color;
        if (ratio < need && !seen.has(key)) { seen.add(key);
          out.contrast.push(`${ratio.toFixed(2)} < ${need}  "${el.textContent.trim().slice(0, 40)}"  (${el.tagName.toLowerCase()}.${String(el.className).split(' ')[0]})`); }
      }
    }
    if (el.matches('a, button, input, select, [role=button], [role=tab]')) {
      const inline = el.tagName === 'A' && cs.display === 'inline' && el.closest('p, li, td');
      if (!inline && (r.height < 44 || r.width < 44) && out.smallTargets.length < 10)
        out.smallTargets.push(`${el.tagName.toLowerCase()} "${(el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 24)}" ${Math.round(r.width)}x${Math.round(r.height)}`);
    }
  });
  out.overflowX = Math.max(document.documentElement.scrollWidth, window.innerWidth) - W;
  return out;
}
"""

async def settle(pg):
    h = await pg.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < h:
        await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(150); y += 400
        h = await pg.evaluate("document.documentElement.scrollHeight")
    await pg.wait_for_timeout(1200)

async def audit(browser, path, outdir):
    name = os.path.basename(os.path.dirname(os.path.abspath(path))) + "-" + os.path.splitext(os.path.basename(path))[0]
    url = "file://" + os.path.abspath(path)
    report = {"page": path, "errors": []}
    for label, vp, scheme, mobile in [("desktop-light", (1280, 900), "light", False), ("desktop-dark", (1280, 900), "dark", False), ("mobile", (390, 844), "light", True)]:
        ctx = await browser.new_context(viewport={"width": vp[0], "height": vp[1]}, color_scheme=scheme, is_mobile=mobile, has_touch=mobile)
        pg = await ctx.new_page()
        pg.on("pageerror", lambda e: report["errors"].append(str(e)))
        pg.on("console", lambda m: report["errors"].append(m.text) if m.type == "error" else None)
        await pg.goto(url); await settle(pg)
        await pg.evaluate(f'window.__LG_W = {vp[0]}')
        res = await pg.evaluate(JS_AUDIT)
        await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(400)
        shot = os.path.join(outdir, f"{name}-{label}.png"); await pg.screenshot(path=shot)
        report[label] = res | {"screenshot": shot}
        await ctx.close()
    return report

def summarise(r):
    hard = 0
    print(f"\n=== {r['page']}")
    if r["errors"]: hard += 1; print("  FAIL JS errors:", r["errors"][:3])
    for mode in ("desktop-light", "desktop-dark", "mobile"):
        m = r[mode]
        if m["contrast"]: hard += 1; print(f"  FAIL contrast ({mode}):"); [print("     ", c) for c in m["contrast"][:10]]
        if m["hidden"]: print(f"  WARN {m['hidden']} text elements still invisible after scrolling ({mode}) — content must be visible at rest")
        if m["glassText"]: print(f"  CHECK {m['glassText']} text elements sit on glass/gradient ({mode}) — verify by eye in the screenshot")
    mob = r["mobile"]
    if mob["overflowX"] > 0: hard += 1; print("  FAIL page scrolls sideways at 390 px by", mob["overflowX"], "px")
    if mob["pastEdge"]: hard += 1; print("  FAIL elements past the right edge at 390 px (clipped):", mob["pastEdge"])
    if mob["smallTargets"]: print("  WARN tap targets < 44 px:", mob["smallTargets"])
    print("  screenshots:", ", ".join(r[m]["screenshot"] for m in ("desktop-light", "desktop-dark", "mobile")))
    print("  RESULT:", "PASS" if hard == 0 else f"{hard} hard failure group(s)")
    return hard

async def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    outdir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "qa-shots"
    if "--out" in sys.argv: args.remove(outdir)
    os.makedirs(outdir, exist_ok=True)
    async with async_playwright() as p:
        exe = os.environ.get("CHROMIUM_PATH")
        browser = await p.chromium.launch(**({"executable_path": exe} if exe else {}))
        reports = [await audit(browser, a, outdir) for a in args]
        await browser.close()
    json.dump(reports, open(os.path.join(outdir, "qa.json"), "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if sum(summarise(r) for r in reports) else 0)

if __name__ == "__main__":
    asyncio.run(main())
