# Conflicts: CR-405 rebased onto origin/main (a8f17555)

Command: `git rebase --onto origin/main f5e1365b`. One conflicted file.

## hub/cycle.py, `Hub.cycle`
- HEAD (main, CR-401): the per-project body inlined, with `journal.set_aside(...)` and `journal.skipped(refused)` setting `entry["error"]` to `skipped: ...`.
- CR-405: the body moved to `Hub._project` (registry, connectors, providers).
- Choice: kept CR-405's `_project`; ported CR-401's behaviour into it: the providers' events go through `journal.set_aside`, the accepted are appended, and a refusal puts `skipped: ...` in the entry's error.

## Not conflicting, but changed
- `hub/batch_prs.py` already uses `journal.merged_events` / `journal.red_event`, which write the typed `merged@1` / `checks-red@1`: no change.
- `tests/test_hub_connectors.py`: two assertions expected the old `merged` type; now `merged@1`.

The rebased commit is 83dbd515; the cycle.py fix after the first gate run and the test edits are in the worktree, uncommitted (the resolver never commits).

## Fast gate
`just check` (in the worktree): first run 3 failed (the above, before the set_aside port and test fix); final run: 1096 passed, 14 skipped, release-notes ok, exit 0. Log: work/gates/conflict-check.log.
