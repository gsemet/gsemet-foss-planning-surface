# Mutation summary

Generated 2026-11-21T14:08:58.348Z. Phases: core, others.

Mutants: 3080 Killed, 1700 CompileError, 729 Survived, 105 NoCoverage, 384 Timeout, 9 Ignored. Tests that ran: 1475.

## Sample

This is a sample: 51 of 162 files of src/core were mutated, so every reading below is "on the sample". Tests that only load sampled modules are not judged: a test is listed as zero-kill or redundant only when its test file is named after a sampled source file of the same sub-folder. Tests left out of the judgement: 11 zero-kill, 722 redundant, 101 reaching no sampled mutant.

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
| comments | 91.1% | 336 | 33 | 2 | 24 | 203 | 0 | 0 | 91.1% |
| configuration | 92.9% | 52 | 4 | 0 | 0 | 32 | 0 | 1 | 94.6% |
| directives | 86.2% | 18 | 2 | 2 | 7 | 13 | 3 | 0 | 86.2% |
| edits | 68.5% | 37 | 14 | 3 | 0 | 16 | 2 | 0 | 68.5% |
| export | 57.1% | 12 | 9 | 0 | 0 | 9 | 0 | 0 | 57.1% |
| find | 78.6% | 50 | 11 | 4 | 5 | 27 | 0 | 0 | 78.6% |
| frontmatter | 73.8% | 445 | 129 | 36 | 19 | 328 | 2 | 2 | 74.1% |
| mapping | 93.4% | 328 | 24 | 0 | 14 | 62 | 0 | 0 | 93.4% |
| myst | 84.0% | 64 | 13 | 0 | 4 | 52 | 0 | 0 | 84.0% |
| navigation | 95.0% | 237 | 13 | 0 | 8 | 101 | 0 | 0 | 95.0% |
| palette | 3.3% | 2 | 58 | 0 | 0 | 12 | 0 | 17 | 31.7% |
| paste | 58.5% | 445 | 275 | 41 | 1 | 237 | 0 | 0 | 58.5% |
| preview | 84.7% | 220 | 42 | 0 | 13 | 111 | 0 | 1 | 85.1% |
| protocol | 98.9% | 185 | 2 | 0 | 0 | 134 | 1 | 0 | 98.9% |
| render | 85.7% | 202 | 34 | 8 | 49 | 161 | 0 | 1 | 86.0% |
| scroll | 78.2% | 164 | 44 | 2 | 1 | 43 | 0 | 0 | 78.2% |
| security | 97.8% | 64 | 2 | 4 | 197 | 25 | 0 | 0 | 97.8% |
| state | 90.9% | 205 | 18 | 3 | 4 | 123 | 1 | 6 | 93.5% |
| syntax | 96.3% | 14 | 2 | 0 | 38 | 11 | 0 | 0 | 96.3% |

## Score per SwRS

Share of the mutants reached by the tests of the SwRS that those tests kill (a test can carry several IDs, so the shares overlap).

| SwRS | tests | mutants reached | killed | score |
| --- | --- | --- | --- | --- |
| StRS-MDOKFSTUDIO-CORE-006 | 1 | 574 | 356 | 62.0% |
| StRS-MDOKFSTUDIO-FMSCHEMA-001 | 1 | 68 | 38 | 55.9% |
| SwRS-MDOKFSTUDIO-BLOCK-003 | 1 | 132 | 74 | 56.1% |
| SwRS-MDOKFSTUDIO-BLOCK-014 | 2 | 372 | 331 | 89.0% |
| SwRS-MDOKFSTUDIO-BLOCK-017 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-042 | 5 | 223 | 176 | 78.9% |
| SwRS-MDOKFSTUDIO-BLOCK-087 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-094 | 4 | 65 | 47 | 72.3% |
| SwRS-MDOKFSTUDIO-BLOCK-109 | 4 | 96 | 42 | 43.8% |
| SwRS-MDOKFSTUDIO-BLOCK-117 | 3 | 121 | 84 | 69.4% |
| SwRS-MDOKFSTUDIO-BLOCK-124 | 2 | 44 | 38 | 86.4% |
| SwRS-MDOKFSTUDIO-BLOCK-127 | 2 | 96 | 70 | 72.9% |
| SwRS-MDOKFSTUDIO-BLOCK-156 | 1 | 44 | 38 | 86.4% |
| SwRS-MDOKFSTUDIO-BLOCK-166 | 2 | 121 | 77 | 63.6% |
| SwRS-MDOKFSTUDIO-BLOCK-169 | 1 | 44 | 38 | 86.4% |
| SwRS-MDOKFSTUDIO-BLOCK-174 | 1 | 44 | 38 | 86.4% |
| SwRS-MDOKFSTUDIO-BLOCK-191 | 2 | 11 | 8 | 72.7% |
| SwRS-MDOKFSTUDIO-BLOCK-193 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-205 | 1 | 16 | 10 | 62.5% |
| SwRS-MDOKFSTUDIO-BLOCK-234 | 9 | 216 | 113 | 52.3% |
| SwRS-MDOKFSTUDIO-BLOCK-256 | 1 | 44 | 38 | 86.4% |
| SwRS-MDOKFSTUDIO-BLOCK-257 | 4 | 93 | 61 | 65.6% |
| SwRS-MDOKFSTUDIO-BLOCK-259 | 7 | 120 | 55 | 45.8% |
| SwRS-MDOKFSTUDIO-BLOCK-260 | 5 | 331 | 302 | 91.2% |
| SwRS-MDOKFSTUDIO-BLOCK-262 | 4 | 93 | 61 | 65.6% |
| SwRS-MDOKFSTUDIO-BLOCK-263 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-265 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-266 | 11 | 421 | 351 | 83.4% |
| SwRS-MDOKFSTUDIO-BLOCK-268 | 6 | 123 | 63 | 51.2% |
| SwRS-MDOKFSTUDIO-BLOCK-269 | 5 | 123 | 63 | 51.2% |
| SwRS-MDOKFSTUDIO-CODE-001 | 9 | 448 | 345 | 77.0% |
| SwRS-MDOKFSTUDIO-CODE-007 | 2 | 94 | 61 | 64.9% |
| SwRS-MDOKFSTUDIO-CODE-008 | 2 | 96 | 61 | 63.5% |
| SwRS-MDOKFSTUDIO-CODE-014 | 2 | 454 | 330 | 72.7% |
| SwRS-MDOKFSTUDIO-CODE-019 | 1 | 96 | 42 | 43.8% |
| SwRS-MDOKFSTUDIO-CODE-039 | 8 | 502 | 342 | 68.1% |
| SwRS-MDOKFSTUDIO-CODE-040 | 5 | 404 | 334 | 82.7% |
| SwRS-MDOKFSTUDIO-CORE-001 | 3 | 330 | 284 | 86.1% |
| SwRS-MDOKFSTUDIO-CORE-003 | 8 | 503 | 340 | 67.6% |
| SwRS-MDOKFSTUDIO-CORE-008 | 2 | 93 | 61 | 65.6% |
| SwRS-MDOKFSTUDIO-CORE-010 | 3 | 495 | 342 | 69.1% |
| SwRS-MDOKFSTUDIO-CORE-012 | 5 | 410 | 340 | 82.9% |
| SwRS-MDOKFSTUDIO-CORE-013 | 5 | 429 | 347 | 80.9% |
| SwRS-MDOKFSTUDIO-CORE-022 | 6 | 490 | 351 | 71.6% |
| SwRS-MDOKFSTUDIO-CORE-025 | 1 | 318 | 284 | 89.3% |
| SwRS-MDOKFSTUDIO-CORE-028 | 6 | 331 | 284 | 85.8% |
| SwRS-MDOKFSTUDIO-CORE-034 | 3 | 330 | 284 | 86.1% |
| SwRS-MDOKFSTUDIO-CORE-050 | 3 | 93 | 62 | 66.7% |
| SwRS-MDOKFSTUDIO-CORE-071 | 10 | 505 | 327 | 64.8% |
| SwRS-MDOKFSTUDIO-CORE-072 | 12 | 377 | 335 | 88.9% |
| SwRS-MDOKFSTUDIO-CORE-073 | 4 | 574 | 405 | 70.6% |
| SwRS-MDOKFSTUDIO-CORE-079 | 20 | 428 | 353 | 82.5% |
| SwRS-MDOKFSTUDIO-CORE-088 | 2 | 526 | 344 | 65.4% |
| SwRS-MDOKFSTUDIO-CORE-089 | 3 | 93 | 61 | 65.6% |
| SwRS-MDOKFSTUDIO-DIAG-001 | 3 | 593 | 407 | 68.6% |
| SwRS-MDOKFSTUDIO-DIAG-005 | 1 | 93 | 61 | 65.6% |
| SwRS-MDOKFSTUDIO-DIAG-017 | 2 | 470 | 345 | 73.4% |
| SwRS-MDOKFSTUDIO-DIAG-023 | 2 | 459 | 335 | 73.0% |
| SwRS-MDOKFSTUDIO-DIAG-024 | 4 | 433 | 345 | 79.7% |
| SwRS-MDOKFSTUDIO-DIAG-032 | 1 | 93 | 61 | 65.6% |
| SwRS-MDOKFSTUDIO-DIAG-050 | 2 | 96 | 42 | 43.8% |
| SwRS-MDOKFSTUDIO-DIAG-054 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-DIAG-068 | 3 | 435 | 351 | 80.7% |
| SwRS-MDOKFSTUDIO-DIAG-084 | 10 | 3 | 2 | 66.7% |
| SwRS-MDOKFSTUDIO-DIAG-089 | 4 | 393 | 335 | 85.2% |
| SwRS-MDOKFSTUDIO-DIAG-097 | 4 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-DIAG-105 | 4 | 522 | 377 | 72.2% |
| SwRS-MDOKFSTUDIO-DIAG-121 | 5 | 460 | 357 | 77.6% |
| SwRS-MDOKFSTUDIO-DIAG-122 | 9 | 452 | 360 | 79.6% |
| SwRS-MDOKFSTUDIO-DIAG-124 | 1 | 565 | 405 | 71.7% |
| SwRS-MDOKFSTUDIO-DIAG-125 | 14 | 444 | 345 | 77.7% |
| SwRS-MDOKFSTUDIO-DIAG-126 | 1 | 330 | 284 | 86.1% |
| SwRS-MDOKFSTUDIO-FMEDIT-004 | 1 | 92 | 38 | 41.3% |
| SwRS-MDOKFSTUDIO-FMEDIT-010 | 3 | 274 | 125 | 45.6% |
| SwRS-MDOKFSTUDIO-FMEDIT-016 | 4 | 171 | 63 | 36.8% |
| SwRS-MDOKFSTUDIO-FMEDIT-024 | 3 | 92 | 57 | 62.0% |
| SwRS-MDOKFSTUDIO-FMEDIT-029 | 3 | 92 | 57 | 62.0% |
| SwRS-MDOKFSTUDIO-FMEDIT-043 | 8 | 207 | 116 | 56.0% |
| SwRS-MDOKFSTUDIO-FMEDIT-067 | 3 | 125 | 53 | 42.4% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-001 | 2 | 383 | 306 | 79.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-004 | 1 | 48 | 38 | 79.2% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-005 | 4 | 129 | 85 | 65.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-006 | 5 | 53 | 41 | 77.4% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-014 | 2 | 71 | 48 | 67.6% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-023 | 2 | 107 | 43 | 40.2% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-029 | 1 | 53 | 38 | 71.7% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-039 | 2 | 65 | 38 | 58.5% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-046 | 10 | 230 | 131 | 57.0% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-050 | 3 | 181 | 83 | 45.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-055 | 6 | 211 | 114 | 54.0% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-063 | 1 | 53 | 38 | 71.7% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-067 | 6 | 489 | 360 | 73.6% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-084 | 5 | 92 | 71 | 77.2% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-090 | 1 | 53 | 38 | 71.7% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-091 | 3 | 137 | 72 | 52.6% |
| SwRS-MDOKFSTUDIO-GFM-001 | 4 | 358 | 324 | 90.5% |
| SwRS-MDOKFSTUDIO-GFM-008 | 3 | 465 | 352 | 75.7% |
| SwRS-MDOKFSTUDIO-GFM-009 | 38 | 508 | 357 | 70.3% |
| SwRS-MDOKFSTUDIO-GFM-016 | 2 | 331 | 302 | 91.2% |
| SwRS-MDOKFSTUDIO-GFM-021 | 2 | 192 | 93 | 48.4% |
| SwRS-MDOKFSTUDIO-GFM-031 | 2 | 440 | 327 | 74.3% |
| SwRS-MDOKFSTUDIO-GFM-034 | 6 | 500 | 386 | 77.2% |
| SwRS-MDOKFSTUDIO-GFM-040 | 11 | 459 | 417 | 90.8% |
| SwRS-MDOKFSTUDIO-GFM-041 | 8 | 124 | 82 | 66.1% |
| SwRS-MDOKFSTUDIO-LAYOUT-001 | 1 | 93 | 61 | 65.6% |
| SwRS-MDOKFSTUDIO-LAYOUT-002 | 4 | 99 | 67 | 67.7% |
| SwRS-MDOKFSTUDIO-LAYOUT-007 | 1 | 93 | 61 | 65.6% |
| SwRS-MDOKFSTUDIO-LAYOUT-022 | 2 | 93 | 61 | 65.6% |
| SwRS-MDOKFSTUDIO-LAYOUT-023 | 1 | 93 | 61 | 65.6% |
| SwRS-MDOKFSTUDIO-LAYOUT-032 | 2 | 93 | 61 | 65.6% |
| SwRS-MDOKFSTUDIO-LIFE-004 | 2 | 355 | 288 | 81.1% |
| SwRS-MDOKFSTUDIO-LIFE-026 | 1 | 10 | 10 | 100.0% |
| SwRS-MDOKFSTUDIO-LIFE-032 | 1 | 109 | 49 | 45.0% |
| SwRS-MDOKFSTUDIO-LIFE-039 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-044 | 1 | 1 | 0 | 0.0% |
| SwRS-MDOKFSTUDIO-LIFE-049 | 1 | 93 | 61 | 65.6% |
| SwRS-MDOKFSTUDIO-LIFE-069 | 3 | 523 | 384 | 73.4% |
| SwRS-MDOKFSTUDIO-LIFE-071 | 1 | 536 | 403 | 75.2% |
| SwRS-MDOKFSTUDIO-LIFE-094 | 9 | 61 | 59 | 96.7% |
| SwRS-MDOKFSTUDIO-LIFE-100 | 1 | 28 | 23 | 82.1% |
| SwRS-MDOKFSTUDIO-LIFE-108 | 1 | 96 | 42 | 43.8% |
| SwRS-MDOKFSTUDIO-LIFE-119 | 3 | 157 | 103 | 65.6% |
| SwRS-MDOKFSTUDIO-LIFE-125 | 1 | 18 | 10 | 55.6% |
| SwRS-MDOKFSTUDIO-LIFE-127 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-149 | 1 | 1 | 0 | 0.0% |
| SwRS-MDOKFSTUDIO-LIFE-156 | 1 | 1 | 0 | 0.0% |
| SwRS-MDOKFSTUDIO-LIFE-169 | 5 | 131 | 67 | 51.1% |
| SwRS-MDOKFSTUDIO-LIFE-170 | 3 | 33 | 13 | 39.4% |
| SwRS-MDOKFSTUDIO-LIFE-173 | 2 | 134 | 63 | 47.0% |
| SwRS-MDOKFSTUDIO-LIFE-174 | 1 | 1 | 0 | 0.0% |
| SwRS-MDOKFSTUDIO-LIFE-175 | 4 | 41 | 37 | 90.2% |
| SwRS-MDOKFSTUDIO-LIFE-178 | 2 | 427 | 342 | 80.1% |
| SwRS-MDOKFSTUDIO-LIFE-181 | 1 | 43 | 25 | 58.1% |
| SwRS-MDOKFSTUDIO-LIFE-183 | 5 | 21 | 21 | 100.0% |
| SwRS-MDOKFSTUDIO-LIFE-184 | 9 | 20 | 20 | 100.0% |
| SwRS-MDOKFSTUDIO-MYST-001 | 11 | 496 | 362 | 73.0% |
| SwRS-MDOKFSTUDIO-MYST-006 | 3 | 498 | 354 | 71.1% |
| SwRS-MDOKFSTUDIO-MYST-013 | 5 | 480 | 352 | 73.3% |
| SwRS-MDOKFSTUDIO-MYST-017 | 3 | 474 | 328 | 69.2% |
| SwRS-MDOKFSTUDIO-MYST-019 | 5 | 466 | 351 | 75.3% |
| SwRS-MDOKFSTUDIO-MYST-024 | 8 | 436 | 320 | 73.4% |
| SwRS-MDOKFSTUDIO-MYST-031 | 3 | 465 | 342 | 73.5% |
| SwRS-MDOKFSTUDIO-MYST-036 | 1 | 442 | 327 | 74.0% |
| SwRS-MDOKFSTUDIO-MYST-038 | 3 | 108 | 51 | 47.2% |
| SwRS-MDOKFSTUDIO-MYST-045 | 5 | 216 | 125 | 57.9% |
| SwRS-MDOKFSTUDIO-MYST-053 | 4 | 371 | 330 | 88.9% |
| SwRS-MDOKFSTUDIO-MYST-057 | 7 | 362 | 308 | 85.1% |
| SwRS-MDOKFSTUDIO-MYST-063 | 5 | 474 | 351 | 74.1% |
| SwRS-MDOKFSTUDIO-MYST-066 | 12 | 79 | 49 | 62.0% |
| SwRS-MDOKFSTUDIO-MYST-072 | 2 | 458 | 358 | 78.2% |

85 more row(s): see summary.json.

## Tests that kill nothing

Tests that reach killable mutants and kill none of them (zero-kill candidates).

| test | mutants reached |
| --- | --- |
| core/comments/commentModel.holes.test.js::a valid sidecar returns its document name and every thread | 88 Killed, 105 CompileError, 8 Survived |
| core/configuration/editingConfiguration.test.js::a fresh workspace starts the palette in GFM | 2 CompileError, 1 Killed |
| core/configuration/editingConfiguration.test.js::stored choice wins: a stored palette mode is kept over the default and the setting | 2 CompileError, 1 Killed |
| core/configuration/plantUmlConfiguration.test.js::uses an empty path for non-string configuration values | 4 CompileError, 3 Killed |
| core/mapping/sourceMapping.holes.test.js::every kind of line ending counts as one break | 34 Killed, 2 CompileError, 1 Survived |
| core/myst/confLocator.test.js::myst_nb counts like myst_parser | 37 Killed, 41 CompileError, 9 Survived, 3 Timeout |
| core/navigation/openingPolicy.test.js::rule 9: a plain opening, or a jump with the setting off, stays a text editor | 17 CompileError, 16 Killed |
| core/protocol/hostToPage.holes.test.js::a value that is not an object is never a host message | 17 Killed, 46 CompileError, 1 Survived |
| core/render/blockTagTitle.test.js::text that is not an opening tag has no title | 4 CompileError, 10 Timeout, 1 Killed |
| core/render/chartData.test.js::inlineChartFiles puts the rows of each read file into values and leaves no url | 1 CompileError, 2 Survived, 3 Killed |
| core/state/navigationHistory.holes.test.js::the oldest place goes only when the cap is passed, never at exactly the cap | 20 Killed, 7 CompileError, 1 Survived |
| core/state/previewTheme.test.js::a fresh workspace has no stored mode and the built-in default is cream | 9 CompileError, 13 Killed, 1 Survived |
| core/syntax/markdownSyntax.test.js::advanceFence tracks one fence at a time, with colon fences on request | 13 Killed, 76 Timeout, 9 CompileError, 1 Survived |

## Redundant tests (greedy set)

A keeper set of 286 test(s) kills every killed mutant; the others below add nothing the keepers do not kill. Two duplicate tests are never both listed: one of them is a keeper.

| redundant test | killed mutants | also killed by keepers |
| --- | --- | --- |
| core/comments/commentModel.test.js::T42: a valid file parses into threads | 45 | 8 keeper(s), for example core/comments/commentEditing.test.js |
| core/comments/commentModel.test.js::T42: serialization is stable: fixed key order, 2 spaces, trailing newline | 51 | 8 keeper(s), for example core/comments/commentEditing.test.js |
| core/comments/inlineThread.test.js::a reply goes above the closing marker and nothing else changes | 54 | 10 keeper(s), for example core/edits/sourceEdits.test.js |
| core/comments/inlineThread.test.js::blank lines inside a message are kept, and a tab indent is accepted | 20 | 9 keeper(s), for example core/edits/sourceEdits.test.js |
| core/directives/registry.test.js::each directive name has one plug-in, found by its exact name | 1 | 4 keeper(s), for example core/render/mystFeatures.test.js |
| core/directives/registry.test.js::the figure pass puts the source lines on the figure; the table pass marks a list-table | 2 | 5 keeper(s), for example core/render/mystFeatures.test.js |
| core/edits/textEdit.test.js::source lines split on LF, CRLF and CR, and a final line break adds an empty last line | 10 | 1 keeper(s), for example core/edits/sourceEdits.test.js |
| core/export/htmlExport.test.js::a THREAD chip with its popover, a TODO chip, source-mapping attributes and the tabindex of mapped blocks are left out | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::a front matter value and a key under their editors are exported shown, without the editor | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::a local image becomes a data URI and an unreadable one is counted and loses its source | 4 | 3 keeper(s), for example core/export/htmlExport.test.js |
| core/export/htmlExport.test.js::a mailto link is kept and a file: link, an invalid anchor and a query-only link are unwrapped and reported | 15 | 8 keeper(s), for example core/export/htmlExport.test.js |
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
| core/frontmatter/sameData.holes.test.js::isSameData matches the members of a set or the keys of a map whatever their order, using each match once | 33 | 1 keeper(s), for example core/frontmatter/sameData.holes.test.js |
| core/frontmatter/sameData.test.js::isSameData compares key lists in order, as the patch verification needs | 22 | 2 keeper(s), for example core/frontmatter/frontmatterPreservation.test.js |
| core/frontmatter/schemaValidator.test.js::validator cache returns the same compiled function for a schema object | 1 | 40 keeper(s), for example core/edits/sourceEdits.test.js |
| core/frontmatter/stemIndex.holes.test.js::a root that is gone is indexed as empty, and indexed again once it exists | 3 | 1 keeper(s), for example core/frontmatter/stemIndex.holes.test.js |
| core/mapping/blankRuns.test.js::CR LF and lone CR line endings give the same runs | 12 | 40 keeper(s), for example core/edits/sourceEdits.test.js |
| core/mapping/blankRuns.test.js::a CommonMark blank line holds only spaces and tabs | 1 | 40 keeper(s), for example core/edits/sourceEdits.test.js |
| core/mapping/blankRuns.test.js::one blank line is the separator, two or more are a run | 14 | 40 keeper(s), for example core/edits/sourceEdits.test.js |
| core/mapping/blankRuns.test.js::spaces and tabs are blank, a no-break space is not | 14 | 40 keeper(s), for example core/edits/sourceEdits.test.js |
| core/mapping/blankRuns.test.js::the frontmatter is not part of a run, and the lines after it can be | 12 | 40 keeper(s), for example core/edits/sourceEdits.test.js |
| core/mapping/imageReference.test.js::relativeImageReference accepts Windows separators and refuses another drive | 7 | 2 keeper(s), for example core/mapping/dropReferences.test.js |
| core/mapping/imageReference.test.js::relativeImageReference gives a POSIX path relative to the document folder | 4 | 2 keeper(s), for example core/mapping/dropReferences.test.js |
| core/mapping/labelRename.test.js::the renderer, the page and the host share one label name pattern | 6 | 5 keeper(s), for example core/mapping/labelRename.test.js |
| core/mapping/pastedImage.holes.test.js::sniffImage accepts input exactly as long as the signature and refuses one byte less | 1 | 1 keeper(s), for example core/mapping/pastedImage.holes.test.js |
| core/mapping/pastedImage.test.js::isBase64 accepts the base64 alphabet only | 9 | 1 keeper(s), for example core/protocol/pageToHost.test.js |
| core/mapping/pastedImage.test.js::nextImageName gives up after 1000 suffixes | 9 | 1 keeper(s), for example core/mapping/pastedImage.test.js |
| core/mapping/textDiff.holes.test.js::a CRLF pair is kept whole when only one of the two texts holds it, at the start or the end of the change | 44 | 1 keeper(s), for example core/mapping/textDiff.holes.test.js |
| core/mapping/textDiff.holes.test.js::a surrogate pair is kept whole when only one of the two texts holds it | 7 | 1 keeper(s), for example core/mapping/textDiff.holes.test.js |
| core/mapping/textDiff.test.js::identical input yields an empty replacement | 7 | 3 keeper(s), for example core/edits/sourceEdits.test.js |
| core/mapping/textDiff.test.js::insertion at the start and at the end | 20 | 3 keeper(s), for example core/edits/sourceEdits.test.js |
| core/mapping/textDiff.test.js::insertion, deletion and replacement in the middle | 22 | 3 keeper(s), for example core/edits/sourceEdits.test.js |
| core/mapping/textDiff.test.js::repeated characters do not let prefix and suffix overlap | 5 | 3 keeper(s), for example core/edits/sourceEdits.test.js |
| core/myst/confLocator.holes.test.js::a conf.py that cannot be read gives no set, and does not stop other lookups | 4 | 2 keeper(s), for example core/render/renderPipeline.test.js |
| core/myst/confLocator.test.js::D29: a single conf.py in a common folder of the root is the fallback | 24 | 8 keeper(s), for example core/myst/confLocator.test.js |
| core/myst/confLocator.test.js::D29: an ancestor conf.py wins over a fallback, and invalidation covers the fallback | 36 | 8 keeper(s), for example core/myst/confLocator.test.js |
| core/myst/confLocator.test.js::the nearest conf.py wins and the enabled set comes from it | 15 | 7 keeper(s), for example core/render/renderPipeline.test.js |
| core/navigation/openingPolicy.test.js::rule 7: with Open Markdown files in Studio on, a jump opens Studio at the line and a plain opening opens Studio | 7 | 5 keeper(s), for example core/navigation/openingPolicy.test.js |
| core/navigation/openingPolicy.test.js::rule 8: with Open search results in Studio on, a jump opens Studio at the line | 5 | 5 keeper(s), for example core/navigation/openingPolicy.test.js |
| core/navigation/previewNavigation.test.js::a link path is decoded once: a literal percent is reachable, an escaped percent is not decoded again | 7 | 5 keeper(s), for example core/export/htmlExport.test.js |
| core/navigation/previewNavigation.test.js::marker navigation selects exact marker identities | 11 | 2 keeper(s), for example core/frontmatter/fileLinks.test.js |
| core/paste/htmlToMarkdown.test.js::T1: htmlToMarkdown, VS Code copy: one line stays plain text | 11 | 10 keeper(s), for example core/paste/htmlToMarkdown.test.js |
| core/paste/htmlToMarkdown.test.js::T1: htmlToMarkdown, VS Code copy: several lines stay raw text, never wrapped in a fence | 24 | 10 keeper(s), for example core/paste/htmlToMarkdown.test.js |
| core/preview/contentPatch.test.js::T08: two renders with different zoom have the same shell key and the same context key | 62 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/preview/contentPatch.test.js::T17: the shell key is equal whatever the incoming-changes preference, and the Diff button is in both | 64 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/preview/contentPatch.test.js::T34: content that mentions a container inside the content does not change the extracted content | 34 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/preview/contentPatch.test.js::T34: extractMainContent returns the inner HTML of the content container of a real page | 35 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/preview/contentPatch.test.js::T34: injecting PlantUML diagrams into a page keeps its shell key, so the diagrams can be patched in | 47 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/preview/contentPatch.test.js::T34: reuseNonce swaps every occurrence, in the policy tokens and in the attributes | 8 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/preview/contentPatch.test.js::T34: shell keys differ when Mermaid appears or disappears, and when math appears | 67 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/preview/contentPatch.test.js::T34: two renders of one document type have equal shell keys despite other text, nonces and identifiers | 64 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/preview/contentPatch.test.js::the page script is injected verbatim even when it contains replacement patterns | 5 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/preview/previewStyles.test.js::MyST simple and no-icon admonition modifiers are styled | 3 | 5 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/previewStyles.test.js::Sphinx version admonitions use success, warning, and danger accents | 3 | 5 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/previewStyles.test.js::caution callouts are red with the octagon icon, not the warning amber | 3 | 5 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/previewStyles.test.js::dropdown admonitions show their open or closed state with a chevron | 3 | 5 keeper(s), for example core/render/mystFeatures.test.js |
| core/preview/previewStyles.test.js::every admonition flavour gets an accent colour | 3 | 5 keeper(s), for example core/render/mystFeatures.test.js |
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
| core/render/radioGroups.test.js::a group without a selection and a group with two selections render as written | 41 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/render/radioGroups.test.js::a lone radio item stays plain text | 7 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/render/radioGroups.test.js::in a list that mixes task items and options, and in a nested group, the option items and paragraphs are out of the Tab order | 59 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/render/radioGroups.test.js::radio markers stay literal in code and keep exact columns in quotes, CRLF files and after frontmatter | 42 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/render/radioGroups.test.js::the marker is ( ), (x) or (X) followed by a space or a tab, at the start of a list item | 46 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
| core/render/radioGroups.test.js::the webview sanitizer keeps the radio roles, states and source attributes | 49 | 42 keeper(s), for example core/edits/sourceEdits.test.js |
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
| core/comments/commentEditing.test.js::S-04: a comments file that is a symbolic link is refused and its target is never written | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/comments/commentEditing.test.js::T43: ids are a prefix and 8 hex characters | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/comments/commentEditing.test.js::T43: resolveAuthor uses the setting, then Git, then the OS user, then Anonymous | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/commentsConfiguration.test.js::T43: a non-string author name falls back to the empty default | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/editingConfiguration.test.js::falls back to GFM for an unknown or non-string palette mode | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/frontmatterConfiguration.test.js::frontmatter visibility and strict validation can be configured independently | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/previewConfiguration.test.js::comment chips are shown by default and can be turned off | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/previewConfiguration.test.js::incremental updates can be turned off and default to on | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/previewConfiguration.test.js::normalizes preview content width and reserves zero for unlimited | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/previewConfiguration.test.js::normalizes sticky heading depth to one through six levels | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/previewConfiguration.test.js::the content width setting is rounded to whole pixels and a negative value gives the default | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/settingsRegistry.test.js::a setting with nothing stored reads as its schema default | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/settingsRegistry.test.js::categories keep their titles and order, and settings are sorted by their order | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/settingsRegistry.test.js::the Opening Files settings are two booleans: the search results one on by default, the every-file one off | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/settingsRegistry.test.js::the Studio settings live under their own prefix, and no source writes a setting of the built-in Markdown preview | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/settingsRegistry.test.js::the generated settings schema is the package.json one, byte for byte | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/configuration/settingsRegistry.test.js::the page gets the scroll, reveal, sticky band and comment chip settings in its boot context | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/export/htmlExport.test.js::the snapshot guard accepts the page shape and refuses a malformed one | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/frontmatter/stemIndex.holes.test.js::a symbolic link to a Markdown file is indexed under its own stem | reaches only 7 timeout, 1 compile-error mutant(s) |
| core/mapping/dropReferences.test.js::droppedFilePath reads local file addresses only | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/mapping/dropReferences.test.js::firstHeadingTitle reads the first heading outside front matter and code | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/mapping/mystTargets.test.js::bibKeys reads entry keys and titles, and skips comment, string and preamble entries | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/mapping/mystTargets.test.js::collectBibKeys merges files, removes duplicates, sorts and caps | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/mapping/mystTargets.test.js::docReference gives a POSIX path relative to the document, without the extension | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/mapping/textDiff.test.js::replacement reproduces the target for 200 seeded random pairs | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/palette/paletteActions.test.js::a popover descriptor carries what its popover shows | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/palette/paletteActions.test.js::every descriptor names a known icon, mode and scope, and every icon is used by an action or a slash variant | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/palette/paletteActions.test.js::the registry lists every palette action once, in display order | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/palette/paletteActions.test.js::the two chart actions are listed for Full only, in the Full group, with the chart slash names | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/paste/paletteReq.requirements.test.js::in forced-colours mode the slash menu uses Canvas and the lit command Highlight | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/codeBlockStyles.test.js::code blocks are Dark+ editor surfaces unless the dark background setting is off | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/codeBlockStyles.test.js::code text and line numbers keep WCAG AA contrast on the dark background; light tokens on the cream page | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/codeBlockStyles.test.js::line numbers are generated content gated by the setting, and MyST options are not gated | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/codeBlockStyles.test.js::with the dark background off the Light+ colours apply in the light themes and light VS Code themes | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/commentContrast.test.js::comment thread text reaches WCAG AA 4.5:1 on its surface in every theme mode | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/commentContrast.test.js::the comment popover and boxes never dim their text with opacity | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/creamTheme.test.js::cream defines a light warm palette for every variable white mode overrides | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/creamTheme.test.js::cream mirrors the white-mode code colouring | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/creamTheme.test.js::cream text and background pairs meet WCAG AA 4.5:1 | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/creamTheme.test.js::explicit themes override the same host colors, including the floating toolbar | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/creamTheme.test.js::toolbar theme icons are well-formed sibling svgs, one per mode | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/diagReq.styles.requirements.test.js::a PlantUML message uses the theme error colour with a red fallback, in italics | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/diagReq.styles.requirements.test.js::a PlantUML picture is a block centred with automatic inline margins | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/diagReq.styles.requirements.test.js::a PlantUML picture is scaled down to the column and never set to a fixed width | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/diagReq.styles.requirements.test.js::the PlantUML source disclosure has the rules of the Mermaid one | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/diagReq.styles.requirements.test.js::the sticky heading band takes the page colours of the forced mode | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/gridCardEditStyles.test.js::a grid row with an open block editor lets its tracks grow to the minimum width of the card being edited | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/gridCardEditStyles.test.js::in a card the palette stays in the flow above the text box with a maximum height and a vertical scroll | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/gridCardEditStyles.test.js::the card being edited is not clipped, so the palette may leave it | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/gridCardEditStyles.test.js::the text box of a block editor in a card keeps a readable minimum width | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/inlineCode.test.js::inline code is a subtle tinted pill derived from the text colour | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/inlineCode.test.js::inline code scales with its context and wraps without growing the line | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/inlineCode.test.js::inline code stays compact in table cells | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/inlineCode.test.js::inline code text keeps 4.5:1 on the tinted background in every forced mode | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/layoutThemeStyles.test.js::a table is centred through automatic inline margins and a figure paragraph is centred, in every width mode | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/layoutThemeStyles.test.js::no rule of the page palette is keyed to a host theme kind, so the host variables rule in high contrast too | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/layoutThemeStyles.test.js::the toolbar does not scale with the zoom: no toolbar rule reads the zoom variables | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/listItemHandleStyles.test.js::a block with no room on its left is pushed right by a handle's width, without a max-content width | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/listItemHandleStyles.test.js::every list item handle rule is scoped to edit mode | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/listItemHandleStyles.test.js::the dragged item is dimmed and the drop lines use the theme focus colour | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/listItemHandleStyles.test.js::the list handle layer sits at the page origin and each handle ends left of its column, on its line | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 034: a narrow pane keeps the palette sticky; it wraps inside the pane instead of leaving the flow | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 034: the table toolbar rides down with a scrolling table by a transform, not by layout | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 046: the motion layer is short and never animates layout or the table bar's transform | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 107: the preview block quote background outranks the VS Code webview default rule | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 112: a horizontal rule is 12px taller above and below than its line, with the spacing unchanged | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 112: the edit bar buttons share the floating toolbar's tooltip bubble and slide it in on hover | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 123: the frame reserves the distance the sticky palette rides down, as a top margin | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 143: the chevron shows on hover, focus and while folded, and a folded block drops its spacing | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 143: the toolbar has a Fold button, off until a section is folded | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 162: every tooltip bubble slides in from the left with one shared animation | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 162: reduced motion turns off the tooltip slide-in and the toolbar rows unroll | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 162: the toolbar rows unroll as one block, only under the animating mark | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR 168: the table toolbar paints above the row and column handle layer | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR147: the side-by-side cards are two columns, switch off with the page attribute and never show in edit mode | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::CR147: the toolbar offers a Side-by-side button in the review row after the Table of contents button, not pressed at first | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::K1: long words and bare URLs wrap inside text blocks, links and table cells | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::Mermaid diagrams keep SVG images contained and source inspectable | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::MyST numbered and emphasized code lines are styled | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::MyST table alignment and notebook output placeholders are styled | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::P11: the slash menu floats above the toolbar and the palette popovers and is placed by the runtime | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::P4: the palette sits on top of the frame and sticks below the sticky band and the toolbar | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::P4: the palette stays in the flow in short panes and when the runtime says it is too tall | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::P7: full width uses the 16 px gutter a broken-out table keeps in auto | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::README HTML: align, per-theme picture images and the edit-mode frame titled with the tag | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::T08: zoom scales the content font size and the column width together | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::T10: full width lifts the column limit and auto lets flagged elements break out | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::T10: the auto measure lifts every cap, the row-handle one included | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::T15: an open comment is an admonition-like box and showComments off hides the gray chips only | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::T16: the change bars sit in one column of a layer, square, with no layout shift | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::T16b: only the current TOC entry loses its rounded corners | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::T21: the edition palette is a wrapping pill bar with an in-frame popover and no inline style | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::T28: insertion points are zero-height, hover-revealed gutter buttons | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::T43: the pending overlay is fixed, pointer-transparent and never in flow | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::T44: the Orphaned comments box sits in the content's bottom padding and adds no scroll height | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::a block quote is tinted with the theme block quote background | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::a captioned code block is left-aligned with its caption as a title bar on top | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::a narrow pane with the TOC on pads the content for the 16px rail and keeps the overlay under the toolbar tooltip | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::a narrow pane with the TOC on shows a rail and opens the column as an overlay | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::active paragraph editors share the rendered paragraph spacing | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::active toolbar toggles do not show a redundant focus ring | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::an inline thread is a green chip with a bubble, a green titled box, and goes with the gray chips | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::block editing grows without internal scrolling and is framed | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::code blocks use one font scale, one box, and scroll a long line only when it does not fit | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::comments hidden by the button or the setting: highlights lose their paint, badges and the orphan box go | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::content table cells keep a 5em minimum width in the rendered view, the properties table keeps its own | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::control tooltips retain their offset while sticky headings remain at the top | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::description header controls align right and restore only when collapsed | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::diff lines use full-width theme-aware add and delete treatments | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::edit mode outlines the hovered block without moving the layout | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::edit mode titles an open comment with its literal tag in code font | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::fenced code uses the editor foreground and one font scale | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::figure captions are centred and de-emphasised | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::first-element gap: 40px on the first child, clearance only on the first editor and the Start writing button | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::floating preview toolbar supports forced dark and white palettes | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::forced preview themes supply dropdown colors independently of the host | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::frontmatter and table editors keep the active cell surface without nested input frames | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::frontmatter edit hover colors follow the selected preview theme | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::frontmatter edits stay inline while edit mode preserves source newlines | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::frontmatter field actions sit in the editing row with labels and no pseudo-tooltips | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::frontmatter link tooltips wrap text in a fixed theme-aware pointer-transparent surface | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::frontmatter properties label is inset, table-matched, and unboxed | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::images never overflow the preview column | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::in edit mode table cells keep a minimum width and the edited cell is wider | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::linked file details are muted, italic, and clipped to the available line | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::list insertion lines show the drop boundary without moving the rows | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |
| core/preview/previewStyles.test.js::narrow properties wrap long paths without hiding expanded descriptions | load-time coverage only: every mutant it reaches is also credited to every test of its file, so zero kills proves nothing (extends mt-Q11) |

78 more row(s): see summary.json.

## Holes

Mutants no test of src/core kills (survived or no coverage), labelled by the others phase.

| file | line | mutator | replacement | status | label | killed by |
| --- | --- | --- | --- | --- | --- | --- |
| src/core/comments/commentModel.ts | 55:18 | Regex | /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z\| | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 55:18 | Regex | /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 59:39 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 59:39 | EqualityOperator | value.length < 40 | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 136:18 | MethodExpression | parsed.every(comment => comment === undefined) | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 136:30 | ArrowFunction | () => undefined | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 136:43 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/comments/commentModel.ts | 147:7 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 57:11 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 57:20 | StringLiteral | "Stryker was here!" | Survived | no test kills it |  |
| src/core/comments/inlineThread.ts | 66:44 | Regex | /^\n/u | Survived | no test kills it |  |
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
| src/core/frontmatter/fileLinks.ts | 49:7 | BooleanLiteral | annotation.tooltipShowsFields?.length | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 49:7 | ConditionalExpression | false | Survived | no test kills it |  |
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
| src/core/frontmatter/fileLinks.ts | 111:8 | MethodExpression | configured | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 112:17 | MethodExpression | configured | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 115:7 | ArrayDeclaration | [] | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 115:21 | LogicalOperator | workspaceRoots[0] && path.dirname(filePath) | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 118:77 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 125:21 | BooleanLiteral | isWithin(candidate, path.resolve(filePath)) | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 126:21 | MethodExpression | ["index.md", "log.md"].every(name => fs.statSync(path.join(c | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 126:21 | ArrayDeclaration | [] | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 126:22 | StringLiteral | "" | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 126:34 | StringLiteral | "" | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 126:49 | ArrowFunction | () => undefined | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 126:99 | ObjectLiteral | {} | NoCoverage | killed only by another layer | page/fmtableReqFrontmatter.requirements.test.js::the number input carries no schema limits and a value out of range is refused at save time |
| src/core/frontmatter/fileLinks.ts | 126:117 | BooleanLiteral | true | NoCoverage | killed only by another layer | page/fmtableReqFrontmatter.requirements.test.js::the number input carries no schema limits and a value out of range is refused at save time |
| src/core/frontmatter/fileLinks.ts | 176:72 | MethodExpression | target.endsWith("\\\\") | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 199:8 | EqualityOperator | navigationRoots.length >= 0 | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 199:55 | ArrayDeclaration | [] | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 200:7 | ArrayDeclaration | [] | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 204:7 | EqualityOperator | resolution !== "document-relative" | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 204:7 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 204:7 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 206:9 | MethodExpression | containmentRoots.every(containmentRoot => isWithin(containme | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 206:91 | BlockStatement | {} | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 212:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 212:42 | BlockStatement | {} | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 213:39 | StringLiteral | `` | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 215:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 215:78 | BlockStatement | {} | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 216:39 | StringLiteral | `` | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 218:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 218:9 | EqualityOperator | resolution !== "document-relative" | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 218:9 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 220:11 | MethodExpression | containmentRoots.every(containmentRoot => { try { retu | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 223:17 | BlockStatement | {} | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 224:18 | BooleanLiteral | true | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 226:11 | BlockStatement | {} | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 227:39 | StringLiteral | `` | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 231:37 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 242:7 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 242:63 | StringLiteral | `` | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 243:7 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 243:59 | StringLiteral | "" | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 254:7 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 257:11 | StringLiteral | `` | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 259:11 | StringLiteral | `` | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 260:11 | StringLiteral | `` | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 263:7 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 263:65 | StringLiteral | `` | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 287:13 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 299:25 | LogicalOperator | (navigationRoots.find(root => isWithin(root, filePath)) ?? n | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 299:46 | ArrowFunction | () => undefined | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 303:11 | LogicalOperator | relative && path.basename(filePath) | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 303:69 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 325:7 | CallExpression | ; | NoCoverage | no test kills it |  |
| src/core/frontmatter/fileLinks.ts | 328:43 | LogicalOperator | item.arrayIndex && "scalar" | Survived | no test kills it |  |

684 more row(s): see summary.json.

## Test files left out

None: all 163 test files ran.
