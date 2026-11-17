## Summary

The repository's change requests now live in a separate planning repository, and chantier runs
their lifecycle and status board. Guidelines, the exploratory QA skill and a few test comments still
pointed contributors to a local `.agents/changes/` folder with the old stage names. They now point to
the planning folder named by `AGENTS.md`, with its current stage and file names.

## Deliverables

Before and after, for the lifecycle guideline and the tooling it described:

| Before | After |
| --- | --- |
| Local, git-ignored `.agents/changes/{1-inbox,2-backlog,3-requests,4-archives,5-trash}` | The planning folder's `1-inbox`, `2-backlog/P1..P4`, `3-ready`, `4-batch`, `5-archives`, `6-trash` |
| Guideline spelling out the old steps, status table and run-state brief | One short guideline: what stays project-specific, and a pointer to chantier for the rest |
| `just orchestrator` generating a status table | Removed; chantier's board shows the status |
| QA scripts reading `<repo>/.agents/changes` | Default to the planning folder; `QA_CHANGES_ROOT` still overrides it |

## Changes

- Rewrite `.agents/guidelines/change-requests-lifecycle.guidelines.md` around the planning folder;
  the old heartbeat, driver prompts and report formats are not kept, since chantier runs them.
- Update the pull-request, owner-review and short-demo guidelines, `AGENTS.md` "Process", the
  exploratory QA skill (docs, `coverage-map.py`, `new-features.py`) and two test comments.
- Remove the `orchestrator` recipe, `scripts/generate_orchestrator.py` and its test.
- The `.agents/changes/` line of `.gitignore` is kept, so local leftovers stay ignored.

## Impacts

No visual change. Contributors following the guidelines are sent to the planning folder.

## Blast radius

Grade: **1**. Documentation, two QA helper scripts and a removed generator; a `git revert` restores
everything.

## Test plan

- [x] New or changed tests: none needed; the generator's own test is removed with it
- [x] Requirements: No behaviour change
- [x] Changelog: No user-facing change
- [x] Local gates: `just ci-static` passed at 884949f; `test/build/test_guideline_isolation.py` (9 passed)
- [x] Review: approved at 0a60fd3d (the same patch, rebased)
- [x] Verified at f6482d0 (the same patch, carried over a clean rebase to 884949f)
- [x] CI green at 884949f (static, static-windows, visual, report)

## Internal references

Request CR-338; the owner decided to remove the generator (planning folder, answers to the
request).
