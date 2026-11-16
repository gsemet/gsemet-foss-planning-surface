## Summary

An agent driving a change had a long gate (the project's slow full test run) going when its branch had to be rebased. That run could no longer count, but the agent had no way to stop it. It ran `chantier cancel`, which stopped the gate and also cancelled the whole change request, moving it to the trash with all its work.

This PR gives such an agent a named way to stop only its own running long gate, `gate <cr> --stop`, and makes the CLI refuse `cancel` unless the steering session (the agent that coordinates the batch) passes `--epoch`.

## Deliverables

- `gate <cr> --stop` stops the CR's running suite and frees the gate lock. The run is recorded as `stopped`: not a pass, not a failure, so not a round. The stopped `gate` command prints `STOPPED <command> at <sha7>: no pass` and exits 4. A stopped run also voids an earlier pass at the same head.
- Exit codes: 0 when it stopped the gate (or when none was running, saying so), 2 when the lock names another CR (that gate keeps running), 1 when given a command.
- `cancel <cr>` without `--epoch` exits 2 and points to `gate <cr> --stop`.

```
gate <cr> --stop
  lock names <cr>   -> marker .long-gate.stop, stop the suite group, record "stopped", exit 0
  lock names other  -> nothing stopped, exit 2
  no gate running   -> "nothing to stop", exit 0
```

The agent guidance says when to stop (the head is about to move, or the steering session says stop; never because a gate is slow) and that `cancel` is never the working agent's command.

| Run | Record | Output |
|---|---|---|
| gate stopped | one `gate` event `stopped` at the start head; log ends `result: stopped ...: no pass` | `STOPPED ...`, exit 4 |
| earlier pass at that head | voided | the head must be proved again |

## Blast radius

Grade: 1. It adds a flag to `gate` and a refusal to `cancel`; `cancel` with `--epoch` is unchanged. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The stop travels to the running gate through a separate marker file (`.long-gate.stop`, ignored by git) that the gate never rewrites, because a first design with a flag in the run file lost a stop to a write race and could record a killed command as a failure.
- The gate also checks the marker right after starting each command and between commands, so a stop landing at any moment is recorded `stopped`.

<details>
<summary>Details</summary>

## Changes

- `commands.py`: `_gate_stop`, the stop marker and the run file (atomic writes), the `STOPPED` outcome in `gate()`, the epoch requirement in `cancel()`.
- `cli.py`: `gate --stop`, command optional at the parser.
- `state.py`: the two new local files are ignored.
- The agent guidance cards (`driver.md`, `concepts.md`): the stop, when to use it, and the `cancel` rule. `CONTRIBUTING.md`, `scenario/README.md`, `evals/SCORECARD.md`: one line each.
- `scenario/run_scenario.py`: a new step covering the stop, the record, the freed lock, a voided pass, a stop with no gate, another CR's gate, usage errors and the refused bare `cancel`.

## Human decisions

- The stop is a way of `gate`, not a new command, and acts only on the gate the lock names for the CR given; another CR's gate is refused, and with none running it says so without error.
- A stopped run is recorded apart from a failure, leaves the CR untouched and voids an earlier pass at the same head.
- It is used only when the run can no longer count (the head is about to move) or on the steering session's stop, never because a gate is slow.
- `cancel` is refused without `--epoch` rather than by role, since the CLI knows no role; other commands' missing epoch is left to its own change.

## Impacts

No visual change. Agents use `gate <cr> --stop`; a script calling `cancel` without `--epoch` now fails.

## Test plan

- [x] New or changed tests (they fail on the previous code): scenario step "stop own gate"
- [x] Local gates at `24d6c45`: `just check` (49 passed), `just scenario` carried from `cdd65a5`: patch unchanged; the long gate runs once at the top of the stack, PR 152 (595/595 on GitHub and GitLab at `cdd65a5`)
- [x] Evidence: the scenario step at `24d6c45`
- [x] Review: approved at `cdd65a5` (code judged at round 2, two small follow-ups applied after; carried to `24d6c45`: patch unchanged by the restack)
- [x] Verified at `24d6c45`
- [x] CI green at `24d6c45`

## Internal references

CR-198 stop-own-gate (batch-15).

</details>
