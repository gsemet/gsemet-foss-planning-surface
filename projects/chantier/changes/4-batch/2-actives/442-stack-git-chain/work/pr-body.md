## Summary

In a stack or series batch, a branch could be cut from the default branch while its pull request targeted the branch below it. The pull requests looked like a chain on the forge, but the branches were not one, and a restack that wrongly concluded nothing was needed voided several gates and verdicts. `ship` and `stack --out-of-draft` now refuse such a branch, and the stack driver's card checks the chain with `git merge-base` first.

## Deliverables

A branch that does not hold the recorded head of the CR below it is refused, naming both CRs, before any gate is paid:

```text
B: branch not based on A's head 1a2b3c4: rebase onto <A's branch>, push, ship again; nothing recorded
B: A's branch moved since its last ship (1a2b3c4 -> 5d6e7f8): it ships first, then ship again; nothing recorded
B: branch not based on A's head 1a2b3c4: put B, C' PRs back to draft, rebase onto <A's branch>, push, ship, then stack --out-of-draft again; nothing recorded
```

(A, B and C are sample CRs of a stack; the real line from the scenario is quoted once its gate has run.) New read-only git read `is_ancestor` (exit 0, 1, other) is the only ancestry test; the CLI writes no git and has no flag to pass the refusals.

## Blast radius

Grade: 2. `ship` and `stack --out-of-draft` gain a refusal in stack, series and release flows; a revert restores today's behaviour, but existing stacked flows must rebase before shipping.

## Autonomous decisions

- None.

## Known gaps

- Scenario proof not yet run at this head; the real refusal line is added once the long gate has passed.

<details>
<summary>Details</summary>

## Changes

- `core/git.py`: `is_ancestor` three-way read.
- `stacks.py`: `stack_base` takes `landed`; `chain_below` returns the CR below.
- `commands/delivery.py`: chain check in `ship` and `stack --out-of-draft`.
- `driver.md`, `foreman.md`: the stack driver's chain check, bottom-up ships, the refusal sentences for CR, release and stack drivers.
- Tests and the scenario made true to the chain.

## Human decisions

- The check applies to stack and series batches, and to the release CR on the top CR.
- `ship` refuses, naming both CRs; the caller of the refused `ship` rebases its own branch, with no route through another role.
- `stack --out-of-draft` refuses the same broken chain and tells the stack driver to put the pull requests back to draft first.
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
