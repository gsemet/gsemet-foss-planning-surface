# A number property without a schema opens a text area that cannot be committed

Severity Medium · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-FMEDIT-015, SwRS-MDOKFSTUDIO-FMEDIT-007 · Area Frontmatter (Obsidian-style notes) · Side preview · QA210-08 · Replay `scenarios/c6-3-schemaless-number-editor-cannot-commit.json` · P2

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![Schema-less number: textarea](evidence/currently.jpg)<br><pre>(no change: buffer equals disk, editor still open on "3.5\n")</pre> | <pre>-rating: 4.5<br>+rating: 3.5</pre> |
| *Currently: `rating` (no schema) opens a TEXTAREA with value `"3.5\n"`; Enter adds a newline and the buffer is unchanged (replay `c6-3` on b9118506).* | *Expected: the working case next to it, a schema number (`priority`) opens a one-line INPUT; the schema-less number behaves the same and commits on Enter.* |

The Currently shot is the before-shot the fix PR must reproduce.

## Why this is wrong

An author changes `rating: 4.5` to `3.5` in an Obsidian-style note without a schema. The editor is a
multi-line box holding `4.5` plus a trailing newline, so every key the author reaches for fails:
Enter inserts another newline, and Cmd+Enter answers "Enter a valid number." because the text read
back is `3.5\n`. Nothing is written and focus then leaves the box (see QA210-01). In the same
preview a schema number opens a one-line input and commits. FMEDIT-015 does give schema-less fields
a YAML text box where Enter adds a line and Cmd or Ctrl+Enter saves, so Enter alone may stay a
newline there; but the saving key must work, which it does not for a number. The owner decided (2026-10-31) to keep the multi-line box of FMEDIT-015; the fix makes
Cmd+Enter commit by trimming the trailing newline.

## Steps to reproduce

1. Fixture `synth/vault-props.md` (in `assets/synth/`); open the preview to the side, edit mode on.
2. Click the `rating` value, press Cmd+A, type `3.5`, press Enter: a newline is added.
3. Press Cmd+Enter: "Enter a valid number." and nothing is written.

## Impact

Numbers in schema-less notes cannot be edited in the preview with the obvious keys.

## Where it comes from

The number branch of `saveValue` in `src/page/features/frontmatterValueEditor.ts` reads
`Number(control.value)` including the trailing newline; the control kind differs between schema and
schema-less rows, at the tested commit.

## Suggested direction

Keep FMEDIT-015 (schema-less fields keep the multi-line YAML box, Enter adds a line). The fix makes Cmd/Ctrl+Enter commit a number by trimming the trailing newline before `Number(...)` in `saveValue`. Done when: a schema-less number is edited and committed with Cmd/Ctrl+Enter; replay `c6-3` passes.

Uncheck to disagree: [x]

## Requirement to write or change

FMEDIT-015 stays as it is (owner decision 2026-10-31); no new requirement.

Uncheck to disagree: [x]

## Test to add

Add a unit test on `saveValue`: a number value `3.5\n` commits as `3.5` (diff `-rating: 4.5` `+rating: 3.5`). It earns a test because the failure is a silent inability to write, one line to pin.

Uncheck to disagree: [x]

Sources: sheet [c6-3](../../../4-archives/210-qa-campaign-2026-10-31/06-frontmatter/c6-3-schemaless-number-cannot-commit.md),
replay [c6-3](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c6-3-schemaless-number-editor-cannot-commit.json),
[campaign index](../../../4-archives/210-qa-campaign-2026-10-31/00-index.md).
