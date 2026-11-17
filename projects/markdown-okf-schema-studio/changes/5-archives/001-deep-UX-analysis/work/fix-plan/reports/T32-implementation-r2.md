# T32 implementation — round 2

STATUS: DONE

## Summary
`previewReady` now reports the pinned anchor (only when the pin was applied). The pending pin carries a `minVersion` and is no longer consumed by a render of an older document version. The pin is stored only in the accepted save paths. RI-T32 list now puts the reading line inside the list and adds a second-render re-measure; the table sub-case keeps the table visible.

## Files changed (all in Allowed files)
- src/webview/scrollSync.ts — `pinApplied` flag set in `restoreState`; `previewReady` adds `anchorField()` only when set.
- src/extension.ts — `pendingPin.minVersion`; `storePendingPin` (called from `handleFrontmatterSave` after `applyEdit` resolves true, and from `handlePreviewEditSave` for `final === true` after validation); `completeActiveBlockEdit` raises `minVersion` to `document.version` once every apply of the edit resolved; `takePendingPin(preview, documentId, renderedVersion)` keeps the pin for older versions, clears on use or expiry. The old unconditional store in `handlePreviewSyncMessage` is removed.
- test/webview/scrollSync.test.ts — new test for `previewReady.anchorLine`.
- test/integration/realInput.test.ts — RI-T32 reworked (import line unchanged).
- docs/scroll-anchoring.md — R7: two more sentences.

## Tests written first (failing before the fix)
- NOT DONE as red-first, again. I applied the `previewReady` fix before writing its unit test and could not restore the old behaviour (no reverting or swapping source). The new unit test cannot pass on the r1 tree: `previewReady` had no `anchorLine`, and the test asserts `typeof anchorLine === "number"`. No red run is recorded.

## Tests added or changed
- Unit "previewReady reports the pinned anchor only when the load restored a pin": with `initialPin` the message has a numeric `anchorLine` >= 1; a plain harness has no `anchorLine` key.
- RI-T32 list (reworked, finding 3): the list top is scrolled to about 40 px below the viewport top (`min(40, reading offset - 25)`; measured reading offset 81.8 px). It asserts the reading line lies inside the list (T0=39.6, reading 81.8). Then click "Refrigerated goods", Mod+End logic as before (End, Enter, "Frozen goods", Mod+Enter). Measured: T0=39.609375, T1=39.609375, drift 0.
- RI-T32 second render (finding 1): an edit appended far below (WorkspaceEdit) gives a render with no pin. Measured T2 = 39.609375 (drift 0) 800 ms after the render, T3 re-measured 700 ms later (1.5 s after the render, past the link-enrichment reload), also within 3 px (asserted).
- RI-T32 table (finding 4): 6 filler paragraphs above, nothing below, so the page has only about 260 px of scroll room and the typing jump cannot push the table out of view. It asserts `0 <= Tcommit <= viewportHeight` and the same after Save. Measured T0=299.1, Tcommit=38.5, T1=38.1, drift -0.39. The `33-save-keeps-table-in-place` screenshot shows the table (as designed; not re-viewed by me).

## Existing assertions changed
- none (`git diff 29a3df8 -- test/` has no removed lines)

## Feedback addressed
1. [MAJOR] `previewReady` anchor — done as specified (flag, `anchorField()`, no host change; `validAnchorLine` already accepts it and `handlePreviewSyncMessage` stores `value.anchorLine` before dispatch). Unit test added. E2E re-measure added (T2 and T3, see above). Red-first not recorded (see above).
2. [MAJOR] `minVersion` — implemented as in fix parts 1–3 (stored at the final message with the current version, raised after all applies resolve in `completeActiveBlockEdit`; frontmatter stores after `applyEdit` resolves, with `document.version`). `takePendingPin` keeps the pin when `renderedVersion < minVersion`.
   - Test: NOT covered by a test. There is no unit seam (`extension.ts` imports `vscode`; no unit test loads it, and the task does not allow a new seam file). I tried the RI-T32 sub-case and removed it. Findings from those attempts:
     - The preview's own autosaves never start a render while the block editor is open: `refreshPreview` skips change events while `edit.applying`. Evidence: the document version went to 2 at +418 ms and no render followed in 6 s of polling.
     - So the review's scenario (autosave render in flight at Mod+Enter) cannot occur for the preview's own edits. Other triggers I tried (REFRESH command, touching the file for a watcher event) destroyed the open editor in the webview before Save, so they do not make a valid test.
     - The guard stays as defence for external renders; it is unproven by E2E. Please judge whether that is acceptable.
3. [MAJOR] list case — reworked so the reading line is inside the list (see above). The orchestrator runs it at 29a3df8. The file can be copied to the base worktree: RI-T32 uses only harness functions already in `test/integration/realInput/harness.ts` (unchanged since base: `waitFor`, `waitForRender`, `withCurrentFrame`, `findCurrentFrame`, `openSidePreview`, `setEditMode`, `typeText`, `press`, `caretToEnd`, `bufferText`, `waitForEditor`, `MOD`), the file-local `withDocument`, `captureAfter`, `waitForNoBlockEditor`, and `getActivePreviewForTests` from `extensionApi`; the new helpers are defined inside the scenario. It reads the `--sphinx-preview-reading-offset` CSS variable (published by the base runtime too; falls back to 0 if absent, which would make the "reading line inside the list" assertion fail loudly at base). Expect a failure at base on the T1 or T2 drift assertion; record the measured drift from the console line `RI-T32 list (...)`. If the first assertion fails at base only because of the missing CSS variable, tell me.
4. [MAJOR] table case — done (see above). Side finding: in a long document, typing in a table cell (even the first character) pages the document by hundreds of px (-1407 and -864 px seen) before any commit; unrelated to T32, suggest a separate UX item. The test avoids it by using a short document.
5. [MINOR] RI-T21: a full run during debugging failed once at RI-T21 ("the StRS-A link has a box") and passed on the next run with the same code, so it is a flake and not tied to T32. The two final `full` runs both pass. I added no settle step.
6. [NIT] `pendingPin` store moved into the accepted `previewEditSave` (final) and `previewFrontmatterSave` (after apply) paths.

## Verification
- `PLAN/scripts/gate.sh T32-impl2 unit types contracts full visual` → compile, unit, types, contracts PASS; full PASS (RI-T32 list drift 0, T2 drift 0, table drift -0.39); visual PASS vs baseline (0 new).
- `PLAN/scripts/gate.sh T32-impl2c full` → PASS (same RI-T32 numbers).
- Logs: PLAN/logs/T32-impl2-*.log, T32-impl2c-full.log. Intermediate debug runs: T32-dbg*-full.log, T32-impl2b-*.log (failed runs on my own test design, fixed).

## Open points
- Finding 2 is untested end to end (see above).
- No red-first run for finding 1 (see above); the base "before" drift is for the orchestrator.
- Typing in a table cell of a long document jumps the page (pre-existing; new UX item suggested).
- `src/extension.ts.orig` still exists in the tree, untouched.
