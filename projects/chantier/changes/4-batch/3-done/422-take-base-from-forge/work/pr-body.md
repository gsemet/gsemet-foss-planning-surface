## Summary

In a stack batch, the CLI took its answers from the recorded order of the CRs, and they were wrong on the forge. `take` told a new CR to start on the branch of a CR whose PR the forge already showed merged (not yet recorded), and a ready CR whose PR was out of draft on the default branch read `PR in draft, waits for <CR>` because CRs before it in the order were still working.

Now the base `take` prints leaves out a CR the forge hub's journal shows merged, and a ready CR that the stack driver has not placed reads its word from its PR's base on the forge, as `ship` last recorded it.

## Deliverables

The CLI makes no new forge read. The base reads the journal the forge hub already writes (`merged@1` lines); the word reads `pr_base` and `pr_draft`, already recorded by `ship`.

| Case | Before | After |
| --- | --- | --- |
| `take` of a CR whose nearest earlier CR has a PR the journal shows merged | base is that CR's branch | base skips it (default branch, or the next CR below with an open PR) and a `base: not <CR>'s branch: ...` line says why |
| Not placed, PR out of draft on the default branch, a CR before it still working | `PR in draft, waits for <CR>` | `ready to merge` |
| Not placed, PR draft on the default branch | `PR in draft, waits for <CR>` | `PR in draft`, waits for its turn out of draft |
| Not placed, PR based on another open CR's branch | by the order | `ready to merge` while that CR is, else `PR in draft` |
| Placed CR, release, no recorded base | chain rule | unchanged |

```python
# hub/journal.py
def seen_merged(entries, d) -> frozenset[str]: ...
# stacks.py: optional last argument, empty set = today's result
def start_base(d, c, repo, landed: frozenset[str] = frozenset()) -> str: ...
```

## Blast radius

The change is limited to the CLI's stack-batch base and ready word; it adds no field, no label form and no forge read. `git revert` restores the previous behaviour.

Grade: 2

## Autonomous decisions

- The words block (`ready_word`, `draft_waited`, `draft_clause`, `draft_waits`, `state_word`, `pr_base_of`) moved from `stacks.py` to a new `stack_words.py`, since `stacks.py` went over the repository's 400-line cap for a module; signatures and texts are unchanged, importers updated.
- The `base:` line also shows in a `take` that records a `start_on` on a lower CR while a nearer CR was seen merged.
- For a CR read by its PR's base on a merged CR's branch, `draft_waited` falls to the chain and never names the merged CR.

## Known gaps

- The word is as fresh as the last `ship`: a PR retargeted on the forge with no `ship` after it reads from the old base until the next `ship`.
- The scenario's stack unit budget (640 s) was exceeded in a local run (1196.8 s, run beside `just check`); the two new cases cost about 90 s alone.

<details>
<summary>Details</summary>

## Changes

- `hub/journal.py`: `seen_merged`.
- `stacks.py`: `landed` set threaded through the start-base functions.
- `stack_words.py`: the ready word and what a draft waits for follow the PR's base for a CR not placed.
- `commands/driver.py`, `commands/facts.py`: `take` reads the journal once; the `base:` line.
- Cards (`concepts.md`, `foreman.md`, `driver.md`), `scenario/` checks 1 to 10 and README, tests in `test_stack_base.py`.

## Impacts

No visual change: no `STATUS.json` field and no label form changes.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test_stack_base.py`, CI green at `d2c4ff1`: pending at `d2c4ff1`
- [x] Local gates: `just check`, `just eval-dry-run`, passed before the first push
- [ ] Evidence: scenario stack unit, checks 1 to 10, `just scenario (ubuntu-latest)` green at `d2c4ff1`: pending at `d2c4ff1`

## Internal references

CR-422 take-base-from-forge.

</details>
