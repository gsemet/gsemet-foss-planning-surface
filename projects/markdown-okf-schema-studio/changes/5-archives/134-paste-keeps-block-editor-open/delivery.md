# Report — paste-keeps-block-editor-open

Status: **done** (2026-10-27, branch `change-requests/134-paste-keeps-block-editor-open`, PR #142, merge commit 5727da8b).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | fix(edit-mode): keep the page still after a paste in a block editor | 5727da8b |

## Proof of completion

- Merged through gh stack #143 (PRs #140–#142). CI run 40536077611 passed; heavy CI run 40538102998 passed (static, visual, integration, stress).
- Rounds: r1 APPROVE, r2 CI fix (SwRS file lists unsorted). Screenshots on branch `change-requests/134-paste-keeps-block-editor-open-assets` (5fd74b10).
- Details in `reports/` and `reviews/`; PR body in `reports/PR-BODY.md`.

## Open items

- The editor still closes now and then (about 3 of 8 runs) after a paste into a tall block, before and after the fix: candidate backlog item (to be filed by the main session).
