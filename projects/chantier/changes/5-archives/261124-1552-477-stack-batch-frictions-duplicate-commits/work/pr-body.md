## Summary

In a stacked batch, four frictions slowed the work: after a rebase merge the PR above still showed the merged PR's commits; `take` printed the wrong base after a reorder; `ship` printed `off:` where `carried:` belongs after a clean restack; and a dead Driver's lease blocked `ship` until someone found the right command. This PR makes the CLI say what the stack owes, print true bases, carry a clean restack, and name the exact command in each lease refusal. It adds no command and no tool.

## Deliverables

- `order merged` in a stack batch prints one line, `restack owed: <crs> stood on <merged>'s branch; ...`, naming who restacks (a `take stack --epoch <n>` or the note `merged: <cr>` to the stack driver).
- `take`, `round` and `handoff` print the base of the CR's place in the stack; the forge's own base follows as `; PR on <ref>` when it differs, or `; PR base ? (not read from <link>: ...)` when the read failed.
- A clean restack carries the long gate and the verdict: the judged commits are compared with the new ones by their own patch, not by the commits the base moved under them.
- Each lease refusal ends with the command to run:

```
<unit> is held: lease <n> live until <hh:mm:ss>; once the host shows its holder ended,
`agents set <unit> - --epoch <n>` ends it; `take <unit> --reclaim ...` only on the user's word
```

## Blast radius

Grade: **2**. Shared CLI code (`stacks.py`, carry check, leases) and two cards change; revert is possible, with the new test files to drop.

## Autonomous decisions

- The carry rule counts the judged own commits as those of `g.base..g.head` that are also in `head_base..g.head`, less the ones whose patch the new base already holds. The intersection is needed because `head_base..g.head` alone counts a CR rewritten under another CR's branch as the CR's own, which broke an existing carry case (CR judged on another CR's branch).
- `check_merged` and `open_ids` moved from `orders_apply.py` to `orders_merged.py` to avoid an import cycle.

## Known gaps

- A not confirmed lease is still ended only by `take ... --reclaim` (the specification's open question).

<details>
<summary>Details</summary>

## Changes

- `commands/orders_merged.py`, `commands/orders_apply.py`: the restack line.
- `commands/facts.py`, `stacks.py`, `stack_apart.py`: the place's base, `start_on` following the order.
- `commands/crs.py`: the carry check.
- `core/leases.py`, `commands/delivery.py`: lease refusal texts.
- `scenario/run_scenario.py`: two checks expect the place's base for a stacked CR.
- `skills/chantier/references/driver-retake.md`, `foreman-stack.md`: card sentences.
- New tests: `test_restack_line.py`, `test_place_base.py`, `test_carry_restack.py`, `test_lease_commands.py`; `test_leases.py` and `test_stack_hold.py` adjusted to the new texts.

## Human decisions

- `order merged` only prints that a restack is owed and who owes it; no new tool rebases or force-pushes for the stack.
- `take` prints the true base, including after a reorder; the forge's own base stays visible beside it.
- A clean restack must carry the gate and verdict: the old `off:` there is a defect of the carry code.
- Lease refusals name the exact command; no new command is added.

## Impacts

CLI output only; no visual change.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates: `just check`, `just eval-dry-run` at `f20227a`; long gate `scenario` passed locally at `91c934f`
- [x] Evidence: none beyond tests
- [x] Review: approved at `91c934f`
- [x] Verified at `91c934f`
- [x] CI green at `91c934f`

## Internal references

CR-477 stack-frictions.

</details>
