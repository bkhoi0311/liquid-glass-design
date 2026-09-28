# Liquid Glass Design

One Claude Code skill for Apple-style Liquid Glass interfaces — web (HTML, React, Next.js, Vite, Tailwind; deploys to Vercel/Netlify as static assets) and native SwiftUI (iOS 26+ / macOS 26+). It is written to be the **default design system** for every UI request, except ClassIn-branded work.

## What is inside (v2 — merged)

```
plugins/liquid-glass-design/skills/liquid-glass-design/
  SKILL.md              rules, workflow, quality gate, kit reference, SwiftUI APIs
  assets/tokens.css     tokens (light/dark) + components: glass, nav, buttons, toolbar,
                        segmented, card, grouped list, sheet, tab bar, backdrop, reveal
  assets/liquid-glass.js real edge refraction (Chromium) + frosted fallback
  assets/starter.html   reviewed reference page (light, dark, mobile)
  assets/LiquidGlass.tsx React / Next.js wrapper
  references/           14 web topics + 7 SwiftUI files, read on demand only
```

v1 shipped 27 separate skills (13 + 14 HIG). v2 merges them into one and drops what does not serve UI work: backend/CDN analysis, marketing tactics, macOS/visionOS/watchOS notes, gestures, SF Symbols, design history, the 14 HIG skills and demo images.

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
