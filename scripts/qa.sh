#!/usr/bin/env bash
# Run the Liquid Glass quality gate with the repo's own Python env (Playwright + Chromium).
# Usage: ~/Developer/liquid-glass-design/scripts/qa.sh page.html [more.html] [--out DIR]
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$ROOT/.venv/bin/python"; [ -x "$PY" ] || PY=python3
exec "$PY" "$ROOT/plugins/liquid-glass-design/skills/liquid-glass-design/scripts/qa.py" "$@"
