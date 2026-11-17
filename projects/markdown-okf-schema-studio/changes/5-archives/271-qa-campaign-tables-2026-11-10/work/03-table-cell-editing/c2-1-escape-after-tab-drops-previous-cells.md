# Escape in the next cell silently drops the text of the cells left with Tab, an arrow or a click

Severity High · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-TABLE-035, SwRS-MDOKFSTUDIO-TABLE-013, SwRS-MDOKFSTUDIO-TABLE-025 · Area Tables · Side preview ·
c2-1 · Replay `scenarios/271-c2-1-escape-after-tab-reverts-previous-cell.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![currently](../../evidence/c2-1-currently.jpg) | Buffer defect: two code blocks below. |
| After "alpha" + ` X`, Tab, Escape the preview still shows "alpha X" but the buffer says `\|alpha\|1\|`. | The buffer and the preview agree (source: TABLE-035, the cell left shows the text just typed; the shown cell text equals the buffer). |

Today, after Tab then Escape in the next cell (buffer vs the state before the edit):

```diff
(no change; the typed " X" is gone from the buffer, the preview cell still reads "alpha X")
```

Expected, either of the two (owner's choice, see Decision below):

```diff
- |alpha|1|
+ |alpha X|1|        <- Escape only cancels the cell it was pressed in
```

or the preview cell goes back to "alpha" when Escape restores the original table.

## Why this is wrong

An author types in a cell, presses Tab to go on, then presses Escape in the next cell to cancel only that second cell (or just to leave the editor). The preview keeps showing the first cell's new text, so the author believes it is saved, but the buffer has silently lost it: a save writes the old text. This breaks the invariant that the shown cell text equals the buffer, and TABLE-035 says the cell left shows the typed text. TABLE-013 keeps one edit session across cells and TABLE-025 only says Escape drops "the typed text", so the whole-session cancel may be intended, but then the preview must follow the buffer. Same loss after ArrowRight and after a click on another cell; Enter in the next cell keeps the text.

## Steps to reproduce

1. Fixture `synth/tables.md`; open it, Open Preview to Side, edit mode on.
2. Click the cell `alpha`, End, type ` X`, press Tab (the editor moves to the cell `1`; buffer and preview show `alpha X`).
3. Press Escape in the cell `1`.
4. Compare: the preview cell reads `alpha X`; `q spy --diff synth/tables.md --against mark` shows no change.

Variants on `synth/c5-tables.md` (clean clone, same result): typing in two cells with Tab Tab Escape drops both; typing, clicking another header cell, Escape drops the first; typing, ArrowRight, Escape drops it; Tab then Enter keeps it.

## Impact

Silent loss of typed table text with a preview that claims otherwise; the author finds out only after reopening the file.

## Where it comes from

Escape calls the cancel path that asks the host to restore the original table of the session (`restoreTableCellContent` in `src/page/features/tableCellEditor.ts` around line 80 is the neighbour), while the cell left keeps its locally rendered text. Code reading is partial, at commit `293366d0`.

## Suggested direction

- (x) Escape cancels only the edits made in the open cell, or the shown text of every restored cell is redrawn from the buffer
- ( ) Keep whole-session cancel, but redraw all cells touched by the session from the restored table
- ( ) Leave as is

## Test to add

Real-input E2E: type in a cell, Tab, Escape; assert the shown text of the first cell equals the buffer line (diff against the mark).

Uncheck to disagree: [x]

## Requirement to write or change

Amend SwRS-MDOKFSTUDIO-TABLE-025: state whether Escape drops only the open cell's text or the whole session, and that the preview shows what the buffer holds after a cancel.

Uncheck to disagree: [x]

## Done when

- [ ] After Tab then Escape the preview and the buffer agree for every cell of the table.
- [ ] The replay scenario passes.
