## Summary

A release used to cost the user two round trips: one to merge the version PR, then a second "yes" for the tag and the forge release, which started a second Release driver. This change lets the user give the word for those post-merge steps in the same message that offers the version PR to merge, so one Release driver runs every approved step and asks only for the others. It also fixes a bug that made this unsafe: under "auto", the steering session's merge go spent the first approval the user had recorded for a post-merge step.

## Deliverables

The answer of `release go` while the release PR is recorded and not merged (`skills/chantier/scripts/cli/src/chantier/rails_release.py`):

| Grant | Before | After |
| --- | --- | --- |
| none | `merge` | `merge` (unchanged) |
| live ("auto") | `go`, spending the first recorded approval | `go` on the grant's own reason, no approval read or spent |

The cards (shared by both hosts) now say: the ready line for the version PR asks the word for each irreversible post-merge step; each yes is recorded with `order approve` before `order merged`; the Foreman does not start a Driver for an approval on a ready release; the Release driver runs approved steps and holds the rest, a later `wait:` note being stronger than an approval.

## Blast radius

Grade: 2

One CLI branch changes (only when a grant is live and the release PR waits for its merge); the rest is card text and the scripted scenario. Revert restores the previous behaviour.

## Autonomous decisions

- The scenario's scripted Foreman marks an `approve` order on a ready release `done` at once, and skips `wait:` notes when reading why a CR is back, as the cards now say.

## Known gaps

- Both hosts share the cards; the run is unproved on Copilot, and on Claude Code without a grant a refused `gh release create` still ends in `blocked approval: publish: <command>`. A real release proves whether one Driver goes to the end.
- A "wait" written before the merge in the answers file is a card rule with no CLI part; nothing scripts it.

<details>
<summary>Details</summary>

## Changes

- `rails_release.py`, `commands/release.py`: the grant alone answers while `pr` is set; docstrings updated.
- `chief-of-staff.md`, `foreman.md`, `driver.md`: the post-merge word at the ready ask, its recording, the Foreman's `order done`, the Driver's handling of approved and held steps.
- `scenario/run_scenario.py`, `scenario/README.md`: the scripted Foreman follows the cards; the `release` unit and `release_on_stack` check that an approval is not spent by the grant's merge go, is kept across a redo, and reaches the Driver started at the merge.
- `tests/test_rail_refusals.py`: one parametrized test of the answer, with and without a grant.

## Impacts

No visual change. Release hand-offs now carry the user's pre-merge yeses to the Driver started at the merge.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_rail_refusals.py` release-go test, scenario `release` unit
- [x] Local gates at `73f246f`: `just check`, `just test`, `just eval-dry-run`, `just scenario` (local, passes at `73f246f`)
- [x] Evidence: none (no visible change)
- [x] Review: approved at `73f246f`
- [x] Verified at `73f246f`
- [x] CI green at `73f246f`

## Internal references

CR-368 ask-the-release-s-post-merge-word-with-t (batch-27), from the retro of CR-366.

</details>

