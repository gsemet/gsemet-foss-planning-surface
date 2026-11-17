# Report — foreman-plans-release

Status: **done** (2026-11-05, branch `change-requests/258-foreman-plans-release`, PR #315, merge commit `69d916a9`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | The Foreman plans the release | `b2fe33ab` |
| T1 | Real VS Code jobs run on every push to `main`, never on a PR | `9f572841` |
| T1 | Release driver and `STATE.md` header moved to their guidelines | `69d916a9` |

## Proof of completion

- `just check` passed; `ci-static` and `ci-visual` passed in `just preflight`.
- Main run 42031878313 at `69d916a9` failed on: integration, report, checks. Later main runs are green.
- `just preflight` never passed in full on the Mac for this CR.

## Open items

- The branch is kept: open PR 320 is based on it.
