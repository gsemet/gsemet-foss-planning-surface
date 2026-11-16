# Change Specification: one way to run the CLI, a root pyproject.toml, uvx at the pinned release ref, the local code in chantier's own checkout

## Goal

The user's words (`intake/request.md`, 2026-11-13, and `02-answers.md`): there is one way to run the
CLI and the versions stay aligned ("il faut qu'une seule méthode, en s'assurant que les versions
soient bien alignées"). The package is declared once, in a `pyproject.toml` at the repository's
root ("on passe à un pyproject.toml à la racine"). This makes
`uvx --from git+https://github.com/gsemet/chantier@<ref> chantier` work with no `#subdirectory`.
The skill names the ref it launches, and `just version` writes it ("le skill hardcode la version
du ref à utiliser … qui sera utilisé lors de l'uvx git+http"). In chantier's own checkout, the skill
runs the local code, live, and fetches nothing ("en mode dev de chantier lui-même il faut pas que ça
checkout quoi que ce soit").

The same command also serves a launch with no agent and no plugin: the web board started from a
planning surface on a machine where only `uv` is installed.

This CR runs right after CR-221 (`python-inline-deps`). It is written against the layout CR-221
leaves, read from CR-221's branch head `b2c970a` (`chantier.worktrees/batch-17-CR-221`), which has
not merged yet. If CR-221 merges with a different layout, the Driver applies this specification to
the merged layout and names each difference in the PR.

## Decisions carried from `02-answers.md`

| Decision | Where this spec carries it |
| --- | --- |
| 1. One method, aligned versions; no second way to launch the CLI | "The two modes", "What disappears", the test of "Tests" that ties the skill's text to the CLI's |
| 2. CR-221 finishes as specified; this CR follows it in batch-17; the queued Python CRs wait for it | "Order" |
| 3. A root `pyproject.toml`; `uvx --from git+…@<ref> chantier` with no `#subdirectory` | "The root project" |
| 4. The skill pins the ref; `just version` and `just bump-version` write it | "The pinned ref", "`scripts/version.py`" |
| 5. In chantier's own checkout: the local code, live, no fetch. Installed as a plugin: `uvx` at the pinned ref | "The two modes", "Detection" |
| 6. What the answers leave open takes defaults, listed as open points | "Open points" |

## What exists today (the layout CR-221 leaves)

The figures below were measured on 2026-11-13, on CR-221's head.

- **The package.** The source is `skills/chantier/scripts/cli/src/chantier/`, as layered packages:
  `core/`, `commands/`, `board/`, `playbook/`, `status/`, `costs/`, `lifecycle/`, plus
  `plugin_files.py` and `cli.py`. It is declared in `skills/chantier/scripts/cli/pyproject.toml`,
  which holds `[project] dependencies = ["pydantic>=2.11", "ruamel.yaml>=0.18", "psutil>=7"]`, the
  ruff, mypy and pytest configuration, and `[project.scripts] chantier = "chantier.cli:main"`. Its
  lock is `skills/chantier/scripts/cli/uv.lock`.
- **The entry point.** `skills/chantier/scripts/cli/chantier.py` carries a PEP 723 block with the
  same three packages and `[tool.uv] no-build = true`, locked in `chantier.py.lock`. It adds
  `src/` to `sys.path` and calls `chantier.cli.main`. A structure test,
  `tests/test_code_targets.py`, checks that the block and `pyproject.toml` list the same packages.
- **`session_usage.py`** keeps its own PEP 723 block, with its pinned PyPI index, for
  `copilot-session-usage`. `costs/copilot.py` finds it as
  `Path(__file__).resolve().parents[3] / "session_usage.py"`.

Every place that calls the CLI today:

| Site | What it says |
| --- | --- |
| `skills/chantier/SKILL.md` line 16 | `$CHANTIER` means `uv run --script "<this skill's folder>/scripts/cli/chantier.py"` |
| `skills/chief-of-staff/SKILL.md` 21, `skills/griller/SKILL.md` 15, `skills/status/SKILL.md` 15 | the same, with `<../chantier made absolute>` |
| `skills/chantier/references/concepts.md` 205 | `$CHANTIER`: "exactly as your prompt gives it (`uv run --script "<…>/chantier.py"`; …)" |
| `skills/chantier/references/chief-of-staff.md` 453 | the Foreman's prompt: `CLI: uv run --script "<skill>/scripts/cli/chantier.py" <command> --batch <batch>` |
| `skills/chantier/references/hosts/claude-code.md` 131, 133, 180, 196, 215–216, 324 | the `uv` prerequisite, the `python` row, and the allow rule `Bash(uv run --script *chantier.py *)` / `PowerShell(…)` with its row, its block and its unproved auto-mode note |
| `src/chantier/plugin_files.py` `cli_command` | `uv run --script "<skill_dir()>/scripts/cli/chantier.py"` plus ` --project "<folder>"` on a surface; printed as the `cli:` line of `take`'s facts (`commands/facts.py` 116) |
| `src/chantier/commands/permissions.py` `SAMPLES` | `("always", "uv run --script /plugin/skills/chantier/scripts/cli/chantier.py status", "uv run --script *chantier.py *")`: P10's sample and rule |
| `justfile` | `run-cli := "uv run --no-project --with-requirements skills/chantier/scripts/cli/chantier.py python"` for `scenario` and `eval-dry-run`; `test` runs `cd {{cli}}; uv run --group dev pytest`; `lint` runs ruff, mypy (`--with-requirements chantier.py`) and `uv lock --script chantier.py --check` from `{{cli}}` |
| `scenario/run_scenario.py` 82–83, 639 | runs `sys.executable -m chantier` with `PYTHONPATH=<cli>/src` and `CHANTIER_SKILL_DIR`; checks that a fact line starts with `cli: uv run --script` |
| `evals/kit/setup.py` 39, 272, 293 | `CLI = …/chantier.py`; `uv run --script CLI init`; prints `CHANTIER = uv run --script "<CLI>"` |
| `evals/kit/audit.py` 56, 65, 771 | `CLI = …/chantier.py`; the regex `CLI_CALL` recognizes a call by `chantier\.py` or by a variable; `uv run --script CLI cost` |
| `evals/kit/dry_run.py` 23–24, 148, 282 | `[sys.executable, str(CLI)]` with `CHANTIER_SKILL_DIR` |
| `evals/README.md` 77, 190 | `$CHANTIER` is `uv run --script "<this checkout>/skills/chantier/scripts/cli/chantier.py"` |
| `hooks/register.test.tsx` 920 | an example command string, `uv run --script "C:/x/…/chantier.py" note CR-5 "a > b" --batch b`, in a list of commands whose quoted `>` is not a write. It is a fixture, not a call. |

No agent file (`agents/`, `com.github.copilot/agents/`) and no other card names the command: they
say `$CHANTIER`. `hooks/register.tsx` does not parse the CLI's command.

What the CLI needs from the skill folder: `skill_dir()` (`CHANTIER_SKILL_DIR`, else the nearest
parent of `plugin_files.py` holding `SKILL.md`) is read by `skill_version` (preflight P5),
`plugin_root` (`skill_dir().parents[1]` with a plugin manifest), and from there by `agent_problems`
(P4), `plugin_roles` and `read_playbook`. Those in turn serve `open`, `cost`, `preflight`, `rules`
and `playbook`. `skill_dir()` is also read by the `cards:` and `cli:` lines of `take`'s facts. The
board (`board/collect.py`) needs none of them: it reads `chantier.yaml` through `load_board` alone.

## Measurements (Windows 11, uv 0.13.6, 2026-11-13)

These were taken on a copy of CR-221's head with a root `pyproject.toml` added as below
(`packages = ["skills/chantier/scripts/cli/src/chantier"]`, hatchling), and against GitHub's
`v0.9.0` tag with `#subdirectory=skills/chantier/scripts/cli`. Each wall time is for
`chantier --version`, warm cache, five runs.

| Launch | Warm time | Offline after a first run |
| --- | --- | --- |
| `uv run --script <cli>/chantier.py` (today) | 495–608 ms | yes |
| `uv run --project <root> chantier` (editable install in `<root>/.venv`) | 505–566 ms | yes |
| `uvx --from <local folder> chantier` | 514–628 ms | yes |
| `uvx --from git+https://github.com/gsemet/chantier@<full commit SHA>#subdirectory=… chantier` | 792–980 ms | yes |
| `uvx --from git+https://github.com/gsemet/chantier@v0.9.0#subdirectory=… chantier` (a tag) | 1,858–2,091 ms (the first warm run: 4,598 ms) | **no**: "failed to fetch branch or tag `v0.9.0` … Remote Git fetches are not allowed because network connectivity is disabled" |

- **A cold first run** (empty `UV_CACHE_DIR`) takes 5.2 s from a local git URL and 5.7 s from GitHub.
  These times include building chantier with hatchling and downloading the wheels.
- **A tag is fetched again at every call.** `git ls-remote` of the tag alone takes 477–497 ms. A
  full commit SHA is not fetched again.
- **`uvx` ignores the package's `uv.lock`.** The test locked with `--resolution lowest-direct`,
  giving pydantic 2.11.0, psutil 7.0.0 and ruamel.yaml 0.18.0, and committed the lock. `uvx`
  from that commit installed pydantic 2.14.3, psutil 7.2.2 and ruamel.yaml 0.19.1: the newest that
  meet the floors.
- **`uvx --no-build` cannot be used.** It refuses chantier itself ("Building source distributions
  is disabled, but attempted to build `chantier`"), because a git source is always built.
  `[tool.uv] no-build = true` in the root `pyproject.toml` does not stop `uv run --project` from
  building the project itself, so it can stay there for the dependencies.
- **Concurrent runs are safe.** Eight `uv run --locked --project <root> chantier --version` run at
  once, right after a version change that forced a reinstall of chantier, all succeeded.
- **The skill folder is not found under `uvx`.** `uvx --from git+…@v0.9.0#subdirectory=… chantier
  preflight` fails with "error: cannot find the chantier skill folder; set CHANTIER_SKILL_DIR": the
  installed package is in uv's cache, far from any `SKILL.md`.
- **Plugin installs carry no `.git`.** The Claude Code plugin copies in
  `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` have none (chantier 0.1.0 and 0.8.0,
  impeccable 4.9.0). The marketplace clones in `~/.claude/plugins/marketplaces/` do. The user's own
  marketplace `chantier` is a `directory` source on the main checkout, which has `.git`. A Copilot
  install was not available to look at (open point 6).
- **The tag `v0.9.0` has no root `pyproject.toml`.** `git ls-tree v0.9.0` shows only the
  `skills/chantier/scripts/cli/` layout. `main` is 9 commits past `v0.9.0` and still carries version
  0.9.0.

## The root project

- **`pyproject.toml` at the repository's root** becomes the only declaration of the package:
  - `[project]`: `name = "chantier"`, the version, the description and `requires-python = ">=3.11"`.
  - `dependencies`: the three packages of CR-221 (see open point 4 for `==` or `>=`).
  - `[project.scripts] chantier = "chantier.cli:main"`.
  - `[dependency-groups] dev = ["pytest>=8"]`.
  - `[tool.uv] no-build = true`.
  - `[build-system]`: hatchling.
  - `[tool.hatch.build.targets.wheel] packages = ["skills/chantier/scripts/cli/src/chantier"]`.

  The wheel holds the `chantier` package only: no tests, no cards, no `session_usage.py`.
- **The configuration moves there too.** CR-221's `[tool.ruff]`, `[tool.ruff.lint…]`, `[tool.mypy]`
  and `[tool.pytest.ini_options]` move to the root file. Their scope stays exactly CR-221's "Scope":
  - ruff is given the paths `skills/` (or `include` restricts it there), so `scenario/`, `evals/`
    and `scripts/` stay outside the targets, as CR-221 decided;
  - mypy's `files` become `skills/chantier/scripts/cli/src`, `…/tests` and `…/session_usage.py`;
  - pytest's `testpaths` becomes `skills/chantier/scripts/cli/tests`.
- **`uv.lock` at the root** is the only lock. Dev mode, `just test`, `just lint`, `just scenario`
  and `just eval-dry-run` use it (`--locked`). CI therefore runs the locked versions.
- **The source does not move.** It stays in `skills/chantier/scripts/cli/src/chantier/`, and the
  tests stay in `…/tests/`. In dev mode the editable install keeps `plugin_files.py` under the skill,
  so `skill_dir()` still finds `SKILL.md` by its parents. CR-221's layers and targets are unchanged.

## What disappears

| File | Becomes |
| --- | --- |
| `skills/chantier/scripts/cli/chantier.py` (the PEP 723 entry point) | deleted: no mode runs a script any more |
| `skills/chantier/scripts/cli/chantier.py.lock` | deleted: the root `uv.lock` replaces it |
| `skills/chantier/scripts/cli/pyproject.toml` and `…/uv.lock` | deleted: the root files replace them |
| `skills/chantier/scripts/cli/.gitignore` | kept only if it still ignores something the root `.gitignore` does not (the root already ignores `.venv`, `__pycache__/` and `.pytest_cache/`); else deleted |
| `session_usage.py` | **kept**, with its own PEP 723 block, its pinned index and `--no-config`. It is a separate tool that the CLI starts with `uv run --script`, not an entry point of the CLI (open point 8). |
| `scripts/version.py`, `scripts/release_notes.py` (PEP 723, `dependencies = []`) | unchanged: repository tools, not the CLI |

After this CR, no file under `skills/` holds a PEP 723 block except `session_usage.py`.

## The two modes

### Detection

The **plugin root** is the folder two levels above the common skill (`<skill>/../..`, made
absolute). The mode follows one rule, written once in prose in the skill and once in code in the
CLI:

- **Dev mode:** `<plugin root>/.git` exists, as a folder (a clone) or a file (a git worktree). This
  is chantier's own checkout: the main checkout that the user's marketplace points at, or a
  worktree started with `claude --plugin-dir`.
- **Plugin mode:** anything else, such as a host's plugin copy.

### What `$CHANTIER` means

| Mode | `$CHANTIER` |
| --- | --- |
| Dev | `uv run --locked --project "<plugin root>" chantier` |
| Plugin | `uvx --from git+https://github.com/gsemet/chantier@v<version> chantier --skill "<skill folder>"` |

In both modes, a planning surface adds `--project "<the project's folder>"` after `chantier`, as
today.

- **Dev mode runs the local code, live.** uv installs the package in editable mode in
  `<plugin root>/.venv`, as measured: a `.pth` file points at `…/scripts/cli/src`. So an edit or a
  fast-forward of the main checkout runs at the next call, with no fetch, no reinstall and no
  network once the dependencies are in uv's cache. `--locked` refuses a `uv.lock` that no longer
  matches `pyproject.toml` with uv's own message. It never rewrites the lock in the main checkout,
  so that checkout stays clean for the fast-forward after a merge. `.venv` is already ignored by
  the root `.gitignore`.
- **Plugin mode runs the release the skill names.** `<version>` is the plugin's version, written
  by `just version` (see "The pinned ref"). `--skill` gives the CLI the plugin's own skill folder.
  Through it the CLI reaches the cards, the plugin's agents (P4, the roles of `chantier.yaml`) and
  `session_usage.py`, which the package fetched by `uvx` does not contain.
- **No mode falls back to the other.** A failed `uvx` (offline with a tag, a tag not yet pushed)
  fails with uv's message. The agent reports it, as for any other refused tool.

### The skill's text

The four `SKILL.md` files (`chantier`, `chief-of-staff`, `griller`, `status`) replace their
`$CHANTIER means uv run --script …` sentence with the rule above. They keep each file's own way of
naming the common skill: "this skill's folder", or "`../chantier` made absolute". The sentence
names:

- the `.git` test;
- the two exact forms, with the literal ref `@v<version>` (for example `@v0.10.0`);
- that the mode is checked once, at the session's start.

Their "Nothing to install or set up" sentence stays true and gains one clause: in plugin mode the
first call fetches the CLI from GitHub, and every call needs the network (see open point 1 for the
tag).

### The CLI

- **A global option `--skill <folder>`**, parsed like `--project`: accepted before and after the
  command, through the same `argparse.SUPPRESS` subparser option. `skill_dir()` reads, in order:
  1. `--skill`;
  2. `CHANTIER_SKILL_DIR`, which the tests, the scenario and the dry run keep using;
  3. the parents of `plugin_files.py`, as in dev mode.

  The error when none applies becomes "cannot find the chantier skill folder: pass --skill <the
  skill's folder>". It keeps exit code `EXIT_PRECONDITION`.
- **`cli_command(repo)`** returns the form of the mode, by the same `.git` test on
  `skill_dir().parents[1]`. In plugin mode the ref is `v{__version__}` and `--skill` is
  `skill_dir()` as POSIX text; the surface's `--project` comes after. The `cli:` line of `take`'s
  facts therefore gives every Driver the same `$CHANTIER` as the skill.
- **`costs/copilot.py`** finds `session_usage.py` as `skill_dir() / "scripts" / "cli" /
  "session_usage.py"`, no longer through `__file__`. Its uv call is unchanged.
- **The board needs no skill folder.** `chantier --project <surface folder> board` must run under
  `uvx` on a machine with no plugin, as must `status` and the other commands that never call
  `skill_dir()`. A command that needs the skill folder and has none fails with the message above,
  never with a traceback.

### The commands of this repository's tools

| Site | Becomes |
| --- | --- |
| `justfile` `run-cli` | `uv run --locked python` (from the root: the project's environment, chantier installed) for `scenario` and `eval-dry-run` |
| `justfile` `test` | `uv run --locked --group dev pytest {{args}}` from the root |
| `justfile` `lint` | ruff on `skills/` from the root; mypy against the locked dependencies (for example `uv run --locked --group dev --with mypy==<pin> mypy`, or an equivalent the Driver measures); `uv lock --check` in place of `uv lock --script chantier.py --check` |
| `scenario/run_scenario.py` 639 | the `cli:` check expects the dev form (`cli: uv run --locked --project `), because the scenario's skill is in a git checkout. The `PYTHONPATH` and `CHANTIER_SKILL_DIR` of line 82 stay. |
| `evals/kit/setup.py` 39, 272, 293 | `CLI` names the package's source or the root. `init` and the printed `CHANTIER` use the dev form on this checkout (an eval's workspace gets the plugin from the user's own install, which is this checkout, so it runs in dev mode). |
| `evals/kit/audit.py` 56, 65, 771 | `CLI_CALL` also recognizes a call as `chantier` after `uv run … --project …` or `uvx --from …`, besides `chantier.py` (old logs) and a variable. The `cost` call uses the dev form. |
| `evals/kit/dry_run.py` | runs `[sys.executable, "-m", "chantier", …]` under the recipe's `uv run --locked`, with its `CHANTIER_SKILL_DIR`; its docstring (lines 23–24) follows |
| `evals/README.md` 77, 190 | `$CHANTIER` is the dev form on this checkout |
| `hooks/register.test.tsx` 920 | **unchanged.** It is a string fixture for the quoted `>` rule, and it is still a valid command line. So `hooks/` does not change and `just mod` is not owed. |

## The pinned ref

- The ref is the release tag `v<version>` (answer 4), written literally in the four `SKILL.md`
  files. `cli_command` derives it from `__version__`, so the CLI holds no second copy to rewrite.
- The tag exists once `just tag` has pushed it after the release PR's merge (CONTRIBUTING,
  Release, step 4). Between a version bump and its tag, plugin mode at that version cannot fetch,
  and fails with uv's message. Users install the plugin after the release, so this window matters
  only to someone who installs from `main` in those minutes.

### `scripts/version.py`

`TARGETS` changes:

- `CLI / "pyproject.toml"` becomes `ROOT / "pyproject.toml"`, with the same pattern.
- `CLI / "uv.lock"` becomes `ROOT / "uv.lock"`, with the same pattern.
- Four new targets, one per `SKILL.md` (`skills/chantier`, `chief-of-staff`, `griller`, `status`):
  the pattern `chantier@v{V} chantier`, one match each. A `SKILL.md` whose ref disagrees with the
  current version makes `set` and `bump` write nothing, as for any target today.
- The pattern list in the module docstring is unchanged; `show` and `check-tag` are unchanged.

`just version`, `just bump-version` and `just release` then move the ref with every other version
line, in one go.

## The permission rules

- `hosts/claude-code.md`, the table and the JSON block replace `Bash(uv run --script *chantier.py
  *)` / `PowerShell(…)` with two pairs:
  - `Bash(uvx --from git+https://github.com/gsemet/chantier@* chantier *)` / `PowerShell(…)` (plugin
    mode). Risk accepted: any ref of that repository.
  - `Bash(uv run --locked --project * chantier *)` / `PowerShell(…)` (dev mode, chantier's own
    checkout). Risk accepted: any local project whose script is named `chantier`.

  The auto-mode note of row 180 and line 324 carries over to both, still **unproved**. The
  sentence of line 196 ("covered by the `chantier.py` rule") names the new rules.
- `hosts/claude-code.md` 131 and 133 say `$CHANTIER` runs through `uv` or `uvx`, and that uv
  provides the interpreter in both modes.
- **`commands/permissions.py` `SAMPLES`** gets both forms, each with its rule, so that P10 checks
  the rule of the mode that `cli_command` gives in this install. The structure test that compares
  the block with the CLI's list still passes.
- A user's settings that hold only the old rule get P10's warning naming the new rule. The release
  notes of the release that ships this CR say so.

## Cards

- `concepts.md` 205: `$CHANTIER` is "the CLI, exactly as your prompt gives it (in chantier's own
  checkout `uv run --locked --project "<…>" chantier`, else `uvx --from git+…@v<version> chantier
  --skill "<…>"`; with a planning surface, plus `--project <folder>`)".
- `chief-of-staff.md` 453: the Foreman's prompt line becomes `CLI: <$CHANTIER, exactly as your
  skill gives it> <command> --batch <batch>`.
- No other card and no agent file changes: they say `$CHANTIER`.

## `AGENTS.md`

This CR edits the text CR-221 leaves (lines 9–13, 23–26, 28–31 at CR-221's head).

- **The CLI's line** ("The CLI's dependencies are Python packages declared in its scripts' PEP 723
  inline metadata and locked beside them; …") becomes: "The CLI is one Python package declared in
  the root `pyproject.toml`, its dependencies listed there once and locked in `uv.lock`. Installed
  as a plugin, it runs through `uvx` at the release tag the skill names, which `just version`
  writes. In chantier's own checkout, it runs the local code with `uv run --project`. A dependency
  ships wheels for Linux, macOS and Windows and replaces hand-written code. The CLI stays portable
  (POSIX and Windows, UTF-8 everywhere)."
- **The board's clause** ("takes its dependencies through the CLI's PEP 723 inline metadata like
  the rest of the CLI") becomes "is part of the CLI's package and runs with no plugin too
  (`uvx --from git+…@v<version> chantier board`)".
- **"The plugin must work with no setup"** keeps its words. One clause is added after "are the
  only configuration": "; `uv` is the only tool to install, and as a plugin the CLI needs the
  network to fetch its release". What chantier writes is unchanged. The `.venv` of dev mode is in
  chantier's own checkout, never in a user's project.

## `CONTRIBUTING.md`, `README.md`, docs and docstrings

- **`CONTRIBUTING.md`, item 2** (line 70 at CR-221's head): the CLI is a package declared in the
  root `pyproject.toml` and locked in `uv.lock`. It runs by `uvx` at the release tag when installed
  as a plugin, and by `uv run --project` from the local code in this checkout.
- **`CONTRIBUTING.md`, item 2's board line** (lines 84–86): as in `AGENTS.md`.
- **`CONTRIBUTING.md`, repository layout** (line 134): `pyproject.toml` and `uv.lock` at the root;
  `scripts/cli/` holds the package's source, its tests and `session_usage.py`.
- **`CONTRIBUTING.md`, Set up** (line 144): unchanged in substance. A new sentence after line 157
  says that, in this checkout, `$CHANTIER` runs the local code with no fetch (dev mode).
- **`CONTRIBUTING.md`, Code standards** (line 259): `uv lock` (from the root) after a change to the
  dependencies; `just lint` refuses a stale lock.
- **`CONTRIBUTING.md`, Versions** (line 239): the list of files that carry the version gains "the
  root `pyproject.toml` and `uv.lock`, and the release ref in the four `SKILL.md`".
- **`README.md`, Install** (line 208, CR-221's sentence about the first run): as a plugin, the CLI
  is fetched from GitHub at the plugin's release. Its first call takes a few seconds and needs the
  network, and every call needs the network (the tag is checked each time; open point 1).
- **`docs/boards.md`**: the launch with no plugin and no agent, from a planning surface:
  `uvx --from git+https://github.com/gsemet/chantier@v<version> chantier --project <folder> board`.
  `<version>` is the release the surface's planners use (open point 10).
- **Docstrings**: `plugin_files.skill_dir` (the order `--skill`, `CHANTIER_SKILL_DIR`, parents),
  `cli_command` (the two modes), and `costs/copilot.py`'s path of `session_usage.py`.

## Tests

The structure tests stay few. This CR changes two tests and adds one.

- **CR-221's test "the dependency lists agree"** (`tests/test_code_targets.py`) becomes: the root
  `pyproject.toml` holds the dependencies and `no-build = true`. No `.py` file under
  `skills/chantier/scripts/cli/` holds a PEP 723 block except `session_usage.py`.
  `skills/chantier/scripts/cli/pyproject.toml` and `chantier.py` do not exist.
- **The version test** (`test_plugin_files.py`, whichever reads the version targets) checks the root
  files and the four refs.
- **New: one launch, two modes, one text.** `cli_command` is computed for a temporary skill folder
  whose plugin root has a `.git` folder, and for one with none. The test expects exactly:
  - with `.git`: the dev form;
  - without: the plugin form, with `@v{__version__}` and `--skill`.

  It then checks that each `SKILL.md` names both forms, with its ref equal to `__version__`. A
  structure test that runs the CLI as `chantier.py` follows the new entry (`python -m chantier` or
  `cli.main`).

## Order

- The CR's `depends.json` already holds `{"after": ["python-inline-deps"]}`.
- Answer 2 says the queued Python CRs wait for this one. Recording that is the Chief of Staff's
  part, not this specification's. `222-visualization-backend` and `223-cr-summaries` wait today for
  `python-inline-deps` only. Every pending CR that touches the CLI's Python gets
  `after: root-pyproject-launch`.

## Out of scope

- Any change to what a command does or prints, apart from the `cli:` fact line and the new
  `--skill` option. The STATUS files, the records and the pane are unchanged, so `AGENTS.md`'s
  screenshot rule does not apply.
- `hooks/` and `types/` (so no `just mod`). The agent files.
- Publishing to PyPI.
- Moving the package's source out of `skills/`.
- Pinning the marketplaces to a tag (open point 2).
- A version bump: the release process does it (open point 3 asks for a release right after).
- `.github/workflows/ci.yml`: its steps do not change (see "CI").
- The surface's autosync and the board's framework: `227-surface-autosync` and
  `222-visualization-backend`.

## CI

`.github/workflows/ci.yml` does not change. Its recipes do: `check` (with `lint` and `test` at the
root) runs on `ubuntu-latest`, `macos-15-intel` and `windows-latest`; `scenario` and
`eval-dry-run` run on `ubuntu-latest`. On those runners uv comes from `astral-sh/setup-uv` with an
empty cache, the network is there, uv picks the Python, and there is no `claude`. The checkout is a
git clone, so every recipe runs in dev mode. CI never runs plugin mode: that is proved by E5 and
E7 below, on the local machine.

The recipes now resolve a root project instead of a script. So the cold-cache proof of
CONTRIBUTING is taken, as in CR-221 (E6). Only the first CI run proves:

- the editable build on Linux and macOS;
- the `--locked` environment of `scenario` and `eval-dry-run` on Linux.

## Evidence

The Verifier keeps each item in `work/verifier/evidence/`, and the PR body quotes it.

- **E1.** `just check` passes on Windows, then in CI on the three systems.
- **E2.** `just scenario` passes on both forges, on the branch's head, locally and in CI.
  `git diff main -- scenario/` shows only the `cli:` check.
- **E3.** `just eval-dry-run` passes, locally and in CI.
- **E4. Dev mode, live.** From a cwd outside the checkout:
  1. `uv run --locked --project "<worktree>" chantier --version` prints the version.
  2. Edit one help string in `src/chantier/`. The next call shows it, with no reinstall. Revert
     the edit.
  3. `git status` of the worktree is clean (no rewritten `uv.lock`).
  4. With `UV_OFFLINE=1`, the call still works.
- **E5. Plugin mode, from GitHub.** Once the branch is pushed:
  1. Copy the plugin's files to a folder with no `.git`, as a host's cache holds them.
  2. Run `uvx --from git+https://github.com/gsemet/chantier@<the branch head's full SHA> chantier
     --skill "<copy>/skills/chantier" preflight` in a scratch git repository. A SHA is used because
     the tag does not exist before the release. There is no `#subdirectory`. P4 and P5 pass on the
     copy's agents and version.
  3. `take` in a scratch batch prints `cli: uvx --from git+https://github.com/gsemet/chantier@v<version>
     chantier --skill "<copy>/skills/chantier" …`.
  4. The same `preflight` without `--skill` fails with the new one-line message, with no traceback.
- **E6. A fresh machine.** With `UV_CACHE_DIR` set to a new empty folder outside the repository:
  1. `just check`, `just scenario` and `just eval-dry-run` pass.
  2. The cold time of E5's first call is recorded.
  3. With `UV_OFFLINE=1`, the SHA form still runs.
  4. With `UV_OFFLINE=1`, a tag form (`@v0.9.0#subdirectory=skills/chantier/scripts/cli`) fails
     with uv's message, as measured above.
- **E7. The board with no plugin.** In a scratch planning surface with no plugin and no
  `CHANTIER_SKILL_DIR`, run `uvx --from git+…@<SHA> chantier --project <folder> board --port <n>`.
  It serves the page (an HTTP 200 on `/`), and `… status` prints the batch.
- **E8. The version moves the ref.** In a scratch worktree: `just version 9.9.9` writes 9.9.9 in
  the root `pyproject.toml`, the root `uv.lock`, and the four refs `@v9.9.9`. `just version-show`
  prints 9.9.9. A `SKILL.md` with a wrong ref makes `just version` write nothing. The worktree is
  then dropped.
- **E9. Times.** Ten runs each of `chantier --version` and `chantier status`, warm, on Windows:
  `main`'s `uv run --script`, the branch's dev form, and the plugin form at a SHA. The medians go
  in the PR body. No threshold is set.

## Open points (defaults taken, for the Chief of Staff to confirm with the user)

1. **A tag costs time and the network at every call.** Measured: 1.9–2.1 s per call against
   0.5 s today, and a tag fails offline even with a warm cache. A full commit SHA costs 0.8–1.0 s
   and works offline, but `just version` cannot write the SHA of a commit that does not exist yet.
   **Default: the tag `v<version>`, as the user said.** Alternative: in plugin mode, `uvx --from
   "<plugin root>"`, the plugin's own copy. That is aligned with the cards by construction, takes
   0.5 s and works offline. The git ref would then serve only the launch with no plugin. The user
   may see that as the second method that answer 1 refused.
2. **Same version, different code between releases.** Today `main` is 9 commits past `v0.9.0`, with
   the same version 0.9.0. A user who installs the plugin from `main` between two releases runs
   `main`'s cards with `v0.9.0`'s CLI, and preflight P5 sees equal versions. **Default: accept and
   document it in `README.md`, Install.** Alternative: pin each marketplace entry's source to the
   release tag, so that users get released trees only. Whether Claude Code's and Copilot's
   marketplace sources accept a ref is unproved; that would be another CR.
3. **The first ref does not exist yet.** At this CR's merge the version is still 0.9.0, and
   `v0.9.0` has no root `pyproject.toml`, so plugin mode fails until the next release is tagged.
   The user's own install is in dev mode and is not affected. **Default: the Chief of Staff orders
   a release right after this CR.**
4. **`uvx` ignores `uv.lock`** (measured). Plugin users get the newest versions that meet the
   floors, not the versions CI ran. **Default: pin the three direct dependencies exactly (`==`) in
   the root `pyproject.toml`.** Their transitive dependencies still float within the pins' own
   ranges (pydantic pins pydantic-core exactly). `uv.lock` stays for dev and CI. Alternative: keep
   CR-221's floors and accept newer versions in plugin mode.
5. **No `no-build` in plugin mode.** `uvx --no-build` refuses chantier itself (measured). A
   dependency with no wheel for the user's Python would therefore be compiled, and fail with a
   compiler's error rather than uv's no-wheel message. **Default: accept it.** Alternative: add
   `--no-build-package <each dependency>` to the plugin form, which lengthens `$CHANTIER` and must
   follow every change to the dependencies.
6. **Copilot's install.** Whether a Copilot plugin install keeps `.git` was not seen. If it does,
   that install runs in dev mode: the same code, but uv writes `.venv` in the plugin's folder.
   **Default: the `.git` rule anyway.** A Copilot trial records what its install holds.
7. **The allow rules.** **Default: two rules (plugin and dev) in the block, and P10 checks the
   current mode's rule.** Users replace the old `uv run --script *chantier.py *` rule; the release
   notes say so. Whether auto mode classifies `uvx` and `uv run --project` as package-manager runs
   is still unproved.
8. **`session_usage.py`.** **Default: it keeps its own PEP 723 block and pinned index**, since it is
   a separate tool. "The dependency list lives once" then holds for the CLI's package, not for that
   helper. Alternative: move `copilot-session-usage` into the root dependencies and import it in
   the process. That loses `--no-config` and the pinned index.
9. **Where the source lives.** **Default: unchanged, in `skills/chantier/scripts/cli/src/`**, which
   keeps dev mode's parent search and CR-221's paths. Alternative: a root `src/`, which needs
   `skill_dir()` from `--skill` or the environment in dev mode too.
10. **The ref in the docs.** **Default: the docs write `v<version>` as a placeholder**, so
    `version.py` gets no target outside the four `SKILL.md`. Alternative: a literal ref in
    `docs/boards.md`, added to `TARGETS`.
11. **`--locked` in dev mode.** **Default: `--locked`**, which refuses a stale lock and never
    rewrites `uv.lock` in the main checkout. Alternative: no flag, so uv relocks silently and the
    main checkout gets dirty, which blocks its fast-forward after a merge.

## Decisions after the specification (they replace the open points they name)

Asked by the Chief of Staff, 2026-11-13 (in French, recorded in English).

- **Plugin mode runs `uvx --from "<plugin root>" chantier`** (the user: "je veux bien ce fonctionnement
  avec --from"), not `uvx --from git+https://…@v<version>`. One method, `uvx --from <source> chantier`;
  only the source differs: the installed plugin's own folder (cards and CLI from the same commit, no
  fetch, offline, about 0.5 s per call), chantier's checkout in dev mode (live, no fetch), and
  `git+https://github.com/gsemet/chantier@v<version>` for a launch with no agent (a planning surface's
  `just board`), the version pinned where that launch lives. This replaces open points 1, 2 and 3: no
  release is needed for plugin mode to work after this CR, and no version mismatch between the cards
  and the CLI. The skill keeps no hard-coded ref for plugin mode; `just version` still writes the
  version into the root `pyproject.toml` and the documented `git+https` example. Measure that uvx from
  the plugin folder picks up a new plugin version after an update (cache keys), and say so in the PR.