# Verify CR-344

Head: 03ee16df1fb9ab49ef70e1b1573e71b020c74273

Verdict: VERIFIED (third verification; move 6f63babc..03ee16df, restack with conflicts resolved, base ad5dd947). Earlier judgments (6f63bab) follow below, carried as marked.

## Claims at 03ee16df

1. Tests at 03ee16d. `uv run --no-sync pytest skills/chantier/scripts/cli/tests/test_board_design.py skills/chantier/scripts/cli/tests/test_code_targets.py -q`: `31 passed in 1.05s`. PASS.
2. CI at 03ee16d. `gh pr checks 306`: just check macos/ubuntu/windows, eval-dry-run, scenario (ubuntu-latest) all pass. PASS.
3. PRs page filter chips (css/components/chip.css, resolved from postit.css). Real Chromium 1440x900 on the board served from the worktree (docs demo data, scratch script, `uv run --with playwright`): the 4 `[data-pvf]` and 4 `[data-pvs]` chips have computed `::before` content `none` (all 8 `none`, both projects); clicking the 2nd state chip gives `v=prs&st=open` with `open` on, the 2nd sort chip gives `&sort=opened` with `opened` on. evidence/after-prs-03ee16d.png (looked at: no glyph, no username, no home path; the demo's forge is unreachable, so no PR rows: only the chips and the error line show). PASS.
4. Batch graph cards through the one card component. Same run: 13 `.card` elements in the Batch view, `PR` tag text on 5 cards (`t('pr.tag')`), no page error. evidence/after-batch-03ee16d.png (looked at: nodes and PR column are cards, PR shown; no username/home path). PASS. MR wording on a GitLab forge: NOT PROVED (the demo is GitHub; the i18n key `pr.tag` / `mr.*` path is as in the conflict record, not exercised in a browser).
5. Overview (Home of the surface). Same run: `.overview .note` reads "One line per project of the surface. A click opens the project; a CR link opens the PR to review." (CR-343's shared-forge note, PR wording on GitHub), 3 `.overview .cards .card` (CR-344's projectCard). evidence/after-overview-03ee16d.png (looked at: no username/home path, made-up /home/demo paths). PASS.
6. Kanban (r6 fix holds). Same run: every card in every `.column-body` has clientHeight = scrollHeight (e.g. 150/150, 168/168), none squeezed; evidence/after-kanban-03ee16d.png shows the Inbox cards with their meta band ("2 files / raw"). PASS.
7. Costs (r6 fix holds). Same run on mobile-app: `.ticket .meta` background `rgb(246, 247, 248)` (the band is present). PASS.
8. Review box: carried from 6f63bab; the Driver's note of the move says the Inspector approved the move at 03ee16d (per prompt; `chantier log` not re-read here). Move proof for the description pass is the Driver's: see below.
9. Claims 2, 4, 5 of the second verification (no side border, docs, test fails on base) carried from 6f63bab: the move's patch is unchanged for commits 2 and 3 (range-diff '='); commit 1 changed only by the three conflict resolutions, proved again by claims 1, 3-5 above.
10. PR description: NOT re-judged (prompt asks the code views only); the description pass of 6f63bab stands for text carried; the head changed, so the Driver must keep the test-plan SHAs current. Known gaps of 6f63bab still apply (Copy as image output, stack rail hairline) , carried from 6f63bab.

Scratch: my script and images under work/scratch removed (earlier scratch files of the previous verification remain). Not a username/home leak: error line in after-prs shows 'example/shop-api' only.

VERIFIED

---- Earlier verifications (carried as marked) ----

## Claims

1. Tests green at cd015442. Command: `uv run --no-sync pytest skills/chantier/scripts/cli/tests/test_board_design.py skills/chantier/scripts/cli/tests/test_code_targets.py -q`. Output: `31 passed in 1.03s`. PASS.
2. test_board_design.py fails on the base's code. Copied into a detached worktree of 1690ec4f, same command: `4 failed, 22 passed` (test_token_table, test_sheets, test_components, test_one_card; e.g. `js/views/batch-graph.js: class list 'node card' writes a card class`). PASS.
3. CI at cd015442 (`gh pr checks 306`): just check macos/ubuntu/windows pass, just eval-dry-run pass, just scenario (ubuntu-latest) pass. PASS.
4. No side accent border left. `grep -rnE "border-(left|right|inline)" css | grep -v tokens.css`: panel.css:53 (`border-right: 1px solid var(--line)`), panel.css:221 (`0`), sidebar.css:8 (`1px solid var(--side-line)`), views/batch-prs.css:52 (`border-left: 1px solid var(--line)`). Only allowed separators. PASS.
5. Docs: `git diff 1690ec4f HEAD -- docs/web-board.md` removes "and its card's left border" (line 61) and "and their left border" (line 67); 25 docs/web-board/*.png changed. AGENTS.md line 76 and CONTRIBUTING.md name DESIGN.md. DESIGN.md (283 lines) and css/components/{card,chip,column}.css (184, 257, 118 lines) exist. PASS. (Token table = tokens.css: proved by test_token_table, claim 1.)
6. Review box: log shows `r5 approved at 306f15b9, committed as cd015442`. PASS.
7. Screenshots at cd015442 (before from 1690ec4f), in evidence/ (see evidence/before-after.md): before-/after-triage, kanban, batch, config-timing, costs, home, overview-phone .png. Each opened and looked at: no username or home path. Triage: same column, lanes with chips, check mark after chip, sub-lines: PASS. Batch, Config timing, Home, Overview phone: unchanged: PASS.
8. FAIL: Kanban cards are squeezed in a scrolling column. after-kanban.png: the Inbox column's cards lose their meta band ("2 files / raw"), which before-kanban.png shows. Probe at cd015442 (`.column-body`, overflow auto): card heights 131/131/131/146 while content scrollHeight is 150/150/150/168 and the body's scrollHeight equals its clientHeight (580), so the body never scrolls; the base: cards 152 = content, body overflow visible. Cards shrink (flex-shrink) instead of the body scrolling. The PR's own Autonomous decision ("a Kanban column taller than the page now scrolls its body") is not what happens: the cards are clipped. Fix: cards in `.column-body` must not shrink (`flex: none`).
9. FAIL (unmentioned change): the Costs receipt's header meta box (grey band behind "parallel, foreman / dates / duration") is gone after (before-costs.png vs after-costs.png), and the header rows sit 9 px higher. The receipt is a protected feature and the spec says "receipt unchanged". It looks like the old `.meta` band leaking into `.ticket .meta` was removed, which is probably right, but the PR does not say it. State it in the PR (Autonomous decisions) or restore it.
10. NOT PROVED: the receipt with its stamp on a running batch, and "Copy as image": the only capture (shop-api batch-03) showed the machine's home folder in the receipt's error text and was deleted. Name them in Known gaps. The Batch stack rail hairline was not visible in the demo view.
11. PR description (as posted): clean and consistent with the diff except claim 9 (receipt change unmentioned). It declares "No before/after screenshots yet" in Known gaps, and its Deliverables carry no images: the Driver adds them from evidence/ (images 1-7), made-up paths. Test plan line "[ ] Evidence" and "[ ] Verified" are open (expected).

## Evidence images (CR folder evidence/)

evidence/before-triage.png, after-triage.png, before-kanban.png, after-kanban.png, before-batch.png, after-batch.png, before-config-timing.png, after-config-timing.png, before-costs.png, after-costs.png, before-home.png, after-home.png, before-overview-phone.png, after-overview-phone.png; list and reproduction in evidence/before-after.md. The before worktree and the scratch folders are removed.

## Second verification at 6f63babc5d5b5f7782b0f22d7174ee3cdc4379c9

The move touched css/components/column.css (`.column-body > * { flex: none }`), css/views/costs.css (`.costs .ticket .meta` band restored) and docs/web-board/{costs,kanban,editor}-*.png. Claims 1-3 redone, 8-10 redone, 4-7 carried.

- 1 redone at 6f63bab: same pytest command: `31 passed in 1.04s`. PASS.
- 3 redone at 6f63bab: `gh pr checks 306`: just check macos/ubuntu/windows, eval-dry-run, scenario (ubuntu-latest) all pass. PASS.
- 2, 4, 5 carried from cd01544: the move touched no test, no border rule, no DESIGN.md or docs text (git diff --stat cd015442 HEAD lists only the 2 css files and 5 png).
- 6 Review box: `Review: approved at cd01544`; log: `r6 approved at cd015442, committed as 6f63babc`. PASS.
- 8 FIXED (was FAIL): evidence/after-kanban.png recaptured at 6f63bab (same scratch method, 1440x900, made-up paths): Inbox cards keep their meta band ("2 files / raw") and the column body is cut by the page edge, as it scrolls. Looked at: no username or home folder. PASS.
- 9 FIXED (was FAIL): evidence/after-costs.png recaptured at 6f63bab: the receipt's grey header meta band (parallel, foreman / dates / duration) is back, identical in place to evidence/before-costs.png (base 1690ec4f). Looked at: no username or home folder. PASS.
- 10 partly proved: evidence/after-costs-running.png (shop-api batch-03, running, 6f63bab): the receipt shows its NOT FINISHED stamp, and the "Copy as image" button is present. Paths in the transcript error text rewritten in the DOM to /home/demo/app before the shot (JS replaces any text with gaeta or Users; the check printed no remaining match); looked at: no username or home folder. The stamp's look was not compared to the base (not captured), and the stamp overlaps the demo's error lines (demo data, "Foreman transcript not found"). The "Copy as image" output (the PNG it renders) is NOT PROVED (not run). The Batch stack rail hairline is NOT PROVED: evidence-free in the Batch view (scratch shot at 1440x900 shows the PR column but no stack rail one can tell apart).
- 11 PR description (as posted, 6f63bab): FAIL. Known gaps says only "No before/after screenshots yet", and does not name "Copy as image" and the stack rail hairline as unproved, while line 16 states the hairline as a fact; Deliverables carry no images (evidence/ has them, made-up paths). Driver: add the two Known gaps bullets (or prove them), and attach the images (evidence/after-kanban.png, after-costs.png, after-costs-running.png and the carried ones).

NOT VERIFIED

## Description pass at 6f63babc5d5b5f7782b0f22d7174ee3cdc4379c9 (posted body, gh pr view 306 --json body)

Head: 6f63babc5d5b5f7782b0f22d7174ee3cdc4379c9

Verdict: VERIFIED (description). Code claims 1-10 carried from the second verification at 6f63babc (no commit since).

11. Description. PASS.
- Renders: sections, tables, fold, 15 images resolve (downloaded all user-attachments assets with curl).
- Images attached = images captured: md5 of each downloaded asset equals the matching evidence/ file (before/after triage, kanban, batch, costs, config-timing, home, phone, after-costs-running). Captions and SHAs match before-after.md (after-kanban and after-costs at 6f63bab, others cd01544, before 1690ec4). Costs and Home pairs are byte-identical, as the text says (unchanged).
- Look at triage-after, kanban-after, batch-after, costs-before, costs-running, config-after, home, phone: paths are /home/demo/... only, no username or real home folder.
- Each UNVERIFIED claim has its Known gap: hairline (Deliverables UNVERIFIED, gap 2), Copy as image output (gap 1); before-after.md's two "not proved" items are both in Known gaps.
- Internal references: "CR-344" appears only in Internal references; no other role or CR name.
- Summary, Deliverables, Changes match the diff (carried claims 4, 5). Test plan SHAs 6f63bab.
- Review box: log has "r6 approved at cd015442, committed as 6f63babc" and r6 inspector approved at cd015442; the box cites 6f63bab, the round's committed-as SHA: proved.

## Description pass at 03ee16df1fb9ab49ef70e1b1573e71b020c74273 (posted body, gh pr view 306)

Head: 03ee16df1fb9ab49ef70e1b1573e71b020c74273

- Renders; images resolve: downloaded the four new assets; md5 equals evidence/after-{prs,batch,overview,kanban}-03ee16d.png. PASS.
- Look (opened as images): after-prs, after-batch, after-overview, after-kanban at 03ee16d show only made-up /home/demo paths and 'example/shop-api'; no username or home folder. The earlier images passed the look in the 6f63bab pass; carried. PASS.
- Captions/SHAs: Before 1690ec4; after carried from 6f63bab / cd01544 (same patch; pages touched recaptured at 03ee16d). Test plan: Local gates at 03ee16d `just check` run by me in the worktree: `All checks passed!` `549 passed in 20.11s`. PASS.
- CI at 03ee16d: `gh pr checks 306`: just check macos/ubuntu/windows, eval-dry-run, scenario (ubuntu-latest) all pass. PASS.
- Review box approved at 03ee16d: log `move 6f63bab..03ee16d (conflict) inspector approved at 03ee16df...`. PASS.
- Known gaps: Copy as image, stack rail hairline, MR on GitLab, PRs rows after rebase: each matches an UNVERIFIED claim of verify.md claims 3-4, 10. PASS.
- Internal references only CR-344; no role names elsewhere. Summary/Deliverables/Changes match the diff (claims 1, 9). PASS.

VERIFIED (description)
