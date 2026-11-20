# Conflicts: CR-397 rebased on cr-396

- `lifecycle/stages.py`, import block (commit 33db841d): kept HEAD's `core.files` import with `subject` and the single-line `core.records` import (`CrEntry, read_batch_json`). The CR side added no name, only a multi-line reformat, so it was dropped.
- Commit ad46081c: no conflict.
- Slip: I staged and continued before the markers were removed, so commit 33db841d holds the conflict markers in `stages.py`. The fix is in the working tree, uncommitted (I never commit). The Driver must commit it, as a fixup into 33db841d or as a new commit.

Fast gate: `just check` run in the worktree, with the fix in the working tree: 977 passed, 1 skipped; release-notes check ok.
