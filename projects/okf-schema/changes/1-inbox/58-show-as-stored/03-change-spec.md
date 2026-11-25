# show: print the stored file, without the trust line

issue: https://github.com/gsemet/okf-schema/issues/58

## Goal

`okf-schema show --path <bundle> <concept>` prints the concept file exactly as it is stored:
byte for byte, frontmatter style, comments, quoting, line endings and body untouched, with
nothing added. It no longer prints `trust: <tier>` or `stale: true`. It does not validate the
file: a file without frontmatter or with invalid YAML is printed as it is, exit code 0, nothing
on stderr. The Python API `show_bundle` keeps its current fields and gains `raw`, the exact
stored text.

Code base: `origin/main` at 2f09cef (0.18.1); the line numbers below are from that commit.

**This CR stacks on CR-101 `show-extensionless-names` (issue 56)**, in the same batch, which
changes the same function and command. Everything below applies on top of CR-101's change:
CR-101's concept resolution, containment checks, error messages, exit codes, requirement
SwRS-OKFSCHEMA-CORE-010 and CORE-005 S3 stay as CR-101 delivers them. Where a surface is edited
by both CRs (the `show_bundle` docstring, the `show` docstring, `docs/source/reference/cli.md`
section `## okf-schema show`, the `skills/okf-schema/SKILL.md` row, SwRS-OKFSCHEMA-CORE-005, the
acceptance test), this CR extends CR-101's text and keeps all of it. If CR-101's final wording
differs from its specification, keep CR-101's delivered wording and add this CR's part to it.

## Current behavior (checked)

- `src/okf_schema/api.py:376` `show_bundle` reads the file with `read_text(encoding="utf-8")`
  (universal newlines: `\r\n` and `\r` become `\n`), splits it with `extract_frontmatter`,
  parses the frontmatter with `parse_yaml` (`None` for invalid YAML or a non-mapping, which then
  gives `{}`), derives `trust_tier` and `stale`, and returns
  `ConceptDetail(frontmatter, body, trust_tier, stale)`. The stored text is not returned.
- `src/okf_schema/_internal/models.py:179` `ConceptDetail` has `frontmatter`, `body`,
  `trust_tier: str = "unverified"`, `stale: bool = False`.
- `src/okf_schema/cli.py:754-770` `show` re-dumps `detail.frontmatter` with `make_yaml()`
  between `---` lines (flow mappings and lists become block style, datetimes are rewritten and
  quoted, comments are lost), prints `trust: <tier>` (line 766), `stale: true` when stale, then
  the body when it is not blank. A file without frontmatter, or with invalid YAML, is shown with
  an invented `---` / `{}` / `---` block, exit 0, nothing on stderr.
- No test, tutorial, skill, example or script reads the `trust:` or `stale: true` lines of
  `show` (checked in `tests/`, `docs/`, `skills/`, `examples/`, `scripts/`).
  `requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-006.md` S2 names `stale: true`.
- `list` prints a ` [STALE]` marker (`cli.py:713`); it does not change.

## What changes

### 1. Runtime: `ConceptDetail` (`src/okf_schema/_internal/models.py`)

Add one field, last, with a default so positional construction keeps working (Q4: the current
fields do not change):

```python
raw: str = ""
```

Extend the class docstring (Google style, per
`.github/guidelines/python-module-documentation.guidelines.md`) with an `Attributes:` section
describing all five fields; `raw` is "the concept file's exact stored text, decoded as UTF-8,
line endings and any byte order mark kept". `docs/source/reference/models.md:30` renders it
through `autoclass ... :members:`; no edit there.

### 2. Runtime: `show_bundle` (`src/okf_schema/api.py`)

CR-101's resolution steps 1 to 4 do not change. Its step 5 ("read the target and build the
`ConceptDetail` as today") becomes:

1. `data = target.read_bytes()`; `raw = data.decode("utf-8")` (strict, as today's
   `read_text`; see open question 1).
2. `text = raw.replace("\r\n", "\n").replace("\r", "\n")`: the same text `read_text` gave
   today, so `frontmatter`, `body`, `trust_tier` and `stale` are computed from it exactly as now
   (`extract_frontmatter`, `parse_yaml`, `{}` when absent or unparseable, `_derive_trust_tier`,
   `_is_stale`). Their values do not change for any file.
3. Return `ConceptDetail(frontmatter=..., body=..., trust_tier=..., stale=..., raw=raw)`.

`show_bundle` still does not raise for a file without frontmatter or with invalid YAML (Q3).

Docstring: the summary line and `Returns:` say the result holds the parsed frontmatter, the
body, the derived trust tier and staleness, and `raw`, the exact stored text. Keep CR-101's
`Args:`/`Raises:` text. Keep the markers CR-101 leaves on `show_bundle`
(`@implements_req SwRS-OKFSCHEMA-CORE-006` and `-CORE-005`).

### 3. Runtime: `show` command (`src/okf_schema/cli.py`)

- After the unchanged `try`/`except` around `show_bundle` (CR-101's error handling), replace
  lines 754-770 (the `io`/`make_yaml` dump, the `trust:` and `stale: true` echoes and the body
  echo) with a write of the stored bytes to the binary standard output:

  ```python
  stdout = click.get_binary_stream("stdout")
  stdout.write(detail.raw.encode("utf-8"))
  stdout.flush()
  ```

  Encoding a strictly decoded UTF-8 string gives back the stored bytes exactly. The binary
  stream is required: `click.echo` adds a final newline and, on Windows, a text stream turns
  `\n` into `\r\n`. Nothing else is written on success: no added newline, no `---` for a file
  without frontmatter, no `trust:`, no `stale:` (Q1, Q2, Q3). An empty file prints nothing,
  exit 0.
- The local imports `io` and `make_yaml` inside `show` go away. The module-level
  `from okf_schema._internal.yaml import make_yaml` (line 21) stays: it is used at line 277.
- Docstring: the first line (Click's help summary) becomes "Print a concept file exactly as
  stored." Add, next to CR-101's sentence about `.md` and the bundle: "The file is not parsed or
  validated; nothing is added to it. Read the trust tier from its `verified` field." Keep the
  `Examples:` CR-101 sets.
- The `# @implements_req SwRS-OKFSCHEMA-CORE-005` marker stays where it is (`list`, line 705);
  `cli.py` is already in CORE-005's `implemented_in_files`. Add the same marker inside `show`
  (above the `try`), since `show` now carries CORE-005 S4.

Q5: no command prints the trust tier any more. Its source stays the file's `verified` field,
which `show` now prints faithfully; `list` keeps `[STALE]`; the API keeps `trust_tier` and
`stale`. No new option, no stderr line.

### 4. Requirements

Follow `src/okf_schema/data/requirements/guidelines/requirements.guidelines.md` and
`requirements/guidelines/project.guidelines.md`. Both documents stay `req_lifecycle: proposed`
and get no approval. Keep `id`, `uuid`, titles and every authored field not named here.

#### 4a. `requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-005.md`

On top of CR-101's edits (S3, widened S2, `depends_on`):
- Add to `scenarios:` and as a body section `### Scenario S4: Show a concept as stored`:
  - GIVEN a concept file in the bundle, whatever its frontmatter style, comments, line endings,
    or whether it has frontmatter or valid YAML at all
  - WHEN the user shows it
  - THEN the CLI writes the stored bytes to standard output, unchanged and with nothing added
    (no trust or staleness line), exits 0 and writes nothing to standard error, and the API
    result's `raw` holds the stored text
- Add under `### Verification notes`, Criteria: `show` output equals the stored file byte for
  byte, including a file without frontmatter, with invalid YAML, or with CRLF line endings.
- Leave the frontmatter `description` and the normative paragraph unchanged (they still
  describe `show` correctly: deterministic results, bundle not modified).

#### 4b. `requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-006.md`

S2's THEN names `stale: true`, a line `show` no longer prints. Replace
"it is stale (W11, `stale: true`)" with "it is stale (W11 on validation, `stale` true in the
API result, `[STALE]` in `list`)". The rest of S2, the other scenarios, the description and the
normative paragraph do not change.

#### 4c. Generated fields, navigation and log

- Run `okfreq update-coverage requirements` and
  `okfreq lint requirements --prose --check-links --project-root .`. Never edit generated
  fields or Links sections by hand.
- In `requirements/tiers/log.md`, under the day's `## YYYY-MM-DD` heading (one heading per
  date, newest first; share it with CR-101's entry if it is the same day, keep earlier entries):
  CORE-005 gained S4 (show prints the stored file, nothing added, no validation); CORE-006 S2
  no longer names the removed `stale: true` line; the reason (`show` re-serialized the
  frontmatter and printed a `trust:` line inside the document); the verification results. No
  ticket named.

### 5. Human documentation

- `docs/source/reference/cli.md`, section `## okf-schema show` (as CR-101 leaves it): the
  description line becomes "Print a concept file exactly as stored." Add an "Output" paragraph:
  standard output is the file byte for byte (frontmatter style, comments, line endings, body);
  `show` does not parse or validate it, so a file without frontmatter or with invalid YAML is
  printed as is with exit 0 (use `okf-schema validate` to check it); nothing is added, in
  particular no trust tier or staleness line. To learn the trust tier, read the `verified` field
  in the output; `okf-schema list` marks stale concepts with `[STALE]`; the Python API
  `show_bundle` returns `trust_tier`, `stale` and `raw`. Keep CR-101's `CONCEPT_PATH`, errors,
  exit code and macOS limit text.
- `docs/source/tutorials/getting-started.md:89` ("Inspect the document and its frontmatter")
  and `docs/source/tutorials/knowledge-graph.md:94` show no output and stay true. Unchanged.
- `README.md`: no `show` usage. Unaffected.
- `docs/source/explanation/project-feature-coverage.md:31` (OKF 0.2 staleness row): replace
  "`tests/test_api.py` covers `stale` in `list`/`show`" with "`tests/test_api.py` covers
  `stale` in `list_bundle` and `show_bundle`", since the `show` command no longer prints it.

### 6. Standalone agent skill

- `skills/okf-schema/SKILL.md:135`, the row as CR-101 leaves it, becomes
  `` `show --path <bundle> <concept>` | Print a concept file exactly as stored (not reformatted,
  not validated, no trust line); `.md` is optional; paths and symlinks leaving the bundle are
  refused (exit 2) ``. Line 45 ("init, list, show, stats, index") stays. No other skill or
  reference mentions the `show` command.

### 7. Other surfaces (checked, unaffected; give these reasons in the change summary)

- Scaffold guidance `src/okf_schema/data/`: no `show` usage.
- Examples `examples/`: no example runs `show`.
- CI, `justfile`, packaging: unchanged. `CHANGELOG.md` is generated at release; do not edit.

### 8. Commit and release (Q6)

- One plain `fix(show): ...` commit, following
  `.github/guidelines/git-commit-message.guidelines.md`: no `!`, no `BREAKING CHANGE:`. The body
  may say that `show` now prints the stored file and no longer prints `trust:`/`stale: true`,
  and that `ConceptDetail` gains `raw`. An issue reference, if kept, is a project choice (for
  example a `Closes #58` trailer).
- The release is the patch 0.18.2 made by the project's commitizen release from the `fix`
  commits (shared with CR-101 when released together). The Driver does not bump the version.

## Out of scope

- Concept resolution, containment and error messages: CR-101.
- Any option to print the trust tier (`--trust`, a header, a stderr line): Q2/Q5 drop it; no
  new CR.
- `list`, `validate`, `lint` and the other commands; `[STALE]` in `list` stays.
- The values of `ConceptDetail.frontmatter`, `body`, `trust_tier`, `stale`.
- A file inside the bundle that is not valid UTF-8 or not readable: behavior unchanged
  (open question 1).

## Evidence

Tests follow `.github/guidelines/python-unittest.guidelines.md`; fixtures are written in
`tmp_path` with `write_bytes` where exact bytes matter. New tests carry
`# @tests_req SwRS-OKFSCHEMA-CORE-005#S4` unless stated otherwise.

API, `tests/test_api.py` (show_bundle section, next to CR-101's tests):
1. A file with flow-style frontmatter, a YAML comment, an unquoted datetime and a body:
   `detail.raw == path.read_bytes().decode("utf-8")`, and `frontmatter`/`body` are as before.
2. A CRLF file (`write_bytes(b"---\r\ntitle: T\r\n---\r\nBody\r\n")`): `raw` keeps `\r\n`;
   `frontmatter == {"title": "T"}` and `body` has no `\r`, as with today's `read_text`.
3. Invalid YAML frontmatter (for example `---\ntitle: [unclosed\n---\nBody\n`): no exception,
   `frontmatter == {}`, `raw` equals the stored text.
4. The existing `test_show_bundle_*` tests (trust tier, stale, no frontmatter) pass unchanged.
   Extend `test_show_bundle_concept_without_frontmatter` with an assertion on `raw`.

CLI, `tests/test_cli_remaining.py` (`show` section), comparing `result.stdout_bytes` with
`path.read_bytes()`:
5. `concept-a.md` of `_make_bundle` (flow list `tags: [alpha, beta]`): exact equality; and
   `b"trust:"` not in the output.
6. A file with `verified:` (human actor) and a past `stale_after` (a file that holds neither
   `trust:` nor `stale:`): exact equality, and neither `b"trust:"` nor `b"stale: true"` is in
   the output.
7. No frontmatter (`# Title\n\nBody.\n`): exact equality, no `---` added, exit 0,
   `result.stderr == ""`.
8. Invalid YAML frontmatter: exact equality, exit 0, empty stderr.
9. CRLF file and a file without a final newline: exact equality (no `\r` added or removed, no
   newline appended).
10. Real process, to catch Windows text-mode translation that `CliRunner` cannot see: run
    `subprocess.run([sys.executable, "-c", "from okf_schema.cli import cli; cli()", "show",
    "--path", str(bundle), "lf.md"], capture_output=True)` on an LF file and assert
    `stdout == path.read_bytes()`. This runs on `windows-latest` and `macos-latest` in the
    `cross-platform` CI job and must pass there.
11. Existing tests that assert substrings of `show` output
    (`test_show_show_outputs_frontmatter_and_body`,
    `tests/test_integration.py::test_cli_integration_show_cli_output`, the defensive
    `NotADirectoryError` test, CR-101's tests) keep passing; tighten
    `test_show_show_outputs_frontmatter_and_body` to the exact-bytes assertion of test 5 or
    leave it, but do not weaken it.

Acceptance, `tests/test_acceptance_core.py::test_inspection_reports_matching_concepts_and_changes_no_file`
(`@accepts_req StRS-OKFSCHEMA-CORE-002#S3`, installed wheel, reading the shipped command):
12. After the existing `lint`, assert that the output of
    `inspect("show", "--path", str(bundle), "concepts/clock.md")` equals
    `(bundle / "concepts" / "clock.md").read_text(encoding="utf-8")` and has no `trust:` line.
    Keep CR-101's extensionless `inspect(... "concepts/clock")` assertion. The snapshot check
    still proves nothing was written. In
    `test_init_then_new_creates_a_valid_bundle_that_keeps_the_authored_concept` the
    `"title: Clock"` and `"The clock ticks."` assertions stay true.

Scenario steps (a real run, output kept as evidence), in a disposable folder, with
`uv run -- okf-schema ...` from the worktree:
- `okf-schema init my-knowledge-base`;
  `okf-schema new --path my-knowledge-base/bundle --name api/health-check --type "API Endpoint" --title "Health Check"`;
  `okf-schema show --path my-knowledge-base/bundle api/health-check` (CR-101's form): output
  identical to the file (compare with `cmp` or a byte diff), no `trust: unverified` line.
- Edit the file to flow style with a comment (`links: [api/health-check.md]  # keep`), run
  `okf-schema lint --path my-knowledge-base/bundle`, then `show`: output identical to the file.
- Write `broken.md` with `---\ntitle: [unclosed\n---\nBody\n` and a `plain.md` without
  frontmatter in the bundle; `show` each: exit 0, output identical to the file, empty stderr.

Requirement checks: after `okfreq update-coverage requirements`, CORE-005 S4 has `@tests_req`
markers; `okfreq trace requirements --json` shows CORE-005 and CORE-006 covered.

Gates: `okfreq update-coverage requirements --check`,
`okfreq validate requirements --prose --check-links --project-root .`,
`okfreq lint requirements --check --check-links --project-root .`, then `just preflight`. All
pass; review the generated diffs before reporting, as `AGENTS.md` asks.

No host and default matrix applies: nothing depends on the agent host or a configured value.
The one OS difference (Windows text-mode newline translation) is covered by test 10, which the
`cross-platform` job runs on Windows and macOS.

## Open questions

1. A concept file that is not valid UTF-8: today `show` fails with an uncaught
   `UnicodeDecodeError` (a traceback), and CR-101 left unreadable files out of scope. "show ne
   valide pas" could mean `show` should print such bytes too, but `raw` is text in the API.
   This specification keeps today's behavior. Should the CLI instead print the bytes as they
   are (and the API keep failing), or report a plain `Error:` with exit 2?
