# okfreq: acceptance paths, declared scenarios, two StRS counters

Type: feat (okfreq, requirements) · Requested 2026-11-23 by the markdown-okf-schema-studio
Griller from the Studio owner's grill ([request](intake/request.md), [intent](01-intent.md),
[answers](02-answers.md)) · Forge-neutral (GitHub and GitLab) · One CR, one batch (Q10) ·
Grilled enough 2026-11-23, destination `3-ready` (Q17).

A new `strs_test_coverage_mode` makes `okfreq` measure that a StRS is proved by tests that walk
its declared main paths, instead of counting any direct link as a validation test. Requirements
declare their paths (StRS) or transition scenarios (SwRS) in one shared frontmatter field,
`scenarios:`. Tests name a path with a `#S<n>` fragment. Each StRS gets two counters:
"tested", from `@tests_req` on the simulated bench, and "accepted", from the new
`@accepts_req` on the real bench.

## Goal, in the user's terms

The Studio counts 93 of its 94 live StRS as validated. A 1-in-6 sample of its 185 direct
`@tests_req StRS-...` markers
([audit](../../../../markdown-okf-schema-studio/changes/2-backlog/P2/strs-path-validation/experiments/02-audit-sample.md))
shows that only 13 of 31 walk a StRS main path. A marker is a link, not a proof. The owner
wants `okfreq` to:

1. let a requirement declare its paths or transitions with stable short ids (`S1`, `S2`, never
   reused) and a title, in a `scenarios:` frontmatter field that both tiers share and that has no
   `kind`;
2. recognise an end-to-end acceptance test (`@accepts_req StRS-X#S<n>`) and a path or
   transition test (`@tests_req StRS-X#S<n>`, `@tests_req SwRS-X#S<n>`);
3. report, per StRS, which fraction of its paths is tested on the simulated bench and which is
   accepted on the real bench;
4. tell an agent exactly how to declare `scenarios:` when a StRS has none (no migration
   command).

The Studio's own migration (sorting its 185 markers and writing the acceptance tests) is the
Studio CR `strs-path-validation`, which waits for this one.

## Starting point (code read on 2026-11-23)

I read the clone `/Users/az02065/Projects/DevTools/okf-schema` read-only, on branch
`dev/gsemet` at `89b52ad` (version 0.16.0). The default branch is `main` on GitHub. Tag
`v0.17.0` (`8f56838`, `feat(okfreq)!: keep requirement bundles native OKF v0.2 bundles`) already
changes `core.py`, `cli.py` and the schemas: the lifecycle field becomes `req_lifecycle`,
`approved_on` becomes `approved_at`, `status`/`verified` are generated, `okfreq validate` also
runs the base OKF checks, and `log.md` headings must be exactly `## YYYY-MM-DD`, newest first,
with `### Topic` sub-headings. **The Driver works from the head of `main`.** Function names below
hold at both commits; line numbers do not, so the spec gives none.

What exists today, in `src/okf_schema/okfreq/core.py`:

- `STRS_TEST_COVERAGE_MODES = ("linked-swrs", "linked-swrs-and-validation-test")` and
  `STRS_TEST_COVERAGE_DESCRIPTIONS`. `load_config` defaults the mode to `linked-swrs` and
  `_strs_test_coverage_mode` refuses other values with
  `unsupported strs_test_coverage_mode: <mode>; expected one of: <list>`.
- `load_config` defaults `markers` to `{"implements": "@implements_req", "tests": "@tests_req"}`
  plus `id_pattern` (default `[A-Za-z][A-Za-z0-9_-]*`). `DEFAULT_CONFIG` (what `okfreq init`
  writes) lists the same two markers.
- `marker_scan(root)` builds one regex,
  `^\s*(?:(?:#|//|/\*|\*|<!--)\s*)?(?P<marker>implements|tests)\s+(?P<identifier>id_pattern)`.
  It reads implementation markers only in `source_dirs` and test markers only in `test_dirs`.
  It records `implemented` and `tested` for leaf (SwRS) IDs and `validation_tests` for a
  `@tests_req` on a StRS. Unknown IDs go to `missing_ids`, other non-leaf IDs to `non_leaf`.
  It keeps one entry per (target, ID, file) and records no line numbers. **Because the ID
  pattern stops at `#`, a marker `@tests_req SwRS-X#S1` already counts today as
  `@tests_req SwRS-X`: the fragment is silently dropped.**
- `validate_requirements` returns findings: plain errors, `W…` warnings (`W001` and `W002` are
  prose warnings, emitted only with `--prose`; `W17` comes from schemas) and `I…` infos (`I1`,
  `I2`). It **does not scan markers**. `okfreq validate` exits 1 on any error. `okfreq lint` runs
  the same validation through `_run_validation` and fails with a `ClickException`. `okfreq status`
  counts the errors.
- `update_coverage` writes `implemented_in_files`/`tested_in_files` for SwRS from `marker_scan`
  and removes them from StRS.
- `report(root)` computes each StRS's `stakeholder_test_coverage` (`status`, `mode`,
  `linked_swrs`, `validation_tests`), the aggregate `stakeholder_test_coverage`, totals and
  scopes, and writes `"format_version": 1`. `report_schema()` fixes
  `"format_version": {"type": "integer", "const": 1}` and the `$defs`
  `stakeholder_requirement_coverage`. `write_markdown_report` renders the
  "By stakeholder requirement" table (`| Scope | Tier | ID | Name | Tests |`), followed by a
  note built from `STRS_TEST_COVERAGE_DESCRIPTIONS[mode]`.
- `initialize_bundle`'s `schema_text("base")` generates `tiers/_schema/base.schema.yaml` with
  `additionalProperties: true`. The repository's `requirements/tiers/_schema/*.schema.yaml`
  also accept unknown properties, so no shipped schema refuses `scenarios:` today. Nothing
  declares it either.
- `src/okf_schema/okfreq/cli.py`: `validate`, `lint`, `trace` (summary
  `implemented: N; tested: N; missing IDs: N`), `update-coverage`, `generate-report`.
- `requirements/config.yml` uses `strs_test_coverage_mode: linked-swrs-and-validation-test`.
  `tests/test_project_contract.py::test_live_requirements_preserve_complete_real_evidence`
  asserts that mode, an empty `validate_requirements(...)` and full stakeholder coverage.
- Changelog: `just changelog` (`cz changelog`) generates `CHANGELOG.md` from conventional commit
  subjects. Nobody edits it by hand.
- The Studio's bodies show the shapes to read for the agent message (Q13): a StRS has
  `### Main paths` followed by `#### Path 1: Wait for a render`, `#### Path 2: …`. A SwRS has
  `### Scenario: Repeated block`. okfreq's own SwRS template (`_SWRS_BODY`) also writes
  `### Scenario: <…>` headings.

## Decisions carried (from `02-answers.md`)

| Q | Decision | Where in this spec |
|---|---|---|
| Q1 | A new value of `strs_test_coverage_mode` (e.g. `linked-swrs-and-acceptance-paths`) activates the feature; without it, `scenarios:` and `@accepts_req` are accepted but nothing is required or counted. | Rule 1 |
| Q2 | No bench configuration: the marker tells the bench. `@accepts_req` = real bench, `@tests_req` = simulated bench; the two may be different tests. | Rules 3, 5 |
| Q3 | One fraction of paths per counter (tested 2/3, accepted 1/3); the StRS is "tested" (boolean) when its fraction is complete, and likewise "accepted". | Rule 5 |
| Q4 | Direct `@tests_req StRS-X` in the new mode: ignored for coverage, reported as a warning. **Superseded by Q14 for a StRS that declares paths**; it still applies to a StRS that declares none. | Rule 4 |
| Q5 | Error for an unknown `#S<n>` fragment; warning for a live StRS with no declared path. | Rule 6 |
| Q6 | `@tests_req StRS-X#S<n>` counts path `S<n>` as tested (simulated bench); with no fragment it is the Q4 case. | Rules 4, 5 |
| Q7 | Fragments on a SwRS count: a SwRS with declared transitions is covered only when every transition has a `@tests_req SwRS-X#S<n>`. | Rule 5 |
| Q8 | No migration subcommand: okfreq's message tells agents how to declare `scenarios:` themselves. | Rule 6 (W003) |
| Q9 | Declaring `scenarios:` on an approved StRS: edit the frontmatter only (body intact) and log it in `requirements/tiers/log.md`. The Studio's owner agreement already covers this metadata-only change. | Rule 7, surfaces 2–5 |
| Q10 | One CR, one batch. | Header |
| Q11 | New mode only, for StRS and SwRS alike: once `scenarios:` are declared, each must be covered. **Refined by Q14**: a fragmentless test covers everything only when no `scenarios:` are declared. | Rules 1, 4, 5 |
| Q12 | JSON and Markdown, schema version incremented. Per StRS: `paths: {total, tested, accepted}` and the two booleans. Per SwRS: tested and missing transitions. The Markdown shows the two counters as columns. | Rule 8 |
| Q13 | The message names the StRS, quotes the `### Main paths` / `### Scenario` headings it found, gives the `scenarios:` block to paste and the documentation link. | Rule 6 (W003) |
| Q14 | When a StRS or SwRS declares `scenarios:`, every `@accepts_req` / `@tests_req` marker that targets it must carry `#S<n>`. | Rule 4 |
| Q15 | A marker without a fragment on such a target is an error: `okfreq validate` fails and asks for `#S<n>`, and the marker does not count. | Rules 4, 6 |
| Q16 | All six surfaces of `AGENTS.md`, plus `docs/source/explanation/project-feature-coverage.md`. | What changes, by surface |
| Q17 | Grilled enough; next batch (`3-ready`). | Header |

The request's point 3 named benches "in the project's config". Q2 replaces that: there is no
bench configuration. The request's point 5 asked for migration help. Q8 and Q13 make that help an
okfreq message, not a command.

## The rules

"The new mode" below means `strs_test_coverage_mode: <new mode name>`. The name is open
question 1; this spec writes `linked-swrs-and-acceptance-paths`.

### Rule 1: activation (Q1, Q11)

- `STRS_TEST_COVERAGE_MODES` gains the new mode, with a description in
  `STRS_TEST_COVERAGE_DESCRIPTIONS`. Its wording depends on open question 2. `load_config` and
  `_strs_test_coverage_mode` accept it, and the refusal message lists all three modes.
- In `linked-swrs` (the shipped default) and `linked-swrs-and-validation-test`, okfreq accepts
  `scenarios:` and `@accepts_req` markers, but requires and counts nothing new. Every finding,
  coverage figure and generated field stays as today. In particular, a fragment on a marker is
  ignored, as it is today: `@tests_req StRS-X#S1` still counts as a validation test in
  `linked-swrs-and-validation-test`, and `@tests_req SwRS-X#S1` still covers SwRS-X. An
  `@accepts_req` marker counts toward nothing. Open question 3 asks whether the shape checks of
  Rule 2 and the unknown-fragment error also apply outside the new mode.
- Rules 4 to 6 and the new report fields of Rule 8 apply only in the new mode.

### Rule 2: the `scenarios:` frontmatter field (request point 1)

- It is one authored field that both tiers share. On a StRS it lists its main paths; on a SwRS
  it lists its transition scenarios. The tier says which, so an entry has no `kind`.
- Its shape is a list of mappings. Each entry has an `id`, a short stable id `S<n>`, and a
  non-empty `title`, and no other key:

  ```yaml
  scenarios:
    - id: S1
      title: Wait for a render
    - id: S2
      title: The source is gone
  ```

- An id is never reused, even after its scenario is removed. okfreq cannot see history, so the
  guidance states this rule (open question 4).
- Declare the field in the **base** schema. Change both `schema_text("base")` in
  `initialize_bundle` (new bundles) and `requirements/tiers/_schema/base.schema.yaml` (this
  repository). Proposed property: `type: array`; `items` is an object with
  `required: [id, title]`, `id: {type: string, pattern: '^S[1-9][0-9]*$'}`,
  `title: {type: string, minLength: 1}` and `additionalProperties: false`. The
  `additionalProperties: false` on the item is what forbids `kind`. A description says what an
  entry means on each tier and that ids are never reused. It carries no `x-okf-link`: these are
  not links. The top-level `additionalProperties: true` stays.
- `okfreq init` never replaces an existing schema. A bundle created before this change therefore
  does not declare the property, but still accepts the field. In the new mode, okfreq checks the
  shape in code too (`validate_requirements`), because the counters depend on it. A duplicate
  `id`, an `id` that is not `S<n>`, a missing or empty `title`, or a `scenarios` that is not a
  list of mappings is an error. Proposed message:
  `<file>: scenarios: <problem> (each entry is {id: S<n>, title: <text>}, ids unique)`.
- `update_coverage` preserves the field: it is authored, never generated. This needs no change
  in `_render_frontmatter`, which keeps unknown keys. A test proves it.

### Rule 3: markers and the fragment syntax (request point 2, Q2)

- A third marker kind, `@accepts_req`, marks an end-to-end acceptance test on the **real** bench
  (Q2). `@tests_req` is a test on the **simulated** bench (Q2). One path may have a
  `@tests_req` test and a different `@accepts_req` test. Nothing forbids one test from carrying
  both markers.
- Its keyword is configurable like the other two, as `markers.accepts` (open question 5).
  `load_config` defaults it to `@accepts_req` even in a `config.yml` that lists only
  `implements` and `tests`. `DEFAULT_CONFIG` lists it, so `okfreq init` writes it.
- `@accepts_req` is a test marker: `marker_scan` reads it only in `test_dirs`, as it reads
  `@tests_req`. In `source_dirs` it is skipped, as a test marker is there today.
- Fragment: an optional `#<fragment>` directly after the ID, with no space, for example
  `@accepts_req StRS-X#S2` or `# @tests_req SwRS-X#S1`. It is allowed on `@accepts_req` and
  `@tests_req` and is optional (Q14 says when it becomes mandatory). A valid fragment is `S<n>`.
  The proposed regex extension of `marker_scan` is:

  ```text
  (?P<marker>implements|tests|accepts)\s+(?P<identifier>id_pattern)(?:#(?P<fragment>[A-Za-z0-9_]*))?
  ```

  `fragment` is then valid when it fully matches `S[1-9][0-9]*`. The exact syntax is open
  question 6. The capture is wide on purpose, so a malformed fragment (`#s1`, `#path1`, an empty
  `#`) is captured and reported, never silently dropped. `markers.id_pattern` still matches the
  whole ID and nothing more. The documentation says that a custom `id_pattern` must not admit
  `#`.
- `marker_scan` records, for each `@tests_req`/`@accepts_req` occurrence, the marker kind, the
  ID, the fragment (or none), the project-relative file and the **line number**. Messages need
  the line. The de-duplication key includes the fragment. `implemented`, `tested`,
  `validation_tests`, `missing_ids`, `non_leaf` and `warnings` keep their meaning, so the old
  modes and `report()` keep their results. New keys are added: `accepted` (ID → files) and a list
  of the occurrences with fragments and lines. Their names are open question 7. The
  `marker_scan` doctest lists the keys and is updated.
- Unknown ID in an `@accepts_req`: it goes to `missing_ids`, as today.

### Rule 4: which marker counts, in the new mode (Q4, Q6, Q11, Q14, Q15)

| Marker | Target declares `scenarios:` | Target declares none |
|---|---|---|
| `@tests_req StRS-X#S<n>`, `S<n>` declared | path `S<n>` **tested** (Q6) | — |
| `@accepts_req StRS-X#S<n>`, `S<n>` declared | path `S<n>` **accepted** | — |
| `@tests_req SwRS-X#S<n>`, `S<n>` declared | transition `S<n>` tested (Q7) | — |
| any `#<fragment>` not declared on the target, or malformed | **error**, does not count (Q5) | **error**, does not count (Q5: a `#S<n>` must name a declared scenario) |
| `@tests_req StRS-X` (no fragment) | **error**, does not count (Q14, Q15) | ignored for coverage, **warning** W004 (Q4, Q6) |
| `@accepts_req StRS-X` (no fragment) | **error**, does not count (Q14, Q15) | open question 8 |
| `@tests_req SwRS-X` (no fragment) | **error**, does not count (Q14, Q15) | covers the whole SwRS, as today (request point 2, Q11 as refined by Q14) |
| `@accepts_req SwRS-X[#S<n>]` | open question 9 | open question 9 |

### Rule 5: counters and coverage, in the new mode (Q2, Q3, Q7, Q11)

- **Per StRS**, `total` = the number of declared paths. `tested` = the number of declared paths
  with at least one counting `@tests_req StRS-X#S<n>`. `accepted` = the number of declared paths
  with at least one counting `@accepts_req StRS-X#S<n>`. The StRS is **tested** when
  `tested == total` and **accepted** when `accepted == total` (Q3). The value for a StRS with no
  declared path (`0/0`) is open question 8.
- **Per SwRS** (leaf, no `annotation_exemption`): with declared transitions, it is test-covered
  only when every declared `S<n>` has a counting `@tests_req SwRS-X#S<n>` (Q7). Without
  declared transitions, it is test-covered by any fragmentless `@tests_req SwRS-X`, as today.
  This covered status drives the SwRS `tests.status`, `totals.tested`, the scopes' `tested`, the
  `marker_coverage.missing_tests`, and the `linked_swrs[].status` of its StRS.
  Source coverage (`@implements_req`) does not change.
- **The StRS's own `status`** (`covered`/`missing`) in the new mode, and so the aggregate
  `stakeholder_test_coverage.covered` and the Markdown "StRS test coverage" line, are open
  question 2: the answers fix the two counters but not which of them (with the linked-SwRS rule)
  makes a StRS covered.
- `update_coverage`: whether `tested_in_files` of a SwRS that declares transitions leaves out
  the files whose only markers do not count (fragmentless or unknown fragment) is open
  question 10. StRS still carries no `implemented_in_files`/`tested_in_files`.

### Rule 6: findings and messages (Q5, Q8, Q13, Q15)

The new findings come from `validate_requirements`, in the new mode only. It calls
`marker_scan` then, and today it does not. So `okfreq validate` and `okfreq lint` fail on the
errors (Q15), `okfreq status` counts them, and `report()` lists each one in the
`diagnostics.errors` of the requirement whose ID it contains. Warnings print with or without
`--prose` and never change the exit code, as the existing `W…` findings do. The codes are
proposed (open question 11); the wording is the Driver's within these contents.

- **Error, fragment missing** (Q14, Q15):
  `<test file>:<line>: @tests_req SwRS-X has no scenario fragment; SwRS-X declares scenarios S1, S2: write @tests_req SwRS-X#S<n> (this marker does not count)`.
  The same applies to `@accepts_req` on a StRS that declares paths. The message uses the
  configured keyword.
- **Error, unknown or malformed fragment** (Q5):
  `<test file>:<line>: @accepts_req StRS-X#S4 names no declared scenario of StRS-X (declared: S1, S2)`.
  When the target declares none, the message ends with `(StRS-X declares no scenarios:)`.
  A malformed fragment gets `#path1 is not a scenario id S<n>`.
- **Error, malformed `scenarios:`** (Rule 2).
- **`W003`, live StRS with no declared path** (Q5, Q8, Q13). One finding per StRS, in a detailed
  message for an agent. It:
  1. names the StRS and its file;
  2. quotes the headings found in its body: every heading under `### Main paths` (such as
     `#### Path 1: Wait for a render`) and every `### Scenario…` heading. If there are none, it
     says so;
  3. gives the `scenarios:` block to paste into the frontmatter. The block has one entry per
     heading found, numbered `S1`, `S2`… in order, with the heading's title (the text after
     `Path <n>:` / `Scenario:`). With no heading, it has one placeholder entry
     `- id: S1` / `  title: <main path title>`;
  4. says to edit the frontmatter only. On an approved StRS the body stays intact and the change
     is logged in the bundle's `tiers/log.md` (Rule 7);
  5. gives the documentation link (open question 12).

  The heading-reading rule (which levels, which prefixes, where a `### Main paths` section ends,
  including before a generated `### Links` block) is open question 13. "Live" is open
  question 14.
- **`W004`, fragmentless `@tests_req StRS-X` on a StRS that declares no path** (Q4, Q6):
  `<test file>:<line>: @tests_req StRS-X is ignored for coverage in mode <mode>; declare scenarios: on StRS-X and mark each path test @tests_req StRS-X#S<n>`.
- No finding for a SwRS without `scenarios:`, even when its body has `### Scenario:` headings.
  Open question 15 asks whether such a SwRS should get a hint.

### Rule 7: approved StRS (Q9)

Declaring `scenarios:` on an approved StRS is a frontmatter-only edit. The body stays exactly as
it was, and the change is logged in the bundle's `tiers/log.md` (`requirements/tiers/log.md` in
this repository). This is guidance (shipped guideline, skills, docs and the W003 message), not a
new check. `_approval_findings` checks only that the approval record is present, so it needs no
change. A test proves that an approved StRS (with its approval fields) that gains only
`scenarios:` still validates. The Studio's owner has already agreed to this change for the
Studio. Open question 16 asks what the shipped, project-neutral guidance says about the
approval record (`approved_by`, `approved_at`) for such an edit.

### Rule 8: the report (Q12)

- `"format_version": 2` in `report()` and `"const": 2` in `report_schema()` (the number is open
  question 17). `report_schema()`'s mode enums follow `STRS_TEST_COVERAGE_MODES`.
- In the new mode, each StRS record's `stakeholder_test_coverage` gains
  `"paths": {"total": 3, "tested": 2, "accepted": 1}`, `"tested": false` and
  `"accepted": false`. `$defs.stakeholder_requirement_coverage` declares them as optional
  properties (`paths` with `total`/`tested`/`accepted`: integers ≥ 0, `tested`/`accepted`:
  booleans).
- In the new mode, each SwRS record that declares transitions gains
  `"transitions": {"tested": ["S1"], "missing": ["S2"]}`, which `$defs.requirement` declares as
  optional. The key name is open question 7.
- What `validation_tests` and the StRS `tests.files` hold in the new mode is open question 18.
  They keep their meaning in the other modes.
- `write_markdown_report`: in the new mode, the "By stakeholder requirement" table gains two
  columns, `Tested` and `Accepted`, each showing `tested/total` and `accepted/total`
  (e.g. `2/3`), with ✅ when complete. In the other modes the table is unchanged. The note below
  it uses the new mode's description. Whether the Summary lines and the aggregate
  `stakeholder_test_coverage` also carry path totals, and whether the SwRS table shows missing
  transitions, is open question 19.

## What changes, by surface (Q16)

`AGENTS.md` names six surfaces, all reviewed in this change, plus the feature map. The PR's
summary says, for each surface, what changed, or gives a concrete reason why it did not
(`.github/guidelines/product-maintenance.guidelines.md`, step 3).

### 1. Runtime: `src/okf_schema/`

- `okfreq/core.py`: `STRS_TEST_COVERAGE_MODES`, `STRS_TEST_COVERAGE_DESCRIPTIONS`,
  `DEFAULT_CONFIG` (`markers.accepts`), `load_config` (default `accepts`),
  `_strs_test_coverage_mode`, `initialize_bundle`/`schema_text("base")` (`scenarios`),
  `marker_scan` (third marker, fragment, line numbers), `validate_requirements` (Rule 6, in the
  new mode), `update_coverage` (Rule 5 / open question 10), `report`, `report_schema`,
  `write_markdown_report` (Rules 5 and 8). Add new private helpers as needed. Proposed:
  `_declared_scenarios(data)` for the shape and its findings, `_scenario_findings(...)` and
  `_scenario_coverage(...)` shared by validation, coverage and report, and
  `_scenarios_block_hint(text)` for the W003 headings and block. Public functions get Google-style
  docstrings with `.. versionchanged:: <next version>` (open question 20), following
  `.github/guidelines/python-module-documentation.guidelines.md`. Put
  `# @implements_req <new SwRS>` on the new code (surface 5).
- `okfreq/cli.py`: the `trace` summary adds `accepted: N`. The help and docstring of `validate`,
  `lint` and `generate-report` mention the new mode's findings and report fields.

### 2. Human documentation: `docs/source/`, `README.md`

- `reference/okfreq-configuration.md`: the `strs_test_coverage_mode` row and the
  "StRS test-coverage modes" section gain the new mode: what it requires, the two benches given
  by the marker, the counters and the marker rules of Rule 4. The `markers` row and the YAML
  example gain `accepts`, with the note that `id_pattern` must not admit `#`.
- `reference/okfreq-frontmatter.md`: a "Declared scenarios" section with the label
  `(okfreq-declared-scenarios)=`, which is the W003 link target. It covers the field, its shape,
  ids that are never reused, the StRS vs SwRS meaning, how to declare it from `### Main paths` /
  `### Scenario` headings, and Rule 7. "Marker fields" gains `@accepts_req` and the `#S<n>`
  fragment. The StRS coverage paragraph names the new mode.
- `reference/okfreq-cli.md`: the `validate`, `trace` and `generate-report` rows (new findings
  W003/W004 and errors, `accepted` count, report fields, `format_version` 2).
- `explanation/okfreq-coverage-boundaries.md`: the modes table gains a row. A section explains
  "tested" (simulated bench) vs "accepted" (real bench), both declared by the marker. This is
  still linkage, not execution: `execution_evidence` stays `not_collected`, and the marker
  declares the bench, okfreq does not observe it.
- `tutorials/okfreq-traceability.md` (near "If the project needs a direct stakeholder
  validation-test definition…") and `how-to/okfreq-build-requirement-base.md` (step choosing
  the mode): one short paragraph each on the new mode.
- `explanation/project-feature-coverage.md` (Q16): a new row, "Acceptance paths and declared
  scenarios", naming the new SwRS, the tests and the showcase scenario. If the live bundle does
  not switch mode (open question 21), the row says so and why. The "Stakeholder validation tests"
  row stays true.
- `README.md`: route to the new section only if the README already lists okfreq coverage modes.
  Otherwise the PR states that `README.md` is unaffected and why.

### 3. Standalone agent skills: `skills/`

Each skill must work without this repository (`tests/test_skill_resources.py`).

- `skills/okfreq/SKILL.md` ("Leaf requirements connect to evidence" bullet and the StRS
  authoring step) and `skills/okfreq/references/operations.md` (the config example and the
  "default StRS mode" bullet): the new mode, `markers.accepts`, `scenarios:`, the fragment rules
  of Rule 4, and how to read and fix W003, W004 and the fragment errors.
- `skills/okfreq-gardening/SKILL.md`: declaring `scenarios:` from existing `### Main paths` /
  `### Scenario` headings (frontmatter only, ids `S1…` in order, never reused); Rule 7 for
  approved StRS; sorting existing fragmentless markers into `#S<n>` path tests, acceptance tests
  or SwRS markers; never inventing acceptance tests to fill a counter.
- `skills/okfreq-setup/SKILL.md`: the mode choice names the new mode.
- No skill relies on the documentation link: the W003 message and the skill text carry the full
  instructions.

### 4. Scaffold guidance: `src/okf_schema/data/`

- `src/okf_schema/data/requirements/guidelines/requirements.guidelines.md` ("Traceability
  markers", "Lifecycle and approval", "Tier-specific authoring formats"): `scenarios:`, the
  `#S<n>` fragment, `@accepts_req` (real bench) vs `@tests_req` (simulated bench), and Rule 7.
  Then run `just refresh-requirements-guideline`, which regenerates
  `requirements/guidelines/requirements.guidelines.md`. `just refresh-okfreq-examples`
  regenerates the example's copy. Neither copy is edited by hand.
- The generated `base.schema.yaml` and `DEFAULT_CONFIG` (surface 1) are scaffold too:
  `okfreq init` keeps an existing project's files and policy, as today.

### 5. Own requirements: `requirements/`

- Create one bounded SwRS with `okfreq new swrs` (the tool allocates the number), scope
  `okfreq`, `--derives-from StRS-OKFSCHEMA-OKFREQ-001`, `--lifecycle proposed`,
  `--project okf-schema`. It states Rules 1 to 8 as observable behavior, with nominal and
  boundary/failure scenarios and verification criteria. Its authored `documentation_files`,
  `agent_skill_files` and `example_files` name real files from surfaces 2, 3 and 6. Real
  `@implements_req`/`@tests_req` markers go on the new code and tests. Check that
  SwRS-OKFSCHEMA-OKFREQ-003, -004 and -005 are still true. Change one only if its statement
  became false.
- `requirements/tiers/_schema/base.schema.yaml`: the `scenarios` property (Rule 2).
- `requirements/tiers/log.md`: one entry under today's `## YYYY-MM-DD` heading (newest first)
  with a `### Topic` sub-heading. It names the new SwRS, the schema change, whether the live mode
  changed and why, and the verification result.
- Whether `requirements/config.yml` switches to the new mode is open question 21. Until the
  answer, it stays `linked-swrs-and-validation-test` (`tests/test_project_contract.py` asserts
  it). The new mode is demonstrated in the disposable showcase, as the project guideline asks for
  alternative policies.
- Then `okfreq update-coverage requirements`, `okfreq lint requirements --prose --check-links
  --project-root .`, `okfreq validate requirements --prose --check-links --project-root .`,
  `okfreq trace requirements --json`.

### 6. Concrete examples: `examples/`

- `examples/okfreq-examples/showcase.py`: a new step, after the existing
  `strict_stakeholder_coverage` step, in the disposable project. Its config already uses custom
  `@delivers`/`@verifies`. Add `markers.accepts: '@accepts'` and switch to the new mode. Declare
  `scenarios:` (S1, S2) on `StRS-DELIVERY-001` and (S1, S2) on one SwRS, then assert in order:
  1. W003 names the StRS before it declares paths, and its block lists the headings the step
     wrote into its body;
  2. a fragmentless `@verifies SwRS-…` is an error that does not count;
  3. an unknown `#S9` is an error;
  4. `paths` go `0/2` → tested `2/2` with `@verifies StRS-DELIVERY-001#S1`/`#S2` → accepted `1/2`
     then `2/2` with `@accepts StRS-DELIVERY-001#S<n>`, and the booleans follow;
  5. the SwRS turns covered only when both transitions are marked;
  6. `report_schema()` validates the report.

  Record `outcomes["acceptance_paths"]`, then restore the earlier mode so the later steps keep
  their meaning.
- The checked-in example (`examples/okfreq-examples/requirements`, `dist/`) keeps the shipped
  default mode. `just refresh-okfreq-examples` regenerates its config (with `markers.accepts`),
  its base schema (with `scenarios`), its guideline copy and `dist/requirements-report*.json`
  (`format_version` 2). These generated diffs are reviewed and kept.
- `examples/okfreq-examples/README.md`: name the new showcase outcome if it lists outcomes.

### 7. Verification and packaging: `tests/`, `justfile`, `pyproject.toml`, CI

- New tests are listed under Evidence. `justfile` and `.github/workflows/ci.yml` (which runs
  `uv run --no-sync -- just preflight`) do not change: no CI job is added or changed, so no CI
  environment needs proving. Packaging does not change: the skills and guideline are already
  shipped resources.

## Out of scope

- The Studio's migration: its `scenarios:` declarations, sorting its 185 markers and writing its
  acceptance tests (Studio CR `strs-path-validation`).
- A migration subcommand (Q8).
- Any bench configuration or bench names in `config.yml` (Q2).
- Test-result ingestion: counters stay linkage, `execution_evidence.status` stays
  `not_collected`.
- Changing `okfreq new`'s templates or making it write `scenarios:` (not asked; open
  question 22).
- Several IDs or fragments on one marker line: one marker per line, as today.
- Changing the behavior of `linked-swrs` or `linked-swrs-and-validation-test` (Rule 1).

## Evidence

### Checks

`tests/test_okfreq.py` (unit, through `okf_schema.okfreq.core`), following
`.github/guidelines/python-unittest.guidelines.md`. Each test builds its bundle with
`init_requirements`/`initialize_bundle` and `create_requirement` in `tmp_path`, edits
`config.yml` the way a user does, and writes real test files with markers:

1. `load_config` accepts the new mode. The refusal of an unsupported mode lists the three modes
   (update the existing `unsupported strs_test_coverage_mode` test).
2. `okfreq init` output: the generated `tiers/_schema/base.schema.yaml` declares `scenarios`
   with the item shape, and the generated `config.yml` has `markers.accepts: '@accepts_req'`.
   The test reads the files `initialize_bundle` writes, not a copy.
3. `marker_scan`: `@accepts_req` is read in `test_dirs` and skipped in `source_dirs`. The
   fragment and line are captured. A custom `markers.accepts` keyword works, and an old
   `config.yml` without `accepts` gets the default. The same ID with two fragments in one file
   gives two occurrences. A malformed fragment (`#path1`, `#`) is captured.
4. Each row of the Rule 4 table, in the new mode: counted or not, error or W004, with the
   message's contents (file:line, configured keyword, declared ids, the request for `#S<n>`).
5. Rule 5: the StRS fractions and booleans for `0/2`, `1/2`, `2/2`, with tested and accepted
   apart (a path tested but not accepted, and the reverse). A SwRS with transitions is covered
   only when all are marked. A SwRS without transitions is covered by a fragmentless marker. An
   exempted SwRS stays out of the population.
6. W003: a StRS whose body has `### Main paths` / `#### Path 1: …` / `#### Path 2: …` gets one
   W003. It names the StRS, quotes both headings, and gives a block with `S1`/`S2` and their
   titles plus the documentation link. A StRS with no heading gets the placeholder block. A
   deprecated or superseded StRS gets none (per the answer to open question 14). Warnings appear
   without `prose=True`.
7. Rule 2 shape errors in the new mode (duplicate id, `P1`, empty title, extra `kind` key via the
   schema). `update_coverage` preserves `scenarios:` byte-for-byte.
8. Rule 7: an approved StRS (approval fields present) that gains only `scenarios:` still
   validates, and its body is unchanged.
9. Rule 8: `report()` has `format_version` 2 in every mode, with `paths`/`tested`/`accepted` and
   `transitions` in the new mode and absent in the others. `Draft202012Validator(report_schema())`
   validates the report of each mode. `write_markdown_report` shows the `Tested`/`Accepted`
   columns with `2/3` in the new mode and the unchanged table in the others.
10. The matrix cells below.

`tests/test_okfreq_cli.py` (Click `CliRunner`):

- `okfreq validate` exits 1 on a fragment error, and exits 0 while printing W003/W004.
- `okfreq lint` fails on the same error.
- `okfreq trace` prints `accepted: N`.
- `okfreq generate-report` writes the columns.

`tests/test_skill_resources.py`: the shipped `skills/okfreq/SKILL.md`,
`skills/okfreq/references/operations.md` and `skills/okfreq-gardening/SKILL.md`, read from the
repository as they ship, mention the new mode, `@accepts_req`, `scenarios:` and `#S<n>`. The
installed-wheel tests keep the references self-contained.

Shipped guideline:

- A test reads `src/okf_schema/data/requirements/guidelines/requirements.guidelines.md` as it
  ships and checks that it states the fragment rule and Rule 7.
- `tests/test_project_contract.py::test_repository_guideline_is_the_installed_shipped_text`
  keeps the repository copy equal to the `okfreq init` output.

Other existing tests:

- `tests/test_examples.py::test_okfreq_showcase_runs_in_an_empty_project` runs the new showcase
  step.
- `tests/test_project_contract.py::test_live_requirements_preserve_complete_real_evidence` still
  passes on the live bundle, including the new SwRS. Its mode assertion changes only if open
  question 21 says so.

Then run `just preflight` (style, lint, `requirements-lint`, changelog, typecheck, guideline
refresh, tests, `refresh-all-examples`, `requirements-report`, docs with `-W`). Review its
generated diffs (examples, `dist/`, guideline copies, `CHANGELOG.md`) before the hand-back.

### Default and configured-value matrix

What this CR changes depends on the shipped default mode and markers versus a configured mode
and markers. There is no host dependency: okfreq is a CLI, with the same behavior under any
agent host. Each cell starts from a real `okfreq init` in a temporary project. A configured cell
edits `config.yml` as a user would. The same fixture is used in each cell: a StRS with
`scenarios:` S1/S2 and `#### Path` headings, a second StRS with no `scenarios:`, a SwRS with
transitions S1/S2, and a test file with `@accepts_req StRS-A#S1`, `@tests_req StRS-B`,
`@tests_req SwRS-A` and `@tests_req SwRS-A#S9`.

| Cell | Configuration | Result it must show |
|---|---|---|
| D1 | Shipped default: `okfreq init` and no edit (`linked-swrs`, default markers incl. `accepts`) | `okfreq validate` 0 errors, no W003/W004, no fragment error. Coverage figures equal to what the same bundle gives with the fragments removed. `format_version` 2, no `paths`/`transitions`. `@accepts_req` counted nowhere. |
| D2 | `strs_test_coverage_mode: linked-swrs-and-validation-test` | As today: `@tests_req StRS-B` counts as StRS-B's validation test, `@accepts_req StRS-A#S1` counts for nothing, and `@tests_req SwRS-A#S9` covers SwRS-A. A further step adds `@tests_req StRS-A#S1` and sees it counted as StRS-A's validation test. No new finding. No `paths`. |
| D3 | `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`, default markers | The Rule 4 table. Validate exits 1 on `SwRS-A` (fragmentless) and `#S9`. W003 on StRS-B. W004 on `@tests_req StRS-B`. StRS-A paths `{total: 2, tested: 0, accepted: 1}`. SwRS-A transitions missing S1, S2. Markdown columns `0/2`, `1/2`. |
| D4 | The new mode with custom `markers.tests: '@verifies'`, `markers.accepts: '@accepts'` (the showcase) | The same results as D3 with the custom keywords, which the messages quote. |
| D5 | The new mode with a `config.yml` written before this change (no `markers.accepts` key) | `@accepts_req` is recognised by default, with the same results as D3. |
| D6 | `strs_test_coverage_mode: unsupported` | `RequirementError` listing the three modes. `okfreq validate` exits non-zero with that message. |

### Scenario steps (manual demonstration for the PR)

In a temporary directory:

1. `okfreq init requirements`, then `okfreq new strs …` and `okfreq new swrs … --derives-from …`.
2. Set the new mode in `requirements/config.yml`, add `### Main paths` / `#### Path 1: …` to the
   StRS body, and add `@tests_req <SwRS>` in `tests/`.
3. `okfreq validate requirements`: W003 quotes the path heading and prints the block.
4. Paste the block, then `okfreq validate requirements` again. The fragmentless `@tests_req` on
   the SwRS is still fine, because the SwRS declares no transitions.
5. Add `@tests_req <StRS>#S1` and `@accepts_req <StRS>#S1`, then
   `okfreq generate-report requirements`: the StRS row shows `Tested 1/1 ✅` and
   `Accepted 1/1 ✅`.
6. Add `scenarios:` S1 to the SwRS. `okfreq validate` exits 1 and asks for `#S<n>` on its
   marker. Fix the marker, and it exits 0.

## Open questions

The answers leave these open. Each comes with a proposal the Driver applies unless the user
decides otherwise.

1. **Mode name.** Q1 says "e.g. `linked-swrs-and-acceptance-paths`". Proposal: that exact name.
2. **What makes a StRS `covered` in the new mode** (its `status`, the aggregate `covered`, and
   the mode description). Is it the linked-SwRS rule plus "tested", plus "accepted", or plus both?
   Proposal: linked-SwRS rule plus "accepted", as the mode name says, with "tested" reported
   beside it.
3. **Outside the new mode:** are malformed `scenarios:` (Rule 2) and unknown or malformed
   fragments errors too, or is everything accepted silently (Q1)? Proposal: silent outside the
   new mode, apart from what the bundle's own JSON Schema refuses.
4. **"Never reused" ids:** guidance only, or a recorded list (like `retired_ids`) that okfreq
   checks? Proposal: guidance only.
5. **Configurable keyword** `markers.accepts`, written by `okfreq init`. Proposal: yes.
6. **Fragment syntax:** `#` directly after the ID, a valid fragment `S[1-9][0-9]*`, the capture
   `[A-Za-z0-9_]*` so that malformed fragments are reported. Proposal: as in Rule 3.
7. **Public JSON key names:** `accepted` and the occurrence list in `okfreq trace --json`,
   `transitions` on a SwRS record. Proposal: `accepted`, `scenario_markers`, `transitions`.
8. **A StRS that declares no path, in the new mode:** is it "tested"/"accepted" at `0/0`, and
   does a fragmentless `@accepts_req StRS-X` on it count, get ignored with a warning (as Q4 does
   for `@tests_req`), or fail? Proposal: `0/0` is neither tested nor accepted (W003 already
   asks for paths), and a fragmentless `@accepts_req` is ignored with W004, like `@tests_req`.
9. **`@accepts_req` on a SwRS** (with or without a fragment). Proposal: an error,
   "`@accepts_req` targets a StRS path only".
10. **`tested_in_files` of a SwRS that declares transitions:** does it leave out the files whose
    markers do not count (Q15)? Proposal: yes, so the generated field agrees with coverage.
11. **Finding codes:** `W003` (live StRS without paths) and `W004` (ignored fragmentless
    `@tests_req StRS-X`); the errors carry no code, as okfreq's structural errors do today.
    Proposal: as written.
12. **Documentation link in W003:**
    `https://okf-schema.readthedocs.io/en/stable/reference/okfreq-frontmatter.html#okfreq-declared-scenarios`
    (`stable` resolves once released). Proposal: that URL.
13. **Heading-reading rule for W003:** every heading below `### Main paths` up to the next `###`
    heading or the generated links block, plus `### Scenario…` headings. The title is the text
    after `Path <n>:` / `Scenario:`, else the whole heading. Proposal: as written.
14. **"Live" StRS for W003:** every lifecycle except `deprecated` and `superseded` (`draft`
    included)? Proposal: yes.
15. **A SwRS with `### Scenario` headings but no `scenarios:`:** no finding (as written), or an
    informational hint with its own block? Proposal: no finding. Q5 and Q13 speak of StRS only.
16. **Approval record for a frontmatter-only `scenarios:` edit on an approved requirement**, in
    the shipped, project-neutral guidance. The Studio's owner already agreed for the Studio.
    Proposal: the guideline says that the project's owner decides whether this metadata change
    needs a new approval record. When it does not, `approved_by`/`approved_at` stay unchanged and
    the log entry names the agreement.
17. **Report schema version:** `format_version` 2 in every mode. Proposal: yes.
18. **StRS `validation_tests` and `tests.files` in the new mode.** Proposal: `tests.files` lists
    the files of counting path markers of both kinds, and `validation_tests` keeps listing direct
    fragmentless `@tests_req` files (now ignored) with status `missing`.
19. **More report detail:** path totals in the aggregate `stakeholder_test_coverage` and the
    Markdown Summary, and a missing-transitions column in the SwRS table. Proposal: add
    `paths_tested`/`paths_accepted`/`paths_total` to the aggregate and one Summary line. Keep the
    SwRS table's columns: its status already reflects transitions, and the JSON lists them.
20. **Version and changelog:** the docstrings say `.. versionchanged:: 0.18.0` (the next minor
    after `v0.17.0`). The commit subject, which `just changelog` turns into the `CHANGELOG.md`
    entry, is `feat(okfreq): measure StRS acceptance paths with declared scenarios`. Is the
    `format_version` 2 a breaking change (`feat(okfreq)!` with a `BREAKING CHANGE:` footer)?
    Proposal: not breaking. The old modes' fields are unchanged and the new ones are optional;
    only consumers that pin `const: 1` notice.
21. **This repository's own mode:** switch `requirements/config.yml` to the new mode (declaring
    real paths on the five StRS, and real `@accepts_req` tests for them), or keep
    `linked-swrs-and-validation-test` and demonstrate the new mode in the showcase? Proposal:
    keep the current mode. Its StRS have no real-bench acceptance tests today, and the project
    guideline forbids nominal evidence.
22. **`okfreq new`:** should it pre-fill `scenarios:` (for example from the SwRS template's two
    `### Scenario:` headings)? Proposal: no, out of scope.
