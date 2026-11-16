# Investigation: CR-222, `chantier board` becomes the web board's server

Worktree: `C:\Users\gaeta\Projets\chantier.worktrees\batch-17-CR-222`, branch
`chantier/batch-17/cr-222-change-specification-chantier-board-beco`, based on e54e299 (CR-237).
Nothing was edited in the code. Paths below are relative to the worktree; `SRC` =
`skills/chantier/scripts/cli/src/chantier`, `TESTS` = `skills/chantier/scripts/cli/tests`.

## 1. Code map and entry points

The CLI is one hatchling package declared in the root `pyproject.toml` (no `chantier.py`, no PEP 723
block, no `chantier.py.lock`). Dev: `uv run --locked --project <root> chantier`; plugin:
`uvx --from <plugin root> chantier --skill <skill folder>` (`plugin_files.cli_command`).

| Spec name | Real place |
| --- | --- |
| `board.py` | already split: `SRC/board/{__init__,collect,render,server}.py`. The command lives in `server.py` (`register`, `board`, `serve`, `_bind`, `_probe` on `/api/status`, `_wait_for_takeover`, `_watch`, `_seat_gone`, `is_loopback`, `_inside`, `_listing`, `_Server(ThreadingHTTPServer)`, `SEAT_CHECK_S=10`, `FILE_LIMIT=1_000_000`). No `command.py` yet. |
| `collect`/`settings` | `board/collect.py`: `collect(repo, seat)`, `settings(repo, host, port)` (via `playbook.config.load_board`), `DEFAULT_HOST/PORT = 127.0.0.1/8765`, `EVENTS_HIDDEN`, `EVENTS_SHOWN=12`. Uses `status.views.dashboard_view(repo, stage_layout(repo))` and `batch_view`. |
| `subject()`, `project_name()`, `_url_link` | `board/render.py` (`project_name(repo)` = `(repo.project_dir or repo.root).name`; `_url_link` private, http(s) only; `subject` strips "Change Specification: "). They must move out before `render.py` is deleted. |
| clock | `core/clock.py` (13 lines): `now()`, `stamp()`, `age_minutes(ts)` all call `datetime.now(UTC)` directly: no override exists. `--clock` needs a process-level override covering all three. |
| repo | `core/repo.py`: `Repo.find(cwd, project, readonly)` raises `SurfaceChoice` for a surface with several projects and no `--project`; `surface_projects(root)`; `Repo._external` runs git twice (build each project's Repo once). `repo.git_dir` = the key file's "git common dir" (the surface's when external). `repo.root` is the clone in a surface. |
| seat | `core/seat.py`: `read_seat(repo) -> SeatRecord|None`; `seat.json` at `repo.changes/seat.json`. |
| chain / stack_base | `commands/facts.py` (plain module, 189 lines): `chain(b_data)` (stack mode only, release last, fixes outside), `top_cr`, private `_start_base`, public `stack_base(b_data, c, repo, planned=False)`; need `repo.config["default_branch"]`. It imports `commands.crs`, `lifecycle.convert.open_repo`, `plugin_files`, `rails`: check no import cycle (`test_code_targets` counts lazy imports in its graph). |
| cost_rows / cost_groups | `commands/cost/sessions.py` `cost_rows(repo, d, host, uuids)` (raises `ChantierError(..., EXIT_EXTERNAL)` when no priced call) and `foreman_uuid(d)`; `commands/cost/breakdown.py` `cost_groups(repo, batch, rows, by)` returns `{key: [calls, usd, unpriced, peak_context, compactions]}`; `commands/cost/command.py` has private `_by_cr`. The board must not use `open_repo()` (it may convert the tree): use `Repo.find(readonly=True)`. |
| status views | `status/views.py`: `batch_view`, `dashboard_view`, private `_row`, `_backlog`, `_past`, `spec_state`, `when_of`; `PAST_LIMIT=50`, `SCHEMA=3`. `_row` omits `after`, `kind`, `order`, `stacked`, `merged_at`, `round_limit`: add them in the board's own data, never in `status.py` (the pane and `status` share that view; `hooks/` and `types/` stay untouched). |
| load_board | `playbook/config.py` `load_board(path) -> (dict, problems)`, `BOARD_KEYS=("host","port")`; messages stay unchanged. |
| stages | `lifecycle/stages.py` `stage_layout(repo)`, `PRIORITIES`, `prepared_cr`. |
| records | `core/records.py`: pydantic `BatchRecord`, `CrEntry`, `EventRecord` (extras via `__getattr__`), `OrderRecord`, `AskRecord`; `read_batch_json`, `read_events`, `round_limit(d, c)`, `chief_sessions`. |
| errors | `core/errors.py`: `ChantierError(message, code)`; board uses `EXIT_EXTERNAL = 4` for "port held". |

How commands register: `cli.py` (108 lines) imports `from chantier.board import server` at module
level and lists it in the tuple whose members get `module.register(sub)`; `commands/registry.py`
`add_command(sub, name, fn, help_, scope)` adds `--project`, `--skill` and (unless `NO_BATCH`)
`--batch`. `board` is `NO_BATCH`. `cli.main` sets `repo.PROJECT = args.project`. The new
`board/command.py` replaces `server` in that tuple and in the import. `cli.py` also holds
`FULL_OUTPUT`, `MAX_LINES = 10` and a note that `board` prints its own lines: keep it working.

Dependencies and lazy imports: root `pyproject.toml` `[project] dependencies =
["pydantic==2.14.3", "ruamel.yaml==0.19.1", "psutil==7.2.2"]`; `[tool.uv] no-build = true` (wheels
only); a test asserts every dependency is pinned with `==`. Lazy imports are enforced by ruff TID253
through `banned-module-level-imports = ["ruamel", "ruamel.yaml", "psutil"]`: add `starlette`,
`uvicorn` (and `anyio`, `h11` are transitive only) there and import them inside `board/` functions
so `chantier --version` and `chantier status` keep their start time (baseline here: ~0.55 s warm,
median of 5; 1.27 s first run which built the venv). A `uv lock` dry run in a scratch copy resolved
20 packages and adds anyio 4.16.0, click 8.5.1, h11 0.16.0, idna 3.20, starlette 1.10.0, uvicorn
0.54.0 (about 70 lock lines); `colorama` and `typing-extensions` were already locked. `uv.lock` is
tracked; `just lint` runs `uv lock --check`.

Package data: hatchling ships non-Python files inside the package folder, and dev mode is editable,
so `Path(__file__).parent / "web"` (or `importlib.resources`) works in both. Hatch honours
`.gitignore`, whose root file has `lib/`, `build/`, `dist/`, `*.log`, `parts/`, `share/`: web paths
must not use those names (a `lib/` folder would silently vanish from the wheel). Map content types
explicitly (`.js` text/javascript, `.css` text/css, `.svg` image/svg+xml, `.html`, `.json`):
Python's `mimetypes` reads the Windows registry (values were right here, not guaranteed elsewhere).

## 2. The smallest change

New `SRC/board/` modules `command, address, key, projects, state, files, fingerprint, costs, seats,
app` (each under 400 lines, every function under 50, 5 arguments max, complexity 10); delete
`collect.py`, `render.py`, `server.py`; add `board/web/` (frame, no build step, no framework);
`--clock` override in `core/clock.py`; two pins in `pyproject.toml` and the lock. `status.py`, `hooks/`,
`types/`, CI jobs and the plugin manifests stay untouched. `board/app.py` must not import
`board/command.py` (cycle in `test_code_targets`).

## 3. Tests, justfile, CI

- `TESTS`: `conftest.py` (fixtures `repo`, `sh`, `load_script`, `SKILL`, `PLUGIN_ROOT`),
  `test_cli_runs.py`, `test_cli_units.py`, `test_code_targets.py`, `test_costs.py`,
  `test_plugin_files.py`. There is **no `tests/test_structure.py`** (the spec and brief name it): its
  role is `test_plugin_files.py`. There is **no unit test of the board**: only scenario 16c and the
  surface step cover it; `test_the_board_mod_is_wired_on_claude_only` concerns the mod, not the CLI.
- `test_code_targets.py`: `CLI = Path(__file__).resolve().parents[1]`, `MAX_FILE_LINES=400`,
  `MAX_FUNCTION_LINES=50`, `SCOPE` = every `.py` under CLI (no `.venv`, no `__pycache__`); helpers
  `_module`, `_imports` (ast, counts imports inside functions), `_cycle` (DFS), `_size_problems`;
  test 1 `test_files_and_functions_are_small_and_the_imports_have_no_cycle`; test 2
  `test_one_root_project_holds_the_dependencies_and_nothing_else_is_a_script` (deps pinned with `==`,
  `no-build`, no `CLI/pyproject.toml`, no `CLI/chantier.py`, only `session_usage.py` is a PEP 723
  script). Style: plain functions, pathlib, `assert not problems, "\n".join(problems)`. The new web
  test follows it (root `CLI/src/chantier/board/web`, one test): no JS/CSS file over 400 lines; the
  ES-module import graph has no cycle and every module is reached from `main.js`; `index.html` has no
  inline script, no inline style, no `on*=` attribute; no `http(s)://` in `board/web`; `innerHTML`
  only in `js/dom.js`; one module per view in `js/views/`.
- `justfile`: `lint` = `uvx ruff@0.17.5 format --check skills`, `uvx ruff check skills`, `uv run
  --locked --group dev --with mypy==1.20.0 --with types-psutil mypy`, `uv lock --check`; `check` =
  lint + test + release-notes; `scenario` = `uv run --locked python scenario/run_scenario.py --forge
  github` then `--forge gitlab`; `set windows-shell := ["powershell.exe", ...]`. ruff: line 100, rules
  E W F I B UP SIM C90 PL RUF PGH004 PLR1702 TID253; mypy strict with the pydantic plugin; `files`
  covers src, tests and `session_usage.py`.
- `.github/workflows/ci.yml`: `check` (ubuntu, macOS Intel and windows; macOS `continue-on-error`),
  `scenario` (ubuntu only), `eval-dry-run`. The spec says CI does not change: a new lint step inside
  `just lint` runs on all three systems with no workflow edit. Consequence: the linter's first run
  needs the npm registry on the runner (CI has network).

## 4. Scenario steps to rewrite

`scenario/run_scenario.py`:
- `remote_board(w)` lines 1084-1241 (step 16c), called at line 1016. `BoardProc` lines 1019-1048
  (Popen `[sys.executable, "-m", "chantier", ...]`, reader thread, `line(timeout)`, `stop()`);
  `free_port()` 1051; `fetch(port, path, method, host)` 1057 (no proxy; returns status, headers,
  body; POST sends `data=b"x"`); `folder_state` 1069; `without_time` 1075.
- Today's checks (all replaced by the spec's 12 checks): loopback start line `board on
  http://127.0.0.1:{port}/ over {state}`; `/` is HTML; `/api/status` = index view + `planning_folder`,
  `seat`, `board: True`; `/file?p=` and 404 outside paths; POST gives 405; nothing written; a second
  board prints `board already running at ...`; a held port exits 4; seat moved to s-2 stops the board
  with exit 0; `--host 0.0.0.0` prints a second line ("listens beyond this machine ... no password");
  `chantier.yaml` board keys and their problem lines.
- `BoardProc` and `fetch` gain key handling (the `?k=` URL, `X-Chantier-Board-Key` header, cookie and
  the 303 exchange, no redirect following, ETag/`If-None-Match`).
- Surface step lines 5460-5474: `BoardProc(w, "board", "--project", "demo", "--port", port,
  cwd=w.surface)`; checks the start line starts `board on ` and holds `projects/demo/changes`, `/`
  lists "Surface work", `/file?p=` with `../../other/changes/1-inbox` and `../../../../code/app.py`
  answers 404. It becomes spec check 12 (both projects served, `surface: true`).
- The scenario starts boards through `sys.executable -m chantier`, so the root-project dependencies
  are on the path; `scenario/README.md` lines 84-92 and 127 describe the surface step and need a
  glance (check wording only).

## 5. Where sections 12 and 13 of the spec edit (current text, current lines)

The spec's line numbers are stale. Real places:
- `AGENTS.md`: writes sentence 10-14; the board exception 21-27 ("a read-only web view of the record
  the CLI already keeps, for the user in remote: it writes no file, is part of the CLI's package and
  runs with no plugin too (`uvx --from git+https://github.com/gsemet/chantier@v<version> chantier
  board`), and knows no role; anything more (answering an ask, filing an item) is another CR"). The
  spec's replacement text drops the uvx clause: keep it. Line 11 "`uv` is the only tool to install":
  the linter must go through uvx. Line 29 onward: root pyproject rules.
- `CONTRIBUTING.md`: the board's line 86-90 (spec: 84-86); mod item 100+; "the CR board pane and
  `chantier board` show the same view (`schema` 3) and change with `status.py`" lines 110-111 (spec:
  107-108; make it the pane only, the web board has its own state with a shared base); layout line
  `pyproject.toml, uv.lock` 127 and `scripts/cli/` 137; "Code standards" 244-266 (line 261 lists the
  layers including `board/`; 265-266 "The board CRs add the JS and CSS targets with their linter":
  write the targets now).
- `skills/chantier/references/session-start.md` "The board" lines 62-77 (bullets 68-74).
- `chief-of-staff.md`: routing row line 40; "what you can say" list 648-649 (spec: 643-645).
- `hosts/claude-code.md`: trials 37-38; remote row 505 (spec: 499; mentions Tailscale/LAN);
  `hosts/copilot.md` 29-30.
- `docs/boards.md`: intro line 3 ("two read-only views"); "## The remote board" 68-90 (yaml block and
  a uvx example). Renaming it to "The web board" breaks the anchor `boards.md#the-remote-board`
  linked from `docs/agents-and-models.md` line 28 (that line does not say "read-only"): update the
  link. `README.md` line 241 ("the CR board and the remote board") and 162-170 (pane, unchanged).
- Not to edit: `docs/release-notes/2026-11-13-v0.9.0/release-notes.md` (history).
- `prototype/README.md` in the CR folder has stale paths.

## 6. Spec statements that no longer match the code

1. No `chantier.py`, PEP 723 block or `chantier.py.lock`: dependencies go in the root pyproject with
   `==` pins, then `uv lock`; the check is the existing `uv lock --check` in `just lint`.
2. `board.py` is already `board/{collect,render,server}.py`; the command sits in `server.py`.
3. `chain` and `stack_base` are public in `commands/facts.py`; `_start_base` private; `chain` returns
   stack mode only. Cost helpers: `commands/cost/{command,breakdown,sessions}.py`, `_by_cr` private.
4. `project_name`, `subject`, `_url_link` are in `render.py`, which goes away.
5. No `tests/test_structure.py`.
6. Doc line numbers shifted (section 5); the AGENTS.md text must keep the uvx clause.
7. `probe on /api/status` (today's `_probe`) becomes a probe on `/api/board` with the key from the
   file, as the spec says; note the old board answered unauthenticated.
8. CI `scenario` is ubuntu only; `just scenario` uses `uv run --locked python`.
9. `04-feasibility.md` file paths (`src/board.py`, `commands.py`) are stale; its semantics fixes hold.
10. `core/clock.py` has no override: the spec's `--clock` is new code, not a hook-up.

## 7. Risks

- uvicorn: pre-bind the socket and pass `Server.run(sockets=[sock])` so a held port exits 4 and
  `--port 0` can print the picked port; no `SO_REUSEADDR` on Windows (as today). Keep stdout to the
  start lines (`log_config=None`, `access_log=False`): the scenario reads stdout.
- The seat-watch thread sets `server.should_exit`; Ctrl-C and seat change must both exit 0.
- `--clock` must override `age_minutes` and `stamp` as well as `now`, or ages disagree.
- Values derived from measured sizes: the frame's layout (sticky headers, panes) must not derive
  sizes in JS from elements that other code measures; keep widths and heights in CSS tokens.
- `board/state.py` imports `commands.facts` (heavy): keep that import lazy or confirm no cycle in
  `test_code_targets`.
- Hatch and `.gitignore` (section 1); Windows mimetypes (section 1).
- CRLF: files written on Windows trip Biome's formatter; set `formatter.lineEnding: "lf"` and add a
  `.gitattributes` line `skills/chantier/scripts/cli/src/chantier/board/web/** text eol=lf` (today's
  file only holds `evals/kit/dry-run/*.patch text eol=lf`).
- A 5-minute live-cost rule means the cost endpoint reads transcripts: it must never write
  `batch.json` or `events.jsonl` (E5 proves it).
- Dependencies from a git+https `uvx --from` run: the same pyproject applies, nothing else to do.
- A LAN-open default (0.0.0.0) with the key in the URL: decided by the Chief of Staff (defaults stay).

## 8. JS/CSS/HTML linter through uvx on a PyPI Node (tested on this Windows machine)

PyPI has no Biome, ESLint, Stylelint or Prettier binaries (`biome` there is an unrelated env tool;
`prettier` is a pretty-printer). Node itself comes from PyPI:
- `uvx --from nodejs-wheel node|npm|npx ...` works (`nodejs-wheel` 24.22.1 resolved
  nodejs-wheel-binaries 24.19.0, Node v24.19.0 here). Pin it: `nodejs-wheel==24.22.1`.
- `nodejs-bin` provides only `node`; `nodejs-wheel-binaries` alone fails ("does not provide any
  executables").
- The tool then comes from npm: `uvx --from nodejs-wheel npx --yes @biomejs/biome@<pin> check <dir>`.

Options: (A) **Biome** (recommended): one native binary, one `biome.json`, lints and formats JS, CSS
and HTML (2.6.x); worked on Windows (first run ~2.7 s); `noExcessiveLinesPerFile` (maxLines 400),
`noInlineStyles`, `suspicious/noVar` cover several targets directly; in `biome.json` use `preset`, not
the deprecated `recommended`, and `suspicious/noVar` (not `style/noVar`). (B) ESLint 10 + Stylelint
18 + Prettier 3: three configs and many npm packages (flat config needs local installs), several more
network fetches per run, much more to pin. Recommendation: A, pinned in the justfile (Node and Biome
versions as recipe variables), run inside `just lint` so `just check` covers Linux, macOS, Windows. A
machine's own `node.exe` is not relied on. Cannot be shown here: macOS and Linux behaviour (CI only).

## 9. Evidence plan

Kind of change: a new behaviour (HTTP server and web UI) plus a rewrite of tested behaviour. The
project's rules on evidence rank above this plan. What shows it before/after: the scenario's old and
new 16c, and screenshots beside the prototype's v6-09 and v6-11.

| # | Evidence | Command / technique |
| --- | --- | --- |
| E1 | `just check` passes (ruff, mypy, lock check, Biome, tests) | `just check` on Windows; CI on 3 systems |
| E2 | The 12 scenario checks, both forges | `just scenario` here, and CI on Linux |
| E3 | Phone use over LAN with the key URL | manual by the user; PR Known gaps names it until done |
| E4 | Surface mode, two projects | scratch surface through the scenario's helpers, `fetch` on `/api/board` and both projects' state, `surface: true` |
| E5 | Live cost equals `chantier cost --by cr`; no write; no transcript case | compare `chantier cost --by cr` with `GET /api/projects/{id}/costs`; hash `batch.json` and `events.jsonl` before/after; empty `CLAUDE_CONFIG_DIR` gives `live.error` |
| E6 | The pages look right at desktop and phone | `uv run --with playwright` script kept in `evidence/` (never shipped) at 1400x860 and 375x812, or headless Chrome (`C:\Program Files\Google\Chrome\Application\chrome.exe --headless --screenshot --window-size`); caption with the head's 7-char SHA; check console has no error |
| E7 | Polling is cheap | median of ten wall times of a 304, of the full state and of the tree, on Windows |
| E8 | No start-time regression | `chantier --version` and `chantier status`, median of ten, main vs branch (baseline `--version` ~0.55 s) |

Cannot be shown: E3 (needs the user's phone and network); wheel contents on Linux and macOS (CI
only; a wheel build check `uv build` here proves Windows packaging: the web files are inside);
Chrome and Playwright availability on the Verifier's machine (Chrome present here; Edge is not;
Playwright 1.65.2 with chromium-1248 cached).
The pane (`hooks/register.tsx`) is untouched: no `just mod`, no pane screenshot.

## 10. Split into three Coder rounds

Round 1, backend Python (+ its tests):
- `pyproject.toml` (starlette==1.10.0, uvicorn==0.54.0; ruff banned-module-level list), `uv.lock`.
- `SRC/board/{command,address,key,projects,state,files,fingerprint,costs,seats,app}.py`; delete
  `SRC/board/{collect,render,server}.py`; `SRC/cli.py` (import and registration tuple); `SRC/core/clock.py`
  (`--clock`); docstrings of `SRC/commands/__init__.py` and `SRC/__init__.py`.
- `TESTS/test_board.py` (new, few and fast: key file and `--new-key`, file confinement, a state
  derivation); keep `test_code_targets.py` green (sizes, no cycle).
- Gate: `just check`; the old scenario step fails until round 3: say so.

Round 2, frontend:
- `SRC/board/web/index.html`, `css/{tokens,frame,components}.css`,
  `js/{main,api,store,router,time,dom,icons,frame}.js`, `js/views/{home,triage,kanban,batch,costs}.js`,
  the language files (`web/i18n/en.js`, `fr.js`, one word file per language, extensible), no `lib/`,
  `build/`, `dist/` names.
- `biome.json` (root), `justfile` lint step with pinned Node and Biome, `.gitattributes` eol entry.
- The web test in `TESTS/test_code_targets.py`; the JS and CSS targets in CONTRIBUTING "Code
  standards".
- Gate: `just check`; screenshots (E6) from a running board.

Round 3, scenario, docs, cards:
- `scenario/run_scenario.py` (16c, `BoardProc`, `fetch`, surface step ~5460), `scenario/README.md`
  check.
- `AGENTS.md`, `CONTRIBUTING.md` (86-90, 110-111, 127/137, 261-266),
  `skills/chantier/references/{session-start.md,chief-of-staff.md}`, `hosts/{claude-code,copilot}.md`,
  `docs/boards.md`, `docs/agents-and-models.md` (anchor), `README.md` line 241.
- CR folder: `evidence/` for E1-E8, the prototype README path fix.
- Gate: `just check` and `just scenario`.

## 11. Questions only the user can answer

None blocking. The Chief of Staff decided the spec's open points (two languages, Biome allowed, network
and key defaults). E3 needs the user's phone; until then the PR's Known gaps names it.
