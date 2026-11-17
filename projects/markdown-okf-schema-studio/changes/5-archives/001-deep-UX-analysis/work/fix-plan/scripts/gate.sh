#!/usr/bin/env bash
# Runs test gates for the Markdown OKF-Schema Studio fix plan and writes one log per level.
#
# Usage: gate.sh <label> <level> [<level>...]
#   label   free text used in log names, e.g. T04, T04-impl, T04-review, PHASE2
#   levels  unit | types | contracts | trusted | scroll | reload | full | visual
#           (visual compares with logs/visual-baseline-failures.txt and restores the tracked
#           screenshots folder; see visual_level below)
#
# Prints one summary line per level and exits non-zero if any level failed.
set -uo pipefail
export LC_ALL=C  # sort and comm must agree on the order of the visual failure lists

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <label> <level> [<level>...]" >&2
  exit 2
fi

PLAN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$(git -C "$PLAN_DIR" rev-parse --show-toplevel)"
EXT="$ROOT/src/markdown-okf-schema-studio"
LABEL="$1"
shift
mkdir -p "$PLAN_DIR/logs"

# The VS Code test host refuses to start when it inherits the variables of a running VS Code
# ("Code: bad option: --user-data-dir"), so strip them for every level.
for name in $(env | awk -F= '/^(VSCODE|ELECTRON)_/ { print $1 }'); do
  unset "$name"
done

if ! command -v fnm >/dev/null 2>&1; then
  echo "fnm is not on PATH; cannot select the pinned Node version" >&2
  exit 2
fi

status=0

run() {
  local name="$1"
  shift
  local log="$PLAN_DIR/logs/$LABEL-$name.log"
  local start
  start=$(date +%s)
  (cd "$EXT" && "$@") >"$log" 2>&1
  local code=$?
  local duration=$(( $(date +%s) - start ))
  local verdict="PASS"
  [[ $code -ne 0 ]] && verdict="FAIL"
  echo "$name: $verdict (exit $code, ${duration}s) log=$log"
  [[ $code -ne 0 ]] && status=1
  return $code
}

# The visual capture (test/visual/capture.py) writes into the tracked folder test/visual/screenshots.
# The gate keeps a copy of each run in logs/visual-<label>/ and puts the tracked folder back, so a
# task never carries regenerated screenshots. HEAD already fails some visual checks (recorded by
# T00 in logs/visual-baseline-failures.txt), so the level fails only on failures that are not in
# that baseline.
SHOTS="$EXT/test/visual/screenshots"
VISUAL_BASELINE="$PLAN_DIR/logs/visual-baseline-failures.txt"

visual_signature() {
  # One line per failing scenario and per failing rendering check, without duplicates.
  awk '/^failed: / || /^  [^ ]+\.html: /' "$1" | sort -u
}

restore_shots() {
  git -C "$ROOT" restore -- "$SHOTS"
  git -C "$ROOT" ls-files --others --exclude-standard -- "$SHOTS" | while IFS= read -r file; do
    rm -f "$ROOT/$file"
  done
}

visual_level() {
  local log="$PLAN_DIR/logs/$LABEL-visual.log"
  local keep="$PLAN_DIR/logs/visual-$LABEL"
  local current="$PLAN_DIR/logs/$LABEL-visual-failures.txt"
  if [[ -n "$(git -C "$ROOT" status --porcelain -- "$SHOTS")" ]]; then
    echo "visual: FAIL (test/visual/screenshots has uncommitted changes before the run; not overwriting them)"
    status=1
    return 1
  fi
  local start code duration
  start=$(date +%s)
  (cd "$EXT" && fnm exec -- npm run test:visual) >"$log" 2>&1
  code=$?
  duration=$(( $(date +%s) - start ))
  rm -rf "$keep"
  mkdir -p "$keep"
  cp -R "$SHOTS/." "$keep/"
  restore_shots
  visual_signature "$log" >"$current"
  if ! awk '/^(passed|failed): /{found=1} END{exit !found}' "$log"; then
    echo "visual: FAIL (exit $code, ${duration}s; the capture did not run any scenario) log=$log"
    status=1
    return 1
  fi
  if [[ ! -f "$VISUAL_BASELINE" ]]; then
    local verdict="PASS"
    [[ $code -ne 0 ]] && verdict="FAIL" && status=1
    echo "visual: $verdict (exit $code, ${duration}s; no baseline file) log=$log screenshots=$keep"
    return 0
  fi
  # Some failure messages embed measured coordinates, which move by sub-pixel amounts whenever the
  # layout above them changes. Compare with every number replaced by "#", as a multiset (no -u), so
  # a known failure whose coordinates moved stays known, while one more occurrence of a message, or
  # a new message or page, is still new. Exact-text drift is reported separately.
  local norm_base norm_current new fixed shifted
  norm_base="$PLAN_DIR/logs/$LABEL-visual-baseline-normalized.txt"
  norm_current="$PLAN_DIR/logs/$LABEL-visual-failures-normalized.txt"
  sed -E 's/[0-9]+(\.[0-9]+)?/#/g' "$VISUAL_BASELINE" | sort >"$norm_base"
  sed -E 's/[0-9]+(\.[0-9]+)?/#/g' "$current" | sort >"$norm_current"
  rm -f "$PLAN_DIR/logs/$LABEL-visual-new-failures.txt"
  new=$(comm -13 "$norm_base" "$norm_current" | awk 'END{print NR}')
  fixed=$(comm -23 "$norm_base" "$norm_current" | awk 'END{print NR}')
  shifted=$(comm -13 "$VISUAL_BASELINE" "$current" | awk 'END{print NR}')
  shifted=$(( shifted - new ))
  if [[ $new -gt 0 ]]; then
    comm -13 "$norm_base" "$norm_current" >"$PLAN_DIR/logs/$LABEL-visual-new-failures.txt"
    echo "visual: FAIL ($new new failure line(s) vs baseline, $fixed baseline line(s) now passing, exit $code, ${duration}s) new=$PLAN_DIR/logs/$LABEL-visual-new-failures.txt log=$log screenshots=$keep"
    status=1
    return 1
  fi
  echo "visual: PASS vs baseline (0 new failure lines, $fixed baseline line(s) now passing, $shifted known line(s) with moved coordinates, exit $code, ${duration}s) log=$log screenshots=$keep"
}

for level in "$@"; do
  case "$level" in
    unit)
      run compile fnm exec -- npm run compile && run unit fnm exec -- npm run test:unit
      ;;
    types)
      run types fnm exec -- npm run check-types
      ;;
    contracts)
      run contracts-compile fnm exec -- npm run compile && run contracts fnm exec -- npm run test:contracts
      ;;
    trusted)
      run trusted-build fnm exec -- bash -c 'npm run compile && npm run bundle' \
        && run trusted fnm exec -- node out/test/integration/run-tests.js --trusted-only
      ;;
    scroll)
      run scroll fnm exec -- npm run test:scroll
      ;;
    reload)
      run reload fnm exec -- npm run test:reload
      ;;
    full)
      run full fnm exec -- npm run test:integration
      ;;
    visual)
      visual_level
      ;;
    *)
      echo "unknown level: $level" >&2
      status=1
      ;;
  esac
done

exit $status
