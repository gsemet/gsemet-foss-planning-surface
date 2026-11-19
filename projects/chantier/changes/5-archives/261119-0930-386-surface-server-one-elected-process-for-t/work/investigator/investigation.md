# CR-386 investigation (first take, worktree at the CR-385 head f9fb169c)

`C/` = `skills/chantier/scripts/cli/src/chantier/`, `T/` = `skills/chantier/scripts/cli/tests/`.

## 1. Where the spec's names do not match the code

| Spec says | Code has |
|---|---|
| `commands/batch_status.py` `_hub_line` (sections 1, 4) | `hub/lines.py` `hub_line` (and `board_lines`, `watch_lines`). `batch_status.py` only imports `watch_lines`. The edit goes in `hub/lines.py`. |
| CR-384's two readers of the board's version "in `hub/watch.py`" | They are `hub/autostart.py` `board_clause` (calls `running.live(key_path(repo))`), used by `watch.py` `start_line` and `lines.py` `board_lines`. `autostart.py` imports `board.running` and `board.key`: that import moves to the new state module. |
| `hub/lock.py` "RECORD and record functions" | `live`, `start_record`, `write`, `remove`, `other_version`, `_read`, `_epoch`, `RECORD`. `HubLock`, `WatcherLock`, `watchers` stay. `running.py` has its own duplicate `_epoch`/`_read_file`: merge. |
| `board/running.py` "record functions" | `write`, `remove`, `live`, `_store`. `stop_command` and `find_pid` are not state; they stay (used by `command.py` and tests). |
| `Hub.cycle` "a failed hub-entry write is retried at the next cycle" | `Hub.__init__`, `Hub.cycle` call `lock.write` unguarded and `Hub.close` calls `lock.remove`. Answer 17 needs a guard on all three. |
| scenario lines 1695, 1809, 1988, 2200, 2208 | now `run_scenario.py` 1712 (`hub_json` var), 1825 and 1838 (check text), 2082-2083 (key check), 2294 and 2302 (`board.json` record checks). Also `scenario/README.md` 287, 313, 347. |
| `chief-of-staff.md` about 1061-1065 | the "hub (or the board)" line is at 1130. |
| `foreman.md` about 772 | the `forge hub:` text is at 794. |
| CONTRIBUTING.md 85-120 | the git-folder sentence is at line 89. |
| `board/context.py` reads `key` | `context.py` only holds a `KeyFile`; the path is built in `board/command.py` `_run`. Four test files build `KeyFile(key_path(...))` (`test_board_config.py:46`, `test_board_journal.py:42`, `test_board_prs.py:19,57`, `test_board_running.py`): keep `key_path` exported from `board.key`, or edit them. |
| Test names in the Tests section | all exist (`test_forge_hub.py:123, 200, 307`; `test_board_running.py:69, 115`). Not named by the spec but also using the old files/functions: `test_watcher_autostart.py:221`, `test_watch_events.py`, `test_forge_hub.py:253, 264, 349, 352`. |

## 2. Files and entry points

- `board/key.py`: `key_path` -> `board.json`; `read_key`, `load_or_create` (merges `kept` on `--new-key`), `KeyFile.current` (re-reads on mtime/size change; returns `""` when `read_key` raises).
- `board/running.py`: `write`, `remove(path, pid)`, `live` (`procs.alive_since(..., unreadable=True)`), `stop_command`, `find_pid`.
- `board/command.py`: `board()` order today: `load_or_create` -> `running.live` -> `_recorded` / `_answering` -> `_bind` -> `running.write` -> print lines -> `_run` (Context, `make_server`, `seats.arm`, uvicorn run, `finally: sock.close(); running.remove`). Tests stub `command._run`, so the hub thread must start INSIDE `_run`, not in `board()`.
- `hub/lock.py`: `HubLock` (`try_lock`, never waits) and the `hub.json` record functions.
- `hub/cycle.py`: `Hub` (record, `due`, `projects`, `cycle`, `close`); seam `forge_read.read`; events via `journal.append(repo, ..., "hub")`.
- `hub/watch.py`: `Watch.elect`, `start_line`, `poll`, `close`.
- `hub/autostart.py` `board_clause`; `hub/lines.py`; `hub/times.py` `cycle_s`, `poll_s`.
- `core/files.py`: `try_lock`, `unlock`, `write_json` (atomic replace, retried on Windows), `read_text` (retried on PermissionError).
- Journal writers already go through `hub/journal.py` `append` with source `board` (`board/prs.py:297`, `board/config_api.py:147`, `board/write_api.py:83`) and `hub` (`cycle.py`): nothing to change there. `changes_lock` takes its own handle, so it already serializes threads.

## 3. Smallest change

1. New module `hub/state.py`: `path(git_dir)`; `read`; `live_entry(git_dir, name)` (the `alive_since` check, one `_epoch`); `update(git_dir, name, value_or_None, only_pid=None)` which takes `server.json.lock` with `try_lock` retried for 1 s, reads, changes one entry, replaces atomically, chmod 0600, and raises one error type on `OSError` or lock timeout; `migrate(git_dir)` (key/created + `running` -> `server` in one write, delete `board.json`); the first hub writer deletes `hub.json`. `board/key.py` keeps `key_path` as an alias of `state.path` (saves editing 5 test files). `running.py` loses `write/remove/live` (callers use `state`), keeps `stop_command`, `find_pid`.
2. `hub/lock.py`: drop `RECORD`, `live`, `start_record`, `write`, `remove`; keep `other_version`. `Hub` writes through `state.update(git_dir, "hub", ...)`, swallowing a failure and setting a "dirty" flag so the next cycle writes it again (also in `__init__`). `Hub.close` removes the entry with `only_pid`.
3. `hub/watch.py`: `elect` tries the hub lock only when `state.live_entry(git_dir, "server")` is None; in `poll`, after the cycle, a hub watcher that sees a live server calls `hub.close()`, `lock.release()`, `hub = None`. The same gate makes it elect again once the server entry is dead (answer 16). `start_line`/`board_clause` read versions from `state`. `--once` untouched.
4. `board/command.py`: `board()` calls `migrate` then `load_or_create`; any state write failure -> `_not_started(f"{path}: {reason}")`; `_run` starts the hub thread after `make_server`, and its `finally` stops the thread (releases the lock) then removes the `hub` and `server` entries by PID.
5. New `HubLoop` (in `hub/cycle.py` or `hub/loop.py`): `poll(now)` = try the lock if not held, create a `Hub`, `cycle` when `due`; `run()` = daemon thread calling `poll(time.monotonic())` every `hub_times.poll_s()`; `stop()`. `poll(now)` is the fake-clock seam for the spec's thread test, as `Watch.poll` is.
6. `hub/lines.py` `hub_line`: compare the `hub` entry's PID with the live `server` entry's PID -> `the surface server` / `a watcher`.
7. Docs and cards as spec section 5. AGENTS.md lines 24-25 (git folder clause), ~64-80 (three named exceptions -> two), the "two named git exceptions" line; CONTRIBUTING.md ~89 and the exceptions text; `docs/web-board.md` 172-177; docstrings of `hub/__init__.py`, `hub/lock.py`, `board/__init__.py`, `board/running.py`; `session-start.md` "The board" and "The watcher"; check `chief-of-staff.md:1130` and `foreman.md:794`.
8. Tests as the spec lists; scenario: `forge_hub` (16d, ~1712-1900) and the surface-board unit (~2082, 2294, 2302), plus the spec's steps 1-7; `scenario/README.md` 287, 313, 347 (keeps `test_scenario_coverage.py` green).

## 4. Risks

- **R1 Windows read race on a file now rewritten each hub cycle** (20 s; 0.5-1 s in the scenario). `read_text` retries PermissionError for 1 s, but a state reader that turns an error into `{}` reads "no server" (a watcher elects, a second `board` starts instead of attaching), and `KeyFile.current` returns `""` (the request is refused as keyless) during a replace. Mitigation: `KeyFile` keeps the last good key on a transient failure; `state.read` tells "missing" from "unreadable".
- **R2 Election gated on `server.json`.** A server alive but whose hub thread died leaves no hub, and watchers never elect. Default per "no fallback": a crashed hub thread stops the server with a stderr line. Not a user question unless the author wants otherwise.
- **R3 "Refuse before the socket is bound"** (answer 17): today `running.write` runs after `_bind`, because the port is only known then. The spec needs the refusal with nothing bound, so a pre-bind write check (migration write, or a lock probe on `server.json.lock`) is needed, then the real `server` entry after bind. The spec test ("write lock held, prepared as such") checks exactly that.
- **R4 One process in tests.** The server-thread test and a `Watch` share the test's PID, so `alive_since` is true for both; tests must monkeypatch `procs.alive_since` or set pid/started explicitly (existing tests do).
- **R5 Upgrade:** an older watcher-hub writing `hub.json` is out of scope; the scenario's "git folder holds only ..." check must not run while one lingers.
- **R6 Old names.** `board.json` / `hub.json` appear in 12 files (AGENTS, CONTRIBUTING, docs/web-board, scenario README + run_scenario, key.py, running.py, cycle.py, lock.py, 3 tests); none in the cards. The scenario's `record()` helper and `hub_json` read the old top-level shape (`pid`, `projects`): they become `["hub"]["pid"]`, `["hub"]["projects"]`.
- **R7** `test_scenario_coverage.py`: new README bullets must name their tests.
- **R8** `just test` budget (+30 s): the thread test uses the fake clock, no real sleep or thread.

## 5. Questions only the user can answer

None.

## 6. Evidence plan

Kind: CLI behaviour (state file, election) plus card and doc text. No UI, no pane, no screenshot.
- Before/after: listing of the git folder's `chantier/` (before `board.json`, `hub.json`, `hub.lock`; after `server.json`, `server.json.lock`, `hub.lock`), `server.json` with the key redacted, and `status`'s `forge hub:` line (`PID n, last read t` -> `PID n, the surface server, last read t` or `a watcher`).
- Technique: `just scenario` units surface-board and 16d (fake `gh`, `CHANTIER_HUB_TEST_TIMES`), output saved in `evidence/`; `just test`; `just check`; `just eval-dry-run`.
- Real run on the user's Windows machine (answer 9): the four commands including `taskkill /PID <n> /T /F` and the watcher taking over; pasted in the PR's Deliverables.
- Cannot be shown here: the Windows lock and replace behaviour in the pipeline (Linux only) and a real forge merge wake; the local `chantier gate` and the real run cover them. No `just mod`, no `DESIGN.md`.
