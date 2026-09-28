---
name: liquid-glass-design
description: Hub for Apple-style Liquid Glass UI on any stack. Use when the user asks for liquid glass, iOS 26 / macOS Tahoe glass, glassmorphism, frosted or translucent surfaces, vibrancy, "make it look like Apple", or a glass nav/card/modal/button/tab bar — on the web (HTML, React, Next.js, Vite, Tailwind, deployed to Vercel/Netlify) or in SwiftUI/UIKit. Decides the platform, applies the shared tokens and rules below, then routes to liquid-glass-web, liquid-glass-swiftui or the apple-design-* skills.
---

# Liquid Glass Design (hub)

One entry point for glass UI. Read this first, then load exactly one implementation skill.

## 1. Route by platform

| Target | Load | Why |
|---|---|---|
| Swift / SwiftUI / UIKit, iOS 26+, macOS 26+ | `liquid-glass-swiftui` | Native `.glassEffect()`, `GlassEffectContainer`, `.buttonStyle(.glass)`. Never fake glass with blur on these OS versions. |
| Web (HTML, React, Next.js, Vite, Astro, Vue) | `liquid-glass-web` | Real SVG-displacement refraction (Chromium) + frosted fallback (Safari/Firefox). Module: `templates/liquid-glass.js`. |
| Apple.com-style landing / marketing page | `apple-design-web` + this hub | Page formula, scroll storytelling; glass only on nav and floating chrome. |
| Colors, type, spacing decisions | `apple-design-foundations` | |
| Materials, vibrancy, app icon squircle, SF Symbols | `apple-design-materials` | |
| Springs, transitions, gestures | `apple-design-motion` | |
| Stats / timeline cards, one-page project summary | `apple-bento-grid` | |
| Full HIG lookups (if the `apple-hig` plugin is enabled) | `hig-*` skills | |

If the stack is unclear and the repo is available, detect it (`package.json` → web; `*.xcodeproj` / `Package.swift` → SwiftUI) instead of asking.

## 2. Where glass belongs (the rule most builds get wrong)

- Glass is a **navigation / control layer that floats above content**: nav bars, tab bars, toolbars, sidebars, sheets, popovers, floating buttons, small cards over imagery.
- Content itself (article body, tables, forms, long lists) sits on **solid** surfaces. Glass-on-glass stacks and full-page glass backgrounds are wrong.
- Glass needs something behind it. Over a flat white page it is invisible — put it over imagery, gradients or scrolling content.
- One tint per surface, used for the primary action only.

## 3. Shared web tokens

Copy `templates/tokens.css` into the project (e.g. `app/glass.css` or `src/styles/glass.css`). It defines:

- Apple system colors, light/dark (`--lg-*`), from `references/apple-glass-design-md.md`.
- Materials: `--lg-material-thin | regular | thick` (alpha fills) + `--lg-blur: 30px`, `--lg-saturate: 180%`.
- Classes: `.lg-surface` (frosted, all browsers), `.lg-refract` (add when using `liquid-glass.js`), `.lg-button`, `.lg-nav`.
- Accessibility fallbacks for `prefers-reduced-transparency`, `prefers-contrast: more`, `prefers-reduced-motion`.

React/Next.js: use `templates/LiquidGlass.tsx` (client component, loads the module once, calls `destroy()` on unmount).

## 4. Non-negotiables (check before you say "done")

1. Text contrast inside glass ≥ 4.5:1 against the worst-case background (test over the brightest and darkest area behind it). Raise tint alpha before reducing blur.
2. Reduced transparency → opaque surface (`--lg-material-thick` without blur). Already in `tokens.css`; do not remove.
3. Refraction is decoration only (Chromium). Nothing may depend on it; Safari/Firefox must look finished with the frosted fallback.
4. No drop shadow on the glass *material* itself over busy content, no 1px hard borders on cards — use the inset highlight recipe.
5. Refraction elements ≤ ~800 px per side; do not animate size every frame (map regenerates on resize).
6. Touch targets ≥ 44 px; font stack `-apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui` (do not ship SF Pro webfont files — Apple's license does not allow web embedding).
7. Next.js/SSR: glass JS runs client-side only (`"use client"`, inside `useEffect`).

## 5. Deploying (Vercel / Netlify / GitHub Pages)

Nothing special on the host side: `liquid-glass.js` and `tokens.css` ship as normal static assets inside the build (`public/` for Next.js/Vite). No server code, no env vars. Check the deployed page in Safari as well as Chrome, because the two render different paths.

## References

- `references/apple-glass-design-md.md` — Apple glass/soft-futurism DESIGN.md (tokens, components, do/don't).
- `references/arc-glass-design-md.md` — alternative glass direction (Arc browser style) for non-Apple brands.
- `templates/tokens.css`, `templates/LiquidGlass.tsx`, `templates/liquid-glass.js`.
