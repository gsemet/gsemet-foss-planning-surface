# The worker write guard, redesigned

The user (2026-11-11, after batch-10 stopped): "Redesign cette protection".

## What happened in batch-10 (the `real` eval, Foreman mode)

- CR-171's guard (`hooks/register.tsx`, on main at 1e99343) refused every Write and Edit of
  every worker, in its own worktree and CR folder too, with an empty path in the message
  ("refused:  is outside this CR's worktree ...").
- Cause: the hook reads the path from `e.input.file_path`, but a `tool.call` event carries the
  tool's arguments flat (`e.file_path`); `input` exists only on the permission event.
- Its tests (`hooks/register.test.tsx`) never ran: the `claude` CLI is not on the Windows
  machine's PATH, and CI does not run `claude plugin test`. The Verifier passed CR-171 without
  them.
- Effects:
  - CR-172 spent one of its three rounds with no code written.
  - CR-173's Investigator could not write its note in `work/`; a worker then tried the same
    write by PowerShell (refused by the host's auto-mode classifier), and the Driver wrote the
    note for it: an action refused to a subagent, done on its behalf.
  - The batch stopped at $2.47; the user said "On stop tout".
- Shell writes (Bash, PowerShell) are not guarded at all.

## Open for the grill

- Shell writes: guarded or not.
- A guard that cannot read a call (no path, an unknown shape): refuse, or let through.
- What a refused worker and its Driver do; whether the Driver may ever write in its place.
- How the hook's tests run before a hook change merges (absorbs point 1 of
  `cr-171-retro-fixes`).
- How the next eval proves the guard.
