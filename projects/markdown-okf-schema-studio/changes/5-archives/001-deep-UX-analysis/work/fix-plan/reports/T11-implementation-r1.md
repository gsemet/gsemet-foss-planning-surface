# T11 implementation — round 1

STATUS: DONE

## Summary
Added the pure module `continueOnEnter`, runtime wiring (`applyTextEdit`, plain-Enter branch in the
block textarea keydown), unit tests, RI-T11, the `capture.py` changes and the README sentence. Enter
now continues lists (bullets, numbers, tasks), quotes and indentation, exits on an empty item, stays
native inside the marker, in plain text and with Shift+Enter. All gates pass.

## Files changed (under )
- src/webview/textEditing.ts (new)
- src/webview/scrollSync.ts — import, injection, `applyTextEdit`, Enter branch
- test/webview/textEditing.test.ts (new), test/webview/scrollSync.test.ts (2 new tests + setup line below)
- test/visual/capture.py — `check_nested_list_typing`, and one check in `check_preview_edit_mode` (amendment 2)
- test/integration/realInput.test.ts — RI-T11 `scenarioEnterContinuesList`, registered in `run`
- README.md — one sentence in the Edit mode paragraph

## Tests written first (failing before the fix)
- "Enter in a list item continues the list, and Shift+Enter stays native" — `0 !== 1` (prevented count)
- "Enter on an empty list item empties the line and Enter in plain text stays native" — failed likewise
- RI-T11 was written after the wiring and not run red.

## Tests added or changed
- textEditing.test.ts: 21 table cases plus the non-collapsed selection case.
- scrollSync.test.ts: the two tests above.
- RI-T11: nested list, click "Refrigerated goods", caretToEnd, Enter, type "Frozen goods", click the
  heading; asserts the buffer has `    - Frozen goods` as a sibling and `  - Deduplication` unchanged.

## Existing assertions changed
- scrollSync.test.ts "active Markdown editors leave repeated spaces and Enter to native text input" —
  setup line only: added `textarea.setSelectionRange(0, 0);` with a comment before the key loop; all
  assertions unchanged — required by: D-03 (the editor opens with the caret at the end of a list line,
  where Enter now continues the list). Amendment 1.
- capture.py `check_nested_list_typing` — old: Enter then typing ``  - `new-skill` `` expecting `"\n"`;
  new: Enter, assert text equals previous + `"\n  - "`, then type `` `new-skill` `` and assert the final
  text — required by: list continuation. Also added `page.wait_for_timeout(600)` before reading the
  autosave message (autosave is debounced at 400 ms since T09).
- capture.py `check_preview_edit_mode` — old: immediate `page.evaluate` of the "wrapped table-cell edit
  did not autosave" predicate; new: `page.wait_for_function` on the same predicate with `timeout=2000`,
  same failure on `PlaywrightTimeoutError` (new import) — required by: the 400 ms autosave debounce
  from T09. Amendment 2.

## Verification
- `gate.sh T11-impl unit types` → PASS (logs/T11-impl-unit.log, logs/T11-impl-types.log)
- `gate.sh T11-impl trusted` → PASS incl. RI-T11 (logs/T11-impl-trusted.log); screen was not locked
- `gate.sh T11-impl unit visual` (final run) → unit PASS; visual PASS vs baseline, 0 new failure lines
  (logs/T11-impl-visual.log)

## Evidence for reviewers
- RI-T11 screenshot `17-enter-continues-list` (listed in the trusted log).

## Open points / STOP reason
None. Note: `capture.py` was edited after the last `trusted` run, but `trusted` does not use it.
