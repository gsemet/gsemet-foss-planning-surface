# Dev mode for chantier only; a blocked sync names, waits, never kills

Short name: `sync-lock`. From the batch-29 retro, kept point 3 (the retro critic kept it).

## Goal

In the user's terms: a sync of chantier's checkout is never blocked by, and never kills, another
project's chantier process.

In batch-29, `uv sync --locked` of chantier's main checkout failed on Windows (os error 32)
because other projects' `chantier.exe` processes ran from the checkout's `.venv`: Studio's
watcher, then a Studio gate, which the user had to approve killing mid-run. Batch-17 failed the
same way, with another cause. Today any project whose session loads the plugin from chantier's
checkout runs in the dev mode (the rule is only "`<plugin root>/.git` exists"), so it runs
`uv run --no-sync --project "<plugin root>" chantier` and holds `<plugin root>/.venv`'s
executables open.

## Decisions carried (02-answers.md)

- **sync-lock-Q1 (C, both).** (a) The dev mode applies only when the session's project is chantier
  itself. Other projects run in the plugin mode, their own copy of the code through
  `uvx --from "<plugin root>"`, even when the plugin is loaded from chantier's checkout. (b) The
  sync names the processes that hold it and waits, for chantier's own processes (a gate, a
  watcher).
- **sync-lock-Q2 (A).** A sync still blocked waits, names the processes, never kills, and tells the
  user after a few minutes.
- **sync-lock-Q3 (A).** Grilled enough; specify now. The spec critic noted that the CR changes
  how every session launches the CLI (the role skills and cards).

## What changes

### 1. The launch rule: dev mode only for chantier itself

The rule becomes: **dev mode** when the plugin root holds `.git` (a folder or a file) **and** the
session's project is chantier itself; **plugin mode** in every other case, including a project
whose session loads the plugin from chantier's checkout.

"The session's project is chantier itself" means: the project's code repository is the plugin
root's repository. In-project, the session's repository (the main checkout or one of its
worktrees) has the same git common directory as the plugin root. In a planning surface, the
project's clone (its `checkout.yml` `repo:`, `Repo.root`) has the same git common directory as
the plugin root. (Today `projects/chantier/checkout.yml` holds `repo: ../../../chantier/`, the
plugin root itself.) See open question 2.

In the plugin mode, `$CHANTIER` is `uvx --from "<plugin root>" chantier --skill "<skill
folder>"` (plus `--project <folder>` in a surface), unchanged from today's plugin mode, and that
session never runs `uv sync`.

Write this rule consistently, in the same words, in each place that states it today:

- `skills/chantier/SKILL.md` (line 15), `skills/chief-of-staff/SKILL.md` (line 18),
  `skills/griller/SKILL.md` (line 16), `skills/status/SKILL.md` (line 15): the paragraph "`$CHANTIER`
  is the CLI, one launch in two modes...". The `.git` test gets the second condition; the
  "Otherwise ... plugin mode" sentence covers both "no `.git`" and "another project".
- `skills/chantier/references/concepts.md` (the `$CHANTIER` entry, line 417): "in chantier's own
  checkout" becomes "in chantier's own checkout, when the session's project is chantier".
- `skills/chantier/references/chief-of-staff.md` (Starting a batch, step 1, line 792; the
  fast-forward paragraph, line 1106) and `skills/chantier/references/foreman.md` (line 640): "In
  chantier's own checkout (the dev mode)" names the dev mode as redefined.
- `skills/chantier/references/hosts/claude-code.md` (lines 218, 267-269, 381, 448, 472): the dev
  mode's rows and the "Every batch" row say "chantier's own checkout, when the session's project is
  chantier"; the plugin mode's row says it also covers other projects run from chantier's
  checkout. The allow rules themselves (`uv run --no-sync --project * chantier *`,
  `uv sync --locked --project *`, `uvx --from * chantier *`) do not change.
- `AGENTS.md`, the bullet "The CLI is one Python package...": "in chantier's own checkout (a
  `.git` at the plugin root)" becomes "in chantier's own checkout (a `.git` at the plugin root),
  for a session whose project is chantier"; "never `uvx --from <checkout>`" changes to say that
  other projects run the plugin mode, `uvx --from <plugin root>`, even from chantier's checkout,
  and that chantier's own sessions never do (see open question 1).
- `CONTRIBUTING.md` (lines 70-80 and 220-227) and `docs/web-board.md` (lines 209-212): the same
  rule, the same words.

The CLI prints the launch for prompts and orders (`cli:` facts of `take`, the Driver prompt, the
orders, the watcher's `watch: not running` line). It must follow the same rule:

- `skills/chantier/scripts/cli/src/chantier/plugin_files.py`: `is_dev_checkout()` stays the `.git`
  test; `cli_command(repo)` and `sync_command()` return the dev form only when, in addition, the
  repo's project is chantier itself (same git common directory as the plugin root, as defined
  above); else the plugin form, and `sync_command()` returns None. `sync_command()` takes the repo
  (its only caller is `commands/preflight.py`, which has one). The callers stay:
  `commands/driver.py`, `commands/facts.py`, `commands/orders.py`, `hub/autostart.py`,
  `commands/preflight.py`.
- `hub/autostart.py`: a watcher of another project now starts with the plugin form, so it no
  longer holds `<plugin root>/.venv`.

### 2. A blocked sync: name, wait, never kill, tell the user

The dev-mode sync (`uv sync --locked --project "<plugin root>"`, run only by the steering session
at a session's start, a batch's start, and after a merge that changes `uv.lock`) behaves this way
when chantier processes hold the checkout's `.venv`:

- **Before or on a blocked sync, name the holders:** each chantier process that holds
  `<plugin root>/.venv` (its PID, what it is: a gate, a watcher, the board or hub, another
  command, and the project or worktree its command line names). How they are found is open
  question 3.
- **Wait:** the steering session waits, and retries the sync when the holders are gone.
- **Never kill:** no session stops, kills or asks to kill a holder to make the sync pass. (The
  steering session's own board stop around the sync, which the cards already prescribe, is open
  question 4.)
- **Tell the user after a few minutes:** when the holders are still there after a few minutes
  (open question 5), one line to the user naming them, and the session keeps waiting.
- **The other cases keep their handling:** a sync that fails for another reason stays "one line to
  the user with uv's text, and you go on" (chief-of-staff.md, Starting a batch, step 1); the
  failure rule of `startup-core.md` stays.

Where this goes:

- `skills/chantier/references/chief-of-staff.md`: Starting a batch, step 1 (line 792: "stop the
  board ..., run `uv sync ...`, then start the board again; no gate runs then"), and the
  fast-forward paragraph (line 1106: "sync once `$CHANTIER status` shows no gate running ...;
  until then say `sync pending`"). Both get the name, wait, never kill, tell-the-user rule.
- The four SKILL.md files: the session-start sync ("run `uv sync --locked --project "<plugin
  root>"` once, before the first `$CHANTIER` command") points to the same rule.
- `skills/chantier/scripts/cli/src/chantier/commands/preflight.py`, `_check_tools`: the P5 tail
  on Windows ("dev mode on Windows: $CHANTIER runs --no-sync; sync with ... only when no chantier
  process runs (the board, a gate): os error 32 otherwise") is printed only in the dev mode as
  redefined, and says that a blocked sync names the holders and waits, never kills.

## Out of scope

- Any kill, stop or restart of another project's or another session's chantier process.
- Changing the allow rules or `commands/permissions.py`.
- The batch-17 cause (another cause, not named in the request).
- The eval kit's own `uv run --no-sync --project <chantier root>` calls (`evals/kit/dry_run.py`),
  which run chantier's own code for chantier; and the eval workspace's `uv sync --locked`
  (`evals/kit/setup.py`), which syncs the workspace's own project.
- POSIX: os error 32 is a Windows failure; the rule is written for every system, but nothing is
  expected to block there.

## Evidence

Launch matrix, one line per cell (in the checks below):

- Plugin root with `.git`, session's project is chantier (in-project, main checkout or a
  worktree): dev form, `uv run --no-sync --project "<plugin root>" chantier`; `sync_command()` is
  the sync line.
- Plugin root with `.git`, session's project is chantier in a planning surface (clone = plugin
  root): dev form plus `--project "<folder>"`; the sync line.
- Plugin root with `.git`, session's project is another project (in-project or in a surface):
  plugin form, `uvx --from "<plugin root>" chantier --skill "<skill folder>"` (plus `--project`);
  `sync_command()` is None.
- Plugin root without `.git` (a host's plugin copy), any project: plugin form; None.

Checks:

- `skills/chantier/scripts/cli/tests/test_plugin_files.py`,
  `test_one_launch_two_modes_one_text`: extend it to the four cells above (a prepared plugin root
  with and without `.git`, a prepared repo that is or is not the plugin root's repository). Its
  part that reads the four shipped `SKILL.md` files from the repository as they ship, at the head
  under test, also asserts that each states the second condition (the session's project is
  chantier), in the same words in all four.
- The same test, or one beside it, reads the shipped `AGENTS.md`, `concepts.md` and
  `chief-of-staff.md` and asserts the rule's words there; and asserts that `chief-of-staff.md`
  states the blocked sync's "never kill" and "tell the user" rule.
- `scenario/run_scenario.py`: the scenario's sandbox project ("demo") is not chantier, so the
  printed forms change to the plugin form: the P5 check (line 970) expects no dev-mode tail; the
  `take` facts check (line 1093) expects `cli: uvx --from `; the watcher lines (`cli_form`, lines
  2086 and 9653) expect the plugin form. Add one scenario step where the project is chantier's own
  repository (the dev form and the P5 tail on Windows), if the scenario can prepare it; else the
  unit test above carries that cell, said so in the PR.
- `just check`, `just test` (within its time budget), `just eval-dry-run` (the change is under the
  CLI's `src/`), and `just scenario` per AGENTS.md.
- The wait and the user line are card behaviour: no automated check proves them; the PR's Known
  gaps says so unless open question 3 adds a CLI listing, which then gets a test on a prepared
  process list.

## Open questions for the user

1. **Stale build for other projects.** The rule "never `uvx --from <checkout>`" exists because uv
   caches a local source by its version: even with `--refresh` it served an older build
   (2026-11-14, a board with no Triage view). With this CR, other projects (Studio...) run
   `uvx --from <chantier checkout>` and may get a build older than the checkout, while their cards
   are read live from the checkout. Is that accepted (their code changes at each version bump), or
   must something keep their copy current (and what)?
2. **"chantier itself".** Is "the project's code repository is the plugin root's repository (same
   git common directory)" the right test? A second clone of chantier elsewhere would then run the
   plugin mode.
3. **How the holders are named.** By the steering session itself with the shell (the cards then
   need host-specific text in `hosts/`), or by one read-only CLI listing of the processes that hold
   `<plugin root>/.venv` (`procs.py` already lists processes through psutil)? AGENTS.md admits a
   new CLI tool only from a measured cost: batch-29 (a mid-run kill approved by the user) and
   batch-17 are the measure offered.
4. **The session's own processes.** Today the Chief of Staff stops its own board around the sync
   and starts it again; its own watcher (run for the whole session) also holds the `.venv`. Does
   "never kill" cover them (the session then waits on itself), or does the session keep stopping
   and restarting its own board, and do the same for its own watcher?
5. **"A few minutes".** How long before the user is told (for example 5 minutes), and does the
   session keep waiting after telling the user, or wait for the user's word?
6. **What the wait blocks.** At a session's start the sync comes before the first `$CHANTIER`
   command; at a batch's start it is preflight's first step. Does the session (or the batch's
   start) wait there, or go on with the environment as it is and say `sync pending`, as after a
   merge?
