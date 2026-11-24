# okfreq: acceptance paths, declared scenarios, two StRS counters

Type: feat (okfreq, requirements, docs) · Requested 2026-11-23 by the markdown-okf-schema-studio
Griller from the Studio owner's grill ([request](intake/request.md), [intent](01-intent.md),
[answers](02-answers.md), Q1–Q62) · Forge-neutral (GitHub and GitLab) · One CR, one batch (Q10)
· Grilled enough 2026-11-23, destination `3-ready` (Q17) · Release `0.18.0`, not breaking (Q40).

A new `strs_test_coverage_mode`, `linked-swrs-and-acceptance-paths` (Q24), makes `okfreq`
measure that a StRS is proved by tests that walk its declared main paths, instead of counting
any direct link as a validation test. Requirements declare their main paths (StRS) or their
transition scenarios (SwRS) in one shared frontmatter field, `scenarios:`. Tests name one of
them with a `#S<n>` fragment, mandatory on every marker whose target declares `scenarios:`
(Q53). Two test verbs:

- `@tests_req <ID>#S<n>`: a test of a SwRS transition or of a StRS main path, as today, now
  per scenario;
- `@accepts_req StRS-X#S<n>` (new): the acceptance test of a StRS main path (Q52).

Each StRS gets two independent counters (Q54), "tested" and "accepted". It is covered when its
linked SwRS are covered or individually exempted, and either all its paths are accepted or the
whole StRS has a justified acceptance waiver (U1-U2). A waiver is not acceptance evidence.
okfreq does not check where or how a test runs. The documentation recommends, without enforcing
it, `@accepts_req` on the tests closest to the final product, which may be costly and run in
the main-branch pipeline, and `@tests_req` on cheaper tests run on every pull or merge request;
when the tests are cheap, `@accepts_req` goes directly on them (Q52, Q55). A warning, `W004`,
flags a live, non-waived StRS with no acceptance test (Q56, Q60, U1). The repository applies
the mode to itself, its examples and its documentation (Q21, Q35), and the documentation site
explains the possibilities and why (Q46).

## Goal, in the user's terms

The Studio counts 93 of its 94 live StRS as validated. A 1-in-6 sample of its 185 direct
`@tests_req StRS-...` markers
([audit](../../../../markdown-okf-schema-studio/changes/2-backlog/P2/strs-path-validation/experiments/02-audit-sample.md))
shows that only 13 of 31 walk a StRS main path. A marker is a link, not a proof. The owner
wants `okfreq` to:

1. let a requirement declare its paths or transitions with stable short ids (`S1`, `S2`, never
   reused) and a title, in a `scenarios:` frontmatter field that both tiers share, with no
   `kind`;
2. tell apart, by the marker, a test of a requirement's scenario (`@tests_req`) and the
   acceptance test of a StRS main path (`@accepts_req`);
3. report, per StRS, which fraction of its paths is tested and which is accepted;
4. tell an agent exactly how to declare `scenarios:` when a StRS has none (no migration
   command), and warn when a StRS has no acceptance test;
5. show all of this, and why, in the published documentation, explained by execution cost.

The Studio's own migration (declaring its `scenarios:`, adding `#S<n>` fragments to its
`@tests_req StRS-...` markers, writing its acceptance tests) is the Studio CR
`strs-path-validation`, outside this CR, which waits for this one.

## Starting point (code read on 2026-11-23)

For independent implementations and a fair comparison, start each run on a separate branch
from **`8f56838fd6b4443df602e58c36492d0e56ea34b3`** (`chore: version 0.17.0`, v0.17.0).
This was `refs/remotes/origin/main` when the implementation began; a future fetch may advance
that ref, so the commit, not the current ref, fixes the common starting point. Do not use
another implementation branch, its commits, or its diff as the starting point or as instructions
for a competing run. This document contains the common requirements and decisions; implementations
may choose their own internal design while meeting the observable contract.

At the original interview the local clone was on `dev/gsemet` at `89b52ad` (0.16.0). A local
branch named `origin/main` shadowed the remote-tracking branch, and local `main` was behind; use
the full commit ID rather than those short names. The baseline contains
`feat(okfreq)!: keep requirement bundles native OKF v0.2 bundles`. Everything below describes
that baseline unless a rule says otherwise; function names identify existing integration points.

`src/okf_schema/okfreq/core.py`:

- `STRS_TEST_COVERAGE_MODES = ("linked-swrs", "linked-swrs-and-validation-test")`,
  `STRS_TEST_COVERAGE_DESCRIPTIONS`, `_strs_test_coverage_mode` (refuses other values with
  `unsupported strs_test_coverage_mode: <mode>; expected one of: <list>`).
- `DEFAULT_CONFIG` (written by `okfreq init`) lists `markers: {implements: '@implements_req',
  tests: '@tests_req', id_pattern: ...}` and `generated_fields: [derived_by, supersedes,
  implemented_in_files, tested_in_files, default_owner_email, status, verified]`;
  `SUPPORTED_GENERATED_FIELDS` is the same set; `load_config` fills the same defaults
  (`generated_fields` defaults to every supported field).
- `LIFECYCLE_DESCRIPTION`, the base schema's `req_lifecycle` description written by
  `schema_text("base")`, says of `approved`: "Any significant change (normative statement,
  scenarios, criteria, deprecation or supersession) needs the owner's explicit, justified
  agreement, recorded in approved_by and approved_at". This repository's
  `requirements/tiers/_schema/base.schema.yaml` carries the same text, and so does the
  `approved` row of the "Lifecycle states" table of `docs/source/reference/okfreq-frontmatter.md`.
  Three other texts tell an agent whose task changes an approved requirement to set
  `approved_by` to the owner's email and `approved_at` to the current date and time: the
  guideline's bullet "When the task asks you to change an approved requirement…" ("Lifecycle
  and approval"), the paragraph "A coding agent never approves a requirement…" of
  `docs/source/reference/okfreq-frontmatter.md`, and the bullet "**`approved` belongs to the
  owner.**" of `skills/okfreq/SKILL.md` ("only the owner agrees to approve or change one,
  recorded in `approved_by` and `approved_at`").
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
  findings are errors (no prefix), `W…` warnings (`W001`/`W002`, as `W00n <file>: …`, only with
  `--prose`) and `I…` infos. `okfreq validate` and `okfreq lint` fail on errors.
- `update_coverage` writes the generated `implemented_in_files`/`tested_in_files` on SwRS from
  `marker_scan`, each only when listed in `generated_fields`, and removes both from StRS. The
  scaffolded `swrs.schema.yaml` declares them ("Generated source paths." / "Generated test
  paths.") as arrays with `x-okf-link: {resolution: project-relative, syntax: plain,
  basename_marker: '@implements_req' | '@tests_req', id_marker: id, show_line_number: true}`:
  generated fields are how a marker reaches a tier schema today. The scaffolded
  `strs.schema.yaml` declares neither, and its description says a StRS carries no
  implementation or coverage fields.
- `retire_requirement` (`okfreq retire`) refuses when a marker of kind `implemented`, `tested`
  or `validation_tests` names the ID.
- `report(root)` builds each StRS's `stakeholder_test_coverage` (`status`, `mode`,
  `linked_swrs`, `validation_tests`); a StRS record's `tests` follows `validation_tests`. Each
  record's `diagnostics.errors` lists the `validate_requirements` findings containing its ID,
  `W…` and `I…` findings excluded. The aggregate `marker_coverage` and
  `legacy.marker_coverage` copy the scan (`implemented`/`tested` counts, `missing_ids`,
  `duplicates`, `non_leaf`, `warnings`, `missing_implementation`, `missing_tests`,
  `validation_tests`, `exemptions`). `"format_version": 1`; `report_schema()` declares
  `const: 1`; it is **only written** (`write_report_schema`, by `okfreq generate-report`),
  never checked at run time. `write_markdown_report` renders "By stakeholder requirement"
  (`| Scope | Tier | ID | Name | Tests |`) and "By software requirement"
  (`| Scope | Tier | ID | Name | Source | Tests |`).
- `initialize_bundle`'s `schema_text("base" | "strs" | "swrs")` generates the three schemas;
  `okfreq init` never replaces existing ones. Every shipped schema keeps
  `additionalProperties: true`, so nothing refuses `scenarios:` today.
- `create_requirement` writes the body from `ears_body`: `_SWRS_BODY` has two
  `### Scenario: <…>` headings; `_STRS_BODY` has no path section, and has a `## User Need`
  heading between its `### Preserved stakeholder intent` and `### Rationale and constraints`
  sections.

`src/okf_schema/okfreq/cli.py`: `validate`, `lint`, `trace` (summary
`implemented: N; tested: N; missing IDs: N`), `update-coverage`, `generate-report`, `new`,
`retire`.

This repository: `requirements/config.yml` uses `linked-swrs-and-validation-test`, lists the
seven `generated_fields` above and no `retired_ids`;
`tests/test_project_contract.py::test_live_requirements_preserve_complete_real_evidence`
asserts that mode, zero findings and full stakeholder coverage. It has 5 StRS (all
`proposed`, none with a `### Main paths` section) and 29 SwRS (CORE 9, OKFKB 6, OKFREQ 14),
every one with `### Scenario:` headings, 93 in all; the next SwRS of scope `okfreq` is
`SwRS-OKFSCHEMA-OKFREQ-015`. Six real direct StRS markers exist in `tests/`:
`tests/test_examples.py` (`StRS-OKFSCHEMA-OKFREQ-001`), `tests/test_file_links.py`
(`StRS-OKFSCHEMA-CORE-003`), `tests/test_integration.py` (`CORE-002`, `CORE-001`,
`OKFKB-001`) and `tests/test_okfreq.py` (`OKFREQ-001`). `tests/test_skill_resources.py`
already runs the shipped product:
`test_installed_wheel_commands_install_complete_families_without_source_checkout` builds the
wheel (`uv build --offline --wheel`), installs it in an isolated venv and runs the installed
console scripts as subprocesses with no source checkout on the path.

`just docs` runs `just changelog` then `sphinx-build -W -b html docs/source docs/_build/html`
(warnings fail). The changelog is generated by `cz` from commit subjects.

## Decisions carried (from `02-answers.md`)

| Q | Decision | Where |
|---|---|---|
| Q1 | A new mode value activates the feature; without it, `scenarios:` and the new marker are accepted but nothing is required or counted. | Rule 1 |
| Q2 | No bench configuration: the marker says what a test is. Since Q52/Q55, `@accepts_req` declares acceptance and `@tests_req` a test; where a test runs is the project's choice. | Rules 3, 5 |
| Q3 | One fraction of paths per counter; the StRS is "tested"/"accepted" when its fraction is complete. | Rule 5 |
| Q4 | Superseded by Q19. | — |
| Q5 | Error for an unknown `#S<n>`; warning for a live StRS with no declared path. | Rule 6 |
| Q6 | A path is "tested" by a `@tests_req` marker with `#S<n>` (Q52). | Rules 4, 5 |
| Q7 | A SwRS with declared transitions is covered only when each has a `@tests_req SwRS-X#S<n>`. | Rules 4, 5 |
| Q8 | No migration subcommand; okfreq's message tells agents how to declare `scenarios:`. | Rule 6 |
| Q9 | On an approved StRS: frontmatter-only edit, body intact, logged in `tiers/log.md`. | Rule 7 |
| Q10 | One CR, one batch. | Header |
| Q11 | New mode only, StRS and SwRS alike; once declared, each scenario must be covered. Refined by Q14/Q19/Q53. | Rules 1, 4, 5 |
| Q12 | JSON and Markdown, version incremented; per StRS `paths: {total, tested, accepted}` and two booleans; per SwRS tested and missing transitions; two Markdown columns. | Rule 8 |
| Q13 | Detailed agent message: StRS named, headings quoted, `scenarios:` block to paste, doc link. | Rule 6 |
| Q14 | When `scenarios:` is declared, every marker targeting it must carry `#S<n>`; both verbs, both tiers (Q53). | Rule 4 |
| Q15 | A missing fragment there is an error: `okfreq validate` fails, the marker does not count. | Rules 4, 6 |
| Q16 | All six surfaces of `AGENTS.md` plus `docs/source/explanation/project-feature-coverage.md`. | Surfaces |
| Q17 | Grilled enough; next batch. | Header |
| Q18 | In the new mode a StRS is covered by the linked-SwRS rule plus "accepted"; U1 later adds a justified whole-StRS waiver as an alternative to acceptance. | Rule 5 |
| Q19 | Same for StRS and SwRS, and for both verbs (Q53): `scenarios:` declared → a fragmentless marker is an error; not declared → fragmentless markers count. W003 stays. | Rules 4, 5 |
| Q20 | `@accepts_req` on a SwRS is an error, enforced in the JSON Schema. | Rules 4, 6 |
| Q21 | okf-schema applies the mode to its own requirements. | Surface 5 |
| Q24 | Mode name `linked-swrs-and-acceptance-paths`. | Rule 1 |
| Q25 | Outside the new mode: silent for a malformed `scenarios:` or unknown fragment, apart from what the bundle's own JSON Schema refuses. | Rule 1 |
| Q26 | "Ids never reused": documentation only; okfreq checks nothing. | Rule 2 |
| Q27 | `markers.accepts`, configurable, written by `okfreq init`. | Rule 3 |
| Q28 | `#` glued to the ID; only `S<n>` is a fragment; any other suffix is ignored as today; an unknown `S<n>` is an error. | Rule 3 |
| Q29 | JSON keys `accepted`, `scenario_markers` (`trace --json`), `transitions` (SwRS record). | Rules 3, 8 |
| Q30 | `tested_in_files` of a SwRS with transitions lists only files with a counting marker. | Rule 5 |
| Q31 | Errors carry no code. The warnings are `W003` and, since Q56/Q60, `W004`. | Rule 6 |
| Q32 | W003 link `https://okf-schema.readthedocs.io/en/stable/reference/okfreq-frontmatter.html#okfreq-declared-scenarios`. | Rule 6, surface 2 |
| Q33 | Headings read for W003: every heading under `### Main paths`, plus `### Scenario…`; title after `Path <n>:` / `Scenario:`, else the whole heading. Reading under `### Main paths` stops at the next heading of level 1 to 3 or at the generated links block. U4 adds headings with explicit scenario IDs. | Rule 6 |
| Q34 | Live = every lifecycle except `deprecated` and `superseded`; used by W003 and W004. | Rule 6 |
| Q35 | No warning for a SwRS with `### Scenario` headings and no `scenarios:`; instead the CR migrates the project, its examples and its docs correctly. | Rule 6, surfaces 2, 5, 6 |
| Q36 | Approval for a `scenarios:`-only edit: the owner decides; without new approval `approved_by`/`approved_at` stay and the log names the agreement. | Rule 7 |
| Q37 | `format_version` 2 in every mode. | Rule 8 |
| Q38 | Superseded by Q42. | — |
| Q39 | Path totals in the aggregate, one Markdown summary line, a "Missing transitions" column in the SwRS table. | Rule 8 |
| Q40 | `0.18.0`, `feat(okfreq): …`, not breaking. | Surface 1, Evidence |
| Q41 | `okfreq new` pre-fills `scenarios:` from the template headings, in the new mode only; the old modes' output stays byte-identical (Q59). | Rule 9 |
| Q42 | Per StRS `acceptance_tests` (`@accepts_req` files); `validation_tests` kept for backward compatibility. | Rule 8 |
| Q43 | Superseded by Q55. | — |
| Q44 | Superseded by Q52. | — |
| Q45 | Superseded by Q52. | — |
| Q46 | Document this part well; the built documentation site shows the possibilities and why. | Surface 2 |
| Q47 | Superseded by Q52. | — |
| Q48 | In the new mode, a bundle whose `swrs.schema.yaml` does not refuse `accepted_in_files` makes `okfreq validate` fail with an error asking the project to update its bundle schema (property and 0.18.0 declaration named). No shipped default, no silent fallback. | Rules 4, 6 |
| Q49 | In the new mode a StRS's `validation_tests` has the same files and status as its `acceptance_tests`. | Rule 8 |
| Q50 | The checked-in example moves to the new mode with a real acceptance test of its export (`Accepted 1/1`); its README and the showcase follow. Spec-writer's choice, not an answer: `test_export_rows` carries `@tests_req StRS-CORE-001#S1`. U5 adds a second, commented slow acceptance test. | Surface 6 |
| Q51 | The 5 StRS main paths are the spec-writer's proposed ones; the PR lists them for the owner's review. | Surface 5 |
| Q52 | No `@simulates_req`, no `markers.simulates`. `@tests_req` on a StRS is valid; `@accepts_req` declares a StRS's acceptance coverage. `@accepts_req` on the tests closest to the final product and `@tests_req` on others is a recommendation, not an obligation. | Rules 3, 4, surface 2 |
| Q53 | One fragment rule for both verbs on a StRS and `@tests_req` on a SwRS: when the target declares `scenarios:`, `#S<n>` is mandatory (error otherwise; the marker does not count). | Rule 4 |
| Q54 | Independent counters: a path with only `@accepts_req` is accepted, not tested; one with only `@tests_req` is tested, not accepted. | Rule 5 |
| Q55 | No bench vocabulary. The docs explain execution cost: costly → `@accepts_req` in the main-branch pipeline and `@tests_req` on a cheaper test in the pull or merge request pipeline; cheap → `@accepts_req` on the tests directly. Generated fields `accepted_in_files` and, on a StRS, `tested_in_files` (as on a SwRS). | Rules 4, 5, 8, surface 2 |
| Q56 | Documentation, plus a warning when a StRS has no `@accepts_req` marker. | Rule 6, surface 2 |
| Q57 | `@accepts_req` markers naming an ID also block `okfreq retire`, in every mode. | Rule 1, surface 1 |
| Q58 | In the new mode `marker_coverage.*`, `legacy.marker_coverage.*` and each SwRS's `tests.files` hold only the markers that count. | Rule 8 |
| Q59 | `okfreq new` pre-fills `scenarios:` in the new mode only; old-mode output byte-identical. | Rule 9 |
| Q60 | `W004`: a live StRS with no valid `@accepts_req` marker at all; the message points to the documentation on execution cost; independent of W003. U1 later suppresses W004 for a justified whole-StRS acceptance waiver. | Rule 6 |
| Q61 | Old modes: `update-coverage` removes `tested_in_files` and `accepted_in_files` from a StRS whatever `generated_fields` says. New mode: it writes each when listed in `generated_fields` and leaves it untouched when not. | Rules 1, 5 |
| Q62 | Keep `stakeholder_test_coverage.tests` (`@tests_req` files); the reference page states how it differs from the StRS record's `tests` (which follows `validation_tests`, the `@accepts_req` files). | Rule 8, surface 2 |

The request's point 3 named benches "in the project's config" and used `@accepts_req` for both
benches; Q2 replaces the config, Q52 keeps `@tests_req` for tests of a StRS and
`@accepts_req` for its acceptance, and Q55 replaces the benches by an execution-cost
recommendation. The request's point 5 (migration help) became an okfreq message (Q8, Q13).

### Decisions made during implementation

These later user decisions refine the interview above and take precedence over a conflicting
earlier formulation:

| Decision | User request and resulting contract | Where |
|---|---|---|
| U1 | Consolidation is an interactive agent skill, not a feature for which to invent a dedicated CLI command or fake automated acceptance test. The user asked for a frontmatter waiver with a reason when the requirement cannot be acceptance-tested and said it must not be counted uncovered for that reason alone. The user chose a waiver for the whole StRS, not one scenario, and asked for clear documentation of why and when to use it. | Rules 2, 5, 6, 8; surfaces 2-5 |
| U2 | The SwRS for interactive consolidation also needs its own explicit, justified annotation exemption; a StRS waiver does not waive its children. | Rule 5; surface 5 |
| U3 | Acceptance of file-link navigation uses the installed wheel's API from an isolated subprocess, rather than inventing a navigation command; the link-checking path still uses the installed command. | Surface 5 |
| U4 | Scenario IDs and names should agree between frontmatter and Markdown headings. Reinforce this as authoring guidance and align the repository's existing requirements and examples; do not make heading equality a new general validation rule. IDs stay stable and are not renumbered when scenarios are reordered or removed. | Rules 6-7, 9; surfaces 2-6 |
| U5 | Show two acceptance-test variants for the same StRS: one fast, executable test and one slow test entirely in comments, with no implementation. The commented example must not be counted as evidence. | Surface 6; Evidence |

The field names and report shapes in the rules below make these decisions an explicit,
reimplementable contract; they are design choices, not words attributed to the user. For the
original implementation run the user also requested a GitHub pull request titled with
`[Fusion]`, the session cost in its description, and a passing CI. Those are delivery
instructions for that run, not product behavior or a model-independent label for every
competing implementation.

## The rules

"The new mode" means `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`. "The old
modes" are `linked-swrs` (the shipped default) and `linked-swrs-and-validation-test`.
"Counting" marker: a marker that Rule 4 counts (not an error).

### Rule 1: activation (Q1, Q11, Q24, Q25, Q57, Q61)

- `STRS_TEST_COVERAGE_MODES` gains `linked-swrs-and-acceptance-paths`. Its description
  explains the linked-SwRS condition, including justified SwRS annotation exemptions; the
  acceptance condition, including the justified whole-StRS waiver; the fragmentless fallback
  when no paths are declared; and the separate tested counter. The same description is written
  in `coverage_definition.stakeholder_tests` and the Markdown note below the StRS table.
  `load_config` and `_strs_test_coverage_mode` accept the mode; the refusal lists all three.
- In the old modes okfreq accepts `scenarios:` and `@accepts_req` and requires and counts
  nothing new. Coverage, generated fields and findings stay as today, apart from the
  every-mode changes below: `@accepts_req` counts
  toward nothing, `@tests_req StRS-X` (with or without suffix) is still the validation test of
  `linked-swrs-and-validation-test`, and a suffix on any marker is ignored, as today. The only
  refusals are those of the bundle's own JSON Schema on the frontmatter (Rule 2's schema
  property) (Q25). `okfreq new` is unchanged in the old modes (Rule 9).
- **Every-mode changes**, intended, and the only ones:
  1. `report()`'s `format_version` 2 and `report_schema()`'s `const: 2`, the new mode in its
     mode enums, and its new optional properties (Q37, Rule 8);
  2. `marker_scan` reads `@accepts_req` (`markers.accepts`) in `test_dirs`: `okfreq trace`'s
     summary line gains `accepted: N`, and `trace --json` gains the keys `accepted` and
     `scenario_markers` (Rule 3);
  3. an `@accepts_req` naming an unknown ID goes to `missing_ids`, like any marker today;
  4. two marker kinds configured with the same keyword is a `RequirementError` (Rule 3);
  5. `okfreq retire` is refused when an `@accepts_req` marker names the ID (Q57);
  6. `accepted_in_files` is a supported generated field that `okfreq init` lists (Rule 5); in
     the old modes `update_coverage` writes it on no requirement and removes both
     `tested_in_files` and `accepted_in_files` from a StRS whatever `generated_fields` says,
     as it removes `tested_in_files` there today (Q61);
  7. the schemas, `config.yml` and shipped guideline (`guidelines/requirements.guidelines.md`,
     surface 4) that `okfreq init` writes (Rules 2, 3, 4, 7); `okfreq init` still never
     replaces an existing bundle's schemas or `config.yml`, and replaces an existing installed
     guideline only with `--force`, as today.
- Rules 4 to 6, 8 (new fields) and 9 apply in the new mode only.

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
  `scenarios:`. In the new mode only, okfreq also checks in code what the counters depend on:
  a list of mappings, `id` matching `S[1-9][0-9]*`, ids unique (JSON Schema cannot express
  it), non-empty `title`. Error:
  `<file>: scenarios: <problem> (each entry is {id: S<n>, title: <text>}, ids unique)`. In the
  old modes none of these code checks runs (Q25).
- `update_coverage` preserves the field (authored, never generated); `_render_frontmatter`
  already keeps unknown keys. A test proves it.

#### Authored StRS acceptance waiver (U1)

- Declare optional `acceptance_exemption` (boolean) and
  `acceptance_exemption_reason` (string) in the generated and repository StRS schemas. If
  `acceptance_exemption` is `true`, a reason is required and must be non-empty; in the new
  mode validation also rejects whitespace-only reasons. Like other bundle schema checks, the
  generated schema's type and conditional-required checks apply in every mode; existing bundle
  schemas are not silently replaced.
- Both fields are authored frontmatter, never generated; `update-coverage` preserves them.
  A waiver is effective only in the new mode when the flag is true and the reason is a
  non-blank string. A missing or false flag is not a waiver. The reason explains why automated
  acceptance is not possible, rather than asserting that acceptance happened.
- It applies to the complete StRS, not an individual `scenarios:` entry. It does not create an
  acceptance marker, change `accepted` or any path count, or relax the linked-SwRS rule,
  fragment errors, scenario declarations, or W003. Rule 5 defines its effect on coverage;
  Rule 6 defines its effect on W004; Rule 8 defines its report.
- Documentation says the owner reviews the exemption under the project's approval rules,
  removes it when no longer justified, and does not use it to hide an acceptance test that
  can be written. okfreq does not collect or verify that approval. Being slow or expensive
  alone is not a reason to waive acceptance.

### Rule 3: markers and the fragment (Q2, Q27, Q28, Q29, Q52)

- Three marker kinds; two are test markers, read only in `test_dirs` (skipped in
  `source_dirs`, as a test marker is today):

  | Config key | Default keyword | Meaning |
  |---|---|---|
  | `markers.implements` | `@implements_req` | implementation of a SwRS (unchanged; `source_dirs`) |
  | `markers.tests` | `@tests_req` | test of a SwRS or a StRS, or of one of its scenarios |
  | `markers.accepts` | `@accepts_req` | acceptance test of a StRS, or of one of its main paths (Q27, Q52) |

- `DEFAULT_CONFIG` lists `accepts`, so `okfreq init` writes it. `load_config` defaults it even
  when an existing `config.yml` lists only `implements` and `tests`. Two kinds configured with
  the same keyword is a `RequirementError` (`markers.<a> and markers.<b> use the same keyword
  <kw>`), since the kind would be ambiguous.
- The marker regex of `marker_scan` becomes:

  ```text
  ^\s*(?:(?:#|//|/\*|\*|<!--)\s*)?(?P<marker>implements|tests|accepts)\s+
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
  - `accepted`: ID → files of `@accepts_req` markers (Q29);
  - `scenario_markers`: one entry per (kind, ID, fragment, file), with the first line:
    `{"marker": "tests" | "accepts", "id", "fragment": "S1" | null, "file", "line"}` (Q29).
    Messages need the line.
  A `@tests_req` on a StRS still goes to `validation_tests` (the old modes read it there); an
  unknown ID of either test kind goes to `missing_ids`, as today. The `marker_scan` doctest
  lists the new keys. `marker_scan` takes no mode, so its `validation_tests` stays the raw
  files of `@tests_req` markers on a StRS in every mode, and so does `okfreq trace --json`'s.
  In the new mode the report's `validation_tests` (`marker_coverage`,
  `legacy.marker_coverage`, per StRS) holds the counting `@accepts_req` files instead (Q49,
  Q58, Rule 8). This difference is kept, not fixed: changing the scan's key would change
  `trace --json` in a way no answer asks for and break Rule 3's "every existing key keeps its
  meaning"; the reference page and `okfreq-cli.md` document it (surface 2).
- `okfreq trace` prints `implemented: N; tested: N; accepted: N; missing IDs: N`; `--json`
  prints the whole scan.

### Rule 4: what each marker does

Old modes (Rule 1): today's behavior; `@accepts_req` counts toward nothing; no new finding.

Rules 4 to 6 apply to StRS and SwRS targets only. A marker on any other tier (a tier a project
adds, see `docs/source/reference/okfreq-configuration.md`, "Extending tiers and fields") keeps
today's handling, with no fragment check, no merge into its frontmatter and no new finding: a
`@tests_req` on a tier that is a parent of another goes to `non_leaf`, and on a leaf tier
counts as `marker_scan` counts it today (`_leaf_levels`); an `@accepts_req` on it counts
toward nothing.

New mode: **one fragment rule for every test marker** (Q53). When the targeted requirement
declares `scenarios:`, a `@tests_req` or `@accepts_req` on it must carry a declared `#S<n>`;
when it declares none, a fragmentless marker counts for the whole requirement and any `S<n>`
fragment is an error. "Fragmentless" includes a marker whose suffix is not `S<n>` (Rule 3).

| Marker | Target declares `scenarios:` | Target declares none |
|---|---|---|
| `@tests_req StRS-X#S<n>`, `S<n>` declared | path `S<n>` **tested** (Q6, Q52) | — |
| `@accepts_req StRS-X#S<n>`, `S<n>` declared | path `S<n>` **accepted** | — |
| `@tests_req` / `@accepts_req StRS-X#S<n>`, `S<n>` not declared | **error**, does not count (Q5, Q28) | **error**, does not count (Q28) |
| `@tests_req StRS-X` fragmentless | **error**, does not count (Q14, Q19, Q53) | counts: StRS **tested** (Q19, Q52) |
| `@accepts_req StRS-X` fragmentless | **error**, does not count (Q19, Q53) | counts: StRS **accepted** (Q19) |
| `@tests_req SwRS-X#S<n>`, `S<n>` declared | transition `S<n>` tested (Q7) | — |
| `@tests_req SwRS-X#S<n>`, `S<n>` not declared | **error**, does not count (Q5) | **error**, does not count (Q28) |
| `@tests_req SwRS-X` fragmentless | **error**, does not count (Q14, Q15, Q53) | covers the whole SwRS, as today (Q19) |
| `@accepts_req SwRS-X`, any suffix | **error**, from the SwRS schema (Q20, below) | same |
| `@implements_req SwRS-X` | unchanged | unchanged |

**How Q20 is "in the JSON Schema".** The code enforces a JSON Schema at run time in one place
only, `validate_requirements`, on a requirement's frontmatter; `report_schema()` is never
checked. A marker reaches a tier schema only as a marker-derived frontmatter property, the way
`tested_in_files` carries `@tests_req` files and is declared in `swrs.schema.yaml` with
`x-okf-link.basename_marker: '@tests_req'`. So:

- One new marker-derived property, `accepted_in_files`: the files of `@accepts_req` markers
  that target the requirement. It is a generated field (Rule 5, Q55).
- `strs.schema.yaml` (scaffold `schema_text("strs")` and `requirements/tiers/_schema/`)
  declares on a StRS `tested_in_files`, with exactly the declaration `swrs.schema.yaml` already
  has for it (array of strings, `x-okf-link: {resolution: project-relative, syntax: plain,
  basename_marker: '@tests_req', id_marker: id, show_line_number: true}`, "Generated test
  paths."), and `accepted_in_files`, the same with `basename_marker: '@accepts_req'` and the
  description "Generated acceptance-test paths: files of @accepts_req markers that count, in
  mode linked-swrs-and-acceptance-paths." Its top-level description changes from "does not
  carry implementation or source coverage fields" to: a StRS carries no implementation fields;
  in mode `linked-swrs-and-acceptance-paths` it carries the generated `tested_in_files` and
  `accepted_in_files`.
- `swrs.schema.yaml` (both copies) keeps its `tested_in_files` and refuses `accepted_in_files`:

  ```yaml
  accepted_in_files:
    type: array
    maxItems: 0
    description: Never present. @accepts_req names a StRS main path; mark a SwRS test
      with @tests_req <SwRS-ID>#S<n>.
  ```

- In the new mode, `validate_requirements` validates each StRS and SwRS frontmatter **with
  `accepted_in_files` replaced by its marker-derived value** (the files of every `@accepts_req`
  naming it, from `marker_scan`, when non-empty) against its tier schema. An error on this
  property is reported per marker with the schema's own `description`:
  `<test file>:<line>: @accepts_req SwRS-X: Never present. @accepts_req names a StRS main path;
  …` (the configured keyword is used). The rule's text and its tier live in the schema.
- Outside the new mode no merge happens, so `@accepts_req SwRS-X` is accepted and counts
  nothing (Q1, Q25).
- **A bundle whose `swrs.schema.yaml` does not refuse `accepted_in_files`** (Q48). `okfreq
  init` never replaces schemas, so a bundle created before 0.18.0 (the Studio's) does not
  declare it. In the new mode `validate_requirements` checks that the SwRS tier schema, as it
  composes it, refuses the property (a SwRS frontmatter carrying it with one file is refused on
  that property). When it does not (the property is not declared, or its declaration accepts a
  file), `okfreq validate` fails with one error, whether or not a marker uses it:
  `<swrs.schema.yaml path>: accepted_in_files is not refused; mode
  linked-swrs-and-acceptance-paths needs the okf-schema 0.18.0 declaration: update the bundle
  schema by adding under properties:` followed by the declaration above, exactly the text
  `schema_text("swrs")` writes. okfreq applies no shipped declaration and has no silent
  fallback. Outside the new mode nothing is checked (Rule 1).

### Rule 5: counters and coverage, in the new mode (Q2, Q3, Q7, Q11, Q18, Q19, Q30, Q54, Q55, Q61)

- **StRS that declares `scenarios:`**: `total` = declared paths; `tested` = declared paths with
  at least one counting `@tests_req StRS-X#S<n>`; `accepted` = declared paths with at least
  one counting `@accepts_req StRS-X#S<n>`. **Tested** = `tested == total`; **accepted** =
  `accepted == total` (Q3). The two counters are independent (Q54): a path with only
  `@accepts_req` is accepted and not tested; a path with only `@tests_req` is tested and not
  accepted.
- **StRS that declares none**: `paths` is `{total: 0, tested: 0, accepted: 0}`; **tested** is
  true when at least one fragmentless `@tests_req StRS-X` counts, **accepted** when at least
  one fragmentless `@accepts_req StRS-X` counts (Q19). W003 still asks for paths; W004 flags
  the absence of a counting acceptance marker unless the StRS has a justified waiver (Rule 6).
- **StRS `status` `covered`** = linked-SwRS rule (at least one linked SwRS, each either
  test-covered as below or individually exempted with a non-blank `exemption_reason`) **and
  (accepted or a justified whole-StRS acceptance waiver)** (Q18, U1-U2). "Tested" is reported
  beside it and does not change the status. This drives aggregate
  `stakeholder_test_coverage.covered` and the Markdown line. The waiver changes only this
  policy decision: `accepted` and path counts still reflect actual counting markers.
- **SwRS** (leaf, no `annotation_exemption`): with declared transitions, test-covered only when
  every declared `S<n>` has a counting `@tests_req SwRS-X#S<n>` (Q7); without, test-covered by
  any fragmentless `@tests_req SwRS-X`, as today. This status drives `tests.status`,
  `totals.tested`, the scopes' `tested`, `marker_coverage.missing_tests` and the
  `linked_swrs[].status` of its StRS. Source coverage is unchanged.
- **SwRS annotation exemption** (U2): the existing `annotation_exemption: true` and
  `exemption_reason` exempt that SwRS from its source and test annotation coverage. In the new
  mode a linked SwRS with a non-blank reason satisfies its parent's linked-SwRS condition and
  is reported as `exempt`, not `covered`; a missing or blank reason cannot satisfy it. This
  does not waive its parent's acceptance condition. Conversely, a StRS acceptance waiver
  neither exempts nor fabricates evidence for any SwRS. Old-mode behavior remains unchanged.
- **Generated fields** (Q30, Q55, Q61). `SUPPORTED_GENERATED_FIELDS` and `DEFAULT_CONFIG`'s
  `generated_fields` gain `accepted_in_files`. In the new mode `update_coverage` writes each of
  these fields only when it is listed in `generated_fields`, like every generated field, and
  leaves it untouched (an existing value stays, none is added) when it is not listed (Q61):
  - on a SwRS, `tested_in_files` lists only the files of its counting `@tests_req` markers
    (Rule 4): its fragmentless markers when it declares no transitions, its markers with a
    declared `#S<n>` when it does (Q30); a rejected marker's file is not listed;
  - on a StRS, `tested_in_files` (files of its counting `@tests_req`) and `accepted_in_files`
    (files of its counting `@accepts_req`), sorted, as on a SwRS.
  `update_coverage` still removes `implemented_in_files` from a StRS in every mode, as today.
  These are generated-field updates like `derived_by` on a StRS today: `_approval_findings` is
  unchanged. In the old modes `update_coverage` also removes `tested_in_files` and
  `accepted_in_files` from a StRS whatever `generated_fields` says (Rule 1, Q61).

### Rule 6: findings and messages (Q5, Q8, Q13, Q15, Q31–Q35, Q48, Q53, Q56, Q60)

In the new mode `validate_requirements` calls `marker_scan` (it does not today), so
`okfreq validate` and `okfreq lint` fail on these errors (Q15), `okfreq status` counts them, and
`report()` lists each in the `diagnostics.errors` of the requirement whose ID it contains.
Errors carry no code; the warnings are `W003` and `W004` (Q31, Q56, Q60), printed as
`W00n <file>: …` like `W001`/`W002`, with or without `--prose`; they never change the exit
code. Messages use the configured keywords.

- **Fragment missing** (Q19, Q53): `<file>:<line>: @tests_req SwRS-X has no scenario fragment;
  SwRS-X declares scenarios S1, S2: write @tests_req SwRS-X#S<n> (this marker does not
  count)`. Same text for `@tests_req` and `@accepts_req` on a StRS that declares paths.
- **Unknown fragment** (Q5, Q28): `<file>:<line>: @accepts_req StRS-X#S4 names no declared
  scenario of StRS-X (declared: S1, S2)`; when none is declared the message ends `(StRS-X
  declares no scenarios:)`.
- **`@accepts_req` on a SwRS** (Q20): Rule 4's schema-driven error.
- **SwRS schema that does not refuse `accepted_in_files`** (Q48): Rule 4's
  update-the-bundle-schema error.
- **Malformed `scenarios:`**: Rule 2.
- **`W003`, live StRS with no `scenarios:`** (Q5, Q8, Q13, Q32–Q34). Live = any lifecycle but
  `deprecated` and `superseded` (`draft` included). One finding per StRS, addressed to an
  agent. It:
  1. names the StRS and its file;
  2. quotes the headings found in the body (Q33): every heading under `### Main paths` up to
     the next heading of level 1 to 3 (`#`, `##` or `###`; the StRS template has `## User Need`
     between two `###` sections) or the generated links block (`<!-- okf:links:start -->`),
     plus every `### Scenario…` heading; or says none was found;
  3. gives the `scenarios:` block to paste, one entry per heading in order. Understand legacy
     `Path <n>:` / `Scenario:` headings and explicit `Path S<n>:` / `Scenario S<n>:` headings;
     use the title after the prefix and preserve explicit IDs in the suggestion (U4). Assign
     unique `S<n>` IDs without colliding with explicit IDs for other headings; with no heading,
     use one placeholder entry `- id: S1` / `  title: <main path title>`;
  4. says to edit the frontmatter only, and on an approved StRS to log the change in the
     bundle's `tiers/log.md` (Rule 7);
  5. ends with
     `https://okf-schema.readthedocs.io/en/stable/reference/okfreq-frontmatter.html#okfreq-declared-scenarios`.

  The heading reader is one helper (`_scenario_headings(text)`), shared with Rule 9.
- **`W004`, live StRS with no acceptance test** (Q56, Q60, U1). Same "live" as W003. One
  finding per live StRS on which no `@accepts_req` marker counts (none at all, or only
  rejected ones), unless it has a justified whole-StRS acceptance waiver. A StRS with at least
  one counting `@accepts_req` (even `accepted 1/3`) gets none. It is independent of W003: a
  non-waived live StRS with no `scenarios:` and no acceptance test gets both; a waived one
  still gets W003. Text:
  `W004 <file>: StRS-X has no acceptance test: no @accepts_req marker that counts names it.
  Mark the test closest to the final product that walks each main path with
  @accepts_req StRS-X#S<n> (@accepts_req StRS-X while it declares no scenarios:). That test may
  be costly and run in the main-branch pipeline, beside cheaper @tests_req tests run on every
  pull or merge request. See
  https://okf-schema.readthedocs.io/en/stable/explanation/okfreq-acceptance-paths.html#okfreq-execution-cost`.
- **No finding** for a SwRS without `scenarios:`, even with `### Scenario` headings (Q35).
- **In the report**: `report()` keeps dropping `W…` findings from `diagnostics.errors`, as
  today. The facts behind them show in the per-StRS coverage: `paths.total` 0 (W003) and
  `acceptance_tests.status` `missing` when no acceptance marker counts, including for a waived
  StRS where W004 is suppressed.

### Rule 7: approved requirements (Q9, Q36)

Declaring `scenarios:` on an approved requirement is a frontmatter-only edit: the body stays
exactly as it was, and the change is logged in the bundle's `tiers/log.md`. The project's owner
decides whether this metadata change needs a new approval; without a new approval,
`approved_by`/`approved_at` stay unchanged and the log entry names the agreement (Q36). This is
guidance (guideline, skills, docs, W003 message), not a check: `_approval_findings` is
unchanged. Two kinds of text gain this exception for an edit that only adds `scenarios:` (Q36):

- the texts that say any change of an approved requirement's scenarios needs the owner's
  agreement recorded in `approved_by`/`approved_at`: `LIFECYCLE_DESCRIPTION` (scaffold, surface
  1, and this repository's `requirements/tiers/_schema/base.schema.yaml`, surface 5) and the
  `approved` row of the frontmatter reference's "Lifecycle states" table (surface 2);
- the texts that tell an agent whose task changes an approved requirement to set `approved_by`
  to the owner and `approved_at` to now: the guideline's bullet "When the task asks you to
  change an approved requirement…" in "Lifecycle and approval" (surface 4), the paragraph "A
  coding agent never approves a requirement…" of `docs/source/reference/okfreq-frontmatter.md`
  (surface 2), and the bullet "**`approved` belongs to the owner.**" of
  `skills/okfreq/SKILL.md` (surface 3). Each says that an edit that only adds `scenarios:`
  leaves `approved_by`/`approved_at` unchanged unless the owner gives a new approval, and is
  logged in `tiers/log.md` naming the agreement.

A test proves an approved StRS that gains only `scenarios:` still validates. The Studio's owner
has already agreed for the Studio.

U4's heading alignment can change the body. It is not part of this frontmatter-only exception:
for an approved requirement, obtain the owner's agreement under the normal approval rules and
record the change; never silently alter approval fields. A waiver is also authored metadata and
does not grant approval to edit an approved requirement.

### Rule 8: the report (Q12, Q29, Q37, Q39, Q42, Q49, Q55, Q58, Q62)

- `"format_version": 2` in `report()` and `"const": 2` in `report_schema()`, in every mode
  (Q37). The mode enums follow `STRS_TEST_COVERAGE_MODES`. Every new property is optional in the
  schema, so old-mode reports keep their shape apart from the version.
- New mode, per StRS, `stakeholder_test_coverage` gains:

  ```json
  "paths": {"total": 3, "tested": 2, "accepted": 1},
  "tested": false,
  "accepted": false,
  "tests": {"status": "defined", "files": ["tests/test_flow.py"], "count": 1},
  "acceptance_tests": {"status": "defined", "files": ["tests/test_acceptance.py"], "count": 1}
  ```

  `tests` lists the files of the **counting** `@tests_req` markers on the StRS (its generated
  `tested_in_files`), named like the SwRS record's `tests` (Q55, Q62); `acceptance_tests` lists the
  files of the counting `@accepts_req` markers (its `accepted_in_files`, Q42). Both are shaped
  like `validation_tests` (`status` `defined`/`missing`). `validation_tests` stays, required,
  for backward compatibility (Q42); in the new mode it has the same files and status as
  `acceptance_tests` (Q49). The StRS record's own `tests.files`/`count` keep following
  `validation_tests`, as the code does today, so in the new mode they hold the `@accepts_req`
  files, while `stakeholder_test_coverage.tests` holds the `@tests_req` files (Q62); the
  reference page (surface 2) states this difference.
- When a StRS has a justified acceptance waiver, include
  `"acceptance_exemption": {"reason": "<authored reason>"}` in its
  `stakeholder_test_coverage` (U1). Omit it otherwise. Do not change `accepted`,
  `acceptance_tests`, `validation_tests`, or `paths.accepted`: actual markers alone determine
  those. Include waived StRS in the aggregate path denominator and count only actual accepted
  paths. A linked SwRS with its own justified annotation exemption has `linked_swrs[].status`
  `exempt` (U2).
- New mode, only counting markers (Q58): the aggregate `marker_coverage` and
  `legacy.marker_coverage` are built from the counting markers: `validation_tests` maps each
  StRS to its `acceptance_tests` files, `missing_tests` follows Rule 5, and `tested` stays what
  it is in the code today (`len(trace["tested"])`), a **link count**: the number of leaf IDs
  with at least one counting `@tests_req`, not the number of test-covered SwRS. So a SwRS that
  declares S1 and S2 and has a counting marker on S1 only counts in `marker_coverage.tested`
  and is listed in `missing_tests`; the test-covered count is `totals.tested`, as today (where
  `marker_coverage.tested` already differs from it, e.g. by counting exempted leaves). Each SwRS
  record's `tests.files`/`count` list only the files of its counting `@tests_req`, that is its
  `tested_in_files` (Rule 5): fragmentless markers when it declares no transitions, markers
  with a declared `#S<n>` when it does (Q30). The rejected markers are listed only by the
  errors (`okfreq validate`, `diagnostics.errors`). `missing_ids`, `duplicates`, `non_leaf`,
  `warnings` and the implementation fields are unchanged. The reference page (surface 2) says
  that `marker_coverage.tested` is a link count and `totals.tested` the coverage count.
- New mode, per SwRS that declares transitions: `"transitions": {"tested": ["S1"], "missing":
  ["S2"]}` (Q29).
- New mode, aggregate `stakeholder_test_coverage` gains `"paths": {"total", "tested",
  "accepted"}`, the sums over StRS (Q39). `coverage_definition.tests` says "every declared
  transition has a test marker with its fragment, or at least one test marker when none is
  declared".
- `report_schema()`: `$defs.stakeholder_requirement_coverage` declares `paths`, `tested`,
  `accepted`, `tests`, `acceptance_tests`, and the optional `acceptance_exemption.reason`;
  `linked_swrs[].status` also permits `exempt`; `$defs.requirement` declares `transitions`;
  the aggregate declares `paths`. Both waived and unwaived reports validate.
- `write_markdown_report`, new mode only:
  - Summary gains `- StRS paths: tested <t>/<n>, accepted <a>/<n>` (Q39);
  - "By stakeholder requirement" gains `Tested` and `Accepted` columns: `2/3`, with ✅ when
    complete; for a StRS without paths, `✅ no paths` / `❌ no paths` from the booleans.
    A waived StRS's `Accepted` cell says `exempt` instead of claiming acceptance; the JSON
    and aggregate still show the actual counts;
  - "By software requirement" gains `Missing transitions`: `S2, S3`, or `—`;
  - the note below the StRS table uses the new description.
  In the old modes the Markdown is unchanged.

### Rule 9: `okfreq new` pre-fills `scenarios:` (Q41, Q59)

In the new mode, `create_requirement` (`okfreq new`) pre-fills `scenarios:` from the headings of
the body it writes, read with `_scenario_headings` (Rule 6), so the frontmatter and body start
in step:

- **SwRS**: its two headings are `### Scenario S1: <nominal behavior>` and
  `### Scenario S2: <boundary or failure behavior>`; they give
  `[{id: S1, title: <nominal behavior>}, {id: S2, title: <boundary or failure behavior>}]`.
  Apply these heading changes only in the new mode.
- **StRS**: in the new mode, `ears_body` adds to the StRS body, after "Normative behavior", a
  section

  ```markdown
  ### Main paths

  #### Path S1: <main path title>

  1. <first step the stakeholder observes>
  2. <next step, up to the observable outcome>
  ```

  and `scenarios:` gets `[{id: S1, title: <main path title>}]`. The author adds
  `#### Path S2: …` headings and matching entries as needed.
- The placeholders are bracketed like every template placeholder, so `body_is_unfilled` and
  `W002` keep flagging an unfilled body.
- In the old modes `okfreq new` writes byte for byte what it writes today, so their output, the
  tests that pin it and old-mode projects stay unchanged (Q59, Rule 1).

## What changes, by surface (Q16)

`AGENTS.md` names six surfaces, all changed here, plus the feature map. The PR summary says, per
surface, what changed (`.github/guidelines/product-maintenance.guidelines.md`, step 3).

### 1. Runtime: `src/okf_schema/`

- `okfreq/core.py`: `STRS_TEST_COVERAGE_MODES`, `STRS_TEST_COVERAGE_DESCRIPTIONS`,
  `DEFAULT_CONFIG` (`markers.accepts`, `accepted_in_files` in `generated_fields`),
  `SUPPORTED_GENERATED_FIELDS`, `load_config`, `_strs_test_coverage_mode`,
  `LIFECYCLE_DESCRIPTION` (Rule 7 exception), `initialize_bundle`/`schema_text` (base
  `scenarios`; strs `tested_in_files`/`accepted_in_files`; swrs refused `accepted_in_files`),
  `marker_scan` (Rule 3), `validate_requirements` (Rules 2, 4, 6), `update_coverage` (Rule 5),
  `retire_requirement` (refused on `@accepts_req` markers too, in every mode, Q57; docstring
  "Raises" updated), `report`, `report_schema`, `write_markdown_report` (Rule 8),
  `ears_body`/`create_requirement` (Rule 9). New private helpers shared by validation, coverage
  and report, e.g. `_declared_scenarios`, `_scenario_headings`, `_scenario_findings`,
  `_scenario_coverage`. Public functions get Google-style docstrings with
  `.. versionchanged:: 0.18.0` (`.github/guidelines/python-module-documentation.guidelines.md`)
  and doctests still pass.
- `okfreq/cli.py`: `trace` summary (Rule 3); help and docstrings of `validate`, `lint`, `new`,
  `update-coverage`, `generate-report` and `retire` mention the new mode or the new marker.
- Put real `@implements_req` markers on the new code for the new SwRS (surface 5).

### 2. Human documentation: `docs/source/`, `README.md` (Q46, Q52, Q55, Q56)

The built site must show the possibilities and why. No page speaks of "benches": the
documentation explains the choice between the two verbs by **execution cost**. Pages to add or
change:

- **New explanation page** `docs/source/explanation/okfreq-acceptance-paths.md`, "Why okfreq
  measures acceptance paths", added to the toctree of `docs/source/explanation/index.md` after
  `okfreq-coverage-boundaries`. It explains, project-neutrally:
  - why a direct StRS marker is a link, not a proof (a test that photographs one state or
    repeats one SwRS transition does not walk a stakeholder path);
  - the two verbs: `@tests_req` (a test of a requirement or of one of its scenarios) and
    `@accepts_req` (the acceptance test of a StRS main path), and the two independent counters
    they feed, "tested" and "accepted" (Q54), and why coverage normally needs "accepted"
    (Q18), with the explicit waiver exception (U1);
  - a section **"Choosing by execution cost"**, with the label `(okfreq-execution-cost)=` (the
    W004 target): when the test closest to the final product is expensive, mark it
    `@accepts_req` and run it in the main-branch pipeline, and mark a cheaper test of the same
    path `@tests_req` and run it in the pull or merge request pipeline; when tests are cheap,
    put `@accepts_req` directly on them. This is a recommendation, not an obligation: okfreq
    does not check where or how a test runs (Q52, Q55); `W004` says a non-waived StRS has no
    acceptance test at all;
  - why and when an owner may waive acceptance for a whole StRS that cannot be
    acceptance-tested, an interactive skill as an example, why cost alone is not sufficient,
    how to document and later remove the reason, and why an exemption is not an accepted path
    or a substitute for its SwRS coverage (U1-U2);
  - why a fragment: a marker must say which path it walks, so a fraction can be computed;
  - why declaring `scenarios:` makes fragments mandatory, for both verbs and both tiers: once
    paths exist, a fragmentless marker would claim every path at once (Q14, Q19, Q53), whereas
    without declared paths it is the only honest link;
  - why the verb is in the marker and not in a setting: the test itself states what it is, no
    configuration can drift (Q2);
  - that this is still linkage, not execution: `execution_evidence` stays `not_collected`;
  - how to choose a mode, with a link to the comparison below.
- **New reference page** `docs/source/reference/okfreq-acceptance-paths.md`, "Acceptance paths
  and scenario markers", added to the toctree of `docs/source/reference/index.md` after
  `okfreq-configuration`. It holds:
  - the **verb table**: `@tests_req`, on a SwRS transition or a StRS path, recommended for the
    cheap tests run on every pull or merge request; `@accepts_req`, on a StRS path only, the
    acceptance test, recommended for the tests closest to the final product, possibly costly
    and run in the main-branch pipeline, or for any test when tests are cheap; with the
    recommendation stated as such (not checked);
  - the **mode comparison**: the three modes, what each requires for a SwRS and for a StRS,
    and what each does with `@tests_req`/`@accepts_req` on a StRS;
  - the **combination table**: every marker (`@implements_req`, `@tests_req`, `@accepts_req`)
    × tier (StRS, SwRS) × `scenarios:` declared or not × fragment (none, declared `S<n>`,
    undeclared `S<n>`, other suffix) × mode (old modes, new mode) → result (counts as …, error,
    ignored). It reproduces Rules 1 and 4 completely;
  - the fragment syntax (Rule 3) and the three marker keys;
  - **worked examples**, each with the frontmatter, the test markers, and the resulting JSON
    excerpt and Markdown row:
    1. a StRS with three paths, tested 2/3 by `@tests_req` and accepted 1/3 by `@accepts_req`,
       one path accepted and not tested (Q54) (not covered; both columns shown);
    2. a SwRS with transitions S1, S2 where only S1 has a test (missing S2, SwRS not
       covered, its StRS not covered);
    3. a StRS without `scenarios:`: a fragmentless `@tests_req` counts, no `@accepts_req`:
       `W003` printed with its block and `W004`;
    4. a justified whole-StRS waiver with at least one unaccepted path and a separately
       exempted linked SwRS: the StRS may be covered by policy, but the JSON and Markdown
       distinguish exemption from actual acceptance and the actual path count is unchanged;
  - the findings (each error, `W003`, `W004`) with their messages, and how to fix each,
    including the update of a bundle schema written before 0.18.0 (Q48), the waiver's required
    reason and its effect on W004 but not W003;
  - the report fields (Rule 8), stating that per StRS `stakeholder_test_coverage.tests` lists
    the `@tests_req` files while the StRS record's own `tests` follows `validation_tests`, that
    is the `@accepts_req` files in the new mode (Q62), and that `marker_coverage.tested` is a
    link count while `totals.tested` is the test-covered count; and that in the new mode the
    report's `validation_tests` (aggregate and per StRS) holds the `@accepts_req` files (Q49)
    while `okfreq trace --json`'s `validation_tests` keeps the raw `@tests_req` files on a
    StRS (Rule 3).
  The page also gives the waiver frontmatter, owner-review guidance, when to remove it, its
  whole-StRS scope, the distinct SwRS annotation exemption, and the unchanged evidence
  counters. The first three examples' blocks carry a `:caption:` so a test can read them
  (Evidence).
- `docs/source/reference/okfreq-frontmatter.md`:
  - a "Declared scenarios" section with the label `(okfreq-declared-scenarios)=` (W003 target,
    Q32): the field, its shape, ids never reused (Q26), StRS vs SwRS meaning, declaring it from
    `### Main paths` / `### Scenario` headings, matching IDs and titles in frontmatter and body
    as authoring guidance, Rule 7, and a link to the reference page;
  - "Lifecycle states": the `approved` row gains the Rule 7 exception, and so does the paragraph
    "A coding agent never approves a requirement…" below the table;
  - "Tier-specific Markdown bodies": the StRS example shows a `### Main paths` section and its
    `scenarios:` and matching `#### Path S1: …` headings, and the SwRS example shows matching
    `### Scenario S1: …` headings and `scenarios:` frontmatter;
  - document `acceptance_exemption` and `acceptance_exemption_reason` as authored StRS fields
    distinct from a SwRS's `annotation_exemption` and `exemption_reason`;
  - "Generated and externally maintained fields": a row `accepted_in_files`, and the
    `tested_in_files` row and the paragraph "StRS intentionally has no implementation or test
    coverage fields" say a StRS carries `tested_in_files` and `accepted_in_files` in the new
    mode;
  - "Marker fields" gains `@accepts_req` and `#S<n>`; its paragraph on direct StRS validation
    tests names the modes.
- `docs/source/reference/okfreq-configuration.md`: the `strs_test_coverage_mode` row and the
  "StRS test-coverage modes" section gain the new mode (link to the reference page); the
  `markers` row and YAML example gain `accepts`, and the `id_pattern` note; `generated_fields`
  gains `accepted_in_files`.
- `docs/source/reference/okfreq-cli.md`: `validate` (new errors, the Q48 error, `W003`,
  `W004`), `trace` (counts, `scenario_markers`, and its `validation_tests` key: the raw
  `@tests_req` files on a StRS in every mode, unlike the report's `validation_tests` in the new
  mode, Rule 3), `update-coverage` (StRS fields), `new`
  (pre-filled `scenarios:`), `generate-report` (new fields, columns, `format_version` 2),
  `retire` (blocked by `@accepts_req` markers too, Q57).
- `docs/source/explanation/okfreq-coverage-boundaries.md`: the modes table gains a row and
  links to the new explanation page; "SwRS test-link coverage" (today "test-link covered when
  at least one configured `@tests_req SwRS-ID` marker is found") adds the new-mode rule: a
  SwRS that declares `scenarios:` is test-link covered only when each declared transition has
  a `@tests_req SwRS-ID#S<n>` marker (Rule 5).
- `docs/source/explanation/okfreq-choices.md`: the paragraph on authored and generated fields
  names `scenarios:` (authored) and `accepted_in_files` (generated), and "The in-source and
  in-tests marker vocabulary defaults to `@implements_req` and `@tests_req`" adds
  `@accepts_req`, with a link to the new explanation page.
- `docs/source/tutorials/okfreq-traceability.md` (near "If the project needs a direct
  stakeholder validation-test definition…") and
  `docs/source/how-to/okfreq-build-requirement-base.md` (mode choice): one short paragraph each,
  linking to the new pages. `test_tutorial_okfreq.py` keeps passing.
- `docs/source/explanation/project-feature-coverage.md` (Q16): the "Stakeholder validation
  tests" row becomes "Acceptance paths": this project uses the new mode, its acceptance tests
  run the installed wheel, its other tests of a StRS path keep `@tests_req`, and the showcase
  step.
- `README.md` (Use Case 3, the list item "`@implements_req` and `@tests_req` markers for
  implementation and test traceability"): lists the three markers and the `#S<n>` fragment,
  and links the two new pages.

### 3. Standalone agent skills: `skills/`

Each skill must work without this repository (`tests/test_skill_resources.py`).

- `skills/okfreq/SKILL.md`: the "Leaf requirements connect to evidence" step (which says that
  in `linked-swrs-and-validation-test` mode a direct `@tests_req <StRS-ID>` defines a
  stakeholder validation test) and step 1 of the authoring procedure ("Add a direct test
  marker only when the configured StRS coverage mode requires an explicit validation test"):
  the new mode, `scenarios:`, the fragment rule, `@accepts_req` for a StRS's acceptance, the
  cost recommendation in one sentence. The bullet "**`approved` belongs to the owner.**" gains
  the Rule 7 exception for an edit that only adds `scenarios:`. `accepted_in_files` joins the
  generated-field lists: the paragraph "`implemented_in_files` and `tested_in_files` use exact
  project-relative paths" (around line 256) and rule 4 of "Universal guardrails", "Never treat
  generated `derived_by`, `supersedes`, `implemented_in_files`, `tested_in_files` or
  `default_owner_email` as authored truth" (around lines 313-314).
- `skills/okfreq/references/operations.md` (the config example and the "default StRS mode"
  bullet that names `@tests_req StRS-...`): the new mode, the three marker keys,
  `accepted_in_files`, Rule 4 in short, and how to fix each error, `W003` and `W004`. The
  bullet "Only the seven listed `generated_fields` are supported. … StRS never carries
  generated source/test file arrays, even when the setting lists those fields." becomes: eight
  supported fields (with `accepted_in_files`); a StRS never carries `implemented_in_files`,
  and carries `tested_in_files`/`accepted_in_files` in the new mode only (Rule 5, Q61).
- `skills/okfreq-gardening/SKILL.md` (the bullet "Add a direct validation-test…"): declaring
  `scenarios:` from existing headings (frontmatter only, `S1…` in order, never reused), Rule 7,
  adding to each existing marker the `#S<n>` of the scenario its test really exercises,
  choosing `@accepts_req` for the acceptance test of a StRS path (by what the test does and its
  execution cost), using a justified whole-StRS waiver only when appropriate, and never
  inventing a test or a marker to fill a counter. Heading alignment is authoring guidance and
  any approved-body edit follows Rule 7. The bullet "Never
  hand-edit `derived_by`, `supersedes`, `implemented_in_files`, `tested_in_files`,
  `default_owner_email`, indexes or reports" (around line 48) also lists `accepted_in_files`.
  The backlog CR
  `okfreq-gardening-skill-audit-checks` also edits this file (Out of scope).
- `skills/okfreq-setup/SKILL.md`: step 11 "**Mark.**" (`@implements_req` at the code,
  `@tests_req` at the test) gains: a marker carries `#S<n>` when its requirement declares
  `scenarios:`, and in the new mode each StRS main path gets an `@accepts_req` on the test
  closest to the final product.
- No skill depends on the documentation links: the W003/W004 messages and the skills carry the
  instructions.

### 4. Scaffold guidance: `src/okf_schema/data/`

- `src/okf_schema/data/requirements/guidelines/requirements.guidelines.md` ("Traceability
  markers", the StRS test-marker sentence, "Lifecycle and approval", "Tier-specific authoring
  formats"): `scenarios:`, `#S<n>` and its one rule, the two test verbs and the cost
  recommendation, the StRS `### Main paths` format, Rule 7 (the exception for a
  `scenarios:`-only edit in "Lifecycle and approval", in the bullet "When the task asks you to
  change an approved requirement…"). Require consistent IDs and titles in `scenarios:` and
  corresponding `### Scenario S<n>: <title>` / `#### Path S<n>: <title>` headings as a good
  authoring practice, not a new validator rule. IDs remain stable when scenarios are reordered
  or removed. Explain the justified whole-StRS acceptance waiver and its distinction from
  acceptance and from a SwRS annotation exemption (U1-U4). In "While editing", the sentence "Never
  hand-edit generated `derived_by`, `supersedes`, `implemented_in_files`, `tested_in_files`,
  `default_owner_email`, `status` or `verified` fields" also lists `accepted_in_files`. Then
  `just refresh-requirements-guideline` regenerates
  `requirements/guidelines/requirements.guidelines.md`; neither copy is edited by hand.
- `DEFAULT_CONFIG`, `LIFECYCLE_DESCRIPTION` and the generated schemas (surface 1) are scaffold
  too; `okfreq init` keeps an existing project's files, as today.

### 5. Own requirements: `requirements/` and their tests (Q21, Q35, Q51, Q52)

This repository switches to the new mode and is migrated for real. The project guideline
forbids nominal evidence, so each marker goes only on a test that does what the marker says.

**Acceptance tests in this repository.** An acceptance test (`@accepts_req`) runs the product
as a user gets it: build the wheel (`uv build --offline --wheel`), install it in an isolated
venv, and exercise the installed console scripts (`okf-schema`, `okfkb`, `okfreq`) in
subprocesses in a fresh temporary project, with no source checkout on `PYTHONPATH`, as
`test_installed_wheel_commands_install_complete_families_without_source_checkout` does.
The navigation path is the exception: invoke the installed wheel's Python API in an isolated
subprocess and assert the returned file-link targets, without importing the checkout or
inventing a navigation CLI (U3). The separate link-checking path uses the installed command.
Share the wheel and environment setup with the existing installed-wheel test, built once per
pytest worker. On Windows the new tests call `pytest.skip` (that test today returns early when
`sys.platform == "win32"`, so it passes without running). They run in `just test` with the
rest of the suite, like that test today, so this repository's CI does not change (surface 7).
The in-process tests (`CliRunner`, API calls, `runpy`) that walk a path keep `@tests_req`.

**Steps.**

1. `requirements/config.yml`: `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`;
   `markers.accepts: '@accepts_req'`; `accepted_in_files` added to `generated_fields`; the new
   acceptance test modules added to the `test_dirs` of their scopes.
2. The 5 StRS (all `proposed`, so their body may change through the usual review): add a
   `### Main paths` section with `#### Path S<n>: <title>` and its steps, and the matching
   `scenarios:`, derived from each StRS's normative statement (Q51):
   - CORE-001: S1 Validate a conforming bundle; S2 Report a non-conforming bundle without
     changing it.
   - CORE-002: S1 Create a bundle and author a concept; S2 Normalize and index a bundle;
     S3 Inspect bundle knowledge read-only.
   - CORE-003: S1 Navigate declared file links; S2 Check declared file links on request.
   - OKFKB-001: S1 Capture an immutable finding; S2 Update a knowledge base's indexes and lint;
     S3 Propose a consolidation for human review.
   - OKFREQ-001: S1 Set up a bundle and author linked requirements; S2 Trace markers and
     refresh generated coverage; S3 Audit the requirements base with validate and a report.

   StRS content is the owner's: the PR lists these paths for the owner's review.
3. Implement an acceptance test for each of the 12 executable paths, in
   `tests/test_acceptance_core.py`, `tests/test_acceptance_okfkb.py` and
   `tests/test_acceptance_okfreq.py`, using the installed interface above and asserting the
   observable outcome, marked `# @accepts_req StRS-OKFSCHEMA-…#S<n>`. The thirteenth path,
   OKFKB-001 S3, is interactive consolidation for human review, not a deterministic command:
   do not invent a CLI or a marker for it. Add `acceptance_exemption: true` and an explicit
   `acceptance_exemption_reason` to the whole `StRS-OKFSCHEMA-OKFKB-001` (U1).
4. The 6 `@tests_req StRS-OKFSCHEMA-…` markers in `tests/` stay `@tests_req` (Q52); each gets
   the fragment of the path its test exercises (one line per path if it exercises several,
   e.g. the showcase test). Every StRS now declares paths, so a fragmentless marker would be an
   error (Q53): a test that exercises no declared path loses the marker. Starting points:
   `tests/test_integration.py::test_end_to_end_workflow_init_creates_base_schema_and_validates`
   (CORE-001), `::test_end_to_end_workflow_format_then_validate_consistency` (CORE-002),
   `::test_kb_end_to_end_workflow_kb_update` (OKFKB-001),
   `tests/test_file_links.py::test_inspect_file_links_exposes_successes_failures_and_suffixes`
   (CORE-003), `tests/test_okfreq.py::test_report_and_cli_surface` and
   `tests/test_examples.py::test_okfreq_showcase_runs_in_an_empty_project` (OKFREQ-001).
5. The 29 SwRS (and the new one): declare `scenarios:` from their 93 existing `### Scenario:`
   headings, `S1…` in order, titles from the headings, and align each body heading's ID and
   title with its frontmatter (U4). For each non-exempt scenario, put
   `# @tests_req SwRS-…#S<n>` on the test function(s) that exercise it, found among the SwRS's
   current `tested_in_files`. File-level fragmentless markers become per-test markers (they are
   errors now). A scenario with no exercising test gets a real new test; a marker never goes on
   a test that does not exercise its scenario. For `SwRS-OKFSCHEMA-OKFKB-005`, the interactive
   consolidation requirement, set its existing `annotation_exemption: true` and a specific
   non-blank `exemption_reason` instead of inventing source or test markers (U2).
6. Create one bounded SwRS, `SwRS-OKFSCHEMA-OKFREQ-015`, with `okfreq new swrs` in the new mode
   (pre-filled, Rule 9), scope `okfreq`, `--derives-from StRS-OKFSCHEMA-OKFREQ-001`,
   `--lifecycle proposed`, `--project okf-schema`. It states Rules 1 to 9 as observable
   behavior, with scenarios and verification criteria; its `documentation_files`,
   `agent_skill_files` and `example_files` name the real files of surfaces 2, 3 and 6. Check
   SwRS-OKFSCHEMA-OKFREQ-002, -003, -004, -005 and -011 (retire, Q57) still hold; change one only
   where its statement became false.
7. `requirements/tiers/_schema/base.schema.yaml` (`scenarios`; the `req_lifecycle` description
   with the Rule 7 exception), `strs.schema.yaml` (authored waiver and Rule 4 fields) and
   `swrs.schema.yaml` (Rule 4).
8. `requirements/guidelines/project.guidelines.md`: replace "This project uses
   `linked-swrs-and-validation-test`…" and "Keep the strict StRS coverage mode and direct
   validation-test evidence current" with the new mode and the definition of this repository's
   acceptance tests above.
9. `requirements/tiers/log.md`: one entry under today's `## YYYY-MM-DD` heading (newest first),
   `### Acceptance paths`: the mode switch, the new SwRS, the schema changes, the declared
   paths and transitions, the fragments added to the markers, the new acceptance tests, the
   two justified exemptions, heading alignment and the verification result.
10. `okfreq update-coverage requirements`, then `okfreq validate requirements --prose
    --check-links --project-root .`, `okfreq lint requirements --prose --check-links
    --project-root .`, `okfreq trace requirements --json`.

### 6. Concrete examples: `examples/` (Q35, Q50)

- `examples/okfreq-examples/showcase.py`: a new step after `strict_stakeholder_coverage`, in
  the disposable project (custom `@delivers`/`@verifies` already). `StRS-DELIVERY-001` was
  created in `linked-swrs-and-validation-test` mode, so it has no `### Main paths`; the step
  first writes into its body a `### Main paths` section with `#### Path S1: …` and
  `#### Path S2: …`. It adds `markers.accepts: '@accepts'`, switches to the new mode, then
  asserts in order:
  1. W003 names `StRS-DELIVERY-001`, quotes the two `#### Path` headings, and gives the block;
     W004 names it too;
  2. after pasting `scenarios:` (S1, S2) on the StRS and (S1, S2) on `SwRS-DELIVERY-001`, the
     fragmentless `@verifies SwRS-DELIVERY-001` and `@verifies StRS-DELIVERY-001` are errors
     and do not count (Q53); `@verifies SwRS-DELIVERY-002` stays fragmentless and counts, since
     that SwRS declares no `scenarios:`;
  3. `#S9` is the unknown-fragment error;
  4. `@accepts StRS-DELIVERY-001#S1` alone gives accepted `1/2`, tested `0/2` (Q54), and W004
     disappears; `@verifies …#S1`/`#S2` give tested `2/2`; `@accepts …#S2` gives accepted
     `2/2`; the booleans and the StRS `status` follow;
  5. `SwRS-DELIVERY-001` is covered only when both transitions are marked; with it and
     `SwRS-DELIVERY-002` covered and the StRS accepted, the StRS is `covered`;
  6. `@accepts SwRS-DELIVERY-001` is the schema-driven error;
  7. `Draft202012Validator(report_schema())` validates the report.
  Record `outcomes["acceptance_paths"]`; restore the earlier mode and test file afterwards (the
  `scenarios:` and `### Main paths` may stay: the old modes accept them, Rule 1).
  `tests/test_examples.py` expects 13 outcomes. The module docstring and the comment "These
  markers demonstrate linkage only. Actual CSV behavior is tested in tests/test_export.py…"
  also name `tests/test_acceptance_export.py` as the checked-in example's acceptance test; the
  showcase's own `@accepts` markers stay linkage fixtures.
- The checked-in example `examples/okfreq-examples/` moves to the new mode with a real
  acceptance test of its export (Q50), kept small:
  - `requirements/config.yml`: `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`
    (`markers.accepts` and `accepted_in_files` in `generated_fields` come from `okfreq init`).
  - StRS-CORE-001 declares one main path, `S1` "Export selected rows for offline review", with
    its `### Main paths` / `#### Path S1: Export selected rows for offline review` section and
    steps.
  - Its SwRS declare `scenarios:` (SwRS-CORE-001: S1 Export selected rows, S2 Export an empty
    selection; SwRS-CORE-002: S1 Return a Rust CSV row, S2 Export an empty Rust row) and its
    `### Scenario S<n>: <title>` body headings match those IDs and titles (U4). Its tests carry
    per-test fragments: `tests/test_export.py::test_export_rows` `#S1`,
    `::test_export_rows_with_empty_selection` `#S2`, and the two Rust tests in
    `tests/rust_export_test.rs`. `test_export_rows`, the cheap in-process test of the path,
    also carries `@tests_req StRS-CORE-001#S1`.
  - **Its acceptance test**: the export as a user runs it, in a separate process, with the
    report written to and read back from disk. `src/export.py` gains a small `main()` run under
    `if __name__ == "__main__"`: `python src/export.py <rows.json> <report.csv>` reads a JSON
    list of rows and writes them with `export_rows`. A new
    `tests/test_acceptance_export.py::test_fast_export_selected_rows_for_offline_review(tmp_path)`
    writes `rows.json`, runs `src/export.py` with `sys.executable` through `subprocess` from
    `tmp_path` (no `sys.path` insertion), then reads `report.csv` with `csv.reader` and asserts
    the selected rows come back exactly. It is marked `# @accepts_req StRS-CORE-001#S1`.
  - **Its second, slow acceptance variant** (U5) names the same `StRS-CORE-001#S1`, but is
    entirely commented out and has no implementation. Keep its illustrative marker inactive,
    for example `# # @accepts_req StRS-CORE-001#S1`, so the scanner cannot count it. It is not
    collected as a test and must not fabricate acceptance evidence. A focused test removes
    the fast marker in a temporary copy and proves the commented variant does not count and
    W004 returns.
  - Result: StRS-CORE-001 `Tested 1/1 ✅`, `Accepted 1/1 ✅`, covered, no W003 or W004; its
    generated `tested_in_files` is `tests/test_export.py` and `accepted_in_files`
    `tests/test_acceptance_export.py`; both SwRS covered with no missing transition.
  - The `refresh-okfreq-examples` recipe of the `justfile` is updated so that regeneration
    produces this state (mode, pre-filled `scenarios:` titles replaced like the body
    placeholders, the StRS `### Main paths` text); its existing pytest step runs the new
    acceptance test. `dist/requirements-report*.json|md` are regenerated (`format_version` 2)
    and reviewed.
- `examples/okfreq-examples/README.md`: says the example runs in the new mode; explains its
  main path, the two test verbs it uses (`@tests_req …#S<n>` on the SwRS tests and on
  `test_export_rows` for the StRS, `@accepts_req` on the acceptance test) and why the
  fast acceptance test runs the export as a separate process, and that the commented slow
  variant is only a future example and not evidence; adds the acceptance test to
  "Pointers" and to the sentence on executable evidence; the showcase bullet "both StRS
  coverage policies, including a direct stakeholder validation marker" names the three modes
  and the new acceptance-paths outcome.

### 7. Verification and packaging: `tests/`, `justfile`, `pyproject.toml`, CI

New and changed tests are listed under Evidence. `justfile` changes only in
`refresh-okfreq-examples`. CI (`.github/workflows/ci.yml`, `just preflight` on Linux ×4 Pythons,
macOS, Windows) does not change; the acceptance tests need `uv` and an offline build, which the
existing installed-wheel test already needs there. Packaging does not change.

## Out of scope

- The Studio's migration: its `scenarios:`, the `#S<n>` fragments on its markers, its
  acceptance tests, and the `accepted_in_files` declaration its pre-0.18 `swrs.schema.yaml`
  needs before it switches mode (Studio CR `strs-path-validation`).
- The backlog CR `okfreq-gardening-skill-audit-checks` (`2-backlog/P1`), which also edits
  `skills/okfreq-gardening/SKILL.md`: its "tests against scenarios" audit builds on the
  `scenarios:` field and `#S<n>` fragments of this CR instead of a separate heading-based
  audit. This CR changes that skill only as surface 3 says.
- A migration subcommand (Q8); bench configuration, or any check of where a test runs (Q2,
  Q52, Q55).
- Test-result ingestion: counters are linkage; `execution_evidence` stays `not_collected`.
- A general validator enforcing that `scenarios:` IDs or titles match body headings, or a
  history of retired ids (Q26, U4). Project-specific checks may verify the migrated examples
  and requirements follow the guidance.
- Several IDs or fragments on one marker line: one marker per line, as today.
- Any change of behavior in the old modes beyond the every-mode changes listed in Rule 1.

## Evidence

### Checks

`tests/test_okfreq.py` (unit, `okf_schema.okfreq.core`, per
`.github/guidelines/python-unittest.guidelines.md`). Each test builds its bundle with
`initialize_bundle`/`create_requirement` in `tmp_path`, edits `config.yml` as a user does, and
writes real test files with markers:

1. `load_config` accepts the new mode; the refusal lists three modes; duplicate keywords fail
   in every mode; an old `config.yml` without `accepts` gets the default; `generated_fields`
   accepts `accepted_in_files`.
2. `okfreq init` output, read from the files written: the base schema has `scenarios` and the
   Rule 7 exception in its `req_lifecycle` description;    the strs schema declares `tested_in_files`, `accepted_in_files` and the optional authored
   waiver with its conditional required reason; the swrs schema refuses `accepted_in_files`;
   `config.yml` has `markers.accepts` and `accepted_in_files` in `generated_fields`.
3. `marker_scan`: `@accepts_req` read in `test_dirs` only; fragment and line captured; custom
   keywords; `#path1`, `#S1a`, `#` read as fragmentless; `#S0` captured; two fragments of one
   ID in one file give two `scenario_markers`; an `@accepts_req` on an unknown ID lands in
   `missing_ids`; the new keys and the doctest.
4. **Every row of Rule 4's table** in the new mode, with the message contents (file:line,
   configured keyword, declared ids); a marker with a fragment on a project-added tier keeps
   today's handling (`non_leaf` for a parent tier) with no finding.
5. Rule 5: StRS fractions and booleans at `0/3`, `2/3` tested with `1/3` accepted, `3/3`; the
   counters independent both ways (a path accepted and not tested, one tested and not
   accepted, Q54); covered needs linked SwRS plus acceptance or a justified StRS waiver; StRS without `scenarios:` tested or
   accepted by fragmentless markers; SwRS with transitions covered only when all marked;
   `update_coverage` in the new mode writes a StRS's `tested_in_files`/`accepted_in_files` from
   counting markers only, each when listed in `generated_fields`, and leaves a field that is
   not listed untouched (a hand-placed value stays, none is added); in the old modes it removes
   both from a StRS even when `generated_fields` lists them (Q61); a SwRS's `tested_in_files`
   lists only the files of its counting markers (fragmentless without transitions, declared
   `#S<n>` with them; a rejected marker's file absent, Q30); exempted SwRS stay out. Test a
   partial and an entirely unaccepted waived StRS, no linked SwRS, a missing linked SwRS,
   a separately justified exempt SwRS, and a missing or blank SwRS reason. The waiver never
   manufactures markers, booleans or path counts; old modes ignore its coverage effect.
6. W003: body with `### Main paths` / `#### Path 1: …` / `#### Path 2: …` → headings quoted,
   block with titles, link; body with `### Scenario: …` headings; no heading → placeholder
   block; reading stops at the next `#`, `##` (e.g. `## User Need`) or `###` heading and at the
   links block; deprecated/superseded → none; draft → one; printed without `prose=True`; no
   finding for a SwRS without `scenarios:`. Explicit `Path S<n>:` and `Scenario S<n>:` IDs
   survive in the suggested block, including mixed legacy headings. W004: a live StRS with no `@accepts_req` → one,
   with the cost link; with only rejected `@accepts_req` markers → one; with one counting
   `@accepts_req` (`accepted 1/3`) → none; deprecated/superseded → none; a StRS without
   `scenarios:` and without acceptance → both W003 and W004; printed without `prose=True`.
   A justified waiver suppresses W004, not W003 or fragment errors; true with a missing,
   empty or whitespace-only reason is invalid. `update_coverage` preserves both waiver fields.
7. Rule 2: the schema refuses `kind`, `P1`, empty title, `[]` in every mode; in the new mode
   the code refuses duplicate ids, and in the old modes a duplicate passes; `update_coverage`
   preserves `scenarios:` byte for byte.
8. Rule 4's schema mechanism: `@accepts_req SwRS-X` is an error carrying the schema
   description; a `swrs.schema.yaml` that does not declare `accepted_in_files` (pre-0.18) and
   one that drops the `maxItems: 0` each make validation fail with one error naming the
   property and giving the 0.18.0 declaration (Q48); the same bundles validate as today in the
   old modes.
9. Rule 7: an approved StRS (approval fields present) that gains only `scenarios:` validates.
10. Rule 8: `format_version` 2 in all three modes; new fields present in the new mode and
    absent otherwise; in the new mode `validation_tests` equals `acceptance_tests` (files and
    status, Q49) and the StRS `tests` lists its counting `@tests_req` files while the StRS
    record's `tests` follows `validation_tests` (Q62); the new-mode description (with "when it
    declares no paths, at least one @accepts_req names the StRS") is in
    `coverage_definition.stakeholder_tests` and the Markdown note; Q58: a
    fragmentless `@tests_req` on a SwRS with transitions and an undeclared fragment appear in
    neither `marker_coverage`, `legacy.marker_coverage` nor the SwRS's `tests.files`, and a SwRS
    with a counting marker on S1 only of S1/S2 counts in `marker_coverage.tested` (link count),
    is listed in `missing_tests` and is not in `totals.tested`, while the
    old modes' values are unchanged; `Draft202012Validator(report_schema())` validates each
    mode's report; Markdown columns, summary line and `Missing transitions` in the new mode,
    unchanged table in the old modes. A waived report contains its reason, unchanged actual
    acceptance and path counts, an `exempt` Markdown acceptance cell, and `exempt` for an
    individually waived SwRS; it validates against `report_schema()`.
11. Rule 9: `create_requirement` in the new mode pre-fills `scenarios:` for SwRS (S1, S2) and
    StRS (S1 and the `### Main paths` section), with IDs and titles matching both tiers' body
    headings; in the old modes the output is byte-identical to today's (Q59).
12. Q57: `retire_requirement` refuses a draft named only by an `@accepts_req` marker, in each
    of the three modes, naming the file, and changes nothing.

`tests/test_okfreq_cli.py` (`CliRunner`): `validate` exits 1 on each error kind and 0 while
printing W003 and W004; `lint` fails on the same; `trace` prints `accepted:`;
`update-coverage` writes the StRS fields in the new mode; `generate-report` writes the columns;
`new` pre-fills; `retire` exits non-zero on an `@accepts_req` reference.

`tests/test_skill_resources.py`: the shipped `skills/okfreq/SKILL.md`,
`skills/okfreq/references/operations.md`, `skills/okfreq-gardening/SKILL.md` and
`skills/okfreq-setup/SKILL.md`, read as they ship, mention the new mode, `@accepts_req`,
`scenarios:` and `#S<n>`; installed references stay
self-contained. A test reads
`src/okf_schema/data/requirements/guidelines/requirements.guidelines.md` as it ships and checks
it states the two test verbs and the cost recommendation, the fragment rule and Rule 7;
`tests/test_project_contract.py::test_repository_guideline_is_the_installed_shipped_text`
keeps the copy equal.

Documentation:

- A new test (e.g. `tests/test_okfreq_docs.py`) reads the captioned blocks of the three worked
  examples from `docs/source/reference/okfreq-acceptance-paths.md`, builds each bundle and its
  test files from them, and asserts the JSON excerpt and Markdown row the page shows, and W003
  and W004 for the third. The page and the code cannot drift.
- `just docs` (`sphinx-build -W`) succeeds: both new pages are in a toctree, every cross-link
  resolves. Then check the built site: `docs/_build/html/explanation/okfreq-acceptance-paths.html`
  exists and contains `id="okfreq-execution-cost"` (the W004 link target),
  `docs/_build/html/reference/okfreq-acceptance-paths.html` exists, and
  `docs/_build/html/reference/okfreq-frontmatter.html` contains `id="okfreq-declared-scenarios"`
  (the W003 link target).

Repository and examples:

- `tests/test_project_contract.py::test_live_requirements_preserve_complete_real_evidence`
  asserts the new mode, zero findings (so no fragment error, no W003, no W004), all 5 StRS
  covered by the policy, 12 of 13 paths actually accepted, and no non-exempt `missing_tests`.
  It identifies the justified StRS waiver and the independently exempted consolidation SwRS;
  it does not claim that interactive consolidation is accepted. Verify migrated requirement
  and example headings match their frontmatter without introducing a general validator rule.
- The new acceptance tests run on Linux and macOS in `just test` and fail if the installed
  interface does not produce each executable path's outcome; the navigation test imports the
  installed API in an isolated subprocess. No acceptance marker or dedicated CLI represents the
  interactive consolidation path.
- `tests/test_examples.py::test_okfreq_showcase_runs_in_an_empty_project` runs the new step.
- `just refresh-okfreq-examples` runs the example's acceptance test, and the regenerated
  `examples/okfreq-examples/dist/requirements-report.json` shows the new mode, StRS-CORE-001
  covered with `paths {1, 1, 1}` and no error, W003 or W004 (Q50). The fast and commented slow
  variants name the same StRS; removing the fast marker proves the slow comment is not counted.
- `just preflight` (style, lint, `requirements-lint`, changelog, typecheck, guideline refresh,
  tests, `refresh-all-examples`, `requirements-report`, `docs`). Review its generated diffs
  (examples, `dist/`, guideline copies, `CHANGELOG.md`) before hand-back. The commit subject is
  `feat(okfreq): measure StRS acceptance paths with declared scenarios` (no `!`, Q40);
  `pyproject.toml`'s version is bumped by the release flow, not by hand.

### Default and configured-value matrix

No host dependency: okfreq is a CLI and behaves the same under any agent host. Each cell starts
from a real `okfreq init` in a temporary project; configured cells edit `config.yml` as a user
would. Shared fixture: StRS-A with `scenarios:` S1/S2 and `#### Path` headings; StRS-B without
`scenarios:`; SwRS-A (from StRS-A) with transitions S1/S2; a draft StRS-C; a test file with
`@accepts_req StRS-A#S1`, `@tests_req StRS-A#S2`, `@tests_req StRS-A`, `@tests_req StRS-B`,
`@tests_req SwRS-A`, `@tests_req SwRS-A#S9`, `@accepts_req SwRS-A`, `@accepts_req StRS-C`.

| Cell | Configuration | Result it must show |
|---|---|---|
| D1 | Shipped default (`linked-swrs`, the three default markers) | `okfreq validate` 0 errors, no W003/W004; coverage equal to the same bundle without the suffixes and the `@accepts_req` lines; `@accepts_req` counts nowhere. Only the every-mode changes of Rule 1 show: `format_version` 2 with no new report fields; `okfreq trace` prints `accepted: 3` and `--json` has `accepted`/`scenario_markers`; `okfreq retire StRS-C` is refused, naming the test file; `update-coverage` removes any `tested_in_files`/`accepted_in_files` from a StRS (Q61); `okfreq new` output as today. |
| D2 | `linked-swrs-and-validation-test` | As today: `@tests_req StRS-B` is StRS-B's validation test; `@tests_req StRS-A` and `@tests_req StRS-A#S2` are StRS-A's (suffix ignored); `@tests_req SwRS-A#S9` covers SwRS-A; `@accepts_req SwRS-A` is accepted silently and counts nothing. Every-mode changes as D1. |
| D3 | `linked-swrs-and-acceptance-paths`, default markers | Validate exits 1: fragmentless `@tests_req StRS-A`, fragmentless `@tests_req SwRS-A`, `#S9`, `@accepts_req SwRS-A` (schema description). W003 on StRS-B and StRS-C (no `scenarios:`); W004 on StRS-B only (StRS-A and StRS-C have a counting `@accepts_req`). StRS-A `paths {2, 1, 1}` (S2 tested, S1 accepted: independent); StRS-B tested by the fragmentless `@tests_req`, not accepted; SwRS-A missing S1, S2. After `update-coverage`, StRS-A has `tested_in_files` and `accepted_in_files` = the test file. `validation_tests` = `acceptance_tests`. Markdown `1/2`, `1/2`; StRS-B `✅ no paths` / `❌ no paths`. |
| D4 | New mode, custom `tests: '@verifies'`, `accepts: '@accepts'` (the showcase) | Same as D3 with the custom keywords quoted in messages. |
| D5 | New mode, `config.yml` written before this change (no `accepts` key; `generated_fields` without `accepted_in_files`), schemas from this version (with older schemas it is D6) | Default keyword recognised; results as D3, except that `update-coverage` leaves `accepted_in_files` untouched on every StRS (not a configured generated field, Q61): none is added, and a value already in a StRS's frontmatter stays as it is. |
| D6 | New mode, `swrs.schema.yaml` written before this change | `okfreq validate` exits 1 with one error naming `accepted_in_files` and `swrs.schema.yaml` and giving the 0.18.0 declaration to add; no shipped declaration is applied. After the declaration is added, results as D3. In an old mode the same bundle validates as today. |
| D7 | `strs_test_coverage_mode: unsupported` | `RequirementError` listing the three modes; `okfreq validate` exits non-zero with it. |
| D8 | New mode, StRS-A has a justified whole-StRS waiver and SwRS-A is test-covered | StRS-A is covered despite its unaccepted S2; `accepted` remains false, paths remain `{2, 1, 1}`, JSON records the waiver reason, and the Markdown acceptance cell says `exempt`. Remove all acceptance markers: W004 remains suppressed, acceptance is still false and W003 is unaffected. |
| D9 | New mode, StRS-A waived but linked SwRS-A is not test-covered | StRS-A remains missing. A separate `annotation_exemption: true` with non-blank `exemption_reason` makes SwRS-A `exempt` and satisfies that linked-SwRS condition; an absent or blank reason does not. A StRS without any linked SwRS remains missing. |

### Scenario steps (manual demonstration for the PR)

In a temporary directory:

1. `okfreq init requirements`, set the new mode in `requirements/config.yml`.
2. `okfreq new strs …`: the body has `### Main paths` / `#### Path S1: <main path title>` and
   the frontmatter `scenarios:` S1. Replace the placeholder in both, add `#### Path S2: …` and S2.
   `okfreq validate requirements` prints W004 for it.
3. `okfreq new swrs … --derives-from …`: `scenarios:` S1, S2 pre-filled.
4. Add `# @tests_req <SwRS>` in `tests/`: `okfreq validate requirements` exits 1 and asks for
   `#S<n>`. Mark two tests `#S1`, `#S2`: exits 0.
5. Add `@tests_req <StRS>#S1`, `#S2` and `@accepts_req <StRS>#S1`, then
   `okfreq generate-report requirements`: the StRS row shows `Tested 2/2 ✅`, `Accepted 1/2`,
   status missing, and W004 is gone; adding `@accepts_req <StRS>#S2` makes it covered.
6. Remove `scenarios:` from the StRS: `W003` quotes both path headings and prints the block,
   and the `#S<n>` markers on it become unknown-fragment errors.
7. `just docs` in okf-schema and open the two new pages, the "Declared scenarios" anchor and
   the "Choosing by execution cost" anchor.
8. In a separate fixture, waive an StRS with a justified reason, leaving a path unaccepted:
   W004 disappears and the report says `exempt`, while the accepted fraction stays honest.
   Remove `scenarios:` to see W003 still appears; test an independently exempted linked SwRS.
