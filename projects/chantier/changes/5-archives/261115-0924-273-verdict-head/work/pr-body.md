## Summary

A Verifier could record `VERIFIED` without having written its proof note at the head it judged, and the Driver only found out afterwards. `verdict <cr> VERIFIED` now refuses (exit 2, nothing logged) unless `work/verify.md` in the CR's folder has a `Head:` line naming the full SHA of the head the verdict records, so the Verifier is stopped inside its own run and fixes the note before it replies. `NOT VERIFIED` is never refused. The check reads one file and one git head, so it is the same on both hosts and both forges.

## Deliverables

The refusal, as the Verifier sees it:

| Note state | `verdict <cr> VERIFIED` |
| --- | --- |
| no `work/verify.md` | exit 2, `no such file` |
| no `Head:` line | exit 2, `no Head: line` |
| `Head:` names another or a short SHA | exit 2, `its Head: line names <sha7>` |
| `Head: <full head>` (indented, backticks and trailing text allowed) | accepted |

```text
CR-123: verdict VERIFIED needs <CR folder>/work/verify.md with a line "Head: <full SHA>" for the head abc1234 it records: <reason>
```

Choices: the note lives at `work/verify.md` (the cards now say so); a short SHA does not match; the check is role-free and compares only with the worktree's head.

## Blast radius

Grade: 1. Local to `verdict`'s precondition and the cards that describe it; a `git revert` restores the previous behaviour.

## Autonomous decisions

- The scenario helper `World.verified` writes the note and runs the verdict, and every scenario `verdict ... VERIFIED` goes through it, to keep the calls in one place.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `commands/delivery.py`: `verdict` reads `work/verify.md` through a small helper for `VERIFIED` only.
- `worker.md`, `driver.md`, `concepts.md`: the note's place and the refusal.
- `tests/test_verdict_note.py`: one parametrized test of the cases above.
- `scenario/run_scenario.py`, `scenario/README.md`: the note before each `VERIFIED`, and three checks in `handback_proofs`.
- `evals/kit/dry_run.py`, `evals/SCORECARD.md`: the dry run writes the note; row C6 names the refusal.

## Impacts

No visual change. A Verifier or a Driver that records `VERIFIED` must have the note first.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_verdict_note.py`, parametrized
- [x] Local gates at `6af61f5`: `just check` pass (168 tests); `just scenario` pass
- [x] Evidence: after at `6af61f5`: the three refusals (exit 2, no new event), the accepted `VERIFIED` and `NOT VERIFIED` with no note, run by hand on a scratch batch; before: the previous code accepted all of them
- [x] Review: approved at `6af61f5`
- [x] Verified at `6af61f5`
- [x] CI green at `6af61f5`: `gh pr checks 219`, 5 jobs pass

## Internal references

- CR-273 verdict-head
- Scratch-batch transcript: `work/verifier/evidence/scratch-run.txt` (not uploaded)
</details>

