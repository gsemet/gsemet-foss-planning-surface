## Summary

A change request taken on top of a ready stack could already have a draft PR on its place before the stack driver (the chantier role that stacks the PRs) had placed it. `forge-stack show` then read that PR as a missing row (`check 2: missing #<n>`), so the ask to merge the ready part of the stack waited until the record was reordered by hand. A working CR that the stack driver has not named in `stack <cr>…` yet is now kept out of the stack as it stands and listed under `to come:`, so it no longer blocks the ask. The start base of a newly taken CR is unchanged.

## Deliverables

The new predicate and where it is used:

```python
def to_come(d, c, repo) -> bool:
    # not in the stack as it stands: no PR, a PR off its place,
    # or a working CR the stack driver has not placed yet
    return (not c.pr or off_place(d, c, repo) is not None
            or (c.status == "working" and not c.stacked))
```

| CR state | Before | After |
| --- | --- | --- |
| working, draft PR on its place, not placed | a row; check 2 reports it missing | under `to come:` |
| working, placed by the stack driver | a row | a row |
| ready, PR on its place | a row | a row |

`create` and `rebuild` (GitHub and GitLab) share the plan, so they do not retarget or stack such a PR. When the first CR of the chain is in this state, the refusal now reads `no PR placed at the bottom of the stack: <cr> is working and the stack driver has not placed its PR <link> yet`.

## Blast radius

Grade: 1. Local to the stack plan of `forge-stack` and to three card sentences; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The new refusal in the bottom-of-stack check was added as the specification describes; no scenario check covers that text (the unit test and the scenario check cover the `to come:` listing).

## Known gaps

- The new bottom-of-stack refusal text has no scenario check of its own.

<details>
<summary>Details</summary>

## Changes

- `stacks.py`: new `to_come` predicate.
- `commands/forge_stack.py`: the plan stops at the first CR `to_come` returns true for; the bottom-of-stack refusal names a working, unplaced CR correctly.
- Cards: `concepts.md` ("Stack as it stands", "To come"), `foreman.md` (the partial ask's `to come:` gloss), `driver.md` (the five checks).
- Tests: one parametrized `to_come` test in `test_stack_due.py` (five cases); one GitHub `forge-stack` scenario check; the scenario README paragraph.

## Human decisions

- A CR's start base stays the nearest earlier CR of the batch that already has a PR; only the stack's ask changes.

## Impacts

No visual change. Operators see a working, unplaced CR under `to come:` instead of a failing check 2.

## Test plan

- [x] New or changed tests (they fail on the previous code): `to_come` cases in `test_stack_due.py`; the scenario check
- [x] Local gates: carried from `ea0ecda` (`just check` pass (570 tests), `just eval-dry-run` pass (17 of 17)); at `a99c1b5`, after the restack onto CR-346: `just scenario --unit stack --forge github` pass (177 of 177), `tests/test_stack_due.py` pass (18)
- [ ] Evidence: none beyond tests and scenario
- [x] Review: approved at `a99c1b5` (restack onto CR-346: the same patch, context and offsets only)
- [x] Verified at `a99c1b5`
- [x] CI green at `a99c1b5`

## Internal references

- CR-347 stack-top-cr-out-of-ask (batch-24)

</details>
