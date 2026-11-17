# Enter in a card `:header:` editor inserts a blank line into the option block

Severity Medium · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-BLOCK-258 · Area Inline editing, MyST cards · Side preview · QA210-03 · Replay `scenarios/c1-2-card-header-enter-adds-blank-line.json` · P2

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![Header option editor after typing and Enter, still open](evidence/currently.jpg)<br><pre>-:header: Since v2.1.154, published 2026-05-28<br>+:header: Since v2.1.154, published 2026-05-28 Q<br>+<br> :footer: Documented in the workflows guide</pre> | <pre>-:header: Since v2.1.154, published 2026-05-28<br>+:header: Since v2.1.154, published 2026-05-28 Q<br> :footer: Documented in the workflows guide</pre> |
| *Currently: Enter in the `:header:` editor adds a line (editor stays open, status shows "Line 18"); replay `c1-2` on b9118506 gives -1 +2.* | *Expected: Enter commits the one-line option, the editor closes, the diff is -1 +1.* |

The Currently shot is the before-shot the fix PR must reproduce.

## Why this is wrong

An author fixes the header of a card and presses Enter to finish, as in the card title editor.
Instead the document gains an empty line between `:header:` and `:footer:`. In MyST a blank line
ends the directive options, so the `:footer:` line is at risk of turning into body text: a habitual
key silently changes the structure of the document. The header is a one-line option (BLOCK-258
edits it on its own line), so a newline has no meaning there and the change goes beyond the edited
line.

## Steps to reproduce

1. Fixture `fixtures-visual/68-cards-tabs-version.md`; open the preview to the side, edit mode on.
2. Click the card header "Since v2.1.154, published ...", press End, type ` Q`, press Enter.
3. The editor stays open and the buffer diff is -1 +2 (see above).

## Impact

Silent change of the document structure; the `:footer:` option can be lost to the body.

## Where it comes from

The header and footer option editor is the multi-line block editor: Enter inserts a newline and the
value is written back as is, at the tested commit.

## Suggested direction

Make option editors single-line: Enter commits (Shift+Enter ignored or turned into a space), like the title editor. Done when: Enter commits the option on one line and the editor closes; replay `c1-2` passes.

Uncheck to disagree: [x]

## Test to add

Add a unit test on the buffer: a header edit committed with Enter leaves a one-line diff and no blank line in the option block. It earns a test because the blank line breaks the directive's option block, a buffer change outside the edited text. The replay `c1-2` stays as the manual check.

Uncheck to disagree: [x]

Sources: sheet [c1-2](../../../4-archives/210-qa-campaign-2026-10-31/01-myst-cards-tabs/c1-2-card-header-enter-adds-blank-line.md),
replay [c1-2](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c1-2-card-header-enter-adds-blank-line.json),
[campaign index](../../../4-archives/210-qa-campaign-2026-10-31/00-index.md).
