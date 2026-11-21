# Dev mode only for chantier itself; other projects in plugin mode

Short name: `sync-lock`. From the batch-29 retro, kept point 3 (the retro critic kept it). This CR
is the launch part; the wait part is the inbox item `sync-lock-wait` (sync-lock-Q4).

## Goal

In the user's terms: a sync of chantier's checkout is never blocked by another project's chantier
process, because another project no longer runs chantier's checkout's own environment.

In batch-29, `uv sync --locked` of chantier's main checkout failed on Windows (os error 32)
because other projects' `chantier.exe` processes ran from the checkout's `.venv`: Studio's
watcher, then a Studio gate, which the user had to approve killing mid-run. Batch-17 failed the
same way, with another cause. Today any project whose session loads the plugin from chantier's
checkout runs in the dev mode (the rule is only "`<plugin root>/.git` exists"), so it runs
`uv run --no-sync --project "<plugin root>" chantier` and holds `<plugin root>/.venv`'s
executables open.

## Decisions carried (02-answers.md)

- **sync-lock-Q1 (C, both), launch half.** The dev mode applies only when the session's project is
  chantier itself. Other projects run in the plugin mode, their own copy of the code through
  `uvx --from "<plugin root>"`, even when the plugin is loaded from chantier's checkout. (Q1's
  other half, the wait, went to `sync-lock-wait`: Q4.)
- **sync-lock-Q2 (A).** Moved with the wait part to `sync-lock-wait` (Q4); not specified here.
- **sync-lock-Q3 (A).** Grilled enough. The spec critic noted that the CR changes how every
  session launches the CLI (the role skills and cards).
- **sync-lock-Q4 (A, split).** This CR keeps the launch part: dev mode only for chantier itself,
  P10, the tests and the scenario. The wait part (name the holders, wait, never kill, tell the
  user), the first spec's open questions 3 to 6 and the critic's findings 3, 4 and 7 (for the wait)
  are the inbox item `sync-lock-wait`.
- **sync-lock-Q5 (A).** In this CR, P10 follows the same test as the launch: a project in the
  plugin mode is offered the `uvx --from` rule, chantier the `uv run` rules (and the sync rule).
  This CR comes after `permissions-bypass` (`depends.json`: `{"after": ["permissions-bypass"]}`),
  which touches the same file, `commands/permissions.py` (critic finding 2; see "Overlap with
  permissions-bypass").
- **sync-lock-Q6.** How a session knows its project is chantier: from its own context, the project
  the session works on (its folder, or the surface project it is started on, such as
  `projects/chantier`). The question is "is the project chantier", not "does it use chantier". A
  file found only in chantier's repository may confirm it. A session in a planning surface working
  on the chantier project alone is the dev mode. This replaces the first spec's git-common-dir
  test.
- **sync-lock-Q7 (A).** The stale build for other projects is accepted: another project's code
  changes at each chantier version bump. The risk is named below and in the cards.
- **sync-lock-Q8 (A).** Grilled enough; this revision; destination the next batch (`3-ready`); a
  second spec-critic run after this revision.

## What changes

### 1. The launch rule: dev mode only for chantier itself

The rule becomes: **dev mode** when the plugin root holds `.git` (a folder or a file) **and** the
session's project is chantier itself; **plugin mode** in every other case, including a project
whose session loads the plugin from chantier's checkout.

**"The session's project is chantier itself" (Q6), as a session applies it by hand:** the session
reads its own context, the project it works on: in-project, the repository it was started in; in a
planning surface, the project it was started on (`projects/<name>`, the `--project` folder its
`$CHANTIER` carries). The project is chantier when that project is chantier (in a surface, the
project `projects/chantier`; in-project, chantier's own repository). A file only chantier's
repository holds may confirm it: the plugin manifest `.claude-plugin/plugin.json` whose `name` is
`chantier`, at the project's repository root (in a surface, its clone). A surface session working
on the chantier project alone is the dev mode; a surface session working on another project is the
plugin mode. The question asked is "is the project chantier", never "does the project use
chantier".

In the plugin mode, `$CHANTIER` is `uvx --from "<plugin root>" chantier --skill "<skill
folder>"` (plus `--project <folder>` in a surface), unchanged from today's plugin mode, and that
session never runs `uv sync`.

**The stale-build risk, accepted (Q7).** The rule "never `uvx --from <checkout>`" exists because uv
caches a local source by its version: even with `--refresh` it served an older build (2026-11-14,
a board with no Triage view). With this CR, other projects (Studio...) run
`uvx --from "<chantier checkout>"` and may get a build older than the checkout, while their cards
are read live from the checkout; their code changes at each chantier version bump. Accepted; the
`AGENTS.md` bullet and `CONTRIBUTING.md` say so in one sentence.

Write the rule consistently, in the same words, in each place that states it today:

- `skills/chantier/SKILL.md` (line 15), `skills/chief-of-staff/SKILL.md` (line 18),
  `skills/griller/SKILL.md` (line 16), `skills/status/SKILL.md` (line 15): the paragraph "`$CHANTIER`
  is the CLI, one launch in two modes...". The sentence "If `<plugin root>/.git` exists (a folder or
  a file), this is chantier's own checkout, the dev mode" gets the second condition, the session's
  project is chantier (from the session's context, as above, the manifest confirming); the
  "Otherwise it is a host's plugin copy, the plugin mode" sentence covers both "no `.git`" and
  "another project, even from chantier's checkout". The same sentence, word for word, in all four.
- `skills/chantier/references/concepts.md` (the `$CHANTIER` entry, line 417): "in chantier's own
  checkout" becomes "in chantier's own checkout, when the session's project is chantier".
- `skills/chantier/references/chief-of-staff.md` (Starting a batch, step 1, line 792; the
  fast-forward paragraph, line 1106) and `skills/chantier/references/foreman.md` (line 640): "In
  chantier's own checkout (the dev mode)" names the dev mode as redefined. Their sync behaviour is
  otherwise unchanged here (its change is `sync-lock-wait`'s).
- `skills/chantier/references/hosts/claude-code.md` (lines 218, 267-269, 381, 448, 472): the dev
  mode's rows and the "Every batch" row say "chantier's own checkout, when the session's project is
  chantier"; the plugin mode's row says it also covers other projects run from chantier's
  checkout. The allow rules' texts are this file's and `permissions-bypass`'s; this CR changes only
  which mode's rules apply to a project.
- `AGENTS.md`, the bullet "The CLI is one Python package...": "in chantier's own checkout (a
  `.git` at the plugin root)" becomes "in chantier's own checkout (a `.git` at the plugin root),
  for a session whose project is chantier"; "never `uvx --from <checkout>`" becomes: chantier's own
  sessions never run `uvx --from <checkout>`; other projects run the plugin mode,
  `uvx --from <plugin root>`, even from chantier's checkout, their build changing at each version
  bump (Q7).
- `CONTRIBUTING.md` (lines 70-80 and 220-227) and `docs/web-board.md` (lines 209-212): the same
  rule, the same words.

### 2. The CLI's own test, consistent with the session's

The CLI prints the launch for prompts and orders (`cli:` facts of `take`, the Driver prompt, the
orders, the watcher's command and `watch: not running` line) and picks P10's rules and P5's tail.
It follows the same rule, judged from the `Repo` it runs for, which is the session's project:

- `skills/chantier/scripts/cli/src/chantier/plugin_files.py`:
  - `is_dev_checkout()` stays the `.git` test on the plugin root.
  - A new `is_chantier_project(repo: Repo | None) -> bool`: in a planning surface
    (`repo.external`), the project's folder is `projects/chantier` (`repo.project_folder.name ==
    "chantier"`); in-project, `repo.root` holds `.claude-plugin/plugin.json` whose `name` is
    `chantier` (the file only chantier's repository holds). `None` (no project found) is False.
    No git-common-dir comparison with the plugin root: a second clone of chantier, or a worktree,
    is chantier too.
  - `cli_command(repo)` returns the dev form only when `is_dev_checkout()` and
    `is_chantier_project(repo)`; else the plugin form. Its docstring states the rule.
  - `sync_command(repo)` takes the repo and returns the sync line under the same two conditions;
    else None.
  - Callers: `commands/driver.py:89`, `commands/facts.py:110`, `commands/orders.py:141`,
    `hub/autostart.py:37,54` already pass the repo; `commands/preflight.py` passes it to
    `_check_tools` (today `_check_tools(r)` at line 288; `repo` is in scope from line 285) and to
    `sync_command(repo)` (line 102).
- `hub/autostart.py`: a watcher of another project now starts with the plugin form, so it no
  longer holds `<plugin root>/.venv`.
- `commands/preflight.py`, `_check_tools`: the P5 Windows tail ("dev mode on Windows: $CHANTIER
  runs --no-sync; sync with ... only when no chantier process runs ...") is printed only in the
  dev mode as redefined, since it keys on `sync_command(repo)`. Its wording is otherwise unchanged
  here.
- `commands/permissions.py`, `_forges(remote)` (line 256): the `"dev"` / `"plugin"` choice
  (line 261, today `"dev" if is_dev_checkout() else "plugin"`) follows the same test as the launch
  (Q5): `_forges` takes the repo (from `commands_not_allowed(repo, ...)`, line 366) and adds
  `"dev"` only when `is_dev_checkout()` and `is_chantier_project(repo)`, else `"plugin"`. A project
  in the plugin mode is then offered the `uvx --from` rule; chantier the `uv run --no-sync` and
  `uv sync --locked` rules. The import of `is_dev_checkout` (line 17) becomes the import the new
  test needs.

### 3. Overlap with permissions-bypass

`permissions-bypass` (ordered before this CR) rewrites P10's plugin-mode sample and rule in
`commands/permissions.py` (the `SAMPLES` rows at lines 64-81: the rule becomes
`uvx --from "<plugin root>" chantier *`, built from `cli_command`'s plugin form) and adds deny
rules. This CR touches the same file only at `_forges` (which rows apply: dev or plugin), and calls
the plugin form through the same `plugin_files` functions. The Driver rebases on
`permissions-bypass`'s merged head and keeps its sample and rule texts; if `permissions-bypass`
builds the plugin sample from `cli_command(repo)`, that call must ask for the plugin form whatever
the project (the sample names the plugin-mode rule), which the Driver checks after the rebase.

## Out of scope

- The wait part: a blocked sync naming chantier's holders, waiting, never killing, telling the
  user after a few minutes, and the first spec's open questions 3 to 6 (how the holders are named,
  the session's own board and watcher, "a few minutes", what the wait blocks), with the critic's
  findings 3, 4 and 7 for it: the inbox item `1-inbox/sync-lock-wait` (sync-lock-Q4). The sync
  paragraphs of `chief-of-staff.md` (lines 792, 1106), the SKILL.md session-start sync sentence's
  behaviour on a block, and the P5 tail's wording stay as they are here.
- Any kill, stop or restart of another project's or another session's chantier process.
- The allow and deny rules' texts (`permissions-bypass`'s); this CR changes only which mode's
  rows apply.
- Keeping another project's build current beyond the version bump (Q7: accepted).
- The batch-17 cause (another cause, not named in the request).
- The eval kit's own `uv run --no-sync --project <chantier root>` calls (`evals/kit/dry_run.py`),
  which run chantier's own code for chantier; and the eval workspace's `uv sync --locked`
  (`evals/kit/setup.py`), which syncs the workspace's own project.
- POSIX: os error 32 is a Windows failure; the rule is written for every system.

## Evidence

Launch matrix, one line per cell (the checks below carry each):

- Plugin root with `.git`, in-project, repo root holding chantier's manifest (main checkout or a
  worktree): dev form, `uv run --no-sync --project "<plugin root>" chantier`; `sync_command(repo)`
  is the sync line; P10 offers the `uv run` and `uv sync` rules; P5's Windows tail printed.
- Plugin root with `.git`, planning surface, project `projects/chantier`: dev form plus
  `--project "<folder>"`; the sync line; P10's dev rules.
- Plugin root with `.git`, another project (in-project, no chantier manifest; or a surface project
  not named `chantier`): plugin form, `uvx --from "<plugin root>" chantier --skill "<skill
  folder>"` (plus `--project`); `sync_command(repo)` is None; P10 offers the `uvx --from` rule; no
  P5 tail.
- Plugin root without `.git` (a host's plugin copy), any project, chantier included: plugin form;
  None; P10's plugin rule.
- No project found (`repo` None): plugin form; None.

Checks:

- `skills/chantier/scripts/cli/tests/test_plugin_files.py`,
  `test_one_launch_two_modes_one_text` (line 361): extend `command_for` to the cells above, with a
  prepared plugin root with and without `.git` and a prepared `Repo` that is or is not chantier
  (in-project with and without the manifest; external with a `projects/chantier` folder and with
  another name). Prepared texts here are inputs (repositories), not shipped files.
- The same test's part that reads the four shipped `SKILL.md` files (`PLUGIN_ROOT / "skills" /
  name / "SKILL.md"`, line 384) from the repository as they ship, at the head under test, also
  asserts that each states the launch sentences this CR changes: the second condition (the
  session's project is chantier, from the session's context) and the plugin mode covering another
  project run from chantier's checkout; and that the dev-mode sentence is the same text in all
  four (extracted and compared, not only each containing a phrase).
- The same test, or one beside it, reads the shipped `AGENTS.md`, `concepts.md` and
  `hosts/claude-code.md` from the repository at the head under test and asserts the rule's words
  there ("when the session's project is chantier", or the chosen phrase, the same in each), and
  the stale-build sentence in `AGENTS.md`.
- A permissions test (beside the existing P10 tests): `commands_not_allowed` for a repo that is
  chantier with a `.git` plugin root counts the `uv run` and `uv sync` samples and not the `uvx`
  one; for another project from the same plugin root, the `uvx` sample and not the dev ones.
- `scenario/run_scenario.py`: the scenario's sandbox project ("demo") is not chantier, so the
  printed forms change to the plugin form: the P5 check (line 970) expects no dev-mode tail; the
  `take` facts check (line 1093) expects `cli: uvx --from `; the watcher lines (`cli_form`, lines
  2086 and 9653) expect the plugin form; any P10 line the scenario checks expects the plugin rule.
  Add one scenario step where the project is chantier (dev form and, on Windows, the P5 tail) if
  the scenario can prepare it; else the unit tests above carry that cell, said so in the PR.
- `just check`, `just test` (within its time budget), `just eval-dry-run` (the change is under the
  CLI's `src/`), and `just scenario` per AGENTS.md.
- A session applying the rule by hand (Q6) is card behaviour: no automated check proves a session's
  reading of its context; the shipped-text checks above prove the cards say it. The PR's Known gaps
  says so.

## Open questions for the user

1. **The CLI's test in a planning surface.** The CLI takes a surface project as chantier from its
   folder's name (`projects/chantier`), the session's context. Should it also require the file only
   chantier's repository holds (the manifest in the project's clone) to confirm it, which would
   make a surface with a missing clone run the plugin mode?
