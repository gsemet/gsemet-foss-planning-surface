# UX-02 — Inline typing creates one source undo step per character

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced (spy extension recorded every `onDidChangeTextDocument` event) |
| Area | Inline block editing |
| Modes | Side preview and Open With |
| Evidence | Change log: 52 typed characters produced 52 document versions, each replacing lines 134-138 |

## Use case

An author edits a paragraph in the preview, then moves to the source editor and presses Cmd+Z to
take the whole edit back.

## Steps to reproduce

1. Side preview on `book/chapters/02-foundations.md`, edit mode on.
2. Click a paragraph and type a 20-character sentence.
3. Click into the source editor and press Cmd+Z repeatedly.

## Expected

One undo step per editing session (or per word/pause), as in the VS Code text editor, where
consecutive typing is grouped.

## Observed

Each keystroke is posted as `previewEditSave` with `final: false` and applied as a separate
`WorkspaceEdit` that replaces the **whole block** (here 5 lines, about 360 characters). Undo in the
source removes one character at a time: 20 Cmd+Z for a 20-character sentence.

Side effects of whole-block replacement per keystroke:

- the source editor's cursor and selection inside that block are moved on every keystroke;
- decorations, folding, and diagnostics on the block are invalidated each time;
- `onDidChangeTextDocument` listeners (other extensions, Copilot, linters) see a 360-character
  replace per keystroke.

## Where it comes from

- `src/webview/scrollSync.ts` L1716-L1719: `input` → `autosaveBlockEdit()` → `postBlockEditSave(false)`.
- `src/extension.ts` `drainActiveBlockEdit` (L1109-L1156): one `vscode.workspace.applyEdit` per
  pending text, replacing the full block range.

## Suggested direction

Debounce autosave (for example 300-500 ms idle) and send a minimal diff (common prefix/suffix
trimmed) instead of the whole block. Optionally apply the final edit with `undoStopBefore`
semantics so one inline session maps to one undo step.

## Test to add

Unit test on the host edit path: N `previewEditSave` messages within the debounce window produce
one `applyEdit`. E2E: type 20 characters inline, Cmd+Z once in the source, assert the block is
back to its original text.

## Done when

Undoing an inline edit from the source takes one or a few steps, and the edit range is limited to
the changed characters.
