# T20 implementation — round 1

STATUS: STOP

(Code complete; unit, types and trusted pass. Only the `visual` level is not verified, see the end.)

## Summary
One click on a boolean value cell in edit mode now toggles and saves it. `openFrontmatterEditor(row, options)`
takes `{ toggleBoolean: true }`; at its end, for a schema-found checkbox row, it sets `control.checked = value !== true`,
updates the label and calls `saveValue()`. The document click listener passes the option for value cells of
`data-okf-type="checkbox"` rows. The keyboard listener is unchanged (Enter/Space still opens the editor).

## Files changed
- src/webview/scrollSync.ts — option + click wiring (about 9 lines).
- test/webview/scrollSync.test.ts — 3 new tests; opening step of one existing test changed (below).
- test/integration/realInput.test.ts — RI-T20 (`scenarioBooleanOneClick`, registered at the end of `run`).
- test/visual/capture.py — `frontmatter-boolean` opens the editor by keyboard.

## Tests written first (failing before the fix)
- "one click on a boolean value cell toggles and saves it" — `'previewReady' !== 'previewFrontmatterSave'`
- "one click on a true boolean value cell saves false" — `undefined !== false`
- RI-T20 against unmodified source (logs/T20-pre-trusted.log): `Error: Timed out waiting for the toggled boolean to reach the source buffer.`
  (the click only opened the editor; buffer unchanged).
- "clicking a boolean name cell still opens the key editor and reading mode does nothing" — guard test, passes before and after.

## Tests added or changed
- The three unit tests above; RI-T20 (real `page.mouse.click` on the read-mode checkbox centre; asserts buffer
  `annotation_exemption: true` with a one-line delta and no `[data-okf-frontmatter-editor]` after re-render).
  The read-mode checkbox is `aria-disabled`, which Playwright treats as not enabled, hence mouse.click on its bounding box.

## Existing assertions changed
- scrollSync.test.ts: "boolean frontmatter values use a checkbox and save on change" — old: opening `click` on the value cell → new:
  `keydown` Enter on the value cell; all assertions kept. Required by: a click now toggles directly (amended task).
- test/visual/capture.py `frontmatter-boolean` branch — old: `target.click()` → new: `target.focus()` + `page.keyboard.press("Enter")`
  for this target only; all following checks kept. Same reason.

## Verification
- unit → PASS (logs/T20-impl-unit.log)
- types → PASS (logs/T20-impl-types.log)
- trusted → PASS incl. RI-T20 (logs/T20-impl-trusted.log)
- visual → NOT RUN, see below.

## Open points / STOP reason
My first combined gate run was killed (launched while the fix was not yet restored; I ran `pkill`) after its visual step had
started, so `test/visual/screenshots` was left with uncommitted regenerated files. The gate refuses to run visual in that state.
I tried to restore it (`git restore` of that folder plus removing untracked files, what the gate itself does) and the permission
classifier denied it. Please run `git restore -- test/visual/screenshots` (and delete untracked files there),
then `PLAN/scripts/gate.sh T20-impl visual`. Do not commit the screenshot changes. The only visual-relevant edit is capture.py.
