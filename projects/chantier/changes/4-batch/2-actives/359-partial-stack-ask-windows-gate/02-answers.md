# Answers

- The user (2026-11-17), on the five retro points of batch-24: "remet les 5 dans le batch et on
  continue" (put the five back in the batch and carry on). No grill: the behaviour choices below
  are the Chief of Staff's.
- The retro point (intake): a partial stack was merged before the local Windows `just scenario`
  had run at its top (one `gate` event only, CR-334 at 796686b). The `stack-ready-to-merge` ask for
  a partial stack states whether that gate ran at its top, and the card names it as a condition of
  that ask.

## Settled by the Chief of Staff

- **Which rule.** Generic, not Windows-specific: it applies when the project's rules ask the
  stack's top for a local run of the long gate (chantier's `AGENTS.md`: "the CR on top of the stack
  also passes `just scenario` locally (`chantier gate`) at its head before the user merges"). With
  no such rule, nothing changes and the ask carries no new clause.
- **Which head.** The top of the mergeable part: the PR whose head is the `<sha7>` of "partial
  stack mergeable below <sha7>", not the stack's top draft. That is what the user merges.
- **Who runs it.** The stack driver, in that CR's worktree, with `$CHANTIER gate <cr>
  "<command>"`, before its hand-back that makes the first stack, unless a pass is already at that
  head (a gate it ran, or a `carried:` line of `ship` at that head). No new Driver, no CLI change.
- **What the ask says.** A clause `local gate <cr> at <sha7>: passed|failed|not run`, before the
  `to come:` tail, in the partial form only. The complete form is unchanged (its top's Driver
  already hands back on its own local pass, with no `--no-gate`).
- **The condition.** The Foreman sends the partial ask only with `passed`. A `failed` run is the
  stack driver's anomaly: no ask; the CR goes back to its Driver for a round. One exception: at a
  `deliver by <time>` time, the ask goes as it stands, with `not run` or `failed` stated.
- **What the user hears.** The Chief of Staff quotes the clause in the user's language before
  saying the stack is mergeable; with `not run` or `failed` (or no clause in a project with the
  rule), it says the project's rule asks that gate before the merge and it has not passed at that
  head; merging anyway is the user's choice and is recorded as any merge, never refused.
- **The record.** The pass is the CLI's `gate` event at that head (`events.jsonl`). `status`'s
  "Long gate" column keeps showing `exempt: <rule>` for a CR handed back with `--no-gate`: no CLI
  or pane change in this CR.
- **Gates of this CR.** A cards-only change: `just check`; the pipeline's `just scenario
  (ubuntu-latest)` green at the PR's head; the batch's top-of-stack local `just scenario` when this
  CR is the top. No `just eval-dry-run`, no `just mod`, no pane screenshot.

- Settled by the Chief of Staff (the spec-writer's open question, growth of the mergeable part):
  the local gate runs again at each new top of the mergeable part before each new partial ask, as
  AGENTS.md already says ("when a CR joins on top, the local run moves to it"); a head with a pass
  or a carried pass is not run again.