## Summary

When a Driver hands a CR back ready and the CR reads "PR in draft", the CLI printed `it waits on main` (the forge's base branch) even for a PR that was out of draft and stacked on another CR. Drivers stopped on that line, and one put a correct PR back to draft because of it. The line now states the PR's own draft state as the forge has it, and names the CR (with its PR) it waits on.

## Deliverables

The second line of a "PR in draft" hand-back, before and after:

```text
before: CR-3 PR in draft: it waits on main
after:  CR-3 PR in draft: its PR <link> is out of draft on the forge; it waits on CR-2 (<link>)
```

- Draft state comes from what `ship` last read: `a draft on the forge`, `out of draft on the forge`, or `of unknown draft state (draft not read: ship <cr> <pr>)`.
- The waited-on part uses the same answer as the status label and the STATUS files: `<cr> (<pr>)`, `<cr> (no PR yet)`, `the branch <b> (no CR of this batch)`, or `for its turn out of draft`.
- A prepared release reads `the release PR <pr> is <state>; ...`.
- The Driver card and the glossary say the line asks for no change on the forge.

## Blast radius

Grade: **1**. One printed line and two card paragraphs; a plain `git revert` restores the previous text.

## Autonomous decisions

- `draft_waits()` keeps its string result for the views; a sibling `draft_waited()` returns the CR, so the line and the label cannot disagree.
- The status line in a CR's STATUS.md and the state label are left as they are (the specification asks only for the ready line).

## Known gaps

- The stack scenario unit now runs about 430 s against its 320 s budget on a loaded machine (a warning only); the budget is not raised here.
- The GitLab scenario unit was not run locally.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/scripts/cli/src/chantier/stacks.py`: `draft_waited()`; `draft_waits()` built on it.
- `skills/chantier/scripts/cli/src/chantier/commands/driver.py`: the "PR in draft" line of `_ready_lines()`.
- `skills/chantier/references/driver.md`, `skills/chantier/references/concepts.md`, `scenario/README.md`: the wording.
- `scenario/run_scenario.py`: the existing line checks updated; new checks for the run-1 case (forge base `main`), a waited-on CR with no PR, and an unknown draft state.

## Impacts

No visual change; the printed hand-back line reads differently.

## Test plan

- [x] New or changed tests (they fail on the previous code): scenario checks in `ready_words` and `base_from_pr`
- [x] Local gates at `e856ee7` (carried over a clean rebase to `96ab57c`): `just check` pass; scenario units `stack` 132/132 and `parallel` 185/185 pass
- [x] Evidence: the hand-back lines in the scenario's output at `96ab57c` (no image)
- [x] Review: approved at `e856ee7` (carried from `e856ee7` over a clean rebase to `96ab57c`)
- [x] Verified at `96ab57c`
- [x] CI green at `96ab57c`: `gh pr checks 231`, all five jobs pass

## Internal references

CR-277 stacked-ready-line-names-cr; work files under the CR folder's `work/` (`r1.md`).

</details>
