# show: print the stored file; new trust command for the tier

issue: https://github.com/gsemet/okf-schema/issues/58

## Goal

`okf-schema show --path <bundle> <concept>` prints the concept file exactly as it is stored:
byte for byte, frontmatter style, comments, quoting, line endings and body untouched, with
nothing added. It no longer prints `trust: <tier>` or `stale: true`. It does not validate the
file: a file without frontmatter, with invalid YAML, or not valid UTF-8 is printed as it is,
exit code 0, nothing on stderr. The Python API `show_bundle` keeps its current fields and gains
`raw`, the exact stored text.

A new, documented command, `okf-schema trust --path <bundle> <concept>`, prints exactly the two
lines `show` used to add: `trust: <tier>`, then `stale: true` when the concept is stale. The
removal and its replacement land together, in one pull request (Q10).

Code base: `origin/main` at 2f09cef (0.18.1); the line numbers below are from that commit.

**Stacking.** This CR lands after two CRs of the same batch, and applies on top of both:

- **CR-101 `show-extensionless-names`** (issue 56) changes the same function and command:
  concept resolution (with or without `.md`; a name starting with `/` read from the bundle root,
  per its updated specification), containment checks, error messages, exit codes, the new
  requirement SwRS-OKFSCHEMA-CORE-010 and CORE-005 S3 and S4 stay as CR-101 delivers them.
  Where a surface is edited by both CRs (the `show_bundle` docstring, the `show` docstring,
  `docs/source/reference/cli.md` section `## okf-schema show`, the `skills/okf-schema/SKILL.md`
  row, SwRS-OKFSCHEMA-CORE-005, SwRS-OKFSCHEMA-CORE-010, the acceptance test), this CR extends
  CR-101's text and keeps all of it. If CR-101's delivered wording or code differs from its
  specification, keep what CR-101 delivered and add this CR's part to it.
- **CR `trust-actor-forms`** (not yet specified) makes the trust tier right for the actor forms
  of OKF 0.2 (`_derive_trust_tier`, W10, their documentation). This CR does not touch the tier
  derivation (Q12): the `trust` command prints the tier `_derive_trust_tier` returns as that CR
  leaves it. Where both CRs edit SwRS-OKFSCHEMA-CORE-006 or `requirements/tiers/log.md`, keep
  that CR's edits and add this CR's.

**Neighbour CR 57 `index-broken-root-links`** (issue 57, same batch) edits some of the same
files: `skills/okf-schema/SKILL.md` (its `index` row, line 136, right next to this CR's `show`
row and new `trust` row), `docs/source/reference/cli.md` (its `## okf-schema index` section,
right after this CR's new `## okf-schema trust` section) and `requirements/tiers/log.md` (an
entry under the same day heading). Whichever of 57 and 58 lands second rebases on the other and
keeps both CRs' rows, both CRs' `cli.md` changes and both log entries.

**Neighbour inbox item `bundle-outside-symlinks`** (split from CR-101, not yet specified) adds
`validate`, `list`, `index`, `backlinks` and `lint` to the same SHALL sentence of
SwRS-OKFSCHEMA-CORE-010 (its frontmatter `description` and normative paragraph, which section 5c
widens to `trust`) and removes CR-101's "Known issue" line. Whichever of that item and this CR
lands second merges both widenings into one statement (and the same for the scenarios' WHEN
lines and the verification Method), keeping both. The "Known issue" line follows that item: this
CR neither edits nor removes it.

## Current behavior (checked)

- `src/okf_schema/api.py:376` `show_bundle` reads the file with `read_text(encoding="utf-8")`
  (universal newlines: `\r\n` and `\r` become `\n`; a file that is not valid UTF-8 raises
  `UnicodeDecodeError`), splits it with `extract_frontmatter`, parses the frontmatter with
  `parse_yaml` (`None` for invalid YAML or a non-mapping, which then gives `{}`), derives
  `trust_tier` (`_derive_trust_tier`, `validator.py:355`) and `stale` (`_is_stale`,
  `validator.py:432`), and returns `ConceptDetail(frontmatter, body, trust_tier, stale)`. The
  stored text is not returned.
- `_derive_trust_tier` returns one of `"unverified"`, `"machine-confirmed"`,
  `"human-reviewed"`, from the `verified` field only; a bare mapping is read as a one-element
  list. `_is_stale` is true when the current instant (for an offset datetime, UTC) or the
  current calendar day (for a bare date) has reached `stale_after`; an absent or unparseable
  value is never stale.
- `src/okf_schema/_internal/models.py:179` `ConceptDetail` has `frontmatter`, `body`,
  `trust_tier: str = "unverified"`, `stale: bool = False`.
- `src/okf_schema/cli.py:754-770` `show` re-dumps `detail.frontmatter` with `make_yaml()`
  between `---` lines (flow mappings and lists become block style, datetimes are rewritten and
  quoted, comments are lost), prints `trust: <tier>` (line 766), `stale: true` when stale, then
  the body when it is not blank. A file without frontmatter, or with invalid YAML, is shown with
  an invented `---` / `{}` / `---` block (and `trust: unverified`), exit 0, nothing on stderr. A
  file that is not valid UTF-8 ends in a `UnicodeDecodeError` traceback.
- No test, tutorial, skill, example or script reads the `trust:` or `stale: true` lines of
  `show` (checked in `tests/`, `docs/`, `skills/`, `examples/`, `scripts/`).
  `requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-006.md` S2 names `stale: true`.
- `list` prints a ` [STALE]` marker (`cli.py:713`); it does not change.
- No command is named `trust` (`cli.py` registers `init`, `new`, `validate`, `validate-md`,
  `lint`, `list`, `show`, `index`, `stats`, `backlinks`, `kb`, `install-skills`).

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

### 2. Runtime: concept resolution and `show_bundle` (`src/okf_schema/api.py`)

- **One resolution for `show_bundle` and the `show` command.** The `show` command must print the
  bytes of a file that is not valid UTF-8 (Q11), while `show_bundle` keeps failing on it, so the
  command cannot go through `show_bundle`. Move CR-101's resolution and containment steps (every
  step before "read the target") into one private function of `api.py`:

  ```python
  def _resolve_concept_file(bundle_path: str | Path, concept_path: str) -> Path:
  ```

  It returns the target file and raises exactly what CR-101's steps raise (`FileNotFoundError`
  with CR-101's messages, `NotADirectoryError` for a bundle path that is a file). It reads no
  file content. Google-style docstring with `Args:`, `Returns:`, `Raises:`. If CR-101's
  delivered code already has such a function, reuse it under its name instead of adding one.
  Keep CR-101's `_require_inside_bundle` helper and its `@implements_req SwRS-OKFSCHEMA-CORE-010`
  marker where CR-101 put them.
- **`show_bundle`** becomes:
  1. `target = _resolve_concept_file(bundle_path, concept_path)`.
  2. `raw = target.read_bytes().decode("utf-8")`: strict, so a file that is not valid UTF-8
     still raises `UnicodeDecodeError`, as today (Q11: the API keeps failing).
  3. `text = raw.replace("\r\n", "\n").replace("\r", "\n")`: the same text `read_text` gave
     today, so `frontmatter`, `body`, `trust_tier` and `stale` are computed from it exactly as
     now (`extract_frontmatter`, `parse_yaml`, `{}` when absent or unparseable,
     `_derive_trust_tier`, `_is_stale`). Their values do not change for any file.
  4. Return `ConceptDetail(frontmatter=..., body=..., trust_tier=..., stale=..., raw=raw)`.

  `show_bundle` still does not raise for a file without frontmatter or with invalid YAML (Q3).
- Docstring of `show_bundle`: the summary line and `Returns:` say the result holds the parsed
  frontmatter, the body, the derived trust tier and staleness, and `raw`, the exact stored text.
  Keep CR-101's `Args:`/`Raises:` text and add to `Raises:` `UnicodeDecodeError` when the file
  is not valid UTF-8. Keep the markers CR-101 leaves on `show_bundle`
  (`@implements_req SwRS-OKFSCHEMA-CORE-006` and `-CORE-005`).

### 3. Runtime: `show` command (`src/okf_schema/cli.py`)

- Import `_resolve_concept_file` from `okf_schema.api` (the module already imports a private
  helper, `_register_install_skills` from `okf_schema.skill_cli`). `show_bundle` stays imported:
  the `trust` command uses it.
- In `show`, the `try` calls `target = _resolve_concept_file(bundle_path, concept_path)` instead
  of `show_bundle`, with CR-101's unchanged `except (FileNotFoundError, NotADirectoryError)`
  (`Error: <message>` on stderr, exit 2). Then replace lines 754-770 (the `io`/`make_yaml` dump,
  the `trust:` and `stale: true` echoes and the body echo) with a write of the stored bytes to
  the binary standard output:

  ```python
  stdout = click.get_binary_stream("stdout")
  stdout.write(target.read_bytes())
  stdout.flush()
  ```

  The bytes are never decoded, so a file that is not valid UTF-8 is printed as it is, exit 0
  (Q11), and a byte order mark or CR/CRLF line endings are kept. The binary stream is required:
  `click.echo` adds a final newline and, on Windows, a text stream turns `\n` into `\r\n`.
  Nothing else is written on success: no added newline, no `---` for a file without
  frontmatter, no `trust:`, no `stale:` (Q1, Q2, Q3). An empty file prints nothing, exit 0. A
  file that cannot be read (permissions) keeps today's behaviour (out of scope).
- The local imports `io` and `make_yaml` inside `show` go away. The module-level
  `from okf_schema._internal.yaml import make_yaml` (line 21) stays: it is used at line 277.
- Docstring: the first line (Click's help summary) becomes "Print a concept file exactly as
  stored." Add, next to CR-101's sentence about `.md` and the bundle: "The file is not parsed or
  validated; nothing is added to it. Use `okf-schema trust` for its trust tier and staleness."
  Keep the `Examples:` CR-101 sets.
- Add `# @implements_req SwRS-OKFSCHEMA-CORE-005` inside `show` (above the `try`), since `show`
  now carries CORE-005 S5 (section 5a). `cli.py` is already in CORE-005's `implemented_in_files`.

### 4. Runtime: new `trust` command (`src/okf_schema/cli.py`)

Q9, Q10: a new command, placed right after `show` under its own three-line comment banner
(`# ---...`, `# trust`, `# ---...`), as the other commands have:

```python
@cli.command()
@click.option(
    "--path",
    "bundle_path",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Root directory of the OKF bundle.",
)
@click.argument("concept_path")
@click.pass_context
def trust(ctx: click.Context, bundle_path: str, concept_path: str) -> None:
```

- Behaviour: `detail = show_bundle(bundle_path, concept_path)` inside
  `try`/`except (FileNotFoundError, NotADirectoryError)` that prints `Error: <message>` to stderr
  and exits 2, as `show` does. Then:

  ```python
  click.echo(f"trust: {detail.trust_tier}")
  if detail.stale:
      click.echo("stale: true")
  ```

  Exactly what `show` added, nothing more (Q9): no score, no title, no path, no `stale: false`
  line, no listing of the whole bundle.
- The concept is resolved as `show` resolves it (through `show_bundle`, hence CR-101's rules:
  `.md` optional, a leading `/` read from the bundle root, paths and symlinks leaving the bundle
  refused with exit 2).
- The tier is `detail.trust_tier`, from the file's `verified` field only, with the code's tier
  names: `unverified`, `machine-confirmed`, `human-reviewed`. A bare `verified` mapping counts as
  a one-element list. The derivation itself is `_derive_trust_tier` as CR `trust-actor-forms`
  leaves it; this CR does not change it.
- Staleness is judged apart from the tier: `stale: true` when `detail.stale` (`_is_stale`: the
  current instant has reached `stale_after`, `now >= stale_after`; a bare date from that day on).
  An absent or unparseable `stale_after` prints no `stale:` line (W16 stays `validate`'s
  report).
- An unverified concept is a normal result: `trust: unverified`, exit 0. So is a file without
  frontmatter or with invalid YAML (`show_bundle` gives `{}`, hence `trust: unverified`), as
  `show` printed before. Every successful run exits 0, whatever the tier and staleness.
- The command never writes: no file of the bundle is created or changed.
- A file that is not valid UTF-8: `show_bundle` raises `UnicodeDecodeError` (Q11), which this
  command does not catch, so it ends in a traceback as `show` did before this CR (open
  question 1).
- Markers: `# @implements_req SwRS-OKFSCHEMA-CORE-006` inside `trust` above the `try` (it
  carries CORE-006 S5 and S6, section 5b).
- Docstring (Google style; its first line is Click's help summary): "Print a concept's trust
  tier and staleness." Then: "Prints `trust: <tier>` (`unverified`, `machine-confirmed` or
  `human-reviewed`, derived from the `verified` field) and, when `stale_after` has been reached,
  `stale: true`. The concept is resolved as `show` resolves it. Nothing is written." `Args:` for
  `ctx`, `bundle_path`, `concept_path`; `Examples:` `okf-schema trust --path bundle
  concepts/clock`.

### 5. Requirements

Follow `src/okf_schema/data/requirements/guidelines/requirements.guidelines.md` and
`requirements/guidelines/project.guidelines.md`. Every edited document stays
`req_lifecycle: proposed` and gets no approval. Keep `id`, `uuid`, titles and every authored
field not named here. The guideline makes a command a scenario of the behaviour it drives, not
a SwRS of its own: the `trust` command is a scenario of SwRS-OKFSCHEMA-CORE-006, whose S1
already derives the trust tier and staleness when a concept is "validated or inspected"; its
refusal is a scenario of its own, as the guideline asks (one scenario per refusal).

#### 5a. `requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-005.md`

On top of CR-101's edits (S3 "Resolve a concept name without its extension", S4 "Read a name
from the bundle root", widened S2, `depends_on`):
- Add to `scenarios:` and as a body section `### Scenario S5: Show a concept as stored` (S5 is
  the next free number after CR-101's S4; if CR-101 delivered another numbering, use the next
  free number in every place this specification says CORE-005 S5):
  - GIVEN a concept file in the bundle, whatever its frontmatter style, comments, line endings,
    encoding, or whether it has frontmatter or valid YAML at all
  - WHEN the user shows it
  - THEN the CLI writes the stored bytes to standard output, unchanged and with nothing added
    (no trust or staleness line), exits 0 and writes nothing to standard error, and the API
    result's `raw` holds the stored text of a UTF-8 file
- Add under `### Verification notes`, Criteria: `show` output equals the stored file byte for
  byte, including a file without frontmatter, with invalid YAML, with CRLF line endings, or not
  valid UTF-8.
- Leave the frontmatter `description` and the normative paragraph unchanged (they still
  describe `show` correctly: deterministic results, bundle not modified).

#### 5b. `requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-006.md`

On top of `trust-actor-forms`'s edits, if any:
- S2's THEN names `stale: true` as a `show` line. Replace "it is stale (W11, `stale: true`)"
  with "it is stale (W11 on validation, `stale: true` from `okf-schema trust`, `stale` true in
  the API result, `[STALE]` in `list`)". The rest of S2 does not change.
- Add to `scenarios:` and as a body section a scenario `S5` (or the next free number if
  `trust-actor-forms` added one; use that number in every marker below)
  `### Scenario S5: Print a concept's trust tier and staleness`:
  - GIVEN a concept in the bundle, with or without a `verified` field (a list or a bare
    mapping) and a `stale_after` value
  - WHEN the user runs `okf-schema trust` on it
  - THEN standard output is `trust: <tier>` with the tier derived from `verified` only
    (`unverified`, `machine-confirmed` or `human-reviewed`), followed by `stale: true` only when
    the concept is stale; the command exits 0 for every tier, including `unverified`, prints no
    score, and writes no file
- Add to `scenarios:` and as a body section, right after S5, a refusal scenario `S6` (the
  number after S5's; use it in every marker below)
  `### Scenario S6: Refuse to print the trust tier of a missing concept`:
  - GIVEN a concept path that names no file in the bundle, with or without `.md`
  - WHEN the user runs `okf-schema trust` on it
  - THEN the command writes `Error: Concept not found: ...` (the message `show` gives for it,
    as CR-101 delivers it) to standard error, prints no `trust:` line, exits 2 and writes no
    file
  A path leaving the bundle is not restated here: it is SwRS-OKFSCHEMA-CORE-010's refusal
  (section 5c).
- Normative paragraph and frontmatter `description`, word for word the same single SHALL
  statement, so that it covers printing the tier when a concept is inspected, as S1 already
  says ("validated or inspected"): "When OKF 0.2 metadata is validated or inspected, okf-schema
  SHALL derive its trust tier and staleness and enforce provenance, verification, lifecycle,
  resource, trust-tier, and staleness rules with actionable findings." If `trust-actor-forms`
  changed that statement, apply the same two additions ("or inspected", "derive its trust tier
  and staleness and") to its wording.
- Add `depends_on: [SwRS-OKFSCHEMA-CORE-010]` (authored field; the `trust` command resolves the
  concept under that rule). `okfreq lint` writes the "Depends on" group of the Links section.
- Add under `### Verification notes`, Method: "and CLI tests of the `trust` command"; Criteria:
  "`trust` prints exactly `trust: <tier>` and, when stale, `stale: true`, and changes no file;
  a missing concept is refused with exit 2".
- Leave the title and S1, S3, S4 unchanged.

#### 5c. `requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-010.md` (created by CR-101)

The `trust` command applies the same containment rule (it resolves through `show_bundle`), and a
SwRS states what the code does:
- Frontmatter `description` and the normative paragraph, word for word the same: "When a user
  shows a concept" becomes "When a user shows a concept or prints its trust tier"; the rest of
  CR-101's statement stays.
- S1, S2 and S3: "WHEN the user shows it" becomes "WHEN the user shows it or prints its trust
  tier".
- `### Verification notes`, Method: "public API and CLI tests of `show` and `trust`".
- CR-101's "Known issue" line (the other commands that still follow outside symlinks) does not
  name `trust`; this CR leaves it as is. It follows the inbox item `bundle-outside-symlinks`
  (see "Neighbour `bundle-outside-symlinks`"), which removes it.

#### 5d. Generated fields, navigation and log

- Run `okfreq update-coverage requirements` (CORE-006 then lists `src/okf_schema/cli.py` and
  `tests/test_cli_remaining.py`) and
  `okfreq lint requirements --prose --check-links --project-root .`. Never edit generated
  fields or Links sections by hand.
- In `requirements/tiers/log.md`, under the day's `## YYYY-MM-DD` heading (one heading per
  date, newest first; share it with the entries of CR-101, `trust-actor-forms` and CR 57 when
  they are the same day, keep all of them): CORE-005 gained S5 (show prints the stored file,
  nothing added, no validation, any encoding); CORE-006 gained S5 (the `trust` command) and
  S6 (its refusal of a missing concept), `depends_on` CORE-010 and a statement that covers
  inspection ("validated or inspected", deriving the trust tier and staleness), and S2 names
  `trust` instead of the removed `show` line; CORE-010 now
  covers `trust` too; the reason (`show` re-serialized the frontmatter and printed a `trust:`
  line inside the document; the trust tier moved to its own command); the verification results.
  No ticket named.

### 6. Human documentation

- `docs/source/reference/cli.md`, section `## okf-schema show` (as CR-101 leaves it): the
  description line becomes "Print a concept file exactly as stored." Add an "Output" paragraph:
  standard output is the file byte for byte (frontmatter style, comments, line endings,
  encoding, body); `show` does not parse or validate it, so a file without frontmatter, with
  invalid YAML or not valid UTF-8 is printed as is with exit 0 (use `okf-schema validate` to
  check it); nothing is added, in particular no trust tier or staleness line: use
  `okf-schema trust`. The Python API `show_bundle` returns `trust_tier`, `stale` and `raw` (and
  raises `UnicodeDecodeError` for a file that is not valid UTF-8). Keep CR-101's
  `CONCEPT_PATH`, errors, exit code and macOS limit text.
- `docs/source/reference/cli.md`, new section `## okf-schema trust`, right after
  `## okf-schema show` and before `## okf-schema index` (CR 57 edits that next section; see
  "Neighbour CR 57"), with the `---` separators the page uses:
  - "Print a concept's trust tier and staleness."; usage
    `okf-schema trust --path BUNDLE CONCEPT_PATH`; `CONCEPT_PATH` as for `show` (link to that
    section, no repeated rules).
  - Output: `trust: <tier>`, one of `unverified`, `machine-confirmed`, `human-reviewed`, derived
    from the concept's `verified` field only (a single mapping counts as one entry; link to W10
    in `validation-codes.md` for the actor forms, without restating them here, since
    `trust-actor-forms` owns them); then `stale: true` when `stale_after` has been reached
    (an instant with its offset, or a bare date from that day on); no line when it is absent or
    unparseable (`validate` reports W16). No score.
  - Exit codes: 0 for every tier, including `unverified`, and for a file without frontmatter or
    with invalid YAML (`trust: unverified`); 2 with `Error: ...` for a missing concept or a path
    leaving the bundle, as `show`. The command writes nothing.
  - One example per case: `trust: unverified`; `trust: human-reviewed` with `stale: true`.
- The "Exit codes" table of the page does not change.
- `docs/source/explanation/project-feature-coverage.md:31` (OKF 0.2 staleness row): replace
  "`tests/test_api.py` covers `stale` in `list`/`show`" with "`tests/test_api.py` covers
  `stale` in `list_bundle` and `show_bundle`; `tests/test_cli_remaining.py` covers the
  `stale: true` line of `okf-schema trust`". Add a row after it: "Trust tier of one concept
  (`okf-schema trust`)" | "SwRS-OKFSCHEMA-CORE-006 S5 and S6; `tests/test_cli_remaining.py` covers each
  tier, a bare `verified` mapping, staleness, refusals and that no file changes; the installed
  wheel runs it in `tests/test_acceptance_core.py`."
- `docs/source/tutorials/getting-started.md:89` ("Inspect the document and its frontmatter")
  and `docs/source/tutorials/knowledge-graph.md:94` show no output and stay true. Unchanged.
- `README.md`: its command example block (lines 180-197) shows neither `show` nor the other
  inspection commands beyond `list` and `backlinks`, and routes to the CLI reference, which
  documents `trust`. Unaffected.

### 7. Standalone agent skill (`skills/okf-schema/SKILL.md`)

- Line 135, the `show` row as CR-101 leaves it, becomes
  `` `show --path <bundle> <concept>` | Print a concept file exactly as stored (not reformatted,
  not validated, no trust line); `.md` is optional; paths and symlinks leaving the bundle are
  refused (exit 2) ``.
- New row right after it (before the `index` row CR 57 edits):
  `` `trust --path <bundle> <concept>` | Print `trust: <tier>` (`unverified`,
  `machine-confirmed`, `human-reviewed`, from `verified`) and `stale: true` once `stale_after`
  is reached; exit 0 for every tier; writes nothing ``.
- Line 45 "Bundle management via CLI and Python API: init, list, show, stats, index" becomes
  "init, list, show, trust, stats, index".
- No other skill or reference mentions the `show` command; the agent can run `trust` from the
  installed CLI with this row alone.

### 8. Other surfaces (checked, unaffected; give these reasons in the change summary)

- Scaffold guidance `src/okf_schema/data/`: no `show` or trust-tier command usage.
- Examples `examples/`: no example runs `show`; none needs `trust`.
- CI, `justfile`, packaging: unchanged (the new command ships in the existing console script).
  `CHANGELOG.md` is generated at release; do not edit.

### 9. Commit and release (Q10, replacing Q6)

- One `feat` commit, following `.github/guidelines/git-commit-message.guidelines.md`: no `!`, no
  `BREAKING CHANGE:` section; subject at most 71 characters, for example
  `feat(cli): print concepts as stored and add a trust command`. The body says what users gain:
  `show` prints the stored file (any encoding, nothing added); the trust tier and staleness move
  to `okf-schema trust`; `ConceptDetail` gains `raw`. An issue reference, if kept, is a project
  choice (for example a `Closes #58` trailer).
- The release is the minor 0.19.0, made by the project's commitizen release (`bump_map`:
  `^feat` gives MINOR) from this `feat` commit together with the `fix` commits of CR-101 and
  `trust-actor-forms`. The Driver does not bump the version.

## Out of scope

- Concept resolution, containment and error messages: CR-101.
- The trust tier derivation (actor forms, W10, their documentation): CR `trust-actor-forms`
  (Q12).
- A `--trust` option, a header or a stderr line on `show`; a listing of the trust tier of every
  concept of a bundle; a score (Q9).
- `list`, `validate`, `lint` and the other commands; `[STALE]` in `list` stays.
- The values of `ConceptDetail.frontmatter`, `body`, `trust_tier`, `stale`.
- `show_bundle` on a file that is not valid UTF-8: it keeps raising `UnicodeDecodeError` (Q11).
- A file inside the bundle that cannot be read (permissions): behaviour unchanged.

## Evidence

Tests follow `.github/guidelines/python-unittest.guidelines.md`; fixtures are written in
`tmp_path` with `write_bytes` where exact bytes matter. New `show` tests carry
`# @tests_req SwRS-OKFSCHEMA-CORE-005#S5` (CR-101's tests keep their `#S4`), new `trust` tests
`# @tests_req SwRS-OKFSCHEMA-CORE-006#S5` (the numbers section 5b settles), unless stated
otherwise.

API, `tests/test_api.py` (show_bundle section, next to CR-101's tests):
1. A file with flow-style frontmatter, a YAML comment, an unquoted datetime and a body:
   `detail.raw == path.read_bytes().decode("utf-8")`, and `frontmatter`/`body` are as before.
2. A CRLF file (`write_bytes(b"---\r\ntitle: T\r\n---\r\nBody\r\n")`): `raw` keeps `\r\n`;
   `frontmatter == {"title": "T"}` and `body` has no `\r`, as with today's `read_text`.
3. Invalid YAML frontmatter (for example `---\ntitle: [unclosed\n---\nBody\n`): no exception,
   `frontmatter == {}`, `raw` equals the stored text.
4. A file that is not valid UTF-8 (`write_bytes(b"---\ntitle: caf\xe9\n---\nBody\n")`):
   `pytest.raises(UnicodeDecodeError)` (Q11, the API keeps failing).
5. The existing `test_show_bundle_*` tests (trust tier, stale, no frontmatter) pass unchanged.
   Extend `test_show_bundle_concept_without_frontmatter` with an assertion on `raw`.

CLI `show`, `tests/test_cli_remaining.py` (`show` section), comparing `result.stdout_bytes`
with `path.read_bytes()`:
6. `concept-a.md` of `_make_bundle` (flow list `tags: [alpha, beta]`): exact equality; and
   `b"trust:"` not in the output.
7. A file with `verified:` (human actor) and a past `stale_after` (a file that holds neither
   `trust:` nor `stale:`): exact equality, and neither `b"trust:"` nor `b"stale: true"` is in
   the output.
8. No frontmatter (`# Title\n\nBody.\n`): exact equality, no `---` added, exit 0,
   `result.stderr == ""`.
9. Invalid YAML frontmatter: exact equality, exit 0, empty stderr.
10. CRLF file and a file without a final newline: exact equality (no `\r` added or removed, no
    newline appended).
11. The non-UTF-8 file of test 4: exact equality, exit 0, empty stderr, no exception
    (`result.exception is None`) (Q11).
12. Real process, to catch Windows text-mode translation that `CliRunner` cannot see: run
    `subprocess.run([sys.executable, "-c", "from okf_schema.cli import cli; cli()", "show",
    "--path", str(bundle), "lf.md"], capture_output=True)` on an LF file and assert
    `stdout == path.read_bytes()`. This runs on `windows-latest` and `macos-latest` in the
    `cross-platform` CI job and must pass there.
13. Existing tests that assert substrings of `show` output
    (`test_show_show_outputs_frontmatter_and_body`,
    `tests/test_integration.py::test_cli_integration_show_cli_output`, CR-101's tests) keep
    passing; tighten `test_show_show_outputs_frontmatter_and_body` to the exact-bytes assertion
    of test 6 or leave it, but do not weaken it.
14. `test_defensive_error_handling_show_exits_2_on_api_error` patches `okf_schema.cli.show_bundle`,
    which `show` no longer calls: retarget it to `okf_schema.cli._resolve_concept_file` (same
    `NotADirectoryError("boom")`, exit 2, `boom` in the output).

CLI `trust`, `tests/test_cli_remaining.py` (new `trust` section after `show`; the module
docstring lists `trust` among the commands). Each test asserts `result.output` exactly:
15. `concept-a.md` (no `verified`): `"trust: unverified\n"`, exit 0.
16. `verified:` list with `{by: "human:alice", at: "2026-11-01"}`: `"trust: human-reviewed\n"`.
17. `verified:` as a bare mapping `{by: "process:ci-lint", at: "2026-11-01"}` (a form both the
    current code and `trust-actor-forms` read as machine): `"trust: machine-confirmed\n"`.
18. A `verified` entry by `reference_agent/gemini-2.5-pro` (the `<producer>/<version>` form):
    the output is the tier `trust-actor-forms` delivers for it (`"trust: machine-confirmed\n"`
    per that CR's intent). This test asserts the stacked fix through the new command; it does
    not re-test the derivation rules.
19. A past `stale_after` (`2020-01-01`) with no `verified`: `"trust: unverified\nstale: true\n"`,
    exit 0. A past offset datetime (`2020-01-01T00:00:00Z`) gives the same.
20. A future `stale_after` (`2999-01-01`) and an unparseable one (`not-a-date`): no `stale:`
    line.
21. No frontmatter and invalid YAML frontmatter: `"trust: unverified\n"`, exit 0.
22. The extensionless name (`concept-a`) and CR-101's leading `/` form (`/concept-a`) give the
    same output as `concept-a.md`.
23. `missing.md` and `missing`: exit 2, `Error: Concept not found` on stderr, no `trust:` line
    on stdout, no traceback, and no file of the bundle changed
    (`# @tests_req SwRS-OKFSCHEMA-CORE-006#S6`, the refusal scenario of section 5b).
    `../outside.md` with the file present beside the bundle: exit 2, `Error: Concept path is outside the bundle`
    (`# @tests_req SwRS-OKFSCHEMA-CORE-010#S1`).
24. Writes nothing: in test 19, the bundle's file contents and modification times are identical
    before and after the run.
25. `test_defensive_error_handling_trust_exits_2_on_api_error`: patch `okf_schema.cli.show_bundle`
    with `NotADirectoryError("boom")`; exit 2, `boom` in the output.
26. `okf-schema --help` lists `trust`, and `okf-schema trust --help` shows the summary
    "Print a concept's trust tier and staleness." (reads the shipped command, not a copy).

Acceptance, `tests/test_acceptance_core.py::test_inspection_reports_matching_concepts_and_changes_no_file`
(`@accepts_req StRS-OKFSCHEMA-CORE-002#S3`, installed wheel, reading the shipped command):
27. After the existing `lint`, assert that the output of
    `inspect("show", "--path", str(bundle), "concepts/clock.md")` equals
    `(bundle / "concepts" / "clock.md").read_text(encoding="utf-8")` and has no `trust:` line.
    Keep CR-101's extensionless `inspect(... "concepts/clock")` assertion.
28. Add `trusted = inspect("trust", "--path", str(bundle), "concepts/clock")` and assert
    `trusted.splitlines() == ["trust: unverified"]` (the `_CLOCK` fixture has a `generated`
    field but neither `verified` nor `stale_after`). The snapshot check still
    proves nothing was written, now including `trust`. In
    `test_init_then_new_creates_a_valid_bundle_that_keeps_the_authored_concept` the
    `"title: Clock"` and `"The clock ticks."` assertions stay true.

Scenario steps (a real run, output kept as evidence), in a disposable folder, with
`uv run -- okf-schema ...` from the worktree:
- `okf-schema init my-knowledge-base`;
  `okf-schema new --path my-knowledge-base/bundle --name api/health-check --type "API Endpoint" --title "Health Check"`;
  `okf-schema show --path my-knowledge-base/bundle api/health-check` (CR-101's form): output
  identical to the file (compare with `cmp` or a byte diff), no `trust: unverified` line.
- `okf-schema trust --path my-knowledge-base/bundle api/health-check`: `trust: unverified`,
  exit 0.
- Edit the file to flow style with a comment (`links: [api/health-check.md]  # keep`), add
  `verified: {by: human:alice, at: 2026-11-25}` and `stale_after: 2020-01-01`, run
  `okf-schema lint --path my-knowledge-base/bundle`, then `show`: output identical to the file;
  then `trust`: `trust: human-reviewed` and `stale: true`, exit 0, and the file's hash is the
  same before and after `trust`.
- Write `broken.md` with `---\ntitle: [unclosed\n---\nBody\n`, a `plain.md` without frontmatter
  and a `latin1.md` holding a Latin-1 byte (`printf -- '---\ntitle: caf\xe9\n---\n'`) in the
  bundle; `show` each: exit 0, output identical to the file, empty stderr.

Requirement checks: after `okfreq update-coverage requirements`, CORE-005 S5 and CORE-006 S5
and S6 have `@tests_req` markers; CORE-006 lists `src/okf_schema/cli.py`; CORE-006's Links section has
the "Depends on" group naming CORE-010; `okfreq trace requirements --json` shows CORE-005,
CORE-006 and CORE-010 covered.

Gates: `okfreq update-coverage requirements --check`,
`okfreq validate requirements --prose --check-links --project-root .`,
`okfreq lint requirements --check --check-links --project-root .`, then `just preflight`. All
pass; review the generated diffs before reporting, as `AGENTS.md` asks.

No host and default matrix applies: nothing depends on the agent host or a configured value.
The one OS difference (Windows text-mode newline translation of `show`) is covered by test 12,
which the `cross-platform` job runs on Windows and macOS. The `trust` lines go through
`click.echo` like every other text command, so a Windows console ends them with `\r\n`, as
`show` did.

## Open questions

1. `okf-schema trust` on a concept file that is not valid UTF-8: `show_bundle` keeps raising
   `UnicodeDecodeError` (Q11), so `trust` ends in a traceback, as `show` did before this CR.
   This specification keeps that. Should `trust` instead report a plain `Error: <file> is not
   valid UTF-8` with exit 2?
