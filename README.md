# Liquid Glass Design (v2.2)

One Claude Code skill for Apple-style Liquid Glass interfaces — web (HTML, React, Next.js, Vite, Tailwind; deploys to Vercel/Netlify as static assets) and native SwiftUI (iOS 26+ / macOS 26+). It is written to be the **default design system** for every UI request, except ClassIn-branded work.

## What is inside

```
plugins/liquid-glass-design/skills/liquid-glass-design/
  SKILL.md              rules, workflow, quality gate, kit reference, SwiftUI APIs
  assets/tokens.css     tokens (light/dark) + components: glass, nav, buttons, toolbar,
                        segmented, card, grouped list, sheet, tab bar, backdrop, reveal
  assets/liquid-glass.js real edge refraction (Chromium) + frosted fallback
  assets/starter.html   landing starter: split hero, proof row, pricing, testimonial, CTA
  assets/dashboard-starter.html  dashboard starter: KPIs, CSS bar chart, alerts, table→cards
  scripts/qa.py         one-command quality gate (contrast, clipping, JS errors, screenshots)
  assets/LiquidGlass.tsx React / Next.js wrapper
  references/           14 web topics + 7 SwiftUI files, read on demand only
```

v1 shipped 27 separate skills (13 + 14 HIG). v2 merges them into one and drops what does not serve UI work: backend/CDN analysis, marketing tactics, macOS/visionOS/watchOS notes, gestures, SF Symbols, design history, the 14 HIG skills and demo images.

## Blind benchmark (28/09/2026)

Same brief (EdTech landing + school dashboard), each skill built in an isolated session, 2 blind judges per page, 7 criteria.

| Version | Accessibility errors (axe, both pages) | Build time | Landing (round 3, 4-way) |
|---|---|---|---|
| v1/v2.0 | 19 (contrast) | 12.4 min · 208k tokens | 49.0 / 70 (4th) |
| v2.1 | 1 | 6.8 min · 175k tokens | 54.5 / 70 (2nd) |
| **v2.2** | **2 (0 contrast)** | **5.9 min · 159k tokens** | **58.5 / 70 (1st, both judges)** |
| design-taste-frontend | 7 | 8.3 min · 177k tokens | 52.5 / 70 (3rd) |

Dashboard scores varied ±6 points between rounds for identical pages (judge noise); v2.2 dashboard fixes after round 3 are not re-measured.

## Quality gate

```bash
./scripts/qa.sh page.html [more.html]      # uses .venv (Playwright + Chromium); falls back to python3
```

## Install

**All projects on your Mac (user scope)**
```
/plugin marketplace add bkhoi0311/liquid-glass-design
/plugin install liquid-glass-design@liquid-glass-design
```
Or `./scripts/install-global.sh` (symlink into `~/.claude/skills`). Use one route, not both.

**Inside one project (local + Claude Code on the web + GitHub Actions)**
```bash
~/Developer/liquid-glass-design/scripts/add-to-project.sh /path/to/project            # copy skill + web assets
~/Developer/liquid-glass-design/scripts/add-to-project.sh /path/to/project --mode both # also register the plugin in .claude/settings.json
git add .claude public/liquid-glass.js && git commit -m "Add Liquid Glass Design"
```
Web assets are copied only when `package.json` exists: `public/liquid-glass.js` and `app/liquid-glass.css` (or `src/styles/liquid-glass.css`).

**Vercel:** does not run Claude Code. Commit the generated code and `public/liquid-glass.js`; they ship as static files.

## Prompts

- "Làm landing page cho sản phẩm X" — the skill applies by default
- "Migrate this SwiftUI app to Liquid Glass"
- "Tạo bento grid tổng kết Q3"
- ClassIn work → `design-classin-2026` takes over

## Licenses

MIT sources, notices in `licenses/`: deepika-builds/liquid-glass, haider-nawaz/liquid-glass-skill (MIT per README, no LICENSE file), s1gmamale1/apple-design-skills, hubeiqiao/apple-bento-grid, rohitg00/awesome-claude-design.
