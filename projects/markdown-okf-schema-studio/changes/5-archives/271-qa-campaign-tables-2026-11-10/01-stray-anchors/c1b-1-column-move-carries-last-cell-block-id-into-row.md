# A column move carries the block id at the end of a row into the middle of the row

Severity Medium · Reproduced · Verdict Gap · Requirements: none found (SwRS-MDOKFSTUDIO-TABLE-007 says the column moves "in every row as one source edit", nothing about a token written at the end of a row; TABLE-002 same for rows) · Area Tables · Anchors · Side preview ·
c1b-1 · Replay `scenarios/271-c1b-1-column-move-carries-last-cell-block-id-into-row.json`

## Currently / Expected

Buffer defect, no useful picture. Fixture `synth/anchors-trailing-tokens.md`, table T2, column handle of "Note", Alt+Left (same with the mouse drag; also seen in C1 on `anchors-tables.md`).

Currently (buffer diff):

```diff
-| Name | Value | Note |
+| Name | Note | Value |
 | --- | --- | --- |
-| alpha | 1 | first ^row-b |
+| alpha | first ^row-b | 1 |
```

Expected (source: Obsidian convention, a block id ends its line; and the author's wording "anchors in the middle of a table"):

```diff
-| Name | Value | Note |
+| Name | Note | Value |
 | --- | --- | --- |
-| alpha | 1 | first ^row-b |
+| alpha | first | 1 | ^row-b
```

(or the move is refused for that table, or the token is left in the last column.)

## Why this is wrong

The author wrote `^row-b` at the end of the row to name that row. A column move is a layout action: it must not change which text names the row. Today the token is read as cell text, so it travels with the "Note" column and ends up in the middle of the row, and a link to `^row-b` is no longer on the row. The diff shows no warning and no sign that content changed. It is a silent change of the author's content, so Medium.

## Steps to reproduce

1. Fixture `synth/anchors-trailing-tokens.md` (new in `assets/synth/`), open it, Open Preview to Side, edit mode on.
2. Click the column handle above "Note" in table T2, press Alt+Left (or drag the handle onto "Value").
3. `q spy --diff anchors-trailing-tokens.md --against mark`: the diff above.

## Consequence checked

The table still parses, every cell and every paragraph still opens an editor, no console error, Meta+z x4 and Meta+Shift+z x2 are exact, save then reload keeps the moved text. Four moves back and forth keep the token inside the same cell (it never leaves the cell, it moves with it). Not reproduced: a blocked page. Trailing spaces after the closing pipe and `<a id="x"></a>` in the last cell behave the same way (they move with the cell; the trailing spaces stay on the line).

## Impact

A row id, a `<a id>` anchor or a `{#id}`-like token written in the last cell changes position after a column move, and the author may not notice.

## Where it comes from

`src/page/modules/markdownTable.ts` `moveColumn`, around line 331: the last cell text is moved whole, the token is part of it.

## Suggested direction

- (x) Leave the token where it is: a trailing `^id` of the last cell stays at the end of the row after a column move
- ( ) Refuse the move for a row that carries such a token, and say why
- ( ) Leave as is and document it

## Test to add

Real-input E2E: T2 above, Alt+Left on the Note handle, assert the diff keeps `^row-b` at the end of the row.

Uncheck to disagree: [x]

## Requirement to write or change

TABLE-007 (and TABLE-002): the extension SHALL keep a block id written at the end of a row at the end of that row when a column moves.

Uncheck to disagree: [x]

## Done when

- [ ] The replay scenario passes.
