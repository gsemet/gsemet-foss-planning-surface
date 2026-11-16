# Answers

- 2026-11-07, the user: "tu mets le batch en pause quand tout est fini": once every CR is
  merged, the steering session lands the batch and it is paused; it is not closed (the Chief of
  Staff had planned the close flow at the end of batch-08).
- 2026-11-07, the user: the batch lifecycle is to be respecified, priority P1.
- 2026-11-07, the user (asked when a batch is closed): "je veux que quand un batch est complet,
  il est mis en pause. Et les coûts sont quand même affichés": a complete batch is paused, and
  the costs are shown at the pause all the same (today `land` says the cost is not final and only
  `close` prints it). The question of when to close was not understood; to ask again, plainly.
- 2026-11-07, the user: the state is called "paused" everywhere (CLI output, STATUS files,
  cards); "landed" goes away.
- 2026-11-07, the user: the end-of-run report's last line says the batch is paused and lists
  the inbox ideas ready for a grill; it does not mention closing.
- 2026-11-07, the user: the merged CRs' worktrees and branches are removed by the steering
  session before the pause, as foreman.md says today.
- 2026-11-07, the user (asked again, plainly): a batch can still be ended for good, only on the
  user's word ("close the batch"); until then a paused batch stays paused and takes the new CRs.
- 2026-11-07, the user: at the pause, the full cost to date is computed and shown (the cost
  table by role and its explanation, as the final report shows today); it grows if the batch
  runs again.
- 2026-11-07, the user, on the restated shared understanding (complete → worktrees cleaned →
  "paused", cost to date shown, new CRs set it running again, closed only on the user's word,
  same in Foreman and direct mode): grilled enough, with one change: the end message may invite
  the user to close the batch or to add other CRs to the same batch later (this replaces the
  earlier "does not mention closing").
- 2026-11-07, the user (spec-writer's open questions): the `land` command becomes `pause`
  (the command, the event in the history, the cards and the docs); `land` goes away.
- 2026-11-07, the user: a working batch's state becomes "running" (states: running, paused,
  closed); "open" as a state goes away.
- 2026-11-07, the user: the CLI reads an old `status: "landed"` as paused and rewrites it at its
  next write (batch-08 is recorded landed today).
- 2026-11-07, the user: the CR board's "Landed (n of m)" list becomes "Merged (n of m)", and
  `order slots 0` is called "hold" (no new Driver), so that "pause" names only the batch state.
- 2026-11-07, the user (spec-writer's second open question): the CLI also reads an old
  `status: "open"` as running and rewrites it at its next write, the same way as "landed"
  (batch-08 is running when this CR merges).
- Superseded by the answers above (was open): when `close` happens at all, and who asks for it; what the
  Completion report's last line says on a paused batch; how a paused batch differs from a landed
  one, if at all; what the next batch's `open` does with a paused batch (one batch open at a time).
