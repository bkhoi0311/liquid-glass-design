#!/usr/bin/env bash
# Add Liquid Glass Design to a project so Claude Code picks it up
# locally AND in cloud sessions (Claude Code on the web, GitHub Actions, teammates).
#
# Usage:
#   add-to-project.sh [PROJECT_DIR] [--mode vendor|plugin|both] [--no-assets]
#
#   vendor (default) : copy skills into PROJECT/.claude/skills. Works everywhere,
#                      including cloud sandboxes that cannot reach a private GitHub repo.
#   plugin           : register the GitHub marketplace in PROJECT/.claude/settings.json
#                      (needs access to github.com/bkhoi0311/liquid-glass-design).
#   both             : both of the above.
#   --no-assets      : do not copy liquid-glass.js / tokens.css into the web project.
set -euo pipefail

REPO="bkhoi0311/liquid-glass-design"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CORE="$ROOT/plugins/liquid-glass-design/skills"

PROJECT="."; MODE="vendor"; ASSETS=1
while [ $# -gt 0 ]; do
  case "$1" in
    --mode) MODE="$2"; shift 2 ;;
    --no-assets) ASSETS=0; shift ;;
    -h|--help) sed -n 2,14p "$0"; exit 0 ;;
    *) PROJECT="$1"; shift ;;
  esac
done
PROJECT="$(cd "$PROJECT" && pwd)"
echo "Project: $PROJECT  (mode=$MODE assets=$ASSETS)"

vendor() {
  mkdir -p "$PROJECT/.claude/skills"
  for s in liquid-glass-design; do
    src="$CORE/$s"
    rm -rf "$PROJECT/.claude/skills/$s"
    cp -R "$src" "$PROJECT/.claude/skills/$s"
    echo "  skill  -> .claude/skills/$s"
  done
}

plugin() {
  mkdir -p "$PROJECT/.claude"
  f="$PROJECT/.claude/settings.json"
  [ -f "$f" ] || echo '{}' > "$f"
  python3 - "$f" "$REPO" <<'PY'
import json, sys
path, repo = sys.argv[1], sys.argv[2]
with open(path) as fh:
    data = json.load(fh)
data.setdefault("extraKnownMarketplaces", {})["liquid-glass-design"] = {
    "source": {"source": "github", "repo": repo}
}
data.setdefault("enabledPlugins", {})["liquid-glass-design@liquid-glass-design"] = True
with open(path, "w") as fh:
    json.dump(data, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
PY
  echo "  config -> .claude/settings.json (marketplace + enabledPlugins)"
}

assets() {
  [ -f "$PROJECT/package.json" ] || { echo "  (no package.json: web assets skipped)"; return 0; }
  mkdir -p "$PROJECT/public"
  cp "$CORE/liquid-glass-design/assets/liquid-glass.js" "$PROJECT/public/liquid-glass.js"
  echo "  asset  -> public/liquid-glass.js"
  target="$PROJECT/src/styles"; [ -d "$PROJECT/app" ] && target="$PROJECT/app"
  mkdir -p "$target"
  cp "$CORE/liquid-glass-design/assets/tokens.css" "$target/liquid-glass.css"
  echo "  asset  -> ${target#$PROJECT/}/liquid-glass.css (import once in the root layout)"
}

case "$MODE" in
  vendor) vendor ;;
  plugin) plugin ;;
  both) vendor; plugin ;;
  *) echo "unknown --mode $MODE" >&2; exit 1 ;;
esac
if [ "$ASSETS" = 1 ]; then assets; fi

echo
echo "Done. Commit so cloud sessions and Vercel builds get it:"
echo "  git add .claude public/liquid-glass.js && git commit -m 'Add Liquid Glass Design'"
