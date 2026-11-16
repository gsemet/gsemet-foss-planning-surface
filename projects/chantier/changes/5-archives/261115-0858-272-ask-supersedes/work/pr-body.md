## Summary

When the Foreman asked the Chief of Staff to relay "this change is ready to merge" for a change request and then asked again after a restack, both asks stayed unread and the Chief of Staff could relay the stale one. A new readiness ask now marks the earlier unread readiness ask of the same change request (or of the stack) as read, so only the latest is relayed.

## Deliverables

The rule, as the CLI applies it when `chantier asks "<text>"` records an ask:

| New ask (first word) | Key | Marks read (unread, same family, same key) |
| --- | --- | --- |
| `ready-to-merge`, `pr-in-draft`, `ready-locally` | the change request named by the second word, if it is in the batch | earlier asks of those three words for that change request |
| `stack-ready-to-merge` | the batch | earlier `stack-ready-to-merge` asks |
| anything else (`question`, `blocked`, ...) | none | nothing; and such asks are never superseded |

```text
[foreman→chief-of-staff] ask A-22: ready-to-merge CR-1 ...
A-21 superseded by A-22 (marked read)
```

The first line is unchanged; the second is for the Foreman and is not sent. The event log records `asks-read` with `superseded_by`, and the `ask` event now carries its change request.

## Blast radius

Grade: 1. Local to ask recording; a `git revert` restores the previous behaviour.

## Autonomous decisions

- The match is on the first word exactly (no case folding, no icon stripping), as asks start with that word today.

## Known gaps

- The optional replay of the rule against a real batch's recorded asks was not run; the scenario checks cover the rule instead.

<details>
<summary>Details</summary>

## Changes

- `rails_release.py`: `readiness_key` helper; `record_ask` supersedes and logs.
- `commands/batch_status.py`, `declare/batch_status.py`: the second printed line and the help clause.
- `references/foreman.md`: one sentence on the `asks` bullet.
- `scenario/run_scenario.py`: checks for the supersession cases; `tests/test_ask_readiness.py`: parametrized helper test.

## Human decisions

- The two families (per-change-request and stack) never supersede each other.
- A stack readiness ask is keyed on the batch.
- `question` and `blocked` asks are never superseded.

## Impacts

No visual change; fewer unread asks in `status` and the board.

## Test plan

- [x] New or changed tests: a parametrized helper test and scenario checks for the supersession cases
- [x] Local gates at `43e3719`: `just check` pass, `just scenario` pass
- [x] Evidence: the cases were run by hand in a scratch batch at `43e3719`; no visual change
- [x] Review: approved at `43e3719` (reviewed at the base `afd42be` with the round's changes uncommitted, committed as `43e3719`)
- [x] Verified at `43e3719`
- [x] CI green at `43e3719`: check on three systems, eval-dry-run and scenario all pass

## Internal references

CR-272 ask-supersedes.

</details>
