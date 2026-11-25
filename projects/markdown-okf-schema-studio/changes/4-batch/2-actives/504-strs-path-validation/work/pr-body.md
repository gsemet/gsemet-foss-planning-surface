## Summary

The requirements bundle moves to okf-schema 0.18.1, which lets a requirement declare the paths or scenarios a test must name (`#S<n>`) and adds the `@accepts_req` marker for acceptance tests. This PR keeps the current StRS coverage mode and prepares the declarations: the bundle schemas and configuration, the exemption of retired requirements, and a marker check that understands the new marker and the `#S<n>` fragments.

Every requirement group now declares its scenarios (SwRS) and paths (StRS) with stable ids `S<n>`, and every test marker on a declaring requirement names its fragment. The requirements viewer shows, per path and per scenario, the test files that test or accept it, with new cards and columns. The coverage mode is not switched here.

One consequence to know before merging: in the current coverage mode the report's "StRS covered" figure goes from 23 of 95 on `main` to 0 of 95 until the follow-up change switches the mode (see Impacts).

## Deliverables

The marker check gains seven rules (the seventh, `implements-fragment`, rejects a `#S<n>` on `@implements_req`) and a baseline for StRS markers still in integration tests:

| Rule | What it rejects |
| --- | --- |
| `fragment-undeclared` | a `#S<n>` the target does not declare |
| `fragment-required` | a fragmentless marker on a target that declares `scenarios:` |
| `fragment-unexpected` | a fragment on a target with no `scenarios:` |
| `accepts-on-swrs` | `@accepts_req` on a SwRS |
| `accepts-placement` | `@accepts_req` outside the files the config allows |
| `implements-fragment` | a `#S<n>` fragment on `@implements_req` |
| `strs-tests-in-integration` | a new `@tests_req StRS-...` in `test/integration` (the baseline is now empty) |

Choices made:

- The coverage mode is not switched here; the old mode keeps working with the new schemas.
- The 97 retired SwRS get an explicit exemption so they declare no scenarios.
- A new SwRS (`SwRS-MDOKFSTUDIO-CORE-096`) states the behaviour of the marker check, each rule tested by its own test; a seventh rule, `implements-fragment`, rejects a `#S<n>` on `@implements_req`.
- All 16 requirement groups declare `scenarios:` and carry `Scenario S<n>` / `Path S<n>` headings; each SwRS test marker is one line per scenario.
- StRS markers in tests were sorted (table in Details): 61 became `@accepts_req` (walks in real VS Code, and the walks of CORE-007, CORE-008 and TRUST-014 outside it), 2 simulated paths, 122 removed because a SwRS marker already covers them.
- The mutation report reads the `#S<n>` fragments.
- The requirements viewer reads `scenarios:` from the requirement files and joins them with the okfreq trace: home cards "StRS paths tested", "StRS paths accepted", "StRS covered" and "SwRS scenarios tested" (the "StRS with a stakeholder validation test" card is removed), area columns "Paths tested" and "Paths accepted", the tested and accepted files of each path on a use case page, and the tests of each scenario, or "missing", on a behaviour page. Without a trace the declared counts stay and the file figures read "n/a". SwRS CORE-069, CORE-080 and CORE-082 gain the scenarios for this.
- `just requirements-report` and `just requirements-report-json` also write `out/reports/requirements/requirements-trace.json`.
- The vendored okfreq and okfreq-gardening skills and `requirements/guidelines/requirements.guidelines.md` are refreshed from okf-schema 0.18.1; the Studio's bench convention is in a new "Benches" section of the project guidelines and in CONTRIBUTING; the glossary gains "acceptance test", "accepted", "path (StRS)", "scenario (SwRS)" and "waiver".
- The second path of StRS TRUST-014 (diagram checks) was removed: CORE-087 and CORE-090 are build-time checks no path cites.

### Approved requirements changed

The 15 approved StRS only get `approved_at` set to the time of the scripted rename (plus `scenarios:` and path headings for some); no normative text changed. Owner review of this PR is their re-approval: BLOCK-003, BLOCK-011, BLOCK-025, DIAG-001, DIAG-006, GFM-002, LAYOUT-001, LAYOUT-003, PALETTE-015, CORE-001, REVIEW-001, REVIEW-003, REVIEW-012, REVIEW-015, TABLE-001.

### Validation in the new coverage mode (scratch, not applied)

A scratch copy of the bundle and of the sources, with the mode set to `linked-swrs-and-acceptance-paths`, validates with 0 errors and 64 warnings: W004 x38 (a StRS with no `@accepts_req` yet) and W2 x26 (placeholder cross-links that existed before). The mode switch and the W004 are for the follow-up change.

## Blast radius

Grade: **2**. The check script, the bundle schemas and the Python lock change; a `git revert` restores the previous state, but the new schemas and the exemptions must go back together.

## Autonomous decisions

- A migration script, run group by group, declared `scenarios:` and renamed the headings; each group commit carries its markers' fragments.
- The first fragment sweep was a keyword heuristic; its 486 weak entries were then read one by one (142 kept, 206 moved to the scenario really exercised, 136 dropped because the test checks no declared scenario). Fragments scored good, and 45 lines on 6 SwRS with generic scenarios, were not re-read.
- StRS markers in tests were sorted: kept as `@tests_req` or `@accepts_req` on a declared path, or removed when a SwRS marker already covers them; `strsTestsInIntegration` is now empty.
- Exemption reasons of the retired SwRS reuse one text per kind of retirement; LIFE-174, 182-185 have their own.
- The viewer's new behaviour is stated as new scenarios of three existing `proposed` SwRS (CORE-069, CORE-080, CORE-082), with no new SwRS.
- `requirements/guidelines/okfreq-baseline.guidelines.md` is left as it is: it matches no okf-schema file.
- The project guidelines state their own SwRS scenario heading, with the kind, which overrides the refreshed shared guideline.
- Two deliveries, decided during preparation: this PR declares the paths and scenarios in the current coverage mode; the mode switch is deferred to a follow-up change.
- No simulated walk is written for every StRS path: the viewer shows what the marker sort finds and says so. The release, site and package StRS (CORE-007, CORE-008, TRUST-014) may be accepted outside VS Code; CORE-006 stays in VS Code.

## Known gaps

Left for the follow-up change:

- 722 of 2622 in-force SwRS scenarios have no scenario marker.
- 94 of 156 StRS paths have no marker (counts per group in Details).
- 38 StRS have no acceptance test (W004, markers scanned).

Others:

- "StRS covered" reads 0 of 95 in the current coverage mode (see Impacts).
- `StRS-MDOKFSTUDIO-LIFE-023` shows its four paths with no tested or accepted file: no test marker names it.
- Fragments scored good in the first pass of the sweep were not re-read.
- The new viewer cards and pages are checked by unit tests only; the site was not looked at in a browser.

<details>
<summary>Details</summary>

## StRS marker classification

Every StRS marker (file, line, StRS, class, outcome), before and after the sort:

| File | Line before | StRS | Class | Outcome | Line now |
|---|---|---|---|---|---|
| test/build/test_plugin_manifests.py | 93 | StRS-MDOKFSTUDIO-CORE-006 | removed | marker removed | - |
| test/build/test_release.py | 322 | StRS-MDOKFSTUDIO-CORE-007 | product path outside VS Code | @accepts_req #S1 | 328 |
| test/core/frontmatter/diagReq.frontmatter.requirements.test.ts | 54 | StRS-MDOKFSTUDIO-FMSCHEMA-001 | removed | marker removed | - |
| test/core/render/writingSkill.test.ts | 134 | StRS-MDOKFSTUDIO-CORE-006 | removed | marker removed | - |
| test/integration/blockClipboard.test.ts | 82 | StRS-MDOKFSTUDIO-BLOCK-025 | real VS Code path | @accepts_req #S2 | 82 |
| test/integration/blockClipboard.test.ts | 83 | StRS-MDOKFSTUDIO-BLOCK-016 | real VS Code path | @accepts_req #S1 | 83 |
| test/integration/blockMove.test.ts | 36 | StRS-MDOKFSTUDIO-BLOCK-025 | removed | marker removed | - |
| test/integration/blockMove.test.ts | 37 | StRS-MDOKFSTUDIO-BLOCK-014 | removed | marker removed | - |
| test/integration/blockMove.test.ts | 78 | StRS-MDOKFSTUDIO-TRUST-009 | removed | marker removed | - |
| test/integration/checkboxToggle.test.ts | 66 | StRS-MDOKFSTUDIO-GFM-003 | real VS Code path | @accepts_req #S1 | 66 |
| test/integration/commentAnchors.test.ts | 32 | StRS-MDOKFSTUDIO-REVIEW-008 | real VS Code path | @accepts_req #S1 | 32 |
| test/integration/commentAnchors.test.ts | 33 | StRS-MDOKFSTUDIO-REVIEW-001 | removed | marker removed | - |
| test/integration/commentWrite.test.ts | 37 | StRS-MDOKFSTUDIO-REVIEW-001 | removed | marker removed | - |
| test/integration/commentWrite.test.ts | 38 | StRS-MDOKFSTUDIO-REVIEW-003 | real VS Code path | @accepts_req #S1 | 37 |
| test/integration/commentWrite.test.ts | 121 | StRS-MDOKFSTUDIO-TRUST-009 | removed | marker removed | - |
| test/integration/commentWrite.test.ts | 222 | StRS-MDOKFSTUDIO-TRUST-001 | real VS Code path | @accepts_req #S1 | 225 |
| test/integration/dirtySnapshots.test.ts | 67 | StRS-MDOKFSTUDIO-LIFE-005 | real VS Code path | @accepts_req #S1 | 67 |
| test/integration/editKeys.test.ts | 38 | StRS-MDOKFSTUDIO-BLOCK-008 | removed | marker removed | - |
| test/integration/editToolbarCover.test.ts | 86 | StRS-MDOKFSTUDIO-PALETTE-005 | removed | marker removed | - |
| test/integration/exportHtml.test.ts | 51 | StRS-MDOKFSTUDIO-TOOLBAR-014 | real VS Code path | @accepts_req #S1 | 51 |
| test/integration/findInPreview.test.ts | 72 | StRS-MDOKFSTUDIO-TOOLBAR-003 | real VS Code path | @accepts_req #S1 | 72 |
| test/integration/imagePaste.test.ts | 26 | StRS-MDOKFSTUDIO-PALETTE-018 | real VS Code path | @accepts_req #S1 | 26 |
| test/integration/imagePicker.test.ts | 26 | StRS-MDOKFSTUDIO-PALETTE-007 | real VS Code path | @accepts_req #S1 | 26 |
| test/integration/inlineThread.test.ts | 100 | StRS-MDOKFSTUDIO-REVIEW-015 | real VS Code path | @accepts_req #S1 | 100 |
| test/integration/labelRename.test.ts | 35 | StRS-MDOKFSTUDIO-MYST-009 | removed | marker removed | - |
| test/integration/lifecycle.test.ts | 43 | StRS-MDOKFSTUDIO-LIFE-001 | real VS Code path | @accepts_req #S1 | 43 |
| test/integration/lifecycle.test.ts | 44 | StRS-MDOKFSTUDIO-LIFE-003 | real VS Code path | @accepts_req #S1 | 44 |
| test/integration/lifecycle.test.ts | 45 | StRS-MDOKFSTUDIO-LIFE-007 | removed | marker removed | - |
| test/integration/lifecycle.test.ts | 145 | StRS-MDOKFSTUDIO-THEME-004 | removed | marker removed | - |
| test/integration/mystBlocksWindow.ts | 150 | StRS-MDOKFSTUDIO-MYST-016 | real VS Code path | @accepts_req #S1 | 150 |
| test/integration/mystDiagnostics.test.ts | 47 | StRS-MDOKFSTUDIO-MYST-007 | real VS Code path | @accepts_req #S1 | 47 |
| test/integration/mystPickers.test.ts | 8 | StRS-MDOKFSTUDIO-PALETTE-013 | removed | marker removed | - |
| test/integration/paletteMode.test.ts | 39 | StRS-MDOKFSTUDIO-PALETTE-002 | real VS Code path | @accepts_req #S1 | 39 |
| test/integration/previewEditing.test.ts | 45 | StRS-MDOKFSTUDIO-FMSCHEMA-001 | removed | marker removed | - |
| test/integration/previewEditing.test.ts | 141 | StRS-MDOKFSTUDIO-FMSCHEMA-014 | real VS Code path | @accepts_req #S1 | 123 |
| test/integration/previewEditing.test.ts | 638 | StRS-MDOKFSTUDIO-BLOCK-003 | real VS Code path | @accepts_req #S1 | 623 |
| test/integration/previewEditing.test.ts | 1042 | StRS-MDOKFSTUDIO-FMSCHEMA-010 | removed | marker removed | - |
| test/integration/previewEditing.test.ts | 1123 | StRS-MDOKFSTUDIO-FMSCHEMA-006 | removed | marker removed | - |
| test/integration/previewHistory.test.ts | 41 | StRS-MDOKFSTUDIO-TOOLBAR-009 | real VS Code path | @accepts_req #S1 | 41 |
| test/integration/previewHistory.test.ts | 42 | StRS-MDOKFSTUDIO-TOOLBAR-011 | real VS Code path | @accepts_req #S1 | 42 |
| test/integration/projectFeatures.test.ts | 138 | StRS-MDOKFSTUDIO-CORE-002 | real VS Code path | @accepts_req #S1 | 136 |
| test/integration/projectFeatures.test.ts | 153 | StRS-MDOKFSTUDIO-CORE-002 | removed | marker removed | - |
| test/integration/radioChoice.test.ts | 187 | StRS-MDOKFSTUDIO-GFM-005 | real VS Code path | @accepts_req #S1 | 187 |
| test/integration/realInput/blockKeys.ts | 139 | StRS-MDOKFSTUDIO-REVIEW-012 | real VS Code path | @accepts_req #S2 | 225 |
| test/integration/realInput/blockKeys.ts | 225 | StRS-MDOKFSTUDIO-REVIEW-012 | removed | marker removed | - |
| test/integration/realInput/blockKeys.ts | 280 | StRS-MDOKFSTUDIO-BLOCK-014 | real VS Code path | @accepts_req #S2 | 280 |
| test/integration/realInput/blockKeys.ts | 346 | StRS-MDOKFSTUDIO-BLOCK-016 | real VS Code path | @accepts_req #S1 | 347 |
| test/integration/realInput/blockKeys.ts | 549 | StRS-MDOKFSTUDIO-BLOCK-008 | real VS Code path | @accepts_req #S2 | 552 |
| test/integration/realInput/blockKeys.ts | 606 | StRS-MDOKFSTUDIO-TABLE-015 | real VS Code path | @accepts_req #S1 | 610 |
| test/integration/realInput/blockKeys.ts | 640 | StRS-MDOKFSTUDIO-TABLE-014 | real VS Code path | @accepts_req #S1 | 645 |
| test/integration/realInput/editorWidgets.ts | 385 | StRS-MDOKFSTUDIO-BLOCK-008 | real VS Code path | @accepts_req #S1 | 386 |
| test/integration/realInput/editorWidgets.ts | 427 | StRS-MDOKFSTUDIO-TABLE-001 | real VS Code path | @accepts_req #S1 | 429 |
| test/integration/realInput/editorWidgets.ts | 683 | StRS-MDOKFSTUDIO-BLOCK-003 | removed | marker removed | - |
| test/integration/realInput/editorWidgets.ts | 723 | StRS-MDOKFSTUDIO-BLOCK-003 | removed | marker removed | - |
| test/integration/realInput/editorWidgets.ts | 770 | StRS-MDOKFSTUDIO-BLOCK-001 | real VS Code path | @accepts_req #S1 | 771 |
| test/integration/realInput/editorWidgets.ts | 850 | StRS-MDOKFSTUDIO-TABLE-006 | real VS Code path | @accepts_req #S1 | 852 |
| test/integration/realInput/editorWidgets.ts | 931 | StRS-MDOKFSTUDIO-TABLE-008 | real VS Code path | @accepts_req #S1 | 935 |
| test/integration/realInput/flushBeforeNavigate.ts | 236 | StRS-MDOKFSTUDIO-BLOCK-006 | real VS Code path | @accepts_req #S2 | 236 |
| test/integration/realInput/flushBeforeNavigate.ts | 259 | StRS-MDOKFSTUDIO-BLOCK-006 | removed | marker removed | - |
| test/integration/realInput/flushBeforeNavigate.ts | 283 | StRS-MDOKFSTUDIO-BLOCK-006 | removed | marker removed | - |
| test/integration/realInput/flushBeforeNavigate.ts | 309 | StRS-MDOKFSTUDIO-TABLE-001 | removed | marker removed | - |
| test/integration/realInput/flushBeforeNavigate.ts | 402 | StRS-MDOKFSTUDIO-FMEDIT-008 | removed | marker removed | - |
| test/integration/realInput/frontmatterFields.ts | 142 | StRS-MDOKFSTUDIO-FMEDIT-001 | removed | marker removed | - |
| test/integration/realInput/frontmatterFields.ts | 417 | StRS-MDOKFSTUDIO-FMEDIT-005 | real VS Code path | @accepts_req #S2 | 417 |
| test/integration/realInput/frontmatterFields.ts | 504 | StRS-MDOKFSTUDIO-FMEDIT-005 | removed | marker removed | - |
| test/integration/realInput/labelRenameAboveTable.ts | 43 | StRS-MDOKFSTUDIO-MYST-009 | real VS Code path | @accepts_req #S2 | 43 |
| test/integration/realInput/previewWindow.ts | 200 | StRS-MDOKFSTUDIO-LIFE-001 | removed | marker removed | - |
| test/integration/realInput/previewWindow.ts | 216 | StRS-MDOKFSTUDIO-TOOLBAR-013 | removed | marker removed | - |
| test/integration/realInput/previewWindow.ts | 355 | StRS-MDOKFSTUDIO-THEME-002 | removed | marker removed | - |
| test/integration/realInput/previewWindow.ts | 381 | StRS-MDOKFSTUDIO-DIAG-001 | removed | marker removed | - |
| test/integration/realInput/renderPatching.ts | 532 | StRS-MDOKFSTUDIO-BLOCK-011 | real VS Code path | @accepts_req #S1 | 533 |
| test/integration/realInput/tableEscape.ts | 42 | StRS-MDOKFSTUDIO-TABLE-001 | removed | marker removed | - |
| test/integration/realInput/tableInsertSlash.ts | 41 | StRS-MDOKFSTUDIO-TABLE-016 | real VS Code path | @accepts_req #S1 | 41 |
| test/integration/realInput/textEditing.ts | 83 | StRS-MDOKFSTUDIO-FMEDIT-008 | real VS Code path | @accepts_req #S1 | 83 |
| test/integration/realInput/textEditing.ts | 125 | StRS-MDOKFSTUDIO-FMEDIT-008 | removed | marker removed | - |
| test/integration/realInput/textEditing.ts | 191 | StRS-MDOKFSTUDIO-FMEDIT-001 | real VS Code path | @accepts_req #S1 | 190 |
| test/integration/realInput/textEditing.ts | 500 | StRS-MDOKFSTUDIO-PALETTE-015 | real VS Code path | @accepts_req #S1 | 499 |
| test/integration/realInput/textEditing.ts | 621 | StRS-MDOKFSTUDIO-PALETTE-019 | real VS Code path | @accepts_req #S1 | 622 |
| test/integration/realInput/textEditing.ts | 622 | StRS-MDOKFSTUDIO-PALETTE-005 | real VS Code path | @accepts_req #S1 | 623 |
| test/integration/realInput/textEditing.ts | 742 | StRS-MDOKFSTUDIO-PALETTE-007 | removed | marker removed | - |
| test/integration/realWindowGaps.ts | 100 | StRS-MDOKFSTUDIO-REVIEW-018 | real VS Code path | @accepts_req #S1 | 100 |
| test/integration/realWindowGaps.ts | 182 | StRS-MDOKFSTUDIO-REVIEW-017 | real VS Code path | @accepts_req #S1 | 183 |
| test/integration/realWindowGaps.ts | 556 | StRS-MDOKFSTUDIO-PALETTE-018 | removed | marker removed | - |
| test/integration/realWindowGaps.ts | 668 | StRS-MDOKFSTUDIO-BLOCK-001 | removed | marker removed | - |
| test/integration/realWindowGaps.ts | 669 | StRS-MDOKFSTUDIO-TRUST-001 | removed | marker removed | - |
| test/integration/reload-suite.ts | 112 | StRS-MDOKFSTUDIO-LIFE-014 | real VS Code path | @accepts_req #S1 | 112 |
| test/integration/reload-suite.ts | 113 | StRS-MDOKFSTUDIO-THEME-011 | real VS Code path | @accepts_req #S1 | 113 |
| test/integration/reviewComments.test.ts | 38 | StRS-MDOKFSTUDIO-REVIEW-001 | real VS Code path | @accepts_req #S1 | 38 |
| test/integration/scroll-sync-suite.ts | 273 | StRS-MDOKFSTUDIO-LIFE-010 | real VS Code path | @accepts_req #S1 | 273 |
| test/integration/scroll-sync-suite.ts | 274 | StRS-MDOKFSTUDIO-TOOLBAR-013 | real VS Code path | @accepts_req #S1 | 274 |
| test/integration/serializer.test.ts | 28 | StRS-MDOKFSTUDIO-LIFE-014 | removed | marker removed | - |
| test/integration/serializer.test.ts | 29 | StRS-MDOKFSTUDIO-LIFE-001 | removed | marker removed | - |
| test/integration/serializer.test.ts | 30 | StRS-MDOKFSTUDIO-LIFE-007 | removed | marker removed | - |
| test/integration/sourceMapping.test.ts | 29 | StRS-MDOKFSTUDIO-LIFE-010 | removed | marker removed | - |
| test/integration/standalone-suite.ts | 39 | StRS-MDOKFSTUDIO-TRUST-001 | removed | marker removed | - |
| test/integration/standalone-suite.ts | 40 | StRS-MDOKFSTUDIO-TRUST-004 | removed | marker removed | - |
| test/integration/stockCoexistence.test.ts | 76 | StRS-MDOKFSTUDIO-LIFE-001 | removed | marker removed | - |
| test/integration/tableMoves.ts | 191 | StRS-MDOKFSTUDIO-TABLE-013 | real VS Code path | @accepts_req #S1 | 191 |
| test/integration/tableMoves.ts | 255 | StRS-MDOKFSTUDIO-TABLE-002 | real VS Code path | @accepts_req #S1 | 258 |
| test/integration/tableMoves.ts | 300 | StRS-MDOKFSTUDIO-TABLE-002 | real VS Code path | @accepts_req #S2 | 304 |
| test/integration/trusted-suite.ts | 128 | StRS-MDOKFSTUDIO-TRUST-006 | real VS Code path | @accepts_req #S1 | 128 |
| test/integration/untrusted-suite.ts | 89 | StRS-MDOKFSTUDIO-TRUST-004 | real VS Code path | @accepts_req #S1 | 89 |
| test/integration/untrusted-suite.ts | 154 | StRS-MDOKFSTUDIO-TRUST-001 | real VS Code path | @accepts_req #S1 | 155 |
| test/integration/updateGlow.test.ts | 52 | StRS-MDOKFSTUDIO-LIFE-005 | removed | marker removed | - |
| test/integration/workspaceDisposal.test.ts | 28 | StRS-MDOKFSTUDIO-LIFE-022 | real VS Code path | @accepts_req #S1 | 28 |
| test/page/modules/alertLazyEditAction.test.ts | 32 | StRS-MDOKFSTUDIO-PALETTE-020 | removed | marker removed | - |
| test/security/package-contract.test.ts | 20 | StRS-MDOKFSTUDIO-TRUST-012 | simulated path | @tests_req #S2 | 20 |
| test/security/package-contract.test.ts | 35 | StRS-MDOKFSTUDIO-LIFE-021 | removed | marker removed | - |
| test/security/package-contract.test.ts | 385 | StRS-MDOKFSTUDIO-TRUST-014 | product path outside VS Code | @accepts_req #S1 | 388 |
| test/security/userFacingText.test.ts | 131 | StRS-MDOKFSTUDIO-TRUST-012 | simulated path | @tests_req #S1 | 131 |
| test/site/requirementsViewer/write.test.ts | 65 | StRS-MDOKFSTUDIO-CORE-008 | product path outside VS Code | @accepts_req #S1 | 61 |
| test/visual/capture_layout_checks.py | 206 | StRS-MDOKFSTUDIO-TOOLBAR-002 | removed | marker removed | - |
| test/visual/mathScenarios.ts | 22 | StRS-MDOKFSTUDIO-MYST-006 | removed | marker removed | - |
| test/visual/releaseShowcaseScenarios.ts | 15 | StRS-MDOKFSTUDIO-CORE-001 | removed | marker removed | - |
| test/visual/releaseShowcaseScenarios.ts | 16 | StRS-MDOKFSTUDIO-DIAG-015 | removed | marker removed | - |
| test/visual/scenarioAssertions.ts | 673 | StRS-MDOKFSTUDIO-LAYOUT-004 | removed | marker removed | - |
| test/visual/scenarioAssertions.ts | 720 | StRS-MDOKFSTUDIO-TOOLBAR-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 67 | StRS-MDOKFSTUDIO-CORE-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 109 | StRS-MDOKFSTUDIO-THEME-002 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 206 | StRS-MDOKFSTUDIO-LAYOUT-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 220 | StRS-MDOKFSTUDIO-MYST-015 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 274 | StRS-MDOKFSTUDIO-CORE-003 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 275 | StRS-MDOKFSTUDIO-MYST-005 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 337 | StRS-MDOKFSTUDIO-PALETTE-018 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 375 | StRS-MDOKFSTUDIO-DIAG-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 406 | StRS-MDOKFSTUDIO-DIAG-007 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 452 | StRS-MDOKFSTUDIO-CODE-004 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 638 | StRS-MDOKFSTUDIO-LAYOUT-003 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 675 | StRS-MDOKFSTUDIO-CODE-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 718 | StRS-MDOKFSTUDIO-CODE-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 785 | StRS-MDOKFSTUDIO-FMSCHEMA-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 786 | StRS-MDOKFSTUDIO-FMSCHEMA-006 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 825 | StRS-MDOKFSTUDIO-FMSCHEMA-014 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 965 | StRS-MDOKFSTUDIO-TABLE-008 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1233 | StRS-MDOKFSTUDIO-BLOCK-003 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1234 | StRS-MDOKFSTUDIO-LAYOUT-004 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1274 | StRS-MDOKFSTUDIO-BLOCK-011 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1301 | StRS-MDOKFSTUDIO-TOOLBAR-004 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1315 | StRS-MDOKFSTUDIO-TOOLBAR-013 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1385 | StRS-MDOKFSTUDIO-MYST-005 | removed | marker removed | - |
| test/visual/scenarioDefinitions1.ts | 1402 | StRS-MDOKFSTUDIO-MYST-005 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 251 | StRS-MDOKFSTUDIO-TOOLBAR-004 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 313 | StRS-MDOKFSTUDIO-FMSCHEMA-010 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 347 | StRS-MDOKFSTUDIO-FMSCHEMA-006 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 402 | StRS-MDOKFSTUDIO-FMSCHEMA-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 513 | StRS-MDOKFSTUDIO-LAYOUT-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 538 | StRS-MDOKFSTUDIO-CORE-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 550 | StRS-MDOKFSTUDIO-MYST-016 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 564 | StRS-MDOKFSTUDIO-FMSCHEMA-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 608 | StRS-MDOKFSTUDIO-TOOLBAR-006 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 647 | StRS-MDOKFSTUDIO-REVIEW-012 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 698 | StRS-MDOKFSTUDIO-MYST-017 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 699 | StRS-MDOKFSTUDIO-MYST-009 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 728 | StRS-MDOKFSTUDIO-CORE-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 752 | StRS-MDOKFSTUDIO-CODE-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 787 | StRS-MDOKFSTUDIO-GFM-002 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 798 | StRS-MDOKFSTUDIO-MYST-018 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 822 | StRS-MDOKFSTUDIO-MYST-012 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 844 | StRS-MDOKFSTUDIO-DIAG-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 857 | StRS-MDOKFSTUDIO-DIAG-006 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 858 | StRS-MDOKFSTUDIO-DIAG-007 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 900 | StRS-MDOKFSTUDIO-DIAG-009 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 928 | StRS-MDOKFSTUDIO-FMSCHEMA-001 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 962 | StRS-MDOKFSTUDIO-THEME-002 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 975 | StRS-MDOKFSTUDIO-THEME-011 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 990 | StRS-MDOKFSTUDIO-THEME-004 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1048 | StRS-MDOKFSTUDIO-TOOLBAR-013 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1064 | StRS-MDOKFSTUDIO-TOOLBAR-004 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1078 | StRS-MDOKFSTUDIO-TOOLBAR-004 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1092 | StRS-MDOKFSTUDIO-TOOLBAR-004 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1107 | StRS-MDOKFSTUDIO-BLOCK-016 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1124 | StRS-MDOKFSTUDIO-PALETTE-015 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1138 | StRS-MDOKFSTUDIO-LAYOUT-003 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1153 | StRS-MDOKFSTUDIO-REVIEW-017 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1266 | StRS-MDOKFSTUDIO-MYST-007 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1330 | StRS-MDOKFSTUDIO-PALETTE-018 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1388 | StRS-MDOKFSTUDIO-TABLE-002 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1401 | StRS-MDOKFSTUDIO-TABLE-002 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1424 | StRS-MDOKFSTUDIO-TABLE-002 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1442 | StRS-MDOKFSTUDIO-TABLE-002 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1456 | StRS-MDOKFSTUDIO-TABLE-002 | removed | marker removed | - |
| test/visual/scenarioDefinitions2.ts | 1475 | StRS-MDOKFSTUDIO-TABLE-002 | removed | marker removed | - |
| test/visual/slashAdmonitionScenarios.ts | 13 | StRS-MDOKFSTUDIO-PALETTE-021 | removed | marker removed | - |
| test/visual/svgPictureScenarios.ts | 40 | StRS-MDOKFSTUDIO-DIAG-015 | removed | marker removed | - |
| test/visual/svgPictureScenarios.ts | 54 | StRS-MDOKFSTUDIO-DIAG-015 | removed | marker removed | - |

Totals: 185 markers; removed 122, accepted 61 (real VS Code, or the product path outside it), simulated path 2. Markers now with no pre-sort counterpart: 1.


## Declared scenarios with no marker

Uncovered SwRS scenarios by group: BLOCK 86, CODE 18, CORE 26, DIAG 38, FMEDIT 34, FMSCHEMA 36, GFM 14, LAYOUT 16, LIFE 67, MYST 29, PALETTE 125, REVIEW 82, TABLE 69, THEME 18, TOOLBAR 44, TRUST 20 (total 722).

Uncovered StRS paths by group: BLOCK 9, CODE 3, CORE 5, DIAG 9, FMEDIT 1, FMSCHEMA 6, GFM 2, LAYOUT 6, LIFE 13, MYST 11, PALETTE 8, REVIEW 5, TABLE 3, THEME 3, TOOLBAR 8, TRUST 2 (total 94).

The per-scenario list is not inlined (it is about 800 lines); the counts above are exact.

## Changes

- `pyproject.toml`, `uv.lock`: `okf-schema>=0.18.1`.
- `requirements/config.yml`: `markers.accepts: '@accepts_req'` and the generated `accepted_in_files` field.
- `requirements/tiers/_schema/{base,strs,swrs}.schema.yaml`: `scenarios`, `acceptance_exemption`, `tested_in_files`, `accepted_in_files`.
- 97 retired SwRS files: `annotation_exemption` and its reason.
- `scripts/check-marker-companions.mjs`, `scripts/marker-baseline.json`: the rules above.
- `test/build/checkMarkers.test.ts`: seven new tests; `test/build/test_check_main_paths.py`: a `Path S1:` case.
- `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-096.md` (new) and its regenerated StRS and index; `requirements/tiers/log.md`.
- `test/site/requirementsViewer/` (`model.ts`, `home.ts`, `pages.ts`, `viewer.css`, their tests and fixture); SwRS CORE-069, CORE-080, CORE-082.
- `justfile`: the trace JSON in the two report targets.
- `.agents/skills/okfreq/`, `.agents/skills/okfreq-gardening/`, `requirements/guidelines/requirements.guidelines.md`, `requirements/guidelines/project.guidelines.md`, `.agents/glossary/common.md`, `CONTRIBUTING.md`.

## Human decisions

- Paths of a StRS and scenarios of a SwRS share one `scenarios:` field with stable ids `S<n>`, never reused, and the fragment `#S<n>` on both markers.
- Acceptance tests use a distinct marker, `@accepts_req`.
- Bench convention: `@tests_req StRS-...#S<n>` is a path walked on the simulated bench (every pull request), `@accepts_req StRS-...#S<n>` a path walked in real VS Code (pushes to `main`).
- The viewer shows home cards for paths tested, paths accepted, StRS covered and scenarios tested, area columns for paths tested and accepted, each path of a use case page with its files and waiver, and each scenario of a behaviour page with its tests or "missing".
- Headings are renamed to `Path S<n>:` and `Scenario S<n>:`.
- The scripted rename of the 15 approved StRS headings is agreed; their re-approval is the owner's review of this PR.
- A SwRS never declares a scenario that is not tested: agreed as the target; 722 scenarios still have no marker, and closing that gap is deferred to the follow-up change.

## Impacts

No change in the extension. Contributors see the new marker rules in `just check` and the new cards, columns and pages in the generated requirements site.

"StRS covered", current coverage mode, live StRS:

| | `main` | this PR |
| --- | --- | --- |
| StRS covered | 23 / 95 | 0 / 95 |
| StRS with every linked SwRS `covered` | 24 | 24 |

The current mode asks for a direct `@tests_req` marker on the StRS and every linked SwRS `covered`. The marker sort moved the real VS Code walks to `@accepts_req`, which this mode does not count, so only TRUST-012 keeps a direct marker, and one of its linked SwRS is exempt, which this mode reports as `missing`. The specification expected the exemption of the retired SwRS to help this figure; it does not in this mode. The follow-up change switches the mode, where `@accepts_req` counts and exempt SwRS are accepted. `just check` and `just requirements-lint` pass with this figure; only the requirements viewer reads it.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test/build/checkMarkers.test.ts` (the new marker rules), `test/build/mutationReport.test.ts`, and in `test/site/requirementsViewer/` `model.test.ts`, `home.test.ts`, `pages.test.ts`, `write.test.ts` and `mainPaths.test.ts`
- [ ] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
  - `SwRS-MDOKFSTUDIO-CORE-069`, `CORE-080`, `CORE-082` (viewer: `test/site/requirementsViewer/model.ts`, `home.ts`, `pages.ts`; tests `model.test.ts`, `home.test.ts`, `pages.test.ts`, `write.test.ts`)
  - `SwRS-MDOKFSTUDIO-CORE-096` (marker check: `scripts/check-marker-companions.mjs`; test `test/build/checkMarkers.test.ts`)
- [ ] Changelog: no user-facing change
- [ ] Local gates: pending
- [ ] Evidence: none for a visible change
- [ ] Review: pending
- [ ] Verified: pending
- [ ] CI green: pending

## Internal references

- CR-504 strs-path-validation (batch-09), `work/coder/r1.md` to `r5.md`, `evidence/`.
- The follow-up change is CR-505; it takes the first three Known gaps and the coverage-mode switch.

</details>


🤖 Generated with [Claude Code](https://claude.com/claude-code)
