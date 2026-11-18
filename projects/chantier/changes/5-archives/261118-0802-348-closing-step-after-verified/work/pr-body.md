## Summary

A CR Driver that has driven a change through its rounds, the long gate and the verification often runs out of context just after the Verifier's `VERIFIED`, while it writes the PR description. Several Drivers hit the 130,000-token hand-back limit there and needed a fresh Driver to re-read the state. This change makes that hand-off systematic: the first `VERIFIED` at the pushed head ends the Driver's run with a recorded note, and a fresh Driver that reads only the CR's notes does the closing work.

## Deliverables

The closing hand-off, as the cards now describe it:

```mermaid
sequenceDiagram
    participant D as CR Driver
    participant F as Foreman
    participant N as Fresh Driver
    D->>D: Verifier replies VERIFIED at pushed head
    D->>D: note "closing: VERIFIED at sha7; ...; next: ..."
    D->>F: handback blocked "context: closing: VERIFIED at sha7; next: ..."
    F->>N: take with note "resume: closing" (no round, no ask)
    N->>N: evidence, description pass, PR ready, handback ready
```

- The hand-back reason `context: closing: ...` needs no 130,000-token reading, and a Driver started with `resume: closing` (or whose log holds a `closing:` note) never hands off for it again.
- `handback` prints a dedicated line for it: "<cr> verified; the Foreman restarts a fresh Driver for the closing step, with no ask to the Chief of Staff".
- The Foreman restarts it without counting a round or a "driver out of context" end.

## Blast radius

Grade: 1. Card text, one printed line in the CLI and one scenario check; `git revert` restores the previous behaviour. The record format does not change.

## Autonomous decisions

None.

## Known gaps

- The long gate ran in CI only (Ubuntu), not locally.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: the CR driver's closing hand-off and note, the `resume: closing` reading rules, the exception to the 130,000-token rule, the no-loop rule, the Startup core line.
- `skills/chantier/references/foreman.md`: the `context: closing:` take-back path and its exclusion from the context counting.
- `skills/chantier/scripts/cli/src/chantier/commands/driver_checks.py`: `handback_blocked` prints the closing line before the general `context:` branch.
- `scenario/run_scenario.py`: one check of the closing hand-back and take-back, and the card strings.

## Human decisions

- The hand-off always happens at the first `VERIFIED` recorded at the pushed head while the closing is still to do; a matrix probe's `VERIFIED` or a verdict carried by `ship` does not trigger it.
- The closing step is a fresh Driver started by the existing restart path; no new role.
- The hand-back is `blocked context: closing: VERIFIED at <sha7>; next: ...` and the take-back note is `resume: closing`.
- The closing Driver reads only the CR's notes; it reads the specification, investigation, round notes and diff only when a step outside the closing comes up.
- A Driver started with `resume: closing`, or whose log holds a `closing:` note, never hands off for the closing again.
- A closing hand-off does not count as "out of context" or "driver ended"; reports call it "the closing step".
- Scope is the CR driver only; the CLI changes only the line `handback` prints.

## Impacts

No visual change. A CR Driver's run now ends at its pushed-head `VERIFIED`, and a fresh Driver closes the CR.

## Test plan

- [x] New or changed tests: scenario check of the closing hand-back and take-back (fails on the previous code)
- [x] Local gates: carried from `4d58060` (`just check`; clean rebase onto CR-347, head `b359d53`)
- [x] Evidence: No visual change
- [x] Review: carried from `4d58060` (approved at `ef9f977`; clean rebase onto CR-347, head `b359d53`)
- [x] Verified: carried from `4d58060` (clean rebase onto CR-347, head `b359d53`)
- [x] CI green at `b359d53` (checks on three systems, scenario, eval dry run)

## Internal references

CR-348 closing-step-after-verified.

</details>
