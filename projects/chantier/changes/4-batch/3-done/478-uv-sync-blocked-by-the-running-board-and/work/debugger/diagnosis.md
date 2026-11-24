# Diagnosis: scenario surface-board (github), "the old process ended ..." red on Linux

Reproduction: `just scenario` on Linux/macOS (CI run 45435795166, ubuntu-latest), unit surface-board;
the case is `restart_board` in scenario/run_scenario.py (check at line 2900). Not reproduced
locally (Windows host, no Linux here); the cause is read from the code, not run.

## Cause
The check's first clause is `not psutil.pid_exists(old_pid)`. `old` is a `BoardProc`, a direct
`subprocess.Popen` child of the scenario runner. When `serve --restart` stops it cleanly, the old
board exits, but on POSIX a dead child stays a zombie until its parent reaps it (`wait`/`poll`).
The runner never polls `old` before the check (it only calls `old.stop()` in `finally`), so the
zombie remains, and `psutil.pid_exists` returns True for a zombie on Linux/macOS. On Windows a
exited process's PID disappears, so it passed locally.

The product is right: the earlier check (the `board stopped:` line, which needs
`restart._ended` -> `procs.alive`) passed in CI, and `procs.alive` (chantier/procs.py:138) counts
a zombie as gone. Only the scenario's own liveness test is wrong. The other two clauses
(`surface_pid(sw) != old_pid`, the 200 from /api/board) are not implicated.

## Fix (scenario only, no CLI change)
Replace the clause with the product's own test, `chantier.procs.alive(old_pid)`:
`not procs.alive(old_pid) and ...` (import `from chantier import procs` in `restart_board`).
Alternative: `old.p.wait(timeout=10) is not None` (reaps the child, then pid_exists is False).
Same pitfall: `surface_alive()` (line 2351) uses `psutil.pid_exists`; it is used right after
`surface_kill` for the new board (a child of `new`, which is reaped by new's own process only when
`new.stop()`... the new board IS `new.p` itself or its child): check that loop at 2905-2907 too;
CI passed that far only because it did not run, so switch `surface_alive` to `procs.alive` as well
to be safe, since later checks (`not surface_alive(sw)`) depend on it.
