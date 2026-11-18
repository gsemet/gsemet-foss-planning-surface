# Change Specification: chantier validate checks a whole planning folder

## Goal

A planning surface (or a project's own `.agents/changes/`) is checked by chantier itself: one
read-only command, `chantier validate`, tells whether the planning folder follows chantier's
layout and stays readable by the board, with one exit code for gaps (to fix, nothing breaks) and
another for errors (chantier or the board misreads the folder). A surface's `just validate` then
calls it and keeps no validation of its own.

Today's code read at `main` `3a9afc2c` (2026-11-18). The layout checked is the one the cards
already give (`skills/chantier/references/concepts.md`, "Change Request", "A CR's summary",
"Planning folder", "Lifecycle"; `docs/planning-folder.md`): the command adds no rule.

## The command

```text
chantier [--project <the project's folder>] validate
```

- Declared in a new `src/chantier/declare/validate.py` (`add_command(sub, "validate", ...,
  NO_BATCH)`; `--project` accepted after the command too, as `add_command` does), registered in
  `cli.py`'s module tuple. No positional argument: it checks the whole planning folder.
- `validate` joins `FULL_OUTPUT` in `cli.py`: every line is printed, never cut at ten.
- The handler, in a new `src/chantier/commands/validate.py`, finds the planning folder with
  `Repo.find(readonly=True)` and writes nothing at all (no `.gitignore`, no lock file, no STATUS,
  no summary); it takes no lifecycle lock.
- **It could not run → exit 1**, `error: <cause>` on stderr, nothing on stdout: a `ChantierError`
  raised while finding the planning folder (outside a git repository, an unknown `--project`, a
  surface with several projects and no `--project`, whose `SurfaceChoice` exits 2 elsewhere) is
  raised again with `EXIT_USAGE` and its message kept; a planning folder that does not exist
  gives `error: no planning folder at <path>`. So a caller never takes a refusal for a gap.
- Paths: relative to the planning folder, forward slashes (`repo.rel`), the form `summary set`
  reads.

### Output and exit codes

```text
no error, no gap (<k> CRs)                       exit 0
<m> gap(s) in <k> CRs                            exit 2 (EXIT_PRECONDITION), gaps only
<n> error(s), <m> gap(s) in <k> CRs              exit 3 (EXIT_CONFLICT), at least one error
error <path>: <what is wrong>[ → <what closes it>]
gap <path>: <what is wrong>[ → <what closes it>]
```

`<k>` counts the CR folders found in every stage. The errors come first, then the gaps, each group
sorted by path; one line per finding.

## What it checks

"Live stages": `1-inbox`, `2-backlog/P1`..`P4`, `3-ready`, `4-batch/1-pending`, `2-actives`,
`3-done` (what `cr_folders(paths)` returns). "All stages": the live ones plus `5-archives` and
`6-trash`. Entries whose name starts with a dot are skipped everywhere (`.gitkeep`, locks,
`.long-gate.queue`). A missing stage folder is not reported.

A **CR folder** is a folder directly in a stage folder (as `lifecycle/stages.py` reads it);
`5-archives/batches/` is the batches' records, no CR. Elsewhere, a folder is **CR-like** when it
holds one of `intake/`, `01-intent.md`, `02-answers.md`, `03-change-spec.md`, `summary.json`.

### 1. Placement (all stages), errors

| Finding | Line |
|---|---|
| A folder directly in `2-backlog/` that is not `P1`..`P4` | `error 2-backlog/<x>: in 2-backlog without a P1..P4 folder → move it into 2-backlog/P<n>/` (`triage` reads no such folder) when `<x>` is CR-like, else `error 2-backlog/<x>: not a priority folder (P1..P4)` |
| A folder directly in `4-batch/` that is not `1-pending`, `2-actives`, `3-done` | `error 4-batch/<x>: not a batch state folder (1-pending, 2-actives, 3-done)` |
| A folder directly in the planning folder that is not a stage (`1-inbox`, `2-backlog`, `3-ready`, `4-batch`, `5-archives`, `6-trash`) and is CR-like or holds a CR-like folder | `error <x>: a CR outside a stage folder` |
| A CR folder named `P1`..`P4` outside `2-backlog/` (in any other stage) that holds a CR-like folder | `error <stage>/P<n>: a priority folder outside 2-backlog` (its children are then not reported again as nested) |
| A CR-like folder anywhere under a CR folder (any depth) | `error <path>: a CR inside the CR <cr path>` |

Today's surface holds none of these (read on 2026-11-18, every project).

### 2. `summary.json` format (all stages), errors

Read as the board reads it: `summaries.store.read` (the `CrSummary` model; it raises
`UnreadableSummary`). Then, on a readable file, the limits `summary set` enforces, each through
the existing helper so the rule stays in one place: `title` (when not empty) through
`summaries.edit.one_line(..., "title", TITLE_MAX)`, `summary` with `SUMMARY_MAX`, `group` with
`GROUP_MAX`, `labels` each matching `LABEL_PATTERN` (`core.records`), and `schema` equal to
`SUMMARY_SCHEMA`.

| Finding | Line |
|---|---|
| Unreadable (not JSON, or not the model) | `error <cr>/summary.json: unreadable (<why>) → repair or remove it, then summary set <cr> …` (the `why` of `UnreadableSummary`) |
| A field outside `summary set`'s limits | `error <cr>/summary.json: <the helper's message> → summary set <cr> --title/--summary … ` (labels: `→ summary label <cr> --remove <label>`; group: `→ summary group <cr> --name/--clear`) |
| `schema` other than 1 | `error <cr>/summary.json: schema <n>, this chantier reads 1` |

An empty or absent `title` or `summary` is not an error: it is the "no summary" gap of §3.

### 3. Missing or late summary (live stages), gaps

Exactly `summary lint`'s gaps over `cr_folders(paths)` (`summaries.gaps.gap_of`, a folder with no
covered file skipped), with the very line `summary lint` prints, prefixed `gap `: `_gap_line` of
`commands/summary.py` moves to `summaries/gaps.py` as a public `gap_line(repo, gap)` that both
commands call. The `unreadable` kind is not repeated here: §2 reports it as an error.

### 4. CR folder shape (live stages), gaps

| Finding | Line |
|---|---|
| A file (not a folder) directly in a stage folder | `gap <stage>/<file>: a file in a stage folder, not a CR → move it into a CR folder or out of the planning folder` |
| A CR folder with no request: none of `intake/*.md`, `01-intent.md`, `03-change-spec.md` | `gap <cr>: no request (no intake/*.md, 01-intent.md or 03-change-spec.md) → write its request or move the folder out` |
| An entry at a CR folder's top level outside the CR's tree | `gap <cr>/<name>: not in a CR folder's layout (concepts.md, "Change Request")` |
| A known entry of the wrong kind (`intake`, `evidence`, `work`, `prototypes`, `experiments` that is a file; `01-intent.md`, `02-answers.md`, `03-change-spec.md`, `summary.json`, `delivery.md`, `depends.json`, `STATUS.md`, `STATUS.json` that is a folder) | `error <cr>/<name>: a file where chantier reads a folder` or `... a folder where chantier reads a file` (an error: `open`, `summary` and the board read it by kind) |

The CR's tree: `intake/`, `01-intent.md`, `02-answers.md`, `03-change-spec.md`, `summary.json`,
`STATUS.md`, `STATUS.json`, `prototypes/`, `experiments/`, `evidence/`, `work/` (concepts.md's
tree), plus `delivery.md` (an archive), `depends.json` (a dependency) and `report.md`,
`conversation.md` (a release CR's sources, `release-template.md`). The set is one constant in
the new module, with a comment naming those places.

### 5. Broken links between Markdown files (live stages and the planning folder's top level), gaps

- Files read: every `*.md` under the planning folder except under `5-archives/` and `6-trash/`,
  in a folder whose name starts with a dot, or named `STATUS.md` (the CLI rewrites it). Read as
  UTF-8, a byte-order mark dropped, undecodable bytes replaced (never a failure).
- Links read: inline `[text](target)` (not images: `![...]`) and reference definitions
  `[id]: target`, outside fenced code blocks and code spans. The target: `<...>` and a quoted
  title stripped, the anchor (`#...`) and query dropped, percent-escapes decoded.
- Checked only when the target is relative (no scheme such as `https:` or `mailto:`, not
  starting with `/` or a drive), ends in `.md` (any case), and, resolved from the folder of the
  file that holds it, lies inside the planning folder. Reported when it does not exist:
  `gap <file>: link to <target as written> does not resolve`, one line per link (a target
  repeated in one file: one line).

Measured with this reading on 2026-11-18: the `chantier` project has none; the
`markdown-okf-schema-studio` project has 11 (CRs moved from the project's `.agents/changes/`:
`../../../../AGENTS.md` and the like), `agentic-planning-surface` 6 (under a CR's `work/`).

## Code

- `src/chantier/declare/validate.py`: the parser (help: "check the whole planning folder: stages,
  CR folders, summary.json's format, missing or late summaries, broken links; exit 2 gaps, 3
  errors"). Start-up stays standard library only (`test_code_targets.py`): the handler is
  `lazy("chantier.commands.validate:validate")`.
- `src/chantier/commands/validate.py`: the handler, the counts line, the order, the exit code.
- `src/chantier/lifecycle/layout_check.py` (new): placement (§1) and shape (§4), returning
  findings (a small frozen dataclass: severity `error`/`gap`, path, text), reusing
  `stage_layout`, `PRIORITIES`, `STATE_FOLDERS`.
- `src/chantier/lifecycle/links.py` (new): §5.
- `src/chantier/summaries/format.py` (new): §2, on one folder.
- `src/chantier/summaries/gaps.py`: gains `gap_line` (moved from `commands/summary.py`, which
  imports it); the `summary lint` output does not change by one character.
- `src/chantier/cli.py`: the module tuple and `FULL_OUTPUT`.
- Every file within the code targets (400 lines, functions of 50, `mypy --strict`, ruff), the
  layers kept (`core` → `lifecycle`/`summaries` → `commands` → `cli`).

## Docs and cards

- `skills/chantier/references/concepts.md`, "Planning folder": one sentence: `$CHANTIER validate`
  checks the whole planning folder (stages, CR folders, `summary.json`'s format, missing or late
  summaries, broken links between its Markdown files), writes nothing, exits 2 on gaps and 3 on
  errors; a surface's own validation calls it; it blocks no other command. No role's card
  changes: no agent is told to run it.
- `docs/planning-folder.md`: a short paragraph after the summary paragraph, with the command, what
  it checks (the five areas, which stages each covers), the output and the exit codes, and that
  a surface's `just validate` calls it.
- `scenario/README.md`, "Coverage": one bullet naming the unit and the test below.

## Evidence

- **Tests** (`skills/chantier/scripts/cli/tests/test_validate.py`, new; in-process through the
  `chantier` fixture; few, parametrized, fast):
  - one test parametrized over the `repo` and `surface` cells: a planning folder made by the
    CLI's own commands (`init` where it applies, `file`, `summary set`, `triage --priority`)
    validates with exit 0 and `no error, no gap (<k> CRs)`; the tree's files and their bytes are
    the same after the run, and no `.gitignore` or lock appeared that was not there;
  - one test parametrized over the findings, each a broken input built in a temporary planning
    folder (the cases the CLI's commands cannot produce): a CR-like folder in `2-backlog/`
    without a priority, a non-state folder in `4-batch/`, a CR-like folder at the top level, a
    `P2/` in `3-ready/` holding a CR, a CR inside a CR's `work/`, an unreadable `summary.json`, a
    title of 121 characters, a bad label, `schema: 2`, a file where a folder is read: exit 3 and
    the expected `error` line; a missing summary, a late summary (same line as `summary lint`
    prints, read from `summary lint` in the same test), a file in `1-inbox/`, a CR with only
    `work/`, an unknown top-level entry, a broken `../../P1/x/01-intent.md` link (and, in the same
    file, a code span, a fenced block, an `https:` link, an image and a link leaving the planning
    folder, none reported): exit 2 and the expected `gap` line; one error and one gap together:
    exit 3, the error line before the gap line;
  - the same broken summary and link put in `5-archives/<x>/` give no §3, §4 or §5 line, and
    the unreadable `summary.json` there still gives its §2 error;
  - refusals: a surface with two projects and no `--project`, and an in-project repository with
    no planning folder: exit 1, `error:` on stderr, stdout empty;
  - eleven findings: all printed (no `… N more lines`).
  `just test` stays within its budget (30 s above its 18.5 s on the user's Windows machine).
- **Scenario** (`scenario/run_scenario.py`):
  - unit `cr_summary`, after `summary_walk` (eleven filed items with no summary): `validate`
    exits 2, its first line `<m> gap(s) in <k> CRs`, every gap printed (more than ten lines),
    each `no summary` line equal to `gap ` + the matching `summary lint` line;
  - unit `external_surface`, after the batch's `close` (archives with `delivery.md`,
    `5-archives/batches/`): `chantier --project <the project's folder> validate` reports no
    `error` line (exit 0 or 2), so a closed batch's own output never reads as an error.
- **Gates**: `just check`, `just eval-dry-run` (a change under the CLI's `src/`) at the rebased
  head before the first push; `just scenario (ubuntu-latest)` green at the PR's head.
- **A real run** (read-only, in the PR's Deliverables): from the planning surface,
  `uv run --no-sync --project <the worktree> chantier --project projects/<name> validate` for
  each of its projects, the first line and exit code of each quoted. Expected on 2026-11-18's
  state: no `error` line anywhere; `chantier` gaps for its missing or late summaries only.
- No host and default matrix: the command reads no host and no configuration.

## Out of scope

- The surface's side: once a chantier release ships `validate`, the surface's
  `scripts/validate-bundles.py` pins that release and calls `chantier --project <p> validate`
  in place of its placement check and its `summary lint` call (0 and 2 pass, the gap lines
  shown; 3 fails; any other code: chantier could not run), and its `AGENTS.md` "Validation"
  section says so. That is a change in the surface's repository, made after the release, not in
  this PR.
- A check of one CR folder only (`validate <folder>`), of every project of a surface in one run,
  of `depends.json`'s content, of archive folder names, of anchors inside a linked file, of links
  to non-Markdown files, or of UTF-8 and byte-order marks.
- Any fix: `validate` reports, never repairs or moves.
- The `v0.9.0` tag that `uvx --from git+...@v0.9.0` cannot run: a published tag is not rewritten.

## Open questions (for the Chief of Staff, to the user)

1. **Which findings fail the surface's `just validate`?** The specification makes errors (exit 3)
   only what chantier or the board misreads: a CR out of place or nested, `summary.json`
   unreadable, beyond `summary set`'s limits or of another schema, a file where a folder is read
   (or the reverse). Everything else is a gap (exit 2, the surface passes and shows it): a
   missing or late summary, a file in a stage folder, a CR with no request, an entry outside the
   CR's tree, a broken link. Should broken links, or a CR with no request, fail instead?
2. **The archives and the trash.** The specification checks placement and `summary.json`'s
   format in every stage, but the missing or late summaries, the CR folder's shape and the links
   only outside `5-archives/` and `6-trash/` (as `summary lint` does today): a closed CR is
   history, and checking its links would report hundreds of old ones in one project (the
   Markdown OKF-Schema Studio's archives) and a dozen loose run briefs. Should the archives be
   checked in full instead?
