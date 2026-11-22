## Summary

In a stack or series batch, a branch could be cut from the default branch while its pull request targeted the branch below it. The pull requests looked like a chain on the forge, but the branches were not one, and a restack that wrongly concluded nothing was needed voided several gates and verdicts. `ship` and `stack --out-of-draft` now refuse such a branch, and the stack driver's card checks the chain with `git merge-base` first.

## Deliverables

A branch that does not hold the recorded head of the CR below it is refused, naming both CRs, before any gate is paid. The line below is real, from the scenario's `ship` of a stacked CR cut from main (run at 311ccf4):

```text
CR-103: branch not based on CR-102's head d8be1c4: rebase onto chantier/batch-01/cr-102-stack-middle, push, ship again; nothing recorded
```

The other two refusals, as the code words them (A, B, C are sample CRs):

```text
B: A's branch moved since its last ship (1a2b3c4 -> 5d6e7f8): it ships first, then ship again; nothing recorded
B: branch not based on A's head 1a2b3c4: put B, C' PRs back to draft, rebase onto <A's branch>, push, ship, then stack --out-of-draft again; nothing recorded
```

What `ship` and `stack --out-of-draft` refuse, before and after:

| Case | Before | After |
| --- | --- | --- |
| B placed on A, B's branch cut from main, PR retargeted to A | accepted | refused: not based on A's head |
| B rebased onto A, A amended and shipped again since | accepted | refused: B must be rebased onto A's new head |
| B based on A's pushed tip, A not shipped again | accepted | refused: A ships first |
| B holds A's recorded head | accepted | accepted |
| `stack --out-of-draft` on a chain that is not one | turned the PRs out of draft | refused, PRs stay draft |
| CR with no CR below, or one below merged or cancelled | accepted | accepted |

New read-only git read `is_ancestor` (exit 0, 1, other) is the only ancestry test; the CLI writes no git and has no flag to pass the refusals.

The `stack --out-of-draft` refusal is proved by a unit test, not a scenario step: the scenario reaches the same chain helpers through `ship`, and a step for the out-of-draft path would cost a second full stack set-up for a refusal that shares the code already exercised.

## Blast radius

Grade: 2. `ship` and `stack --out-of-draft` gain a refusal in stack, series and release flows; a revert restores today's behaviour, but existing stacked flows must rebase before shipping.

## Autonomous decisions

The questions below were answered by the advisor during the specification, not by the user (the user's grill answers are Q1-Q4):

- Q5: the caller of the refused `ship` rebases its own branch; no route through the stack driver or the Foreman.
- Q6: `stack --out-of-draft` refuses the same broken chain.
- Q7: a CR taken onto another's branch and not placed yet is checked when its `start_on` is live.
- Q8: the CR below is read with the journal's seen-merged CRs; a CR seen merged is never the CR below.
- Q9: a second `ship` message when the CR below moved since its last ship.
- Q10: the release CR is checked against the top CR, with the same messages.
- Q11: the stack driver's card runs the `merge-base` check before turning any PR out of draft.
- Q12: a CR whose CR below moved is shipped first by the stack driver only when it has no live Driver, else left to come.

## Known gaps

- None.

<details>
<summary>Details</summary>

## Changes

- `core/git.py`: `is_ancestor` three-way read.
- `stacks.py`: `stack_base` takes `landed`; `chain_below` returns the CR below.
- `commands/delivery.py`: chain check in `ship` and `stack --out-of-draft`.
- `driver.md`, `foreman.md`: the stack driver's chain check, bottom-up ships, the refusal sentences for CR, release and stack drivers.
- Tests, and the scenario's stacked, series and release steps made true to the chain (rebase onto the CR below before `ship`, `base=` on the stacked rounds, one more `ship` after an amend).

## Human decisions

- The check applies to stack and series batches, and to the release CR on the top CR.
- `ship` refuses, naming both CRs; the caller of the refused `ship` rebases its own branch, with no route through another role.
- `stack --out-of-draft` refuses the same broken chain and tells the stack driver to put the pull requests back to draft first (advisor-taken, Q6 and Q11).
- No flag skips either refusal, and the CLI restacks nothing and writes no git.

## Impacts

No visual change. A stacked CR must be rebased onto the CR below before `ship`.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`: pending
- [ ] Evidence: pending
- [ ] Review: pending
- [ ] Verified at `<sha7>`: pending
- [ ] CI green at `<sha7>`: pending

## Internal references

- CR-442 stack-git-chain

</details>
