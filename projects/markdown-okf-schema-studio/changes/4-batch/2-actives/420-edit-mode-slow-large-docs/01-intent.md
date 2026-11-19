---
type: cr-intent
id: 420-edit-mode-slow-large-docs
description: "Bug: edit mode lags on large documents (hover on the floating toolbar, opening a block editor); fix the layout thrash the issue measures."
generated: {by: "agent:claude-opus", at: "2026-11-19T10:00:00Z"}
sources: [{id: issue, resource: "https://github.com/gsemet/markdown-okf-schema-studio/issues/420", title: "Edit mode very slow on large documents: hover on floating menu/toolbar and opening a block editor lag", author: "github:gsemet", last_modified: "2026-11-19"}]
---

# Edit mode slow on large documents

issue: https://github.com/gsemet/markdown-okf-schema-studio/issues/420

On a long document with many tables, edit mode lags: hovering the floating toolbar and opening a
block editor take visible time. The audit in the issue and its follow-up comment measure the
causes: the row handle placement alternates a box read with a style write for every handle (up
to 76 layouts), and typing forces dozens of layouts on the caret path.

## Known

- `tableRowMove.position()` reads and writes in turn, once per handle.
- `markWideTables` reads `scrollWidth` right after writing to each table.
- Each typed key reveals the caret twice (`input`, then `keyup`).
- The width-mode mutation observer measures every wide block whenever any block enters or leaves
  edit, even a paragraph.
