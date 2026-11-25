# show: resolve concept names without .md, stay inside the bundle

issue: https://github.com/gsemet/okf-schema/issues/56

## Goal

`okf-schema show --path <bundle> api/health-check` prints the concept, as the Getting Started
and knowledge-graph tutorials say. `show` takes a concept name with or without `.md`. It opens
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
2. `raw = bundle / concept_path`. With pathlib, an absolute `concept_path` replaces `bundle`, so
   an absolute path is handled by the same steps. An absolute path inside the bundle stays
   accepted (Q6).
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
     The file is never opened. This holds for `../x.md`, an absolute path elsewhere, a symlinked
     file whose target is outside, and a file under a symlinked directory that points outside.
   - When no candidate is a file and the real path of `raw` is outside the bundle, raise the
     same "outside the bundle" `FileNotFoundError` (Q4: a path that leaves the bundle is an
     error, whether or not something exists there).
   - When no candidate is a file and `raw` is inside the bundle or is the bundle root (`.`,
     `""`, `sub/..`), raise `FileNotFoundError(f"Concept not found: {raw}")`. This keeps today's
     message. The bundle root and any other directory with no matching `.md` end here (Q3).
5. Read the target and build the `ConceptDetail` as today. A `..` path whose real path stays
   inside the bundle (for example `sub/../concept-a.md`) works as before (Q4: nothing changes for
   paths inside).

Q7: the API raises `FileNotFoundError` in every refusal (not found, directory, outside, symlink
leaving), each with an explicit message. No new exception type is added. `NotADirectoryError`
for a bundle path that is a file does not change.

Update the `show_bundle` docstring (Google style, per
`.github/guidelines/python-module-documentation.guidelines.md`):
- `concept_path`: a bundle-relative or absolute path, with or without `.md`;
- the resolution order;
- `Raises: FileNotFoundError` for a missing concept, a directory, or a path or symlink whose
  real path is outside the bundle; `NotADirectoryError` as today.
`docs/source/reference/api.md:137` renders this docstring through `autofunction`.

Keep the `# @implements_req SwRS-OKFSCHEMA-CORE-006` marker on `show_bundle`, because it still
derives the trust tier and staleness. Add `# @implements_req SwRS-OKFSCHEMA-CORE-005` next to
it, since this CR changes the inspection contract of CORE-005.

### 2. Runtime: `show` command (`src/okf_schema/cli.py`)

- No new option. The existing `except (FileNotFoundError, NotADirectoryError)` already prints
  `Error: <message>` and exits 2. Now that the new tests cover that line, remove its
  `# pragma: no cover`.
- Docstring `Examples:` gains `okf-schema show --path bundle concepts/clock` next to the
  existing `.md` form. Add one sentence: the `.md` extension is optional, and a path outside the
  bundle is refused. Click shows this text in `okf-schema show --help`.

### 3. Requirement: `requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-005.md`

Follow `src/okf_schema/data/requirements/guidelines/requirements.guidelines.md` and
`requirements/guidelines/project.guidelines.md`. Keep the `id`, `uuid`, title, existing
scenarios S1/S2 and the authored metadata. The document stays `req_lifecycle: proposed` and
gets no approval.
- Add to `scenarios:` and to the body:
  - `S3` "Resolve a concept name without its extension": GIVEN a bundle with `api/health-check.md`
    (and possibly an `api/` directory beside an `api.md`), WHEN the user shows `api/health-check`
    or `api`, THEN the exact path is used when it is a file, else `<name>.md`, and a directory is
    never shown.
  - `S4` "Refuse a target outside the bundle": GIVEN a concept path, absolute path or symlink
    whose real path is outside the bundle, WHEN the user shows it, THEN okf-schema reports an
    "outside the bundle" error, exits 2 on the CLI, raises `FileNotFoundError` in the API, and
    reads nothing outside the bundle.
- Extend S2's GIVEN to "a missing bundle, a missing concept path, or a directory".
- Add one sentence to the normative paragraph: show resolves a concept path with or without
  `.md` and never reads outside the bundle.
- Then run `okfreq update-coverage requirements` (generated fields such as `tested_in_files`)
  and `okfreq lint requirements --prose --check-links --project-root .` (navigation). Do not
  edit the generated fields by hand.
- Append a dated entry to `requirements/tiers/log.md` (authored, newest first, keep earlier
  entries): CORE-005 gained S3/S4 and a widened S2, with the reason (issue 56) and the
  verification results.

### 4. Human documentation

- `docs/source/reference/cli.md`, section `## okf-schema show` (line 223): document
  `CONCEPT_PATH` (bundle-relative or absolute, `.md` optional, the exact file first, else
  `<name>.md`, a directory is never a concept), the errors (`Error: Concept not found: ...`,
  `Error: Concept path is outside the bundle: ...`, which also applies to symlinks whose target
  is outside), exit code 2, and one example for each form.
- `docs/source/tutorials/getting-started.md:89` and `docs/source/tutorials/knowledge-graph.md:94`
  already use the extensionless form, and this CR makes it work. Do not change their text.
- `README.md`: no `show` usage to update (it only mentions `stats`). Unaffected.

### 5. Standalone agent skill

- `skills/okf-schema/SKILL.md:135`: the table row becomes
  `` `show --path <bundle> <concept>` | Show a single concept's frontmatter and body; `.md` is
  optional; paths and symlinks leaving the bundle are refused (exit 2) ``.
  No other skill or reference mentions `show` (checked with `git grep`).

### 6. Other surfaces (checked, unaffected; give these reasons in the change summary)

- Scaffold guidance `src/okf_schema/data/`: no `show` usage.
- Examples `examples/`: no example runs `show`.
- `docs/source/explanation/project-feature-coverage.md`: it maps okfreq and project capabilities.
  Its CORE-006 row mentions `stale` in `show`, which does not change. No row added.
- CI, `justfile`, packaging: unchanged.
- `CHANGELOG.md` is generated from the commit messages at release. Do not edit it. The commit
  follows `.github/guidelines/git-commit-message.guidelines.md` (a `fix(show): ...` type, with
  the issue reference the guideline asks for).

## Out of scope

- How `validate`, `list`, `index`, `backlinks` and `lint` handle symlinks: the separate CR
  `bundle-outside-symlinks` (Q8).
- The `show` output format: issue 58.
- Any change to `backlinks_bundle`, `new` or the other commands.
- A file inside the bundle that cannot be read (permissions, encoding): its behavior does not
  change.

## Evidence

The tests follow `.github/guidelines/python-unittest.guidelines.md`. Each new test carries
`# @tests_req SwRS-OKFSCHEMA-CORE-005#S<n>` with the fragment. Fixtures are built in `tmp_path`.
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
5. `.` raises `FileNotFoundError` matching `Concept not found` (#S2).
6. `../outside.md` (the file exists beside the bundle) and `../outside` both raise
   `FileNotFoundError` matching `outside the bundle` (#S4).
7. An absolute path to a concept inside the bundle succeeds. An absolute path to an existing
   file outside raises the outside error (#S4).
8. `sub/../concept-a.md` succeeds (#S3, inside path unchanged).
9. A symlink file inside the bundle that points outside, and a file reached through a symlinked
   directory that points outside, both raise the outside error. A symlink inside that points to
   a concept inside succeeds (#S4).
10. The existing tests at `tests/test_api.py:551-635` keep passing unchanged.

CLI, `tests/test_cli_remaining.py` (`show` section, using `_make_bundle`):
11. `show --path <bundle> concept-a` exits 0, and its output equals the output of `concept-a.md`
    (#S3).
12. `show --path <bundle> subdir` exits 2. The output has `Error: Concept not found`, has no
    `Traceback`, and `result.exception` is a `SystemExit` (#S2).
13. `show --path <bundle> ../outside.md` (the file exists) exits 2 with
    `Error: Concept path is outside the bundle` (#S4).

Acceptance, `tests/test_acceptance_core.py::test_inspection_reports_matching_concepts_and_changes_no_file`
(`@accepts_req StRS-OKFSCHEMA-CORE-002#S3`, installed wheel):
14. Add `inspect("show", "--path", str(bundle), "concepts/clock")` and assert that
    `"The clock ticks."` is in its output. This is the issue's own invocation, run against the
    installed console script. The snapshot check still proves that nothing was written.

`tests/test_edge_cases.py::test_path_edge_cases_concept_path_with_parent_references` claims to
test `..` but passes `concept.md`. Make it pass `sub/../concept.md` (with `sub/` created) so it
tests what its name says.

Scenario steps (a real run, output kept as evidence), from a disposable folder with the built
package (`uv run -- okf-schema ...` from the worktree):
- `okf-schema init my-knowledge-base`, then
  `okf-schema new --path my-knowledge-base/bundle --name api/health-check`, then
  `okf-schema show --path my-knowledge-base/bundle api/health-check`: exit 0, the frontmatter
  and body are printed (the Getting Started step).
- `okf-schema show --path my-knowledge-base/bundle api`: exit 2,
  `Error: Concept not found: ...`, no traceback.
- Write `secret.md` in the disposable folder, then
  `okf-schema show --path my-knowledge-base/bundle ../../secret`: exit 2,
  `Error: Concept path is outside the bundle: ...`.

Gates: `okfreq update-coverage requirements --check`,
`okfreq validate requirements --prose --check-links --project-root .`,
`okfreq lint requirements --check --check-links --project-root .`, then `just preflight`. All
pass. Review the generated diffs before reporting, as `AGENTS.md` asks.

No host and default matrix applies: the change does not depend on the agent host or on a
configured value. OS differences are covered above: the directory failure looked different on
Windows and POSIX, and `is_file()` now removes it on both; symlink creation needs a privilege on
Windows, so those tests skip there when it is missing and run in CI.

## Open questions

1. On macOS (a case-insensitive file system where `resolve()` does not fix the case), an
   absolute `CONCEPT_PATH` whose bundle part is spelled in a different case from `--path` (for
   example `/Users/me/KB/x.md` with `--path /Users/me/kb`) fails the `is_relative_to` check and
   is refused as outside the bundle. Should this be accepted (compare with
   `os.path.samefile` on the ancestors, more code), or is the refusal acceptable as a documented
   limit? Proposed: accept the refusal and document it in `docs/source/reference/cli.md`.
