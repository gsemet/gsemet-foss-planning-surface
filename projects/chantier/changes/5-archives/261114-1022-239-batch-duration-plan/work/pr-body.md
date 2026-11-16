## Summary

The Chief of Staff (the agent that steers a chantier batch for the user) used to promise a delivery time ("you should have a stack when you wake up") with no figure behind it, and a 13-change batch with a six-level dependency chain missed it two nights running. The Chief of Staff's card now allows a delivery time only when it comes from a "floor": a lower bound counted by hand from facts the record and the forge already hold. It is never a prediction.

## Deliverables

The floor is the larger of two terms:

| Term | Count |
| --- | --- |
| Lock term | changes still to pass their long gate x the long gate's time (long gates run one at a time) |
| Chain term | depth of the dependency chain x (long gate time + one CI run), since a level cannot start before the one under it is ready |

Card example: "lock: 13 gates x 35 min = about 7.6 h; chain: 6 levels x (35 min + <CI> min); at least the larger; critical path: <first change> -> ... -> <last change>."

- Before the go, the plan shows the floor, its critical path and the delivery time ("not before <time>"), or "unknown" when no gate time is on record. When the floor exceeds the time the user gave, the plan also proposes a cut (the largest set of changes that fits, short chains first) and the user chooses.
- Every progress report gives the remaining floor and the updated delivery time, says a slip of an hour or more with its cause, and names the mergeable partial stack (`partial stack mergeable below <commit>`). When the time will not hold, the steering aims at the largest mergeable partial stack from the bottom.
- Choices made: no estimator, no median, no new CLI command; a slip is only reported (no new cut); with no gate time, no delivery time is told.

## Blast radius

A card-only change to the Chief of Staff's behaviour; no code. Revert restores the previous wording.

Grade: **1**

## Autonomous decisions

- When the CI run's time cannot be read (no `gh` or `glab`, no rights, no passed run), the chain term counts the gate alone, the line says `CI time unknown, not counted`, and the delivery time is still told as "not before". The specification left this open and chose this default.

## Known gaps

- The card's example leaves the CI run's time as a symbol, since the specification holds no measured one; the worked example with measured figures is in the Test plan.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/chief-of-staff.md`: new subsection "The floor"; the plan (step 2 of "Starting a batch") gains a floor item and a "cut" paragraph; the "Reports" bullet gives the remaining floor, the slip and the partial stack; new bullet "When the time will not hold"; a Hard rule and a Never bullet.
- `skills/chantier/references/status-layout.md`: Notes of a Progress report hold the floor line, the slip line and the partial stack line; the Completion report gets none.

## Human decisions

- The floor is counted by the Chief of Staff by hand; no CLI change.
- When the floor exceeds the time given, the plan proposes a cut and the user chooses.
- With no gate time on record, the floor is the depth alone and no delivery time is told; nobody is asked and no gate is run to measure it.
- A slip past the time given is only reported; the steering works toward the largest mergeable partial stack.
- Each level of the chain counts at least one long gate and one CI run.
- Progress reports say regularly where the mergeable partial stack stands ("partial stack mergeable below <commit>"), beside the floor.

## Impacts

No visual change; the Chief of Staff's reports gain a floor line and a partial stack line.

## Test plan

- [x] New or changed tests: No behaviour change (cards only)
- [x] Local gates at `af970ea`: `just check` pass, `just scenario` pass (long gate)
- [x] Evidence at `af970ea`: `rg -n "floor"` finds every listed element in the two cards. Worked example, 13 changes at depth 6: gate run 20261113-190315-26164 took 24 min (19:03:15 local = 18:03:15Z, ended 18:27:15Z); a recent passed CI run 10.4 min (`gh run list --json`, run on 8566cca); lock term 13 x 24 = 312 min (about 5.2 h); chain term 6 x (24 + 10.4) = 206.4 min (about 3.4 h); floor at least about 5.2 h, the lock term binding
- [x] Review: approved at `af970ea` (inspector pass recorded on the pre-commit tree)
- [x] Verified at `af970ea`
- [x] CI green at `af970ea`: gh pr checks 181, all five checks pass

## Internal references

- CR-239 batch-duration-plan
</details>




