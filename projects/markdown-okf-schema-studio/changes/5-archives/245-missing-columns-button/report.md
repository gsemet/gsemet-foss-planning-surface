# Report: CR 245

Status: **done** (2026-11-03, branch `change-requests/245-missing-columns-button`, PR [#299](https://github.com/gsemet/markdown-okf-schema-studio/pull/299), merged as 20f8f2f6).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | The MyST palette has Card and Grid toolbar buttons and `/card` and `/grid` slash entries, each opening a small form. The Card form has Title, Header, Footer and Link. The Grid form has Columns, Gutter and the number of cards, and also edits each card's header, footer and link (three fields, one entry per card separated by `|`; more entries than cards, or invalid values, keep the form open). Four simulated `palette-slash` scenarios (Card and Grid, light and dark) with screenshots in the PR body. | 20f8f2f6 (the branch's commits were squashed into one when stacked) |

Requirements: new SwRS PALETTE-270 (Card form) and PALETTE-271 (Grid form), both `proposed`, renumbered from 268 and 269 when stacked after the earlier palette CRs; log entry; one CHANGELOG line.

## Proof of completion

- Round 3 added three tests that failed on the old code (Grid per-card fields) and the visual scenarios; fixture `78-card-grid-forms`.
- `just check` green (3563 unit, 73 security, 153 Python at round 2); `palette-slash` visual group all scenarios passed in simulation. Reviews: round 1 FIX-REQUIRED (SwRS cited a test file that did not exist), rounds 2 and 3 APPROVE (3 of 3 rounds used). CI green. Real-window jobs not run.
- Two fixes outside the listed scope, accepted by the reviewer: `card` and `grid` added to the button lists in `capture_edit_checks.py` and `capture_comment_checks.py`; `editPaletteStyles.ts` brought from 803 to exactly 800 lines.

## Open items

- A `|` inside a link cannot be expressed in the Grid form (documented in the SwRS).
- Long Grid field labels wrap on narrow panes.
- `editPaletteStyles.ts` is at the 800-line limit and `capture_comment_checks.py` at 1480 of 1500.
