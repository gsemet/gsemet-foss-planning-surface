Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.3 critic review: scope theme-zoom (12 StRS, 55 SwRS)

Worktree: `markdown-okf-schema-studio-wt-059-b3`. Read: constitution, requirements guideline, the
inventory, the two example reviews, all 12 StRS and all 55 SwRS. Code and tests checked for 55 of
55 SwRS (all Known issues, all "Untested" notes, every named test, the lifecycle and real-input
harnesses, the visual scenario assertions) and compared with the TOOLBAR, CORE, MYST, DIAG and
LAYOUT SwRS.

Verdict: REVISE

## What passed

- All 55 SwRS headings equal their frontmatter titles, descriptions equal the first normative
  sentence, no placeholders, every SwRS has two scenarios and a Method/Criteria pair.
- Every named unit, integration and visual test exists (`cycles preview theme modes...`, `T08: ...`,
  `cream ...`, `every theme token maps...`, `the theme-triggered bounded render`, real-input check
  `38-toolbar-{host}-{mode}`, captures r01..r08 with r03 `capture: false`).
- Numbers and texts match the code: tooltips and labels (`themeMode.ts:applyPreviewThemeMode`,
  `viewControls.ts:apply`), zoom 70/200/10 and defaults, 400 ms fallback (`motion.ts:themeSwitch`),
  57 token names, 960 default width, rgb values of Dark, White and Cream (`realInput.test.ts`
  palettes), `Failed to persist ...` strings, precedence mode (host, saved state, Cream) and zoom
  (saved, stored, 100).
- Read-only acceptance (015, 054) is correct: only `EDIT_REQUEST_TYPES` are refused
  (`pageMessages.ts`), `viewState.ts` handlers have no readOnly check.
- Known issue of 048 (validator accepts 75, storage rounds to 80) is real:
  `pageToHost.ts:VIEW_PREFERENCE_VALIDATORS.zoom` vs `previewViewPreferences.ts:normalizeZoom`.
- Every F-THEME line of the inventory maps to an SwRS (F-THEME-021 and F-THEME-024 by citation).
- No SwRS text names a backlog item. No leaked internal ids except defect 6.

## Defects (18)

1. **THEME-017, false Known issue.** It says "no style rule and no page script reads
   `data-sphinx-preview-theme`" and that the attribute "changes nothing the reader sees".
   `src/page/modules/mermaidPreview.ts:151` lists `data-sphinx-preview-theme` in the
   `attributeFilter` of `themeObserver`, and SwRS-MDOKFSTUDIO-DIAG-006 specifies that redraw.
   Fix: reword to "no style rule reads the attribute; the only consumer is the Mermaid theme
   observer (see SwRS-MDOKFSTUDIO-DIAG-006), which redraws only when the drawn colours differ".
   Also drop "changes nothing the reader sees".

2. **THEME-012 and THEME-006, wrong "no session-level test".** Both say the host handler and the
   boot-context hand-over have no session test. `test/integration/lifecycle.test.ts:71-75` posts
   `previewThemeModeChanged` dark through the real handler and line 135 asserts the next page html
   matches `"previewThemeMode":"dark"`. Fix: Method of 012 and 006 cites that integration test for
   "next boot context carries the mode"; keep "storage write and stale-message drop not asserted".

3. **THEME-013, verification cites a helper the host does not use.**
   `previewTheme.ts:isPreviewThemeModeChangedMessage` is not imported by any file in `src/`
   (only its own test). The live validator is
   `PAGE_TO_HOST_VALIDATORS.previewThemeModeChanged` (`pageToHost.ts:550`, uses `isPreviewThemeMode`).
   Fix: Method names `pageStateMessages.test.ts` (corpus with `neon` and absent mode, lines
   169-179) as the evidence; say the first test exercises an unused helper (or drop it).

4. **THEME-048, 052, 053, 055 (and 014 by analogy) duplicate TOOLBAR SwRS.**
   TOOLBAR-013 = zoom accepted only as a whole number 70..200 (052); TOOLBAR-015 = zoom rounded to
   10 and clamped, bad value to default (053); TOOLBAR-014 = accepted preference stored under
   `markdownOkfSchemaStudio.viewPreferences`, same 75 to 80 scenario, same "No storage" scenario,
   same Known issue with the identical log string (048, 055). Fix: archive 052, 053, 055; reduce 048
   to the zoom-specific part (zoom message from the held preview reaches the next boot context) and
   cite TOOLBAR-013/014/015 by id; remove the duplicated 75/80 Known issue from 048; update
   StRS-012 `derived_by`.

5. **THEME-032, duplicate and bundled.** "Panel colour distinct from the page" and "source line" are
   SwRS-MDOKFSTUDIO-MYST-003 (any theme, includes Cream). The SHALL carries two behaviours (panel
   colour and following paragraph colour). Scenario 2 is MYST behaviour, not a boundary of this
   SHALL. The check is a luminance gap (`capture_support.py:249-254`, `__MIN_CONTRAST__`), not
   "colour differs". Fix: keep one SHALL "the paragraph after an admonition keeps the body text
   colour on the Cream page" (`capture_support.py:310-322`), cite MYST-003 for panel/title, replace
   scenario 2 by a real boundary (no admonition: nothing to check is not testable, so use
   "gallery on White keeps it too" only if asserted; otherwise archive).

6. **THEME-008 and THEME-009, leftover internal ids.** 008 Method "follows from B1", 009 Method "(B5)".
   Fix: replace by "follows from SwRS-MDOKFSTUDIO-THEME-009" / "SwRS-MDOKFSTUDIO-THEME-012 and 013".

7. **THEME-038 and THEME-040, tests overclaimed.** 038: "the 190 to 200 step is covered by `T08: the
   zoom limits...`". That test (`runtimePageControls.test.ts:287-303`) goes 80 to 70 and starts at
   200; no test clicks 190 to 200. 040: scenario says "both zoom buttons are enabled" and "no zoom
   message posted at start"; `T08: zoom buttons set...` (262-285) asserts neither at start (it
   measures `before` only after). Fix: state "190 to 200 untested, code in `viewControls.ts:change`"
   and "enabled and no start message not asserted".

8. **THEME-041 contradicts THEME-042; THEME-042 bundled.** 041 says whenever a zoom is shown Zoom in
   reads "Zoom in ({zoom+10} %)"; at 200 the code gives "Zoom in (maximum 200 %)"
   (`viewControls.ts:apply`) and at 70 "Zoom out (minimum 70 %)". 042 then has three SHALLs
   in one (disable, tooltip, post nothing). Fix: 041 "When Zoom in is below 200 / Zoom out above
   70 ..." plus a limit tooltip clause moved there with its two texts; 042 only "disable and post
   nothing at a limit".

9. **THEME-007, two SHALLs.** "...SHALL show the saved mode; when both exist, ... SHALL show the
   mode stored". Fix: one sentence in the style of THEME-049: "the mode stored for the workspace,
   else the mode saved with the panel, else Cream" (then 004 and 006 keep their own scenarios).

10. **THEME-018, no distinct behaviour.** "Take colours from host variables as for any other theme"
    is THEME-016 again; the proof is an absent rule and the informational attribute of 017. Not
    testable as stated (its own Method says "by code reading only"). Fix: archive 018; add the high
    contrast kinds 3 and 4 as a scenario of 017 and one sentence in 016 ("for every host theme kind").

11. **THEME-029 and THEME-030, bundled and partly untested.** 029 bundles toolbar and sticky band;
    the band half has no test (own Method). 030 bundles page, toolbar text, pressed button and
    borders and restates the palettes of 025-027 and 029. Fix: 029 = toolbar only (band: separate
    SwRS marked untested or removed from the SHALL); 030 = only "independent of the host theme",
    values cited from 025/026/027, borders in their own SwRS (`realInput.test.ts` border map).

12. **THEME-025, colour scheme claim unchecked.** SHALL says "a light colour scheme". v01/v07 run
    `check_forced_white_theme` (`capture_page_checks.py:625-661`) which checks background,
    foreground and panel only; colour scheme is asserted for Cream (`:757`) and Dark
    (`scenarioAssertions.ts:370`) but not White (set at `pageChromeStyles.ts:97`). Fix: say in
    Method "White colour scheme is not asserted" (or drop it from the SHALL).

13. **THEME-031 Known issue is not a behaviour; THEME-034 number unasserted.** "Only Cream is
    checked for contrast" is a coverage gap (guideline: Known issue = behaviour that looks wrong).
    Fix: remove the Known issue from 031 (keep it in StRS-007 rationale as a limit, or a note in
    Verification). 034 states "57 names"; `themeTokens.test.ts` never counts them
    (`themeTokens.ts:THEME_TOKEN_NAMES` has 57 today). Fix: drop the number or write "(57 at the
    time of writing, not asserted)".

14. **THEME-014 and THEME-055, silent failure not flagged.** TOOLBAR-014 records the same behaviour
    (write fails: only a console error, reader informed of nothing) as a Known issue; 014/055 and
    StRS-004 describe it as a feature. Fix: add "Known issue: the failure is only logged; the choice
    is lost at the next start" to 014 (and cite TOOLBAR-014 instead of 055).

15. **StRS-010 leaks implementation; StRS-004/008 bundle.** Description "neutral token ... VS Code
    variable of the same name" and rationale "--studio-editor-background maps to
    --vscode-editor-background" are CSS names (guideline: no implementation detail). StRS-009 says
    "theme kind". StRS-004 and StRS-008 have two SHALLs. Fix 010: "When a maintainer ports the
    preview to another host, the Studio SHALL take every page colour from one named list that the
    host can map to its own palette" (names go to SwRS-034). Split 004 (remember / ignore invalid)
    and 008 (fade / reduced motion).

16. **StRS-008 fade has no SwRS here; THEME-024 near-duplicates CORE-050.** The fade is
    SwRS-MDOKFSTUDIO-CORE-053 and "no motion under reduced motion" is CORE-050, but StRS-008 and
    its rationale cite "the rendering-core requirements" without ids. Fix: cite CORE-053 and
    CORE-050 by id in StRS-008 (and DIAG-006 in StRS-006 for the Mermaid redraw); reduce 024 to the
    page-side refusal only if CORE-050 does not already say it, else archive 024.

17. **THEME-033 and THEME-051, scenarios off target.** 033 scenario 1 reads "inline code after the
    properties table" for v04, but v04 uses fixture `04-code-and-tables` (no table; the
    frontmatter check runs only on `07-frontmatter`, `capture_page_checks.py:784-816`). Fix: assign
    the "after the properties table" text to v05 and the "translucent tint" to v04 separately.
    051 scenario 2 ("Toolbar markup holds the Zoom out button") is not a boundary of the SHALL
    (shell key equality). Fix: replace by a boundary the test asserts, or drop and keep one scenario
    plus the context-key assertion (`contentPatch.test.ts:274-277`).

18. **THEME-021, Method misses existing unit coverage.** "Untested at unit level" ignores
    `test/core/state/editLock.test.ts` (lines 14, 26, 51, 93-151) which tests
    `EditLock.shouldDeferReload`, the condition `deferWhileEditing` uses
    (`blockEdits.ts:446`). Fix: cite it, keep "theme-render key and notifyTheme order not asserted".

## Re-check

Scope read again: 13 StRS, 52 active SwRS (58 files, 6 deprecated: 018, 024, 052, 053, 055, 056), new
057 and 058, checked against `src/`, `test/` and the TOOLBAR, CORE, MYST, DIAG, CODE and LAYOUT SwRS
of the same worktree.

Verdict: FIX-REQUIRED

### The 18 earlier defects

All 18 are fixed in the text, verified against code and tests:

- 1: 017 now names the Mermaid observer (`mermaidPreview.ts:151`, DIAG-006) and has the kinds 3 and 4.
- 2, 3: 006 and 012 cite `lifecycle.test.ts:71-75,135`; 013 cites the live validator and the corpus
  `cream`/`neon`/absent (`pageStateMessages.test.ts:179`).
- 4 (partly): 052, 053, 055 archived and 048 reduced; see D1 below, the archive left a hole.
- 5: 032 is one SHALL. Open doubt settled: `PAGE_CHECKS` (`capture_support.py:124-331`) is evaluated
  by `capture.py:180-211` for every scenario page, and the paragraph-after-admonition check
  (`:310-322`) is unconditional (no theme or fixture test). Scenario 2 and the Method of 032 are
  correct. Their criterion is the colour of the first plain paragraph, as written.
- 6 to 18: ids removed, 038/040 untested parts stated, 041/042 split, 007 single sentence, 018 archived,
  029/030 split with 057 (band, untested) and 058 (borders, `realInput.test.ts:3695-3703` checks the
  toolbar and every `.admonition`, top/right/bottom, with exactly these three rgb values), 025 states
  the colour scheme is not asserted, 031 Known issue removed, 034 "not asserted", 014 Known issue,
  StRS-010/004/008 reworded and cited, 021 cites `editLock.test.ts`, 033/051 scenarios on target.
- Also verified: headings equal titles, descriptions equal the normative sentence, derives_from and
  derived_by are mutually consistent, 52 active SwRS, every cited non-theme id exists
  (CORE-050/053, DIAG-006, MYST-003, CODE-016/038, LAYOUT-001, TOOLBAR-013/014/015), numbers and
  texts (palettes, 60 contrast pairs, border map, zoom 70/200/10, tooltips) match the code.

### Defects

1. **THEME-048 and StRS-012, zoom validation and normalisation now owned by nobody (dangling cites in
   both directions).** The revision archived 052 (host accepts only an integer 70..200) and 053
   (stored zoom rounded to 10, clamped, bad value to 100) as "duplicates of TOOLBAR-013/015", and 048
   says "storage and validation: SwRS-MDOKFSTUDIO-TOOLBAR-013 and 014" and "Normalisation of a stored
   zoom is SwRS-MDOKFSTUDIO-TOOLBAR-015". The TOOLBAR texts say the opposite:
   `SwRS-MDOKFSTUDIO-TOOLBAR-013` SHALL covers only toc, incomingChanges, comments, toolbarCollapsed
   (booleans) and its Method says "The zoom rule is SwRS-MDOKFSTUDIO-THEME-052";
   `SwRS-MDOKFSTUDIO-TOOLBAR-015` SHALL lists width margin, toc off, incoming on, comments on,
   toolbar collapsed (no zoom) and its Method says "Zoom rounding is SwRS-MDOKFSTUDIO-THEME-053".
   Result: the code behaviour `VIEW_PREFERENCE_VALIDATORS.zoom` (`pageToHost.ts`) and `normalizeZoom`
   (`previewViewPreferences.ts`), with tests `previewViewPreferenceChanged validates the value per
   preference` and `zoom is clamped to 70-200 and rounded to 10`, has no active SwRS, and two active
   TOOLBAR SwRS point to archived ids. Only 014 (storage key, no storage, stale message, Known issue
   of the write failure) really duplicates a TOOLBAR SwRS; the zoom 75-to-80 Known issue is gone from
   048 and that is fine, but nothing records it either.
   Exact fix (choose one, the first needs no change outside the scope):
   (a) set `lifecycle: draft` again on SwRS-MDOKFSTUDIO-THEME-052 and 053 (keep 055 archived, 014 of
   TOOLBAR covers the failed write), restore their bodies (they are intact), keep them in StRS-012
   `derived_by`; in 048 replace "storage and validation: ... TOOLBAR-013 and 014" by "validation:
   SwRS-MDOKFSTUDIO-THEME-052, storage: SwRS-MDOKFSTUDIO-TOOLBAR-014" and "Normalisation of a stored
   zoom is SwRS-MDOKFSTUDIO-TOOLBAR-015" by "... is SwRS-MDOKFSTUDIO-THEME-053"; in 052 and 053 add
   the Known issue of the validator accepting 75 and storage rounding it to 80
   (`pageToHost.ts` vs `normalizeZoom`) in one of them only; or
   (b) edit TOOLBAR-013 and TOOLBAR-015 (toolbar-navigation scope) so that their SHALL covers zoom,
   remove their "THEME-052/053" Method sentences, and only then keep 052/053 archived and drop the
   archived ids from StRS-012 `derived_by`.
   Do not leave the current state: either way the two scopes must agree in the same commit.
