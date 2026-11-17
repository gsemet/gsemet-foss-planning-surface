# The Comments toolbar button hides only the inline chips (the button should hide everything)

Severity Medium · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-REVIEW-152 (to widen) · Area Review comments, toolbar · Side preview · QA210-10, QA215-06 · Replay `scenarios/c2-1-comments-toggle-keeps-threads.json`, `scenarios/c4-1-comments-button-leaves-review-threads.json` · P2

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![Comments off: thread highlight stays](evidence/currently.jpg) | ![Expected if all review marks hide](evidence/expected.jpg) |
| *Currently: with the Comments button off the thread highlight (`retry budget`) and underline (`resolved topic`) stay (replay `c2-1` on b9118506).* | *Expected (annotated copy, only if the owner decides the button hides every review mark): both marks hidden.* |

| ![Comments hidden: a thread highlight still opens its popover](evidence/currently-clickable.jpg) | *Expected: with comments hidden, highlights and badges are plain text and open no popover.* |

The Currently shot is the before-shot the fix PR must reproduce.

## Why this is wrong

An author who switches Comments off expects the review marks to go away, yet the highlighted quotes
(`mark[data-okf-comment-thread]`), the badges and the "Orphaned comments" list stay fully visible;
only the inline `<!-- comment -->` and `<!-- THREAD` chips are hidden. The button's name suggests
all comments. REVIEW-152 was written for the chips only. Campaign 215 (QA215-06, Medium) adds that the hidden
highlights and badges stay **clickable**: a click opens the thread popover, so threads can be read and
edited while the button says comments are hidden. The page contradicts its own button label. The owner decided (2026-10-31) that the button hides every review mark, so REVIEW-152 is widened and the current behaviour is a Bug against it.

**Steps.** Fixture `synth/review-threads.md` with `review-threads.comments.json` (both in
`assets/synth/`): open the side preview, open the toolbar chevron, click Comments (it becomes "Show
comments", `aria-pressed=false`).

## Suggested direction

Extend `src/core/preview/styles/commentStyles.ts` (~L535, which hides only `.okf-comment` chips for `data-sphinx-preview-comments="off"`) to `mark[data-okf-comment-thread]`, the badges and the orphan list. Done when: with the button off, chips, highlights, badges and the "Orphaned comments" list are all hidden, a click on the former highlight opens no popover, and replays `c2-1` and `c4-1` pass.

Uncheck to disagree: [x]

## Requirement to write or change

Widen REVIEW-152 (owner agreed 2026-10-31): the setting and the button hide and show every review mark: chips, highlights, badges and the orphan list. If REVIEW-152 is approved, the fix CR sets `approved_by` / `approved_on` to the owner when it changes it.

Uncheck to disagree: [x]

## Test to add

No test: a CSS toggle with no data at risk; the widened REVIEW-152 and the replay `c2-1` are the check.

Uncheck to disagree: [x]

Sources: sheet [c2-1](../../../210-qa-campaign-2026-10-31/work/02-review-comments/c2-1-comments-toggle-keeps-threads.md),
replay [c2-1](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c2-1-comments-toggle-keeps-threads.json),
[campaign index](../../../210-qa-campaign-2026-10-31/work/00-index.md),
sheet [QA215-06](../../../215-qa-campaign-2026-10-31/work/03-review-comments/c4-1-comments-button-leaves-review-threads.md).
History: CR [092](../../../092-comments-button-hides-threads/01-intent.md) made the button hide the inline
thread chips (REVIEW-158); the highlights and badges from the comments file were never in its scope, so
this is not a regression.
