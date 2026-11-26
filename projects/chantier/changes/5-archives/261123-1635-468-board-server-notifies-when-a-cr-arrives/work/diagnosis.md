# CR-468: why `surface-board (github)` is 157/178 at 0267f737

Source: `scenario/results/20261123-152408-28108/surface-board-github.{json,md,out}` in the worktree
(the gate's scenario output; no run started by me). Reproduce one unit:
`uv run --locked python scenario/run_scenario.py surface-board` (check the CLI of run_scenario for
the unit selector). The json names 21 failed checks; they come from two causes.

## Cause A (code bug): `seat take`/`seat leave` deadlock on the lifecycle lock (3 checks)

`commands/seat.py` runs `_take` inside `with changes_lock(repo)` (line ~176). The commit added
`*arrival_lines(repo)` to `_take`'s output. `arrival_lines` (`commands/arrival_line.py`) calls
`arrival_mark.move_told_mark`, which takes `changes_lock(repo)` again. The lock is not re-entrant
(`store/folder.py` `lock()` opens the lock file anew; msvcrt `LK_NBLCK` / flock refuse a second
handle of the same process), so it waits 30 s and fails: `error: CR lifecycle is locked for over 30 s`,
exit 2. It only fires when a told mark has to move, that is when untold `arrived@1` lines exist and no
watcher runs: the case of every scenario that files CRs before `seat take`.
Failed checks: `seat take s-1 ... exits 0` (remote_board), `seat take sess-a exits 0` (forge_hub and
surface_server). Real-world effect: `seat take` hangs 30 s then fails for a Chief of Staff
that has arrivals to be told. Not a scenario problem.
Fix: in `_take` (and `_get`, which is not under the lock, is fine) do not call
`arrival_lines` under the lock: build the lines after the `with` in `seat()`, or give
`move_told_mark` a variant that assumes the lock held (`_move_told_mark_locked`), used from `_take`.
The seat also stays untaken after the failure, which cascades into the checks that need A's seat
(B below: board not started with `--seat`, `watch: not running`, etc.).

## Cause B (scenario drift): the new `arrived@1` lines change seq numbers and line shapes

`file` and `triage` now append an `arrived@1` line (via `session`) to the project's
`forge-journal.jsonl` unless the run holds the seat (`arrivals.own_session`). The scenarios' helpers
`SurfaceWorld.prepare` (run_scenario.py ~10719) and the board's `file`/`triage` calls run before any
`seat take`, so each CR prepared adds two lines (1-inbox, then the backlog). So in `forge_hub`
(6 + 1 CRs prepared in demo, `Hub A1..A6`) the journal of `demo` holds 12 `arrived@1` lines before the
test begins, and every hard-coded cursor or seq is off. Evidence in the `.md`: `status` prints
`another session wrote 1-inbox/hub-a1 (new in 1-inbox) ...` x10 + `and 2 more arrivals`, and
`watch: ... watch --after 12`, where the checks expect `--after 0` / cursor 0 / `seq 1`.

Checks that fail from it:
- `status` ... no watcher ... ends with the `watch: not running` line (expects `no_watcher(0)`, gets cursor 12;
  arrivals lines also precede it).
- `watch --after 5 exits 1` and `watch --after past the journal's end exits 1` (journal now has 12 lines, 5 is not past the end).
- A's watcher start line `from cursor 0` (is `cursor 12`), the board's command line check (empty argv:
  the board was not started because the start line check failed first, and the seat was absent: cause A),
  B's watcher `from cursor 0` (is `cursor 2`), `hub` entry of `server.json`
  (`board_pid` None), `status` holds the `pull path` line `--after 0` (is `--after 12`), A's watcher
  ends with `forge saw merged` + `cursor(1)` (is `--after 13`).
- `forge_hub`, `surface_server` ran to the end: `KeyError: 'cr'` (`e["cr"]` over journal entries that now include
  `arrived@1`, which has no `cr`); `remote_board`: `KeyError: 'action'` at run_scenario.py:1990
  (`forge_lines()` now holds `arrived@1` lines, no `action`; the expected `seq == [1,2,3]` too);
  `external_surface`: `KeyError: 'key'` (config@1 filter over lines now holding `arrived@1`).
- `journal add issue@1` expects `seq 1`, gets `seq 4` (3 arrivals first); second add expects `already there (seq 1)`.
- `a remote status prints what status --profile local prints, less watch:`: `status` now writes the told mark: the first
  `status` (remote) tells the 3 arrivals and moves the mark, the second (`--profile local`) prints none
  (remote has 3 `another session wrote ...` lines, local has `watch: not running` line only). Status is no longer idempotent.
- `a watcher of A started while the board runs ... from cursor 0` (is `cursor 6`).
- `webui on a running server prints board already running`: output is `board on http://...` (a new
  board was started): the board the scenario expected is not running; probably a cascade of the failed
  seat/watcher steps (the board was started `--stop-idle` and gone). I did not prove it separately: re-check after A and B are fixed.

## Fix proposal (scenario `run_scenario.py`, plus the seat.py fix)

1. Code: remove the re-entrant lock in `seat take` (cause A). Add a test (`tests/`) of `seat take` with an
   untold arrival and no watcher: exits 0, prints the arrival line.
2. Scenario: make the setup arrivals not count, in `SurfaceWorld.prepare`/the board's filing
   helpers: either take the seat before filing (own_session needs `autostart.holds_seat(seat.transcript)`,
   which the scenario's host may not satisfy: check) or, simpler and honest, run the helper's `file`/`triage` with
   the env that says "own session", or move the told mark after setup:
   after the preparations, call `status` once (tells and marks the arrivals) and set the cursors in the checks to the
   journal's length, e.g. `cur = len(journal())` rather than 0/1/5. Prefer computing offsets from `journal()`
   (`no_watcher(cur)`, `watch --after cur+5`, `cursor(cur+1)`, `seq cur+1`, `from cursor cur`).
3. Scenario readers of the journal (`e["cr"]`, `e["action"]`, `e["key"]`, `forge_lines()`, `journal()`): filter
   by `type` (`merged@1`, `board@1`, `config@1`, `issue@1`) before indexing, as the new surface_writer check does.
4. Remote `status` comparison: call `status` once beforehand (to tell the arrivals), then compare.
5. Add the scenario's own `arrived@1` assertions only in `surface_writer` (already done at 0267f737).
