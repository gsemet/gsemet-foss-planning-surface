## Summary

The review comments file reader accepted a creation date naming a day that does not exist, such as `2026-02-30T10:00:00Z`: `Date.parse` rolls it over to March, so the check let it through. Such a date now rejects the whole file, like any other bad date.

## Deliverables

None (a one-function fix in the comments file parser).

## Changes

- `src/core/comments/commentModel.ts`: `isIsoDate` also checks that the day exists in its month (leap years included) before the instant check.
- `test/core/comments/commentModel.holes.test.ts`: impossible days (2026-02-30, 2026-02-29, 1900-02-29, 2026-04-31, month 00) are refused; real days (2024-02-29, 2000-02-29, 2026-04-30) are read.
- SwRS-MDOKFSTUDIO-REVIEW-004 and `requirements/tiers/log.md` describe the stricter rule.

## Impacts

A hand-edited or generated comments file with an impossible date is now reported as not valid instead of loading. No visual change.

## Blast radius

Grade: 1. One validation function; a plain `git revert` restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [x] Changelog: No user-facing change (only an invalid, hand-edited file is affected)
- [x] Local gates: `just check`, the targeted unit test, `just requirements-update`, `just requirements-lint`
- [x] Review: inspector approved at 589c77c
- [ ] CI green
