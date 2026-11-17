# Palette actions answer "out of date" once the block editor has autosaved

User decision (2026-10-25): P1, verify first, then fix.

Current behaviour (SwRS-MDOKFSTUDIO-TRUST-065 (was SwRS-MDOKFSTUDIO-PALETTE-181), Known issue; same cause in PALETTE-109, 140, 144,
148, 150, 168, 188, 195, 271; read from the code and covered by a unit test, not run in VS Code):
after the block editor saves anything (autosave after typing, or a palette button), Reference,
Citation, Document link, Image and the figure form's Browse answer "The preview is out of date.
Try again once it has refreshed." until the editor closes. `currentPreviewDocument`
(`src/session/sessionDocuments.ts`) requires the document revision to equal the render revision
the request carries; the autosave moves the document revision and the preview only refreshes when
the editor closes. Pasting an image or rich text is not affected (PALETTE-200, 202).

## Steps

1. Verify in VS Code: edit mode, open a paragraph, type text, wait for the autosave, press
   Reference. Record the result (screenshot).
2. If confirmed: these requests accept the revision produced by the open editor's own saves (the
   way the paste path does), so they keep working while the editor is open.
3. Integration test "type, then Reference/Citation/Image"; update the listed SwRS in the same PR.

Related, not in scope unless the fix covers them naturally: BLOCK-248 and PALETTE-175 (a request
naming an older render is dropped with no answer, so the page waits for its own timeout).

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
