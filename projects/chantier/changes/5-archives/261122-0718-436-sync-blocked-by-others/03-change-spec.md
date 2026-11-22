# Dev mode only for chantier itself; other projects in plugin mode

Short name: `sync-lock`. From the batch-29 retro, kept point 3 (the retro critic kept it). This CR
is the launch part; the wait part is the inbox item `sync-lock-wait` (sync-lock-Q4). It lands in
batch-30 right after CR-432 (`permissions-bypass`), on CR-432's merged head (sync-lock-Q10, the
user's words of 2026-11-21; `depends.json`: `{"after": ["permissions-bypass"]}`).

Spec v3 (2026-11-21): the spec critic's run-2 findings 1 to 3 and sync-lock-Q12 applied.

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
- **sync-lock-Q5 (A).** P10 follows the same test as the launch: a project in the plugin mode is
  offered the `uvx --from` rule, chantier the `uv run` rule and the sync rule. This CR comes after
  CR-432, which touches the same file, `commands/permissions.py` (section 3).
- **sync-lock-Q6.** How a session knows its project is chantier: from its own context, the project
  the session works on (its folder, or the surface project it is started on, such as
  `projects/chantier`). The question is "is the project chantier", not "does it use chantier". A
  file found only in chantier's repository may confirm it. A session in a planning surface working
  on the chantier project alone is the dev mode.
- **sync-lock-Q7 (A).** The stale build for other projects is accepted: another project's code
  changes at each chantier version bump. The risk is named below and in the cards.
- **sync-lock-Q8 (A).** Grilled enough; the revision to the launch part; a second critic run.
- **sync-lock-Q9 (A).** In a planning surface, the CLI takes the project as chantier from its
  folder's name (`projects/chantier`) alone; the manifest in the project's clone is only a
  possible confirmation, never required (a surface with a missing clone stays in the dev mode for
  `projects/chantier`).
- **sync-lock-Q10 (C)** and the user's words of 2026-11-21: set aside with `permissions-bypass`,
  then taken up with it: batch-30, after CR-432.
- **sync-lock-Q12 (B, a Fable advisor in the user's place, under Q7).** The surface-wide processes
  on another project's build are accepted in words only (section 1, "The stale-build risk,
  accepted"); a notice of a foreign build is out of scope (inbox item
  `surface-server-foreign-build`).

## What changes

Paths: `CLI/` is `skills/chantier/scripts/cli/src/chantier/`, `REF/` is
`skills/chantier/references/`, `TESTS/` is `skills/chantier/scripts/cli/tests/`.

**Finding the places.** The Driver works on CR-432's merged head and finds each place below by
its text (the function's name, the quoted sentence or row), never by a line number: CR-432 moves
the lines. Where a quoted sentence is today's text and CR-432 rewrites it, the Driver edits
CR-432's text with the same intent.

### 1. The launch rule: dev mode only for chantier itself

The rule becomes: **dev mode** when the plugin root holds `.git` (a folder or a file) **and** the
session's project is chantier itself; **plugin mode** in every other case, including a project
whose session loads the plugin from chantier's checkout.

**"The session's project is chantier itself" (Q6, Q9), as a session applies it by hand:** the
session reads its own context, the project it works on: in-project, the repository it was started
in; in a planning surface, the project it was started on (`projects/<name>`, the `--project`
folder its `$CHANTIER` carries). The project is chantier when that project is chantier: in a
surface, the project folder `projects/chantier`, by its name alone; in-project, chantier's own
repository, which the plugin manifest at the repository's root confirms
(`.claude-plugin/plugin.json` or `.github/plugin/plugin.json` whose `name` is `chantier`). A
surface session working on the chantier project alone is the dev mode; a surface session working
on another project is the plugin mode. The question asked is "is the project chantier", never
"does the project use chantier".

In the plugin mode, `$CHANTIER` is `uvx --from "<plugin root>" chantier --skill "<skill
folder>"` (plus `--project <folder>` in a surface), unchanged from today's plugin mode, and that
session never runs `uv sync`.

**The stale-build risk, accepted (Q7, Q12).** The rule "never `uvx --from <checkout>`" exists
because uv caches a local source by its version: even with `--refresh` it served an older build
(2026-11-14, a board with no Triage view). With this CR, other projects (Studio...) run
`uvx --from "<chantier checkout>"` and may get a build older than the checkout, while their cards
are read live from the checkout; their code changes at each chantier version bump. The same holds
for the surface-wide processes: the board server, its writer and the forge hub, started from
another project's session in plugin mode, run that cached build and serve every project of the
surface, chantier included; a chantier session sees no notice while the version string is equal
(`hub/state.py`'s `other_version`, behind `hub/autostart.py`'s `board_clause`, compares only
the version string, and the board's `already serves this surface` line names only the version); that build is refreshed at the
next version bump, or when the process is stopped by hand and a chantier session starts it again.
Accepted. The sentence to write, the same in each place Q12 names (the `AGENTS.md` bullet below,
`CONTRIBUTING.md`, and `REF/session-start.md`, the card that starts the board and the watcher that
can be the hub):

> Another project runs chantier from its checkout in plugin mode, a build uv caches by version: it
> changes at each version bump. The board server, its writer and the forge hub, started from
> another project's session, run that build and serve every project of the surface, chantier
> included, with no notice while the version is equal, until the next version bump or until
> stopped by hand and started again from a chantier session.

Write the rule consistently, in the same words, in each place that states it:

- The four SKILL.md files that define `$CHANTIER`: `skills/chantier/SKILL.md`,
  `skills/chief-of-staff/SKILL.md`, `skills/griller/SKILL.md`, `skills/status/SKILL.md`, the
  paragraph that begins "`$CHANTIER` is the CLI, one launch in two modes". The sentence "If
  `<plugin root>/.git` exists (a folder or a file), this is chantier's own checkout, the dev mode"
  gets the second condition, the session's project is chantier (from the session's context; in a
  surface the folder `projects/chantier`; in-project the manifest confirming); the sentence
  "Otherwise it is a host's plugin copy, the plugin mode" covers both "no `.git`" and "another
  project, even from chantier's checkout". CR-432's added path sentence (`<plugin root>` is
  written absolute, with forward slashes, quoted, the same path as P10's rule holds...) is kept
  word for word. The whole paragraph is the same text in all four files.
- `REF/concepts.md`, the `$CHANTIER` entry: "in chantier's own checkout" becomes "in chantier's
  own checkout, when the session's project is chantier"; CR-432's path sentence there is kept word
  for word.
- `REF/chief-of-staff.md` (Starting a batch, step 1, the sync sentence; the fast-forward paragraph
  after a merge that changes `uv.lock`) and `REF/foreman.md` (its "chantier's own checkout"
  sentence): "In chantier's own checkout (the dev mode)" names the dev mode as redefined. Their
  sync behaviour is otherwise unchanged here (its change is `sync-lock-wait`'s).
- `REF/hosts/claude-code.md`: the `uv` row of the tools table, the three chantier rows of "Allow
  rules", the "Every batch" row of "Capabilities and their commands" and the two lines that name
  the chantier rules' trial: the dev mode reads "chantier's own checkout, when the session's
  project is chantier"; the plugin row's "Risk accepted" (CR-432's "every chantier subcommand of
  the plugin at that path") also covers another project run from chantier's checkout: the rule
  then names the checkout's path and lets through every chantier subcommand of the build uv
  caches from it. The rules' texts, Marks and placeholders stay CR-432's; this CR changes only
  which mode's rules apply to a project.
- `AGENTS.md`, the bullet "The CLI is one Python package...": "in chantier's own checkout (a
  `.git` at the plugin root)" becomes "in chantier's own checkout (a `.git` at the plugin root),
  for a session whose project is chantier"; "never `uvx --from <checkout>`" becomes: chantier's own
  sessions never run `uvx --from <checkout>`; other projects run the plugin mode,
  `uvx --from <plugin root>`, even from chantier's checkout; then the Q12 sentence above.
- `CONTRIBUTING.md`: the CLI paragraph of the architecture list ("Installed as a plugin, it runs
  by `uvx --from`...") and the paragraph "In this checkout, `$CHANTIER` runs the local code,
  live": the same rule, the same words, and the Q12 sentence once.
- `docs/web-board.md`, "By hand" ("In chantier's own checkout, start it with `uv run --no-sync`
  ... never `uvx --from <checkout>`"): "for the chantier project; another project's session runs
  it in plugin mode".
- `REF/session-start.md`, the paragraph **The board.** (it starts the board, the writer and the
  hub) and **The watcher.** (a watcher with no board is the hub): the Q12 sentence once, after
  **The board.**'s first paragraph, which **The watcher.** points to.

### 2. The CLI's own test, consistent with the session's

The CLI prints the launch for prompts and orders (`cli:` facts of `take`, the Driver prompt, the
orders, the watcher's command and `watch: not running` line), and picks P10's rules and P5's tail.
It follows the same rule, judged from the `Repo` it runs for, which is the session's project.

- `CLI/plugin_files.py`:
  - `is_dev_checkout()` stays the `.git` test on the plugin root.
  - A new `is_chantier_project(repo: Repo | None) -> bool`: in a planning surface
    (`repo.external`), the project's folder is named `chantier` (`repo.project_folder.name ==
    "chantier"`, Q9, no clone needed); in-project, `repo.root` holds `.claude-plugin/plugin.json`
    or `.github/plugin/plugin.json` whose `name` is `chantier` (an unreadable or non-JSON file is
    False). `None` (no project found) is False. No git-common-dir comparison with the plugin root:
    a second clone of chantier, or a worktree, is chantier too.
  - `cli_command(repo)` and `sync_command(repo)` keep CR-432's composition: each calls CR-432's
    per-form functions (the plugin form, the dev form, the sync line), which build the text from
    the plugin root whatever the mode. This CR adds only the second condition: the dev form and
    the sync line when `is_dev_checkout()` and `is_chantier_project(repo)`; else the plugin form
    and None. `sync_command` takes `repo: Repo | None = None` if CR-432 left it without one.
    `cli_command`'s docstring states the rule.
  - Callers: `commands/driver.py`, `commands/facts.py`, `commands/orders.py` and
    `hub/autostart.py` already pass the repo to `cli_command`. `commands/preflight.py`: `preflight`
    passes its `repo` (from `_open_project`) to `_check_tools`, which passes it to
    `sync_command(repo)`.
- `hub/autostart.py`: a watcher of another project now starts with the plugin form, so it no
  longer holds `<plugin root>/.venv`.
- `commands/preflight.py`, `_check_tools`: the P5 Windows tail ("dev mode on Windows: $CHANTIER
  runs --no-sync; sync with ...") is printed only in the dev mode as redefined, since it keys on
  `sync_command(repo)`. Its wording is unchanged here.
- `CLI/commands/permissions.py`, one mode helper: a private function, for instance
  `_dev_mode(repo: Repo | None) -> bool`, true only when `is_dev_checkout()` and
  `is_chantier_project(repo)`. `commands_not_allowed(repo, ...)` passes its `repo` to it (through
  the functions that need the mode), and every mode test of the file uses it, none calling
  `is_dev_checkout()` directly:
  - `_forges` (it takes the repo): `"dev"` when the helper is true, else `"plugin"`;
  - CR-432's replacing-rule count (only the samples of this install's mode count: the plugin
    sample in plugin mode, the dev sample and the sync line in dev mode);
  - CR-432's stale-rule rules (a plugin-form rule of another path stale only in plugin mode; in
    dev mode plugin-form rules are left alone; a dev-form rule stale in either mode only when its
    folder is gone).
  The import of `is_dev_checkout` becomes the imports the helper needs. P10's samples and rules
  keep coming from CR-432's form and rule functions, the plugin-form sample built whatever the
  mode (CR-432 §1). The probes, the broad-rule matching and the P10 line's wording are CR-432's,
  unchanged.

**What a session already set up sees (Q21 of CR-432).** A Studio session whose user added
CR-432's real-path dev rules (`uv run --no-sync --project "<checkout>" chantier *`,
`uv sync --locked --project "<checkout>"`) runs in plugin mode after this CR: at its next batch
start P10 names one missing rule, `uvx --from "<checkout>" chantier *`, and the Chief of Staff asks
one question for it. Its dev rules stay and are not named stale (a dev rule is stale only when its
folder no longer exists, and the checkout exists). A chantier session keeps its dev rules and is
asked nothing new.

### 3. On CR-432's merged head

CR-432 (batch-30) gives, in `CLI/plugin_files.py`, one function per form (the plugin form, the dev
form, the sync line) and the filled rule functions, and in `CLI/commands/permissions.py` the
placeholder `SAMPLES` filled from them, the broad-rule probes, the replacing rules and the stale
rules. This CR re-applies on that head as follows, and touches nothing else of CR-432's:

- `cli_command(repo)` and `sync_command(repo)`: CR-432's composition kept, the second condition
  `is_chantier_project(repo)` added (section 2).
- `permissions.py`: the mode helper replaces each `is_dev_checkout()` mode test CR-432 has or adds
  (section 2); the rows, probes, rule texts and P10 line are CR-432's.
- The cards: CR-432's added `$CHANTIER` path sentence kept word for word; its host card rows, Marks
  and paragraphs kept, with section 1's mode words added.
- CR-432's tests and scenario check, whose mode came from `is_dev_checkout()`, follow the helper
  (Evidence).

## Out of scope

- The wait part: a blocked sync naming chantier's holders, waiting, never killing, telling the
  user after a few minutes, and the first spec's open questions 3 to 6, with the critic's findings
  3, 4 and 7 for it: the inbox item `1-inbox/sync-lock-wait` (sync-lock-Q4). The sync paragraphs
  of `chief-of-staff.md`, the SKILL.md sync sentence's behaviour on a block, and the P5 tail's
  wording stay as they are here.
- A notice that the board server, writer or hub runs another project's build at an equal version
  string: the inbox item `surface-server-foreign-build` (sync-lock-Q12).
- Any kill, stop or restart of another project's or another session's chantier process.
- The allow rules' texts, probes and P10 wording (CR-432's); this CR changes only which mode's
  rules apply.
- Keeping another project's build current beyond the version bump (Q7: accepted).
- The batch-17 cause (another cause, not named in the request).
- The eval kit's own `uv run --no-sync --project <chantier root>` calls (`evals/kit/dry_run.py`),
  which run chantier's own code for chantier; and the eval workspace's `uv sync --locked`
  (`evals/kit/setup.py`), which syncs the workspace's own project.
- POSIX: os error 32 is a Windows failure; the rule is written for every system.

## Host and default matrix

The launch depends on the install (a `.git` at the plugin root or not) and the session's project;
P10 exists on Claude Code only. One line per cell:

| Cell | Launch, sync, P5 | P10 (Claude Code) |
| --- | --- | --- |
| `.git` plugin root, in-project, repo root with chantier's manifest (main checkout or a worktree) | dev form; the sync line; P5's Windows tail | the dev rule and the sync rule; plugin-form rules left alone |
| `.git` plugin root, surface, `projects/chantier` (clone present or not) | dev form plus `--project "<folder>"`; the sync line | as above |
| `.git` plugin root, another project (in-project with no chantier manifest, or a surface project with another name) | plugin form `uvx --from "<plugin root>" chantier --skill "<skill folder>"` (plus `--project`); no sync line; no P5 tail | the plugin rule with the checkout's path; a plugin rule of another path stale; dev rules of an existing checkout left alone |
| No `.git` (a host's plugin copy), any project, chantier included | plugin form; no sync line | the plugin rule with the copy's path |
| No project found (`repo` None) | plugin form; no sync line | the plugin rule |
| Copilot, any cell | the same launch | no P10 |

## Evidence

Checks read shipped files from the repository as they ship, at the head under test; prepared
repositories and settings files are inputs, not shipped files.

- `TESTS/test_plugin_files.py`, `test_one_launch_two_modes_one_text`: extend `command_for` to the
  launch cells above, with a prepared plugin root with and without `.git` and a prepared `Repo`
  that is or is not chantier (in-project with and without the manifest, each of the two manifest
  files; external with a `projects/chantier` folder and no clone, and with another name), for
  both `cli_command(repo)` and `sync_command(repo)`; and `repo` None.
- The same test's part that reads the four shipped SKILL.md files (`PLUGIN_ROOT / "skills" / name
  / "SKILL.md"`): it extracts the whole paragraph that begins "`$CHANTIER` is the CLI, one launch
  in two modes" from each and asserts the four are the same text; and that the paragraph states
  the second condition (the session's project is chantier), the plugin mode covering another
  project run from chantier's checkout, and CR-432's path sentence.
- Beside it, one test reads the shipped `AGENTS.md`, `CONTRIBUTING.md`, `REF/concepts.md`,
  `REF/hosts/claude-code.md` and `REF/session-start.md` and asserts the rule's phrase ("when the
  session's project is chantier", or the chosen phrase, the same in each that states the dev mode)
  and the Q12 sentence, the same text, in `AGENTS.md`, `CONTRIBUTING.md` and `REF/session-start.md`.
- `TESTS/test_cli_runs.py`, CR-432's mode-parametrized P10 tests (the plugin rule or the dev rules
  named; the broad rules with or without a replacing rule; the stale rules): the "plugin" case
  stays a plugin root with no `.git`; the "dev" case needs a `.git` plugin root and a chantier
  `Repo` (a prepared repository holding chantier's manifest); a third case, a `.git` plugin root
  with another project's `Repo`, expects exactly the plugin case's outcome (the plugin rule with
  the checkout's path; `uvx --from *` replaced by it; the two dev forms and `uv run --script * *`
  "no chantier command needs it"; a plugin rule of another path stale; a dev rule of an existing
  folder not named).
- `scenario/run_scenario.py`: the sandbox project ("demo") is not chantier, so it now runs in plugin
  mode even from chantier's checkout:
  - the P5 check expects no "dev mode on Windows" tail;
  - the `take` facts check expects `cli: uvx --from ` in place of `cli: uv run --no-sync --project `;
  - the watcher lines (both `cli_form` definitions) expect the plugin form,
    `uvx --from "<plugin root>" chantier --skill "<skill folder>"`;
  - CR-432's broad-rule check (it sets `uvx --from * chantier *`,
    `uv run --no-sync --project * chantier *` and `uv run --script * *`) takes its mode from the
    sandbox's project, now plugin mode: a replacing rule (the plugin rule with the checkout's path)
    for `uvx --from *`, and "no chantier command needs it" for `uv run --no-sync --project *` and
    `uv run --script * *`; the settings it writes for "P10 ok" are the plugin mode's filled rules.
  The chantier cells (dev form, the P5 tail on Windows, the dev rules) are carried by the unit
  tests above; the scenario prepares no chantier project, which the PR says.
- Gates owed (`AGENTS.md`): `just check`, `just test` within its time budget, `just eval-dry-run`
  (the CLI's `src/` changes), and the pipeline's `just scenario (ubuntu-latest)` job at the PR's
  head; as the top CR of batch-30 while it is, `chantier gate` locally. No `hooks/` or `types/`
  change.
- A session applying the rule by hand (Q6) is card behaviour: no automated check proves a
  session's reading of its context; the shipped-text checks prove the cards say it. The board,
  writer and hub on another project's build (Q12) are accepted in words; no check proves them. The
  PR's Known gaps says both.

## Open questions for the user

None: the answers through sync-lock-Q12 settle every point of the launch part.
