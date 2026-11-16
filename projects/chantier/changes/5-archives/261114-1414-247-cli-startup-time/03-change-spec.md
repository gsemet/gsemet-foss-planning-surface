# Change Specification: the CLI starts as fast as it did before CR-221

## Goal

The user's words (2026-11-14, `intake/request.md`): "70 minutes ? Pourquoi est-il aussi long ?".
Since CR-221 (`python-inline-deps`), every `chantier` command starts slower, so every long gate
(`just scenario`, about 1,000 CLI calls per forge) and every agent's `$CHANTIER` call pays the
difference. The measured figures: a long gate went from about 700 s to about 1,075 s per forge
(+55 %, +12 minutes per gate, about +2.5 hours over batch-17's 13 gates). `uv run --script
chantier.py --help` went from 264–444 ms (at `2d9a2aa`) to 489–562 ms (at `ff701a9`).

This CR:

- measures where the start-up time goes, per command;
- brings the start-up back to the level before CR-221, within about 10 % (answer 2), and keeps the
  CLI's declared dependencies and its pydantic records;
- adds a structure test that fails when a simple command imports a heavy library at start
  (answer 3), so a later refactor cannot slow the CLI down without anyone noticing.

The CR has no `issue:` line.

## Decisions carried from `02-answers.md`

| Decision | Where this spec carries it |
| --- | --- |
| 1. P1, grilled and specified, then added at the end of batch-17's stack | "Where this CR stands" |
| 2. Back to the start-up before CR-221, within about 10 %. Keep the dependencies and the pydantic records. Chosen over "as fast as possible" | "The target", "What changes", "Out of scope" |
| 3. A structure test: a simple command imports none of the heavy libraries at start. It is deterministic and does not depend on the machine's speed. Chosen over a time threshold in `just check` | "The guard" |
| 4. Grilled enough, after the full restatement | (this specification) |
| 5. Commands that read a record: each command imports what it needs lazily, when it runs. The target is met when `--version` and `--help` are within about 10 % of `2d9a2aa`, and every other command comes as close as it can, at worst at the measured pydantic import floor, which the PR reports. No follow-up CR on pydantic's import cost | "The target", "What changes" (section 1), "Out of scope" |
| 6. CR-237's launch cost: the PR measures uv's share of the launch agents use and reports it. This CR leaves the launch alone, with no follow-up CR | "The target", "Out of scope", E1 |

## Where this CR stands

- The CR joins batch-17's stack at its end, after CR-246. Its branch starts from the top of the
  stack. It is written against the code that the CRs under it leave. Two of them touch the CLI's
  entry and launch:
  - **CR-237 (`root-pyproject-launch`, PR #171, ready)** sets the launch. In chantier's own
    checkout (dev mode), `$CHANTIER` is `uv run --locked --project "<plugin root>" chantier`. In a
    host's plugin copy (plugin mode), it is `uvx --from "<plugin root>" chantier --skill "<skill>"`.
    CR-237 also adds the root `pyproject.toml` and `uv.lock`, deletes the PEP 723 entry
    `skills/chantier/scripts/cli/chantier.py`, adds the global option `--skill` (in `cli.py` and in
    `commands/registry.add_command`, and stored in `plugin_files.SKILL`), and sets the `justfile`'s
    `run-cli := "uv run --locked python"`.
    **This CR changes none of that.** It keeps the two launch forms, the `SKILL.md` text, the root
    `pyproject.toml`'s dependencies and the lock. It changes only what Python imports between the
    process's start and the call of the chosen command's handler. The request's "PEP 723
    dependencies" refers to the layout before CR-237. After CR-237 the rule is the root
    `pyproject.toml`, and this CR keeps it.
  - **CR-222 (`visualization-backend`, PR #174, in CI)** replaces `board/server.py` with the
    `board/` package (`command.py`, `address.py`, `app.py`, `routes.py`, `state.py`, …). It adds
    `starlette==1.10.0` and `uvicorn==0.54.0` to the root `pyproject.toml`, and adds both to ruff's
    `banned-module-level-imports`, so they load only in `board/app.py` when the board serves. But
    `cli.py` imports `chantier.board.command` at start. That module imports `board/address.py`
    (`urllib.request`, and through it `http.client` and `email`) and `board/app.py`, whatever the
    command. **This CR moves that cost behind the `board` command.** `board`'s options, help and
    behaviour stay as CR-222 and the board CRs above it (225–228) leave them.
- The other CRs of the stack (223, 225–228, 232–235, 238–246) may add commands, options or modules.
  This CR's rules apply to every command module present at the branch's base. If a name below has
  moved on the base, the Driver uses the base's name and says so in the PR.

## Where the time goes (measured 2026-11-14)

Measured on Windows 11, Python 3.15.2 (CR-222's worktree `.venv`), uv 0.13.6, warm, with
`PYTHONPYCACHEPREFIX` in a scratch folder. Each figure is the sorted wall times of 7 runs. The
machine was loaded (a gate was running), so the absolute figures run higher than the request's.
The differences are what count.

| What runs | Wall time (ms) |
| --- | --- |
| `python -c pass` | 33–46 |
| `python -m chantier --version`, source at `2d9a2aa` (before CR-221) | 405–423 |
| `python -m chantier --version`, source at `main` `ff701a9` | 685–724 |
| `python -m chantier --version`, source at CR-222's head `c8dc8e4` (on CR-237) | 681–725 |
| `uv run --script <empty PEP 723 script>` (no dependencies) | 54–74 |
| `uv run --script <the same script with the three CLI dependencies>` | 55–57 |
| `uv run --script skills/chantier/scripts/cli/chantier.py --version` at `main` | 720–786 |
| `python -c "import pydantic"` | 210–216 |
| `python -c "from pydantic import BaseModel"` | 339–350 |
| `python -c "import chantier.core.records"` (CR-222 head) | 447–478 |
| `python -c "import chantier.core.repo, chantier.status.views, chantier.status.write"` (a `status`-like chain) | 491–512 |

What this shows, and what the Driver confirms with its own measurements (E1):

- **uv is not the cause.** `uv run --script` adds about 20–30 ms whether the script declares the
  three dependencies or none. The lock check of the request's hypothesis costs no measurable time.
  `just scenario` runs `python -m chantier` directly (`scenario/run_scenario.py`, `Work.run` near
  line 137, with `PYTHONPATH` set to `src/`), with no uv at all, and it still lost 55 %.
- **The imports are the cause.** `chantier.cli` imports every command module at start (its
  `from chantier.commands import (…)` block, `board.command`, `commands.cost.command`) to build the
  parser. Through `plugin_files` (which imports `core.records.CrEntry`) and `cli.py`'s own
  `from chantier.core.records import normalize_cr`, every command, `--version` and `--help`
  included, imports pydantic and builds the twelve models of `core/records.py`. `-X importtime` at
  CR-222's head: `chantier.cli` 407 ms cumulative. Of that, `chantier.plugin_files` takes 259 ms
  and `chantier.core.records` 239 ms (pydantic 72 ms, and the models' schema building, through
  `pydantic._internal._generate_schema`). `chantier.board.command` takes 91 ms (`board.app`,
  `board.address`, `urllib.request`, `http.client`).
- **`ruamel.yaml` and `psutil` are already lazy.** `playbook/yaml_subset.py` and `procs.py` import
  them inside their functions, and ruff's `banned-module-level-imports` enforces it. `starlette`
  and `uvicorn` are lazy in `board/app.py` on CR-222.
- **Before CR-221 the CLI also imported everything at start**, all from the standard library:
  `board` 284 ms cumulative, `argparse` 61 ms, `urllib.request` 70 ms. So making the start-up lazy
  saves more than pydantic's cost for a command that does not need the board's or another
  command's modules.

## The target

- **Measured:** for each command of the measured set (E1), the median wall time of ten warm runs
  at the branch's head, against the same command at `2d9a2aa`, on the same machine and in the same
  sitting. The target is the head's median at most 10 % above `2d9a2aa`'s.
- **Two launches are measured**:
  - the direct one, `python -m chantier`, which the scenario and the tests use;
  - the launch an agent uses, which is `uv run --script <skill>/scripts/cli/chantier.py` at
    `2d9a2aa` and CR-237's dev form `uv run --locked --project "<root>" chantier` at the head.
- **The measured set:** `--version`, `--help`, `status` and `rules` in a scratch project with one
  running batch. To these the Driver adds the three commands the scenario calls most, counted from
  the `Work.run` and `subprocess` calls of `scenario/run_scenario.py` (or from a run's log), and
  names them in the PR.
- **When the target is met (answer 5).** `--version` and `--help` must each be within about 10 %
  of `2d9a2aa`, for both launches. Every other command of the set comes as close as it can, and at
  worst sits at the measured pydantic import floor. A command that reads a record keeps reading it
  through `core/records.py`'s pydantic models, so it pays pydantic's import, and each command
  imports what it needs lazily, when it runs. The Driver does not work around the floor (no record
  read as a plain dict, no second reader). The PR measures the floor (the cost of `from pydantic
  import BaseModel` and of building the models the command uses, over a bare interpreter) and
  reports it beside each command that sits above 10 %.
- **uv's share (answer 6).** The PR measures uv's share of the launch agents use (CR-237's dev
  form, and its plugin form `uvx --from "<plugin root>"`) and reports it. Whatever it measures, this
  CR leaves the launch as CR-237 set it.

## What changes

### 1. The start-up imports only the standard library and chantier's light modules

From the process's start to the call of the chosen command's handler (`args.fn(args)` in
`cli.main`), Python imports:

- the standard library;
- `chantier`, `chantier.cli`, `chantier.commands.registry`, `chantier.core.errors`;
- the modules that declare the commands' parsers, and the modules those import, provided none of
  them imports a third-party package or a command's handler chain.

How the Driver gets there is its choice, within these constraints:

- **The parser stays the same.** `chantier --help`, `chantier <command> --help` for every command,
  the commands' names, options, defaults, `--project` and `--skill` before and after the command
  (`add_command`'s `argparse.SUPPRESS` options), `--batch`, `--epoch`, the exit codes, and the
  error text of a usage error are all byte for byte as on the base (E3).
- **A command's handler module loads when that command runs**, not before. This covers
  `commands/*.py`, `commands/cost/command.py`, `board/command.py` and the rest of `board/`. One way
  to do it: each module's `register(sub)` stays where it is, and the handler is named by its module
  path and resolved at dispatch. Another: the `register` functions move into light modules apart
  from their handlers. Either way, `cli.py` holds no `from chantier.commands import (…)` of handler
  modules at its top.
- **`normalize_cr` and `normalize_batch`** (in `core/records.py` today, used by `cli._one_spelling_of_a_cr`
  at every start) move to a light module, for example `core/ids.py`, with no pydantic import.
  `core/records.py` re-exports them or its callers import the new module. The `core/records.py`
  docstring ("and the ids of batches and CRs") follows.
- **`plugin_files`** is no longer imported at start for `plugin_files.SKILL = args.skill`. The value
  is stored where `skill_dir()` reads it without importing `core.records` at start: in a light
  module, or with `plugin_files`'s own `CrEntry` import moved to the function that needs it. The
  same goes for `repo.PROJECT = args.project`: `core/repo.py` is imported at start only if it
  imports no third-party package.
- **`FULL_OUTPUT`, `MAX_LINES`** and the output rules of `cli.main` are unchanged.
- **The layer rules of CR-221 hold**: no import cycle, 400 lines a file, 50 a function, ruff and
  mypy strict at zero (`tests/test_code_targets.py`, `just lint`). The lazy loads keep mypy's types:
  a handler resolved by name is typed as `Handler` (`commands/registry.py`).

### 2. The pydantic models cost no more than the command uses

- The models of `core/records.py` stay pydantic models with the same fields, `extra="allow"`, and
  `to_data`, `unset` and `append`. Every read and write of `batch.json`, `events.jsonl`,
  `seat.json`, `.long-gate.run` and `restored.json` goes through them, as on the base.
- If the Driver measures a gain, the models are built at their first use instead of at import, for
  example with pydantic's `defer_build=True` in `Record.model_config`. A model that a command never
  validates then costs that command nothing. Whether a deferred build is kept is decided by the
  measurement (E1). The PR gives the figure either way.
- `pydantic.mypy` (the mypy plugin) and the models' behaviour are unchanged. The scenario's record
  checks pass as they are.

### 3. The board's cost stays in `board`

- `board`'s heavy imports (`urllib.request`, `http.client`, `socket`, `ipaddress`, and `starlette`
  and `uvicorn` through `board/app.py`) load only when `board` runs. This applies to every module
  of `board/` that the CRs under this one leave.
- ruff's `banned-module-level-imports` keeps `ruamel`, `ruamel.yaml`, `psutil`, `starlette` and
  `uvicorn`. The Driver may add `pydantic` with a per-file ignore for `core/records.py` alone, so
  that the linter also states which module imports it. This is optional, and the test of
  "The guard" is the rule.

### 4. `CONTRIBUTING.md`

One sentence in "Code standards", next to CR-221's targets: the CLI's start-up (parsing and
dispatch) imports only the standard library and chantier's own modules. A command imports its
libraries when it runs. `tests/test_code_targets.py` checks it for `--version` and `--help`.

No change to `AGENTS.md`, the cards, the agent files, the `SKILL.md` files, `hooks/` or `types/`.

## The guard (answer 3)

One structure test, in `skills/chantier/scripts/cli/tests/test_code_targets.py` (beside CR-221's
targets), run by `just test` and so by `just check` on the three systems:

- For each of `["--version"]` and `["--help"]`, it starts a **fresh** interpreter
  (`sys.executable`, the test environment's, with `PYTHONPATH` set to the package's `src/` as
  `conftest.py` and the scenario do). That interpreter calls `chantier.cli.main(argv)`, catches the
  `SystemExit` that argparse raises for both, and prints the sorted top-level names of
  `sys.modules`.
- The test fails when a top-level name is none of these:
  - in `sys.stdlib_module_names`;
  - `chantier`;
  - `__main__`;
  - one of the interpreter's own site hooks, named in the test (`_virtualenv`, `_distutils_hack`,
    `sitecustomize`, `usercustomize`).

  Its message names each offending module, for example "`chantier --version` imports pydantic,
  pydantic_core at start: import them in the command that needs them". So a new dependency, or a
  new eager import of an existing one (pydantic, `ruamel.yaml`, psutil, starlette, uvicorn, or any
  later one), fails `just check` with no list to keep up to date.
- It depends on no timing and no machine speed. It reads no planning folder and writes nothing.
- It stays one test function with the two cases, in keeping with "Tests check the structure only".

## Out of scope

- The launch forms, `$CHANTIER`, the `SKILL.md` text, the `--skill` option, the allow rules
  (CR-237's). uv's share of the launch is measured and reported, never changed here, and no
  follow-up CR on the launch is planned (answer 6).
- Replacing pydantic, reading a record without its model, or dropping a dependency (answer 2). No
  follow-up CR on pydantic's import cost (answer 5).
- A time threshold in `just check` or in CI (answer 3 chose the import test).
- What a command does or prints. The STATUS files and the pane are unchanged, so `AGENTS.md`'s
  screenshot rule does not apply. `hooks/` and `types/` are unchanged, so no `just mod`.
- The board's behaviour (CR-222, 225–228).
- `session_usage.py` and its own PEP 723 block.
- `scenario/`, `evals/`: no change. The scenario's duration is a measurement, not a step.
- A version bump.

## CI

`.github/workflows/ci.yml` does not change, and no job is added. The new test runs inside `just
check` on `ubuntu-latest`, `macos-15-intel` and `windows-latest`, with uv from `astral-sh/setup-uv`
and an empty cache, uv's own Python, and the locked environment of the root project (CR-237). Two
things there differ from the local machine: the interpreter's site hooks (a Linux or macOS uv
Python may load a different hook module), and the Python version uv picks. Only the PR's first CI
run proves that the test's list of site hooks is complete on Linux and macOS. The local proof
before the push is E2 on Windows.

## Evidence

The Verifier keeps each item in `work/verifier/evidence/`, and the PR body quotes it.

- **E1. Where the time goes, per command.** On the Windows machine, in one sitting, the PR body
  gives a table for each command of the measured set (see "The target"). Each table holds:
  - the median of ten warm runs at `2d9a2aa`, at the branch's base and at the head, for both
    launches (direct `python -m chantier`, and the agent's launch);
  - uv's share (the agent's launch minus the direct one);
  - the head's top five cumulative importers from `python -X importtime`, against the base's.

  The verdict line says, for each command, whether the head is within 10 % of `2d9a2aa`. It also
  gives the gain of a deferred model build (section 2), measured with and without it.
- **E2. The guard.** `just check` passes on Windows. Then, on a scratch copy of the head, adding
  `import pydantic` at the top of `cli.py` makes the new test fail with a message that names
  `pydantic`. The copy is then dropped. `just check` then passes in CI on the three systems.
- **E3. Same parser.** `chantier --help` and `chantier <command> --help` for every command are
  captured at the base and at the head, and their diff is empty. The same goes for the output and
  exit code of one usage error (`chantier status --no-such-option`) and of an unknown command.
- **E4. The long gate.** `just scenario` passes on both forges at the head, locally and in CI.
  `git diff <base> -- scenario/` is empty. The PR gives each forge's duration and check count
  at the base and at the head, beside the request's figures (about 700 s and 690 s on 2026-11-13,
  about 1,075 s and 1,065 s from 2026-11-14). The scenario has grown since then, so its duration is
  reported, not judged. The target is judged on E1.
- **E5.** `just eval-dry-run` passes, locally and in CI.
- **E6. The agent's launch.** From a cwd outside the checkout:
  `uv run --locked --project "<worktree>" chantier --version` and `… status` in the scratch project
  give the same output as at the base, and `git status` of the worktree stays clean.
