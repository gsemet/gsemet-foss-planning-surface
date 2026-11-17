# T12 review — round 1

Base: e4d9e7c · Reviewed diff: 6 files, ~+260/-2 (README, scrollSync.ts, textEditing.ts, 3 test files)

## Gates
compile: PASS · unit: PASS (logs/T12-unit.log, 0 `not ok`) · types: PASS · trusted: PASS (logs/T12-trusted.log, exit 0, RI-T12 `18-tab-indents` captured) · visual: PASS, 0 new failure lines vs T00 baseline (logs/T12-visual.log).

## Done-when
- [x] `unit` and `trusted` gates pass; RI-T12 passes — logs above; red run in logs/T12-red-trusted.log (`'LI' !== 'TEXTAREA'`).
- [x] README Edit-mode sentence "Tab and Shift+Tab indent and outdent lines; press Escape to leave the editor." — README.md diff.
- [x] Pure-function spec items 1–6 — textEditing.test.ts `indentSelection …` cases: `- a`→`  - a`, `1. a`→`   1. a`, `10. a`, two-line selection, last-line exclusion (`- a\n[- b\n]`), outdent `    - a`→`  - a`, nothing to remove → undefined, caret mid-prose → 4 spaces at caret, selection preserved, quote prefix `> - a`→`>   - a`, tab-char outdent.
- [x] Runtime wiring: Tab without Meta/Ctrl/Alt always `preventDefault`, edit via `applyTextEdit` + resize + autosave — scrollSync.test.ts "Tab and Shift+Tab indent the block editor without closing it" (prevent count, value, non-final autosave, editor element kept, no-op outdent still prevented).
- [x] Escape then Tab leaves the editor — RI-T12 asserts activeElement not TEXTAREA and buffer unchanged.

## Protected features checked
P-E3: Tab branch placed after `keepUndoInControl`/`navigateBlockEdit`/Enter and before Escape; Escape/blur/Cmd+Enter paths untouched; existing scrollSync tests "raw Markdown block edits autosave…" pass in unit gate.
P-E4: arrow navigation runs before the Tab branch, unchanged; covered by "arrow boundaries transfer block editing…".
P-E5: only one `"Tab"` occurrence in scrollSync.ts, inside the block textarea listener created in `receiveBlockEditSource`; table cell editor keydown untouched (T17 scope).
P-E7: frontmatter controls have no Tab handling added; native Tab preserved.
P-E8: handler only exists on the block editor textarea, which is never created in read-only mode; untrusted suite in trusted gate passes.
P-S2/P-S4: no new message types; no innerHTML.
Conventions §2: scrollSync hunk has no backticks, no `${`, no backslashes, no global setTimeout. Regexes live in textEditing.ts (same injection mechanism as T11's continueOnEnter, already proven).

## Findings
1. [MINOR] test/webview/textEditing.test.ts — pure `indentSelection` tests were written after the function, so not shown red (the runtime and RI-T12 tests were shown red, which covers the interaction bug). No action required.
2. [NIT] textEditing.ts:indentSelection — quote-prefix regex is recomputed for the collapsed-caret branch; harmless.

Reviewed logic by hand: `shift()` correctly moves a caret at the line start with its indentation, clamps a caret inside removed spaces, and keeps multi-line selections; `\n`-only splitting matches the textarea value (browsers normalise to `\n`).
Screenshot `.artifacts/real-input-lqARyZ/18-tab-indents.png`: preview intact, editor on "Refrigerated goods", no clipping or layout shift.

## Existing assertions changed
None (verified in diff: test files only gain new tests).

VERDICT: PASS
