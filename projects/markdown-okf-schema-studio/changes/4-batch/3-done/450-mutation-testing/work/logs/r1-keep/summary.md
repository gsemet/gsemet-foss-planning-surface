# Mutation summary

Generated 2026-11-21T11:16:32.381Z. Phases: core, others.

Mutants: 366 Killed, 111 CompileError, 198 Survived, 15 NoCoverage, 77 Timeout. Tests that ran: 1396.

## Score per sub-folder of src/core

| folder | score | killed | survived | no coverage | timeout | compile error | ignored | holes only another layer kills | score with other layers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| find | 78.6% | 50 | 11 | 4 | 5 | 27 | 0 | 0 | 78.6% |
| scroll | 67.8% | 142 | 62 | 6 | 1 | 43 | 0 | 0 | 67.8% |
| syntax | 65.3% | 174 | 125 | 5 | 71 | 41 | 0 | 17 | 69.9% |

## Score per SwRS

Share of the mutants reached by the tests of the SwRS that those tests kill (a test can carry several IDs, so the shares overlap).

| SwRS | tests | mutants reached | killed | score |
| --- | --- | --- | --- | --- |
| StRS-MDOKFSTUDIO-CORE-006 | 1 | 277 | 72 | 26.0% |
| StRS-MDOKFSTUDIO-FMSCHEMA-001 | 1 | 22 | 9 | 40.9% |
| SwRS-MDOKFSTUDIO-BLOCK-003 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-014 | 2 | 152 | 70 | 46.1% |
| SwRS-MDOKFSTUDIO-BLOCK-017 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-042 | 2 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-087 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-094 | 4 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-109 | 4 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-117 | 3 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-124 | 2 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-127 | 2 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-156 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-166 | 2 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-169 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-174 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-191 | 2 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-193 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-205 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-234 | 9 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-256 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-257 | 4 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-259 | 7 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-260 | 5 | 136 | 54 | 39.7% |
| SwRS-MDOKFSTUDIO-BLOCK-262 | 4 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-263 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-265 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-BLOCK-266 | 11 | 157 | 70 | 44.6% |
| SwRS-MDOKFSTUDIO-BLOCK-268 | 6 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-BLOCK-269 | 5 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-CODE-001 | 9 | 159 | 73 | 45.9% |
| SwRS-MDOKFSTUDIO-CODE-007 | 2 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-CODE-008 | 2 | 20 | 9 | 45.0% |
| SwRS-MDOKFSTUDIO-CODE-014 | 2 | 159 | 70 | 44.0% |
| SwRS-MDOKFSTUDIO-CODE-019 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-CODE-039 | 8 | 159 | 70 | 44.0% |
| SwRS-MDOKFSTUDIO-CODE-040 | 5 | 159 | 70 | 44.0% |
| SwRS-MDOKFSTUDIO-CORE-001 | 3 | 135 | 54 | 40.0% |
| SwRS-MDOKFSTUDIO-CORE-003 | 8 | 276 | 71 | 25.7% |
| SwRS-MDOKFSTUDIO-CORE-008 | 2 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-CORE-010 | 3 | 156 | 70 | 44.9% |
| SwRS-MDOKFSTUDIO-CORE-012 | 5 | 274 | 86 | 31.4% |
| SwRS-MDOKFSTUDIO-CORE-013 | 5 | 152 | 70 | 46.1% |
| SwRS-MDOKFSTUDIO-CORE-022 | 6 | 167 | 70 | 41.9% |
| SwRS-MDOKFSTUDIO-CORE-025 | 1 | 135 | 54 | 40.0% |
| SwRS-MDOKFSTUDIO-CORE-028 | 6 | 135 | 54 | 40.0% |
| SwRS-MDOKFSTUDIO-CORE-034 | 3 | 135 | 54 | 40.0% |
| SwRS-MDOKFSTUDIO-CORE-050 | 3 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-CORE-071 | 10 | 140 | 54 | 38.6% |
| SwRS-MDOKFSTUDIO-CORE-072 | 12 | 152 | 70 | 46.1% |
| SwRS-MDOKFSTUDIO-CORE-073 | 4 | 277 | 72 | 26.0% |
| SwRS-MDOKFSTUDIO-CORE-079 | 20 | 152 | 70 | 46.1% |
| SwRS-MDOKFSTUDIO-CORE-088 | 2 | 265 | 56 | 21.1% |
| SwRS-MDOKFSTUDIO-CORE-089 | 3 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-DIAG-001 | 3 | 161 | 70 | 43.5% |
| SwRS-MDOKFSTUDIO-DIAG-005 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-DIAG-017 | 2 | 159 | 70 | 44.0% |
| SwRS-MDOKFSTUDIO-DIAG-023 | 2 | 159 | 70 | 44.0% |
| SwRS-MDOKFSTUDIO-DIAG-024 | 4 | 159 | 70 | 44.0% |
| SwRS-MDOKFSTUDIO-DIAG-032 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-DIAG-050 | 2 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-DIAG-054 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-DIAG-068 | 3 | 155 | 71 | 45.8% |
| SwRS-MDOKFSTUDIO-DIAG-084 | 10 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-DIAG-089 | 4 | 159 | 70 | 44.0% |
| SwRS-MDOKFSTUDIO-DIAG-097 | 4 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-DIAG-105 | 4 | 161 | 70 | 43.5% |
| SwRS-MDOKFSTUDIO-DIAG-121 | 5 | 155 | 70 | 45.2% |
| SwRS-MDOKFSTUDIO-DIAG-122 | 9 | 152 | 70 | 46.1% |
| SwRS-MDOKFSTUDIO-DIAG-124 | 1 | 161 | 70 | 43.5% |
| SwRS-MDOKFSTUDIO-DIAG-125 | 14 | 155 | 70 | 45.2% |
| SwRS-MDOKFSTUDIO-DIAG-126 | 1 | 135 | 54 | 40.0% |
| SwRS-MDOKFSTUDIO-FMEDIT-004 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-FMEDIT-010 | 3 | 22 | 11 | 50.0% |
| SwRS-MDOKFSTUDIO-FMEDIT-016 | 4 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-FMEDIT-024 | 3 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-FMEDIT-029 | 3 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-FMEDIT-043 | 6 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-FMEDIT-067 | 3 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-001 | 2 | 141 | 54 | 38.3% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-004 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-005 | 4 | 22 | 12 | 54.5% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-006 | 5 | 22 | 12 | 54.5% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-014 | 2 | 22 | 9 | 40.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-023 | 2 | 22 | 9 | 40.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-029 | 1 | 22 | 9 | 40.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-039 | 2 | 22 | 9 | 40.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-046 | 4 | 19 | 10 | 52.6% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-050 | 3 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-055 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-063 | 1 | 22 | 9 | 40.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-067 | 4 | 142 | 59 | 41.5% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-084 | 1 | 22 | 11 | 50.0% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-090 | 1 | 22 | 9 | 40.9% |
| SwRS-MDOKFSTUDIO-FMSCHEMA-091 | 3 | 22 | 9 | 40.9% |
| SwRS-MDOKFSTUDIO-GFM-001 | 4 | 152 | 70 | 46.1% |
| SwRS-MDOKFSTUDIO-GFM-008 | 3 | 156 | 72 | 46.2% |
| SwRS-MDOKFSTUDIO-GFM-009 | 38 | 325 | 140 | 43.1% |
| SwRS-MDOKFSTUDIO-GFM-016 | 2 | 136 | 54 | 39.7% |
| SwRS-MDOKFSTUDIO-GFM-021 | 2 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-GFM-031 | 2 | 140 | 54 | 38.6% |
| SwRS-MDOKFSTUDIO-GFM-034 | 6 | 140 | 54 | 38.6% |
| SwRS-MDOKFSTUDIO-GFM-040 | 11 | 155 | 70 | 45.2% |
| SwRS-MDOKFSTUDIO-GFM-041 | 8 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-LAYOUT-001 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-LAYOUT-002 | 4 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-LAYOUT-007 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-LAYOUT-022 | 2 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-LAYOUT-023 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-LAYOUT-032 | 2 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-LIFE-004 | 2 | 135 | 54 | 40.0% |
| SwRS-MDOKFSTUDIO-LIFE-026 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-032 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-LIFE-039 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-044 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-049 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-LIFE-069 | 3 | 145 | 54 | 37.2% |
| SwRS-MDOKFSTUDIO-LIFE-071 | 1 | 161 | 70 | 43.5% |
| SwRS-MDOKFSTUDIO-LIFE-094 | 6 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-100 | 1 | 28 | 23 | 82.1% |
| SwRS-MDOKFSTUDIO-LIFE-108 | 1 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-LIFE-119 | 1 | 153 | 81 | 52.9% |
| SwRS-MDOKFSTUDIO-LIFE-125 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-127 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-149 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-156 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-169 | 5 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-LIFE-170 | 3 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-173 | 2 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-LIFE-174 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-175 | 4 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-178 | 2 | 159 | 70 | 44.0% |
| SwRS-MDOKFSTUDIO-LIFE-181 | 1 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-183 | 4 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-LIFE-184 | 9 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-MYST-001 | 11 | 140 | 54 | 38.6% |
| SwRS-MDOKFSTUDIO-MYST-006 | 3 | 159 | 71 | 44.7% |
| SwRS-MDOKFSTUDIO-MYST-013 | 5 | 159 | 72 | 45.3% |
| SwRS-MDOKFSTUDIO-MYST-017 | 3 | 140 | 54 | 38.6% |
| SwRS-MDOKFSTUDIO-MYST-019 | 5 | 156 | 70 | 44.9% |
| SwRS-MDOKFSTUDIO-MYST-024 | 8 | 140 | 54 | 38.6% |
| SwRS-MDOKFSTUDIO-MYST-031 | 3 | 156 | 70 | 44.9% |
| SwRS-MDOKFSTUDIO-MYST-036 | 1 | 140 | 54 | 38.6% |
| SwRS-MDOKFSTUDIO-MYST-038 | 2 | 17 | 9 | 52.9% |
| SwRS-MDOKFSTUDIO-MYST-045 | 3 | 19 | 10 | 52.6% |
| SwRS-MDOKFSTUDIO-MYST-053 | 4 | 152 | 70 | 46.1% |
| SwRS-MDOKFSTUDIO-MYST-057 | 7 | 164 | 70 | 42.7% |
| SwRS-MDOKFSTUDIO-MYST-063 | 5 | 156 | 70 | 44.9% |
| SwRS-MDOKFSTUDIO-MYST-066 | 8 | 0 | 0 | n/a |
| SwRS-MDOKFSTUDIO-MYST-072 | 2 | 140 | 54 | 38.6% |

84 more row(s): see summary.json.

## Tests that kill nothing

Tests that reach killable mutants and kill none of them (zero-kill candidates).

| test | mutants reached |
| --- | --- |
| core/comments/anchoring.test.js::T45: a deleted quote orphans the thread and keeps its old line | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: a long unique quote that moved far away is found | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: a quote still inside its lines stays anchored | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: a quote that changed by more than 20 percent is orphaned, not guessed | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: a quote that spans lines is found, and CRLF documents work | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: a short quote is only found inside the +-50 line window | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: a small edit of the quote is followed by the fuzzy search | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: a thread without quote stays where it is while the line exists | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: duplicate quotes are decided by prefix and suffix | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: duplicate quotes without usable context use proximity only inside the window | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: fuzzy search needs a candidate containing the rarest word | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: lines inserted above move the thread to the new line | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: markdown markup does not hide the quote | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: reanchorThreads updates moved threads, keeps orphans untouched and loses nothing | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: shiftThreadLines keeps endLine at or after line | 3 CompileError, 5 Survived, 16 Killed, 9 Timeout |
| core/comments/anchoring.test.js::T45: the cost stays bounded for a large document and many fuzzy threads | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45: two fuzzy matches far apart are ambiguous and orphan the thread | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45r2: a copy in the old lines that does not fit the context yields to the copy that does | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45r2: a quote that resembles the old lines (60 % of its words, in order) is not orphaned | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45r2: a short quote never re-attaches when the surroundings disagree | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45r2: fuzzy matches must agree on numbers and negations | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45r2: several copies and no context match is no move | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45r2: text that renders differently from its source stays anchored at the original line | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/comments/anchoring.test.js::T45r2: the old lines are checked before the candidate cap | 9 Timeout, 10 Killed, 6 CompileError, 3 Survived |
| core/directives/registry.test.js::each directive name has one plug-in, found by its exact name | 9 Timeout, 5 Killed, 3 Survived |
| core/directives/registry.test.js::every plug-in renders, styles the preview and names MyST palette actions that exist | 9 Timeout, 5 Killed, 3 Survived |
| core/directives/registry.test.js::plug-in attribute rules are for data-* attributes the sanitizer does not handle itself | 9 Timeout, 5 Killed, 3 Survived |
| core/directives/registry.test.js::the admonition pass gives the directive's position to its admonition and infers the title | 9 Timeout, 5 Killed, 3 Survived |
| core/directives/registry.test.js::the figure pass puts the source lines on the figure; the table pass marks a list-table | 9 Timeout, 5 Killed, 3 Survived |
| core/directives/registry.test.js::the figure rule accepts a plain width only (the sanitizer applies it, see html-policy tests) | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::CRLF: an emptied block is removed whether or not the autosave wrote the placeholder | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::CRLF: an emptied first, last, tight and loose list item leave no blank line | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::CRLF: planBlocksDelete drops the trailing blank lines of the span | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::CRLF: planBlocksDelete refuses an include, the frontmatter and stale lines | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::CRLF: planBlocksDelete takes the separator like a cut (middle, first, last) | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::CRLF: stale lines give no removal | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::LF: an emptied block is removed whether or not the autosave wrote the placeholder | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::LF: an emptied first, last, tight and loose list item leave no blank line | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::LF: planBlocksDelete drops the trailing blank lines of the span | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::LF: planBlocksDelete refuses an include, the frontmatter and stale lines | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::LF: planBlocksDelete takes the separator like a cut (middle, first, last) | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::LF: stale lines give no removal | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::lone CR: an emptied block is removed whether or not the autosave wrote the placeholder | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::lone CR: an emptied first, last, tight and loose list item leave no blank line | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::lone CR: planBlocksDelete drops the trailing blank lines of the span | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::lone CR: planBlocksDelete refuses an include, the frontmatter and stale lines | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::lone CR: planBlocksDelete takes the separator like a cut (middle, first, last) | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/blocksDelete.test.js::lone CR: stale lines give no removal | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/frontmatterEdit.test.js::a YAML value is parsed; invalid YAML is refused unless the save is a flush | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/frontmatterEdit.test.js::a flush writes the value as typed and asks for no schema check | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/frontmatterEdit.test.js::a remove may not leave a required field newly missing | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/frontmatterEdit.test.js::a stale field, a bad new key and a value of the wrong type are refused | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/frontmatterEdit.test.js::a value change edits the field in place and gives the edited text | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/frontmatterEdit.test.js::a value fits its field type only with a schema and a known type | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/frontmatterEdit.test.js::add, rename and remove plan their edits; a duplicate name is named in the error | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/frontmatterEdit.test.js::with a schema the save needs the check of its edited text | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/lineEndingPreservation.test.js::a save never adds a bare LF to a CRLF file nor a CR to an LF file | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/lineEndingPreservation.test.js::saving one block of each fixture changes that block only and keeps every other byte | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/radioSelect.test.js::a group whose markers moved, an unknown target or a repeated option is refused | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/radioSelect.test.js::a group with no selection gets one (x), and CRLF files keep their offsets | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/radioSelect.test.js::a radio marker starts a list item and is followed by a space or a tab | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/radioSelect.test.js::one group is accepted across nested lists, lazy lines, quotes and two-digit ordered markers | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/radioSelect.test.js::positions that are not one group of consecutive radio items of one list are refused | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/radioSelect.test.js::selecting an option writes (x) on it and ( ) on the old one: two characters on two lines | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/radioSelect.test.js::selecting the only selected option writes nothing | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/radioSelect.test.js::with two selected options, a choice normalises the group in one plan | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a block move is refused for an included block, after the planner's own checks | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a block move swaps the blocks in one edit and gives the moved block's new first line | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a block text edit is the smallest replacement, offset by the block start | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a block text with no line break is left as the text box returned it, and a mixed one keeps the endings of the lines left alone | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a checkbox already in the asked state is unchanged, a missing one is refused | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a checkbox toggle changes the one character between the brackets | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a list mapped up to its trailing blank line moves like any block | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a multi-line block edited in a CR document keeps CR inside the block | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a multi-line block edited in a CRLF document keeps CRLF inside the block | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a multi-line block edited in a LF document keeps LF inside the block | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a paste inserts the clipboard as new blocks, never next to an included block | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a single-line block takes the line ending of the document | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::a thread reply replaces the closing line and uses the document's line break | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::copy and cut refuse an included block and a range outside the text | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::copy gives the exact Markdown of the blocks, cut also removes them with one separator | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::deleting a thread at the end of the file removes the line break before it | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::deleting a thread removes whole lines and one of two surrounding blank lines | 9 Timeout, 5 Killed, 3 Survived |
| core/edits/sourceEdits.test.js::thread lines are read only when they are exactly one thread comment | 9 Timeout, 5 Killed, 3 Survived |
| core/export/htmlExport.test.js::a THREAD chip with its popover, a TODO chip, source-mapping attributes and the tabindex of mapped blocks are left out | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::a front matter value and a key under their editors are exported shown, without the editor | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::a local image becomes a data URI and an unreadable one is counted and loses its source | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::a mailto link is kept and a file: link, an invalid anchor and a query-only link are unwrapped and reported | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::a paragraph under the block editor is exported, its editor is not | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::a properties table without a schema keeps its two columns inside the closed details | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::a style value cannot close the style element and a script URL is dropped | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::a tab set works without script: radios, labels, and the shown tab is the one the page showed | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::a table cell under the cell editor is exported with its content shown and without the editor | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::a task list checkbox stays, disabled and without its edit attributes | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::every candidate of a srcset is embedded and an unreadable one is dropped | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::folded sections are shown and the fold attributes are gone | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::links keep external and anchor targets and unwrap the others, reporting them once | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::nested tab sets get their own radio names and a dropdown keeps its open state | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::review comments, controls and editing chrome are left out, find marks keep their text | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::the Description column stays and the editing data goes, whatever the toggle state of the page | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::the KaTeX sheet and its fonts are inline, and only for a page with math | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::the file is one document with no script, no linked file and no import, and no vscode- name | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::the host's list of blank runs and a blank-lines block are not exported | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::the properties table becomes a closed details with a summary and no editing data | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::the resolved theme tokens replace the host mapping and the theme kind class goes on the body | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::the snapshot guard accepts the page shape and refuses a malformed one | 9 Timeout, 5 Killed, 3 Survived |
| core/export/htmlExport.test.js::the title falls back to the first heading, then to the file name | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::the token rule follows the preview sheet and names every resolved token | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/export/htmlExport.test.js::the width mode, the width rule and the theme mode go on the file, the zoom and clearance do not | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/frontmatter/diagReq.frontmatter.requirements.test.js::a JSON5 schema that cannot be parsed gives the generic table and one warning row; a YAML error is not reported as such | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/frontmatter/diagReq.frontmatter.requirements.test.js::an absolute link target is refused with an E10 error in POSIX, drive-letter and UNC form | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/diagReq.frontmatter.requirements.test.js::an empty or comment-only YAML schema is reported as empty: generic table, one info note, no throw | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/diagReq.frontmatter.requirements.test.js::frontmatter that is a list or an empty block gives the not-a-mapping error row and one error | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/frontmatter/diagReq.frontmatter.requirements.test.js::the registry keeps 64 resolved schemas and drops the oldest at the 65th | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/diagReq.frontmatter.requirements.test.js::the title badge counts infos only when there is no error and no warning | 9 Timeout, 10 Killed, 3 Survived, 1 CompileError |
| core/frontmatter/fileLinks.test.js::auto-detected git roots outside the workspace are ignored | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/fileLinks.test.js::conditional, patternProperties, and additionalProperties schemas are traversed | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/fileLinks.test.js::document-relative links stay inside workspace roots unless explicitly allowed | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/fileLinks.test.js::link display options reject invalid metadata | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/fileLinks.test.js::oneOf annotations are collected only when exactly one branch matches | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::add after a list keeps a column-0 comment with the next field | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::add after a list keeps its commented-out item above the new field | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::add after a list keeps its commented-out item above the new field on CRLF | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::add after a nested map keeps its trailing comment above the new field | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::add of a multi-line value after a commented list is still positioned | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::removing the only field leaves a valid empty mapping | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::removing the only field of a CRLF document leaves a valid empty mapping | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural CRLF add after a field keeps CRLF line endings | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural CRLF add at the end appends one CRLF line before the fence | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural CRLF remove deletes the field lines and keeps CRLF | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural CRLF remove of the last field drops the preceding break | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural F1 add of a list uses the compact sequence style | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural F1 add owner appends one line before the closing delimiter | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural F2 add after the last field matches the add without afterField | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural F2 add owner after title inserts one line directly after the title | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural F2 edits keep both comments unless their own line is removed | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural F2 remove links deletes exactly that line | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural F2 remove of the last field keeps the blank line and the closing fence | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural F2 remove tags deletes exactly the sequence lines | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural F2 rename title to heading keeps the trailing comment | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural F2 rename to a key that needs quoting changes only that line | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::structural add to an empty frontmatter block writes the pair into the fence | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::value edit F1 annotation_exemption changes only the named field | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::value edit F1 derived_by changes only the named field | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::value edit F1 derives_from changes only the named field | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::value edit F1 exemption_reason changes only the named field | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::value edit F1 lifecycle changes only the named field | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::value edit F1 title changes only the named field | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::value edit F2 links changes only the named field | 9 Timeout, 5 Killed, 3 Survived |
| core/frontmatter/frontmatterPreservation.test.js::value edit F2 quoted changes only the named field | 9 Timeout, 5 Killed, 3 Survived |

348 more row(s): see summary.json.

## Redundant tests (greedy set)

A keeper set of 34 test(s) kills every killed mutant; the others below add nothing the keepers do not kill. Two duplicate tests are never both listed: one of them is a keeper.

| redundant test | killed mutants | also killed by keepers |
| --- | --- | --- |
| core/comments/anchoring.test.js::T45: shiftThreadLines applies several changes of one event (multi-cursor, undo order) | 10 | 1 keeper(s), for example core/scroll/anchorPolicy.test.js |
| core/comments/anchoring.test.js::T45: shiftThreadLines follows lines inserted and removed above | 13 | 1 keeper(s), for example core/scroll/anchorPolicy.test.js |
| core/comments/anchoring.test.js::T45: text inside code fences and front matter is never a match | 11 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/edits/sourceEdits.test.js::a label rename changes the label line only and counts the remaining references | 1 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/find/findMatches.test.js::a literal query finds every occurrence, ignoring case unless asked | 8 | 6 keeper(s), for example core/find/findMatches.test.js |
| core/frontmatter/fileLinks.test.js::link annotations read target fields and exact marker lines afresh | 1 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/frontmatter/frontmatterFence.test.js::frontmatter fence: CRLF empty block accepts an added field with CRLF endings | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/frontmatterFence.test.js::frontmatter fence: CRLF line endings | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/frontmatterFence.test.js::frontmatter fence: a document without a closing fence has no frontmatter | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/frontmatterFence.test.js::frontmatter fence: dashes inside a quoted string | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/frontmatterFence.test.js::frontmatter fence: dot-dot-dot closing fence | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/frontmatterFence.test.js::frontmatter fence: empty block stays valid | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/frontmatterFence.test.js::frontmatter fence: trailing spaces after the closing fence | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/frontmatterFence.test.js::frontmatter fence: value ending in four dots | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/frontmatterFence.test.js::frontmatter fence: value ending in three dashes | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/frontmatterFence.test.js::frontmatter fence: value ending in three dots | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/frontmatterFence.test.js::linked file details read the frontmatter of a BOM-prefixed file | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/frontmatterFence.test.js::patch guard refuses patches that lose, duplicate or corrupt a key | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/frontmatterParseOnce.test.js::a document's frontmatter is parsed once for the render and every analysis of that text | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/frontmatter/propertiesTable.test.js::T220: the known stems are rendered as a second escaped row attribute next to the suggestions | 2 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/frontmatter/propertiesTable.test.js::T22: link suggestions are rendered as an escaped row attribute only when present | 5 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/frontmatter/propertiesTable.test.js::diagnostic errors span every table column and expose their severity | 2 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/frontmatter/propertiesTable.test.js::error rows carry the red underline class and hover tooltip | 2 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/frontmatter/propertiesTable.test.js::escapes list preview items without truncating short lists | 3 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/frontmatter/propertiesTable.test.js::exposes unused schema field metadata for the frontmatter toolbar | 2 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/frontmatter/propertiesTable.test.js::exposes unused schema keys for frontmatter key editing | 2 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/frontmatter/propertiesTable.test.js::nested object values render as escaped YAML while keeping edit metadata | 2 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/frontmatter/propertiesTable.test.js::renders a two-column Obsidian-like table with escaped values | 3 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/frontmatter/propertiesTable.test.js::structured values and enum choices are exposed for schema-aware editing | 2 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/frontmatter/propertiesTable.test.js::valid link tooltips expose workspace-relative paths | 4 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/mapping/labelRename.test.js::counts {ref} uses with and without a title, not other roles or names | 2 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/navigation/previewNavigation.test.js::marker navigation selects exact marker identities | 1 | 1 keeper(s), for example core/syntax/markdownSyntax.test.js |
| core/preview/contentPatch.test.js::CR 149: shell keys differ when a chart appears or disappears, and charts of two pages share a shell | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::P-03: a plan parses the new page only, because the loaded page was analyzed as the previous new page | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T08: two renders with different zoom have the same shell key and the same context key | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T17: the shell key is equal whatever the incoming-changes preference, and the Diff button is in both | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: a ready report with the identifiers of the last assignment is a webview that was created again | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: canPatch refuses next content that carries a script or a nonce | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: canPatch refuses pages without a content container | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: content that mentions a container inside the content does not change the extracted content | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: extractMainContent returns the inner HTML of the content container of a real page | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: injecting PlantUML diagrams into a page keeps its shell key, so the diagrams can be patched in | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: reuseNonce swaps every occurrence, in the policy tokens and in the attributes | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: shell keys differ when Mermaid appears or disappears, and when math appears | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: status lines that the runtime would reject keep the patch from being sent | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: the record of a patched page carries the nonce of the loaded page and keeps its shell | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: the runtime context key covers the startup settings and nothing the page follows itself | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: the shell key ignores the status region and the runtime script, and nothing else | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::T34: two renders of one document type have equal shell keys despite other text, nonces and identifiers | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/preview/contentPatch.test.js::the page script is injected verbatim even when it contains replacement patterns | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertInsideColonContainer.test.js::a grid inside the alert "> **Note**" stays inside its note | 14 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertInsideColonContainer.test.js::a grid inside the alert "> [!NOTE]" stays inside its note | 14 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertInsideColonContainer.test.js::an alert in a three-colon card of a nested grid keeps the text after it in the card | 19 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertInsideColonContainer.test.js::an alert inside a card keeps the text after it inside the card | 19 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertInsideColonContainer.test.js::an alert inside a tab item of a tab set keeps the text after it in the tab | 11 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertInsideColonContainer.test.js::an alert without a colon fence in its body keeps the three-colon admonition | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertInsideColonContainer.test.js::inside a colon container the alert is a backtick directive; outside it stays a colon fence | 19 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertInsideColonContainer.test.js::the blocks of a grid inside an alert map to the lines of the document | 14 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::a lazy continuation line renders inside the alert, which ends on that line | 57 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::a lazy line of a CRLF alert stays in the alert | 57 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::a lazy line of an alert nested in a list item stays in the alert | 57 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::a lazy setext underline or delimiter row adds no heading or table to the alert | 15 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> <!-- c -->\n> text\nlazy\n" | 57 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> Line one.\nlazy line.\n" | 57 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a \| b\n:-\|-:\n" | 60 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a \| b\n> --\|--\nfoo\n" | 36 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n +++\nb\n" | 63 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n === \n" | 62 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n***\nb\n" | 20 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n*\n" | 14 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n+ b\n" | 10 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n+++\nb\n" | 61 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n- item\n" | 10 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n--\n" | 62 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n1) b\n" | 10 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n1. item\n" | 10 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n:::{tip}\ninner\n:::\n" | 22 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n===\n" | 60 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n=\n" | 61 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n> # head\nb\n" | 42 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n> ***\nb\n" | 35 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n> 2. x\n" | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n> <custom-x>\nlazy\n" | 57 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n>\nb\n" | 24 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n\nb\n" | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n```\ncode\n```\n" | 24 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\nb\nc\n> d\n" | 57 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> a\n~~~\ncode\n~~~\n" | 24 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\n> \| a \| b \|\n\| - \| - \|\n" | 64 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertLazyContinuation.test.js::an unquoted line joins the alert only as a lazy continuation of its open paragraph: "> [!NOTE]\nlazy right after head\n" | 49 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::a context tag group re-parsed from raw HTML maps the alert of its body to the lines of the block | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::a quote nested in an alert (no nested alert) keeps its lines | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::alert markers inside a fenced code block stay untouched and do not move later lines | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::an alert after a frontmatter block carries the absolute lines of the file | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::an alert between context tags keeps the lines of the tag group, the alert and the next blocks | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::an alert followed by a blank line and a paragraph keeps the paragraph on its line | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::an alert followed directly by a lazy line ends on that line and keeps the next blocks in place | 52 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::an alert followed directly by a list item ends on its last quoted line and keeps the list in place | 10 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::an alert inside a grid card keeps the lines of the grid, the card, the alert and the next blocks | 19 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::an alert inside a list item keeps the lines of the item, the alert and the next blocks | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::an alert inside a tab item keeps the lines of the tab set, its panels and the next blocks | 11 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::an unclosed fence after an alert is reported and shown with its own line | 3 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::every alert type, the bold markers and a titled alert keep the lines of the document | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::the document with an important alert then a note alert maps every block to its own lines | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::the same document with CRLF line breaks carries the same lines | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertSourceLines.test.js::two consecutive alerts and the blocks after them carry the lines of the document | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertTitle.test.js::Studio and GitHub agree on the title and the body order of the committed GitHub fixtures | 5 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertTitle.test.js::a MyST admonition still takes its title from a leading heading | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertTitle.test.js::a legacy bold-marker alert keeps a heading in the body | 5 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertTitle.test.js::an alert between context tags keeps a heading in the body | 5 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertTitle.test.js::an alert whose first body line is a heading keeps the default title and the heading | 18 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertTitle.test.js::an alert whose first body line is a lone bold line keeps the default title and the bold line | 5 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertTitle.test.js::an alert with marker text keeps it as the title and keeps a heading in the body | 5 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/alertTitle.test.js::the heading inside an alert sits in the admonition, which the TOC column and sticky band exclude | 5 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/bareUrlAutolink.test.js::bare URLs in list items and table cells are links | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/bareUrlAutolink.test.js::bare http(s) and www URLs render as links with GFM trailing-punctuation rules | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/bareUrlAutolink.test.js::code, links, autolinks, math, emails and non-URLs stay as they are | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/bareUrlAutolink.test.js::generated links pass through the same sanitizer and navigation routing as Markdown links | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/bareUrlAutolink.test.js::javascript-looking and other non-http text is never linkified | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/bareUrlAutolink.test.js::pathological URLs render in linear time | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/bareUrlAutolink.test.js::prose contexts are linkified while directive option text stays literal | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/bareUrlAutolink.test.js::the source text sent to the editor keeps the raw URL | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/blankRunsList.test.js::a blank run in a code fence is not a run of the source's blocks | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/blankRunsList.test.js::a source with no run has the list element with an empty value, and every render carries it | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/blankRunsList.test.js::an edit changes the list: the next render of the content patch carries the new runs | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/blankRunsList.test.js::the rendered content ends with a hidden list of the blank runs of the source | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/blockBreakInContainer.test.js::a +++ line at the root stays a block break | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/blockBreakInContainer.test.js::a +++ line in a directive body renders as text | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/blockBreakInContainer.test.js::a +++ line in a directive body with metadata renders as text | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/blockBreakInContainer.test.js::a +++ line in a list item renders as text | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/blockBreakInContainer.test.js::a +++ line in a quote renders as text | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/blockBreakInContainer.test.js::a +++ line in an alert followed by a list item renders as text | 3 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/blockBreakInContainer.test.js::a +++ line in the end of an alert renders as text | 4 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::a card nests inside a grid item and holds a code block | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::a card without header or footer shows the title and body only | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::a comment and a thread in a tab item keep their own source line range | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::a nested tab set in a tab item is no block of its own, only the outer item is edited | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::a standalone card shows its header option above the title, then the body and the footer | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::a standalone card splits header and footer at ^^^ and +++, and links its title | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::a tab set renders a tablist of buttons wired to panels with ARIA roles | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::a table, a code block, a card and a grid in a tab item are no blocks of their own | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::a version admonition is titled with its version and no trailing colon | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::class-card adds safe class names only, on a standalone card and on a grid card | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::each tab item and the tab set carry their own source lines for editing | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::tab item titles stay plain text inside the tab button | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::tab panels hold any block, a grid and a card among them, and tab sets nest | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::tabs keep their sync key and the sync group of the set | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::the :selected: tab shows its panel and the others are hidden; the first tab is the default | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::the sanitized preview keeps the tab roles, ids and hidden panels but no script or handler | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |
| core/render/cardsTabs.test.js::the stylesheet gives a standalone card the grid card look and its own spacing | 2 | 20 keeper(s), for example core/render/alertLazyContinuation.test.js |

363 more row(s): see summary.json.

## Tests not judged

Tests whose mutants are all excluded, timed out or not compilable: the run cannot say whether they matter.

| test | reason |
| --- | --- |
| core/comments/commentEditing.test.js::S-04: a comments file that is a symbolic link is refused and its target is never written | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::S-04: a write goes to a temporary file and is renamed onto the comments file; a failed rename leaves no temporary file | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T43: a create and a reply queued together both land | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T43: addReply appends to the named thread only | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T43: addThread appends a thread with its first comment and does not touch the input | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T43: addThread refuses a full file and a repeated id | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T43: an invalid existing file is never overwritten, and a refusal does not stop the queue | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T43: ids are a prefix and 8 hex characters | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T43: isValidAnchor enforces lines and the 500 / 32 / 32 limits | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T43: normalizeBody trims and enforces 1 to 10000 characters | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T43: resolveAuthor uses the setting, then Git, then the OS user, then Anonymous | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T43: the result carries the written text and its hash (the host ignores that echo) | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T43: two quick creates never lose one (per-file queue: read latest, apply, write) | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T44: deleteThread removes the named thread only; the last one leaves an empty list | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T44: resolve and delete go through the same per-file queue as create | reaches no mutant of the sampled files |
| core/comments/commentEditing.test.js::T44: setResolved resolves and reopens the named thread only, without touching the input | reaches no mutant of the sampled files |
| core/comments/commentModel.test.js::T42: a valid file parses into threads | reaches no mutant of the sampled files |
| core/comments/commentModel.test.js::T42: hostile strings stay plain data and unknown fields are dropped | reaches no mutant of the sampled files |
| core/comments/commentModel.test.js::T42: limits on size, threads, comments and string length | reaches no mutant of the sampled files |
| core/comments/commentModel.test.js::T42: malformed JSON and wrong shapes give errors and no threads | reaches no mutant of the sampled files |
| core/comments/commentModel.test.js::T42: one invalid thread rejects the whole file | reaches no mutant of the sampled files |
| core/comments/commentModel.test.js::T42: serialization is stable: fixed key order, 2 spaces, trailing newline | reaches no mutant of the sampled files |
| core/comments/commentModel.test.js::T42: sidecarNameFor puts .comments.json next to the document | reaches no mutant of the sampled files |
| core/comments/inlineThread.test.js::CRLF line ends and trailing spaces or tabs do not change the messages | reaches no mutant of the sampled files |
| core/comments/inlineThread.test.js::a new thread snippet holds the header and an indented caret line | reaches no mutant of the sampled files |
| core/comments/inlineThread.test.js::a reply cannot close the comment early, and an empty reply or a non-thread is refused | reaches no mutant of the sampled files |
| core/comments/inlineThread.test.js::a reply goes above the closing marker and nothing else changes | reaches no mutant of the sampled files |
| core/comments/inlineThread.test.js::a reply keeps the indentation and the text after the closing marker | reaches no mutant of the sampled files |
| core/comments/inlineThread.test.js::a thread body is read as messages with author, date and text | reaches no mutant of the sampled files |
| core/comments/inlineThread.test.js::a thread closed on the last message line is split before the reply | reaches no mutant of the sampled files |
| core/comments/inlineThread.test.js::an author is written on one line | reaches no mutant of the sampled files |
| core/comments/inlineThread.test.js::blank lines inside a message are kept, and a tab indent is accepted | reaches no mutant of the sampled files |
| core/comments/inlineThread.test.js::deleting takes one surrounding blank line when both neighbours are blank | reaches no mutant of the sampled files |
| core/comments/inlineThread.test.js::the date is written in local time as YYYY-MM-DD HH:MM | reaches no mutant of the sampled files |
| core/comments/inlineThread.test.js::what is not a thread is refused | reaches no mutant of the sampled files |
| core/comments/reviewReq.requirements.test.js::a change that makes the serialized file larger than 2 MiB is refused before the write | reaches no mutant of the sampled files |
| core/configuration/commentsConfiguration.test.js::T43: a non-string author name falls back to the empty default | reaches no mutant of the sampled files |
| core/configuration/commentsConfiguration.test.js::T43: reads the author name of the comments section | reaches no mutant of the sampled files |
| core/configuration/editingConfiguration.test.js::a fresh workspace starts the palette in GFM | reaches no mutant of the sampled files |
| core/configuration/editingConfiguration.test.js::falls back to GFM for an unknown or non-string palette mode | reaches no mutant of the sampled files |
| core/configuration/editingConfiguration.test.js::reads the default palette mode of the editing section | reaches no mutant of the sampled files |
| core/configuration/editingConfiguration.test.js::stored choice wins: a stored palette mode is kept over the default and the setting | reaches no mutant of the sampled files |
| core/configuration/editorAssociationMigration.test.js::an association of *.md to another editor, another pattern or another shape is left alone | reaches no mutant of the sampled files |
| core/configuration/editorAssociationMigration.test.js::an object that held only the Studio entry becomes undefined, which removes the key | reaches no mutant of the sampled files |
| core/configuration/editorAssociationMigration.test.js::the legacy array form loses the Studio *.md entry only | reaches no mutant of the sampled files |
| core/configuration/editorAssociationMigration.test.js::the object form loses its *.md entry for Studio and keeps every other entry | reaches no mutant of the sampled files |
| core/configuration/frontmatterConfiguration.test.js::frontmatter settings use their own section and defaults | reaches no mutant of the sampled files |
| core/configuration/frontmatterConfiguration.test.js::frontmatter visibility and strict validation can be configured independently | reaches no mutant of the sampled files |
| core/configuration/plantUmlConfiguration.test.js::reads and trims the configured PlantUML JAR path | reaches no mutant of the sampled files |
| core/configuration/plantUmlConfiguration.test.js::resolves the PlantUML engine from useJar and the workspace trust | reaches no mutant of the sampled files |
| core/configuration/plantUmlConfiguration.test.js::the built-in PlantUML engine is the default and useJar is read as a strict boolean | reaches no mutant of the sampled files |
| core/configuration/plantUmlConfiguration.test.js::uses an empty path for non-string configuration values | reaches no mutant of the sampled files |
| core/configuration/previewConfiguration.test.js::comment chips are shown by default and can be turned off | reaches no mutant of the sampled files |
| core/configuration/previewConfiguration.test.js::incremental updates can be turned off and default to on | reaches no mutant of the sampled files |
| core/configuration/previewConfiguration.test.js::normalizes preview content width and reserves zero for unlimited | reaches no mutant of the sampled files |
| core/configuration/previewConfiguration.test.js::normalizes sticky heading depth to one through six levels | reaches no mutant of the sampled files |
| core/configuration/previewConfiguration.test.js::reads independent studio preview settings without stock configuration keys | reaches no mutant of the sampled files |
| core/configuration/previewConfiguration.test.js::the content width setting is rounded to whole pixels and a negative value gives the default | reaches no mutant of the sampled files |
| core/configuration/settingsRegistry.test.js::a setting with nothing stored reads as its schema default | reaches no mutant of the sampled files |
| core/configuration/settingsRegistry.test.js::categories keep their titles and order, and settings are sorted by their order | reaches no mutant of the sampled files |
| core/configuration/settingsRegistry.test.js::the Opening Files settings are two booleans: the search results one on by default, the every-file one off | reaches no mutant of the sampled files |
| core/configuration/settingsRegistry.test.js::the Studio settings live under their own prefix, and no source writes a setting of the built-in Markdown preview | reaches no mutant of the sampled files |
| core/configuration/settingsRegistry.test.js::the generated settings schema is the package.json one, byte for byte | reaches no mutant of the sampled files |
| core/configuration/settingsRegistry.test.js::the host writes the boot settings as configured, in table order | reaches no mutant of the sampled files |
| core/configuration/settingsRegistry.test.js::the page gets the scroll, reveal, sticky band and comment chip settings in its boot context | reaches no mutant of the sampled files |
| core/configuration/settingsRegistry.test.js::the page reads missing or odd boot entries with the page defaults | reaches no mutant of the sampled files |
| core/directives/renderReq.registry.requirements.test.js::a directive name registered twice raises an error naming it; distinct names register | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::a definition indented by four spaces or a tab is code and stays counted | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::a link or a definition in a fenced code block stays counted: the reader sees it as code | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::a link target that repeats the text is left out: the visible matches are replaced, the target kept | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::a match is replaced at its own span and the rest of the file is byte-identical | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::a match that does not map one-to-one to the source is skipped and counted | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::a reference definition is left out; a footnote definition stays counted | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::a replacement with a dollar sign or regex characters is inserted as given | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::a white space of the matched text stands for a wrapped line break of the source | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::an autolink and a link written in a code span stay counted: the reader sees their text | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::an inline image is left out as a whole: its alt text is neither counted nor replaced | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::lines that are gone and overlapping spans are skipped; nothing to replace is refused | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::link titles, angle-bracket targets and targets with parentheses are left out too | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::no link inside a link: the outer target after an inner link is visible text | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::the info string of a fence is not taken for the visible match of a definition or link in it | reaches no mutant of the sampled files |
| core/edits/findReplace.test.js::the occurrence picks the right one among several in a block, markup around it kept | reaches no mutant of the sampled files |
| core/edits/matchLineEndings.test.js::a text unchanged but for its line endings is the reference again, every fixture, every block | reaches no mutant of the sampled files |
| core/edits/matchLineEndings.test.js::a text with the LF a text box returns takes the one line ending of the reference | reaches no mutant of the sampled files |
| core/edits/matchLineEndings.test.js::with mixed endings, the lines left alone keep theirs and a changed line takes the one it replaces | reaches no mutant of the sampled files |
| core/edits/textEdit.test.js::a refusal is told apart from a plan | reaches no mutant of the sampled files |
| core/edits/textEdit.test.js::overlapping or out-of-range text edits are refused | reaches no mutant of the sampled files |
| core/edits/textEdit.test.js::source lines split on LF, CRLF and CR, and a final line break adds an empty last line | reaches no mutant of the sampled files |
| core/edits/textEdit.test.js::text edits apply in offset order, whatever order they come in | reaches no mutant of the sampled files |
| core/frontmatter/frontmatterChanges.test.js::CR 155: a body that lost lines but no field adds no range | reaches no mutant of the sampled files |
| core/frontmatter/frontmatterChanges.test.js::CR 155: a changed value is modified and a new key is added | reaches no mutant of the sampled files |
| core/frontmatter/frontmatterChanges.test.js::CR 155: a key that disappeared is removed, a changed list item modifies the field | reaches no mutant of the sampled files |
| core/frontmatter/frontmatterChanges.test.js::CR 155: a removed field adds a range on line 1 so that the properties table is marked | reaches no mutant of the sampled files |
| core/frontmatter/frontmatterChanges.test.js::CR 155: a removed field with a changed field reports the table line and the changed field | reaches no mutant of the sampled files |
| core/frontmatter/frontmatterChanges.test.js::CR 155: a text without front matter, or with an invalid one, has no field lines | reaches no mutant of the sampled files |
| core/frontmatter/frontmatterChanges.test.js::CR 155: changed and added fields keep their line ranges and add nothing | reaches no mutant of the sampled files |
| core/frontmatter/frontmatterChanges.test.js::CR 155: the lines of each field cover its key line and the lines of its value | reaches no mutant of the sampled files |
| core/frontmatter/frontmatterChanges.test.js::CR 155: the same fields in another order are not changes, and a missing front matter has none | reaches no mutant of the sampled files |
| core/frontmatter/requirementSchemas.test.js::requirement schema strs: accepts a real requirement and rejects an unknown key | reaches no mutant of the sampled files |
| core/frontmatter/requirementSchemas.test.js::requirement schema swrs: accepts a real requirement and rejects an unknown key | reaches no mutant of the sampled files |
| core/frontmatter/sameData.test.js::isSameData compares key lists in order, as the patch verification needs | reaches no mutant of the sampled files |
| core/frontmatter/sameData.test.js::isSameData decides like util.isDeepStrictEqual on parsed YAML and near misses | reaches no mutant of the sampled files |
| core/frontmatter/schemaValidator.test.js::validator cache returns the same compiled function for a schema object | reaches no mutant of the sampled files |
| core/mapping/dropReferences.test.js::droppedFilePath reads local file addresses only | reaches no mutant of the sampled files |
| core/mapping/dropReferences.test.js::droppedReference writes a relative, percent-encoded link or image | reaches no mutant of the sampled files |
| core/mapping/dropReferences.test.js::droppedText joins the references with a space and skips files without one | reaches no mutant of the sampled files |
| core/mapping/dropReferences.test.js::firstHeadingTitle reads the first heading outside front matter and code | reaches no mutant of the sampled files |
| core/mapping/imageReference.test.js::isImageFileName accepts png, jpeg, gif, webp and svg only | reaches no mutant of the sampled files |
| core/mapping/imageReference.test.js::relativeImageReference accepts Windows separators and refuses another drive | reaches no mutant of the sampled files |
| core/mapping/imageReference.test.js::relativeImageReference gives a POSIX path relative to the document folder | reaches no mutant of the sampled files |
| core/mapping/imageReference.test.js::relativeImageReference refuses a path that cannot be written in a reference | reaches no mutant of the sampled files |
| core/mapping/lineDiff.test.js::T16: a base without a trailing newline matches one with it | reaches no mutant of the sampled files |
| core/mapping/lineDiff.test.js::T16: a modified line is one range and two separate edits are two ranges | reaches no mutant of the sampled files |
| core/mapping/lineDiff.test.js::T16: above the size cap the whole middle counts as changed | reaches no mutant of the sampled files |
| core/mapping/lineDiff.test.js::T16: added lines are reported in current line numbers | reaches no mutant of the sampled files |
| core/mapping/lineDiff.test.js::T16: deleted-only lines give no range | reaches no mutant of the sampled files |
| core/mapping/lineDiff.test.js::T16: identical text has no changed range | reaches no mutant of the sampled files |
| core/mapping/lineDiff.test.js::T16: line endings do not count as changes | reaches no mutant of the sampled files |
| core/mapping/lineDiff.test.js::T16: many differences beyond the edit budget fall back to the whole middle | reaches no mutant of the sampled files |
| core/mapping/lineHunks.test.js::CR147: a block is changed when it meets added lines or holds a removal | reaches no mutant of the sampled files |
| core/mapping/lineHunks.test.js::CR147: a hunk gives the base lines and the current lines | reaches no mutant of the sampled files |
| core/mapping/lineHunks.test.js::CR147: above the size caps the whole differing middle is one hunk | reaches no mutant of the sampled files |
| core/mapping/lineHunks.test.js::CR147: added lines have an empty base side and removed lines an empty current side | reaches no mutant of the sampled files |
| core/mapping/lineHunks.test.js::CR147: identical texts have no hunk, line endings do not count | reaches no mutant of the sampled files |
| core/mapping/lineHunks.test.js::CR147: lines removed and added before the next common line form one hunk | reaches no mutant of the sampled files |
| core/mapping/lineHunks.test.js::CR147: separate edits are separate hunks | reaches no mutant of the sampled files |
| core/mapping/lineHunks.test.js::CR147: the base lines of a block follow the hunks | reaches no mutant of the sampled files |
| core/mapping/lineHunks.test.js::CR234: a removal is never merged across a heading or a text line | reaches no mutant of the sampled files |
| core/mapping/lineHunks.test.js::CR234: a removal next to a changed line across a blank line is one hunk | reaches no mutant of the sampled files |
| core/mapping/pastedImage.test.js::a spoofed mime type is told apart from the bytes | reaches no mutant of the sampled files |
| core/mapping/pastedImage.test.js::isBase64 accepts the base64 alphabet only | reaches no mutant of the sampled files |
| core/mapping/pastedImage.test.js::nextImageName gives up after 1000 suffixes | reaches no mutant of the sampled files |
| core/mapping/pastedImage.test.js::nextImageName takes image.ext, then the first free suffix | reaches no mutant of the sampled files |
| core/mapping/pastedImage.test.js::sniffImage recognises png, jpeg, gif and webp by their magic bytes | reaches no mutant of the sampled files |
| core/mapping/pastedImage.test.js::sniffImage refuses everything else, including SVG, text and short input | reaches no mutant of the sampled files |
| core/mapping/sourceMapping.test.js::accepts Windows separators without weakening document identity | reaches no mutant of the sampled files |
| core/mapping/sourceMapping.test.js::keeps only active-document mappings in DOM order for ties | reaches no mutant of the sampled files |
| core/mapping/sourceMapping.test.js::source ranges preserve line endings and reject invalid bounds | reaches no mutant of the sampled files |
| core/mapping/textDiff.test.js::a CRLF pair is never split | reaches no mutant of the sampled files |
| core/mapping/textDiff.test.js::a surrogate pair is never split | reaches no mutant of the sampled files |
| core/mapping/textDiff.test.js::identical input yields an empty replacement | reaches no mutant of the sampled files |
| core/mapping/textDiff.test.js::insertion at the start and at the end | reaches no mutant of the sampled files |
| core/mapping/textDiff.test.js::insertion, deletion and replacement in the middle | reaches no mutant of the sampled files |
| core/mapping/textDiff.test.js::repeated characters do not let prefix and suffix overlap | reaches no mutant of the sampled files |
| core/mapping/textDiff.test.js::replacement reproduces the target for 200 seeded random pairs | reaches no mutant of the sampled files |
| core/mapping/wordDiff.test.js::CR147: a replaced word is removed on the left and added on the right | reaches no mutant of the sampled files |
| core/mapping/wordDiff.test.js::CR147: a very long pair marks everything | reaches no mutant of the sampled files |
| core/mapping/wordDiff.test.js::CR147: an empty side marks all of the other | reaches no mutant of the sampled files |
| core/mapping/wordDiff.test.js::CR147: consecutive changed words are one range, separate ones are separate | reaches no mutant of the sampled files |
| core/mapping/wordDiff.test.js::CR147: identical texts have no changed word | reaches no mutant of the sampled files |

201 more row(s): see summary.json.

## Holes

Mutants no test of src/core kills (survived or no coverage), labelled by the others phase.

| file | line | mutator | replacement | status | label | killed by |
| --- | --- | --- | --- | --- | --- | --- |
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
| src/core/find/findMatches.ts | 83:9 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 83:9 | EqualityOperator | index > match.groups.length | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 83:41 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 84:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/find/findMatches.ts | 86:36 | StringLiteral | "Stryker was here!" | NoCoverage | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 79:12 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 85:11 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 85:11 | LogicalOperator | (!finite(block.top) \|\| !finite(block.height) \|\| block.height | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 85:11 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 85:11 | LogicalOperator | (!finite(block.top) \|\| !finite(block.height) \|\| block.height | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 85:11 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 85:11 | LogicalOperator | (!finite(block.top) \|\| !finite(block.height)) && block.heigh | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 85:11 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 85:11 | LogicalOperator | !finite(block.top) && !finite(block.height) | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 85:58 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 85:58 | EqualityOperator | block.height <= 0 | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 86:35 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 86:35 | EqualityOperator | block.line <= 1 | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 86:51 | BlockStatement | {} | NoCoverage | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 89:21 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 89:21 | LogicalOperator | finite(block.endLine) \|\| block.endLine > block.line | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 89:46 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 89:46 | EqualityOperator | block.endLine >= block.line | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 92:19 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 92:19 | EqualityOperator | tops.length >= 0 | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 92:39 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 94:29 | EqualityOperator | index <= tops.length | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 95:15 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 100:5 | MethodExpression | raw | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 100:31 | LogicalOperator | left.y - right.y && left.line - right.line | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 100:31 | ArithmeticOperator | left.y + right.y | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 100:51 | ArithmeticOperator | left.line + right.line | NoCoverage | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 104:11 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 104:11 | LogicalOperator | point.y < last.y && point.line < last.line | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 104:11 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 104:11 | EqualityOperator | point.y <= last.y | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 104:31 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 104:31 | EqualityOperator | point.line <= last.line | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 105:11 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 105:11 | LogicalOperator | point.y === last.y \|\| point.line === last.line | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 105:11 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 105:11 | EqualityOperator | point.y !== last.y | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 105:33 | ConditionalExpression | true | NoCoverage | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 105:33 | EqualityOperator | point.line !== last.line | NoCoverage | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 108:12 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 108:12 | EqualityOperator | map.length >= 1 | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 112:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 112:9 | LogicalOperator | map.length === 0 && !finite(y) | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 112:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 113:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 113:9 | EqualityOperator | y < map[0].y | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 114:25 | EqualityOperator | index <= map.length | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 116:11 | EqualityOperator | y < next.y | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 118:13 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 122:16 | ArithmeticOperator | map.length + 1 | NoCoverage | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 126:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 126:9 | LogicalOperator | map.length === 0 && !finite(line) | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 126:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 127:9 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 127:9 | EqualityOperator | line < map[0].line | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 128:25 | EqualityOperator | index <= map.length | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 130:11 | EqualityOperator | line < next.line | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 132:13 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 136:16 | ArithmeticOperator | map.length + 1 | NoCoverage | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 142:12 | EqualityOperator | top <= offset | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 147:20 | EqualityOperator | y <= offset * 2 | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 228:47 | EqualityOperator | now >= expected.expiresAt | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 232:17 | ArithmeticOperator | Math.min(expected.fromLine, expected.line) + 1 | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 234:9 | EqualityOperator | topLine > low | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 234:27 | EqualityOperator | topLine < high | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 253:24 | MethodExpression | [...changes] | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 253:59 | ArithmeticOperator | right.startLine + left.startLine | Survived | no test kills it |  |
| src/core/scroll/anchorPolicy.ts | 255:9 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 12:25 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 14:5 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 15:5 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 20:3 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 27:4 | Regex | / {0,3}<(?:script\|pre\|style\|textarea)(?:\s\|>\|$)/iu | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 27:4 | Regex | /^ {0,3}<(?:script\|pre\|style\|textarea)(?:\s\|>)/iu | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 27:4 | Regex | /^ {0,3}<(?:script\|pre\|style\|textarea)(?:\S\|>\|$)/iu | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 28:4 | Regex | / {0,3}<!--/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 29:4 | Regex | / {0,3}<\?/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 29:4 | Regex | /^ <\?/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 30:4 | Regex | / {0,3}<![A-Za-z]/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 30:4 | Regex | /^ <![A-Za-z]/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 30:4 | Regex | /^ {0,3}<![^A-Za-z]/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 31:4 | Regex | / {0,3}<!\[CDATA\[/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 31:4 | Regex | /^ <!\[CDATA\[/u | Survived | killed only by another layer | page/tableBreakout.test.js::an editor opened on a paragraph does not measure the tables again; one opened on a table does |
| src/core/syntax/blockQuoteRange.ts | 37:3 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 39:21 | Regex | / {0,3}#{1,6}(?:[ \t]\|$)/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 39:21 | Regex | /^ {0,3}#(?:[ \t]\|$)/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 42:24 | Regex | /^ {0,3}(?:(?:\*[^ \t]*){3,}\|(?:-[ \t]*){3,}\|(?:_[ \t]*){3,} | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 42:24 | Regex | /^ {0,3}(?:(?:\*[ \t]*){3,}\|(?:-[ \t]){3,}\|(?:_[ \t]*){3,})$ | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 45:23 | Regex | /^ {0,3}\\|?[ \t]*:?-+:?[ \t]*(?:\\|[ \t]*:?-+:?[ \t]*)*\\|?[^  | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 47:27 | Regex | /^ (?:[-*+]\|1[.)])[ \t]+\S/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 47:27 | Regex | /^ {0,3}(?:[-*+]\|1[^.)])[ \t]+\S/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 47:27 | Regex | /^ {0,3}(?:[-*+]\|1[.)])[ \t]\S/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 47:27 | Regex | /^ {0,3}(?:[-*+]\|1[.)])[ \t]+\s/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 49:21 | Regex | /^ {0,3}(?:[-*+]\|\d[.)])(?:[ \t]\|$)/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 50:29 | Regex | /^ {0,3}(?:[-*+]\|\d[.)])[ \t]+\S/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 50:29 | Regex | /^ {0,3}(?:[-*+]\|\D{1,9}[.)])[ \t]+\S/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 50:29 | Regex | /^ {0,3}(?:[-*+]\|\d{1,9}[^.)])[ \t]+\S/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 50:29 | Regex | /^ {0,3}(?:[-*+]\|\d{1,9}[.)])[ \t]\S/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 52:25 | Regex | / {0,3}(?:[-*+]\|\d{1,9}[.)])[ \t]*$/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 52:25 | Regex | /^ {0,3}(?:[-*+]\|\d{1,9}[.)])[ \t]*/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 52:25 | Regex | /^ (?:[-*+]\|\d{1,9}[.)])[ \t]*$/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 52:25 | Regex | /^ {0,3}(?:[^-*+]\|\d{1,9}[.)])[ \t]*$/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 52:25 | Regex | /^ {0,3}(?:[-*+]\|\d[.)])[ \t]*$/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 52:25 | Regex | /^ {0,3}(?:[-*+]\|\D{1,9}[.)])[ \t]*$/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 52:25 | Regex | /^ {0,3}(?:[-*+]\|\d{1,9}[^.)])[ \t]*$/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 52:25 | Regex | /^ {0,3}(?:[-*+]\|\d{1,9}[.)])[ \t]$/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 52:25 | Regex | /^ {0,3}(?:[-*+]\|\d{1,9}[.)])[^ \t]*$/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 54:26 | Regex | / {0,3}\+{3}/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 54:26 | Regex | /^ {0,3}\+/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 55:18 | Regex | /(?: {4}\|\t\| {1,3}\t)/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 55:18 | Regex | /^(?: \|\t\| {1,3}\t)/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 55:18 | Regex | /^(?: {4}\|\t\| \t)/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 59:7 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 66:24 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 71:14 | MethodExpression | row | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 72:7 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 72:7 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 72:7 | MethodExpression | text.endsWith("\|") | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 72:23 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 72:36 | MethodExpression | text | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 73:7 | ConditionalExpression | true | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 73:7 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 73:7 | LogicalOperator | text.endsWith("\|") \|\| !text.endsWith("\\\|") | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 73:7 | MethodExpression | text.startsWith("\|") | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 73:21 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 73:29 | BooleanLiteral | text.endsWith("\\\|") | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 73:30 | MethodExpression | text.startsWith("\\\|") | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 73:44 | StringLiteral | "" | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 73:59 | MethodExpression | text | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 86:10 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 86:10 | LogicalOperator | HTML_BLOCK_START.test(line) && kind7 && HTML_BLOCK_7.test(li | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 86:42 | ConditionalExpression | false | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 91:20 | Regex | /[ \t]*/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 91:20 | Regex | /^[ \t]/u | Survived | no test kills it |  |
| src/core/syntax/blockQuoteRange.ts | 91:20 | Regex | /^[^ \t]*/u | Survived | no test kills it |  |

63 more row(s): see summary.json.

## Test files left out

None: all 144 test files ran.
