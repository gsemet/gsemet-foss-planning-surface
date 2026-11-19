## Summary

The eval audit (`evals/kit/audit.py`) did not know the QA driver's first line, `chantier qa-driver for <folder> of batch <batch>, in the project <root>.`. A QA driver started with the line its agent file gives would fail check J1 and skip every other check of that agent. This PR teaches the audit that form, audits the QA driver as the Driver it is, and adds a dry-run case that proves it.

## Deliverables

What the audit does with a QA driver, before and after:

| Case | Before | After |
| --- | --- | --- |
| first line `chantier qa-driver for <folder> of batch <batch>, ...` | J1 fails, other checks skipped | J1, J2, J3, J4, C12 and J17 run |
| `chantier coder for <folder> ...` or `chantier qa-driver about ...` | J1 fails | J1 still fails |
| detached `git worktree add` | would fail J3 once recognised | lawful, PASS label "creates no worktree but its detached one of the default branch" |
| branch worktree (`-b <branch>`) | n/a | J3 fails |
| write to `<folder>/04-result.md` | would fail J3 "writes no code itself" | its own file |
| write elsewhere (e.g. `src/...`) | n/a | J3 fails |
| direct-mode batch | listed apart, unaudited | audited as a Driver of the batch |

A new dry-run case, `audit-qa-prompt`, reads the first line from `agents/qa-driver.md` and runs seven variants (`own`, `form`, `role`, `card`, `branch`, `outside`, `direct`).

Evidence at `1b58d39`: `just eval-dry-run` ends `dry run: 18 of 18 cases as expected`, `audit-qa-prompt` ok. With the QA first-line recognition disabled the case fails on J1; with J3's worktree allowance restored to the verifier alone it fails on J3 (0 of 1 each time).

## Blast radius

Grade: 1. The change is confined to the eval kit (audit and its dry run); `git revert` restores the previous behaviour.

## Autonomous decisions

None.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `evals/kit/audit.py`: the QA form gives role `qa-driver` and the folder as written; J3 accepts its detached worktree and its writes inside its QA folder; in direct mode it stays among the audited agents; docstring updated.
- `evals/kit/dry_run.py`: case `audit-qa-prompt` with planted breaches.
- `evals/README.md`: the dry-run row lists the new detector.

## Human decisions

- In direct mode the audit also checks a QA driver the Chief of Staff starts, as a Driver of the batch.

## Impacts

No visual change. Eval audits stop failing a QA driver started with its card's first line.

## Test plan

- [x] New or changed tests (judged at `1b58d39`; with the QA recognition or the J3 relaxation removed, the case fails) (they fail on the previous code): `audit-qa-prompt` in `evals/kit/dry_run.py`
- [x] Local gates at `1b58d39`: `just check` pass (635 tests); `just eval-dry-run` pass (18 of 18 cases as expected)
- [x] Evidence: `just eval-dry-run` output at `1b58d39`, `audit-qa-prompt` and its `direct` variant included
- [x] Review: approved at `1b58d39`
- [x] Verified at `1b58d39`
- [x] CI green at `1b58d39` (5 of 5 jobs)

## Internal references

- CR-373 audit-j1-qa-driver; specification `03-change-spec.md`.

</details>
