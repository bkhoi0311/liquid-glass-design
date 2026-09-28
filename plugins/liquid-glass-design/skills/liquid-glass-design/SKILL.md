---
name: liquid-glass-design
description: DEFAULT design system for ANY visual or UI work — websites, landing pages, web apps, dashboards, components, HTML artifacts, mockups, React/Next.js/Vite/Tailwind, SwiftUI/iOS/macOS — in Apple's Liquid Glass style (iOS 26 / macOS Tahoe glass, glassmorphism, frosted translucent chrome, Apple HIG polish). Use it whenever the user asks to design, build, restyle or beautify an interface, even if "glass" or "Apple" is not mentioned. Does NOT apply to ClassIn-branded work (use design-classin-2026 / guide-classin-2026) or when the user names another style.
---

# Liquid Glass Design (v2.2)

Apple-grade Liquid Glass interfaces on web and SwiftUI. Goal: **beautiful, clear, professional, trusted** — premium through restraint, not effects. v2.2 folds in what won two blind benchmark rounds (trust-first structure, hero discipline, contrast-safe tokens, light utility typography) and caps the cost of each build.

## 0. Scope and priority

- **Default** for every design/UI request.
- **Exception — ClassIn:** ClassIn / EEO work, or the user names `design-classin-2026` → use that skill (and `guide-classin-2026`). Never mix.
- The user names another style or brand → follow the user; keep the quality gate (section 7).
- Video, slides and documents use their own skills.

## 1. Design read (one line, before any code)

Write: **"Reading this as: ‹page kind› for ‹audience›, trust level ‹high/normal›, surface ‹utility/flagship›."**
- **Audience decides, not taste.** B2B buyers (schools, finance, public sector, IT, procurement) = **trust-first**: calm, dense with facts, glass only on nav/toolbars, no cinematic effects except one product demo moment.
- **Utility** (app, dashboard, form, settings): motion ≤ 300 ms, no scroll scenes.
- **Flagship** (consumer launch, product showcase): at most ONE scroll-linked scene.

## 2. Workflow and cost budget

1. Design read (section 1).
2. **Start from a kit page** — never from zero:
   - Landing / marketing → `assets/starter.html`
   - Dashboard / app screen → `assets/dashboard-starter.html`
   - Always with `assets/tokens.css` (+ `assets/liquid-glass.js` only if refraction is used). Single-file deliverable → inline both.
   - Existing project → add `tokens.css` as `app/liquid-glass.css` or `src/styles/liquid-glass.css`, `liquid-glass.js` to `public/`.
3. Replace content with the real brief. Keep the structure; add sections the brief needs.
4. Run the gate **once**: `python3 scripts/qa.py page.html [page2.html]` (needs `pip install playwright && playwright install chromium`; on Daniel's Mac use `~/Developer/liquid-glass-design/scripts/qa.sh page.html`) → read its report + the 3 screenshots → fix → run **once more**. Stop there.

**Budget:** read at most 2 reference sections (grep the heading, read only that section). No repeated screenshot loops. No reading references "just in case". If the kit is not on disk, `git clone --depth 1 https://github.com/bkhoi0311/liquid-glass-design` once.

## 3. Rules that make it look Apple and earn trust

**Layering**
- Glass = floating chrome only: nav bar, tab bar, toolbar, sheet, popover, player/widget over media. Content (text, tables, forms, pricing, KPIs, lists) sits on **solid** `--lg-bg-elevated`.
- Never glass on glass. Glass needs something behind it (imagery, `.lg-backdrop`, scrolling content).
- Buttons on solid surfaces use `.lg-button` (fill + hairline) or `--prominent`. `.lg-button--glass` only over imagery.

**Colour and type**
- Light by default (`#f5f5f7` page, white cards). Dark follows the OS; at most one deliberate dark section per page.
- **One accent, locked for the whole page.** Text/links use `--lg-tint`, filled buttons `--lg-tint-fill`, text on soft tint `--lg-tint-ink`. Status uses `--lg-positive / --lg-negative / --lg-warning` — never the accent.
- Only use token colours for text. Every text token passes 4.5:1; do not invent lighter greys or dim "inactive" text below 4.5:1 (hide it or keep it readable).
- **One shape scale:** pill buttons, 20 px cards, 12 px inner items (concentric).
- Font: use `--lg-font` / `--lg-font-display` exactly (SF → Segoe → Roboto → Helvetica → **Arial**). Never end a stack on `system-ui` (heavy DejaVu on Linux). Weights: display 650, titles 600, body 400 — avoid 700+ outside the hero.
- Headline tracking −0.03em; body 17 px on marketing pages, 15 px (`.lg-dense` on `<body>`) on utility screens; `tabular-nums` for all figures.

**Landing page structure (trust-first)**
1. **Hero fits the first viewport:** headline ≤ 2 lines desktop, subtext ≤ 25 words, max 4 text elements (optional eyebrow, headline, subtext, CTAs), 1 primary + max 1 secondary CTA, the **real product visible** (screenshot or faithful HTML mock) — split layout by default.
2. **Proof row directly under the hero** (`.lg-proof`): the real numbers from the brief.
3. Features: varied layout, exactly as many cells as items — no empty tiles, no empty areas inside cards.
4. **Pricing** (`.lg-pricing`): featured tier = tint ring + badge **inside the card flow** (never overlapping the plan name); every tier has a visible button; show billing terms (VAT, per year).
5. Testimonial: ≤ 3 lines, name + role + organisation.
6. Final CTA with a concrete next step (demo length, phone/email as text).
- **One label per intent** (e.g. "Đặt lịch demo" everywhere, not three variants). Button labels never wrap.
- **Eyebrows (small labels above headings): max 1 per 3 sections.**
- **Product mocks are complete and correct:** every panel filled with plausible content; any plotted curve/number is mathematically right; floating chips/cards sit **outside** key UI (never over buttons, names, titles, faces).

**Content at rest**
- Everything is readable with no scrolling or JS: reveal effects use `.lg-js .lg-reveal` (visible without JS), numbers are rendered final in HTML — **no count-up animations**.
- Scroll scenes: max one, every step readable, no empty runway after the last step, and the section must make sense as a static screenshot.

**Motion**
- Spring-like curves (`--lg-ease`, `--lg-ease-spring`), transform/opacity only, press `scale(.97)`. Always honour `prefers-reduced-motion`.

**Mobile (390 px) — decide per section**
- Every multi-column block states its phone layout. Tables become cards with **all** columns (`.lg-table` + `data-label`). Nothing may cross the right edge (`qa.py` checks).
- **Tab bar only in apps/dashboards, never on marketing websites** (it covers content). Websites collapse the nav to logo + primary CTA (+ menu button). App top bar keeps search (short placeholder) + avatar; filters move into the page header.

## 4. Dashboards (utility)

- Order: page title + period → KPI row → main chart + "needs attention" → detail table.
- **KPI** (`.lg-kpi`): label, value, delta = arrow + sign + unit + "so với tuần trước", semantic colour. **No decorative progress bars** unless there is a real target.
- **Alerts** (`.lg-alert--critical / --warning / default` + `.lg-alert-icon`): compact rows, icon + 600-weight title + one-line meta + one **text** action (`.lg-button--plain`). Critical rows get a tinted background so problems stand out; information stays neutral; count pill in the header ("2 khẩn").
- **Status colour = meaning:** negative/warning only for problems; scheduled / in progress = info; done = neutral.
- **Use the brief's labels verbatim** (alert text, class names, menu items) — do not split, shorten or rename them.
- **Mobile:** KPI cards 2 per row; every sidebar destination reachable (tab bar max 5 = 4 + "Thêm"/More).
- **Charts:** bar charts use `.lg-bars` (HTML/CSS — text stays readable on phones; never let an SVG chart scale its text below 11 px). `--max` is a round number above the data max; value labels above bars; optional average line `.lg-bars-ref`; low values `.lg-bar--muted`, the highlight `.lg-bar--peak` (not orange/red unless it is a problem).
- Sidebar colour spans the **whole page height** (paint it on the layout column, not on a 100vh box); current item `--lg-tint-ink` on `--lg-tint-soft`. Glass only on the sticky top bar and mobile tab bar.
- Body `class="lg-dense"`; cards 20 px padding; avoid oversized alert boxes and heavy bold text.

## 5. Web kit (assets/)

| File | Purpose |
|---|---|
| `tokens.css` | Tokens (light/dark via OS or `data-theme`) + `.lg-root .lg-display .lg-secondary .lg-tertiary .lg-num` · `.lg-glass` (`--thin/--ultrathin/--thick/--media`) · `.lg-nav` (`--floating`) · `.lg-button` (`--prominent/--glass/--plain/--sm/--block`) · `.lg-icon-button .lg-toolbar .lg-segmented` · `.lg-card .lg-list` · `.lg-proof` · `.lg-pricing .lg-plan(--featured) .lg-plan-badge .lg-plan-price` · `.lg-kpis .lg-kpi .lg-delta--up/down/flat` · `.lg-bars .lg-bar(--peak/--muted) .lg-bars-ref` · `.lg-pill--positive/negative/warning/info/neutral` · `.lg-alert(--critical/--warning) .lg-alert-icon` · `.lg-table` · `.lg-dense` · `.lg-sheet .lg-tabbar .lg-backdrop .lg-reveal`. Accessibility fallbacks included — keep them. |
| `starter.html` | Landing starter: floating nav, split hero with glass player over a living backdrop, proof row, feature grid, pricing, testimonial, final CTA, sheet, theme toggle. |
| `dashboard-starter.html` | Dashboard starter (`.lg-dense`): full-height sidebar, glass top bar, KPI row, SVG chart, compact severity alerts, table→cards, mobile tab bar. |
| `liquid-glass.js` | Real edge refraction (Chromium); frosted fallback elsewhere. `liquidGlass(el, { scale: -90, chroma: 5, blur: 4 })` on 1–3 hero elements ≤ 800 px. Decoration only. |
| `LiquidGlass.tsx` | React/Next.js client wrapper (`"use client"`, `useEffect`, destroy on unmount). |

Tailwind: keep `tokens.css` and use the classes, or map tokens in `@theme` (`--color-tint: var(--lg-tint)` …). Deploy (Vercel/Netlify): static assets only; test Chrome AND Safari.

## 6. SwiftUI (iOS 26+ / macOS 26+)

Native APIs only — never fake glass with blur.
```swift
Text("Label").padding().glassEffect()
Image(systemName: "heart").padding().glassEffect(.regular.tint(.blue).interactive(), in: .rect(cornerRadius: 16))
GlassEffectContainer(spacing: 30) { /* sibling glass controls; enables morphing */ }
Button("Go") { }.buttonStyle(.glass)   // .glassProminent for the primary action
.backgroundExtensionEffect()
.tabBarMinimizeBehavior(.onScrollDown)
```
Glass only on navigation/controls; `.clear` only over bold media; `.identity` to disable; remove custom bar backgrounds. Details: `references/swiftui/`.

## 7. Quality gate (must pass before "done")

`python3 scripts/qa.py page.html` checks JS errors, text contrast (solid backgrounds), clipped elements at 390 px, sideways scroll, invisible content, small tap targets, and saves light/dark/mobile screenshots. Then check by eye:
1. Text on glass/gradients readable in the screenshots (the script lists how many to check).
2. Hero: fits the first screen, product visible, ≤ 4 text elements.
3. Proof row under hero; pricing badge not overlapping; one label per intent; eyebrows ≤ 1 per 3 sections.
4. No empty areas, no chips covering UI, numbers final.
5. Dark mode and 390 px layouts look finished; frosted fallback looks finished (Safari).

## 8. References (on demand, one section at a time)

`grep -n "^## " file`, read only the needed section. Old names inside files (apple-design-*) map here.

| File | Read when |
|---|---|
| `01-restraint-and-antislop.md` | Unsure how much effect is too much |
| `02-materials-liquid-glass.md` | Custom glass recipe beyond the kit |
| `03-glass-tokens-design-md.md` | Compact Apple token sheet |
| `04-color.md` · `05-typography.md` · `06-layout-grid-spacing.md` | Custom palette · type scale · grids/breakpoints |
| `07-component-anatomy.md` · `08-states-loading-empty-error.md` | Components not in the kit · loading/empty/error states |
| `09-motion.md` · `10-microinteractions.md` | Springs, choreography · feedback details |
| `11-accessibility.md` | WCAG edge cases |
| `12-landing-page-applecom.md` · `13-scrollytelling.md` | Consumer flagship page · the one scroll scene |
| `14-bento-grid.md` | Bento stat cards |
| `swiftui/*` | Native Liquid Glass |

Sources (MIT): deepika-builds/liquid-glass, haider-nawaz/liquid-glass-skill, s1gmamale1/apple-design-skills, hubeiqiao/apple-bento-grid, rohitg00/awesome-claude-design. Trust-first structure informed by a blind benchmark against design-taste-frontend (2026-09-28).
