# T34 review, round 2

Base 0f4605a, uncommitted tree. Static review only (no tests run; the orchestrator gate passed).

## Round-2 scope

- [x] MINOR 1: fresh nonce for every new document loaded from a patched record.
  `freshNonceRecord` (extension.ts ~667) runs only when `recordKeepsLoadedNonce` is set and the
  nonce is not empty. It swaps the nonce in the record through `reuseNonce` (`replaceAll`), then
  clears the flag. Call sites:
  - `setPanelHtml`: it also swaps the nonce in the `html` argument, which comes from the old record
    (status, properties table, deferred full update).
  - Patch-fallback timer (`armContentPatchFallback`).
  - Reload of a recreated webview (`previewReady` + `reportsReloadedDocument`).
  The other `assignWebviewHtml` sites either load a fresh render (new nonce from the render) or
  replace the record with a status page whose nonce is `""` (pending clear, missing source,
  initial). `assignWebviewHtml` resets the flag on every full load.
- [x] The patch path keeps the loaded nonce. In `updatePreview` the record gets
  `reuseNonce(html, webview.nonce, previousNonce)`. In the deferred patch, the record is built from
  the patched record, so it already carries the loaded nonce. `postContentPatch` sets the flag.
- [x] Unpatched flows are unchanged. With the flag false, `freshNonceRecord` returns undefined and
  `setPanelHtml` behaves as at base.
- [x] CSP and script tags stay consistent. `replaceAll` on a long random nonce rewrites both the
  `'nonce-…'` source in the CSP meta and every `nonce="…"` attribute.
- [x] MINOR 2: the unit test "T34: pending block navigation resumes after a content patch" is
  present (scrollSync.test.ts:5915).
- [x] NIT 4: the comment in `postContentPatch` is present.
- [x] `previewEditing.test.ts` has no diff against base.
- [x] The RI-T34 nonce check proves a new document. It waits until the record's nonce differs from
  `nonceBefore` (read from the patched page's script), then needs a frame whose `script[nonce]`
  equals the new nonce. A patch never changes a loaded script's nonce, so only a new document can
  satisfy this, even when VS Code reuses the Frame. Dropping `isDetached` and the page marker is
  therefore acceptable.
- [x] No round-1 or pre-existing assertion was weakened. The only removed line in
  realInput.test.ts is the `scenarioPendingOverlayWithoutReload` call. It is now wrapped in
  `withIncrementalUpdates(false, …)`, which keeps that scenario's original no-patch semantics
  (accepted in round 1).

## Findings

None new. MINOR 3 remains a follow-up.

VERDICT: PASS
