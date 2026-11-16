# Cost: steering turns are not grill turns

## The request

From the retro of real-direct run 1 (2026-11-12, PR 137, finding 3): in a direct batch, `cost`
moves steering turns of the Chief of Staff to the line "grill and specifications with the user
(outside the budget)" although no CR was grilled and no spec-writer ran.

## The problem

- In direct mode the Chief of Staff's transcript is priced from its claim as one row, `Chief of
  Staff, steering the batch`, which counts in the spend and the budget. The turns that grill or
  write specifications leave that row for the grill line, outside the budget
  (`chief-of-staff.md`, "Your epoch").
- `costs.py` decides this per turn (`_grill_use`, `GRILL_NAMES`): a turn is a grill turn as soon
  as the input of any of its tool uses names `01-intent.md`, `02-answers.md`,
  `03-change-spec.md` or `work/specifying`, or starts a spec-writer. The turn goes whole to the
  grill line.
- A steering session names those paths all the time without grilling: the prompt of each Driver
  it starts names the CR's `03-change-spec.md`, and so may a message to a Driver, a command or a
  plain read of a specification. Each such turn leaves the budgeted row.
- Measured on run 1 (every call priced again from the raw transcripts; the per-role and per-CR
  figures were exact to the cent): steering shown $1.18, really $3.61; the batch shown $9.41,
  really $11.84 of a $20 budget; orchestration shown 50%, really 61%. The steering row also
  shrank between two readings ($1.33 then $0.99), because later tool uses reclassified turns.
- Consequences: the budget rail under-counts a direct batch, the report's steering share is
  understated, and the scorecard's direct/Foreman comparison reads a wrong row.

## What would fix it

Inside the steering window, a turn belongs to the grill only when it does grill or specification
work: it writes a CR's intent, answers, specification or `work/specifying` marker, or it starts a
spec-writer. A path that is only named (in the prompt of another agent, a message, a command) or
only read is steering. The request's own wording ("a path that only appears in a `take` output or
an Agent prompt") is the likely cause, not a proved one: a `take` output is a tool result, which
the attribution never reads, so the first step is to find on run 1's transcripts which tool uses
did reclassify the turns.

Done when: on run 1's transcripts the grill line is $0 inside the steering window and the
steering row is the repriced figure ($3.61 at the close, to the cent of the report's method);
a turn that records an answer or starts a spec-writer while steering still goes to the grill
line; the card's sentence on the split says the same thing as the CLI.

## Out of scope

- The split outside a steering window (a Chief of Staff beside a Foreman): unchanged.
- The shape of the cost table and of the reports: the same lines, only the figures move.
- The default budget, and any re-run of the eval; the run 1 report already carries the
  correction and is not rewritten.
- Copilot's cost path (`copilot-session-usage`), which has no such split.
