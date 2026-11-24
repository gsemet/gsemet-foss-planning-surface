# The CLI prints the ready line and the batch's state; rules come back after a compaction

Short name: `ready-line`. The user's words of 2026-11-23: be sure the important rules are
reloaded at a compaction, and have the CLI print the batch's state (mode, slots...) so the agent
does not forget it.

In batch-31 the Chief of Staff wrote its ready-to-merge lines by hand. They had no colour icon,
they used named links instead of the PR's URL, and they did not quote each gap next to its link.
After a compaction it also forgot the batch's state, and `status-layout.md` is read only by the
status action and before a report, not at a reload. The fix has three parts:

1. `chantier status` prints one ready line per CR handed back. The line has the icon and word of
   the CR's `label`, the full PR link, each gap, a "do not merge before X" clause when a step is
   still owed, and the local gate clause. The agent copies that line.
2. `chantier status` prints one `batch:` line with the batch's state: shape, slots, steering,
   rounds limit, budget, who owes the local gate, and who merges.
3. After a compaction, the Chief of Staff and the Foreman read a short piece of rules: the report
   layout, the ready words, the shape rule, and who merges.
