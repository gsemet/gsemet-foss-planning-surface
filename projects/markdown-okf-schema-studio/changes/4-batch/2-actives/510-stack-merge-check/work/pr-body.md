## Summary

New CI runs fail on a pull request above the bottom of a GitHub native stack: the checked-out test merge (`refs/pull/<n>/merge`) is then a chain of merges, one per pull request below plus its own, and the merge-commit check peeled only the last one. The check now peels the whole chain, so such a pull request passes `static`, `static-windows` and the required `checks`, while every merge commit that a branch of the stack really carries still fails it.

## Deliverables

The check walks down the first parents from the checked-out commit and ignores the chain only when it has the shape the forge builds:

```mermaid
flowchart TD
    A["HEAD"] --> B{"two parents, and the second one<br/>nested in the one above?"}
    B -- no --> F["check base..HEAD:<br/>every merge reported"]
    B -- yes --> C{"first parent an ancestor<br/>of the base?"}
    C -- "no: step to the first parent" --> B
    C -- yes --> D{"one merge, or every subject<br/>'Merge sha into sha'?"}
    D -- yes --> E["check base..HEAD^2:<br/>the branches' own commits"]
    D -- no --> F
```

| Checked-out commit | Before | After |
| --- | --- | --- |
| Single forge test merge (GitHub, GitLab merged results) | passes | passes (no subject required) |
| Chain of test merges over nested branches | fails, lists the chain | passes |
| Same chain, one branch of the stack carries a merge | fails, lists the chain and that merge | fails, lists that merge only |
| Chain over unrelated branches, not rooted on the base, or with another subject | fails | fails |

## Changes

- `scripts/check-no-merge-commits.sh`: the single-merge peel becomes a walk over two-parent merges down the first parents. The chain is ignored only when it reaches a first parent that is an ancestor of the base, each lower second parent is an ancestor of the one above, and, for two merges or more, each subject is the forge's `Merge <40-character sha> into <40-character sha>`. Git and bash only, no network.
- `test/build/test_no_merge_commits.py`: seven cases on a three-branch stack built in a throwaway clone, in both directions.
- `.agents/guidelines/pull-request.guidelines.md` ("Updating a branch"): says what the check ignores and what it still reports.

## Impacts

No visual change: a CI build script, its tests and one guideline sentence. A contributor with a stacked pull request no longer gets a red `static` job from the forge's own test merges.

## Blast radius

- **1**: local and isolated; a plain `git revert` restores the previous behaviour.
- **2**: several features or shared code; revert is possible but needs checks or follow-ups.
- **3**: wide impact (data, formats, CI, release, public API); rollback is complex or partial.

Grade: 2. The check is part of the required CI of every pull request; a defect would either block pull requests or let a merge commit through. A plain revert restores the previous check, and with it the red runs on stacked pull requests.

## Autonomous decisions

None.

## Known gaps

- Git alone cannot tell a forge chain from a branch whose own history is a first-parent chain of two or more two-parent merges rooted on the base, with nested second parents and every subject written as `Merge <sha> into <sha>`: checked out at its tip, such a branch passes. A single merge at the tip keeps the same gap as before (no subject required). Merges carried inside the second parents are all still reported.
- The subject is checked for its form only, not that its two identifiers equal the merge's parents.
- A merge of three or more parents at the checked-out commit is no longer ignored (the forge's test merge has two).
- **UNVERIFIED:** the check passing on a real chain in CI, on this pull request above the bottom of its stack. The tests build the chain locally; the live run is still to come.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test/build/test_no_merge_commits.py`, 19 passed; on the previous script 4 of the new cases fail
- [x] Requirements: no behaviour change of the extension (build tooling, no requirement covers it)
- [x] Changelog: no user-facing change (a `ci` change adds no line)
- [ ] Local gates: `just ci-static`, `just preflight`
- [ ] Review
- [ ] CI green

## Internal references

- CR-510 stack-merge-check.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
