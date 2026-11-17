# A table with a token after one row's closing pipe shows move handles that do nothing, and opens in the raw editor

Severity Low · Reproduced · Verdict Gap · Requirements: none found (SwRS-MDOKFSTUDIO-TABLE-001 sends a block that is not an editable pipe table to the raw Markdown editor; TABLE-002 and TABLE-007 do not say handles are hidden then) · Area Tables · Anchors · Side preview ·
c1b-2 · Replay `scenarios/271-c1b-2-token-after-last-pipe-table-handles-inert.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| none: no visible symptom (the handles look normal; only the lack of effect shows). Alt+Left on the Note handle of T1, T3 or T5 leaves the buffer unchanged, and a cell click opens "Raw Markdown editor" (lines 7-11), not the cell editor. | The handles are not offered on a table the editor cannot move, or the move works (source: the same handles work on T2, T4, T6 of `synth/anchors-trailing-tokens.md`). |

## Why this is wrong

With `| alpha | 1 | first | ^row-a`, `{#row-c}` or `<!-- keep -->` after the closing pipe, the table still renders as a table with handles, but the table model refuses it. Column and row moves return silently (no notice), the cell toolbar (Row/Col buttons) is not offered, and each cell click opens the raw editor of the whole table. The author gets controls that do nothing, with no hint why. Nothing is lost, hence Low.

**Steps.** Fixture `synth/anchors-trailing-tokens.md` T1: focus the column handle (Note), Alt+Left: no diff. Click "beta": Raw Markdown editor.
**Fix.** Hide the handles on a table the move refuses, or accept a trailing token after the last pipe. Uncheck to disagree: [x]
**Test.** Real-input E2E: handles absent or move works on a table with `| ^id` after a row. Uncheck to disagree: [x]
**Requirement.** TABLE-002/007: state that handles are offered only on a table the editor can move. Uncheck to disagree: [x]

Not reproduced: a blocked page. Every paragraph and cell still opens an editor, no console error, undo/redo exact.
