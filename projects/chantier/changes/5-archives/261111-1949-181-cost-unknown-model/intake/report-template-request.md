# The reports follow a template, the cost formatted, with room for extra messages

The user's words (2026-11-11, after a `/chantier:status`-shaped report in batch-09): "Il faut
que tu formattes la sortie de cost sur un "status". De manière générale il faut que la sortie
soit avec un template mais en laissant la possibilité de rajouté des messages supplémentaire".

## What happened

The Chief of Staff's Progress report pasted `$CHANTIER cost`'s output raw, in a code block, as
`status-layout.md` "Cost" asks ("the lines of `$CHANTIER cost`, as printed and in that order").
On a phone it reads as a dump, not as part of the report.

## What main says today (b3b2da4)

- `status-layout.md` fixes the columns of the Progress and Completion tables and leaves "the
  text around them" to the writer; the cost part is the raw lines of `cost`.
- The report's shape is described in prose; there is no template file.

## What the user wants

- The cost formatted inside a status report (a table, like the CR table), not raw output.
- More generally, the report comes from a template: a fixed skeleton every report follows,
  with named places where the writer may add extra messages (explanations, warnings, tips).

## Open points for the grill

- Where the template lives (a card, an asset file the CLI prints, or `status` itself printing
  the formatted report), given the CLI's scope rule in AGENTS.md.
- The cost table's columns (who, figure, calls; the Chief of Staff's own line apart).
- Which places accept extra messages, and their order.

## Addition (2026-11-11)

The user's words: "Et dedans tu me donnes un ratio sur l'orchestration".

- The report's cost part gives a ratio of orchestration: what the steering (the Foreman, or the
  Chief of Staff steering in direct mode) and the Drivers cost, against the workers who do the
  work. Today `status-layout.md` "Cost" forbids grouping ("no orchestration, implementation or
  review lines"): the grill decides the ratio's definition and amends that rule.
- Example, batch-09 at $93.53: steering $43.28 (46 %), Drivers $16.31 (17 %), workers $33.94
  (36 %); orchestration (steering + Drivers) 64 %.

## Correction to the ratio (2026-11-11)

The user's words: "Attention je pense que tu as pris ta session entière alors qu'on a enchaîné
les batch dans la même session".

What the CLI does (commands.py `_window`, `_chief_line`, read at b3b2da4):
- The steering row is not the whole session: it counts the Chief of Staff's transcript from
  its claim of batch-09's seat to now, spec-writers excluded. The whole session ($179.76) is the
  `Chief of Staff:` line's second figure; earlier batches are outside the steering row.
- But the window has no end and no gap: in direct mode it counts everything the session did
  since the claim, grill turns while the batch was paused, filing items, and answers to the
  user's questions included. So the 46 % steering share is too high by an unknown amount.
  CR-165 (systematic-retro) splits "grill and specifications" from "steering the batch".
- A Chief of Staff's own `Explore` subagent shows as "Driver Explore" ($0.55, Opus): it has no
  parent link to a CR, so it is classed as a Driver. It belongs to the Chief of Staff.

The ratio of orchestration must be computed on the steering share CR-165 measures.
