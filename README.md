# Liquid Glass Design

Apple-style Liquid Glass skills for Claude Code — one bundle for web (HTML, React, Next.js, Vite; deploys to Vercel/Netlify as static assets) and native SwiftUI (iOS 26+ / macOS 26+).

## What is inside

**Plugin `liquid-glass-design`** (core, 13 skills)

| Skill | Use for | Source (MIT) |
|---|---|---|
| `liquid-glass-design` | Hub: routes by platform, shared tokens, a11y rules, React wrapper | this repo + rohitg00/awesome-claude-design |
| `liquid-glass-web` | Real refraction for the web (`liquid-glass.js`, SVG displacement) + frosted fallback | deepika-builds/liquid-glass |
| `liquid-glass-swiftui` | `.glassEffect()`, `GlassEffectContainer`, migration guide, pitfalls | haider-nawaz/liquid-glass-skill |
| `apple-design` + 8 `apple-design-*` | HIG philosophy, foundations, materials, motion, OS surfaces, apple.com pages, a11y/marketing | s1gmamale1/apple-design-skills |
| `apple-bento-grid` | Apple-style bento stat cards (HTML + PNG) | hubeiqiao/apple-bento-grid |

**Plugin `apple-hig`** (optional, 14 `hig-*` skills) — full Human Interface Guidelines lookups, from raintree-technology/hig-doctor.

## Install

### 1. On your Mac, all projects (user scope)

```bash
# inside Claude Code
/plugin marketplace add bkhoi0311/liquid-glass-design
/plugin install liquid-glass-design@liquid-glass-design
/plugin install apple-hig@liquid-glass-design      # optional
```

Or without the plugin system: `./scripts/install-global.sh` (symlinks into `~/.claude/skills`, `git pull` updates them).

### 2. Inside one project (works locally AND in the cloud)

```bash
~/Developer/liquid-glass-design/scripts/add-to-project.sh /path/to/project            # vendor core 4 skills + web assets
~/Developer/liquid-glass-design/scripts/add-to-project.sh /path/to/project --full     # all skills
~/Developer/liquid-glass-design/scripts/add-to-project.sh /path/to/project --mode both
git add .claude public/liquid-glass.js && git commit -m "Add Liquid Glass Design"
```

| Mode | What it writes | Works in |
|---|---|---|
| `vendor` (default) | `.claude/skills/<skill>/` copied into the repo | Local, Claude Code on the web, GitHub Actions, teammates — no extra access needed |
| `plugin` | `.claude/settings.json` → `extraKnownMarketplaces` + `enabledPlugins` | Anywhere Claude Code can reach this GitHub repo (keep the repo public, or grant access) |

Web assets (only if `package.json` exists): `public/liquid-glass.js` and `app/liquid-glass.css` (or `src/styles/liquid-glass.css`). Vercel serves them as static files; no env vars.

### 3. Vercel / GitHub notes

- Vercel does not run Claude Code; what matters there is that the generated code and `public/liquid-glass.js` are committed. The `.claude/` folder is ignored by the build.
- GitHub Actions (`anthropics/claude-code-action`) and Claude Code on the web read `.claude/skills` and `.claude/settings.json` from the checked-out repo, so the vendor mode is the safe default.

## Usage prompts

- "Dùng liquid-glass-design, làm navbar + hero card kiểu iOS 26 cho trang Next.js này"
- "Migrate this SwiftUI app to Liquid Glass"
- "Tạo bento grid tổng kết Q3 theo phong cách Apple"

## Licenses

All sources are MIT; notices in `licenses/`. `haider-nawaz/liquid-glass-skill` states MIT in its README but ships no LICENSE file.
