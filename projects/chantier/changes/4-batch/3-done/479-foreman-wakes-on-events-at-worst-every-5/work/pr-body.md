## Summary

The Foreman (the session that steers a running batch; the Chief of Staff is the session that talks to the user and relays events) woke on a 30-minute timer and relied on the Chief of Staff to relay each merge and red CI. Cost study of a real batch (UNVERIFIED here: the figure, 41 of 291 Foreman wakes being timer heartbeats, comes from the specification and was not re-measured in this PR): the watcher never woke the Foreman. This change lets the Foreman run its own watcher on its batch's events, and stretches the Claude Code timer to 55 minutes (at worst one wake per 55 minutes, under the 1-hour cache).

## Deliverables

The Foreman's watcher, by what it reads and when it ends:

| | Chief of Staff's watcher | Foreman's watcher (new) |
| --- | --- | --- |
| Who | session holding the seat | session the batch records as its Foreman |
| Reads | all project lines | only its batch's merged, checks-red and wait-cleared lines |
| Starts the server | yes, when it holds the seat | never; with none running it ends with one line |
| Ends | seat moves; 2 h idle with no batch in flight | batch records another Foreman, batch closed, link failure; same 2 h idle end; never on the seat |

- Shipped Claude Code `steering_wake` is `55m` (was `30m`); a configured value still wins and the 60-minute bound is unchanged.
- `watch: not running` line names whose watcher it is; the Chief of Staff's `status` prints `foreman watch: running|not running`.
- The Chief of Staff records and relays a merge or red CI only while the Foreman's watcher does not run.

## Blast radius

Grade: 2. Watcher code and the cards that steer a batch change together; revert restores the 30-minute timer and the Chief of Staff's relay.

## Autonomous decisions

- The Foreman's watcher filters in the watcher (a new `hub/watch_cmd.py` holds the handler), not through a hub audience.
- Test thresholds in `test_start_reading.py` raised for the Foreman's and Chief of Staff's card growth; the 12,544 limit is untouched.

## Known gaps

- **UNVERIFIED:** the 55-minute wake and the Foreman's watcher waking an idle Foreman session on Claude Code are unproved; the cards name the trials for the first batch run on this version.
- The Foreman's watcher link-failure end lines still say "for the Chief of Staff".

<details>
<summary>Details</summary>

## Changes

- `config/chantier.defaults.yml`, `hosts/claude-code.md`, `foreman.md`, docs: 55-minute default.
- `hub/watch.py`, `hub/watch_cmd.py`, `hub/autostart.py`, `hub/watch_lines.py`, `hub/schemas.py`, `hub/lines.py`, `hub/watch_reads.py`, `declare/watch.py`: the Foreman's watcher, its end rules, the `not running` line, message texts "for the steering session".
- Cards (Foreman, Chief of Staff, routing, hosts, session start), docs and AGENTS.md: who records a merge, the watcher rule.
- Tests and scenario step for the Foreman's watcher.

## Human decisions

- Keep the Foreman's timer (30 to 55 minutes on Claude Code) and add a watcher of the Foreman's own, rather than remove the timer.
- In Foreman mode the Foreman records a merge itself after checking it on the forge; the Chief of Staff tells the user and keeps recording whenever the Foreman's watcher does not run.

## Impacts

No visual change. Foreman sessions of a batch wake less on the timer and record merges themselves.

## Test plan

- [x] New or changed tests (`test_watch_foreman.py`, `test_playbook_timing.py`, others)
- [x] Local gates at a92dd75: `just check`, `just eval-dry-run`
- [x] Evidence: scenario step in the long gate, passed locally at a92dd75
- [x] Review: inspector approved round 3 (before the rebase that resolved one conflict; gates and verification re-run at a92dd75)
- [x] Verified at a92dd75
- [x] CI green at a92dd75 (`just check` on three systems, `just eval-dry-run`, `just scenario` on ubuntu)

## Internal references

CR-479 foreman-wake.

</details>
