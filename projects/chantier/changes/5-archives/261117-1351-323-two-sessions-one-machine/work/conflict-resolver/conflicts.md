# Conflicts: CR-323 rebased onto CR-322 (91114fe), stopped on 3cdf05d

1. AGENTS.md, one hunk (chantier-writes sentence). Kept both: the board keeps its key, and while it serves its PID, address and version, in the repository's git folder (`chantier/board.json`), and removes the merged CRs' worktrees and branches at a batch's end (below), and,
2. batch_status.py, `status()`. Kept both: the multi-line `lines = [...]` with `*_other_batches_lines(repo)` after `*_autosync_lines(repo)`, then `lines += _unpaused_line(d)`. Both helpers exist in the file; no import change needed.

No BOM added (AGENTS.md starts with "# A"); no markers left. Staged by path, rebase continued and finished.

Fast gate: `just check` -> ruff clean, 443 passed in 20.24s, release-notes ok. Pass.
