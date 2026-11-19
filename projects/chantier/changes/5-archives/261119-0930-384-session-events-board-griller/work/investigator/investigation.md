# Investigation CR-384 (head 70e5e8a3)

Paths: `cli/` = `skills/chantier/scripts/cli/`, `src/` = `cli/src/chantier/`.

## What already exists (CR-375, CR-383) vs missing

Exists:
- `hub/autostart.py`: `session_key()`, `watch_command(repo,n)`, `other_sessions`, `not_running_line(repo, status)` (returns [] unless status == "running" or session holds lock). `hub/lock.py`: `WatcherLock`, `watchers()`.
- `hub/watch.py`: `Watch` (own lock, `poll`, `lines`), `watch()` handler refusing with no running batch (EXIT_PRECONDITION), reasons `EVENTS`, `NO_BATCH`. `--after` past-end refusal (EXIT_USAGE).
- `hub/journal.py`: `config` line (key/old/new/batch), `config_text`, `_slots_line`, `lines()` (merged + batch.slots). `_key`: config -> key with `t`; checks-red; everything else falls to the merged branch (must be fixed: `kind == "merged"` only).
- `board/config_api.py`: `_put` writes `config` lines for the two LIMIT_KEYS only (`_limit_changes`, `_event`, `_open_batch`), through `forge_journal.append(..., "board")`.
- `hub/lines.py` `watch_lines`: running batch only; line `watch: chantier watch --after <n>`.
- `board/seats.py` `SEAT_CHECK_S = 10`; `core/seat.py` `read_seat`; `board/running.py` `live(path)` + `board/key.py` `key_path(repo)` (record has `version`).
- `playbook/edit.py` `config_view(repo)`: `hosts[host]["roles"]` rows with `agent|model|escalation` each carrying `effective` (model: `{id,name}`; escalation from `escalation.row`: `effective` or None when `allowed` false).

Missing (all of it for CR-384):
- No `board` kind, no writer in `board/write_api.py::_answer` (it only calls `board.journal.record`, line ~80).
- Config lines for role keys (`hosts.<host>.roles.<role>.<key>`); `_limit_changes` skips changes with `host`.
- `event_text` branches for `board` and role `config` (it only has checks-red / config / merged; `config_text` returns plain head for non-slots keys: role text needs "; applies at the next batch; for the Chief of Staff: tell the user, act on nothing" and `board` text).
- `wakes` handling in `Watch.poll` (today every new line sets `last_new`); carried non-waking lines printed at the end.
- `--once`, the seat end, no-batch removal, `board is chantier <v>` start-line clause, `board:` line in `status`, `pull path` line + second clause of the `not running` line, `seat take`/`seat get` line.

## Files and entry points

1. `src/hub/journal.py`: module docstring (writers/readers, `board` kind); `_key` (kind-dispatch: board/config unique key, e.g. include `seq`-independent unique token such as `("board", t, uuid)` or include the line's own `seq`... NB: `_key(line)` is computed after `seq` assigned, so keying on `seq` makes every board/config line unique and replaces the `t` trick); add `board_event(action, items, text, wakes)`; `event_text` dispatch on kind; `config_text` for role keys; `waking(e)` helper (merged, checks-red, config, board with wakes true); `lines()` unchanged except `_slots_line` stays. `hub/__init__.py` docstring.
2. `src/hub/watch.py`: remove refusal (lines ~96-100) and `NO_BATCH` reason/`running_batch` import use in `poll` (keep `running_batch` for the name in `lines`); `poll`: only waking new lines set `last_new`; seat check every `SEAT_CHECK_S` of the injected `now` (read `read_seat`, compare to `self.session`, `session == "none"` or no transcript: no check); new reason `SEAT`; `lines(reason)`: for SEAT print events then `watch: the seat of <project> is another session's now; ended`, no restart line; for EVENTS restart line name = batch id or `<project> (no batch)`; start line adds board-version clause (`running.live(key_path(repo))`, `version != __version__`); `--once` branch before `Watch` is built (no locks, no hub, no `running_batch`), printing `event_text` for every line with seq > after plus `watch: cursor <seq>; next, at the user's next message: <cli_command(repo)> watch --once --after <seq>`; `--once` without `--after`: `EXIT_USAGE`. Beware: `watch()` today builds `Watch` which acquires locks; `--once` must not call `elect`.
3. `src/declare/watch.py`: add `--once` (store_true), help text (board writes, seat end). Registered as `NO_BATCH` (registry constant; no batch needed already).
4. `src/hub/autostart.py`: `not_running_line(repo)` drops the status argument; add helper `pull_command(repo, n)` = `f"{cli_command(repo)} watch --once --after {n}"`; second clause `; after the user's no, at each user message: <pull>`. Callers to update (signature): `commands/batch_status.py:317`, `commands/driver.py:93,156`, `commands/opening.py:400`, `commands/orders.py:293`, `commands/seat.py:83`. Check each caller's own status guards: `driver.py` and `orders.py` gate on `reopened`/`kind == "qa"`; `opening.py:400` (also `_empty_lines`, batch born paused) and `seat.py:83` (direct-mode switch) now print for any status.
5. `src/hub/lines.py::watch_lines`: drop the `d.status != "running"` early return except for the `forge hub:` line (running only); this-session line becomes `watch: this session's watcher runs; pull path: <pull>`; add the `board:` version line (new helper, uses `running.live(key_path(repo))`, `__version__`).
6. `src/commands/seat.py`: `_take` (end, line ~148) and `_get` (~100): append `not_running_line(repo)` when `read_seat` transcript, kept as `re.sub(r"[^A-Za-z0-9-]","",...)`, equals `autostart.session_key()` and key != `none`. In `_take` the seat was just written with `own_transcript(detect_host())`, so the comparison is automatic; `_get` must reread. Note `detect_host()` raises ChantierError in a bare terminal (session_key already handles it).
7. `src/board/write_api.py::_answer` (line 70-92): after `journal.record(...)`, `forge_journal.append(repo, [board_event(kind, slugs, words, kind in WAKING)], "board")`. `kind` there is the board journal kind (new/move/edit/label/group/ungroup/next-batch; confirm the exact strings at each `_answer(...)` call: `_new`, `_move`, `_labels`, `_group`, `_ungroup`, `_file`, `_next_batch`). `_rescan` does not go through `_answer` (it builds its own body, line ~251) so it writes none. Circular-import check: `config_api` already imports `hub.journal`, so fine.
8. `src/board/config_api.py::_put` (line 102): generalise `_limit_changes` to all changes: for a role change compute `before`/`after` from `edit.config_view(repo)` (today only `["limits"]` is read before; read `hosts[host]["roles"][role][key]["effective"]` and, for escalation, the row's `effective`) and key `hosts.<host>.roles.<role>.<key>`; one line per changed key, skip equal; `_limit_line` / response lines unchanged; dry run unchanged (inside `if not dry`).
9. Cards (line numbers at this head): `session-start.md:97-105` ("The watcher"); `chief-of-staff.md`: row 33-34 (watcher end, not running), row 48 (rescan), 930 (step 5), 1300-1334 (The watcher; "no running batch" at ~1303/1313, "a paused batch prints no line" ~1313), 1767, 1802-1804 (handing the seat over); `foreman.md:847` (spec said ~772: the watcher mention is at 847 now; no `board:`/`pull path` mention exists yet, add one sentence); `concepts.md:695-696` (spec ~685; rule 8 text "and stops itself"); `hosts/claude-code.md:53-54`; `hosts/copilot.md:46`. Keep outside "Startup core" sections; `test_startup_manifest.py` and `test_watcher_step.py` check card text/budget: run them.
10. Docs: `AGENTS.md:55-75` (board exception ~57-62, third exception 63-75, "one round trip" line 75), `CONTRIBUTING.md:104-125`, `docs/web-board.md:84` and `:165` (rescan button text), `docs/planning-folder.md:49`.

## Existing tests and scenario to extend

- `cli/tests/test_forge_hub.py`: `test_the_board_and_the_hub_share_the_journal_once` (216), `test_a_watcher_ends_twenty_seconds_after_the_last_event` (273; `ENDS` table incl. the `NO_BATCH` case `([],5,5,NO_BATCH)` and the final assertion on the no-batch line must be replaced), `test_a_config_line_ends_the_watcher_and_is_told_in_its_form` (320, `CONFIGS`), `test_watch_refusals` (338; first assertions expect the no-running-batch refusal: remove), `test_status_and_the_start_line_...` (353).
- `cli/tests/test_watcher_autostart.py`: `test_the_outputs_end_with_the_line_when_no_watcher_of_this_session_runs` (130; asserts `last` with `--after 2` exactly and `watch: chantier watch --after 2` -> both change: second clause and `pull path` text), `test_some_outputs_print_no_line` (170; asserts paused `status` and `order add` print no line: paused status now prints it, revise), plus add `seat take`/`seat` setups to `SETUPS`.
- `cli/tests/test_board.py` (line 51 has the `journal` key list; add the parametrized write-route test), `cli/tests/test_board_config.py` (no forge-journal test exists yet; CR-383's config-line test is in test_forge_hub or elsewhere: grep found none in test_board_config, so add the parametrized one), `test_scenario_coverage.py` (README bullets with unit).
- `scenario/run_scenario.py`: `board_writes` (1461), `forge_hub` (1689): `not_running`/`still_running` helpers 1766-1770, check at 1793-1797 (`status` of running batch), 1825 (`watch: chantier watch --after` line), 1846-1848, the no-batch end check 1912-1921 (`got[-1] == "watch: no running batch in demo; ended"`) and the `status` paused-has-no-`watch:` check 1922-1923, `sw.chantier("watch", expect=2)` check 1932-1934, and the seat-take line check ~2651. `scenario/README.md` 222, 300-322 bullets (update with units).

## Smallest change

One writer helper (`board_event`) + `_key` fix; one `append` call in `_answer`; generalise `_put`; `Watch` gains `waking` filter, seat check and SEAT reason; `--once` as an early branch of `watch()`; `not_running_line` loses its argument; two small output lines; cards/docs. No new module is needed except perhaps a tiny helper for the board-version line (put it in `hub/lines.py`).

## Risks

- `_key` for `board`/`config`: keying on the assigned `seq` is simplest (unique per append); the old `t` key is replaced as the spec says. A `merged` line by hub vs board keep `("merged", batch, cr, landed)`; checks `test_the_board_and_the_hub_share_the_journal_once` still passes.
- Existing journal lines with a kind other than the three now: none; `_key` must keep a fallback only for `merged`.
- `Watch.poll` seat check on an injected clock: the 10 s interval uses `now` from the poll argument (tests have no sleep); first check at the first poll or after 10 s? Spec says "about every 10 s": decide first check at t=0 would make a test seat set before the watcher start end at once, which is desired; the scenario's `seat take` by another session has the seat written after start.
- `seat.json` `transcript` comparison needs the same sanitising as `session_key`; a seat whose `transcript` is None or watcher key `none`: no end. Session key from `own_transcript(detect_host())` reads the environment (`CLAUDE_CODE_SESSION_ID`); in the scenario the watcher is a subprocess, set the env var per process.
- Role `effective` values are dicts (`{id,name}`) for models: the `old`/`new` in the line must be a printable value (spec says "the effective of config_view's row"): decide to write the id (string) or the dict; text uses `<old> -> <new>`, so a dict prints ugly. Suggest the id (name when no id) for model/escalation and the agent's `effective` as is; record in the PR. This is a means, not a behaviour; `inherited` for None.
- The `--once` path must not take `WatcherLock` (`Watch.__init__` creates `HubLock`/`WatcherLock` objects; constructing is harmless, but `elect` must not run) so build a separate function.
- `not_running_line` now prints for a born-paused `open`: `test_open_empty_batch.py` and `test_factory.py`, `test_mode_switch.py`, `test_batch_end.py` may assert exact outputs: run them. The ten-line `cli.cut` keeps the watcher line last (`test_the_ten_line_cut...`), unchanged.
- `status` of a paused batch prints the line; Foreman reads `status` as heartbeat: card line in `foreman.md` tells it to ignore.
- Windows: sleep-free tests; the scenario's seat-end check spawns processes (fine locally at the gate).
- Spec reference check: values searched for old numbers: none (no size change).

## Questions only the user can answer

None. One means to confirm (Chief of Staff, per spec): format of role `old`/`new` (id string vs `{id,name}` dict).

## Evidence plan

Kind: CLI behaviour plus cards/docs change; no UI change (nothing under `board/web/`, no pane): no screenshot, no `DESIGN.md`, no `just mod`.

- Before/after: command outputs, captured in `evidence/`:
  1. `forge-journal.jsonl` content after a board move, new idea, edit, label (a `board` line with `wakes` false for label), a refused move (no line), a model change via PUT /config (role `config` line), a dry run (none); technique: the scenario's `board_writes` leg (real board, real HTTP), plus the in-process unit tests; the log from `just scenario` (unit surface-board) quoted.
  2. `chantier watch` run with a paused batch / no batch: start line, a board move, the end with `board wrote (move)` and the `still running` line (`<project> (no batch)`); `--once --after n` output with the cursor line; `seat take` by another `CLAUDE_CODE_SESSION_ID` ending a watcher with the seat line; technique: `forge_hub` scenario leg with `CHANTIER_HUB_TEST_TIMES=1:4`; before-state is main's refusal `watch: no running batch in <project>: nothing to watch` (show once from the main checkout or from the removed check text).
  3. `status` of a paused batch, `seat take` and `seat` outputs showing the `watch: not running` line with the `after the user's no` clause, and the `pull path` line, the `board:` version line with a fake live board record of another version (unit test seeds `board.json`).
  4. Gates: `just check`, `just eval-dry-run` in the worktree at the rebased head; unit tests listed above; pipeline `just scenario (ubuntu-latest)`; local `just scenario` on Windows via `chantier gate` if CR-384 is the top.
- Cannot be shown: the real main session's wake by a background watcher's end, and whether Claude Code ends an orphaned watcher when its session ends; Copilot's wake. These stay in the PR's Known gaps (the two sentences of the specification) and as host-row trials after merge.
