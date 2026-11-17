## Summary

In 1.7.1 the changelog lines were written late, in the version commit, and the release guide left
three gaps: which Marketplace check counts, what to do when a release closes no issue, and how a
release may ship as a stack that is ready to merge. This updates the release documents to close
them.

## Deliverables

| Document | What changes |
| --- | --- |
| PR template | A "Changelog" checkbox in the Test plan, no new section |
| Release guideline | Each PR adds its own `## Unreleased` line; `vspackage` HTTP 200 is the Marketplace check of record; an empty issue list ends step 8 with one line; new section "The version PR on top of a stack" |
| CONTRIBUTING.md, CI guideline rule 14 | The same stacked way (heavy run on the top branch); a missing line is a gap of its PR |
| Process guideline | The `## Unreleased` line in the code, review and PR steps; the stacked release; the empty-list case |

## Changes

- `.github/PULL_REQUEST_TEMPLATE.md`: one checkbox after "Requirements".
- `.agents/guidelines/release-process.guidelines.md`: intro, merge rights, steps 2, 4, 5, 6, 8, and
  the new stacked-release section.
- `CONTRIBUTING.md` "How to Release": intro, steps 1 and 2.
- `.agents/guidelines/ci.guidelines.md`: rule 14.
- `.agents/guidelines/change-requests-lifecycle.guidelines.md`: lifecycle table, release planning,
  release prompt, "Lists".
- Open VSX text, `src/`, requirements and `CHANGELOG.md` are untouched.

## Impacts

No visual change: process text only.

## Blast radius

Grade: 1. Documents only; a plain `git revert` restores the previous text.

## Test plan

- [x] New or changed tests: none, documents only
- [x] Requirements: No behaviour change
- [x] Changelog: No user-facing change
- [x] Local gates: `just check`, guideline isolation test; local `ci-integration` failed on the dev Mac (several windows at once), so the branch heavy run is the proof
- [x] Review
- [x] CI green: pull request run and branch heavy run (stress re-run once after a round-1 page-runtime timeout)

## Autonomous decisions

- The CI and process guidelines are updated too, so that no document contradicts the stacked way.

## Internal references

- CR-305 release-process-fixes-from-the-v1-7-1-retro
