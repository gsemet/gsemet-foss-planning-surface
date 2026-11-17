# A radio click while a block editor is open writes to the source instead of being refused

Severity Medium · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-GFM-039 (refusal table: "a click while a block or frontmatter editor is open: no message; the editor status reads 'Save or cancel this edit before choosing an option.'"), SwRS-MDOKFSTUDIO-BLOCK-041 · Area Radio choice lists, guards · Side preview · c7-1 · Replay `scenarios/c7-1-radio-click-with-open-editor-writes.json`

## Currently / Expected

```text
Currently: edit mode, editor opened on "## Tasks", then a click on the "Alt+click" option of the
group above. Editor closes, source changes by two lines (diff against mark: -2 +2 at L9), no message.
```

```text
Expected: the editor stays open, nothing is written, the editor status reads
"Save or cancel this edit before choosing an option." (GFM-039).
```

No Currently JPEG: the symptom is a buffer diff (the charter ran out of budget for a shot).

## Why this is wrong

An author who is mid-edit expects one edit at a time (BLOCK-041). Here a stray click on a radio both
discards the open editor and writes a choice the author may not have meant. The refusal row of
GFM-039 says this click must send no message. Seen 4 times (fixture `fixtures-visual/74-radio-plan.md`). The
same click is refused correctly when the radio sits further down in view (third option, editor stays
open, nothing written), so the guard exists but is bypassed when the click first moves or blurs the preview.

## Steps to reproduce

1. Open `fixtures-visual/74-radio-plan.md` in the side preview, edit mode on.
2. Click the "## Tasks" heading: its editor opens.
3. Wheel up a little, then click the second option of "Fix direction" (not the selected one).
4. Observed: editor closed, `(x)` moved, no message. Clicking the third option instead leaves the editor open and writes nothing (correct).

## Impact

Unplanned write plus a lost open edit state, without any explanation.

## Suggested direction

Evaluate the open-editor guard before the editor's blur-commit runs (on mousedown), or treat a radio click as not blurring the editor.

Uncheck to disagree: [x]

## Test to add

Real-input E2E: open a block editor, click an unselected radio that needed a scroll to reach, assert diff unchanged and the editor open.

Uncheck to disagree: [x]

## Done when

- [ ] The replay scenario passes (diff against mark equal, editor still open).
