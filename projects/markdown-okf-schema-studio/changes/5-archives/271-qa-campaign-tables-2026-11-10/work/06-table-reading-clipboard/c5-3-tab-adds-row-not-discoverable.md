# Adding a row from the keyboard is not discoverable

Severity Low · Observed once · Verdict Gap · Requirements: SwRS-MDOKFSTUDIO-TABLE-035 (Tab in the last cell adds a row) · Area Tables · Keyboard · Side preview · c5-3 · Replay none (see steps)

## Currently / Expected

| Currently | Expected |
| --- | --- |
| The cell editor labels are only "Done editing" and "Cancel (Esc)"; nothing says Tab in the last cell adds a row. | A short hint or tooltip on the editor (convention: spreadsheets show shortcuts in tooltips). |

No visual: the labels were read from the DOM (`Markdown table cell;Done editing;Cancel (Esc)`).

## Why this is wrong

The behaviour exists and works (TABLE-035; the diff shows one added line `|       |   |`). An author who wants a row without the mouse cannot learn it: the row buttons live in the table bar and need the pointer. Also, Escape after that Tab leaves the new empty row in the buffer although the editor says "Cancel".

**Steps.** `synth/c5-reading.md`, edit mode, click last cell `3`, read the editor labels, Tab: one empty row appears.
**Fix.** Add the shortcuts to the Done/Cancel tooltips or a hint line. Uncheck to disagree: [x]
**Test.** No test: cosmetic hint. Uncheck to disagree: [x]
**Requirement.** none. Uncheck to disagree: [x]
