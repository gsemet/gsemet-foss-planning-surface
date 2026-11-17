# Stack state (run 5)

Bottom → top, base main: 135 → 137 → 138 → 139 → 140 → 141 → 142 → 143 → 144 → 145 → 146 → 147 → 148 → 149 → 150 → 151.

Stack driver: restacked and pushed (03:30); all 16 PRs open and linked with `gh stack link` (stack #160). Normal CI running. Every CR below is coded, approved and pushed; none
is rebased onto the final CR 135 tip (43c7eea8, which includes the T26 module split).

| CR | Branch | Built on | Head (pre-restack) | Status | PR |
| --- | --- | --- | --- | --- | --- |
| [135](135-audit-security-performance-pack/work/STATE.md) | change-requests/135-audit-security-performance-pack | origin/main 5727da8b | 43c7eea8 (restacked) | restacked, `just check` green, PR open, stack linked | [#144](https://github.com/gsemet/markdown-okf-schema-studio/pull/144) |
| [137](137-plantuml-jar-include-confinement/work/STATE.md) | change-requests/137-plantuml-jar-include-confinement | 135 @99a3de14 | b6609c56 (restacked) | restacked, `just check` green, PR open, stack linked | [#145](https://github.com/gsemet/markdown-okf-schema-studio/pull/145) |
| [138](138-table-column-min-width/work/STATE.md) | change-requests/138-table-column-min-width | 135 @99a3de14 | 28fa3838 (restacked) | restacked, `just check` green, PR open, stack linked | [#146](https://github.com/gsemet/markdown-okf-schema-studio/pull/146) |
| [139](139-external-edit-glow/work/STATE.md) | change-requests/139-external-edit-glow | 135 @0712337f | 4e407be4 (restacked) | restacked, `just check` green, PR open, stack linked | [#147](https://github.com/gsemet/markdown-okf-schema-studio/pull/147) |
| [140](140-edit-mode-tag-in-block-title/work/STATE.md) | change-requests/140-edit-mode-tag-in-block-title | 135 @0712337f | e83ec2b5 (restacked) | restacked, `just check` green, PR open, stack linked | [#148](https://github.com/gsemet/markdown-okf-schema-studio/pull/148) |
| [141](141-readme-html-guaranteed/work/STATE.md) | change-requests/141-readme-html-guaranteed | 140 | a00a9d49 (restacked) | restacked, `just check` green, PR open, stack linked | [#149](https://github.com/gsemet/markdown-okf-schema-studio/pull/149) |
| [142](142-toc-marker/work/STATE.md) | change-requests/142-toc-marker | 141 | 39d0d4d2 (restacked) | restacked, `just check` green, PR open, stack linked | [#150](https://github.com/gsemet/markdown-okf-schema-studio/pull/150) |
| [143](143-heading-folding/work/STATE.md) | change-requests/143-heading-folding | 135 @54c76b5b | 1c0c993d (restacked) | restacked, `just check` green, PR open, stack linked | [#151](https://github.com/gsemet/markdown-okf-schema-studio/pull/151) |
| [144](144-find-and-replace-in-preview/work/STATE.md) | change-requests/144-find-and-replace-in-preview | 143 | b334112d (restacked) | restacked, `just check` green, PR open, stack linked | [#152](https://github.com/gsemet/markdown-okf-schema-studio/pull/152) |
| [145](145-paste-url-as-link/work/STATE.md) | change-requests/145-paste-url-as-link | 135 @0c5cefc9 | 225b6524 (restacked) | restacked, `just check` green, PR open, stack linked | [#153](https://github.com/gsemet/markdown-okf-schema-studio/pull/153) |
| [146](../2-backlog/P3/146-drop-file-as-link/work/STATE.md) | change-requests/146-drop-file-as-link | 145 | 05e7e1c1 (restacked) | restacked, `just check` green, PR open, stack linked | [#154](https://github.com/gsemet/markdown-okf-schema-studio/pull/154) |
| [147](../2-backlog/P3/147-rich-diff-side-by-side/work/STATE.md) | change-requests/147-rich-diff-side-by-side | 135 @4a223496 | 71616824 (restacked) | restacked, `just check` green, PR open, stack linked | [#155](https://github.com/gsemet/markdown-okf-schema-studio/pull/155) |
| [148](148-myst-cards-tabs-version-directives/work/STATE.md) | change-requests/148-myst-cards-tabs-version-directives | 142 | 4af1aad4 (restacked) | restacked, `just check` green, PR open, stack linked | [#156](https://github.com/gsemet/markdown-okf-schema-studio/pull/156) |
| [149](149-vega-lite-charts-full-mode/work/STATE.md) | change-requests/149-vega-lite-charts-full-mode | 148 | 8183fe95 (restacked) | restacked, `just check` green, PR open, stack linked | [#157](https://github.com/gsemet/markdown-okf-schema-studio/pull/157) |
| [150](150-writing-skill-for-studio/work/STATE.md) | change-requests/150-writing-skill-for-studio | 149 | baa8803f (restacked) | restacked, `just check` green, PR open, stack linked | [#158](https://github.com/gsemet/markdown-okf-schema-studio/pull/158) |
| [151](151-dependency-update-security-floors/work/STATE.md) | change-requests/151-dependency-update-security-floors | 149 | c5758312 (restacked) | restacked, `just check` green, PR open, stack linked | [#159](https://github.com/gsemet/markdown-okf-schema-studio/pull/159) |

ID renames done while restacking (collisions between CRs): 145 PALETTE-003 -> PALETTE-264, 147 REVIEW-003 -> REVIEW-010, 148 MYST-097 -> MYST-100, 149 PALETTE-004 -> PALETTE-265.

## Run log (stack driver)

- 03:20 all 16 PRs open, linked (`gh stack link`, stack #160).
- First CI found product/test failures, fixed in rounds and restacked: CR 135 (worker bundle without MyST patch plugin; bundle test and missing-java test not hermetic; host-harness render clock flake), CR 138 (5em floor split identifiers in the Auto break-out table), CR 142 (palette height change after open left a 32 px scroll jump), CR 143 (hr in a folded section kept 1px height), CR 147 (unit test needed Chromium; toolbar button counts in visual checks).
- 05:05 restacked all branches again; normal CI re-running on all PRs.
- 06:19 final restack (CR 144 visual check fix, CR 147 palette reserve fix). Heavy CI started on the top branch: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40637264804
- 06:33 normal CI green on all 16 PRs (#144 to #159). Heavy run 40637264804: static and visual green; integration failed at test/integration/findInPreview.test.ts "the find field has the focus" (CR 144, real window, unverifiable locally: screen locked); stress failed (window loads fail with code -3, likely infra, not analysed). Open question for the user in the report.
- 06:40 CR 144 find-focus fix restacked (head of 151: 9019a003). New heavy run: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40639079833 ; rerun of the first heavy run: stress failed again.
- 06:55 CR 144 round 3 (find command + keybinding) restacked. Heavy bisect runs: 135 40640634459, 142 40640637221, 143 40640639724; heavy on top (new head) dispatched.
- 07:25 CR 143 (heading folding) and CR 144 (find and replace) taken out of the stack (PRs #151 and #152 stay open, #152 on top of #151; both based on CR 142 / each other). Reason: heavy integration passes on CR 135 and CR 142 and fails from CR 143 up (tableMoves column drop zone); CR 144 additionally fails on the find bar in a real window. CRs 145 to 151 rebased onto CR 142 (their own commits only; toolbar counts and banner reserve adapted: 6 buttons in toolbar row 3). New stack: #144 to #150 then #153 to #159 (`gh stack link`, stack #161). Heavy on the new top: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40643701038
- 07:50 heavy on top 40643701038: integration fails (tableMoves column drop zone, same as CR 143), stress fails (incoming-changes click timeout, also on 147/150 runs 40644324751/40644322066; passes on 135 and 142). Bisecting again on 142 (rerun), 145, 146.
- 07:57 heavy bisect: 135 (40640634459) and 142 (40640637221, rerun 40645287945) integration pass (135 and first 142 also stress pass); 145 (40645281839) integration fails on a different test (checkboxToggle: rendered webview timeout, an early-suite window flake); 146 (40645284742) integration fails; 147/150/top fail on tableMoves column drop zone; stress fails from 147 up (incoming-changes click timeout). Heavy stays red above CR 142; cause unproven (flake vs regressions). Final head of CR 151: 29b66f89.

## Run 6 (stack driver restart, 09:10 on)

- 09:30 CRs 146 (#154), 147 (#155), 148 (#156), 149 (#157), 151 (#159) rebased ALONE onto origin/main 6df062d3, `just check` green, pushed, PRs retargeted to main (stack #161 unstacked). 150 (#158) cannot build alone: its writing-skill test renders cards/tabs (CR 148) and Vega-Lite (CR 149), so its branch is main + 148 + 149 + 150 (own commit 28a8dab0). 143 (#151, 4228cc6a) rebased on main, check green, retargeted to main; 144 (#152) rebased on 143 (check running).
- 09:30 heavy runs dispatched on all: 146 40656099555, 147 40656102922, 148 40656106342, 149 40656110094, 150 40656113486, 151(CR 151) 40656116823, 143 40656120188. Stress is advisory.
- 09:20 User merged #144-#150 and #153 (CRs 135, 137-142, 145) on main (6df062d3). CRs 146-151 are each rebased alone on main (146, 147 by me; 148-151 by parallel agents). Heavy per CR dispatched in parallel (146 40656099555, 147 40656102922, 148 40656106342, 149 40656110094, 150 40656113486, 151 40656116823, 143 40656120188).
- Evidence so far: CR 146 fails heavy integration twice on the same test (image drop inserts after the first gap: 40645284742, 40653828236). CR 147 fails the tableMoves column drop zone on 3 runs (40644324751, 40653831894, 40654965310), the same test that fails on CR 143. Common factor of 143 and 147: each adds a 6th button to toolbar row 3 (wider toolbar), hypothesis: it overlaps the table handle strip at the integration window size.
- 09:55 heavy integration: 146 FAIL (dropFiles, link/image on one line), 148/149/150 FAIL (all windowSwitchKeys "Timed out waiting for margin: the keyboard to select a block", also on independent 149 -> suspect flake/ordering or main; heavy on main dispatched: 40658224831 and 40657976144), 143 FAIL (tableMoves). 147 and 151 pending. STATE.md headers of 146/148/150/143 set blocked.
- 10:00 windowSwitchKeys 'margin keyboard' timeout also fails on main itself (run 40657976144) -> flake suspected; reran failed jobs of 148 (40656106342), 149 (40656110094), 150 (40656113486).
- 09:55 Heavy on main itself (40657976144, head 6df062d3) FAILS integration at test/integration/windowSwitchKeys.test.ts ("margin: the keyboard to select a block"): same test fails on 145 (40653824676), 148 (40656106342), 149 (40656110094), 150 (40656113486). CR 142 passes heavy (40640637221), so the regression entered with CR 145 (paste URL, merged; touches blockSourceEditor.ts) or the merge combination. No branch above main can be heavy-green until main is fixed. Other failures: CR 146 image-drop position test (3 runs, deterministic), CR 147 and CR 143 tableMoves column drop zone (4 runs; both add a 6th toolbar button).
- 10:15 147 integration timed out at 30 min (hang, no failing assertion logged; 40656102922), rerun dispatched. main heavy (2 runs) fails windowSwitkKeys deterministically.
- 10:30 reruns of 149 and 150 failed again on windowSwitchKeys (deterministic); main heavy fails the same test twice (40657976144, 40658224831). 147 rerun, 148 rerun, 151 (40656116823) still in progress. No CR is integration-green yet; stack not restacked. Suspect CR 145 (only commit after 142, whose heavy integration passed). Handed back to the main session.
- 10:55 per orchestrator: stack #163 = #156 (148) -> #157 (149) -> #158 (150) on main c9608cbe, check green, linked; heavy on 150: 40661252746. 147 (#155, 529211e2) and 151 (#159, 2faa5dea) rebased alone on c9608cbe, check green; heavy 40661548282 (147), 40661551926 (151). 146 blocked (dropFiles); 143/144 out.
- 11:35 after #164 (main 724841e6): rebased 148 (7c461166) -> 149 (34653639) -> 150 (92795f31), 147 (63fca69e), 151 (731b742c); check green; heavy: 150 40666806719, 151 40666810273, 147 40666814711. Normal CI running.
- 12:05 heavy: 151 integration green (40666810273); 150 stack red: mystBlocksWindow 'editor holds the source of the tab item only' (40666806719); 147 red tableMoves (40666814711), same as 143 -> main heavy dispatched to check. Told main.
- 12:50 stack 148-151 merged. Main heavy 40668487526: integration SUCCESS (tableMoves passes on main). Hotfix PR #166 (tab item edit) heavy 40670233768. #155 rebased on main b2ba3abf (0c423fb1), check green (okfreq 0.16.0), heavy 40670595531.
- 13:30 all rebased on main bc15ce75 (okfreq 0.16): 147 afcd0cd8 (heavy 40672628996), 143 19ea6faf, 144 ddcc4097, 146 d63ed2c0, hotfix #166 bddede2e (heavy 40672624752). Main heavy green. 147 tableMoves red twice -> blocked.
- 13:55 #166 heavy 40672624752: mystBlocksWindow passes now; integration fails later in commentAnchors (ENOENT notes.comments.json, unrelated, main green) -> rerun. 147 heavy 40672628996 tableMoves again -> blocked. Normal CI green on 151,152,154,155; 166 visual pending.
- 14:30 main f7b17518 (143 merged). Rebased: 144 ac7c95ae (#152), 146 d1ab8e61 (#154), 147 e4a16b63 (#155; toolbar now 15 buttons/7 in row 3: Fold + Side-by-side), 166 acfe0bb8. Heavy: 166 40675571987, 147 40675575617. PERMISSION DENIED (not worked around): git add -A docs requirements src test (I then added files by name). 166 old heavy 40672624752: mystBlocksWindow passed, failed in commentAnchors (ENOENT notes.comments.json).
- 15:00 #166 heavy 40675571987 fails tableMoves -> main (with 143 merged f7b17518) now fails tableMoves: the regression comes from CR 143, not from 147. Normal CI green on 152,154,166; 155 visual pending.

## Run 7 (planner-tick mode, 2026-10-28 13:40)

Base origin/main 2992b50a. Separate: [#167](https://github.com/gsemet/markdown-okf-schema-studio/pull/167)
(CR 153, toolbar 4 rows + tableMoves), merges first. Parked: #154 (146), #155 (147), drafts.

Planned stack, bottom → top (each developed alone from origin/main in its own worktree, then
restacked by a stack driver with `gh stack`):

| Pos | CR | Branch | Worktree | PR | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | [154](154-myst-tab-item-edit-source/work/STATE.md) | `fix/tab-item-edit-source` | wt-148 | [#166](https://github.com/gsemet/markdown-okf-schema-studio/pull/166) | finishing (screenshots, body) |
| 2 | [155](155-frontmatter-diff-line/work/STATE.md) | `change-requests/155-frontmatter-diff-line` | wt-155 | [#169](https://github.com/gsemet/markdown-okf-schema-studio/pull/169) | landed alone on main (merge 55b5c371), out of the stack |
| 3 | [156](156-empty-document-keyboard-start/work/STATE.md) | `change-requests/156-empty-document-keyboard-start` | wt-156 | — | coding |
| 4 | [157](157-structural-keyboard-navigation/work/STATE.md) | `change-requests/157-structural-keyboard-navigation` | wt-157 | — | coding (from origin/main, conflicts with 156 resolved at restack) |
| 5 | [158](158-writing-skill-okf-definitions/work/STATE.md) | `change-requests/158-writing-skill-okf-definitions` | wt-158 | [#168](https://github.com/gsemet/markdown-okf-schema-studio/pull/168) | landed alone on main (merge 8a296d5e), out of the stack |

Order rationale: small fixes low; 156/157 adjacent (same keyboard code, both developed from origin/main in parallel, restacked by the stack driver); docs-only
skill at the top (independent, never blocks). Stack assembly = a later "stack driver" tick, once
each PR is open with normal CI green.

## Run 7, stack driver tick (2026-10-28 ~14:40–15:05)

Stack built on origin/main 55b5c371, bottom → top: [#166](https://github.com/gsemet/markdown-okf-schema-studio/pull/166) (154) → [#171](https://github.com/gsemet/markdown-okf-schema-studio/pull/171) (156) → [#170](https://github.com/gsemet/markdown-okf-schema-studio/pull/170) (157).

- 154 rebased on 55b5c371 → 01707157 (conflicts: CHANGELOG, tiers/log.md kept both entries; e2eGroups 396). 156 rebased onto it → 12f8db62 (log.md both; e2eGroups 398; layout-width/v86-v87). 157 squashed (feature + BLOCK-254 renumber fixup) and rebased onto 156 → 886bf47f (CHANGELOG, log.md, docs/user/editing.md and block-editing/index.md: both sides kept; e2eGroups 400; block-editing/v20-v21). Keyboard code merged without conflict (only editModeStyles.ts shared, disjoint hunks). `just requirements-update`: 0 changes at each level; `just check` green at each level (top: 3095 + 69 tests); okfreq validate 1057 / 1058 / 1059 requirements, 0 errors; BLOCK-253 and BLOCK-254 unique; 156+157 webview tests 25/25 at the top.
- `gh stack link` refused: #166 had auto-merge enabled (by the user). Not disabled; bases set with `gh pr edit --base`; stack line added to the three PR bodies.
- Heavy on top dispatched: [40700084682](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40700084682).
- The user merged #170 into 156, #171 into fix/tab-item-edit-source, then #166 into main: main 67ccf8c9 = d100ea3d (154), c6c96731 (156), 67ccf8c9 (157), linear. Main CI: [40700143893](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40700143893).
- Landed 154, 156, 157 (reports in 04-archives). Review notes → [02-backlog/P3/keyboard-nav-followups](../2-backlog/P3/keyboard-nav-followups/01-intent.md). Stack empty. Worktrees and branches kept.
