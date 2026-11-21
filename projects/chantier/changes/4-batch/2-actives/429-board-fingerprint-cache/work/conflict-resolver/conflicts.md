# Conflicts: CR-429 rebase onto origin/main (after CR-426)

Rebase: `git rebase --onto origin/main 7c1d8905`, stopped at commit 3 ("docs(board): cards, docs
and scenario for the server's file watch and the watcher's subscription").

## skills/chantier/references/chief-of-staff.md, "The pull path" bullet (one hunk)

- main (CR-426): added the handling of a `board wrote (...)` line that sets a CR's destination
  (write it into `02-answers.md`, latest word wins; `order add --note <folder>` for a
  `running-batch` line once the specification is final).
- this CR (spec section 6): added "After the user's no, merges go back to the user's word: no board
  reads the forge."
- Choice: kept both. Main's destination sentences first, then the shared `seq` sentence, then this
  CR's sentence. No byte-order mark before or after (file starts with `# C`).

Rebase finished; new head f90c6a3d.

## Fast gate

Command, as run in the worktree: `just check` (log: `work/gates/conflict-resolver-check.log`).
Result: pass (1668 passed, 20 skipped; release-notes ok).
