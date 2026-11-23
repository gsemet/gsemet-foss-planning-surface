## Summary

The pull requests chantier delivers should never hold a merge commit. In a downstream project, merge commits of the base landed twice in PR branches, each costing a rebase round. This change makes the agents that move a CR's branch (the CR driver, the Release driver, the stack driver and the Conflict resolver) update it by rebase only, and makes `ship` refuse a branch that holds a merge commit.

## Deliverables

`ship` now checks the CR's own commits before it reads the forge or records anything:

| Branch state | `ship` before | `ship` now |
| --- | --- | --- |
| Linear above its base | records the PR | records the PR |
| Holds a merge commit above its base | records the PR | exit 2, records nothing, says to rebase |
| Base cannot be read by git | records the PR | exit 2, records nothing, says to fetch and ship again |

```text
CR-12: abc1234 holds a merge commit (def5678) above origin/main: chantier's PRs hold none;
rebase onto main (git -C <worktree> rebase <base>), push with --force-with-lease, and ship again
```

Choices: the range starts at the base the head sits on (in a stack, the CR below), so a merge commit in a lower CR is that CR's refusal; no flag and no `chantier.yaml` key skips the check; the forge's rebase action is allowed but marked unproved, with a trial named.

## Blast radius

Grade: **2**. `ship` can now refuse branches that used to be recorded, and the cards change how Drivers update branches. Revert restores the previous behaviour.

## Autonomous decisions

- The check lives in a new module, `commands/merge_check.py`, because `delivery.py` and `ship` would pass their size limits.
- The note on the forge's rebase action sits in the carries-and-conflicts section of the Driver card, because the Driver's startup readings had no room for it.

## Known gaps

- The forge's rebase action is unproved; the card names the trial and this change does not run it.
- Only `ship` checks; `gate`, `handback`, `stack --out-of-draft` and `forge-stack` keep their behaviour.

<details>
<summary>Details</summary>

## Changes

- `ship` runs `git rev-list --merges <base>..<head>` (base found as the carry finds it, else the default branch on the remote), with git failures read as an unreadable base.
- Rule 8 of the concepts card, the Driver card (rebase and push, carries and conflicts, re-takes of a folded CR, the stack driver) and the Conflict resolver card say: rebase only, never merge the base in, never the forge's "Update branch" button, never `--rebase-merges`.
- The four agent descriptions, on both hosts, name the rule.
- A parametrized unit test, a scenario check and the scenario README line.

## Impacts

No visual change. A Driver whose branch holds a merge commit rebases it and pushes with `--force-with-lease` before `ship` records it.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`: `just check`, `just eval-dry-run`
- [ ] Evidence: none beyond the tests
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-465 rebase-only.

</details>
