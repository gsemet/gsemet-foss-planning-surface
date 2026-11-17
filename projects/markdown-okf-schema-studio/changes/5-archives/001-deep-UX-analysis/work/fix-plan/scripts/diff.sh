#!/usr/bin/env bash
# Prints the fix-plan diff since <base>, restricted to the extension and AGENTS.md, including
# untracked files. Usage: diff.sh <base-sha> [--stat]
set -uo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <base-sha> [--stat]" >&2
  exit 2
fi

PLAN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$(git -C "$PLAN_DIR" rev-parse --show-toplevel)"
BASE="$1"
cd "$ROOT" || exit 2

PATHS=(src/markdown-okf-schema-studio AGENTS.md)

if [[ "${2:-}" == "--stat" ]]; then
  git diff --stat "$BASE" -- "${PATHS[@]}"
else
  git diff "$BASE" -- "${PATHS[@]}"
fi

untracked=$(git ls-files --others --exclude-standard -- "${PATHS[@]}")
if [[ -n "$untracked" ]]; then
  echo
  echo "### Untracked files (new in this task)"
  while IFS= read -r file; do
    echo
    echo "=== $file"
    if [[ "${2:-}" != "--stat" ]]; then
      cat "$file"
    fi
  done <<<"$untracked"
fi
