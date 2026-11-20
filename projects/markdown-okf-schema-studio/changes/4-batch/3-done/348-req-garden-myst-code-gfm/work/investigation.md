# Investigation: CR-348, garden the requirements of myst, code-blocks, gfm

The worktree is `markdown-okf-schema-studio.worktrees/batch-06-CR-348`, at 3766a40e. That is the
head of CR-347's PR 418, which sits on CR-345's PR 415. The merge-base with origin/main is
de96c3df, where CR-343, CR-344 and CR-346 landed. Line numbers are on this branch.

Paths are relative to the worktree. "CODE-001" means the SwRS unless "StRS" is written.

## 0. Lifecycle at start (corrects the spec's "Lifecycle state")

**In-force StRS (10):**
- CODE-001, CODE-004, GFM-003, MYST-005, MYST-006, MYST-007, MYST-009 and MYST-012 are proposed.
- GFM-002 and MYST-001 are approved (`approved_at` 2026-11-12T12:30:00+01:00).

**In-force SwRS: 43, not 44.** CR-347 superseded SwRS GFM-029 by CORE-071, so it is out.
- CODE (10): 001, 005, 007, 008, 014, 017, 019, 026, 039, 040.
- GFM (9): 001, 008, 009, 016, 021, 027, 031, 034, 039.
- MYST (24): 001, 006, 013, 017, 019, 024, 031, 036, 038, 045, 051, 053, 057, 063, 066, 072, 078,
  081, 096, 097, 098, 099, 100, 101.

**Already done by siblings on this branch** (see `requirements/tiers/log.md`: CR-347 at lines
159-194, block-table at line 52):
- TRUST-006 is superseded by TRUST-005. CODE-025 and 13 `depends_on` links were repointed.
- GFM-029, GFM-030 and GFM-033 are superseded by CORE-071.
- BLOCK-041 now derives only from StRS BLOCK-003, and BLOCK-058 only from StRS BLOCK-025.
- GFM-034's marker is on the sanitizer's span-style branch.
- StRS CORE-001 (approved) was corrected and re-approved at 2026-11-17T19:27:51+01:00. It is still
  in force, and CORE-088 holds "CommonMark constructs render the same in every palette mode".

**Wrong claims in the spec, to drop or correct:**
- Every TRUST-006 item: write TRUST-005 instead.
- Every GFM-029 item, in sections 5 and 7: it belongs to CORE-071 and CR-347.
- The BLOCK-041 and BLOCK-058 reparenting: it is already done.
- "44 SwRS": it is 43.

## 1. Per spec section: what holds, what to do

### §1. StRS text fixes

All still to do.
- StRS CODE-001 has 125 lines. Rewrite its normative text and rationale to match CODE-007, 039 and
  040, and drop the `docs/user/editing.md` bullet.
- StRS GFM-002 (approved): the rationale fix is agreed (garden-Q1).
  - Make it one commit, named like CR-345's: `docs: correct the gfm requirement StRS-MDOKFSTUDIO-GFM-002`.
  - Set `approved_by` to gaetan@xeberon.net and `approved_at` to the current time with `+01:00`.
- StRS GFM-003: remove Path 2 (radio) and keep the refusals.
- StRS MYST-005: widen the title to "Constructs the preview cannot build stay visible and labelled"
  (the Q5 recommendation, applied).
- StRS MYST-009: add the "how many references still use the old name" clause.
- Format drift: still present.
  - MYST-097 opens with `## EARS Expression` at line 31. Check MYST-096 the same way.
  - MYST-098, 099 and 100 still use table scenarios.

### §2. New StRS and the MYST-001 split

Both are to do. The split of MYST-001 into four StRS is AGREED (garden-Q1/Q2). Do it in one commit
that names MYST-001.

In-force SwRS that derive from StRS MYST-001 today, and where each goes:
- (a) MYST-001, MYST-006, MYST-013.
- (b) MYST-053, MYST-098, MYST-099, MYST-100.
- (c) MYST-031, MYST-063, GFM-031. GFM-031 also keeps StRS GFM-002.
- (d) MYST-017.
- MYST-101 is superseded into MYST-096 (§4), so it gets no new parent.
- CORE-012: remove MYST-001 from it. It keeps CORE-002 and CORE-003, and also loses GFM-002 (§3).

About 30 superseded SwRS still list StRS MYST-001 in `derives_from`. Leave them as they are, the
way earlier supersessions did. MYST-001 is itself the successor of the old StRS MYST-002, 003, 008,
011 and 013; okfreq must accept a chain.

### §3. Reparenting

What remains in `derives_from`:
- TRUST-005: remove GFM-003, MYST-009 and CODE-004. It keeps 10 other parents.
- TRUST-065: remove CODE-004 and MYST-009. It keeps 6.
- CORE-012: remove GFM-002 and MYST-001.
- MYST-019: remove MYST-005. It keeps MYST-009.
- MYST-097: replace MYST-005 by StRS CORE-001 (Q3, §2 below).
- GFM-031: replace MYST-001 by (c).

What remains in `depends_on` (only the missing links):
- CODE-017: add TRUST-065. It has TRUST-005.
- CODE-019: add TRUST-065 and TRUST-052, which come from CODE-026. Drop CODE-026.
- GFM-021: add TRUST-052, from GFM-027.
- MYST-045: already has BLOCK-041, BLOCK-058, TRUST-005 and TRUST-065. Add TRUST-052 and TRUST-090,
  from MYST-051.
- The two new radio SwRS: TRUST-005, TRUST-065, BLOCK-041 and BLOCK-058, as GFM-039 has today.
  "Choosing" also gets GFM-021.
- MYST-036 and MYST-038 (label lists): add `depends_on` MYST-097.
- MYST-031: add `depends_on` TRUST-025 (§2 below).

### §4. Merges and splits

Every row of the spec table holds except these:
- GFM-027's `depends_on` is TRUST-052, TRUST-005, TRUST-065 and TRUST-090. GFM-021 already has all
  but TRUST-052.
- MYST-051's `depends_on` is TRUST-052, TRUST-005, TRUST-065 and TRUST-090.
- Q4 (cache and lazy-load scenarios become verification notes, as recommended):
  - The tests keep their markers, because they still check the SwRS. They are
    `test/core/render/contentCaches.test.ts:16` (CODE-001), `:33` (MYST-024) and `:90` (MYST-057),
    and `test/core/bundleSplit.test.ts:46-47` and `75-76`.
  - Their notes name these tests.
- Q6 and Q7: see §2 below.

### §5. Code markers (line moves)

- `src/core/preview/styles/contentBlockStyles.ts`: the header block at 6-19 is gone.
  - The block is now at **729-733**, on `CONTENT_BLOCK_CSS`, with 5 IDs: MYST-100, MYST-098,
    CODE-007, CODE-008, CODE-014.
  - Move them into the existing companion `src/core/preview/styles/contentBlockStyles.markers.ts`.
    It uses lines of the form `// @implements_req <ID> — <selector text found in host>`.
  - The other choice is to put them on the CSS rule each one names. The file has 745 lines and the
    limit is 800.
- `src/core/preview/styles/codeBlockStyles.ts:18-21` holds CODE-001, 005, 039 and 040.
  - Remove CODE-005 and CODE-001.
  - CODE-001 is already in `src/core/render/highlight.ts:256-258` and `mystRenderer.ts:73`.
- `src/core/render/mystRenderer.ts`: the block is at **543-546**, not 542-546. It holds CORE-001,
  CORE-071, GFM-008 and MYST-017.
  - Remove GFM-008 and MYST-017. They are already at `src/core/render/mystEngine.ts:8`,
    `mystTables.ts:294` and `mystBlockTransforms.ts:75`.
  - GFM-029 is already gone.
- `src/core/security/html-sanitizer.ts`:
  - GFM-016 is alone at `:268` on `rewriteNode`. Move it to the checkbox-input branch.
  - GFM-034 is already at `:379`. Nothing to do.
- MYST-098: remove it at `src/core/render/mystNode.ts:67`, `mystNormalize.ts:529` and
  `src/page/features/editMode.ts:28`. Keep it at `mystGridToctree.ts:461` and `:484` and
  `pageInput.ts:265`.
- `src/session/pageMessages.ts:182`: remove MYST-038.
- Where the markers of superseded SwRS move:
  - **CODE-005**: `highlight.ts:232-233` (with 039) and `mystNormalize.ts:210-211` (with 014). It
    goes to CODE-039, and to CODE-001 for "special characters".
  - **CODE-026**: `src/core/protocol/pageToHost.ts:241` and `src/session/hostRequests.ts:154`. It
    goes to CODE-019.
  - **GFM-027**: `pageToHost.ts:235`. It goes to GFM-021.
  - **MYST-051**: `pageToHost.ts:264` and `src/session/features/sourceEdits.ts:129`. It goes to
    MYST-045.
  - **MYST-101**: `src/core/render/mystNestedBlockBreaks.ts:44`. It goes to MYST-096.
  - **GFM-039** goes to the two radio SwRS, split by what each line does:
    - `checkboxMarkers.ts:80-81` (with GFM-016);
    - `radioGroups.ts:147` and `radioMarkers.ts:77` (render);
    - `checkboxes.ts:90`, `115`, `185`, `226` and `247`;
    - `sourceEdits.ts:87-88` and `119-120`;
    - `pageToHost.ts:94`;
    - `contentPatch.ts:24-27`;
    - `html-sanitizer.ts:492` (render).
  - **MYST-024 dollar** (`mystInlineTransforms.ts:368`, `418`, `427`): goes to the new
    dollar-prices SwRS.

### §6. Test markers

Wrong markers:
- `test/core/preview/previewStyles.test.ts`: the marker is at **381**, not 380. Change it from
  CODE-007 to CODE-039.
- `test/core/render/codeBlockComfort.requirements.test.ts:78,87`: change CODE-001 to CODE-040.
  This is confirmed: the tests check the CSP and the absence of inline styles.
- `test/core/syntax/markdownSyntax.test.ts:108`: remove MYST-097. The test is
  "escapeHtml and escapeRegExp".
- `test/integration/mystDiagnostics.test.ts:36` (`runUntrusted`): change MYST-081 to MYST-078.
- `test/core/render/mystTablesTree.test.ts:7,16,28`: remove GFM-008.
- `test/security/html-policy.test.ts:450`: the test is at 451, after its marker at 450. Rename
  "span style keeps only hex and rgb colour…".

Unmarked tests. Line numbers in the spec point one line before the `test(` line; the right ones
are:
- `test/core/render/mystFeatures.test.ts`:
  - MYST-001: 290, 514, 543, 564.
  - MYST-006: 943, 564.
  - MYST-013: 1003, 1043, 1072, 1106.
  - MYST-063: 594, 719, 736.
  - GFM-031: 780.
- CODE-001: `renderReq.codeBlocks.requirements.test.ts:77` and `:99`, and
  `test/core/render/highlight.test.ts:21` and `:104`. The test at `:66` ("inline code is never
  highlighted") is CORE-089, so check that marker. It is not CODE-001.
- CODE-017: `test/page/modules/codeCopy.test.ts:256` ("blocks being edited … are skipped").
- CODE-019: `codeCopy.test.ts:249` and `:365`, plus the clipboard write in
  `test/session/renderReq.codeCopy.requirements.test.ts`. That file already carries CODE-026 at 63
  and 86, which becomes CODE-019.
- GFM-001: `test/core/render/bareUrlAutolink.test.ts:54`, `79`, `120`. Confirmed.
- MYST-053: `test/core/render/gridToctree.test.ts:113` and `:136`. The test at `:88`
  ("grid-item-card renders header, body, footer") checks card parts, so mark it **MYST-100**.
- MYST-057: `gridToctree.test.ts:176`, `185`, `192`, and `renderReq.myst.requirements.test.ts:52`.
  Confirmed.
- MYST-024: `test/core/render/mathRenderer.test.ts:25`, `36`, `45`. Confirmed.
- MYST-081: `test/page/modules/warningBanner.test.ts:109`, `118`, `126`, `150`. Confirmed.
- MYST-066:
  - `test/core/myst/confLocator.test.ts:29`, `50`, `92`, `130`;
  - `test/core/myst/confParser.test.ts:57`, `84`.
  - The test files are under `test/core/myst/`.
- MYST-019: `mystPaletteRendering.test.ts:221` is a `});`.
  - The next test, at 222, is "a label before a heading keeps one element with the id": it is a
    MYST-036 anchor test, not MYST-019.
  - Do **not** mark it MYST-019.
- Markers of superseded SwRS in tests. All must move.
  - CODE-005:
    - `highlight.test.ts:89`;
    - `mystFeatures.test.ts:137`;
    - `renderReq.codeBlocks.requirements.test.ts:42`.
  - CODE-026: `pageToHost.test.ts:47`, `codeCopy.test.ts:461`, `renderReq.codeCopy…:63,86`.
  - GFM-027:
    - `pageStateMessages.test.ts:221`;
    - `checkboxRefusal.test.ts:59`;
    - session `radioChoice.test.ts:147`.
  - MYST-051: `pageToHost.test.ts:142`, `labelRename.test.ts:38`.
  - MYST-101: `blockBreakInContainer.test.ts:28,34`.
  - GFM-039: `radioGroups.test.ts`, `runtimeRadioGroups.test.ts`, `radioSelect.test.ts`,
    `test/visual/radioPlanScenarios.ts:44,56`, integration `radioChoice.test.ts:187`,
    `html-policy.test.ts:323`, session `radioChoice.test.ts` (many lines). List them with
    `grep -rn GFM-039 test`.

### §7. Tests for scenarios no test checks

- **Drop the GFM-029 "Kbd with attributes" item.** It belongs to CR-347 and CORE-071.
- CODE-007: `0.92em` is in `contentBlockStyles.ts:173`, so a style test can assert it.
- MYST-053: `MAX_GRID_DEPTH = 8` is at `mystGridToctree.ts:43`, used at `:548`. A depth-9 test is
  feasible.
- **MYST-019 `{numref}`: the scenario contradicts the code.**
  - MYST-019's scenario (lines 54-56 of `requirements/tiers/swrs/myst/SwRS-MDOKFSTUDIO-MYST-019.md`)
    says a `{numref}` "shows its number (Figure 1, Table 1)".
  - `test/core/render/renderReq.myst.requirements.test.ts:99` (marked MYST-017) asserts that each
    numref is "an inert placeholder, never a numbered link", whose text is `{numref}fig-x`.
  - Per §7 ("do not change the code; stop and report"), do not add a numref test under MYST-019.
    Report it in the PR body as a stale scenario or bug for the owner.
  - The heading-text case can still be tested.
- Not verified by me; the Coder checks each first:
  - CODE-001 "a shorter backtick line does not close the fence";
  - CODE-019 "a second click restarts";
  - GFM-008 "reference without definition";
  - the GFM-021 host refusals in `src/session/features/sourceEdits.ts`, using
    `test/session/radioChoice.test.ts:185` as the pattern;
  - MYST-024 "KaTeX bundle missing";
  - MYST-081 "malformed `previewShowProblems` ignored". The router is at
    `src/session/features/viewState.ts:52` and `src/session/pageMessages.ts:89`.

### §8. StRS validation tests

- StRS CODE-001: add the marker to `test/visual/scenarioDefinitions1.ts:702`
  (`diff-dark-preview`), which already holds SwRS CODE-008 there. That makes 2 IDs, which is fine.
- StRS MYST-005: add it to `scenarioDefinitions1.ts:1368` and `1384` (MYST-096).
- StRS MYST-009: add it to the JSDoc of `test/integration/realInput/labelRenameAboveTable.ts`.
  The JSDoc has `@tests_req` MYST-038 at line 42, and the function is at 44.
- New radio StRS: add it to the integration test `radioChoice.test.ts:187`.
- MYST-001 successors:
  - (a): `scenarioDefinitions1.ts:212` (admonitions), replacing StRS MYST-001.
  - (b): `test/integration/mystBlocksWindow.ts:150-153`. That block holds MYST-001, 100, 098 and
    099, so it is over the limit. Split it (§3 below).
  - (c): `test/visual/scenarioDefinitions2.ts:699` (figure-anchors). It holds StRS MYST-001 with
    StRS MYST-009 at 700.
  - (d): the myst gallery scenario at `scenarioDefinitions2.ts:798-808`, marker at 800, which is
    StRS MYST-001 today. Its `MYST_GALLERY_ASSERTIONS` (`test/visual/scenarioAssertions.ts:169-178`)
    already assert `dl dt` count 2, sub/sup, kbd "Ctrl+S" and abbr "Heart Rate". So no new
    assertion is needed.
  - Every StRS MYST-001 marker that remains moves to a successor:
    `scenarioDefinitions2.ts:551`, `699`, `800`, and `scenarioDefinitions1.ts:212`.
- StRS MYST-006: no marker exists.
  - `scenarioDefinitions2.ts` has exactly **1500 lines**, the test limit, so put the new scenario in
    a new module, for example `test/visual/mathScenarios.ts`.
  - Spread it in `scenarioDefinitions1.ts` (1454 lines; the other modules are spread at 471-500).
  - Register its id in `test/visual/scenarioIds.ts`.
  - Fixture: reuse or extend `test/visual/fixtures/55-dollar-prices.md`, or add `89-…`; the last
    used number is 88.
  - Assert `.katex` and `[data-studio-math-error]`, set by `src/core/render/mathRenderer.ts:125`.
- Already covered:
  - StRS CODE-004: `scenarioDefinitions1.ts:444`.
  - StRS GFM-002: `scenarioDefinitions2.ts:788`.
  - StRS GFM-003: integration `checkboxToggle.test.ts:109`.
  - StRS MYST-007: integration `mystDiagnostics.test.ts:47`.
  - StRS MYST-012: `scenarioDefinitions2.ts:822`.

### §9. Use case diagrams

To do for 9 + 1 + 4 = 14 StRS: the in-force ones without MYST-001, plus the radio StRS and (a)-(d).

The spec's last bullet is wrong: garden-Q2 says an added diagram on an approved StRS is editorial
and needs no re-approval. GFM-002's diagram therefore needs no new `approved_at`. Its rationale fix
does (§1).

### §10. Generated files, log, baseline

- Run `just requirements-update`.
- Log: add a `### Garden myst, code-blocks, gfm` entry under `## 2026-11-18`, which is the top
  heading.
- Baseline: see §3 below.

## 2. Placement answers

- **Q3, MYST-097 →** `derives_from` StRS **CORE-001**.
  - It is approved, in force, and corrected by CR-347; CORE-088 carries "same in every mode".
  - The `derived_by` link that okfreq generates on CORE-001 is not authored text, so it needs no
    re-approval (garden-Q2).
  - MYST-036 and MYST-038 cite MYST-097 by `depends_on`.
- **Q6, GFM-009's alert-body click →** `SwRS-MDOKFSTUDIO-BLOCK-014` ("A click or Enter on a mapped
  block opens its editor").
  - It **already** holds the scenario: the nominal one at lines 62-66 ("title or the body of the
    alert … the whole alert"), the row at 81 and the notes at 181.
  - So remove the scenario from `GFM-009.md:147-155` and its notes at 187-188.
  - Then re-check each GFM-009 marker in `test/session/alertBlockEditOpen.test.ts` (74, 142, 172,
    200, 220, 228) and `test/visual/alertEditingScenarios.ts:15`. Those that test the click become
    BLOCK-014; those that test recognition stay.
  - `src/page/.../mappedBlocks.ts:121` (GFM-009): keep it only if it is recognition code.
- **Q7, MYST-063's table palette action → no PALETTE SwRS fits.**
  - `paletteActions` of the `table` directive (`src/core/directives/tables.ts:72`, value
    `["tableCaption","listTable","pipeTable"]`) has no runtime reader.
  - Only `test/core/directives/registry.test.ts:34` reads it (markers MYST-031 at :32 and MYST-063
    at :33).
  - The actions are TABLE-scope: TABLE-115 for the caption and TABLE-122 for the conversion.
  - Per the recommendation's fallback, **keep the scenario in MYST-063** (normative text at lines 9
    and 42, scenario at 85-90) and report it in the PR body.
- **MYST-031 `depends_on` → SwRS-MDOKFSTUDIO-TRUST-025** ("A resource reference resolves only to an
  existing file inside a root").
  - Its accepted row is: "a document in book/chapters, an image in book/external-img and the
    workspace folder as resource root → rewritten (parent-relative figure image)".
  - TRUST-002 only covers restricted reads and refuses those resources, so the spec's
    "TRUST-002 else CORE" premise is wrong.
  - TRUST-091 (restricted-reads images) is optional.
  - Keep the scenario at `MYST-031.md:61-64` as an outcome, and cite TRUST-025 for the rule.

## 3. Marker gate

Read `scripts/marker-baseline.json`. The value is the largest block size in the file.

Entries made only of CODE/GFM/MYST IDs (all must reach 0):
- `src/core/preview/styles/codeBlockStyles.ts` = 4. After the §5 removals it is 2.
- `src/core/preview/styles/contentBlockStyles.ts` = 5. Move the IDs to the companion.
- `test/integration/mystBlocksWindow.ts` = 4, the block at 150-153.
  - It becomes StRS (b) plus MYST-100, 098, 099, which is still 4.
  - Split it: put the StRS (b) marker alone on the test function, and the SwRS markers inside the
    body or on the helper each one checks.

Mixed entries that this CR clears:
- `src/core/render/mystRenderer.ts` = 4. After the change it holds CORE-001 and CORE-071, which is 2.
- `test/integration/labelRename.test.ts` = 4, the block at 35-38 (StRS MYST-009, TRUST-065,
  MYST-045, MYST-051). It becomes 3 once MYST-051 merges into MYST-045.

Mixed entries that must not grow:
- `src/page/features/contentPatch.ts:24-27` = 4. GFM-039 gets exactly one successor there, or the
  block is split.
- `src/session/features/sourceEdits.ts:145-148` = 4. It holds no ID of this CR.
- `test/core/protocol/pageStateMessages.test.ts:220-224` = 5. GFM-027 becomes GFM-021; if GFM-021
  is already in the block, the count drops.

After the edits:
- Run `node scripts/check-marker-companions.mjs --update`. It lowers the entries and removes those
  at 0.
- Never raise an entry.

## 4. Mechanics

**okfreq commands.** Prefix each with `uv run --no-sync --group requirements`.
- `okfreq supersede SwRS-MDOKFSTUDIO-CODE-005 SwRS-MDOKFSTUDIO-CODE-039 SwRS-MDOKFSTUDIO-CODE-001 --yes`
- Then the same for CODE-026→CODE-019, GFM-027→GFM-021, MYST-051→MYST-045 and MYST-101→MYST-096.
- Radio and dollar SwRS:
  - `okfreq new swrs "<title>" --description "<EARS>" --project markdown-okf-schema-studio --scope gfm --derives-from <radio StRS> --lifecycle proposed`, twice.
  - The same with `--scope myst --derives-from StRS-MDOKFSTUDIO-MYST-006` for dollar prices.
  - Then `okfreq supersede SwRS-…-GFM-039 <render> <choose> --yes`.
- New StRS: `okfreq new strs … --user-need … --lifecycle proposed`, five times (radio, a, b, c, d).
  Then `okfreq supersede StRS-MDOKFSTUDIO-MYST-001 <a> <b> <c> <d> --yes`.
- After that, run `just requirements-update`, which runs update-coverage and regenerates the Links
  blocks.
- Never hand-edit `status`, `verified` or Links.
- The sibling pattern is in the log entries of CR-345 (log.md:113) and CR-347 (log.md:159).

**Commits.** One commit per corrected approved StRS, as CR-345 did ("docs: correct the layout
requirement StRS-LAYOUT-003"):
- one for GFM-002's rationale and re-approval;
- one for the MYST-001 supersession.

Name both in the PR body under "Approved requirements changed".

**Diagram rule** (`requirements/guidelines/project.guidelines.md:81-108`):
- `### Use case diagram` comes after the last authored section and before `### Main paths`.
- It holds exactly one mermaid fence, plus an optional one-line caption.
- Kind: `sequenceDiagram` by default, `flowchart` for several roles, `stateDiagram-v2` for a mode.
- No SwRS IDs and no PlantUML.

The audit's "flow" (GFM-002, MYST-012) and "use case" (MYST-001) map to sequence, or to flowchart
when several roles take part. Example from `requirements/tiers/strs/block-editing/StRS-MDOKFSTUDIO-BLOCK-001.md`:

```text
### Use case diagram

The preview is in reading mode or in edit mode, and the writer or the saved choice moves it between them.

` ` `mermaid
stateDiagram-v2
    [*] --> Reading: new preview, any edit mode last chosen
    Reading --> Editing: writer clicks Edit, layout unchanged
    Editing --> Reading: writer clicks Edit, open editor saved
` ` `
```

**Mermaid limits:**
- `Box` is a reserved participant id; use `Field` or similar.
- `node` can parse only sequence diagrams. Flowchart and state diagrams need DOMPurify or a DOM,
  so check them by the site build or the GitHub branch preview.

**Checker.** Copy it into this CR's `work/scratch/`:
`…/changes/4-batch/2-actives/347-req-garden-core-diagrams-trust/work/scratch/mm2.mjs`. Run
`node mm2.mjs <worktree>`; `fix` rewrites `Box`.

**Size limits** (`scripts/check-file-sizes.mjs`: src 800 lines, test 1500; the baseline is empty).
- `test/visual/scenarioDefinitions2.ts` is at **1500**: every edit there must be line-neutral.
- Other files near their limit:
  - `test/core/preview/previewStyles.test.ts`: 1452.
  - `scenarioDefinitions1.ts`: 1454.
  - `mystFeatures.test.ts`: 1310.
  - `contentBlockStyles.ts`: 745 of 800.
  - `mystGridToctree.ts`: 741.

## 5. Risks

- The stack moves under you.
  - PR 418 (CR-347) and PR 415 (CR-345) are not landed; a rebase can shift every line above.
  - CR-347's sections 5-7 (markers and tests) are "not in this change yet". It may still touch
    `mystRenderer.ts:543-546`, `contentBlockStyles.ts`, `html-sanitizer.ts` or
    `renderReq.codeBlocks…:66`.
  - Touch only CODE, GFM and MYST IDs in those blocks.
- The MYST-001 supersede is the largest move: 12 SwRS, 4 new StRS, 4 diagrams and 4 validation
  markers. `check_main_paths.py` refuses a Main path that cites a SwRS no longer deriving from the
  StRS. Rewrite each successor's Main paths, and GFM-003's, in the same commit.
- The numref contradiction in MYST-019 (§7). Report it; do not fix the code.
- `scenarioDefinitions2.ts` is at 1500 lines. One added line fails `just check`.
- The integration files (`mystBlocksWindow.ts`, `labelRename.test.ts`, `labelRenameAboveTable.ts`,
  `radioChoice.test.ts`, `mystDiagnostics.test.ts`) are proven only by a heavy CI run.
- Splitting GFM-039 across about 30 test markers is error-prone. List them with grep first, then
  decide render or choose per test.
- Round budget 3: §7 (about 10 new tests) and §9 (14 diagrams) are the bulk. Do them after the
  requirement moves pass validation.

## 6. Ordered checklist for the Coder

1. Run `git log -1` and confirm the head is 3766a40e, or the rebased stack. Re-check the line
   numbers here with grep.
2. Do the SwRS supersessions and text edits (§4). After each one, run
   `okfreq validate --check-links --project-root .`.
3. Do the reparenting and `depends_on` work (§3), with Q3 → CORE-001 and MYST-031 → TRUST-025.
4. Create the radio StRS and its two SwRS, and supersede GFM-039.
5. Make the GFM-002 rationale and re-approval commit.
6. Create the four StRS, supersede MYST-001, move the `derives_from` links and Main paths, and
   commit.
7. Do the StRS text fixes and the format drift (§1). MYST-005 gets the widened title.
8. Apply Q6: remove the GFM-009 scenario and re-mark the click tests to BLOCK-014. Leave Q7 in
   MYST-063 and note it.
9. Do the code markers (§5) and the test markers (§6), with the corrected lines.
10. Add the tests (§7). Skip GFM-029 and the numref case; report numref.
11. Add the StRS validation markers and the math visual module (§8).
12. Add the diagrams (§9) and check them with mm2.mjs, sequence diagrams only.
13. Run `just requirements-update`, add the log entry, and run
    `node scripts/check-marker-companions.mjs --update`.
14. Run the gates below.

**Evidence plan:**
- `uv run --no-sync --group requirements okfreq validate --check-links --project-root .`
- `just requirements-lint`: the main-paths line shows all valid.
- `just requirements-report`.
- `just check`: markers and file sizes included.
- `just visual`: the new math scenario passes its assertions.
- `just preflight`: the static stage on Windows.
- `uv run --no-sync --group requirements okfreq trace requirements --json`: TRUST-005 and TRUST-065
  have no CODE-004, GFM-003 or MYST-009 parent; MYST-019 and MYST-097 have no MYST-005 parent;
  CORE-012 has no GFM-002 parent.
- `grep -rn "CODE-005\|CODE-026\|GFM-027\|GFM-039\|MYST-051\|MYST-101" src test sphinx` finds no
  marker.
- `grep StRS-MDOKFSTUDIO-MYST-001 test` finds nothing.
- The baseline has no CODE, GFM or MYST entry.
- Heavy CI: `gh workflow run ci.yml --ref <branch> -f heavy=true`, for the integration markers.
- PR body:
  - the IDs added, changed and superseded, with their files;
  - "Approved requirements changed" (GFM-002, MYST-001), naming their commits;
  - the Q7 and numref reports;
  - the placements the Driver chose.
