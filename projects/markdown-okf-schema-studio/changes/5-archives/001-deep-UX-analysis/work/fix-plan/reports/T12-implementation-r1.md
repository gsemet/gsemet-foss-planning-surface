# T12 implementation — round 1

STATUS: DONE

## Summary
Added `indentSelection` to `createTextEditingTools` and wired Tab / Shift+Tab in the block textarea
keydown handler. Tab always calls `preventDefault` (focus never leaves the editor) and applies the
edit through `applyTextEdit`. List lines move by marker plus spacing width, other lines by 4 spaces;
a collapsed caret on a non-list line inserts 4 spaces at the caret. Escape still closes the editor,
and the next Tab then moves focus natively. README sentence added.

## Files changed (under )
- src/webview/textEditing.ts — `indentSelection`
- src/webview/scrollSync.ts — Tab branch in the block textarea keydown handler
- test/webview/textEditing.test.ts — 18 indentSelection cases
- test/webview/scrollSync.test.ts — one new Tab test
- test/integration/realInput.test.ts — RI-T12 `scenarioTabIndents`, registered in `run`
- README.md — one sentence in the Edit mode paragraph

## Tests written first (failing before the fix)
- "Tab and Shift+Tab indent the block editor without closing it" (scrollSync, with the Tab branch
  disabled) — `0 !== 1` (preventDefault count)
- RI-T12 (run with the Tab branch disabled, log logs/T12-red-trusted.log) — `AssertionError: Tab keeps
  the focus in the editor` / `'LI' !== 'TEXTAREA'` (native Tab moved focus and committed)
- The pure `indentSelection` unit tests were written after the function, so they were not run red.

## Tests added or changed
- textEditing.test.ts: indent `- a`, `1. a`, `10. a`, multi-line selection, last-line exclusion,
  outdent (list, prose, tab char), nothing to remove -> undefined, caret mid-prose, selection
  preserved, quote prefix.
- scrollSync.test.ts: Tab prevents default, indents, debounced autosave is non-final, Shift+Tab
  restores, outdent with nothing to remove is still prevented, editor element stays.
- RI-T12: click "Refrigerated goods", caretToEnd, Home, Tab -> textarea focused and line gained 2
  spaces; Shift+Tab -> original; Escape, Tab -> focus not in a textarea; buffer unchanged.

## Existing assertions changed
None.

## Verification
- `gate.sh T12-impl unit types trusted` -> PASS (logs/T12-impl-unit.log, -types.log, -trusted.log), incl. RI-T12
- `gate.sh T12-impl visual` -> PASS vs baseline, 0 new failure lines (logs/T12-impl-visual.log)

## Evidence for reviewers
- RI-T12 screenshot `18-tab-indents` (see trusted log).

## Open points / STOP reason
None. Note: the trusted run preceded two unit-test-only edits (expectation fixes in
textEditing.test.ts and scrollSync.test.ts); source files were unchanged after it.
