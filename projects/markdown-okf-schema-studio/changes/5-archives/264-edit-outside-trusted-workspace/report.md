# Report — edit-outside-trusted-workspace

Status: **done** (2026-11-06, branch `change-requests/264-edit-outside-trusted-workspace`, PR #327, merge commit `22bcae8a`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A document is editable whatever the workspace trust, in Restricted Mode and for a standalone file; reads stay limited; a file VS Code holds read-only answers so on every write path; approved StRS BLOCK-025, REVIEW-003, REVIEW-015, TABLE-001 changed with the owner's agreement | `22bcae8a` |

## Proof of completion

- `just check` exit 0 on the rebased round 1; PR CI green; heavy run 42184807228 green on the stack top (static, static-windows, visual, integration, stress), same tree as the merged stack.
- Inspection: three bounded Opus inspectors on round 1 (`reviews/T1-r1-inspection.md`), one on round 2 (`reviews/T1-r2-inspection.md`), one on round 3 (approved). The whole-diff inspection hung three times before the slices.
- Screenshots: before and after in the PR, on branch `change-requests/264-edit-outside-trusted-workspace-assets` (kept).
- `just preflight` was not run locally.

## Open items

- Weak `aliveWhenPosted` assertion; no test fails without the target-after-flush fix.
- Capture id `r01-untrusted-read-only` and stress scenario `untrusted-read-only` keep their old names.
- No changelog line in `## Unreleased`: to add before the next release.
