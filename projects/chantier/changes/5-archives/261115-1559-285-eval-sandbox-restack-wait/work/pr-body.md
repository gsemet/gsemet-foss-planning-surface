## Summary

In a stack run on the eval sandbox, each merge at the bottom makes GitHub restack the pull requests above it and rerun their CI. The operator's next `sandbox.py merge <n>` then met a pending check at the new head and was refused at once, so the operator had to run `gh pr checks <n> --watch` and retry. `merge` now waits for the checks at the PR's head, for a bounded time, instead of refusing.

## Deliverables

The merge reads the PR again every 10 s, at most 31 reads (300 s in all). Only unfinished checks wait; every other refusal stays immediate.

| Situation at the PR's head | Before | After |
| --- | --- | --- |
| a check pending (or no check registered yet) and none failed | refused at once | `waiting for the checks of PR #<m> at its head <sha7> (up to 300 s)`, then merges at the first read where all pass |
| still pending after 300 s | refused at once | refused: `... after waiting 300 s: test=pending; nothing merged` (exit 2) |
| a check finished and not green, PR not open, title without the run's prefix | refused at once | unchanged, even when another check is pending |

Each read redoes the whole check from the stack's PRs on, so a stack or head that moved with the restack is followed; the head passed to the merge is the one the last read gave.

## Blast radius

Grade: 1. Evaluation tooling only (the sandbox kit and its dry run); no CLI, card, agent or CI file changes. A plain `git revert` restores the immediate refusal.

## Autonomous decisions

- A rollup with no check at all waits too (the restacked head's CI may not be registered yet), as the specification proposes; a PR with no CI at all is therefore refused only after the bound.
- The bound is 31 reads with 30 sleeps of 10 s, so the 300 s stated is the real wait.

## Known gaps

- What only a real run proves: the shape of GitHub's rollup on a restacked head, and that 300 s covers the sandbox's CI. The next real stack run is the proof; no run was made here.

<details>
<summary>Details</summary>

## Changes

- `evals/kit/sandbox.py`: `merge` loops on `CHECKS_WAIT` / `CHECKS_TRIES`; new `checks_pending` decides which refusal waits (an open, prefixed PR whose checks are unfinished, none failed). `checks_green`, `merge_refusal`, `merge_async`, the exit codes and the command line are unchanged.
- `evals/kit/sandbox_forge.py`: the fake `gh` can stage a head that is pending for its first k reads (`mark_pending_for`), kept in the state file.
- `evals/kit/dry_run.py`: the `merge-refused` case checks the failed and unprefixed PRs are refused at once, the forever-pending one after the wait (constants patched small, in-process), and a pending-then-green one waits then merges.
- `evals/README.md`: "A merge", the kit table row and the `sandbox.py merge` paragraph say it.

## Impacts

No visual change. The operator no longer needs `gh pr checks --watch` before a merge after a restack.

## Test plan

- [x] New or changed tests (they fail on the previous code): the `merge-refused` dry-run case
- [x] Local gates at `430187c`: `just check` (235 tests) and `just eval-dry-run` (16 of 16 cases) pass
- [x] Evidence: no visual evidence (command-line change); the dry run's case output at `430187c`
- [x] Review: approved at `9d04743`; the conflict-resolving rebase approved at `d662a73`, carried over a later clean rebase to `430187c`
- [x] Verified at `430187c`
- [x] CI green at `430187c`: `just check` on three systems, `just eval-dry-run` and `just scenario` pass

## Internal references

- CR-285 restack-wait
- Evidence behind it: the real-foreman run of 2026-11-15, audit item 4

</details>
