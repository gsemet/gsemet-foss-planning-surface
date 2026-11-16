# A batch closes only when nothing runs, and its cost is final there

## Problem

A batch's cost means something only if nothing spends after it is taken. Today:

- `close` only checks that the batch's folder holds no sub-folder: no CR status, no order, no agent.
- `land` refuses on recorded state only, and the CLI has no proof that an agent really stopped.
- `order add` reads no batch status: on batch-06 it was accepted 27 s after `land`, and CR-129 ran on
  a landed batch. The card says new work joins until `close`, so the add is right and the landed
  state is what is wrong.
- The spend stops at `landed` and `status` calls it final there: what runs after is in no figure.
- `land` builds its summary before it records its time, so a second `land` priced up to the first:
  `STATUS.md` showed $49.38 in its Cost section under a header of $53.12.

## Change

**`close` refuses while anything runs.** In `rails.py`, a check `close` calls, with or without
`--yes`: it refuses, naming each cause, on a CR that is not merged or cancelled, an open order, a
stack agent, or a transcript of the Foreman or of any agent of the batch written in the last 5
minutes. A Driver of any kind counts, a QA, release or user's own one included, with no role name in
the CLI: the transcripts are the batch's, whatever their type. A long tool call writes nothing, so
the recorded state stays the first proof. On Copilot, use what the host's session records offer; if
they give no such time, `close` refuses and says `not measured`.

**`order add` reopens a landed batch.** A CR added to a landed batch sets it back to running and
clears `landed`, with a line that says so. The Chief of Staff's card says it starts the Foreman's work
again by the usual order. `land` then runs again at the end, on a running batch only: a `land` on a
landed batch is refused.

**The cost is final at `close`.** `land` records a figure printed as not final, in `status` and in
`STATUS.md`. `close` prices the batch up to now, with no end date taken from `land`, and prints the
final breakdown, with and without `--yes`. The summary uses the same time as the state it records,
so a header and a Cost section can no longer differ.

**The cards.** `chief-of-staff.md`, Landing: the Completion report takes its figures from `close`
without `--yes`, and a refusal is reported to the user with its causes. `foreman.md`: the Foreman
ends its work and stays idle before the Chief of Staff closes. `concepts.md` and the README say the
same.

## Out of scope

The drivers' model (`drivers-sonnet`), pricing compaction calls, and keeping the final figures once
the folder is deleted.

## Done when

- On a fixture, `close` refuses, naming the cause, on each of: a CR ready, an open order, a stack
  agent, a transcript written within 5 minutes. It passes once none holds.
- `order add` on a landed batch sets it back to running; its spend then counts past the old landing.
- A second `land` on a landed batch is refused.
- `land` prints the cost as not final; `close` prints the final one, and a call made after `land`
  is in it.
- `STATUS.md`'s header and Cost section show the same total.
- The cards, the README and the scenario say the same thing.
- `just check` and `just scenario` pass.
