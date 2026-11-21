# CR-435 verify

Head: 2004e521db9acf1b8d752f0f5b7cb422d7939108

Scope: first verification. Branch is on origin/main 33d10454 (CR-425 and CR-434 not landed): the spec's
CR-425/CR-434 parts are judged as adapted (batch-head.js calls steeringWord, no steeringFactoryWord; tab bar as main has it).
Evidence (pictures, before-after.md, measures) is in evidence/ of the CR folder, as the prompt asked.

## Claims

1. Shipped test passes. SHA 2004e521db9acf1b8d752f0f5b7cb422d7939108. Command: uv run --no-sync --project . pytest skills/chantier/scripts/cli/tests/test_board_design.py -q
   Output: 32 passed in 0.30s. VERIFIED (that it fails on the previous code was not run: UNVERIFIED, not claimed).
2. Gate pass at the head. Cited: work/gates/20261121-222311.log first line "gate CR-435 branch chantier/batch-30/cr-435-batch-page-the-mode-and-the-legend-move- head 2004e521db9acf1b8d752f0f5b7cb422d7939108", last line "result: pass at 2004e521db9acf1b8d752f0f5b7cb422d7939108". CI at the head (gh pr checks 408): check macos/ubuntu/windows, eval-dry-run, scenario all pass. VERIFIED.
3. Old rules gone, new scoped. Command: grep -nE "\.batch (\.mode|\.mb|\.ms|\.lg|\.tip)|\.bmode \.(mode|mb)\b" css/views/batch.css -> no output; grep steeringFactoryWord js -> none; grep 'class="mode"|lgrow|legend(' js/views/batch.js -> none; .bmode rules present (batch.css lines 43-173, hover/focus/focus-within show rules for .mpill and .lgpill, phone block). VERIFIED at 2004e521db9acf1b8d752f0f5b7cb422d7939108.
4. Desktop 1400x860, layout. measure-before.json / measure-after.json (measure.py): .tabs top 353 before, 263 after (90 px higher); .bhead top 143 before and after; title row 58 to 111 both. Pictures batch-pc-before/after.png opened: mode pill, legend pill and hint at the title row's line, switch at the right end, nothing between figures and tab bar. VERIFIED at 2004e521db9acf1b8d752f0f5b7cb422d7939108 (before = 33d10454).
5. Tips at 1400x860 (hover). mpill tip box l510 t117 r810 b184, inside viewport true; lgpill tip l633 t117 r933 b344, inside true. document.elementFromPoint at the centre of the tip's part over a figures tile: mpill (527,164) returns el "tip" inTip true; lgpill (725,195) returns "k" (child) inTip true. Pictures batch-pc-tip-*-after.png opened: both tips whole above the tiles. Cursor help on both pills (measure-after.json: cur "help"). VERIFIED at 2004e521db9acf1b8d752f0f5b7cb422d7939108.
6. Phone 375x812. scrollWidth 375 <= innerWidth 375; .mpill top 127 and .lgpill top 127 (equal); .lghint and .ms display none; mpill tip (focus) l28 r363 inside viewport, lgpill tip (focus) l28 r341 inside; elementFromPoint over a tile returns the tip or a child. Pictures batch-phone-*-after.png opened. VERIFIED at 2004e521db9acf1b8d752f0f5b7cb422d7939108.
7. Closed batch mobile-app batch-01: slot text "Stack · Foreman / States and arrows / hover for the legend / Stack / Series / Parallel", not hidden; picture closed-pc-after.png shows title row, figures, deps note, then the view switch. VERIFIED at 2004e521db9acf1b8d752f0f5b7cb422d7939108.
8. Batch with no CR from a scratch surface (git init, chantier init, open --remote origin --default-branch main, no order add; board started on it): slot text "Parallel · Foreman / Stack / Series / Parallel" (no legend), view shows the four figures then "Paused, no CR yet: order add joins one."; nocr-pc-after.png. VERIFIED at 2004e521db9acf1b8d752f0f5b7cb422d7939108. The scratch batch is in parallel mode (open's default), not stack.
9. DESIGN.md section and docs/web-board.md paragraph (git diff origin/main...HEAD): DESIGN.md "A batch with no CR yet" sentence changed and "## The Batch page's title row" added with the five bullets; web-board.md says the legend pill sits in the title row on every tab and names the mode, legend and switch. VERIFIED at 2004e521db9acf1b8d752f0f5b7cb422d7939108.
10. Docs pictures in the head commit (batch-pc, batch-phone opened): title row holds the pills, no band or legend line. Not retaken by me. VERIFIED as shown at 2004e521db9acf1b8d752f0f5b7cb422d7939108.
11. No username or home folder visible in my captures (all opened; the board's served path is replaced by the script's fix routes; the scratch batch shows only "ncr"). Docs pictures opened: none either.
12. PR description as posted (gh pr view 408 --json body, headRefOid 2004e521db9acf1b8d752f0f5b7cb422d7939108): NOT VERIFIED. It is the draft: it says "Before/after pictures: UNVERIFIED: not yet attached" and "The docs screenshots are not retaken yet", but the head commit retook five Batch pictures (batch-cards-pc, batch-gantt-pc, batch-pc, batch-phone, panel-pc); no pictures or measurements are in Deliverables; no SHA on proofs; the Test plan boxes and the Review box are empty; Changes lists no docs/web-board PNGs. The Driver rewrites it from evidence/ and a description-only pass follows.

Notes: just docs-screenshots run by mistake in the worktree changed unrelated PNGs on this machine (rendering variance); restored with git checkout -- docs/web-board, tree clean. Detached before-worktree and scratch folders removed.

Verdict (first pass): NOT VERIFIED (claim 12 only; claims 1 to 11 VERIFIED).

## Description-only pass, head 2004e521db9acf1b8d752f0f5b7cb422d7939108

Claims 1 to 11: carried from 2004e52 (same head, code unchanged).

13. PR description as posted (gh pr view 408 --json body), compared with work/pr-body.md by diff: identical except the seven image links (now user-attachments URLs, one per picture, same files as evidence/) and one trailing blank line. Sections present, fold (details) closed properly, SHAs on proofs (33d1045 / 2004e52), Internal references only inside the fold, measures (353 to 263, 143, 155 to 176, 375) match measure-*.json and before-after.md, Known gaps true, Review box cb58d84 matches the Driver note "approved at 33d1045..., committed as cb58d84f". Defect: Changes did not list the five retaken docs/web-board PNGs that git diff --stat main...HEAD shows (batch-cards-pc, batch-gantt-pc, batch-pc, batch-phone, panel-pc): a delivered change unmentioned. NOT VERIFIED at 2004e521db9acf1b8d752f0f5b7cb422d7939108. Fixed in work/pr-body.md (one Changes bullet added); the Driver reposts it (with the same image URLs) and a new description pass follows.

Verdict: NOT VERIFIED (claim 13).

## Second description-only pass, head 2004e521db9acf1b8d752f0f5b7cb422d7939108

Claims 1 to 11: carried from 2004e52 (same head, code unchanged).

14. PR description as posted (gh pr view 408 --repo gsemet/chantier --json body), diffed against work/pr-body.md: only the seven image links differ (user-attachments URLs, same pictures as evidence/) and a trailing blank line. The Changes now has the `docs/web-board/*.png` bullet naming the five retaken pictures, matching git diff --stat main...HEAD. All seven image URLs return 200 image/png (curl). Sections, fold, SHAs, Known gaps, Review box as judged in claim 13. VERIFIED at 2004e521db9acf1b8d752f0f5b7cb422d7939108.

Verdict: VERIFIED (claims 1 to 11 carried, 13 fixed, 14).
