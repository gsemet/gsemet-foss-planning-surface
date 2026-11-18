# Verify CR-326

Head: de0993f5467543bc9b025c96b98ed833e608e906

Judged at de0993f (all below). Before = 33a2305 (merge base; origin/main is now a111e18).

1. Kanban bounded, scrollbar in the window, columns scroll alone (de0993f). Command: `uv run --script work/verifier/shots.py <worktree> ... after` (after.log). 1280x800: `boardBottom 776, winH 800, mainSH 800 = mainCH 800, docSH 800, boardSW 2102 > boardCW 968`, columns overflow-y auto with scrollHeight 744/723/950 > clientHeight 569 (bounded). Before (33a2305, before.log): `boardBottom 1151, mainSH 1175 > mainCH 800` (the bug). Phone 390x800 after: `boardBottom 726, mainSH 800, snap "x mandatory"`, one column per width (screenshot kanban-phone.png). The overlay scrollbar itself is not drawn in headless captures: proven by measured sizes only.
2. Priority chips and left borders (de0993f): kanban-pc.png shows P1-P4 chips dark to pale teal and 3px left borders on the Backlog and Grill cards; Inbox cards have none. Triage computed border-left (after.log): guest-checkout/stock-alerts rgb(29,92,99) 3px, saved-addresses/product-reviews rgb(74,126,131), cold-storage-tiering rgb(136,172,176), archive-old-orders rgb(207,226,227); the selected card (stock-alerts, sel=true) keeps rgb(29,92,99) 3px; inbox and 3-ready cards 1px grey. Before: all 1px rgb(235,236,239).
3. Column headers one tint, dots unchanged (de0993f): after.log `colh` seven times rgb(233,241,241) (= --accent-tint #e9f1f1); before transparent. kanban-pc.png dots grey as before.
4. Panels: panel-item-pc.png (P1 chip in head, no left border, as the PR says); panel-pc.png (CR-145 "working" chip on a blue tint).
5. Costs figure cards (costs-pc.png): four teal-tint cards. Batch view (batch-pc.png): tinted merged/PR in draft/working/waits badges, "working" breadcrumb chip on tint. Sidebar tint, active-row tint and project mark: kanban/costs/project screenshots. All projects: three marks D, M, S on their tints (all-projects-pc.png) (the demo has three projects, not six).
6. `--state-*` values unchanged (de0993f). Command: `git diff 33a2305 HEAD -- skills/chantier/scripts/cli/src/chantier/board/web/css/tokens.css | grep -E '^[-+]\s*--state-[a-z]+:'` -> empty output. Only the comment line changed and tint tokens were added.
7. Contrast and marks, own computation (work/verifier/contrast.py, contrast.log): P1 7.6, P2 4.56, P3 4.84, P4 8.83, nav 10.34, marks 0-5 letters 5.34, 4.84, 4.77, 5.21, 4.66, 4.63: all >= 4.5, equal to work/r1-tables.md. Mark hues vs nearest state: 321.1/blocked 30.4, 195.3/working 26.3, 102.0/merged 50.2, 283.6/local 26.0, 64.0/waits 27.7, 176.0/ready 23.5 (mark 5 unmoved, hue kept, spec only requires 0,1,3,4 and 2 if judged; 23.5 is under 25 and is declared in the PR as an autonomous decision). None equals a --pri value.
8. Other views still scroll (de0993f): after.log `home` main scrollHeight 1350 > clientHeight 800, overflowY auto; `config` 2865 > 800 auto; same as before.
9. Tests: `uv run --no-sync pytest skills/chantier/scripts/cli/tests/test_code_targets.py -q` -> `5 passed in 1.79s`. CI at the head (`gh pr view 284`): just check on ubuntu, macos, windows, just scenario (ubuntu-latest) and eval-dry-run all SUCCESS.
10. Screenshots: opened each; they show the claimed screens, made-up paths (/home/demo/...), no username. Files in work/verifier/evidence/{before,after}, listed in before-after.md.

Open items for the Driver (not a code failure): the PR description still says "Screenshots ... to be attached" and its Test plan holds the `<sha7>` placeholders; the screenshots must be attached with the 7-char SHA before handback, and the description is judged again then. The base moved (origin/main a111e18 touches Configuration-page files and plugin_files/edit.py, not the CR's files); a rebase would be a move.

VERIFIED

## Description pass (PR 284 body as posted)

Head: de0993f5467543bc9b025c96b98ed833e608e906

Judged at de0993f (`gh pr view 284 --json body,headRefOid`; headRefOid = de0993f). Description-only; no code move since the VERIFIED above.
- Summary, Deliverables and Changes against `git diff --stat origin/main...HEAD`: 15 files (14 css/js/docs paths + docs/web-board.md), exactly those named (shell.css, kanban.css, tokens.css, tags.css, cards.css, item-card.js, parts.js, header.js, crumbs.css, batch-graph.css, components.css, costs.css, sidebar.css, picker.css, web-board.md); three JS files = "three small JS class additions". No unmentioned change.
- `git diff origin/main -- css/tokens.css | grep -E '^[+-]\s*--state-[a-z]+:'` -> empty output; claim holds.
- Docs: `git diff 33a2305 HEAD -- docs/web-board.md` shows one sentence added each for Kanban and Triage; holds.
- Tables (marks, contrast) equal my own computation in item 7 above (carried from the first pass, same head).
- Images: downloaded all 9 attached URLs (all HTTP 200 image/png, so they resolve); opened each. Kanban before/after (1280x800), phone (390x800), Triage with selected P1 card, item panel, CR panel, Costs, Batch, All projects each show the claimed state and captions match; paths on screen are made-up (/home/demo/planning-surface, shop-api); no username or home folder anywhere.
- Test plan: `gh pr checks 284`: just check macos/ubuntu/windows, eval-dry-run, scenario (ubuntu) all pass; Review box: log note "r1 approved at de0993f... committed as de0993f" matches; the "443 tests" figure is the Coder's local gate in work/coder/r1.md (CI at the head also green).
- Known gaps: two bullets (hand-built state chips; overlay scrollbar), matching item 1 and the Home rows; no UNVERIFIED claim, no failed-and-accepted claim missing. No STALE mark. Role names only in Internal references path list. Details fold renders (details/summary).

VERIFIED
