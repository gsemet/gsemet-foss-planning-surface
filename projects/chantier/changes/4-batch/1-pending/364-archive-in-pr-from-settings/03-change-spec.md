# Archive in the PR: off unless the project asks for it

## Goal

In the batch-05 retro of markdown-okf-schema-studio, `ship` printed `archive missing from the PR`
for every CR, and `take` printed `archive: in the PR at <path>`. That project ignores
`.agents/changes/` in git and keeps its CRs on the planning surface, so the Chief of Staff told each
Driver by hand not to add an archive. The user wants this fixed for good: the project's settings
decide whether a CR's cleaned archive goes in its PR. `take` and `ship` read that setting. When it
is off they do not expect an archive and do not report one as missing, and the cards do not ask
for one, so nobody has to tell a Driver by hand.

## Where things stand (read-only investigation)

- The setting already exists, and the CLI already reads it once. `Repo._external`
  (`skills/chantier/scripts/cli/src/chantier/core/repo.py`) looks in the surface's
  `projects/<name>/project.md` for the line `^\W*Archive in the PR:\s*(yes|no)\b` (any case) and
  stores the result in `Repo.archive_in_pr`. Today a missing line or a missing `project.md` gives
  `True`: only an explicit `no` turns it off.
- Every reader goes through that one value:
  - `plugin_files.archive_path(repo, c)` returns `None` when the project is in-project or
    `archive_in_pr` is false.
  - `take` (`commands/driver.py`, `_cr_driver_block`) adds the archive path to the CR Driver's
    `writes:` line only when `archive_path` returns a path.
  - The facts (`commands/facts.py`, `_external_lines`) print `archive: in the PR at <path>` or
    `archive: not in the PR`.
  - `ship` (`commands/delivery.py`, `ship`) adds `off: archive missing from the PR at <path>` and
    records `archive_seen` only when `archive_path` returns a path.
  - `delivery.md` (`lifecycle/stages.py`, `_delivery`) writes `Archive in the PR: no (project
    setting)` when `archive_in_pr` is false.
- markdown-okf-schema-studio got its line (`- Archive in the PR: no (...)`) in the surface on
  2026-11-17, after its batch-05 ran. That is the manual fix. This CR is the lasting one: a project
  that never states the setting no longer gets the archive.
- In-project mode (CRs in the project's own `.agents/changes/`) never puts an archive in the PR:
  `archive_path` returns `None` whenever `repo.external` is false.
- chantier keeps no `CHANGELOG.md`: `docs/release-process.md`, "Release notes", says the notes of a
  version are written in its version PR (`docs/release-notes/YYYY-MM-DD-vX.Y.Z/release-notes.md`)
  from the commits since the previous tag and from the CRs' PR descriptions.

## Decisions carried from 02-answers.md

1. **The setting.** The existing setting is kept as the one source: the `- Archive in the PR:
   yes|no` line of the surface's `projects/<name>/project.md`. That setting already exists, so no
   key is added to `chantier.yaml`. It is read once into `Repo.archive_in_pr`. `take` and `ship`
   read that value and nothing else. When it is off they neither expect an archive nor report one
   as missing.
2. **The default.** With an external planning surface the default becomes **off**: no line, a
   line with neither `yes` nor `no`, or no `project.md` all give `archive_in_pr = False`. Only
   `yes` turns it on. In-project the behaviour does not change (no archive in the PR, as today).
   AGENTS.md's "a CR's cleaned archive in its PR when the project asks for it" stays true word for
   word: the project now asks by writing `yes`.
3. **The cards.** When the setting is off, the Driver's card and the PR template do not ask for
   the archive. No hand-written instruction to a Driver is needed.
4. **The spec critic** reviews this specification, because it changes what `ship` reports and what
   a Driver ships. This decision is for the one who grills, not for the Driver.
5. **The user's own surface projects.** No `- Archive in the PR: yes` line is added to
   `projects/agentic-planning-surface` or `projects/okf-schema`: their CRs live on the surface, so
   the new default (off) is the intended behaviour for them too. This CR edits no surface's
   `project.md`.
6. **A default change, named as such.** The default becomes `no` for every external surface, even
   though the setting already exists: a project whose CRs live on the surface should not have to
   declare it. The change is named where the project records its changes for its users, as a
   default change, with the `- Archive in the PR: yes` line that keeps the old behaviour (see
   "Change record" below).

## What changes

### CLI

- `skills/chantier/scripts/cli/src/chantier/core/repo.py`, `Repo._external`: the last argument
  becomes true only when the line is found and says `yes`, in place of
  `not (mine and mine[1].lower() == "no")`. The regex and the file it reads do not change. The
  field `Repo.archive_in_pr` keeps its name. In-project, `Repo.find` builds the `Repo` with no
  `archive_in_pr` argument, so the dataclass default applies there. `archive_path` ignores it
  in-project, so either default is correct. The Driver may set the field default to `False` so
  that the field reads the same in both modes, and records that choice in its notes.
- `skills/chantier/scripts/cli/src/chantier/plugin_files.py`, `archive_path`: its docstring says
  `None` when the mode is in-project or the project does not set `- Archive in the PR: yes`. No
  logic change.
- No change to `take`, the facts, `ship` or `_delivery`. They already read only
  `archive_path` / `archive_in_pr`, and once the default changes they print `archive: not in the
  PR`, add no archive path to `writes:`, add no `archive missing` off line, and write
  `Archive in the PR: no (project setting)` in `delivery.md`. No new message and no new refusal.

### Cards (`skills/chantier/references/`)

- `concepts.md`, "Planning surface": `` `- Archive in the PR: yes|no`, `yes` when absent `` becomes
  `` `no` when absent ``. "Archive" (the cleaned archive in the PR "when `take` prints `archive: in
  the PR at <path>`") stays as it is.
- `driver.md`:
  - In the `writes:` paragraph (around line 89), "you write your notes, `pr-body.md`, your large
    outputs and the archive" becomes "... and, when `take` prints an archive path, the archive".
  - In "The archive in the PR" (lines 422 to 439), keep the trigger on `archive: in the PR at
    <path>`. The paragraph's last sentence today is "`archive: not in the PR`: nothing to add."
    (line 439). Replace that sentence, do not add a second one, with: `archive: not in the PR`
    means no archive in the worktree, no `.agents/changes/` path in the diff, and no `delivery.md`
    to write for the PR; that is the default with a planning surface.
  - In the CI paragraph (around line 444), "the archive's `delivery.md`" becomes "the archive's
    `delivery.md` when `take` printed an archive path".
  - In "CR driver" (around line 626), "It writes only its notes, `pr-body.md` and the CR's
    archive" becomes "... and, when `take` prints an archive path, the CR's archive".
- `pr-template.md`, "The rules": after the bullet "When `take` says `archive: in the PR at
  <path>`...", add that when `take` says `archive: not in the PR`, the diff holds no archive folder
  and the description names none. The template body and the audit do not change.
- `agents/` and `com.github.copilot/agents/` are not touched: the contract lives in the cards.

### Docs

- `docs/planning-modes.md`:
  - Table row "Archive in the PR", External column: `by the project's setting, default no`.
  - "`project.md` is your prose. One fixed line is read: `- Archive in the PR: yes` or `no`
    (`no` when absent)."
  - "Archives, in two places": "when `project.md` says `yes` (or says nothing)" becomes "when
    `project.md` says `yes`".
- `docs/planning-folder.md` (line 43) and `docs/planning-modes.svg` / `docs/planning-modes-texts.md`
  ("archive in the PR, by the setting") are already correct: no change. The demo projects'
  `project.md` files (`docs/demo/projects/*/project.md`) keep their explicit `yes`.
- `scenario/README.md` (around line 266): the external-mode line names the default, for instance
  "`not in the PR` for a project that does not set it to `yes`".

### Change record (decision 6)

chantier has no `CHANGELOG.md`, and the next version's release folder is created by its version
PR, not by a CR (`scripts/release_notes.py --check` expects one notes folder for the current
version). So the default change is recorded where the next release notes are written from:

- The commit that changes `Repo._external` carries, in its body, a paragraph starting
  `Default change:` that says: with an external planning surface, a CR's cleaned archive no longer
  goes in its PR unless the project's `project.md` holds `- Archive in the PR: yes`; add that line
  to keep the old behaviour.
- The PR description's summary carries the same paragraph, under the same `Default change:` lead.
- Do not create a `CHANGELOG.md` or a `docs/release-notes/` folder. The version PR's author writes
  the next release notes from these commits and PR descriptions (`docs/release-process.md`), so the
  notes name the default change and the line.

## Out of scope

- A `chantier.yaml` key for the archive: the existing `project.md` line is the setting, as the
  answers chose.
- Detecting that the project's repository ignores `.agents/changes/` and inferring the setting
  from it: not decided, not done. The Driver card's existing "When the project ignores
  `.agents/changes/` ... the Chief of Staff asks the user (no `git add -f`)" stays as it is. With
  the new default it only applies to a project that wrote `yes`.
- In-project mode: no change.
- Editing any surface's `project.md` (decision 5): the surface is not this repository.
- The AGENTS.md wording on configuration: it does not change (decision 2).
- Writing the next version's release notes (see "Change record").

## Evidence

- **Unit test (new, one parametrized test, fast).** In
  `skills/chantier/scripts/cli/tests/test_cli_runs.py`, or the test file that already covers
  `Repo` in external mode, add one test parametrized over the content of
  `projects/demo/project.md` in a minimal surface: no file, a file without the line,
  `- Archive in the PR: no`, `- Archive in the PR: no (comment)`, `- Archive in the PR: yes`,
  `- Archive in the PR: Yes`. For each case it asserts `Repo.find(project=...).archive_in_pr`
  (true only for the two `yes` cases), and that `plugin_files.archive_path(repo, cr)` is `None`
  exactly when that value is false. The `project.md` texts are the user's own input, prepared on
  purpose, and are not a shipped file. The test must fail on the current code: the "no file" and
  "no line" cases give `True` today.
- **Existing unit test, parametrized over two cases, with one `ship` each.**
  `test_an_external_surface_gets_the_planning_folder_and_the_project_stays_clean`
  (`tests/test_cli_runs.py`) writes no `project.md` today and asserts `archive: in the PR at ...`
  and the archive in `writes:`. It becomes parametrized over the content of
  `projects/demo/project.md`, written before the surface's first commit:
  - **no `project.md`** (the shipped default): `take` prints `archive: not in the PR`, and the CR
    Driver prompt's `writes:` line holds only the CR folder, with no second path.
  - **`- Archive in the PR: yes`**: the existing checks hold as they are (`archive: in the PR at
    .agents/changes/5-archives/`, `_the_cr_drivers_writes_hold_the_folder_then_the_absolute_archive`).

  In both cases the test then runs `ship` once, as `test_carry_ship.py`'s `stack` fixture does:
  `git worktree add` at the CR's recorded `worktree` and `branch` in the clone, one commit there,
  `monkeypatch.setattr(delivery, "read_state", lambda link: ("main", False, ""))`, then
  `chantier("ship", "CR-101", PR)`. It asserts exit 0, and that `ship`'s output holds no line
  containing `archive missing` in the no-`project.md` case and a line containing `archive missing
  from the PR at .agents/changes/5-archives/` in the `yes` case. The test's existing final checks
  (the surface shows only `projects/demo/changes/` files, the clone's main checkout is clean) run
  before the worktree is added, or are kept true by it; the Driver places them so they still hold.
  This is the off case of `ship` proved through `ship` itself, not only through `archive_path`.
- **Scenario (`scenario/run_scenario.py`, the external-surface world, around line 8070).** The
  `other` project's `project.md` drops its `Archive in the PR` line, so that project now proves
  the default in `take`. The check at around line 8433 ("a project set to keep its archive out of
  the PR says so in the facts") gets a new label, for instance "a project that does not ask for
  its archive in the PR gets `archive: not in the PR` in the facts", and also asserts that the CR
  Driver prompt's `writes:` line holds only the CR folder, with no second path. The `other` CR
  runs no `ship` in the scenario: its `ship` off case is proved by the unit test above. The `demo`
  project keeps `yes`. Its existing checks (`archive: in the PR at`, `ship` saying `archive missing
  from the PR at`, then nothing once the archive is committed, `delivery.md` saying `Archive in
  the PR: yes, at ...`) prove that the `yes` cell still works end to end.
- **Matrix (a shipped default against a configured value), one line per cell:**
  - External, no line (the shipped default): `archive: not in the PR`, no archive in `writes:`, no
    `archive missing` from `ship`. Proved by the new unit test (`archive_path` is `None`), the
    parametrized external unit test (`take` and one `ship` call) and the scenario's `other`
    project (`take`).
  - External, `no`: same as above. Proved by the new unit test, through `archive_path`, which is
    the one value `take` and `ship` read.
  - External, `yes`: `archive: in the PR at <path>`, the path in `writes:`, `ship` reports a
    missing archive. Proved by the new unit test, the parametrized external unit test and the
    scenario's `demo` project.
  - In-project: unchanged, `archive_path` is `None`. Covered by the existing in-project tests,
    whose facts print no `archive:` line.

  The host (Claude Code or Copilot) does not change the result: the scenario's `other` take runs
  under Copilot, the `demo` take under Claude.
- **Change record.** The PR's commit holding the `Repo._external` change has the `Default change:`
  paragraph in its body, and the PR description's summary has it too (decision 6); the reviewer
  checks both.
- **Gates.** `just check` and `just eval-dry-run` in the worktree, because the change is under the
  CLI's `src/`. `just scenario` must be green on the pipeline's `just scenario (ubuntu-latest)` job
  at the PR's head before the PR, since the CR changes the CLI, the cards and the scenario.
  `just test` stays within its time budget: one small parametrized test and one more case of an
  existing test are added.
