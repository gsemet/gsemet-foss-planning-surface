# c6-1 — After a rejected commit the frontmatter editor loses focus and Escape no longer closes it

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced (5 times, number field and YAML object field, two fixtures) |
| Area | Frontmatter |
| Modes | Side preview |
| Evidence | DOM and diff checks of the replay (no image) |
| Related | c6-3 (the textarea number editor hits this state every time) |
| Replay | `scenarios/c6-1-invalid-commit-strands-editor.json` |

## Use case

An author edits a schema-bound field (`priority`, maximum 5) or a YAML object field (`owner`) and
presses Enter with a value the validation rejects.

## Steps to reproduce

1. Open `synth/frontmatter-edge.md`, open the preview to the side, switch edit mode on.
2. Click the `priority` value, press Cmd+A, type `7`, press Enter.
3. The message "Schema validation failed: must be <= 5" appears. Press Cmd+A, type `4`, press Enter.
4. Press Escape, or click the `title` value.

## Expected

Focus stays in the input so the author can correct it; Escape cancels the edit; another field opens.

## Observed

`document.activeElement` becomes the table cell (TD). Keys typed afterwards go nowhere (the retry in
step 3 changed nothing), Escape does not close the editor, and clicking another value does not open
its editor. The author must click back into the input first. The buffer stays untouched (diff
against the mark is empty), so there is no data loss.

## Impact

Friction and apparent freeze after any validation error; the invalid-YAML message of an object
field behaves the same.

## Where it comes from

The save path of `src/page/features/frontmatterValueEditor.ts` (`saveValue`) returns after setting
the status; the focus is not restored to `control`.

## Suggested direction

Refocus the control after a rejected save, and let Escape work from the cell as well.

## Test to add

Real-input E2E: reject a number, assert `activeElement` is the input, then Escape closes the editor.

## Done when

The replay scenario passes.

**Coordinator triage (2026-10-31).** Same defect as 001 part-2 UX-38 (High, open), replayed by C8
([c8-2](../09-previous-highs-replay/c8-2-invalid-field-blocks-other-fields.md)) and again by the
coordinator in a fresh session: still present. Severity raised to **High** (QA210-01).
