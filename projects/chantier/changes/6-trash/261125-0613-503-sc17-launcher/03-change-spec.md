# SC17: one launcher that picks the mode and runs the CLI

Child 17 of 28 of the program CR `simplify-cards-and-prompts`. The program's `03-change-spec.md`
("Child 17", "Rules for every child") and its `02-answers.md` answers 17 to 22 rank above this
file. One Driver and one PR, in the running stack batch (batch-31). Code read: `origin/main` at
`8a960d34`. Short forms used below:

- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`;
- `<plugin root>` is the folder that holds `.claude-plugin/plugin.json` (chantier's checkout, or a
  host's plugin copy); `<skill folder>` is `<plugin root>/skills/chantier`.

## Goal

Each of the four `SKILL.md` files (`skills/chantier`, `skills/chief-of-staff`, `skills/griller`,
`skills/status`) carries the same `$CHANTIER` paragraph, about 2.3 KB (study-fable-v2). Every
steering session reads it and then works out the launch by hand:
- is this chantier's own checkout, and is the session's project chantier: dev or plugin mode;
- in the dev mode, `uv sync --locked --check`, naming the holders of `.venv`, the sync, or
  `sync pending: held by …`;
- the exact form to type, with `--skill` in the plugin mode.

This child moves that work into code: one launcher shipped with the plugin. It picks the mode,
runs the dev mode's checked sync when asked and prints `sync pending: held by …` itself, and
runs the CLI by the one method AGENTS.md describes. An agent then types one fixed form:

```
uv run --script "<plugin root>/skills/chantier/scripts/chantier.py" [--project <folder>] <command> ...
```

Nothing uses the launcher yet. The four `SKILL.md` keep their paragraph. Child 23 writes the
one line that names the launcher, in the unloaded set, and child 24 swaps it in. This child
ships the launcher, its tests, and a trial in a real session showing that the host's allow rule
matches it as it matches today's form.

## Place in the chain

- **Base:** child 16's branch (`sc16-retro-draft`), the previous CR of the stack. Nothing of
  child 16 is used here.
- **Uses from earlier children:** nothing. `src/launch.py` and `src/plugin_files.py` are as on
  `origin/main`.
- **Built on this branch:** child 18 (`roles-data-check`). It uses nothing from this one.
- **Depends on this child:**
  - child 23 (`cards-host-and-shared`) writes, in `cards-next/skills/`, the four `SKILL.md` texts
    with one line that names the launcher. It also writes the host topic that holds the launcher's
    allow rule. It reads the form from `launch.launcher_line` and `launch.launcher_rule`
    (section 2) and the sync's lines from section 4;
  - child 24 (`cards-swap`) brings in those texts. It adds the launcher's P10 sample and its
    rule to `src/commands/allow_samples.py` and to the host card's table and JSON block. It also
    decides whether `plugin_files.cli_command` (the `cli:` fact, the briefs) prints the launcher
    form (section 6);
  - child 28 (the real run) runs the new cards, which type the launcher.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Program child 17, Scope | A launcher shipped with the plugin decides the dev or plugin mode | sections 1, 2, 3 |
| Program child 17, Scope | It checks `uv sync --check` and prints `sync pending: held by …` itself | section 4 |
| Program child 17, Scope | It runs the CLI by the one method AGENTS.md describes: `uvx --from <plugin root>`, or in the dev mode `uv run --no-sync --project` | section 3 |
| Program child 17, Scope | The four `SKILL.md` keep their paragraph until child 23 | section 6, "Out of scope" |
| Program child 17, Evidence | Pytest of the mode choice on prepared folders | section 7 |
| Program child 17, Evidence | A trial in a real session shows the host's allow rule matching the launcher as it matches today's `uv run` form, recorded in the PR | section 8 |
| Program child 17, Evidence | An unmatched or refused launcher is not worked around: the child hands back blocked | section 8 |
| Program child 17, Must not | Change the run method; install anything | sections 3, 4, "Must not" |
| Program child 17, Risk | P10's samples change with the launcher; one new rule may be asked by preflight; the ready ask names it | section 6 |
| Program child 17, Risk | AGENTS.md: the run-method paragraph names the launcher | "AGENTS.md" |
| Answer 18 | Tools first: only additions; every intermediate `main` keeps working with the old cards | no card, no existing output changed |
| Program rules, "Card text" | No child before 19 edits an existing card's text | section 6 |
| Answer 22, F17 | A claim about the host or a tool not proved here is marked "unproved" | sections 3, 4, 8 |
| Answer 22, F20 | The PR states the seconds its tests add to `just test` | "Gates and evidence" |

On P10, the program says the samples change "with the launcher". This child carries that as the
launcher's rule text (`launch.launcher_rule`), ready for P10. It does not add a sample row.
`tests/test_cli_runs.py::test_the_allow_rules_json_block_lists_exactly_what_preflight_checks`
ties `SAMPLES` to the table and JSON block of `references/hosts/claude-code.md`. A new row would
force an edit of that card, which the program's "Card text" rule forbids before child 19. Child
1 (CR-487, `push`) made the same choice. While no card types the launcher, a rule asked for it
would cover no command. So P10 starts asking for it at the swap (child 24), and the ready ask
says so (section 6).

## What changes

### 1. The launcher file (`skills/chantier/scripts/chantier.py`, new)

A short script with an inline metadata block, as `scripts/version.py` has:

```
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

`requires-python` is the same as the root `pyproject.toml`'s (a test checks it). The script holds
no logic. It puts `Path(__file__).resolve().parent / "cli" / "src"` first on `sys.path`, imports
`chantier.launcher`, and calls `raise SystemExit(main(sys.argv[1:]))`. The plugin root is
`Path(__file__).resolve().parents[3]`.

The launcher runs as `uv run --script "<path>"`, never from the project's `.venv`. A script with
inline metadata gets uv's own environment, so the launcher never holds `<plugin root>/.venv`,
even in chantier's checkout. This follows uv's documentation; it is **unproved** here until
the scenario step (section 7) and the trial (section 8) show it. With `dependencies = []`, it
needs no package. It needs a Python of at least 3.11, which uv finds or fetches once, as `uvx`
does today. With uv's cache warm, it needs no network (shown with `UV_OFFLINE=1`, sections 7
and 8).

Add `"skills/chantier/scripts/chantier.py"` to `[tool.mypy] files` in `pyproject.toml`.
`just lint` already formats and checks `skills/` with ruff.

### 2. The one source of the texts (`src/launch.py`)

`launch.py` stays standard-library only (a test checks it, section 7). Add:

- `LAUNCHER = Path("skills/chantier/scripts/chantier.py")`: the launcher's path from the plugin
  root.
- `launcher_line(root: Path) -> str`: `uv run --script "<root>/skills/chantier/scripts/chantier.py"`,
  written with forward slashes and quoted, as `dev_launch` and `plugin_launch` are.
- `launcher_rule(root: Path) -> str`: `f"{launcher_line(root)} *"`. P10 and child 23's host topic
  read this rule text, and the trial proves it.
- `project_is_chantier(cwd: Path, project: str | None) -> bool`: the launcher's half of the mode
  rule, with no `Repo`. It runs read-only `git rev-parse` calls through `subprocess` (no
  `chantier.core` import). It answers what `is_chantier_project(Repo.find(cwd, project))`
  answers:
  - `CHANTIER_ROOT`, when set, replaces `cwd`, as in `Repo.find`;
  - with `project`:
    - a bare name (one part, not absolute) is taken as `<git top of cwd, or cwd>/projects/<name>`;
    - another relative path is taken from `cwd`, then resolved;
    - the answer is whether the folder's name is `chantier`, by its name alone, as the
      `SKILL.md` paragraph and `is_chantier_project` say for a surface;
  - without `project`: take the root as the parent of `git rev-parse --path-format=absolute
    --git-common-dir` (so a worktree of chantier counts as chantier). Then:
    - when the root has no `.agents/changes/` and its `projects/` holds exactly one project
      (`checkout.yml` or `changes/` inside, as `surface_projects` says), the answer is whether
      that project's name is `chantier`;
    - with several projects, the answer is `False` (the CLI refuses with its `--project` line
      anyway);
    - otherwise the answer is the manifest test of `is_chantier_project`: the root's
      `.claude-plugin/plugin.json` or `.github/plugin/plugin.json` has `name` `chantier`;
  - outside a git repository, the answer is `False`.

  Refactor `is_chantier_project`'s manifest test into a helper that both functions call, so the
  manifest rule is written once. `is_chantier_project`'s behaviour does not change.

### 3. The mode and the run (`src/launcher.py`, new, standard-library only)

`main(argv: list[str]) -> int`, and the pure functions it calls (tests call them with prepared
folders and a fake process runner):

- **The mode.** `dev` when `<plugin root>/.git` exists (a folder or a file) and
  `project_is_chantier(cwd, project)` holds. This is `plugin_files.is_dev_mode`'s rule. `plugin`
  in every other case: a host's plugin copy, or another project's session even when run from
  chantier's checkout.
- **The root options.** The launcher reads the CLI's root options that come before the first
  word that is not an option: `--project <v>` and `--project=<v>`; it also skips `--profile` and
  `--skill`, which take a value. It reads them and leaves them in place: the argument list goes
  to the CLI unchanged.
- **The command it runs**, as a list with no shell:
  - dev: `uv run --no-sync --project <plugin root> chantier <argv...>`;
  - plugin: `uvx --from <plugin root> chantier --skill <skill folder> <argv...>`. `--skill` is
    added only when `argv` does not already carry it.

  The prefix tokens are built from the same strings as `launch.dev_launch` and
  `launch.plugin_launch`, so the forms cannot drift. A test checks that the joined, quoted list
  equals `plugin_files.cli_command(repo)` for the same folders (section 7).
- **The run.** The CLI inherits standard input, output and error. The launcher adds nothing to
  standard output on a run, buffers nothing (a `watch --stream` stays live), and exits with the
  CLI's exit code.
  - On POSIX it replaces itself with `os.execvp`, so no process of its own is left between the
    host and the CLI.
  - On Windows it runs the command with `subprocess.run` and returns its code. On Ctrl-C it waits
    for the child, which gets the same console signal.

  When `uv` or `uvx` is not found, it prints one line, `chantier launcher: uv is not on PATH
  (uv is the one tool chantier needs)`, and exits 127. It tries nothing else.
- **`--print`**, as the first argument only: it prints the launch form that the run would use,
  and runs nothing. That is `plugin_files.cli_command`'s text for the same folders, `--project
  "<absolute folder>"` included when `--project` was given. It exits 0. The tests, the scenario
  and the trial read it.
- **`--sync`**, as the first argument only: section 4.
- The launcher never runs `uv sync` outside `--sync`. In the dev mode an ordinary call runs no
  check, as today's `--no-sync` form does. Only the steering session syncs, at the moments the
  cards name.

### 4. The dev mode's checked sync (`--sync`, in `src/launcher.py`)

These are steps 1 to 4 of `references/sync-checkout.md`, done by the launcher itself. Steps 5
and 6 stay with the steering session: the user told once after 3 minutes, and the offer to stop
its own board and watcher. They need the session's judgement and its seat.

- In the plugin mode it prints `plugin mode: no sync (only chantier's own checkout syncs)`,
  exits 0, and runs nothing.
- In the dev mode:
  1. It runs `uv sync --locked --check --project <plugin root>`. Exit 0: it prints `in sync`
     and exits 0. Exit 1 with uv's text `The environment is outdated`: step 2. Any other exit is
     an ordinary sync failure, never `sync pending`: it prints uv's text and exits with uv's
     code.
  2. It names the holders of `<plugin root>/.venv` by the commands of the host row "Name the
     holders of the checkout's environment" (`references/hosts/claude-code.md`), read-only:
     - on Windows: `powershell.exe -NoProfile -NonInteractive -Command` with `Get-CimInstance
       Win32_Process | Where-Object { $_.ExecutablePath -like '<root with backslashes>\.venv\*' }
       | Select-Object ProcessId, ParentProcessId, CommandLine`, its output read as JSON
       (`ConvertTo-Json`);
     - elsewhere: `ps -eo pid,ppid,args`, keeping the lines that hold `<plugin root>/.venv/`.

     It reads them as the row says. A `chantier` process and its `python` child are one holder,
     named by the top process's PID. Each holder is written `PID <n> <subcommand> <project>`,
     with the subcommand and the `--project` value taken from its command line. A `serve` with
     `--stop-idle` and no `--seat` is written `PID <n> serve <project> (started by webui)`. It
     never stops a holder.
  3. With no holder, it runs `uv sync --locked --project <plugin root>`. On success it prints
     `synced` and exits 0. When it fails with os error 32 (a holder the listing missed), it goes
     to step 4 with `an unlisted process`. Any other failure: uv's text, uv's code.
  4. With any holder, it prints `sync pending: held by <holders>` (holders joined by `, `) and
     exits 0. The session goes on unsynced: its next ordinary call runs the `--no-sync` form.
     Its next `--sync`, at a later turn, starts again from step 1.

`sync pending` exits 0 because it is not a failure: `startup-core.md` routes failures, and the
paragraph keeps `sync pending` out of them. The three lines `in sync`, `synced` and `sync pending:
held by …` are fixed texts. Child 23 quotes them, and the tests assert them.

Unproved here: the Windows listing run from Python rather than typed into the `PowerShell` tool
(the row's listing was exercised by hand on 2026-11-21); the macOS and Linux listing (untested,
as the row says).

### 5. What does not change

- The four `SKILL.md` files, every card under `references/`, the hook and the agent wrappers.
- `plugin_files.cli_command`, `sync_command`, `sync_check_command` and every CLI output: the `cli:`
  fact, the briefs and the Driver prompts keep today's forms.
- `src/commands/allow_samples.py`, `src/commands/permissions.py` (`PROBES`, `_PLUGIN_FORM`,
  `_DEV_FORM`, `_stale`) and P10's output.
- The run method: the dev mode still runs `uv run --no-sync --project`, and the plugin mode
  `uvx --from <plugin root> chantier --skill <skill folder>`. The launcher only chooses between
  them and runs them.

### 6. For the swap, and the ready ask

The PR's body has a section "For child 24", and the ready ask quotes its first point:

- **No new allow rule is asked yet.** P10 starts asking for `Bash(<launcher_rule>)` and
  `PowerShell(<launcher_rule>)` from child 24 on, when the cards type the launcher. That is the
  one new rule a user who granted today's rules will add, asked by preflight as today.
- Child 24 adds one `SAMPLES` row, `("batch", "any", f"{launcher_line(<plugin root>)} status",
  launcher_rule(<plugin root>))`, filled by `fill_rule` and `fill_sample` like the other chantier
  rows. It also adds the matching line to the host card's table and JSON block.
- Child 24 reviews `permissions.py`:
  - a user's broad `uv run --script * *` (already in `PROBES`) then reads "replaced by" the
    launcher's rule;
  - `_stale` learns the launcher's form for a rule that names a moved plugin.
- Whether the old forms (dev, sync, check, plugin) stay as rules once no card types them is
  child 24's call.
- Whether `cli_command` prints the launcher form is child 24's call: the `cli:` fact and the
  briefs carry it verbatim.

### 7. Tests (`tests/test_launcher.py`, new)

All in-process, with prepared folders under `tmp_path`, and no `uv`, `uvx` or `powershell`
started. The process runner is a fake that returns prepared outputs and records the commands.

- **The mode choice.** Parametrized over the cells of `tests/test_launch_modes.py`'s
  `LAUNCH_CELLS` (`claude`, `copilot`, `surface-chantier`, `plain`, `other-name`, `broken`,
  `surface-studio`, `none`), plus:
  - a surface whose only project is `chantier`, with no `--project`;
  - a surface with two projects;
  - a bare `--project chantier` inside a surface;
  - a worktree of a chantier-manifest repository;
  - `CHANTIER_ROOT` set to another folder;

  each crossed with a plugin root that holds `.git` and one that does not. For each, it asserts:
  - the launcher's mode;
  - that `project_is_chantier` equals `is_chantier_project(Repo.find(...))`, and the mode equals
    `plugin_files.is_dev_mode(...)`, with `CHANTIER_SKILL_DIR` pointed at the prepared plugin
    (the parity that guards the two halves against drift);
  - that `--print`'s line equals `cli_command(repo)`, `--project` included, also with a space in
    the path;
  - the argument list of the run: the root options left in place, `--skill` added once, the
    rest unchanged.
- **The sync.** The fake runner gives each case:
  - check exit 0: `in sync`, no sync run;
  - outdated with no holder: `synced`, the sync run once;
  - outdated with a board and its `python` child plus a `webui`-started server:
    `sync pending: held by PID 10 serve chantier, PID 30 serve chantier (started by webui)`,
    no sync run, exit 0;
  - the sync failing with os error 32: `sync pending: held by an unlisted process`;
  - another failure: uv's text and code;
  - the plugin mode: its line, nothing run.

  It also asserts that an ordinary call runs no `uv sync` in either mode.
- **The shipped files, read from the repository at the head under test.**
  - `skills/chantier/scripts/chantier.py`: its metadata block says `dependencies = []`, and its
    `requires-python` equals `pyproject.toml`'s;
  - `src/launcher.py` and `src/launch.py`: they import only modules in
    `sys.stdlib_module_names`, plus `chantier.launch` from `launcher.py`. This is an AST read of
    the files.
- **The missing `uv`.** The fake runner raises `FileNotFoundError`: one line, exit 127.

**Scenario** (`scenario/run_scenario.py`): a new section function `launcher_modes`, added to the
unit that already runs preflight's P10 step, inside its time budget. It runs the shipped launcher
for real with `uv run --script`, `UV_OFFLINE=1` in its environment:
- in the sandbox project (not chantier), `--print` equals the `cli:` fact's form;
- with `--project <a prepared surface>/projects/chantier`, `--version` runs the dev form and
  prints `chantier <version>`, exit 0;
- in the sandbox, `--sync` prints the plugin-mode line, exit 0;
- `<checkout>/.venv` is unchanged across the three calls, which proves on ubuntu that the
  launcher does not run from it. The check reads the modification time of
  `<checkout>/.venv/pyvenv.cfg` and the listing of `.venv/`.

Add its bullet to `scenario/README.md`'s Coverage list, ending `(unit: <that unit>, test:
test_launcher.py::<the mode test>)`. Whether ubuntu's runner has uv's cache warm enough for
`UV_OFFLINE=1` is proved only by the first CI run.

### 8. The trial in a real session (recorded in the PR)

The Driver runs it on its own machine and records it in the PR under "Trial". It runs before
the PR is called ready.

- **The settings.** A scratch settings file in the session's scratch folder, never
  `~/.claude/settings.json` and never the project's settings. It holds the filled rules
  `Bash(<launcher_rule(<plugin root>)>)` and `PowerShell(<launcher_rule(<plugin root>)>)`, plus,
  as the control, today's filled rule of the same mode: `dev_rule` in chantier's checkout for
  the chantier project.
- **The session.** Claude Code headless (`claude -p`), started in a scratch folder outside the
  repository, with `--permission-mode dontAsk`. This is the cell the host card proved for
  today's forms: main session, `dontAsk`. It uses `--settings <scratch file>`, plus whatever
  flags keep the user's own allow rules out (recorded).
- **The commands.** The prompt asks the session to run, one command each, exactly:
  - `<launcher_line> --project "<surface>/projects/chantier" --version` with the `Bash` tool;
  - the same with the `PowerShell` tool, when the session has it;
  - today's `<dev_launch> --version` with each tool.
- **What it records:**
  - the Claude Code version (`claude --version`), the system, the permission mode and the exact
    flags;
  - each command's verdict: run, or refused with the refusal quoted;
  - a negative control: the same session with the scratch settings minus the launcher's rules
    must refuse the launcher. That shows the rule is what lets it through.
- **Pass:** the launcher runs exactly where today's form runs, and the negative control refuses
  it. Auto mode and a Driver (subagent) stay **unproved**, as for today's forms. Copilot is
  **unproved**: no trial. When the Driver can, it adds one auto-mode try and records the verdict
  as information.
- **Fail:** the rule does not match, the host refuses, the negative control cannot be shown, or
  `claude -p` itself is refused to the Driver. The child hands back blocked with the transcript's
  lines. No other path form, no wrapper and no broader rule is tried.
- **Also recorded:**
  - the launcher's overhead: the median of 5 `--version` calls through the launcher against 5
    through today's form, in each mode on the Driver's machine;
  - one stop check. Through the launcher, start a long CLI command in a scratch in-project
    repository (`serve --ui none`), then stop the launcher's top process (the `uv run --script`
    one) the way the host stops a background shell. Then list whether a `chantier` process
    from it is left.

  A `chantier` process left behind does not block this child, which nothing uses yet. It goes
  in the PR's Known gaps ("the launcher leaves the CLI running after its stop on <system>"), the
  ready ask quotes it, and child 24 must not switch the cards until it is fixed.

## Out of scope

- Any edit of the four `SKILL.md`, `references/sync-checkout.md`, `references/startup-core.md`
  or any other card (children 23 and 24).
- P10's samples, the recommended rules and the host card's table (child 24, section 6).
- Steps 5 and 6 of `sync-checkout.md` (the 3-minute message, the offer to stop the session's own
  board and watcher).
- Copilot's allow rules for the launcher.
- A launcher on PATH, a `bin/` folder, a shell or `.cmd` wrapper. The one form is `uv run
  --script "<path>"`, the same text in `Bash` and `PowerShell`.
- Any change to how the board, the hub or the watcher are started.

## Must not

- Change the run method: the launcher runs exactly the dev form or the plugin form, chosen by
  today's rule. In the dev mode it never runs `uvx --from <checkout>`, and in the plugin mode it
  never runs `uv sync`.
- Install anything: no `uv tool install`, no PATH or profile change, no package in the
  launcher's metadata. The one write is `uv sync --locked` under `--sync`, in chantier's own
  checkout, which the cards run today.
- Stop, kill or signal a holder of `.venv`.
- Add a line to the CLI's output on a run, or change any existing output.
- Edit a card, a hook, a wrapper, or a version by hand.

## Gates and evidence

- `just test` passes with `tests/test_launcher.py`. `tests/test_launch_modes.py` and
  `tests/test_allow_rules.py` pass unchanged.
- The added `just test` seconds are measured before (at the base) and after (at the head) on the
  same machine and go under the PR's Deliverables. Expected: under 1 s (about 30 parametrized
  cases of pure functions on small prepared folders, with a few `git init`s).
- `just check` and `just eval-dry-run` (a change under `src/`) run in the worktree at the rebased
  head before the first push.
- The long gate `just scenario (ubuntu-latest)` is green at the PR's head, since the CLI's
  package and the scenario change. The local Windows `chantier gate <cr> scenario` is owed only
  while this CR is the stack's top; it moves to the CR that joins above it.
- The trial of section 8, recorded in the PR. Without its pass, the child hands back blocked.
- No `hooks/` or `types/` change, so `just mod` is not owed. No journal type, so no `just
  journal-schemas`.
- The shipped-file checks read `skills/chantier/scripts/chantier.py`, `src/launcher.py`,
  `src/launch.py` and `pyproject.toml` from the repository at the head under test (section 7).
- Matrix (install × project × host). The launcher's code acts the same on both hosts; the
  allow-rule match depends on the host:
  - chantier's checkout, project chantier: dev form (tests, scenario);
  - chantier's checkout, another project: plugin form from the checkout (tests, scenario);
  - plugin copy (no `.git`), project chantier: plugin form (tests);
  - plugin copy, another project: plugin form (tests);
  - Claude Code, main session, `dontAsk`: the rule matches (the trial, section 8);
  - Claude Code, auto mode or a Driver: **unproved** (one auto-mode try recorded when possible);
  - Copilot: **unproved**, no trial.

## AGENTS.md

Edit the repository's root `AGENTS.md` (as on `origin/main`):

- **The run-method bullet** ("The CLI is one Python package … One method runs it, `uvx --from
  <source> chantier`: …"): after the sentence that ends "then `uv run --no-sync --project` runs
  the local code, live;", add:

  > The plugin ships one launcher, `skills/chantier/scripts/chantier.py`, run as
  > `uv run --script "<plugin root>/skills/chantier/scripts/chantier.py" …` from uv's own
  > environment, never the checkout's `.venv`. It picks the mode by this rule and runs the CLI by
  > this one method, adding `--skill` in the plugin mode. With `--sync`, in the dev mode only, it
  > runs the checked sync: the check, the holders named read-only, the sync when there are none,
  > else `sync pending: held by …`. It stops no process, installs nothing, has no dependency of
  > its own, and runs no `uv sync` but under `--sync`. It is built on study-fable-v2's measure
  > (the `$CHANTIER` paragraph, about 2.3 KB in each of the four skills) and the user's answers
  > simplify-cards-Q18 and Q22.

- **The no-setup bullet's "chantier writes only …" sentence:** add "and, through the launcher's
  `--sync` in the dev mode, uv's sync of chantier's own checkout's `.venv`", so the sentence stays
  true.

## Risk

- The long gate is owed (the CLI's package and the scenario).
- The trial may fail. The host may not match a `uv run --script "<path>" *` rule as it matches
  today's `uv run --no-sync --project "<path>" chantier *`, or its classifier may treat the form
  as a package-manager run. The child then hands back blocked, and children 23 and 24 keep
  today's paragraph until the owner decides.
- One more process per CLI call (uv's script environment and a Python start). The trial
  measures the cost. See the open question.
- On Windows the launcher stays as the CLI's parent (no `exec` there). Whether stopping it, or
  the host stopping its shell, ends the CLI is **unproved** until section 8's stop check.
- The mode rule is now written twice: once in `launch.project_is_chantier` and once in
  `Repo.find` plus `is_chantier_project`. The parity test guards it, but a change to `Repo.find`'s
  project choice must update both.
- P10 asks for no launcher rule until child 24. A user who adds the rule early, from this
  child's PR, gets no warning about it either way.

## Open questions

1. **The launcher's overhead.** Each CLI call through the launcher starts one more Python, in
   uv's script environment, before the CLI's own. The trial records the median added time on the
   Driver's machine. Above what figure, if any, should child 24 keep today's paragraph rather than
   switch the cards to the launcher? Until you answer, the figure is only reported, and child 24
   switches whatever it is.
