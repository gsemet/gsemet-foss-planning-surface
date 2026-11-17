# c1-2 — Enter in a card `:header:` editor inserts a blank line that breaks the option block

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced (two runs) |
| Area | Inline editing, MyST cards |
| Modes | Side preview |
| Evidence | [c1-2-card-header-enter.jpg](../../evidence/c1-2-card-header-enter.jpg) |
| Related | #236 |
| Replay | `scenarios/c1-2-card-header-enter-adds-blank-line.json` |

## Use case

An author edits the `:header:` option of a `{card}` and presses Enter to finish, as in the card title editor.

## Steps to reproduce

1. Open `fixtures-visual/68-cards-tabs-version.md`, preview to the side, edit mode on.
2. Click the card header "Since v2.1.154, published ...", press End, type ` Q`, press Enter.

## Expected

Enter commits and closes (as in the title editor, where Cmd+Enter or Enter commit), or at least never writes a newline into a one-line option.

## Observed

The editor stays open and the buffer diff is -1 +2: `:header: ... Q` followed by a new empty line, before `:footer:`. A blank line ends the directive options, so the `:footer:` line is at risk of turning into body text.

## Impact

Silent change of the document structure from a habitual key.

## Where it comes from

The header/footer option editor is the multi-line block editor; Enter inserts a newline and the value is written back as is.

## Suggested direction

Single-line option editors: Enter commits (Shift+Enter ignored or turned into a space), same as the title editor.

## Test to add

Real-input E2E: header edit + Enter keeps the diff to one line.

## Done when

Replay passes (diff is one line).
