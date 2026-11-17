# Report: CR 252

Status: **done** (2026-11-03, branch `change-requests/252-table-move-e2e-test`, PR [#295](https://github.com/gsemet/markdown-okf-schema-studio/pull/295), merged as bd6145f5, middle of stack #296).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A simulated end-to-end scenario `table-editing/v27-row-move-breakout-table-auto-light-900`: it drags row handle 1 below row 3, applies the host patch, then checks the rendered rows, the margin breakout, the 3 row handles and the 5 column handles (`test/visual/capture_table_move.py`, `@tests_req` TABLE-002 and TABLE-007). Test-only, no CHANGELOG line. | bd6145f5 |

## Proof of completion

- Removing the `reposition` callback from `installWidthMode` in `src/page/runtime.ts` made the scenario fail (handles off by 11 to 55 px); it passes when restored (coder's run).
- `just check` passed (3553 node tests, 73 in the second suite); simulated `table-editing` group 27 scenarios; scenario count 439 to 440. One round, reviewer APPROVE. CI green. Real-window jobs not run.

## Open items

- The `table-editing` run reports 27 scenarios but 26 screenshots; not investigated.
- The check builds the `previewContentPatch` itself because the visual harness has no host.
