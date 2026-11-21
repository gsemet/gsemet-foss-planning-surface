## Summary

Two long gates running at once on Windows could fail with `PermissionError: [WinError 32]` on a queue ticket (or its "first" mark): one gate removed its ticket while the other was reading it, and Windows refuses an open file's removal. The scenario "two at once" failed on Windows for that reason while Linux CI was green. The queue now tolerates that sharing violation, on every OS, and keeps its order and meaning.

## Deliverables

The queue's file operations that can meet a file held open for a moment now go through one bounded retry, and a reader treats a ticket being removed as gone for that pass.

```python
# gate_queue.py
def _shared(op, *args):
    """op(*args), retried every 10 ms for ~300 ms on PermissionError, then raised."""
```

| Operation | Before | After |
| --- | --- | --- |
| Reader meets a ticket being removed (`read_ticket`) | raises `PermissionError` | ticket counts as gone for that pass |
| Orphan mark removed by `ordered(drop=True)` | raises on `PermissionError` | suppressed (the mark is going anyway) |
| Mark touched by `move_first` | raises | bounded retry, then that mark is skipped |
| Ticket published (`os.replace`) | raises at once | bounded retry; the `.tmp` is removed if it still fails |
| Owner removes ticket and mark | raises at once | bounded retry; if it still fails the gate goes on and tries again when it releases its slot |

Choices: the retry is on every OS (so a portable test can exercise it) and does not reuse the generic Windows-only retry; a ticket that cannot be removed is dropped by the existing stale-ticket path once its process ends.

## Blast radius

Grade: 1. The change is limited to the long gate's queue file operations; the slot locks and the queue's order are untouched. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The retry helper lives in `gate_queue.py` and `gate_lock.py` imports it: both files do the queue's file I/O, and one helper avoids a second copy.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `gate_queue.py`: `_shared` helper; `read_ticket` returns `None` on `PermissionError`; `ordered(drop=True)` suppresses `PermissionError` on an orphan mark; `move_first` touches marks through the helper.
- `commands/gate_lock.py`: ticket publication and removal go through the helper; a ticket or mark that stays is retried once more when the slot is released; never raises there.
- `tests/test_gate_queue_order.py`: a portable test simulating the sharing violation on the reader and owner sides.

## Impacts

No visual change. Parallel gates on Windows no longer crash on a ticket race.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_a_sharing_violation_on_a_ticket_or_a_mark_stops_no_gate` fails on the base and passes at the head
- [x] Local gates at `0f0ca54` (carried from `830b74d`): `just check` pass; `just eval-dry-run` pass (18 of 18)
- [x] Local long gate at `0f0ca54`: `just scenario` pass (the batch top runs it locally)
- [x] Evidence: none (no visible change)
- [x] Review: approved at `0f0ca54` (carried from `830b74d`)
- [x] Verified at `0f0ca54` (carried from `830b74d`)
- [x] CI green at `0f0ca54`: check (3 systems), eval-dry-run and scenario (ubuntu) pass

## Internal references

- CR-400 gate-queue-ticket-unlink-races-on-windows

</details>
