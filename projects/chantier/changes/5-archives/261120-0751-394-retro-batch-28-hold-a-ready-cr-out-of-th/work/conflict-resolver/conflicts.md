# Conflicts, rebase on cr-393 branch

- stacks.py `start_on_for`: kept the base's `_below_with_pr` (chain already excludes held CRs); dropped this CR's older `order`-based scan.
- stacks.py `start_base` tail: kept the base's single `stack_start` route; dropped this CR's duplicate start_on block.
- Merge of both intents (post-rebase, uncommitted edits): new `_live_start` (start_on owner neither ended nor held) used by `stack_start` and `start_base`; `stack_base` returns the default branch for a held CR; a placed CR in `start_base` keeps only a live start_on, else falls through to after/default.
- test_stack_hold.py: the queued CR-9 is appended to the record for `start_on_for` (the base's version reads the chain), then removed.
- scenario/run_scenario.py, driver.md: auto-merged, no marker.

Fast gate: `just check` (in the worktree): pass, 929 passed 1 skipped, lint and release-notes ok.
