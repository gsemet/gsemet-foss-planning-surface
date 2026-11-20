# Verify CR-345 (second pass, after the move 9b66d1e9..c3b98022)

Head: c3b9802218344aa425264a591529963e1f07cbc8

Base de96c3df (merge-base with main). All claims judged at 9b66d1e unless noted. Worktree
`markdown-okf-schema-studio.worktrees/batch-06-CR-345`.

## Gate pass

`work/gates/20261118-153451.log` line 1: `gate CR-345 branch chantier/batch-06/cr-345-... head 9b66d1e9383ecd6099e0a97579312d445dd2c1a5`;
last line `result: pass at 9b66d1e9383ecd6099e0a97579312d445dd2c1a5` (`just check`, Windows preflight = static stage). VERIFIED.

## Claims

1. IDs added: `git diff --name-status de96c3df HEAD -- requirements` gives 8 `A`: StRS PALETTE-019, 020, 021; SwRS
   PALETTE-276, 277, 278, 279, 280 (the rest `M`). VERIFIED.
2. Superseded, none deleted: `git diff de96c3df HEAD --name-only --diff-filter=D | wc -l` = 0. Files with a new
   `superseded_by` (frontmatter `req_lifecycle: superseded`): StRS PALETTE-001 -> 019/020/021; SwRS PALETTE-045, 048, 126,
   135, 138 -> 276; 049, 052, 053, 123, 267 -> 277; 265, 273, 274 -> 001 + 278; 130, 137 -> 127; 268 -> 238; 010 and
   THEME-013 -> LIFE-169; LAYOUT-018 -> LAYOUT-011. Matches the body's list and table exactly. VERIFIED.
3. Reparenting: SwRS PALETTE-114 derives_from StRS REVIEW-015; PALETTE-275 from PALETTE-015; PALETTE-001 from PALETTE-002 only.
   TABLE-085 lost StRS-PALETTE-015, CORE-028 lost THEME-002, TRUST-006 lost THEME-011 (git diff of their `derives_from`).
   VERIFIED for the facts. The wording "moved to the palette need they serve" (body Changes, and `requirements/tiers/log.md`)
   is NOT VERIFIED: the diff shows the palette/theme parent was dropped, nothing was moved to a palette need
   (TABLE-085 now derives only from TABLE-015, TABLE-111 from TABLE-016, CORE-028 from CODE-001/CORE-001, etc.).
4. Use case diagrams: script over `requirements/tiers/strs` (scopes palette-slash, theme-zoom, layout-width, not
   superseded) found 15 in-force StRS (LAYOUT-001, 003, 004; PALETTE-002, 005, 007, 013, 015, 018, 019, 020, 021;
   THEME-002, 004, 011); each has `### Use case diagram` count 1, mermaid fence count 1, diagram line < `### Main paths` line.
   VERIFIED.
5. Diagrams parse: `mermaid.parse` (node_modules mermaid 12.2.0, DOMPurify stubbed because node has no DOM) on the fence of
   each of the 15: all OK (sequence or stateDiagram), `failures 0`. `grep -E 'participant +box'` finds no `Box` participant;
   commit ee5ae7ad renamed it `Field` in PALETTE-007, 013, 018, 019, 020, 021 (the pre-fix 27b2cd9c has
   `participant Box as Text box`). Not rendered by the site build (gallery skipped), so the site drawing is the body's
   Known gap. VERIFIED (parse), site rendering UNVERIFIED as the body says.
6. `just requirements-lint` exit 0: `1147 requirements, 0 errors, 26 warnings`; `main paths: 83 StRS checked, 546 SwRS
   citations, all valid`; `0 indexes would change`, `0 requirement OKF projections would change`, `update-coverage --check`
   `0 files would change`. The warnings are W2 broken-link notes on SwRS text (e.g. PALETTE-264 `url`), none are errors.
   VERIFIED.
7. `just check-markers` exit 0: `10 companion file(s), 404 in-force SwRS marked, 34 files on the marker baseline`. VERIFIED.
8. `okfreq trace requirements --json`: `missing_ids` 0; of the 79 in-force SwRS of the three scopes, 0 lack an implementation
   file and 0 lack a test file; the 15 StRS each appear in `validation_tests` with a file other than
   `realInput/markers.ts` (e.g. THEME-004 `lifecycle.test.ts`, PALETTE-019 `realInput/textEditing.ts`, PALETTE-020
   `alertLazyEditAction.test.ts`, PALETTE-021 `slashAdmonitionScenarios.ts`). VERIFIED.
9. Markers: no `src`/`test`/`scripts` line names any superseded ID (grep returns nothing). Scan of all `@implements_req` /
   `@tests_req` lines in src and test: 0 lines with more than 3 IDs. `editPalette.ts` header split into single-ID markers
   (e.g. lines 49, 90, 124, 148, 202). PALETTE-264 markers sit only on `pasteUrl.ts`, `blockSourceEditor.ts:188`,
   `test/page/modules/pasteUrl.test.ts`, `test/integration/pasteUrl.test.ts:59` and `runtimePaletteActions.test.ts`
   (not on `integrationEditModeRestore.test.ts`). PALETTE-001 no longer marked on `package-contract.test.ts`; THEME-016 no
   longer on `editLock.test.ts`. LAYOUT-011 on `runtime.ts:283` and `firstClearance.ts:85,308`. Style markers live in the
   new `*.markers.ts` companions. VERIFIED.
10. No product behaviour change: `git diff de96c3df HEAD -U0 -- src` minus comment lines leaves only five `+export {};`
    lines (the companion files). VERIFIED.
11. New tests exist and pass: `npm run compile` then `node --test` on layoutThemeStyles, widthModeScenarios,
    previewConfiguration, firstClearance, runtimePageControls, editActions, slashMenu: `tests 331, pass 331, fail 0`.
    Markers present on LAYOUT-002 (rounding, negative), LAYOUT-022 (centring, figure mark), LAYOUT-023 (%/em/rem, Mermaid
    wrapper, re-measure), LAYOUT-011 (narrow fallback), THEME-043, THEME-016 (kinds). VERIFIED. (Whether they fail on the
    old code is not needed: the CR changes no code; the body's "they fail on the previous code" box is a template line.)
12. Owner-approved StRS corrections, each in its own commit: `git show --stat` of c145e649 (LAYOUT-001 only), 0240436a
    (LAYOUT-003 only), 9e210e0a (PALETTE-015 only), each one file. Each file has `approved_by: gaetan@xeberon.net`,
    `approved_at: '2026-11-17T22:42:16+01:00'`. `02-answers.md` garden-Q1/Q2 records the advance agreement. LAYOUT-003 rationale
    has 7 bullets as the body says. VERIFIED.
13. CI: `gh pr checks 415` at 9b66d1e: checks, report, static, static-windows, visual pass; integration, stress and
    gallery skipping on the PR (CI rules). Heavy run 44325795176 `success`, headSha 9b66d1e, integration success, stress
    success, visual success, gallery skipped. VERIFIED. The body's gallery Known gap is accurate.
14. PR description (local `work/pr-body.md`, which differs from the posted body: the posted one lacks the Mermaid `Field`
    line, the commit SHAs and the gallery gap): NOT VERIFIED, for these reasons:
    - Changes, "Reparented": "TABLE-085, 111, CORE-028, TRUST-001, 005, 006, 065 moved to the palette need they serve"
      contradicts the diff (claim 3); the same sentence is in `requirements/tiers/log.md` (line ~129).
    - Known gaps first bullet says "StRS PALETTE-114" but PALETTE-114 is a SwRS (its parent moved to StRS REVIEW-015).
    - The posted body on the forge is stale against `work/pr-body.md`; it must be re-posted.
    - Template lines still hold placeholders (`<fill>`, `<sha7>`); the Driver fills them. The Test plan box "they fail on the
      previous code" does not apply to a markers-only CR; the new tests only pass today's code.
    Nothing in the description was found unrendered otherwise; it contains no image.

## UNVERIFIED for the body

- The requirements site's drawing of the 15 diagrams (gallery job skipped).
- "Review: approved at <sha7>" is not judged here (no `$CHANTIER log` review box check requested).

## Evidence pairs

No screenshots or videos: a requirements-text CR with no UI change. `before-after.md` not written; before = base
de96c3df requirement files, after = 9b66d1e; reproducible with the git diff commands above.

## Second pass at c3b9802218344aa425264a591529963e1f07cbc8

Move 9b66d1e9..c3b98022 (new commit, same base de96c3df): `git diff --stat 9b66d1e9 HEAD` = `requirements/tiers/log.md | 38 ++++++-----`, one file.
Claims 1, 2, 4-13 above are carried from 9b66d1e: the move touched no requirement, source, test or marker file, so their proofs are unchanged
(claim 6 re-run below anyway). Claim 3 and 14 judged again.

- Gate: `work/gates/20261118-162243.log` line 1 `gate CR-345 ... head c3b9802218344aa425264a591529963e1f07cbc8`, last line `result: pass at c3b9802218344aa425264a591529963e1f07cbc8` (`just preflight`, `ci-static: passed`). VERIFIED.
- Claim 3 (changelog wording), c3b9802: the "moved to the palette need" sentence is gone from log.md; the new entry says the SwRS "only drop a palette or theme parent and keep their other parents". Checked each against `git diff -U0 origin/main HEAD -- <file>`:
  TABLE-085 drops StRS-PALETTE-015; TABLE-111 drops PALETTE-001; CORE-028 drops THEME-002; TRUST-001 drops PALETTE-002; TRUST-005 drops PALETTE-013 and 007; TRUST-065 drops PALETTE-007 and 013; TRUST-006 drops THEME-011; PALETTE-192 drops PALETTE-013 (196, 203 listed in the same sentence, in the diff); PALETTE-115 loses PALETTE-001 and 005, gains only PALETTE-020; PALETTE-039 and 052 move 001 -> 019; PALETTE-086 not in the diff (keeps PALETTE-001). Matches. VERIFIED.
  Residual (minor, already noted by the inspector): log.md says PALETTE-039 and 052 "keep StRS-PALETTE-015 too"; 052 is a superseded SwRS. Not a delivered-change error.
- `just requirements-lint` at c3b9802: exit 0, `0 indexes would change`, `0 requirement OKF projections would change`, `0 files would change`, `main paths: 83 StRS checked, 546 SwRS citations, all valid`; only W2 warnings (PALETTE-264 `url`). VERIFIED.
- CI at c3b9802: `gh pr checks 415`: checks, report, static, static-windows, visual pass; gallery, integration, stress skipping on the PR. `gh run view 44334938903`: conclusion success, headSha c3b9802218344aa425264a591529963e1f07cbc8, integration success, stress success, visual success, gallery skipped. VERIFIED; site drawing of the diagrams stays UNVERIFIED, as the Known gap says.
- Review box (`approved at c3b9802`): `chantier log 345`: note "r7 approved at 9b66d1e, committed as c3b98022" (the round's committed-as SHA). Proves the review. VERIFIED.
- Claim 14, PR description as posted (`gh pr view 415 --json body`, headRefOid c3b9802...): identical to `work/pr-body.md` (diff shows only one trailing blank line). Stale Known gap ("StRS PALETTE-114") now reads "SwRS PALETTE-114's parent moved to StRS REVIEW-015"; the Field/Box line, commit SHAs and gallery Known gap are present; no `<fill>`/`<sha7>` placeholders; Test plan items name c3b9802; Reparented paragraph matches the diff checked above; 15 diagrams matches claim 4; no image, no STALE mark; sections and fold well formed. Only unchecked box is "Verified", which this pass answers. Known gaps: gallery gap present. No role names outside Internal references. VERIFIED.

## Verdict at c3b9802218344aa425264a591529963e1f07cbc8

VERIFIED. Site drawing of the use case diagrams UNVERIFIED (gallery job skipped), listed in the description's Known gaps.

## Description pass (third) at c3b9802218344aa425264a591529963e1f07cbc8

Command: `gh pr view 415 -R gsemet/markdown-okf-schema-studio --json body,headRefOid` -> headRefOid c3b9802218344aa425264a591529963e1f07cbc8.
Judged against `.agents/guidelines/pull-request.guidelines.md`, the patch and the claims above (carried, same head).

- Test plan items name c3b9802 (local gates, Review, Verified, CI): match the gate log, `gh run view 44334938903` and the review note above. VERIFIED.
- New Known gap on log.md: `grep -n "keep StRS" requirements/tiers/log.md` -> lines 127-128 say PALETTE-039 and 052 keep StRS-PALETTE-015 too; 052 is superseded in this change, so the gap is true, worded as a changelog slip with no requirement affected. VERIFIED.
- Gallery Known gap kept; other Known gaps unchanged. VERIFIED.
- Renders: sections, table and fold well formed; no image, no placeholder, no STALE mark; role names only in Internal references. VERIFIED.

VERIFIED (description at c3b9802218344aa425264a591529963e1f07cbc8).
