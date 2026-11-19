## Summary

A change request that runs out of rounds because of a red the batch itself caused (a restack, a rebase onto another request's branch, a request merged or moved below it) used to wait for the user to grant one more round, even for a trivial fix. The Chief of Staff may now grant the next round itself, up to two, and tells the user in the same message. This is called the rounds exception; every other grant of rounds stays the user's.

## Deliverables

The rule, as the cards now state it:

| | Before | After |
| --- | --- | --- |
| Who grants a round past the limit | the user only | the user; the Chief of Staff too, when the batch caused the red |
| Cap | none for the user | for the exception: the batch's `settings.max_rounds` + 1 per grant, never above `max_rounds` + 2 (default: the 4th, then the 5th round) |
| Orders sent to the Foreman | `order rounds <cr> --note <n>` | the same, plus `order note <cr> --note "rounds exception: <event>; <failing check>"`, in one message |
| Next Driver's take | `escalate: rounds` | `take <cr> --note "rounds exception: <cause>"`, no escalation |
| Blocked twice | a `rounds:` hand-back counts | one covered by the exception does not count |

The CLI is unchanged: `order rounds` keeps its whole-number note and the Foreman holds no check of the cap; the Chief of Staff alone answers for using the exception rightly.

## Blast radius

Grade: **1**. Card wording only; a plain `git revert` restores the previous rule.

## Autonomous decisions

- The exception is stated in the Chief of Staff, concepts and Foreman cards and the eval scorecard only, with no CLI change, as the specification asks.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/chief-of-staff.md`: a "rounds exception" paragraph in Steering, the `order rounds` comment, row G of the refusals table, and the Escalation bullet of direct mode.
- `skills/chantier/references/concepts.md`: the rounds sentence of "Slots, budget, rounds", the first escalation row, the blocked-twice row.
- `skills/chantier/references/foreman.md`: the take with a `rounds exception:` note, and the Escalation bullet.
- `evals/SCORECARD.md`: row C4.

## Human decisions

- A red caused by the batch (a restack, a rebase onto another request, a request merged or moved below) lets the Chief of Staff grant the 4th and 5th round, and tell the user, without waiting.
- The Foreman takes every `order rounds`; there is no hold rule and no check of the cap.
- A grant under the exception keeps the batch's model (no escalation) and does not count toward "blocked twice".

## Impacts

No visual change. Chief of Staff and Foreman sessions follow the new rule from the next session.

## Test plan

- [x] No behaviour change: cards only, no test added
- [x] Local gates at `0449478` (carried to `c23abc5`): `just check` passes
- [x] Evidence: none (cards only)
- [x] Review: approved at `c23abc5` (carried from `0449478`)
- [x] Verified at `c23abc5` (carried from `0449478`)
- [x] CI green at `c23abc5`: all 5 checks pass

## Internal references

- CR-387 the-chief-of-staff-grants-a-4th-and-5th

</details>
