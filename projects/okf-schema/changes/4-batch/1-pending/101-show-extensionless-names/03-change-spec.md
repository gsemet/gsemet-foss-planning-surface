# show: resolve concept names without .md, stay inside the bundle

issue: https://github.com/gsemet/okf-schema/issues/56

## Goal

`okf-schema show --path <bundle> api/health-check` prints the concept, as the Getting Started
and knowledge-graph tutorials say. `show` takes a concept name with or without `.md`. A name
starts from the bundle root, with or without a leading `/` (OKF 0.2 section 6.1), from any
terminal folder: `/api/health-check` and `api/health-check` name the same concept. It opens
only files inside the bundle, symlinks included. A directory or a path that leaves the bundle
gets a plain error and exit code 2, never a traceback. The Python API `show_bundle` follows the
same rules.

Code base: `origin/main` at 2f09cef (0.18.1). The line numbers below are from that commit.

## Current behavior (checked)

- `src/okf_schema/api.py:376` `show_bundle(bundle_path, concept_path)` builds
  `target = bundle / concept_path`, checks only `target.exists()` and reads it. Problems:
  - `api/health-check` gives `FileNotFoundError("Concept not found: ...")`;
  - a directory passes `exists()`, so `read_text` fails with `PermissionError` on Windows and
    `IsADirectoryError` on POSIX. The CLI does not catch these, so a traceback is printed;
  - `../x.md` and an absolute path outside the bundle are read;
  - a symlink inside the bundle that points outside it is followed and read.
- `src/okf_schema/cli.py:732` `show` catches `(FileNotFoundError, NotADirectoryError)`, prints
  `Error: <message>` to stderr and exits 2. The `except` line carries `# pragma: no cover`.
- `backlinks_bundle` (`api.py:841`) already accepts targets without `.md`. It does not change in
  this CR.

## What changes

### 1. Runtime: `show_bundle` (`src/okf_schema/api.py`)

Resolve the concept in this order. Each step carries one decision of `02-answers.md`:

1. `bundle = _resolve_bundle(bundle_path)` (no change; it is already `resolve()`d).
2. Read the name into `raw`, the first rule that applies (Q6, Q14, Q15):
   a. Disk path inside the bundle (Q6): when `Path(concept_path).is_absolute()` and its lexical
      form `Path(os.path.normpath(concept_path))` (no link followed) `is_relative_to(bundle)`,
      `raw = bundle / concept_path` (pathlib: the absolute path replaces `bundle`). The test is
      lexical on purpose: an absolute path to a symlink inside the bundle whose target is
      outside still reaches step 4 and gets the outside refusal (Q5).
   b. Name from the bundle root (Q14, Q15): otherwise, when `concept_path` starts with `/`,
      strip every leading `/` and `raw = bundle / <the rest>`, as a `/` link is read in OKF 0.2.
      On POSIX this also covers an absolute disk path outside the bundle: `/etc/passwd` becomes
      `<bundle>/etc/passwd`, is searched in the bundle and is not found. On Windows `/api/status`
      has no drive, is never a disk path, and is always read this way.
   c. Otherwise `raw = bundle / concept_path`: a relative name starts from the bundle root,
      never from the current working directory (Q15; today's behavior, kept). A Windows drive
      path outside the bundle (`C:\other\x.md`) replaces `bundle` here and is refused at step 4.
   `os` is already imported by `api.py`.
3. Candidates, in order (Q2):
   a. `raw`, when `raw.is_file()` (links followed). A directory is never a concept;
   b. otherwise `<raw>.md`: the string of `raw` plus `.md`, so `api` becomes `api.md` even when
      `api/` exists. This follows the answer literally: `.md` is added whenever the exact path
      is not a file.
   The target is the first candidate that is a file.
4. Containment (Q4, Q5), always on the **real** path (`Path.resolve()`, links followed). A path
   counts as inside when `real.is_relative_to(bundle)` and `real != bundle`. `is_relative_to`
   exists from Python 3.9, and the project needs 3.10.
   - When a target was found and its real path is outside the bundle, raise
     `FileNotFoundError(f"Concept path is outside the bundle: {concept_path} (bundle: {bundle})")`.
     The file is never opened. This holds for `../x.md`, a Windows drive path elsewhere, a symlinked
     file whose target is outside, and a file under a symlinked directory that points outside.
   - When no candidate is a file and the real path of `raw` is outside the bundle, raise the
     same "outside the bundle" `FileNotFoundError` (Q4: a path that leaves the bundle is an
     error, whether or not something exists there).
   - When no candidate is a file and `raw` is inside the bundle or is the bundle root (`.`,
     `""`, `/`, `sub/..`), raise `FileNotFoundError(f"Concept not found: {raw}")`. This keeps today's
     message. The bundle root and any other directory with no matching `.md` end here (Q3).
   - Bundle root with a file beside it: for `.`, `""` or `/`, `raw` is the bundle itself, so the
     `<raw>.md` candidate is `<parent>/<bundle>.md`, a file beside the bundle. When that file
     exists, it is the target found in step 3, its real path is outside, and the first bullet
     applies: the "outside the bundle" error, not "Concept not found". The steps stay in this
     order, with no special case for the root. Both outcomes exit 2 and read nothing.
5. Read the target and build the `ConceptDetail` as today. A `..` path whose real path stays
   inside the bundle (for example `sub/../concept-a.md`) works as before (Q4: nothing changes for
   paths inside).

Q7: the API raises `FileNotFoundError` in every refusal (not found, directory, outside, symlink
leaving), each with an explicit message. No new exception type is added. `NotADirectoryError`
for a bundle path that is a file does not change.

Update the `show_bundle` docstring (Google style, per
`.github/guidelines/python-module-documentation.guidelines.md`):
- `concept_path`: a name from the bundle root, with or without a leading `/`, or an absolute
  disk path inside the bundle, with or without `.md`;
- the reading of the name (step 2) and the resolution order;
- `Raises: FileNotFoundError` for a missing concept, a directory, or a path or symlink whose
  real path is outside the bundle; `NotADirectoryError` as today.
`docs/source/reference/api.md:137` renders this docstring through `autofunction`.

Put the containment check of step 4 in one private helper of `api.py` (for example
`_require_inside_bundle(bundle, real, concept_path)`, which raises the "outside the bundle"
`FileNotFoundError`), so that the follow-up CR `bundle-outside-symlinks` can reuse it. That
helper carries `# @implements_req SwRS-OKFSCHEMA-CORE-010` (the new requirement of section 3a;
use the ID `okfreq new` prints if it differs).

Keep the `# @implements_req SwRS-OKFSCHEMA-CORE-006` marker on `show_bundle`, because it still
derives the trust tier and staleness. Add `# @implements_req SwRS-OKFSCHEMA-CORE-005` next to
it, since this CR changes the inspection contract of CORE-005 (names without `.md`, a
directory reported as not found).

### 2. Runtime: `show` command (`src/okf_schema/cli.py`)

- No new option. The existing `except (FileNotFoundError, NotADirectoryError)` already prints
  `Error: <message>` and exits 2. Now that the new tests cover that line, remove its
  `# pragma: no cover`.
- Docstring `Examples:` gains `okf-schema show --path bundle concepts/clock` next to the
  existing `.md` form. Add one sentence: the name starts from the bundle root (a leading `/` is
  allowed), the `.md` extension is optional, and a path outside the bundle is refused. Click shows this text in `okf-schema show --help`.

### 3. Requirements

Follow `src/okf_schema/data/requirements/guidelines/requirements.guidelines.md` and
`requirements/guidelines/project.guidelines.md`. Q11: the rule "stay inside the bundle" is a
requirement of its own, created now; CORE-005 cites it with `depends_on` and does not carry it
(the guideline: "A rule shared by many features ... is written once and cited by
`depends_on`"). The follow-up CR `bundle-outside-symlinks` adds the other commands to that new
requirement rather than writing the rule again.

#### 3a. New requirement "Stay inside the bundle"

Create it with `okfreq new`, never by hand (the guideline forbids hand-allocated IDs and UUIDs):

```console
okfreq new swrs "Stay inside the bundle" \
  --description "When a user shows a concept, okf-schema SHALL refuse, without reading it, a concept path whose real path, symbolic links followed, is outside the bundle." \
  --project okf-schema --scope core \
  --derives-from StRS-OKFSCHEMA-CORE-002 \
  --lifecycle proposed --path requirements
```

- Expected ID: `SwRS-OKFSCHEMA-CORE-010` (CORE-009 is the highest on `origin/main` and
  `requirements/config.yml` has no `retired_ids`). Use the ID the command prints everywhere
  this specification says CORE-010.
- `req_lifecycle: proposed`: it is delivered with its code. It gets no approval.
- Parent: `StRS-OKFSCHEMA-CORE-002` "Maintain and inspect OKF bundles", the parent of CORE-005.
- The statement covers `show` only, because only `show` behaves this way after this CR (a SwRS
  states what the code does). The follow-up CR widens it to the other commands.
- Complete the scaffold `okfreq new` writes. The frontmatter `description` and the normative
  paragraph stay the same single SHALL statement, word for word. Authored fields as the other
  core SwRS: `owner: okf-schema maintainers`, `verification_method: test`,
  `verification_criteria: Focused regression tests and the complete project preflight pass.`;
  plus `documentation_files: [docs/source/reference/cli.md]` and
  `agent_skill_files: [skills/okf-schema/SKILL.md]` (both change in this CR). Scenarios, in
  `scenarios:` and as `### Scenario S<n>: <title>` sections in the body:
  - `S1` "Refuse a concept path that leaves the bundle": GIVEN a concept path such as
    `../outside.md` or `../outside`, a Windows drive path outside the bundle, or `.` with a file
    `<bundle name>.md` beside the bundle, WHEN the user shows it, THEN okf-schema reports
    `Concept path is outside the bundle: <path> (bundle: <bundle>)`, exits 2 on the CLI,
    raises `FileNotFoundError` in the API, and reads nothing outside the bundle.
  - `S2` "Refuse a symbolic link that leaves the bundle": GIVEN a symlinked file inside the
    bundle whose target is outside it, or a file reached through a symlinked directory that
    points outside, WHEN the user shows it, THEN the same refusal as S1 applies and the target
    is not read.
  - `S3` "Keep paths that stay inside": GIVEN `sub/../concept-a.md`, an absolute disk path
    inside the bundle, or a symlink inside the bundle whose target is inside, WHEN the user shows it,
    THEN the concept is shown as before.
- A line in the body, outside the normative paragraph: "Known issue: `validate`, `list`,
  `index`, `backlinks` and `lint` still follow symbolic links whose target is outside the
  bundle." This is the guideline's form for a behavior that is wrong and not fixed yet. A
  requirement names no ticket, so the line does not name the follow-up CR.
- A line in the body (Q13, read with Q14): on a case-insensitive file system such as macOS, an
  absolute path whose bundle part is spelled in another case than `--path` is not recognized as
  a disk path inside the bundle; it is read from the bundle root and reported as not found.
- A line in the body (Q14): a concept path starting with `/` that is not a disk path inside the
  bundle is read from the bundle root, so on POSIX an absolute path outside the bundle is
  searched in the bundle and never read.
- `### Verification notes`: Method: public API and CLI tests of `show`. Criteria: a path,
  Windows drive path or symlink whose real path is outside the bundle is refused without being
  read; a POSIX absolute path outside the bundle is searched in the bundle and never read; a
  `..` path, an absolute disk path or a symlink whose real path stays inside works.

#### 3b. `requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-005.md`

Keep the `id`, `uuid`, title, existing scenarios S1/S2 and the authored metadata. The document
stays `req_lifecycle: proposed` and gets no approval.
- Add `depends_on: [SwRS-OKFSCHEMA-CORE-010]` (authored field). `okfreq lint` then writes the
  "Depends on" group of the generated Links section; never edit that section by hand.
- Add to `scenarios:` and to the body `S3` "Resolve a concept name without its extension":
  GIVEN a bundle with `api/health-check.md` (and possibly an `api/` directory beside an
  `api.md`), WHEN the user shows `api/health-check` or `api`, THEN the exact path is used when
  it is a file, else `<name>.md`, and a directory is never shown.
- Add `S4` "Read a name from the bundle root" (Q14, Q15): GIVEN a bundle with
  `api/health-check.md`, WHEN the user shows `/api/health-check` or `api/health-check`, from any
  current working directory, THEN both show the same concept, read from the bundle root; a
  leading `/` name with no such file in the bundle (for example `/etc/passwd`) is reported as
  not found and nothing outside the bundle is read.
- Extend S2's GIVEN to "a missing bundle, a missing concept path, or a directory".
- No scenario of CORE-005 states the outside-bundle refusal: that rule lives in CORE-010 only.
- Leave the frontmatter `description` and the normative paragraph unchanged: they are the
  same single SHALL statement word for word, as the requirements guideline asks.
- Add to `### Verification notes`, under Criteria: a concept path resolves with or without
  `.md`, from the bundle root with or without a leading `/`, a directory is never shown, and the
  paths `show` accepts are bounded by
  SwRS-OKFSCHEMA-CORE-010.

#### 3c. Generated fields, navigation and log

- Run `okfreq update-coverage requirements` (generated fields: `implemented_in_files`,
  `tested_in_files`, `derived_by` of StRS-OKFSCHEMA-CORE-002, `status`, ...) and
  `okfreq lint requirements --prose --check-links --project-root .` (Links sections and the
  navigation in `requirements/tiers/index.md`, `requirements/tiers/swrs/index.md` and
  `requirements/tiers/swrs/core/index.md`). Do not edit the generated fields by hand.
- Append a dated entry `## YYYY-MM-DD` (the day of the change; one heading per date, newest
  first, keep earlier entries) to `requirements/tiers/log.md`: added SwRS-OKFSCHEMA-CORE-010
  (S1 to S3) as the shared "stay inside the bundle" rule, applied to `show` only so far;
  CORE-005 gained S3, S4 (a leading `/` reads from the bundle root, OKF 0.2 section 6.1), a
  widened S2 and `depends_on` CORE-010; the reason (`show` read files outside the bundle and
  refused names without `.md`); the verification results. The entry
  names no ticket.

### 4. Human documentation

- `docs/source/reference/cli.md`, section `## okf-schema show` (line 223): document
  `CONCEPT_PATH` (a name from the bundle root, with or without a leading `/`, from any
  terminal folder; or an absolute disk path inside the bundle; a `/` path that is not a disk
  path inside the bundle is read from the bundle root, so on POSIX `/etc/passwd` is searched in
  the bundle and not found; `.md` optional, the exact file first, else `<name>.md`, a directory
  is never a concept), the errors (`Error: Concept not found: ...`,
  `Error: Concept path is outside the bundle: ...`, which also applies to symlinks whose target
  is outside), exit code 2, and one example for each form.
  Add the limit (Q13): on a case-insensitive file system such as macOS, an absolute
  `CONCEPT_PATH` whose bundle part is spelled in another case than `--path` (for example
  `/Users/me/KB/x.md` with `--path /Users/me/kb`) is not recognized as inside the bundle: it is
  read from the bundle root and reported as `Error: Concept not found: ...`; spell it as
  `--path` does, or pass a name from the bundle root.
- `docs/source/tutorials/getting-started.md:89` and `docs/source/tutorials/knowledge-graph.md:94`
  already use the extensionless form, and this CR makes it work. Do not change their text.
- `README.md`: no `show` usage to update (it only mentions `stats`). Unaffected.

### 5. Standalone agent skill

- `skills/okf-schema/SKILL.md:135`: the table row becomes
  `` `show --path <bundle> <concept>` | Show a single concept's frontmatter and body; `.md` is
  optional; names start from the bundle root (a leading `/` is allowed); paths and symlinks
  leaving the bundle are refused (exit 2) ``.
  No other skill or reference mentions `show` (checked with `git grep`).

### 6. Other surfaces (checked, unaffected; give these reasons in the change summary)

- Scaffold guidance `src/okf_schema/data/`: no `show` usage.
- Examples `examples/`: no example runs `show`.
- `docs/source/explanation/project-feature-coverage.md`: it maps okfreq and project capabilities.
  Its CORE-006 row mentions `stale` in `show`, which does not change. No row added.
- CI, `justfile`, packaging: unchanged.
- `CHANGELOG.md` is generated from the commit messages at release. Do not edit it.

### 7. Commit and release (Q12)

- One plain `fix(show): ...` commit, following
  `.github/guidelines/git-commit-message.guidelines.md`: no `!` after the type and no
  `BREAKING CHANGE:` section. Reading outside the bundle was never documented, so refusing it
  fixes a defect. The body may say that paths outside the bundle are now refused.
- The release is a patch, 0.18.2, made by the project's commitizen release
  (`version_scheme = "semver"` in `pyproject.toml`) from that `fix` commit. The Driver does not
  bump the version and does not write a `chore: version` commit.
- That guideline asks for no issue reference; one, if kept, is a project choice (for example
  a `Closes #56` trailer).

## Out of scope

- How `validate`, `list`, `index`, `backlinks` and `lint` handle symlinks: the separate CR
  `bundle-outside-symlinks` (Q8), which adds those commands to SwRS-OKFSCHEMA-CORE-010 (Q11)
  and removes its "Known issue" line.
- The `show` output format: issue 58.
- Links written inside Markdown files (a path without `/` or `./` is relative to the file that
  holds it) and the validation of Markdown files: already applied by the tool, unchanged (Q14,
  Q15: that rule concerns links in files, not the name given to `show`).
- Any change to `backlinks_bundle`, `new` or the other commands.
- A file inside the bundle that cannot be read (permissions, encoding): its behavior does not
  change.

## Evidence

The tests follow `.github/guidelines/python-unittest.guidelines.md`. Each new test carries
`# @tests_req <ID>#S<n>` with the fragment: `SwRS-OKFSCHEMA-CORE-005#S2` or `#S3` for name
resolution, directories and names from the bundle root (written `#S<n>` below), `SwRS-OKFSCHEMA-CORE-010#S1`, `#S2` or
`#S3` for containment (written `010#S<n>` below). Fixtures are built in `tmp_path`.
Symlink tests create the link with `Path.symlink_to`. When that raises `OSError` (Windows
without the symlink privilege), they call `pytest.skip("symlinks not permitted on this host")`.
The `windows-latest` runner allows symlinks: the existing
`tests/test_cli_core.py::test_install_skills_rejects_owned_symlink_with_click_error` already
creates them there. These tests must therefore run, not be skipped, in the CI log of the
`cross-platform` job.

API, `tests/test_api.py` (next to the `show_bundle` tests near line 546):
1. `api/health-check` resolves to `api/health-check.md` (#S3).
2. When both `notes` (a file with frontmatter) and `notes.md` exist, `notes` reads the
   extensionless file (#S3).
3. With an `api/` directory and `api.md`, `api` reads `api.md` (#S3).
4. An `api/` directory with no `api.md` raises `FileNotFoundError` matching
   `Concept not found` (#S2).
5. `.` and `/` raise `FileNotFoundError` matching `Concept not found` (#S2). With a file
   `<bundle name>.md` created beside the bundle, `.` raises `FileNotFoundError` matching
   `outside the bundle` instead, and that file is not read (010#S1).
6. `../outside.md` (the file exists beside the bundle) and `../outside` both raise
   `FileNotFoundError` matching `outside the bundle` (010#S1).
7. An absolute disk path to a concept inside the bundle (`str(bundle / "concept-a.md")`)
   succeeds (010#S3). An absolute disk path to an existing file outside (`str(outside)`) raises
   `FileNotFoundError` and the file is not read: on Windows (a drive path) matching
   `outside the bundle` (010#S1); on POSIX (it starts with `/`) matching `Concept not found`
   (#S4). The test picks the expected message from `os.name`.
7b. `/concept-a` and `/concept-a.md` give the same `ConceptDetail` as `concept-a.md` (#S4).
    With `etc/notes.md` created in the bundle, `/etc/notes` reads it (#S4; portable, since no
    host has that path inside `tmp_path`). `/etc/passwd` raises `FileNotFoundError` matching
    `Concept not found` (#S4).
8. `sub/../concept-a.md` succeeds (010#S3).
9. A symlink file inside the bundle that points outside, and a file reached through a symlinked
   directory that points outside, both raise the outside error (010#S2). A symlink inside that
   points to a concept inside succeeds (010#S3).
10. The existing tests at `tests/test_api.py:551-635` keep passing unchanged.

CLI, `tests/test_cli_remaining.py` (`show` section, using `_make_bundle`):
11. `show --path <bundle> concept-a` exits 0, and its output equals the output of `concept-a.md`
    (#S3).
12. `show --path <bundle> subdir` exits 2. The output has `Error: Concept not found`, has no
    `Traceback`, and `result.exception` is a `SystemExit` (#S2).
13. `show --path <bundle> ../outside.md` (the file exists) exits 2 with
    `Error: Concept path is outside the bundle` (010#S1).
13b. `show --path <bundle> /concept-a` exits 0 and its output equals the output of
     `concept-a.md`; run again after `monkeypatch.chdir` to another `tmp_path` folder, with an
     absolute `--path`, `show --path <bundle> concept-a` gives the same output (#S4).

Acceptance, `tests/test_acceptance_core.py::test_inspection_reports_matching_concepts_and_changes_no_file`
(`@accepts_req StRS-OKFSCHEMA-CORE-002#S3`, installed wheel):
14. Add `inspect("show", "--path", str(bundle), "concepts/clock")` and assert that
    `"The clock ticks."` is in its output. This is the issue's own invocation, run against the
    installed console script. The snapshot check still proves that nothing was written.

`tests/test_edge_cases.py::test_path_edge_cases_concept_path_with_parent_references` claims to
test `..` but passes `concept.md`. Make it pass `sub/../concept.md` (with `sub/` created) so it
tests what its name says, and mark it `# @tests_req SwRS-OKFSCHEMA-CORE-010#S3`.

Scenario steps (a real run, output kept as evidence), from a disposable folder with the built
package (`uv run -- okf-schema ...` from the worktree):
- `okf-schema init my-knowledge-base`, then
  `okf-schema new --path my-knowledge-base/bundle --name api/health-check`, then
  `okf-schema show --path my-knowledge-base/bundle api/health-check`: exit 0, the frontmatter
  and body are printed (the Getting Started step).
- `okf-schema show --path my-knowledge-base/bundle /api/health-check`: exit 0, the same output.
- `okf-schema show --path my-knowledge-base/bundle /etc/passwd`: exit 2,
  `Error: Concept not found: ...` naming a path inside the bundle; nothing outside is read.
- `okf-schema show --path my-knowledge-base/bundle api`: exit 2,
  `Error: Concept not found: ...`, no traceback.
- Write `secret.md` in the disposable folder, then
  `okf-schema show --path my-knowledge-base/bundle ../../secret`: exit 2,
  `Error: Concept path is outside the bundle: ...`.

Requirement checks: after `okfreq update-coverage requirements`, SwRS-OKFSCHEMA-CORE-010 lists
`src/okf_schema/api.py` in `implemented_in_files` and the test files above in
`tested_in_files`; each of its scenarios S1 to S3 has at least one `@tests_req` marker;
`okfreq trace requirements --json` shows it covered; CORE-005 has the "Depends on" group
naming CORE-010 in its Links section.

Gates: `okfreq update-coverage requirements --check`,
`okfreq validate requirements --prose --check-links --project-root .`,
`okfreq lint requirements --check --check-links --project-root .`, then `just preflight`. All
pass. Review the generated diffs before reporting, as `AGENTS.md` asks.

No host and default matrix applies: the change does not depend on the agent host or on a
configured value. OS differences are covered above: the directory failure looked different on
Windows and POSIX, and `is_file()` now removes it on both; a leading `/` is never a disk path
on Windows and is one on POSIX, so test 7 states both outcomes and tests 7b and 13b are
portable; symlink creation needs a privilege on
Windows, so those tests skip there when it is missing and run in CI.

## Open questions

1. Windows names starting with `\` (for example `\api\status`): answers 14 and 15 speak of a
   leading `/` only. As specified, a leading `\` is not stripped: on Windows it is a
   drive-rooted path, outside the bundle unless the bundle sits there, so it gets the "outside
   the bundle" refusal. Should a leading `\` be read from the bundle root like `/` on Windows?
