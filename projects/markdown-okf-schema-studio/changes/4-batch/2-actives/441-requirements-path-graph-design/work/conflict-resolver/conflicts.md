# Conflicts, CR-441 rebase onto 4f982640

- Commit 13cb386b: one conflict, `requirements/tiers/log.md` (2026-11-21 section). HEAD added the CR-439 entry, the CR added its CR-441 entry. Kept both; order newest first: CR-441, CR-440, CR-439. No BOM.
- Commit 5abb7af1: applied with no conflict.
- Rebase finished successfully; nothing pushed.

Fast gate: `just check` (as run in the worktree) passed, exit 0 (only existing W2 broken cross-link warnings from okfreq).
