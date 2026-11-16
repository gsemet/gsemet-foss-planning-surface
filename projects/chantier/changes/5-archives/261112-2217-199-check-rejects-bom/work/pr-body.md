## Summary

A UTF-8 byte-order mark written by an agent on Windows was only caught a round later, at review. `just check` now fails when a tracked file starts with one, and the worker card repeats the rule where the fault happens.

## Deliverables

`just check` (through the structure tests) names every tracked file that starts with the bytes `EF BB BF`, on Linux, macOS and Windows:

```text
files with a UTF-8 byte-order mark (write them as UTF-8 without one): README.md, evals/kit/dry_run.py
```

Choices: every tracked file is read (no exception list, no extension filter), the first three bytes only; untracked and ignored files are not read; UTF-16/UTF-32 marks are out of scope. The cards say "add none, strip none": a file that already has a mark keeps it.

## Blast radius

Grade: 1. A new test and two card sentences; `git revert` restores the previous behaviour.

## Autonomous decisions

- The existing agent-file byte-order-mark check is kept next to the new general test, with its reason (a mark hides the frontmatter from a host), so an agent file with a mark stays red in both.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/scripts/cli/tests/test_structure.py`: one test listing tracked files with `git ls-files -z`, collecting every file whose first three bytes are `EF BB BF`, then asserting the list is empty.
- `skills/chantier/references/worker.md`: one sentence in the Coder section, and one in the Conflict resolver section with a check before `git rebase --continue`.

## Impacts

No visual change. A file a Coder creates is untracked until committed, so the round's fast gate does not see it; the long gate and CI do.

## Test plan

- [x] New or changed tests: `test_no_tracked_file_starts_with_a_utf8_byte_order_mark`; red on a marked file, naming every one (verified at 1a891d4)
- [x] Local gates at 1a891d4: `just check` and `just scenario` pass
- [x] Evidence at 1a891d4: red on two marked tracked files naming both; an agent file with a mark still red; an untracked file with a mark not red
- [x] Review: approved at 1a891d4
- [x] Verified at 1a891d4
- [x] CI green at 1a891d4: check on three systems, eval dry run and scenario
## Internal references

CR-199 check-rejects-bom

</details>
