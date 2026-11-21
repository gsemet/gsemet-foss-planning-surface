# Conflicts: CR-427 rebase onto origin/main

One conflicted file: `skills/chantier/references/chief-of-staff.md` (commit f89cb50f), one hunk in the Chief of Staff's command table.

- "board on my phone" row: kept main's (network host, `board.host: network`, `--host`); dropped the CR's older `board.host: 127.0.0.1` wording, which main replaced.
- "a new board key" row: kept main's (new in main, absent from the CR).
- "rescan" row: kept the CR's, adding "a `running-batch` write, a move to `3-ready`, or a move that clears a running-batch mark: act as at a watcher's end". The rest of the row is identical on both sides.

No BOM added; no conflict markers left.

Fast gate: `just check` (in the worktree, after the rebase): 1531 passed, 20 skipped; release-notes check ok. Pass.
