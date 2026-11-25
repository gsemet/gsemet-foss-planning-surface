## Summary

Three parts, one branch. They give a steering session (the Foreman that runs a batch, or the Chief of Staff in direct mode) and a Driver cheaper, surer ways to know what to do next and to talk to each other:

1. **`status --since` and the watcher's `state:` line.** `chantier status --since <seq>` prints only what changed in the batch's event sequence after `<seq>`, and the steering watcher prints one `state:` line (what is due now) instead of a full status read at each wake.
2. **`chantier next` and the `next:` lines.** `next <cr>` prints the one step a Driver owes now, from the CR's recorded state (step table, the same checks `handback` makes), and the commands a Driver runs print a `next:` line with it.
3. **`chantier msg` and `chantier inbox`.** A Driver sends one line (`note`, `anomaly`, `blocked`) to the batch's steering session as a `msg@1` journal line; the steering session's watcher wakes on `anomaly` and `blocked` and tells a `note` at its next block; `inbox` reads and marks the lines.

## Deliverables

- New commands: `next`, `msg`, `inbox`; new option `status --since <seq>`; new journal type `msg@1`.
- New lines printed by existing commands: the watcher's `state:` line, and a `next:` line after the batch commands a Driver runs.
- `msg` prints `not delivered: no watcher subscribed` and exits non-zero when no watcher is subscribed.
- `AGENTS.md` names the new commands and the one `role:steering` audience value of `msg@1` as a named exception to "the CLI knows no role".

What a Driver now sends and reads (shapes, abridged):

```text
chantier msg steering anomaly "CI red on the PR" --cr CR-12 --lease 2   # appends one msg@1 line
chantier inbox [--read <seq>|all]                                       # the steering session reads and marks them
chantier next CR-12                                                     # next: <the one command owed now>
chantier status --since 41                                              # only the events after seq 41
watcher wake:  state: <what is due now>                                  # one line instead of a status read
```

| At a wake | Before | After |
|---|---|---|
| steering watcher | a full `status` read to learn what is due | one `state:` line, `status --since <seq>` for the delta |
| a Driver's command | its own output only | its output plus a `next:` line |

## Blast radius

**2**: shared CLI code (status, batch commands, the hub's journal schema and watcher lines) changes; every part is additive, and a revert of the branch restores the previous behaviour. The `next:` lines go through wrapper handlers, so a command's own output is unchanged but for the added line.

## Autonomous decisions

- Part 1: the `state:` line is built by `steering_state` in `hub/watch_reads.py`, not a method `Watch._state()` as first planned, because `hub/watch.py` is at its 400-line limit; the behaviour is the specified one.
- Part 2: the `next:` lines are added by wrapper handlers in `commands/next_lines.py`, registered in place of each command's handler, because `driver.py` is at 398 lines; lease events count as quiet in the step walk; `next` accepts `--lease` on a CR with no lease recorded; `restack_line` moved to `status/due.py` so the due list and `order merged` print the same words.
- Part 3: the event's field is `msg_kind` (not `kind`), the refusals carry a `msg: ` prefix, an empty text and a `--cr` that is not `CR-<n>` or `stack` exit 1, a wrong target or kind exits 2 through argparse; `Msg1` lives in a new `hub/schemas_msg.py` (`schemas.py` would pass 400 lines); `inbox` is among the commands that print the batch's epoch hint. The test that no role is named in the journal code now spares the one `role:steering` value.

## Known gaps

- `--since` takes the event sequence only, not the watcher's journal cursor (settled in the grill, to be confirmed by the owner); a cursor form is not built.
- The scenario's new `msg` steps (the SC13 steps of the scenario) read right in review but their timing is proved only by the pipeline's ubuntu `scenario` job; the stack unit's local run took 742 s of its 750 s budget with two units at once (a unit over budget warns only).
- No Windows run of the long gate: this CR is not the top of its stack (CR-514 is; the ubuntu scenario at the head covers it).
- `just test` seconds: 144.6 s on the base (2745 tests) and 130.8 s at the head (2825 tests), each run alone: no measurable increase.

<details><summary>Details</summary>

## Changes

- `status --since` and the `state:` line: `declare/batch_status.py`, `commands/batch_status*.py`, `status/state_line.py`, `status/due.py`, `hub/watch_reads.py`; tests `test_status_since.py`, `test_watch_state_line.py`.
- `next`: `declare/next.py`, `commands/next_advice.py`, `commands/next_lines.py`, `core/driver_steps.py`, `status/advice.py`; test `test_next_advice.py` (its agreement test calls `handback_refusals`).
- `msg` and `inbox`: `declare/msg.py`, `commands/msg.py`, `hub/schemas_msg.py`, `hub/schemas.py`, `hub/schemas.json`, watcher delivery in `hub/watch_lines.py`; test `test_msg_steering.py`.
- `AGENTS.md`, `docs/planning-folder.md`, `scenario/run_scenario.py` and `scenario/README.md`; supporting edits in `cli.py` (registration), `core/batch.py`, `core/records.py`, `hub/journal.py` and `near_misses.py` (the new commands, the batch's event fields, the epoch hint).

## Human decisions

- `status --since` takes the batch's event sequence only, no journal-cursor form.
- `next` follows the defaults chosen in the grill: it prints the one step owed now from the CR's recorded state, and the `next:` lines reuse the same words as the due list.

## Impacts

Developers and Drivers: new commands and lines as above; the steering watcher's output is shorter at a wake. Users: no visual change.

## Test plan

- [ ] New or changed tests (they fail on the previous code): the five test files above
- [ ] Local gates at `5d96982`: `env -u NO_COLOR just check`, `just eval-dry-run`: `just check` passed (2825 passed, 20 skipped), `just eval-dry-run` passed (25 of 25 cases as expected)
- [ ] Evidence: No before/after capture: CLI output only; the tests and the scenario carry it
- [x] Review: approved at `5d96982`: part 1 at e8278a9, part 2 at 7f5f944, part 3 at 5d96982
- [ ] Verified at `5d96982`
- [ ] CI green at `5d96982`

## Internal references

- CR-497 (SC11, SC12, SC13), batch batch-31, after CR-495.

</details>
