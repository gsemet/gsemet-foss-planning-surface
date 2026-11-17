# Report — table-column-min-width

Status: **done** (2026-10-28, branch `change-requests/138-table-column-min-width`, PR #146, merge commit d53e258f).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | fix(preview): give table columns a readable minimum width | d53e258f |

## Proof of completion

- Merged by the user through gh stack #161 (`gh stack merge`, 2026-10-28 08:01). Normal CI (static, visual, checks) green on the PR; heavy CI: not run on this branch alone; stack heavy CI ran on the top.
- Reviewer APPROVE; screenshots on branch `change-requests/138-table-column-min-width-assets` where the change is visible; PR body in `reports/PR-BODY.md`; Requirements traceability table in the PR body.

## Open items

- Final normal CI fix: the minimum-width floor no longer splits words in the Auto break-out table.
