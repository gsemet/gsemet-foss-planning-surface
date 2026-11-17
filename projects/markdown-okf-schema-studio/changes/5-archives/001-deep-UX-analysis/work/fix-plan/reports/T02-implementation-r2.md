# T02 implementation — round 2

STATUS: DONE

## Summary
Round 2 fixes the two MAJOR findings and MINOR 3 and 4 from `reviews/T02-review-r1.md`, and the documentation parts of MINOR 5 and 6 and NIT 7. The commit actions of S1, S4 and S5 are now asserted by a re-render wait (`waitForRender` plus a check of the rendered DOM). The proof step ran each commit action removed in turn, and each removal made its scenario time out at the new wait. The macOS caret keys (`Meta+End` does nothing there) are replaced by `caretToEnd`, and the caret is asserted before typing in S2 and S3. The frame lookup now also matches `data-sphinx-preview-document-id`. While proving, I hit two webview-replacement flakes. Both are fixed in the harness: `setEditMode` now retries its click and its first read, and the detach pattern also matches the CDP "Cannot find context" error. No `src/` file changed. Only the four allowed files changed.

## Files changed
- `test/integration/realInput/harness.ts` — `waitFor` treats a detached-frame error as "not yet" and keeps polling; `findCurrentFrame` returns undefined without a preview and matches `data-sphinx-preview-document-id`; `waitForEditor` moved here and exported; new exports `caretToEnd` and `focusedCaret`; `setEditMode` reads through `withCurrentFrame` and clicks up to three times, each click followed by a 1.5 s wait for the mode; the detach pattern is one shared constant that also matches "cannot find context with specified id"; JSDoc on `withCurrentFrame` (only repeat safe or loud actions), `capture` (call only after the last action, with the side effects listed) and `closeAllEditors` (both facts from MINOR 5).
- `test/integration/realInput.test.ts` — S1, S4 and S5 wait for `waitForRender` after their commit, then assert the rendered DOM (S1: one `p` with `Second paragraph. Added.` and no open block-editor value containing `Second paragraph`; S4: no cell editor and one `td` `one1`; S5: no block editor and one `p` `Second paragraph. Z`). S2 and S3 use `caretToEnd` plus `waitForCaretAtEnd` instead of `${MOD}+End`. The local `waitForEditor` moved to the harness. `waitForNoBlockEditor` and `waitForCaretAtEnd` are new local helpers. The `Frame` type import is gone.
- Not changed: `trusted-suite.ts`, `review-index.ts` (round 1, unchanged this round), `checkboxToggle.test.ts`, `previewEditing.test.ts`, any `src/` file.

## Tests written first (failing before the fix)
The new commit checks were written first and were run with the commit action removed (proof step below). Each one fails at its new wait:
- S1 paragraph blur commit, heading click removed — `Error: Timed out waiting for the preview to render the current document version.` (`logs/T02-proof-s1-trusted.log:302`, scenario `scenarioParagraphBlurCommit`)
- S4 table cell Enter, `press(page, "Enter")` removed — `Error: Timed out waiting for the preview to render the current document version.` (`logs/T02-proof-s4b-trusted.log:323`, scenario `scenarioTableCellEnter`; the first attempt, `logs/T02-proof-s4-trusted.log`, died earlier on the flake described below, so it is not counted)
- S5 Open With Cmd/Ctrl+Enter, `press(page, MOD+Enter)` removed — `Error: Timed out waiting for the preview to render the current document version.` (`logs/T02-debug3-trusted.log:762`, scenario `scenarioOpenWithEditor`; the buffer reached version 3 while the preview stayed at version 1)

Each proof run removed one action only. The suite stops at the first failure, so the three proofs were three separate gate runs. Logs are `logs/T02-proof-s1-trusted.log`, `logs/T02-proof-s4b-trusted.log` and `logs/T02-debug3-trusted.log`. The debug3 run also carried temporary diagnostic `console.log` lines, which are removed (see Verification).

Proof step restore: every removed action was restored before the final gates. `rg -n "PROOF-TEMP|DEBUG-TEMP" test/integration/realInput*` finds nothing.

## Tests added or changed
- S1 `scenarioParagraphBlurCommit` — the rendered paragraph has the committed text and no block editor holds it after blur (MAJOR 1).
- S2 `scenarioCtrlEnterCommit` — the caret is at the end before typing, so ` X` lands after `line two.` on macOS too (MAJOR 2).
- S3 `scenarioArrowNavigation` — same caret check before ArrowDown (MAJOR 2).
- S4 `scenarioTableCellEnter` — the cell editor closes after the re-render and one `td` reads `one1` (MAJOR 1).
- S5 `scenarioOpenWithEditor` — the block editor closes and the paragraph renders `Second paragraph. Z` after Cmd/Ctrl+Enter (MAJOR 1).

## Existing assertions changed
None. No existing assertion in any file was changed. The test names and the assertions of S1–S5 keep their original checks; the new checks are added after them.

## Verification
- `scripts/gate.sh T02-impl unit trusted` → PASS (`logs/T02-impl-compile.log`, `logs/T02-impl-unit.log`, `logs/T02-impl-trusted.log`)
  - compile: PASS
  - unit: PASS, 355 tests, 321 pass, 0 fail, 34 todo; the same counts as T01
  - trusted: PASS in 33 s; the log shows `PASS real-input screenshot: 01-paragraph-blur-commit` through `05-open-with-editor`
- `.artifacts/REAL-INPUT-LATEST.md` says `Suite: **passed**`; its `real-input-S1fbeY/INDEX.md` lists 5 captures.
- `rg -n "sendPreviewMessageForTests|\.fill\(" test/integration/realInput*` → no matches.
- Temporary diagnostics: a `console.log` in `findCurrentFrame`, `waitForRender` and the scenario setup was added during debugging and removed before the final gates. `rg` for `DEBUG-TEMP` finds nothing.
- Evidence proof runs: `logs/T02-proof-s1-trusted.log`, `logs/T02-proof-s4b-trusted.log`, `logs/T02-debug3-trusted.log` (failing on purpose, see above).

## Evidence for reviewers
- Final captures: `.artifacts/real-input-S1fbeY/` (`01-paragraph-blur-commit.png` … `05-open-with-editor.png`, `INDEX.md`).
- Each proof log is in `logs/`. The proof for S5 ran with the earlier `setEditMode` (one click). The S1 and S4 proofs ran before the detach-pattern and `setEditMode` changes. Those changes do not touch the commit waits, but the reviewer should know that the three proofs and the final gate did not run on the same harness revision.

## Feedback addressed (rounds 2–3)
- Finding 1 (MAJOR, commit checks): S1, S4 and S5 wait for `waitForRender` after the commit and assert the rendered DOM. The proof step (above) ran each commit action removed in turn; each timed out at the new wait; each action was restored.
- Finding 2 (MAJOR, macOS caret keys): `caretToEnd` (Meta+ArrowDown on darwin, Control+End elsewhere) and `focusedCaret` are exported from the harness. S2 and S3 call `caretToEnd` then `waitForCaretAtEnd`; `${MOD}+End` is gone.
- Finding 3 (MINOR, frame identity): `findCurrentFrame` returns undefined when there is no preview, and it compares `data-sphinx-preview-document-id` to `preview.documentUri` before the version and request id. Verified: the Open With webview and the side preview both match with this check; the document id attribute is set from `documentKey` in `scrollSync.ts:46`.
- Finding 4 (MINOR, detach errors): `waitFor` treats a detached-frame error as false and keeps polling (any other error rethrows). `waitForEditor` is in the harness and exported. Beyond the review text, the detach pattern is one shared constant that also matches `Cannot find context with specified id`. That message is the CDP form of the same webview replacement; it was seen once on a click in `setEditMode` (`logs/T02-proof-s4-trusted.log`) and it had caused a failure before this round's change.
- Finding 5 (MINOR, closeAllEditors): documented in the JSDoc (both facts). The optional explicit revert of dirty fixture buffers was not added; the review called it optional, and it is not needed for the gates.
- Finding 6 (MINOR, capture side effects): JSDoc says to call `capture` only after the last action and lists the side effects. The optional `keepView` option was not added.
- Finding 7 (NIT, retry double-run): JSDoc on `withCurrentFrame` added.
- Finding 8 (NIT, edit-mode persistence note): not in this round's files. T38 must turn edit mode off in `finally` if edit mode becomes per workspace. This is a follow-up note for the plan, not a change here.
- Finding 9 (NIT, fixture gitignore): not changed; `.gitignore` is outside the allowed files.
- Extra change, not in the review text: `setEditMode` now clicks up to three times and reads the mode through `withCurrentFrame`. This matches the harness contract in the task ("clicks until the mode matches"). Before this, one S5 run failed with `Timed out waiting for edit mode on` after a single lost click (`logs/T02-proof-s5b-trusted.log`).

## Open points / STOP reason
- Flakes seen during proofing, before the fixes above: (a) `Frame was detached` at `setEditMode` (`logs/T02-proof-s5-trusted.log`), (b) `Cannot find context with specified id` on a click in S2 (`logs/T02-proof-s4-trusted.log`), (c) one lost toggle click in S5 (`logs/T02-proof-s5b-trusted.log`). The final gate passed, but only one green run is recorded for this harness revision. The reviewer should rerun `trusted` once to judge stability.
- The `.artifacts/real-input-*` folders and the `test/integration/fixtures/realinput-*` folders are untracked. NIT 9 (gitignore) is still open.
