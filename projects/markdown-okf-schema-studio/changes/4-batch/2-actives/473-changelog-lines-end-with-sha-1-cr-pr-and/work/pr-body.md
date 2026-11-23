build: end CHANGELOG lines with their commit, change request, PR/MR and issue

## Summary

A changelog line gave no way to find where it came from, and forgotten pull request numbers had to be added by follow-up commits on `main`. Every line of `CHANGELOG.md` now ends with its references in parentheses, in the forge's own notation (`PR #476` on GitHub, `MR !476` on GitLab, `issue PROJ-12` for Jira). The author writes all but the commit; the release adds the commit with a new script, so no follow-up commit is needed.

## Deliverables

Format of a line, as the author writes it and after release:

```text
- Fixed the tooltip of the change bar. (CR-463 change-bar-tooltip, PR #476, issue #413)
- Fixed the tooltip of the change bar. (commit 1a5b98b, CR-463 change-bar-tooltip, PR #476, issue #413)
```

New release step: `just changelog-refs` (forge-neutral: `git` only, no forge API) finds the commit that added each line of `## Unreleased` with `git blame` and inserts `commit <sha>` as first item; a second run changes nothing, a dirty file or a commit not on the base stops it, and `--skip-missing` leaves such a line as it is (version PR on top of a stack).

## Blast radius

Grade: 1. New release tooling and guideline text; nothing in the extension. A plain `git revert` restores the previous behaviour.

<details><summary>Details</summary>

## Changes

- `scripts/changelog_refs.py`, `just changelog-refs`, and `test/build/test_changelog_refs.py` (added to `release-tests`).
- New "CHANGELOG line" section in the pull-request guideline; release-process guideline steps and `CONTRIBUTING.md` "How to Release" updated.
- New software requirement for the script, with its traceability markers.

## Impacts

No user-facing change; release tooling and contributor guidelines only.

## Test plan

- [x] New or changed tests (they fail on the previous code): 11 tests in `test/build/test_changelog_refs.py`
- [x] Requirements: SwRS added, markers in code and tests, `just requirements-update`
- [x] Changelog: No user-facing change
- [x] Local gates: `just check`
- [x] Review: approved at c9712e2 (restack onto CR-472, one justfile conflict resolved; rest carried from d86fd91)
- [ ] CI green at c9712e2

## Internal references

CR-473 changelog-refs, batch-09.

</details>
