## Summary

A batch's Driver, the stack driver and a QA order each hold a short lease (10 minutes) on the unit `take` or `order qa` gave them, renewed by their own commands. A live lease protects the unit from a second Driver; a lease that expired is only "not confirmed": the steering session checks with the host that the Driver ended, then takes the unit again with `take --reclaim`. On Copilot, `close` reads leases in place of the "session file written in the last 5 minutes" heuristic. A long CI watch or long gate keeps the lease live.

## Deliverables

New and changed commands:

| Command | What it does |
| --- | --- |
| `take <cr\|stack>` | starts lease `n`, refuses a live or not-confirmed one, `--reclaim` takes it anyway and logs `reclaim` |
| `--lease <n>` | required on `round`, `ship`, `handback`, `release start\|go\|published` and the stack driver's writing forms; optional on `gate`, `note`, `phase`; renews the lease; a stale number gets `claim lost` |
| `lease <unit>` | prints the lease: live, not confirmed, ended, or none |
| `lease <unit> renew --lease <n>` | renews |
| `lease <unit> hold --lease <n> -- <command>` | runs one command as a child and keeps the lease live while it runs, renews once at its end |
| `agents set <cr\|O-k\|stack> -` | ends a live lease; a not-confirmed one is left for `--reclaim` |

Choices: 10 minutes renewed every 3 are constants (no configuration); the state lives in `batch.json`, local, never published; times in lease texts are UTC; a batch opened before this version needs no `--lease`.

## Blast radius

Grade: 2. It touches the take, round, ship, hand-back, release, stack and QA-order paths and Copilot's `close`; a revert restores the previous behaviour, and batches opened under it carry a lease field earlier code ignores.

## Autonomous decisions

- `ship`, `stack` and `forge-stack` accept a unit whose lease already ended with no number (the stack driver's `ship` of a CR already handed back, and its calls after `agents set stack -`, have none to pass); a stale number still gets `claim lost`, a live or re-taken lease still needs its number.
- `agents set O-k` after a clearance that ended lease 1 before any agent was recorded starts lease 2 (the specification does not say).
- `lease hold` reads `--batch` and `--lease` only before `--`; the driver card says so.
- Command files were split (`commands/agents.py`, `commands/leases.py`, `driver_notes.py`, `forge_stack_apart.py`, `rails_idle.py`) to keep each module small.

## Known gaps

- Departs from the specification: `ship`, `stack` and `forge-stack` accept a unit whose lease ended, with no number, where the specification gives `claim lost`. It was left because the stack driver has no number to pass after the lease ended; a stale number still gets `claim lost`.
- `agents set O-k` after a clearance that ended lease 1 before any agent was recorded starts lease 2; the specification does not say what it should do.
- No screenshot is owed: the change draws nothing on the board or the pane.
- The scenario's `parallel` unit runs about 200 s alone against a 260 s budget; under four parallel jobs it reached 248-261 s.
- A Driver's leftover background work after its hand-back is no longer seen by Copilot's `close` until the Copilot end-event work lands.

<details>
<summary>Details</summary>

## Changes

- `core/leases.py` (new): TTL, RENEW, liveness (expiry, a running or queued long gate of the unit, a live `lease hold` record), claim checks and texts; `core/records.py` gains `Lease`, `CrEntry.lease`, `BatchRecord.stack_lease`, `OrderRecord.lease`; `.lease-hold.*.run` is ignored.
- `take`, `order qa`, `order done`, `agents set`, `cancel`, `order drop`, `handback`, `release`, `stack`, `forge-stack`, `status`, `handoff` and the Driver facts follow the lease rules.
- `close` on Copilot: a held agent holds its unit while its lease is live; no lease reads `not measured (no lease)`; the Foreman counts while its heartbeat is under 10 minutes. On Claude Code a live lease is shown, never a cause.
- Cards (driver, foreman, chief-of-staff, concepts), `AGENTS.md`, the docs and the scenario say and exercise the same; the Driver card's common path stays under its 45,000-byte cap.

## Human decisions

- A lease is local to the machine that runs the batch, kept in `batch.json`, never published.
- Ten minutes, renewed every three, a constant (not configured).
- Quality orders get leases too, taken and renewed as a Driver does.
- On Copilot, `close` reads leases in place of the 5-minute session-file rule until the end-event work lands; on Claude Code the transcripts stay the source and a live lease is only shown.
- A long CI watch or gate keeps the lease live; an expired lease is only "not confirmed", and the steering session checks with the host before `--reclaim`.
- `lease` is a named exception to the measured-cost rule for new CLI tools, built on the user's "all" answer.

## Impacts

No visual change. Drivers pass `--lease <n>` on the named commands; the steering session uses `take --reclaim` after checking with the host.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_leases.py`, `test_rail_refusals.py` Copilot and Claude Code `close` cases
- [x] Local gates at `db78350`: `just check` pass, `just eval-dry-run` pass (18 of 18)
- [ ] Evidence: scenario units `parallel`, `release`, `gates` and others pass locally
- [x] Review: approved at `db78350` (code approved at 8bd198b, move reviewed at db78350)
- [x] Verified at `db78350`: every claim but the description's gaps, fixed since
- [x] CI green at `db78350` (check on three systems, eval-dry-run, scenario)

## Internal references

CR-403 driver-leases (batch-29), Part D of the planning-server split.

</details>
