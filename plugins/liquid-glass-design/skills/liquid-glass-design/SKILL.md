---
name: liquid-glass-design
description: DEFAULT design system for ANY visual or UI work — websites, landing pages, web apps, dashboards, components, HTML artifacts, mockups, React/Next.js/Vite/Tailwind, SwiftUI/iOS/macOS — in Apple's Liquid Glass style (iOS 26 / macOS Tahoe glass, glassmorphism, frosted translucent chrome, Apple HIG polish). Use it whenever the user asks to design, build, restyle or beautify an interface, even if "glass" or "Apple" is not mentioned. Does NOT apply to ClassIn-branded work (use design-classin-2026 / guide-classin-2026) or when the user names another style.
---

# Liquid Glass Design

One skill for Apple-grade Liquid Glass interfaces on web and SwiftUI. Goal: **beautiful, clear, professional** — premium through restraint, not effects.

## 0. Scope and priority

- This is the **default** for every design/UI request.
- **Exception — ClassIn:** if the work is for ClassIn / EEO (or the user says "ClassIn design", "design-classin-2026"), use `design-classin-2026` (and `guide-classin-2026`) instead. Do not mix the two.
- If the user explicitly names another style or brand system, follow the user. Keep this skill's quality gate (section 6) anyway.
- Video, slides and documents use their own skills; borrow tokens from here only if asked.

## 1. Workflow (do in order)

1. **Classify the surface.**
   - *Utility* (app screen, dashboard, form, settings, tool): motion near-invisible (≤300 ms), no cinematic effects.
   - *Flagship* (landing, product, hero): motion is the substance — at least one scroll-linked scene; a static page fails.
2. **Detect the platform.** `package.json` → web. `*.xcodeproj` / `Package.swift` → SwiftUI (go to section 5). Unclear and no repo → web.
3. **Start from the kit, not from zero.**
   - New page / artifact: copy `assets/starter.html` + `assets/tokens.css` + `assets/liquid-glass.js`, then replace content.
   - Existing project: add `tokens.css` (as `app/liquid-glass.css` or `src/styles/liquid-glass.css`) and `liquid-glass.js` (to `public/`); map to the project's components.
   - Single-file artifact: inline `tokens.css` and `liquid-glass.js` into the page.
4. **Place glass only on floating chrome** (section 2), build content on solid surfaces, then add motion to the surface budget.
5. **Run the quality gate** (section 6) and fix before saying "done".

## 2. The rules that make it look Apple (not AI-generic)

**Layering**
- Glass = the **navigation/control layer floating above content**: nav bar, tab bar, toolbar, sidebar, sheet, popover, floating button, player/widget over media.
- Content (text blocks, tables, forms, lists, cards of information) sits on **solid** `--lg-bg-elevated`. Ask: "could a plain solid card replace this glass with no loss?" — then use solid.
- **Never glass on glass.** Group neighbouring glass controls in ONE container (`.lg-toolbar`), like SwiftUI `GlassEffectContainer`.
- Glass needs something behind it. Over a flat page it is invisible — use `.lg-backdrop`, real imagery, or scrolling content.

**Restraint**
- **Light by default** (`#f5f5f7` page, white cards). Dark is either the user's OS setting or one deliberate section — never a dark-by-default hero.
- **One accent** (`--lg-tint`, default `#0071e3`). Neutral everywhere else. Gradient text 0–1 times per page.
- **Type + whitespace carry hierarchy**, not borders, boxes or glow. Big, tight headline (`.lg-display`, tracking −0.035em); body 17 px; secondary text in `--lg-text-secondary`.
- **Show the real product**: real screenshot or a faithful UI mock in a device frame. Abstract blobs as "the product" = fail.
- No hard 1 px borders on cards, no drop shadows on content cards, no rainbow tiles, no emoji icons. Use simple stroke SVG icons (never ship SF Symbols or SF Pro files on the web — license).
- For every effect: "remove it — does the design lose meaning or only decoration?" Decoration → remove.

**Shape and space**
- Radii: 12 / 18 / 26 / 36 / pill. **Concentric corners:** inner radius = outer radius − padding.
- 4/8 pt spacing; sections 80–120 px apart on desktop; touch targets ≥ 44 px.

**Motion**
- Spring-like curves (`--lg-ease`, `--lg-ease-spring`), interruptible, transform/opacity only.
- Press feedback: `scale(0.96)`. Sheets rise with a spring. Reveal-on-scroll with `.lg-reveal`.
- Always honour `prefers-reduced-motion`.

## 3. Web kit (assets/)

| File | Purpose |
|---|---|
| `tokens.css` | All tokens (light + dark via OS or `data-theme`) and components below. Accessibility fallbacks included — do not delete them. |
| `liquid-glass.js` | Real edge refraction + chromatic fringe via SVG displacement (Chromium). Safari/Firefox get frosted fallback automatically. |
| `starter.html` | Reviewed reference page: floating nav, hero, glass player + toolbar + segmented control over a living backdrop, solid feature cards, grouped list, sheet, mobile tab bar, theme toggle. |
| `LiquidGlass.tsx` | React/Next.js client component wrapping `liquid-glass.js` (loads once, destroys on unmount, skips on reduced transparency). |

**Classes:** `.lg-root` (on `<html>`), `.lg-display`, `.lg-secondary` · `.lg-glass` + `--thin | --ultrathin | --thick | --media` (media = dark tint + white text for photos/video) · `.lg-nav` (+ `--floating` capsule) · `.lg-button` (+ `--prominent | --plain | --sm`), `.lg-icon-button` · `.lg-toolbar` · `.lg-segmented` (buttons with `aria-pressed`) · `.lg-card`, `.lg-list`, `.lg-list-icon` (solid content) · `.lg-sheet` (on `<dialog>`) · `.lg-tabbar` · `.lg-backdrop` · `.lg-reveal` (+ `.is-in`).

**Refraction (`liquid-glass.js`)**
```js
const g = liquidGlass(el, { scale: -90, chroma: 5, blur: 4 }); // add class lg-refract to el
// subtle -60/4 · default -112/6 · dramatic -180. g.supported false → frosted fallback. g.destroy() on unmount.
```
- Use on 1–3 hero elements (cards, player, floating toolbar) ≤ ~800 px per side. Never on full-page or scrolling lists.
- Refraction is decoration only; the page must look finished in Safari.
- Keep `color-interpolation-filters="sRGB"` (the module sets it).

**React / Next.js:** copy `liquid-glass.js` to `public/`, import `tokens.css` once in the root layout, use `<LiquidGlass className="lg-glass--media">…</LiquidGlass>`. Glass JS is client-only (`"use client"`, inside `useEffect`).

**Tailwind:** keep `tokens.css` and use the classes, or map tokens in `tailwind.config` / `@theme` (`--color-tint: var(--lg-tint)` etc.). Tailwind equivalent of `.lg-glass`: `bg-white/70 dark:bg-zinc-900/65 backdrop-blur-xl backdrop-saturate-[1.8] rounded-[26px] shadow-[inset_0_1px_0.5px_rgba(255,255,255,.85),0_0_0_.5px_rgba(0,0,0,.06),0_16px_40px_rgba(0,0,0,.12)]`.

**Deploy (Vercel / Netlify / GitHub Pages):** the assets are static files; no env vars, no server code. Test the deployed URL in Chrome AND Safari.

## 4. Special layouts

- **Landing / marketing page:** apple.com formula — sticky translucent nav, product-as-hero, one idea per section, full-bleed feature sections, bento once, fat footer. Read `references/12-landing-page-applecom.md` and `13-scrollytelling.md`.
- **Stats / summary cards:** Apple bento grid — `references/14-bento-grid.md`.
- **App screens / settings / forms:** `references/07-component-anatomy.md`; loading, empty and error states from `08-states-loading-empty-error.md`.
- **Dashboards:** solid cards on `--lg-bg`; glass only on the top bar, filters toolbar and floating actions. Charts on solid surfaces.

## 5. SwiftUI (iOS 26+ / macOS 26+)

Use native APIs — never fake glass with blur on these OS versions.
```swift
Text("Label").padding().glassEffect()                                 // capsule, .regular
Image(systemName: "heart").padding().glassEffect(.regular.tint(.blue).interactive(), in: .rect(cornerRadius: 16))
GlassEffectContainer(spacing: 30) { /* sibling glass controls; enables morphing */ }
Button("Go") { }.buttonStyle(.glass)          // .glassProminent for the primary action
.backgroundExtensionEffect()                   // content extends under sidebar/toolbar
.tabBarMinimizeBehavior(.onScrollDown)
```
- Glass only on navigation/controls; `.clear` only over bold media; `.identity` to switch glass off.
- Remove old custom backgrounds on toolbars/tab bars/sheets — the system applies glass.
- Details: `references/swiftui/overview.md` → `api-reference.md`, `migration-guide.md` (5-phase), `pitfalls.md`, `platform-specifics.md`, `landmarks-patterns.md`, `ios-ipados-surfaces.md`. Check Apple's current docs when an API looks uncertain.

## 6. Quality gate (must pass before "done")

1. **Screenshots:** light, dark and 390 px mobile (Playwright or the browser). Look at them; fix what looks off.
2. **Contrast:** text on glass ≥ 4.5:1 against the brightest AND darkest area behind it. Fix by raising fill alpha or switching to `--media`, not by shrinking blur.
3. **Safari/Firefox:** frosted fallback looks finished (no layout depending on refraction).
4. **Accessibility:** reduced transparency → solid surfaces; reduced motion → no animation; `:focus-visible` rings; 44 px targets; semantic HTML and labels on icon buttons.
5. **Restraint pass:** one accent; glass only on chrome; no glass-on-glass; gradient text ≤ 1; removed at least one effect since the first draft.
6. **Surface budget:** utility screen is calm; flagship page has at least one scroll-linked scene.
7. **No console errors;** no horizontal scroll at 390 px.

## 7. References (read only the section you need)

Files are long. `grep -n "^## " file` first, then read the one section. Old skill names inside files (apple-design-*) map to the files below.

| File | Read when |
|---|---|
| `01-restraint-and-antislop.md` | Before any "make it premium/Apple" work; slop traps; surface budget |
| `02-materials-liquid-glass.md` | Glass recipes, living backdrops, dark chrome glass, fidelity limits |
| `03-glass-tokens-design-md.md` | Compact Apple glass token sheet (DESIGN.md format) |
| `04-color.md` · `05-typography.md` · `06-layout-grid-spacing.md` | Palettes & semantic colour · type scale & tracking · grids, breakpoints, adaptive layout |
| `07-component-anatomy.md` | Nav bars, lists, forms, buttons, alerts, search, empty states; multi-step flows |
| `08-states-loading-empty-error.md` | Skeletons, optimistic UI, empty/error/disabled states |
| `09-motion.md` · `10-microinteractions.md` | Springs, choreography, FLIP, scroll-progress · button/toggle/loading feedback |
| `11-accessibility.md` | WCAG 2.2 AA, Dynamic Type reflow, reduce transparency/motion |
| `12-landing-page-applecom.md` · `13-scrollytelling.md` | apple.com page formula, nav scroll states · pinned/scrubbed scenes |
| `14-bento-grid.md` | Bento stat cards: tokens, zero-gap grid, templates, dark theme |
| `swiftui/*` | Native Liquid Glass (section 5) |

**If `references/` or `assets/` is missing** (e.g. this skill was loaded from an account copy): `git clone --depth 1 https://github.com/bkhoi0311/liquid-glass-design` and read `plugins/liquid-glass-design/skills/liquid-glass-design/`.

Sources (MIT): deepika-builds/liquid-glass, haider-nawaz/liquid-glass-skill, s1gmamale1/apple-design-skills, hubeiqiao/apple-bento-grid, rohitg00/awesome-claude-design.
