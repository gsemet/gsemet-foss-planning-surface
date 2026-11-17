# T35 review — round 1

Base: d596de8 · Reviewed diff: 8 files (7 modified + 1 new test), +110/-9 plus `test/security/userFacingText.test.ts` (new, ~150 lines)

## Gates
- compile, unit, types, contracts: PASS (`logs/T35-*.log`)
- trusted: PASS (81 s)
- visual: PASS vs T00 baseline, 0 new failures; `logs/visual-T35/MACHINE-CHECKS.md`: 99 scenarios, 0 failing applicable checks.
- No new failure compared with the T00 baseline.

## Done-when
- [x] No user-facing "Sphinx" in scanned sources. Evidence: `userFacingText.test.ts` "no user-facing string literal mentions Sphinx". Its pre-fix failure lists exactly the two `extension.ts` notifications (lines 1755, 1819), which shows the scanner reaches the end of `extension.ts` and is not vacuous. I also grepped `src/` for quoted "Sphinx": the only remaining hits are in `src/build/sphinxBuild.ts` (see below) and the ignored `src/extension.ts.orig`.
- [x] Status pages put the title and the message on two lines. Evidence: the CSS in `PREVIEW_ACCESSIBILITY_CSS`, the unit test "status titles and messages are block-level only on status pages and non-pending banners", and the RI-T35 capture (`.artifacts/real-input-Dw2A6s/35-status-two-lines.png`): "Preview source missing" in bold with "The active Markdown source was deleted." below it, with no clipping. `status-two-lines` was checked as PASS.
- [x] Amendment: the body carries `data-sphinx-preview-status-page` (`buildStatusWebviewHtml`, asserted in `stockCoexistence.test.ts`). Every `display:block` selector is scoped by the page marker or by `:not([data-sphinx-preview-status="pending"])`, and the unit test enforces this. The pending banner keeps one line. `success` is still hidden at the container level (previewStyles.ts:32), so the block children do not matter there.
- [x] RI-T35 passes with `required: ["status-two-lines"]`, and recovery to the rendered heading is asserted (P-L4).
- [x] Internal identifiers, classes, message types and status values are unchanged.

## Protected features checked
- P-L4: RI-T35 deletes the source, sees the `missing-source` status and page, restores the file, and waits for the rendered `h1`. `lifecycle.test.ts` is unchanged and passed in trusted.
- P-L2/P-L9: `stockCoexistence.test.ts` only gained assertions and passed.
- P-N4: the link-navigation logic is unchanged. Only the two warning texts changed, and no test asserted the old text.
- P-S4: `statusMarkup` still escapes the message. Only a static attribute was added to the body.
- P-R*/P-E*: not touched. The visual campaign shows 0 new failures.

## Orchestrator notes, judged
- **stockCoexistence.test.ts scope.** It falls under the amendment's "existing tests that compare the exact status page html". This test is the one that inspects `buildStatusWebviewHtml` output. The change only adds assertions and weakens nothing. Accepted, keep it.
- **RI-T35 deviations.**
  - The test still proves the requirement. It asserts a newline between the title and the message in `innerText`, and the `status-two-lines` geometry check is required.
  - Finding the frame by the body marker is correct, because status pages have no render markers.
  - Using `vscode.workspace.fs.delete` still drives the real deletion path that sets `missing-source`. The 2 s settle points at a possible watcher gap: an external `rm` of a file created moments earlier may be missed. That is unlikely in real use, but it is unverified. Logged as MINOR follow-up 2.
  - The missing pre-fix failure for RI-T35 is acceptable here. This is a styling/wording task, not an interaction bug, and the unit CSS test plus the body-marker assertion did fail before the fix.
- **sphinxBuild.ts.** Nothing imports `src/build/sphinxBuild.ts`. `buildSphinxSnapshot` is only referenced inside that file, and `sourceTransforms.ts:67` only mentions it in a comment. No path from `src/extension.ts` reaches it, so it is not user-facing today. Follow-up 1 asks to delete it or add it to the scan.
- **Tokenizer.**
  - It skips `//` and `/* */` comments, which the self-test covers.
  - It scans template heads and tails across `${}`.
  - It does not handle regex literals. A regex such as `/["']/` could desync it. Real evidence shows it is not vacuous: before the fix it found both offenders deep in `extension.ts`.
  - It has no per-file guard that it found at least one literal. Follow-up 3 adds one.

## Findings
1. [MINOR] `src/build/sphinxBuild.ts` — dead module with "Sphinx" error strings ("Sphinx preview is disabled…", "Sphinx exited with…"). Nothing imports it, so users never see them. Fix (follow-up task): delete the module if nothing else uses it, or else add it to `scannedFiles()` in `userFacingText.test.ts` and reword its strings.
2. [MINOR] `test/integration/realInput.test.ts`:`scenarioStatusPageTwoLines` — it needs a 2 s settle and `workspace.fs.delete` because `fs.rmSync` right after creation was missed. Fix (follow-up): add a lifecycle probe that creates a file, opens the preview, waits for the render, runs `fs.rmSync`, and expects `missing-source` within 10 s. If that fails, investigate the watcher setup in `extension.ts`.
3. [MINOR] `test/security/userFacingText.test.ts`:`literals` — nothing guards against a silently empty scan, and regex literals are not handled. Fix: in "no user-facing string literal mentions Sphinx", assert `literals(source).length > 0` for every file. Also assert that `extension.ts` yields a literal containing `"could not follow the link"`, so a tokenizer desync before line 1755 fails the test.
4. [NIT] `src/extension.ts.orig` (git-ignored) still holds old strings. It is not shipped and not part of this task. Delete the local file when convenient.

## Existing assertions changed
- None modified or deleted. Added only: `stockCoexistence.test.ts` (2 assertions, justified by the amendment), and a new test in `previewStyles.test.ts`. OK.

VERDICT: PASS
