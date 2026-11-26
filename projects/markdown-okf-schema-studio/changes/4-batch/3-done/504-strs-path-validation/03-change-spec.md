# StRS paths and SwRS scenarios declared on okfreq 0.18 (CR-A)

This CR moves the Studio requirements bundle to okf-schema 0.18.1 and keeps the **current**
coverage mode. It covers five things:

- Every live StRS path and every live, non-exempt SwRS scenario gets a stable id (`S<n>`). The id
  goes in a `scenarios:` frontmatter field and in the body heading.
- Every test marker that targets one of these requirements names the path or scenario it checks
  (`#S<n>`).
- The existing `@tests_req StRS-…` markers are sorted into `@tests_req …#S<n>`,
  `@accepts_req …#S<n>` or removed.
- The marker check learns the new marker.
- The requirements viewer shows paths and scenarios.

The next CR (CR-B) switches to `linked-swrs-and-acceptance-paths`. Before that it writes the
missing tests and the acceptance job. See "Handed to the next CR (CR-B)".

This is one subject (Q10, Q34) delivered as two CRs (Q36). CR-A is stacked in batch-09 on the
linearised stack once CR-492 to CR-503 are merged (D16).

Short name: `strs-validation`.

Sources:

- the CR folder: `01-intent.md`, `02-answers.md` (Q1 to Q42), `work/okf-schema-0.18-plan.md` and
  `experiments/02-audit-sample.md`;
- the released okf-schema 0.18.1 documentation, tag `v0.18.1`
  (<https://okf-schema.readthedocs.io/en/stable/>): `explanation/okfreq-acceptance-paths`,
  `reference/okfreq-acceptance-paths`, `reference/okfreq-frontmatter#okfreq-declared-scenarios`,
  `reference/okfreq-configuration`, `reference/okfreq-cli` and the CHANGELOG.

The figures come from the Studio's `origin/main` at `4a47151e` (2026-11-25). The coder recounts
them on its parent (D16).

The project rules apply as written and this spec does not restate them:

- the constitution (`.agents/constitution.md` in the Studio repository);
- `AGENTS.md`;
- `requirements/guidelines/requirements.guidelines.md`;
- `requirements/guidelines/project.guidelines.md`;
- `.agents/guidelines/ci.guidelines.md`.

## What shipped in okf-schema 0.18.1 (the contract this CR builds on)

0.18.1 is 0.18.0 plus release fixes only. This is what the Studio relies on, as released:

- **Mode.** The new mode is `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`. CR-A
  does not set it (Q36). In the older modes, okfreq accepts `scenarios:` and markers with or
  without fragments without an error. The new markers do not change those modes' counts. The
  critic checked this on 0.18.1.
- **`scenarios:`.** A frontmatter list on either tier: `[{id: S<n>, title: <text>}]`.
  - The keys are exactly `id` and `title`, and the list is never empty.
  - `id` matches `S[1-9][0-9]*` (`S0` is invalid), and an id is never reused.
  - On a StRS an entry is a main path; on a SwRS it is a transition scenario.
  - Adding only `scenarios:` to an approved requirement leaves `approved_by` and `approved_at`
    unchanged; the edit is logged in `tiers/log.md`.
- **Markers.**
  - `@tests_req <ID>#S<n>` counts the path or scenario as tested.
  - `@accepts_req <StRS-ID>#S<n>` counts a StRS path as accepted. Its config key is
    `markers.accepts`.
  - `@accepts_req` on a SwRS is an error, raised through the SwRS schema (`accepted_in_files`
    with `maxItems: 0`).
- **Fragment rule, new mode only.** Once the target declares `scenarios:`, the `#S<n>` fragment
  is required on both verbs. A fragmentless marker, or a fragment naming an undeclared id, is
  then an error and does not count. A target without `scenarios:` takes fragmentless markers
  only. In the old mode these are not errors. So CR-A checks them itself (D10, and the scratch
  validation in "Evidence").
- **StRS `covered`, new mode.** Two conditions must both hold:
  - the linked-SwRS rule: each linked SwRS is covered or exempt;
  - every path is accepted, or the StRS has an acceptance waiver.

  "Tested" is reported but does not change the status.
- **Waiver.** `acceptance_exemption: true` plus a non-blank `acceptance_exemption_reason`, for a
  whole StRS.
- **Warnings, new mode.**
  - W003: a live StRS with no `scenarios:`.
  - W004: a live StRS with no counting `@accepts_req`.

  Neither changes the exit code.
- **Report.** `okfreq generate-report [PATH] --output-json FILE` writes JSON with
  `format_version` 2. The per-StRS `paths`, `tested`, `accepted`, `acceptance_tests` and
  `acceptance_exemption` fields, and the per-SwRS `transitions`, appear only in the new mode.
  There is no `report --format json` command.
- **Trace.** `okfreq trace [PATH] --json` prints `scenario_markers` in every mode.
  - There is one entry per (id, fragment, file), `{marker: tests|accepts, id, fragment, file,
    line}`, and `line` is the first occurrence only.
  - It is enough to count paths and scenarios and list their files.
  - It does not list every marker line. Any work that must see every marker (the sort, the
    fragment sweep) reads the files.
- **Headings.** `okfreq new` writes `#### Path S1: <title>` on a StRS and
  `### Scenario S1: <title>` on a SwRS.
- **Schemas.** `okfreq init` writes the 0.18 declarations into a new bundle but never replaces
  existing schemas. In the new mode, `okfreq validate` fails on a bundle whose `swrs.schema.yaml`
  does not refuse `accepted_in_files`.
- **The bump alone is safe.** With 0.18.1 and the old mode, the current bundle validates with
  exit 0, and `okfreq update-coverage --check` reports no file to change.

### Differences from the grill, settled by what shipped

- Q18 (optional fragment) is replaced by Q29 and Q30. In the new mode, the fragment is required
  once `scenarios:` exists, so CR-A gives every marker on a declaring target its fragment.
- Q22 (counters by bench) is replaced by Q28. okfreq counts markers by verb; which bench runs a
  test is a Studio convention.
- Q31: okfreq does not need `Path S<n>:` headings to count. The rename is a Studio decision, for
  readers and for the viewer (Q31, Q31b).

## Decisions

Every decision from 02-answers that this subject carries comes first, then the decisions this
spec takes (D1 to D17). A decision whose work belongs to CR-B is marked (CR-B).

### From the owner and the Chief of Staff (02-answers)

- **Q1:** an automated end-to-end test of a StRS path is an **acceptance** test.
- **Q3 (CR-B):** one nominal path per acceptance test.
  - It runs end to end in one go and asserts the final result, plus the steps no SwRS covers.
  - It never covers edge cases or errors.
- **Q5:** the marker is `@accepts_req`.
- **Q6 (CR-B):** a human step is a simulated input.
  - The test asserts the system's gate (blocked without the step, proceeds with it) and the
    content it can check, never a judgment.
  - Another verification method is a rare exception, written in the path.
- **Q7, Q29:** every `@tests_req StRS-…` marker is sorted, one by one, and none stays
  fragmentless. Each ends in exactly one of these forms:
  - `@tests_req StRS-X#S<n>`;
  - `@accepts_req StRS-X#S<n>`;
  - removed.
- **Q8:** all paths, no pilot.
- **Q10, Q34, Q36:** one subject in two CRs.
  - CR-A, this one: the declarations, the sort, the fragments, check-markers, the viewer and the
    docs, in the old mode.
  - CR-B: the missing tests, the acceptance tests and their CI job, the D11 gate and the mode
    switch.
- **Q15:** TRUST-012 and TRUST-014 each get a short path that starts from the built VSIX. Every
  live StRS has at least one path, with no exception.
- **Q21:** one field, `scenarios:`, on both tiers, with `S<n>` ids and no `kind`. The fragment is
  `#S<n>` on both markers.
- **Q24:** owner agreement (2026-11-23) for the scripted migration that declares the existing
  paths of approved StRS as `scenarios:`. It covers metadata only.
- **Q27 (CR-B):** switch the mode and show the honest number.
- **Q28:** the bench convention.
  - `@tests_req StRS-X#S<n>` = the path walked on the simulated bench, run on every PR.
  - `@accepts_req StRS-X#S<n>` = the path walked in real VS Code (`test/integration`), run on
    pushes to `main`.
  - It is written in CONTRIBUTING and in the okfreq skill. The only exception is D7.
- **Q30:**
  - Every `@tests_req SwRS-X` marker on a SwRS that declares scenarios gets its `#S<n>`: one
    marker per scenario the test checks (CR-A).
  - A SwRS never keeps a scenario without a test: write the test, or remove the scenario (CR-B).
- **Q30b (CR-B):** the coder writes the test by default.
  - It removes a scenario only when another scenario or SwRS already says the same, or when the
    scenario cannot be observed.
  - Every removal is listed in the PR with its reason and logged.
- **Q31, Q38:** StRS headings become `#### Path S<n>: <title>`, including LIFE-023's `Path 0`
  (renumbered).
  - The owner's agreement covers this scripted rename on the 15 approved StRS.
  - It follows project.guidelines "Approved requirements": `approved_at` is set to the time of
    the change, the 15 are listed in the PR body, and the owner's review is requested on the PR.
    The owner's click on the PR is the re-approval.
  - Any other normative change to an approved StRS goes to the owner one by one.
- **Q31b:** SwRS headings become `### Scenario S<n>: <title>`, matching the `scenarios:` ids (with
  the kind kept, D3).
- **Q32 (CR-B):**
  - A waiver is only for a StRS with no step that can be automated.
  - A path with a human step (CORE-007 path 1) gets an acceptance test that stops before that
    step.
- **Q33:** the viewer changes.
  - Home cards: paths tested, paths accepted, StRS covered and SwRS scenarios tested. They replace
    "StRS with a stakeholder validation test".
  - Area table: columns "Paths tested" and "Paths accepted".
  - StRS page: each path with its tested and accepted files, and a waiver badge.
  - SwRS page: each scenario with its tests, and the missing ones marked.
- **Q35:** counts are marker-based, as okfreq counts. The proof that a test passes is its bench's
  CI job.
- **Q37 (CR-B):** the acceptance budget; see CR-B.
- **Q39:** the two exempt live SwRS (TRUST-070, TRUST-075) get no `scenarios:`. Their fragmentless
  markers stay valid.
- **Q40:**
  - D11 runs `okfreq generate-report --output-json` itself and lands with the switch (CR-B).
  - `scenario_markers` has one entry per (id, fragment, file).
  - `okfreq validate` runs in the new mode on a scratch config at each commit.
- **Q41:**
  - D9: no simulated walk is written for every path; the tested card says so.
  - D7: CORE-007, CORE-008 and TRUST-014 may be accepted outside VS Code; CORE-006 stays in
    VS Code.
- **Q42:** the spec corrections, applied throughout. The CI wiring goes to CR-B; the other items
  are fixed figures and the D13, D14 and D16 wording.

### Taken by this spec

- **D1. Pin `okf-schema>=0.18.1`.** 0.18.0 is never used.
- **D2. Only live, non-exempt requirements declare scenarios.**
  - On the base, the 459 live SwRS are all `proposed`. 2 of them are exempt (Q39), so 457 SwRS
    declare `scenarios:` and get their headings renamed.
  - The 95 live StRS all declare `scenarios:` (after D6).
  - Retired requirements (superseded, deprecated) keep their body and get no `scenarios:`. No
    marker targets a retired SwRS (0 on the base), and "never untested" cannot hold for
    behaviour that no longer ships.
- **D3. The SwRS heading keeps its kind.**
  - With a kind (`nominal`, `boundary`, `refusal`, `failure`), the heading becomes
    `### Scenario S<n> (<kind>): <title>`; without one, `### Scenario S<n>: <title>`.
  - The `scenarios:` title is the text after the colon. A heading with no other text, such as
    `### Scenario: Nominal`, keeps that text as its title.
  - Reason: the viewer's kind badge and the Main paths `Option … (<kind>)` bullets read the kind.
- **D4. Ids follow body order, starting at `S1`.** On StRS, `Path <n>` becomes `S<n>`, except
  LIFE-023, whose `Path 0..3` become `S1..S4`.
- **D5. Retired SwRS that are not exempt get the exemption.**
  - Whatever its lifecycle, okfreq counts a SwRS as a coverage target and as a linked SwRS of its
    StRS unless it has `annotation_exemption: true`.
  - 97 retired SwRS (92 superseded, 5 deprecated) lack it, against the project convention. They
    keep `covered` from **46** live StRS.
  - Each gets `annotation_exemption: true` and an `exemption_reason` in the existing form:
    `Superseded by SwRS-…` naming its `superseded_by`, or `Archived. <why>` for a deprecated one.
  - This is metadata only, and none of the 97 is approved.
  - The change already helps the current mode's StRS status.
- **D6. The three live StRS with no path get paths:**
  - BLOCK-027, copy a selection as exact Markdown (SwRS BLOCK-271 to BLOCK-286);
  - TRUST-012, visible text and icon (SwRS TRUST-070, TRUST-074);
  - TRUST-014, pinned dependencies, ships what it loads (SwRS CORE-087, CORE-090, TRUST-075,
    TRUST-092).

  All three are `proposed`, so no owner agreement is needed. TRUST-012 and TRUST-014 start from
  the built VSIX (Q15). Each path cites only SwRS that `scripts/check_main_paths.py` accepts and
  states what the extension does today.
- **D7. Products other than the editor (Q41).**
  - CORE-007 (the release), CORE-008 (the site) and TRUST-014 (the built VSIX) take
    `@accepts_req` on the test closest to that product, under `test/build`, `test/security`,
    `test/site` or `test/core`.
  - CORE-006 (the writing skill) and TRUST-012 are accepted in VS Code like every other StRS.
  - The allow-list lives in the placement check (D10) and in project.guidelines "Benches" (D14).
- **D8 (CR-B). Acceptance layout.** See CR-B.
- **D9. "Tested" shows what the sort finds (Q41).**
  - `@tests_req StRS-X#S<n>` stays where an existing simulated test walks the path.
  - No new simulated walk is written.
  - The viewer's "Paths tested" card says that a path counts as tested only where a simulated walk
    exists.
- **D10. The marker check learns the new marker.** `scripts/check-marker-companions.mjs`
  changes as follows:
  - Its `MARKER` regex and the companion-line regex accept `@accepts_req` and an optional `#S<n>`
    after the ID.
  - The ID-exists check and the 3-ID block cap use the ID without its fragment: two fragments of
    one ID count as one ID.
  - New rule: a fragment names an id declared in the target's `scenarios:`.
  - New rule: a marker on a target with `scenarios:` has a fragment; a marker on a target without
    `scenarios:` has none. This is the new-mode error, enforced while the bundle is still in the
    old mode.
  - New rule: `@accepts_req` appears only under `test/integration/`, except for the D7 StRS, and
    never targets a SwRS.
  - New rule: no `@tests_req StRS-…` under `test/integration/` (a walk in real VS Code is an
    acceptance; Q28).
  - Each failure prints `<path>:<line>: <rule>: <marker>`.
  - The script reads `scenarios:` from the requirement files. Its tests in
    `test/build/checkMarkers.test.ts` include one case per new rule, and each case fails on the
    old script.
- **D11 (CR-B). Scenario coverage gate.** See CR-B.
- **D12. The viewer reads paths and scenarios from frontmatter and trace.**
  - `just requirements-report` and `just requirements-report-json` also write
    `okfreq trace requirements --json` to `out/reports/requirements/requirements-trace.json`.
  - The viewer counts declared paths and scenarios from the `scenarios:` frontmatter. It reads
    the files that test or accept each one from the trace's `scenario_markers`, by
    (id, fragment).
  - These counts do not depend on the coverage mode, because the old-mode report has no per-path
    fields.
- **D13. The vendored okfreq text is refreshed from v0.18.1.**
  - The tool: `okfreq install-skills <temp-dir>` from okf-schema 0.18.1 (run through the
    justfile's `okfreq` command), into a temporary folder.
  - `okfreq/` and `okfreq-gardening/` are copied over `.agents/skills/okfreq/` and
    `.agents/skills/okfreq-gardening/`.
  - `okfreq-setup` is **not** vendored: the bundle already exists, and the okfreq skill already
    says "use `okfreq-setup` when it is installed; otherwise run `okfreq init`".
  - `requirements/guidelines/requirements.guidelines.md` becomes the guideline that
    `okfreq init` 0.18.1 writes into a temporary folder. That copy already has the
    `@implements_req` line stripped.
  - `requirements/guidelines/okfreq-baseline.guidelines.md` is refreshed the same way if it
    matches an okf-schema file, and left as is otherwise. Nothing links to it.
  - A short "Studio benches" note is added at the end of `.agents/skills/okfreq/SKILL.md`. It
    points to project.guidelines "Benches" and is re-added after any later refresh.
- **D14. project.guidelines gets a "Benches" section and the new heading forms.**
  - "Benches" states Q28, the D7 allow-list and, from CR-B on, the acceptance layout. In CR-A it
    names that layout as "added by the acceptance CR".
  - "Main paths of a StRS" shows `#### Path S<n>:` and the `scenarios:` block.
  - A new "Scenarios of a SwRS" section shows `### Scenario S<n> (<kind>): <title>`. It states
    that this project form **overrides** the packaged guideline's `### Scenario S<n>: <title>`:
    project.guidelines ranks above the shared guideline for this project.
  - "Marker placement" shows the `#S<n>` fragment and the D10 rules.
- **D15 (CR-B). Waiver candidates: none.** See CR-B.
- **D16. Stack parent.**
  - CR-A's parent is the linearised batch-09 stack once CR-492 to CR-503 are merged, including
    the clip CRs and the vega chart CRs 502 and 503.
  - The coder recounts every figure and every marker there. The sort, the fragments and the
    checks cover the requirements and markers those CRs add.
- **D17. Approved SwRS.** On the base, none of the 459 live SwRS is approved (all are `proposed`,
  2 of them exempt). If the parent has an approved SwRS, it gets no rename and no `scenarios:`,
  and the coder reports it to the Foreman.

### Approved requirements changed

These 15 StRS get `scenarios:` (Q24) and the heading rename (Q31). Per Q38, `approved_at` is set
to the time of the change, `approved_by` stays the owner, the PR body lists them under "Approved
requirements changed", and the owner's review is requested on the PR. The owner is
`default_owner_email` of `requirements/config.yml`.

StRS-MDOKFSTUDIO-BLOCK-003, BLOCK-011, BLOCK-025, DIAG-001, DIAG-006, GFM-002, LAYOUT-001,
LAYOUT-003, PALETTE-015, CORE-001, REVIEW-001, REVIEW-003, REVIEW-012, REVIEW-015, TABLE-001
(30 paths).

No other approved text changes. Adding a path or a scenario to an approved requirement, or
removing one, is a normative change. The coder does not make it and reports it.

## What changes, area by area

### 1. Dependency and bundle schemas

- `pyproject.toml`: in the `requirements` group, `okf-schema>=0.17.0` becomes
  `okf-schema>=0.18.1`. `uv.lock` is relocked (`uv lock --upgrade-package okf-schema`).
- `requirements/tiers/_schema/base.schema.yaml`, `strs.schema.yaml` and `swrs.schema.yaml` get the
  0.18 declarations, copied from a fresh `okfreq init` run in a temporary folder with okf-schema
  0.18.1:
  - base: `scenarios`, and the lifecycle description text with its `scenarios:` exception;
  - strs: `tested_in_files`, `accepted_in_files`, `acceptance_exemption`,
    `acceptance_exemption_reason` and the top-level description;
  - swrs: `accepted_in_files` with `maxItems: 0`, and its description.

  The Studio's own additions to these schemas stay (the OKF projections and `req_lifecycle`).
- `requirements/config.yml`: add `markers.accepts: '@accepts_req'`, and add `accepted_in_files`
  to `generated_fields`. **`strs_test_coverage_mode` is not changed.**

### 2. Requirements migration (scripted, then reviewed)

A one-off script in the scratch space (not committed) runs on the parent:

- On each live StRS with `#### Path <n>: <title>` headings: rename them to
  `#### Path S<n>: <title>` (D4) and add `scenarios:`, one `{id, title}` per path. On the 15
  approved StRS, also set `approved_at` (Q38).
- On each live, non-exempt SwRS (D2): rename `### Scenario[ (<kind>)]: <title>` to
  `### Scenario S<n>[ (<kind>)]: <title>` (D3) and add `scenarios:`.
- On the 97 retired, non-exempt SwRS: add `annotation_exemption: true` and an `exemption_reason`
  (D5).

Then, by hand: Main paths and `scenarios:` for BLOCK-027, TRUST-012 and TRUST-014 (D6).

`scripts/check_main_paths.py` keeps working: it reads `### Main paths` and the SwRS citations,
not the path headings. Its fixtures in `test/build/test_check_main_paths.py` gain a `Path S1:`
case.

### 3. Markers

The sort and the sweep read the test files, not `okfreq trace`, because trace keeps only the
first line per (id, fragment, file).

- **StRS markers.** On the base there are 185 lines in 62 files, plus the lower CRs' markers,
  recounted on the parent. Each one is read and classified with the rubric of
  `experiments/02-audit-sample.md` (walks a path / partial path / single-state snapshot / SwRS
  duplicate / other). The outcome depends on the class:
  - walks path n in real VS Code (`test/integration`) → `@accepts_req StRS-X#S<n>`;
  - walks path n on the simulated bench → `@tests_req StRS-X#S<n>`;
  - walks a path of a D7 StRS → `@accepts_req StRS-X#S<n>` on the closest test;
  - anything else → removed. Its `@tests_req SwRS` markers stay, because a snapshot or a
    one-transition test is a SwRS test.

  The PR body holds the classification table: file, line, StRS, class, outcome.
- **SwRS markers.** On the base there are 3959 `@tests_req SwRS-…` lines, plus the lower CRs'
  markers.
  - Each marker on a SwRS that declares `scenarios:` becomes one `@tests_req SwRS-X#S<n>` per
    scenario the test checks (Q30).
  - The scenario is read from the test, not guessed from the test's name.
  - Markers on the two exempt SwRS stay fragmentless (Q39).
  - A test that checks no declared scenario is read again. Either it checks a scenario the SwRS
    does not declare yet (add it: a normative change, allowed on a proposed SwRS), or the marker
    moves to the SwRS the test does check.
- A marker block still names at most 3 distinct IDs (D10). `scripts/marker-baseline.json` may
  only shrink.
- Scenarios that no marker covers after the sweep stay declared and are listed in the PR body. CR-B
  writes their tests or prunes them (Q30b).

### 4. Requirements viewer (`test/site/requirementsViewer/`)

- `model.ts`:
  - reads `scenarios:` per requirement, and joins `requirements-trace.json` (D12) to get the
    files that test and that accept each StRS path and each SwRS scenario;
  - `parseScenarios` accepts the optional `S<n>` id in `### Scenario S<n> (<kind>): <title>` and
    keeps the kind;
  - `stakeholderValidated` is replaced by the report's StRS status `covered`;
  - the scope stats gain paths total, tested and accepted, StRS covered, and scenarios total and
    tested.
- `mainPaths.ts`: `PATH_HEADING` accepts `Path S<n>:` and yields the id, and the title without
  the id.
- `home.ts`:
  - New cards: "StRS paths tested t/N", "StRS paths accepted a/N" (N = live StRS paths), "StRS
    covered c/M" (M = live StRS) and "SwRS scenarios tested s/S".
  - The "StRS with a stakeholder validation test" card is removed.
  - The "Paths tested" card carries the D9 note.
  - The "StRS covered" card's caption says it follows okfreq's current coverage mode. CR-B changes
    the caption with the switch.
  - Area table: columns "Paths tested" and "Paths accepted" after "Tested".
- `pages.ts`:
  - The use case page lists each path (`S<n>` and its title) with its tested files and its
    accepted files. It shows a "waived" badge with the reason when `acceptance_exemption` is
    set; none is set in CR-A.
  - The behaviour page lists each scenario with its tests and marks the untested ones as
    "missing".
- Tests: `model.test`, `home.test`, `mainPaths.test`, `pages.test`, `write.test` and `fixture.ts`
  are updated. Each new reading has a test that fails on the old code.
- The Studio's SwRS for the requirements viewer and for the marker check are updated for the new
  cards, columns, pages and rules. They carry `@implements_req` and `@tests_req …#S<n>` markers,
  and are created `proposed` when new.

### 5. justfile

`requirements-report` and `requirements-report-json` also write `requirements-trace.json` (D12).
No other target changes in CR-A.

### 6. Docs and skills

- `CONTRIBUTING.md`: the bench convention (Q28, D7), the `check-markers` rules (D10) and the
  viewer cards. The CI section is unchanged in CR-A.
- `requirements/guidelines/project.guidelines.md`: D14.
- `.agents/skills/okfreq/`, `.agents/skills/okfreq-gardening/`,
  `requirements/guidelines/requirements.guidelines.md`: D13.
- `.agents/glossary/common.md`: the terms "acceptance test", "path (StRS)", "scenario (SwRS)",
  "accepted" and "waiver".
- `requirements/tiers/log.md`: one entry under `## 2026-11-<day>`, with `### Topic` sub-headings
  for:
  - the migration (the Q24 and Q31/Q38 agreements, D2 to D4, D6);
  - the retired exemptions (D5);
  - the marker sort.
- No change to the writing skill `skills/writing-for-markdown-okf-schema-studio/`: no rendered
  syntax changes.
- After the changes, run `just requirements-update` and commit the files it generates.

## Commit order

Each commit leaves `just requirements-lint` and `just check` green. Each commit also passes the
scratch new-mode validation (Evidence, check 3) with zero errors. So the `scenarios:` of a
requirement and the fragments of its markers land in the same commit.

1. The bump, the schemas, `markers.accepts` and `generated_fields`.
2. The retired SwRS exemptions (D5).
3. The marker check (D10). Its rules already pass, because no requirement declares scenarios
   yet.
4. Per e2e group, or in one commit, for each group:
   - `scenarios:` and the heading renames;
   - the SwRS fragment sweep;
   - the StRS marker sort for that group's StRS.

   The log entry and the approved StRS go in the first of these commits.
5. New paths for BLOCK-027, TRUST-012 and TRUST-014 (D6), with their markers.
6. The viewer.
7. The docs and the skills.
8. `just requirements-update`.

The coder may split these commits further, but keeps this order.

## Out of scope (all of it is in "Handed to the next CR (CR-B)" unless noted)

- The mode switch and the D11 gate.
- Missing SwRS scenario tests and their pruning.
- Acceptance tests, the acceptance CI job and all CI wiring.
- Any change to okf-schema itself (not in CR-B either).
- Retired requirements, beyond the D5 exemption (not in CR-B either).
- A simulated walk for every StRS path (D9; not in CR-B either).
- Counting passing tests rather than markers (Q35).
- Normative changes to approved requirements beyond Q24 and Q31/Q38.
- `src/` runtime code. A bug found on the way is filed, not fixed here.
- Making the use case diagram mandatory.

## CI environment

No CI job or workflow changes in CR-A. `requirements-lint`, `check` and the viewer tests run in
the existing `static`, `static-windows` and `report` jobs, as today.

## Evidence

Every check on a shipped file reads it from the repository at the head under test.

### Checks

1. `just requirements-lint` passes, still in the old mode.
2. On the head, `requirements/config.yml` meets all of these:
   - it keeps the old `strs_test_coverage_mode`;
   - it has `markers.accepts: '@accepts_req'`;
   - it lists `accepted_in_files` in `generated_fields`.

   Also, `pyproject.toml` pins `okf-schema>=0.18.1`, and `uv.lock` resolves 0.18.1 or later.
3. **Scratch new-mode validation, at every commit.** Copy `requirements/` into a scratch folder
   and set `strs_test_coverage_mode: linked-swrs-and-acceptance-paths` there. Then run
   `okfreq validate <scratch> --check-links --project-root .`.
   - It reports **0 errors**: no fragment error, no schema error, no `@accepts_req` on a SwRS.
   - It reports no W003.
   - W004 may remain; CR-B removes it.

   The PR body gives the summary line of the last commit's run.
4. On the head, every live StRS and every live, non-exempt SwRS declares `scenarios:`. A scan of
   the requirement files must show:
   - ids that match their body headings one for one;
   - no `#### Path [0-9]` heading in `requirements/tiers`;
   - no `### Scenario:` or `### Scenario (` heading in a live SwRS;
   - no `scenarios:` on TRUST-070, TRUST-075 or any retired requirement.
5. A scan of every test file on the head (not trace) must show:
   - no `@tests_req StRS-…` without a fragment;
   - no `@tests_req StRS-…` under `test/integration/`;
   - `@accepts_req` only under `test/integration/` or on a D7 StRS;
   - no fragmentless marker on a target that declares scenarios.
6. The 97 SwRS of D5 have `annotation_exemption: true` and a reason. The 15 approved StRS have
   `approved_at` set by this change, and the same `approved_by`.
7. `just check` passes. It runs check-markers with the D10 rules, and each rule has a test that
   fails on the old script.
8. `just release-tests` passes, with the `Path S1:` case of `test_check_main_paths.py`.
9. The viewer unit tests pass, and each new reading has a test that fails on the parent.
10. `just preflight` passes. On Windows that is the static stage only; CI runs the rest.
11. `requirements/tiers/log.md` on the head has the dated entry with the agreements, D5 and the
    sort.

### Scenario steps (owner's view)

1. Build the site (`just ci-report`) and open the requirements viewer home. The four cards of
   Q33 are there, and the old validation card is gone. "Paths accepted" shows the count the sort
   found.
2. Open the area table: the "Paths tested" and "Paths accepted" columns are filled for every area.
3. Open the use case page of StRS-MDOKFSTUDIO-LIFE-023. It shows four paths, `S1` to `S4`, each
   with the files that test or accept it.
4. Open a SwRS page: each scenario lists its tests, and the untested ones are marked "missing".
5. Add `@accepts_req StRS-…#S1` to a `test/visual` file and run `just check-markers`. It fails
   with the placement rule. Restore the file.
6. Remove the fragment from one `@tests_req SwRS-…#S1` marker and run `just check-markers`. It
   fails with the fragment rule. Restore it.

## Self-containment

The coder needs:

- this spec;
- `02-answers.md` and `experiments/02-audit-sample.md` (the sort rubric) from this CR folder;
- the released okf-schema 0.18.1 docs named at the top;
- the repository's own rules.

Every figure comes from the base named at the top and is recounted on the parent (D16).

## Open questions

None. The coder stops and reports to the Foreman in these cases:

- an approved SwRS turns up on the parent;
- a normative change to an approved requirement is needed.

## Handed to the next CR (CR-B)

CR-B is filed after CR-A is final and is stacked on CR-A (Q36). Its spec-writer starts from this
section, `02-answers.md` (Q3, Q6, Q27, Q30, Q30b, Q32, Q35, Q37, Q40, Q41, Q42) and the CR-A head.

1. **Missing SwRS scenario tests (Q30, Q30b).**
   - Start from the list in CR-A's PR body, recounted on CR-A's head.
   - For each declared scenario with no `@tests_req …#S<n>`, write the test on the bench where
     its siblings live, or remove the scenario. Remove it only when another scenario or SwRS
     already says the same, or when it cannot be observed.
   - List every removal in the PR with its reason and log it in `tiers/log.md`.
   - Removing a scenario from an approved requirement goes to the owner.
2. **Acceptance tests (Q1, Q3, Q6, Q32, D7).** Every live StRS path without an `@accepts_req`
   gets one.
   - One nominal path per test, end to end, with the final result asserted.
   - A human step is a simulated input; the test asserts the gate and the content.
   - CORE-007 S1 stops before CORE-078, the maintainer's review.
   - CORE-007, CORE-008 and TRUST-014 may be accepted on their D7 bench. Every other StRS,
     CORE-006 included, is accepted in real VS Code.
3. **Acceptance layout (D8).**
   - Each e2e group of `test/shared/e2eGroups.ts` gets a file
     `test/integration/acceptance/<group>.acceptance.ts`, under 1500 lines and split when needed.
   - `test/integration/acceptance-suite.ts` loads them.
   - `run-tests.ts` gains `--acceptance-only`.
   - The manifest goes to `out/reports/acceptance/acceptance-manifest.json`, with the same shape
     as `integration-manifest.json`.
   - Existing `test/integration` tests already re-marked `@accepts_req` by CR-A stay where they
     are.
4. **Acceptance budget (Q37).**
   - Each e2e group shares one window. A group may use several launches, each with its own budget
     under the 15-minute launch deadline.
   - The job is sharded by group in a matrix.
   - The spec states the expected step duration.
   - No stress-plan entry is needed; the spec says so.
   - No fresh window per test, and no raised timeouts.
5. **Scripts and targets (Q42).**
   - `package.json` gets `test:acceptance`, which includes `npm run bundle` before the run.
   - `just ci-acceptance` opens the e2e campaign like `ci-integration`
     (`scripts/e2e-campaign.mjs begin acceptance`, `_require-unlocked-screen`, the hang
     watchdog).
   - `just preflight` runs it.
6. **CI wiring (Q42).**
   - The job `acceptance` has the same trigger as `integration` (push to `main`, heavy dispatch).
     It runs `ubuntu-latest` under `xvfb-run`, from the lock files with no local caches, with a
     matrix by group, the hang dump step, and the per-attempt artifact named `-attempt-<n>`
     through a job output.
   - `tag-release` needs `acceptance`. The `report` and `checks` jobs, and the pages build, take
     the acceptance results.
   - ci.guidelines rules 11, 13 and 14 apply.
   - The CI job list in `AGENTS.md` and in CONTRIBUTING's CI section is updated.
   - The first heavy dispatch provides the measured duration, which sets the timeouts at about
     twice it with no retries, and the manifest artifact.
7. **D11 gate (Q40).** The new `scripts/check_scenario_coverage.py` runs
   `okfreq generate-report requirements --output-json <file under out/>` itself, then reads it.
   - It fails when a live, non-exempt SwRS has a non-empty `transitions.missing`.
   - It fails when a live StRS has `paths.accepted < paths.total` without `acceptance_exemption`.
   - It fails when a live StRS has no `scenarios:`.
   - It prints one line per gap, and ends with
     `scenario coverage: <s> SwRS scenarios tested, <p>/<P> StRS paths accepted, all complete`.
   - It runs in `just requirements-lint`, with tests in
     `test/build/test_check_scenario_coverage.py` run by `release-tests`.
   - It lands with the switch.
8. **Mode switch (Q27).**
   - `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`, then `just requirements-update`.
   - Commit what it generates (`tested_in_files`, `accepted_in_files`, the coverage fields).
   - Log it in `tiers/log.md`.
   - The viewer's "StRS covered" caption changes to the new rule.
9. **Waiver candidates (D15): none.**
   - CORE-006: the agent's writing is a simulated input.
   - CORE-007: its test stops before the review.
   - A StRS found to have no step that can be automated goes to the owner. The coder never
     writes a waiver itself.
10. **D14 completion.** The "Benches" section of project.guidelines gets the acceptance layout and
    the job.
11. **CR-B evidence.**
    - The report shows paths accepted = total, live StRS covered M/M and every live, non-exempt
      SwRS with no missing transition.
    - No W003, no W004, no errors.
    - `just requirements-lint`, `just check` and `just preflight` pass.
    - A heavy dispatch on the branch head is green for `integration` and every `acceptance`
      shard.
