## Summary

The planning folder's `.gitignore` listed `work/gates/`, but git anchors a pattern that has a slash in the middle to the `.gitignore`'s own folder. It only matched `<planning folder>/work/gates/`, a folder that never exists, so a raw log kept in a CR's `work/gates/` (for example `out.txt`) was published with the planning surface. The entry is now `**/work/gates/`, which matches at any depth.

## Deliverables

Before and after, for a file `2-backlog/P1/<cr>/work/gates/out.txt`:

| Entry in `IGNORED` | `git check-ignore` |
| --- | --- |
| `work/gates/` | no match |
| `**/work/gates/` | match |

An existing planning folder whose `.gitignore` holds the old line gets `**/work/gates/` appended at the next CLI call that opens the repository for writing; the old line stays, harmlessly. The other slash-bearing entries (`/4-batch/...`, `.long-gate.queue/`, `**/work/scratch/`) were checked and are correct.

## Blast radius

Grade: 1. It only widens an ignore pattern for local logs; a `git revert` restores the previous behaviour. Files already tracked under a `work/gates/` stay tracked.

## Autonomous decisions

None.

## Known gaps

- No cleanup of files already published under a `work/gates/` in a planning surface, and the old `work/gates/` line is not removed from existing `.gitignore` files: both were left out on purpose.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/scripts/cli/src/chantier/core/files.py`: `IGNORED` entry `work/gates/` becomes `**/work/gates/`.
- `scenario/run_scenario.py`: the init check tests the line exactly, and a new check runs `git check-ignore` on a log named `out.txt` under a CR's `work/gates/`.
- `skills/chantier/scripts/cli/tests/test_driver_prompt.py`: the ignore test also asserts the line and the match; one new test covers a `.gitignore` written by an older CLI.

## Impacts

No visual change. Logs under any CR's `work/gates/` are no longer published with the planning surface.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`: `just check`, `just eval-dry-run`
- [ ] Evidence: No visual change
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-360 "the planning folder ignores every CR's work/gates/"; follows CR-328 (PR 287), which fixed `work/scratch/` the same way.

</details>
