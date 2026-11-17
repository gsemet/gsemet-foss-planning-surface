# T34 implementation — round 2

STATUS: DONE

## Summary
Round-2 fixes from `reviews/T34-review-r1.md`: every new webview document that is loaded from a record
that went through a content patch now gets a fresh nonce (MINOR 1); a unit test proves that pending
block navigation (P-E4) resumes after a content patch (MINOR 2); a comment explains the `documentId`
of the patch message (NIT 4). MINOR 3 (PlantUML patch fallback timer) is not in scope.

## Feedback addressed
- **MINOR 1 — fresh nonce for every new document.** `src/extension.ts`: `freshNonceRecord(preview)` creates a nonce
  with `createNonce()` (the generator `buildPreviewWebviewHtml` uses), sets
  `preview.webview = { ...preview.webview, html: reuseNonce(html, old, fresh), nonce: fresh }` and returns the
  fresh nonce. It only acts when the record keeps a loaded nonce (new field `recordKeepsLoadedNonce`, set in
  `postContentPatch`, cleared in `assignWebviewHtml` when a new document is assigned), so records and
  assignments without a patch behave exactly as before (no extra reloads of identical status html). Called before
  the new document is loaded on: the 2 s fallback (`armContentPatchFallback`), the reloaded-document branch of
  `handlePreviewSyncMessage`, and `setPanelHtml` (which covers the PlantUML fallback, `setStatus`/stale pages and
  the properties-table fallback: it maps the html it was given from the old nonce to the fresh one). The patch
  path keeps the loaded nonce.
- **MINOR 2 — P-E4 on the patch path.** New test "T34: pending block navigation resumes after a content patch":
  edit mode, open a block, change it, ArrowDown at the end (final save posted, `pendingBlockNavigation` set to
  line 100 / caret start), apply a success `previewContentPatch`; the next block gets `previewEditOpen` with the
  new identifiers, the navigation is spent, and after the source reply the new editor's caret is `[0, 0]`. It
  passed without a runtime change.
- **NIT 4.** Comment in `postContentPatch` on why `documentId: previous.activeDocumentIdentity` is the target.

## Files changed
- `src/extension.ts` — `freshNonceRecord`, `recordKeepsLoadedNonce`, `createNonce` import, calls on the three paths, comment.
- `test/webview/contentPatch.test.ts` — `reuseNonce` swaps every occurrence.
- `test/webview/scrollSync.test.ts` — P-E4 patch test.
- `test/integration/realInput.test.ts` — RI-T34 fresh-nonce assertion; `setRenderOverrideForTests` import.

## Tests written first (failing before the fix)
- RI-T34 with `freshNonceRecord` disabled by a temporary mutation (restored; `logs/T34-r2-red-trusted.log`):
  `Real-input integration failed: Error: Timed out waiting for a new document with a fresh nonce.`
- The P-E4 unit test passes without a runtime change (the review asked to fix the runtime only if it failed).

## Tests added or changed
- `T34: reuseNonce swaps every occurrence, in the policy tokens and in the attributes` — two `'nonce-…'` tokens and three `nonce="…"` attributes are replaced, nothing of the old nonce is left, and the swap is reversible.
- `T34: pending block navigation resumes after a content patch` — see above.
- RI-T34 (new part, after the slow render): the record's nonce equals the loaded page's `script[nonce]`; a render failure (`setRenderOverrideForTests`) loads the stale status as a new document; a frame whose `script[nonce]` equals the record's nonce, and that differs from the nonce before, appears; the next good render recovers in that document (text `…yz!?` shown). `previewEditing.test.ts` is unchanged and passes.

## Existing assertions changed
- None.

## Verification
- `gate.sh T34-impl2 unit types contracts` → PASS (`logs/T34-impl2-unit.log`, `-types.log`, `-contracts.log`; unit now 652 tests)
- `gate.sh T34-impl2 full` → PASS, 257 s (`logs/T34-impl2-full.log`, shows `RI-T34 typing: 0 html assignments, 20 content patches`)
- Two earlier `full` runs in this round failed at my own new RI-T34 assertion about the frame (`frame.isDetached()`, then the page marker): VS Code reuses the Playwright `Frame` for a replaced webview document and the old document stays reachable for a moment. I removed those two assertions; the nonce comparison is the proof of a new document. Those logs were overwritten by the passing run.
- `trusted` with the mutation (red evidence) FAILED as intended; the source was restored afterwards and the passing `full` run used the restored source.
- The screen was unlocked before every long gate. No gate or test process of mine is left running.

## Evidence for reviewers
- `logs/T34-r2-red-trusted.log` (red), `logs/T34-impl2-full.log` (green).

## Open points / STOP reason
- MINOR 3 (PlantUML patch has no fallback timer) remains a follow-up, as instructed.
- The stale link-hint limit and the recreated-webview guard (not exercised end to end) are unchanged from round 1.
