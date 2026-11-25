# CR-504 round 2, group 2a: StRS marker sort (file, StRS, outcome)

Rubric: experiments/02-audit-sample.md. accepts = a path walked in real VS Code (or a D7 StRS on its closest test); tests = a path on the simulated bench; removed = snapshot, partial path or duplicate of a SwRS marker (its SwRS markers stay).

| File | StRS marker | Outcome |
|---|---|---|
| test/core/frontmatter/diagReq.frontmatter.requirements.test.ts | StRS-MDOKFSTUDIO-FMSCHEMA-001 | removed |
| test/integration/blockMove.test.ts | StRS-MDOKFSTUDIO-TRUST-009 | removed |
| test/integration/checkboxToggle.test.ts | StRS-MDOKFSTUDIO-GFM-003 | accepts_req S1 |
| test/integration/commentWrite.test.ts | StRS-MDOKFSTUDIO-TRUST-009 | removed |
| test/integration/commentWrite.test.ts | StRS-MDOKFSTUDIO-TRUST-001 | accepts_req S1 |
| test/integration/labelRename.test.ts | StRS-MDOKFSTUDIO-MYST-009 | removed |
| test/integration/lifecycle.test.ts | StRS-MDOKFSTUDIO-THEME-004 | removed |
| test/integration/mystBlocksWindow.ts | StRS-MDOKFSTUDIO-MYST-016 | accepts_req S1, accepts_req S2 |
| test/integration/mystDiagnostics.test.ts | StRS-MDOKFSTUDIO-MYST-007 | accepts_req S1 |
| test/integration/previewEditing.test.ts | StRS-MDOKFSTUDIO-FMSCHEMA-001 | removed |
| test/integration/previewEditing.test.ts | StRS-MDOKFSTUDIO-FMSCHEMA-014 | accepts_req S1 |
| test/integration/previewEditing.test.ts | StRS-MDOKFSTUDIO-FMSCHEMA-010 | removed |
| test/integration/previewEditing.test.ts | StRS-MDOKFSTUDIO-FMSCHEMA-006 | removed |
| test/integration/radioChoice.test.ts | StRS-MDOKFSTUDIO-GFM-005 | accepts_req S1 |
| test/integration/realInput/flushBeforeNavigate.ts | StRS-MDOKFSTUDIO-FMEDIT-008 | removed |
| test/integration/realInput/frontmatterFields.ts | StRS-MDOKFSTUDIO-FMEDIT-001 | removed |
| test/integration/realInput/frontmatterFields.ts | StRS-MDOKFSTUDIO-FMEDIT-005 | accepts_req S2 |
| test/integration/realInput/labelRenameAboveTable.ts | StRS-MDOKFSTUDIO-MYST-009 | accepts_req S2 |
| test/integration/realInput/previewWindow.ts | StRS-MDOKFSTUDIO-THEME-002 | removed |
| test/integration/realInput/previewWindow.ts | StRS-MDOKFSTUDIO-DIAG-001 | removed |
| test/integration/realInput/textEditing.ts | StRS-MDOKFSTUDIO-FMEDIT-008 | accepts_req S1 |
| test/integration/realInput/textEditing.ts | StRS-MDOKFSTUDIO-FMEDIT-001 | accepts_req S1 |
| test/integration/realWindowGaps.ts | StRS-MDOKFSTUDIO-TRUST-001 | removed |
| test/integration/reload-suite.ts | StRS-MDOKFSTUDIO-THEME-011 | accepts_req S1 |
| test/integration/standalone-suite.ts | StRS-MDOKFSTUDIO-TRUST-001 | removed |
| test/integration/standalone-suite.ts | StRS-MDOKFSTUDIO-TRUST-004 | removed |
| test/integration/trusted-suite.ts | StRS-MDOKFSTUDIO-TRUST-006 | accepts_req S1 |
| test/integration/untrusted-suite.ts | StRS-MDOKFSTUDIO-TRUST-004 | accepts_req S1 |
| test/integration/untrusted-suite.ts | StRS-MDOKFSTUDIO-TRUST-001 | accepts_req S1 |
| test/security/package-contract.test.ts | StRS-MDOKFSTUDIO-TRUST-012 | tests_req S2 |
| test/security/package-contract.test.ts | StRS-MDOKFSTUDIO-TRUST-014 | accepts_req S1 |
| test/security/userFacingText.test.ts | StRS-MDOKFSTUDIO-TRUST-012 | tests_req S1 |
| test/visual/mathScenarios.ts | StRS-MDOKFSTUDIO-MYST-006 | removed |
| test/visual/releaseShowcaseScenarios.ts | StRS-MDOKFSTUDIO-DIAG-015 | removed |
| test/visual/scenarioAssertions.ts | StRS-MDOKFSTUDIO-LAYOUT-004 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-THEME-002 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-LAYOUT-001 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-MYST-015 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-MYST-005 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-DIAG-001 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-DIAG-007 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-CODE-004 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-LAYOUT-003 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-CODE-001 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-FMSCHEMA-001 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-FMSCHEMA-006 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-FMSCHEMA-014 | removed |
| test/visual/scenarioDefinitions1.ts | StRS-MDOKFSTUDIO-LAYOUT-004 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-FMSCHEMA-010 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-FMSCHEMA-006 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-FMSCHEMA-001 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-LAYOUT-001 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-MYST-016 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-MYST-017 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-MYST-009 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-CODE-001 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-GFM-002 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-MYST-018 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-MYST-012 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-DIAG-001 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-DIAG-006 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-DIAG-007 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-DIAG-009 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-THEME-002 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-THEME-011 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-THEME-004 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-LAYOUT-003 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-MYST-007 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-PALETTE-018 | removed |
| test/visual/scenarioDefinitions2.ts | StRS-MDOKFSTUDIO-TABLE-002 | removed |
| test/visual/svgPictureScenarios.ts | StRS-MDOKFSTUDIO-DIAG-015 | removed |
