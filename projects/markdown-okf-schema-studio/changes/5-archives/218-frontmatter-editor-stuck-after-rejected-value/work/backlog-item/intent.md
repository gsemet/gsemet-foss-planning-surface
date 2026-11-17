# A rejected front-matter value strands the field editor and blocks every other field

Severity High · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-FMEDIT-019, SwRS-MDOKFSTUDIO-FMEDIT-020 · Area Frontmatter · Side preview · QA210-01 · Replay `scenarios/c6-1-invalid-commit-strands-editor.json` · P1

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![Priority set to 7, error banner, editor still open](evidence/currently.jpg) | No visual: the defect is about focus and editor state, not layout.<br>Expected: after the rejected commit focus stays in the field (`activeElement` is the `INPUT`), Escape closes the editor, and a click on `title` opens its `TEXTAREA`. |
| *Currently: `priority` set to 7 (schema max 5), the error banner shows and the editor stays open (replay `c6-1` on b9118506: all three focus checks fail, buffer unchanged).* | *Measurements: `D.activeElement.tagName === 'INPUT'` is false after the rejection; the Escape and "another field opens" checks are false too.* |

The Currently shot is the before-shot the fix PR must reproduce.

## Why this is wrong

An author types a value the schema refuses (`7` where the maximum is 5) and gets the right error
message. After that the editor is a trap: focus has jumped to the table cell, so the corrected
value `4` goes nowhere, Escape does nothing and a click on another field opens nothing. The author
must click back into the input before anything works, and nothing on screen says so. The
requirements already say how it must behave: Escape closes a field editor without saving
(FMEDIT-020), and committing posts a save only for a changed value while the editor shows the
outcome (FMEDIT-019). The same defect was first reported as UX-38 in campaign 001 and is still
open, so authors keep meeting it after every validation error.

## Steps to reproduce

1. Fixture `synth/frontmatter-edge.md` (in `assets/synth/`); open the preview to the side, switch
   edit mode on.
2. Click the `priority` value, press Cmd+A, type `7`, press Enter. The message "Schema validation
   failed: must be <= 5" appears.
3. Press Cmd+A, type `4`, press Enter: nothing changes.
4. Press Escape, then click the `title` value: the editor does not close and `title` does not open.

Second symptom (UX-38, replay `ux-38`): after the rejected `9` in `priority`, a click on the
`reviewed_on` value opens no editor. An invalid YAML in an object field (`owner`) behaves the same.

## Impact

Apparent freeze after any validation error; the author cannot correct the value or edit another
field without clicking back into the stuck input. No data loss: the buffer stays untouched.

## Where it comes from

`saveValue` in `src/page/features/frontmatterValueEditor.ts` returns after setting the error status
without restoring focus to the control or releasing the open-editor state, at the tested commit.

## Suggested direction

Refocus the control after a rejected save, let Escape work from the cell as well, and close or revert the invalid editor when another field is clicked. Done when: after a rejected value focus stays in the field, Escape closes the editor and one click on another field opens it; replays `c6-1` and `ux-38` pass.

Uncheck to disagree: [x]

## Test to add

Add a real-input E2E (the replays `c6-1` and `ux-38` promoted): reject a number, assert `activeElement` is the input, Escape closes the editor, a click on `title` opens its editor. It earns a test because a stuck editor blocks all editing and it is a regression of focus handling that returns silently.

Uncheck to disagree: [x]

Sources: sheet
[c6-1](../../../210-qa-campaign-2026-10-31/work/06-frontmatter/c6-1-rejected-commit-strands-editor.md),
sheet [c8-2 / UX-38](../../../210-qa-campaign-2026-10-31/work/09-previous-highs-replay/c8-2-invalid-field-blocks-other-fields.md),
replays [c6-1](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c6-1-invalid-commit-strands-editor.json)
and [ux-38](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-38-invalid-field-does-not-block-others.json),
[campaign index](../../../210-qa-campaign-2026-10-31/work/00-index.md).
