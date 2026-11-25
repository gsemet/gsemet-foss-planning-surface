# CR-504 round 2, group 2a: sweep entries where the keyword match was weak (S1 or best guess; to review)

| File:line (before the sweep) | SwRS | Chosen | Score | Test title |
|---|---|---|---|---|
| test/core/directives/registry.test.ts:17 | SwRS-MDOKFSTUDIO-MYST-001 | S2,S5 | 1.0 | each directive name has one plug-in, found by its exact name |
| test/core/edits/radioSelect.test.ts:79 | SwRS-MDOKFSTUDIO-GFM-041 | S2 | 0.45 | a radio marker starts a list item and is followed by a space or a tab |
| test/core/edits/radioSelect.test.ts:119 | SwRS-MDOKFSTUDIO-GFM-041 | S1 | 0.5 | one group is accepted across nested lists, lazy lines, quotes and two-digit ordered markers |
| test/core/export/htmlExport.test.ts:312 | SwRS-MDOKFSTUDIO-FMSCHEMA-091 | S1 | 0.58 | the Description column stays and the editing data goes, whatever the toggle state of the page |
| test/core/frontmatter/fileLinks.holes.test.ts:58 | SwRS-MDOKFSTUDIO-FMSCHEMA-046 | S3,S6 | 0.88 | the project root is the Git root of the document, only when a navigation root holds it |
| test/core/frontmatter/fileLinks.holes.test.ts:75 | SwRS-MDOKFSTUDIO-FMSCHEMA-046 | S3,S6 | 0.88 | an absolute target is refused by its shape and a target that only contains a colon is not |
| test/core/frontmatter/fileLinks.holes.test.ts:92 | SwRS-MDOKFSTUDIO-FMSCHEMA-046 | S6 | 0.58 | a document-relative target is resolved from the real folder of the document and contained by the nav |
| test/core/frontmatter/fileLinks.holes.test.ts:124 | SwRS-MDOKFSTUDIO-FMSCHEMA-046 | S6 | 1.15 | bundle-relative and project-relative targets start from their own root, and bundle-relative-stem add |
| test/core/frontmatter/fileLinks.holes.test.ts:151 | SwRS-MDOKFSTUDIO-FMSCHEMA-046 | S6 | 0.88 | a missing root is reported by its kind, and a target leaving its root is refused before the disk is  |
| test/core/frontmatter/fileLinks.test.ts:91 | SwRS-MDOKFSTUDIO-FMSCHEMA-046 | S2,S4 | 0.71 | conditional, patternProperties, and additionalProperties schemas are traversed |
| test/core/frontmatter/linkFiles.memory.test.ts:107 | SwRS-MDOKFSTUDIO-FMSCHEMA-055 | S5 | 1.34 | an invalidation during a build discards that build |
| test/core/frontmatter/linkFiles.memory.test.ts:137 | SwRS-MDOKFSTUDIO-FMSCHEMA-063 | S1,S3 | 1.41 | a linked file with a BOM and a marker gives its details through the port |
| test/core/frontmatter/okfFrontmatter.test.ts:102 | SwRS-MDOKFSTUDIO-FMEDIT-043 | S1,S3 | 0.89 | frontmatter scalar and object edits preserve YAML node metadata |
| test/core/frontmatter/okfFrontmatter.test.ts:136 | SwRS-MDOKFSTUDIO-FMEDIT-043 | S1,S3 | 0.45 | frontmatter array edits keep comments attached to reordered items |
| test/core/frontmatter/schemaValidator.holes.test.ts:33 | SwRS-MDOKFSTUDIO-FMSCHEMA-084 | S5 | 0.71 | a branch validator is compiled once per branch and root, and released with its root |
| test/core/myst/confLocator.holes.test.ts:47 | SwRS-MDOKFSTUDIO-MYST-066 | S3,S4 | 0.89 | an answer is trusted for fewer than 2000 ms, and the disk is checked again at exactly 2000 ms |
| test/core/preview/contentPatch.test.ts:124 | SwRS-MDOKFSTUDIO-DIAG-001 | S2,S7 | 0.71 | T34: shell keys differ when Mermaid appears or disappears, and when math appears |
| test/core/preview/contentPatch.test.ts:140 | SwRS-MDOKFSTUDIO-DIAG-124 | S1 | 0.0 | CR 149: shell keys differ when a chart appears or disappears, and charts of two pages share a shell |
| test/core/protocol/pageStateMessages.test.ts:221 | SwRS-MDOKFSTUDIO-GFM-021 | S4,S5 | 0.58 | the page-state validators accept exactly what the frozen validator accepted |
| test/core/protocol/pageToHost.test.ts:29 | SwRS-MDOKFSTUDIO-TRUST-052 | S1,S5 | 1.0 | rejects non-objects, unregistered and prototype-key types |
| test/core/render/chartData.test.ts:16 | SwRS-MDOKFSTUDIO-DIAG-121 | S1 | 0.0 | parseChartSource reads a JSON or YAML object and gives the reason for anything else |
| test/core/render/chartData.test.ts:53 | SwRS-MDOKFSTUDIO-DIAG-122 | S1 | 0.0 | parseDelimited reads quoted fields, CRLF and a byte order mark, and types numbers and booleans |
| test/core/render/plantUmlRenderer.test.ts:222 | SwRS-MDOKFSTUDIO-DIAG-097 | S4,S8 | 0.8 | asks the runner to cap stderr at 64 KiB and notes the truncation it reports |
| test/core/render/plantUmlRenderer.test.ts:239 | SwRS-MDOKFSTUDIO-DIAG-097 | S4,S8 | 0.8 | a stderr within the cap carries no truncation note |
| test/core/state/boundedState.test.ts:30 | SwRS-MDOKFSTUDIO-FMSCHEMA-014 | S6 | 0.41 | evicts the least recently set entry once the cap is exceeded |
| test/core/state/editLock.test.ts:23 | SwRS-MDOKFSTUDIO-DIAG-105 | S6,S7 | 0.45 | reloads are deferred while held and flushed once on release |
| test/integration/blockClipboard.test.ts:87 | SwRS-MDOKFSTUDIO-TRUST-065 | S5 | 0.76 | run |
| test/integration/blockClipboard.test.ts:161 | SwRS-MDOKFSTUDIO-TRUST-005 | S1,S3 | 1.34 | runUntrusted |
| test/integration/blockMove.test.ts:222 | SwRS-MDOKFSTUDIO-TRUST-005 | S1,S3 | 1.0 | runUntrusted |
| test/integration/commentWrite.test.ts:224 | SwRS-MDOKFSTUDIO-TRUST-005 | S2 | 0.89 | runUntrusted |
| test/integration/exportHtml.test.ts:94 | SwRS-MDOKFSTUDIO-DIAG-128 | S1 | 0.0 |  |
| test/integration/genericMarkdown.test.ts:72 | SwRS-MDOKFSTUDIO-FMSCHEMA-005 | S1,S4 | 1.34 | run |
| test/integration/imagePaste.test.ts:29 | SwRS-MDOKFSTUDIO-TRUST-005 | S1,S5 | 1.34 | run |
| test/integration/inlineThread.test.ts:102 | SwRS-MDOKFSTUDIO-TRUST-090 | S4,S6 | 1.0 | run |
| test/integration/labelRename.test.ts:36 | SwRS-MDOKFSTUDIO-TRUST-065 | S5 | 0.76 | run |
| test/integration/mystBlocksWindow.ts:182 | SwRS-MDOKFSTUDIO-MYST-001 | S4,S5 | 0.71 |  |
| test/integration/mystPickers.test.ts:9 | SwRS-MDOKFSTUDIO-TRUST-090 | S9 | 0.89 | run |
| test/integration/previewEditing.test.ts:31 | SwRS-MDOKFSTUDIO-FMSCHEMA-001 | S1 | 0.0 | stepFrontmatterTable |
| test/integration/previewEditing.test.ts:52 | SwRS-MDOKFSTUDIO-FMSCHEMA-084 | S1 | 0.89 | stepLinkTooltips |
| test/integration/previewEditing.test.ts:127 | SwRS-MDOKFSTUDIO-FMSCHEMA-073 | S1,S2 | 1.0 | stepLinksOpen |
| test/integration/previewEditing.test.ts:334 | SwRS-MDOKFSTUDIO-FMEDIT-024 | S1,S3 | 0.82 | stepFrontmatterSaves |
| test/integration/projectFeatures.test.ts:47 | SwRS-MDOKFSTUDIO-DIAG-001 | S5,S7 | 1.0 | run |
| test/integration/realInput/previewWindow.ts:356 | SwRS-MDOKFSTUDIO-THEME-001 | S3,S4 | 0.5 |  |
| test/integration/realInput/previewWindow.ts:357 | SwRS-MDOKFSTUDIO-THEME-025 | S1,S2 | 0.58 |  |
| test/integration/standalone-suite.ts:41 | SwRS-MDOKFSTUDIO-TRUST-001 | S1 | 0.0 | run |
| test/integration/standalone-suite.ts:42 | SwRS-MDOKFSTUDIO-TRUST-005 | S1 | 0.0 | run |
| test/integration/standalone-suite.ts:43 | SwRS-MDOKFSTUDIO-TRUST-007 | S1 | 0.0 | run |
| test/integration/trusted-suite.ts:68 | SwRS-MDOKFSTUDIO-TRUST-012 | S1 | 0.0 | run |
| test/integration/trusted-suite.ts:130 | SwRS-MDOKFSTUDIO-TRUST-036 | S1,S5 | 1.34 | runHostilePreview |
| test/integration/untrusted-suite.ts:90 | SwRS-MDOKFSTUDIO-TRUST-025 | S5,S6 | 1.41 | runRestrictedImages |
| test/integration/untrusted-suite.ts:155 | SwRS-MDOKFSTUDIO-TRUST-005 | S1 | 0.0 | run |
| test/integration/untrusted-suite.ts:156 | SwRS-MDOKFSTUDIO-TRUST-001 | S5 | 0.41 | run |
| test/integration/untrusted-suite.ts:157 | SwRS-MDOKFSTUDIO-TRUST-005 | S1 | 0.0 | run |
| test/page/chartCsp.test.ts:15 | SwRS-MDOKFSTUDIO-DIAG-122 | S1 | 0.58 | a Vega-Lite and a Vega chart are drawn under the page's Content Security Policy, with no eval violat |
| test/page/geometryChecks.test.ts:92 | SwRS-MDOKFSTUDIO-LAYOUT-001 | S1 | 0.0 | geometry checks define one function that reports the four check ids |
| test/page/modules/chartError.test.ts:28 | SwRS-MDOKFSTUDIO-DIAG-123 | S1 | 0.5 | the reason is plain text, never HTML |
| test/page/modules/firstClearance.test.ts:241 | SwRS-MDOKFSTUDIO-LAYOUT-011 | S7 | 0.5 | a late load or font settlement measures again |
| test/page/modules/labelRename.test.ts:233 | SwRS-MDOKFSTUDIO-MYST-038 | S1,S3 | 0.58 | the preview toolbar band counts as the top obstruction |
| test/page/modules/mermaidError.test.ts:36 | SwRS-MDOKFSTUDIO-DIAG-015 | S1,S3 | 0.8 | K3: the parser message is plain text, never HTML, and the details start closed |
| test/page/modules/mermaidPreviewEntry.test.ts:54 | SwRS-MDOKFSTUDIO-DIAG-001 | S2 | 1.01 | Mermaid draws only once the page fonts are loaded |
| test/page/runtimeRadioGroups.test.ts:228 | SwRS-MDOKFSTUDIO-GFM-040 | S1,S3 | 0.89 | after a choice with Space or a click and the content patch that follows, the option of the same line |
| test/page/runtimeRadioGroups.test.ts:262 | SwRS-MDOKFSTUDIO-GFM-041 | S2,S3 | 0.3 | a content patch while no option has the focus (an external rewrite) gives the focus to no option |
| test/page/runtimeScroll.test.ts:359 | SwRS-MDOKFSTUDIO-THEME-001 | S1,S3 | 0.82 | cycles preview theme modes and restores the saved selection |
| test/security/html-policy.test.ts:25 | SwRS-MDOKFSTUDIO-TRUST-025 | S6 | 1.34 | rewrites local resources and removes active HTML content |
| test/security/package-contract.test.ts:195 | SwRS-MDOKFSTUDIO-CODE-039 | S1,S2 | 1.0 |  |
| test/security/package-contract.test.ts:304 | SwRS-MDOKFSTUDIO-DIAG-124 | S1 | 0.0 | CR 149: the chart runtime ships pinned in its own bundle and evaluates expressions with the interpre |
| test/security/package-contract.test.ts:386 | SwRS-MDOKFSTUDIO-TRUST-092 | S3 | 0.71 | CR 135: the VSIX leaves out source maps, internal docs, agent files and the Python project file |
| test/security/readOnlyRoot.requirements.test.ts:150 | SwRS-MDOKFSTUDIO-TRUST-002 | S4 | 0.71 | on Windows USERPROFILE wins over HOME, elsewhere HOME wins |
| test/security/resource-policy.test.ts:35 | SwRS-MDOKFSTUDIO-TRUST-025 | S3,S5 | 1.12 | canonicalizes local resources and rejects hostile paths |
| test/security/svgSanitizer.test.ts:37 | SwRS-MDOKFSTUDIO-DIAG-125 | S3 | 0.5 | removes event handler attributes |
| test/security/svgSanitizer.test.ts:45 | SwRS-MDOKFSTUDIO-DIAG-125 | S3 | 0.5 | removes foreignObject with the HTML inside it |
| test/security/svgSanitizer.test.ts:59 | SwRS-MDOKFSTUDIO-DIAG-125 | S3 | 0.8 | removes the style element and a style attribute that is not a presentation property |
| test/security/svgSanitizer.test.ts:80 | SwRS-MDOKFSTUDIO-DIAG-125 | S3 | 0.5 | removes javascript, data and external URLs from attribute values |
| test/security/svgSanitizer.test.ts:121 | SwRS-MDOKFSTUDIO-DIAG-125 | S3 | 0.8 | title and desc keep only text; an element inside them is dropped |
| test/security/svgSanitizer.test.ts:151 | SwRS-MDOKFSTUDIO-DIAG-125 | S3 | 0.8 | a value is an allow-list: no other function than colours, var, url(#id) and transforms, and no schem |
| test/security/svgSanitizer.test.ts:164 | SwRS-MDOKFSTUDIO-TRUST-036 | S5 | 1.45 | the value check of the final sanitizer accepts a presentation value and refuses a remote one |
| test/security/trustReq.requirements.test.ts:49 | SwRS-MDOKFSTUDIO-TRUST-012 | S2,S4 | 0.88 | fonts and media load only from the webview source |
| test/session/blockReq.requirements.test.ts:446 | SwRS-MDOKFSTUDIO-TRUST-001 | S1,S4 | 1.15 | a block save on a file VS Code holds read-only is told, and the images pasted meanwhile are removed |
| test/session/dropFiles.requirements.test.ts:141 | SwRS-MDOKFSTUDIO-TRUST-001 | S1 | 1.15 | a drop on a file VS Code holds read-only answers the read-only reason |
| test/session/dropFiles.requirements.test.ts:153 | SwRS-MDOKFSTUDIO-TRUST-005 | S2 | 0.89 | a drop on a standalone file links any file relative to the document, reading none |
| test/session/renderReq.labelRename.requirements.test.ts:65 | SwRS-MDOKFSTUDIO-TRUST-001 | S1,S4 | 1.15 | a rename on a file VS Code holds read-only answers the read-only reason |
| test/session/reviewReqThreads.requirements.test.ts:154 | SwRS-MDOKFSTUDIO-TRUST-001 | S1 | 1.15 | a reply, a delete and a find replace on a file VS Code holds read-only answer the read-only reason |
| test/visual/capture_layout_checks.py:763 | SwRS-MDOKFSTUDIO-LAYOUT-020 | S3 | 1.41 | check_width_modes |
| test/visual/cardsTabsScenarios.ts:61 | SwRS-MDOKFSTUDIO-MYST-001 | S2,S4 | 0.71 |  |
| test/visual/cardsTabsScenarios.ts:62 | SwRS-MDOKFSTUDIO-MYST-100 | S1 | 0.89 |  |
| test/visual/exportHtmlScenarios.ts:19 | SwRS-MDOKFSTUDIO-FMSCHEMA-091 | S1 | 1.15 |  |
| test/visual/frontmatterCollapseScenarios.ts:31 | SwRS-MDOKFSTUDIO-FMSCHEMA-090 | S1 | 1.41 |  |
| test/visual/frontmatterCollapseScenarios.ts:44 | SwRS-MDOKFSTUDIO-FMSCHEMA-090 | S1,S4 | 0.71 |  |
| test/visual/mathScenarios.ts:24 | SwRS-MDOKFSTUDIO-MYST-102 | S1 | 1.34 | myst/v47-maths-offline-light-900 |
| test/visual/radioPlanScenarios.ts:44 | SwRS-MDOKFSTUDIO-GFM-040 | S1 | 0.76 |  |
| test/visual/radioPlanScenarios.ts:56 | SwRS-MDOKFSTUDIO-GFM-041 | S1 | 1.0 |  |
| test/visual/scenarioAssertions.ts:125 | SwRS-MDOKFSTUDIO-LAYOUT-032 | S3,S4 | 0.71 |  |
| test/visual/scenarioAssertions.ts:736 | SwRS-MDOKFSTUDIO-LAYOUT-011 | S2,S3 | 1.0 |  |
| test/visual/scenarioDefinitions1.ts:207 | SwRS-MDOKFSTUDIO-LAYOUT-001 | S1 | 0.5 | handbook-narrow-table |
| test/visual/scenarioDefinitions1.ts:376 | SwRS-MDOKFSTUDIO-DIAG-005 | S1,S2 | 0.71 | mermaid-map-dark |
| test/visual/scenarioDefinitions1.ts:387 | SwRS-MDOKFSTUDIO-DIAG-001 | S1 | 0.0 | mermaid-map-light |
| test/visual/scenarioDefinitions1.ts:407 | SwRS-MDOKFSTUDIO-DIAG-105 | S5 | 0.89 | plantuml-success-light |
| test/visual/scenarioDefinitions1.ts:440 | SwRS-MDOKFSTUDIO-DIAG-089 | S5 | 0.88 | plantuml-executable-not-found |
| test/visual/scenarioDefinitions1.ts:453 | SwRS-MDOKFSTUDIO-CODE-017 | S2,S4 | 1.22 |  |
| test/visual/scenarioDefinitions1.ts:467 | SwRS-MDOKFSTUDIO-CODE-017 | S8,S9 | 1.15 |  |
| test/visual/scenarioDefinitions1.ts:676 | SwRS-MDOKFSTUDIO-CODE-001 | S1,S2 | 0.5 | syntax-dark-rust |
| test/visual/scenarioDefinitions1.ts:762 | SwRS-MDOKFSTUDIO-CODE-007 | S3 | 1.34 | syntax-narrow-python |
| test/visual/scenarioDefinitions1.ts:787 | SwRS-MDOKFSTUDIO-FMSCHEMA-006 | S1,S5 | 0.71 | okf-schema-table |
| test/visual/scenarioDefinitions1.ts:800 | SwRS-MDOKFSTUDIO-FMSCHEMA-014 | S4,S7 | 0.58 | okf-schema-narrow |
| test/visual/scenarioDefinitions1.ts:1386 | SwRS-MDOKFSTUDIO-MYST-096 | S1 | 1.34 |  |
| test/visual/scenarioDefinitions2.ts:314 | SwRS-MDOKFSTUDIO-FMSCHEMA-006 | S1,S3 | 0.71 | okf-schema-dark |
| test/visual/scenarioDefinitions2.ts:379 | SwRS-MDOKFSTUDIO-FMSCHEMA-005 | S2 | 0.5 | frontmatter-scroll-feedback |
| test/visual/scenarioDefinitions2.ts:700 | SwRS-MDOKFSTUDIO-MYST-036 | S1 | 1.34 |  |
| test/visual/scenarioDefinitions2.ts:715 | SwRS-MDOKFSTUDIO-FMSCHEMA-067 | S5,S6 | 1.41 |  |
| test/visual/scenarioDefinitions2.ts:799 | SwRS-MDOKFSTUDIO-MYST-006 | S4,S5 | 0.45 |  |
| test/visual/scenarioDefinitions2.ts:800 | SwRS-MDOKFSTUDIO-MYST-001 | S2 | 1.0 |  |
| test/visual/scenarioDefinitions2.ts:859 | SwRS-MDOKFSTUDIO-DIAG-024 | S4,S5 | 1.22 |  |
| test/visual/scenarioDefinitions2.ts:901 | SwRS-MDOKFSTUDIO-DIAG-039 | S4 | 1.15 |  |
| test/visual/scenarioDefinitions2.ts:976 | SwRS-MDOKFSTUDIO-THEME-043 | S2,S3 | 0.71 |  |
| test/visual/scenarioDefinitions2.ts:1004 | SwRS-MDOKFSTUDIO-TRUST-001 | S1 | 1.15 |  |
| test/visual/scenarioDefinitions2.ts:1267 | SwRS-MDOKFSTUDIO-MYST-081 | S4,S8 | 1.0 |  |
| test/visual/svgPictureScenarios.ts:42 | SwRS-MDOKFSTUDIO-DIAG-126 | S1,S2 | 0.58 |  |
| test/visual/scenarioDefinitions3.ts:63 | SwRS-MDOKFSTUDIO-GFM-034 | S1,S4 | 1.15 |  |
| test/visual/scenarioDefinitions3.ts:74 | SwRS-MDOKFSTUDIO-MYST-102 | S1,S2 | 1.34 |  |
