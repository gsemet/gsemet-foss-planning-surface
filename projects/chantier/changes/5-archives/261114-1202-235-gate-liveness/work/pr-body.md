## Summary

A merged change request could leave its long-gate suite running, and the lock then made the next gate wait up to an hour (a recorded pid can also name an unrelated process after Windows reuses it). The activity line also showed nothing for a gate that was queued, not running, so a healthy Driver looked lost. This PR makes the gate lock and the activity line report what is true.

## Deliverables

- `order merged <cr>` stops that CR's long gate when the lock names it, the way `gate <cr> --stop` does (recorded `stopped`, no pass, no failure), and prints `stopped the long gate of <cr> (pg<m>)`.
- A pid recorded in the lock or in a queue ticket counts as alive only while the process with that pid was created no later than the file's last write (plus one second).
- `activity` shows `gate running` only for a live holder, and `gate queued behind <cr>` (or `gate queued`) for a CR with a live ticket.

```text
procs.alive_since(pid, recorded, unreadable) -> bool     # psutil create_time vs recorded time
gate_lock.parse_holder / holder_alive / read_ticket      # one reading of the lock and tickets
gate_run.stop_gate(repo, holder, batch, fallback_head)   # shared by `gate --stop` and `order merged`
activity.activity(...)                                   # moved out of batch_status.py
```

## Blast radius

Grade: **2**. The gate lock, `cancel`, `gate --stop` and `order merged` share the new identity check; a revert restores the previous behaviour.

## Autonomous decisions

- The stop of `order merged` runs after its refusals and before the folder moves, so the gate log is not held open during the move on Windows.
- The lock and ticket text readers were merged into one parser, and the run-file helpers and the activity line moved to new modules, to keep files under 400 lines.
- An unreadable creation time counts as alive for waiting and is never stopped.

## Known gaps

- No scenario step checks that order merged stops nothing when the lock names another CR; this case is proven by reading the code only.

<details>
<summary>Details</summary>

## Changes

- `procs.py`: `alive_since`.
- `commands/gate_lock.py`: shared lock and ticket reading, identity check in the queue and the wait, read-only `gate_state`.
- `commands/gate_run.py` (new): run-file helpers and the shared stop; `gate.py`, `orders_apply.py` (`_merged`) and `release.py` (`cancel`) use it.
- `commands/activity.py` (new): the activity line; `status --refresh` help updated.
- `skills/chantier/references/foreman.md`: the activity list and the lost-Driver rule name `gate queued`.
- `scenario/run_scenario.py`: steps for the merge stop, a reused pid (lock and ticket) and the activity lines.

## Impacts

Command output only: one more line after `order merged`, and the new activity line. No visual change.

## Test plan

- [ ] New or changed tests: scenario steps in the sections `stop_own_gate`, `rails`, `driver_liveness`
- [x] Local gates at the pre-restack head: `just check` and `just scenario` (both forges) pass; `mypy --strict` for linux, darwin and win32: no issues
- [x] Evidence: after at the pre-restack head (a repro of the identity rule and the activity lines, plus the scenario transcripts of both forges)
- [x] Review: approved at the pre-restack head (reviewed at the pre-restack head plus the uncommitted change, committed as the pre-restack head)
- [ ] Verified at `6641ff1` (restack onto main; pending)
- [ ] CI green at `6641ff1` (restack onto main; pending)

## Internal references

CR-235 gate-liveness. Work files under the CR's `work/`.

</details>



