Head: a2a083af9e92e5949c683fae754752999b542618

All claims judged at a2a083af (the pushed head), by a Playwright run (Chromium, 1600x900 with the PR column, demo project shop-api, board started from this worktree on a demo copy, clock fixed). Raw data: verifier/evidence/after.json and before.json (before = base dce2c644, detached worktree, removed). Script: verifier/probe.py.txt.

1. Transitive reduction. `after.json` folded.edges = CR-142>CR-143, CR-143>CR-145, CR-144>CR-147, CR-145>CR-148, CR-146>CR-148; to148 = 2, all = 5 (before at dce2c644: to148 = 3, all = 6). No redundant edge CR-142/CR-143/CR-141 into CR-148. PASS.
2. Fold. folded: n141 = 0, chip "1 merged", aria-expanded "false", title "Show the merged CRs in their levels". Click: unfolded n141 = 1, to148 = 3, aria-expanded "true", title "Fold the merged CRs". Click again: refolded equals folded (sh 518, svg 518). PASS.
3. Keyboard. After reload, focus on the chip, Enter: aria-expanded "true"; Space: "false". PASS.
4. Order. folded order [CR-142, CR-146, CR-144, CR-149], [CR-143, CR-147], [CR-145], [CR-148], as the spec names; reload_order identical. PASS.
5. Fit. folded gscroll sw 886 = cw 886, sh 518 = ch 518, both SVG layers 518; unfolded 661 / 661; refolded back to 518 (before: sw 1502 > cw 886, scrolled). PASS.
6. Hover CR-148. Picture after-desktop-hover.png: cards 142, 143, 145, 146 lit, top layer has 2 lit paths (CR-145, CR-146) and 1 head; count reads 5 with title "Waits for CR-141, CR-142, CR-143, CR-145, CR-146". PASS.
7. Closed record (mobile-app batch-01). nchip 0, 2 nodes drawn, as before. PASS.
8. Phone 375: pagew [375, 375] (page does not scroll sideways), graph box scrolls inside (sw 1182 > cw 383), chip present. PASS.
9. Docs picture docs/web-board/batch-graph-pc.png (opened): 1400x860 graph with the chip "1 merged", reduced arrows, four levels scrolling inside the box as the spec says; no username or home folder shown (path "shop-api" only). My captures were opened too: they show the same, no username or home path. PASS.
10. Test: `uv run --no-sync python -m pytest tests/test_board_graph_arrows.py -q` -> 3 passed. CI at a2a083af (`gh pr view 431`): check x3, scenario (ubuntu), eval-dry-run all SUCCESS. PASS.
11. PR description (gh pr view 431, body equals work/pr-body.md but for one trailing blank line): renders, Summary/Deliverables/Changes match `git diff --stat dce2c644 HEAD` (13 files, the same list), image URL pinned at a2a083af and the file is in that commit, Known gaps lists the missing before picture (now captured here), the badge clip at 1400-1600 and the local scenario. Review box: notes in `log` show approved at dce2c644, 1c3a4ef7/d5ef37f3 and r3 inspector approved at d5ef37f3 (the lint round that became a2a083a); no note names a2a083a itself, accepted because the box cites d5ef37f3 and the lint diff is a format-only change (CI green). No role name misuse found. PASS.

Known: state badges clip at the card edge at 1600 wide (visible in after-desktop-folded.png), listed in Known gaps, outside the spec.

VERIFIED
