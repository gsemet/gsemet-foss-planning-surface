# Report — link-scheme-check-before-open-external

Status: **done** (2026-10-27, branch `change-requests/132-link-scheme-check-before-open-external`, PR #140, merge commit f8139a5d).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | fix(security): open only http, https and mailto links outside VS Code | f8139a5d |

## Proof of completion

- Merged through gh stack #143 (PRs #140–#142). CI run 40536060802 passed; heavy CI run 40538102998 passed (static, visual, integration, stress).
- Rounds: r1 APPROVE, r2 CI fix (SwRS file lists unsorted). Real-window previewHistory suite passed under the lock.
- Details in `reports/` and `reviews/`; PR body in `reports/PR-BODY.md`.

## Open items

- None recorded here; see the last `reports/T1-r*.md`.
