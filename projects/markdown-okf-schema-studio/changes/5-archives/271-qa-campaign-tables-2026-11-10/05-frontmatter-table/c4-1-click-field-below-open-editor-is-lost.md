# Clicking a field below an open properties-table editor does nothing

Severity Medium · Reproduced · Verdict Gap · Requirements: none found for an unchanged editor (SwRS-MDOKFSTUDIO-FMEDIT-019 only specifies the refused-value and changed-value cases) · Area Front matter table · Side preview · c4-1 · Replay `scenarios/271-c4-1-click-field-below-open-editor-is-lost.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![currently](../evidence/c4-1-currently.jpg) | ![expected](../evidence/c4-1-expected.jpg) |
| Title editor open (unchanged), click on the notes cell: no editor opens, the buffer is unchanged. | The same click on a field above the open editor opens that field at once (in-product working case; FMEDIT-019 also wants the clicked field to open "in the same click" after a refusal). |

## Why this is wrong

An author who opened a field and wants another one clicks it. The open editor row is 108 px high (31 px closed), so on mouse down the editor closes on blur, the rows below move up about 77 px and the mouse up lands on another row: the click is swallowed and the author must click a second time. It only happens towards fields below, never above, so it looks random. The refused-value case already promises that the click opens the other field; the plain unchanged case does the same thing wrong. Changed-value case: FMEDIT-019 says that click saves and opens nothing, so it is not reported.

## Steps to reproduce

1. Fixture `synth/frontmatter-edge.md`, side preview, edit mode.
2. Click the `title` value cell (editor opens, row grows 31 -> 108 px), then click the `notes` value cell: nothing opens. Same for summary -> notes, title -> summary, title -> priority. Reverse direction (notes -> title) works.

## Impact

Every move to a lower field costs a second click; the layout shift makes the first click land on a different row.

## Where it comes from

Editor close on blur in `src/page/features/frontmatterValueEditor.ts` (blur handler, around line 280) changes the row height before the click completes.

## Suggested direction

Open the clicked field on mouse down (as the refused-value path does), or keep the editor row height equal to the closed row.

Uncheck to disagree: [x]

## Test to add

Real-input E2E: open a field editor, click a field below it, assert its editor is open (extend scenarioRefusedValueKeepsEditorUsable).

Uncheck to disagree: [x]

## Requirement to write or change

Extend FMEDIT-019: WHEN the writer clicks another field's cell while an editor holds an unchanged value, the clicked field's editor SHALL open in the same click.

Uncheck to disagree: [x]

## Done when

- [ ] Title -> notes, summary -> notes and title -> priority each open the target field with one click.
- [ ] The replay scenario passes.
