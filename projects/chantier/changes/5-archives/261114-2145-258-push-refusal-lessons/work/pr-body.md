## Summary

When the host refuses a Driver's force push, the CR's record only said "Force push refused by host", so nobody could tell a missing allow rule from the classifier blocking a matching rule. The Driver also waited in its turn for the push result and could run out of context while it waited. This changes the cards so the refusal is recorded exactly and the Driver ends instead of waiting.

## Deliverables

A CR Driver (or Release driver) whose force push is refused now ends its turn, and a fresh Driver continues once the answer arrives:

```mermaid
sequenceDiagram
    participant D as Driver
    participant F as Foreman
    participant C as Chief of Staff
    D->>D: note "refused: <command> -> <host text>"
    D->>D: note "next after push: <steps>"
    D->>F: handback blocked waits: push ...; push line
    Note over D: ends, no wait
    F->>C: push line, as it came
    C-->>F: pushed / push failed / push refused
    F->>D: take --note "push: <answer>", fresh Driver
    Note over D: acts on the answer from "next after push"
```

Choices made: the hand-back reason is the existing `waits:` (no new reason, no CLI change); the stack driver keeps its rule (it sends the push line and waits), since a hand-back halfway through a restack is another shape.

## Blast radius

The change is to instruction cards only; a plain `git revert` restores the previous behaviour.

Grade: 1

## Autonomous decisions

- Also changed `evals/SCORECARD.md` (row J11) and `evals/real-direct/RUNBOOK.md`, which said the Driver hears the push result as a live note; left the earlier release notes as history.

## Known gaps

- The stack driver still waits for the push result in its turn; it is left out on purpose and can be filed again if a stack batch shows the same context loss.
- No automated check that a `refused:` note exists before a `waits: push` hand-back; a new CLI rule needs measured cost first.

<details>
<summary>Details</summary>

## Changes

- `driver.md`: the force-push bullet records `refused: <exact command> -> <host's exact text>`, then `next after push: <steps>`, then `handback <cr> blocked waits: push <branch> <expected> <local>`, sends the push line and ends; a fresh Driver reads the four answers from its `take` note.
- `foreman.md`: on each answer the Foreman takes the CR back with `take <cr> --note "push: <answer>"` and starts a new Driver before any queued CR, without a round; it handles an answer that comes before the hand-back, and never pings a CR handed back `waits: push`.
- `routing.md` (rows 12 and 15), `chief-of-staff.md` (step 4, direct mode), `status-layout.md` (the report quotes the recorded refusal, or says none was recorded), `hosts/claude-code.md` (Auto mode clause).

## Human decisions

- Only the exact-text record and the hand-back instead of a wait are in scope; the permission rules and the Chief of Staff's own push are unchanged.
- The stack driver is left out of this change.

## Impacts

No visual change; the cards read differently for Drivers, the Foreman and the Chief of Staff.

## Test plan

- [ ] New or changed tests: No behaviour change (cards only)
- [x] Local gates at `4254a29`: `just check` (by the author of the change) and `just scenario` pass
- [x] Evidence at `4254a29`: read-through of the cards with `git grep`, and a CLI check in a scratch project: `handback <cr> blocked waits: push ...` exits 0 and `take <cr> --note "push: ..."` counts no round
- [x] Review: approved at `4254a29` (reviewed at ce00ec3 uncommitted, committed as 4254a29)
- [x] Verified at `4254a29`
- [x] CI green at `4254a29`: five checks pass (`just check` on three systems, `just eval-dry-run`, `just scenario`)

## Internal references

- CR-258 push-refusal-lessons
- Specification: `.agents/changes/4-batch/2-actives/258-push-refusal-lessons/03-change-spec.md`

</details>
