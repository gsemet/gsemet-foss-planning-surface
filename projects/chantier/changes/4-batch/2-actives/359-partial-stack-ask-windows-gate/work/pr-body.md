## Summary

A partial stack (a mergeable part with drafts or CRs still to come) could be offered for merge before the project's local gate had run at the top of the mergeable part. The project's rule asks the stack's top for a local run of the long gate; for a partial stack, the part the user merges had no such run.

This change makes the stack driver keep one invariant under such a rule: the top of the mergeable part has passed the local gate at its head. Each partial merge ask now states the result, and the Chief of Staff tells the user what it says before saying the stack can be merged. Cards only.

## Deliverables

The partial ask gains a clause, worded the same in the three cards:

| Card | Where the clause appears |
| --- | --- |
| `driver.md` (stack driver) | the hand-back: `hand-back ready to merge <stack link> <cr>=<link>… local gate <cr> at <head7>: passed\|failed\|not run` |
| `foreman.md` | the partial ask and the asks list: `… local gate <cr> at <sha7>: passed to come: …`, sent only on `passed` (a `deliver by` time excepted) |
| `chief-of-staff.md` | quoted to the user before the sentence that says the stack can be merged |

Choices: the gate runs at the first mergeable top and at each new top (draft turned ready, restack, insertion, drop), skipping a head that already has a pass or a carried pass; a PR turns out of draft only once its gate passed; a failed gate stays a draft and the previous top keeps its pass; merging anyway stays the user's choice.

## Blast radius

Grade: 1. Three cards change; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

None.

## Known gaps

- The behaviour is unproved until a real stack batch makes a partial stack under the rule; the trial is a hand-back that carries the clause, with a gate event of the mergeable top at that head before the ask.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: the local gate at the mergeable top, wired into the first stack, a draft turned ready, the restack, the insertion and the drop; the deliver-by case; the hand-back line.
- `skills/chantier/references/foreman.md`: the partial ask and its condition, the failed-local-gate anomaly, the deliver-by case, the asks list.
- `skills/chantier/references/chief-of-staff.md`: the clause told to the user on a partial ask.

## Impacts

No visual change. A partial ask under the rule now carries the local gate's result.

## Test plan

- [ ] New or changed tests (they fail on the previous code): no behaviour change in the CLI
- [x] Local gates at `79c3fe0`: `just check` passes
- [ ] Evidence: none, cards only
- [x] Review: approved at `79c3fe0`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-359 partial-stack-ask-windows-gate.

</details>
