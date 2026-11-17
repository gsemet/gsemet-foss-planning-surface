# T21 implementation — round 1

STATUS: DONE

## Summary
In edit mode a plain click on an okf link in a properties value cell now opens that field's editor
(capture-phase document click listener, registered before `installLinkNavigation`); Cmd/Ctrl+click
and reading mode still navigate. In list editor items, Enter inserts an empty item after the current
one and focuses it; Enter on an empty last item removes it and saves; Backspace in an empty item
removes it and focuses the previous input (caret at end), else the next, else "+ Add item"; Cmd/Ctrl+Enter
saves. Focus moves before the row is removed, so the editor `focusout` save never fires.
`linkNavigation.ts` is untouched.

## Files changed
- src/webview/scrollSync.ts — capture click listener; `focusNeighbour`; item `keydown`; `appendItem` returns its row
- test/webview/scrollSync.test.ts — fake `closest` supports the two okf-link selectors; 8 new T21 tests
- test/integration/realInput.test.ts — RI-T21 scenario
- README.md — two sentences in the Edit mode paragraph

## Tests written first (failing before the fix)
- T21: in edit mode a plain click on an okf link opens the field editor and does not navigate — `0 !== 1` (editor count)
- T21: Enter in a list item inserts an empty item after it... — deepEqual: expected `''` between `one` and `two` missing
- T21: Enter in an empty last list item removes it and saves the list — `TypeError: Cannot set properties of undefined (setting 'value')`
- T21: Backspace in an empty middle item / first item / only item (3 tests) failed likewise (row not removed)
- T21: Cmd or Ctrl+Enter saves the list — failed (no save)
- (Cmd/Ctrl click and reading-mode tests pass before and after by design: they pin unchanged behaviour.)
- RI-T21 on unmodified code (log logs/T21-impl-pre-trusted.log): `Error: Timed out waiting for the editor matching [data-okf-frontmatter-editor] .okf-list-editor.` after the plain click on `StRS-A` (it navigated instead).

## Tests added or changed
- 9 unit tests prefixed "T21:" in scrollSync.test.ts (click edit / Cmd+Ctrl navigate / reading mode navigate; Enter inserts after and focuses without save; Enter on empty last saves without it; Backspace middle/first/only; Backspace non-empty untouched; Cmd/Ctrl+Enter saves; composing/Shift ignored).
- RI-T21 (real mouse and keyboard): plain click opens the list editor with `documentUri` unchanged; End, Enter, type `StRS-B`, Enter, Enter saves; buffer delta is exactly `+ - StRS-B`; Cmd/Ctrl+click makes `StRS-A.md` the active text editor.

## Existing assertions changed
- none. (Only the fake DOM `closest` gained two selectors; no assertion touched.)

## Verification
- `gate.sh T21-impl unit types trusted visual` → unit PASS, types PASS, trusted PASS, visual PASS vs baseline (0 new failure lines, 4 baseline lines now passing) — logs/T21-impl-*.log, screenshots logs/visual-T21-impl

## Evidence for reviewers
- RI-T21 evidence frames `27-list-click-edits` and `28-list-enter-adds` are in the real-input evidence folder written by the trusted run.

## Feedback addressed (rounds 2–3)
- n/a

## Open points / STOP reason
- One small addition beyond the task text: the click interception also requires `data-okf-editable="true"` on the row and ignores the name cell, so a non-editable row's link keeps navigating instead of becoming a dead click.
- Enter on a focused link in edit mode still navigates (linkNavigation keydown); the task only specified click.
