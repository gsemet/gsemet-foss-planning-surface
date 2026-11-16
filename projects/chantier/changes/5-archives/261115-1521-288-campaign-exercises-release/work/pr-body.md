## Summary

A release used to claim changes that no eval run had brought to the test (four of the current release's: the merge that stops a running long gate, a pipeline job as the long gate, the early conflict check, and the refusal of a verify note that does not name the head). Nothing said so. Now every release comes with a claims file that says, per change, whether an eval run exercised it, and the release notes list what no run exercised.

## Deliverables

The new flow, per release:

| Step | Where | What |
| --- | --- | --- |
| Before the campaigns | `evals/results/claims-vX.Y.Z.md` | one row per `feat:`/`fix:` commit since the previous tag, with its scorecard rail and the campaigns where that rail can come up; the campaigns are launched in the modes that cover them |
| After the campaigns | same file | `Result` filled: `exercised`, `scenario only` or `not exercised`, with the evidence |
| Release notes | `🛠 For contributors` | a bullet `**Not exercised by an eval.**` listing every claim not `exercised` |
| `just check` | `scripts/release_notes.py --check` | from 0.9.1, refuses notes without that bullet |

Three new scorecard rails (all `by hand`): C21 (merge while the CR's long gate runs), J27 (a pipeline job as the long gate), J28 (the Foreman's `git merge-tree` check in a parallel batch). C6 gains a sentence on when its refusal path is seen.

## Blast radius

Grade: 1. Docs, a scorecard table and one check in the release-notes script that only applies from version 0.9.1; `git revert` restores the previous state.

## Autonomous decisions

- The CR numbers were dropped from the `from` cells of the new scorecard rows; the scorecard names code and cards, not changes.
- J28 does not list `real-direct`: the Chief of Staff's card carries no `git merge-tree` check.

## Known gaps

- J27 and C21 cannot come up in a sandbox run as it is (its rule names a local long gate; no merge is recorded while a long gate runs): they will appear in the release notes as not exercised until a later change gives the campaigns a way.

<details>
<summary>Details</summary>

## Changes

- `evals/SCORECARD.md`: rows C21, J27, J28; one sentence on C6.
- `evals/README.md`: new section "Before a release: the claims", a "Claims" section in the report, and the campaign paragraph names the claims file's modes.
- `docs/release-process.md`: the notes' sources gain the claims file; the `Not exercised by an eval.` bullet and its "None" form.
- `scripts/release_notes.py`: `FIRST_CLAIMS_VERSION = (0, 9, 1)`; `validate_notes` refuses, from that version, notes with no such bullet inside the contributors block.
- `CONTRIBUTING.md`: the pre-release campaigns are launched in the modes the claims file names.

## Impacts

No visual change. Release authors write a claims file and one more bullet in the notes; 0.9.0's notes are unchanged and still pass.

## Test plan

- [x] New or changed tests: none; the check is exercised on the function directly
- [x] Local gates at `64acc00`: `just check` (pass, 190 tests; release notes ok on 0.9.0)
- [x] Evidence: the function run with versions 0.10.0 and 0.9.0 on three texts, at `64acc00`: validate_notes refuses 0.10.0 notes without the bullet, accepts them with the claims bullet and with the "None" form, accepts 0.9.0 without it
- [x] Review: approved at `64acc00`
- [x] Verified at `64acc00`
- [x] CI green at `64acc00`: gh pr checks 235, all five jobs pass

## Internal references

CR-288 eval-campaign-exercises-release.

</details>
