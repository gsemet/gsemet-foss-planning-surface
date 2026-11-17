# Report — toc-marker

Status: **done** (2026-10-28, branch `change-requests/142-toc-marker`, PR #150, merge commit 00f40bd1).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | feat(preview): render [TOC], [[_TOC_]] and {contents} as a clickable table of contents | 00f40bd1 |

## Proof of completion

- Merged by the user through gh stack #161 (`gh stack merge`, 2026-10-28 08:01). Normal CI (static, visual, checks) green on the PR; heavy CI: 40640637221 and 40645287945 (integration green; stress green on the first).
- Reviewer APPROVE; screenshots on branch `change-requests/142-toc-marker-assets` where the change is visible; PR body in `reports/PR-BODY.md`; Requirements traceability table in the PR body.

## Open items

- Scope changed mid-run by the user: `[TOC]`, `[[_TOC_]]` and MyST `{contents}`; `[[toc]]` dropped.
