# Conflict resolution: CR-221 rebased on origin/main 12df9b4 (CR-224, batch history)

Rebase of the one commit; result 66659bd. Conflicts: modify/delete on `commands.py`, `state.py`,
`status.py` (modified by CR-224, deleted by the split). The three stay deleted; each CR-224
change was ported by hand:

| origin/main change | Now in |
| --- | --- |
| `state.py`: `RECORDS`, `next_batch_number` reads the records | `core/repo.py` |
| `state.py`: `write_file` writes `\n` on Windows | `core/files.py` |
| `state.py`: `Batch` reserves the record at `open`, removes it on a failed open | `core/batch.py` |
| `state.py`: `resolve_batch` names the last closed batch | `core/batch.py` |
| `state.py`: backfill after the old-tree conversion | `lifecycle/convert.py` (`open_repo`) |
| `status.py`: `_past` skips `batches` | `status/views.py` (`_when` made public as `when_of`, backfill uses it) |
| `commands.py`: `archived_merged` skips `batches` | `commands/opening.py` |
| `commands.py`: `status` prints the last-closed line | `commands/batch_status.py` |
| `commands.py`: `close` writes the record and retro | `commands/closing.py` (+ new `commands/close_archive.py`: `Closing`, `archive_and_delete`) |
| `history.py` (new) | split in two: `core/batch_records.py` (paths, read/write, reserve, check/undo close, last closed; no domain import, so `core.batch` can use it with no cycle) and `history.py` (texts: last-closed line, record entries, `batch-NN.md`) |
| `backfill.py` (new) | `lifecycle/backfill.py` |

`scenario/run_scenario.py`, docs and cards merged with no conflict.

## Numbers (ruff 0.17.5, mypy 1.20.0 --strict)

- ruff check: 49 before the rebase, 46 after.
- mypy: 407 errors before, 402 after.
- history/backfill code: no ruff finding, no mypy error of its own; files 172 to 236 lines; no
  function over 50 lines; PEP 723 deps unchanged (stdlib only).
- `just test`: 59 pass, 1 fails: `test_code_targets` (functions over 50 lines in `board/server.py`,
  `cost/*`, `delivery`, `facts`, `forge_stack`, `intake`, `seat`, `costs/copilot`, `stages`,
  `playbook/config`, one test). Same list as before the rebase; none in the new or ported code.

## Not met

Nothing of the CR's code targets is missing for history/backfill. `close_archive.py`'s
`Closing` carries `d: dict`-like records typed `Rec`; the rest of the debt above is the CR's own.
