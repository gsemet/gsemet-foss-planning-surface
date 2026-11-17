# Report — myst-cards-tabs-version-directives

Status: **done** (2026-10-28, branch `change-requests/148-myst-cards-tabs-version-directives`, PR #156, merge commit 97c9512a).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | feat(preview): render MyST cards, tabs and version directives, and show them in the README | 97c9512a |

## Proof of completion

- Heavy run on the stack top (40666806719) failed integration on `mystBlocksWindow` ('editor holds the source of the tab item only'); merged by the user's decision with normal CI green. Real-window screenshots were headless captures (screen locked overnight).
- Reviewer APPROVE; requirements traceability table in the PR body (`reports/PR-BODY.md`).

## Open items

- Real-window scenario `mystBlocksWindow` failed on heavy run 40666806719 ('editor holds the source of the tab item only'): needs a follow-up round (backlog item `02-backlog/P2/myst-tab-item-edit-source/`).
- No unit test of `:class-card:` through the sanitizer (reviewer note).
