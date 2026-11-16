# Change Specification: the CLI takes its dependencies through PEP 723, and its code is split and checked

## Goal

The user's words (`intake/request.md`, 2026-11-13): "you use uv, you can install dependencies in
inline metadata to simplify and modularise the Python code; it should be done anyway, to be
clean; maybe put this refactor first among the CRs".

The grill (`02-answers.md`) makes it a refactor with no change of behaviour. chantier's Python may
now declare packages in the PEP 723 block that `uv run --script` already reads (today
`dependencies = []`). The refactor splits `commands.py` (3,198 lines) into modules and replaces
hand-written code with a library where one does the job. At the end, every Python file of the
plugin meets measured targets that `just check` enforces on Linux, macOS and Windows. The
user's words: "make sure the code is very clean, with good standards and modularity, for easy
maintenance". This CR runs before the board CRs, which build on the new structure.

## Decisions carried from `02-answers.md`

| Decision | Where this spec carries it |
| --- | --- |
| 1. Dependencies are Python packages in the script's PEP 723 block, installed by uv; no vetted list in `AGENTS.md` | "Dependencies", "AGENTS.md" |
| 2. Split `commands.py` into modules; replace hand-written code with libraries where one does the job (argument parsing, JSON models…); no change of behaviour | "The package layout", "Libraries", "Behaviour kept" |
| 3. The first run needs the network to fetch the dependencies; after that uv's cache is enough | "Dependencies", "Docs", evidence E6 |
| 4. The board server may use a web framework; its interface is hand-written HTML, CSS and JS with no compiler; Playwright through a uv script for the screenshots | "Out of scope" (the board CRs carry it); this CR only splits `board.py` and changes the board's rule |
| 5. This CR runs first; `visualization-backend` and `cr-summaries` wait for it | Already recorded: both `depends.json` files hold `{"after": ["python-inline-deps"]}`; nothing to do |
| 6. `AGENTS.md`: "The CLI has no dependencies" and the board's "standard library only" change to say dependencies come through PEP 723 | "AGENTS.md" |
| 7. Very clean, standard, modular code; for this CR and every board CR after it | "Targets", "CONTRIBUTING.md" |
| 8. Measured targets for every Python file of the plugin, enforced by `just check` on three systems, tools through `uvx` | "Targets", "`just check`", evidence E1 |
| 8. JS and CSS targets for the board | "Out of scope" (the board CRs) |

## Scope: which Python files

The targets of answer 8 apply to **the plugin's Python**, which is every `.py` file under
`skills/`. Today those files are all in `skills/chantier/scripts/cli/`:

- `chantier.py`
- `session_usage.py`
- `src/chantier/*.py`
- `tests/*.py`

The tests are under `skills/` and ship with the plugin, so they count.

The repository's own tools are not the plugin, and the targets do not apply to them. They change
only where they must run the CLI with its dependencies:

| Entry point | In this CR |
| --- | --- |
| `scripts/version.py`, `scripts/release_notes.py` (`uv run --script`, `dependencies = []`), `scripts/mod.py` | No change. They import nothing from the CLI, and `chantier.py.lock` carries no project version, so `version.py`'s `TARGETS` stay as they are. |
| `scenario/run_scenario.py`, `scenario/fake_*.py` | Two changes only: the `just scenario` recipe runs them with the CLI's dependencies, and the imports of moved names follow their new modules (see "Behaviour kept"). No check changes. |
| `evals/kit/dry_run.py` | Its CLI calls (`[sys.executable, str(CLI)]`) need the dependencies, so the `just eval-dry-run` recipe runs it with them. The kit's own code stays standard library only. |
| `evals/kit/setup.py`, `evals/kit/audit.py` | No change. They call `uv run --script <CLI>`, which installs the dependencies itself. |

## Dependencies

- `skills/chantier/scripts/cli/chantier.py` declares the packages in its PEP 723 block. The
  block also sets `[tool.uv] no-build = true`: a package without a wheel for the user's system
  and Python fails at once, with uv's own message. Nothing is ever built from source on the
  user's machine. This was measured on 2026-11-13: PyYAML 6.0.3 has no CPython 3.15 wheel for
  Windows, and uv then tried to compile it and failed for lack of MSVC. A dependency must ship
  wheels for Linux, macOS (x86_64 and arm64) and Windows.
- `requires-python = ">=3.11"` stays. Ruff's `target-version` and mypy's `python_version` are 3.11.
- The resolved versions are locked in `skills/chantier/scripts/cli/chantier.py.lock`
  (`uv lock --script chantier.py`). The lock is committed, and `uv run --script` uses it, so a
  user runs the versions CI ran. The inline block gives floors (`>=`); the lock gives exact pins.
- `skills/chantier/scripts/cli/pyproject.toml` lists the same packages in `[project]
  dependencies`, and its `uv.lock` is refreshed, for `just test`. A test checks that the two
  lists agree (see "Tests").
- The command an agent runs does not change: `uv run --script "<skill>/scripts/cli/chantier.py" …`,
  as in `commands.cli_command`, the cards, the four `SKILL.md` files and the allow rules
  `uv run --script *chantier.py *` in `references/hosts/claude-code.md` and `_SAMPLES`. No
  card, skill or permission rule changes.
- `session_usage.py` keeps its own block and its pinned PyPI index, unchanged.
- The libraries that only some commands need are imported lazily: `ruamel.yaml` by the commands
  that read `chantier.yaml`, and `psutil` by `cancel` and `gate`. Measured on Windows, CPython
  3.11 and 3.15: importing `ruamel.yaml` takes 0.10 to 0.15 s, `pydantic` 0.07 to 0.20 s and
  `psutil` 0.03 to 0.05 s. A bare `uv run --script` takes 66 ms; with all three imported at
  start, it takes 290 ms. The lazy imports are declared in ruff's configuration
  (`lint.flake8-tidy-imports.banned-module-level-imports`, which ruff's `PLC0415` exempts), not
  marked with `noqa`.

## Libraries

Each library below replaces hand-written code. No other library comes in. Measured on
2026-11-13: each one installs from wheels alone (`no-build`) on Windows with CPython 3.11 and 3.15
(`ruamel.yaml` 0.19.1, `pydantic` 2.14.3, `psutil` 7.2.2).

### `pydantic` (v2): the JSON records

It replaces the hand-written record handling in `state.py`, and the `.get(…, default)` reads
spread over `commands.py`, `rails.py` and `status.py`:

- `read_batch_json`, which rewrites the old words `landed` and `open` to `paused` and `running`.
  This becomes a `model_validator(mode="before")`.
- `apply_batch_settings`'s `isinstance` check ("invalid batch settings; refusing to run"). This
  becomes the type of `settings`. The message is kept.
- The fallbacks of `chief_sessions` and `round_limit`. These become fields with defaults.
- The `try/except (OSError, ValueError, KeyError, TypeError)` read of `restored.json` in
  `next_cr_number`.
- `commands._run_read` and `_run_write` (`.long-gate.run`), and `_read_seat` (`seat.json`).

There is one model per record:

- `batch.json`, its settings and its CR entries
- an `events.jsonl` line
- `seat.json`
- `.long-gate.run`
- `restored.json`

The models use `extra="allow"`, so a key this version does not declare survives a read and a
write. They write with the keys that were set only (`exclude_unset`), so an absent key stays
absent. The code reads and changes a record through the models' attributes. No record is passed
around as `dict[str, Any]`. The views (`STATUS.json`, `STATUS.md`, the board's data) may use
models or `TypedDict`s, as long as their output stays byte-identical (see "Behaviour kept").

### `ruamel.yaml`: reading `chantier.yaml`

It replaces the YAML tokenizer and parser in `playbook.py`, about 190 lines:

- `_strip_comment`, `_tokens`, `_scalar`, `_double`, `_flow_list`, `_inline`, `_block`, `_list`,
  `_map`, `parse`
- `_Token`

ruamel's composer reads the file (pure Python, its C extension not required). A short walk over
the composed nodes builds the same `Node` tree (`kind`, `line`, `value`) that `load`,
`load_board`, `_role`, `_prices`, `_five` and `_board` validate today. Those functions keep
their messages and lines.

The walk keeps every structural refusal of the subset, with today's words and line:

| Refused | Today's message |
| --- | --- |
| A tab in the indentation | "a tab in the indentation: indent with spaces" (a line check before the parse) |
| Several documents | "several documents (`---`) are not accepted: one document" |
| Anchors, aliases and tags | "anchors, aliases and tags are not accepted: found `…`" |
| Block scalars | "block scalars (`|`, `>`) are not accepted: write the value on the line" |
| Flow mappings | "flow mappings (`{}`) are not accepted: use a block mapping" |
| A list inside a list | "a list inside a list is not accepted" |
| A duplicate key | "duplicate key `k` (first at line n)" |
| An empty value | "an empty value" |

Scalars stay strings: the composer is used, never the constructor, so `port: 8765` is still the
text `"8765"`. Where ruamel refuses a line for a lexical reason (an unclosed quote, a plain
value holding `: `), the message is `chantier.yaml:<line>: <ruamel's problem text>`, with
ruamel's line plus one. See open point 1.

### `psutil`: finding and stopping processes

It replaces the process listing and signalling in `procs.py`:

- `_cwds`: `/proc` on Linux, `lsof` on macOS
- `_cmdlines`: `ps`, and PowerShell `Get-CimInstance` on Windows
- `_taskkill`
- the `ctypes` `OpenProcess`/`GetExitCodeProcess` check in `alive`, and `_alive`'s zombie check

`stop_group` on POSIX keeps `os.killpg`, which psutil does not offer. The rules stay as they
are:

- A process belongs to a worktree when its directory is in it (POSIX only, as today) or when its
  command line names it. On Windows the match ignores case and slash direction.
- The process itself and its parent are excluded.
- On POSIX, SIGTERM is sent, then SIGKILL after the grace period. On Windows, the process tree
  ends at once.
- A zombie counts as gone.

See open point 3.

### Not replaced, and why

- **Argument parsing stays `argparse`** (standard library, not hand-written). Click or Typer
  would change the usage errors, which the scenario checks (`"invalid choice"`,
  `run_scenario.py` line 2620), and the help text. Typer also pulls in `rich`, which formats
  errors on its own. What is wrong today is the 214-line `cli._parser`. Each command module now
  declares its own subparser in a `register(sub)` function, next to its handler (see "The
  package layout"). See open point 2.
- **The locks stay hand-written.** `_LongGateLock` keeps its holder's text after byte 0 of the
  lock file, and `filelock` truncates the file and, on Windows, deletes it. So the `fcntl` and
  `msvcrt` code in `state.py` stays, moved to `core/files.py`.
- **`read_keyed`** (9 lines, `checkout.yml`), **`rule_matches`/`_glob`** and **the Markdown
  writers of `status.py`** stay as code. No library replaces them clearly, and the STATUS files
  must stay byte-identical.
- **The board's HTTP server** (`http.server`) stays. Its framework belongs to
  `visualization-backend`.

## The package layout

The code of `skills/chantier/scripts/cli/src/chantier/` moves into layers. A module imports only
from its own layer or the layers below it. Each module has one responsibility, stated in its
docstring. The line ranges below are those of today's `commands.py`. The Driver may split a
module further to meet the targets, but not merge two of them.

**Layer 0: `core/`, the foundation**

| Module | What goes in it (from) |
| --- | --- |
| `core/errors.py` | `ChantierError`, `EXIT_*` (`state.py`) |
| `core/files.py` | `read_text`, `write_file`, `write_json`, `_retry`, the OS locks `_try_lock`/`_unlock` (now public), `IGNORED` and `ensure_gitignore` (`state.py`) |
| `core/clock.py` | `now`, `stamp`, `age_minutes` (`state.py`) |
| `core/git.py` | `git`, `default_branch` (`state.py`) |
| `core/records.py` (or `core/records/`) | the pydantic models of "Libraries", with the old-word migration |

**Layer 1: `core/`, the repository and the batch**

| Module | What goes in it (from) |
| --- | --- |
| `core/repo.py` | `Repo`, `SurfaceChoice`, `surface_projects`, `project_path`, `read_keyed`, `PROJECT`, `CHANGES`, `DEFAULT_CONFIG` (`state.py`) |
| `core/batch.py` | `Batch`, `normalize_batch`, `normalize_cr`, `resolve_batch`, `check_epoch`, `read_batch`, `find_cr_batch`, `next_cr_number`, `move_directory` (`state.py`) |
| `core/seat.py` | `_read_seat` (`commands.py` 986–996), which `board.py` imports today |

**Layer 2: the domain modules**

| Module | What goes in it (from) |
| --- | --- |
| `lifecycle/stages.py` | `stage_layout`, `changes_lock`, `PreparedCR`, `prepared_cr`, the moves, `archive_name`, `move_backlog_item` |
| `lifecycle/convert.py` | `old_tree`, `convert_old_tree`, `_convert`, `_undo`, `write_dashboard_after_rename` |
| `rails.py` | unchanged in role |
| `procs.py` | rewritten on psutil |
| `playbook/models.py` | `Model`, `MODELS`, `SETS_MODEL_AT_START`, `ESCALATION`, `normalise`, `resolve` |
| `playbook/yaml_subset.py` | ruamel and the refusal walk: `YamlError`, `Node` |
| `playbook/config.py` | `load`, `load_board`, `_role`, `_prices`, `_five`, `_board`, `_number` |
| `playbook/lines.py` | `playbook_lines`, `team_lines`, `escalate_line` |
| `costs/transcripts.py` | the Claude transcript and its prices (`PRICE`, `usage`, `_add`, `_wakes`, `_grill_use`) |
| `costs/sessions.py` | `session_costs`, `idle_seconds`, `agent_records`, `agent_context`, the spec-writer filters |
| `costs/copilot.py` | `copilot_session_costs`, `SESSION_USAGE_SCRIPT`, the uv call |
| `status/words.py` | `step`, `forge_word`, `severity`, `icon`, `label`, `steering_word`, `shape_word` |
| `status/views.py` | `cr_view`, `batch_view`, `dashboard_view` and their helpers |
| `status/markdown.py` | `cr_markdown`, `batch_markdown`, `dashboard_markdown` |
| `status/write.py` | `write_batch`, `write_final_pages`, `write_dashboard` |
| `plugin_files.py` | `commands.py` 52–175: `skill_dir`, `plugin_root`, `cli_command`, `detect_host`, `project_instructions`, `surface_instructions`, `archive_path`, `_skill_version`, `_agent_files`, `plugin_roles`, `read_playbook`, `_agent_problems` |

`rails.py` is 383 lines today and must shed its `costs` import if that import forms a cycle.

**Layer 3: `commands/`, one module per family of commands**

Each module holds its handlers and its `register(sub)`.

| Module | What goes in it (`commands.py` lines) |
| --- | --- |
| `commands/permissions.py` | 176–351: `_SAMPLES`, `RECOMMENDED_ALLOW`, `rule_matches`, `_settings_rules`, `_sample_groups`, `commands_not_allowed` |
| `commands/preflight.py` | 352–447: `preflight` |
| `commands/intake.py` | 448–613: `init`, `file_cr`, `triage`, `abandon`, `restore` |
| `commands/crs.py` | 614–702, the CR facts shared by several commands: `_batch_cr`, `_work`, `_worktree`, `_cr_events`, `same_head`, `_short`, `_dirty`, `gate_passed`, `last_verdict`, `grant_line`, `filed_fix` |
| `commands/opening.py` | 703–937: `add_cr`, `cr_slug`, `read_depends`, `archived_merged`, `declare_dependencies`, `check_series_order`, `_release_tag`, `release_waits_for_all`, `check_cycles`, `open_batch` |
| `commands/seat.py` | 938–1046: `foreman`, `seat`, `_own_transcript` |
| `commands/orders.py` | 1042–1380: `ORDER_KINDS`, `CR_ORDERS`, `order`, `_order_done`. The 171-line `_apply_order` becomes a table of one small handler per kind. |
| `commands/orders_release.py` | the release kinds (`approve`, `grant`, `confirm`, `add --release`, `add --fix-for`): `_release_cr`, `_add_release`, `_join_release`, `_check_release_open`, `_started`, `_refused` |
| `commands/batch_status.py` | 1381–1612: `status`, `_activity`, `_refresh`, `_stop_heartbeat`, `_record_costs`, `asks`, `agents` |
| `commands/facts.py` | 1613–1757: `_chain`, `_top_cr`, `_start_base`, `_stack_base`, `_ref`, `_base_of`, `_stack_ref`, `_facts`, `handoff` |
| `commands/driver.py` | 1758–2007: `_reopen`, `_check_release_branch`, `take`, `round_`, `_context_line`, `handback`, `note`, `log` |
| `commands/rules.py` | 2008–2072: `_linked`, `playbook`, `rules` |
| `commands/gate_lock.py` | 2073–2205: `_lock_holder`, `_LongGateLock` |
| `commands/gate.py` | 2207–2384: the run and stop files, `_gate_stop`, `gate` |
| `commands/delivery.py` | 2382–2535: `VERDICTS`, `verdict`, `ship`, `stack`, `release`, `cancel` |
| `commands/closing.py` | 2536–2743: `pause`, `close`, `_close_target`, `_retro_target`, `_batch_files`, `_archive_and_delete`, `_final_rows`, `_final_pages`, `TO_DATE` |
| `commands/cost/pricing.py` | 2744–2837: `_prices`, the unpriced sums, `_spend`, `_hints`, `_cost_rows`, `_window` |
| `commands/cost/sessions.py` | 2838–2934: `_claimed`, `_foreman_uuid`, `_chief_unknown`, `_chief_line`, `OWN_CHIEF`, `OWN_FOREMAN`, `STEER_OUT`, `GRILL_OUT`, `WHOLE` |
| `commands/cost/breakdown.py` | 2935–3139: `_cost_groups`, `_apportion`, `_kind`, `_label`, `_steers`, `_breakdown`, `_restarted`, `_explain`, `_cost_summary`, `_orchestration`, `COMPACTION_USD`, `STEERING`, `UNSPLIT`, `EXPIRY_NOTE` |
| `commands/cost/command.py` | 3140–3198: `cost` |
| `commands/forge_stack.py` | today's `forge_stack.py`. It imports `_chain` from `commands/facts.py`, not from a module of a higher layer. |
| `board/collect.py` | `board.py` split, still standard library: `collect`, `_tail_events`, `settings` |
| `board/render.py` | `page`, `render_body`, the row helpers, the escaping |
| `board/server.py` | `_handler`, `_Server`, `serve`, `_probe`, `is_loopback`, `board` |

**Layer 4: `cli.py`.** It holds `main()`: UTF-8 streams, parse, the one spelling of a CR,
dispatch, and the ten-line cap with `FULL_OUTPUT`. `_parser` builds the root parser and the
shared options (`--project`, `--batch`, `--epoch`), then calls each command module's `register`.
`__main__.py` and `chantier.py` stay the entry points.

Names that today start with `_` but are used from another module drop the `_` once they live in
their own module, for example `_SAMPLES`, `_breakdown`, `_kind`, `_label`, `_read_seat` and
`_chain`. No compatibility re-export is kept: the tests and the scenario import the new paths.

**No import cycle.** No module imports inside a function to dodge a cycle. Three places do it
today:

- `state.Repo.find` imports `lifecycle.convert_old_tree`.
- `state.Batch.__exit__` imports `status.write_batch`/`write_dashboard`.
- `lifecycle.write_dashboard_after_rename` imports `status.write_dashboard`.

These are resolved by structure. `Batch` saves the record. The STATUS rewrite after a save, and
the conversion of an old tree on the first run, are called from a layer that may import both.
For example, `Batch` can take a callback given by the layer above, or a function in layer 2 can
open, save and render. The lazy imports of `ruamel.yaml` and `psutil` are not cycles; they are
declared as in "Dependencies".

## Targets (answer 8)

At the end of this CR, every file of "Scope" meets these targets:

- **File:** at most 400 lines, one responsibility per module, no import cycle.
- **Function:** at most 50 lines, cyclomatic complexity at most 10 (ruff `C901`, `max-complexity
  = 10`). At most 5 arguments (`PLR0913`, and `PLR0917` for positional ones), 12 branches
  (`PLR0912`), 6 returns (`PLR0911`) and 50 statements (`PLR0915`). Nesting at most 3 levels
  (`PLR1702` with `max-nested-blocks = 3`, enabled alone through `explicit-preview-rules` while
  it is a preview rule).
- **Style:** `ruff format`, and `ruff check` with `E`, `W`, `F`, `I`, `B`, `UP`, `SIM`, `C90`, `PL`
  and `RUF`, clean. Line length is 100. No blanket `noqa`: `PGH004` is selected to enforce it, and
  `RUF100` removes the unused ones. No rule of those families is turned off in the configuration.
  A `# noqa: <code>` names its code and says why on the same line. One configuration entry is
  needed: `lint.allowed-confusables` for the characters the CLI prints today (`→`, `…`, `–`;
  `RUF001`), because the output is behaviour.
- **Types:** every function annotated, `mypy --strict` clean. `copilot_session_usage` has no type
  information, so it gets a per-module `ignore_missing_imports` override, the only one. The
  pydantic mypy plugin is on.
- **Behaviour unchanged:** see "Behaviour kept".

Today's distance from the targets, measured on 2026-11-13 with ruff 0.17.5 over `src`, `tests`,
`chantier.py` and `session_usage.py` with the rules above: 294 findings. The main ones are 121
`E501`, 25 `PLR2004`, 21 `C901`, 20 `RUF005`, 13 `PLR0912`, 10 `PLC0415`, 9 `PLW1510`, 7
`PLR0915`, 5 `PLR0913` and 2 `PLR0911`. 16 files would be reformatted. 18 functions are over 50
lines, among them `cli._parser` (214), `_apply_order` (171), `lifecycle._convert` (108),
`costs.usage` (106) and `gate` (101). Over 400 lines are:

- `commands.py` (3,198)
- `state.py` (611)
- `playbook.py` (527)
- `test_structure.py` (520)
- `costs.py` (497)
- `status.py` (490)
- `board.py` (418)
- `lifecycle.py` (409)

`PLR2004` (magic values) is met with named constants, not with ignores.

## `just check` and the tools

- The `justfile` gets a `lint` recipe, and `check` becomes `check: lint test release-notes`.
  `lint` runs from `skills/chantier/scripts/cli`. Each tool's version is pinned once, in a
  variable of the `justfile`.
  - `uvx ruff@<pin> format --check .`
  - `uvx ruff@<pin> check .`
  - `uvx --with-requirements chantier.py --from mypy==<pin> mypy --strict …`, which installs the
    script's own dependencies beside mypy (checked to work with uv 0.13.6), or an equivalent
    that types against the versions the lock pins.
  - `uv lock --script chantier.py --check`: the lock matches the block.
- The configuration (`[tool.ruff]`, `[tool.mypy]`) lives in the CLI's `pyproject.toml`. Ruff
  run from that folder therefore covers exactly "Scope", and the rest of the repository is not
  checked.
- `just test` runs pytest in the CLI project's environment, which now has the dependencies.
- `just scenario`: `uv run --no-project --with-requirements
  skills/chantier/scripts/cli/chantier.py python scenario/run_scenario.py --forge …`. The
  scenario keeps running the CLI as `sys.executable -m chantier` and imports its modules
  in-process, so its interpreter needs the dependencies.
- `just eval-dry-run`: the same `--with-requirements`, for `dry_run.py`'s `python chantier.py`
  calls.
- No user installs anything: `uv`, `just` and `git` stay the only tools (CONTRIBUTING "Set up").

## Tests

The structure tests stay few (`AGENTS.md`).

- `tests/test_structure.py` (520 lines) is split by subject into files of at most 400 lines,
  with the same tests. For example: `test_plugin_files.py` (versions, manifests, agents, model
  table, references, hosts, byte-order marks, release scan), `test_cli_runs.py` (the smoke runs:
  seat, no setup, external surface, direct and Foreman batches, preflight allow rules, `init`),
  and `test_cli_units.py` (CR spelling, gate and verdict at a head, the cost breakdown, the
  sandbox checks). The imports follow the moved names. `conftest.py` and `test_costs.py` meet the
  targets too.
- At most two tests are added, in `tests/test_code_targets.py`:
  1. **Sizes and imports.** For every `.py` file of "Scope", through `ast`: at most 400 lines
     per file and at most 50 lines per function. The import graph of `chantier.*`, with the
     imports inside functions counted, has no cycle. A failure names the file, the function or
     the cycle.
  2. **The dependency lists agree.** The PEP 723 block of `chantier.py` (read with `tomllib`, as
     `test_copilot_cost_helper_declares_pypi` reads `session_usage.py`'s) names the same
     packages as `pyproject.toml`'s `[project] dependencies`, and holds `no-build = true`.

## Behaviour kept

The refactor changes no output, exit code, file or rule, except the wording named in open
point 1.

- **Commands:** every command, option, help text, output line, ten-line cap and exit code is
  as today. The `--project` option is accepted before and after the command (the
  `argparse.SUPPRESS` subparser option is kept).
- **The views:** `STATUS.md` and `STATUS.json` (schema 3, read by `hooks/register.tsx`'s pane),
  the dashboard and the final pages stay byte-identical for the same record. The pane therefore
  draws the same thing, and `AGENTS.md`'s screenshot rule is not triggered. If the Driver finds
  a byte that must change, it stops and says so: that would be a change to what the pane shows,
  outside this CR.
- **The records:** a `batch.json` written by 0.9.0 reads and continues under the new code, with
  every key and value kept on write. Key order may change on the first write (models dump their
  declared fields first). `events.jsonl` lines keep their keys and values. The old words
  (`landed`, `open`) still read.
- **A batch already running:** the plugin runs live from the main checkout, so the merge of this
  CR switches a running batch to the new code between two commands. The locks keep the same
  files and mechanisms (`fcntl`/`msvcrt` on byte 0), so an old and a new process exclude each
  other.
- **`chantier.yaml`:** each refusal of scenario S4 keeps its line and words. Every valid file
  resolves to the same playbook.

## `AGENTS.md`

There are two edits, and nothing else changes there:

- "The CLI has no dependencies and must stay portable (POSIX and Windows, UTF-8 everywhere)."
  becomes: "The CLI's dependencies are Python packages declared in its scripts' PEP 723 inline
  metadata and locked beside them; uv installs them at the first run, with no install by the
  user. A dependency ships wheels for Linux, macOS and Windows and replaces hand-written code.
  The CLI stays portable (POSIX and Windows, UTF-8 everywhere)."
- The board's "it writes no file, uses the standard library only and knows no role" becomes
  "it writes no file, takes its dependencies through the CLI's PEP 723 inline metadata like the
  rest of the CLI, and knows no role".

## `CONTRIBUTING.md`, `README.md` and docstrings

- **`CONTRIBUTING.md`, item 2** (lines 69–70): "plain Python with no dependency, run by `uv run
  --script`" becomes Python whose dependencies are declared in `chantier.py`'s PEP 723 block and
  locked in `chantier.py.lock`, run by `uv run --script`.
- **`CONTRIBUTING.md`, lines 84–86:** the board line is changed as in `AGENTS.md`.
- **`CONTRIBUTING.md`, "Set up":** uv fetches Python, the CLI's dependencies and the check tools.
- **`CONTRIBUTING.md`, new section "Code standards"** (after "Daily work"):
  - the targets of answer 8, and that `just check` enforces them through `just lint`;
  - the layers of "The package layout";
  - the rule that a dependency must replace hand-written code and ship wheels for the three
    systems;
  - `uv lock --script chantier.py` after a change to the block;
  - that the board CRs add the JS and CSS targets with their linter.
- **`CONTRIBUTING.md`, repository layout:** the `scripts/cli/` line names `chantier.py.lock`.
- **`README.md`, line 208:** after "the only thing to install is `uv`", add that the first run
  fetches the CLI's Python packages, so it needs the network once, and that uv's cache is
  enough after that (answer 3).
- **Docstrings:** they no longer say "no dependency" or "standard library only":
  - the header of `commands.py`, which moves to `commands/__init__.py`;
  - `playbook.py`'s first paragraph;
  - `board.py`'s;
  - `session_usage.py`'s "the rest of the CLI has no dependency".

## Out of scope

- The board's web framework, its routes, live updates, ES modules and screenshots with
  Playwright: `visualization-backend` and the board CRs after it (answer 4). Here `board.py` is
  only split to meet the targets, still on `http.server`.
- The JS and CSS targets and their linter (answer 8, last item): the board CRs.
- Holding `scenario/`, `evals/kit/` and `scripts/` to the targets. `run_scenario.py` is 5,277
  lines. A later CR may do it.
- Any new command, option, output or rule. Any change to the cards, the agents, `hooks/` or
  `types/` (so no `just mod`). Any change to `.github/workflows/ci.yml`.
- A version bump: the release process does it.
- Widening what `cancel` finds on Windows (see open point 3).

## CI

`.github/workflows/ci.yml` does not change, but what its recipes run does. The `check` job runs
`just check`, now with `lint`, on `ubuntu-latest`, `macos-15-intel` (named `macos-latest`,
`continue-on-error`) and `windows-latest`. The `scenario` and `eval-dry-run` jobs run on
`ubuntu-latest`. On those runners:

- uv comes from `astral-sh/setup-uv`, with an empty cache at each run.
- The network is available.
- uv chooses the Python, as on a user's machine: the newest it has or downloads that meets
  `>=3.11`.
- There is no `claude` binary.

Compared with the local machine, the runners have no warm uv cache, no ruff, mypy or packages
already downloaded, and a different system and Python.

CONTRIBUTING's cold-cache rule binds a change to a job's steps. Here the steps are the same, but
the recipes now fetch packages, so the same proof is taken: E6 below. Only the first CI run can
prove the rest:

- the wheels of the locked versions on Linux x86_64 and macOS Intel;
- the cold `uvx` fetch of ruff and mypy on each runner;
- the `--with-requirements` environment of `just scenario` and `just eval-dry-run` on Linux.

## Evidence

The Verifier keeps each item in `work/verifier/evidence/`, and the PR body quotes them.

- **E1.** `just check` passes on the Windows machine, then in CI on Linux, macOS and Windows, with
  `lint` in it. Its output shows 0 ruff findings, 0 mypy errors and the two new tests passing.
  For contrast, the same `lint` recipe run against `main`'s code fails with the counts above.
- **E2.** `just scenario` passes on both forges on `main` before the work starts (the head's
  short SHA is recorded) and on the branch's head. `git diff main -- scenario/` shows only import
  paths. CI's `scenario` job is green. The scenario's process steps (`cancel`, `gate --stop`, the
  long gate queue) prove the psutil rewrite. `just scenario` also passes on the Windows dev
  machine, because CI runs it on Linux only and `procs.py` differs per system.
- **E3.** `just eval-dry-run` passes, because its recipe changed. CI's `eval-dry-run` job is green.
- **E4. A running batch survives the upgrade.** In a scratch repository outside this one:
  1. With `main`'s CLI (`git worktree` of `main`): `open` a batch of two CRs, `take` one, `round`,
     `note`, and record an order and an ask.
  2. Then with the branch's CLI on the same planning folder: `status --refresh`, `round`,
     `handback ready`, `ship`, `order merged`, `pause`, `close --yes`.
  
  Every command gives the same lines as `main`'s CLI gives on a copy of the same folder.
  `batch.json` before and after the first write of the branch is equal as JSON, key order apart.
- **E5. The views are byte-identical.** From copies of the planning folders of E4 and of a
  `just scenario` run kept on disk, `STATUS.md`, `STATUS.json`, the dashboard and a closed
  batch's final pages are rendered by `main`'s code and by the branch's, then compared byte for
  byte (`cmp`/`fc /b`): no difference.
- **E6. A fresh machine.** On Windows, with `UV_CACHE_DIR` set to a new empty folder outside the
  repository, the same for every step:
  1. `uv run --script skills/chantier/scripts/cli/chantier.py --version` installs from wheels only
     and prints the version.
  2. `just check`, `just scenario` and `just eval-dry-run` pass.
  3. The same `--version` with `UV_OFFLINE=1` passes from that cache (answer 3).
  
  `just check` also passes with `UV_PYTHON=3.11` (the floor).
- **E7. Start-up time.** The wall time of `chantier --version` and of `chantier status` in a
  repository with a running batch, warm cache, on Windows. The median of ten runs each, for
  `main` and for the branch, goes in the PR body. No threshold is set (open point 6).
- **E8. `chantier.yaml`.** Scenario S4 passes (the eight structural refusals, with their lines).
  The PR body adds a table of the lexical errors whose words change: the message on `main` and
  on the branch for an unclosed single quote, an unclosed double quote, a bad escape, and a
  plain value holding `: `. Each keeps its `chantier.yaml:<line>:` prefix and exit 2.

## Open points (defaults taken, for the Chief of Staff to confirm with the user)

1. **YAML library and wording.** The default is `ruamel.yaml`, not PyYAML, because PyYAML has
   no CPython 3.15 wheel on Windows (measured). The structural refusals keep their words. The
   lexical errors (unclosed quote, bad escape, `: ` in a plain value) take ruamel's words, with
   the same line and exit code. Double-quoted escapes other than `\"` and `\\` become accepted,
   since they are valid YAML. Otherwise, the hand-written parser stays and only its style is
   brought to the targets.
2. **Argument parsing.** The default keeps `argparse` and gives each command module its own
   `register`. A parsing library would change the usage errors that the scenario and the agents
   read. The user's examples named "argument parsing" as a candidate.
3. **`cancel` on Windows.** psutil can read a Windows process's directory, which today's code
   cannot. The default keeps today's rule (command line only on Windows), for no change of
   behaviour. Widening it is a later CR.
4. **Package index.** The default declares no index in `chantier.py`, so the user's own uv
   configuration applies, as for any uv script. This differs from `session_usage.py`, which
   chantier runs with `--no-config` and a pinned PyPI index. A user whose network reaches
   packages only through a mirror then uses the mirror. The alternative is to pin PyPI as
   `session_usage.py` does.
5. **Newest Python without wheels.** The default keeps `requires-python = ">=3.11"`, with no
   upper bound, and `no-build = true`. When a new CPython ships before `pydantic-core` publishes
   its wheel, the CLI fails at once with uv's message. The alternative is an upper bound raised
   at each Python release.
6. **Start-up budget.** No threshold was set. The default is lazy imports and the figure
   reported in the PR (E7). The user may set one.
7. **Where the targets are written.** The default puts them in `CONTRIBUTING.md` ("Code
   standards") and enforces them in `just check`. `AGENTS.md` gets only the two edits of answer
   6. The alternative adds one line to `AGENTS.md` pointing to them.
8. **Tests in the targets.** The default holds `tests/*.py`, which live under `skills/`, to the
   targets, `mypy --strict` included.
9. **The lock file.** The default commits `chantier.py.lock`, so users run the versions CI ran.
   `just check` refuses a stale lock.
