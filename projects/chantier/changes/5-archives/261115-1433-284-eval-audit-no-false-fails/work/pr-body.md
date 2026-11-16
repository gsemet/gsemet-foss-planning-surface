## Summary

The eval audit (`evals/kit/audit.py`) ended two real sandbox runs at exit 1 with three FAIL lines that were all false: the agents had done what the cards say and the audit misread it. This change makes the audit read those three behaviours as PASS, keeps it failing on the real breaches those checks exist for, and adds one dry-run case per detector so the misreading cannot come back.

## Deliverables

| Check | Misread before | Read now |
| --- | --- | --- |
| J1 | A retro critic started with `chantier retro-critic for the Chief of Staff, in the project <root>.` had no recognised role | The prompt form `for the Chief of Staff` (with or without `of batch <batch>`) gives the agent its role; it is audited by its own card, not as a worker or a review step |
| J14 | A shell call that claimed the session and read `chantier rules` in one line was dropped by the time filter | The steering session's window starts at the call that made its claim, that call included |
| J26 | `git -C <main checkout>` inside a Python here-doc was read as `git checkout` | A here-doc body is data, unless the here-doc feeds a shell (`bash`, `sh`, `zsh`, `dash`, `ksh`, `pwsh`, `powershell`) |

Three new dry-run cases, each with a planted breach that must still FAIL:

- `audit-cos-prompt`: PASS for the well-formed prompt; FAIL for an unrecognised first line and for a prompt that does not name its card.
- `audit-claim-call`: PASS when `chantier rules` runs in the claim call; FAIL when it only ran before it.
- `audit-heredoc`: PASS for the Python here-doc; FAIL for a plain `git checkout main` and for the same move in a here-doc fed to `bash`.

## Blast radius

Grade: **1**. The change is confined to the eval kit (audit, dry run, README); a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The QA driver's first line is left out of the change; no run has shown it.

## Known gaps

- A here-doc that feeds a shell after the here-doc marker (`cat <<EOF | bash`, `<<EOF sh`) is still read as data, so a git move run that way is missed; a rare form the specification did not name.
- The new cases check J14 only for the claim call; the shared window also reaches the other steering checks, which no case exercises directly.
- The QA driver's first line has the same J1 cause and is not fixed here.

<details>
<summary>Details</summary>

## Changes

- `evals/kit/audit.py`: `PROMPT` accepts `for the Chief of Staff`; such agents are checked against their own card, are not review steps, and are not asked for the rules line; the steering session's window starts at its claim call; J26 reads commands with here-doc bodies and PowerShell here-strings removed, except a here-doc fed to a shell; docstring updated.
- `evals/kit/dry_run.py`: the three cases above, in `CASES` and the module docstring.
- `evals/README.md`: the dry run's row lists the three new planted faults.

## Impacts

No change for users of chantier; the eval kit's audit gives fewer false FAIL lines.

## Test plan

- [x] New or changed tests: three dry-run cases (`audit-claim-call` and `audit-heredoc` fail on the previous audit; `audit-cos-prompt` errors there, as the previous audit has no Chief of Staff form)
- [x] Local gates at `fc55ab0`: `just eval-dry-run` (11 of 11 cases as expected), `just check` (190 passed)
- [x] Evidence: dry-run output at `fc55ab0`, 11 of 11 cases as expected
- [x] Review: approved at `fc55ab0` (carried from `9d4136c`, over a clean rebase)
- [x] Verified at `fc55ab0`
- [x] CI green at `fc55ab0`

## Internal references

- CR-284, specification `03-change-spec.md` in the CR folder.

</details>
