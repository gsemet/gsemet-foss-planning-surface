# Specification: 420-edit-mode-slow-large-docs

## Summary

Remove the forced layouts that grow with the size of the document in edit mode, without changing
what the reader sees.

## Scope

1. `src/page/features/tableRowMove.ts`: place the handles in phases (clear the shifts, read the
   table edges, set the shifts, read every box, then write every handle style). The table box is
   read once per table per pass, not once per handle.
2. `src/page/features/scrollCore.ts`: `markWideTables` marks the short cells, then reads all the
   overflows, then writes all the flags.
3. `src/page/features/blockSourceEditor.ts`: the caret is revealed on `input`; `keyup`, `mouseup`
   and `select` reveal it only when the text length, the selection or the scroll changed since.
4. `src/page/modules/widthMode.ts`: the editing observer measures again only when the edited
   block is a top-level block that can break out (table, figure, image, code block, Mermaid
   diagram, paragraph holding an image).

## Tests

Each test fails on the code before the change:

- `test/page/runtimeTableRowMove.test.ts`: 14 handles, the table box is read 6 times (45 before).
- `test/page/tableBreakout.test.ts` (real Chromium): an editor on a paragraph measures nothing; on
  a table it measures and the table leaves the breakout.
- `test/page/runtimeEditPalette.test.ts`: the key release of a typed key does not measure the
  caret again; a caret move does.

Requirements: verification lines in SwRS-LAYOUT-023 (plus one scenario row), PALETTE-021,
TABLE-002; no normative change.

## Out of scope (follow-ups)

- The `beginEditAnchor` read after inserting the editor (anchoring needs it).
- `syncPaletteSticky` and `resizeTextarea` ordering on the typing path.
- Lazy insert bars, `content-visibility: auto` (breaks rect-based scroll sync), `:has()` rules.
- Caching `topLevelMappedBlocks` and debouncing `stabilizeLayout`.
