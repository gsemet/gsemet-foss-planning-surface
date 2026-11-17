# Report — paste-url-as-link

Status: **done** (2026-10-28, branch `change-requests/145-paste-url-as-link`, PR #153, merge commit 6df062d3).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | feat: pasting a URL makes a link, an image URL an image | 6df062d3 |

## Proof of completion

- Merged by the user through gh stack #161 (`gh stack merge`, 2026-10-28 08:01). Normal CI (static, visual, checks) green on the PR; heavy CI: not run on this branch alone; stack heavy CI ran on the top.
- Reviewer APPROVE; screenshots on branch `change-requests/145-paste-url-as-link-assets` where the change is visible; PR body in `reports/PR-BODY.md`; Requirements traceability table in the PR body.

## Open items

- Cmd/Ctrl+Shift+V raw paste is unit-tested only, not driven in a real window.
