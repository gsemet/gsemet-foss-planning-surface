## Summary

When a GitHub native stack is merged in one go, every PR of the stack lands on the default branch, but GitHub reports each PR above the bottom one as merged into the branch below it. The forge hub and the board's PRs page then wrote a `merged` journal line with no `landed_with`, and `status` and the watcher told the user "not landed" until the branch below landed, so the stack's merges were left unrecorded. A PR merged into a branch below it whose merge commit is on the default branch is now told as the bottom one is: landed with the bottom CR, `order merged <cr>`.

## Deliverables

The forge read now carries one more fact per merged PR, and the judgment uses it as a second way to land:

| | Before | After |
| --- | --- | --- |
| Forge read | `head` only | plus `merged_on_default` (the PR's `mergeCommit.oid` is in the default branch's last 100 commits, `DEFAULT_HISTORY`) |
| `prs.landed_with` | base merged at the same time or later | same, or `merged_on_default` True and the chain of merged bases reaches a CR merged into a non-CR branch |
| Native stack merged bottom-up | `merged` line, no `landed_with` | `landed with <bottom>`, `for the Chief of Staff: order merged <cr>` |

```python
# prs.py
def landed_with(row, by_cr):  # two ways: base merged at or after, or own merge on the default branch
```

## Blast radius

Grade: **1**. The read stays one GraphQL call per batch; a merge older than the 100-commit window is told "not landed" as before. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The "merged on default" row `False` base-earlier case is not added to the `LANDING` table: `test_board_prs.py` is at the size-test limit, and the existing "base merged before it" row covers the absent case.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `board/forge_read.py`: `mergeCommit { oid }` in `GITHUB_FIELDS`, the `dh:` history alias with `DEFAULT_HISTORY = 100`, `merged_on_default` in `github_state` (None on GitLab).
- `board/prs.py`: `row_of` copies it; `landed_with` gains the second way.
- `hub/journal.py`: docstring only.
- `skills/chantier/references/chief-of-staff.md`: the `landed with` paragraph names the second way.
- Tests in `test_board_prs.py`, `test_forge_hub.py`, `test_board_forge_read.py`.

## Impacts

No visual change. The hub, `status` and the watcher tell a natively stacked merge landed.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`:
- [ ] Evidence: none beyond the tests
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-389 "Change Specification: a native forge stack's merges are told landed" (batch-29)

</details>
