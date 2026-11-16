## Summary

An agent that ends before its part is done, or is refused at its start, now comes back exactly once and never in silence: one restart from what the record holds, by one way (a message that resumes it, or a new start, never both), with a note that says why. This closes three gaps seen in a recent batch: a Driver ended by a host API error, Drivers lost when a direct batch switched to Foreman mode, and a refused agent that a message resumed beside its replacement, so that two spec-writers wrote the same file.

## Deliverables

The three cases, each answered once:

| Case | Way | Where |
| --- | --- | --- |
| Host failure (an API error ends a Driver) | the existing restart path, `resume: host failure: <text>`; not a silent end; a second failure with nothing new recorded becomes an ask | Foreman card, "A host failure" |
| Switch from direct to Foreman mode | live Drivers are stopped at once; the Foreman restarts each, `resume: switch to Foreman mode` | Chief of Staff card, Foreman card |
| First-line refusal | always a new start, never a message; a refused agent answers any later message with the same refusal | every agent file, concepts |

The refusal text, identical in all 24 agent files (12 roles, both hosts):

```text
... a message to me gets this same answer: start a new agent with that line." and stop.
Any later message gets the same answer.
```

One spec-writer per CR is guarded by the card: the `work/specifying` marker.

## Blast radius

Grade: 1. Cards, agent prompts, one doc and a structure test change; no code. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- Open questions took the specification's recommended answers: a repeated host failure becomes an ask; a switch stops the running Drivers at once.
- The specification says 13 roles per host; the repository has 12, and all 24 files are updated.

<details>
<summary>Details</summary>

## Changes

- `concepts.md`: refusal text; new paragraph "An agent that ends before its part is done" (causes, one way, worker restart); rule 3 points to it.
- `foreman.md`, `chief-of-staff.md`, `griller.md`, `driver.md`: host failure, switch, spec-writer guard, worker restart with no new round.
- `hosts/claude-code.md`: a row for resuming a stopped subagent.
- `agents/*.md` and `com.github.copilot/agents/*.agent.md`: the new refusal text.
- `docs/use-cases-direct.md`: the switch to Foreman mode.
- `test_structure.py`: asserts the new phrases.

## Impacts

No visual change. Agents started without their first line now answer every later message with the same refusal.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_structure.py` checks the new phrase in all agent files
- [x] Local gates at `308f510`: `just check`, `just scenario`
- [x] Evidence: No behaviour change in the CLI; the grep for the old phrases finds nothing
- [x] Review: approved at `308f510` (round 2 pass recorded at `7705f00`, committed as `308f510`)
- [x] Verified at `308f510`
- [x] CI green at `308f510` (gh pr checks 158: 5 checks pass)

## Internal references

- CR-217 agent-restart-once

</details>
