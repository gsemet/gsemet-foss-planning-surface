# CR-447 diagnosis (round 2): Mod+X does not cut after Mod+C

Correction: the first diagnosis was wrong. receiveBlocksResult (src/page/features/blockSelectionView.ts:462-473)
is `if (op === "copy") showSelectionNotice(...) else if (op !== delete...) clearBlockSelection()`:
a successful COPY keeps the selection (only cut/paste clear it). That is why the older scenario presses Escape
after Mod+C, and why run 44896847967 timed out waiting for the copy to clear it. The re-select added in
b39e99d2 is unnecessary.

Cause (most likely, from code; no local real-VS-Code repro): a race in the scenario, not a product defect.
- Host copy (src/session/features/sourceEdits.ts:440-443) writes the clipboard, THEN posts previewBlocksResult.
- The page sets blocksFlight when it posts the copy (blockSelectionView.ts:272) and clears it only on that result
  (:463-464). While blocksFlight is set, the clipboard keydown handler does preventDefault then `if (blocksFlight) return;`
  (:592-594): the key is swallowed silently.
- blockKeys.ts (HEAD~1 :459-466, original run) waits only for the clipboard to equal the list, i.e. for the
  host's write, which happens BEFORE the result reaches the page, then writes "sentinel" and presses Mod+X at once.
  The X lands while blocksFlight is still set and is dropped; nothing retries, so the wait at "Cmd or Ctrl+X to
  cut the list" times out (clipboard stays "sentinel", doc unchanged). Same swallow would hit any quick second chord.
- Ruled out: host refusal for the list (planBlocksCopyCut/planCut on lines 5-7 gives lines 5-8 deleted, exactly
  the expected document; pinViewportTop is valid; blocksDocument only refuses an open edit or stale revision, neither
  applies); focus (dump: webview focused, no toast, no dialog, no quick input; copy worked in the same focus);
  protocol validator (pageToHost.ts:311 accepts an absent or finite pinViewportTop). The dump does not show the page's
  own status text, so a page-side notice cannot be excluded from the log alone.
- Note: this is the first real-input cut scenario in test/integration (grep '+X' finds none), so no older
  C-then-X sequence exists to compare with.

Fix (test only), test/integration/realInput/blockKeys.ts scenarioCutCopyListBeforeBlankLines (now ~:463-466):
remove the "copy to clear the block selection" wait and the selectListInPreview re-select; instead, after the
clipboard wait and the unchanged-document assert, wait for the page to have received the copy result:
`waitFor("the page to report the copy", async () => (await withCurrentFrame(page, (frame) => frame.evaluate(() =>
window.document.querySelector(".sphinx-preview-selection-status")?.textContent ?? ""))) === "Copied as Markdown")`
(the notice lasts 4 s, selectionNoticeTimer, so poll fast), and assert selectedBlocks(page).length === 1 still.
Then writeText("sentinel") and press Mod+X. Alternative with no timing dependence: press Escape and re-select
(selection cleared by Escape, flight irrelevant) is NOT enough either, since the flight can still be set; the notice
wait is the reliable signal.
Optional product hardening (not needed for this CR): in the handler, do not swallow the chord silently while a
flight is pending (or drop blocksFlight for copy, which changes nothing).
If this fix still times out, dump the page status text and `blocksFlight` state at the failing step (add the status
text to the failure dump) before changing anything else.
