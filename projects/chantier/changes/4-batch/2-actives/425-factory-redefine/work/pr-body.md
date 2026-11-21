## Summary

Chantier had a "factory mode" for a batch, a special switch that made a batch pick up work as it was grilled. That framing was wrong: it is not a mode of the batch, it is a choice made while planning. This PR removes the factory mode. When a change request is grilled enough, the user now says where it goes: the next batch (`3-ready`, the default) or, when a batch is open, the running batch (`4-batch/1-pending/`). Placing a CR in `1-pending` is the go, in every mode.

## Deliverables

The destination question and the running-batch mark:

| Step | Before | After |
| --- | --- | --- |
| "Grilled enough?" | specify, back to the backlog, not yet | specify for the next batch (recommended), specify for the running batch, back to the backlog, not yet |
| Each spec-writer start | no destination asked | destination asked when a batch is open; a later run keeps the recorded one |
| Joining the running batch | `triage --ready` in a factory batch | `triage --running-batch` marks the CR; `order add --note <folder>` joins it once its specification is final |
| Opening a batch with no CR | `open --factory`, or a factory batch | an ordinary paused batch that waits for CRs in `1-pending` |
| A batch's last CR | factory batch waits for the next ready CR | the ordinary pause, retro and close offer |

```text
triage <folder> --running-batch   # writes work/running-batch (time, batch id); moves nothing
status                            # running batch: <n> CRs marked, not joined: <folder> (specifying|written), ...
order add --note <folder>         # moves the folder to 4-batch/1-pending/, clears the mark
```

Choices: `open --factory` and `order factory on|off` are removed (refused as usage errors). Old records with `factory: on` still read and behave as an ordinary batch. No factory word remains in `status`, the board state or the web client.

## Blast radius

The change touches the CLI's open, order, triage, status and end-of-batch paths, the cards and the web client's batch views. Old `batch.json` records stay readable. Rolling back is a revert, with follow-ups for the cards.

Grade: 2

## Autonomous decisions

- The mark lives in `lifecycle/running_batch.py`, a lifecycle function the board's lane will call, as the specification asks.

## Known gaps

- The board's backlog lane for the running batch is not part of this PR (a separate change builds on the mark function).
- **UNVERIFIED:** the pipeline's full scenario job and the Windows gate have not run at this head yet.

<details>
<summary>Details</summary>

## Changes

- Cards: `chief-of-staff.md`, `griller.md`, `concepts.md`, `routing.md`, `foreman.md`, `hosts/claude-code.md`, `hosts/copilot.md`: four-option "grilled enough?", destination at every spec-writer start, factory text removed.
- CLI: `triage --running-batch`, `status` lines for marked CRs, `endpause.py` without its factory branch, `open --factory` and `order factory` removed, `commands/factory.py` deleted, `BatchRecord.factory` dropped.
- Web client: `steeringFactoryWord` and the factory i18n keys removed.
- Docs: README section "Running batch or next batch", use-case docs, batch-lifecycle texts and SVG, scenario README.
- Tests and scenario: new running-batch tests, factory tests removed or reworked, the scenario's `running_batch` step replaces `factory_batch`.

## Human decisions

- Factory is not a mode: the user picks the next batch (default) or the running batch at the spec-writer's start.
- Placing a CR in `1-pending` is the go, in every mode.
- A batch's last CR leads to the ordinary pause, retro and close offer.
- The mark is refused for an ungrilled CR; a `3-ready` CR joins with `order add`.

## Impacts

Users see a four-option "grilled enough?" question and no factory wording on the board or in `status`. No visual change otherwise.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `66d9b1c`: `just check` (1489 passed, 20 skipped), `just eval-dry-run` (18 of 18 cases)
- [ ] Evidence: none yet

## Internal references

CR-425 running-batch-or-next-batch-the-factory-mode-removed.

</details>
