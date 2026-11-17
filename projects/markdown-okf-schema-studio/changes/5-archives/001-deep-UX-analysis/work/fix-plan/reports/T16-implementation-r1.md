# T16 implementation — round 1

STATUS: DONE

## Summary
Deleted the two edit-mode paragraph rules (`p[data-sphinx-source-line] { white-space: pre-wrap }` and its
table exception) from previewStyles.ts, so edit mode no longer shows source line breaks and keeps
the reading layout. Added RI-T16 (failed first), updated the matching unit assertion and the two
capture.py checks that asserted pre-wrap in edit mode. `measureLineTops` is untouched; the scroll
gate passes.

## Files changed
All under :
- src/preview/previewStyles.ts — removed both rules.
- test/webview/previewStyles.test.ts — assertion replaced (see below).
- test/visual/capture.py — two edit-mode checks inverted (see below).
- test/integration/realInput.test.ts — RI-T16 `scenarioEditModeNoReflow`, registered in run().

## Tests written first (failing before the fix)
- RI-T16 against unmodified code (logs/T16-impl-pre-trusted.log): `Real-input integration failed: AssertionError [ERR_ASSERTION]: scrollHeight changed from 982 to 1117`
- Note: with the task's ~60-character source lines the first attempt PASSED on unmodified code, because the side preview is about 520 px wide and 60-character lines fit one rendered line each (the reflow is invisible). The fixture therefore hard-wraps at about 40 characters, which reproduces the bug. Deviation from "about 60" is intentional.

## Tests added or changed
- RI-T16: reading-mode vs edit-mode `scrollHeight` and third paragraph top (page coordinates) differ by at most 2 px (three 4-line paragraphs plus a table, real pencil click via setEditMode).

## Existing assertions changed
- previewStyles.test.ts:"frontmatter edits stay inline while edit mode preserves source newlines" — old: assert.match pre-wrap rule for edit-mode `p[data-sphinx-source-line]` and assert.match table rule `white-space: normal` → new: the task's doesNotMatch regex, plus a doesNotMatch that no edit-mode `table p[data-sphinx-source-line]` rule exists — required by: removal of both rules.
- capture.py check_preview_edit_mode: old: paragraphs must be `pre-wrap` + `overflow-wrap: anywhere` ("paragraphs do not preserve source breaks while wrapping") → new: no paragraph may be `pre-wrap` ("edit mode shows source line breaks in rendered paragraphs"); the horizontal-overflow check is kept.
- capture.py same function, 08-okf-schema warning paragraph: old: warning paragraph must span at least 2 rendered line tops ("did not expand to its source lines"; this asserts the pre-wrap expansion, not line-level scroll mapping) → new: warning paragraph must not be `pre-wrap`. Without this change edit-paragraph-dark / edit-mode-dark failed.
- No check asserting line-level scroll mapping in edit mode was touched.

## Verification
- `gate.sh T16-impl unit` → PASS (logs/T16-impl-unit.log)
- `gate.sh T16-impl trusted` → PASS, incl. RI-T16 (logs/T16-impl-trusted.log)
- `gate.sh T16-impl scroll` → PASS (logs/T16-impl-scroll.log)
- `gate.sh T16-impl visual` → gate reports FAIL: 4 "new" lines, all the baseline failure "table action bar is not aligned with its active cell" for 08-okf-schema dark/light sticky-3, same message, only the embedded coordinates differ by about 0.4 px (cellTop 122.515 in baseline, 122.125 now; barTop 76.515 vs 76.125), a direct effect of the paragraph no longer reflowing. Those 4 failures exist in the baseline with identical text apart from the numbers. All other failures are baseline; 4 baseline lines now pass (edit-paragraph-dark family). The orchestrator may need to refresh the baseline signature. (logs/T16-impl-visual.log, logs/T16-impl-visual-new-failures.txt)

## Evidence for reviewers
- RI-T16 screenshot: .artifacts/real-input-*/23-edit-mode-no-reflow.png (latest run dir).
- Visual screenshots: /Users/az02065/Projects/Nestor/agentic-coding-white-paper/.agents/changes/requests/deep-UX-analysis/fix-plan/logs/visual-T16-impl/ (relied on: edit-paragraph-dark, edit-admonition-dark, edit-mode-dark pages).

## Open points / STOP reason
- Visual gate comparison differs only by sub-pixel coordinates inside a baseline-failing message (see above).
