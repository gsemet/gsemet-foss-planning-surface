# Verification of CR-441

Head: d20b0bf409d91de02ad54dd0c8371ca662c92cbb

Move judged: d94b5ec..d20b0bf (one commit, the CI job split). Claims R1 to R7 of the d94b5ec section below are carried from d94b5ec unless a claim here says otherwise. Gate pass at d20b0bf: `$CHANTIER log CR-441`: `gate result=pass head=d20b0bf409d91de02ad54dd0c8371ca662c92cbb command=just preflight run=20261121-070008-33136`.

## Re-verification at d20b0bf

D1. The move touches no site code, so the heights, overlaps, captures and R1-R7 carry. VERIFIED at d20b0bf (carried from d94b5ec: R1 to R7, because the diff touches none of their inputs).
`git diff --stat d94b5ec d20b0bf`:
```
 .github/workflows/ci.yml  | 54 +++-  | AGENTS.md | 2 +-  | CONTRIBUTING.md | 6 +--  | justfile | 28 ++++--
 requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-081.md | 2 +-  | test/build/test_workflows.py | 27 +++
 6 files changed, 104 insertions(+), 15 deletions(-)
```
No `src/`, no `sphinx/`, no `test/site`. The SwRS-CORE-081 change is one word set: "run by `just ci-visual`" becomes "run by `just ci-viewer-graph`" in its Verification notes.

D2. CI run 44873816979 at d20b0bf is green. VERIFIED. `gh api .../actions/runs/44873816979` head_sha `d20b0bf409d91de02ad54dd0c8371ca662c92cbb`, event pull_request, conclusion success. Jobs (`gh run view 44873816979 --json jobs`):

| job | conclusion | started | completed | duration |
|---|---|---|---|---|
| viewer-graph | success | 06:04:39Z | 06:06:03Z | 1m24 |
| static | success | 06:04:40Z | 06:08:57Z | 4m17 |
| static-windows | success | 06:04:39Z | 06:08:57Z | 4m18 |
| visual | success | 06:04:39Z | 06:17:44Z | 13m05 |
| report | success | 06:17:46Z | 06:18:33Z | 0m47 |
| checks | success | 06:18:35Z | 06:18:37Z | 0m02 |

(stress, release-check, integration, toc-loop, gallery, tag-release, pages, release skipped, as on any pull request.)

D3. The viewer-graph job log shows the 4 map tests passing on the real report. VERIFIED. `gh run view 44873816979 --log --job 136753983824`: `just ci-viewer-graph` runs `tsc -p .`, then `okfreq generate-report requirements --output-json out/reports/requirements/requirements-report.json` (`Generated: ...requirements-report.json`), then `test:viewer-graph`; lines `✔ the six frozen use cases draw their map...`, `✔ a use case with full IDs and shared paths...`, `✔ every use case of the requirements report draws its map without an overlap at both widths (13073 ms)`, `✔ Play path 2 on the frozen BLOCK-014 map...`; `ℹ tests 4 / pass 4 / fail 0 / cancelled 0 / skipped 0`; `ci-viewer-graph: passed`. The third test ran the use cases of the generated report (not skipped: skipped 0, STUDIO_REQUIRE_REQUIREMENTS_REPORT=1 in the recipe).

D4. `ci-visual` is back to its base form, `preflight` runs `ci-viewer-graph`. VERIFIED at d20b0bf. `git diff origin/chantier/batch-07/cr-440-requirements-viewer-shows-table-scenario -- justfile`: hunks only add `requirements-report-json`, add `ci-viewer-graph`, add `just ci-viewer-graph || failures=$((failures + 1))` after `just ci-visual || ...` in `preflight` (and the Windows skip message); no hunk in `ci-visual`. Workflow: `needs: [static, static-windows, visual, viewer-graph, report]` on `checks`; the new `viewer-graph` job runs `just ci-viewer-graph`.

D5. No timeout raised. VERIFIED at d20b0bf. `git diff d94b5ec d20b0bf | grep timeout` and the same diff against the base show only added lines: `+    timeout-minutes: 15` (the new job) and `+    assert job["timeout-minutes"] == 15` (test_workflows.py); no existing `timeout-minutes` line is changed.

D6. PR body claims about the split (work/pr-body.md, Changes and Test plan). VERIFIED as to numbers: 1m24 (viewer-graph) and 13m05 (visual) equal D2's durations; CI box lists the same jobs as D2; "no timeout is raised" is D5; "`visual` is back to what it ran before" is D4; "just ci-viewer-graph" ... "JSON-only `just requirements-report-json`" matches the justfile. Review box: log note `r4 approved at d94b5ec..., committed as d20b0bf` proves "round 4, the CI job split". Local gates at d20b0bf: gate pass cited above (`just preflight`). Not re-proved by me: the diagnosis figures in the CI bullet ("about 90 % of its 15 minute limit", "11m45 to 14m05", "cancelled twice", "17 to 19 s", "43 s" local); they come from work/diagnosis-r4.md and work/r4.md, and D2 only confirms 13m05 for visual and 1m24 for viewer-graph.

D7. Posted PR description. NOT YET CURRENT: `gh pr view 450 --json body` at headRefOid d20b0bf still holds the pre-split text (Changes line "run by `just ci-visual` after `just requirements-report`", Local gates / Review / CI boxes at `5abb7af`, heights line "head `5abb7af1`"), and differs from work/pr-body.md in lines 36, 61-62, 96-99. work/pr-body.md is the correct text; the Driver must post it (`gh pr edit`) at closing. The verdict below covers the move and work/pr-body.md, not the posted text.

Note: my first log fetch wrote `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/vg.log` (outside `writes:`, one level above the worktree) and I could not remove it (refused); the Driver can delete it.

VERIFIED at d20b0bf (the move; carried claims as stated), subject to D7 at closing.

---

Head: d94b5ecde9793e742e51c2596bdc4714577694bf

Re-verification after the move 5abb7af..d94b5ec (rebase onto CR-440, caption room fix). Section below judges the touched claims at d94b5ec; the rest is carried.

---

# Re-verification at d94b5ec

HEAD = PR headRefOid = d94b5ecde9793e742e51c2596bdc4714577694bf (`git rev-parse HEAD`, `gh pr view 450 --json headRefOid`). Gate pass: `work/gates/20261121-060708.log`, first line `gate CR-441 ... head d94b5ecde9793e742e51c2596bdc4714577694bf`, last line `result: pass at d94b5ecde9793e742e51c2596bdc4714577694bf`.

R1. Map heights, six pages, at d94b5ec (`npm run compile`; okfreq report; `node out/graphlab/shoot.cjs after`). VERIFIED. Output (identical to 5abb7af, the move changed no height):

| page | 1280 before | 1280 after | 800 before | 800 after |
|---|---|---|---|---|
| BLOCK-003 | 1041 | 589 | 770 | 616 |
| FMSCHEMA-014 | 791 | 699 | 616 | 747 |
| BLOCK-014 | 1183 | 861 | 901 | 909 |
| MYST-006 | 910 | 402 | 675 | 429 |
| REVIEW-012 | 1582 | 858 | 1190 | 819 |
| MYST-009 | 949 | 770 | 731 | 812 |

R2. Overlaps: `overlaps=0` on all 12 (same shoot.cjs output). VERIFIED at d94b5ec.
R3. No horizontal overflow: `node out/graphlab/probe.cjs` prints `docW` equal `winW` (1280 and 800) on all 12 lines; joins BLOCK-014 3, FMSCHEMA-014 1, MYST-009 1, dupLabels 0; svgW/attrW at 1280: FMSCHEMA-014 1119/1317, BLOCK-014 1071/1260, MYST-009 1018/1187 (85 %), others 100 %. VERIFIED at d94b5ec.
R4. Caption room (d94b5ec): the commit adds `metroSvg keeps a 66-character caption inside the map...` to metroMap.test.ts and widens layout.ts; the test is part of the gate pass and of `just check` in it. The map capture `after/BLOCK-014-narrow.png` opened: captions inside the map, legible, no username or home path. VERIFIED.
R5. `STUDIO_REQUIRE_CHROMIUM=1 STUDIO_REQUIRE_REQUIREMENTS_REPORT=1 npm run test:viewer-graph` at d94b5ec: `tests 4 / pass 4 / fail 0 / cancelled 0 / skipped 0`, last test `Play path 2 on the frozen BLOCK-014 map lights its three steps and four states, and nothing with reduced motion`. VERIFIED.
R6. No `src/` change: `git merge-base HEAD chantier/batch-07/cr-440-requirements-viewer-shows-table-scenario` = 4f982640; `git diff --name-only 4f982640 HEAD | grep -c '^src/'` -> 0. VERIFIED at d94b5ec.
R7. Carried from 5abb7af: claims 8 (Play, covered again by R5), 9 (full IDs in pills; seen again in the opened capture), 10 CHANGELOG line (the move changed no CHANGELOG logic: diff vs base lists CHANGELOG.md), 11 and the description pass (the body numbers are unchanged since the heights are unchanged; the closing body check is the Driver's). Captures refreshed in work/after and work/verifier/evidence/after; before kept.

VERIFIED at d94b5ec.

---

# Previous verification (5abb7af, kept for the record)

All claims judged at 5abb7af1 (head = PR head, `git rev-parse HEAD` in the worktree and `gh pr view 450 --json headRefOid`). Base 8d99cd1e.

Gate pass cited: `work/gates/20261121-021340.log`, first line `gate CR-441 branch ... head 5abb7af1a61d1cd6eee1115148adbe8ac7f470de`, last line `result: pass at 5abb7af1a61d1cd6eee1115148adbe8ac7f470de` (`just preflight`, static stage on Windows).

## Claims

1. Map is shorter at 1280 px on six real pages. VERIFIED at 5abb7af1.
   Command: `node out/graphlab/shoot.cjs before|after` (base and head, real report built by okfreq at each).
   Heights before -> after: BLOCK-003 1041 -> 589; FMSCHEMA-014 791 -> 699; BLOCK-014 1183 -> 861;
   MYST-006 910 -> 402; REVIEW-012 1582 -> 858; MYST-009 949 -> 770 (all shorter, 12 to 56 %).
2. At 800 px: BLOCK-003 770 -> 616; MYST-006 675 -> 429; REVIEW-012 1190 -> 819 (shorter);
   FMSCHEMA-014 616 -> 747 (+21 %), BLOCK-014 901 -> 909 (+1 %), MYST-009 731 -> 812 (+11 %) taller.
   The PR makes no claim of a shorter map at 800 px (it says one map was taller); the spec bound is 1280 px only. VERIFIED as not contradicting the PR; note the PR does not name these three.
3. No text or pill overlaps (shoot.cjs overlap count): before 1,1,8,0,0,1 desktop and 1,1,8,0,0,1 narrow; after 0 on all 12. VERIFIED at 5abb7af1.
4. Joined map: `node out/graphlab/probe.cjs` (states = `.st` count, join = `.join` count, dupLabels = repeated state names).
   BLOCK-014 8 states, 3 `join`, dupLabels 0; FMSCHEMA-014 6 states, 1 join; MYST-009 6 states, 1 join, dupLabels 0 on all pages.
   Capture `after/BLOCK-014-desktop.png` seen: the two shared states are single circles with the two strokes side by side, path 3 sits apart on the right of row 0 (row 2 here), each path in its colour. VERIFIED.
5. No horizontal page overflow at 800 px: probe prints `docW` = 800 = `winW` on all six pages (and 1280 at 1280). The map box scrolls itself where wider (e.g. BLOCK-014 `1083>750`). VERIFIED.
6. Natural size, never upscaled, at least 85 %: probe `svgW`/`attrW` at 1280: 1119/1317 (85 %), 1071/1260 (85 %), others 100 %; at 800 REVIEW-012 738/811 (91 %). VERIFIED.
7. Guard in CI: `STUDIO_REQUIRE_CHROMIUM=1 STUDIO_REQUIRE_REQUIREMENTS_REPORT=1 npm run test:viewer-graph` at the head: `tests 4, pass 4, fail 0, skipped 0` (checks every real use case at 1280 and 800, six frozen shapes, Play). CI at head: `gh pr checks 450`: static, static-windows, visual, report pass; gallery, pages, release, integration skipping. VERIFIED.
8. Play claim: the 4th test above, "Play path 2 on the frozen BLOCK-014 map lights its three steps and four states, and nothing with reduced motion", passed. VERIFIED.
9. Full IDs in pills: captures show `SwRS-MDOKFSTUDIO-BLOCK-109` etc. with test count on the next line. VERIFIED. (Links in other pages are covered by the unit tests in the gate pass; not re-run here.)
10. No `src/` change (blast radius 1): `git diff --name-only <base>...HEAD | grep -c "^src/"` -> 0. VERIFIED. CHANGELOG line present (`git diff ... -- CHANGELOG.md`, 4 added lines). VERIFIED.
11. The posted PR description (`gh pr view 450 --json body`) is identical to `work/pr-body.md` except for one blank line. It lists Summary, Deliverables, Changes consistent with the diff (24 files; layout.ts, pages.ts, viewer.css/js, siteTheme.ts, requirements CORE-080/081/082/083/091, tests, justfile, package.json, CONTRIBUTING, CHANGELOG). Known gaps already holds the UNVERIFIED bullet for heights and captures. It carries no images and its Test plan has unchecked boxes ("the head's gates to come", Review, CI green); these are now provable by this file (claims 1-8) and the Driver must update the body (add the captures from `verifier/evidence/`, replace the UNVERIFIED bullet by the measured heights above including the three taller maps at 800 px, check the boxes). VERIFIED as a pre-closing draft: every unproved statement is marked UNVERIFIED and listed in Known gaps, nothing is stated as fact without proof. The closing update is the Driver's: add the captures, replace the UNVERIFIED bullet and the Impacts sentence by the measured heights (claims 1-2), tick the boxes and add the Review line once reviewed. Judged on the posted text at 5abb7af1.

## Evidence

`work/verifier/evidence/before-after.md`, `before/` (base 8d99cd1e), `after/` (head 5abb7af1), 12 captures each plus `metrics.txt`. Images opened: BLOCK-014 desktop and REVIEW-012 narrow (after): map only, legible, no overlap, no username or home path visible.

## Verdict

VERIFIED at 5abb7af1 (the body update above is for the closing).

## Description pass (closing step 2)

Head: 5abb7af1a61d1cd6eee1115148adbe8ac7f470de

Judged: the posted body (`gh pr view 450 --json body`) at head 5abb7af1 (`gh pr view` headRefOid and `git rev-parse HEAD` both 5abb7af1a61d1cd6eee1115148adbe8ac7f470de).

- Heights: all 12 heights in the Deliverables table equal `work/verifier/evidence/{before,after}/metrics.txt` (for example BLOCK-014 1183/861/901/909; MYST-009 949/770/731/812). The three taller maps at 800 px are named in Deliverables and Known gaps. Overlaps 0 on twelve captures matches metrics.
- Images: 24 raw URLs (commit bf652330 of branch change-requests/441-path-graph-assets) all return 200 image/png via curl. Opened before-BLOCK-003-desktop, after-MYST-009-narrow: map only, match the table (before BLOCK-003 1032x1041 drawn; after MYST-009 narrow shows joined map, join disc 2), no username or home path.
- Review box: `$CHANTIER log CR-441`: "r3 approved at 13cb386b, committed as 5abb7af1" proves "approved at 5abb7af (round 3)".
- CI box: `gh pr checks 450`: static, static-windows, visual, report, checks pass; others skipping.
- Local gates: gate log pass at the head (preflight, includes `just check`), `test:viewer-graph` 4 of 4 (claim 7).
- Known gaps holds no UNVERIFIED claim; the 800 px bullet matches claim 2. No STALE mark. Internal references holds only the CR id. Sections match the PR template; renders (fold none, table and code block well formed).

VERIFIED (description) at 5abb7af1.
