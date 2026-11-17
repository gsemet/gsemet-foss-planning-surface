# Report: CR 242

Status: **done** (2026-11-03, branch `change-requests/242-bug-margin-breaking`, PR [#301](https://github.com/gsemet/markdown-okf-schema-studio/pull/301), merged as 857720fa).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | New Auto width rule (variant D): a table stays in the text column when it fits and breaks out only when it needs to; minimum prose column width 24ch (owner-confirmed). | 9ab0c413 |
| T1 | `docs/user/wide-tables.md` describes the Auto width rule; the claim about raw HTML tables was removed (no code, test or SwRS backs it). | b6e6afea |
| T1 (round 5) | Fixture `test/visual/fixtures/63-breakout-table-handles.md`: the three Description cells now hold multi-word prose (input change only, owner-approved), so scenarios v26/v27 render the wrapped column. Before/after screenshots in `screenshots/r5/`. | 857720fa |

Requirements: new SwRS LAYOUT-044, markers, dated log entry. One CHANGELOG line.

## Proof of completion

- 5 rounds (limit raised to 5 by the owner). Round 5 fixed the red visual scenarios v26/v27 on table-editing; the debugger proved a fixture problem, not a code defect.
- CI green on the pushed head 4c245e8f (static, static-windows, visual, report). Real-window jobs not run.

## Open items

- Case 6 has only about 11 px of margin and depends on the font.
- Follow-up P2 `breakout-scroll-handles-scenario` is filed.
