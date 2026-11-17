# T02 implementation — round 1

STATUS: DONE

## Summary
Added a real-input E2E harness (`test/integration/realInput/harness.ts`) and a smoke suite
(`test/integration/realInput.test.ts`) with five scenarios RI-S1 to RI-S5. Every action uses
`page.mouse`/`page.keyboard`/`locator.click()`/`locator.press()`. Reads use the preview hooks and the
DOM. The suite is registered in `trusted-suite.ts` after the checkbox block, and `review-index.ts`
gained item 6 "Real-input editing". All five scenarios pass against the current product, so no
product code changed and no existing assertion changed. The bug-first step does not apply because
this task adds smoke tests only.

## Files changed
- `test/integration/realInput/harness.ts` (new) — the harness API from the task, plus two extra
  exports: `findCurrentFrame` (non-throwing frame lookup) and `withCurrentFrame` (see Open points).
- `test/integration/realInput.test.ts` (new) — `run()` and scenarios RI-S1 to RI-S5, each with its own
  fixture, cleaned up in `finally`.
- `test/integration/trusted-suite.ts` — import `runRealInput`; try/catch block after the checkbox block.
- `test/integration/review-index.ts` — item 6 "Real-input editing" linking to `REAL-INPUT-LATEST.md`.

## Tests written first (failing before the fix)
Not applicable. T02 adds smoke tests of existing behaviour, not bug tests. Two failures occurred
during the harness build, and both were in the harness and suite code, not in the product:
- `setEditMode` clicked the toggle again after a successful wait, so edit mode flipped back off.
  Failure excerpt: `Error: Timed out waiting for edit mode on.` Fixed by clicking only when the mode is wrong.
- A detached preview frame during a click (scenario 2). Failure excerpt: `locator.click: Frame was
  detached`. Fixed with `withCurrentFrame`, which re-resolves the frame on detach errors only.
- The table cell editor is a `<textarea>`, not an `<input>`. Failure excerpt: `Timed out waiting for the
  editor matching [data-sphinx-preview-table-cell-editor] input`. Selector corrected.

## Tests added or changed
- RI-S1 paragraph blur commit — End, type ` Added.`, click the heading; buffer equals SMOKE with that line changed.
- RI-S2 Cmd/Ctrl+Enter — buffer line 4 is `continues on line two. X`; no block editor after the re-render.
- RI-S3 arrow navigation — ArrowDown moves the editor to the table, textarea starts with `| Name | Value |`.
- RI-S4 table cell Enter — buffer contains `| alpha | one1 |`; the table still has four lines.
- RI-S5 Open With editor — `openStudioEditor` (no side preview); buffer contains `Second paragraph. Z`.

## Existing assertions changed
None.

## Verification
- `gate.sh T02-impl unit types` → PASS (`logs/T02-impl-unit.log`: 355 tests, 321 pass, 0 fail, 34 todo from T01; `logs/T02-impl-types.log`)
- `gate.sh T02-impl trusted` → PASS (`logs/T02-impl-trusted.log`; log shows the five `PASS real-input screenshot` lines, 01 to 05)
- `rg -n "sendPreviewMessageForTests|\.fill\(" test/integration/realInput*` → no matches
- `.artifacts/REAL-INPUT-LATEST.md` → `Suite: **passed**`; `.artifacts/real-input-tXfPtx/INDEX.md` lists five captures
- Fixture directories are removed after each scenario (`test/integration/fixtures/` has no `realinput-*` leftovers)

## Evidence for reviewers
- Captures: `.artifacts/real-input-tXfPtx/` (`01`–`05` `.png` and `.md`, with `INDEX.md`)
- Latest pointer: `.artifacts/REAL-INPUT-LATEST.md`
- Diagnostic-only log from the edit-mode debugging run: `logs/T02-diag-trusted.log` (the diagnostics were removed from the code)

## Feedback addressed (rounds 2–3)
Not applicable (round 1).

## Open points / STOP reason
- **Extra exports beyond the spec:** `findCurrentFrame` and `withCurrentFrame` are exported from the
  harness. `withCurrentFrame` retries an action only on "frame detached" or "execution context was
  destroyed" errors. Later tasks should use it for every action in the same way.
- **`capture()` buffer excerpt:** the spec gives `capture(page, frame, name, note)` no document
  parameter, so the excerpt is read from the first `vscode.workspace.textDocuments` entry under a live
  fixture directory (tracked by `createFixture`). Only one fixture is live at a time.
- **Edit mode is set in every scenario:** it persists per workspace, and the checkbox suite leaves it on.
  Each scenario calls `setEditMode(page, true)` explicitly so that it does not depend on order.
  RI-S5 uses the same call after opening the Open With editor.
- **Table output:** after the cell edit, the table is re-serialised with padded separators. The
  row `| alpha | one1 |` is asserted exactly, as the task requires. The rest of the table
  formatting may change under T04, as the task anticipates.
- **Earlier failed runs:** `.artifacts/real-input-*` directories from failed attempts remain. They are
  gitignored and match the existing `checkbox-e2e-*` pattern.
- The pre-existing modifications in `book/` and `.agents/thinking/` were already present at the
  start and were not touched. No commit was made.
