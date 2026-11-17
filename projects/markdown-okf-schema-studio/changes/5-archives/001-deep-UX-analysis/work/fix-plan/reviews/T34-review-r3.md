# T34 review — round 3 (chained patches, fallback re-arm)

Scope: `git diff 8d1ee21 -- src/markdown-okf-schema-studio` (extension.ts +31/-2, two test files additive).
Static review only; no build or test run by the reviewer.

## 1. Ordering
- [x] `applyContentPatch` (scrollSync.ts:254) is fully synchronous: validation, DOM capture, editor
  closes, `main.innerHTML`, then `context.documentVersion/requestId` mutation. No `await`, timer or
  promise before the context update. A patch addressed to stage N is therefore matched after patch N
  has run. Unit test "apply in order" covers 3 chained patches → ready 12, 13, 14.

## 2. Rejected chain / fallback
- [x] Fallback (`armContentPatchFallback`) unchanged: on fire it calls `freshNonceRecord` then
  `assignWebviewHtml` — fresh nonce kept.
- [x] Re-arm only when a timer is already pending, the `documentId` matches the current stage, and
  `requestId < stage.requestId`. A rejected patch makes the runtime drop it and every later chained
  patch (unit test "rejected chain": no ready at all), so no further intermediate readies arrive; the
  fallback fires at most 2 s after the last ready the page did send.
- [x] Indefinite postponement needs a non-terminating stream of distinct intermediate readies; each
  one requires a patch that was actually applied, and the chain length is bounded by renders sent.
  A rejected newest patch ends the stream. Not realistic. Stale-page readies (lower requestId, same
  doc) can only occur once each and are likewise bounded.
- [x] Intermediate readies return early before `matchesCurrentPreview`, so `readyRequestId` is not
  set to an intermediate stage and the fallback's "ready for stage" guard stays correct.

## 3. Clearing `patchedRequestId`
- [x] Cleared inside `assignWebviewHtml` alongside `readyRequestId`. The only `webview.html = ` writes
  (extension.ts:605, 622) are inside that function, and fallback, reload branch, deserialize,
  recreated webview and document switch (lines 666, 769, 861, 985, 2245, 2407, 2746) all go through it.
- [x] Patch condition still also requires same `activeDocumentIdentity`/`activeDocumentPath` and a
  non-empty nonce; a stale `patchedRequestId` cannot survive a document load, so no cross-document patch.

## 4. The rest
- [x] T43 overlay: `armPendingOverlay` uses `pageHasStage`; posting an overlay to a page that will
  reach the stage after queued patches is correct because messages are handled in order, and the
  patch itself clears the overlay before re-applying (as before).
- [x] T30 `patchPropertiesTable` and the PlantUML patch keep the plain `readyRequestId` check: more
  conservative, worst case they defer to the normal path. Acceptable.
- [x] No other production change.

## 5. Tests
- [x] `scenarioLargeDocumentPatched`: ~70 KB fixture (asserted >65 000 chars), asserts zero html
  assignments, >0 patches, same page (marker), typed text visible, request-id attribute equals host
  requestId. Matches its claim.
- [x] Only additions; no existing assertion modified.
- [x] CDP throttling is deliberate (rate 6), reset to 1 and the session detached in `finally`.

## Notes (non-blocking)
- The 600 ms settle wait plus 30 s ready wait make the scenario slow under throttling; fine for the
  integration tier.

VERDICT: PASS
