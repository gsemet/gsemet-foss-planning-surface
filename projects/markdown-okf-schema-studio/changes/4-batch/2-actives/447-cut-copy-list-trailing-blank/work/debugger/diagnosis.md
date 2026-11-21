# CR-447 diagnosis: Timed out waiting for Cmd or Ctrl+X to cut the list

Reproduction: heavy CI run 44894547616, job integration (real VS Code); or `just ci-integration` with the real-input group.

Cause: defect in the new scenario, not in the product.
A successful copy clears the block selection (src/page/features/blockSelectionView.ts:462-468,
receiveBlocksResult: ok on any op other than delete / delete-blank-lines calls clearBlockSelection()).
scenarioCutCopyListBeforeBlankLines (test/integration/realInput/blockKeys.ts:449-457) presses Mod+C then Mod+X
with no new selection. The keydown handler (blockSelectionView.ts:586,590) then has range undefined and
`if (key !== "v" && !range) return;` so previewBlocksCut is never posted. Clipboard stays "sentinel", document
unchanged, the wait at :455 times out. The copy step passed (its wait ends before the result message clears
the selection).
The pre-existing scenarioBlockSelection hides this: after Mod+C it presses Escape and waits for "selected = 0",
which is already true.

Product check: cut itself is right. planBlocksCopyCut (src/core/edits/sourceEdits.ts:251-265) trims the trailing
blank lines (lines 5-6), copies "- item a\n- item b", planCut (src/core/mapping/blockRange.ts:117-153) skips
blank lines 7-8, touchesAbove is false, deletes lines 5-8: result
"# Clip\n\nAlpha paragraph.\n\nOmega paragraph.\n", equal to the scenario's expectation. Host handler
(src/session/features/sourceEdits.ts:420-470) is fine.

Fix (test only): in blockKeys.ts scenarioCutCopyListBeforeBlankLines, between the copy wait/assert (:452) and
`writeText("sentinel")` / press X (:453-454), re-select the list: call selectListFollowedByBlankLines(page,
document) logic again, i.e. repeat the Shift+click on the `ul` (:431) and the waitFor "exactly the list to be
selected" (:432-435), or split the scenario into two documents (copy, then cut) each calling
selectListFollowedByBlankLines. Preferred: re-select after copy, and also wait for the "Copied as Markdown"
notice / selection cleared first (waitFor selected().length===0) so the result message cannot arrive after the
re-selection and clear it. Paste scenario (:469-487) is unaffected (paste does not follow a copy).
Secondary check once fixed: the selection after cut is cleared by the same receiveBlocksResult path; r25 capture is taken after waitForRender, no change needed.

Not run: no local real-VS-Code reproduction (Linux xvfb job); diagnosis is from code reading plus the CI log.
