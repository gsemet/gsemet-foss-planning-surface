# Investigation CR-345 (read only; worktree `batch-06-CR-345`, HEAD db9e4560 = CR-342 branch)

Environment: the worktree has an EMPTY `.venv` and no `node_modules`; `just dev` was NOT run. okfreq
(okf-schema 0.17.0) exists only in the main checkout's `.venv` (used for `--help` only). `just` and
`node` are on PATH; `npm` is not (the justfile uses `fnm exec -- npm.cmd`). The Coder needs `just dev`
before any `okfreq`, `check-markers` (needs the `yaml` npm package) or `just check`.

## 1. Marker rules (CR-340 gate, CR-342 diagrams)

Source: `scripts/check-marker-companions.mjs` (header), `requirements/guidelines/project.guidelines.md`
("Marker placement", "Use case diagram of a StRS", "Main paths of a StRS").

- **Marker block**: markers with no CODE line between them; blank lines and comment lines (`//`, `#`,
  `/*`, `*`, `<!--`, or ending `*/` / `-->`) do NOT end a block; only a code line does. At most **3
  distinct IDs per block**, in every tracked file under the source and test dirs (all scopes: `src`,
  `sphinx`, `skills`, `test`, `sphinx/tests`). StRS and SwRS IDs both count. Move a marker = put it on
  another declaration, or inside the test body (a statement line separates the blocks).
- **Rule 1**: every in-force (`draft|proposed|approved`) SwRS with `annotation_exemption != true` has
  its ID in an `@implements_req` line under `src`/`sphinx`/`skills` (companions count). No baseline.
  => each NEW SwRS needs an implementation marker or `just check-markers` fails at once. Superseded
  SwRS drop out of the rule.
- **Companion file**: `src/**` or `test/**` file named `*.markers.ts`, or containing a
  `// Companion of: <path>` line. Only comment lines and `export {};`; at least one marker; the host
  exists; every ID exists in `requirements/tiers/`. Line format (rule 3):
  `// @tests_req <ID> — <scenario>` or `// @implements_req <ID> — <code point>` (separator is
  space, em dash U+2014, space); the name must occur as TEXT in the host file or in a file directly in
  the host's folder. A companion with all lines named is not held to the 3-ID limit. Worked example
  (`src/core/render/siteTheme.markers.ts`):
  ```
  // Companion of: test/site/siteTheme.ts
  // Requirement markers for ...
  // @implements_req SwRS-MDOKFSTUDIO-CORE-086 — SITE_CSS
  export {};
  ```
  Use for CSS template strings (a marker cannot sit inside one) -> a companion
  `src/core/preview/styles/pageChromeStyles.markers.ts` with `— --sphinx-preview-zoom`-style code points.
- **Baseline** `scripts/marker-baseline.json`: `{ "description", "limit": 3, "blocks": { "<file>": <sum of
  IDs over its over-limit blocks> }, "unnamedCompanionLines": { "<file>": <count> } }`. Ratchet: a listed
  file may only shrink; check FAILS when a file shrank (stale) or is clean/gone, until you run
  `node scripts/check-marker-companions.mjs --update` (lowers or removes, never raises). Worked example:
  `test/integration/paletteMode.test.ts:39-42` holds StRS-PALETTE-002, LIFE-169, PALETTE-010, LIFE-170
  = 4 IDs (baseline 4); after PALETTE-010 is superseded and its marker dropped = 3 IDs, so the entry is
  REMOVED.
- **CR-342 diagram**: authored `### Use case diagram` heading, exactly one ```` ```mermaid ```` fence plus
  an optional one-line caption sentence; before `### Main paths` (Main paths stays the last authored
  section, before `<!-- okf:links:start -->`). Kinds: `sequenceDiagram` (default), `flowchart` (actors
  diagram, one node per role), `stateDiagram-v2` (mode). No PlantUML. No SwRS ID in the diagram. Not
  linted (optional rule, okfreq accepts it). The site build fails with the StRS id if Mermaid cannot draw
  the fence. No StRS in the repo carries one yet (this CR is the first user). Worked example:
  ```
  ### Use case diagram

  ```mermaid
  sequenceDiagram
    actor W as Writer
    participant P as Palette
    participant T as Text box
    W->>P: press Bold
    P->>T: wrap the selection in ** (one native edit)
    alt nothing to wrap
      P-->>W: status line gives the reason
    end
  ```
  ```
- **Main paths** (CR-341 landed, commit 9bae4f9a): `scripts/check_main_paths.py` accepts a cited SwRS that
  derives from the StRS OR is in the StRS's `depends_on`. Cited SwRS must be active (not superseded).

## 2. okfreq usage (okf-schema 0.17.0)

- New: `uv run --no-sync --group requirements okfreq new strs "<title>" --description "<EARS ... SHALL ...>"
  --project markdown-okf-schema-studio --scope palette-slash --user-need "<need>" --lifecycle proposed
  --path requirements` (`new swrs` same, no `--user-need`; `--derives-from` is REPEATABLE:
  `--derives-from StRS-...A --derives-from StRS-...B`). The command prints the created path and the
  new ID (next number above the highest ever used; PALETTE SwRS next is 276+). Record each new ID in
  `work/` at once, round 2 needs them.
- Supersede: `okfreq supersede OLD NEW [NEW...] --path requirements --yes` (sets
  `req_lifecycle: superseded`, `superseded_by` list; refuses unknown IDs, self, repeats, cycles). Then
  `okfreq update-coverage` refreshes the generated `supersedes`. Archive: `okfreq archive ID --path
  requirements --yes` (deprecated). There is NO `okfreq update`.
- Recipes (justfile): `just requirements-lint` = `okfreq validate requirements --check-links
  --project-root .` + `okfreq lint requirements --check --check-links --project-root .` + `okfreq
  update-coverage requirements --check` + `python scripts/check_main_paths.py requirements`.
  `just requirements-update` = `okfreq update-coverage requirements` + `okfreq lint requirements --prose
  --check-links --project-root .` (writes generated fields/indexes/Links). `just check-markers` = `npm run
  check:markers`. They run in the worktree only after `just dev` (uv sync --group requirements, npm ci).
- Authored vs generated: `derives_from`, `depends_on`, `relates_to`, `superseded_by` authored on the
  child; never edit `derived_by`, `supersedes`, `implemented_in_files`, `tested_in_files`, `status`.
- Approved StRS (LAYOUT-001, LAYOUT-003, PALETTE-015; owner gaetan@xeberon.net): text change needs
  `approved_by` + `approved_at` (ISO with offset). Owner answers (02-answers.md) garden-Q1: agreed in
  advance, ONE COMMIT PER corrected approved StRS, Driver records re-approval; garden-Q2: added diagram
  and generated links = no re-approval.

## 3. Where things are (worktree, verified) and the scope's IDs

Scope today: 12 StRS files in force at layout/theme + PALETTE (LAYOUT-001/003/004, PALETTE-001/002/005/
007/013/015/018, THEME-002/004/011; lifecycle `proposed` except the 3 approved). In-force SwRS: LAYOUT 11
(001,002,007,011,018,020,022,023,032,043,044), THEME 8 (001,013,016,025,031,034,038,043), PALETTE 75 (001-004,
010,017,021,031,036,039,043,045,048-050,052-054,058,069,072,078,083,089,092,109,114,115,123-127,130,132,133,
135-138,140,147-150,153,160,178,183,192,196,203,213,217,229,232,238,240,242,252,256,263-275). All `proposed`;
none `approved`. 39 superseded + 6 deprecated exist already.

### Spec section 5 (implementation markers) - current position

| Spec ref | Today | Verdict |
| --- | --- | --- |
| `editPalette.ts:23-39` 17 IDs | `src/page/modules/editPalette.ts:23-39` (16 PALETTE + LIFE-169) | exact |
| `paletteActions.ts:209-211` (263,001,275) | 209-211 before `PALETTE_ACTIONS` | exact; also 268 at :197, 273 at :659, 265 at :689/:699, 274 at :709 |
| `blockSourceEditor.ts:44-51` | the 8-ID block is **:45-52** (BLOCK-029,087,216, PALETTE-001, TRUST-001, PALETTE-021, TABLE-001,034) on `receiveBlockEditSource`; :332 (031) and :361 (017) correct | shifted by 1 |
| `pageChromeStyles.ts:1` 002 | :1-3 (PALETTE-002, TOOLBAR-129, -130) | exact |
| pageChromeStyles cluster `:145-151` | LAYOUT-002, LIFE-049, MYST-081, THEME-031, THEME-043, TOOLBAR-001, -025 (7 IDs) | exact; after moving the 3 in-scope IDs 4 foreign IDs stay > 3: file stays on baseline (7 -> 4) unless sibling CRs move them |
| `--sphinx-preview-content-max-width` rule `:164`; zoom `:168` | :164 (max-width) and :166-168 (`--sphinx-preview-zoom` ... column-width); Cream block at :100-101 inside `FORCED_THEME_MODES_CSS` (const at :7, THEME-025 + REVIEW-002 above it) | approx. These are inside ONE template string `PAGE_CHROME_CSS`: a marker cannot be placed "at the rule". Use a `pageChromeStyles.markers.ts` companion (code point `--sphinx-preview-content-max-width`, `--sphinx-preview-zoom`) or keep them on the constant. THEME-031 can go above `FORCED_THEME_MODES_CSS` (3 IDs ok) |
| 002 tooltip rule | tooltip rules at :461-515 | same string constraint -> companion |
| `contentLayoutStyles.ts:80-90` 11 IDs | exact: CORE-028,034, TOOLBAR-003,133, LAYOUT-001, LAYOUT-022, **PALETTE-021 (not named by the spec)**, THEME-001, TOOLBAR-025,037,045 | spec forgets PALETTE-021 (in scope); 7 foreign IDs remain after the 4 moves -> baseline 11 -> 7, not removed |
| wrapping rules `:314`, `:407`, `contentBlockStyles.ts:161` | `overflow-wrap: anywhere` at contentLayoutStyles :314, :407; contentBlockStyles :161 | exact; again inside CSS strings |
| `themeMode.ts:88` THEME-001 | :88 (THEME-001), :89 LIFE-169, :67 THEME-016, :68 CORE-050 | exact |
| `tableStyles.ts:1-3` LAYOUT-032 | :1-3 (CORE-034, CORE-077, LAYOUT-032) = 3 IDs, not over limit | exact; not baselined; "move to the rule" impossible (string) -> leave or companion |
| `contentBlockStyles.ts:6-19` LAYOUT-043 at :19 | block :6-19 = 14 IDs, LAYOUT-043 at :19; `contentLayoutStyles.ts:41` has LAYOUT-043 | exact; baseline 14 -> 13 |
| `propertiesStyles.ts:1` CORE-050; reduced-motion `@media` `:535` | :1 (CORE-050, FMSCHEMA-005, TOOLBAR-129, -130 = 4 IDs, baseline 4), @media at :535 | exact; string again |
| `editPalettePopovers.ts:397` 036 | :396 PALETTE-058, :397 PALETTE-036 (`buildColor`); `linkPanel.ts:39` ok | exact |
| `blockEditor.ts:41` 089 | :39-43 block of 5 (BLOCK-148, -228, PALETTE-089, TABLE-064, -085); baseline 10 counts other blocks too | exact |
| `runtime.ts:283`, `firstClearance.ts:308` LAYOUT-018 | exact (also :85 LAYOUT-011, :146 LAYOUT-043) | exact |
| `webview.ts:162-166` LAYOUT-002 (5 IDs, baseline 5) | NOT in the spec: DIAG-001, DIAG-023, LAYOUT-002, TRUST-022, TRUST-002 | add to the list |
| per-action markers | blockEditActions.ts: 049 :36, 052 :58, 053 :59, 123 :305, 267 :315, 127/130/268 :392-394, 137 :543, 265 :566/:589, 273 :634, 274 :650; inlineEditActions.ts: 045 :10, 114 :207, 048 :239, 135 :305, 138 :357, 126 :372 | exact set for the merges |

### Spec sections 6 (test markers) - current position

| Spec ref | Today | Verdict |
| --- | --- | --- |
| `editActions.test.ts:9-48` 40 `@tests_req` | header :9-51 (43 IDs counting non-PALETTE); test lines 325, 346, 383, 519, 542, 711, 749, 847, 859, 913, 943, 972, 977, 986, 995, 1009, 1017, 1039, 1055, 1062, 1095, 1381 all match the spec | exact. NOTE: the header also holds 039,043,052,053,054,058,069,072,083,089,092,109,115,148,150 and foreign DIAG-017, REVIEW-160, TABLE-073/074/076/106/111/115/117: the spec table moves only part, so the entry stays on baseline (43 -> lower) unless every ID is moved; the foreign ones belong to sibling CRs |
| `pasteUrl` unit `test/page/modules/pasteUrl.test.ts:12-69` | 7 markers 12,21,27,39,50,56,69 (path has `modules/`) | exact path `test/page/modules/pasteUrl.test.ts`; `test/integration/pasteUrl.test.ts:59` ok; the wrong one `test/build/integrationEditModeRestore.test.ts:10`; extra markers 264 at `page/runtimePaletteActions.test.ts:821,848` (not in spec: check they test paste URL) |
| PALETTE-001 `test/security/package-contract.test.ts:40` | :40 (block 34-40, 7 IDs, baseline 7: other IDs foreign) | exact; other PALETTE-001 test markers stay: `core/configuration/editingConfiguration.test.ts:12`, `core/palette/paletteActions.test.ts:18`, `page/modules/editPalette.test.ts:92`, `page/runtimeEditPalette.test.ts:31`, `page/runtimePaletteActions.test.ts:25`, `paletteReq.requirements.test.ts:155` |
| title "outside the three modes" | `test/page/modules/paletteReq.requirements.test.ts:156` (marker :155) | shifted by 1; path has `modules/` |
| THEME-016 `core/state/editLock.test.ts:24` | exact (block 22-24 with BLOCK-191, DIAG-105); other THEME-016 markers: `integration/lifecycle.test.ts:48`, `page/runtimePageControls.test.ts:151` | exact |
| PALETTE-240 `slashMenu.test.ts:762`, `:783` | tests at 762 and 783 exist; existing marker :323 | exact |
| PALETTE-256 (marker "`:680`") | marker at :679 before test :680 ("menu opens under the caret... flips above", covers Room below, No room below, Pane edge); :709 (follows the caret on scroll / caret scrolls out), :722 (left edge as query grows), :806 (scroll inside the menu does not move it). All 6 scenarios have a test -> only marker moves, no new test | shifted by 1 |
| `realInput/markers.ts` | companion, 64 unnamed lines (baseline 64 and 64). In scope lines 34-38 (SwRS PALETTE-153,031,232,242,238), 45-47 (THEME-001, -016, -025), 57-60 (StRS PALETTE-001,005,007,015), 66 (StRS THEME-002) = 13 lines | exact; removing the 13 -> baseline 51 (both maps) |

### Other baseline entries holding in-scope IDs (scripts/marker-baseline.json)

contentBlockStyles 14, contentLayoutStyles 11, pageChromeStyles 7, blockEditor 10, blockSourceEditor 8,
editPalette 17, webview 5 (spec omitted), pageStateMessages.test 9 (THEME-013 at :226), imagePaste.test 5
(StRS-PALETTE-018 + 196 + 217 + 2 foreign), lifecycle.test 6 (THEME-016 :48), mystPickers.test 4 (StRS-
PALETTE-013 + 178 + 183 + TRUST-090), paletteMode.test 4 (leaves baseline with the 010 drop),
realInput/markers.ts 64, editActions.test 43, package-contract.test 7. Realistic outcome: editPalette.ts
(17 -> 0, all in scope except LIFE-169 which is shared) leaves the baseline; editActions.test, markers.ts,
pageChromeStyles, contentLayoutStyles, contentBlockStyles shrink only. After each batch of edits run
`node scripts/check-marker-companions.mjs --update` and commit the baseline.

## Spec errors and gaps the Driver must know

1. Diagrams: guideline says "exactly one mermaid fence". Spec section 10 wants "state + sequence" for
   PALETTE-002: pick ONE fence (suggest `stateDiagram-v2` for the nested modes, the message flow goes in the
   Main paths).
2. Garden-Q3 (answers) supersedes open question 2: cite LIFE-169/170 with `depends_on` on LAYOUT-003,
   PALETTE-002, THEME-004, THEME-011 (add authored `depends_on` to the 4 StRS, which today have none) and drop
   those 4 StRS from LIFE-169/170 `derives_from` (they then derive LIFE-014 etc.; the lifecycle CR owns the rest).
   LAYOUT-003 is approved: the `depends_on` edit is authored frontmatter; put it in LAYOUT-003's single commit.
   Order risk with req-garden-toolbar-lifecycle on the LIFE-169/170 frontmatter: keep both CRs' edits. Same for
   CORE-050 / BLOCK-047 (keep derivation or move to depends_on; spec section 3 "keep"; Q3 says depends_on).
3. Supersession breaks Main-path citations (`check_main_paths.py` requires active SwRS):
   `StRS-LAYOUT-004` cites LAYOUT-018 (x2) -> LAYOUT-011; `StRS-PALETTE-002` cites PALETTE-010 -> LIFE-169
   (depends_on); `StRS-THEME-004` cites THEME-013 -> LIFE-169; `StRS-PALETTE-001` path 1 cites 045 -> merged ID.
   LAYOUT-011 derives LAYOUT-004 already (ok). The spec does not list these edits.
4. Superseding StRS-PALETTE-001: every SwRS that still lists it in `derives_from` must be re-parented first.
   Single-parent today: PALETTE-003 (-> A), 114 (-> REVIEW-015); PALETTE-001 itself (-> PALETTE-002 only),
   275 (-> PALETTE-015). Two-parent SwRS to just drop 001: 004 (018), 021 (005), 054 (013), 058/072/089/092/109/
   150/153/160 (007), 213/264 (018), 238/242 (015), 263 (015, 007), TABLE-111 (TABLE-012). Members of the new
   A/B/C swap 001 for A, B or C. PALETTE-115 derives 001+005: becomes B only. PALETTE-086 (deprecated) also lists
   001; leave it.
5. PALETTE-007 already has 2 paths -> the "Write a link" path of PALETTE-001 is DROPPED (no scenarioLinkPanel marker).
6. LAYOUT-032 already has two unit tests (`previewStyles.test.ts:763,775`): the section 8 "unit test of the scroll-box
   rule" exists; add only a marker move. LAYOUT-002 "rendered column at 0" is covered by `previewStyles.test.ts:712`
   (`previewContentWidthCss(0)` -> none); decimals/negative are not covered (see below).
7. `editToolbarCover.test.ts:86` today carries SwRS-PALETTE-021 (integration, VS Code): add the StRS-PALETTE-005 marker
   as a separate block there.
8. LIFE-169 stale-message drop: probably already tested (`core/protocol/pageToHost.test.ts:90` and 14 more
   `@tests_req LIFE-169`): add nothing (belongs to toolbar-lifecycle) unless the Coder finds it missing.
9. New SwRS need `@implements_req` right away (rule 1), so round 1 cannot be green on `just check-markers` without it.

## 4. Sections 7 and 8: tests that exist, cheapest place

### Section 7 (StRS validation tests)

| StRS | Marker today | Cheapest |
| --- | --- | --- |
| A, B, C (new) | none | `test/integration/realInput/textEditing.ts` (real window, CI only): `scenarioPalette` :612 (A, B step), `mystPickers.test.ts` for C (VS Code). Needs an alert + admonition step if absent: that is VS Code / real-window |
| PALETTE-002 | `integration/paletteMode.test.ts:39` ok | - |
| PALETTE-005 | only in `realInput/markers.ts:58` | `scenarioPalette` :612 + `editToolbarCover.test.ts:86` (VS Code) |
| PALETTE-007 | `integration/imagePicker.test.ts:26` ok | - |
| PALETTE-013 | `integration/mystPickers.test.ts:8` ok (block of 4 on baseline) | - |
| PALETTE-015 | `visual/scenarioDefinitions2.ts:1124` ok | add `scenarioSlashMenu` :495 |
| PALETTE-018 | `imagePaste.test.ts:26`, `realWindowGaps.ts:556`, visual :329/:1330 ok | - |
| LAYOUT-001 | `visual/scenarioDefinitions1.ts:198` ok | optional visuals v78-v80 (`scenarioIds.ts:233-235`, 460 px) marker |
| LAYOUT-003 | `scenarioDefinitions1.ts:622`, `scenarioDefinitions2.ts:1138` ok already | `capture_layout_checks.py:764 check_width_modes` marker optional (python, CI) |
| LAYOUT-004 | `scenarioAssertions.ts:673`, `scenarioDefinitions1.ts:1217` ok | - |
| THEME-002 | `scenarioDefinitions1.ts:101`, `scenarioDefinitions2.ts:962` ok (visual) | spec: `realInput/previewWindow.ts:352` (the `38-toolbar-{host}-{mode}` captureAfter, app window) |
| THEME-004 | `scenarioDefinitions2.ts:990` ok (visual) | `integration/lifecycle.test.ts:77-83` sends `previewThemeModeChanged` dark; "next page carries it" is NOT asserted: add (VS Code) in the test body, NOT in the 6-ID header (:43-48, baselined) |
| THEME-011 | `scenarioDefinitions2.ts:975` ok | `integration/reload-suite.ts:196-219` confirmed (zoom 130 survives reload and close/reopen); add the marker next to :208 and :219 (reload-suite has only LIFE-014/-170 markers at :112) |

VS Code / app window / python-playwright needed for: lifecycle.test.ts, reload-suite.ts, paletteMode, mystPickers,
imagePicker, editToolbarCover, realInput/*, `test/visual/*`. They run in CI (`gh workflow run ci.yml --ref <branch> -f heavy=true`),
not locally.

### Section 8 (missing scenario tests) - unit placement

| SwRS | Test | Cheapest location |
| --- | --- | --- |
| LAYOUT-002 decimal, negative | `readPreviewConfiguration` | extend `test/core/configuration/previewConfiguration.test.ts:89-110` (today 2500->2400, 0, NaN only) |
| LAYOUT-002 open-preview update | exists `test/session/diagReq.settings.requirements.test.ts:95` | none |
| LAYOUT-022 centring / negative figure mark | CSS or `runtimePageControls.test.ts:416` | `test/core/preview/previewStyles.test.ts:918` (CSS assertion) or runtimePageControls harness |
| LAYOUT-023 %, em, rem widths; Mermaid wrapper; re-measure after patch / image load / TOC toggle | `test/page/tableBreakout.test.ts` (:372-417), `runtimePageControls.test.ts:358,438,494`, `runtimeScroll.test.ts:1170` | unit, same files |
| LAYOUT-011 narrow-table fallback; layout re-measure (from 018) | `test/page/modules/firstClearance.test.ts:60,241` | unit, same file |
| LAYOUT-032 | exists | marker only |
| THEME-016 kinds default,1,3,4 | `test/page/runtimePageControls.test.ts:151` (uses `pageLiveStateMessages(ready, {themeKind: 2})`, asserts `data-sphinx-preview-theme`) | add a table test there (unit), mark THEME-016 |
| THEME-043 toolbar does not scale | `previewStyles.test.ts:893` covers zoom scaling of font+column only | add CSS assertion (toolbar font/width not tied to `--sphinx-preview-zoom`) there |
| PALETTE-256 | all 6 scenarios already tested | marker moves only |
| LIFE-169 stale drop | see gap 8 | none |

Untestable without VS Code in this CR: none of section 8 (all unit). If the code differs from the SwRS: SwRS follows code + "Known issue".

## 5. Proposed rounds, risks, evidence plan

**Round 1 (requirement text, supersedes, reparenting, diagrams, log)** - one commit per area, each green on
`just requirements-lint`:
1. `just dev`; run `just requirements-lint` for the baseline.
2. Create A, B, C (`okfreq new strs`), then the new SwRS (inline buttons, line-prefix buttons, starter blocks, scroll-
   sync PALETTE-021 split, rule-icon split); write `work/id-map.md` (old -> new IDs).
3. Reparent per section 3 + gaps 2-5; edit StRS text (section 1); supersede; PALETTE-021 / PALETTE-002 edits in place;
   LAYOUT-023/044, LAYOUT-001/032, THEME-034, PALETTE-275 in place.
4. Fix Main paths citing superseded SwRS (gap 3); move PALETTE-001 path 1 into A.
5. Diagrams on the 15 StRS (one fence each, not 2); approved StRS: LAYOUT-001, LAYOUT-003 own commits (Q1), set
   `approved_by`/`approved_at`.
6. Mechanically rename markers of superseded IDs to the new ID in the same commit (so no marker sits on a superseded ID)
   and add one `@implements_req` per new SwRS (rule 1).
7. `just requirements-update`; log entry in `requirements/tiers/log.md` (`## 2026-11-17`, `### Topic`).

**Round 2 (code and test markers)**: sections 5 and 6, baseline `--update`; companion files for CSS strings; test-header
splits; `realInput/markers.ts` lines removed (the StRS lines go to scenario functions, section 7). Pure comment moves:
verify with `git diff -w` showing only comment lines.

**Round 3 (new tests)**: section 8 unit tests (above); section 7 additions (step in `scenarioPalette`, alert/admonition
steps, lifecycle "next page" assertion, reload-suite markers). Tests must pass on today's code.

**Risks**
- Marker blocks: a "moved" marker next to another marker stays in the same block; always separate by a code line.
- CSS strings: markers cannot sit in `*_CSS` templates; ">3 IDs" files with foreign IDs stay baselined (cannot be removed
  by this CR; lower only).
- Mass supersede cascades (okfreq refuses cycles; StRS-001 supersede while SwRS still derive from it).
- New SwRS IDs are unknown until created: keep `id-map.md` current; round 2 depends on it.
- Sibling CRs touch `editActions.test.ts`, `realInput/markers.ts`, LIFE-169/170 frontmatter, TRUST/CORE/TABLE parents:
  expect rebase conflicts, keep both.
- `just check` includes file-size checks (`scripts/file-size-baseline.json`): adding tests to big test files may trip it.
- Real-window and VS Code checks are CI only: unverifiable locally.

**Evidence plan (Verifier)** - the change has no UI; evidence = command outputs saved in `evidence/*.log`:
1. `just dev` (once), then `just requirements-lint`: expect `main paths: <n> StRS checked, <m> SwRS citations, all
   valid`, 0 errors, no orphan SwRS.
2. `just requirements-update` then `git status --porcelain requirements/` empty; `okfreq lint --check` and
   `okfreq update-coverage --check` clean; `okfreq validate --check-links --project-root .` 0 errors.
3. `uv run --no-sync --group requirements okfreq trace requirements --json`: no `missing_ids`; scope's in-force SwRS each
   have an implementation and a test file; every in-force StRS of the scope has a test marker outside
   `test/integration/realInput/markers.ts`.
4. `just check-markers`: pass, summary `files on the marker baseline` lower than before (record before/after of
   `scripts/marker-baseline.json`: 61 entries now in `blocks`); `git grep -c "@tests_req SwRS-MDOKFSTUDIO-PALETTE-264"`
   only in pasteUrl tests (+ runtimePaletteActions if relevant); `markerBlocks` on `editPalette.ts` all <= 3.
5. `just check` (or `just preflight` on Windows) for new unit tests; then `gh workflow run ci.yml --ref <branch> -f
   heavy=true` for integration/real-window changes (CI evidence, cannot be shown locally).
6. Spot check: SwRS-PALETTE-045 and SwRS-LAYOUT-018 are `superseded` with `superseded_by` pointing at the merged SwRS.
7. Cannot be shown locally: Mermaid GitHub rendering (check on the PR branch), VS Code/real-window scenario results.

## Questions for the user
None beyond the spec: the owner's answers cover approvals (Q1, Q2) and shared rules (Q3). Driver to settle: the
PALETTE-114 parent (REVIEW-015 approved; answer Q5 = take the spec recommendation) and the PALETTE-002 single-fence choice.
