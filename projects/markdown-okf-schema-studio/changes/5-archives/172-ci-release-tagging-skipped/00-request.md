# 172 — CI: release tagging skipped on main since the heavy split (HOTFIX)

Type: fix (CI) · Priority: P1 · Approved by the user via the Chief of Staff, 2026-10-28 · From
`origin/main` b723e176, one PR, not stacked. Target: 1.0.1 tags itself (1.0.0 is tagged by hand).

## Problem

The push run on main for the 1.0.0 version merge (run 40775866410, b723e176) was green, but
`tag-release`, `release` and `pages` were all skipped, so no tag was created.

## Cause

Since the heavy split, `integration` and `stress` only run on `workflow_dispatch` with `heavy`.
`report` needs `[visual, integration]` (it has `if: !cancelled()`), `checks` needs `report`, and
`tag-release` (`.github/workflows/ci.yml:296`) has
`if: github.event_name == 'push' && github.ref == 'refs/heads/main'` with an implicit `success()`,
which is false when any ancestor job was skipped. `release` and `pages`
(`if: needs.tag-release.outputs.tag != ''`) have the same implicit `success()`.

## Fix

- `tag-release`: `if: ${{ !cancelled() && needs.checks.result == 'success' &&
  github.event_name == 'push' && github.ref == 'refs/heads/main' }}`.
- `release`, `pages`: `if: ${{ !cancelled() && needs.tag-release.result == 'success' &&
  needs.tag-release.outputs.tag != '' }}`.
- Audit every other job for the same pattern (e.g. `gallery`).
- Workflow test in `test/build/test_workflows.py` (new, pytest, like `test_release.py`): parse
  `ci.yml`, compute for each job whether an ancestor can be skipped (job with an `if` that can be
  false on push, i.e. heavy-only), and assert that every job downstream of such an ancestor uses an
  explicit `needs.<job>.result` check plus `!cancelled()` (or `always()`). It must fail on the
  current `ci.yml` and pass on the fix.
- Requirement: update or add (proposed) the release/CI requirement if one describes tagging.

## Gate

`just check` (pytest included); normal CI. Heavy not needed unless heavy jobs change. PR body for
an external reader.
