# Report — plantuml-jar-include-confinement

Status: **done** (2026-10-28, branch `change-requests/137-plantuml-jar-include-confinement`, PR #145, merge commit bc8f0ed3).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | fix(security): keep PlantUML JAR includes inside the workspace | bc8f0ed3 |

## Proof of completion

- Merged by the user through gh stack #161 (`gh stack merge`, 2026-10-28 08:01). Normal CI (static, visual, checks) green on the PR; heavy CI: not run on this branch alone; stack heavy CI ran on the top.
- Reviewer APPROVE; screenshots on branch `change-requests/137-plantuml-jar-include-confinement-assets` where the change is visible; PR body in `reports/PR-BODY.md`; Requirements traceability table in the PR body.

## Open items

- `!theme ... from <path>` is not scanned for includes (driver note): candidate follow-up.
