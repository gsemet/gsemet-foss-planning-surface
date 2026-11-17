# Conflicts, CR-320 rebase onto CR-319's new head (commit 17b1c6b)

- skills/chantier/references/foreman.md (heartbeat end): kept the base's "the pause (the CLI's or yours)" and CR-320's "first wake that sees no Driver ... run for 30 minutes or more, whatever the wake's interval, and no order is undone" plus "The 30 minutes do not follow the wake". The base's "since the last wake" idle condition was replaced.
- skills/chantier/references/hosts/claude-code.md (ScheduleWakeup end): kept the base's "every pause already does", "right after the pause, the steering session's own or the automatic one (the record alone does not stop the wake...)", and CR-320's 30-minutes-whatever-the-interval idle condition.
- skills/chantier/references/hosts/copilot.md (/every): kept CR-320's `<steering wake>` / `timing:` line wording and the base's "every pause, the automatic one included, ... in direct mode, in its own session" delete-the-/every wording, plus CR-320's idle condition.
- No product-intent conflict: both idle conditions say the same thing (CR-320's is the interval-independent form).
- No BOM in the three files (first bytes checked); staged by path; `GIT_EDITOR=true git rebase --continue` succeeded.

Fast gate: `just check` -> passed (biome clean, 422 tests passed, release-notes ok).
