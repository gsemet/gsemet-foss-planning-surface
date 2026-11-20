# Audit: scopes myst, code-blocks, gfm (read-only)

Repository `markdown-okf-schema-studio` at `main` (dedbdb2a), 2026-11-17. Phases 4, 6 and 6b of
the okfreq-gardening skill, read-only. Sources: frontmatter of every requirement, `okfreq trace
requirements --json`, `@implements_req` / `@tests_req` lines with the code or test that follows.

In force: 10 StRS (CODE-001, CODE-004, GFM-002, GFM-003, MYST-001, MYST-005, MYST-006, MYST-007,
MYST-009, MYST-012), 44 SwRS of these scopes, plus 8 cross-scope SwRS that they derive (CORE-012,
CORE-022, CORE-028, TRUST-005, TRUST-006, TRUST-065, BLOCK-041, BLOCK-058). 12 StRS of these scopes
are superseded, and each one names its replacement. No in-force StRS cites an inactive SwRS in its
body or Main paths. `derived_by` matches `derives_from`. **No orphan SwRS.**

Marker convention used: a `@tests_req` marks the test that follows it. A test that the verification
notes cite but that carries no marker is listed as "unmarked".

## Summary

| StRS | Title | #SwRS (own + cross) | Relevance | Split OK? | Markers OK? | Tests OK? | Validation test? | Diagram |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CODE-001 | A reader reads highlighted, numbered and diff code | 7 + 1 | Real; **text contradicts its SwRS** | No | Partly | Partly | Yes (visual) | State |
| CODE-004 | A reader copies the exact code of a block | 3 + 2 | Real, clear | Mostly | Yes | Partly | Partial (visual) | Sequence |
| GFM-002 | GFM renders as on GitHub, safely | 6 + 1 | Real; **approved text contradicts GFM-034** | No | Partly | Partly | Yes (visual) | Flow |
| GFM-003 | A writer toggles task checkboxes from the preview | 4 + 3 | Real; radio choice missing from the normative text | Uneven | Yes | Partly | Yes (integration) | Sequence |
| MYST-001 | MyST directives and roles render as readable blocks | 12 + 2 | Real but a catalogue, too broad | No | Partly | Partly | Yes (visual) | Use case |
| MYST-005 | Build-dependent constructs appear as labelled placeholders | 1 + 3 | Real; 2 of 4 SwRS do not fit it | No | Yes | Partly | Yes (visual) | State |
| MYST-006 | Maths is typeset offline and bad formulas stay readable | 1 | Real, short and clear | No (1 oversized SwRS) | Yes | Partly | **No** | Sequence |
| MYST-007 | Sphinx configuration gaps are reported before building | 4 | Real, good | Mostly | Yes | Partly | Yes (integration + visual) | Sequence |
| MYST-009 | A writer sees, links and renames labels safely | 5 + 3 | Real; the user need promises more than the SwRS give | Mostly | Mostly | Mostly | Partial (integration at message level) | Sequence |
| MYST-012 | A toctree shows the linked documents and marks missing ones | 1 | Real, short | Yes | Yes | Partly | Yes (visual) | Flow |

## StRS-MDOKFSTUDIO-CODE-001: highlighted, numbered and diff code

SwRS: CODE-001, 005, 007, 008, 014, 039, 040, plus CORE-028 (inline code).

1. **[high] The StRS contradicts its SwRS.** The normative text says the highlighting "follows the VS
   Code theme". CODE-007 has the scenario "The colours do not depend on the VS Code theme", and
   CODE-040 draws Dark+ in every preview theme, or Light+ when its setting is off. The rationale
   says "Line numbers ... apply to MyST code directives; plain fences are covered by the
   highlighted code samples", but CODE-039 numbers plain fences of two lines or more (setting on
   by default). Rationale bullet 1 ("the shared language list is not documented in
   docs/user/editing.md") reads as a leftover. Rewrite the normative text and the rationale to
   match CODE-007, CODE-039 and CODE-040.
2. **[medium] Split.** CODE-005 is a grab-bag: wrapping into lines (internal markup), MyST
   numbering and emphasis (overlaps CODE-039), and "special characters shown once" (escaping,
   which belongs with the literal-text rule of CODE-001). CODE-001 has 9 scenarios, two of them
   internal: "not highlighted again" (cache) and "loads on the first code block" (bundle split).
   CODE-007 repeats the Dark+ token colours of CODE-001 and CODE-040. Proposed mapping:
   - CODE-005 numbering and emphasis go into CODE-039, renamed "Code lines are numbered and
     emphasized". The special-characters scenario goes to CODE-001. The wrapping scenario is
     dropped as internal. Then supersede CODE-005.
   - The token-colour scenarios of CODE-001 and CODE-007 go to CODE-040 (colours by setting and
     theme). CODE-001 keeps grammar selection, the literal text and the fallback. CODE-007 keeps
     the block box (font, radius, scrolling).
   - The cache and lazy-load scenarios of CODE-001 move to a performance or bundle SwRS of
     rendering-core, or become verification notes.
3. **[medium] Markers.**
   - `src/core/preview/styles/contentBlockStyles.ts:6-16` is a file-header block of 11 or more
     markers (CODE-007, CODE-008, CODE-014, MYST-098, MYST-100, CORE-028 and others) on one large
     stylesheet. Move each marker to the CSS block it names.
   - `src/core/preview/styles/codeBlockStyles.ts:18-21` puts 4 markers on `CODE_BLOCK_CSS`.
     CODE-039 and CODE-040 fit there; CODE-001 and CODE-005 are weak there.
   - These are well placed: `highlight.ts:219` (diff classification), `:232-233` (line wrapper),
     `:256-258`, `mystNormalize.ts:210-211` (code options), `settingsRegistry.ts:215,224` and
     `pageSettings.ts:33-34`.
4. **[medium] Tests.**
   - `test/core/preview/previewStyles.test.ts:380` is marked CODE-007, but it tests the styles of
     numbered and emphasized lines (CODE-005 or CODE-039).
   - The CODE-007 scenarios for the box (0.92em, 4 px radius, border, nested block) and "exact-fit
     line needs no scrollbar" have no test: nothing in `test/` matches `0.92em`. Only
     `scenarioDefinitions1.ts:745` (long-line scroll) and the cream test are marked.
   - CODE-001 markers sit on CSP tests (`codeBlockComfort.requirements.test.ts:78,87`). Those
     check the "Strict policy" scenario of CODE-040.
   - Cited but unmarked CODE-001 tests: `renderReq.codeBlocks.requirements.test.ts:66` (inline
     code), `:77` (fallback), `:99` (literal fence text), `highlight.test.ts:21` (aliases) and
     `:104` (unknown language). CODE-001 scenario "A shorter backtick line does not close the
     fence" has no named test.
5. **[low] Validation.** `test/visual/scenarioDefinitions1.ts:659` (syntax-dark-rust) and
   `scenarioDefinitions2.ts:753` (caption) carry the StRS. Nothing validates Path 2 (diff) at
   StRS level; adding the StRS marker to `scenarioDefinitions1.ts:702` (diff-dark-preview) would
   cover it.
6. **Diagram (state).** States: fenced block → language known? → highlighted / literal → (two
   lines or more and setting on) numbered. Side branch: diff label → lines marked +/-. Side
   branch: MyST directive with `:caption:` or `:filename:` → title bar.

## StRS-MDOKFSTUDIO-CODE-004: copy the exact code

SwRS: CODE-017, 019, 026, plus TRUST-006 and TRUST-065 (shared rules).

1. **[medium] Split.** CODE-026 (copy request validation and size limit) is the host-side refusal
   of CODE-019. The guideline asks protocol shapes to stay with the behaviour they serve: merge
   CODE-026 into CODE-019 as refusal scenarios. CODE-017 (9 scenarios, 1073 words) is detailed
   but is one behaviour.
2. **[low] Wording.** The H2 of CODE-026 reads "An invalid, oversized or gestureless copy request
   is refused", but its title and description omit the gesture refusal that its test checks
   (`test/session/renderReq.codeCopy.requirements.test.ts:86`). Align them.
3. **[medium] Cross-derivations.** TRUST-065 (13 parent StRS) and TRUST-006 (7) are shared rules
   that CODE-017, CODE-019 and CODE-026 already cite through `depends_on`. Deriving them from this
   StRS as well is the repetition the guideline forbids. Keep `depends_on` only. This applies to
   every StRS below as well.
4. **Markers** OK. `src/page/modules/codeCopy.ts:1` is a header marker, but the file is
   dedicated to the button. `codeCopy.ts:77,100`, `contentPatch.ts:59` (hide on patch),
   `pageToHost.ts:241` and `hostRequests.ts:154` are precise.
5. **[medium] Tests.**
   - Unmarked tests of CODE-019: `test/page/modules/codeCopy.test.ts:249` (focus kept) and `:365`
     (edit mode opens no editor).
   - Unmarked test of CODE-017: `:256` (excluded blocks).
   - CODE-019 scenario "A second click restarts the confirmation" has no named test.
   - CODE-019 verification cites `test/session/renderReq.codeCopy.requirements.test.ts` for the
     clipboard write, but that file only marks CODE-026.
6. **[low] Validation.** `scenarioDefinitions1.ts:444` (code-copy-button) carries the StRS. It is
   a screenshot with `codeCopyChecks`: the post of the raw code is checked, the real clipboard is
   not. Acceptable.
7. **Diagram (sequence).** Reader → Page: hover or Tab → Page shows button → Reader clicks →
   Page → Host: previewCopyText (gesture) → Host validates (size, render gate) → Host writes the
   clipboard → Host → Page: ok or reason → Page shows "Copied" or the reason.

## StRS-MDOKFSTUDIO-GFM-002: GFM renders as on GitHub, safely (approved)

SwRS: GFM-001, 008, 009, 029, 031, 034, plus CORE-012.

1. **[high] The approved StRS contradicts its SwRS.** The rationale says "only hex and rgb colours
   are kept on coloured text". GFM-034 keeps named, hex, rgb/rgba and hsl/hsla, and its tests
   prove it: `test/core/security/spanColors.test.ts:20,47` and `mystFeatures.test.ts:828` ("keeps
   named, hex, rgb and hsl"). The test name at `test/security/html-policy.test.ts:449` ("keeps
   only hex and rgb") is stale too. Fixing the StRS needs the owner's agreement (approved, locked).
2. **[medium] Misderivation.** CORE-012 (include expansion) derives from GFM-002 (and from
   MYST-001). An include is not GFM; only its "alerts in included files" scenario touches GFM.
   Drop GFM-002 from its `derives_from`.
3. **[medium] Split.** GFM-009 has 2502 words and 12 scenarios. Two of them belong elsewhere:
   - "Every block keeps the lines of the document": source-line mapping, a rule of CORE-003. Cite
     it through `depends_on`.
   - "A click in the body of an alert opens the whole alert": a block-editing behaviour (BLOCK
     scope).

   GFM-008 "Source lines of a table without a second parse" is internal (no second parse).
   Mapping: move those three scenarios out, and keep GFM-009 as alert recognition, title, body
   extent, fences and CRLF.
4. **[medium] Markers.**
   - `src/core/render/mystRenderer.ts:542-546` puts GFM-029, GFM-008 and MYST-017 (with CORE-001)
     on `renderMyst`, the entry point of the whole pipeline. GFM-008 is already at
     `mystEngine.ts:8` (strikethrough option) and `mystTables.ts:294` (alignment). MYST-017 is
     already at `mystBlockTransforms.ts:75`. GFM-029 belongs at `mystBlockTransforms.ts:116`
     (details and kbd, already marked) and the sanitizer drop.
   - `src/core/security/html-sanitizer.ts:268-275` puts 8 markers on `rewriteNode`, among them
     GFM-016 and GFM-034. Move them to the checkbox-input branch and the span-style branch of the
     function.
   - `spanColors.ts:1` (dedicated file), `mystInlineTransforms.ts:178` (autolink) and
     `mystGithubAlerts.ts:42,164` are fine.
5. **[medium] Tests.**
   - GFM-001: 1 of 8 tests marked (`test/core/render/bareUrlAutolink.test.ts:21`). The refusal and
     linear-time tests at `:54`, `:79` and `:120` are unmarked.
   - GFM-029: the refusal "Kbd with attributes" is untested; its verification notes admit it.
   - GFM-031: "raw HTML table cell styles are preserved" (`mystFeatures.test.ts:779`) is unmarked.
   - GFM-008: two of its five markers sit on internal HTML-pass tests
     (`mystTablesTree.test.ts:7,16,28`). Footnote "Reference without definition" has no marked
     test.
6. **Validation** OK. `scenarioDefinitions2.ts:788` (gfm gallery, 3 widths, content assertions).
7. **Diagram (flow).** Markdown source → MyST/GFM parse (autolink, strikethrough, footnotes,
   tables, alerts) → raw-HTML allow-list (details, kbd, table, span) → sanitizer drops unsafe
   tags, styles and schemes → page applies the revalidated colours → rendered preview.

## StRS-MDOKFSTUDIO-GFM-003: toggle task checkboxes

SwRS: GFM-016, 021, 027, 039, plus BLOCK-041, BLOCK-058 and TRUST-005 (shared rules).

1. **[medium] Relevance.** Path 2 and GFM-039 add radio choice lists, but the title, the user need
   and the normative text speak only of checkboxes. Widen the text to "task checkboxes and radio
   choices", or move radio choices to a StRS of their own.
2. **[medium] Uneven split.** The checkbox needs 3 SwRS: render (GFM-016), toggle (GFM-021) and
   message validation (GFM-027). The radio does all of it in one SwRS (GFM-039: 1595 words, 9
   implementation files). Proposed mapping:
   - GFM-027 → merge into GFM-021 as refusal scenarios (a protocol shape belongs to its
     behaviour).
   - GFM-039 → split into "radio group renders" (with GFM-016's sibling scenarios) and "choosing
     an option moves the (x)" (with GFM-021's).
3. **[medium] Cross-derivations.** BLOCK-041, BLOCK-058 and TRUST-005 are listed both as
   `depends_on` of GFM-021 and GFM-039 and as derived from this StRS. Keep `depends_on` only.
4. **Markers** OK and specific: `sourceEdits.ts:50,69`, `checkboxes.ts:72-247`,
   `session/features/sourceEdits.ts:87-120`, `pageToHost.ts:94,235` and
   `pageMessages.ts:136`.
   - `checkboxMarkers.ts:80-81` (GFM-039 on the checkbox placeholder pass) is plausible only if
     the radio markers go through it.
   - `contentPatch.ts:25-26` marks the scenario "content patches clear pending toggles". Fine.
5. **[high] Tests.** GFM-021 declares "Untested: the host refusal paths (marker gone, open
   Markdown edit, apply failure)" and the no-visible-editor apply path. These refusals are in
   the StRS normative text ("refuse with a reason when the preview is stale"). Only the read-only
   case is tested (`test/session/radioChoice.test.ts:185`). GFM-039 has the same untested
   no-editor note.
6. **Validation** OK. `test/integration/checkboxToggle.test.ts:109`: a real VS Code window, a
   real CDP click, both modes. Nothing validates Path 2 at StRS level;
   `test/integration/radioChoice.test.ts:187` could also carry the StRS.
7. **Diagram (sequence).** Writer → Page: click box → Page marks busy and posts previewCheckboxToggle
   → Host validates the message and the render gate → alt (editor open, stale, read-only): Host →
   Page: reason, box reverts → else Host edits one character as one undo step → Host re-renders
   once → Page shows the ticked box.

## StRS-MDOKFSTUDIO-MYST-001: MyST directives and roles (approved)

SwRS: MYST-001, 006, 013, 017, 031, 053, 063, 098, 099, 100, 101, plus CORE-012 and GFM-031.

1. **[medium] Relevance and readability.** This is a catalogue of 7 construct families and 14
   SwRS, against a guideline of 3 to 8 per StRS. Tabs, standalone cards, version and Quarto
   admonitions are not in the normative text, although Path 2 is about tabs. Proposed StRS
   split, which needs the owner's agreement:
   - (a) callouts: admonitions and context tags (MYST-001, 006, 013);
   - (b) layout blocks: grids, cards and tabs (MYST-053, 098, 099, 100, 101);
   - (c) figures and tables (MYST-031, 063, GFM-031);
   - (d) inline text constructs (MYST-017).
2. **[medium] Split.**
   - MYST-053 ("A card shows its parts", "Card title link and empty card") and MYST-100
     (standalone card parts) are near-duplicates. Merge the card rendering into MYST-100 ("A
     card, in a grid or alone, shows header, title, body and footer"); MYST-053 keeps the
     columns.
   - The gallery scenarios of MYST-006 ("Admonition gallery ... without sideways scroll", "The
     MyST gallery renders without sideways scroll") are test fixtures, not behaviours. Move them
     to the verification notes.
   - MYST-101 (`+++` in a container renders as text) is a parser-robustness rule. It fits MYST-096
     ("the render continues") better: merge it there.
   - MYST-031 "A figure image outside the document folder loads" is the resource policy (TRUST-002
     or a CORE rule). Cite it with `depends_on`.
   - MYST-063 "offer the table palette action" is a palette concern.
3. **[low] Format drift.** MYST-098, 099, 100 and 101 use `### Scenario: Nominal` and `### Scenario:
   Boundary or refusal` with tables, not named `Scenario (kind): name` blocks. MYST-099 hides all
   its key cases in one table.
4. **[medium] Markers.** MYST-098 sits on generic helpers:
   - `src/core/render/mystNode.ts:66-67` (`sourcePositionProperties`, used by every block);
   - `src/core/render/mystNormalize.ts:529` (the generic block-line mapping);
   - `src/page/features/editMode.ts:28` (edit hover).

   Keep only `mystGridToctree.ts:461,484` (tab-set build), `pageInput.ts:265` (tab-bar click
   exclusion) and the style. Elsewhere `admonition.ts:11,26`, `mystNormalize.ts:321-322`,
   `mystContextTags.ts:100`, `figure.ts:13`, `tables.ts:38`, `mystGridToctree.ts:278,356` and
   `tabs.ts:47,83` are well placed.
5. **[medium] Tests.** The verification notes cite tests that carry no marker:
   - MYST-001: `test/core/render/mystFeatures.test.ts:289` (custom title), `:513` (untitled),
     `:542` (Quarto), `:563` (simple, icon-less and dropdown).
   - MYST-006: `:940` (mapped block; the marker at `:908` is CORE-003) and `:563` (dropdown).
   - MYST-013: `:1000`, `:1040`, `:1069`, `:1103` (nested, unpaired and non-context tags).
   - MYST-063: `:593`, `:718`, `:735`.
   - MYST-053: `gridToctree.test.ts:88`, `:113`, `:136`.

   MYST-053 "Grids deeper than 8 levels" is untested, as its notes admit.
6. **Validation** OK. `scenarioDefinitions1.ts:212` (admonitions-dark-full) and
   `scenarioDefinitions2.ts:551,699` carry the StRS. Path 2 (tabs) is validated only by SwRS-level
   markers in `test/integration/mystBlocksWindow.ts:150-153`; that file could carry the StRS.
7. **Diagram (use case).** Actor Writer, with one use case per family: "see a callout",
   "see a layout block", "see a figure or table", "read inline constructs". Each use case extends
   to its SwRS. If the StRS is split, use one small sequence per new StRS, for example tabs:
   Writer → Page: click or arrow key → Page selects the tab and its synced tabs → panel shown.

## StRS-MDOKFSTUDIO-MYST-005: build-dependent constructs as placeholders

SwRS: CORE-022, MYST-019, MYST-096, MYST-097.

1. **[high] Two SwRS do not serve this use case.**
   - MYST-019 (`{ref}` links) derives from MYST-005 and MYST-009. It has no placeholder or build
     scenario; its unresolved-target case is "a missing label raises no warning". Drop MYST-005
     from its `derives_from`.
   - MYST-097 ("Code fences and front matter are read the same way everywhere") is an internal
     consistency rule across renderer, comment anchoring, link fragments and label lists. It is
     not observable on its own and not about placeholders. It should be a rendering-core rule that
     others cite with `depends_on`; as an SwRS, its parent is a rendering or review StRS.
2. **[low] Title too narrow.** MYST-096 (an unparsable directive shows its source and the render
   continues) is a different need from "needs a build". Either widen the StRS to "Constructs the
   preview cannot build stay visible and labelled", or keep the two paths and add the parse case
   to the normative text.
3. **[low] Format drift.** MYST-096 and MYST-097 start with `## EARS Expression`, not the title.
4. **Markers** OK: `mystDirectiveErrors.ts:10`, `mystUnclosedFences.ts:35`, and
   `markdownSyntax.ts:6,13,36` on the primitives.
5. **[medium] Tests.** `test/core/syntax/markdownSyntax.test.ts:108` marks MYST-097 on "escapeHtml
   and escapeRegExp", an unrelated test. MYST-096 is well covered: 14 marked tests in
   `renderReq.syntaxErrors.requirements.test.ts`.
6. **Validation** OK. `scenarioDefinitions1.ts:267` (unresolved-dark-full) covers Path 1. Path 2 is
   covered by SwRS-level visual scenarios (`:1368`, `:1384`), which could carry the StRS.
7. **Diagram (state).** Construct in source → recognised? → rendered; build-only → muted
   placeholder plus warning; unparsable → raw source as a code block, and the render continues.

## StRS-MDOKFSTUDIO-MYST-006: offline maths

SwRS: MYST-024 (13 scenarios, 1063 words).

1. **[medium] Split.** MYST-024 holds four behaviours: typesetting, invalid-formula fallback,
   dollar prices kept as text, and long-equation scroll. It also holds two internal scenarios:
   "not typeset again" (cache) and "KaTeX loads on the first equation" (bundle). Proposed mapping:
   - MYST-024 keeps typesetting, offline, active content refused, the invalid formula, Sphinx
     delimiters and scroll.
   - A new SwRS takes "dollar amounts and bold prices stay text".
   - The cache and lazy-load scenarios move to a CORE performance or bundle SwRS, or to the
     verification notes.
2. **Markers** OK: `mathRenderer.ts:79`, and `mystInlineTransforms.ts:368,418,427` (dollar
   handling).
3. **[high] Tests.** The refusal at the heart of this StRS is checked, but by unmarked tests:
   - "Unparsable formulas stay readable": `test/core/render/mathRenderer.test.ts:36`;
   - "Maths cannot run active content": `:45`;
   - "Sphinx delimiters": `:25`.

   "The KaTeX bundle is missing" has no named test besides the general one at `:9`. The marked
   tests are mostly dollar, cache and bundle tests.
4. **[medium] Validation.** No `@tests_req StRS-MDOKFSTUDIO-MYST-006` anywhere. Candidate: the
   visual scenario `scenarioDefinitions1.ts:587` (chapter-dark-half, display maths) or
   `scenarioDefinitions2.ts:1372` (dollar prices, which has three real maths spans). Neither shows
   an invalid formula; a fixture with one bad formula would complete it.
5. **Diagram (sequence).** Writer types `$...$` → renderer marks maths nodes and protects dollar
   prices → KaTeX (bundled, lazy) typesets → alt (parse error): the source is shown as readable
   text → page shows the formula, with long ones scrolling in their box.

## StRS-MDOKFSTUDIO-MYST-007: Sphinx configuration gaps

SwRS: MYST-066, 072, 078, 081.

1. **[medium] Duplicate scenario.** MYST-078 "The warning banner opens the Problems view" (and
   "malformed previewShowProblems ignored") repeats MYST-081 "Open Problems opens the Problems
   view". Keep it in MYST-081 only.
2. **Markers** OK: `confLocator.ts:73`, `confParser.ts:201`, `mystSyntaxDetect.ts:73`,
   `mystRenderer.ts:430` (extension-check pass), `diagnostics.ts:31-32`, `hostEvents.ts:179`,
   `warningBanner.ts:105`, `workspaceChoices.ts:48` and `viewState.ts:50`.
3. **[medium] Tests.**
   - `test/integration/mystDiagnostics.test.ts:36` marks MYST-081 on `runUntrusted`, which checks
     that no Problems entries exist: that is MYST-078's refusal scenario. Move the marker to
     MYST-078.
   - MYST-078 has only the integration marker. The cited unit tests in `pageToHost.test.ts`,
     `trustReq.requirements.test.ts` and `warningBanner.test.ts` are unmarked.
   - MYST-081: `test/page/modules/warningBanner.test.ts:118` (Open Problems), `:126` (close),
     `:150` (Restricted Mode) and `:109` (other statuses show no banner, which partly covers the
     "untested" refusal) are unmarked.
   - MYST-066: 2 of 17 tests marked. `confLocator.test.ts:29,50,92,130` (no conf, above the root,
     D29 fallback, outside the workspace) and `confParser.test.ts:57,84` are unmarked.
4. **Validation** OK. `test/integration/mystDiagnostics.test.ts:47` (Path 1, real Problems view)
   and `scenarioDefinitions2.ts:1266` (Path 2, banner).
5. **Diagram (sequence).** Writer opens the doc → Host finds the governing conf.py and reads it as
   text → Renderer detects MyST syntax of disabled extensions → warnings with lines → alt
   (trusted): Problems view entries → Page banner "N warnings" → Open Problems or Close
   (remembered per warning set).

## StRS-MDOKFSTUDIO-MYST-009: labels seen, linked and renamed

SwRS: MYST-019, 036, 038, 045, 051, plus BLOCK-041, TRUST-005 and TRUST-065.

1. **[low] The user need over-promises.** "rename labels without references silently breaking" is
   true only because MYST-038 reports the remaining `{ref}` uses: MYST-045 does not rewrite them
   ("The uses of the old name are counted, not rewritten"). Say so in the normative text: "and
   tells the writer how many references still use the old name".
2. **[medium] Split.** MYST-051 (message validation and answer) is the protocol side of MYST-045.
   Merge MYST-051 into MYST-045 as its accepted-shape and stale scenarios. MYST-038 (10 scenarios,
   1567 words) includes popover placement, which is fine as one behaviour.
3. **Markers** OK: `labelRename.ts:17,29` (core), `page/modules/labelRename.ts:64,160`,
   `sourceEdits.ts:90` and `session/features/sourceEdits.ts:129,148`.
   - **[low]** `src/session/pageMessages.ts:182` marks MYST-038 on `refuseStaleRequest`, the
     generic stale answer of every request (TRUST-065). Remove it.
   - **[low]** `mystInlineTransforms.ts:34` marks MYST-019 on `normalizeAnchors`. Fine: it makes
     the label `{ref}` links.
4. **[low] Tests.** Mostly good: MYST-038 has 13 marked tests.
   - MYST-019 "A reference to a heading shows the heading text" has no marked test.
     `mystPaletteRendering.test.ts:221` (label before a heading) is unmarked for MYST-019 and does
     not check the link text.
   - The `{numref}` case is untested, as its notes admit.
5. **[medium] Validation.** `test/integration/labelRename.test.ts:35` carries the StRS, but it posts
   `previewLabelRename` messages directly and does not go through the anchor icon and popover.
   `test/integration/realInput/labelRenameAboveTable.ts:43` (real input) is closer to the user
   path and could carry the StRS too.
6. **Diagram (sequence).** Writer in edit mode → Page: click anchor icon → Rename popover (valid
   name only) → Page → Host: previewLabelRename (line, old, new, render) → Host checks the gate
   and that the line is still `(old)=` → edits that text, one undo step → Host → Page: ok plus the
   remaining `{ref}` count, or the reason.

## StRS-MDOKFSTUDIO-MYST-012: toctree

SwRS: MYST-057.

1. **[low] Split.** "A target is read once per render" is internal (cache). Move it to the
   verification notes.
2. **Markers** OK: `mystGridToctree.ts:640` and `documentGlob.ts:44`.
3. **[medium] Tests.** Cited but unmarked: glob (`test/core/render/gridToctree.test.ts:185`),
   missing target (`:192`, which is the refusal of the StRS), hidden (`:176`) and reversed
   (`renderReq.myst.requirements.test.ts:52`).
4. **Validation** OK. `scenarioDefinitions2.ts:822` (toctree with caption, missing target, glob,
   hidden, plus content assertions).
5. **Diagram (flow).** `{toctree}` entries → resolve each (title / first H1 / file name; glob
   expanded and sorted) → found: preview link; missing: warned text without link.

## Cross-scope SwRS derived by these StRS

- **[medium]** TRUST-065 (13 parents), TRUST-005 (11), BLOCK-041 (10), BLOCK-058 (8) and TRUST-006
  (7) are shared rules. In this audit they are derived from CODE-004, GFM-003 and MYST-009 and
  also cited by `depends_on` from GFM-021, GFM-027, GFM-039, MYST-045, MYST-051, CODE-017,
  CODE-019, CODE-026 and MYST-078. Per "a rule shared by many features ... is cited by
  `depends_on`", drop these StRS from their `derives_from`. Each needs another home parent, such as
  a TRUST or BLOCK StRS.
- **[medium]** CORE-012 (include) derives from GFM-002 and MYST-001: see GFM-002 finding 2.
- CORE-022 is the right main SwRS of MYST-005. CORE-028 (inline code typesetting) is a fair
  secondary of CODE-001.

## Orphan SwRS

None. Every in-force SwRS of myst, code-blocks and gfm derives from at least one in-force StRS.

## Systemic finding

**[medium] Under-marked tests.** In the files read, tests that the verification notes cite usually
carry no `@tests_req`:

| Test file | Tests | Marked |
| --- | --- | --- |
| `bareUrlAutolink.test.ts` | 8 | 1 |
| `confLocator.test.ts` | 10 | 1 |
| `mathRenderer.test.ts` | 8 | 4 |
| `warningBanner.test.ts` | 12 | 2 |
| `mystFeatures.test.ts` (admonitions, context tags, tables) | about 15 | 0 |

The coverage fields therefore under-report real coverage. Refusal and boundary scenarios are the
ones most often left unmarked. Fixing this is mechanical: one marker per cited test, done in the
same pass as the verification notes.

## Counts

- StRS audited: 10. SwRS audited: 44 own + 8 cross-scope. Orphans: 0. In-force StRS citing an
  inactive SwRS: 0. StRS without a validation test: 1 (MYST-006). StRS whose validation misses a
  path or the user path: 4 (CODE-001 diff, GFM-003 radio, MYST-001 tabs, MYST-009 anchor click).

| Category | High | Medium | Low |
| --- | --- | --- | --- |
| StRS text contradicts or misstates its SwRS | 2 (CODE-001, GFM-002) | 2 (GFM-003 radio, MYST-001 breadth) | 2 (MYST-005 title, MYST-009 user need) |
| Misderived / mis-parented SwRS | 1 (MYST-005 ← MYST-019, MYST-097) | 2 (CORE-012; shared TRUST/BLOCK rules) | 0 |
| Split: merge or move proposals | 0 | 7 (CODE-005, CODE-001/007 colours, CODE-026, GFM-009, GFM-027/039, MYST-053/100, MYST-024, MYST-051) | 4 (MYST-006 gallery, MYST-101, MYST-057 cache, GFM-008 internal) |
| SwRS describing internals | in the above: cache or lazy load in CODE-001, MYST-024, MYST-057; HTML pass in GFM-008; wrapping in CODE-005; MYST-097 | | |
| Code markers misplaced | 0 | 4 (contentBlockStyles header; renderMyst hub; rewriteNode hub; MYST-098 on generic helpers) | 1 (pageMessages.ts:182) |
| Test markers on the wrong test | 0 | 4 (previewStyles:380 CODE-007; codeBlockComfort:78,87 CODE-001; markdownSyntax:108 MYST-097; mystDiagnostics:36 MYST-081) | 0 |
| Scenarios with no test | 2 (GFM-021 host refusals, MYST-024 refusals only in unmarked tests) | 3 (CODE-007 box style; GFM-029 kbd attrs; MYST-053 depth) | 3 (CODE-019 second click; MYST-019 heading text, numref) |
| Cited tests left unmarked | 0 | 1 systemic | 0 |
| StRS validation missing or partial | 0 | 2 (MYST-006 none; MYST-009 message-level) | 3 (CODE-001, GFM-003, MYST-001 path gaps) |
| Format and wording drift | 0 | 0 | 3 (CODE-026 H2; MYST-096/097 "EARS Expression" H2; MYST-098 to 101 scenario format) |

Proposed merges if all are approved: CODE-005, CODE-026, GFM-027 and MYST-051 merged away (4 fewer
SwRS). GFM-039 split into 2 and MYST-024 split into 2 (2 more). MYST-001 split into 3 or 4 StRS.
