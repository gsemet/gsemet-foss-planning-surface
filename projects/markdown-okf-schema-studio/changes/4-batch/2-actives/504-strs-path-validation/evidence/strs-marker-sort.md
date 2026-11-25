# CR-504: StRS marker sort, all groups (file, line, StRS, class, outcome)

Every `@tests_req StRS-...` and `@accepts_req StRS-...` marker of `test/`, `src/`, `scripts/` and `sphinx/` at the start of the sort (commit e5ee7ec1, the bundle move), against the same files now. Markers of one file and one StRS are paired in order. `Line before` is the line at e5ee7ec1, `Line now` the line in the worktree (`-` when removed). Classes: `real VS Code path` = a path walked on the real VS Code bench, or a D7 StRS on its closest test, now `@accepts_req ...#S<n>`; `simulated path` = a path walked on the simulated bench, now `@tests_req StRS-...#S<n>`; `removed` = a snapshot, a partial path or a duplicate of a SwRS marker (its SwRS markers stay).

| File | Line before | StRS | Class | Outcome | Line now |
|---|---|---|---|---|---|
| test/build/test_plugin_manifests.py | 93 | StRS-MDOKFSTUDIO-CORE-006 | removed | marker removed | - |
| test/build/test_release.py | 322 | StRS-MDOKFSTUDIO-CORE-007 | real VS Code path | @accepts_req #S1 | 328 |
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
| test/security/package-contract.test.ts | 385 | StRS-MDOKFSTUDIO-TRUST-014 | real VS Code path | @accepts_req #S1 | 388 |
| test/security/userFacingText.test.ts | 131 | StRS-MDOKFSTUDIO-TRUST-012 | simulated path | @tests_req #S1 | 131 |
| test/site/requirementsViewer/write.test.ts | 65 | StRS-MDOKFSTUDIO-CORE-008 | real VS Code path | @accepts_req #S1 | 61 |
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

Totals: 185 markers; removed 122, real VS Code path 61, simulated path 2. Markers now with no pre-sort counterpart: 1.
