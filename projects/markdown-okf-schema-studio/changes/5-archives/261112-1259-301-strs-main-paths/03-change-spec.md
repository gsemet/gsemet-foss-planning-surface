# Change Specification: every use case (StRS) states its main paths

Sources: `01-intent.md`, `02-answers.md` (2026-11-12), the reference files
`../302-requirements-viewer/main-paths/FORMAT.md` and
`../302-requirements-viewer/main-paths/StRS-MDOKFSTUDIO-DIAG-001.md`, and the code at `origin/main`
(`0e79699d`). The project rules apply as they stand: `.agents/constitution.md`, `AGENTS.md`,
`requirements/guidelines/requirements.guidelines.md` and `requirements/guidelines/project.guidelines.md`.

## Goal

A StRS describes a whole use case (A, then B, then C gives D). Testing every way through it end to
end is too combinatorial; its SwRS are the options at each state, each tested on its own. Each StRS
gets a `### Main paths` section that names one or two paths through the use case, step by step.
Each step is backed by the SwRS that moves the user from one state to the next, with the SwRS of the
other outcomes at that state. The owner wants these paths drafted from the StRS and its SwRS
wherever possible, ideally on every StRS ("il faudra faire créer intelligemment les main path la ou
c'est possible idéalement sur tous les StRS").

This change comes first. The second change, the requirements viewer
(`.agents/changes/3-requests/batch-01/302-requirements-viewer`), draws these sections as a metro map and parses
them, so the format below must be followed exactly. Priority P1, in the same batch as
`gallery-page-social-card` and `requirements-viewer`.

## Decisions carried from the grill

| Decision | Source |
| --- | --- |
| The Main paths are a change of their own, before the viewer ("Ok pour 2 CR"). | 02-answers |
| Main paths are drafted for every active StRS where possible, from the StRS and its SwRS. | intent, 02-answers |
| A step cites only an existing SwRS of that StRS; no behaviour is invented. | intent |
| A StRS whose SwRS do not form a path gets no section; it is listed in the report with the reason. | intent |
| The check is a project script run by `just requirements-lint` and so by CI; okfreq is not changed. | 02-answers |
| The check verifies that every cited SwRS exists, is active and derives from that StRS. | intent, 02-answers |
| The format is `FORMAT.md` of the viewer CR, documented in `requirements/guidelines/project.guidelines.md`. | intent |
| `just requirements-update` runs and `requirements/tiers/log.md` gets a dated entry. | intent |
| One pull request, one area (scope) per commit. The grill did not ask for one PR per area. | intent |
| The owner agrees that this change adds Main paths to all 16 `approved` StRS ("Yes, all 16"); `approved_by` and `approved_at` are stamped again and the owner reviews the PR. | 02-answers, 2026-11-12 |
| A path may cite a `draft` SwRS ("Yes, draft allowed"): active means `draft`, `proposed` or `approved`. | 02-answers, 2026-11-12 |
| The check script gets no SwRS of its own ("No SwRS"). | 02-answers, 2026-11-12 |

## What changes

### 1. The format, documented in the project guideline

File: `requirements/guidelines/project.guidelines.md`. Add a section `## Main paths of a StRS` (after
"Log headings", before "During a change"). It states the format of `FORMAT.md` as a project rule,
with no reference to the viewer CR or to any process document (constitution, section 8):

````markdown
### Main paths

#### Path 1: <short name of the path>

1. <state, in the reader's words>
   - SwRS-<ID>: <what moves the reader to the next state>
   - Option SwRS-<ID> (<nominal|boundary|refusal>): <another thing that can happen here>
2. <next state>
   ...
3. <final state: the result the user wanted>

#### Path 2: <name>

1. <a state already named in path 1, same words: the paths join there>
   - SwRS-<ID>: ...
2. <final state>
````

Rules to copy into the guideline:

- A state is the same state in every path when its text is the same.
- The first bullet without `Option` is the step to the next state; it is drawn on the path.
- `Option` bullets are drawn as branches; the scenario kind in brackets, when given, picks the
  scenarios of the SwRS that this option covers.
- A SwRS that derives from the StRS and appears in no path is listed under the map as "also serves
  this need" (by the reader of the section; it is not written in the StRS).
- The last state of a path has no bullet.

Rules that follow from the intent and also go in the guideline:

- One or two paths per StRS.
- Every cited SwRS exists, is active (`req_lifecycle` is `draft`, `proposed` or `approved`, not
  `deprecated` nor `superseded`; a `draft` SwRS may be cited) and has that StRS in its `derives_from`. Paths
  state what the extension does today, like the rest of the requirement; a step never describes
  behaviour that no cited SwRS specifies.
- The section is authored text: it sits after the last authored section of the StRS (usually
  `### Rationale and constraints`) and before the generated `<!-- okf:links:start -->` block.
- A StRS whose SwRS do not form a path has no section.
- `just requirements-lint` checks the cited SwRS (section 3 below).

The okfreq skill (`.agents/skills/okfreq/SKILL.md`, "Author and implement requirements") describes
the content of an StRS only generically (normative behavior, user need, rationale). It is the
shared, packaged okfreq text, like `requirements.guidelines.md`, which takes no project rule. It is
not changed: the project guideline carries the rule.

### 2. Main paths in the StRS files

Files: `requirements/tiers/strs/<scope>/StRS-MDOKFSTUDIO-*.md`, the active ones only. On
`origin/main` there are 80 active StRS in 16 scopes: 62 `proposed`, 16 `approved`, 2 `draft`
(StRS-MDOKFSTUDIO-TOOLBAR-002 and -003). The 53 `deprecated` or `superseded` StRS are not touched.

For each active StRS, the author:

1. Reads the StRS (normative behavior, preserved intent, rationale and constraints) and every active
   SwRS whose `derives_from` holds its ID (the generated `derived_by` list, cross-scope ones
   included, for example SwRS-MDOKFSTUDIO-REVIEW-017 under StRS-MDOKFSTUDIO-DIAG-001).
2. Draws one or two paths from the user's starting state to the result the user wanted. Each state
   is in the reader's words; each step and each option cites one of those SwRS, and its text says
   only what that SwRS's normative behavior or scenarios say. The scenario kind in brackets matches
   a scenario the SwRS has.
3. Writes the section in the format above, at the place given in section 1. It changes nothing else
   in the file: no frontmatter, no other section, never the Links block.
4. When the SwRS do not form a path (for example a gap: a state with no SwRS to leave it, or SwRS
   that are only unrelated constraints), writes no section and notes the StRS and the reason for
   the report (section 5).

Sample: `.agents/changes/3-requests/batch-01/302-requirements-viewer/main-paths/StRS-MDOKFSTUDIO-DIAG-001.md`
(in the main checkout; the folder is git-ignored) is the starting point for StRS-MDOKFSTUDIO-DIAG-001;
each of its steps is checked against the cited SwRS like any other before it is kept.

Approved StRS: 16 of the 80 are `approved` (BLOCK-003, BLOCK-025, CORE-001, DIAG-001, DIAG-006,
GFM-002, LAYOUT-001, LAYOUT-003, MYST-001, PALETTE-015, REVIEW-001, REVIEW-003, REVIEW-012,
REVIEW-015, TABLE-001, TABLE-012; owner gaetan@xeberon.net). The project guideline ("Approved
requirements") requires the owner's explicit agreement, recorded in this specification, before an
approved requirement is changed. That agreement is recorded: on 2026-11-12 the owner answered "Yes,
all 16" (02-answers.md), so this change adds Main paths to all 16. On each of them the Driver sets
`approved_by` to `gaetan@xeberon.net` and `approved_at` to the current date and time with its UTC
offset (ISO 8601, for example `2026-11-12T10:00:00+01:00`), then runs `just requirements-update`
(which regenerates `verified`). The PR body lists them under "Approved requirements changed", and
the Driver requests the owner's review on the PR.

### 3. The check: `scripts/check_main_paths.py`

A new Python script, run with the project's environment:

```sh
uv run --no-sync --group requirements python scripts/check_main_paths.py requirements
```

Behaviour:

- Argument: the bundle root (`requirements`). It reads `config.yml` for the tier folders and
  prefixes (`tiers.StRS.folder`, `tiers.SwRS.folder`, the `SwRS-MDOKFSTUDIO` prefix) instead of
  hard-coding them, and parses frontmatter with `ruamel.yaml` (already in the `requirements` group
  through `okf-schema`; no new dependency).
- It indexes every SwRS file under `tiers/swrs/` by `id`, with its `req_lifecycle` and
  `derives_from`.
- In every StRS file under `tiers/strs/`, it finds the `### Main paths` section (from that heading
  to the next `### ` heading or `<!-- okf:links:start -->`) and every SwRS ID in it.
- For each cited ID it reports, with the file path and line number:
  - `<path>:<line>: <ID> does not exist`
  - `<path>:<line>: <ID> is <lifecycle>, not active`
  - `<path>:<line>: <ID> does not derive from <StRS-ID>`
- Exit 0 with a one-line summary (`main paths: <n> StRS checked, <m> SwRS citations, all valid`)
  when nothing is wrong; exit 1 after listing every problem otherwise.
- Works on Linux, macOS and Windows (`ci-static` runs on Windows): `pathlib`, UTF-8 reads,
  CRLF line endings accepted, forward-slash paths in messages.

Wiring, in `justfile`:

- `requirements-lint` gains, after its three okfreq lines:
  `uv run --no-sync --group requirements python scripts/check_main_paths.py requirements`.
  `just check` already depends on `requirements-lint`, and `just ci-static` runs `just check` on
  Linux and Windows in `.github/workflows/ci.yml`, so CI runs the check with no workflow change.
- `release-tests` gains `test/build/test_check_main_paths.py` in its pytest list.

Test: `test/build/test_check_main_paths.py` (pytest, loading the script with
`importlib.util.spec_from_file_location` like `test/build/test_select_e2e_run.py`). It builds a
small bundle in `tmp_path` (a `config.yml`, two StRS, a few SwRS) and asserts:

- a valid section passes (exit 0);
- an unknown SwRS ID fails with "does not exist";
- a `superseded` and a `deprecated` SwRS fail with "not active";
- a SwRS that derives from another StRS fails with "does not derive from";
- an `Option` bullet is checked like a step bullet;
- a StRS without the section, and an ID cited outside the section, are ignored;
- every problem is listed, not only the first;
- a CRLF file is read the same way.

The script and its test are build tooling, not a behaviour of `src/`. The owner decided on
2026-11-12 that the check gets no SwRS of its own ("No SwRS"), so neither file carries
`@implements_req` / `@tests_req` markers.

### 4. Generated files and log

- `just requirements-update` after the edits; its generated changes (indexes) are committed with the
  area they belong to. No generated field, index block or Links block is hand-edited.
- `requirements/tiers/log.md`: one entry under the date heading `## YYYY-MM-DD` of the day of the
  change (newest first, appended to the existing heading of that date if any), with a
  `### Main paths in the StRS` sub-heading. It lists the StRS that got a section, the StRS without
  one with the reason for each, the 16 approved StRS changed with the owner's agreement of
  2026-11-12, the new check, and the verification results actually run.

### 5. The report of StRS without a section

The list of active StRS left without a Main paths section, each with its reason, goes in the
`log.md` entry (section 4) and in the PR body. Nothing is written in those StRS files.

### 6. Delivery shape

One pull request. Commits, following `.agents/guidelines/git-commit-message.guidelines.md` (no scope
on `build` or `docs`):

1. `build: check the SwRS cited by the Main paths of a StRS` with the guideline section, the script,
   its test and the `justfile` lines.
2. One commit per scope, `docs: write the main paths of the <scope> use cases`, holding that scope's
   StRS edits (approved ones included, with their new approval stamps) and their regenerated
   indexes.
3. The `log.md` entry, in the last commit or its own `docs:` commit.

The check is in the first commit, so every later commit passes `just requirements-lint` on its own.

## Out of scope

- The requirements viewer and its metro map (`302-requirements-viewer`), and any parsing of the
  `Option` kind or the "also serves this need" list.
- okfreq itself, its schemas and the shared guideline and skill texts it owns.
- Any change to a requirement's frontmatter (other than the approval stamps of the 16 approved StRS),
  normative statement, scenarios, criteria or Links; any new, retired or superseded requirement.
- Deprecated and superseded StRS.
- Any change to `src/`, to tests other than the new check's test, and to the site Requirements page
  (`test/site/requirementsPage.ts` text about `requirements-lint` stays as is).
- Checking the wording of states, the kind in brackets or the shape of the list; the check verifies
  the cited SwRS only, as decided.

## Evidence

Checks (all must pass):

- `just requirements-lint`, which now runs `scripts/check_main_paths.py`.
- `just release-tests`, which now runs `test/build/test_check_main_paths.py`.
- `just requirements-update` leaves no diff after the last commit.
- `just preflight` (completion gate, constitution section 4).
- Before opening the PR, `okfreq validate --check-links --project-root .` and coverage as CI runs
  them (project guideline, "Requirements traceability").

Scenario steps (for the reviewer, on the PR branch):

1. Run `uv run --no-sync --group requirements python scripts/check_main_paths.py requirements`: exit
   0, the summary counts the StRS with a section.
2. In `requirements/tiers/strs/diagrams/StRS-MDOKFSTUDIO-DIAG-001.md` (or another StRS with a
   section), change one cited ID to an unused number such as `SwRS-MDOKFSTUDIO-DIAG-999`: the
   script exits 1 with "does not exist" and the line number.
3. Change it to a superseded SwRS of `tiers/swrs/diagrams/`: "not active".
4. Change it to an active SwRS of another StRS: "does not derive from" that StRS.
5. Revert. Count the StRS: those with a section plus those listed in the log entry without one
   equal the 80 active StRS.
6. On an approved StRS with a section, `approved_by` is `gaetan@xeberon.net`, `approved_at` is the
   date of the change and `verified.at` matches it.
7. Open three StRS of different scopes and read each path against its cited SwRS: every step and
   option says what the SwRS specifies, nothing more.
