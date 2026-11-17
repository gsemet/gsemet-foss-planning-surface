# UX-12 — Editing one table cell rewrites the formatting of the whole table

| Field | Value |
| --- | --- |
| Severity | High |
| Confidence | Reproduced (diff of buffer against the file on disk) |
| Area | Table cell editing |
| Evidence | [u13-cell-tab.jpg](../evidence/u13-cell-tab.jpg) (source line 54 reformatted) |

## Use case

An author fixes one value in a table from the preview and commits the change with Git.

## Steps to reproduce

1. Side preview on `fixtures-visual/04-code-and-tables.md`, edit mode on.
2. Click the "North" cell of row `nw-02` in "A very wide table", type ` Pole`, press Enter.
3. Diff the buffer against the file on disk.

## Observed

```diff
-|-------|--------|------|--------|--------------|...|----------|
+| ------- | -------- | ------ | -------- | -------------- |...| ---------- |
-| nw-02 | North | 9 | 2 | no | ...
+| nw-02 | North Pole | 9 | 2 | no | ...
```

The delimiter row is rewritten although the user did not touch it. The serializer emits every row
as `| cell | cell |` with exactly one space, so:

- compact delimiters (`|---|`, the style used across `book/chapters/`) gain spaces;
- aligned tables lose their padding on **every** row (for example `| first    | second   |` in
  `02-admonition-gallery.md` would become `| first | second |`);
- any cell-level edit therefore produces a whole-table diff.

## Expected

Only the edited cell changes; all other bytes of the table are preserved.

## Where it comes from

`src/webview/markdownTable.ts` `serialize` (L85-L88) rebuilds every line from the model. The unit
tests only round-trip tables that already use the canonical `| --- |` style
(see [QA-01](../08-test-campaign-gaps/QA-01-roundtrip-fixtures-match-serializer-style.md)).

## Suggested direction

Keep the original line text in the model and re-serialize only rows that changed. For a changed
row, replace only the edited cell's text between its pipes, preserving surrounding padding (or
re-pad to the column width when the table was aligned).

## Test to add

Unit: parse → edit one cell → serialize on compact (`|---|`) and padded/aligned tables; assert that
only the edited line differs. E2E: same through real typing in the preview.

## Done when

`git diff` after a cell edit shows exactly one changed line.
