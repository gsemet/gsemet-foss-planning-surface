# Gate queue ticket unlink races on Windows: Change Specification

## Goal

Two long gates running at once on Windows never fail on a queue ticket or a queue mark (its
write, replace, read or unlink) because the other gate holds that file open for a moment. The
stack's local Windows gate (`chantier gate`, `just scenario`, scenario E2 "two at once") passes.
The queue keeps its order and its meaning; the slot locks do not change.

Origin: batch-29, Foreman ask A-8 (2026-11-20). At CR-396 9ff16d5, `just scenario` on Windows
failed in E2: `LongGateLock.__enter__` unlinks its ticket in its `finally`
(`skills/chantier/scripts/cli/src/chantier/commands/gate_lock.py`, line 92) while another gate
reads that ticket (`ordered` / `ticket_cr` -> `read_ticket`), and Windows refuses:
`PermissionError: [WinError 32]`. Ubuntu CI is green at the same head. The race is older than
batch-29.

## Decisions

The user asks no questions on this CR. The Chief of Staff settled these points on 2026-11-20;
this specification records them as such:

1. Scope: only the queue ticket's and mark's sharing violations in the long gate's queue (write,
   replace, read and unlink of tickets and marks), on every OS. No change to the queue's order,
   its meaning or the slot locks.
2. A reader that meets a ticket being removed (`PermissionError` or `FileNotFoundError`) treats
   it as gone for that pass.
3. The owner's unlink and replace retry briefly on `PermissionError` (bounded, a few hundred ms
   in total). If the unlink still fails, the gate does not crash: the ticket is left for the
   existing stale-ticket path to drop. If no such path existed, the retry would stay bounded but
   raise. One exists (see "The stale-ticket path" below), so the unlink does not raise.
4. Tests: one simulated sharing-violation test, portable, in the existing gate tests (no new file
   unless needed), within the test-time budget of `AGENTS.md`.
5. No known gap expected; no pane change.

## The stale-ticket path (checked)

It exists: `gate_queue.ticket_cr(p, drop=True)`, called by every waiting gate through
`LongGateLock._ahead`, deletes a ticket whose pid is no longer alive
(`procs.alive_since(pid, mtime(p), True)` false). `ordered(queue, drop=True)` also deletes a mark
whose ticket is gone.

What it does not cover: it drops a ticket only once its owner's process has ended. A ticket whose
unlink failed belongs to a gate that now holds a slot and runs. Until that gate ends, the ticket
stays live and first by arrival, so the gates behind it wait for it even when
`long_gate.parallel` leaves a slot free. The gate does not crash or deadlock (the owner no longer
reads the queue), but parallel gates run one at a time for that while. Decision 3 accepts this
cost, and the retry makes it rare. To keep the request's "never leave a stale ticket" true at the
end too, the owner tries the unlink once more, with the same bounded retry, when it releases its
slot (`__exit__`). It does not raise there either. A ticket left after that is dead once the
process ends, and the next waiting gate drops it.

## What changes

All paths are under `skills/chantier/scripts/cli/`.

### `src/chantier/gate_queue.py`: one bounded retry, and the reader side

- Add one small helper, private to the queue (for example `_shared(op, *args)`). It calls
  `op(*args)` and, on `PermissionError`, sleeps 10 ms and tries again, up to about 300 ms in
  total (for example 30 tries). It does this **on every OS**, then re-raises the last
  `PermissionError`. Do not reuse `core.files.retry` as it stands: that one retries only on
  `win32` (it raises at once elsewhere, so a portable test could not exercise it), and it waits up
  to a second. Its current callers do not change.
- `read_ticket(p)`: a `FileNotFoundError` or a `PermissionError` returns `None` at once, for this
  pass (decision 2). On Windows, opening a file that is pending deletion raises `PermissionError`.
  A ticket is never written in place (it arrives by `os.replace` from a `.tmp` name the glob does
  not match), so a `PermissionError` on a ticket means it is leaving the queue, not being written.
  The other failures keep their current short retry: an `OSError` other than `PermissionError`,
  a `ValueError`, or content that does not match.
- `ticket_cr(p, drop=True)`: its unlink of a dead ticket already suppresses `OSError`; keep that
  as is.
- `ordered(queue, drop=True)`: the unlink of an orphan mark must not raise on `PermissionError`.
  Two gates may delete the same mark at once, or the owner may be deleting it. Suppress
  `FileNotFoundError` and `PermissionError` there (the mark is going either way).
- `move_first`: the `touch()` of a mark goes through the helper. If it still fails with
  `PermissionError`, skip that mark: a mark that is pending deletion belongs to a ticket that is
  leaving the queue. Do not raise. What `move_first` returns does not change.

### `src/chantier/commands/gate_lock.py`: the owner side

- `__enter__`: `os.replace(tmp, self.ticket)` goes through the helper. If it still fails, the
  `PermissionError` propagates as today. A gate with no ticket cannot queue, and there is no
  ticket to leave behind. Remove the `.tmp` file before re-raising (suppress `OSError` on that
  removal). `tmp.write_text` stays as it is: the `.tmp` name is unique to the process and no
  reader opens it. It may go through the helper too if the Driver prefers.
- The `finally` of `__enter__`: the unlink of the ticket and the unlink of its
  `first-<ticket name>` mark each go through the helper (keep `missing_ok=True`, or the same thing
  with `FileNotFoundError` suppressed). If either still fails with `PermissionError`, swallow it
  and note the ticket as not removed (for example `self.left = True`). The gate goes on.
- `__exit__`: after `holding("")` and `_release()` (keep their current order), when the ticket or
  its mark was left, try both unlinks again through the helper, and suppress `OSError`. Never
  raise from there.
- `_ahead`, `_take`, `_acquire`, `_wait_suite`, `holding`, `_release`, the slot locks and the
  waiting messages do not change.

### Tests: `tests/test_gate_queue_order.py`

That file is the existing test file of the long gate's queue. Add one test (or one parametrized
test with an owner case and a reader case) that simulates the sharing violation on every OS with
`monkeypatch`. No real second process and no `time.sleep` of the test's own: patch the helper's
sleep to a no-op, or keep the default 10 ms steps. The whole test must stay well under one second.

- **Reader side:** a queue with two tickets, where `Path.read_text` on one of them raises
  `PermissionError` (once, or always). `ordered(queue, drop=True)` and `ticket_cr(p, True)` do not
  raise, and the ticket counts as gone for that pass (`ticket_cr` returns `None`). It is not
  deleted by the reader for that reason (its pid is alive: use `os.getpid()`). An orphan mark
  whose `unlink` raises `PermissionError` does not make `ordered(..., drop=True)` raise.
- **Owner side:** `LongGateLock(repo, "CR-1", log)` on a temporary repository. Use the same kind
  of state the CLI tests already prepare, or a minimal stand-in carrying what `changes` and
  `gate_slots.slot` read. `Path.unlink` on its ticket raises `PermissionError` for the first few
  calls and then succeeds: `with LongGateLock(...)` enters, and the ticket is gone after
  `__enter__`. In a second case, the unlink on the ticket always raises during `__enter__`: the
  gate still enters and exits without raising. Lift the patch before `__exit__`: the ticket is
  gone after `__exit__` (the retry at release).

Keep it to these cases; no new test file.

## Out of scope

- The queue's order (next merge, then marked, then arrival), its meaning, `gate --first`'s
  behaviour and messages, `queued_crs`, `gate_state`, `status`/`activity` words.
- The slot locks (`gate_slots.py`, `try_lock`/`unlock`), `gate_run.py`'s run record (it has its own
  replace retry), `core.files.retry` and its callers.
- Any change to the CR board pane, `STATUS.json`, the cards or the scenario's checks. E2 and E5
  stay as they are: E2 already asserts that no ticket is left (`not tickets()`).

## Evidence

- `just test` passes on Windows and on Linux, with the new test included. `just test` stays
  within the `AGENTS.md` budget (at most 30 s above its 18.5 s of 2026-11-14 on the user's
  Windows machine); the new test adds well under a second.
- The new test fails at the base head and passes at the CR's head, on Linux as well as on Windows
  (the simulated `PermissionError` does not depend on the OS). Before the fix, the owner case
  raises `PermissionError` out of `__enter__`.
- `just check` passes (Linux, macOS, Windows in CI). `just eval-dry-run` passes in the worktree
  before the first push (a change under the CLI's `src/`).
- `just scenario (ubuntu-latest)` is green at the PR's head (a CLI change).
- Windows: `just scenario` passes locally at the top of the stack (`chantier gate`), E2
  included. That is the run that failed at CR-396 9ff16d5, and it is the fix's acceptance on the
  OS where the race lives. The scenario run is the real proof of the race. The unit test proves
  both sides survive a simulated violation.
- No host or default matrix: the change does not depend on the host (Claude Code, Copilot) or on
  a shipped versus configured value (`long_gate.parallel` changes nothing in it).
- No known gap; no pane screenshot owed (no pane change).

## Open questions

None that block. One point for the Chief of Staff to confirm or overrule. The brief puts the
scope "in `commands/gate_lock.py`", but the queue's reader (`read_ticket`, `ticket_cr`,
`ordered`) and the mark write (`move_first`) live in `src/chantier/gate_queue.py`, which
`gate_lock.py` imports. This specification touches both files, and only for ticket and mark I/O.
The retry at release in `__exit__` is this specification's reading of the request's "never leave
a stale ticket"; it adds no new behaviour beyond a second bounded unlink.

- Settled by the Chief of Staff (2026-11-20, the user asks no questions): the scope covers `gate_queue.py` too (ticket and mark reads and writes only), and the extra bounded unlink at slot release stays.
