# Radio click in a read-only file shows the new choice, writes nothing and says nothing

Severity Medium · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-GFM-039 (read-only row: controls aria-disabled with the reason as tooltip; "any refusal: the previous selection and tab stop come back, and the reason shows next to the clicked option"), SwRS-MDOKFSTUDIO-TRUST-005 · Area Radio choice lists, read-only · Side preview · c7-2 · Replay `scenarios/c7-2-readonly-radio-click-silent.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![currently](../../evidence/c7-2-currently.jpg) | Same preview with the first option still selected (as in the source) and the reason shown next to the clicked option; or all controls disabled with a tooltip, as in Restricted Mode. |
| Source says `(x) A click in the margin...`; preview shows "Leave as is" selected. | GFM-039: refusal restores the selection and names the reason. |

## Why this is wrong

With `files.readonlyInclude` on the file, a click on the third option leaves the preview showing it selected
while the buffer (v1, disk) is unchanged. The author believes the decision is recorded; it is not. No toast, no
note, no tooltip, `aria-disabled` absent (Restricted Mode, by contrast, disables all five controls with the
tooltip "Editing requires a trusted workspace." and a click changes nothing). Both the read-only row and the
generic refusal row of GFM-039 are broken. The preview does not treat the file as read-only and the failed
apply is swallowed.

## Steps to reproduce

1. Clone workspace; `.vscode/settings.json` = `{"files.readonlyInclude": {"**/74-radio-plan.md": true}}`; reload window.
2. Open `fixtures-visual/74-radio-plan.md`, side preview, click the third option of "Fix direction".
3. Wait 3 s: option stays selected in the preview, `spy --diff --against disk` unchanged, `notifs` empty.

## Impact

Silent lost decision in a file the author cannot write.

## Suggested direction

Check the document's writability (as the apply result) and on failure restore the selection and show the refusal note; ideally disable the controls up front.

Uncheck to disagree: [x]

## Test to add

Integration: with readonlyInclude set, click an option, assert the shown selection returns to the source's and a reason is visible.

Uncheck to disagree: [x]

## Done when

- [ ] The replay scenario passes.
