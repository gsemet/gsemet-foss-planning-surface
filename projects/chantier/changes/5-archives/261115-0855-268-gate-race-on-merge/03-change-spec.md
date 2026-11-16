# Change Specification: `order merged` stops the CR's gate before it moves the folder

## Goal

When a CR is recorded merged (`order merged <cr>`, the user's or the Foreman's `--epoch` form) while
its long gate runs, the CLI stops that gate and waits for the gate's process to end before it moves
the CR's folder from `2-actives` to `3-done`. The stopped gate then writes its last log line and its
`stopped` event with its folder still in place: no `FileNotFoundError` from `_finish_stopped`, no
Windows os error 32 (WinError 32) from a folder moved while a process still holds it, and the
scenario's gates unit E4 stops failing now and then.

Source: batch-18's retro (kept by the retro critic and a Fable review); the race is proved in
batch-18 CR-266's `work/diagnosis.md` (`.agents/changes/4-batch/3-done/266-stack-gate-waiver/work/diagnosis.md`).
First CR of batch-18's stack.

## The race today (read-only facts)

- `chantier gate <cr> "<cmd>"` (`skills/chantier/scripts/cli/src/chantier/commands/gate.py`, `gate()`)
  logs in the CR's own folder, `work/gates/<stamp>.log`, holds a slot of the long-gate lock
  (`LongGateLock`, lock text `<cr> pid <n> pg<m>`), and runs the suite in its own process group.
- `order merged` (`commands/orders.py`, `order()`) takes `changes_lock` and the batch lock
  (`RenderedBatch`), then `orders_apply._merged` calls `_stop_gate` -> `gate_run.stop_gate`, which
  writes the slot's stop marker (`.long-gate[.k].stop`) and stops the suite's group
  (`procs.stop_group`), and returns at once; `merge_done` (`rails_release.py`) then moves the folder
  (`Batch.move`), still under the same locks.
- The gate process wakes from `p.wait()`, sees the stop marker, leaves its lock and runs
  `_finish_stopped`: `if g.log.exists(): g.note(...)` (check, then open), then
  `RenderedBatch(...)` to log its `stopped` event. When it wakes late, the folder moves between the
  check and the open: `FileNotFoundError`, a traceback in the gate's stderr.
- The stopped gate needs the batch lock to log its event, and `order merged` holds that lock while
  it moves the folder. So the wait cannot happen under the batch lock: a wait there would block the
  gate on the lock it needs (up to `LOCK_TIMEOUT_S`, 30 s, in `core/files.py`) and the gate would
  then fail on "batch ... is locked".

## What changes

### 1. `order merged`: check, stop and wait, then record (CLI)

`order merged <cr>` runs in three steps, in this order:

1. **Check, change nothing.** Under `changes_lock` and the batch lock, the same refusals as today,
   in the same words and exit codes: `check_epoch`, an unknown CR, `cannot mark cancelled <cr>
   merged`, and the release CR's `order merged: <ids> not merged or cancelled: the release PR merges
   last`. An already merged CR answers `<cr> already merged` as today, and stops nothing. A refused
   order stops no gate and writes nothing (no record, no event, no order id). The locks are then
   released.
2. **Stop and wait, out of the locks.** When a slot's holder names the CR (`gate_slots.slot_of`) and
   the holder's gate process is still that process (`procs.alive_since(h.pid, mtime(lock), False)`,
   as `stop_gate` reads it today): write the slot's stop marker, stop the suite's group when it
   runs (as `stop_gate` does now), then wait until the gate process (`h.pid`) has ended, polling
   with `procs.alive_since` (`procs.POLL_S`), up to a bound (see the open question; proposed: the
   CLI's lock timeout, `LOCK_TIMEOUT_S`, 30 s). During this wait the gate writes
   `result: stopped at <head>: no pass` in its log and logs its own `stopped` event, under the batch
   lock it can now take, its folder still in `2-actives`.
   - When no slot names the CR, or its gate process is already gone: nothing to stop here; step 3
     handles a stale lock exactly as `_stop_gate` does today.
   - When the gate process has not ended at the bound: `order merged` refuses with nothing changed
     (exit `EXIT_PRECONDITION`, 2), the CR stays where it is, and the message names the CR, the gate's
     pid and what to do, e.g. `order merged CR-103: its long gate (pid 4242) did not end within 30 s
     after its stop: nothing recorded; run the order again once it ends`. No move "anyway" and no
     kill of the gate process itself (no fallback, AGENTS.md).
3. **Record and move.** Under `changes_lock` and the batch lock again: run the step-1 refusals
   again (the state may have changed between the two lock holds), then `_merged` as today: its
   `_stop_gate` call stays and now finds either no holder (the gate left) or a stale one (it records
   `stopped` as today, writing the log line only when the run's log exists); `merge_done` or
   `release_merged` moves the folder; the order is recorded (`_record_order`).

Output: unchanged in shape. The line `stopped the long gate of <cr> (pg<m>)` (or without the group
when none ran) comes from step 2 when step 2 stopped a gate, from step 3's `_stop_gate` otherwise,
and stays at its place today: right after `merged <cr> ...` for a plain CR, after the release line
for a release CR. Exactly one `stopped` gate event per stopped run: the gate's own when it was alive
(step 2), the stopper's when the lock was stale (step 3), never both.

Where the code goes (the Driver judges the details, within these constraints):

- The stop-and-wait is one function shared by nothing else yet, in
  `commands/gate_run.py` next to `stop_gate` (e.g. `stop_and_wait(repo, cr_id, timeout_s) ->
  Stopped | None`), and a wait helper in `procs.py` if one reads better there (e.g.
  `wait_gone(pid, recorded, timeout_s) -> bool`). It takes no `Batch`: it logs no event itself.
  The write of the stop marker and the stop of the group are the same code as `stop_gate`'s alive
  branch, factored, not copied.
- `order()` in `commands/orders.py` stays under its function-size limit (see commits `afd42be` and
  `170daa1`): the three steps live in a helper for the `merged` kind (in `orders.py` or
  `orders_apply.py`, which must stay under 400 lines), and `order()` calls it.
- The `--epoch` form (the Foreman's own merge) and the plain form (the Chief of Staff's) take the
  same path.

### 2. `gate.py`: unchanged

`_finish_stopped` keeps its code: no try/except around `g.note`, no new log place. The gate's log
stays in the CR's folder (`work/gates/`), which stays self-contained (CR-257). `_finish`'s
`if g.log.exists()` check (for `cancel`) is not touched.

### 3. Cards and docs

No card changes: the cards do not describe how `order merged` handles a running gate, and the
change is CLI-only, the same on both hosts (Claude Code, GitHub Copilot) and both forges (GitHub,
GitLab): it reads no host and no forge. So no card line needs the mark "unproved". The help text of
`order` (`orders.py` / the parser) mentions the stop only if it already does; when it does, it adds
"and waits for it to end before the move".

### 4. Scenario (`scenario/run_scenario.py`)

- Gates unit, E4 (`# E4. a stop acts on its slot only`, the check `E4: \`order merged\` stops its CR's
  gate only`, near line 3257): right after `w.chantier("order", "merged", two, "--epoch", 1)`
  returns, and before `second.communicate(...)`, the gate process has already ended
  (`second.poll() is not None`); the check also asks `"Traceback" not in err`, the gate's exit 4,
  the last line of that run's log, read in the CR's `3-done` folder, `result: stopped at <head>: no
  pass`, and exactly one `stopped` gate event for that run. The check's title says so, e.g.
  `E4: \`order merged\` stops its CR's gate only, and waits for it to end before the move`.
- The earlier check `` `order merged` stops the CR's own long gate ... `` (near line 2867) gains the
  same `running.poll() is not None` right after the order returns.

### 5. Tests (`skills/chantier/scripts/cli/tests/`)

One fast refusal test (in `test_gate_refusals.py`), in-process: a prepared batch with a CR in
`2-actives`, a slot lock naming that CR with the pid of a child process started before the lock was
written that ignores the stop (e.g. a sleeping Python child), and the wait bound patched to a
fraction of a second. `order merged <cr> --epoch <n>` exits 2 with the message above; the CR is still
in `2-actives`, its status unchanged, no `merged` event, no order recorded. The child is ended by the
test's teardown. It adds well under a second to `just test`.

## Decisions of `02-answers.md`, carried

- The fix is the request's: `order merged` stops the running gate and waits for its process to end
  before the move; no try/except in `_finish_stopped`, no log outside the CR's folder (section 1, 2).
- Generality: the same on both hosts and both forges; nothing here is host- or forge-specific, so no
  card line carries "unproved" (section 3).
- Place in the stack: first (Goal).
- Windows os error 32 on a folder move: covered by the same order, stop, wait, then move (section 1,
  step 2: the gate process, whose shell holds the log, has ended before the move).

## Out of scope

- `cancel`, which also moves a CR's folder while its gate may run (`_finish`'s check-then-open in
  `gate.py`): not named by the request; untouched.
- `gate <cr> --stop`: moves no folder; untouched.
- The long-gate lock, the queue, the slots and the log format.
- Any try/except or log move in `gate.py` (refused by the request).

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just test` passes, with the refusal test above; its time stays within AGENTS.md's bound.
- `just scenario` passes, gates unit E4 with the strengthened check, and the earlier `order merged`
  check; the gates unit runs alongside the other units on the user's Windows machine with no E4
  failure (the load that exposed the race). CI's Ubuntu run proves POSIX.
- The PR's Deliverables quote the E4 check line from the scenario's result file.

## Open questions

1. The wait's bound, and what happens past it. Proposed: 30 s (the CLI's lock timeout), then
   `order merged` refuses with nothing recorded and the CR not moved (exit 2), naming the gate's pid;
   the Chief of Staff or the Foreman runs the order again once the gate has ended. Is that the
   behaviour the user wants (rather than another bound, or waiting with no bound)?
