# T37 review — round 1

Base: 9659cda · Reviewed diff: 7 files, +22/-14 (approx.)

## Gates
unit, types, contracts: PASS (logs/T37-impl-*.log). full: PASS, exit code 0 (logs/T37-impl-full.log),
including the reload campaign that locates the tab by `Studio · reload-evidence.md`. No new
failure compared with the T00 baseline.

## Done-when
- [x] Custom editor displayName is `MyST + OKF Studio`; extension displayName unchanged — evidence:
  package-contract.test.ts (red log T37-red-unit.log, then green).
- [x] Side preview tab reads `Studio · <file>` — evidence: lifecycle.test.ts new assertion
  `getActivePreviewPanelForTests()?.title === "Studio · preview.md"` (red log T37-red-trusted.log);
  reload campaign locator finds the restored tab by that exact aria-label.
- [x] Open With editor tab reads the basename — evidence: code reading. `resolvePreviewEditor` calls
  `createPreview(..., undefined, false)`, so `previewTitle` returns the basename; `updatePreview`
  and `switchPreviewDocument` go through the same helper with the preview's own flag.
- [x] `unit` and `full` gates pass.

## Title assignments checked
- `updatePreview` (every render): `previewTitle(preview, activeDocumentPath)`.
- `switchPreviewDocument` (side preview follows another file): `previewTitle`.
- `createPreview`: `previewTitle` or `"Studio"` when there is no document; covers the
  replacement path in `switchPreviewDocument` (passes `followsActiveEditor` through), Open With
  (`false`), `openPreview` (default `true`), `deserializePreviewPanel` (default `true`, correct:
  only side previews are serialized).
- `openPreview` initial `createWebviewPanel` title: `"Studio"`.
- Early-return status paths in `resolvePreviewEditor` / `deserializePreviewPanel` do not set a
  title (unchanged behaviour; VS Code keeps the editor/restored title).
- No code path still produces `Markdown OKF-Schema Studio: <file>`; `rg "OKF-Schema Studio:"`
  only matches command titles (palette, contract test, reload-suite command calls).

## Tab locators
Only `test/integration/reload-suite.ts:98` locates a tab by title; updated. `test/visual/capture.py`
has no title locator. Other `aria-label` matches are webview content, unaffected.
U+00B7 bytes (`c2 b7`) verified identical in extension.ts, lifecycle.test.ts, reload-suite.ts,
README.md and AGENTS.md.

## Protected features checked
Must-not-change: extension displayName, command titles, viewTypes, configuration title — unchanged
(contract test still asserts command titles and viewType). Reload/restore of the side preview —
covered by the full reload campaign (PASS). Open With editor — viewType/priority unchanged,
contract test.

## Findings
1. [MINOR] test/integration (no file) — the Open With basename title has no integration assertion.
   The path is a one-line ternary shared with the tested side-preview path, so I do not block on it.
   Follow-up: in an integration test that opens `vscode.openWith(uri, "markdown-okf-schema-studio.editor")`,
   assert the resulting panel's `title === "<basename>"` if a test hook to reach that panel exists.
2. [NIT] src/extension.ts:createPreview — a restored side preview whose source is missing shows
   `Studio` (no file name), same information level as before. Could use
   `restoredState.sourceFile` basename later.

AGENTS.md: only the Identity bullet changed, and it is accurate (extension name, custom editor
name, side preview tab form, viewType, priority). README: picker row, tab titles and the
"what Studio adds" sentence are present.

## Existing assertions changed
- package-contract.test.ts customEditors displayName — OK (listed, D-14).
- reload-suite.ts tab locator — OK (listed, D-15).

VERDICT: PASS
