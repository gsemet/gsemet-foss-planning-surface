# Conflicts: CR-410 rebase onto origin/main

Commit replayed: 69c30dc0 (an outside poller writes issue events into the journal).

## AGENTS.md, "The CLI's scope", named exceptions (one hunk)

- Main side: the `lease` item ("One more exception to the measured-cost rule, not a git one: ...").
- CR side: the `interests` and `journal add` item.
- Choice: kept both. The lease item stays as main has it; the CR's item follows it, with the
  next ordinal ("Fourth, `interests` and `journal add`: ..."), text as in spec section 9.1 edit 3.
- Count recounted from the text as it stands: end-of-batch cleanup (First), surface server
  (Second), `lease`, `interests`/`journal add` = four. "Three named exceptions" became "Four
  named exceptions" (that opening sentence sits outside the conflict hunk; main's text said
  Three).
- The watcher sentence and the "outside poller" journal sentence merged without conflict and were not touched.

## scenario/run_scenario.py, `chantier()` method (one hunk)

- Main side: `lease_unit`/`words` helpers and `chantier(..., lease=True)` with lease injection.
- CR side: `chantier(..., stdin=None)` (the poller case feeds stdin).
- Choice: kept all of main's helpers and lease injection, and added the CR's `stdin=None`
  parameter to the signature: `chantier(self, *args, env=None, expect=0, cwd=None, lease=True,
  stdin=None)`. The `subprocess.run(... input=stdin)` line from the CR was already in the
  non-conflicting part.

## Checks

- No conflict markers left; the files keep their existing line endings; no byte-order mark added.
- `git rebase --continue` finished; working tree clean. Not pushed.
- Fast gate, as run in the worktree: `just check` -> exit 0 (1188 passed, 14 skipped;
  release-notes check ok). Raw log: work/gates/conflict-check.log.
