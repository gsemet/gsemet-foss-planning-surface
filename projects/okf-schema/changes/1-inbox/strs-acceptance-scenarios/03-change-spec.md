# okfreq: acceptance paths, declared scenarios, two StRS counters

Type: feat (okfreq, requirements, docs) · Requested 2026-11-23 by the markdown-okf-schema-studio
Griller from the Studio owner's grill ([request](intake/request.md), [intent](01-intent.md),
[answers](02-answers.md), Q1–Q46) · Forge-neutral (GitHub and GitLab) · One CR, one batch (Q10)
· Grilled enough 2026-11-23, destination `3-ready` (Q17) · Release `0.18.0`, not breaking (Q40).

A new `strs_test_coverage_mode`, `linked-swrs-and-acceptance-paths` (Q24), makes `okfreq`
measure that a StRS is proved by tests that walk its declared main paths, instead of counting
any direct link as a validation test. Requirements declare their main paths (StRS) or their
transition scenarios (SwRS) in one shared frontmatter field, `scenarios:`. Tests name one of
them with a `#S<n>` fragment. Three test markers say what a test is:

- `@tests_req SwRS-X#S<n>`: a SwRS test, as today, now per transition;
- `@simulates_req StRS-X#S<n>` (new): a StRS path walked on the **simulated** bench;
- `@accepts_req StRS-X#S<n>` (new): a StRS path walked on the **real** bench.

Each StRS gets two counters, "tested" (simulated) and "accepted" (real), and is covered when
its linked SwRS are covered and all its paths are accepted. The repository applies the mode to
itself, its examples and its documentation (Q21, Q35), and the documentation site explains the
possibilities and why (Q46).

## Goal, in the user's terms

The Studio counts 93 of its 94 live StRS as validated. A 1-in-6 sample of its 185 direct
`@tests_req StRS-...` markers
([audit](../../../../markdown-okf-schema-studio/changes/2-backlog/P2/strs-path-validation/experiments/02-audit-sample.md))
shows that only 13 of 31 walk a StRS main path. A marker is a link, not a proof. The owner
wants `okfreq` to:

1. let a requirement declare its paths or transitions with stable short ids (`S1`, `S2`, never
   reused) and a title, in a `scenarios:` frontmatter field that both tiers share, with no
   `kind`;
2. tell apart, by the marker, a test of a SwRS transition, a StRS path walked on the simulated
   bench and a StRS path accepted on the real bench;
3. report, per StRS, which fraction of its paths is tested and which is accepted;
4. tell an agent exactly how to declare `scenarios:` when a StRS has none (no migration
   command);
5. show all of this, and why, in the published documentation.

The Studio's own migration (declaring its `scenarios:`, moving its `@tests_req StRS-...`
markers to `@simulates_req` by script, writing its acceptance tests) is the Studio CR
`strs-path-validation`, outside this CR, which waits for this one.

## Starting point (code read on 2026-11-23)

The local clone `/Users/az02065/Projects/DevTools/okf-schema` is checked out on `dev/gsemet` at
`89b52ad` (0.16.0). The default branch `main` is at `8f56838` (`chore: version 0.17.0`), which
contains `feat(okfreq)!: keep requirement bundles native OKF v0.2 bundles`. **The Driver works
from the head of `main`.** Everything below was read on `refs/remotes/origin/main`; the spec
names functions, not line numbers.

`src/okf_schema/okfreq/core.py`:

- `STRS_TEST_COVERAGE_MODES = ("linked-swrs", "linked-swrs-and-validation-test")`,
  `STRS_TEST_COVERAGE_DESCRIPTIONS`, `_strs_test_coverage_mode` (refuses other values with
  `unsupported strs_test_coverage_mode: <mode>; expected one of: <list>`).
- `DEFAULT_CONFIG` (written by `okfreq init`) lists `markers: {implements: '@implements_req',
  tests: '@tests_req', id_pattern: ...}`; `load_config` fills the same defaults.
- `marker_scan(root)` builds one regex
  `^\s*(?:(?:#|//|/\*|\*|<!--)\s*)?(?P<marker>implements|tests)\s+(?P<identifier>id_pattern)`.
  It reads implementation markers only in `source_dirs` and test markers only in `test_dirs`,
  de-duplicates on (kind, ID, file), keeps no line number, and returns `implemented`, `tested`
  (leaf IDs), `validation_tests` (a test marker on a StRS), `missing_ids`, `non_leaf`,
  `duplicates`, `warnings`. **Because the ID pattern stops at `#`, `@tests_req SwRS-X#S1`
  already counts today as `@tests_req SwRS-X`: the suffix is silently ignored.**
- `validate_requirements` validates each requirement's frontmatter against its tier schema
  (`tiers/_schema/<tier>.schema.yaml` composed with `base.schema.yaml`) through
  `Draft202012Validator(...).iter_errors(data)` and reports `<file>: <message>`. This is the
  **only place where a JSON Schema is enforced at run time**. It does not scan markers. Its
  findings are errors (no prefix), `W…` warnings (`W001`/`W002` only with `--prose`) and `I…`
  infos. `okfreq validate` and `okfreq lint` fail on errors.
- `update_coverage` writes the generated `implemented_in_files`/`tested_in_files` on SwRS from
  `marker_scan` and removes them from StRS. The scaffolded `swrs.schema.yaml` declares them with
  `x-okf-link.basename_marker: '@implements_req'` / `'@tests_req'`: generated fields are how a
  marker reaches a tier schema today.
- `report(root)` builds each StRS's `stakeholder_test_coverage` (`status`, `mode`,
  `linked_swrs`, `validation_tests`), the aggregate, totals, scopes, and
  `"format_version": 1`. `report_schema()` declares `const: 1`; it is **only written**
  (`write_report_schema`, by `okfreq generate-report`), never checked at run time.
  `write_markdown_report` renders "By stakeholder requirement" (`| Scope | Tier | ID | Name |
  Tests |`) and "By software requirement" (`| Scope | Tier | ID | Name | Source | Tests |`).
- `initialize_bundle`'s `schema_text("base" | "strs" | "swrs")` generates the three schemas;
  `okfreq init` never replaces existing ones. Every shipped schema keeps
  `additionalProperties: true`, so nothing refuses `scenarios:` today.
- `create_requirement` writes the body from `ears_body`: `_SWRS_BODY` has two
  `### Scenario: <…>` headings; `_STRS_BODY` has no path section.

`src/okf_schema/okfreq/cli.py`: `validate`, `lint`, `trace` (summary
`implemented: N; tested: N; missing IDs: N`), `update-coverage`, `generate-report`, `new`.

This repository: `requirements/config.yml` uses `linked-swrs-and-validation-test`;
`tests/test_project_contract.py::test_live_requirements_preserve_complete_real_evidence`
asserts that mode, zero findings and full stakeholder coverage. It has 5 StRS (all
`proposed`, none with a `### Main paths` section) and 23 SwRS, every one with `### Scenario:`
headings. Six real direct StRS markers exist in `tests/`:
`tests/test_examples.py` (`StRS-OKFSCHEMA-OKFREQ-001`), `tests/test_file_links.py`
(`StRS-OKFSCHEMA-CORE-003`), `tests/test_integration.py` (`CORE-002`, `CORE-001`,
`OKFKB-001`) and `tests/test_okfreq.py` (`OKFREQ-001`). `tests/test_skill_resources.py`
already has a real-bench pattern:
`test_installed_wheel_commands_install_complete_families_without_source_checkout` builds the
wheel (`uv build --offline --wheel`), installs it in an isolated venv and runs the installed
console scripts as subprocesses with no source checkout on the path.

`just docs` runs `just changelog` then `sphinx-build -W -b html docs/source docs/_build/html`
(warnings fail). The changelog is generated by `cz` from commit subjects.

## Decisions carried (from `02-answers.md`)

| Q | Decision | Where |
|---|---|---|
| Q1 | A new mode value activates the feature; without it, `scenarios:` and the new markers are accepted but nothing is required or counted. | Rule 1 |
| Q2 | No bench configuration: the marker tells the bench. Real bench = `@accepts_req`, simulated bench = `@simulates_req` (Q44); the two may be different tests. | Rules 3, 5 |
| Q3 | One fraction of paths per counter; the StRS is "tested"/"accepted" when its fraction is complete. | Rule 5 |
| Q4 | Superseded by Q19, then for `@tests_req` on a StRS by Q45. No `W004`. | Rule 4 |
| Q5 | Error for an unknown `#S<n>`; warning for a live StRS with no declared path. | Rule 6 |
| Q6 | A path is "tested" by a simulated-bench marker with `#S<n>`. The verb is `@simulates_req` (Q44), not `@tests_req`. | Rules 4, 5 |
| Q7 | A SwRS with declared transitions is covered only when each has a `@tests_req SwRS-X#S<n>`. | Rules 4, 5 |
| Q8 | No migration subcommand; okfreq's message tells agents how to declare `scenarios:`. | Rule 6 |
| Q9 | On an approved StRS: frontmatter-only edit, body intact, logged in `tiers/log.md`. | Rule 7 |
| Q10 | One CR, one batch. | Header |
| Q11 | New mode only, StRS and SwRS alike; once declared, each scenario must be covered. Refined by Q14/Q19. | Rules 1, 4, 5 |
| Q12 | JSON and Markdown, version incremented; per StRS `paths: {total, tested, accepted}` and two booleans; per SwRS tested and missing transitions; two Markdown columns. | Rule 8 |
| Q13 | Detailed agent message: StRS named, headings quoted, `scenarios:` block to paste, doc link. | Rule 6 |
| Q14 | When `scenarios:` is declared, every marker targeting it must carry `#S<n>`. For `@tests_req` on a StRS, replaced by Q45. | Rule 4 |
| Q15 | A missing fragment there is an error: `okfreq validate` fails, the marker does not count. | Rules 4, 6 |
| Q16 | All six surfaces of `AGENTS.md` plus `docs/source/explanation/project-feature-coverage.md`. | Surfaces |
| Q17 | Grilled enough; next batch. | Header |
| Q18 | In the new mode a StRS is covered by the linked-SwRS rule plus "accepted". | Rule 5 |
| Q19 | Same for StRS and SwRS: `scenarios:` declared → a fragmentless marker is an error; not declared → fragmentless markers count. Replaces Q4 and the "0/0" question. W003 stays. | Rules 4, 5 |
| Q20 | `@accepts_req` on a SwRS is an error, enforced in the JSON Schema. | Rule 4, Rule 6 |
| Q21 | okf-schema applies the mode to its own requirements. | Surface 5 |
| Q24 | Mode name `linked-swrs-and-acceptance-paths`. | Rule 1 |
| Q25 | Outside the new mode: silent for a malformed `scenarios:` or unknown fragment, apart from what the bundle's own JSON Schema refuses. | Rule 1 |
| Q26 | "Ids never reused": documentation only; okfreq checks nothing. | Rule 2 |
| Q27 | `markers.accepts`, configurable, written by `okfreq init`. | Rule 3 |
| Q28 | `#` glued to the ID; only `S<n>` is a fragment; any other suffix is ignored as today; an unknown `S<n>` is an error. | Rule 3 |
| Q29 | JSON keys `accepted`, `scenario_markers` (`trace --json`), `transitions` (SwRS record). | Rules 3, 8 |
| Q30 | `tested_in_files` of a SwRS with transitions lists only files with a counting marker. | Rule 5 |
| Q31 | `W003` only; errors carry no code. | Rule 6 |
| Q32 | W003 link `https://okf-schema.readthedocs.io/en/stable/reference/okfreq-frontmatter.html#okfreq-declared-scenarios`. | Rule 6, surface 2 |
| Q33 | Headings read for W003: every heading under `### Main paths` up to the next `###` (or the generated links block), plus `### Scenario…`; title after `Path <n>:` / `Scenario:`, else the whole heading. | Rule 6 |
| Q34 | Live = every lifecycle except `deprecated` and `superseded`. | Rule 6 |
| Q35 | No warning for a SwRS with `### Scenario` headings and no `scenarios:`; instead the CR migrates the project, its examples and its docs correctly. | Rule 6, surfaces 2, 5, 6 |
| Q36 | Approval for a `scenarios:`-only edit: the owner decides; without new approval `approved_by`/`approved_at` stay and the log names the agreement. | Rule 7 |
| Q37 | `format_version` 2 in every mode. | Rule 8 |
| Q38 | Superseded by Q42. | — |
| Q39 | Path totals in the aggregate, one Markdown summary line, a "Missing transitions" column in the SwRS table. | Rule 8 |
| Q40 | `0.18.0`, `feat(okfreq): …`, not breaking. | Surface 1, Evidence |
| Q41 | `okfreq new` pre-fills `scenarios:` from the template headings; the StRS case settled here. | Rule 9 |
| Q42 | Per StRS `acceptance_tests` (`@accepts_req` files); `validation_tests` kept for backward compatibility. | Rule 8 |
| Q43 | Per StRS `simulated_tests` (simulated-bench files). | Rule 8 |
| Q44 | New marker `@simulates_req` (`markers.simulates`, written by `okfreq init`), simulated bench for a StRS path, paired with `@accepts_req`. `@tests_req` stays the SwRS marker. | Rules 3, 4 |
| Q45 | `@tests_req StRS-X`: unchanged outside the new mode; an error naming `@simulates_req` in the new mode. The repository's 6 markers move to `@simulates_req` by script; the Studio's too, outside this CR. | Rules 4, 6, surface 5 |
| Q46 | Document this part well; the built documentation site shows the possibilities and why. | Surface 2 |

The request's point 3 named benches "in the project's config"; Q2 replaces that. The request's
point 2 used `@accepts_req` for both benches; Q2 and Q44 give each bench its own verb. The
request's point 5 (migration help) became an okfreq message (Q8, Q13).

## The rules

"The new mode" means `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`. "The old
modes" are `linked-swrs` (the shipped default) and `linked-swrs-and-validation-test`.

### Rule 1: activation (Q1, Q11, Q24, Q25)

- `STRS_TEST_COVERAGE_MODES` gains `linked-swrs-and-acceptance-paths`;
  `STRS_TEST_COVERAGE_DESCRIPTIONS` gains: "An StRS is considered as covered when it is linked
  to at least one SwRS, every linked SwRS is test-covered (one test per declared transition),
  and every declared main path has an acceptance test on the real bench. Paths walked on the
  simulated bench are reported as tested." `load_config` and `_strs_test_coverage_mode` accept
  it; the refusal lists the three modes.
- In the old modes okfreq accepts `scenarios:` and the two new markers and requires and counts
  nothing new. Coverage, generated fields and findings stay exactly as today: `@simulates_req`
  and `@accepts_req` count toward nothing, `@tests_req StRS-X` (with or without suffix) is still
  the validation test of `linked-swrs-and-validation-test`, and a suffix on any marker is
  ignored, as today. The only refusals are those of the bundle's own JSON Schema on the
  frontmatter (Rule 2's schema property) (Q25). `okfreq new` is unchanged in the old modes
  (Rule 9).
- Rules 4 to 6, 8 (new fields) and 9 apply in the new mode only. `report()`'s
  `format_version` 2 applies in every mode (Q37).

### Rule 2: the `scenarios:` frontmatter field

- One authored field, shared by both tiers: on a StRS its main paths, on a SwRS its transition
  scenarios. The tier says which, so an entry has no `kind`.
- Shape: a non-empty list of mappings, each with exactly `id` (`S<n>`) and `title`:

  ```yaml
  scenarios:
    - id: S1
      title: Wait for a render
    - id: S2
      title: The source is gone
  ```

- An id is never reused, even after its scenario is removed. This is guidance in the
  documentation, skills and guideline only; okfreq checks nothing (Q26).
- Declared in the **base** schema, both in `schema_text("base")` (new bundles) and in
  `requirements/tiers/_schema/base.schema.yaml` (this repository):

  ```yaml
  scenarios:
    type: array
    minItems: 1
    description: Authored main paths (StRS) or transition scenarios (SwRS). Each id S<n>
      is stable and never reused, even after its scenario is removed. Test markers name
      one with a #S<n> fragment.
    items:
      type: object
      required: [id, title]
      additionalProperties: false
      properties:
        id: {type: string, pattern: '^S[1-9][0-9]*$'}
        title: {type: string, minLength: 1}
  ```

  The item's `additionalProperties: false` is what refuses `kind`. No `x-okf-link`. The
  top-level `additionalProperties: true` stays. Because this is the bundle's JSON Schema, it
  applies in every mode (Q25).
- A bundle created before this change has no such property and still accepts any
  `scenarios:`. In the new mode, okfreq also checks in code what the counters depend on: a
  list of mappings, `id` matching `S[1-9][0-9]*`, ids unique, non-empty `title`. Error:
  `<file>: scenarios: <problem> (each entry is {id: S<n>, title: <text>}, ids unique)`.
  Duplicate ids are checked in code in every bundle, since JSON Schema cannot express them.
- `update_coverage` preserves the field (authored, never generated); `_render_frontmatter`
  already keeps unknown keys. A test proves it.

### Rule 3: markers and the fragment (Q2, Q27, Q28, Q29, Q44)

- Four marker kinds; three are test markers, read only in `test_dirs` (skipped in
  `source_dirs`, as a test marker is today):

  | Config key | Default keyword | Meaning |
  |---|---|---|
  | `markers.implements` | `@implements_req` | implementation of a SwRS (unchanged; source_dirs) |
  | `markers.tests` | `@tests_req` | test of a SwRS, or of one of its transitions |
  | `markers.simulates` | `@simulates_req` | a StRS path walked on the simulated bench (Q44) |
  | `markers.accepts` | `@accepts_req` | a StRS path accepted on the real bench (Q27) |

- `DEFAULT_CONFIG` lists `simulates` and `accepts`, so `okfreq init` writes them.
  `load_config` defaults both even when an existing `config.yml` lists only `implements` and
  `tests`. Two kinds configured with the same keyword is a `RequirementError`
  (`markers.<a> and markers.<b> use the same keyword <kw>`), since the kind would be ambiguous.
- The marker regex of `marker_scan` becomes:

  ```text
  ^\s*(?:(?:#|//|/\*|\*|<!--)\s*)?(?P<marker>implements|tests|simulates|accepts)\s+
  (?P<identifier>id_pattern)(?:#(?P<fragment>S[0-9]+)(?![A-Za-z0-9_-]))?
  ```

  (each keyword `re.escape`d). This settles Q28: the fragment is `#` glued to the ID followed
  by `S` and digits, ending at a non-identifier character. Any other suffix (`#path1`, `#s1`,
  `#S1a`, `#`) is not a fragment: it is ignored as today and the marker is read **without
  fragment**. `#S0` or `#S01` is a fragment that can name no declared id, so it is the
  unknown-fragment error in the new mode. The fragment is not read on `@implements_req`
  (unchanged). The documentation says a custom `id_pattern` must not admit `#`.
- `marker_scan` keeps every existing key with its meaning (old modes and `report()` keep their
  results) and adds:
  - `simulated`: ID → files of `@simulates_req` markers;
  - `accepted`: ID → files of `@accepts_req` markers (Q29);
  - `scenario_markers`: one entry per (kind, ID, fragment, file), with the first line:
    `{"marker": "tests" | "simulates" | "accepts", "id", "fragment": "S1" | null, "file",
    "line"}` (Q29). Messages need the line.
  A `@tests_req` on a StRS still goes to `validation_tests`; an unknown ID of any test kind goes
  to `missing_ids`, as today. The `marker_scan` doctest lists the new keys.
- `okfreq trace` prints `implemented: N; tested: N; simulated: N; accepted: N; missing IDs: N`;
  `--json` prints the whole scan.

### Rule 4: what each marker does

Old modes (Rule 1): exactly today's behavior; the new kinds count toward nothing; no new
finding.

New mode, by target tier and whether the target declares `scenarios:`. "Fragmentless" includes
a marker whose suffix is not `S<n>` (Rule 3).

| Marker | Target declares `scenarios:` | Target declares none |
|---|---|---|
| `@simulates_req StRS-X#S<n>`, `S<n>` declared | path `S<n>` **tested** | — |
| `@accepts_req StRS-X#S<n>`, `S<n>` declared | path `S<n>` **accepted** | — |
| `@simulates_req` / `@accepts_req StRS-X#S<n>`, `S<n>` not declared | **error**, does not count (Q5, Q28) | **error**, does not count (Q28) |
| `@simulates_req StRS-X` fragmentless | **error**, does not count (Q19) | counts: StRS **tested** (Q19, Q44) |
| `@accepts_req StRS-X` fragmentless | **error**, does not count (Q19) | counts: StRS **accepted** (Q19) |
| `@tests_req StRS-X`, with or without fragment | **error naming `@simulates_req`**, does not count (Q45) | same (Q45) |
| `@tests_req SwRS-X#S<n>`, `S<n>` declared | transition `S<n>` tested (Q7) | — |
| `@tests_req SwRS-X#S<n>`, `S<n>` not declared | **error**, does not count (Q5) | **error**, does not count (Q28) |
| `@tests_req SwRS-X` fragmentless | **error**, does not count (Q14, Q15, Q19) | covers the whole SwRS, as today (Q19) |
| `@accepts_req SwRS-X`, any suffix | **error**, from the SwRS schema (Q20, below) | same |
| `@simulates_req SwRS-X`, any suffix | **error**, from the SwRS schema (open question 1) | same |
| `@implements_req SwRS-X` | unchanged | unchanged |

**How Q20 is "in the JSON Schema".** The code enforces a JSON Schema at run time in one place
only, `validate_requirements`, on a requirement's frontmatter; `report_schema()` is never
checked. A marker reaches a tier schema only as a marker-derived frontmatter property, the way
`tested_in_files` carries `@tests_req` files and is declared in `swrs.schema.yaml` with
`x-okf-link.basename_marker: '@tests_req'`. So:

- Two marker-derived properties: `accepted_in_files` (files of `@accepts_req` markers that
  target the requirement) and `simulated_in_files` (files of `@simulates_req` markers).
- `strs.schema.yaml` (scaffold `schema_text("strs")` and `requirements/tiers/_schema/`)
  declares both as arrays of project-relative links (`x-okf-link` with `basename_marker:
  '@accepts_req'` / `'@simulates_req'`, `id_marker: id`, `show_line_number: true`) whose
  description says they are derived from markers by `okfreq validate` in the new mode and never
  written.
- `swrs.schema.yaml` (both copies) refuses them:

  ```yaml
  accepted_in_files:
    type: array
    maxItems: 0
    description: Never present. @accepts_req and @simulates_req name a StRS main path;
      mark a SwRS test with @tests_req <SwRS-ID>#S<n>.
  simulated_in_files: {...same...}
  ```

- In the new mode, `validate_requirements` validates each requirement's frontmatter **merged
  with its non-empty marker-derived properties** (from `marker_scan`) against its tier schema.
  An error on one of these properties is reported per marker with the schema's own
  `description`: `<test file>:<line>: @accepts_req SwRS-X: Never present. @accepts_req and
  @simulates_req name a StRS main path; …` (the configured keyword is used). The rule's text
  and its tier live in the schema; a project could relax it in its own schema.
- Nothing writes these properties: `update_coverage` does not generate them and keeps
  removing coverage file fields from StRS. A frontmatter that authors one is an error in the new
  mode (`<file>: accepted_in_files is derived from markers; do not author it`).
- Outside the new mode no merge happens, so `@accepts_req SwRS-X` is accepted and counts
  nothing (Q1, Q25).
- A bundle whose `swrs.schema.yaml` predates this change does not declare the property. What
  okfreq does then is open question 2.

### Rule 5: counters and coverage, in the new mode (Q2, Q3, Q7, Q11, Q18, Q19, Q30)

- **StRS that declares `scenarios:`**: `total` = declared paths; `tested` = declared paths with
  at least one counting `@simulates_req StRS-X#S<n>`; `accepted` = declared paths with at least
  one counting `@accepts_req StRS-X#S<n>`. **Tested** = `tested == total`; **accepted** =
  `accepted == total` (Q3).
- **StRS that declares none**: `paths` is `{total: 0, tested: 0, accepted: 0}`; **tested** is
  true when at least one fragmentless `@simulates_req StRS-X` counts, **accepted** when at least
  one fragmentless `@accepts_req StRS-X` counts (Q19). W003 still asks for paths (Rule 6).
- **StRS `status` `covered`** = linked-SwRS rule (at least one linked SwRS, each test-covered as
  below) **and accepted** (Q18). "Tested" is reported beside it and does not change the status.
  This drives the aggregate `stakeholder_test_coverage.covered` and the Markdown line.
- **SwRS** (leaf, no `annotation_exemption`): with declared transitions, test-covered only when
  every declared `S<n>` has a counting `@tests_req SwRS-X#S<n>` (Q7); without, test-covered by
  any fragmentless `@tests_req SwRS-X`, as today. This status drives `tests.status`,
  `totals.tested`, the scopes' `tested`, `marker_coverage.missing_tests` and the
  `linked_swrs[].status` of its StRS. Source coverage is unchanged.
- `update_coverage`: for a SwRS that declares transitions, `tested_in_files` lists only files
  with a counting `@tests_req SwRS-X#S<n>` (Q30). Otherwise unchanged. StRS still carries no
  file fields.

### Rule 6: findings and messages (Q5, Q8, Q13, Q15, Q31–Q35, Q45)

In the new mode `validate_requirements` calls `marker_scan` (it does not today), so
`okfreq validate` and `okfreq lint` fail on these errors (Q15), `okfreq status` counts them, and
`report()` lists each in the `diagnostics.errors` of the requirement whose ID it contains.
Errors carry no code; the one warning is `W003` (Q31). Warnings print with or without
`--prose` and never change the exit code. Messages use the configured keywords.

- **Fragment missing** (Q19): `<file>:<line>: @tests_req SwRS-X has no scenario fragment;
  SwRS-X declares scenarios S1, S2: write @tests_req SwRS-X#S<n> (this marker does not
  count)`. Same for `@simulates_req`/`@accepts_req` on a StRS that declares paths.
- **Unknown fragment** (Q5, Q28): `<file>:<line>: @accepts_req StRS-X#S4 names no declared
  scenario of StRS-X (declared: S1, S2)`; when none is declared the message ends `(StRS-X
  declares no scenarios:)`.
- **`@tests_req` on a StRS** (Q45): `<file>:<line>: @tests_req StRS-X is not a StRS marker in
  mode linked-swrs-and-acceptance-paths: write @simulates_req StRS-X#S<n> for a path walked on
  the simulated bench, or @accepts_req StRS-X#S<n> on the real bench (this marker does not
  count)`. When StRS-X declares no `scenarios:`, the suggestion is without `#S<n>`.
- **`@accepts_req`/`@simulates_req` on a SwRS** (Q20): Rule 4's schema-driven error.
- **Malformed `scenarios:`**: Rule 2.
- **`W003`, live StRS with no `scenarios:`** (Q5, Q8, Q13, Q32–Q34). Live = any lifecycle but
  `deprecated` and `superseded` (`draft` included). One finding per StRS, addressed to an
  agent. It:
  1. names the StRS and its file;
  2. quotes the headings found in the body (Q33): every heading under `### Main paths` up to
     the next `###` heading or the generated links block (`<!-- okf:links:start -->`), plus
     every `### Scenario…` heading; or says none was found;
  3. gives the `scenarios:` block to paste, one entry per heading in order, `S1`, `S2`…, each
     title the text after `Path <n>:` / `Scenario:`, else the whole heading text; with no
     heading, one placeholder entry `- id: S1` / `  title: <main path title>`;
  4. says to edit the frontmatter only, and on an approved StRS to log the change in the
     bundle's `tiers/log.md` (Rule 7);
  5. ends with
     `https://okf-schema.readthedocs.io/en/stable/reference/okfreq-frontmatter.html#okfreq-declared-scenarios`.

  The heading reader is one helper (`_scenario_headings(text)`), shared with Rule 9.
- **No finding** for a SwRS without `scenarios:`, even with `### Scenario` headings (Q35). No
  `W004` (Q19, Q31).

### Rule 7: approved requirements (Q9, Q36)

Declaring `scenarios:` on an approved requirement is a frontmatter-only edit: the body stays
exactly as it was, and the change is logged in the bundle's `tiers/log.md`. The project's owner
decides whether this metadata change needs a new approval; without a new approval,
`approved_by`/`approved_at` stay unchanged and the log entry names the agreement (Q36). This is
guidance (guideline, skills, docs, W003 message), not a check: `_approval_findings` is
unchanged. A test proves an approved StRS that gains only `scenarios:` still validates. The
Studio's owner has already agreed for the Studio.

### Rule 8: the report (Q12, Q29, Q37, Q39, Q42, Q43)

- `"format_version": 2` in `report()` and `"const": 2` in `report_schema()`, in every mode
  (Q37). The mode enums follow `STRS_TEST_COVERAGE_MODES`. Every new property is optional in the
  schema, so old-mode reports keep their shape apart from the version.
- New mode, per StRS, `stakeholder_test_coverage` gains:

  ```json
  "paths": {"total": 3, "tested": 2, "accepted": 1},
  "tested": false,
  "accepted": false,
  "simulated_tests": {"status": "defined", "files": ["tests/test_flow.py"], "count": 1},
  "acceptance_tests": {"status": "defined", "files": ["tests/test_bench.py"], "count": 1}
  ```

  `simulated_tests` / `acceptance_tests` list the files of the **counting** `@simulates_req` /
  `@accepts_req` markers on the StRS (Q42, Q43), shaped like `validation_tests` (`status`
  `defined`/`missing`). `validation_tests` stays, required, for backward compatibility (Q42);
  its content in the new mode is open question 3. The StRS record's `tests.files`/`count` keep
  following `validation_tests`, as the code does today.
- New mode, per SwRS that declares transitions: `"transitions": {"tested": ["S1"], "missing":
  ["S2"]}` (Q29).
- New mode, aggregate `stakeholder_test_coverage` gains `"paths": {"total", "tested",
  "accepted"}`, the sums over StRS (Q39). `coverage_definition.tests` says "every declared
  transition has a test marker with its fragment, or at least one test marker when none is
  declared".
- `report_schema()`: `$defs.stakeholder_requirement_coverage` declares `paths`, `tested`,
  `accepted`, `simulated_tests`, `acceptance_tests`; `$defs.requirement` declares
  `transitions`; the aggregate declares `paths`.
- `write_markdown_report`, new mode only:
  - Summary gains `- StRS paths: tested <t>/<n>, accepted <a>/<n>` (Q39);
  - "By stakeholder requirement" gains `Tested` and `Accepted` columns: `2/3`, with ✅ when
    complete; for a StRS without paths, `✅ no paths` / `❌ no paths` from the booleans;
  - "By software requirement" gains `Missing transitions`: `S2, S3`, or `—`;
  - the note below the StRS table uses the new description.
  In the old modes the Markdown is unchanged.

### Rule 9: `okfreq new` pre-fills `scenarios:` (Q41)

In the new mode, `create_requirement` (`okfreq new`) pre-fills `scenarios:` from the headings of
the body it writes, read with `_scenario_headings` (Rule 6), so the frontmatter and body start
in step:

- **SwRS**: `_SWRS_BODY` is unchanged; its two headings give
  `[{id: S1, title: <nominal behavior>}, {id: S2, title: <boundary or failure behavior>}]`.
- **StRS**: in the new mode, `ears_body` adds to the StRS body, after "Normative behavior", a
  section

  ```markdown
  ### Main paths

  #### Path 1: <main path title>

  1. <first step the stakeholder observes>
  2. <next step, up to the observable outcome>
  ```

  and `scenarios:` gets `[{id: S1, title: <main path title>}]`. The author adds `#### Path 2…`
  headings and entries as needed.
- The placeholders are bracketed like every template placeholder, so `body_is_unfilled` and
  `W002` keep flagging an unfilled body.
- In the old modes `okfreq new` writes exactly what it writes today, so their output, the
  tests that pin it and old-mode projects stay unchanged (Rule 1).

## What changes, by surface (Q16)

`AGENTS.md` names six surfaces, all changed here, plus the feature map. The PR summary says, per
surface, what changed (`.github/guidelines/product-maintenance.guidelines.md`, step 3).

### 1. Runtime: `src/okf_schema/`

- `okfreq/core.py`: `STRS_TEST_COVERAGE_MODES`, `STRS_TEST_COVERAGE_DESCRIPTIONS`,
  `DEFAULT_CONFIG`, `load_config`, `_strs_test_coverage_mode`, `initialize_bundle`/`schema_text`
  (base `scenarios`; strs/swrs marker-derived properties), `marker_scan` (Rule 3),
  `validate_requirements` (Rules 2, 4, 6), `update_coverage` (Rule 5), `report`,
  `report_schema`, `write_markdown_report` (Rule 8), `ears_body`/`create_requirement` (Rule 9).
  New private helpers shared by validation, coverage and report, e.g. `_declared_scenarios`,
  `_scenario_headings`, `_scenario_findings`, `_scenario_coverage`. Public functions get
  Google-style docstrings with `.. versionchanged:: 0.18.0`
  (`.github/guidelines/python-module-documentation.guidelines.md`) and doctests still pass.
- `okfreq/cli.py`: `trace` summary (Rule 3); help and docstrings of `validate`, `lint`, `new`,
  `generate-report` mention the new mode.
- Put real `@implements_req` markers on the new code for the new SwRS (surface 5).

### 2. Human documentation: `docs/source/`, `README.md` (Q46)

The built site must show the possibilities and why. Pages to add or change:

- **New explanation page** `docs/source/explanation/okfreq-acceptance-paths.md`, "Why okfreq
  measures acceptance paths", added to the toctree of `docs/source/explanation/index.md` after
  `okfreq-coverage-boundaries`. It explains, project-neutrally:
  - why a direct StRS marker is a link, not a proof (a test that photographs one state or
    repeats one SwRS transition does not walk a stakeholder path);
  - the two benches: simulated (in-process, faked or stubbed environment) and real (the
    shipped product on its real host), and why each answers a different question;
  - the two counters, "tested" and "accepted", and why coverage needs "accepted" (Q18);
  - why a fragment: a marker must say which path it walks, so a fraction can be computed;
  - why declaring `scenarios:` makes fragments mandatory: once paths exist, a fragmentless
    marker would claim every path at once (Q14, Q19), whereas without declared paths it is the
    only honest link;
  - why one verb per bench (`@simulates_req`, `@accepts_req`) instead of a bench setting: the
    test itself states where it runs, no configuration can drift (Q2, Q44), and why
    `@tests_req` stays the SwRS verb and is refused on a StRS in the new mode (Q45);
  - that this is still linkage, not execution: `execution_evidence` stays `not_collected`;
  - how to choose a mode, with a link to the comparison below.
- **New reference page** `docs/source/reference/okfreq-acceptance-paths.md`, "Acceptance paths
  and scenario markers", added to the toctree of `docs/source/reference/index.md` after
  `okfreq-configuration`. It holds:
  - the **mode comparison**: the three modes, what each requires for a SwRS and for a StRS,
    and what each does with `@tests_req`/`@simulates_req`/`@accepts_req` on a StRS;
  - the **combination table**: every marker (`@implements_req`, `@tests_req`,
    `@simulates_req`, `@accepts_req`) × tier (StRS, SwRS) × `scenarios:` declared or not ×
    fragment (none, declared `S<n>`, undeclared `S<n>`, other suffix) × mode (old modes, new
    mode) → result (counts as …, error, ignored). It reproduces Rules 1 and 4 completely;
  - the fragment syntax (Rule 3) and the four marker keys;
  - **worked examples**, each with the frontmatter, the test markers, and the resulting JSON
    excerpt and Markdown row:
    1. a StRS with three paths, tested 2/3 and accepted 1/3 (not covered; both columns shown);
    2. a SwRS with transitions S1, S2 where only S1 has a test (missing S2, SwRS not
       covered, its StRS not covered);
    3. a StRS without `scenarios:`: a fragmentless `@simulates_req` and `@accepts_req` count,
       `W003` printed with its block;
  - the findings (each error and `W003`) with their messages, and how to fix each.
  Each example's blocks carry a `:caption:` so a test can read them (Evidence).
- `docs/source/reference/okfreq-frontmatter.md`: a "Declared scenarios" section with the label
  `(okfreq-declared-scenarios)=` (W003 target, Q32): the field, its shape, ids never reused
  (Q26), StRS vs SwRS meaning, declaring it from `### Main paths` / `### Scenario` headings,
  Rule 7, and a link to the reference page. "Marker fields" gains `@simulates_req`,
  `@accepts_req` and `#S<n>`; its paragraph on direct StRS validation tests names the modes.
  The tier-body examples show a StRS `### Main paths` section.
- `docs/source/reference/okfreq-configuration.md`: the `strs_test_coverage_mode` row and the
  "StRS test-coverage modes" section gain the new mode (link to the reference page); the
  `markers` row and YAML example gain `simulates` and `accepts`, and the `id_pattern` note.
- `docs/source/reference/okfreq-cli.md`: `validate` (new errors, `W003`), `trace` (counts,
  `scenario_markers`), `new` (pre-filled `scenarios:`), `generate-report` (new fields,
  columns, `format_version` 2).
- `docs/source/explanation/okfreq-coverage-boundaries.md`: the modes table gains a row and
  links to the new explanation page.
- `docs/source/tutorials/okfreq-traceability.md` (near "If the project needs a direct
  stakeholder validation-test definition…") and
  `docs/source/how-to/okfreq-build-requirement-base.md` (mode choice): one short paragraph each,
  linking to the new pages. `test_tutorial_okfreq.py` keeps passing.
- `docs/source/explanation/project-feature-coverage.md` (Q16): the "Stakeholder validation
  tests" row becomes "Acceptance paths": this project uses the new mode, how its acceptance
  tests run on the installed wheel, which tests simulate, and the showcase step.
- `README.md`: route to the new pages only if it lists okfreq coverage modes; otherwise the PR
  says it is unaffected and why.

### 3. Standalone agent skills: `skills/`

Each skill must work without this repository (`tests/test_skill_resources.py`).

- `skills/okfreq/SKILL.md` (the "Leaf requirements connect to evidence" step, which today says
  a direct `@tests_req <StRS-ID>` defines a validation test, and the mode note) and
  `skills/okfreq/references/operations.md` (the config example and the "default StRS mode"
  bullet that names `@tests_req StRS-...`): the new mode, the four marker keys, `scenarios:`,
  Rule 4 in short, and how to fix each error and `W003`.
- `skills/okfreq-gardening/SKILL.md` (the bullet "Add a direct validation-test…"): declaring
  `scenarios:` from existing headings (frontmatter only, `S1…` in order, never reused), Rule 7,
  sorting existing markers into `@tests_req SwRS-X#S<n>`, `@simulates_req StRS-X#S<n>` or
  `@accepts_req StRS-X#S<n>` by what the test really does, and never inventing a test or a
  marker to fill a counter.
- `skills/okfreq-setup/SKILL.md`: the mode choice names the new mode.
- No skill depends on the documentation link: the W003 message and the skills carry the
  instructions.

### 4. Scaffold guidance: `src/okf_schema/data/`

- `src/okf_schema/data/requirements/guidelines/requirements.guidelines.md` ("Traceability
  markers", the StRS test-marker sentence, "Lifecycle and approval", "Tier-specific authoring
  formats"): `scenarios:`, `#S<n>`, the three test verbs and their benches, the StRS
  `### Main paths` format, Rule 7. Then `just refresh-requirements-guideline` regenerates
  `requirements/guidelines/requirements.guidelines.md`; neither copy is edited by hand.
- `DEFAULT_CONFIG` and the generated schemas (surface 1) are scaffold too; `okfreq init` keeps an
  existing project's files, as today.

### 5. Own requirements: `requirements/` and their tests (Q21, Q35, Q45)

This repository switches to the new mode and is migrated for real. The project guideline
forbids nominal evidence, so each marker goes only on a test that does what the marker says.

**Benches in this repository.**

- **Real bench** (`@accepts_req`): the product as a user gets it. The test builds the wheel
  (`uv build --offline --wheel`), installs it in an isolated venv, and runs the installed
  console scripts (`okf-schema`, `okfkb`, `okfreq`) as subprocesses in a fresh temporary project,
  with no source checkout on `PYTHONPATH`, exactly as
  `test_installed_wheel_commands_install_complete_families_without_source_checkout` does. Move
  its helpers (`_build_wheel`, `_link_runtime_dependencies`, venv setup) into a shared,
  session-scoped fixture in `tests/conftest.py` (built once per pytest worker), reused by that
  test. On Windows these tests skip, as that test does today; the Linux and macOS CI jobs run
  them.
- **Simulated bench** (`@simulates_req`): an in-process test (`CliRunner`, API calls, `runpy`)
  that walks the whole path.

**Steps.**

1. `requirements/config.yml`: `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`;
   `markers.simulates: '@simulates_req'`, `markers.accepts: '@accepts_req'`; the new acceptance
   test modules added to the `test_dirs` of their scopes.
2. The 5 StRS (all `proposed`, so their body may change through the usual review): add a
   `### Main paths` section with `#### Path <n>: <title>` and its steps, and the matching
   `scenarios:`. The paths are derived from each StRS's normative statement and derived SwRS;
   the candidates are open question 5. The PR lists them for the owner.
3. One acceptance test per declared path, in `tests/test_acceptance_core.py`,
   `tests/test_acceptance_okfkb.py` and `tests/test_acceptance_okfreq.py`, each walking the path
   through the installed console scripts and asserting the observable outcome, marked
   `# @accepts_req StRS-OKFSCHEMA-…#S<n>`.
4. The 6 `@tests_req StRS-OKFSCHEMA-…` markers in `tests/` move to `@simulates_req` by a
   one-off command in the PR (not an okfreq subcommand, Q8), then each gets the fragment of the
   path its test really walks (several lines if it walks several, e.g. the showcase test). A
   test that walks no declared path loses the marker. Starting points:
   `tests/test_integration.py::test_end_to_end_workflow_init_creates_base_schema_and_validates`
   (CORE-001), `::test_end_to_end_workflow_format_then_validate_consistency` (CORE-002),
   `::test_kb_end_to_end_workflow_kb_update` (OKFKB-001),
   `tests/test_file_links.py::test_inspect_file_links_exposes_successes_failures_and_suffixes`
   (CORE-003), `tests/test_okfreq.py::test_report_and_cli_surface` and
   `tests/test_examples.py::test_okfreq_showcase_runs_in_an_empty_project` (OKFREQ-001).
5. The 23 SwRS (and the new one): declare `scenarios:` from their `### Scenario:` headings,
   `S1…` in order, titles from the headings. For each scenario, put
   `# @tests_req SwRS-…#S<n>` on the test function(s) that exercise it, found among the SwRS's
   current `tested_in_files`. File-level fragmentless markers become per-test markers (they are
   errors now). A scenario with no exercising test gets a real new test; a marker never goes on
   a test that does not exercise its scenario.
6. Create one bounded SwRS with `okfreq new swrs` in the new mode (pre-filled, Rule 9), scope
   `okfreq`, `--derives-from StRS-OKFSCHEMA-OKFREQ-001`, `--lifecycle proposed`,
   `--project okf-schema`. It states Rules 1 to 9 as observable behavior, with scenarios and
   verification criteria; its `documentation_files`, `agent_skill_files` and `example_files`
   name the real files of surfaces 2, 3 and 6. Check SwRS-OKFSCHEMA-OKFREQ-002, -003, -004 and
   -005 still hold; change one only where its statement became false.
7. `requirements/tiers/_schema/base.schema.yaml` (`scenarios`), `strs.schema.yaml` and
   `swrs.schema.yaml` (marker-derived properties, Rule 4).
8. `requirements/guidelines/project.guidelines.md`: replace "This project uses
   `linked-swrs-and-validation-test`…" and "Keep the strict StRS coverage mode and direct
   validation-test evidence current" with the new mode and the bench definitions above.
9. `requirements/tiers/log.md`: one entry under today's `## YYYY-MM-DD` heading (newest first),
   `### Acceptance paths`: the mode switch, the new SwRS, the schema changes, the declared
   paths and transitions, the moved markers, the new acceptance tests, the verification result.
10. `okfreq update-coverage requirements`, then `okfreq validate requirements --prose
    --check-links --project-root .`, `okfreq lint requirements --prose --check-links
    --project-root .`, `okfreq trace requirements --json`.

### 6. Concrete examples: `examples/` (Q35)

- `examples/okfreq-examples/showcase.py`: a new step after `strict_stakeholder_coverage`, in
  the disposable project (custom `@delivers`/`@verifies` already). Add
  `markers.simulates: '@rehearses'` and `markers.accepts: '@accepts'`, switch to the new mode,
  then assert in order:
  1. W003 names `StRS-DELIVERY-001`, quotes the `#### Path` headings the step wrote, and gives
     the block;
  2. after pasting `scenarios:` (S1, S2) on the StRS and (S1, S2) on `SwRS-DELIVERY-001`, a
     fragmentless `@verifies SwRS-DELIVERY-001` is an error and does not count;
  3. `@verifies StRS-DELIVERY-001` is the error naming `@rehearses`;
  4. `#S9` is the unknown-fragment error;
  5. `paths` go `0/2` → tested `2/2` with `@rehearses …#S1`/`#S2` → accepted `1/2` then `2/2`
     with `@accepts …#S<n>`; the booleans and the StRS `status` follow;
  6. the SwRS is covered only when both transitions are marked;
  7. `@accepts SwRS-DELIVERY-001` is the schema-driven error;
  8. `Draft202012Validator(report_schema())` validates the report.
  Record `outcomes["acceptance_paths"]`; restore the earlier mode afterwards.
  `tests/test_examples.py` expects 13 outcomes.
- The checked-in example `examples/okfreq-examples/`: migrated as open question 4 settles. In
  any case its SwRS declare `scenarios:` (SwRS-CORE-001: S1 Export selected rows, S2 Export an
  empty selection; SwRS-CORE-002: S1 Return a Rust CSV row, S2 Export an empty Rust row) and its
  tests carry per-test fragments: `tests/test_export.py::test_export_rows` `#S1`,
  `::test_export_rows_with_empty_selection` `#S2`, and the two Rust tests in
  `tests/rust_export_test.rs`. The `refresh-okfreq-examples` recipe of the `justfile` is updated
  so that regeneration produces this state (mode, pre-filled `scenarios:` titles replaced like
  the body placeholders, the StRS `### Main paths` text). `dist/requirements-report*.json|md`
  are regenerated (`format_version` 2) and reviewed.
- `examples/okfreq-examples/README.md`: names the new showcase outcome and, if the checked-in
  example shows a gap, why.

### 7. Verification and packaging: `tests/`, `justfile`, `pyproject.toml`, CI

New and changed tests are listed under Evidence. `justfile` changes only in
`refresh-okfreq-examples`. CI (`.github/workflows/ci.yml`, `just preflight` on Linux ×4 Pythons,
macOS, Windows) does not change; the acceptance tests need `uv` and an offline build, which the
existing installed-wheel test already needs there. Packaging does not change.

## Out of scope

- The Studio's migration: its `scenarios:`, moving its markers to `@simulates_req` by script,
  its acceptance tests (Studio CR `strs-path-validation`).
- A migration subcommand (Q8); bench configuration (Q2).
- Test-result ingestion: counters are linkage; `execution_evidence` stays `not_collected`.
- Checking that `scenarios:` titles match the body headings, or a history of retired ids (Q26).
- Several IDs or fragments on one marker line: one marker per line, as today.
- Any change of behavior in the old modes (Rule 1).

## Evidence

### Checks

`tests/test_okfreq.py` (unit, `okf_schema.okfreq.core`, per
`.github/guidelines/python-unittest.guidelines.md`). Each test builds its bundle with
`initialize_bundle`/`create_requirement` in `tmp_path`, edits `config.yml` as a user does, and
writes real test files with markers:

1. `load_config` accepts the new mode; the refusal lists three modes; duplicate keywords fail;
   an old `config.yml` without `simulates`/`accepts` gets the defaults.
2. `okfreq init` output, read from the files written: base schema has `scenarios`; strs/swrs
   schemas have the marker-derived properties; `config.yml` has both new markers.
3. `marker_scan`: the two new kinds read in `test_dirs` only; fragment and line captured;
   custom keywords; `#path1`, `#S1a`, `#` read as fragmentless; `#S0` captured; two fragments of
   one ID in one file give two `scenario_markers`; the new keys and the doctest.
4. **Every row of Rule 4's table** in the new mode, with the message contents (file:line,
   configured keyword, declared ids, the suggested marker).
5. Rule 5: StRS fractions and booleans at `0/3`, `2/3` tested with `1/3` accepted, `3/3`;
   tested and accepted independent; covered needs accepted plus linked SwRS; StRS without
   `scenarios:` tested/accepted by fragmentless markers; SwRS with transitions covered only when
   all marked; `tested_in_files` per Q30; exempted SwRS stay out.
6. W003: body with `### Main paths` / `#### Path 1: …` / `#### Path 2: …` → headings quoted,
   block with titles, link; body with `### Scenario: …` headings; no heading → placeholder block;
   reading stops at the next `###` and at the links block; deprecated/superseded → none; draft →
   one; printed without `prose=True`; no finding for a SwRS without `scenarios:`.
7. Rule 2: the schema refuses `kind`, `P1`, empty title, `[]`; the code refuses duplicate ids;
   `update_coverage` preserves `scenarios:` byte for byte.
8. Rule 4's schema mechanism: `@accepts_req SwRS-X` is an error carrying the schema
   description; a project schema that drops the `maxItems: 0` accepts it; an authored
   `accepted_in_files` is an error; a pre-0.18 `swrs.schema.yaml` behaves per open question 2.
9. Rule 7: an approved StRS (approval fields present) that gains only `scenarios:` validates.
10. Rule 8: `format_version` 2 in all three modes; new fields present in the new mode and
    absent otherwise; `Draft202012Validator(report_schema())` validates each mode's report;
    Markdown columns, summary line and `Missing transitions` in the new mode, unchanged table in
    the old modes.
11. Rule 9: `create_requirement` in the new mode pre-fills `scenarios:` for SwRS (S1, S2) and
    StRS (S1 and the `### Main paths` section); in the old modes the output is identical to
    today's.

`tests/test_okfreq_cli.py` (`CliRunner`): `validate` exits 1 on each error kind and 0 while
printing W003; `lint` fails on the same; `trace` prints `simulated:` and `accepted:`;
`generate-report` writes the columns; `new` pre-fills.

`tests/test_skill_resources.py`: the shipped `skills/okfreq/SKILL.md`,
`skills/okfreq/references/operations.md`, `skills/okfreq-gardening/SKILL.md` and
`skills/okfreq-setup/SKILL.md`, read as they ship, mention the new mode, the three test verbs,
`scenarios:` and `#S<n>`; installed references stay self-contained. A test reads
`src/okf_schema/data/requirements/guidelines/requirements.guidelines.md` as it ships and checks
it states the three verbs, the fragment rule and Rule 7;
`test_repository_guideline_is_the_installed_shipped_text` keeps the copy equal.

Documentation:

- A new test (e.g. `tests/test_okfreq_docs.py`) reads the captioned blocks of the three worked
  examples from `docs/source/reference/okfreq-acceptance-paths.md`, builds each bundle and its
  test files from them, and asserts the JSON excerpt and Markdown row the page shows, and W003
  for the third. The page and the code cannot drift.
- `just docs` (`sphinx-build -W`) succeeds: both new pages are in a toctree, every cross-link
  resolves. Then check the built site: `docs/_build/html/explanation/okfreq-acceptance-paths.html`
  and `docs/_build/html/reference/okfreq-acceptance-paths.html` exist, and
  `docs/_build/html/reference/okfreq-frontmatter.html` contains `id="okfreq-declared-scenarios"`
  (the W003 link target).

Repository and examples:

- `tests/test_project_contract.py::test_live_requirements_preserve_complete_real_evidence`
  asserts the new mode, zero findings (so no fragment error, no W003), `covered ==
  requirements` (every path accepted, every transition tested) and no `missing_tests`.
- The new acceptance tests run on Linux and macOS in `just test` and fail if the installed
  scripts do not produce the path's outcome.
- `tests/test_examples.py::test_okfreq_showcase_runs_in_an_empty_project` runs the new step.
- `just preflight` (style, lint, `requirements-lint`, changelog, typecheck, guideline refresh,
  tests, `refresh-all-examples`, `requirements-report`, `docs`). Review its generated diffs
  (examples, `dist/`, guideline copies, `CHANGELOG.md`) before hand-back. The commit subject is
  `feat(okfreq): measure StRS acceptance paths with declared scenarios` (no `!`, Q40);
  `pyproject.toml`'s version is bumped by the release flow, not by hand.

### Default and configured-value matrix

No host dependency: okfreq is a CLI and behaves the same under any agent host. Each cell starts
from a real `okfreq init` in a temporary project; configured cells edit `config.yml` as a user
would. Shared fixture: StRS-A with `scenarios:` S1/S2 and `#### Path` headings; StRS-B without
`scenarios:`; SwRS-A (from StRS-A) with transitions S1/S2; a test file with
`@accepts_req StRS-A#S1`, `@simulates_req StRS-B`, `@tests_req StRS-B`, `@tests_req SwRS-A`,
`@tests_req SwRS-A#S9`, `@accepts_req SwRS-A`.

| Cell | Configuration | Result it must show |
|---|---|---|
| D1 | Shipped default (`linked-swrs`, all four default markers) | `okfreq validate` 0 errors, no W003; coverage equal to the same bundle without the suffixes; `@simulates_req`/`@accepts_req` count nowhere; `format_version` 2, no new fields; `okfreq new` output as today. |
| D2 | `linked-swrs-and-validation-test` | As today: `@tests_req StRS-B` is StRS-B's validation test; `@tests_req SwRS-A#S9` covers SwRS-A; `@accepts_req SwRS-A` is accepted silently. A step adds `@tests_req StRS-A#S1` and sees it counted as StRS-A's validation test. |
| D3 | `linked-swrs-and-acceptance-paths`, default markers | Validate exits 1: fragmentless `@tests_req SwRS-A`, `#S9`, `@tests_req StRS-B` (naming `@simulates_req`), `@accepts_req SwRS-A` (schema description). W003 on StRS-B. StRS-A `paths {2, 0, 1}`; StRS-B tested by the fragmentless `@simulates_req`; SwRS-A missing S1, S2. Markdown `0/2`, `1/2`, `✅ no paths`. |
| D4 | New mode, custom `tests: '@verifies'`, `simulates: '@rehearses'`, `accepts: '@accepts'` (the showcase) | Same as D3 with the custom keywords quoted in messages. |
| D5 | New mode, `config.yml` written before this change (no `simulates`/`accepts` keys) | Default keywords recognised; same results as D3. |
| D6 | New mode, `swrs.schema.yaml` written before this change | `@accepts_req SwRS-A` behaves as open question 2 decides; everything else as D3. |
| D7 | `strs_test_coverage_mode: unsupported` | `RequirementError` listing the three modes; `okfreq validate` exits non-zero with it. |

### Scenario steps (manual demonstration for the PR)

In a temporary directory:

1. `okfreq init requirements`, set the new mode in `requirements/config.yml`.
2. `okfreq new strs …`: the body has `### Main paths` / `#### Path 1: <main path title>` and the
   frontmatter `scenarios:` S1. Replace the placeholder in both, add `#### Path 2: …` and S2.
3. `okfreq new swrs … --derives-from …`: `scenarios:` S1, S2 pre-filled.
4. Add `# @tests_req <SwRS>` in `tests/`: `okfreq validate requirements` exits 1 and asks for
   `#S<n>`. Mark two tests `#S1`, `#S2`: exits 0.
5. Add `@simulates_req <StRS>#S1`, `#S2` and `@accepts_req <StRS>#S1`, then
   `okfreq generate-report requirements`: the StRS row shows `Tested 2/2 ✅`, `Accepted 1/2`,
   status missing; adding `@accepts_req <StRS>#S2` makes it covered.
6. Remove `scenarios:` from the StRS: `W003` quotes both path headings and prints the block.
7. `just docs` in okf-schema and open the two new pages and the "Declared scenarios" anchor.

## Open questions

Only these remain; each has a proposal the Driver applies unless the user decides otherwise.

1. **`@simulates_req` on a SwRS.** Q20 covers `@accepts_req` only. Proposal: an error too, by
   the same schema mechanism (`simulated_in_files` refused in `swrs.schema.yaml`), since the
   simulated-bench verb names a StRS path and a SwRS test is `@tests_req`.
2. **Q20 on a bundle whose `swrs.schema.yaml` predates 0.18.0** (`okfreq init` never replaces
   schemas, so it does not declare `accepted_in_files`/`simulated_in_files`; the Studio is in
   this case). Silent, or an error anyway? Proposal: when a leaf tier's schema does not declare
   the property at all, okfreq applies the shipped declaration (the same text `schema_text`
   writes), so every bundle gets the error; a project that declares the property in its own
   schema decides for itself. The docs tell existing projects to add the declaration.
3. **`validation_tests` of a StRS in the new mode** (kept "for backward compatibility", Q42).
   Proposal: the same files and status as `acceptance_tests`, so an old consumer reading
   `validation_tests` sees the real-bench evidence that now makes a StRS covered; a
   `@tests_req StRS-X` (an error in this mode) never appears in it.
4. **The checked-in example's mode** (Q35 "migrate the examples correctly"). It has no real
   bench for its toy CSV export. Proposal: switch it to the new mode; declare one path on
   StRS-CORE-001 ("Export selected rows for offline review"), mark `test_export_rows` with
   `@simulates_req StRS-CORE-001#S1`, add no acceptance test, and let the report honestly show
   `Tested 1/1 ✅`, `Accepted 0/1`, StRS not covered, explained in its README. The showcase
   shows a complete `2/2`.
5. **The main paths of this repository's 5 StRS** (StRS content is the owner's). Proposal,
   from each StRS's normative statement:
   - CORE-001: S1 Validate a conforming bundle; S2 Report a non-conforming bundle without
     changing it.
   - CORE-002: S1 Create a bundle and author a concept; S2 Normalize and index a bundle;
     S3 Inspect bundle knowledge read-only.
   - CORE-003: S1 Navigate declared file links; S2 Check declared file links on request.
   - OKFKB-001: S1 Capture an immutable finding; S2 Update a knowledge base's indexes and lint;
     S3 Propose a consolidation for human review.
   - OKFREQ-001: S1 Set up a bundle and author linked requirements; S2 Trace markers and
     refresh generated coverage; S3 Audit the requirements base with validate and a report.
