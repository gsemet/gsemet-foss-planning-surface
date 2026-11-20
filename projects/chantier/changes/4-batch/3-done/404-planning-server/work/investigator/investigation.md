# Investigation: CR-404, the surface's writer (Part C)
Map at head `97ffe81d` (Parts A, B in). Paths are under
`skills/chantier/scripts/cli/src/chantier/` (`SRC`) and `skills/chantier/scripts/cli/tests/`
(`T`) unless they start with `docs/`, `scenario/`, `scripts/` or `skills/`. Project rules read
(`$CHANTIER rules`): AGENTS.md, CONTRIBUTING.md, the surface's AGENTS.md; the ones that bind this
CR are in AGENTS.md (write list, git exceptions, `just check`/`eval-dry-run`/`scenario`, board
`DESIGN.md`, "no fallback", agents hand-written) and are changed by the spec itself (C.11).

## 0. What Parts A and B left
- `store/`: `base.py` already declares `REFUSES_WITHOUT_PUBLISHER` (in `FEATURES`) and `PlanStore`
  has `check_publish(rels, *, config, command)`. `FolderStore.check_publish` only checks paths
  stay inside the folder. `SurfaceStore(changes, project)` (`store/surface.py`, 28 lines) has
  `features = {PUBLISHES, LOCAL_FILES}` and NO refusal yet and NO git dir.
  `Repo.store` (`core/repo.py` L225-233) builds it; `Repo.check_publish` (L235-240) passes
  `command=self.command or COMMAND`. Every published write already calls `check_publish` before
  it changes anything (see `grep check_publish`: `crs.py`, `driver.py`, `intake.py`, `joining.py`,
  `orders_apply.py`, `summary.py`, `core/batch.py`, `lifecycle/*`, `close_archive.py`,
  `playbook/edit.py` L366 with `config=True`, `summaries/edit.py`). Nothing to add at call sites.
- `hub/schemas.py`: `PUBLISHED` has `merged@1`, `checks-red@1`, `config@1`, `board@1`; `Entry(model,
  wakes, text, key, example)`; `hub/schemas.json` shipped; recipe `just journal-schemas`
  (`scripts/journal_schemas.py`). `hub/journal.py`: `SOURCES = ("hub","board","cli")` (L47),
  `append(repo, events, source)` takes `changes_lock(repo)` (L251), `waking` (L196),
  `event_text` (L281), `lines()` (L306) prints only `merged@1` and the newest `batch.slots`
  `config@1`: there is no generic "show this type" path, so the writer lines of `status` are new
  code.
- `hub/loop.py` (`HubLoop.poll(now)` / `HubThread`, daemon thread, `on_death` = server stop),
  `hub/lock.py` (`_FileLock`, `HubLock`: `try_lock` never waited on; folder `<git dir>/chantier/`),
  `hub/times.py` (constants + one env var, `_test()`), `hub/state.py` (`SERVER`, `HUB` names,
  `modify`, `write_hub`, `remove_entry`, `live_entry`, `other_version`).
  The writer copies these shapes; do not extend them except as listed below.

## 1. Round 1: writer package, `core/git.py`, `hub/state.py`, store refusal, schemas, tests

### Files and entry points
| File | Change |
| --- | --- |
| `core/git.py` L12-34 (`git`) | add keywords `env: dict[str,str] \| None`, `input: str \| None`, `raw: bool = False`. `env` merged over the built env (`{**os.environ, GIT_EDITOR..., **env}`); `input` -> `subprocess.run(input=...)`; `raw` returns `p.stdout` unstripped. `check=False` callers unchanged. Add a helper that returns `(returncode, stdout, stderr)`: the writer needs git's message on failure for `failure.text` and the network-failure test, and `git()` raises `ChantierError("git <args>: <stderr>")` (exit 3, `EXIT_EXTERNAL`) which is parseable, but the stdout of a failed rebase (`CONFLICT ...` lines) is lost. Smallest: keep `git()`, strip the `git <args>: ` prefix as `refusal()` does (L48-54), and for the conflict file list run `git diff --name-only --diff-filter=U` (read) before `rebase --abort`. |
| `hub/state.py` | `WRITER = "writer"`; `write_writer(git_dir, record)` (as `write_hub`, no `hub.json` cleanup); docstring paragraph for the entry. `live_entry` already generic (checks `pid`+`started` via `procs.alive_since`; the SERVER-only port check stays). `remove_entry(git_dir, WRITER, pid)` exists. |
| `hub/lock.py` | add `WRITER_LOCK = "writer.lock"`, `class WriterLock(_FileLock)` (6 lines; `acquire()/release()/held`). Also the wake file `writer.wake`: put the path helper here (`wake_path(git_dir)`) so the CLI (`sync now`) and the board button import it without importing the writer package. |
| `hub/journal.py` | `SOURCES += "writer"` (L47); docstring L1-30 ("four published types", "writes ... the forge hub, the board") updated; `hub/schemas.py`: four models `SyncConflict1(upstream: Sha, local: Sha, files: list[str], projects: list[str])`, `SyncBlocked1(reason: str, text: str)`, `SyncLate1(since: str, paths: int, ahead: int)`, `SyncResumed1(after: str)`, four texts (C.10 wording), `wakes` True/True/True/False, key `None` (each line its own: two conflicts with the same shas in two episodes must both be told; say it in the docstring), examples; then `just journal-schemas` adds the four entries to `hub/schemas.json` (never edit by hand; the file must stay canonical, LF). `test_event_types.py` loops `PUBLISHED`, so the new entries are exercised by its parametrized tests (check its duplicate-rule expectations for `key=None`, as `config@1`). `Sha` pattern requires 40/64 hex: use real `rev-parse` output. |
| NEW `writer/__init__.py` | docstring: the package's one-paragraph contract. |
| NEW `writer/times.py` | `EVERY_S=30, QUIET_S=10, MAX_WAIT_S=120, FETCH_EVERY_S=60, LATE_S=300`, `TEST_ENV="CHANTIER_WRITER_TEST_TIMES"` `every:quiet:max_wait:fetch_every:late` parsed like `hub/times._test` (all five > 0 else None); accessors; `POLL_S = 1.0` (wake-file look), `FINAL_S=30`. |
| NEW `writer/record.py` | the `writer` entry: build (`pid, version, started, state, reason, text(<=200), since, last_cycle, pending, pending_since, ahead, unpushed_since, last_commit, last_push, last_fetch, conflict, failure`), `publish()` (suppress `OSError`/`StateError` as `Hub.publish`), `read(git_dir)` for readers (returns `{"state":"off"}` when no live entry), state words as constants. |
| NEW `writer/paths.py` | pathspec: `projects`, `chantier.yaml`, `chantier.yml` + one `:(exclude)<surface-relative path>` per project: use `Repo._external(root, str(root/"projects"/name))` (as `hub/cycle.py::Hub.projects` does) and read `repo.clone_dir` / `repo.worktrees_dir` (set in `Repo._external` L141-153 from `read_keyed(checkout.yml)` with `.repo`/`.worktrees` defaults) -> never re-implement the defaults. Keep only those inside `surface_root` (`is_relative_to`, after `resolve()`); forward slashes. `surface_projects(root)` (core/repo) lists the project names. Porcelain parse (`-z`, raw), nested repo detection (untracked entry ending `/`, or mode 160000 via `git ls-files -s` of the pathspec), fingerprint (paths + size + mtime). |
| NEW `writer/git_ops.py` | every git call through `core.git.git` with `env={"LC_ALL":"C","LANGUAGE":"C"}` (a test asserts each call receives them: route all through one `_run()`), `raw=True` for `status -z`; `status`, `add -A -- <spec>`, `commit -m --pathspec-from-file=- --pathspec-file-nul` (input = NUL-joined paths), `fetch <remote> <branch>`, `merge --ff-only --autostash`, `rebase --autostash`, `rebase --abort`, `push <remote> HEAD:<branch>` (never `-f`, never `--no-verify`), reads (`rev-list --count`, `rev-parse`, `diff --name-only --diff-filter=U`, `stash list`, `git rev-parse --git-path` for `rebase-merge`/`rebase-apply`/`MERGE_HEAD`/`CHERRY_PICK_HEAD`/`REVERT_HEAD` busy check, `merge-base --is-ancestor`). Branch/upstream: `default_branch(root)` (core/git L37) reads `origin/HEAD`; upstream via `rev-parse --abbrev-ref @{u}` (fails -> `no-upstream`). Network-failure classifier (list in C.5; LFS texts set by the LFS test). The staged-by-hand rule: `diff --cached --name-only -z` minus the writer's own paths. |
| NEW `writer/cycle.py` | `Writer` (like `hub/cycle.py::Hub`): `due(now)`, `cycle(now, final=False)` = steps 1-8; holds per-project `Repo`s; commits under `changes_lock` per project in sorted order (`lifecycle.stages.changes_lock(repo)` = `repo.store.lock()`, which also `mkdir`s the changes folder and writes its `.gitignore` via `ensure_gitignore`: acceptable but note a project with no `changes/` gets one created); releases the locks BEFORE `journal.append(repo, [...], "writer")` (append takes the same lock, non-reentrant on Windows/POSIX). Episode bookkeeping: `failure{step,text,cycles}`, once-per-episode flags (`blocked`, `late`), `staged` seen-twice memory, the `conflict` state resume test (step 1), the Q30 stash exception (`git stash list` before/after the integrate; the stash is new when the count grows). |
| NEW `writer/loop.py` | `WriterLoop(repo, version)`: `lock = WriterLock(repo.git_dir)`, `poll(now)` (acquire, build `Writer`, write the entry, cycle when `due(now)` or `writer.wake` mtime > last cycle start), `stop()` = final cycle limited to 30 s then `remove_entry(WRITER)` and `release()`; `WriterThread` copies `HubThread` (join 5 s is too short for a 30 s final cycle: `JOIN_S` must be `FINAL_S + 5`; `HubThread.stop` is called in `board/command.py::_run` `finally`, order: writer.stop BEFORE `state.remove_entry(SERVER)`, which is already the order there). `on_death`: a dead writer thread should print `board: the writer stopped: ...` and NOT stop the server? Spec silent: the HubThread ends the server on death; for the writer, "no writer, no write" is already enforced by the CLI, so keep the server serving and leave the entry removed (to confirm with the Driver; low risk). |
| `store/surface.py` | `SurfaceStore.__init__(changes, project, git_dir)`; `features |= {REFUSES_WITHOUT_PUBLISHER}`; `check_publish` first runs the parent's path check, then: if any `rel` is `published(rel)` (use `is_published`) or `config=True`, and `state.live_entry(git_dir, WRITER)` is None -> `ChantierError(C.8 text, EXIT_PRECONDITION)`. Older-board variant: `live_entry(SERVER)` with `other_version(...)` -> text with `running.stop_command(pid)`. `Repo.store` (core/repo.py L225-233) passes `self.git_dir`. Import cost: `chantier.board.running` has no heavy import, but `chantier.board/__init__` must be checked for imports (cycle: `hub.journal` -> `core.repo` -> `store` -> `hub.state`: `hub/state.py` imports only `procs`, `core.clock`, `core.files`; OK). One `live_entry` per `check_publish` call (psutil is ~ms, 10x on Windows): do not call per path. The command name in the text is the `command` argument (`Repo.check_publish` passes it). The "writer: <state>: not pushed yet" extra output line (C.8) is added by the commands' output, not the store: smallest is one helper `writer_note(repo) -> list[str]` in `writer/lines.py` appended in `cli.py`'s result path for external mode when the command did a published write; simplest honest rule: append in `cli.py` after any command whose store recorded a publish (the store sets a flag `published_something` on `Repo`/store when `check_publish` passes a published path). Decide; the spec only says "the command's output adds one line". |
| `core/repo.py` | `SurfaceStore(...)` call; nothing else. |

### Existing tests that break in round 1 (and the one fix)
Every test that writes a published path on an external surface now exits 2. The
`surface` fixture (`T/conftest.py` L111-150, copy of a template per test) and
`enter_state`/`build_states` in `T/store_spy.py` L141-180 (builds `backlog`/`batch` states by
running real commands, session-wide, under `build_states`) are the choke points. Add in ONE
place a helper `live_writer(git_dir)` (`T/conftest.py`: `state.modify` writing a `writer` entry
with `pid=os.getpid()`, `started=clock.now()`, `state:"synced"`) and call it from the `surface`
fixture, from `build_states._build` (before `_run`) and `enter_state` (the copied `.git/chantier/
server.json` carries the entry, but check: `copytree` of the state keeps it, whose pid is the
session's pid, alive; OK for a single worker, but with xdist `-n auto` the building worker's
pid differs from the test worker's: write the entry in `enter_state` again). `forge_world.py`
(`World(surface, ...)`) uses the same `surface`. Files that use a surface and may write: see
`grep -l "surface"` list: `test_board*`, `test_forge_hub`, `test_limits*`, `test_playbook_*`,
`test_summary_lint`, `test_surface_batches`, `test_surface_server`, `test_validate`,
`test_watcher_autostart`, `test_external_archive`, `test_open_no_clone`, `test_event_audience`,
`test_cli_runs`. Do not edit them one by one: fixture only. Also `test_store_conformance.py`
fixture `store`: `SurfaceStore(project/"changes", project)` gets `git_dir=tmp/"surface"/".git"`
(a folder is enough: `live_entry` reads `server.json` there; no git needed) and the existing
`test_refuses_without_publisher` (L198-205, needs the feature) then runs on `surface`; add the
"with a live writer entry both return" assertion (spec §6) and keep `test_check_publish_returns`
(L190-195: `check_publish(["3-ready/x/01-intent.md"...])` on a surface with no writer now
raises: it must run on the folder store only, or with the entry prepared; adjust it, spec §6
already says conformance runs both ways). `test_store_command_table.py` L29 imports
`autosync_tool` (removed in round 2) and L157 monkeypatches it: delete those two lines then.
`test_store_command_table` also needs the writer entry (via `world`/`enter_state`).

### New tests of round 1
`T/test_writer_cycle.py` (spec §6 list, one bare origin per module, `poll(now)` with explicit
floats, times via `monkeypatch.setenv("CHANTIER_WRITER_TEST_TIMES", ...)`). Reuse
`conftest.surface_template` (has `.repo` as a git repo, `checkout.yml` worktrees `../../../wt`)
for the nested-repo exclusion case, plus project `b`/`c` built in the test. Needs: a bare origin
(`git init --bare`), `git remote add origin`, `git push -u`, `origin/HEAD` set
(`git remote set-head origin -a` or `git symbolic-ref refs/remotes/origin/HEAD`), a second clone.
Hooks: write `.git/hooks/pre-commit` (a `sh` script: Git for Windows runs it through its sh, fine
on all three OSes). Offline: rename the origin folder away (Windows can refuse a rename of a
folder a git process holds: no process holds it between cycles). LFS case: skip unless
`git lfs version` works; records git-lfs's message that sets the classifier's LFS texts.
`T/test_writer_lines.py`, extension of `test_event_types.py` (automatic), extension of
`test_store_conformance.py`, `T/test_surface_writes.py` (command table of Part B:
`test_store_command_table.py::ROWS` is the existing parametrized table: reuse its `Row`s and
`_prepare`, running with no writer entry; this overlaps the table's own run: keep one
parametrization, two fixtures).

### Round 1 risks
1. The writer must hold `changes_lock` of EVERY project in sorted order while it runs `git add`/
   `commit`/`rebase`; a CLI write in another process waits up to 30 s (`LOCK_WAIT_S`). A slow
   user hook or a rebase of a big tree blocks all CLI writes: by design (spec C.5), but test
   with a sleeping hook shorter than 30 s only.
2. `git status -z --untracked-files=all` of `projects/` on a big surface with the code clones
   inside it (default `.repo`) is slow only if not excluded; the exclude covers it. A `.repo`
   that is NOT inside the surface (the usual `checkout.yml`) needs no exclude.
3. Windows: a rebase over a file open in another process fails -> `git-error` (no retry loop);
   mtime resolution used by the fingerprint; `index.lock` race with the user's IDE.
4. `rebase --abort` after a conflict: confirm `git status` shows `rebase-merge` absent; and with
   `--autostash` a conflict leaves the stash applied back by `--abort` (git does). Test it.
5. `hub/state.modify` takes a 1 s write lock: the writer writes its entry every cycle (30 s)
   plus on each state change; fine. `last_cycle` is written EVERY cycle (spec) so `sync now`
   can wait on it: with 30 s cycles the file is rewritten twice a minute, not an issue.
6. `procs.alive_since(pid, started)` uses `clock.now()` at second precision against psutil
   `create_time`: fine for a real process; in tests `os.getpid()` is older than `started`.
   But `board --clock <fixed>` (docs screenshots, scenario `--clock`) makes `clock.now()` a
   fixed past time -> `started` before the process start -> the entry is "not live"
   (`create_time <= recorded + CLOCK_MARGIN_S` false). The hub entry already suffers the same
   in `write_hub`/`hub_record` (they use `clock.now()`); the screenshots run passes `--clock`
   (`scripts/docs_screenshots.py` L100-ish, `CLOCK`). Check `procs.CLOCK_MARGIN_S` and how the
   existing `server` entry copes; the writer must stamp `started` the same way as `write_server`.
   This is the likeliest surprise in round 3's screenshots.
7. `append` dedupes by `_key`; `key=None` keeps each line. Shared `server.json`: key `writer` must survive `state.migrate`/`write_server` (they only
   `__setitem__` their own entry: verified).

## 2. Round 2: commands, status, seat, P13, board start lines, removals, cards, AGENTS.md

### Files and entry points
| File | Change |
| --- | --- |
| NEW `declare/sync.py` + `cli.py` L13-32 import and L68 module tuple | `sync` (NO_BATCH), optional positional `now`. Handler NEW `commands/sync.py`: in-project -> `sync: in-project planning folder: chantier commits nothing` (exit 0); `sync` prints the state line + one line per conflicted file; `sync now` touches `writer.wake`, polls the entry's `last_cycle` for up to 10 s (this is a CLI process sleeping: allowed in product code; the Investigator no-sleep rule is about me), prints the line; no writer -> the C.8 error, exit 2. Add `sync` to `cli.py` `FULL_OUTPUT` (L38-55) if it can print > 10 lines (conflict lists). `validate` is the closest model (`declare/validate.py`). `commands/permissions.py` lists the commands agents run for P10 (`CAPABILITIES`): check whether `sync` must be listed (hosts/claude-code.md table is compared by a test; adding a command only matters if a card makes an agent run it: chief-of-staff.md will, via `$CHANTIER`, which is already allowed as a prefix; verify with `test_plugin_files`). |
| NEW `writer/lines.py` | all C.10 texts: `state_line(entry, other_board=None)`, `p13_lines`, `refusal(command, git_dir)` (shared with `store/surface.py`: put the pure text builders in `store`-importable module to avoid `store -> writer -> core.repo` cycles: `writer/lines.py` must import only `hub.state`, `board.running`, `core.clock`). Times `HH:MM` local like status (`datetime.fromtimestamp(...)` as `autosync/lines.py::_synced` does; read other `HH:MM` helpers in `status/`). `<session id>` in the start command: the card's placeholder is literal in the texts (`$CHANTIER board --seat <session id>`); `$CHANTIER` is also a literal in text the card tells the agent to read. |
| `commands/batch_status.py` L282-287 (`_autosync_lines`) and L306 | replace by `_writer_lines(repo)`: external only; one line right after `_batch_line`; imports L8-10 go. `status --refresh --epoch` shares `status()`. Plus the writer's journal lines "while their episode lasts": a function in `hub/lines.py` (`watch_lines`) or `journal.py`: newest `sync-conflict@1`/`sync-blocked@1`/`sync-late@1` of the project whose episode is the entry's current one (state `conflict`/`blocked`, or late flag): compare the line's `t` >= entry `since`. |
| `commands/seat.py` `_get` (L~95-103) and `_take` (L~137-150) | external mode: append the `writer:` line after the seat's lines (`_own_watch_line` is the neighbour). Note `commands/seat.py::seat` calls `Repo.find()`. |
| `commands/preflight.py` L11-13 imports, L215-222 `_check_autosync`, L232 call | P13 becomes `_check_writer(r, repo)` external only: `P13 ok ...` / `P13 warn ...`; the two extra warns read the surface's rules via `plugin_files.surface_instructions(repo)` (as `autosync/site.py::find_site` does: it reads `rules` with `read_text(errors="replace")`): mention of `.agents/guidelines/autosync.guidelines.md`, and `git pull` / `git push` text (case/regex: plain substring per spec, "the text `git pull` or `git push`"). Also the `foreign-autosync` check lives in the writer (cycle step 2) and P13 shows the `blocked (foreign-autosync)` line through the entry. Report size: `_Report` P10 comment says "the report stays within ten lines" (preflight is in `FULL_OUTPUT`); P13 can now print up to 3 lines: check `test_cli_runs`/preflight tests for a line count. |
| `autosync/` | KEEP `records.py` (`read_group`, `Control.on`, `Watcher.pid`) and `site.py` (state dir constant, `GUIDELINES` for P13's mention test); DELETE `lines.py`, `view.py` (names, `classify`), `reading.py` (`names_of`, `read_view`; `_sessions`). New in the writer: `foreign_running(git_dir) = control.on and watcher.pid alive` (`procs.alive`), reading `read_group(git_dir/"ai-autosync")`. `find_site` is only needed for the guideline mention: reduce or inline (`site.py` L28-47 reads `surface_instructions`). |
| DELETE `board/autosync_api.py`, `board/autosync_tool.py` | and `board/routes.py` L11 import, L78 key `"autosync"` -> `"writer": writer_api.payload(ctx)`, L167 `*autosync_api.ROUTES`. NEW `board/writer_api.py`: `payload(ctx)` = `writer.record.read(git_dir)` (home repo's `git_dir`), route `POST /api/writer/sync` (touch `writer.wake`; `{ok, writer}`); with no live writer answer 409 with C.8's text (use the refusal builder). `board/context.py`: `LastPush` (L26-41, "the tool records none") only served autosync: DELETE it and `Context.last_push` (L58). The write routes' 409 for "writer not started" comes free: `write_api.STATUS` maps `EXIT_PRECONDITION` to 409 (`write_api.py` L37). Config saves go through `playbook/edit.py` (`check_publish([], config=True)`): same path. Check `board/config_api.py` handles the refusal as a 409 too (it has its own try/except at L58 area). |
| `board/command.py` | `_run` (L~98-115): beside `HubThread(HubLoop(projects.home), stop)` start `WriterThread` only when `projects.home.external` (spec C.1: "only when the folder served is an external planning surface"; `projects.surface_mode` is the board's own flag); on a lock held by another process: do not fail the server, print `board: writer not started: <reason>`; stop order: writer first. `board()` L196-226 returns `[]` after `_run` and prints via `_announce`: the "one more start line" is printed there (`writer: <state line>` or `board: writer not started: <reason>`). The writer's first cycle is asynchronous: print the line AFTER the lock is taken and the entry written (synchronously `loop.poll(now)` once before `_announce`'s extra line, or print "writer: syncing"/state read back). `_another_version` / `_silent` already name an older board for the refusal text (`running.stop_command`). The `board --seat` registration path (L205-215) starts no writer, correct. |
| `hub/lines.py::board_lines` | untouched, but its sentence "its writes do not reach the watcher" is about another version; keep. |
| `AGENTS.md` (chantier) | the seven edits of C.11 "Project rules" (write list, no-setup/network sentence, scope exception, "two named git exceptions" -> three, server description, watcher sentence, "records nothing" sentence). Also its `## chantier` planning line stays. Pure text; `test_plugin_files` may count exceptions? grep found no test on AGENTS wording. |
| Cards (`skills/chantier/references/`) | `concepts.md` L125-136 (the autosync paragraph + "Planning folder" published/local), `chief-of-staff.md` L46 (table row `start/stop autosync`), L48 (`rescan`), L395-417 (the "A surface with an autosync" block, replaced), L732 (`3-ready holds ... not joined` note: check, it refers to autosync-joined status line text that goes), the "With a planning surface" hand-commit rule (search "commit" in that section, ~L380-395), `session-start.md` L91 (`board: autosync not joined`), L118-125 ("The surface's autosync" paragraph), `griller.md` L77, L86, `foreman.md` L512-516. `startup-manifest.json` L70: the section key `"autosync": ["concepts.md","chief-of-staff.md"]` is a reading-plan section: it is loaded by name somewhere? `grep` found no code or card using the key `autosync` other than the manifest: check `test_startup_manifest.py` / `plugin_files.py` for the key set before renaming to `writer`; rename only if the card that names it (grep `startup-manifest`) says so. chief-of-staff.md is 2062 lines and `test_startup_manifest.py` has byte-budget tests (L205 CR-driver common path, L233 reload budget): the CoS edit must not grow a budgeted section; the block replaced is about the same length. `agents/` and `com.github.copilot/agents/` untouched (cards only). |
| Removed tests | `T/test_autosync.py` (keep a small test of `foreign_running` + `read_group` read-only: move into `test_writer_cycle` blocked-reason case), `T/test_board.py` L24-25 imports, L112-141 (`test_board_does_not_join_autosync_implicitly`, join tests), L178-254 (`observe_join`/`watch_join`/`_existing_join`), `T/test_board_config.py` L15, L37-43, `T/test_store_command_table.py` L29, L157. Re-read each: delete only the autosync parts; they sit in files with other tests. |
| Tests added | `test_writer_lines.py`, P13 test (the existing P13 tests are in `test_autosync.py`'s `preflight_check` and the scenario's E2; there is no other P13 test file: put the new one next to `test_cli_runs`/`test_autosync`), board `writer` key in `GET /api/board` and `POST /api/writer/sync` (a case in `test_board.py` or `test_surface_server.py`, routes are called in-process as `test_store_command_table._board`). |

### Round 2 risks
- Texts are quoted verbatim by the cards and tests (`writer: not running: ... ($CHANTIER board --seat <session id>)`);
  write them ONCE in `writer/lines.py` and import them in the store refusal; `store -> writer.lines` must not import `core.repo` (cycle).
- `status` is called on every Foreman heartbeat: the `writer:` read is a `server.json` read + one
  psutil call; fine, but never run git there.
- `preflight` P13 on an in-project repo prints nothing (today: nothing unless the surface names
  autosync): keep "external only".
- `seat take` is a local write (never refused); only the extra line is added.
- Deleting `autosync/view.py` removes `Names`, used by `board/autosync_api.py` only (and
  `test_autosync.py`): confirm with grep before deleting.

## 3. Round 3: board web, docs, SVGs, screenshots script, scenario

### Board web (`SRC/board/web/`; read `DESIGN.md` first, `test_board_design.py` checks it)
- DELETE `js/ui/autosync.js` (85), `js/ui/autosync-events.js` (60), `js/ui/autosync-tick.js` (18),
  `css/autosync.css` (194); NEW `js/ui/writer.js`, `js/ui/writer-events.js`,
  `css/writer.css`. Wiring: `index.html` L25 (link), L54 (`#autosync-side`), L64 (`#autosync-phone`);
  `js/main.js` L13-14 imports, L30-33 paint calls, L128 `bindAutosync`; `js/core/store.js` L25
  (`autosync: {open,busy,error}` ui state); `js/core/refresh.js` L23 (`b?.autosync` in the lines
  fingerprint -> `b?.writer`; this decides redraw, easy to forget); i18n `js/i18n/en.js`
  L240-263 and `fr.js` L241-264 (24 keys each, replaced by writer keys; keep en/fr parity: a test
  may check key parity); `nav.sync` label stays.
- `css/tokens.css` L121-129 and `DESIGN.md` L146-153 (token table, compared by
  `test_board_design.check_table`): the `--autosync-*` tokens become `--writer-synced`,
  `--writer-active` (blue), `--writer-offline` (grey), `--writer-blocked` (red), plus the two
  boxes if kept; the component table of DESIGN.md names `autosync.css` (`components(design)`
  checks the sheet file exists: update it); `components.css` imports? (`css/components/` folder:
  grep for `autosync` there found nothing).
- States: `synced` green, `pending`+`syncing` blue, `offline` grey, `conflict`+`blocked` red,
  `off` grey "writer off". Panel facts and one **Sync now** (`POST api/writer/sync`).
- `just lint` runs Biome on `board/web` (format + lint): run it; `uvx --from nodejs-wheel npx biome`
  downloads (network, first run).

### Docs / SVG / texts (C.14), exact files
`docs/planning-modes.md`, `docs/planning-modes-texts.md` + `docs/planning-modes.svg`
(`<desc>` = texts' first paragraph, word for word; check box fit by opening the SVG:
`computer-use`/browser screenshot or render with a headless browser; no SVG tool in the repo, the
screenshots script uses Playwright chromium: reuse it to render), `docs/how-chantier-works-texts.md`
+ `.svg` (`<desc>` currently differs), `docs/planning-folder.md`, `docs/web-board.md`,
`docs/use-cases.md`, `README.md`, `docs/demo/AGENTS.md`, `docs/demo/README.md`; REMOVE
`docs/demo/.agents/guidelines/autosync.guidelines.md`, `docs/demo/scripts/ai-autosync-git.py`,
`docs/web-board/autosync-pc.png`, `autosync-phone.png`; ADD `writer-pc.png`, `writer-phone.png`
and retake every other `docs/web-board/*.png` in one `just docs-screenshots` run (the pill shows
in each). Search to finish: `grep -ril autosync README.md docs skills` outside `docs/release-notes/`
must leave only `foreign-autosync` and P13's warning (also `CONTRIBUTING.md` and `.gitignore`
L226 "The scenario's fake autosync logs" lines: CONTRIBUTING is not in the spec's list: its
autosync mention must be read and fixed or the `evals/results/claims-v0.10.0.md` (history, leave)).
New release-notes file for this version: see `docs/release-process.md` and
`scripts/release_notes.py --check` (part of `just check`: a notes file must exist for a version;
this CR does not bump the version, the Driver/CoS decides: ask if `release-notes` fails).

### `scripts/docs_screenshots.py`
`make_surface` (L41-83) writes fake `ai-autosync` state: replace by a bare origin
(`git init --bare`, `git remote add origin`, `git push -u origin main`, `git remote set-head
origin main` so `origin/HEAD` exists): the writer then reaches `synced` after its first cycle.
`start_board` (L86-) runs `uv run --locked --project ROOT chantier board --host ... --clock
CLOCK`: with `--clock` fixed, the writer entry's `started` (risk 6 of round 1) may read as
"not live" and the pill shows `off`: verify first, with `procs.alive_since`. The `autosync` capture
(L245-251, `EXTRA` L294) becomes `writer` (selectors `data-key="writer-pill"|"writer-dot"`, panel
class); the screenshot waits `.apop` today. `INCIDENT` constant and the secrets-incident fixture
go. The demo's `.repo/chantier.yaml` (L53-58) sits at the default clone path: excluded by the
writer's default exclude; and `.repo` is not a git repo there (a plain folder: no nested repo).
The pictures are taken at the Driver's discretion with a pre-pushed state so nothing is pending.

### Scenario
`scenario/run_scenario.py` (9948 lines). Unit `surface-board` (L114-117) runs the functions
`remote_board`, `forge_hub`, `surface_server`, `external_surface`, `cr_summary`. Every one writes
published paths through `SurfaceWorld` (L8661; `chantier()` L8672, `prepare()` L8694): with no writer ALL of them
get exit 2. The CR must pick ONE mechanism and say it in the PR: (a) `SurfaceWorld.build` starts
a real `board --seat` (BoardProc exists, L1944, L2095) with `CHANTIER_WRITER_TEST_TIMES` and a bare
origin, torn down at the end (honest, but several surface units test "no board running",
"board already running", elections L2276-2580; they create their own SurfaceWorld at L1725 and
L2051 so they need the writer entry too); (b) a prepared `writer` entry in `server.json` for the scenario process: cheaper but a
fake of the product (AGENTS "no fallback" concerns the product, a scenario stub is `fake_autosync`
-like; spec only removes `fake_autosync.py`). Recommend (a) for the new `surface-board` block
(spec §6 lists it: board with `--seat`, `file`, `triage` reach the bare origin, a second clone's
commit integrated, a conflict + scripted resolution, board stopped -> `file` refused with C.8's
text and folder unchanged) and (b) minimal for the older units, after a Driver decision.
Remove: `fake_autosync.py` (file), `surface_autosync` (L8730-8880), its call L9193, E2 lines
L2361-2364 (in-project `api.get("autosync") == {"present": False}`: becomes: in-project board has
no `writer` key or `writer.state` off and no writer thread), `AUTOSYNC_GUIDE` L8723; `.gitignore`
L226. `scenario/README.md` "Coverage" L286-291 bullets replaced, each naming a unit or test that
exists (`test_scenario_coverage.py` checks every bullet). Scenario time: the writer cycle every
30 s is shortened by the test times (`1:0.5:2:1:30`-style); the unit has a time budget
`UNITS["surface-board"][0]` that may need raising (`unit_row` reports over budget).
`just scenario` is the long gate (pipeline `ubuntu-latest` + the top CR locally on Windows).

## 4. Smallest change, and questions
Nothing can be dropped: the refusal (C.8) without the writer (C.5) would lock every surface. Round 1 order: `core/git.py`, `hub/state.py`, `hub/lock.py`, then `writer/paths.py`, `git_ops.py`, `cycle.py`, then the store refusal AND the test fixtures in the same commit (else the suite is red between commits). No question blocks the user. Driver decisions inside the spec's latitude: (1) a dead writer thread: server keeps serving or stops (as `HubThread`); (2) where C.8's "writer: <state>: not pushed yet" line is appended (store flag + `cli.py`); (3) the scenario's writer mechanism for the older surface units (real board vs prepared entry).
## 5. Evidence plan
Kind of change: behaviour of a CLI/server (round 1-2), UI (round 3), docs. Rules: AGENTS.md owes
`just check`, `just eval-dry-run` (CLI `src/` touched), `just scenario` (long gate, pipeline
`ubuntu-latest`; local Windows run by the top CR via `chantier gate`); no `hooks/` or `types/`
change here (so no `just mod`); no board-pane/`STATUS.json` change (`hooks/register.tsx`
untouched), so no pane screenshot owed.
| What | Technique | Evidence file |
| --- | --- | --- |
| Writer cycle, states, conflict, offline, Q25/Q30, LC_ALL | `test_writer_cycle.py` run with `-v` on Windows (the machine at hand), output kept | `evidence/writer-tests.log` (never published as raw: `work/gates/*.log`, summarize in evidence) |
| Refusal text, in-project untouched | `chantier file x` on a prepared surface with no `writer` entry: command, exit code, `git status` clean | `evidence/refusal.md` (command + output) |
| `sync`, `status`, `seat`, P13 lines by state | the same commands in a throwaway surface with a prepared entry per state (the unit test's prepared entries) and one real board | `evidence/lines.md` |
| End to end | `just scenario` unit `surface-board` (CI job `just scenario (ubuntu-latest)` green at the head, plus `chantier gate` locally if the CR is on top) | the job link / `chantier gate` summary |
| Real write path | a throwaway surface + bare origin in the scratchpad, `board --seat`, `file`, wait one shortened cycle, `git -C origin log -1`; board stopped, `file` refused | `evidence/real-run.md` |
| Board pill and panel, phone and PC | `just docs-screenshots` (Playwright, the repo's own script): the new `docs/web-board/writer-pc.png`, `writer-phone.png`; one extra capture of `conflict`/`off` states by a prepared entry for the reviewer (not committed to docs) | `docs/web-board/*.png` plus `evidence/pill-states.png` |
| SVG fit and `<desc>` | render both changed SVGs with Playwright (reuse the script's browser) and diff `<desc>` with the texts' first paragraph by a one-off script | `evidence/svg-planning-modes.png`, `svg-how-chantier-works.png` |
| Docs search | `grep -ril autosync README.md docs skills CONTRIBUTING.md` outside release-notes: only `foreign-autosync` and P13 | `evidence/autosync-search.txt` |
| `just test` time | wall time before/after on Windows (budget 18.5 s + 30 s = 48.5 s) | `evidence/test-time.md` |
Cannot be shown: the LFS offline texts until the LFS test runs on a machine with `git lfs`
(Windows' Git has it; the Ubuntu runner has it); real two-machine behaviour (not weighed by the
spec); Copilot's watcher wake (unproved, as today); a hook-slower-than-30 s lock timeout (not
tested, by spec).
