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

- [ ] New or changed tests (they fail on the previous code): `audit-qa-prompt` in `evals/kit/dry_run.py`
- [ ] Local gates at `<sha7>`: <!-- filled at the pushed head -->
- [ ] Evidence: `just eval-dry-run` output at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-373 audit-j1-qa-driver; specification `03-change-spec.md`.

</details>
