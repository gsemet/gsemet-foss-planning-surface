Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.6 completeness audit (critical)

Auditor: Sonnet, read-only. Worktree `markdown-okf-schema-studio-wt-059-b3`, branch `changes-requests/059-requirements-batch3`, head `c19ae3e`.
Tools: `okfreq validate requirements --prose --check-links --project-root .` (2144 requirements, 0 errors, 0 warnings),
`okfreq update-coverage requirements --check` (0 files would change), `okfreq trace requirements --json`, plus scripted
checks over the requirement files, the 869 checklist rows, the 920 inventory F lines and every marker in `src/`, `test/`, `sphinx/`.
Machine output kept in `/private/tmp/claude-502/-Users-az02065-Projects-Nestor-agentic-coding-white-paper/dd375646-4450-4e52-a643-89ff1d9e405a/scratchpad/audit/`
(`p1.json` structure checks, `crow.json` checklist-row mapping, `fmap.json` F-line mapping, `markers.json`, `allm.json`, `sample.json`).

Verdict: FIX-REQUIRED

Active = every requirement whose lifecycle is not `deprecated`: 228 StRS, 1863 SwRS (53 deprecated: 2 StRS, 51 SwRS).
The baseline is structurally clean and the coverage numbers hold, but the verification notes contradict the markers for
at least 163 SwRS, the checklist trace column was never filled, 27 SwRS (22 + 5) have no marker and no exemption, one test
marker points to a deprecated StRS, and 181 markers sit in companion files that are not at the code or test.
12 numbered defects follow (3 high, 5 medium, 4 low).

## 1. Scripted structure checks (item 1)

| Check | Result |
| --- | --- |
| Active SwRS with `derives_from` pointing to an existing, active StRS | 1863/1863 pass (0 missing, 0 to a deprecated StRS) |
| Active StRS with at least one active SwRS | 228/228 pass |
| Active text citing a deprecated or unknown id (body, description, repo docs, README, CHANGELOG, CONTRIBUTING) | 0 |
| Placeholder (`<...>`, TODO, TBD, "Verification pending", "EARS Expression") | 0 real. 155 raw `TODO` hits are the TODO palette action / TODO word chip in 29 requirements (feature name); one `<jar>` in StRS-DIAG-012 is a literal command-line argument in backticks. No fix needed. |
| `title` equals first `##` heading | 2091/2091 pass |
| `description` equals the Normative behavior sentence (SwRS) | 1838/1863; 25 fail: D8 |
| Exactly one SHALL per SwRS | 1817/1863; 46 have two (D9); 6 StRS have two |
| At least two scenarios per SwRS | 1862/1863; SwRS-TRUST-071 has one (D7) |
| Scenario has GIVEN, WHEN and THEN | all pass |

## 2. Checklist to SwRS coverage (item 2)

Method (and its limits). The `SwRS` column of all 869 checklist rows is empty and 8 of the 16 inventories have no `Requirement id`
column, so no recorded row-to-SwRS link exists; I rebuilt it three ways and took the union:
1. `C-VIS`: scenario id in the row, mapped through `SCENARIO_ID_BY_LEGACY_ID` to the scenario entry, then the `@tests_req SwRS-` lines
   directly above that entry (55 of 320 rows resolve this way).
2. `C-MSG/PAL/SLASH/PKG/TB/CTL/INT`: the backticked identifier or quoted label of the row looked up in the text of the active SwRS (or, for `C-INT`, the
   test file looked up in `tested_in_files`). 236 rows resolve.
3. Row to inventory F line (the F lines cite the C ids in their Checklist column: 844 of 869 rows are cited, 25 are not), then F line to SwRS: the explicit
   `Requirement id` column when present (168 F lines, all active), otherwise the best IDF-weighted word overlap with each active SwRS plus the overlap of
   evidence file paths with `implemented_in_files`/`tested_in_files`. On the 168 F lines that have an explicit id the method puts the right SwRS first for 164 and in the top 3 for all 168.
Limits: step 3 is similarity, not a recorded decision; compound F lines (several behaviours) map to the one best SwRS, and below a score of 0.6 the best match is
sometimes only a neighbour (checked by hand on 14 random cases between 0.45 and 0.6: 5 correct, 8 partial, 1 wrong; in every partial or wrong case a better atomic SwRS existed: Image
button is PALETTE-109/110, post-edit scroll pin is BLOCK-228/229). No content check of the matched SwRS against the full row text was done for all 869 rows.

Result: 818 of 869 rows have at least one strong match to an active SwRS. 51 rows have none, and I checked each by hand:

- 36 are process, CI, release or tooling rows that have no product behaviour (no SwRS expected, but none is recorded as `n/a: reason`):
  AR-066, 067, 080, 112, 115, 116, 118, 119, 120, 130, 131, 132, 133, 135, 136, 137, 143, 146, 148, 149; CL-048, 049, 050, 068, 069, 070, 071, 072, 073, 074, 075, 084, 087, 089; INT-004 (cited only by the "skip: tooling" F-CORE-045); and
  AR-049 (uncited by any F line; the include line mapping is covered by CORE-015).
- 15 are product rows with a weak or composite link, all with an active SwRS found by hand: PKG-009, 010, 011, 012 (LIFE-001), PKG-031 (LIFE-002), PAL-029 (PALETTE-140),
  AR-065 (LIFE-027), AR-081 (BLOCK-032), VIS-002, 012, 043, 045, 047, 049 (composite scenarios F-CORE-029/031, "skip: composite", covered by CORE-002/021/022/006/057 and the layout-width overflow SwRS),
  VIS-227, 228, 229 (TOC gallery F-TOOLBAR-026, covered by TOOLBAR-033 to 053, LAYOUT-023/024).
No checklist row was found whose product behaviour has no active SwRS. Weak spots to keep in mind: the host-to-page result messages
`previewCheckboxResult`, `previewCommentResult`, `previewFrontmatterResult`, `previewListCitationsResult`, `previewPickDocumentResult`, `previewPasteImageResult`,
`previewPasteHtmlResult` (C-MSG-037, 038, 042, 054, 055, 057, 071) are not named by any SwRS (their behaviour is covered under other titles: GFM-023/024, REVIEW-053, FMEDIT-022, PALETTE-172/201/202);
slash variants C-SLASH-003..045 (Heading 3/4, alerts, 8 admonition kinds) rest on the one aggregate PALETTE-262.
The recorded trace is the defect (D2), not the coverage.

## 3. Marker sample, 60 SwRS stratified over 16 scopes (item 3)

Seed 59; 4 per scope (3 for rendering-core, code-blocks, gfm, myst); the first pick of each 4-scope draw is forced to an "Untested" Method where one exists. For each I read the
SwRS sentence, the code after the `@implements_req` line and the test after the `@tests_req` line.

Sound (marker at the code or test of that behaviour, test fails if the behaviour breaks): 40 of 60, 13 of them with a stale Verification note, namely (Method says "Untested" or "to be added" while a real test exists): BLOCK-073, BLOCK-025, BLOCK-173, DIAG-040, DIAG-093, LIFE-005, REVIEW-198, TABLE-012, THEME-023, TOOLBAR-095, TOOLBAR-082, TRUST-088, TRUST-051 (13; D1).
The other 20 are not clean:

| SwRS | Problem |
| --- | --- |
| TABLE-065 | Test marker is on a test of the small bar only; the SwRS is the tall-bar branch (over 40 percent of the viewport stays put) and the Method itself says the branch "has no dedicated test". The test would not fail if the tall-bar branch broke. |
| BLOCK-251 | Impl marker is at line 8 of `src/core/preview/styles/editModeStyles.ts`, above the file header comment, not at the status-wrap rule. Test marker is the visual scenario `edit-affordances-narrow` whose only machine check is `overlay-clipped`; the wrap below the status line is not asserted. |
| FMSCHEMA-063 | Second test marker (`test/integration/previewEditing.test.ts:257`) is above `export async function run()`, a suite of 1000+ lines; nothing there ties it to the focusable link and tooltip. First marker (`propertiesTable.test.ts:98`) is right. |
| GFM-022 | Test marker is above `run()` of `test/integration/checkboxToggle.test.ts` (whole suite); the "single undo step" is not located. |
| DIAG-003 | Visual scenarios `diagrams/v01..v03` only show a loaded image; alt text "Mermaid diagram", data URI and `data-render-state` are not asserted by any machine check (only the error scenario has `img.myst-mermaid-image` count 0). |
| CODE-002 | Test covers the alias `py` only; the SwRS lists py, js, sh, rs, patch. |
| GFM-038 | Test removes `script`; the SwRS lists script, style, iframe, svg, form, embed, object. |
| FMEDIT-049 | Test checks the accept and the refuse branches of `checkFrontmatterCandidate`, not the "other fields or links may be wrong" tolerance that is the SwRS. Partial. |
| LAYOUT-007, LAYOUT-008, THEME-025, THEME-037, TOOLBAR-034 | Impl marker sits at the head of a stylesheet-part module or a large UI module (`contentLayoutStyles.ts` 9/10, `pageChromeStyles.ts` 6/14, `tocColumn.ts` 9), not at the rule or function. Accepted by okfreq, weak as a locator (D6). |
| PALETTE-045, PALETTE-046, PALETTE-131, PALETTE-154, TABLE-076, FMSCHEMA-021 | The `@tests_req` is in a `*.markers.ts` companion that holds only `export {}` (D5). The paired test exists and is right where I checked (T28 admonition, bold/italic rows). |
| MYST-006 | Seven SwRS (MYST-001, 004, 006 to 010) stack on the one `name: "admonition"` plugin entry; correct plugin, coarse. The test marker sits on the test named "nested backtick and colon delimiters" whose second half asserts the nested tip inside the note: correct, misleadingly named. |

So the hard failures in the sample: TABLE-065 (test), BLOCK-251 (locator and test), FMSCHEMA-063 and GFM-022 (suite-level marker), DIAG-003 (assertion missing). No marker in the sample sits between a doc comment and its declaration or in a template literal.

## 4. Marker hygiene (item 4)

Scan of `src/`, `test/`, `sphinx/` with a JS-aware tokenizer (strings, template literals with `${}`, regex literals, comments), 4445 marker lines.
- Not at line start or in a string: 3, all fixtures inside `test/core/navigation/previewNavigation.test.ts:33-35` (`"# @implements_req SwRS-1"`), ignored by okfreq (trace `missing_ids` is empty). Fine.
- Inside a template literal that makes HTML/CSS: 0. (A first pass flagged 75 because of a backtick in a regex literal such as `/[`<>]/`; re-run with regex awareness: 0.)
- Marker between a closing `*/` and its declaration, or followed by a blank line or closer: 0. 976 markers sit directly above a `/** ... */` block (correct form).
- `/** @tests_req` on a JSDoc opening line: 0.
- Duplicate id in one file: 0 (trace `duplicates` is 0).
- Unknown id: 0. Deprecated id: 1 (`StRS-MDOKFSTUDIO-LIFE-019` at `test/integration/realWindowGaps.ts:303`, D4). Marker on `@implements_req` for an StRS: 0. `@tests_req` outside `test_dirs`: 0.
- `trace` `non_leaf` 0, `missing_ids` 0, `warnings` 0. Frontmatter `implemented_in_files`/`tested_in_files` equal the trace for all 1863 SwRS.
- Files per type of anchor: 149 `@implements_req` sit within the first 20 lines above a `/**` (74 of them are the CSS-in-TS style parts `pageChromeStyles.ts` 17, `editModeStyles.ts` 14, `contentLayoutStyles.ts` 18, `contentBlockStyles.ts` 17, `commentStyles.ts` 5 and three more: file-level locators, D6);
  96 `@tests_req` sit above `export async function run()` of integration suites (`previewEditing.test.ts` 26, `previewHistory.test.ts` 13, `scroll-sync-suite.ts` 12, `lifecycle.test.ts` 8 ...) and 104 + 77 above visual scenario entries (correct form).
- Companion files: there are FIVE `*.markers.ts`, not four: `src/page/modules/editPalette.markers.ts` (39 `@implements_req`), `src/page/modules/plantumlBundle.markers.ts` (1), `test/page/modules/editActions.markers.ts` (94 `@tests_req`),
  `test/core/frontmatter/okfFrontmatter.markers.ts` (36), `test/integration/realInput.markers.ts` (96, 9 of them StRS). All are valid (comment lines then `export {};`, ids exist, kinds match their directory).
  The size-limit rationale holds for four (editPalette.ts 766 lines + 39 markers passes 800; okfFrontmatter.test.ts 1468, editActions.test.ts 1438, realInput.test.ts 4580 are at the 1500 ratchet).
  `plantumlBundle.markers.ts` has a different rationale (esbuild output outside the marker dirs), which is acceptable but not "the size limit". They are referenced only by their own header comments and the generated `implemented_in_files`/`tested_in_files`; neither `requirements.guidelines.md` nor CONTRIBUTING mentions the mechanism (D5).
  Effect: 147 SwRS have their only `@tests_req` in a companion (34 SwRS their only `@implements_req`), so the marker is not "at the code/test" required by constitution section 1.

## 5. Statistics (item 5)

Columns: active StRS, active SwRS, deprecated (StRS+SwRS), SwRS with a Known issue, SwRS whose Method starts with "Untested" although a test marker exists, SwRS without `@implements_req`, SwRS without `@tests_req`, StRS with a stakeholder validation test.

| Scope | StRS | SwRS | Deprecated | Known issue | "Untested" Method | No impl marker | No test marker | StRS validated |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| block-editing | 25 | 241 | 13 | 18 | 41 | 1 | 0 | 23/25 |
| code-blocks | 4 | 38 | 0 | 3 | 0 | 0 | 0 | 4/4 |
| diagrams | 14 | 119 | 1 | 70 | 0 | 1 | 5 | 11/14 |
| frontmatter-editing | 11 | 85 | 2 | 15 | 0 | 0 | 0 | 9/11 |
| frontmatter-schema | 18 | 89 | 0 | 29 | 0 | 1 | 0 | 15/18 |
| gfm | 4 | 38 | 0 | 3 | 0 | 0 | 0 | 4/4 |
| layout-width | 9 | 42 | 0 | 34 | 0 | 1 | 0 | 9/9 |
| lifecycle-sync | 22 | 155 | 14 | 9 | 40 | 8 | 0 | 18/22 |
| myst | 14 | 95 | 0 | 2 | 0 | 2 | 0 | 13/14 |
| palette-slash | 27 | 272 | 2 | 12 | 0 | 0 | 0 | 13/27 |
| rendering-core | 5 | 67 | 1 | 2 | 0 | 0 | 0 | 3/5 |
| review-annotations | 18 | 215 | 2 | 3 | 24 | 0 | 0 | 16/18 |
| table-editing | 15 | 122 | 7 | 13 | 0 | 0 | 0 | 10/15 |
| theme-zoom | 13 | 54 | 4 | 2 | 8 | 0 | 0 | 6/13 |
| toolbar-navigation | 14 | 146 | 3 | 12 | 30 | 0 | 0 | 12/14 |
| trust-security | 15 | 85 | 4 | 10 | 20 | 8 | 0 | 3/15 |
| **Total** | **228** | **1863** | **53** | **237** | **163** | **22** | **5** | **169/228** |

- Known issues: 237 active SwRS contain the words "Known issue" (185 in a `### Known issues` section, 23 appended inside the Normative behavior paragraph, the rest in the body). Highest: diagrams 70, layout-width 34, frontmatter-schema 29.
- Untested or weak: 5 SwRS have no test marker and a true "no test" Method: DIAG-012, 013, 014, 031, 116. 163 say "Untested" with a test marker present (listed in D1). 159 SwRS (CORE 66, MYST 93) have the bare Method "test" (D10).
  The gap report's "tests that only approximate the requirement" list stays valid (CORE-030, 039, 046; BLOCK-019, 090, 113; FMEDIT-051, 055; TABLE-072; TOOLBAR-087, 130, 149; LIFE-005, 031, 105, 154, 165; THEME/LAYOUT-040, 045), plus the sample findings above.
- Coverage by marker (trace): implemented 1841/1863 (98.8 percent), tested 1858/1863 (99.7 percent). StRS with a validation test 169 of 228 active (gap-report.md still says 144/230 and a list of 86: stale, D11).

## Defects

### High

D1. Verification notes contradict the markers: 163 SwRS still say "Untested..." in `- Method:` although a `@tests_req` exists (158 of them point to a `*.requirements.test.ts` written in commit fed4181). Commit d38b7bc corrected only part of them.
Sample proof: BLOCK-173 ("no test edits the document during the clipboard write", test `a cut is refused when the document changed while the clipboard was written`), BLOCK-025, DIAG-040 ("to be added", test `the built-in result cache keeps 64 results...`), TRUST-071, TABLE-012.
A further 74 active SwRS have "no test / no dedicated test / to be added" wording in a Method that does not start with "Untested" (e.g. DIAG-020, 051, 090, 096, 098, 099, 104, 105, 117, LIFE-062, 072, 098, 162, TOOLBAR-027, 127, THEME-016, 022, 038, FMEDIT-058, TRUST-002): re-read these too.
Fix: for each id below edit the SwRS body (authored text, not generated fields): replace the Method line with `Unit test <exact test name> in <file>` and keep an "Untested:" sentence only for the branch that still has no assertion (name the branch). Do not touch `tested_in_files`.
IDs (163): BLOCK-006,010,011,015,018,019,024,025,039,040,046,048,054,072,073,082,083,113,122,128,135,172,173,177,178,182,188,199,200,210,215,216,217,218,220,222,223,225,226,229,231; LIFE-001,002,005,007,009,010,013,022,023,028,030,031,034,035,045,046,047,051,053,055,057,063,064,065,066,067,068,075,107,114,115,129,130,138,144,145,147,154,155,165; REVIEW-010,016,022,026,062,064,066,122,123,124,127,128,129,148,155,180,181,182,183,184,197,198,199,213; THEME-009,014,015,023,045,050,054,057; TOOLBAR-016,017,020,030,063,064,074,075,076,078,082,087,095,096,097,101,109,112,113,114,115,116,129,130,141,142,144,146,148,149; TRUST-010,016,017,018,021,022,028,032,039,042,048,051,065,067,068,069,071,079,087,088.
Keep as is (true): DIAG-012, 013, 014, 031, 116.

D2. The traceability record of the baseline is missing: (a) the `SwRS` column of all 869 checklist rows in `.agents/changes/requests/059-requirements-okfreq/checklists/*.md` is empty although `checklists/index.md` says every item must map to a SwRS or `n/a: <reason>` before P10.6 can close;
(b) 8 inventories (`block-editing`, `lifecycle-sync`, `palette-slash`, `review-annotations`, `table-editing`, `theme-zoom`, `toolbar-navigation`, `trust-security`) have no `Requirement id` column, so 552 F lines (plus 9 in rendering-core and 1 in code-blocks without an id) have no F-to-SwRS link; 10 F lines say "skip".
Fix: fill the `SwRS` column from `crow.json` (scratch path above, per row: the ids found by method, with `how`), review the 36 process rows and write `n/a: process/CI/release/tooling` for them (ids in section 2), and add the missing `Requirement id` column to the 8 inventories from `fmap.json` (top match, reviewed for scores under 0.6; 43 F lines score under 0.45 and need a manual look: F-LIFE-081 to 086, F-TRUST-050, 058, 062, 067, F-BLOCK-072, F-TOOLBAR-026, F-PALETTE-016, 048, 059, 062, 074 among them).
These documents are outside git, so this is a CR-folder fix, not a PR change; do it before the PR text claims "every checklist item traced".

D3. Non-exempt SwRS without a marker (27): no `@implements_req` on LIFE-002, 014, 015, 016, 017, 149, 167, 168; TRUST-070, 071, 074, 075, 076, 077, 078, 080; MYST-052, 095; DIAG-079; LAYOUT-035; FMSCHEMA-028; BLOCK-007 (22), and no `@tests_req` on DIAG-012, 013, 014, 031, 116 (5). `annotation_exemption` is false everywhere, so `okfreq report` counts them as gaps and the guideline says traceability must not be claimed.
The gap report leaves it as "Decision needed". Fix (decision for the user, recommended): set `annotation_exemption: true` with `exemption_reason` on the 22 declarative or negative-rule SwRS (package.json, `.nvmrc`, lock file, `.vscodeignore`, `esbuild.mjs`, icon, absence of code in BLOCK-007, FMSCHEMA-028, LIFE-149, TRUST-070; test tooling in LAYOUT-035; library output in MYST-095; whole renderer in MYST-052) or give each a marker in the real source. For the 5 DIAG ids write the browser tests (Mermaid entry point queue, unique ids, late results; built-in engine request log) or exempt them with a reason; keep their Method "No test" until then.

### Medium

D4. `test/integration/realWindowGaps.ts:303`: `// @tests_req StRS-MDOKFSTUDIO-LIFE-019` points to a deprecated StRS (its duplicate owner is `StRS-MDOKFSTUDIO-TRUST-001`, "preview in an untrusted workspace"). Fix: change the id on that line to `StRS-MDOKFSTUDIO-TRUST-001` (keep line 302 `StRS-MDOKFSTUDIO-BLOCK-002`); run `okfreq update-coverage requirements`. Check that the other markers of that file still resolve (trace: 0 missing).

D5. Companion marker files break the anchor rule (constitution section 1): 147 SwRS have their only `@tests_req` and 34 their only `@implements_req` in a `*.markers.ts` that contains no code or test. There are five companions, not four, and none is documented in `requirements.guidelines.md`.
Fix: (a) add a section "Companion marker files" to `requirements/guidelines/requirements.guidelines.md`: allowed only while the host file is at its size limit, name the host file in the header, and list the five files; (b) add a `just check` step (or a case in `scripts/check-file-sizes.mjs`) that fails when a companion's host file is below the limit that justified it (editPalette.ts below 760 lines, okfFrontmatter.test.ts below 1460, editActions.test.ts below 1400) so the markers move home at the next split;
(c) state in the `plantumlBundle.markers.ts` header that the reason is the esbuild entry, not the size limit (already true in its text; just do not describe all as size limit). Splitting the three test files and `editPalette.ts` is the real fix and belongs to the refactoring backlog.

D6. Coarse locators. 74 `@implements_req` sit at the head of the five style-part modules (`src/core/preview/styles/pageChromeStyles.ts`, `editModeStyles.ts`, `contentLayoutStyles.ts`, `contentBlockStyles.ts`, `commentStyles.ts`), and 96 `@tests_req` above the whole `run()` of integration suites.
Fix: for the style parts, add the marker at the named rule block when the CSS is a separate exported constant per section (`export const X_CSS = ...` split), else keep and note the limit in the guideline; for the integration suites move each marker to a comment line inside `run()` immediately before the step that asserts the behaviour (e.g. GFM-022 in `test/integration/checkboxToggle.test.ts`, FMSCHEMA-063 in `test/integration/previewEditing.test.ts`). Do the sample cases first: GFM-022, FMSCHEMA-063, BLOCK-251, LAYOUT-007/008, THEME-025/037, TOOLBAR-034.

D7. TABLE-065 and SwRS-TRUST-071.
TABLE-065: the marked test (`test/page/runtimeTableCellEditor.test.ts:277`) exercises the small bar; the SwRS is the tall bar. Fix: add a test with `tableMenu.height` over 40 percent of the viewport asserting the bar keeps its place, or keep the marker and change the SwRS text to what the test shows and move the tall-bar rule to a new SwRS with no test marker.
TRUST-071: one scenario instead of two. Fix: add `### Scenario: Boundary or refusal` (GIVEN a manifest that gains a capabilities key, WHEN the key set is read, THEN the check fails) to `requirements/tiers/swrs/trust-security/SwRS-MDOKFSTUDIO-TRUST-071.md`. Also: the Method says "Untested: ... never capabilities" but the marked test `test/security/trustReq.requirements.test.ts:310` asserts exactly `"capabilities" in manifest === false` (D1).
Also BLOCK-251 and DIAG-003 are visual-only with a missing assertion: add a content assertion in `test/visual/scenarioAssertions.ts` (status line above the buttons at 460 px; `img.myst-mermaid-image[alt="Mermaid diagram"]` with a `data:image/svg+xml` source and `data-render-state=rendered`).

D8. 25 SwRS where `description` differs from the Normative behavior sentence. 23 have a "Known issue: ..." paragraph appended inside Normative behavior, which also makes the SwRS read as two normative statements: CORE-014, CORE-027, FMEDIT-002, 007, 009, 010, 014, 015, 021, 023, 034, 037, 047, 050, 061, 073, 083, CODE-017, 026, 027, GFM-024, 026, 027 (the other 185 use `### Known issues`).
Fix: move the "Known issue" paragraph under `### Known issues` for these 23. MYST-043 has a second explanatory paragraph in Normative behavior (move to Rationale or Verification notes). LAYOUT-017: the frontmatter `description` was folded at the hyphen and reads `--sphinx- preview-toolbar-bottom`; rewrite the description as a quoted or `>-` scalar so it reads `--sphinx-preview-toolbar-bottom`, and regenerate the index with `okfreq lint requirements`.

D9. 46 SwRS carry two SHALL in the sentence (mostly "SHALL X, and SHALL NOT Y" or two actions). Per guideline one bounded behaviour. List: CORE-018, CORE-029, CORE-047, CORE-032, CORE-063, CORE-027, CORE-066, CORE-033, CORE-065, CORE-055, DIAG-004, DIAG-024, DIAG-051, DIAG-011, DIAG-087, DIAG-025, DIAG-035, DIAG-044, DIAG-015, DIAG-088, DIAG-089, DIAG-018, DIAG-028, DIAG-029, DIAG-108, DIAG-002, DIAG-022, DIAG-047, DIAG-090, DIAG-032, DIAG-091, DIAG-033, DIAG-102, DIAG-003, DIAG-112, TABLE-075, TABLE-124, TABLE-066, TABLE-023, GFM-032, GFM-008, GFM-018, GFM-034, CODE-013, CODE-018, CODE-021.
Fix: for each, either keep one SHALL (turn the second into "and does not ...") or split into two SwRS with `okfreq new swrs` and move the markers/tests (several are one behaviour with its refusal, e.g. TABLE-075/124, DIAG-088/089/090/091; accept those and change the guideline wording instead if the maintainer prefers "affirmative plus its refusal" as one SwRS).

### Low

D10. 159 SwRS have the bare Method `test` (CORE 66, MYST 93: every CORE and MYST SwRS written in batch 1). Fix: name the test file and test name, e.g. MYST-006 `test/core/render/mystFeatures.test.ts` "nested backtick and colon delimiters preserve their enclosing Markdown" (rename that test to say nested admonitions).

D11. `gap-report.md` is stale against `trace`: it lists 86 StRS without a validation test and 144/230 (62.61 percent); the trace now shows 169 of 228 active StRS with a validation test and 59 without. Fix: regenerate the section from `okfreq generate-report` and the list from `validation_tests`.

D12. `requirements/tiers/log.md` has no entry for the marker, test and exemption commits (24a4299, 0ca2961, fed4181, 8390c86, d38b7bc, c19ae3e); the newest entry (2026-10-25 batch 4) still says "No traceability markers yet". Fix: add a dated entry listing the coverage numbers (implemented 1841/1863, tested 1858/1863), the new `*.requirements.test.ts` files, the five companion files and the exemption decision.

## Three most serious
1. D1: 163 (up to 237) SwRS say "Untested" or "to be added" while a test marker points to a test that does exercise it; the verification notes cannot be trusted as written.
2. D2: the checklist to SwRS trace (the point of P10.6) was never recorded: 869 empty SwRS cells and 552 F lines with no requirement id; my rebuilt mapping finds no product row without an SwRS but it is not a recorded decision.
3. D3: 27 non-exempt SwRS have no marker, so the traceability claim is false until the user decides exemption or markers; with D4 (marker on deprecated StRS-LIFE-019) and D5 (181 markers detached in companion files) this keeps the baseline below the constitution section 1 contract.
