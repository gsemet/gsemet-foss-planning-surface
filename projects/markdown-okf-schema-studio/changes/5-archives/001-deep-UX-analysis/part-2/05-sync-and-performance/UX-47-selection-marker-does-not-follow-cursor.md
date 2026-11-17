# UX-47 — `markEditorSelection` does not follow the cursor

| Field | Value |
| --- | --- |
| Severity | Medium (feature does not do what its setting says; off by default) |
| Confidence | Reproduced; code confirms |
| Area | Editor ↔ preview synchronization |
| Evidence | [p2-settings.jpg](../evidence/p2-settings.jpg) (cursor on line 323, preview marks lines 313-314) |

## Steps to reproduce

1. Set `"markdownOkfSchemaStudio.preview.markEditorSelection": true`.
2. Open `book/chapters/08-research-plan-implement.md` with the side preview.
3. Click line 313, then line 323, then press ArrowDown five times, without scrolling.

## Observed

The preview keeps marking the paragraph of lines 313-314. The marker moves only when the editor
scrolls or the preview re-renders.

The marker outline is orange (`rgba(234, 92, 0, 0.33)`), close to the error colour used by the
properties table, so a marked block looks like a block with a problem.

## Where it comes from

`src/extension.ts` sends `selectionLine` only from `syncEditorToPreview` (visible-range changes)
and `markEditorSelectionInPreview` (on `previewReady`). `activate` does not subscribe to
`vscode.window.onDidChangeTextEditorSelection`.

## Suggested direction

Subscribe to selection changes (throttled), post the selection line, and use a neutral accent for
the marker (the editor's line highlight colour).

## Done when

The marker follows the caret within one frame of a cursor move.
