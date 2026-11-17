# T35 implementation — round 1

STATUS: DONE

## Summary
User-facing "Sphinx" wording removed from the two navigation notifications. Status pages now carry
`data-sphinx-preview-status-page` on `<body>`. Title and message are block-level (message gap
0.25em) only on status pages and on non-pending banners; the pending banner above rendered content
stays one line. Lint test, CSS test and RI-T35 added. README sentences reworded.

## Files changed
- src/extension.ts — two notification strings reworded
- src/preview/webview.ts — `<body data-sphinx-preview-status-page>` in buildStatusWebviewHtml
- src/preview/previewStyles.ts — scoped two-line rules in PREVIEW_ACCESSIBILITY_CSS
- README.md — two sentences no longer describe a Sphinx build
- test/security/userFacingText.test.ts — new
- test/webview/previewStyles.test.ts — new scoping test
- test/integration/stockCoexistence.test.ts — added body-marker and strong/message assertions
- test/integration/realInput.test.ts — RI-T35

## Inventory (`rg -n "Sphinx" src`)
- User-facing: extension.ts `Sphinx preview navigation blocked: …`, `Sphinx preview could not open …` (both fixed).
- Internal, unchanged: identifiers/comments in extension.ts, propertiesTable.ts, previewStyles.ts
  comments, `rewriteSphinxHtml`, html-sanitizer.ts.
- `src/build/sphinxBuild.ts` has user-visible-looking error strings ("Sphinx preview is disabled…",
  "Sphinx exited with…") but is outside Allowed files, is not scanned, and `buildSphinxSnapshot`
  is not imported anywhere in src (legacy dead path). Left alone; follow-up candidate.
- `src/render/*.ts`: no hits.

## Tests written first (failing before the fix)
- "no user-facing string literal mentions Sphinx" — `actual: [ 'src/extension.ts:1755: Sphinx preview navigation blocked:', 'src/extension.ts:1819: Sphinx preview could not open' ]`
- "status titles and messages are block-level only on status pages and non-pending banners" — failed (no block rules existed)
- stockCoexistence body-marker assertion — trusted gate T35-prefix-trusted.log: assert.match on `<body data-sphinx-preview-status-page>` failed against `<body><aside …`
- RI-T35 — was added in the same pre-fix run but the suite stops at the first failure (stockCoexistence runs earlier), so its own pre-fix failure was not recorded separately.

## Tests added or changed
- userFacingText.test.ts: tokenizer test (comments skipped, templates scanned) plus the scan of extension.ts, webview.ts, render/*.ts; empty allowlist.
- previewStyles.test.ts: every block rule on status selectors is scoped by `[data-sphinx-preview-status-page]` or the pending `:not()` guard; margin rule present.
- stockCoexistence.test.ts: body marker and `<strong>…</strong><span data-sphinx-preview-status-message>` order.
- RI-T35: deletes the source with `vscode.workspace.fs.delete` after a 2 s settle, finds the status frame
  by the body marker (status pages are not "current frames" for the harness), asserts no "Sphinx" and title/message on two
  lines, captures `35-status-two-lines` with `required: ["status-two-lines"]`, restores the file, waits for the rendered heading.
  Deviation: `fs.rmSync` was not used because the watcher missed it when the fixture was fresh (create+delete coalesced); the 2 s settle was needed and fixed it. Three earlier runs timed out before that.

## Existing assertions changed
- none (stockCoexistence only gained assertions).

## Verification
- `gate.sh T35-impl unit types contracts trusted visual` → compile/unit/types/contracts PASS; trusted PASS
  (logs/T35-impl-trusted.log); visual: PASS vs baseline (0 new failure lines, 0 baseline now passing, 0 moved), log logs/T35-impl-visual.log, screenshots logs/visual-T35-impl.

## Evidence for reviewers
- RI-T35 capture 35-status-two-lines under .artifacts (real-input evidence).

## Open points
- A stale unrelated zsh process (pid 92047, 8 h old) mentions scrollSync.ts swapping; not mine, not touched.
- sphinxBuild.ts strings: see inventory.
