# Charters, campaign 271 (tables usability), 2026-11-10

Scope (owner): Markdown tables and the front matter (properties) table only. Aim at what the e2e
campaign does not assert. Already automated (do not re-explore as is; change corpus or state):
realInput "table cell enter", "table cell bold", "table minimal diff", "table tab", "table toolbar",
"wide table tab", "flush cell and frontmatter", "properties table without reload", "frontmatter value
minimal patch", "frontmatter structural minimal patch", "field blur minimal diff", "refused value keeps
editor usable", "schemaless number commits", "link hint matches table"; machine checks table_move,
table_toolbar_tall, table_menu_above_handles, handles_above_row, table_row_colours, properties_table,
cell_bar_formatting, cell_editor_chrome, cell_end_key, width_modes, width_mode_break, width_mode_scroll.
Revision under test: 293366d0 (origin/main, clean). Corpus: QA workspace (synth/, fixtures-visual/,
fixtures-qa/, docs/). No vault, no book.

## Group A (QA Driver A, 1 window at a time)

### C1 — Stray anchors that block editing (owner report, no steps known) — RUN FIRST
- Mission: reproduce "anchors that ended up in the middle of text or of a table and blocked editing
  of the whole page". Find a sequence of ordinary author actions that (a) writes an anchor-like
  token into the wrong place of the buffer (inside a paragraph or a table row), or (b) leaves an
  anchor/marker element in the preview that sits over text or cells, and after which editing is
  blocked page-wide (no block or cell opens, every click refused, a "blocked" reason shown, or
  edit mode stuck).
- Leads, in this order:
  1. The edit action "Insert label" (src/page/modules/inlineEditActions.ts `insertLabel`, writes
     `(label-name)=` above the first line of the edited text) used from a table CELL editor, from a
     paragraph that follows a table, from a list item, from a heading; then from the slash menu /
     edit palette / shortcut. Does `(name)=` land inside the table source? Does the table break?
  2. The label anchor icon and its rename popover (src/page/modules/labelRename.ts,
     src/core/render/mystInlineTransforms.ts): `(label)=` right above a table, above a paragraph
     next to a table; rename while a cell editor is open; popover left open or pending
     (answerTimeout 6 s) — does it block other editors (`blockedReason`)?
  3. Comment anchors and thread markers (review comments, PR #251/#328/#329): a comment on text
     inside a table cell, on a row, across cells; then edit that cell, add/move/delete the row,
     undo; do marks/chips end up over other text or in the wrong cell; can you still edit?
  4. Heading anchors `{#explicit-id}`, Obsidian block ids `^block-id` at the end of a row or of a
     paragraph next to a table, raw `<a id="x"></a>` in a cell; edit, move rows, undo.
  5. Row add/move/delete + Meta+z in the source, then re-open cells: does any marker drift.
- Corpus: write a new synthetic fixture `synth/anchors-tables.md` (save it to
  $SK/assets/synth/ too) with labels, comments sidecar, block ids, heading ids around and inside
  tables; plus synth/review-threads.md, synth/tables.md, synth/c5-tables.md.
- Oracles: `spy --diff` against mark after every action (where did a token land), `errors`,
  whether a click on another paragraph/cell still opens an editor afterwards (explicit check),
  overlap of marker elements with text (box checks).
- New feature: PR #251, #328, #329 (comment marks/editor) only as they touch tables.
- Budget: 40 driver calls, 6 screenshots, 45 minutes. Session: c1 (workspace ws-c1).
- Group/sheets folder: 01-stray-anchors/

### C3 — Table structure editing beyond the fixture
- Mission: add/delete/move rows and columns with the table toolbar, the handles (PR #285 handles
  on real edges) and drag (PR #295), on tables the e2e fixtures do not have: escaped pipes and inline
  code with `|`, alignment row `:---:`, empty cells, a one-column table, a table at end of file with
  no trailing newline, a table right after a list or inside a blockquote/admonition, a CRLF file
  (synth/crlf.md, add a table if needed), a 30-row table. Then undo/redo from the source editor
  (Meta+1, Meta+z) and from the preview; re-open a cell after undo.
- Oracles: diff against mark (only the touched rows change, alignment row and padding kept),
  errors, handles in viewport and aligned with the row (box), selection/active cell after undo.
- New feature: PR #285, #295.
- Budget: 40 driver calls, 6 screenshots, 45 minutes. Session: c3. Folder: 02-table-structure/

### C6 — Concurrency and time on tables
- Mission: a cell editor open while (a) the same row is edited in the source editor, (b) the file
  is rewritten on disk (external tool), (c) the file is saved (Meta+s) or auto-saved, (d) the
  preview re-renders from another block's change; fast typing then Tab/Arrow immediately
  (debounce); rapid Meta+z / Meta+Shift+z after several cell commits; the same table in two views
  (side preview + "Open With" editor). Check the buffer for lost or doubled text and that editing
  still works afterwards.
- Oracles: diff against disk and mark, errors, `[nav]` count in console.log (full reloads),
  explicit "another cell still opens" check.
- Budget: 40 driver calls, 6 screenshots, 45 minutes. Session: c6. Folder: 04-table-concurrency/

## Group B (QA Driver B, 1 window at a time)

### C2 — Today's table fixes and the wide-table line (new features) — RUN FIRST in group B
- Mission: PR #337 (a cell left with Tab, Shift+Tab or an arrow shows the text you typed) and PR
  #338 (a wide table keeps its Auto breakout while a cell is edited), plus the wide-table line
  #272 (sideways scroll kept across Auto re-measures), #273 (cell editor kept in view moving
  through a wide table), #301 (table in the column when it fits, breakout when it needs to), #306
  (open cell editor kept in view when its table leaves the breakout). Vary what e2e does not: leave
  with Shift+Tab, ArrowUp/Down at the first/last row, Enter, Escape after typing (must cancel),
  a click on another cell, a click outside; type markup (`**b**`, `` `x|y` ``, a pipe `|`, a
  trailing space); a cell whose new text makes the table switch between column and breakout;
  change the width mode (toolbar) while a cell is open; narrow the pane with the sash while
  editing; the last cell of the last row + Tab.
- Corpus: synth/c7-wide.md, synth/c5-tables.md, synth/tables.md, fixtures-visual wide tables.
- Oracles: diff against mark, inViewport of the cell editor, the shown cell text equals the
  buffer, horizontal scroll position before/after, errors.
- New feature: PRs #337, #338, #272, #273, #301, #306.
- Budget: 40 driver calls, 6 screenshots, 45 minutes. Session: c2. Folder: 03-table-cell-editing/

### C4 — Front matter properties table
- Mission: use the properties table as an author: PR #282 collapse/expand (state across edits,
  reloads, switching documents, with a field editor open), PR #245 (refused value), #246
  (schema-less number from the YAML box), #247 (link list editor on files the table resolves); edit
  strings with `:`/`#`/quotes, lists, booleans, dates, empty values, multiline values; add, remove
  and reorder fields; Tab/Shift+Tab/Escape/Enter between fields; undo from the source; a document
  whose front matter has comments or odd indentation (synth/frontmatter-edge.md,
  synth/vault-props.md, fixtures-visual frontmatter fixtures).
- Oracles: diff against mark (minimal YAML change, comments and key order kept), errors,
  collapse state, explicit "another field still opens" check.
- New feature: PR #282, #245, #246, #247.
- Budget: 40 driver calls, 6 screenshots, 45 minutes. Session: c4. Folder: 05-frontmatter-table/

### C5 — Table reading, judgement and clipboard
- Mission: judge tables as a reader and author: PR #317 tints (heading, even rows, hovered row) in
  light and dark themes and with the edit-mode chrome; long cell text wrapping; very wide and very
  narrow panes; tables next to the TOC rail (#287/#333 only as they touch tables); copy a row or
  cells from the preview; paste multi-line text, tab-separated text (from a spreadsheet) and a
  Markdown table into a cell editor; select text across cells; keyboard discoverability (how do I
  add a row without the mouse?); find (Meta+f) text inside a table and edit the hit.
- Oracles: diff against mark after pastes (no broken row: a newline in a cell must not split the
  row), visual judgement shots, errors.
- New feature: PR #317.
- Budget: 40 driver calls, 6 screenshots, 45 minutes. Session: c5. Folder: 06-table-reading-clipboard/

### C0 — No-op sweeps on tables
- Mission: `noop-sweep.mjs <file> cells` and `fields` (and `blocks` for the table neighbours) on
  synth/tables.md, synth/c5-tables.md, synth/c7-wide.md, synth/frontmatter-edge.md,
  synth/vault-props.md, the new synth/anchors-tables.md if C1 created it, and 2 fixtures-visual
  files with the most tables (`grep -c '^|'`). `--limit 30` slices. Reproduce each CHANGED once.
- Budget: 40 driver calls, 25 minutes. Session: c0. Folder: 07-sweeps/
