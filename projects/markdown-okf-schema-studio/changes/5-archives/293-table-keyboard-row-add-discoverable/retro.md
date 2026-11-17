# Retro — 293-table-keyboard-row-add-discoverable

| What happened | Root cause | Process fix |
| --- | --- | --- |
| Round 1 red in CI only: visual `table-editing/v30-cell-tab-hint-light-900` overlay-covers-text (local pass) | The scenario scrolled to the last cell with offset 200, so the table top depended on font metrics and the sticky table bar floated over the rows | Fixed in round 2: scroll to the table with offset 300 in `tableTabHintScenarios.ts`; rule candidate: scenario placement must not depend on font metrics |
| A compound command with `pkill` was refused by the auto mode classifier ([Interfere With Workloads]); the round-2 driver stopped and reported | The driver added an unneeded `pkill` to a command that also rebased | CoS authorized continuing in separate commands without `pkill` or `git stash`; None further |
| Whole stack went BEHIND `origin/main` when #357 landed; the owner asked for one rebase of all six PRs, so every head changed and needed new heavy CI and a fresh Verifier | A docs-only merge on main during a long stack run invalidated every green head | None: the Rebase rule worked as intended |
