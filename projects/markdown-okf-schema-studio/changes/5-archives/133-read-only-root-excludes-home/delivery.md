# Report — read-only-root-excludes-home

Status: **done** (2026-10-27, branch `change-requests/133-read-only-root-excludes-home`, PR #141, merge commit 5b083d91).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | fix(security): read-only previews no longer expose the home folder or dot-directories | 5b083d91 |

## Proof of completion

- Merged through gh stack #143 (PRs #140–#142). CI run 40536067089 passed; heavy CI run 40538102998 passed (static, visual, integration, stress).
- Rounds: r1 FIX-REQUIRED (the webview resource-root narrowing had no test), r2 APPROVE, r3 CI fix (SwRS file lists unsorted).
- Details in `reports/` and `reviews/`; PR body in `reports/PR-BODY.md`.

## Open items

- Nit: a doc comment in `src/session/features/rendering.ts` now sits above `previewLocalResourceRoots` instead of `RenderingController`.
