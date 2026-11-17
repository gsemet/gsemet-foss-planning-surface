# Report: CR 299, the visual campaign export draws Mermaid diagrams

- PR #369, merged by the owner on 2026-11-12 09:25 UTC, merge commit 0e79699d (one commit).
- What landed (test and campaign only): `test/visual/drawnContent.ts` draws the static page with the product's Mermaid page script in headless Chromium; `writeExportFile` feeds that drawn content to the product's `buildHtmlExport`; `capture_export_html.py` asserts the drawn image (`img.myst-mermaid-image`, `data:image/svg+xml`), the closed "Diagram source" and no script; v42/v43 descriptions updated.
- Verifier: VERIFIED at 21606f26 (`work/verifier/T1-r1.md`). Inspector (Opus): two low findings, fixed in the amend.
- Spec point 3 (labels at the top of boxes): not reproduced in the campaign (centred in preview and export, same SVG); nothing changed. Follow-up: P3 `mermaid-labels-top-in-real-export`.
- Not run: the heavy real VS Code run (no product code touched).
