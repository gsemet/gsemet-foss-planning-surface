Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.3 critic review: layout-width StRS and SwRS

Scope `layout-width`: 9 StRS, 35 SwRS (LAYOUT), reviewed against `inventory/layout-width.md`, the
sources and tests of `markdown-okf-schema-studio-wt-059`, and the defect classes of
`reviews/{code-blocks,gfm,myst}-swrs.md`. `okfreq validate --prose --check-links`: 607
requirements, 0 errors, 0 warnings; `lint --check`: 0 indexes would change.

Verdict: REVISE

## What passed

- Coverage: F-LAYOUT-001..028 are all mapped; F-GFM-037 is covered by SwRS-LAYOUT-001 (scenario 2,
  visual `gfm/v02..v04`). derived_by / derives_from are consistent both ways, including the
  cross-scope SwRS-DIAG-021 under StRS-LAYOUT-007. StRS 001-009 are user-observable.
- Numeric thresholds verified against the code: 40 px gap, 8 px margin, 320 px minimum frame,
  inset 292 / 192, clearance 52 / 47, toolbar bottom 92, 200 updates per second, 60 quiet / 300 max
  frames, 16 px gutter, `clamp(16px, 8vw, 78px)`, 256 px TOC reserve (panes of 760 px and more),
  breakouts 200 / 268 / 312 / 201 and shift 30 / 72, 1 px overflow and breakout tolerance, 24
  character short cells, 2400 / 960 / step 50, 100000 px full-width cap. The 480 px limit is
  indeed a rule of `check_first_element_gap` only (interactive elements), not a code constant.
- Known issues confirmed true: 0.2.1 CHANGELOG margins (56 / 24 px), README "all three look the
  same" at 0, README row 3 vs `widthMode.ts` header row 2, v05/v06 titles, v07..v09 "at least 20
  px", unmarked short cell never cleared, %/em/rem and declared-width paths untested.
- Spot check: 26 of 35 SwRS (about 74 percent) read against source/tests.

## Defects (14)

1. SwRS-LAYOUT-002, Known issue 2 is false: "The 1400 px in 2000 px case ... is not asserted by a
   scenario". Visual `layout-width/v85-max-width-setting-light-2000` renders `maxContentWidth: 1400`
   at 2000 px and asserts the column is 1400 px wide and centred (`MAX_WIDTH_ASSERTIONS`,
   `expectedContentWidth`). Fix: delete that Known issue, cite v85 in scenario 2 and in the
   Verification notes (method now "v05, v06, v85").
2. SwRS-LAYOUT-006, Known issue 2 ("not verified whether the update goes through the in-place
   patch or a full page replace") is a non-anchored statement and can be settled from the code: the
   width rule is an inline `<style>` of the page shell, `shellKey` includes it, so a changed rule
   gives different keys, `planContentPatch` returns undefined and the whole page is replaced
   (`contentPatch.ts:analyze/planContentPatch`; `maxContentWidth` is not a `startupSetting`).
   Fix: state this as fact (full page replace with the new rule), drop the "not verified" line, and
   add that the handler also calls `incoming.schedule(session, 0)` for the preview section.
3. SwRS-LAYOUT-005, Known issue ("No test builds a complete page and reads the rule from it") is
   false: `test/session/previewRuntimeFile.test.ts` "PERF-11" builds a full page with
   `maxContentWidth` 720 and asserts the inline style matches `/720/` and is the width rule only.
   Fix: reword to "the full-page test only matches the number 720, not the whole rule text" and cite
   the test in the Verification notes.
4. SwRS-LAYOUT-013, scenario 1 says a paragraph or table may start "lower only as far as the
   shorter toolbar requires". The code never moves them: `--sphinx-preview-first-clearance` applies
   only to the first-block editor, the Start writing button and a leading properties table
   (`contentLayoutStyles.ts`), and `check_first_element_gap` allows the push only for interactive
   elements. This contradicts SwRS-012 (Known issue 2) and is the open question F-LAYOUT-005..008
   "may also sit lower". Fix: scenario 1 must say the paragraph and the table start exactly 40 px
   (within 4 px) below the top with the toolbar collapsed; resolve the open question as "no".
   Also scenario 2 asserts four actions (clearance, sticky heading, TOC layout, width update): keep
   only the clearance update in this SwRS (the others belong to toolbar-navigation / SwRS-031).
5. SwRS-LAYOUT-012, Known issue 2 quotes "The inventory says non-interactive first elements may
   also sit lower": an internal pointer inside a requirement body. Fix: state the code fact only
   ("a non-interactive first element, paragraph or table, is never pushed down; only the first-block
   editor, Start writing and a leading properties table take the clearance") and ask the
   orchestrator to correct F-LAYOUT-010 in the inventory (stale text "(text, table) may also sit
   lower").
6. StRS-LAYOUT-004, Known issue says "the README and older change-log entries still quote the
   superseded margins". The README has no 56 px / 24 px text; only CHANGELOG 0.2.1 does (line 393).
   Fix: "CHANGELOG entry 0.2.1 still quotes the superseded margins".
7. StRS-LAYOUT-006 Known issue and SwRS-LAYOUT-020 Known issue say "CHANGELOG 0.1" puts the Width
   button on row 2. The sentence ("A Width button on the second toolbar row", CHANGELOG line 337)
   sits in the Unreleased section, not in 0.1.0 / 0.1.1 (those start at line 424). Fix: "an older
   bullet of the Unreleased CHANGELOG entry", in both files.
8. SwRS-LAYOUT-001, scenario 1 is not true to any check: no test or visual scenario renders a
   120-character URL in dark, light and cream at 460 px in Margin, Auto and Full. Real evidence:
   K1 unit test (wrapping selectors), v01 (dark 460 Margin table), v78..v80 (light 460, three modes),
   v66..v71 (cream / dark / light at 900 and 1600). Fix: rewrite scenario 1 around the real
   assertions (e.g. v78..v80: light, 460 px, each mode, overflow at most 1 px) and add the K1 rule
   as a second, unit-level scenario; the SwRS has no boundary scenario today (both are nominal).
9. Unbounded or bundled SHALLs (one SwRS = one behaviour):
   - SwRS-003: rounds, caps at 2400 and falls back to 960 (3 rules, and the 0 pass-through is only
     in 004). Fix: split into "cap and rounding" and "fallback for negative or non-numeric", or keep
     one and document the other in a new SwRS.
   - SwRS-016: shortens the table for a Description toggle and pushes it down for other controls
     (two outcomes, plus the 320 px fallback Known issue). Fix: split into two SwRS.
   - SwRS-021: webview state, workspace preference and restore at start. Fix: split "saves on click"
     from "restores with priority state > preference > Margin".
   - SwRS-028: lifts the column limit, sets 16 px margins and centres with 15 px gutters. Fix:
     bound to "lifts the limit and sets a 16 px gutter"; centring is already asserted by SwRS-029
     scope (narrow) or move it to its own SwRS.
   - SwRS-017 scenario 2 checks a second variable (`--sphinx-preview-first-bar-bottom`) not in the
     SHALL; SwRS-018 scenario 2 adds the animation-frame settle (a separate behaviour, cf. SwRS-019
     Known issue). Fix: move each to the SwRS that states it.
10. SwRS-LAYOUT-031, scenario 2 ("Mode change: the clearance is measured again and the reading
    line is kept") is outside its SHALL (Auto re-measures wide elements) and applies to every mode.
    Fix: move it to SwRS-020 (or a new SwRS "A mode change keeps the reading line"), keep in 031
    scenarios for content patch / image load / TOC toggle (all unit-untested: say so), and make
    scenario 1 a real boundary (a 1 px or equal-width element after resize stays unmarked).
11. StRS-LAYOUT-002 says the short-identifier marking "appears only for real overflow ... and
    disappears when the table fits". `markWideTables` writes `data-sphinx-short-cell` on every short
    cell of every non-properties table whether or not it overflows, and never clears it; only the
    CSS `nowrap` is conditional on `data-sphinx-table-overflow="true"`. Fix: say the single-line
    effect applies only while the table overflows, and add the always-set mark as a Known issue to
    SwRS-034 (scenario 2 is true as written only for the effect, not for the attribute).
12. Inventory mapping (split rows): F-LAYOUT-003 text includes "`0` lifts the limit" yet lists only
    SwRS-003; SwRS-004 (zero gives `none`) derives from it. F-LAYOUT-004 lists 004, 005, 006, of
    which only 005 and 006 match its own text (rule in the page; update on change), although its
    `Npx|none` fragment also touches 004. Fix: F-003 -> SwRS-003, SwRS-004; F-004 -> SwRS-005,
    SwRS-006. StRS mapping 003 = F-002..004 is correct.
13. SwRS-LAYOUT-007, Known issue 2 (v07..v09 keep the older "at least 20 px" assertion) is about the
    first-block editor and Start writing, not about the read-mode first element. Fix: remove from
    007 (already present in SwRS-014; add to SwRS-010 for v09 if wanted).
14. SwRS-LAYOUT-030 (optional boundary): `update` marks a figure only for a paragraph with exactly
    one child element that is an `IMG`, while `wrapperOf` treats any `IMG` in an empty-text
    top-level paragraph as the breakout wrapper, so a paragraph of two images breaks out in Auto but
    is not marked as a figure (not centred). Fix: add as a Known issue to SwRS-030 (or scenario 2
    boundary "two images, no text: not marked").

## Notes (no action required)

- Scenario naming differs from batch 1 ("nominal behavior" / "boundary or refusal behavior"); the
  descriptive names here are acceptable and validate cleanly.
- Visual scenarios `gfm/v02..v04` should carry the LAYOUT-001 marker (see the gfm review);
  `tested_in_files` / `implemented_in_files` are empty everywhere, as expected before annotation.
- Anchoring: no desired-state wording found; the Known issues for the 320 px / 480 px rule, README
  "all three look the same" and untested paths are anchored to code.

## Re-check

Scope re-read in full (9 StRS, 40 SwRS) against the worktree sources, the visual harness
(`capture_layout_checks.py:check_width_mode_break`, `scenarioIds.ts`) and the inventory.

All 14 earlier defects are fixed and verified against the code:
1 (v85 cited, false Known issue gone), 2 and 3 (006 states the full page replace; 005 cites PERF-11),
4 and 5 (012/013: a non-interactive first element is never pushed down; code fact only),
6 and 7 (CHANGELOG 0.2.1 / "older bullet of the Unreleased entry"), 8 (001 rewritten around
v78..v80, v01, gfm/v02..v04), 9 (split into 036, 037, 038, 039; 017/018 trimmed), 10 (031 real
boundary, reading line moved to 040), 11 (StRS-002 now limits the effect to overflowing tables;
SwRS-034 Known issue records the always-set mark), 12 (F-003 -> 003, 036, 004; F-004 -> 005, 006),
13 (007 Known issue removed), 14 (030 scenario 3 plus Known issue). Numbers re-checked: 2400, 960,
`none`/`Npx`, 292/192, 52/47, 92, 312/72, 201, 100000 px, 24 characters, 16 px, 15 px gutters.
`v78..v80` = light 460 px margin/auto/full, `v81..v83` = dark 900 px: matches 001 and 039.

DIAG-021 (now `deprecated`) is covered by SwRS-LAYOUT-023 (SHALL names table, figure, image, code
block and Mermaid diagram; scenario 1 and Known issue "only top-level blocks") plus SwRS-LAYOUT-026
(an element under edit keeps the column width = DIAG-021 scenario 2). No gap. Note: StRS-LAYOUT-007
and StRS-DIAG-001 still list the deprecated DIAG-021 in `derived_by`; the validator accepts it, but
the orchestrator may drop it when archiving is finalised.

### Scroll part of the frontmatter-editing visual `v06` (SwRS-FMEDIT-065 criteria)

Layout-width should NOT take it. What `v06` asserts is three vertical scroll cycles over a tall
properties table, a return to the top on source sync, and "the preview reports source line 1": that
is scroll synchronisation (anchor / `previewScroll`), owned by lifecycle-sync or toolbar-navigation,
not width or first-element layout. No SwRS anywhere cites `v06`. Fix: in FMEDIT-065 replace the
criteria sentence "the scroll part of that scenario belongs to layout-width" (dangling pointer) by
either a third scenario in FMEDIT-065 (tall table scrolls to both ends at 460 px in edit mode,
returns to the top on source sync) or a scroll-sync SwRS in the scope that owns scroll sync.

### Remaining defects (3, all minor)

1. SwRS-LAYOUT-040: two outcomes in one SHALL ("keep the line at the reading position" and "measure
   the first-element clearance again"), and neither scenario checks the clearance. The code does
   both (`runtime.ts` width callback: `firstClearance.update(); keepReadingLine();`). Fix: keep the
   SHALL, title and description on the reading line only; state the clearance call as a sentence in
   Verification notes (or add a third scenario "clearance measured again after the mode change").
2. SwRS-LAYOUT-014, scenario 1: still asserts `--sphinx-preview-first-bar-bottom` is `0px` and the
   palette keeps its 40 px place, which the SHALL (shorten by an inline-end inset, keep 40 px) does
   not state; the earlier defect 9 moved it from 017 into 014 instead of out. Fix: delete that
   clause from 014 scenario 1, or add "and publish --sphinx-preview-first-bar-bottom (0px when the
   frame is narrowed, the toolbar bottom when it is pushed: unit test P3, 92px)" to the SHALL of
   SwRS-LAYOUT-012/014 as one stated behaviour.
3. Inventory (orchestrator, not a requirement file): F-LAYOUT-011 still says "(or lower to clear the
   shorter toolbar)", contradicting the settled rule and SwRS-013; F-LAYOUT-004 still carries "not
   verified whether an in-place content patch refreshes the width rule". Fix: edit both rows (full
   page replace; first element exactly 40 px).

Verdict: FIX-REQUIRED

## Re-check 2

Checked in the worktree (`okfreq validate`: 0 errors, 0 warnings, 42 SwRS in scope) against `src/page/modules/firstClearance.ts`, `test/page/modules/firstClearance.test.ts` and `editPaletteStyles.ts` (lines 40-52), plus the commit eb4449c.

Re-check 1 defects:

1. LAYOUT-040: fixed. It now has one SHALL (reading line kept); the clearance re-measure is the new LAYOUT-041 (own SHALL, two scenarios, derived from StRS-006, honest Known issue "no test"); 040 Criteria points to 041. Matches `firstClearance.update(); keepReadingLine();` as inspected earlier.
2. LAYOUT-014 scenario 1: fixed (no `--sphinx-preview-first-bar-bottom` clause left; 014 states inset 292, clearance 0, published as `--sphinx-preview-first-inset`).
3. Inventory F-LAYOUT-011 and F-LAYOUT-004: fixed (the two old phrases are gone).
4. FMEDIT-065 dangling pointer ("scroll part belongs to layout-width"): fixed in FMEDIT-065/087.

Commit eb4449c:

- LAYOUT-042 (first-bar-bottom): numbers match the code and the tests. 900 px column (content box 16..884), toolbar 600..850 ending at 84: inset 884-600+8 = 292, `firstBottom = inset > 0 ? 0 : bottom`, so `--sphinx-preview-first-bar-bottom` 0px and `--sphinx-preview-toolbar-bottom` 92px (test "P3: an open first-block editor keeps its 40px gap..." lines 66-69). 460 px column, toolbar 200..450: 428-252 = 176 < 320, so inset 0, clearance 52, variable 92px (test lines 72-77). The CSS fallback to `--sphinx-preview-toolbar-bottom` when the variable is unset (`editPaletteStyles.ts:51`) matches the Known issue; the Known issue about a leading properties table with a Description toggle is true (the inset is above 0 there as well). One SHALL, two checkable scenarios, no placeholder, Known issue marked, StRS-005 `derived_by` updated, index regenerated. Anchored to `firstClearance.ts` and `firstClearance.test.ts` in the Method.
- Backlog references: `grep -ri backlog requirements/tiers` finds nothing. GFM-024/026/027, MYST-094/095 and CODE-017/026/027 are clean; the guideline now states the rule.
- "Closed schema: no custom key" (FMEDIT-035, FMEDIT-086, FMSCHEMA-041): consistent with the code (see the frontmatter-editing re-check 2).

Remaining defects: none blocking. Nits, not required for approval:

- LAYOUT-042 scenario 1 THEN says "its palette stays in the 40 px place"; the unit test asserts only the two variables, the placement is CSS (`editPaletteStyles.ts` sticky `inset-block-start`, variable + 4px). Optional: reword to "so the sticky palette keeps its 4 px offset instead of the toolbar edge" or note "CSS: not unit-tested" in the Method.
- MYST-094 Criteria reads "verification pending (no test covers a label starting with `_`, `.` or `-`)"; "pending" reads like a placeholder. Optional: "No test covers ...".

Verdict: APPROVE
