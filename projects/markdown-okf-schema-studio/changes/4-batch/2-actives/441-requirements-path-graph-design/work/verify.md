# Verification of CR-441

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
