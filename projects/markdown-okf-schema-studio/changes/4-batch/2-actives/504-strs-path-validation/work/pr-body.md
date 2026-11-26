## Summary

The requirements bundle moves to okf-schema 0.18.1, which lets a requirement declare the paths or scenarios a test must name (`#S<n>`) and adds the `@accepts_req` marker for acceptance tests. This PR keeps the current StRS coverage mode and prepares the declarations: the bundle schemas and configuration, the exemption of retired requirements, and a marker check that understands the new marker and the `#S<n>` fragments.

Every requirement group now declares its scenarios (SwRS) and paths (StRS) with stable ids `S<n>`, and every test marker on a declaring requirement names its fragment. The requirements viewer shows, per path and per scenario, the test files that test or accept it, with new cards and columns. The coverage mode is not switched here.

One consequence to know before merging: in the current coverage mode the report's "StRS covered" figure goes from 23 of 95 on `main` to 1 of 95 until the follow-up change switches the mode (see Impacts).

## Deliverables

The marker check gains seven rules and a baseline for StRS markers still in integration tests:

| Rule | What it rejects |
| --- | --- |
| `fragment-undeclared` | a `#S<n>` the target does not declare |
| `fragment-required` | a fragmentless marker on a target that declares `scenarios:` |
| `fragment-unexpected` | a fragment on a target with no `scenarios:` |
| `accepts-on-swrs` | `@accepts_req` on a SwRS |
| `accepts-placement` | `@accepts_req` outside `test/integration`; StRS CORE-007, CORE-008 and TRUST-014 may also sit under `test/build`, `test/security`, `test/site` or `test/core` |
| `implements-fragment` | a `#S<n>` fragment on `@implements_req` |
| `strs-tests-in-integration` | a new `@tests_req StRS-...` in `test/integration` (the baseline is now empty) |

Choices made:

- The coverage mode is not switched here; the old mode keeps working with the new schemas.
- The 97 retired SwRS get an explicit exemption from markers (`annotation_exemption` with a reason), so okfreq expects no marker on them; in the current coverage mode their StRS still list them as missing (see Impacts).
- A new SwRS (`SwRS-MDOKFSTUDIO-CORE-097`) states the behaviour of the marker check, each rule tested by its own test.
- The requirements that `main` added or extended meanwhile (DIAG-121, DIAG-123, LAYOUT-023 and CORE-096) have numbered scenarios too, and the markers of their tests name a fragment or are gone (see Known gaps). Their scenario and normative text is unchanged.
- All 16 requirement groups declare `scenarios:` and carry `Scenario S<n>` / `Path S<n>` headings; each SwRS test marker is one line per scenario.
- StRS markers in tests were sorted (table in Details, 187 rows for 185 markers): a marker stays only where the test walks the whole declared path. 19 rows are `@accepts_req` (walks in real VS Code), 7 are `@tests_req` (walks on the simulated bench), 161 are removed, each with its class (partial path 111, single-state snapshot 27, SwRS duplicate 12, other 11). The 26 kept markers cover 23 of 156 paths (17 accepted, 6 tested). The SwRS markers stay, except those the review of the fragments dropped because their test checks no declared scenario (see Known gaps).
- The mutation report reads the `#S<n>` fragments.
- The requirements viewer reads `scenarios:` from the requirement files and joins them with the okfreq trace: home cards "StRS paths tested", "StRS paths accepted", "StRS covered" and "SwRS scenarios tested" (the "StRS with a stakeholder validation test" card is removed), area columns "Paths tested" and "Paths accepted", the tested and accepted files of each path on a use case page, and the tests of each scenario, or "missing", on a behaviour page. Without a trace the declared counts stay and the file figures read "n/a". SwRS CORE-069, CORE-080 and CORE-082 gain the scenarios for this.
- `just requirements-report` and `just requirements-report-json` also write `out/reports/requirements/requirements-trace.json`.
- The vendored okfreq and okfreq-gardening skills and `requirements/guidelines/requirements.guidelines.md` are refreshed from okf-schema 0.18.1; the Studio's bench convention is in a new "Benches" section of the project guidelines and in CONTRIBUTING; the glossary gains "acceptance test", "accepted", "path (StRS)", "scenario (SwRS)" and "waiver".
- The three live StRS that had no path get paths: BLOCK-027 (copy a selection verbatim; copy a selection cut inside a construct), TRUST-012 (read a text of the preview; find the Studio in the Extensions view) and TRUST-014 (install and package from pinned dependencies). `main` had none of them.

### Approved requirements changed

The 15 approved StRS only get `approved_at` and `verified.at` set to the time of the scripted rename and, all 15, the `scenarios:` block and the renamed path headings; no normative text changed. Owner review of this PR is their re-approval: BLOCK-003, BLOCK-011, BLOCK-025, DIAG-001, DIAG-006, GFM-002, LAYOUT-001, LAYOUT-003, PALETTE-015, CORE-001, REVIEW-001, REVIEW-003, REVIEW-012, REVIEW-015, TABLE-001.

### Validation in the new coverage mode (scratch, not applied)

Measured before the restack on `main`, at `1905009`: a scratch copy of the bundle and of the sources, with the mode set to `linked-swrs-and-acceptance-paths`, validated with 0 errors and 104 warnings: W004 x78 (a StRS with no `@accepts_req` yet) and W2 x26 (placeholder cross-links that existed before). The mode switch and the W004 are for the follow-up change.

## Blast radius

Grade: **2**. The check script, the bundle schemas and the Python lock change; a `git revert` restores the previous state, but the new schemas and the exemptions must go back together.

## Autonomous decisions

- The project guidelines' limit of "one to three paths" per StRS is reworded, since every live StRS now declares a path and LIFE-023 declares four.
- TRUST-014 has no second path for linting and drawing the use case diagrams (SwRS CORE-087 and CORE-090): they are build-time checks no path cites.
- The StRS markers' sort was carried out by an agent by the agreed classes; the re-approval of the 15 approved StRS by the review of this PR follows the owner's agreement to the scripted rename.
- A migration script, run group by group, declared `scenarios:` and renamed the headings. The migration commits carry the fragments of the markers that existed before the restack on `main`; the fragments of the chart, gallery and Auto width tests of `main` arrive only in the last commit (see Known gaps).
- The scenario fragment of each SwRS test marker was first chosen by a keyword match between the scenario titles and the test, with `S1` when nothing matched. The 486 weakest matches were then read one by one against the test (484 decisions, two entries repeating a block already decided: 142 kept, 206 moved to the scenario really exercised, 136 dropped because the test checks no declared scenario). The other fragments the migration assigned, and 45 lines on 6 SwRS with generic scenarios, are as the match assigned them and were not read against their test.
- StRS markers in tests were sorted: kept as `@tests_req` or `@accepts_req` on a declared path, or removed (a snapshot, a partial path, a duplicate of a SwRS marker, or another reason named in the table); `strsTestsInIntegration` is now empty. SwRS markers go only where the fragment review found no declared scenario checked (for example TRUST-005, TRUST-090, REVIEW-219, LIFE-169, LIFE-170 in some `test/integration` files).
- The exemption reason of a replaced SwRS names its successor with one shared text; LIFE-174 and LIFE-182 to 185, archived with no successor, each have their own reason.
- The viewer's new behaviour is stated as new scenarios of three existing `proposed` SwRS (CORE-069, CORE-080, CORE-082), with no new SwRS.
- `requirements/guidelines/okfreq-baseline.guidelines.md` is left as it is: it matches no okf-schema file.
- The project guidelines state their own SwRS scenario heading, with the kind, which overrides the refreshed shared guideline.
- Two deliveries, decided during preparation: this PR declares the paths and scenarios in the current coverage mode; the mode switch is deferred to a follow-up change.
- No simulated walk is written for every StRS path: the viewer shows what the marker sort finds and says so. The release, site and package StRS (CORE-007, CORE-008, TRUST-014) may be accepted outside VS Code; CORE-006 stays in VS Code.
- Two problems found in review are left to a follow-up change instead of being fixed here: the 136 marker blocks dropped by the fragment review, and the wrong scenario fragments (both described under Known gaps).
- The StRS markers follow a strict rule, and 26 marker lines meet it. A marker stays only if the starting state is set up; each step is performed through the product mechanism (a stub for the user's choice in a native dialog or for the OS clipboard is accepted; an injected page message, a test hook or a faked host result is not); every state and outcome named in a step is asserted (`Option` bullets aside; for an "or", one side); a path whose only step is the page's own rendering counts when every outcome is asserted; in doubt the marker is removed.

## Known gaps

Left for the follow-up change:

- 722 of 2633 in-force SwRS scenarios have no scenario marker (list in Details).
- 133 of 156 StRS paths have no marker (list in Details).
- 78 of 95 StRS have no acceptance test (W004, markers scanned).

Also left for the follow-up change, found in review:

- The review of the fragments dropped 136 marker blocks whose test checks no declared scenario. Each needs either the missing scenario declared or the marker moved to the SwRS the test does check; neither is done for these blocks.
- Some SwRS fragments name a scenario their test does not check, so the "scenarios tested" figures can overstate. 3 of 16 sampled lines are wrong: `test/core/render/mathRenderer.test.ts` line 52 (MYST-024 S8), `test/core/render/alertSourceLines.test.ts` line 150 (GFM-009 S10) and `test/session/lineEndingSave.test.ts` line 40 (BLOCK-234 S3). Apart from the weakest matches that were re-read, and including 45 lines on 6 SwRS with generic scenarios, the migrated fragments are as a keyword match assigned them (`S1` when nothing matched), not read against their test.
- The dropped blocks removed the last `test/integration` marker of 12 SwRS: BLOCK-053, BLOCK-216, CORE-022, CORE-043, DIAG-001, FMEDIT-024, FMSCHEMA-001, FMSCHEMA-084, LIFE-001, PALETTE-031, PALETTE-217 and THEME-001.
- The chart, gallery and Auto width tests that arrived from `main` were brought under the same rule: 15 marker lines were removed, among them tests that check no declared scenario of the requirement they named. These include the DIAG-009 view cache rules, the DIAG-123 input binding, hover box placement and chart runtime, the LAYOUT-023 Mermaid figure that is not a code block, and the CORE-096 gallery page markup and HTML escaping; each needs a declared scenario or no marker. One further line was removed from a style test that checks no redraw (DIAG-123 S2).
- DIAG-009 S3 on the chart find and patch test is a judgement call: the scenario names Mermaid and PlantUML, the test checks that charts keep their view through a patch. The verification notes of DIAG-009 still name `chartViewCache.test.ts`, which has no DIAG-009 marker.
- A known issue of LAYOUT-023 about a table of contents with Auto width may be out of date, and its S5 table still refers to "the code block scenario", now S8; neither text was changed.

Others:

- Only the head of this branch passes the marker check: the five commits from `0796f53c` to `8d72801e` fail it (`just check`, 54 `fragment-required`) and the validation in the new coverage mode (14 errors), because the fragments of the chart, gallery and Auto width tests of `main` arrive in the last commit. The first commit passes both. A merge by rebase puts these commits on `main`; a squash merge does not.
- "StRS covered" reads 1 of 95 in the current coverage mode (see Impacts).
- `StRS-MDOKFSTUDIO-LIFE-023` shows its four paths with no tested or accepted file: no test marker names it.
- Of the 133 StRS paths without a marker, these 66 had a candidate marker at the last re-read, which the strict marker rule removed for a partial walk, a single-state snapshot or another case named in the table. BLOCK 001 S1, 003 S1, 008 S2, 011 S2, 014 S2, 016 S1, 025 S2; CODE 001 S2, 004 S1; CORE 001 S2, 002 S1, 007 S1, 008 S1; DIAG 001 S2, 006 S1, 015 S2; FMEDIT 001 S1, 008 S1; FMSCHEMA 006 S1, 010 S1, 014 S1; GFM 003 S1; LAYOUT 001 S1, 004 S1; LIFE 001 S1, 003 S1, 005 S1, 014 S1, 022 S1; MYST 006 S1, 007 S1, 007 S2, 009 S1, 009 S2, 016 S1, 017 S1; PALETTE 002 S1, 005 S1, 007 S1, 015 S1, 018 S2, 019 S1; REVIEW 001 S1, 003 S1, 015 S1, 017 S1; TABLE 001 S1, 002 S1, 008 S1, 013 S1, 015 S1; THEME 002 S1, 011 S1; TOOLBAR 004 S1, 006 S1, 009 S1, 011 S1, 013 S1, 013 S2, 014 S1; TRUST 001 S1, 004 S1, 006 S1, 012 S1, 012 S2, 014 S1. None of CORE-007, CORE-008, TRUST-012 and TRUST-014 has a marker: their tests run outside a real VS Code and do not walk the path.
- A test that walks only part of a path, or injects or fakes one of its steps, carries no marker for it, even where it exercises most of the path (for example MYST-007 S1, TABLE-015 S1, TABLE-001 S1, LIFE-014 S1, TRUST-004 S1, BLOCK-011 S2, CODE-004 S1, MYST-009 S1 and DIAG-001 S2).
- No screenshot of the requirements site is posted. The "Tested by" block of a scenario card has no horizontal padding: its label and file rows touch the card border.
- The paths of TRUST-012 and TRUST-014 do not start from the built VSIX: their steps start from the running Studio and from a maintainer's install, because a path cites only SwRS that state what the extension does today.
- A scenario of CORE-069 says the counts do not depend on the coverage mode, while the "StRS covered" count follows it.

<details>
<summary>Details</summary>

## StRS marker classification

Every StRS marker (file, line, StRS, class, outcome), before and after the sort (`Line before` at commit e5ee7ec1, taken before the restack on `main`; `Line now` in this PR). A marker stays only where the test walks the whole declared path (the rule is under Autonomous decisions).
| File | Line before | StRS | Class | Outcome | Line now |
|---|---|---|---|---|---|
| test/build/test_plugin_manifests.py | 93 | StRS-MDOKFSTUDIO-CORE-006 | partial path | marker removed | - |
| test/build/test_release.py | 322 | StRS-MDOKFSTUDIO-CORE-007 | partial path | marker removed | - |
| test/core/frontmatter/diagReq.frontmatter.requirements.test.ts | 54 | StRS-MDOKFSTUDIO-FMSCHEMA-001 | SwRS duplicate | marker removed | - |
| test/core/render/writingSkill.test.ts | 134 | StRS-MDOKFSTUDIO-CORE-006 | partial path | marker removed | - |
| test/integration/blockClipboard.test.ts | 82 | StRS-MDOKFSTUDIO-BLOCK-025 | partial path | marker removed | - |
| test/integration/blockClipboard.test.ts | 83 | StRS-MDOKFSTUDIO-BLOCK-016 | partial path | marker removed | - |
| test/integration/blockMove.test.ts | 36 | StRS-MDOKFSTUDIO-BLOCK-025 | other: block move, not an editor edit | marker removed | - |
| test/integration/blockMove.test.ts | 37 | StRS-MDOKFSTUDIO-BLOCK-014 | partial path | marker removed | - |
| test/integration/blockMove.test.ts | 78 | StRS-MDOKFSTUDIO-TRUST-009 | SwRS duplicate | marker removed | - |
| test/integration/checkboxToggle.test.ts | 66 | StRS-MDOKFSTUDIO-GFM-003 | partial path | marker removed | - |
| test/integration/commentAnchors.test.ts | 32 | StRS-MDOKFSTUDIO-REVIEW-008 | real VS Code path | @accepts_req #S1 | 32 |
| test/integration/commentAnchors.test.ts | 33 | StRS-MDOKFSTUDIO-REVIEW-001 | partial path | marker removed | - |
| test/integration/commentWrite.test.ts | 37 | StRS-MDOKFSTUDIO-REVIEW-001 | other: writes threads, no highlight click | marker removed | - |
| test/integration/commentWrite.test.ts | 38 | StRS-MDOKFSTUDIO-REVIEW-003 | partial path | marker removed | - |
| test/integration/commentWrite.test.ts | 121 | StRS-MDOKFSTUDIO-TRUST-009 | SwRS duplicate | marker removed | - |
| test/integration/commentWrite.test.ts | 222 | StRS-MDOKFSTUDIO-TRUST-001 | partial path | marker removed | - |
| test/integration/dirtySnapshots.test.ts | 67 | StRS-MDOKFSTUDIO-LIFE-005 | partial path | marker removed | - |
| test/integration/editKeys.test.ts | 38 | StRS-MDOKFSTUDIO-BLOCK-008 | SwRS duplicate | marker removed | - |
| test/integration/editToolbarCover.test.ts | 86 | StRS-MDOKFSTUDIO-PALETTE-005 | SwRS duplicate | marker removed | - |
| test/integration/exportHtml.test.ts | 51 | StRS-MDOKFSTUDIO-TOOLBAR-014 | partial path | marker removed | - |
| test/integration/findInPreview.test.ts | 72 | StRS-MDOKFSTUDIO-TOOLBAR-003 | real VS Code path | @accepts_req #S1 | 72 |
| test/integration/imagePaste.test.ts | 26 | StRS-MDOKFSTUDIO-PALETTE-018 | partial path | marker removed | - |
| test/integration/imagePicker.test.ts | 26 | StRS-MDOKFSTUDIO-PALETTE-007 | partial path | marker removed | - |
| test/integration/inlineThread.test.ts | 100 | StRS-MDOKFSTUDIO-REVIEW-015 | partial path | marker removed | - |
| test/integration/labelRename.test.ts | 35 | StRS-MDOKFSTUDIO-MYST-009 | partial path | marker removed | - |
| test/integration/lifecycle.test.ts | 43 | StRS-MDOKFSTUDIO-LIFE-001 | partial path | marker removed | - |
| test/integration/lifecycle.test.ts | 44 | StRS-MDOKFSTUDIO-LIFE-003 | partial path | marker removed | - |
| test/integration/lifecycle.test.ts | 45 | StRS-MDOKFSTUDIO-LIFE-007 | single-state snapshot | marker removed | - |
| test/integration/lifecycle.test.ts | 145 | StRS-MDOKFSTUDIO-THEME-004 | partial path | marker removed | - |
| test/integration/mystBlocksWindow.ts | 150 | StRS-MDOKFSTUDIO-MYST-016 | partial path | marker removed | - |
| test/integration/mystBlocksWindow.ts | 150 | StRS-MDOKFSTUDIO-MYST-016 | real VS Code path | @accepts_req #S2 | 150 |
| test/integration/mystDiagnostics.test.ts | 47 | StRS-MDOKFSTUDIO-MYST-007 | partial path | marker removed | - |
| test/integration/mystPickers.test.ts | 8 | StRS-MDOKFSTUDIO-PALETTE-013 | SwRS duplicate | marker removed | - |
| test/integration/paletteMode.test.ts | 39 | StRS-MDOKFSTUDIO-PALETTE-002 | partial path | marker removed | - |
| test/integration/previewEditing.test.ts | 45 | StRS-MDOKFSTUDIO-FMSCHEMA-001 | SwRS duplicate | marker removed | - |
| test/integration/previewEditing.test.ts | 141 | StRS-MDOKFSTUDIO-FMSCHEMA-014 | partial path | marker removed | - |
| test/integration/previewEditing.test.ts | 638 | StRS-MDOKFSTUDIO-BLOCK-003 | partial path | marker removed | - |
| test/integration/previewEditing.test.ts | 1042 | StRS-MDOKFSTUDIO-FMSCHEMA-010 | partial path | marker removed | - |
| test/integration/previewEditing.test.ts | 1123 | StRS-MDOKFSTUDIO-FMSCHEMA-006 | partial path | marker removed | - |
| test/integration/previewHistory.test.ts | 41 | StRS-MDOKFSTUDIO-TOOLBAR-009 | partial path | marker removed | - |
| test/integration/previewHistory.test.ts | 42 | StRS-MDOKFSTUDIO-TOOLBAR-011 | partial path | marker removed | - |
| test/integration/projectFeatures.test.ts | 138 | StRS-MDOKFSTUDIO-CORE-002 | partial path | marker removed | - |
| test/integration/projectFeatures.test.ts | 153 | StRS-MDOKFSTUDIO-CORE-002 | other: unreadable include refusal | marker removed | - |
| test/integration/radioChoice.test.ts | 187 | StRS-MDOKFSTUDIO-GFM-005 | real VS Code path | @accepts_req #S1 | 187 |
| test/integration/realInput/blockKeys.ts | 139 | StRS-MDOKFSTUDIO-REVIEW-012 | SwRS duplicate | marker removed | - |
| test/integration/realInput/blockKeys.ts | 225 | StRS-MDOKFSTUDIO-REVIEW-012 | real VS Code path | @accepts_req #S2 | 225 |
| test/integration/realInput/blockKeys.ts | 280 | StRS-MDOKFSTUDIO-BLOCK-014 | partial path | marker removed | - |
| test/integration/realInput/blockKeys.ts | 346 | StRS-MDOKFSTUDIO-BLOCK-016 | partial path | marker removed | - |
| test/integration/realInput/blockKeys.ts | 549 | StRS-MDOKFSTUDIO-BLOCK-008 | partial path | marker removed | - |
| test/integration/realInput/blockKeys.ts | 606 | StRS-MDOKFSTUDIO-TABLE-015 | partial path | marker removed | - |
| test/integration/realInput/blockKeys.ts | 640 | StRS-MDOKFSTUDIO-TABLE-014 | real VS Code path | @accepts_req #S1 | 641 |
| test/integration/realInput/editorWidgets.ts | 385 | StRS-MDOKFSTUDIO-BLOCK-008 | real VS Code path | @accepts_req #S1 | 386 |
| test/integration/realInput/editorWidgets.ts | 427 | StRS-MDOKFSTUDIO-TABLE-001 | partial path | marker removed | - |
| test/integration/realInput/editorWidgets.ts | 683 | StRS-MDOKFSTUDIO-BLOCK-003 | partial path | marker removed | - |
| test/integration/realInput/editorWidgets.ts | 723 | StRS-MDOKFSTUDIO-BLOCK-003 | partial path | marker removed | - |
| test/integration/realInput/editorWidgets.ts | 770 | StRS-MDOKFSTUDIO-BLOCK-001 | SwRS duplicate | marker removed | - |
| test/integration/realInput/editorWidgets.ts | 850 | StRS-MDOKFSTUDIO-TABLE-006 | real VS Code path | @accepts_req #S1 | 850 |
| test/integration/realInput/editorWidgets.ts | 931 | StRS-MDOKFSTUDIO-TABLE-008 | partial path | marker removed | - |
| test/integration/realInput/flushBeforeNavigate.ts | 236 | StRS-MDOKFSTUDIO-BLOCK-006 | real VS Code path | @accepts_req #S2 | 236 |
| test/integration/realInput/flushBeforeNavigate.ts | 259 | StRS-MDOKFSTUDIO-BLOCK-006 | real VS Code path | @accepts_req #S2 | 260 |
| test/integration/realInput/flushBeforeNavigate.ts | 283 | StRS-MDOKFSTUDIO-BLOCK-006 | real VS Code path | @accepts_req #S2 | 284 |
| test/integration/realInput/flushBeforeNavigate.ts | 309 | StRS-MDOKFSTUDIO-TABLE-001 | partial path | marker removed | - |
| test/integration/realInput/flushBeforeNavigate.ts | 402 | StRS-MDOKFSTUDIO-FMEDIT-008 | SwRS duplicate | marker removed | - |
| test/integration/realInput/frontmatterFields.ts | 142 | StRS-MDOKFSTUDIO-FMEDIT-001 | partial path | marker removed | - |
| test/integration/realInput/frontmatterFields.ts | 417 | StRS-MDOKFSTUDIO-FMEDIT-005 | partial path | marker removed | - |
| test/integration/realInput/frontmatterFields.ts | 504 | StRS-MDOKFSTUDIO-FMEDIT-005 | real VS Code path | @accepts_req #S2 | 505 |
| test/integration/realInput/labelRenameAboveTable.ts | 43 | StRS-MDOKFSTUDIO-MYST-009 | partial path | marker removed | - |
| test/integration/realInput/previewWindow.ts | 200 | StRS-MDOKFSTUDIO-LIFE-001 | SwRS duplicate | marker removed | - |
| test/integration/realInput/previewWindow.ts | 216 | StRS-MDOKFSTUDIO-TOOLBAR-013 | single-state snapshot | marker removed | - |
| test/integration/realInput/previewWindow.ts | 355 | StRS-MDOKFSTUDIO-THEME-002 | partial path | marker removed | - |
| test/integration/realInput/previewWindow.ts | 381 | StRS-MDOKFSTUDIO-DIAG-001 | partial path | marker removed | - |
| test/integration/realInput/renderPatching.ts | 532 | StRS-MDOKFSTUDIO-BLOCK-011 | real VS Code path | @accepts_req #S1 | 533 |
| test/integration/realInput/tableEscape.ts | 42 | StRS-MDOKFSTUDIO-TABLE-001 | partial path | marker removed | - |
| test/integration/realInput/tableInsertSlash.ts | 41 | StRS-MDOKFSTUDIO-TABLE-016 | real VS Code path | @accepts_req #S1 | 41 |
| test/integration/realInput/textEditing.ts | 83 | StRS-MDOKFSTUDIO-FMEDIT-008 | partial path | marker removed | - |
| test/integration/realInput/textEditing.ts | 125 | StRS-MDOKFSTUDIO-FMEDIT-008 | partial path | marker removed | - |
| test/integration/realInput/textEditing.ts | 191 | StRS-MDOKFSTUDIO-FMEDIT-001 | partial path | marker removed | - |
| test/integration/realInput/textEditing.ts | 500 | StRS-MDOKFSTUDIO-PALETTE-015 | partial path | marker removed | - |
| test/integration/realInput/textEditing.ts | 621 | StRS-MDOKFSTUDIO-PALETTE-019 | partial path | marker removed | - |
| test/integration/realInput/textEditing.ts | 622 | StRS-MDOKFSTUDIO-PALETTE-005 | partial path | marker removed | - |
| test/integration/realInput/textEditing.ts | 742 | StRS-MDOKFSTUDIO-PALETTE-007 | other: link panel | marker removed | - |
| test/integration/realWindowGaps.ts | 100 | StRS-MDOKFSTUDIO-REVIEW-018 | real VS Code path | @accepts_req #S1 | 100 |
| test/integration/realWindowGaps.ts | 182 | StRS-MDOKFSTUDIO-REVIEW-017 | partial path | marker removed | - |
| test/integration/realWindowGaps.ts | 556 | StRS-MDOKFSTUDIO-PALETTE-018 | real VS Code path | @accepts_req #S1 | 561 |
| test/integration/realWindowGaps.ts | 668 | StRS-MDOKFSTUDIO-BLOCK-001 | partial path | marker removed | - |
| test/integration/realWindowGaps.ts | 669 | StRS-MDOKFSTUDIO-TRUST-001 | SwRS duplicate | marker removed | - |
| test/integration/reload-suite.ts | 112 | StRS-MDOKFSTUDIO-LIFE-014 | partial path | marker removed | - |
| test/integration/reload-suite.ts | 113 | StRS-MDOKFSTUDIO-THEME-011 | partial path | marker removed | - |
| test/integration/reviewComments.test.ts | 38 | StRS-MDOKFSTUDIO-REVIEW-001 | partial path | marker removed | - |
| test/integration/scroll-sync-suite.ts | 273 | StRS-MDOKFSTUDIO-LIFE-010 | real VS Code path | @accepts_req #S1 | 273 |
| test/integration/scroll-sync-suite.ts | 274 | StRS-MDOKFSTUDIO-TOOLBAR-013 | partial path | marker removed | - |
| test/integration/serializer.test.ts | 28 | StRS-MDOKFSTUDIO-LIFE-014 | partial path | marker removed | - |
| test/integration/serializer.test.ts | 29 | StRS-MDOKFSTUDIO-LIFE-001 | other: panel restore, no open command | marker removed | - |
| test/integration/serializer.test.ts | 30 | StRS-MDOKFSTUDIO-LIFE-007 | partial path | marker removed | - |
| test/integration/sourceMapping.test.ts | 29 | StRS-MDOKFSTUDIO-LIFE-010 | partial path | marker removed | - |
| test/integration/standalone-suite.ts | 39 | StRS-MDOKFSTUDIO-TRUST-001 | partial path | marker removed | - |
| test/integration/standalone-suite.ts | 40 | StRS-MDOKFSTUDIO-TRUST-004 | partial path | marker removed | - |
| test/integration/stockCoexistence.test.ts | 76 | StRS-MDOKFSTUDIO-LIFE-001 | real VS Code path | @accepts_req #S2 | 76 |
| test/integration/tableMoves.ts | 191 | StRS-MDOKFSTUDIO-TABLE-013 | partial path | marker removed | - |
| test/integration/tableMoves.ts | 255 | StRS-MDOKFSTUDIO-TABLE-002 | partial path | marker removed | - |
| test/integration/tableMoves.ts | 300 | StRS-MDOKFSTUDIO-TABLE-002 | real VS Code path | @accepts_req #S2 | 302 |
| test/integration/trusted-suite.ts | 128 | StRS-MDOKFSTUDIO-TRUST-006 | partial path | marker removed | - |
| test/integration/untrusted-suite.ts | 89 | StRS-MDOKFSTUDIO-TRUST-004 | partial path | marker removed | - |
| test/integration/untrusted-suite.ts | 154 | StRS-MDOKFSTUDIO-TRUST-001 | partial path | marker removed | - |
| test/integration/updateGlow.test.ts | 52 | StRS-MDOKFSTUDIO-LIFE-005 | partial path | marker removed | - |
| test/integration/workspaceDisposal.test.ts | 28 | StRS-MDOKFSTUDIO-LIFE-022 | partial path | marker removed | - |
| test/page/modules/alertLazyEditAction.test.ts | 32 | StRS-MDOKFSTUDIO-PALETTE-020 | partial path | marker removed | - |
| test/security/package-contract.test.ts | 20 | StRS-MDOKFSTUDIO-TRUST-012 | other: static manifest check outside VS Code | marker removed | - |
| test/security/package-contract.test.ts | 35 | StRS-MDOKFSTUDIO-LIFE-021 | other: static manifest check | marker removed | - |
| test/security/package-contract.test.ts | 385 | StRS-MDOKFSTUDIO-TRUST-014 | other: static packaging check outside VS Code | marker removed | - |
| test/security/userFacingText.test.ts | 131 | StRS-MDOKFSTUDIO-TRUST-012 | other: static source scan outside VS Code | marker removed | - |
| test/site/requirementsViewer/write.test.ts | 65 | StRS-MDOKFSTUDIO-CORE-008 | partial path | marker removed | - |
| test/visual/capture_layout_checks.py | 206 | StRS-MDOKFSTUDIO-TOOLBAR-002 | partial path | marker removed | - |
| test/visual/mathScenarios.ts | 22 | StRS-MDOKFSTUDIO-MYST-006 | partial path | marker removed | - |
| test/visual/releaseShowcaseScenarios.ts | 15 | StRS-MDOKFSTUDIO-CORE-001 | single-state snapshot | marker removed | - |
| test/visual/releaseShowcaseScenarios.ts | 16 | StRS-MDOKFSTUDIO-DIAG-015 | partial path | marker removed | - |
| test/visual/scenarioAssertions.ts | 673 | StRS-MDOKFSTUDIO-LAYOUT-004 | partial path | marker removed | - |
| test/visual/scenarioAssertions.ts | 720 | StRS-MDOKFSTUDIO-TOOLBAR-001 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 67 | StRS-MDOKFSTUDIO-CORE-001 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 109 | StRS-MDOKFSTUDIO-THEME-002 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 206 | StRS-MDOKFSTUDIO-LAYOUT-001 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 220 | StRS-MDOKFSTUDIO-MYST-015 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 274 | StRS-MDOKFSTUDIO-CORE-003 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 275 | StRS-MDOKFSTUDIO-MYST-005 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 337 | StRS-MDOKFSTUDIO-PALETTE-018 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 375 | StRS-MDOKFSTUDIO-DIAG-001 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 406 | StRS-MDOKFSTUDIO-DIAG-007 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 452 | StRS-MDOKFSTUDIO-CODE-004 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 638 | StRS-MDOKFSTUDIO-LAYOUT-003 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 675 | StRS-MDOKFSTUDIO-CODE-001 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 718 | StRS-MDOKFSTUDIO-CODE-001 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 785 | StRS-MDOKFSTUDIO-FMSCHEMA-001 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 786 | StRS-MDOKFSTUDIO-FMSCHEMA-006 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 825 | StRS-MDOKFSTUDIO-FMSCHEMA-014 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 965 | StRS-MDOKFSTUDIO-TABLE-008 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1233 | StRS-MDOKFSTUDIO-BLOCK-003 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1234 | StRS-MDOKFSTUDIO-LAYOUT-004 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1274 | StRS-MDOKFSTUDIO-BLOCK-011 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1301 | StRS-MDOKFSTUDIO-TOOLBAR-004 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1315 | StRS-MDOKFSTUDIO-TOOLBAR-013 | partial path | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1385 | StRS-MDOKFSTUDIO-MYST-005 | simulated path | @tests_req #S2 | 1375 |
| test/visual/scenarioDefinitions1.ts | 1402 | StRS-MDOKFSTUDIO-MYST-005 | simulated path | @tests_req #S2 | 1392 |
| test/visual/scenarioDefinitions2.ts | 251 | StRS-MDOKFSTUDIO-TOOLBAR-004 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 313 | StRS-MDOKFSTUDIO-FMSCHEMA-010 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 347 | StRS-MDOKFSTUDIO-FMSCHEMA-006 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 402 | StRS-MDOKFSTUDIO-FMSCHEMA-001 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 513 | StRS-MDOKFSTUDIO-LAYOUT-001 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 538 | StRS-MDOKFSTUDIO-CORE-001 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 550 | StRS-MDOKFSTUDIO-MYST-016 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 564 | StRS-MDOKFSTUDIO-FMSCHEMA-001 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 608 | StRS-MDOKFSTUDIO-TOOLBAR-006 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 608 | StRS-MDOKFSTUDIO-TOOLBAR-006 | simulated path | @tests_req #S2 | 605 |
| test/visual/scenarioDefinitions2.ts | 647 | StRS-MDOKFSTUDIO-REVIEW-012 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 698 | StRS-MDOKFSTUDIO-MYST-017 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 699 | StRS-MDOKFSTUDIO-MYST-009 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 728 | StRS-MDOKFSTUDIO-CORE-001 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 752 | StRS-MDOKFSTUDIO-CODE-001 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 787 | StRS-MDOKFSTUDIO-GFM-002 | simulated path | @tests_req #S1 | 780 |
| test/visual/scenarioDefinitions2.ts | 798 | StRS-MDOKFSTUDIO-MYST-018 | simulated path | @tests_req #S1 | 791 |
| test/visual/scenarioDefinitions2.ts | 822 | StRS-MDOKFSTUDIO-MYST-012 | simulated path | @tests_req #S1 | 813 |
| test/visual/scenarioDefinitions2.ts | 844 | StRS-MDOKFSTUDIO-DIAG-001 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 857 | StRS-MDOKFSTUDIO-DIAG-006 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 858 | StRS-MDOKFSTUDIO-DIAG-007 | other: built-in engine, not the own JAR | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 900 | StRS-MDOKFSTUDIO-DIAG-009 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 928 | StRS-MDOKFSTUDIO-FMSCHEMA-001 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 962 | StRS-MDOKFSTUDIO-THEME-002 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 975 | StRS-MDOKFSTUDIO-THEME-011 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 990 | StRS-MDOKFSTUDIO-THEME-004 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1048 | StRS-MDOKFSTUDIO-TOOLBAR-013 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1064 | StRS-MDOKFSTUDIO-TOOLBAR-004 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1078 | StRS-MDOKFSTUDIO-TOOLBAR-004 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1092 | StRS-MDOKFSTUDIO-TOOLBAR-004 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1107 | StRS-MDOKFSTUDIO-BLOCK-016 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1124 | StRS-MDOKFSTUDIO-PALETTE-015 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1138 | StRS-MDOKFSTUDIO-LAYOUT-003 | simulated path | @tests_req #S2 | 1128 |
| test/visual/scenarioDefinitions2.ts | 1153 | StRS-MDOKFSTUDIO-REVIEW-017 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1266 | StRS-MDOKFSTUDIO-MYST-007 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1330 | StRS-MDOKFSTUDIO-PALETTE-018 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1388 | StRS-MDOKFSTUDIO-TABLE-002 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1401 | StRS-MDOKFSTUDIO-TABLE-002 | partial path | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1424 | StRS-MDOKFSTUDIO-TABLE-002 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1442 | StRS-MDOKFSTUDIO-TABLE-002 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1456 | StRS-MDOKFSTUDIO-TABLE-002 | single-state snapshot | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1475 | StRS-MDOKFSTUDIO-TABLE-002 | single-state snapshot | marker removed | - |
| test/visual/slashAdmonitionScenarios.ts | 13 | StRS-MDOKFSTUDIO-PALETTE-021 | other: slash menu list only | marker removed | - |
| test/visual/svgPictureScenarios.ts | 40 | StRS-MDOKFSTUDIO-DIAG-015 | partial path | marker removed | - |
| test/visual/svgPictureScenarios.ts | 54 | StRS-MDOKFSTUDIO-DIAG-015 | partial path | marker removed | - |

Totals: 187 rows; removed 161 (partial path 111, single-state snapshot 27, SwRS duplicate 12, other 11), real VS Code path 19 (`@accepts_req`), simulated path 7 (`@tests_req`). MYST-016 and TOOLBAR-006 have one row per path.


## Declared scenarios and paths with no marker

Every declared scenario or path with no marker, per area as `<requirement number> <ids>` (`BLOCK: 001 S4` is scenario S4 of the BLOCK requirement 001 of that tier). In force and not exempt only.

**SwRS scenarios: 722 of 2633 with no marker**

- BLOCK (86): 001 S4,S6,S7,S8; 004 S4; 017 S3; 026 S1,S2,S3; 033 S6,S8,S11,S12; 041 S5; 053 S3; 058 S5,S7; 061 S4,S6,S7; 069 S2,S3,S4,S7; 079 S3,S8; 087 S1,S3,S6; 094 S6; 102 S4; 109 S1,S6,S10; 117 S1,S2; 127 S9; 130 S4; 140 S2,S3,S5,S6,S7; 148 S5; 156 S4,S6,S8; 166 S3,S5,S6; 169 S2; 174 S3,S6; 191 S1; 193 S1,S3,S5,S9,S10; 205 S4,S8; 216 S1,S2,S7; 228 S2,S3,S4,S7,S9; 254 S3; 255 S2; 259 S3,S8; 264 S1; 272 S2; 273 S2; 274 S2; 275 S2; 276 S2; 277 S2; 281 S1; 282 S1; 284 S2; 285 S1,S2; 286 S3
- CODE (18): 001 S6,S8,S9; 007 S1,S2; 008 S2,S5,S6; 014 S2,S4; 017 S4,S7; 019 S2,S4,S12,S13; 039 S6; 040 S2
- CORE (26): 003 S3,S4,S7; 008 S2,S3,S5; 012 S3,S5; 013 S1; 022 S6; 028 S1; 034 S3; 041 S3; 050 S1; 069 S2; 070 S1; 071 S3; 074 S2; 075 S2; 077 S3; 082 S2; 083 S2; 085 S4,S7; 088 S3; 093 S3
- DIAG (38): 001 S6; 005 S4,S5; 009 S5,S7; 015 S4; 017 S2; 023 S1,S2,S5; 024 S1,S2; 032 S1,S5,S6; 039 S1; 046 S2,S5; 053 S2,S4,S5; 054 S1,S3,S4,S6; 061 S1,S2; 068 S2,S4,S5; 084 S4,S5,S6; 089 S1,S6; 097 S7; 105 S5; 129 S3
- FMEDIT (34): 001 S1,S4; 003 S5,S6,S7,S8,S9; 004 S2,S3,S4,S6,S7; 010 S1,S4,S5,S6; 016 S2,S4,S7,S8,S10; 019 S10; 028 S4,S5; 029 S3,S5; 037 S5,S6,S8; 043 S4; 067 S2,S7,S8,S9
- FMSCHEMA (36): 001 S1; 004 S1,S2; 006 S3,S4; 014 S6,S7; 019 S1,S2; 023 S3,S4,S9; 027 S2,S4; 029 S5,S7; 039 S4; 043 S1,S2; 046 S5,S7; 050 S1,S5,S7,S8; 063 S4,S5,S8; 067 S5,S7; 073 S2,S3; 090 S2,S3,S4; 091 S2
- GFM (14): 001 S2,S5,S6; 008 S2,S5,S6; 016 S2,S4,S5,S6; 021 S3; 031 S2,S6; 034 S3
- LAYOUT (16): 001 S3; 002 S1; 007 S1,S3; 011 S3,S6,S8; 020 S3; 023 S2; 032 S2,S6; 043 S3; 044 S4,S5,S6,S7
- LIFE (67): 001 S3,S5; 002 S2; 003 S1,S5,S6,S12,S13,S14,S16; 018 S1,S2,S3,S6; 024 S4; 026 S2,S6,S9; 032 S4,S6; 038 S2,S4; 044 S5; 049 S2,S6,S8; 059 S1,S2,S3,S4; 062 S2,S3; 069 S1; 071 S2,S3,S4,S7; 094 S1,S6; 100 S1,S6; 108 S1,S4,S5,S7; 119 S2,S5,S6; 125 S1,S2; 127 S3,S6; 143 S4,S6; 149 S1,S4; 151 S3,S5; 156 S3,S4; 169 S7; 170 S1; 180 S1; 187 S2; 189 S2; 190 S1; 193 S2
- MYST (29): 001 S2,S7; 006 S1; 013 S5,S7; 017 S4; 031 S2,S4,S5,S6; 036 S3,S4; 038 S4,S9,S10; 045 S5,S6; 063 S1,S6,S7; 066 S6; 072 S2,S4; 078 S1,S2,S4; 081 S3,S5; 100 S4
- PALETTE (125): 001 S4,S5,S8; 003 S2; 017 S1,S3,S4,S5; 021 S7; 031 S2,S4; 036 S5; 039 S6; 043 S2,S3,S5; 050 S2,S3; 054 S1,S3,S5; 058 S6,S7; 069 S2,S5,S6; 072 S2,S4,S6; 078 S3,S4,S5,S6; 083 S2,S3,S5; 089 S2,S5; 092 S2,S4,S5; 109 S5; 114 S1,S3; 115 S2,S4; 125 S2; 127 S1,S2,S4,S5; 132 S2; 133 S1,S3,S4,S5; 136 S3; 140 S3; 147 S3; 148 S4; 149 S2,S3; 150 S3,S4,S6,S8; 153 S4,S6,S8,S9; 160 S1,S2,S3,S6; 178 S2,S5; 183 S1,S2,S6; 192 S4; 203 S1,S2; 213 S2,S4,S5; 217 S1,S2,S3,S4,S7; 229 S2,S3; 232 S2,S3,S4; 238 S2,S3,S6; 240 S2,S4; 242 S2,S3,S6,S7,S8; 252 S1,S2,S4; 256 S1,S2,S4; 263 S3,S4,S5; 264 S4; 266 S1,S2,S4; 270 S2; 276 S2,S3,S8,S9; 278 S4; 279 S2
- REVIEW (82): 001 S3,S5; 002 S1; 003 S2; 004 S5; 012 S2,S5,S6,S10,S11; 017 S8,S11; 021 S5,S6; 028 S3,S6; 038 S3,S5,S6; 044 S1,S2,S4,S5,S6,S8,S9,S13,S14,S15; 049 S2; 054 S7,S8,S10; 065 S1,S2,S3; 074 S8; 086 S4; 094 S7,S8; 100 S2; 107 S6,S7,S8; 119 S2,S6; 125 S1,S2,S5,S6; 133 S5; 139 S2,S3,S5; 143 S2,S3,S5,S7,S8; 152 S4,S10; 160 S1,S2,S3,S4,S5,S8; 167 S4; 171 S1,S6; 186 S2,S3,S4; 192 S2,S5; 195 S2,S8; 207 S3,S8; 214 S1,S5; 219 S2
- TABLE (69): 001 S2,S6,S7; 002 S9; 006 S2,S3; 007 S8,S9; 013 S1,S3,S4,S5,S7,S8; 018 S2,S6,S8; 025 S11,S15,S16; 034 S4; 048 S2,S3,S7; 055 S4,S5,S6,S12; 064 S6,S8; 085 S3,S7; 091 S1,S4; 094 S3,S5,S6,S7,S15; 106 S1,S2,S3,S5; 111 S1,S4,S6,S8; 115 S3,S4; 117 S1,S3,S4,S5,S8; 120 S5; 122 S2,S3,S5,S6,S7,S11,S16,S20,S21,S22,S24; 123 S5; 124 S3,S4
- THEME (18): 001 S5; 016 S4,S6,S9; 025 S7,S8; 031 S1,S2; 034 S2,S3,S4; 038 S1,S2,S5,S6,S7; 043 S3,S4
- TOOLBAR (44): 001 S2,S6,S7; 003 S3; 007 S4,S5; 010 S5; 018 S2,S7,S8; 025 S2,S3,S6,S8,S11; 030 S1,S3; 033 S4; 037 S2,S3,S5,S6; 040 S4,S8; 054 S1,S4,S6; 077 S6,S10; 079 S2,S8,S11; 085 S1; 094 S4; 098 S1,S3,S4,S5,S6; 117 S2; 120 S10,S11; 128 S5,S6
- TRUST (20): 001 S2; 005 S6; 007 S3,S4; 025 S2,S4; 036 S3,S5; 052 S1,S3,S5,S6; 065 S2,S4; 074 S3; 090 S8,S10; 092 S1,S2,S4

**StRS paths: 133 of 156 with no marker**

- BLOCK (15): 001 S1,S2; 003 S1; 006 S1; 008 S2; 011 S2,S3; 014 S1,S2,S3; 016 S1; 025 S1,S2; 027 S1,S2
- CODE (3): 001 S1,S2; 004 S1
- CORE (8): 001 S1,S2; 002 S1; 003 S1,S2; 006 S1; 007 S1; 008 S1
- DIAG (9): 001 S1,S2; 006 S1,S2; 007 S1; 009 S1,S2; 015 S1,S2
- FMEDIT (3): 001 S1; 005 S1; 008 S1
- FMSCHEMA (7): 001 S1,S2; 006 S1,S2; 010 S1; 014 S1,S2
- GFM (2): 002 S2; 003 S1
- LAYOUT (5): 001 S1,S2; 003 S1; 004 S1,S2
- LIFE (17): 001 S1; 003 S1,S2; 005 S1,S2; 007 S1,S2; 010 S2; 014 S1,S2; 021 S1; 022 S1,S2; 023 S1,S2,S3,S4
- MYST (11): 005 S1; 006 S1; 007 S1,S2; 009 S1,S2; 015 S1,S2; 016 S1; 017 S1,S2
- PALETTE (13): 002 S1; 005 S1,S2; 007 S1,S2; 013 S1,S2; 015 S1,S2; 018 S2; 019 S1; 020 S1; 021 S1
- REVIEW (9): 001 S1,S2; 003 S1,S2; 008 S2; 012 S1; 015 S1,S2; 017 S1
- TABLE (8): 001 S1,S2; 002 S1; 008 S1,S2; 013 S1,S2; 015 S1
- THEME (4): 002 S1,S2; 004 S1; 011 S1
- TOOLBAR (11): 001 S1; 002 S1; 004 S1,S2; 006 S1; 009 S1; 011 S1,S2; 013 S1,S2; 014 S1
- TRUST (8): 001 S1; 004 S1; 006 S1; 009 S1,S2; 012 S1,S2; 014 S1

## Changes

- `pyproject.toml`, `uv.lock`: `okf-schema>=0.18.1`.
- `requirements/config.yml`: `markers.accepts: '@accepts_req'` and the generated `accepted_in_files` field.
- `requirements/tiers/_schema/{base,strs,swrs}.schema.yaml`: `scenarios`, `acceptance_exemption`, `tested_in_files`, `accepted_in_files`.
- 97 retired SwRS files: `annotation_exemption` and its reason.
- `scripts/check-marker-companions.mjs`, `scripts/marker-baseline.json`: the rules above.
- `requirements/tiers/strs/`, `requirements/tiers/swrs/`: `scenarios:` blocks and `Path S<n>` / `Scenario S<n>` headings, new paths for BLOCK-027, TRUST-012 and TRUST-014, and `approved_at` and `verified.at` of the 15 approved StRS.
- Test markers under `test/`: one `#S<n>` line per scenario on `@tests_req SwRS-...`; StRS markers moved to `@accepts_req`, kept on a path, or removed. No file under `src/` changes.
- `scripts/mutation/report-pure.mjs`: reads markers with a `#S<n>` fragment.
- `test/site/requirementsViewer/mainPaths.ts`, `layout.ts`: path ids read from `Path S<n>` headings and shown in the path list; scenario ids on the dots.
- Test files split to stay under the file size limit, for example `previewStylesGutter.test.ts`, `editActionsColour.test.ts`, `runtimeTableCellEditorReveal.test.ts`, `previewEditingSchemaSteps.ts`, `capture_cell_editor_checks.py`, `capture_first_gap_checks.py` and `scenarioDefinitions3.ts`.
- `test/build/checkMarkers.test.ts`: eight new tests; `test/build/test_check_main_paths.py`: a `Path S1:` case.
- `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-097.md` (new) and its regenerated StRS and index; `requirements/tiers/log.md`.
- SwRS DIAG-009, DIAG-121, DIAG-123, LAYOUT-023, CORE-096 and the chart, gallery and Auto width tests of `main`: scenario ids and order, `tested_in_files` and marker fragments.
- `test/site/requirementsViewer/` (`model.ts`, `home.ts`, `pages.ts`, `viewer.css`, their tests and fixture); SwRS CORE-069, CORE-080, CORE-082.
- `justfile`: the trace JSON in the two report targets.
- `.agents/skills/okfreq/`, `.agents/skills/okfreq-gardening/`, `requirements/guidelines/requirements.guidelines.md`, `requirements/guidelines/project.guidelines.md`, `.agents/glossary/common.md`, `CONTRIBUTING.md`.

## Human decisions

- Paths of a StRS and scenarios of a SwRS share one `scenarios:` field with stable ids `S<n>`, never reused, and the fragment `#S<n>` on both markers.
- Acceptance tests use a distinct marker, `@accepts_req`.
- Bench convention: `@tests_req StRS-...#S<n>` is a path walked on the simulated bench (every pull request), `@accepts_req StRS-...#S<n>` a path walked in real VS Code (pushes to `main`).
- The viewer shows home cards for paths tested, paths accepted, StRS covered and scenarios tested, area columns for paths tested and accepted, each path of a use case page with its files and waiver, and each scenario of a behaviour page with its tests or "missing".
- Headings are renamed to `Path S<n>:` and `Scenario S<n>:`.
- The scripted rename of the 15 approved StRS headings is agreed.
- Every live StRS has a path; the TRUST-012 and TRUST-014 paths were asked to start from the built VSIX.
- StRS markers are sorted: `@tests_req` stays on a path an existing simulated test walks, `@accepts_req` on a path walked in real VS Code, and every other StRS marker goes (its SwRS markers stay). How strictly "walks" is read here is under Autonomous decisions and Known gaps.
- A SwRS never declares a scenario that is not tested: agreed as the target; 722 scenarios still have no marker, and closing that gap is deferred to the follow-up change.

## Impacts

No visual change in the extension: no file of `src/` changes behaviour or UI. Contributors see the new marker rules in `just check`. The generated requirements site (a contributor tool, not shipped) changes visibly: before, one card "StRS with a stakeholder validation test" and no path or scenario files; after, the four cards, two area columns and the per-path and per-scenario test lists described above.

"StRS covered", current coverage mode, live StRS:

| | `main` | this PR |
| --- | --- | --- |
| StRS covered | 23 / 95 | 1 / 95 |
| StRS with every linked SwRS `covered` | 24 | 24 |

The current mode asks for a direct `@tests_req` marker on the StRS and every linked SwRS `covered`. The marker sort moved the real VS Code walks to `@accepts_req`, which this mode does not count, and removed the markers of tests that do not walk a whole path: 6 StRS keep a direct `@tests_req` marker, 24 have every linked SwRS `covered`, and 1 has both. The exemption of the retired SwRS was expected to help this figure; it does not in this mode, which reports an exempt linked SwRS as `missing`. The follow-up change switches the mode, where `@accepts_req` counts and exempt SwRS are accepted. `just check` and `just requirements-lint` pass with this figure; only the requirements viewer reads it.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test/build/checkMarkers.test.ts` (the new marker rules), `test/build/mutationReport.test.ts`, and in `test/site/requirementsViewer/` `model.test.ts`, `home.test.ts`, `pages.test.ts`, `write.test.ts` and `mainPaths.test.ts`
- [ ] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
  - `SwRS-MDOKFSTUDIO-CORE-069`, `CORE-080`, `CORE-082` (viewer: `test/site/requirementsViewer/model.ts`, `home.ts`, `pages.ts`; tests `model.test.ts`, `home.test.ts`, `pages.test.ts`, `write.test.ts`)
  - `SwRS-MDOKFSTUDIO-CORE-097` (marker check: `scripts/check-marker-companions.mjs`; test `test/build/checkMarkers.test.ts`)
  - `SwRS-MDOKFSTUDIO-DIAG-009`, `DIAG-121`, `DIAG-123`, `LAYOUT-023`, `CORE-096` (from `main`: scenario ids, scenario order and test markers only)
- [ ] Changelog: no user-facing change
- [x] Local gates: `just check`, `just requirements-lint` and `just preflight` (static stage on Windows) pass at `2f3c629`
- [ ] Evidence: no visual change in the extension; the requirements site is checked by its unit tests, and the verification compared it before and after in a browser at `2f3c629` (screenshots not posted)
- [x] Review: approved at `2f3c629`
- [ ] Verified: pending at `2f3c629`
- [x] CI green: all checks that run on a pull request pass at `2f3c629`

## Internal references

- CR-504 strs-path-validation (batch-09), `work/coder/r1.md` to `r9.md`, `evidence/`.
- The follow-up change is CR-505; it takes the Known gaps carried into the follow-up change, the list of scenarios and paths with no marker, and the coverage-mode switch.

</details>


🤖 Generated with [Claude Code](https://claude.com/claude-code)
