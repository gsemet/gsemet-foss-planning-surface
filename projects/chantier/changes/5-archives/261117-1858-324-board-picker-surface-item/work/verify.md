# Verification of CR-324

Head: 18d82a0e26550d7eda4028fac290702ef76ea440

All claims judged at 18d82a0 (`git rev-parse HEAD` in the worktree), in real Chromium (Playwright) against `chantier board` of the worktree's code on a copy of docs/demo (3 projects, scratch folder, removed at the end). Script: `work/verifier/check.py`; raw output `work/verifier/after.log` (head) and `before.log` (base 33a2305).

1. Click on surface header from any page opens overview (spec step 1). Output (after.log): from costs, triage, kanban, batch, prs, config, home each: `?p=shop-api&v=<view> -> ?p=*&v=home`. Before (base): the same clicks from the six non-home views leave the address unchanged (the bug); from home -> `?p=*&v=home`.
2. Back returns to the page left (step 2): after.log `back: ?p=shop-api&v=costs` (and each other view).
3. On overview, header has `row sfc on` and one `.ok` mark; picking mobile-app gives `?p=mobile-app&v=home`, and row `mobile-app` is `row on` with ok=1 (step 3).
4. Menu order and look (step 4): menu children `BUTTON.row sfc, DIV.sep, BUTTON.row...`, no `.cap`; header text `planning-surface / overview · 3 projects`; computed weights header 500, projects 400; padding-left 8px vs 16px; FR header `vue d'ensemble · 3 projets`. Screenshots after-picker-pc.png and after-picker-phone.png opened and checked.
5. Unchanged (step 5): typed `?p=*&v=costs` -> `?p=shop-api&v=costs`, reload same; bare address after choosing surface on Home -> `?p=*&v=home`. Same output at base.
6. Single-project surface shows no menu: NOT RUN in the browser (only the 3-project demo was served); the diff leaves `canPick` and the `menu()` guard `!canPick(state)` unchanged (picker.js, read at 18d82a0). Not a gate on its own.
7. Screenshots: four images in work/verifier/evidence/, no username or home folder visible (opened and looked at; first Costs-page captures showed the home path and were discarded and retaken on Kanban).
8. CI: PR 282 five jobs green incl. just scenario ubuntu, as stated in the prompt (not re-run by me).

VERIFIED

## Description pass (posted body, head 18d82a0e26550d7eda4028fac290702ef76ea440)

- `gh pr view` headRefOid = 18d82a0e26550d7eda4028fac290702ef76ea440; body read against `git diff origin/main` (6 files): Changes, Deliverables, Impacts match; docs/web-board.md, i18n key, CSS and click handler all in the diff and in the body.
- Sections in template order, fold in place with blank lines, Known gaps present (step 6 gap matches claim 6 above); no internal reference outside Internal references.
- Images: the four user-attachments URLs return 200 and their md5 equal the four files in work/verifier/evidence/ (before/after, PC/phone), already looked at above: no username or home folder. SHAs in captions: base 33a2305 (merge-base), after 18d82a0.
- Review box: `chantier log` note "r1 approved at 33a2305, committed as 18d82a0" cites the committed-as SHA.

VERIFIED (description, at 18d82a0)
