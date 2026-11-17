## Summary

Two chantier sessions on one machine, over the same planning surface, could start a second web board, reuse a stale board of another version in silence, and commit each other's files. This PR makes the board one per surface, tells a session which other batches run on the surface, and tells every session to stage only its own project's folder.

## Deliverables

One board per surface, and the record that makes it possible (a small `running` object next to the key in `chantier/board.json` in the git folder):

```json
{ "key": "...", "created": "...",
  "running": { "pid": 1234, "host": "127.0.0.1", "port": 53211,
               "version": "0.11.0", "served": "<surface>", "started": "<UTC>" } }
```

| A new `board` finds | It does |
| --- | --- |
| a live record, same version, answers | registers its seat, prints `board already running at <link>`, exit 0 (whatever its own `--port`) |
| a live record, another version | starts nothing, signals nothing, exit 4, with the version, the PID and the platform's stop command |
| a live record, silent | the same, with the "does not answer" line |
| a dead record | ignores it, starts, writes a fresh record |
| no record (older board) | probes the configured address; an older board answering gets the "another version" line, PID from `/api/board`, else a process lookup, else `PID unknown` |

Other batches on the surface, one informational line in `preflight` (P14) and `status`:

```text
other batches on this surface: studio batch-05 running, steering Foreman, 3 Drivers; other batch-02 paused, steering direct (the Chief of Staff), 0 Drivers
```

It is read from the other projects' `batch.json`, read-only; no cap, nothing written, no message between sessions. The cards (Chief of Staff, Griller, concepts, session start) now say: stage only this project's folder (`git add -- projects/<name>/...`), then `git pull --rebase --autostash` and `git push`; the plan shows the other batches' Drivers so the user picks slots knowing the load.

## Blast radius

The board's start decision changes for every user of the board; the rest is a new read-only line and card text. A `git revert` restores the previous behaviour; a leftover `running` record is ignored by an older chantier.

Grade: 2

## Autonomous decisions

- The new tests live in `tests/test_board_running.py` and `tests/test_surface_batches.py` instead of `test_board.py`, which would pass 400 lines.
- In the scenario's `remote_board` unit, the "port held by another program" check moved to just before the last step: a live board's record now wins over a configured port, so that check needs no live board.

## Known gaps

- When `--clock` pins a past instant, the recorded `started` is that instant and the liveness check may judge a live board dead; that case is not handled.
- The "another version" refusal was exercised by the unit test only, not on a real board of two versions.
- The Windows local `just scenario` at `0feef12` is not run yet (the user's step before merge); Linux is covered by the `just scenario (ubuntu-latest)` job and all three platforms by the `just check` jobs.

<details>
<summary>Details</summary>

## Changes

- `board/running.py` (new): write, read, remove of the `running` record, liveness check, the stop command's text.
- `board/command.py`: the start decision above; the record is written after the bind and removed on the way out when it names this PID. `board/key.py`: `--new-key` keeps `running`. `board/routes.py`: `/api/board` tells its `pid`.
- `core/surface_batches.py` (new), `commands/preflight.py` (P14), `commands/batch_status.py` (the `status` line).
- Cards and docs: `chief-of-staff.md`, `griller.md`, `concepts.md`, `session-start.md`, `docs/web-board.md`, `docs/planning-modes.md`, `scenario/README.md`, and the board line of `AGENTS.md`.

## Human decisions

- One board per surface, whatever the port; the rule holds in-project too.
- A board of another version or a silent one is reported (version, PID, how to stop it); nothing is started, nothing killed: the user decides.
- No machine-wide cap on Drivers: a session sees the other batches and chooses.
- `board.json` keeps the running board's PID, address and version beside its key.

## Impacts

No visual change. A second `board` now reuses the running one; a stale one is named instead of served in silence.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_board_running.py`, `test_surface_batches.py`
- [x] Local gates at `0feef12`: `just check` (443 tests) (restacked; conflict resolved, inspector approved at `0feef12`); `just scenario` locally on Windows at this head: not yet run (Known gaps)
- [x] Evidence: no visual change
- [x] Review: approved at `0feef12` (restacked; conflict resolved, inspector approved at `0feef12`)
- [x] Verified at `0feef12` (restacked; conflict resolved, inspector approved at `0feef12`)
- [x] CI green at `0feef12`: all five jobs pass (restacked; conflict resolved, inspector approved at `0feef12`)

## Internal references

CR-323 two-sessions-one-machine. Work files: `work/coder/r1.md`.

</details>
