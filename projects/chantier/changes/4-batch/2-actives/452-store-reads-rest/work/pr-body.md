## Summary

The plan's store (`store/`, `repo.store`) is meant to be the one way the board, `status` and the forge hub read the planning folder, so that an index can later sit behind it. They still reached the folder through modules that read files directly. This PR moves those modules onto the store and adds a run-time proof that the three open or list no planning-folder file outside the store. No behaviour and no output changes; no index, no cache.

## Deliverables

Modules moved onto the store (every direct read of the planning folder now goes through `repo.store`):

| Area | Modules |
| --- | --- |
| `lifecycle/` (whole package) | `stages`, `layout_check`, `backlog`, `running_batch`, `links`, `moveout` |
| `core/` | `batch.py`, `leases.py` |
| Gate | `gate_queue.py`, `gate_slots.py` (listing and `stat`) |
| Others | `rails.py`, `history.py`, `summaries/{sources,gaps,origin,title}.py`, `commands/crs.py` |

Callers outside that list change only how they call a moved function (they pass `repo.store`).

The run-time proof (`tests/test_store_runtime.py`) installs an audit hook (`open`, `os.listdir`, `os.scandir`) for one board state, one `status` and one hub cycle on a prepared surface, and fails on any read of the planning folder made outside the store, naming the path, the event and the calling frame. A prepared check proves the hook catches a direct `Path.read_text` and not `store.read_text`.

Impactful choices:

- The held gate lock file's text (`gate_slots.lock_text`, read from byte 1 because byte 0 is the OS lock) stays a direct read, an exempt entry in both the structure test and the run-time proof; its listing and `stat` go through the store.
- Two reads of a worktree (`rails.py`, `commands/crs.py`) are reads of another place, exempt by name.
- The configuration stays read by `playbook/`, not the store.
- `Path.exists`, `is_file`, `is_dir` and `stat` raise no audit event: the run-time proof cannot see them, the static structure test covers them.

## Blast radius

Low. Reads only; same files, same order, same output. Roll back by reverting the PR.

## Autonomous decisions

- Callers of moved functions (`board/write_api.py`, `commands/gate_lock.py`, `gate_run.py`, `orders_merged.py`, `release.py`, `summary.py`, `waits.py`, `hub/issue_refs.py`) pass the store, with the signature picked per module.
- The gate lock exemption in the run-time proof matches the calling function (`lock_text`), not only the path.

## Known gaps

- 20 modules of `commands/` still read directly, 60 calls, none reached by the board, `status` or the hub, and nothing is filed for them: `opening.py` 7; `close_archive.py`, `closing.py`, `delivery.py`, `facts.py` 5 each; `gate.py`, `permissions.py` 4 each; `came_back.py`, `gate_run.py`, `intake.py`, `joining.py`, `rules.py` 3 each; `preflight.py`, `waits.py` 2 each; `driver_notes.py`, `endpause.py`, `opening_record.py`, `release.py`, `summary.py`, `validate.py` 1 each.
- The board's push loop, its file watch and the watcher are not observed by the run-time proof.
- `README.md`, `docs/` and the cards were searched: no sentence this PR makes false was found.

<details><summary>Details</summary>

## Changes

- The modules above read through the store; `tests/test_store_reads.py` lists them (`lifecycle` package and the new modules) with exempt entries for reads of other places.
- New `tests/test_store_runtime.py`, with one module-scoped surface shared by its cases.
- `CONTRIBUTING.md`: the store sentence names the run-time proof and says the configuration is read by `playbook/`.

## Impacts

No visual change. Developers: a new direct read of the planning folder in a listed module fails the structure test, and in the board, `status` or the hub fails the run-time proof.

## Test plan

- `just check` at 9d3ff72: pass (1635 passed, 20 skipped).
- Speed, on a planning folder of 242 backlog CRs plus a running batch, 7 alternating runs base (e417190) then head (9d3ff72), Windows, CPU load 3 to 53 % from other processes: board state median 1.0370 s base, 1.0954 s head (+5.6 %); `status` median 0.6404 s base, 0.6721 s head (+5.0 %, about 0.6 s of it process start). Both within the 10 % rule.
- Time added to `just test`: `tests/test_store_runtime.py` runs in 0.91 s (6 tests, one shared surface built once in 0.38 s).
- **UNVERIFIED:** `just eval-dry-run`, `just scenario` at the pushed head.

## Internal references

- CR-452 `store-reads-rest` (split from CR-419), batch-30.

</details>
