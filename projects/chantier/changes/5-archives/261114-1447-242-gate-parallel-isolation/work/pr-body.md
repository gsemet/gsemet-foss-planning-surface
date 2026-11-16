## Summary

The gate lock let exactly one long gate run in a whole repository, whatever the project. A project whose long gate is isolated per worktree (its own ports, temporary folders and services) lost hours waiting: with four ready changes, the last one waited about two hours. The project can now say in `chantier.yaml` how many long gates may run at once, and the lock admits that many.

## Deliverables

`chantier.yaml` gains one key (default 1, today's behaviour):

```yaml long_gate:
  parallel: 2     # long gates that may run at once in this repository
```

The lock becomes N slot files; the first keeps its current names.

| Slot | Lock | Run file | Stop marker |
| --- | --- | --- | --- |
| 1 | `.long-gate.lock` | `.long-gate.run` | `.long-gate.stop` |
| k >= 2 | `.long-gate.<k>.lock` | `.long-gate.<k>.run` | `.long-gate.<k>.stop` |

- Arrival order is kept: only the first live queued gate tries the slots, 1 to N in order.
- `gate <cr> --stop`, `order merged` and `cancel` act on the slot that names the CR, and on that slot only.
- `gate <cr> --first --epoch <n>` (steering session only) moves a queued long gate to the head of the queue, through a `first-<ticket>` marker; no ticket is rewritten.
- `status` shows `gate running` for each running CR and `gate queued behind <cr>, <cr>` for a waiter.
- Only the project's named long gate goes through `gate`; short gates run outside the lock (cards).
- The init tour and the Chief of Staff ask once whether the long gate is isolated per worktree.

## Blast radius

Grade: **2**. The lock and the stop route are shared code; with `parallel` absent every file name and message is unchanged. Revert restores the single slot.

## Autonomous decisions

- The new code lives in two new modules (`gate_slots.py`, `gate_queue.py`) to keep files under 400 lines.
- `gate` is registered with `--epoch` so that `--first` can be refused without it.

## Known gaps

- The slot-2 file check on the planning surface creates the files by hand rather than running a gate held in slot 2.
- Making this project's own `just scenario` isolable per worktree is not part of this change.

<details>
<summary>Details</summary>

## Changes

- `commands/gate_slots.py`: slot paths, holder parsing, `list_slots`, `slot_of`.
- `commands/gate_queue.py`: tickets, `first-*` markers, `queued_crs`, `move_first`.
- `commands/gate_lock.py`, `gate_run.py`, `gate.py`, `orders_apply.py`, `release.py`: N slots, per-slot stop, `--first`.
- `playbook/config.py`: the `long_gate` key and `load_long_gate`; `core/files.py`: slot files ignored.
- Cards and docs: `driver.md`, `worker.md`, `concepts.md`, `foreman.md`, `chief-of-staff.md`, `init.md`, `docs/gates.md`, `docs/agents-and-models.md`.
- `declare/gate.py`: gate help, `--first` and BATCH_EPOCH.
- `scenario/run_scenario.py`: step 19b, the surface step, and S4's expected top-level key list (now ending `"ci" and "long_gate"`).

## Impacts

No visual change. Projects with no `long_gate` key behave as before.

## Test plan

- [x] New or changed tests: scenario step 19b (parallel slots, stop per slot, move-up, key validation); it ran in the local long gate before the restack (812 of 813, S4 only failing, fixed since) and passed again in the long gate at 1bb3931 (github 813/813, gitlab 791/791)
- [x] Local gates (at 1bb3931: just check, pytest and ruff pass): `just check` passes; `mypy --strict` clean for linux, darwin, win32
- [x] Evidence (carried from before the restack: range-diff shows both patches unchanged after the restack onto main; the long gate at 1bb3931 re-runs it): direct runs of two gates at once, a third waiting behind both, `--first`, and the key's validation (no screenshots: no visual change)
- [x] Review: inspector approved before the restack, at the S4 fix and at the restack onto CR-225; carried to 1bb3931 (restack onto main, same tree, range-diff patches identical)
- [x] Verified at `1bb3931`
- [x] CI green at `1bb3931` (all five jobs pass)

## Internal references

CR-242 gate-parallel-isolation; round notes in `work/r1.md`.

</details>

