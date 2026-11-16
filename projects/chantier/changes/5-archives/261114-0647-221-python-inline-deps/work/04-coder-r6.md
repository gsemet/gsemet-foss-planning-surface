# CR-221 round 6: the JSON records as pydantic models

Done: `core/records.py` holds `Record` (extra="allow", written with `exclude_unset`), `BatchSettings`,
`CrEntry`, `ReleaseGrant`, `OrderRecord`, `AskRecord`, `ClaimRecord`, `BatchRecord`, `EventRecord`,
`SeatRecord`, `RunRecord` and `RestoredRecord`. `Batch` holds a `BatchRecord`; rails, commands, status,
board and the tests read and set attributes. mypy --strict, ruff and the size limits pass.

Not finished, for Known gaps:

- The archive record `5-archives/batches/batch-NN.json` (`core/batch_records.py`, `history.py`'s
  `archive_of`, `cr_entry`, `close_record`, `backfill`) stays data (`dict[str, Any]`). It is a
  different file from the spec's list (batch.json, events, seat, gate run, restored); its keys are
  fixed by a UI reader and it is built whole at `close`, not read-modified-written.
- The views (`cr_view`, `batch_view`, `dashboard_view`, board data) still return output dicts: they
  are the STATUS.json shape, not a stored record. They read models and emit the same bytes.
- `parse_grant` returns a dict of the words of `order grant`; it is applied to the `ReleaseGrant`
  by attribute.
- `release grant published` with no grant recorded now says so (ChantierError) where it was a
  KeyError.
- `scenario/run_scenario.py` wraps its event dicts into `EventRecord` where it calls `gate_passed`.
- `RunRecord` (`.long-gate.run`) is defined and written through the model; the gate lock reads it.
- No screenshot: nothing here changes what the board pane draws.
