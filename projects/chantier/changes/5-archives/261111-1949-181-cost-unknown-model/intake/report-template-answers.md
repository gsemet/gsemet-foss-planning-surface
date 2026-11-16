# Answers: report-template

Grilled with the user on 2026-11-11. The option they picked is quoted.

1. **The ratio of orchestration:** (steering + Drivers) / total, one line under the cost table,
   the steering measured on the batch's window only (no grill, no specifications). (Picked:
   "(steering + drivers) / total".)

## Decisions of 2026-11-11 (the points still open)

Decided by a Fable advisor on the user's delegation: "Grille tout avec une session fable je ne sais pas te répondre…"

2. **The template lives in the card `status-layout.md`, as a literal skeleton for each report**
   (Progress, Completion), read before every report by the Chief of Staff and by
   `/chantier:status`. No template file elsewhere and no new CLI command. Reason: a role's
   contract lives in the cards; the CLI gives the figures, the writer gives the report.
3. **The skeleton's order is fixed:** header line; legend and CR table; **Notes**; cost table and
   the ratio line; **Cost notes**; the Completion report's own parts (not proved, Retro);
   **For you**; the Tip. Reason: the user reads it at a glance on a phone; the same place every
   time.
4. **Two places accept extra messages, and only these: "Notes" under the CR table and "Cost
   notes" under the cost table.** Short lines in the user's language (explanations, warnings);
   an empty place is left out, not written "none". The lines the card already asks for (what a
   waiting or blocked CR waits for, a chain, a force push run for a Driver) go in "Notes".
   Nothing but the Tip follows **For you**. Reason: free text has a home without moving the
   fixed parts.
5. **The cost is a table, never raw output in a code block.** Columns: who, cost, share of the
   batch's spend, calls. Rows, in `cost`'s order: the steering session, its own subagents, each
   Driver type, each worker type, the total. Reason: the user's request; same look as the CR
   table.
6. **The Chief of Staff's own lines (steering outside the budget, grill and specifications,
   whole session) are a second short table under the first, headed as outside the batch's
   spend.** Reason: they are not in the budget; mixed in, the shares would not add up.
7. **Every figure, share and the ratio come from the CLI as printed: the writer copies, and
   computes nothing.** `cost` prints the shares and the ratio line; the card's "you group, add
   and regroup nothing" stays, with the ratio as the one grouping, made by the CLI. Reason: an
   agent's arithmetic is the error the user caught in batch-09.
8. **The ratio (answer 1) uses the steering row as `cost` prints it today.** Main already
   splits the grill and the specifications from the steering, and already labels the steering
   session's own subagents (the "Driver Explore" defect is covered by `cr-171-retro-fixes`
   point 3). Nothing more is designed for it. Reason: checked on main at 24cc7eb.
9. **Where a part is not measured, the cell says `unknown` or `not measured` as the CLI prints,
   and the ratio line says "not measured" rather than a partial ratio** (Copilot, where a Driver
   cannot be told from a worker; a floor from an unpriced model, see `cost-unknown-model`).
   Reason: the reports' rule; a ratio on half the data misleads.
10. **`cost --explain` stays prose, in the Completion report only.** Reason: it explains, it is
    not a table; unchanged.
11. **One CR with `cost-unknown-model` and point 3 of `cr-171-retro-fixes`.** Reason: same
    `cost` code and same card.
