# Investigation CR-429 (fp-cache): the server watches the planning files

Read-only map at the worktree head (based on CR-426's store work). CLI root:
`skills/chantier/scripts/cli/src/chantier/` (`S/` below), tests `skills/chantier/scripts/cli/tests/` (`T/`).

## Files and entry points

Server side (spec sections 1-3):
- `S/board/watch_files.py` NEW. `FileWatchThread`, a pure settle class driven by `(path, now)` (test seam), mode `notify|check`.
  Uses `store`/`project.repo.changes`, `core.files.is_lock`, `fingerprint.SINGLE/HOLDS/DEEP/SHALLOW` to filter paths.
- `S/board/fingerprint.py`: `fingerprint(store, changes, extra)` stays; add a `counts_for(rel)` path filter next to the constants.
- `S/board/context.py`: add `revs: dict[str,str]` + lock (the file already has `_lock`, `Context` is a dataclass built by hand in 11 test files).
- `S/board/reads.py:state_of` (l.25-42): replace the `fingerprint(...)` call by `sha256(rev + "\n" + live.mark())`; lazy rev when none kept. Callers: `topics._project/_costs/_answer`, `ops._prs`, `reads.board_data/costs_data/state_data`.
- `S/board/api/push.py`: `PushLoop.wake()` (Event), `observed()` (needs `_subs` count + long-poll stamp in `hold()`), `PushThread._run` waits on the event instead of `self._done.wait(push_every_s())` (l.~170). `poll(now)` stays the test seam (`due` gate: the wake must force `_next=None`).
- `S/board/api/times.py`: `_test()` is a strict 4-tuple unpack; becomes 4, 5 or 6 fields; add `CHECK_S=5.0`, `IDLE_STOP_S=1800.0`, `check_s()`, `idle_stop_s()`; keep `min>0`.
- `S/board/command.py`: `_run` (start FileWatchThread beside hub/push/writer, first fingerprints before `box[0].run`, idle-stop timer, stop in `finally`), `_announce`/`_running_lines` (add `WATCHES/CHECKS/STOPS_IDLE/FORGE_WHEN_OBSERVED`), new args `--stop-idle`, `--forge-always` (parser lives in `S/cli.py`; refuse both -> EXIT_USAGE), `_silent` text to a shared helper, `state.write_server` call gains `files/stop_idle/forge`.
- `S/hub/state.py:write_server` (l.152): new optional fields; `files` known only after the watch starts -> a second `modify` (or start the watch before `write_server`; the spec says mode decided before the line prints, so start watch first, then write).
- `S/hub/loop.py:HubLoop.poll(now)` -> `poll(now, observed)`; `HubThread` takes the predicate; idle: `Hub.record["idle"]`, `last=None` reset on idle. `S/hub/cycle.py:Hub` gets `set_idle(bool)` (+ `publish`).
- `S/hub/lines.py:hub_line`: drop `a watcher` branch, add idle form. Docstring of `watch_lines` mentions the hub.
- `S/board/seats.py`: no code change expected; idle stop is a second watcher thread next to `Seats._loop` (put it in `command.py` or `watch_files.py`'s sibling, not in Seats). Seats registered must not count (observed() reads PushLoop only).
- `pyproject.toml` (+`uv.lock`): add `watchfiles`, ban module-level import (`banned-module-level-imports`, l.60). `watchfiles` is NOT in `uv.lock` today (anyio is): `uv lock` needs network.

Watcher side (sections 4-5):
- `S/hub/watch.py:Watch` rewrite: drop `HubLock`, `Hub`, `elect` hub part, `yield_hub`, hub clauses of `start_line`, the journal read in `poll` (l.230-240); `poll(now)` takes the queue of `Link` items. Keep `WatcherLock`, `subscription`, `seat_moved`, `open_batch`, `once`, `lines`. New: `IDLE` reason + constant, seat-rule start, detached `Popen`, 20 s wait on `address.probe`, `register_seat`, the three failure endings, `BEYOND/NO_NETWORK/WATCHES/CHECKS` lines. `watch()` (l.292) loop: `time.sleep(poll_s)` must now also drain the link.
  Suggest splitting: `hub/watch.py` (Watch state machine, ~250 lines) and new `hub/watch_board.py` (find/start the board, detached Popen, lines) to stay under the file-size habit (module is 245 lines now).
- `S/hub/times.py`: `_test()` strict 2-tuple unpack -> 2 or 3 fields; `IDLE_END_S=7200.0`, `idle_end_s()`; `wake_every_s` uses `test[1]`.
- `S/clients/tui/link.py:Link` (382 lines): `hub/` must not import `clients.tui.screen`; `link.py` imports only `chantier` core/errors, so `hub/watch.py` can import `clients.tui.link` directly (package `clients/tui/__init__.py` check that it does not pull screen/rich; if it does, move `link.py` to `S/clients/link.py`, and fix `commands/live.py`, `tests/test_live_link.py`). Link hardcodes `CLIENT = chantier-live/...`; needs a client-name arg for the watcher. `items()` is a blocking generator with `Idle` each `STEP_S`=1 s: a reader thread feeding a `queue.Queue` is needed (spec allows). `Link` has no 401 vs silent distinction exposed: `refused()`/`BAD_KEY` -> `ChantierError`; the 20 s no-`welcome` ending needs `Link` to surface it (today `OPEN_S=5` then HTTP; both failing loops forever with `Linked(None)`), so add a `give_up_after` or let the watcher count `Linked(transport=None)` time.
- `S/hub/lines.py`, `S/hub/autostart.py:board_clause` (wording `board is chantier <v>: restart it to run this version`; test strings in `test_watcher_autostart.py`), `S/hub/__init__.py` docstring, `S/writer/lines.py:START`.
- `S/board/address.py` (`register_seat`, `probe`, `loopback_base`, `is_loopback`) used as is. `S/board/running.py:stop_command`, `find_pid` used as is.
- `S/commands/live.py:recorded()` is the model for the watcher's `recorded` (extract to a shared function in `board/address.py` or `hub/`).

Cards/docs/scenario (sections 6-8): `references/session-start.md`, `chief-of-staff.md` (+ `skills/chief-of-staff/SKILL.md` Startup core, quoted by `test_watcher_step.py`), `concepts.md`, `foreman.md` (check only), `hosts/claude-code.md`, `hosts/copilot.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/web-board.md`, `docs/planning-folder.md`, `docs/forge-connectors.md`, `docs/server-api.md`, `docs/hosts.md` (matched the hub grep: check), `scenario/README.md`, `scenario/run_scenario.py` (10748 lines; `forge_hub` at l.2007, `surface_server` at l.2554, `BoardProc` l.1480, other `CHANTIER_HUB_TEST_TIMES` users l.2358, 2448, 2526, 9692), `scenario/fake_gh.py` unchanged. `test_scenario_coverage.py` requires every README bullet `(test: ...)` / `(unit: ...)` to name a real test/unit, so README edits and test renames go together.

## Existing tests to rework (counted from grep)

- `T/test_watch_events.py` (233), `T/test_event_audience.py` (326, Watch built at l.100,136,172,188,296), `T/test_watcher_autostart.py` (237), `T/test_forge_hub.py` (316; l.198-217 HubLock/Watch election tests go), `T/test_surface_server.py` (190; l.41-66 and 153-172 lock tests), `T/test_watcher_step.py` (card sentences: only if SKILL.md wording moves), `T/test_forge_hub_waits.py` (check).
- Tests that build `Context` and mutate files then read state (they will read a stale kept rev): `test_board.py` (l.158,195), `test_board_config.py`, `test_board_journal.py`, `test_board_prs*.py`, `test_board_ui.py`, `test_live_link.py` (l.118 calls `reads.state_of`), `test_server_api*.py` (l.114 `state_of`), `test_store_command_table.py`, `test_writer_commands.py`. One shared helper keeps this small: `Context.settle(project)` (recompute and keep the rev; the same call the watch thread makes) called by tests after a mutation, or by `conftest`'s `Board` fixture's helpers.
- `T/test_board_times.py` (179): seam parsing for 4/5/6 fields; `T/test_board_exposure.py` (157): `_announce` signature.
- New: `T/test_file_watch.py` (settle rule, no-walk, real backend, check mode), `T/test_board_idle.py` (idle stop, observed, hub idle, forge-always, start lines), watcher cases parametrized in a reworked `test_watch_events.py` (+ new `test_watch_board.py` for the seat/server matrix).

## Smallest change

1. `watch_files.py` with a pure `Settler` (project -> first/last change time; `due(now)` returns the projects to settle: quiet 1 s, or 5 s after first change), a thread that feeds it from `watchfiles.watch(..., stop_event, rust_timeout, yield_on_timeout=True)` so the thread also ticks the settler; on settle, `ctx.settle(project)` (walks once, stores rev, `ctx.push.wake()`).
2. `Context.revs` + `Context.settle`; `state_of` uses it. Write ops of the board (`write_api.py`, `backlog.*`, `config.put`) call `ctx.settle(project)` right after their write (see risk 1).
3. Hub: predicate param, `idle` field; `observed()` on PushLoop.
4. Watch rewrite over a `Link` queue; board start helper.
5. Cards/docs/scenario.

## Risks

1. Read-your-writes: a board write op (`backlog.move`) returns, the client's next `project` read sees the old rev for up to ~1 s (settle) and the web client may flash the old state. Spec section 2 is silent. Smallest fix: board write ops call `ctx.settle(project)` after writing (one walk per write, still no timer walk). Decide with the Driver; scenario step "backlog.move ... rev within 3 s" passes either way.
2. Self-triggered loops: the server's own writes (`forge-journal.jsonl` appends by the hub every cycle with events, `.lease-hold.*.run`, `writer` commits touching the planning folder, `.git` is outside `changes/` but the surface's `projects/` watch is recursive over the repo's working tree: writer `git` operations rewrite files there). The filter must restrict to the fingerprint's path set inside `changes/` and only the top-level names of `projects/` (spec says so); do not watch `projects/**` recursively with no filter (`watchfiles` has no path filter in the rust layer: use `watch_filter` callable).
3. Windows: `ReadDirectoryChangesW` delivers paths with the `\\?\` or backslash forms; map paths with `Path.resolve()` vs the project's `changes` (the served root may be via a junction/short name). Tests must run on 3 OS (`just check`); the real-backend test must use a bounded wait and `tmp_path` resolved.
4. `watchfiles` is not locked yet: `uv lock` (network) + `just check` on all three OS; `banned-module-level-imports` means function-level import in `FileWatchThread.start`; the check-mode test monkeypatches the same import site.
5. `watchfiles.watch` blocks in Rust; stop needs `stop_event` and `rust_timeout` (default 5000 ms): choose <=1000 ms so shutdown stays under `JOIN_S=5`.
6. `PushThread._run` today `self._done.wait(push_every_s())`; a wake Event plus the 2 s timeout must not make `poll` run twice per wake (it is gated by `due`; `wake()` must set `_next=None` under the lock so the pass runs now).
7. `CHANTIER_API_TEST_TIMES` and `CHANTIER_HUB_TEST_TIMES` parse with a strict tuple unpack and silently return None on a wrong field count: existing scenario values (`1:6:5:5`, `1:4`) must keep working; add the new fields with an explicit length check (4/5/6 and 2/3).
8. `HubLoop` today elects whenever the lock is free; with `observed()` false it must still hold the lock and write the `hub` entry (spec), so `Hub()` is built but `cycle` skipped; the `idle` flag must clear on the first cycle.
9. Detached start on Windows: `CREATE_NEW_PROCESS_GROUP|CREATE_NO_WINDOW` unproved; spec asks the Known gaps to say so. `subprocess.CREATE_NO_WINDOW` constants only exist on Windows: tests assert with `getattr`/numeric constants guarded by `sys.platform`.
10. Hosts: the watcher is a background task of the host; its detached child board might be killed by the host's process-tree kill (Claude Code on POSIX kills the group; `start_new_session` escapes it; Windows job objects may not be escapable). The trial in the spec's cards covers it; unproved.
11. Value derivations (rule "find by old value"): `20 s` (CYCLE_S/QUIET_S) is not changed; `2 s` PUSH_EVERY_S stays; the doc sentence "looks every 2 s" is `docs/server-api.md` l.~119 (listed). The `a watcher` hub wording appears in `hub/lines.py`, `commands/batch_status.py`, `commands/facts.py`, `commands/waits.py`, `wait_view.py`, `core/waits.py`, `declare/interests.py`, `board/prs.py`, `board/__init__.py`, `cli.py` (grep matched "the hub"/"forge hub"): the Driver must grep each for `hub is chantier`, `a watcher`, `the one watcher`, `yields it` and align the wording (not all are behavioural). The 5 s/1 s/30 min/2 h values are new.
12. File size/lint: `run_scenario.py` is 10748 lines already; add steps in `forge_hub`/`surface_server` only, no new unit (a new unit would need the README coverage bullet and `UNITS`).

## Questions only the user can answer

None. (Spec says none; risk 1 is a Driver decision, no behaviour change visible to the user other than faster refresh.)

## Proposed split into three coder rounds

Round 1, server side (sections 1-3, 5 hub line) plus its tests:
`pyproject.toml`, `uv.lock`; `S/board/watch_files.py` (new), `fingerprint.py`, `context.py`, `reads.py`, `board/api/push.py`, `board/api/times.py`, `board/command.py` (+ parser in `S/cli.py`), `hub/state.py`, `hub/loop.py`, `hub/cycle.py`, `hub/lines.py`, `board/write_api.py` (settle after write); docs touching code text: `hub/__init__.py` docstring first half; `writer/lines.py:START`.
Tests: new `T/test_file_watch.py`, `T/test_board_idle.py`; rework `test_board_times.py`, `test_board_exposure.py`, `test_server_api*.py`, `test_live_link.py`, `test_board*.py` helper `settle`, `test_surface_server.py` (hub lock tests), `test_forge_hub.py` hub_line cases. Gate: `just check`, `just eval-dry-run`. Largest round (about 12 source files, 10 test files).

Round 2, watcher (sections 4, 5 rest):
`S/hub/watch.py`, new `S/hub/watch_board.py`, `S/hub/times.py`, `S/hub/autostart.py` (board_clause wording), `S/clients/tui/link.py` (client name, give-up/silent surface, maybe move), `S/commands/live.py` (shared `recorded`), `board/command.py` (`_silent` shared helper; touched in round 1: round 2 only moves the text), `hub/__init__.py` rest.
Tests: rework `test_watch_events.py`, `test_event_audience.py`, `test_watcher_autostart.py`, `test_forge_hub.py` election tests, new `test_watch_board.py` (seat/server matrix, Popen seam, failure endings, BEYOND/NO_NETWORK lines, idle end, test-times 3rd field). Gate: `just check`, `just eval-dry-run`. Depends on round 1 (`files`, `stop_idle` fields, constants `WATCHES/CHECKS/BEYOND`).

Round 3, cards, docs, scenario (sections 6-8) plus gates:
cards `session-start.md`, `chief-of-staff.md`, `skills/chief-of-staff/SKILL.md` (only if needed), `concepts.md`, `foreman.md` (check), `hosts/claude-code.md`, `hosts/copilot.md`; `AGENTS.md`, `CONTRIBUTING.md`, `docs/web-board.md`, `docs/planning-folder.md`, `docs/forge-connectors.md`, `docs/server-api.md`, `docs/hosts.md` (check); `scenario/README.md`, `scenario/run_scenario.py`. Tests: `test_watcher_step.py` and card-text tests, `test_scenario_coverage.py` stays green. Gate: `just check`, then `just scenario` (ubuntu pipeline job; `chantier gate` Windows for the top CR). This round can start in parallel with round 2 for cards that do not depend on watcher details, but the scenario steps need round 2 merged.

## Evidence plan

Kind: server and CLI behaviour change (no UI pixels; the board pane is untouched: no `hooks/register.tsx` change, so no screenshot owed).
- Before/after measure (spec): a script in the scratchpad run twice (at the base commit and at the head): start `chantier board --ui none` on a copy of the real surface (4 projects), open a WebSocket with subscriptions `board`, `project chantier`, `costs`, `prs`, 60 s idle; count `fingerprint()` calls via a one-line wrapper (env-guarded `sitecustomize`/a small launcher script that monkeypatches `chantier.board.fingerprint.fingerprint` and prints the count and `os.times()` at exit) and CPU of the push thread. Output tables go in `evidence/fp-cache-measure.md` with the head SHA; raw logs `*.log` under `work/gates/`.
- Automatic test (decision 3): the "no walk per pass" test in `test_file_watch.py` (counts `fingerprint` calls over 10 polls = 0).
- Start lines: `evidence/` capture of `chantier board` stdout showing `board: watches the planning files`, and the check-mode line with a forced failure (test seam).
- Watcher-started board: scenario `forge_hub`/`surface_server` logs (the `started the board (PID n)` line, board alive after the watcher ends, idle stop run with the seam).
- Windows no-console-window: cannot be shown by tests; `chantier gate` on the user's machine, user at the screen (Known gaps). Host trials (claude-code, copilot) cannot be shown: stay unproved, trial text in the card rows.
- Cannot show: network-share/WSL `/mnt` behaviour (documented known limit), real-session host process-tree behaviour.
