**Eval run: do not merge.** The maintainer decides what happens to this PR.

## Summary

In direct mode, where the user's own session steers a batch, the "heartbeat N min" that `chantier status` prints showed values that looked wrong: 170 min right after a refresh, 0 min at other times, 439 min after the loop had ended. The CLI printed the true age of the last loop wake each time; what misled was the agent instructions (one rule said to refresh without `--epoch`, another to always carry it), a wake's own line (always 0, hiding the gap since the previous wake) and the lack of any mark for a loop that ended on purpose.

This PR makes the heartbeat mean one thing in both modes: the minutes since the steering session's last `status --refresh --epoch <n>`. A wake's own line shows the gap since the wake before, and a loop that ended is shown as "heartbeat stopped".

## Deliverables

Before and after, one batch at epoch 1 (the new scenario checks assert each line):

| Reading | Before | After |
|---|---|---|
| `status` before any wake | `heartbeat never` | `heartbeat never` |
| first `status --refresh --epoch 1` | `heartbeat 0 min` | `heartbeat 0 min` |
| later wake, previous 45 min ago | `heartbeat 0 min` | `heartbeat 0 min (45 min since the last)` |
| `status --refresh` with no epoch | age unchanged | age unchanged |
| after `status --stop-heartbeat --epoch 1` (or `pause`) | a growing age | `heartbeat stopped` |
| next accepted wake | `heartbeat 0 min` | clears the mark, `heartbeat 0 min (N min since the last)` |

```text
chantier status --stop-heartbeat --epoch <n>   # ends the loop on record; stale epoch: exit 3
```

Choices: the stop is an option of the existing `status` command (no new command); `pause` also records it, since the loop ends right after a pause; `STATUS.json` and the board carry the mark, so a stopped loop is told apart from a silent one.

## Blast radius

Grade: **1**. A new optional `batch.json` field (read with a default, so older batches work) and status wording; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- `pause` also records the stop, because the cards end the loop right after it and the stop would otherwise be forgotten.
- The board shows "heartbeat stopped" too, so it does not show a growing age for a loop that ended on purpose.
- The stop is `status --stop-heartbeat`, which requires `--epoch`.

<details>
<summary>Details</summary>

## Changes

- `commands.py`: `heartbeat_stopped` field; `_refresh` keeps the previous heartbeat and clears the mark on an epoch wake; `status` prints `never`, `N min`, `stopped` and the wake gap; `status --stop-heartbeat --epoch` (lock, stale epoch exit 3, one event); `pause` sets the mark.
- `status.py`, `board.py`: the mark in `STATUS.json` and on the board; `cli.py`: help texts.
- Cards and docs: one `--epoch` rule for a steering session in direct mode, recording the stop where the loop ends (the batch-steering card and both host cards), what the heartbeat measures.
- `scenario/run_scenario.py`: new `direct_batch` checks for each reading above.

## Human decisions

- In direct mode the heartbeat means the minutes since the session's last `status --refresh --epoch`, as in a batch run by a separate steering agent.
- A wake's own line shows the gap since the wake before.
- The refresh before a report carries no epoch; only the loop's wakes move the heartbeat.
- A stopped loop is recorded and shown as "heartbeat stopped".

## Impacts

Users see a true, labelled heartbeat in `status`, `STATUS.json` and the board; no visual change otherwise.

## Test plan

- [x] New or changed tests: `direct_batch` checks for the wake gap and the stop form (they do not pass on the previous code: neither exists there); the no-epoch refresh check is a regression guard
- [x] Local gates at `0314e28`: `just check` and `just scenario` pass
- [x] Evidence at `0314e28`: scenario transcript (578/578 checks) shows each reading above; the real `/loop` behaviour is **UNVERIFIED** (only the CLI form and the card text are shown)
- [x] Review: approved at `0314e28`
- [x] Verified at `0314e28`
- [x] CI green at `0314e28`

## Internal references

CR-187 heartbeat-odd-values; investigation in the CR's `work/01-investigation.md`.

</details>
