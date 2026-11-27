## Summary

After a review comment is created, answered, resolved or deleted, the preview rebuilds the
highlight of every comment thread, and saving a comment asks Git for the author name each time
(https://github.com/gsemet/markdown-okf-schema-studio/issues/547). This change first measures both
waits and the cost of indexing a document for its comment threads.

## Deliverables

The report of the real-window scenario `perf-547` gains the wait of each comment write for the Git
user name, and the time to index a document and to re-anchor its comment threads.

## Changes

- Each comment write records how long it waited for the Git user name, readable by the real-window
  tests only.
- The `perf-547` scenario runs in a test folder that is a Git repository with a user name, and its
  report says so.
- A plain Node step of the same job times the thread index on two generated documents (464 lines
  with 9 threads, 1856 lines with 36 threads). It asserts no limit and changes nothing in how
  threads are indexed, anchored or stored.

## Impacts

No visual change: measurement only.

## Blast radius

- **1**: local and isolated; a plain `git revert` restores the previous behaviour.

Grade: 1

## Known gaps

- The thread index is timed on documents where every thread anchors at its stored place; the cost of
  an orphaned thread or of a search for a changed quote is not measured.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [ ] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [ ] Local gates:
- [ ] Review
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)
