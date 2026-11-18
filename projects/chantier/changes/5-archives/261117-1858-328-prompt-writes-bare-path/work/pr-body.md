## Summary

A worker started from a prompt whose `writes:` line carried text after a path (a parenthetical copied from `folder:`) could not write to its folder, because the write guard reads such an entry as a different folder name. A Verifier also had no allowed place for throwaway projects and left one outside its folders that it could not delete. The CLI now prints the worker's `writes:` line ready to copy, bare, and a `scratch:` folder inside the CR's `work/` for Verifiers; the cards say how to use them.

## Deliverables

The facts block printed by `take`, `round` and `handoff` gains one copy-ready line and one folder (paths made up):

```text
folder: /plan/changes/101-one (work/, evidence/)
scratch: /plan/changes/101-one/work/scratch
...
worker writes line (copy it unchanged, without the two leading spaces, into each worker's prompt):
  writes: /code/wt/batch-1-CR-101; /plan/changes/101-one
```

- The worker line holds two absolute paths with nothing after them, worktree first.
- `work/scratch/` is ignored by the planning folder's `.gitignore`, so a leftover scratch project is never pushed.
- A scratch project is its own git repository and every chantier call aimed at it names it explicitly, so it never reaches the live planning folder.

## Blast radius

Grade: 1. Printed facts, one ignore entry and card wording; a `git revert` restores the previous behaviour. The guard's code is untouched.

## Autonomous decisions

- The ignore entry is `**/work/scratch/` rather than `work/scratch/`: git anchors a pattern that has a slash in the middle, so the bare form would not match `<CR>/work/scratch/` (checked with `git check-ignore`).

## Known gaps

- The existing `work/gates/` entry has the same anchoring flaw and is left as it is; the scenario asserts its literal text. A separate change can fix both.

<details>
<summary>Details</summary>

## Changes

- `commands/facts.py`: prints the `scratch:` line after `folder:` and the `worker writes line`.
- `core/files.py`: `**/work/scratch/` added to the ignored entries.
- `concepts.md`, `driver.md`, `verifier.md`, `hosts/claude-code.md`: the `writes:` template line is bare, workers copy the printed line, Verifiers use `scratch:` as their own repository and drop the neutral-location option.
- Tests and scenario: checks of the printed lines, the ignore entry and scratch isolation.

## Human decisions

- The printed prompt line for `writes:` is a bare path, and Verifiers get a scratch folder inside the CR's `work/`.
- The planning folder's `.gitignore` ignores that scratch folder.
- The "scratch folder at a neutral location" option is dropped; a Verifier rewrites the user's paths in a capture or does not keep it.
- A path too long for Windows under the scratch folder is a stop the Verifier reports, with no workaround.
- A scratch project is its own git repository, and every chantier call there names it explicitly.
- Only throwaways a Verifier makes itself go in the scratch folder; the project's own tests keep their fixtures and temporary folders.

## Impacts

No visual change.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `carried from 906c73f`: `just check` pass (445 tests); the pipeline's `just scenario (ubuntu-latest)` pass at the head
- [x] Evidence: none (no visual change)
- [x] Review: approved at `carried from 906c73f` (carried from `bbabea5`, clean rebase)
- [x] Verified at `carried from 906c73f`
- [x] CI green at `carried from 906c73f`

## Internal references

CR-328 (prompt writes bare path).

</details>
