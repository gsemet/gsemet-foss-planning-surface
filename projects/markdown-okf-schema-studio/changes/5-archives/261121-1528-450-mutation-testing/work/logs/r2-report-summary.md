# Mutation summary

Generated 2026-11-21T13:05:47.325Z. Phases: core, others.

Mutants: 9 Ignored, 1700 CompileError, 185 NoCoverage, 2611 Killed, 398 Timeout, 1104 Survived. Tests that ran: 1396.

## Sample

This is a sample: 51 of 162 files of src/core were mutated, so every reading below is "on the sample". Tests that only load sampled modules are not judged: a test is listed as zero-kill or redundant only when its test file is named after a sampled source file of the same sub-folder. Tests left out of the judgement: 101 zero-kill, 722 redundant, 101 reaching no sampled mutant.

| sampled file | mutants |
| --- | --- |
| src/core/comments/commentModel.ts | 381 |
| src/core/comments/inlineThread.ts | 217 |
| src/core/configuration/commentsConfiguration.ts | 2 |
| src/core/configuration/editingConfiguration.ts | 3 |
| src/core/configuration/editorAssociationMigration.ts | 53 |
| src/core/configuration/frontmatterConfiguration.ts | 2 |
| src/core/configuration/plantUmlConfiguration.ts | 18 |
| src/core/configuration/previewConfiguration.ts | 10 |
| src/core/directives/registry.ts | 45 |
| src/core/edits/textEdit.ts | 72 |
| src/core/export/htmlExport.ts | 30 |
| src/core/find/findMatches.ts | 97 |
| src/core/frontmatter/fileLinks.ts | 367 |
| src/core/frontmatter/frontmatterChanges.ts | 99 |
| src/core/frontmatter/sameData.ts | 212 |
| src/core/frontmatter/schemaRegistry.ts | 24 |
| src/core/frontmatter/schemaValidator.ts | 89 |
| src/core/frontmatter/stemIndex.ts | 168 |
| src/core/mapping/blankRuns.ts | 26 |
| src/core/mapping/imageReference.ts | 24 |
| src/core/mapping/labelRename.ts | 82 |
| src/core/mapping/pastedImage.ts | 91 |
| src/core/mapping/sourceMapping.ts | 80 |
| src/core/mapping/textDiff.ts | 125 |
| src/core/myst/confLocator.ts | 133 |
| src/core/navigation/openingPolicy.ts | 76 |
| src/core/navigation/previewNavigation.ts | 283 |
| src/core/palette/emoji.ts | 64 |
| src/core/palette/paletteIcons.ts | 8 |
| src/core/paste/htmlToMarkdown.ts | 999 |
| src/core/preview/contentPatch.ts | 228 |
| src/core/preview/flushWait.ts | 50 |
| src/core/preview/previewStyles.ts | 23 |
| src/core/preview/themeTokens.ts | 8 |
| src/core/preview/updatedRanges.ts | 77 |
| src/core/protocol/hostToPage.ts | 294 |
| src/core/protocol/revision.ts | 6 |
| src/core/protocol/router.ts | 22 |
| src/core/render/blockTagTitle.ts | 50 |
| src/core/render/chartData.ts | 108 |
| src/core/render/mystNode.ts | 127 |
| src/core/render/radioGroups.ts | 169 |
| src/core/scroll/anchorPolicy.ts | 254 |
| src/core/security/spanColors.ts | 292 |
| src/core/state/blockRange.ts | 19 |
| src/core/state/boundedState.ts | 77 |
| src/core/state/headingFold.ts | 87 |
| src/core/state/navigationHistory.ts | 75 |
| src/core/state/previewTheme.ts | 41 |
| src/core/state/previewViewPreferences.ts | 55 |
| src/core/syntax/markdownSyntax.ts | 65 |

## Score per sub-folder of src/core

| folder | score | killed | survived | no coverage | timeout | compile error | ignored | holes only another layer kills | score with other layers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| comments | 80.0% | 295 | 74 | 5 | 21 | 203 | 0 | 1 | 80.3% |
| configuration | 92.9% | 52 | 4 | 0 | 0 | 32 | 0 | 1 | 94.6% |
| directives | 86.2% | 18 | 2 | 2 | 7 | 13 | 3 | 0 | 86.2% |
| edits | 68.5% | 37 | 14 | 3 | 0 | 16 | 2 | 0 | 68.5% |
| export | 57.1% | 12 | 9 | 0 | 0 | 9 | 0 | 0 | 57.1% |
| find | 78.6% | 50 | 11 | 4 | 5 | 27 | 0 | 0 | 78.6% |
| frontmatter | 52.1% | 309 | 221 | 80 | 19 | 328 | 2 | 2 | 52.5% |
| mapping | 62.3% | 214 | 132 | 6 | 14 | 62 | 0 | 4 | 63.4% |
| myst | 80.2% | 50 | 12 | 4 | 15 | 52 | 0 | 0 | 80.2% |
| navigation | 72.1% | 172 | 67 | 5 | 14 | 101 | 0 | 1 | 72.5% |
| palette | 3.3% | 2 | 58 | 0 | 0 | 12 | 0 | 17 | 31.7% |
| paste | 54.6% | 415 | 292 | 54 | 1 | 237 | 0 | 0 | 54.6% |
| preview | 82.9% | 215 | 47 | 0 | 13 | 111 | 0 | 1 | 83.3% |
| protocol | 77.5% | 145 | 42 | 0 | 0 | 134 | 1 | 0 | 77.5% |
| render | 85.7% | 202 | 34 | 8 | 49 | 161 | 0 | 1 | 86.0% |
| scroll | 67.8% | 142 | 62 | 6 | 1 | 43 | 0 | 0 | 67.8% |
| security | 97.8% | 64 | 2 | 4 | 197 | 25 | 0 | 0 | 97.8% |
| state | 90.0% | 203 | 19 | 4 | 4 | 123 | 1 | 7 | 93.0% |
| syntax | 96.3% | 14 | 2 | 0 | 38 | 11 | 0 | 0 | 96.3% |

## Score per SwRS

Share of the mutants reached by the tests of the SwRS that those tests kill (a test can carry several IDs, so the shares overlap).

| SwRS | tests | mutants reached | killed | score |
| --- | --- | --- | --- | --- |
| StRS-MDOKFSTUDIO-CORE-006 | 1 | 574 | 364 | 63.4% |
| StRS-MDOKFSTUDIO-FMSCHEMA-001 | 1 | 68 | 44 | 64.7% |
| SwRS-MDOKFSTUDIO-BLOCK-003 | 1 | 132 | 74 | 56.1% |
| SwRS-MDOKFSTUDIO-BLOCK-014 | 2 | 372 | 334 | 89.8% |
| SwRS-MDOKFSTUDIO-BLOCK-017 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-042 | 2 | 195 | 105 | 53.8% |
| SwRS-MDOKFSTUDIO-BLOCK-087 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-094 | 4 | 65 | 53 | 81.5% |
| SwRS-MDOKFSTUDIO-BLOCK-109 | 4 | 96 | 39 | 40.6% |
| SwRS-MDOKFSTUDIO-BLOCK-117 | 3 | 121 | 87 | 71.9% |
| SwRS-MDOKFSTUDIO-BLOCK-124 | 2 | 44 | 44 | 100.0% |
| SwRS-MDOKFSTUDIO-BLOCK-127 | 2 | 96 | 73 | 76.0% |
| SwRS-MDOKFSTUDIO-BLOCK-156 | 1 | 44 | 44 | 100.0% |
| SwRS-MDOKFSTUDIO-BLOCK-166 | 2 | 121 | 80 | 66.1% |
| SwRS-MDOKFSTUDIO-BLOCK-169 | 1 | 44 | 44 | 100.0% |
| SwRS-MDOKFSTUDIO-BLOCK-174 | 1 | 44 | 44 | 100.0% |
| SwRS-MDOKFSTUDIO-BLOCK-191 | 2 | 11 | 8 | 72.7% |
| SwRS-MDOKFSTUDIO-BLOCK-193 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-205 | 1 | 16 | 10 | 62.5% |
| SwRS-MDOKFSTUDIO-BLOCK-234 | 9 | 216 | 116 | 53.7% |
| SwRS-MDOKFSTUDIO-BLOCK-256 | 1 | 44 | 44 | 100.0% |
| SwRS-MDOKFSTUDIO-BLOCK-257 | 4 | 93 | 58 | 62.4% |
| SwRS-MDOKFSTUDIO-BLOCK-259 | 7 | 120 | 52 | 43.3% |
| SwRS-MDOKFSTUDIO-BLOCK-260 | 5 | 331 | 305 | 92.1% |
| SwRS-MDOKFSTUDIO-BLOCK-262 | 4 | 93 | 58 | 62.4% |
| SwRS-MDOKFSTUDIO-BLOCK-263 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-265 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-266 | 11 | 421 | 354 | 84.1% |
| SwRS-MDOKFSTUDIO-BLOCK-268 | 6 | 123 | 66 | 53.7% |
| SwRS-MDOKFSTUDIO-BLOCK-269 | 5 | 123 | 66 | 53.7% |
| SwRS-MDOKFSTUDIO-CODE-001 | 9 | 448 | 359 | 80.1% |
| SwRS-MDOKFSTUDIO-CODE-007 | 2 | 94 | 58 | 61.7% |
| SwRS-MDOKFSTUDIO-CODE-008 | 2 | 96 | 58 | 60.4% |
| SwRS-MDOKFSTUDIO-CODE-014 | 2 | 454 | 338 | 74.4% |
| SwRS-MDOKFSTUDIO-CODE-019 | 1 | 96 | 39 | 40.6% |
| SwRS-MDOKFSTUDIO-CODE-039 | 8 | 502 | 356 | 70.9% |
| SwRS-MDOKFSTUDIO-CODE-040 | 5 | 404 | 342 | 84.7% |
| SwRS-MDOKFSTUDIO-CORE-001 | 3 | 330 | 287 | 87.0% |
| SwRS-MDOKFSTUDIO-CORE-003 | 8 | 503 | 354 | 70.4% |
| SwRS-MDOKFSTUDIO-CORE-008 | 2 | 93 | 58 | 62.4% |
| SwRS-MDOKFSTUDIO-CORE-010 | 3 | 495 | 356 | 71.9% |
| SwRS-MDOKFSTUDIO-CORE-012 | 5 | 410 | 343 | 83.7% |
| SwRS-MDOKFSTUDIO-CORE-013 | 5 | 429 | 360 | 83.9% |
| SwRS-MDOKFSTUDIO-CORE-022 | 6 | 490 | 359 | 73.3% |
| SwRS-MDOKFSTUDIO-CORE-025 | 1 | 318 | 287 | 90.3% |
| SwRS-MDOKFSTUDIO-CORE-028 | 6 | 331 | 287 | 86.7% |
| SwRS-MDOKFSTUDIO-CORE-034 | 3 | 330 | 287 | 87.0% |
| SwRS-MDOKFSTUDIO-CORE-050 | 3 | 93 | 59 | 63.4% |
| SwRS-MDOKFSTUDIO-CORE-071 | 10 | 505 | 341 | 67.5% |
| SwRS-MDOKFSTUDIO-CORE-072 | 12 | 377 | 338 | 89.7% |
| SwRS-MDOKFSTUDIO-CORE-073 | 4 | 574 | 413 | 72.0% |
| SwRS-MDOKFSTUDIO-CORE-079 | 20 | 428 | 361 | 84.3% |
| SwRS-MDOKFSTUDIO-CORE-088 | 2 | 526 | 358 | 68.1% |
| SwRS-MDOKFSTUDIO-CORE-089 | 3 | 93 | 58 | 62.4% |
| SwRS-MDOKFSTUDIO-DIAG-001 | 3 | 593 | 415 | 70.0% |
| SwRS-MDOKFSTUDIO-DIAG-005 | 1 | 93 | 58 | 62.4% |
| SwRS-MDOKFSTUDIO-DIAG-017 | 2 | 470 | 353 | 75.1% |
| SwRS-MDOKFSTUDIO-DIAG-023 | 2 | 459 | 343 | 74.7% |
| SwRS-MDOKFSTUDIO-DIAG-024 | 4 | 433 | 359 | 82.9% |
| SwRS-MDOKFSTUDIO-DIAG-032 | 1 | 93 | 58 | 62.4% |
| SwRS-MDOKFSTUDIO-DIAG-050 | 2 | 96 | 39 | 40.6% |
| SwRS-MDOKFSTUDIO-DIAG-054 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-DIAG-068 | 3 | 435 | 359 | 82.5% |
| SwRS-MDOKFSTUDIO-DIAG-084 | 10 | 3 | 2 | 66.7% |
| SwRS-MDOKFSTUDIO-DIAG-089 | 4 | 393 | 343 | 87.3% |
| SwRS-MDOKFSTUDIO-DIAG-097 | 4 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-DIAG-105 | 4 | 522 | 385 | 73.8% |
| SwRS-MDOKFSTUDIO-DIAG-121 | 5 | 460 | 365 | 79.3% |
| SwRS-MDOKFSTUDIO-DIAG-122 | 9 | 452 | 368 | 81.4% |
| SwRS-MDOKFSTUDIO-DIAG-124 | 1 | 565 | 413 | 73.1% |
| SwRS-MDOKFSTUDIO-DIAG-125 | 14 | 444 | 353 | 79.5% |
| SwRS-MDOKFSTUDIO-DIAG-126 | 1 | 330 | 287 | 87.0% |
| SwRS-MDOKFSTUDIO-FMEDIT-004 | 1 | 92 | 44 | 47.8% |
| SwRS-MDOKFSTUDIO-FMEDIT-010 | 3 | 274 | 131 | 47.8% |
| SwRS-MDOKFSTUDIO-FMEDIT-016 | 4 | 171 | 66 | 38.6% |
| SwRS-MDOKFSTUDIO-FMEDIT-024 | 3 | 92 | 63 | 68.5% |
| SwRS-MDOKFSTUDIO-FMEDIT-029 | 3 | 92 | 63 | 68.5% |
| SwRS-MDOKFSTUDIO-FMEDIT-043 | 6 | 92 | 62 | 67.4% |
| SwRS-MDOKFSTUDIO-FMEDIT-067 | 3 | 125 | 59 | 47.2% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-001 | 2 | 383 | 309 | 80.7% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-004 | 1 | 48 | 44 | 91.7% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-005 | 4 | 129 | 88 | 68.2% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-006 | 5 | 53 | 47 | 88.7% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-014 | 2 | 71 | 54 | 76.1% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-023 | 2 | 107 | 49 | 45.8% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-029 | 1 | 53 | 44 | 83.0% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-039 | 2 | 65 | 44 | 67.7% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-046 | 4 | 203 | 105 | 51.7% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-050 | 3 | 181 | 89 | 49.2% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-055 | 1 | 200 | 107 | 53.5% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-063 | 1 | 53 | 44 | 83.0% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-067 | 4 | 470 | 351 | 74.7% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-084 | 1 | 53 | 46 | 86.8% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-090 | 1 | 53 | 44 | 83.0% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-091 | 3 | 137 | 75 | 54.7% |
| SwRS-MDOKFSTUDIO-GFM-001 | 4 | 358 | 327 | 91.3% |
| SwRS-MDOKFSTUDIO-GFM-008 | 3 | 465 | 360 | 77.4% |
| SwRS-MDOKFSTUDIO-GFM-009 | 38 | 508 | 371 | 73.0% |
| SwRS-MDOKFSTUDIO-GFM-016 | 2 | 331 | 305 | 92.1% |
| SwRS-MDOKFSTUDIO-GFM-021 | 2 | 192 | 96 | 50.0% |
| SwRS-MDOKFSTUDIO-GFM-031 | 2 | 440 | 335 | 76.1% |
| SwRS-MDOKFSTUDIO-GFM-034 | 6 | 500 | 394 | 78.8% |
| SwRS-MDOKFSTUDIO-GFM-040 | 11 | 459 | 420 | 91.5% |
| SwRS-MDOKFSTUDIO-GFM-041 | 8 | 124 | 85 | 68.5% |
| SwRS-MDOKFSTUDIO-LAYOUT-001 | 1 | 93 | 58 | 62.4% |
| SwRS-MDOKFSTUDIO-LAYOUT-002 | 4 | 99 | 64 | 64.6% |
| SwRS-MDOKFSTUDIO-LAYOUT-007 | 1 | 93 | 58 | 62.4% |
| SwRS-MDOKFSTUDIO-LAYOUT-022 | 2 | 93 | 58 | 62.4% |
| SwRS-MDOKFSTUDIO-LAYOUT-023 | 1 | 93 | 58 | 62.4% |
| SwRS-MDOKFSTUDIO-LAYOUT-032 | 2 | 93 | 58 | 62.4% |
| SwRS-MDOKFSTUDIO-LIFE-004 | 2 | 355 | 301 | 84.8% |
| SwRS-MDOKFSTUDIO-LIFE-026 | 1 | 10 | 10 | 100.0% |
| SwRS-MDOKFSTUDIO-LIFE-032 | 1 | 109 | 46 | 42.2% |
| SwRS-MDOKFSTUDIO-LIFE-039 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-044 | 1 | 1 | 0 | 0.0% |
| SwRS-MDOKFSTUDIO-LIFE-049 | 1 | 93 | 58 | 62.4% |
| SwRS-MDOKFSTUDIO-LIFE-069 | 3 | 523 | 392 | 75.0% |
| SwRS-MDOKFSTUDIO-LIFE-071 | 1 | 536 | 411 | 76.7% |
| SwRS-MDOKFSTUDIO-LIFE-094 | 6 | 61 | 54 | 88.5% |
| SwRS-MDOKFSTUDIO-LIFE-100 | 1 | 28 | 23 | 82.1% |
| SwRS-MDOKFSTUDIO-LIFE-108 | 1 | 96 | 39 | 40.6% |
| SwRS-MDOKFSTUDIO-LIFE-119 | 1 | 153 | 81 | 52.9% |
| SwRS-MDOKFSTUDIO-LIFE-125 | 1 | 18 | 10 | 55.6% |
| SwRS-MDOKFSTUDIO-LIFE-127 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-149 | 1 | 1 | 0 | 0.0% |
| SwRS-MDOKFSTUDIO-LIFE-156 | 1 | 1 | 0 | 0.0% |
| SwRS-MDOKFSTUDIO-LIFE-169 | 5 | 131 | 64 | 48.9% |
| SwRS-MDOKFSTUDIO-LIFE-170 | 3 | 33 | 13 | 39.4% |
| SwRS-MDOKFSTUDIO-LIFE-173 | 2 | 134 | 60 | 44.8% |
| SwRS-MDOKFSTUDIO-LIFE-174 | 1 | 1 | 0 | 0.0% |
| SwRS-MDOKFSTUDIO-LIFE-175 | 4 | 41 | 37 | 90.2% |
| SwRS-MDOKFSTUDIO-LIFE-178 | 2 | 427 | 351 | 82.2% |
| SwRS-MDOKFSTUDIO-LIFE-181 | 1 | 43 | 25 | 58.1% |
| SwRS-MDOKFSTUDIO-LIFE-183 | 4 | 21 | 20 | 95.2% |
| SwRS-MDOKFSTUDIO-LIFE-184 | 9 | 20 | 20 | 100.0% |
| SwRS-MDOKFSTUDIO-MYST-001 | 11 | 496 | 370 | 74.6% |
| SwRS-MDOKFSTUDIO-MYST-006 | 3 | 498 | 362 | 72.7% |
| SwRS-MDOKFSTUDIO-MYST-013 | 5 | 480 | 360 | 75.0% |
| SwRS-MDOKFSTUDIO-MYST-017 | 3 | 474 | 342 | 72.2% |
| SwRS-MDOKFSTUDIO-MYST-019 | 5 | 466 | 359 | 77.0% |
| SwRS-MDOKFSTUDIO-MYST-024 | 8 | 436 | 328 | 75.2% |
| SwRS-MDOKFSTUDIO-MYST-031 | 3 | 465 | 350 | 75.3% |
| SwRS-MDOKFSTUDIO-MYST-036 | 1 | 442 | 335 | 75.8% |
| SwRS-MDOKFSTUDIO-MYST-038 | 2 | 101 | 47 | 46.5% |
| SwRS-MDOKFSTUDIO-MYST-045 | 3 | 215 | 120 | 55.8% |
| SwRS-MDOKFSTUDIO-MYST-053 | 4 | 371 | 333 | 89.8% |
| SwRS-MDOKFSTUDIO-MYST-057 | 7 | 362 | 311 | 85.9% |
| SwRS-MDOKFSTUDIO-MYST-063 | 5 | 474 | 359 | 75.7% |
| SwRS-MDOKFSTUDIO-MYST-066 | 8 | 60 | 42 | 70.0% |
| SwRS-MDOKFSTUDIO-MYST-072 | 2 | 458 | 363 | 79.3% |

84 more row(s): see summary.json.

## Tests that kill nothing

Tests that reach killable mutants and kill none of them (zero-kill candidates).

| test | mutants reached |
| --- | --- |
| core/configuration/commentsConfiguration.test.js::T43: a non-string author name falls back to the empty default | 1 CompileError, 1 Killed |
| core/configuration/editingConfiguration.test.js::a fresh workspace starts the palette in GFM | 2 CompileError, 1 Killed |
| core/configuration/editingConfiguration.test.js::falls back to GFM for an unknown or non-string palette mode | 1 CompileError, 1 Killed |
| core/configuration/editingConfiguration.test.js::stored choice wins: a stored palette mode is kept over the default and the setting | 2 CompileError, 1 Killed |
| core/configuration/frontmatterConfiguration.test.js::frontmatter visibility and strict validation can be configured independently | 1 CompileError, 1 Killed |
| core/configuration/plantUmlConfiguration.test.js::uses an empty path for non-string configuration values | 4 CompileError, 3 Killed |
| core/configuration/previewConfiguration.test.js::comment chips are shown by default and can be turned off | 1 CompileError, 1 Killed |
| core/configuration/previewConfiguration.test.js::incremental updates can be turned off and default to on | 1 CompileError, 1 Killed |
| core/configuration/previewConfiguration.test.js::normalizes preview content width and reserves zero for unlimited | 1 CompileError, 1 Killed |
| core/configuration/previewConfiguration.test.js::normalizes sticky heading depth to one through six levels | 1 CompileError, 1 Killed |
| core/configuration/previewConfiguration.test.js::the content width setting is rounded to whole pixels and a negative value gives the default | 1 CompileError, 1 Killed |
| core/export/htmlExport.test.js::the snapshot guard accepts the page shape and refuses a malformed one | 24 CompileError, 28 Killed, 71 Timeout, 7 Survived |
| core/mapping/textDiff.test.js::replacement reproduces the target for 200 seeded random pairs | 2 CompileError, 16 Killed, 7 Survived |
| core/myst/confLocator.test.js::myst_nb counts like myst_parser | 41 CompileError, 31 Killed, 9 Survived, 9 Timeout |
| core/navigation/openingPolicy.test.js::rule 9: a plain opening, or a jump with the setting off, stays a text editor | 17 CompileError, 16 Killed |
| core/preview/previewStyles.test.js::CR 034: a narrow pane keeps the palette sticky; it wraps inside the pane instead of leaving the flow | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR 034: the table toolbar rides down with a scrolling table by a transform, not by layout | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR 046: the motion layer is short and never animates layout or the table bar's transform | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR 107: the preview block quote background outranks the VS Code webview default rule | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR 112: a horizontal rule is 12px taller above and below than its line, with the spacing unchanged | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR 112: the edit bar buttons share the floating toolbar's tooltip bubble and slide it in on hover | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR 123: the frame reserves the distance the sticky palette rides down, as a top margin | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR 143: the chevron shows on hover, focus and while folded, and a folded block drops its spacing | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR 143: the toolbar has a Fold button, off until a section is folded | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR 162: every tooltip bubble slides in from the left with one shared animation | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR 162: reduced motion turns off the tooltip slide-in and the toolbar rows unroll | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR 162: the toolbar rows unroll as one block, only under the animating mark | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR 168: the table toolbar paints above the row and column handle layer | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR147: the side-by-side cards are two columns, switch off with the page attribute and never show in edit mode | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::CR147: the toolbar offers a Side-by-side button in the review row after the Table of contents button, not pressed at first | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::K1: long words and bare URLs wrap inside text blocks, links and table cells | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::Mermaid diagrams keep SVG images contained and source inspectable | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::MyST numbered and emphasized code lines are styled | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::MyST table alignment and notebook output placeholders are styled | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::P11: the slash menu floats above the toolbar and the palette popovers and is placed by the runtime | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::P4: the palette sits on top of the frame and sticks below the sticky band and the toolbar | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::P4: the palette stays in the flow in short panes and when the runtime says it is too tall | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::P7: full width uses the 16 px gutter a broken-out table keeps in auto | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::README HTML: align, per-theme picture images and the edit-mode frame titled with the tag | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::T08: zoom scales the content font size and the column width together | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::T10: full width lifts the column limit and auto lets flagged elements break out | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::T10: the auto measure lifts every cap, the row-handle one included | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::T15: an open comment is an admonition-like box and showComments off hides the gray chips only | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::T16: the change bars sit in one column of a layer, square, with no layout shift | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::T16b: only the current TOC entry loses its rounded corners | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::T21: the edition palette is a wrapping pill bar with an in-frame popover and no inline style | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::T28: insertion points are zero-height, hover-revealed gutter buttons | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::T43: the pending overlay is fixed, pointer-transparent and never in flow | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::T44: the Orphaned comments box sits in the content's bottom padding and adds no scroll height | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::a block quote is tinted with the theme block quote background | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::a captioned code block is left-aligned with its caption as a title bar on top | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::a narrow pane with the TOC on pads the content for the 16px rail and keeps the overlay under the toolbar tooltip | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::a narrow pane with the TOC on shows a rail and opens the column as an overlay | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::active paragraph editors share the rendered paragraph spacing | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::active toolbar toggles do not show a redundant focus ring | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::an inline thread is a green chip with a bubble, a green titled box, and goes with the gray chips | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::block editing grows without internal scrolling and is framed | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::code blocks use one font scale, one box, and scroll a long line only when it does not fit | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::comments hidden by the button or the setting: highlights lose their paint, badges and the orphan box go | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::content table cells keep a 5em minimum width in the rendered view, the properties table keeps its own | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::control tooltips retain their offset while sticky headings remain at the top | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::description header controls align right and restore only when collapsed | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::diff lines use full-width theme-aware add and delete treatments | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::edit mode outlines the hovered block without moving the layout | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::edit mode titles an open comment with its literal tag in code font | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::fenced code uses the editor foreground and one font scale | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::figure captions are centred and de-emphasised | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::first-element gap: 40px on the first child, clearance only on the first editor and the Start writing button | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::floating preview toolbar supports forced dark and white palettes | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::forced preview themes supply dropdown colors independently of the host | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::frontmatter and table editors keep the active cell surface without nested input frames | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::frontmatter edit hover colors follow the selected preview theme | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::frontmatter edits stay inline while edit mode preserves source newlines | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::frontmatter field actions sit in the editing row with labels and no pseudo-tooltips | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::frontmatter link tooltips wrap text in a fixed theme-aware pointer-transparent surface | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::frontmatter properties label is inset, table-matched, and unboxed | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::images never overflow the preview column | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::in edit mode table cells keep a minimum width and the edited cell is wider | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::linked file details are muted, italic, and clipped to the available line | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::list insertion lines show the drop boundary without moving the rows | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::narrow properties wrap long paths without hiding expanded descriptions | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::overflowing content tables keep short cells whole and show scroll shadows | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::preview controls stack above the sticky heading band | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::preview toolbar has four rows of four buttons: main with the collapse button, navigation, view, review | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::properties tables fill the preview content column | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::raw Markdown and YAML editors use the editor font, text fields keep the preview font | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::scrollbar tracks and thumbs follow the preview theme | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::selected blocks get a solid focus outline and the count is announced off screen | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::shared borders resolve against the body palette rather than inherited host root colors | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::sticky headings align with content and emphasize text in a full-width band | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::sticky headings start at the viewport top without filler and leave horizontal room for controls | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::table toolbar sits in the document flow above the table with labelled buttons | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the Comments toolbar button hides the gray and thread chips at once and goes away with the setting | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the Names header label never breaks inside the word, even when every key is shorter | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the TOC column is hidden by default, reserves 256px when open and hides on narrow panes | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the block editor status and its buttons share one wrapping row | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the block editor status is not pushed up by the paragraph margin | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the block editor status uses compact text | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the caption title bar takes its colours from theme variables only | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the comment boxes (compose, thread popover, open comment) have square corners | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the find bar and the match paint read the theme tokens, in forced colours as well | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the issue badge is a plain button and a clicked badge highlights its row | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the key column of the properties table fits its keys and never breaks one inside a word | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the table bar draws one rule per group and the cell group carries its own rule | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the table cell editor shares the block editor textarea rule and grows with its content | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the table toolbar status is not pushed up by the paragraph margin | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the theme neutralises Shibuya page gutters | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the top heading keeps the stock preview rule underneath it | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::the warning banner keeps clear of the four-button-wide toolbar, expanded or collapsed | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::toolbar tooltips stay opaque and anchored even on disabled controls | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::typography is driven by VS Code markdown preview variables | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/previewStyles.test.js::white mode keeps code backgrounds soft and code text readable blue | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/themeTokens.test.js::every token the stylesheet or the Mermaid theme reads is in the token map | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/preview/themeTokens.test.js::the forced theme modes set the neutral tokens, not the VS Code variables | 22 CompileError, 28 Killed, 58 Timeout, 7 Survived |
| core/render/blockTagTitle.test.js::text that is not an opening tag has no title | 4 CompileError, 10 Timeout, 1 Killed |
| core/render/chartData.test.js::inlineChartFiles puts the rows of each read file into values and leaves no url | 1 CompileError, 2 Survived, 3 Killed |
| core/state/previewTheme.test.js::a fresh workspace has no stored mode and the built-in default is cream | 9 CompileError, 13 Killed, 1 Survived |
| core/syntax/markdownSyntax.test.js::advanceFence tracks one fence at a time, with colon fences on request | 79 Timeout, 8 Killed, 3 Survived, 9 CompileError |

## Redundant tests (greedy set)

A keeper set of 218 test(s) kills every killed mutant; the others below add nothing the keepers do not kill. Two duplicate tests are never both listed: one of them is a keeper.

| redundant test | killed mutants | also killed by keepers |
| --- | --- | --- |
| core/comments/commentModel.test.js::T42: a valid file parses into threads | 45 | 8 keeper(s), for example core/comments/commentEditing.test.js |
| core/comments/commentModel.test.js::T42: serialization is stable: fixed key order, 2 spaces, trailing newline | 51 | 8 keeper(s), for example core/comments/commentEditing.test.js |
| core/comments/inlineThread.test.js::a reply goes above the closing marker and nothing else changes | 54 | 10 keeper(s), for example core/edits/sourceEdits.test.js |
| core/comments/inlineThread.test.js::blank lines inside a message are kept, and a tab indent is accepted | 20 | 9 keeper(s), for example core/edits/sourceEdits.test.js |
| core/directives/registry.test.js::each directive name has one plug-in, found by its exact name | 1 | 4 keeper(s), for example core/directives/renderReq.registry.requirements.test.js |
| core/directives/registry.test.js::the figure pass puts the source lines on the figure; the table pass marks a list-table | 2 | 5 keeper(s), for example core/directives/renderReq.registry.requirements.test.js |
| core/edits/textEdit.test.js::source lines split on LF, CRLF and CR, and a final line break adds an empty last line | 10 | 1 keeper(s), for example core/edits/sourceEdits.test.js |
| core/export/htmlExport.test.js::a THREAD chip with its popover, a TODO chip, source-mapping attributes and the tabindex of mapped blocks are left out | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::a front matter value and a key under their editors are exported shown, without the editor | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::a local image becomes a data URI and an unreadable one is counted and loses its source | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::a mailto link is kept and a file: link, an invalid anchor and a query-only link are unwrapped and reported | 14 | 7 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::a paragraph under the block editor is exported, its editor is not | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::a properties table without a schema keeps its two columns inside the closed details | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::a style value cannot close the style element and a script URL is dropped | 3 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::a tab set works without script: radios, labels, and the shown tab is the one the page showed | 6 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::a table cell under the cell editor is exported with its content shown and without the editor | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::a task list checkbox stays, disabled and without its edit attributes | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::every candidate of a srcset is embedded and an unreadable one is dropped | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::folded sections are shown and the fold attributes are gone | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::nested tab sets get their own radio names and a dropdown keeps its open state | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::review comments, controls and editing chrome are left out, find marks keep their text | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::the Description column stays and the editing data goes, whatever the toggle state of the page | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::the file is one document with no script, no linked file and no import, and no vscode- name | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::the host's list of blank runs and a blank-lines block are not exported | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::the properties table becomes a closed details with a summary and no editing data | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::the title falls back to the first heading, then to the file name | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::the token rule follows the preview sheet and names every resolved token | 7 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::the width mode, the width rule and the theme mode go on the file, the zoom and clearance do not | 12 | 4 keeper(s), for example core/export/htmlExport.test.js |
| core/find/findMatches.test.js::a literal query finds every occurrence, ignoring case unless asked | 8 | 6 keeper(s), for example core/find/findMatches.test.js |
| core/frontmatter/frontmatterChanges.test.js::CR 155: a key that disappeared is removed, a changed list item modifies the field | 15 | 4 keeper(s), for example core/frontmatter/frontmatterChanges.test.js |
| core/frontmatter/frontmatterChanges.test.js::CR 155: changed and added fields keep their line ranges and add nothing | 5 | 4 keeper(s), for example core/frontmatter/frontmatterChanges.test.js |
| core/frontmatter/frontmatterChanges.test.js::CR 155: the same fields in another order are not changes, and a missing front matter has none | 8 | 2 keeper(s), for example core/frontmatter/frontmatterChanges.test.js |
| core/frontmatter/sameData.test.js::isSameData compares key lists in order, as the patch verification needs | 22 | 2 keeper(s), for example core/frontmatter/sameData.test.js |
| core/frontmatter/schemaValidator.test.js::validator cache returns the same compiled function for a schema object | 1 | 40 keeper(s), for example core/render/mystFeatures.test.js |
| core/mapping/blankRuns.test.js::CR LF and lone CR line endings give the same runs | 12 | 40 keeper(s), for example core/render/mystFeatures.test.js |
| core/mapping/blankRuns.test.js::a CommonMark blank line holds only spaces and tabs | 1 | 40 keeper(s), for example core/render/mystFeatures.test.js |
| core/mapping/blankRuns.test.js::one blank line is the separator, two or more are a run | 14 | 40 keeper(s), for example core/render/mystFeatures.test.js |
| core/mapping/blankRuns.test.js::spaces and tabs are blank, a no-break space is not | 14 | 40 keeper(s), for example core/render/mystFeatures.test.js |
| core/mapping/blankRuns.test.js::the frontmatter is not part of a run, and the lines after it can be | 12 | 40 keeper(s), for example core/render/mystFeatures.test.js |
| core/mapping/imageReference.test.js::relativeImageReference accepts Windows separators and refuses another drive | 7 | 2 keeper(s), for example core/mapping/dropReferences.test.js |
| core/mapping/imageReference.test.js::relativeImageReference gives a POSIX path relative to the document folder | 4 | 2 keeper(s), for example core/mapping/dropReferences.test.js |
| core/mapping/labelRename.test.js::the renderer, the page and the host share one label name pattern | 6 | 5 keeper(s), for example core/mapping/labelRename.test.js |
| core/mapping/pastedImage.test.js::isBase64 accepts the base64 alphabet only | 9 | 1 keeper(s), for example core/protocol/pageToHost.test.js |
| core/mapping/pastedImage.test.js::nextImageName gives up after 1000 suffixes | 9 | 1 keeper(s), for example core/mapping/pastedImage.test.js |
| core/mapping/textDiff.test.js::identical input yields an empty replacement | 7 | 3 keeper(s), for example core/edits/sourceEdits.test.js |
| core/mapping/textDiff.test.js::insertion at the start and at the end | 20 | 3 keeper(s), for example core/edits/sourceEdits.test.js |
| core/mapping/textDiff.test.js::insertion, deletion and replacement in the middle | 22 | 3 keeper(s), for example core/edits/sourceEdits.test.js |
| core/mapping/textDiff.test.js::repeated characters do not let prefix and suffix overlap | 5 | 3 keeper(s), for example core/edits/sourceEdits.test.js |
| core/myst/confLocator.test.js::D29: a single conf.py in a common folder of the root is the fallback | 23 | 6 keeper(s), for example core/render/renderPipeline.test.js |
| core/myst/confLocator.test.js::D29: an ancestor conf.py wins over a fallback, and invalidation covers the fallback | 30 | 6 keeper(s), for example core/render/renderPipeline.test.js |
| core/myst/confLocator.test.js::the nearest conf.py wins and the enabled set comes from it | 14 | 5 keeper(s), for example core/render/renderPipeline.test.js |
| core/navigation/openingPolicy.test.js::rule 7: with Open Markdown files in Studio on, a jump opens Studio at the line and a plain opening opens Studio | 7 | 5 keeper(s), for example core/navigation/openingPolicy.test.js |
| core/navigation/openingPolicy.test.js::rule 8: with Open search results in Studio on, a jump opens Studio at the line | 5 | 5 keeper(s), for example core/navigation/openingPolicy.test.js |
| core/navigation/previewNavigation.test.js::a link path is decoded once: a literal percent is reachable, an escaped percent is not decoded again | 7 | 5 keeper(s), for example core/export/htmlExport.test.js |
| core/navigation/previewNavigation.test.js::marker navigation selects exact marker identities | 11 | 2 keeper(s), for example core/frontmatter/fileLinks.test.js |
| core/paste/htmlToMarkdown.test.js::T1: htmlToMarkdown, VS Code copy: one line stays plain text | 11 | 10 keeper(s), for example core/paste/htmlToMarkdown.test.js |
| core/paste/htmlToMarkdown.test.js::T1: htmlToMarkdown, VS Code copy: several lines stay raw text, never wrapped in a fence | 24 | 10 keeper(s), for example core/paste/htmlToMarkdown.test.js |
| core/preview/contentPatch.test.js::T08: two renders with different zoom have the same shell key and the same context key | 62 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/contentPatch.test.js::T17: the shell key is equal whatever the incoming-changes preference, and the Diff button is in both | 64 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/contentPatch.test.js::T34: content that mentions a container inside the content does not change the extracted content | 34 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/contentPatch.test.js::T34: extractMainContent returns the inner HTML of the content container of a real page | 35 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/contentPatch.test.js::T34: injecting PlantUML diagrams into a page keeps its shell key, so the diagrams can be patched in | 47 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/contentPatch.test.js::T34: reuseNonce swaps every occurrence, in the policy tokens and in the attributes | 8 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/contentPatch.test.js::T34: shell keys differ when Mermaid appears or disappears, and when math appears | 67 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/contentPatch.test.js::T34: two renders of one document type have equal shell keys despite other text, nonces and identifiers | 64 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/contentPatch.test.js::the page script is injected verbatim even when it contains replacement patterns | 5 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/previewStyles.test.js::MyST simple and no-icon admonition modifiers are styled | 3 | 5 keeper(s), for example core/directives/renderReq.registry.requirements.test.js |
| core/preview/previewStyles.test.js::Sphinx version admonitions use success, warning, and danger accents | 3 | 5 keeper(s), for example core/directives/renderReq.registry.requirements.test.js |
| core/preview/previewStyles.test.js::caution callouts are red with the octagon icon, not the warning amber | 3 | 5 keeper(s), for example core/directives/renderReq.registry.requirements.test.js |
| core/preview/previewStyles.test.js::dropdown admonitions show their open or closed state with a chevron | 3 | 5 keeper(s), for example core/directives/renderReq.registry.requirements.test.js |
| core/preview/previewStyles.test.js::every admonition flavour gets an accent colour | 3 | 5 keeper(s), for example core/directives/renderReq.registry.requirements.test.js |
| core/preview/previewStyles.test.js::preview content width is configurable and can be unlimited | 6 | 1 keeper(s), for example core/preview/layoutThemeStyles.test.js |
| core/preview/previewStyles.test.js::status titles and messages are block-level only on status pages and non-pending banners | 1 | 1 keeper(s), for example core/preview/previewStyles.test.js |
| core/preview/themeTokens.test.js::the page stylesheet reads VS Code variables only through the token map | 1 | 1 keeper(s), for example core/preview/previewStyles.test.js |
| core/preview/updatedRanges.test.js::CR 046: the patch that first shows an outside change carries its changed lines | 6 | 2 keeper(s), for example core/preview/updatedRanges.test.js |
| core/preview/updatedRanges.test.js::CR 046: typing in the active text editor does not glow, its undo and redo do | 9 | 1 keeper(s), for example core/preview/updatedRanges.test.js |
| core/protocol/hostToPage.test.js::the save command names the render and carries nothing else | 21 | 6 keeper(s), for example core/protocol/hostToPage.test.js |
| core/protocol/router.test.js::dispatch runs the handler of the message's type with the context and returns its result | 4 | 2 keeper(s), for example core/protocol/router.test.js |
| core/protocol/router.test.js::the router works as the page runtime bundles it | 4 | 2 keeper(s), for example core/protocol/router.test.js |
| core/render/chartData.test.js::isRemoteDataUrl is true for a scheme or a protocol-relative url and false for a path | 3 | 1 keeper(s), for example core/render/chartData.test.js |
| core/render/mystNode.test.js::setHast and mergeProperties add to the element a node renders as | 1 | 2 keeper(s), for example core/render/chartRendering.test.js |
| core/render/mystNode.test.js::source position attributes need a line and keep an end line that is not before it | 2 | 1 keeper(s), for example core/render/includeBudget.test.js |
| core/render/radioGroups.test.js::a group without a selection and a group with two selections render as written | 41 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/render/radioGroups.test.js::a lone radio item stays plain text | 7 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/render/radioGroups.test.js::in a list that mixes task items and options, and in a nested group, the option items and paragraphs are out of the Tab order | 59 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/render/radioGroups.test.js::radio markers stay literal in code and keep exact columns in quotes, CRLF files and after frontmatter | 42 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/render/radioGroups.test.js::the marker is ( ), (x) or (X) followed by a space or a tab, at the start of a list item | 46 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/render/radioGroups.test.js::the webview sanitizer keeps the radio roles, states and source attributes | 49 | 42 keeper(s), for example core/render/mystFeatures.test.js |
| core/scroll/anchorPolicy.test.js::converts lines to scroll positions and back through the reading offset | 80 | 4 keeper(s), for example core/scroll/anchorPolicy.test.js |
| core/security/spanColors.test.js::the colour grammar accepts hex and bounded rgb()/rgba() | 44 | 23 keeper(s), for example core/render/mystFeatures.test.js |
| core/security/spanColors.test.js::the colour grammar refuses every injection shape | 9 | 23 keeper(s), for example core/render/mystFeatures.test.js |
| core/state/blockRange.test.js::STAB-06: an empty block (an insertion editor) conflicts only with a change at its offset | 12 | 3 keeper(s), for example core/state/blockRange.test.js |
| core/state/blockRange.test.js::STAB-06: several changes of one event add up; offsets refer to the text before the event | 6 | 3 keeper(s), for example core/state/blockRange.test.js |
| core/state/boundedState.test.js::evicts the least recently set entry once the cap is exceeded | 7 | 5 keeper(s), for example core/state/boundedState.test.js |
| core/state/boundedState.test.js::migration is a no-op without legacy keys and keeps newer map entries over legacy ones | 20 | 5 keeper(s), for example core/state/boundedState.test.js |
| core/state/boundedState.test.js::migration respects the cap | 20 | 5 keeper(s), for example core/state/boundedState.test.js |
| core/state/headingFold.test.js::a heading inside a folded section stays hidden whatever its own fold state | 7 | 1 keeper(s), for example core/state/headingFold.test.js |
| core/state/navigationHistory.test.js::depart without a known line keeps the entry's line and pushes a new document at line 1 | 12 | 5 keeper(s), for example core/state/navigationHistory.test.js |
| core/state/previewTheme.test.js::accepts only complete theme-mode change messages | 16 | 3 keeper(s), for example core/state/previewTheme.test.js |
| core/state/previewTheme.test.js::restores a stored cream theme mode | 4 | 3 keeper(s), for example core/state/previewTheme.test.js |
| core/state/previewTheme.test.js::restores a valid workspace theme mode and ignores invalid stored values | 6 | 3 keeper(s), for example core/state/previewTheme.test.js |
| core/state/previewViewPreferences.test.js::a fresh workspace starts with the toolbar collapsed | 4 | 2 keeper(s), for example core/state/previewViewPreferences.test.js |
| core/state/previewViewPreferences.test.js::read and write go through a Memento-like store | 10 | 3 keeper(s), for example core/state/previewViewPreferences.test.js |
| core/state/previewViewPreferences.test.js::stored choice wins: a stored expanded toolbar stays expanded | 2 | 2 keeper(s), for example core/state/previewViewPreferences.test.js |
| core/state/previewViewPreferences.test.js::zoom is clamped to 70-200 and rounded to 10 | 7 | 2 keeper(s), for example core/state/previewViewPreferences.test.js |
| core/syntax/markdownSyntax.test.js::escapeHtml and escapeRegExp | 7 | 3 keeper(s), for example core/frontmatter/propertiesTable.test.js |
| core/syntax/markdownSyntax.test.js::every consumer reads code fences the same way | 22 | 7 keeper(s), for example core/mapping/labelRename.test.js |
| core/syntax/markdownSyntax.test.js::frontmatterRange returns the lines taken by the front matter | 7 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |

## Tests not judged

Tests whose mutants are all excluded, timed out or not compilable: the run cannot say whether they matter.

| test | reason |
| --- | --- |
| core/comments/anchoring.test.js::T45: a deleted quote orphans the thread and keeps its old line | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: a long unique quote that moved far away is found | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: a quote still inside its lines stays anchored | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: a quote that changed by more than 20 percent is orphaned, not guessed | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: a quote that spans lines is found, and CRLF documents work | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: a short quote is only found inside the +-50 line window | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: a small edit of the quote is followed by the fuzzy search | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: a thread without quote stays where it is while the line exists | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: duplicate quotes are decided by prefix and suffix | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: duplicate quotes without usable context use proximity only inside the window | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: fuzzy search needs a candidate containing the rarest word | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: lines inserted above move the thread to the new line | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: markdown markup does not hide the quote | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: reanchorThreads updates moved threads, keeps orphans untouched and loses nothing | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: the cost stays bounded for a large document and many fuzzy threads | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45: two fuzzy matches far apart are ambiguous and orphan the thread | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45r2: a copy in the old lines that does not fit the context yields to the copy that does | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45r2: a quote that resembles the old lines (60 % of its words, in order) is not orphaned | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45r2: a short quote never re-attaches when the surroundings disagree | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45r2: fuzzy matches must agree on numbers and negations | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45r2: several copies and no context match is no move | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45r2: text that renders differently from its source stays anchored at the original line | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/comments/anchoring.test.js::T45r2: the old lines are checked before the candidate cap | reaches only 22 timeout, 6 compile-error mutant(s) |
| core/protocol/revision.test.js::a revision is any safe integer | reaches only 1 compile-error mutant(s) |
| core/render/chartData.test.js::chartKindOf names the chart of a vega-lite or vega fence and nothing else | reaches only 6 timeout, 10 compile-error mutant(s) |
| core/render/highlight.test.js::leaves an unregistered grammar as plain text | reaches only 17 timeout mutant(s) |
| core/render/highlight.test.js::the palette languages are the bundled grammars and their aliases | reaches only 17 timeout mutant(s) |
| core/render/chartData.test.js::parseDelimited reads quoted fields, CRLF and a byte order mark, and types numbers and booleans | reaches no mutant of the sampled files |

## Holes

Mutants no test of src/core kills (survived or no coverage), labelled by the others phase.

| file | line | mutator | replacement | status | label | killed by |
| --- | --- | --- | --- | --- | --- | --- |
| src/core/comments/commentModel.ts | 55:18 | Regex | /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z\| | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 55:18 | Regex | /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 55:18 | Regex | /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)(?:Z\| | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 55:18 | Regex | /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z | Survived | no test kills it | timed out in another layer (not counted as a kill) |
| src/core/comments/commentModel.ts | 55:18 | Regex | /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 55:18 | Regex | /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 55:18 | Regex | /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 55:18 | Regex | /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z | Survived | no test kills it | timed out in another layer (not counted as a kill) |
| src/core/comments/commentModel.ts | 59:39 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 59:39 | EqualityOperator | value.length < 40 | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 82:17 | MethodExpression | Math.min(documentName.lastIndexOf("/"), documentName.lastInd | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 86:16 | EqualityOperator | dot >= 0 | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 92:17 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 97:17 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 101:17 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 109:17 | StringLiteral | `` | NoCoverage | no test kills it |  |
| src/core/comments/commentModel.ts | 114:17 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 122:17 | StringLiteral | `` | NoCoverage | no test kills it |  |
| src/core/comments/commentModel.ts | 127:17 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 131:17 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 135:73 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 136:18 | MethodExpression | parsed.every(comment => comment === undefined) | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 136:30 | ArrowFunction | () => undefined | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 136:43 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 143:55 | ArrayDeclaration | ["Stryker was here"] | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 144:31 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 145:7 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 145:48 | StringLiteral | "" | NoCoverage | no test kills it |  |
| src/core/comments/commentModel.ts | 147:7 | LogicalOperator | text.length > MAX_SIDECAR_BYTES && new TextEncoder().encode( | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 147:7 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 147:7 | EqualityOperator | text.length >= MAX_SIDECAR_BYTES | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 147:42 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 147:42 | EqualityOperator | new TextEncoder().encode(text).length >= MAX_SIDECAR_BYTES | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 148:20 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 153:11 | BlockStatement | {} | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 154:20 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 156:39 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 157:56 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 158:49 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 159:52 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 160:57 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 165:43 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 168:19 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 216:45 | EqualityOperator | endLine > line | Survived | killed only by another layer | session/reviewReqComments.requirements.test.js::a comment for a document that is not a file is refused with 'save the document first.' |
| src/core/comments/commentModel.ts | 218:38 | EqualityOperator | prefix.length < MAX_CONTEXT_LENGTH | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 219:38 | EqualityOperator | suffix.length < MAX_CONTEXT_LENGTH | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 30:20 | Regex | /THREAD[ \t]*(?:\r?\n\|$)/u | Survived | no test kills it | timed out in another layer (not counted as a kill) |
| src/core/comments/inlineThread.ts | 30:20 | Regex | /^THREAD[ \t]*(?:\r?\n)/u | Survived | no test kills it | timed out in another layer (not counted as a kill) |
| src/core/comments/inlineThread.ts | 31:16 | Regex | /(?: {1,2}\|\t)/u | Survived | no test kills it | timed out in another layer (not counted as a kill) |
| src/core/comments/inlineThread.ts | 57:11 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 57:20 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 66:44 | Regex | /^\n/u | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 66:53 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 66:65 | Regex | /\n$/u | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 66:74 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 80:74 | Regex | /\s/gu | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 81:10 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 81:22 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 81:27 | StringLiteral | "" | NoCoverage | no test kills it |  |
| src/core/comments/inlineThread.ts | 86:16 | MethodExpression | text.replace(/\r\n?/gu, "\n").replace(/-->/gu, "-- >") | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 86:29 | Regex | /\r\n/gu | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 86:40 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 89:34 | Regex | /[ \t]$/u | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 89:46 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 90:16 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 90:28 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 90:33 | StringLiteral | "Stryker was here!" | NoCoverage | no test kills it |  |
| src/core/comments/inlineThread.ts | 112:17 | Regex | /<!--([\s\S]*?)-->$/u | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 120:32 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 120:112 | Regex | /\r/u | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 120:120 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 135:55 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 135:55 | EqualityOperator | text.length >= MAX_THREAD_REPLY_LENGTH | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 137:41 | Regex | /\r/u | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 137:49 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 139:7 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 142:18 | Regex | /[ \t]*/u | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 149:70 | Regex | /[ \t]$/u | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 163:78 | MethodExpression | line | Survived | no test kills it |  |
| src/core/configuration/editorAssociationMigration.ts | 8:40 | StringLiteral | "" | Survived | killed only by another layer | host/openingWatcher.test.js::a Markdown file that opens at a line is replaced by a Studio tab that waits for the line, and the text tab closes |
| src/core/configuration/editorAssociationMigration.ts | 33:44 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/configuration/editorAssociationMigration.ts | 33:44 | LogicalOperator | isRecord(entry) \|\| entry.filenamePattern === MARKDOWN_PATTER | Survived | no test kills it |  |
| src/core/configuration/editorAssociationMigration.ts | 34:10 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/directives/registry.ts | 40:9 | ConditionalExpression | false | Survived | no test kills it | timed out in another layer (not counted as a kill) |
| src/core/directives/registry.ts | 40:48 | BlockStatement | {} | NoCoverage | no test kills it |  |
| src/core/directives/registry.ts | 41:7 | CallExpression | ; | NoCoverage | no test kills it |  |
| src/core/directives/registry.ts | 43:9 | ConditionalExpression | false | Survived | no test kills it | timed out in another layer (not counted as a kill) |
| src/core/edits/textEdit.ts | 32:51 | LogicalOperator | left.start - right.start && left.end - right.end | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 32:79 | ArithmeticOperator | left.end + right.end | NoCoverage | no test kills it |  |
| src/core/edits/textEdit.ts | 36:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 36:9 | LogicalOperator | !Number.isSafeInteger(edit.start) && !Number.isSafeInteger(e | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 72:42 | BlockStatement | {} | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 73:9 | LogicalOperator | (!Number.isSafeInteger(index) \|\| index < 0) && index >= star | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 73:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 73:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 73:9 | LogicalOperator | !Number.isSafeInteger(index) && index < 0 | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 73:41 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 73:54 | EqualityOperator | index > starts.length | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 73:54 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 73:78 | BlockStatement | {} | NoCoverage | no test kills it |  |
| src/core/edits/textEdit.ts | 74:7 | CallExpression | ; | NoCoverage | no test kills it |  |
| src/core/edits/textEdit.ts | 80:7 | CallExpression | ; | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 84:7 | CallExpression | ; | Survived | no test kills it |  |
| src/core/edits/textEdit.ts | 88:7 | CallExpression | ; | Survived | no test kills it |  |
| src/core/export/htmlExport.ts | 50:59 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/export/htmlExport.ts | 50:59 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/export/htmlExport.ts | 50:59 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/export/htmlExport.ts | 50:68 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/export/htmlExport.ts | 50:75 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/export/htmlExport.ts | 50:75 | EqualityOperator | kind !== "3" | Survived | no test kills it |  |
| src/core/export/htmlExport.ts | 50:84 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/export/htmlExport.ts | 66:11 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/export/htmlExport.ts | 75:118 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 45:62 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 47:68 | Regex | /Invalid regular expression: /u | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 47:102 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 47:108 | StringLiteral | "" | NoCoverage | no test kills it |  |
| src/core/find/findMatches.ts | 58:68 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 58:91 | StringLiteral | `` | NoCoverage | no test kills it |  |
| src/core/find/findMatches.ts | 77:27 | Regex | /\$(\$\|&\|<([^>]*)>\|(\d))/gu | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 79:49 | StringLiteral | "Stryker was here!" | NoCoverage | no test kills it |  |
| src/core/find/findMatches.ts | 83:9 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 83:9 | LogicalOperator | index >= match.groups.length \|\| (digits as string).length == | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 83:9 | EqualityOperator | index > match.groups.length | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 83:9 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 83:41 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 84:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 86:36 | StringLiteral | "Stryker was here!" | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 49:7 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 49:7 | BooleanLiteral | annotation.tooltipShowsFields?.length | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 50:8 | BooleanLiteral | annotation.showLineNumber | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 53:55 | Regex | /\uFEFF/u | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 55:43 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 58:35 | ArrayDeclaration | ["Stryker was here"] | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 60:42 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 60:71 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 66:22 | MethodExpression | annotation.idMarker | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 85:11 | BlockStatement | {} | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 92:10 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 92:23 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 98:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 100:9 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 100:9 | EqualityOperator | parent !== current | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 111:8 | MethodExpression | configured | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 111:48 | BooleanLiteral | true | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 112:17 | MethodExpression | configured | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 115:7 | ArrayDeclaration | [] | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 115:21 | LogicalOperator | workspaceRoots[0] && path.dirname(filePath) | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 118:77 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 125:21 | BooleanLiteral | isWithin(candidate, path.resolve(filePath)) | NoCoverage | no test kills it |  |

1139 more row(s): see summary.json.

## Test files left out

None: all 144 test files ran.
