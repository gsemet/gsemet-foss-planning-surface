# StRS acceptance paths and SwRS scenarios on okfreq 0.18

Move the Studio requirements bundle to okf-schema 0.18.1 and its coverage mode
`linked-swrs-and-acceptance-paths`. Every live StRS path and every live SwRS scenario gets a
stable id (`S<n>`) in a `scenarios:` frontmatter field and in its body heading. Every test marker
names the path or scenario it checks (`#S<n>`). Every live StRS path is walked end to end by an
acceptance test in real VS Code (`@accepts_req`). The requirements viewer shows the new scores.
One CR (Q10, Q34), stacked last in batch-09.

Short name: `strs-validation`. Sources: `01-intent.md`, `02-answers.md` (Q1 to Q37),
`work/okf-schema-0.18-plan.md`, `experiments/02-audit-sample.md`, and the released okf-schema
0.18.1 documentation (tag `v0.18.1`, <https://okf-schema.readthedocs.io/en/stable/>:
`explanation/okfreq-acceptance-paths`, `reference/okfreq-acceptance-paths`,
`reference/okfreq-frontmatter#okfreq-declared-scenarios`, `reference/okfreq-configuration`,
`reference/okfreq-cli`, CHANGELOG). Figures below are taken from the Studio's `origin/main` at
`4a47151e` on 2026-11-25; the coder recounts them on its own base (the CRs below it in the stack
add markers and requirements).

The project rules apply as written: the constitution (`.agents/constitution.md` in the Studio
repository), `AGENTS.md`, `requirements/guidelines/requirements.guidelines.md`,
`requirements/guidelines/project.guidelines.md`, `.agents/guidelines/ci.guidelines.md`. This spec
does not restate them.

## What shipped in okf-schema 0.18.1 (the contract this CR builds on)

0.18.1 is 0.18.0 plus release fixes only. What the Studio relies on, as released:

- **Mode.** `strs_test_coverage_mode: linked-swrs-and-acceptance-paths` in `requirements/config.yml`.
  The older modes count none of the new markers.
- **`scenarios:`.** A frontmatter list on either tier: `[{id: S<n>, title: <text>}]`, exactly the
  keys `id` and `title`, non-empty, `id` matching `S[1-9][0-9]*` (`S0` is invalid), ids never
  reused. On a StRS an entry is a main path; on a SwRS it is a transition scenario. Adding only
  `scenarios:` to an approved requirement leaves `approved_by`/`approved_at` unchanged and is
  logged in `tiers/log.md`.
- **Markers.** `@tests_req <ID>#S<n>` counts the path or scenario as tested.
  `@accepts_req <StRS-ID>#S<n>` (config `markers.accepts`) counts a StRS path as accepted; on a
  SwRS it is an error raised through the SwRS schema (`accepted_in_files` with `maxItems: 0`).
- **Fragment rule.** Once the target declares `scenarios:`, the `#S<n>` fragment is required on
  both verbs: a fragmentless marker, or a fragment naming an undeclared id, is an error and does
  not count. A target without `scenarios:` takes fragmentless markers only.
- **StRS `covered`.** The linked-SwRS rule (each linked SwRS covered or exempt) **and** every path
  accepted, or an acceptance waiver. "Tested" is reported, it does not change the status.
- **Waiver.** `acceptance_exemption: true` plus a non-blank `acceptance_exemption_reason`, for a
  whole StRS. It only lifts W004 and the "accepted" part of `covered`; it never changes the counts.
- **Warnings.** W003: a live StRS with no `scenarios:` (the message proposes a block from the
  headings). W004: a live StRS with no counting `@accepts_req`. Neither changes the exit code.
- **Generated fields.** On a StRS, `tested_in_files` and `accepted_in_files`, when listed in
  `generated_fields`.
- **Report.** JSON `format_version` 2. Per StRS, `stakeholder_test_coverage` holds
  `paths {total, tested, accepted}`, `tested`, `accepted`, `tests`, `acceptance_tests`,
  `validation_tests` (the `@accepts_req` files) and `acceptance_exemption`; an aggregate
  `stakeholder_test_coverage.paths`; per SwRS, `transitions {tested, missing}`. The Markdown report
  gains Tested and Accepted columns, a "Missing transitions" column and the line
  `StRS paths: tested t/n, accepted a/n`.
- **Trace.** `okfreq trace <bundle> --json` prints `scenario_markers`: one entry per marker,
  `{marker: tests|accepts, id, fragment, file, line}`.
- **Headings.** `okfreq new` writes `#### Path S1: <title>` on a StRS and `### Scenario S1: <title>`
  on a SwRS. okfreq reads `Path S<n>:` / `Scenario S<n>:` headings only to propose W003 blocks.
- **Schemas.** `okfreq init` writes the 0.18 declarations into a new bundle but never replaces
  existing schemas. In the new mode, `okfreq validate` fails on a bundle whose `swrs.schema.yaml`
  does not refuse `accepted_in_files` (checked: a scratch copy of the Studio bundle with only the
  mode switched exits 1 with one error, plus W003 x95 and W004 x95).
- **Bump alone is safe.** With 0.18.1 and the old mode, the current bundle validates with exit 0
  and `okfreq update-coverage --check` reports no file to change.

### Differences from the grill, settled by what shipped

- Q18 (optional fragment) is replaced by Q29/Q30: the fragment is required once `scenarios:`
  exists, so every marker on a live requirement carries one.
- Q22 (counters by bench) is replaced by Q28: okfreq counts markers by verb; the bench is the
  Studio's convention (below).
- Q31 (headings): okfreq does not require `Path S<n>:` headings for counting; the rename is a
  Studio decision for readers and for the viewer (Q31, Q31b).

## Decisions

Every 02-answers decision this CR carries, then the decisions this spec takes (D1 to D16).

### From the owner (02-answers)

- Q1: an automated end-to-end test of a StRS path is an **acceptance** test.
- Q3: one nominal path per acceptance test, run end to end in one go, final result asserted
  (plus the steps no SwRS covers); never edge cases or errors.
- Q5: the marker is `@accepts_req`.
- Q6: a human step is a simulated input; the test asserts the system's gate (blocked without it,
  proceeds with it) and the checkable content, never a judgment. Another verification method is a
  rare exception, written in the path.
- Q7, Q29: all `@tests_req StRS-…` markers are sorted, one by one; each ends as
  `@tests_req StRS-X#S<n>`, `@accepts_req StRS-X#S<n>`, or removed. None stays fragmentless.
- Q8: all paths, no pilot.
- Q10, Q34: one CR for everything.
- Q15: TRUST-012 and TRUST-014 get a short path that starts from the built VSIX; every live StRS
  has at least one path, no exception.
- Q21: one field `scenarios:` on both tiers, `S<n>` ids, no `kind`, fragment `#S<n>` on both
  markers.
- Q24: owner agreement (2026-11-23) for the scripted migration that declares existing paths as
  `scenarios:` on approved StRS (metadata only).
- Q27: switch the mode in this CR and show the honest number.
- Q28: bench convention. `@tests_req StRS-X#S<n>` = the path walked on the simulated bench (run on
  every PR); `@accepts_req StRS-X#S<n>` = the path walked in real VS Code (`test/integration`, run
  on pushes to `main`). Written in CONTRIBUTING and the okfreq skill.
- Q30: SwRS scenarios in this CR. Every `@tests_req SwRS-X` marker gets its `#S<n>`, one marker per
  scenario the test checks. A SwRS never declares an untested scenario: write the test, or remove
  the scenario.
- Q30b: the coder writes the test by default; it removes a scenario only when another scenario or
  SwRS already says the same, or it is not observable. Every removal is listed in the PR with its
  reason and logged in `tiers/log.md`.
- Q31: StRS headings become `#### Path S<n>: <title>`, LIFE-023's `Path 0` included (renumbered).
  Owner agreement (2026-11-25) for this scripted rename on the 15 approved StRS: logged,
  `approved_by`/`approved_at` unchanged. Any other normative change to an approved StRS goes to the
  owner one by one.
- Q31b: SwRS headings become `### Scenario S<n>: <title>`, matching the `scenarios:` ids.
- Q32: a waiver only for a StRS with no automatable step. A path with a human step (CORE-007 path
  1) gets an acceptance test that stops before that step. Candidates listed below.
- Q33: viewer. Home cards "StRS paths tested t/N", "StRS paths accepted a/N", "StRS covered c/M"
  (replacing "StRS with a stakeholder validation test") and a card for SwRS scenarios tested; area
  table columns "Paths tested" and "Paths accepted"; StRS page lists each path with its tested and
  accepted files and a waiver badge; SwRS page lists each scenario with its tests and the missing
  ones.
- Q35: counts are marker-based, as okfreq counts; the proof a test passes is its bench's CI job.

### Taken by this spec

- **D1. Pin `okf-schema>=0.18.1`.** 0.18.0 is never used.
- **D2. Scope of the SwRS migration: live SwRS only.** `scenarios:` and the heading rename apply to
  the SwRS whose `req_lifecycle` is `draft`, `proposed` or `approved` (459 on the base). Retired
  SwRS (superseded, deprecated) keep their body; no marker targets them (0 on the base), and Q30's
  "never untested" rule cannot hold on behaviour that is no longer shipped. Retired StRS have no
  path headings and get no `scenarios:` either.
- **D3. SwRS heading form keeps the kind.** `### Scenario S<n> (<kind>): <title>` when the heading
  had a kind (`nominal`, `boundary`, `refusal`, `failure`), `### Scenario S<n>: <title>` otherwise.
  The `scenarios:` title is the text after the colon. Reason: the viewer's kind badge and the
  Main paths `Option … (<kind>)` bullets read the kind; okfreq does not read SwRS headings for
  counting. A heading with no title text after the colon (for example `### Scenario: Nominal`)
  keeps its text as title.
- **D4. Ids are numbered in body order**, `S1` first. LIFE-023's `Path 0..3` become `S1..S4`.
  On StRS `Path <n>` becomes `S<n>` except LIFE-023.
- **D5. Retired SwRS that are not exempt get the exemption.** okfreq counts a SwRS as a coverage
  target and as a linked SwRS of its StRS whatever its lifecycle unless `annotation_exemption: true`.
  97 retired SwRS (92 superseded, 5 deprecated) lack it, against the project convention, and
  block `covered` on 71 of the 95 live StRS (for example StRS-MDOKFSTUDIO-BLOCK-001 through the
  superseded BLOCK-236 and BLOCK-258). Each gets `annotation_exemption: true` and an
  `exemption_reason` in the existing form (`Superseded by SwRS-…` naming its `superseded_by`, or
  `Archived. <why>` for a deprecated one). Metadata only; none of them is approved.
- **D6. The three live StRS with no path get paths.** BLOCK-027 (copy a selection as exact
  Markdown, SwRS BLOCK-271 to 286), TRUST-012 (visible text and icon, SwRS TRUST-070, TRUST-074),
  TRUST-014 (pinned dependencies, ships what it loads, SwRS CORE-087, CORE-090, TRUST-075,
  TRUST-092). All three are `proposed`, so no owner agreement is needed (the plan's "owner review"
  does not apply). TRUST-012 and TRUST-014 start from the built VSIX (Q15). Each path cites only
  SwRS that `check_main_paths.py` accepts and states what the extension does today.
- **D7. Products that are not the editor.** Four live StRS describe a product other than the
  editor in a VS Code window: CORE-006 (the writing skill), CORE-007 (the release), CORE-008 (the
  site), TRUST-014 (the built VSIX). Their `@accepts_req` goes on the test closest to that product
  (under `test/build`, `test/security`, `test/site` or `test/core`), which runs on every PR. This
  follows the okfreq docs (an acceptance test may be cheap when the product is cheap to reach) and
  is the only exception to Q28's "accepts = `test/integration`". The allow-list lives in the
  placement check (D10) and in project.guidelines "Benches" (D14). TRUST-012 is not on the list:
  its path starts from the VSIX but its result is seen in a VS Code window.
- **D8. A new heavy CI job `acceptance`.** Acceptance tests that are new in this CR live in
  `test/integration/acceptance/<group>.acceptance.ts` (one file per e2e group of
  `test/shared/e2eGroups.ts`, each under 1500 lines, split by group when needed), loaded by a new
  `test/integration/acceptance-suite.ts`, run by `run-tests.ts --acceptance-only`, through the
  target `just ci-acceptance`. Reason: the `integration` job's 20-minute test step already runs 14
  to 18 minutes, so it has no room. Existing `test/integration` tests that already walk a path keep
  their place and are re-marked `@accepts_req` in place (they run in the `integration` job). Both
  jobs are real VS Code, so both satisfy Q28.
- **D9. "Tested" shows what the sort finds.** A simulated walk is not written for every path;
  `@tests_req StRS-X#S<n>` stays where an existing simulated test walks the path after the sort.
  Q27 and the okfreq rule tie `covered` to "accepted" only.
- **D10. Marker placement check learns the new marker.** `scripts/check-marker-companions.mjs`:
  - its `MARKER` regex and the companion line regex accept `@accepts_req` and an optional `#S<n>`
    fragment after the ID; the ID-exists check and the 3-ID block cap use the ID without the
    fragment (two fragments of one ID are one ID);
  - a new rule: `@accepts_req` only in files under `test/integration/`, except on the D7 StRS;
  - a new rule: no `@tests_req StRS-…` under `test/integration/` (a real-VS-Code walk is an
    acceptance; Q28);
  - each failure prints `<path>:<line>: <rule>: <marker>`.
- **D11. A scenario coverage gate.** A new `scripts/check_scenario_coverage.py`, run by
  `just requirements-lint` after okfreq, reads `okfreq report --format json` and fails when a live
  SwRS has a non-empty `transitions.missing`, or a live StRS has `paths.accepted < paths.total`
  without `acceptance_exemption`, or a live StRS has no `scenarios:`. It prints one line per gap
  (`<id>: missing S<n>` / `<id>: path S<n> not accepted`) and ends with
  `scenario coverage: <s> SwRS scenarios tested, <p>/<P> StRS paths accepted, all complete`. It
  enforces Q30 and the completion criterion; okfreq's W003/W004 do not change the exit code. Tests
  in `test/build/test_check_scenario_coverage.py`, run by `release-tests` like
  `test_check_main_paths.py`.
- **D12. The viewer reads per-path files from the trace.** `just requirements-report` and
  `just requirements-report-json` also write `okfreq trace requirements --json` to
  `out/reports/requirements/requirements-trace.json`; the viewer joins its `scenario_markers` to
  list, per path and per scenario, the files that test or accept it. The report JSON gives the
  counts.
- **D13. Vendored okfreq text is refreshed from v0.18.1.** `.agents/skills/okfreq/` and
  `.agents/skills/okfreq-gardening/` are replaced by the okf-schema `skills/` content at tag
  v0.18.1; `requirements/guidelines/requirements.guidelines.md` is refreshed from the packaged
  `src/okf_schema/data/requirements/guidelines/requirements.guidelines.md` at v0.18.1, without its
  `@implements_req SwRS-OKFSCHEMA-OKFREQ-002` line. `requirements/guidelines/okfreq-baseline.guidelines.md`
  is refreshed the same way if it is a copy of an okf-schema file, else left as is. A short "Studio
  benches" note is appended to `.agents/skills/okfreq/SKILL.md`, pointing to project.guidelines
  "Benches".
- **D14. project.guidelines gains a "Benches" section and new heading forms.** It states Q28, the
  D7 allow-list, the D8 file layout and the Q3/Q6 rules for an acceptance test; "Main paths of a
  StRS" shows `#### Path S<n>:` and the `scenarios:` block; a SwRS scenario section shows
  `### Scenario S<n> (<kind>): <title>`; "Marker placement" shows the `#S<n>` fragment.
- **D15. Waiver candidates: none.** Every live StRS has an automatable step:
  - CORE-006 (the writing skill): the agent's writing is a simulated input (Q6); the test asserts
    what Studio renders from it. Not waived.
  - CORE-007 (the release), path S1: the acceptance test runs the version commit and tag gate
    (CORE-075, CORE-076) with the reviewed release notes as a simulated input, and stops before the
    maintainer's review (CORE-078) (Q32). Not waived.
  If the coder finds a StRS with no automatable step, it stops and reports it to the Foreman
  instead of writing a waiver: a waiver needs the owner.
- **D16. Stack position.** Last in batch-09. The sort, the fragments and the gate cover every
  marker and requirement on the stack base, including those added by the lower CRs (the clip CRs
  and the vega chart CRs 502 and 503).

### Approved requirements changed

Owner agreement recorded in Q24 (scenarios only) and Q31 (heading rename), `approved_by` and
`approved_at` unchanged, one `tiers/log.md` entry naming both agreements. Owner:
`default_owner_email` of `requirements/config.yml`.

StRS-MDOKFSTUDIO-BLOCK-003, BLOCK-011, BLOCK-025, DIAG-001, DIAG-006, GFM-002, LAYOUT-001,
LAYOUT-003, PALETTE-015, CORE-001, REVIEW-001, REVIEW-003, REVIEW-012, REVIEW-015, TABLE-001
(30 paths).

Any approved SwRS among the live SwRS is migrated under the same metadata-and-heading rule only if
the coder finds the owner's agreement covers it; Q24 and Q31 name StRS. **Decision D17:** an
approved SwRS (none on the base: the 459 live SwRS are 457 proposed and 2 exempt) gets no rename
and no `scenarios:` in this CR; if a lower CR adds one, the coder reports it to the Foreman.

No other approved text changes. A path or scenario added on an approved requirement, or a scenario
removed from one, is a normative change: the coder does not make it and reports it.

## What changes, area by area

### 1. Dependency and bundle schemas

- `pyproject.toml`: in the `requirements` group, `okf-schema>=0.17.0` becomes `okf-schema>=0.18.1`;
  `uv.lock` relocked (`uv lock --upgrade-package okf-schema`).
- `requirements/tiers/_schema/base.schema.yaml`, `strs.schema.yaml`, `swrs.schema.yaml`: the 0.18
  declarations copied from a fresh `okfreq init` in a temporary folder with okf-schema 0.18.1:
  - base: `scenarios` and the lifecycle description text with its `scenarios:` exception;
  - strs: `tested_in_files`, `accepted_in_files`, `acceptance_exemption`,
    `acceptance_exemption_reason` and the top-level description;
  - swrs: `accepted_in_files` with `maxItems: 0` and its description.
  The Studio's own additions to these schemas (the OKF projections, `req_lifecycle`) stay.
- `requirements/config.yml`: `markers.accepts: '@accepts_req'`; `accepted_in_files` added to
  `generated_fields`. The mode stays the old one until step 11.

### 2. Requirements migration (scripted, then reviewed)

A one-off script in the scratch space (not committed) does, on the base:

- each live StRS with `#### Path <n>: <title>` headings: rename to `#### Path S<n>: <title>` (D4),
  add `scenarios:` with one `{id, title}` per path;
- each live SwRS (D2): rename `### Scenario[ (<kind>)]: <title>` to
  `### Scenario S<n>[ (<kind>)]: <title>` (D3), add `scenarios:`;
- the 97 retired non-exempt SwRS: `annotation_exemption: true` and `exemption_reason` (D5).

Then by hand: Main paths and `scenarios:` for BLOCK-027, TRUST-012, TRUST-014 (D6).

`scripts/check_main_paths.py` keeps working (it reads `### Main paths` and SwRS citations, not
the path headings); its test fixtures get a `Path S1:` case.

### 3. Markers

- **StRS markers (185 on the base, plus the lower CRs').** Each is read and classified with the
  rubric of `experiments/02-audit-sample.md` (walks a path / partial path / single-state snapshot /
  SwRS duplicate / other):
  - walks path n in real VS Code (`test/integration`) → `@accepts_req StRS-X#S<n>`;
  - walks path n on the simulated bench → `@tests_req StRS-X#S<n>`;
  - D7 products → `@accepts_req StRS-X#S<n>` on the closest test;
  - otherwise → removed; its `@tests_req SwRS` markers stay (a snapshot or a one-transition test is
    a SwRS test).
  The PR body holds the classification table (file, line, StRS, class, outcome).
- **SwRS markers (3962 on the base, plus the lower CRs').** Each `@tests_req SwRS-X` becomes one
  `@tests_req SwRS-X#S<n>` per scenario the test checks (Q30), read from the test, not guessed from
  the name. A test that checks no declared scenario is re-read: it checks a scenario that is
  missing from the SwRS (add it: a normative change, allowed on a proposed SwRS) or it is moved to
  the SwRS it does check.
- Each marker block still names at most 3 distinct IDs (D10); fragments of one ID count once.
  `scripts/marker-baseline.json` may only shrink.

### 4. Missing tests

- **SwRS scenarios.** For each live SwRS scenario with no marker (180 live SwRS on the base have
  fewer markers than scenarios; the exact list is okfreq's `transitions.missing` after step 3):
  write the test on the bench where its siblings live, or remove the scenario under Q30b. The PR
  lists every removal with its reason; `tiers/log.md` logs them.
- **StRS paths.** For each live StRS path with no `@accepts_req`: write an acceptance test in
  `test/integration/acceptance/<group>.acceptance.ts` (D8), or on the D7 bench. One nominal path per
  test, end to end, final result asserted (Q3); a human step is a simulated input, and the gate and
  content are asserted (Q6). CORE-007 S1 stops before CORE-078 (Q32).
  Each acceptance test starts from a fresh window with the bench's fixtures and drives the user's
  inputs through the real VS Code commands, keys and the preview, as the existing `realInput`
  tests do.

### 5. CI and justfile

- `test/integration/acceptance-suite.ts`: imports and runs every `acceptance/*.acceptance.ts`.
- `test/integration/run-tests.ts`: flag `--acceptance-only`; without a flag, the existing suites
  run as today (the acceptance suite is not added to them). The acceptance run writes its manifest
  to `out/reports/acceptance/acceptance-manifest.json`, with the same shape as
  `integration-manifest.json`.
- `package.json`: script `test:acceptance` = compile and `node out/test/integration/run-tests.js
  --acceptance-only`.
- `justfile`: target `ci-acceptance` (runs `npm run test:acceptance` under the existing hang
  watchdog, as `ci-integration` does); `preflight` runs it after `ci-integration` (on Windows,
  preflight keeps running the static stage only); `requirements-lint` runs
  `scripts/check_scenario_coverage.py` (D11); `requirements-report` and `requirements-report-json`
  write `requirements-trace.json` (D12).
- `.github/workflows/ci.yml`: job `acceptance`, a copy of `integration`'s shape: same trigger
  (`!cancelled()` and heavy dispatch or `release-check` success), `needs: release-check`,
  `ubuntu-latest`, `xvfb-run`, `timeout-minutes: 30` with a 20-minute test step (to be set to about
  twice the measured duration once the first green run is known, per ci.guidelines), the hang dump
  step and an artifact upload of `out/reports/acceptance/`. `tag-release` needs `acceptance`;
  `report` needs `acceptance`. One job, one target.
- `CONTRIBUTING.md`: the CI section lists the `acceptance` job and target.

### 6. Requirements viewer (`test/site/requirementsViewer/`)

- `model.ts`: read `format_version` 2; per StRS keep `paths`, `acceptance_exemption`; per SwRS
  keep `transitions`; join `requirements-trace.json` to get, per StRS path and per SwRS scenario,
  the files that test it and that accept it. `parseScenarios` accepts the optional `S<n>` id in
  `### Scenario S<n> (<kind>): <title>` and keeps the kind. `stakeholderValidated` is replaced by
  the `covered` status of the new mode. Scope stats gain paths total, tested, accepted, StRS
  covered, scenarios total and tested.
- `mainPaths.ts`: `PATH_HEADING` accepts `Path S<n>:` and yields the id and the title without the
  id.
- `home.ts`: the cards of Q33. "StRS paths tested t/N", "StRS paths accepted a/N" (N = live StRS
  paths), "StRS covered c/M" (M = live StRS), "SwRS scenarios tested s/S"; the "StRS with a
  stakeholder validation test" card is removed. Area table: columns "Paths tested" and
  "Paths accepted" after "Tested".
- `pages.ts`: the use case page lists each path (`S<n>` and title) with its tested files and its
  accepted files, and a "waived" badge with the reason when `acceptance_exemption` is set; the
  behaviour page lists each scenario with its tests and marks the ones with no test as missing.
- Tests: `model.test`, `home.test`, `mainPaths.test`, `pages.test`, `write.test` and `fixture.ts`
  updated; each new reading has a test that fails on the old code.

### 7. Docs and skills

- `CONTRIBUTING.md`: the bench convention (Q28, D7), the acceptance layout (D8), `check-markers`
  rules (D10), the viewer cards.
- `requirements/guidelines/project.guidelines.md`: D14.
- `.agents/skills/okfreq/`, `.agents/skills/okfreq-gardening/`,
  `requirements/guidelines/requirements.guidelines.md`: D13.
- `.agents/glossary/common.md`: terms "acceptance test", "path (StRS)", "scenario (SwRS)",
  "accepted", "waiver".
- `requirements/tiers/log.md`: one entry `## 2026-11-<day>` with `### Topic` sub-headings for the
  migration (Q24, Q31 agreements, D2 to D6), the retired exemptions (D5), the removed scenarios
  (Q30b) and the mode switch (Q27).
- No change to the writing skill `skills/writing-for-markdown-okf-schema-studio/` (no rendered
  syntax changes).

### 8. Mode switch

`requirements/config.yml`: `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`, then
`just requirements-update` and its generated files committed (`tested_in_files`,
`accepted_in_files`, coverage fields).

### Requirements of this change

The Studio's own SwRS describing the requirements viewer (scope of `test/site/requirementsViewer`)
and the marker check are updated for the new cards, columns, pages and rules, with
`@implements_req` and `@tests_req …#S<n>` markers, created `proposed` when new.

## Commit order

Each commit leaves `just requirements-lint` and `just check` green:

1. Bump, schemas, `markers.accepts`, `generated_fields` (old mode).
2. Scripted `scenarios:` and heading renames, with the log entry; markers on the migrated
   requirements get their fragments in the same commit (a fragmentless marker on a target with
   `scenarios:` is an error even in the old mode, so steps 2 and 5/6 may be merged or done per
   area).
3. Retired SwRS exemptions (D5).
4. New paths for BLOCK-027, TRUST-012, TRUST-014 (D6).
5. StRS marker sort.
6. SwRS fragments and missing SwRS tests or removals.
7. Acceptance tests, suite, runner flag, `ci-acceptance`, CI job.
8. Viewer.
9. Checks (D10, D11).
10. Docs and skills.
11. Mode switch and `just requirements-update`.

The coder may split commits further; it keeps this order.

## Out of scope

- Any change to okf-schema itself.
- Retired requirements beyond the D5 exemption (no `scenarios:`, no heading rename).
- A simulated walk for every StRS path (D9).
- Counting passing tests rather than markers (Q35).
- Normative changes to approved requirements beyond Q24 and Q31.
- The writing skill, the renderer, the extension's runtime code in `src/` (only test, scripts,
  requirements, CI and docs change; `src/` changes only if a missing test reveals a bug, which is
  then filed, not fixed here, unless it blocks the test).
- Making the use case diagram mandatory.

## CI environment (job `acceptance`)

- Runs on `ubuntu-latest` from the lock files (`just dev-ci`), no local caches, under `xvfb-run`,
  with the VS Code version the `integration` job downloads.
- Not run on pull requests: only on push to `main` and on
  `gh workflow run ci.yml --ref <branch> -f heavy=true`. So the PR proves it through a heavy
  dispatch on the branch head.
- First-run proofs: the job's duration (to set the step timeout at about twice it, no retries), the
  acceptance manifest artifact listing every acceptance test with its result, and the hang dump
  step present.
- `tag-release` now needs it: a red acceptance job blocks a release.

## Evidence

Every check on a shipped file reads it from the repository at the head under test.

### Checks

1. `just requirements-lint` passes. Its output has no W003, no W004, no fragment error, and ends
   with `scenario coverage: …, all complete` (D11) and the `main paths:` line.
2. `out/reports/requirements/requirements-report.json` at the head has `format_version: 2`;
   `stakeholder_test_coverage.paths.accepted == stakeholder_test_coverage.paths.total` counted on
   live StRS; every live StRS has status `covered`; every live SwRS has an empty
   `transitions.missing`; no StRS has `acceptance_exemption` (D15).
3. `requirements/config.yml` at the head has the new mode, `markers.accepts` and
   `accepted_in_files` in `generated_fields`; `pyproject.toml` pins `okf-schema>=0.18.1`;
   `uv.lock` resolves 0.18.1 or later.
4. `okfreq trace requirements --json` at the head: every `scenario_markers` entry whose target is
   a live requirement has a fragment; every `accepts` entry is under `test/integration/` or targets
   a D7 StRS; no `tests` entry targeting a StRS is under `test/integration/`.
5. `git grep -nE '^#### Path [0-9]' -- requirements/tiers` and
   `git grep -nE '^### Scenario( \(|:)' ` on live SwRS files return nothing; the 15 approved StRS
   keep their `approved_by`/`approved_at` values from the base (diff of those two fields is empty).
6. `just check` passes (check-markers with the D10 rules; their tests in
   `test/build/checkMarkers.test.ts` include a case for each new rule that fails on the old script).
7. `just release-tests` passes, with `test_check_scenario_coverage.py`.
8. Viewer unit tests pass, and each new reading has a test that fails on the base.
9. A heavy dispatch on the branch head is green for `integration` and `acceptance`; the acceptance
   manifest artifact lists one test per new acceptance file entry, all passed.
10. `just preflight` passes (on Windows, the static stage; CI runs the rest).
11. `requirements/tiers/log.md` at the head has the dated entry with the Q24/Q31 agreements, D5 and
    the list of removed scenarios.

### Scenario steps (owner's view)

1. Build the site (`just ci-report`) and open the requirements viewer home: the cards show
   "StRS paths tested t/N", "StRS paths accepted N/N", "StRS covered M/M" and "SwRS scenarios
   tested S/S"; the old validation card is gone.
2. Open the area table: the "Paths tested" and "Paths accepted" columns are filled for every area.
3. Open the use case page of StRS-MDOKFSTUDIO-LIFE-023: four paths `S1` to `S4`, each with its
   accepted file.
4. Open StRS-MDOKFSTUDIO-CORE-007: path S1 lists its acceptance test; reading that test shows it
   stops before the maintainer's review.
5. Open a SwRS page: each scenario lists its tests; none is marked missing.
6. Remove one `@accepts_req` marker locally and run `just requirements-lint`: it fails naming the
   path; restore it.
7. Add `@accepts_req StRS-…#S1` in a `test/visual` file and run `just check-markers`: it fails
   with the placement rule; restore it.

## Self-containment

The coder needs: this spec, the CR's `02-answers.md` and `experiments/02-audit-sample.md` (the
sort rubric), the released okf-schema 0.18.1 docs named at the top, and the repository's own
rules. Every figure above is from the base named at the top and is recounted by the coder.

## Open questions

None. Every point was decided above (D1 to D17); a StRS with no automatable step, an approved
SwRS appearing from a lower CR, or a normative change needed on an approved requirement stops
the coder and goes to the Foreman.
