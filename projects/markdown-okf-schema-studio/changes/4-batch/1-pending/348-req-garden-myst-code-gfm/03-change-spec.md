# Change specification: garden the requirements of myst, code-blocks, gfm

Origin: verbal (owner, 2026-11-17), from the requirements gardening audit. No tracker issue.

## Goal

A human reviewer understands each use case of the `myst`, `code-blocks` and `gfm` scopes by
reading its StRS. Each SwRS is one observable behaviour. It is traced by `@implements_req` on the
code that does it and by `@tests_req` on each test that checks one of its scenarios. Each StRS
has a validation test on a real scenario and a use-case diagram.

The change touches requirement text, markers and tests. Product behaviour does not change. The
only `src/` edits move or remove marker comments.

## Sources and rules

- The findings and the proposed old-to-new mappings are in
  `projects/markdown-okf-schema-studio/changes/1-inbox/requirements-gardening/evidence/audit-myst-code-gfm.md`
  (planning surface). The audit was made at `main` dedbdb2a. Line numbers below come from it.
  Before you edit a line, check it again on the branch: the sibling CRs move lines.
- The constitution, `AGENTS.md`, `requirements/guidelines/requirements.guidelines.md`, the okfreq
  baseline and `requirements/guidelines/project.guidelines.md` apply ("During a change",
  "Approved requirements", "Main paths of a StRS"). Run okfreq as
  `uv run --no-sync --group requirements okfreq`.
- Owner decisions (02-answers.md, 2026-11-17):
  - D1. Published requirements are never deleted. Merges and splits use
    `okfreq supersede OLD NEW [NEW...] --yes` (or `okfreq archive`). Never use `git rm` or
    `okfreq retire` on a published requirement.
  - D2. The specification follows this group's audit report. The owner does not review the
    specification.
  - D3. The owner keeps three decisions. Bring each one back to the owner (through the Foreman);
    never take it alone:
    - the re-approval of an approved StRS whose text changes;
    - moving a requirement from `draft` to `proposed`;
    - a proposed merge or split the Driver doubts.
  - D4. No spec critic: the change touches requirement text, markers and tests, not product
    behaviour.
- Dependencies (`depends.json`): this CR starts after `req-use-case-diagrams` and
  `req-marker-gate` have landed. It uses the following from them:
  - the `### Use case diagram` rule, as written in `project.guidelines.md` by
    `req-use-case-diagrams`;
  - the marker gate of `req-marker-gate`: at most 3 IDs per marker comment, companion files
    naming a scenario per ID, and a baseline of offenders that can only shrink.
- Scope ownership with the five sibling `req-garden-*` CRs, which run in the same PR stack:
  - This CR edits the requirements of the `CODE`, `GFM` and `MYST` scopes.
  - In shared files (`contentBlockStyles.ts`, `html-sanitizer.ts`, `mystRenderer.ts`,
    `mystFeatures.test.ts`), it moves only the markers of those three scopes.
  - It edits a requirement of another scope only in the places named below: the
    `derives_from` of cross-scope SwRS, and scenarios moved out to another scope.
  - Rebase on whichever sibling lands first.

## Lifecycle state at the start

- Approved StRS: `StRS-MDOKFSTUDIO-GFM-002` and `StRS-MDOKFSTUDIO-MYST-001`. Both have owner
  `gaetan@xeberon.net` and were approved on 2026-11-12T12:30:00+01:00.
- The 8 other StRS in force are `proposed`: CODE-001, CODE-004, GFM-003, MYST-005, MYST-006,
  MYST-007, MYST-009 and MYST-012.
- The 44 SwRS of these scopes are all `proposed`, so they can be edited without re-approval.
- No `draft` requirement is in scope. If one appears, it moves to `proposed` only on the owner's
  word (D3).
- New StRS and SwRS are created with `okfreq new ... --lifecycle proposed`, per "Approved
  requirements".

## What changes

Requirements are `StRS-MDOKFSTUDIO-*` and `SwRS-MDOKFSTUDIO-*` under `requirements/tiers/`. IDs
below are short: "CODE-001" means the SwRS unless "StRS" is written.

### 1. StRS text fixes

- **StRS CODE-001** (proposed, no re-approval). Rewrite the normative text and the rationale so
  they match CODE-007, CODE-039 and CODE-040:
  - Highlighting does not follow the VS Code theme. It uses Dark+ colours in every preview theme,
    or Light+ when the setting is off (CODE-040).
  - Plain fences of two lines or more are numbered when the setting is on, which is the default
    (CODE-039). Line numbers are not limited to MyST directives.
  - Remove the leftover rationale bullet "the shared language list is not documented in
    docs/user/editing.md".
- **StRS GFM-002** (approved, so this is owner decision D3). The rationale says "only hex and rgb
  colours are kept". Fix it to the colours GFM-034 keeps: named, hex, rgb/rgba and hsl/hsla.
  - Make this change only with the owner's recorded agreement (open question Q1).
  - With agreement: set `approved_by` and `approved_at` (the current time with its UTC offset),
    list the StRS under "Approved requirements changed" in the PR body, and request the owner's
    review.
  - Without agreement: leave the StRS text unchanged and report the contradiction in the PR body.
- **StRS GFM-003** (proposed). Radio choices move to their own StRS (section 2). Remove Path 2
  (radio) from its Main paths. The title, user need and normative text stay about checkboxes. In
  the normative text, keep the refusals and say that each one returns the box to its previous
  state.
- **StRS MYST-005** (proposed). MYST-096 (an unparsable directive shows its source and the render
  continues) is a different need from "needs a build". Choose one of the two options of open
  question Q5:
  - widen the title to "Constructs the preview cannot build stay visible and labelled";
  - or add the parse case to the normative text.
- **StRS MYST-009** (proposed). The user need over-promises: a rename does not rewrite the
  references. Add to the normative text that the rename "tells the writer how many references
  still use the old name" (MYST-038, MYST-045).
- **Format drift** (proposed SwRS):
  - In MYST-096 and MYST-097, replace the first H2 `## EARS Expression` with `## <title>`.
  - In MYST-098, MYST-099 and MYST-100, write the `### Scenario: Nominal` and
    `### Scenario: Boundary or refusal` tables as named `### Scenario (<kind>): <name>` blocks.
    Give each key case of MYST-099 its own scenario.

### 2. New StRS and the MYST-001 split

- **New StRS (gfm) for radio choices:** "A writer or reviewer decides between the options of a
  plan with one click".
  - User need, from audit-crosscutting.md row 2: as a reviewer of an agent's plan, I pick one of
    the `( )`/`(x)` options in the preview and at most two source lines change in one undo step;
    on GitHub the text stays readable.
  - Main paths: take Path 2 of StRS GFM-003.
  - Its SwRS are the two that come out of GFM-039 (section 4).
- **Split of StRS MYST-001** (approved, owner decision D3, open question Q2). The audit proposes
  4 StRS, each `proposed`:
  - (a) callouts: admonitions and context tags (MYST-001, MYST-006, MYST-013). Version and
    Quarto admonitions get their place in the normative text here;
  - (b) layout blocks: grids, cards and tabs (MYST-053, MYST-098, MYST-099, MYST-100). Tabs and
    standalone cards get their place in the normative text here;
  - (c) figures and tables (MYST-031, MYST-063, GFM-031);
  - (d) inline text constructs (MYST-017).

  With the owner's agreement:
  - run `okfreq supersede StRS-MDOKFSTUDIO-MYST-001 <a> <b> <c> <d> --yes`;
  - move each SwRS's `derives_from` from MYST-001 to its new StRS;
  - list MYST-001 under "Approved requirements changed" and request the owner's review.

  Without agreement:
  - MYST-001 keeps its SwRS and its text unchanged;
  - only the proposed SwRS-level work of this spec is done;
  - the gap is reported in the PR body (Path 2 of MYST-001 covers tabs, which its normative text
    does not mention).

### 3. Reparenting

A shared rule is cited by `depends_on` and not derived. Each SwRS derives from the use case it
serves.

- Remove StRS CODE-004, GFM-003 and MYST-009 from the `derives_from` of these SwRS:
  - TRUST-005 (from GFM-003 and MYST-009);
  - TRUST-006 (from CODE-004);
  - TRUST-065 (from CODE-004 and MYST-009);
  - BLOCK-041 (from GFM-003 and MYST-009);
  - BLOCK-058 (from GFM-003).

  Each one keeps its other parents, so none becomes an orphan. Their new home parent belongs to
  `req-garden-core-diagrams-trust` and `req-garden-block-table`.
- Make sure the SwRS that use those rules cite them in `depends_on`:
  - CODE-017 and CODE-019: TRUST-006, TRUST-065;
  - GFM-021, the radio SwRS and MYST-045: TRUST-005, TRUST-065, BLOCK-041, BLOCK-058.
- CORE-012 (include):
  - remove StRS GFM-002 from its `derives_from`;
  - if MYST-001 is superseded (Q2), also remove MYST-001. CORE-012 keeps StRS CORE-002 and
    CORE-003.
- MYST-019 (`{ref}` links): remove StRS MYST-005 from its `derives_from`. It keeps MYST-009.
- MYST-097 (fences and front matter read the same way everywhere): remove StRS MYST-005 from its
  `derives_from`. Give it the rendering-core parent of open question Q3. Its users (MYST-036 and
  MYST-038 for label lists, and others that rely on it) cite it by `depends_on` where they
  depend on it.
- GFM-031: derives from StRS GFM-002 and from (c) if MYST-001 is split; otherwise from GFM-002
  and MYST-001.
- MYST-031 "A figure image outside the document folder loads": the resource policy is cited by
  `depends_on`, not written here. Cite TRUST-002 if its scenarios cover local resources outside
  the document folder; otherwise cite the CORE rule that does.

### 4. SwRS merges and splits

Every SwRS that is merged away is superseded, never deleted (D1). When it is merged away:

- move its markers onto the SwRS that receives its scenarios;
- carry its `depends_on` into that SwRS;
- remove it from any `depends_on` that still names it.

| Old | Action | New |
| --- | --- | --- |
| CODE-005 | The numbering and emphasis scenarios go to CODE-039, renamed "Code lines are numbered and emphasized". The "special characters shown once" scenario goes to CODE-001. The wrapping scenario is internal and becomes a verification note of CODE-039. | `okfreq supersede CODE-005 CODE-039 CODE-001 --yes` |
| CODE-001, CODE-007 | Their token-colour scenarios go to CODE-040. CODE-001 keeps grammar selection, the literal text and the fallback. CODE-007 keeps the block box (font, radius, scrolling); drop "the theme colours" from its title. | edits only |
| CODE-001 | The "not highlighted again" (cache) and "loads on the first code block" (bundle) scenarios move out, per Q4. | edits only |
| CODE-026 | Becomes refusal scenarios of CODE-019: invalid shape, oversized and no gesture. Its depends_on TRUST-052 and TRUST-065 move to CODE-019, and CODE-019 stops citing CODE-026. This also fixes CODE-026's H2/title mismatch. | `okfreq supersede CODE-026 CODE-019 --yes` |
| GFM-027 | Becomes refusal scenarios of GFM-021. Its depends_on TRUST-052 moves to GFM-021. | `okfreq supersede GFM-027 GFM-021 --yes` |
| GFM-039 | Split into two new gfm SwRS deriving from the new radio StRS: "A radio choice list renders as a radio group" (beside the scenarios of GFM-016) and "Choosing an option moves the (x)" (beside those of GFM-021; it depends_on GFM-021). | `okfreq new` ×2, then `okfreq supersede GFM-039 <render> <choose> --yes` |
| GFM-009 | Keeps alert recognition, title, body extent, fences and CRLF. "Every block keeps the lines of the document" becomes `depends_on` CORE-003. "A click in the body of an alert opens the whole alert" moves to a BLOCK-scope SwRS, per Q6. | edits only |
| GFM-008 | "Source lines of a table without a second parse" is internal and becomes a verification note. | edit only |
| MYST-053, MYST-100 | Card rendering ("A card shows its parts", "Card title link and empty card") moves to MYST-100, renamed "A card, in a grid or alone, shows header, title, body and footer". MYST-053 keeps the columns. | edits only |
| MYST-006 | Its gallery scenarios ("Admonition gallery ... without sideways scroll", "The MyST gallery renders without sideways scroll") become verification notes. | edit only |
| MYST-101 | Becomes a scenario of MYST-096: `+++` in a container renders as text. | `okfreq supersede MYST-101 MYST-096 --yes` |
| MYST-063 | "Offer the table palette action" is a palette concern. It moves to the PALETTE SwRS that offers that action, per Q7. | edit; the PALETTE side is coordinated with `req-garden-palette-theme-layout` |
| MYST-024 | Keeps typesetting, offline, active content refused, the invalid formula, Sphinx delimiters and scroll. A new myst SwRS deriving from StRS MYST-006 takes "dollar amounts and bold prices stay text". The cache and lazy-load scenarios move out, per Q4. | `okfreq new` (this is a split that keeps MYST-024, so no supersede) |
| MYST-078 | "The warning banner opens the Problems view" and "malformed previewShowProblems ignored" are removed. MYST-081 keeps them (add the malformed one to MYST-081 if it is missing). | edits only |
| MYST-051 | Becomes the accepted-shape and stale scenarios of MYST-045. Its depends_on TRUST-052 and TRUST-090 move to MYST-045. | `okfreq supersede MYST-051 MYST-045 --yes` |
| MYST-057 | "A target is read once per render" is internal (cache) and becomes a verification note. | edit only |

Result: CODE-005, CODE-026, GFM-027, GFM-039, MYST-051 and MYST-101 are superseded. Three SwRS
are added (two radio SwRS and the dollar-prices SwRS). Main paths that cite a superseded SwRS
are rewritten to cite its successor; `scripts/check_main_paths.py` refuses inactive citations.

If the Driver doubts one of these merges or splits while doing it (for example, a scenario does
not fit its new home), it brings the case back to the owner (D3) and does not improvise.

### 5. Code markers

Move each marker onto the code it names. Keep at most 3 IDs per marker comment, per the gate of
`req-marker-gate`.

- `src/core/preview/styles/contentBlockStyles.ts:6-19` (header block): move CODE-007, CODE-008,
  CODE-014, MYST-098 and MYST-100 to the CSS constant or rule block each one names. The other
  IDs there belong to sibling CRs.
- `src/core/preview/styles/codeBlockStyles.ts:18-21` (`CODE_BLOCK_CSS`):
  - keep CODE-039 and CODE-040;
  - remove CODE-005 (superseded);
  - move CODE-001 to its literal-text or fallback code in `src/core/render/highlight.ts` if it
    is not already marked there.
- `src/core/render/mystRenderer.ts:542-546` (`renderMyst`, the pipeline entry):
  - remove GFM-008, which is already at `mystEngine.ts:8` and `mystTables.ts:294`;
  - remove MYST-017, which is already at `mystBlockTransforms.ts:75`;
  - move GFM-029 to the sanitizer branch that drops the tags outside the subset (it is already at
    `mystBlockTransforms.ts:116`);
  - CORE-001 is left to `req-garden-core-diagrams-trust`.
- `src/core/security/html-sanitizer.ts:268-275` (`rewriteNode`): move GFM-016 to the
  checkbox-input branch and GFM-034 to the span-style branch.
- MYST-098:
  - remove it from the generic helpers: `src/core/render/mystNode.ts:66-67`
    (`sourcePositionProperties`), `src/core/render/mystNormalize.ts:529` and
    `src/page/features/editMode.ts:28`;
  - keep `mystGridToctree.ts:461,484`, `pageInput.ts:265` and its style.
- `src/session/pageMessages.ts:182` (`refuseStaleRequest`): remove MYST-038. TRUST-065 stays.
- Markers of the superseded SwRS (CODE-005, CODE-026, GFM-027, GFM-039, MYST-051, MYST-101) are
  moved onto their successors. After the change, `grep -rn` for these IDs in `src/`, `test/` and
  `sphinx/` finds nothing.
- The new radio and dollar-prices SwRS take the markers of the code they describe:
  - from GFM-039: the radio rendering code, the `checkboxMarkers.ts:80-81` pass if the radio
    markers go through it, and the radio toggle path;
  - from MYST-024: `mystInlineTransforms.ts:368,418,427`.

### 6. Test markers

On the wrong test:

- `test/core/preview/previewStyles.test.ts:380`: CODE-007 becomes CODE-039.
- `test/core/render/codeBlockComfort.requirements.test.ts:78,87`: CODE-001 becomes CODE-040 (the
  "Strict policy" scenario).
- `test/core/syntax/markdownSyntax.test.ts:108` ("escapeHtml and escapeRegExp"): remove MYST-097.
- `test/integration/mystDiagnostics.test.ts:36` (`runUntrusted`): MYST-081 becomes MYST-078.
- `test/core/render/mystTablesTree.test.ts:7,16,28`: remove GFM-008 from the internal HTML-pass
  tests, whose scenario becomes a verification note.
- `test/security/html-policy.test.ts:449`: rename the stale test "span style keeps only hex and
  rgb colour..." to what it checks (named, hex, rgb and hsl colours).

Cited in the verification notes but unmarked. Add one `@tests_req` on each test:

- CODE-001: `renderReq.codeBlocks.requirements.test.ts:66` (inline code; check whether it is
  CORE-028 instead), `:77`, `:99`; `highlight.test.ts:21`, `:104`.
- CODE-017: `test/page/modules/codeCopy.test.ts:256`. CODE-019: `:249`, `:365`, and the clipboard
  write in `test/session/renderReq.codeCopy.requirements.test.ts`.
- GFM-001: `test/core/render/bareUrlAutolink.test.ts:54`, `:79`, `:120`.
- GFM-031: `mystFeatures.test.ts:779`.
- MYST-001: `mystFeatures.test.ts:289`, `:513`, `:542`, `:563`.
- MYST-006: `:940`, `:563`.
- MYST-013: `:1000`, `:1040`, `:1069`, `:1103`.
- MYST-063: `:593`, `:718`, `:735`.
- MYST-053: `gridToctree.test.ts:88`, `:113`, `:136`. If a test checks card parts, mark it
  MYST-100.
- MYST-024: `test/core/render/mathRenderer.test.ts:25`, `:36`, `:45`.
- MYST-078: the unit tests cited in `pageToHost.test.ts`, `trustReq.requirements.test.ts` and
  `warningBanner.test.ts`.
- MYST-081: `test/page/modules/warningBanner.test.ts:109`, `:118`, `:126`, `:150`.
- MYST-066: `confLocator.test.ts:29`, `:50`, `:92`, `:130`; `confParser.test.ts:57`, `:84`.
- MYST-057: `test/core/render/gridToctree.test.ts:176`, `:185`, `:192`;
  `renderReq.myst.requirements.test.ts:52`.
- MYST-019: `mystPaletteRendering.test.ts:221`, only if it checks MYST-019's behaviour.

Every SwRS's verification notes name the real tests that check its scenarios. Each test named
there carries the marker.

### 7. Tests for scenarios no test checks

Add a test, in the layer where the behaviour lives (unit, session or page first; integration
only when the behaviour needs a real VS Code window), for each of these scenarios:

- CODE-001: "A shorter backtick line does not close the fence".
- CODE-007: the box. Check the 0.92em font, the 4 px radius, the border and the nested block
  (nothing in `test/` matches `0.92em` today). Also check "an exact-fit line needs no scrollbar".
- CODE-019: "A second click restarts the confirmation".
- GFM-008: footnote "Reference without definition".
- GFM-029: refusal "Kbd with attributes".
- GFM-021 host refusals:
  - the marker is gone;
  - a Markdown edit is open;
  - the apply fails;
  - the apply path with no visible editor (with `test/session/radioChoice.test.ts:185` as the
    pattern).

  Also cover the no-editor note of the new "choosing an option" radio SwRS.
- MYST-024: "The KaTeX bundle is missing", as a named test.
- MYST-053: "Grids deeper than 8 levels".
- MYST-019: "A reference to a heading shows the heading text" (the test checks the link text),
  and the `{numref}` case.
- MYST-081: the refusal its notes call untested, if `warningBanner.test.ts:109` does not already
  cover it.

When the code does something other than what a scenario says, do not change the code. Stop and
report it: it is a bug to file, not part of this CR.

### 8. StRS validation tests

`strs_test_coverage_mode: linked-swrs-and-validation-test`. Each StRS in force carries one
`@tests_req StRS-...` on a real scenario, not on a companion list.

- StRS CODE-001: add a marker to `test/visual/scenarioDefinitions1.ts:702` (`diff-dark-preview`)
  for Path 2.
- StRS MYST-006 (it has none today):
  - add a visual fixture under `test/visual/fixtures/` with display maths, dollar prices and one
    invalid formula;
  - add a scenario in `test/visual/scenarioDefinitions2.ts` with `contentAssertions`: KaTeX
    elements present, and the invalid formula shown as readable source
    (`data-studio-math-error`);
  - put the StRS marker on that scenario.
- StRS MYST-005: add a marker to the unclosed-directive visual scenarios
  (`scenarioDefinitions1.ts:1368`, `:1384`) for Path 2.
- StRS MYST-009: add a marker to `test/integration/realInput/labelRenameAboveTable.ts:43` (the
  real anchor-click path). Keep `labelRename.test.ts:35`.
- New radio StRS: add a marker to `test/integration/radioChoice.test.ts:187`.
- MYST-001 successors (Q2), one validation each:
  - (a): `scenarioDefinitions1.ts:212` (`admonitions-dark-full`);
  - (b): `test/integration/mystBlocksWindow.ts:150` (tabs, cards);
  - (c): `scenarioDefinitions2.ts:699` (`figure-anchors`) or the table scenario at `:833`;
  - (d): a visual scenario that shows definition lists and roles, with a content assertion. Add
    the assertion to an existing scenario if none checks them.

  If MYST-001 is not split, add its marker to `mystBlocksWindow.ts:150` for Path 2 (tabs).
- StRS CODE-004, GFM-002, GFM-003, MYST-007 and MYST-012 already have a validation test.

### 9. Use-case diagrams

- Each StRS of these scopes that is in force carries a `### Use case diagram` section, as the
  rule landed by `req-use-case-diagrams` says. That covers the 10 StRS less MYST-001 if it is
  split, plus the new radio StRS and the MYST-001 successors.
- Draw the content from the "Diagram" item of each StRS in the audit.
- Use the kinds that the landed rule allows (sequence by default, actors when several roles
  take part, state for a mode). Where the audit proposes a "flow" (GFM-002, MYST-012) or a "use
  case" (MYST-001), use the closest allowed kind unless the rule allows flowcharts.
- Each diagram states only what a cited SwRS specifies.
- Adding the section to an approved StRS (GFM-002, and MYST-001 if it is not split) changes its
  text, so it falls under Q1 and Q2.

### 10. Generated files, log and gate baseline

- `just requirements-update`; commit the generated fields and the Links blocks.
- One entry in `requirements/tiers/log.md` under its `## YYYY-MM-DD` heading, with a
  `### Garden myst, code-blocks, gfm` sub-heading. It holds:
  - the old-to-new mapping of section 4;
  - the reparentings;
  - the StRS text changes;
  - the owner's answers to Q1 and Q2.
- Remove from the marker-gate baseline of `req-marker-gate` every entry made only of CODE, GFM
  or MYST IDs. The baseline only shrinks.
- No rendered syntax changes, so the writing skill `skills/writing-for-markdown-okf-schema-studio/`
  is not touched. No settings, CI workflow or `ci-*` target changes.

## Out of scope

- Deleting any published or retired requirement (D1).
- Any product behaviour change, including a bug found in section 7, which is filed separately.
- GFM-029 versus CORE-071 (two raw HTML subsets): owned by `req-garden-core-diagrams-trust`
  (finding 6 of its audit).
- The markers of other scopes in shared files, the new home parent of TRUST-005, TRUST-006,
  TRUST-065, BLOCK-041 and BLOCK-058, and the CORE-001 marker on `renderMyst`: owned by the
  sibling CRs.
- The diagram rendering on the site, and making the diagram section mandatory
  (`req-use-case-diagrams` and later).
- `draft` to `proposed` moves (D3).

## Evidence

- `uv run --no-sync --group requirements okfreq validate --check-links --project-root .`
  passes, with coverage run with CI's okfreq version.
- `just requirements-lint` passes. Its main-paths line reports no invalid citation.
- `just requirements-report`: every StRS of these scopes has a validation test and linked SwRS.
  Every SwRS of these scopes has an implementation and a test link.
- `just check` passes, the marker gate included. The baseline has no CODE, GFM or MYST entry
  left.
- `grep -rn` finds no marker for CODE-005, CODE-026, GFM-027, GFM-039, MYST-051 or MYST-101.
- `okfreq trace requirements --json`: CODE-004, GFM-003 and MYST-009 no longer derive TRUST-005,
  TRUST-006, TRUST-065, BLOCK-041 or BLOCK-058. MYST-005 no longer derives MYST-019 or MYST-097.
  GFM-002 no longer derives CORE-012.
- Every new test passes in `just check` (unit, contract) or `just visual`. The new MYST-006
  visual scenario appears in the gallery with its content assertions passing.
- `just preflight` passes (on Windows its static stage; CI runs the rest).
- New integration tests, or markers added to integration files, are proven by a heavy CI run on
  the branch: `gh workflow run ci.yml --ref <branch> -f heavy=true`. The real VS Code jobs do not
  run on a pull request.
- The PR body:
  - lists the requirement IDs added, changed and superseded, with their source and test files;
  - has "Approved requirements changed" (GFM-002, MYST-001) with the owner's recorded agreement,
    if Q1 or Q2 was agreed;
  - requests the owner's review.

## Open questions (for the owner)

Q1 and Q2 are owner decisions (D3). Q3 to Q7 are points where the audit offers options and the
answers do not choose. Each question gives a recommendation, which the Driver applies only if
the owner confirms it.

- **Q1. StRS GFM-002 (approved).** Do you agree to fix its rationale to "named, hex, rgb/rgba
  and hsl/hsla colours are kept" (the behaviour GFM-034 and its tests show) and to add its
  use-case diagram, with a new approval date? Recommendation: yes.
- **Q2. StRS MYST-001 (approved).** Do you agree to supersede it by four `proposed` StRS:
  (a) callouts, (b) layout blocks (grids, cards, tabs), (c) figures and tables, (d) inline text
  constructs? Or do you prefer three StRS, with (d) folded into (a) or (c)? Recommendation: four,
  as the audit proposes.
- **Q3. New parent of MYST-097** (fences and front matter read the same way everywhere).
  Recommendation: StRS CORE-001, or its successor in `req-garden-core-diagrams-trust` that holds
  "CommonMark constructs render the same in every mode". Its users cite it by `depends_on`.
- **Q4. Cache and lazy-load scenarios** of CODE-001 and MYST-024: should they become verification
  notes, or a CORE performance or bundle SwRS? Recommendation: verification notes. The SwRS
  would need a sibling CR's scope, and no user observes the cache.
- **Q5. StRS MYST-005:** widen the title to "Constructs the preview cannot build stay visible and
  labelled", or keep the title and add the parse case to the normative text? Recommendation:
  widen the title.
- **Q6. GFM-009 "A click in the body of an alert opens the whole alert":** which BLOCK SwRS
  receives it? Recommendation: the BLOCK SwRS that specifies click-to-edit of a container block,
  coordinated with `req-garden-block-table`. If none fits, keep the scenario in GFM-009 and
  report it.
- **Q7. MYST-063 "offer the table palette action":** which PALETTE SwRS receives it?
  Recommendation: the PALETTE SwRS of the table action, coordinated with
  `req-garden-palette-theme-layout`. If none fits, keep the scenario in MYST-063 and report it.
