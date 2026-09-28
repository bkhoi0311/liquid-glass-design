#!/usr/bin/env bash
# Symlink every Liquid Glass Design skill into ~/.claude/skills (user scope, all projects).
# Use this OR the /plugin install route, not both (duplicate skill names).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
T="$HOME/.claude/skills"; mkdir -p "$T"
for d in "$ROOT"/plugins/*/skills/*/; do
  n="$(basename "$d")"
  if [ -e "$T/$n" ] || [ -L "$T/$n" ]; then echo "  skip (exists): $n"; else ln -s "${d%/}" "$T/$n"; echo "  linked: $n"; fi
done
echo "Done. Restart Claude Code."
