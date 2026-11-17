# Report — 274-table-escape-keeps-cells-left

Status: **done** (2026-11-10, branch `change-requests/274-table-escape-keeps-cells-left`, PR #343, merge commit `d6a0cfbb`; source: QA campaign 271, finding QA271-01; no GitHub issue).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | In a table cell edit session, Escape cancels only the text typed in the cell it is pressed in; the cells left earlier with Tab, an arrow key or a click keep their typed text and the page shows it; SwRS TABLE-025 amended, requirements log, CHANGELOG; visual harness check `capture_table_escape.py` | `d6a0cfbb` |

## Proof of completion

- Three rounds. Round 1 FIX-REQUIRED (Opus Inspector), round 2 APPROVE, then CI failed on the `visual` job at head `7c1c9271` (run 42879302136): the harness check still expected Escape to cancel the whole session, which the amended TABLE-025 no longer does. Round 3 (Opus coder, Opus Inspector APPROVE) fixed the harness expectation, a test change and not a product change.
- Round 3 gates: `just check` passed (3699 unit, 93 contract); `npm run test:visual` 462/462; table-editing capture 28/28.
- CI at head `bc5b3d77`: PR run 42891946427 green; heavy run 42891938744 green.
- The CR 274 driver was restarted once by the Foreman (stale header while the coder ran long); it resumed from the files.

## Open items

- None for this CR. `just preflight` and the real VS Code windows were not run locally (CI ran them).
