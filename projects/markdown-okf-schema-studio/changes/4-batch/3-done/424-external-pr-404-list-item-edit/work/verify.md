# Verify: CR-424 (PR 431), list item edit scope and list items in the TOC (round 2, follow-up)

Head: ea4d1937d66259e6c05993aea87b209704b38ab9

Verdict: VERIFIED

## Follow-up description pass at a6f0de15a2dc34fcb5128b0e91df04af6bef7ff6

`git rev-parse HEAD` = a6f0de1 and `gh pr view 431 --json headRefOid` = a6f0de1; `git status --short` empty. Posted body read with `gh pr view 431 --json body`.

- Known gaps: new last bullet "The item click and pointer screenshots are in the dark theme only, and the ordered-list numbering is checked in Chromium ... not in Firefox or Safari" covers the two "Not captured" lines of before-after.md that failed before; the other Not captured lines (real window/macOS, cost) already had bullets. The previously failed claim now holds.
- Images: the 11 re-uploaded images downloaded from the posted URLs and compared with `sha256sum` to `work/verifier/evidence/`: every hash equals its file; order and captions match (TOC before/on/off; ordered list; item click; hover; rail, the same image both sides as 11 ticks both). Looked at in the earlier pass at the same head: no username, no home folder.
- Other description claims carried from a6f0de1 (earlier pass, same head, no commit since): SHAs and boxes, Summary/Deliverables/Changes match the diff, Review and gates boxes (carry from 06eda91), "Verified at" and "CI green at" left open on purpose.
- Code claims carried from a6f0de1 (same head): tests 329 pass, ordered numbers, TOC on/off, patch-ids, security, requirements (see below).

## Previous pass (superseded)

## Description pass at a6f0de15a2dc34fcb5128b0e91df04af6bef7ff6 (posted body of PR 431, read with `gh pr view 431 --json body,headRefOid`; headRefOid = a6f0de1, `git status --short` empty)

Verdict: NOT VERIFIED (one claim: Known gaps). Code claims below are carried from the earlier pass at the same head a6f0de1 (no commit since).

Holds:
- SHAs: 770c852 and f7d7a6d appear and are in `git log --oneline` of the branch; gates box "at a6f0de1 (carried from 06eda91)" matches the gate log and the `carry` event; Review box "approved at a6f0de1 (carried from 06eda91)" matches `$CHANTIER log CR-424` (`r2 approved at f9c7817 ... committed as 06eda91`, then `carry head=a6f0de1 gate_from=06eda91`). Impacts holds the screenshots; "Verified at" and "CI green at" boxes left open on purpose.
- Images: all 11 downloaded from the posted URLs and compared with `sha256sum` to `work/verifier/evidence/`: each hash equals its file, and placement and caption match before-after.md (TOC table: before-toc-on, after-toc-on, after-toc-off; Impacts: ordered list, item click, hover, rail pairs; the rail before and after are the same image, as 11 ticks both). Looked at in the earlier pass: no username, no home folder.
- Summary, Deliverables and Changes match the diff (earlier pass, same head).

Failed:
1. **Known gaps lacks an evidence pair `before-after.md` says was not captured**: its "Not captured" lists "Light-theme pairs of the item click and hover" (and numbering in Firefox and Safari); Known gaps has neither bullet (it has the real-window/macOS, rail, caret, nested, footnote and cost bullets). Add a bullet for them.

Earlier pass (same head, superseded for the description):

## Claims that hold

- **Patch carried from 06eda91 to a6f0de1 unchanged.** `git patch-id --stable` per commit, base side then head side: `6e8e9005... f7d7a6d9` = `6e8e9005... 20583f69`; `da71a396... 770c852e` = `da71a396... 15b65463`; `7a2ac425... dca81baa` = `7a2ac425... f9c7817c`; `ad2bce19... a6f0de15` = `ad2bce19... 06eda91a`. The base moved (`git diff --name-only 82c11a47 145f1953`: justfile, package.json, requirements/guidelines, requirements/tiers/log.md, StRS TRUST-014, SwRS CORE-090, a use-case-diagram check script and its test, chartCsp/chartPage/pinnedFont/tableBreakout tests): the two files the CR also edits (`package.json`, `requirements/tiers/log.md`) merged mechanically, so I re-ran the checks that read them (next bullets).
- **Settings registry and generated `package.json` agree at the head.** `npm run check:settings` (`node scripts/generate-settings.mjs --check`): `check-settings: passed (20 settings)`.
- **Unit and page tests at a6f0de1.** After `npm run compile` (exit 0), `node scripts/node-test.mjs unit` on listItemEditOpen, alertBlockEditOpen, runtimeBlockEditor, runtimeBlockMoves, runtimeStructuralNavigation, runtimeContentPatch, blockReq.requirements, modules/tocColumn, configuration/settingsRegistry, configuration/previewConfiguration, previewStyles, security/package-contract: `tests 329, pass 329, fail 0` (log `work/gates/verifier-a6f0de1-tests.log`). They cover the item click, the whole-list click, the hover outline on the item, Right/Left/Enter, the arrows between items and past the list, an admonition inner block keeping the arrow, the move chord in an item editor (T37), the TOC with the setting on and off (skips `[TOC]`, footnotes, tables). The test-fails-on-previous-code proof (23 failures on the base with the head's tests) is carried from f9c7817 (`work/gates/verifier-base-with-head-tests.log`): the patch of those commits is unchanged (patch-ids above).
- **Ordered list keeps its numbers while an item is edited** (SwRS-MDOKFSTUDIO-BLOCK-014; the round-1 failure). At a6f0de1: `npm run visual:render` (exit 0, `work/gates/verifier-a6f0de1-render.log`) then `uv run --no-sync --group docs python test/visual/capture.py --scenario edit-list-narrow --scenario edit-affordances-hover-and-open --workers 2` (exit 0): `passed: block-editing/v12-list-item-opens-item-dark-460`, `passed: block-editing/v06-hover-outline-then-editor-dark-900` (log `work/gates/verifier-a6f0de1-capture.log`; this scenario runs `test/visual/capture_list_numbers.py` `check_ordered_item_keeps_numbers`). My own check, `work/verifier/shots.py` (Chromium, "Shift changes" ordered list, edit mode, click on item 2): `after editor: '2. Depot reports vehicle availability.'`, `after list markers: [..., '1. ', '3. ', '4. ', ...]`; on the base the same click gives the whole list in the editor (`before editor: '1. Outgoing shift scans off ...\n2. ...\n3. ...\n4. ...'`). The image `after-ol-item-click-light-900.png` shows `1.`, the editor, `3.`, `4.`. The new check is a rendered one (it failed on round-1 CSS per `work/gates/r2-capture-before.log`, carried: `r2.md`; the test file and the CSS are those of a6f0de1).
- **List items in the TOC, off by default** (SwRS-TOOLBAR-138, TOOLBAR-040, StRS-TOOLBAR-006). `shots.py`: setting on `after toc entries 23 ticks 11` at 900 and 460 px; off `after toc entries 11 ticks 11`; base `before toc entries 11 ticks 11` (images `after-toc-on-light-900.png`, `after-toc-off-light-900.png`).
- **Move chord, SwRS-BLOCK-130 meaning unchanged; requirements** carried from f9c7817 (patch-ids equal; requirement files are part of the same commits): only StRS-BLOCK-003 is an approved requirement changed (commit 770c852 = 15b6546, owner's wording, `approved_by` unchanged); BLOCK-130 gets one Method line and keeps `proposed`.
- **Security** carried from f9c7817 (patch-ids equal): no network call, script or external resource added in `src/`; TOC text set with `textContent`.
- **Images** (all 12 opened, each looked at for a local path and a username): none shows either; each shows its claim: item click (editor holds the item, not the list), hover (outline on the item), ordered list (numbers kept), TOC on/off, rail (11 ticks both sides).
- **CI at a6f0de1**: PR checks run 44719067780 and heavy run 44719102702 were running when I finished; not judged here.

## Evidence

`work/verifier/evidence/before-after.md` (six pairs, before at 145f195, after at a6f0de1). Before-side detached worktree removed at the end.


## Closing description pass at ea4d1937d66259e6c05993aea87b209704b38ab9

Head: ea4d1937d66259e6c05993aea87b209704b38ab9. `git rev-parse HEAD` = ea4d193; `gh pr view 431 --json headRefOid,isDraft` = ea4d193, draft true. Code claims carried from a6f0de1 (clean rebase onto 7644edd, range-diff all '=', `carry` event in `chantier log`; the base change touched only test/node-services/build/buildQueue.test.ts, not what the proofs run).

- SHA marks: `git log --oneline origin/main..HEAD` = ea4d1937, 25de284b, 739a0115, 16a42571; the body names 739a011 (requirement commit) and 16a4257 (contributor, author pspozio per `git log -1 --format=%an`); all in history. Marks read `at ea4d193 (carried from ...)`, each with its reason.
- CI: `gh pr checks 431`: static, static-windows, visual, report, checks pass, heavy jobs skipping (project rule), run 44722192896. `gh run view 44722255133 --json headSha,...`: headSha ea4d193, success; integration, stress, gallery, report, checks success. CI box holds.
- Review box: log note "r2 approved at f9c7817, committed as 06eda91" and the `carry` event at ea4d193 (gate_from 06eda91); carried with reason. Holds.
- Diff vs Summary/Deliverables/Changes: `git diff --stat origin/main...HEAD` (47 files) matches the listed files. No unmentioned change.
- Images: 11 distinct user-attachments URLs in the body, same as those hash-checked at a6f0de1 (no new upload); no username or home folder text in the body (grep count 0).
- Known gaps unchanged and complete; no role name of the doer in the body.

VERIFIED
