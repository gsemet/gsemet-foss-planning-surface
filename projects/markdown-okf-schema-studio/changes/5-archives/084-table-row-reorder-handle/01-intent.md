# Reorder table rows with a handle in edit mode

User idea (2026-10-23): in edit mode, each table row shows a grab handle ("anchor") on its left
side, so rows can be reordered easily by drag and drop.

- Same mark and behaviour as the reorder handle of the frontmatter list editor
  (`.okf-list-editor-item`, drag code in `src/webview/scrollSync.ts` around `listDragInProgress` /
  `draggedRow`, styles in `src/preview/previewStyles.ts` around `data-okf-list-dragging`): reuse
  it rather than inventing a new one.
- When the table spans the full column width, keep enough left margin for the handle so it never
  overlaps the table or is clipped.
- Only in edit mode; the header row is not movable.

To decide at grill time:
- the source edit: move the Markdown row lines (GFM pipe tables); MyST `{list-table}` rows too?
- keyboard alternative (e.g. Alt+Up/Down on a focused row, like block move up/down);
- one undo step per move; the open cell editor and comment chips survive the move;
- tests: unit for the row move on the source, visual scenarios (handle visible, full-width table
  margin, dragging state) light/dark/cream, a real-window drag if feasible.

Priority P2 set by the main session (user did not state one; may change).
