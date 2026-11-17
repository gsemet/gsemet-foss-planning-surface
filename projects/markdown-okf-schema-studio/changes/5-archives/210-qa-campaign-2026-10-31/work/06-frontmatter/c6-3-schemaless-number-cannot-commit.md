# c6-3 — A number property of a note without schema opens a multi-line box where Enter cannot commit

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced (twice) |
| Area | Frontmatter (Obsidian-style notes) |
| Modes | Side preview |
| Evidence | DOM and diff checks of the replay (no image) |
| Related | c6-1 |
| Replay | `scenarios/c6-3-schemaless-number-editor-cannot-commit.json` (fixture `assets/synth/vault-props.md`) |

## Use case

An author changes `rating: 4.5` in an Obsidian-style note that has no schema.

## Steps to reproduce

1. Open `synth/vault-props.md`, preview to the side, edit mode.
2. Click the `rating` value, press Cmd+A, type `3.5`, press Enter. Then try Cmd+Enter.

## Expected

The value commits (as it does in `synth/frontmatter-edge.md` for `priority`, a number input).

## Observed

The row is typed `number` but the editor is a TEXTAREA holding `"4.5\n"`. Enter inserts a newline
(value `"3.5\n"`), Cmd+Enter shows "Enter a valid number." and nothing is written; focus then leaves
the box (c6-1). A workaround by deleting the trailing newline was not verified.

## Impact

Numbers in schema-less notes cannot be edited in the preview by the obvious keys.

## Where it comes from

`src/page/features/frontmatterValueEditor.ts`, number branch of `saveValue` (control read as
`Number(control.value)`); the control kind differs between schema and schema-less rows.

## Suggested direction

Use the number input for every `number` row, or strip the trailing newline before parsing.

## Test to add

Real-input E2E on a schema-less note: edit a number with Enter.

## Done when

The replay scenario passes.
