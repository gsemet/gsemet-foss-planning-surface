# Report: CR 240

Status: **done** (2026-11-03, branch `change-requests/240-bug-row-anchors-in-margin-break`, PR [#285](https://github.com/gsemet/markdown-okf-schema-studio/pull/285), merged by the owner as 5bc2afd9, bottom of stack #288).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Table row and column handles stay on the table's real edges. Cause: the handles were placed once, when edit mode applied; the width mode then broke the table out of the column and nothing placed them again (same after a row or column move). `widthMode.ts` takes an `onLayout` callback, `runtime.ts` calls the new `tableRowMove.reposition()` through it, and `reposition()` re-places the handles on each table's own box. | 5bc2afd9 |

Requirements: SwRS TABLE-002 and TABLE-007 each got a scenario row, markers in place, dated entry in `requirements/tiers/log.md`.

## Proof of completion

- Page test for a table that breaks out fails on the old code and passes now; the in-column test is a regression guard. New simulated scenario `table-editing/v26-handles-breakout-table-auto-light-900` fails on the old code and passes now.
- `just check` passed; simulated `table-editing` group 26 of 26. CI run 41635056592 green (static, visual, report, checks). Real-window jobs not run (manual). One round (1 of 3), reviewer APPROVE.
- Screenshot on branch `change-requests/240-bug-row-anchors-in-margin-break-assets`.

## Open items

- No end-to-end drag-then-render test of a move; one comment line is too long (reviewer notes, non-blocking).
