# Verify: CR-440 Triage fold and writes-count explanation

Head: cdee6c829fd64e6de14eebca97fee8ab9c095518

## Restack pass at cdee6c82 (move 83b3a9a0 -> cdee6c82: restack onto CR-435 local head 8d7ebd66)

- Move: `git range-diff d95695b7..83b3a9a0 8d7ebd66..HEAD` prints `1: 6ab301bb ! 1: 6d7c42d2` (only context hunks differ: the DESIGN.md and test_board_design.py neighbours changed, the CR's added lines are the same) and `2: 83b3a9a0 = 2: cdee6c82`. The base changed under the proof (`git diff --stat 8d7ebd66 HEAD`: 17 files, all the CR's; `git diff --name-only d95695b7 8d7ebd66`: dashboard, board api, cards, web client), so proofs are run again.
- Tests at cdee6c82: `uv run --no-sync --project . python -m pytest -p no:cacheprovider -q skills/chantier/scripts/cli/tests/test_board_design.py skills/chantier/scripts/cli/tests/test_code_targets.py` -> `43 passed in 2.90s`; `git status --short` clean.
- Browser steps 1-14 at cdee6c82: `uv run --script work/verifier/browser_verify.py` (worktree code), steps 1 to 14 each print PASS (step 10 `'P9,,{x'` -> none folded, `'P1,P4'` -> P1 and P4; step 11 panel order B, P.note x3, UL, DIV.row; step 13 `--nav-height=36px`, scrollWidth 366 = clientWidth; step 14 count 4 -> 0), no page error (asyncio Proactor connection-reset noise on Windows at teardown only). Measured values equal those at 83b3a9a0 and 9b22d874.
- Retaken doc image `docs/web-board/triage-pc.png` at cdee6c82 opened and looked at: Triage page with the Kanban tab in the nav, fold chevrons (open) ahead of the P1 and P2 chips, made-up project `shop-api`, no username, no home folder. Shows its claim. `triage-phone.png`, `triage-selection-phone.png` not opened (same retake, carried from 83b3a9a0 look).
- PR body (work/pr-body.md): beyond the stale SHAs, Summary, Deliverables, Changes and Known gaps match the diff (same 17-file CR patch; Known gaps long-line facts carried from 9b22d874, `column.js` lines unchanged by the move per range-diff). Not found wrong.

VERIFIED

---

## Previous judgment (head 83b3a9a0, kept for reference)

## Delta pass at 83b3a9a0 (move 9b22d874 -> 83b3a9a0: restack onto CR-435 d95695b7, conflicts resolved, 2 PNGs retaken)

- Move: `git range-diff 34841dc8~1..9b22d874 d95695b7..83b3a9a0` prints `1: 34841dc8 = 1: 6ab301bb` and `2: 9b22d874 = 2: 83b3a9a0`: both CR commits' textual patches are equal; commit 2 differs only by its binary PNGs (`docs/web-board/triage-pc.png`, `triage-phone.png`, `triage-selection-phone.png`, retaken). The base changed under the proof (`git diff --stat 9b22d874 83b3a9a0`: 99 files, board server, watcher, tests), so the proofs are run again, not carried.
- Checks the spec lists, at 83b3a9a0: `uv run --no-sync --project . python -m pytest -p no:cacheprovider -q skills/chantier/scripts/cli/tests/test_board_design.py skills/chantier/scripts/cli/tests/test_code_targets.py` -> `42 passed in 4.07s`; `git status --short` clean.
- Browser steps 1-14, at 83b3a9a0: `uv run --script work/verifier/browser_verify.py` (same script, worktree code, demo surface in `work/scratch/v`): steps 1 to 14 each print PASS (step 2 chevron `matrix(0, -1, 1, 0, 0, 0)`, count 2->2; step 6 drops land and the row stays folded; step 10 `'P9,,{x'` -> none folded, `'P1,P4'` -> P1 and P4; steps 11/12 panel and tooltip in both languages; step 13 `--nav-height=36px`, no overflow; step 14 count 4 -> 0), no page error. Measured values equal those recorded at 9b22d874 below. Screenshots rewritten to `work/verifier/evidence/`.
- Retaken doc images at 83b3a9a0: `docs/web-board/triage-pc.png` and `triage-phone.png` opened and looked at: Triage page, fold chevrons ahead of the P1 and P2 chips (open, pointing down), made-up project `shop-api`, no username and no home folder visible; they show the fold chevrons the commit claims. `triage-selection-phone.png` not opened (changed by 262 bytes, same retake).
- PR #410 as posted: `gh pr view 410 --json headRefOid` = 83b3a9a0367a8bb83abab0b7a034025f2814fea9, draft. Its body is NOT refreshed: it still says "Screenshots at 9b22d87", "Local gates at 9b22d87", "Review/Verified/CI green at 9b22d87"; `gh pr checks 410` reports no checks yet at this head; `chantier log 440` shows a `ship` event with `no long gate passed at 83b3a9a`. The description is not judged clean here: the Driver refreshes it, then a description pass follows.

Verdict for the behaviour at 83b3a9a0: VERIFIED. Description at 83b3a9a0: not passed (stale SHAs; gate, review and CI not yet at this head).

VERIFIED

---

## Previous judgment (head 9b22d87490cbedbbc31b797543989ca79cc396c3, kept for reference)

All claims below are judged at 9b22d874 (full SHA above), the worktree head, with the worktree's own code (`uv run --no-sync --project <worktree> chantier board`, via `scripts/docs_screenshots.py`'s `make_surface`/`start_board` helpers, imported, not run: no tracked file written). Demo surface = a copy of `docs/demo/` in a scratch folder (own git repo, own bare origin), plus two seeds: `P2/returns-policy` (a copy of P1/stock-alerts, so P2 holds two loose post-its) and the mark file `work/running-batch` (`batch-03`) in P2/saved-addresses (a CR marked for the running batch, drawn in "Running batch"). Chromium via Playwright, PC 1400x860 (English; the language toggled to French for step 12) and phone 390x844 (is_mobile, touch). The earlier head f97eb39 is the same patch before a clean rebase; it is not carried, everything is run at 9b22d874.

Reproduce: `uv run --script work/verifier/browser_verify.py` (raw output `work/verifier/browser-run.log`).

## Checks the spec lists (command run in the worktree at 9b22d874)

Command: `uv run --no-sync --project . python -m pytest -p no:cacheprovider -q skills/chantier/scripts/cli/tests/test_board_design.py skills/chantier/scripts/cli/tests/test_code_targets.py`
Output: `42 passed in 2.71s` (includes the guard test on shipped text and the 300-line and word-key checks). `git status --short` after: clean.

## In a browser (steps 1-14, 9b22d874)

Each line is the script's own output for the step: PASS/FAIL then the measured values.

```text
step 1: PASS [('P1', 'true', 'Hide the P1 post-its', 'none'), ('P2', 'true', 'Hide the P2 post-its', 'none'), ('P3', 'true', 'Hide the P3 post-its', 'none'), ('P4', 'true', 'Hide the P4 post-its', 'none')]
step 2: PASS folded=['P2'] body display=none visible postits=0 aria-expanded=false label='Show the P2 post-its' svg transform=matrix(0, -1, 1, 0, 0, 0) count 2->2 head html before='<button type="button" class="column-fold" data-key="fold-P2" aria-expanded="true" aria-label="Hide the P2 post-its"><svg class="svgi" viewBox="0 0 24 24" aria-hidden="true"><path d="m7 10 5 5 5-5"></path></svg></button><span class="tag pri-P2">P2</span><span class="column-count">2</span><span class=' after='<button type="button" class="column-fold" data-key="fold-P2" aria-expanded="false" aria-label="Show the P2 post-its"><svg class="svgi" viewBox="0 0 24 24" aria-hidden="true"><path d="m7 10 5 5 5-5"></path></svg></button><span class="tag pri-P2">P2</span><span class="column-count">2</span><span class'
step 3: PASS stored='P2' after reload=['P2'] mobile-app triage=['P2'] back=['P2']
step 4: PASS after Enter=([], 'fold-P2') after Space=(['P2'], 'fold-P2')
step 5: PASS a: P2 postits=2 bar before=(1, ['2 selected']) bar after fold=0 picked after reopen=0; b: running postits=1 loose P2=2 bar before fold=['2 selected'] after fold=['1 selected'] marked CR (saved-addresses, in Running batch) still selected=1
step 6: PASS post-it guest-checkout P1->P2 head: lit while over=['P2']; P2 count 2->3; folded=['P2']; group api-hardening (1) from inbox onto P2: over=['P2'] count 3->4 folded=['P2']
step 7: PASS archive-old-orders P4->P2 via selbar: P2 count 4->5 folded=['P2']
step 8: PASS filter=checkout: folded P2 head=('1', ['P2', '1', '1']); opened P2 head=('1', ['P2', '1', '1']); visible post-its 1; folded-state heads of all rows={'P1': ('0', ['P1', '0']), 'P2': ('1', ['P2', '1', '1']), 'P3': ('0', ['P3', '0']), 'P4': ('0', ['P4', '0'])}
step 9: PASS P3 empty=True empty text='empty: drop a post-it here'; fold -> (['P3'], ('false', 'column-lane column-empty column-folded')) (an empty row already hides its body: CSS .column-empty); open -> ([], ('true', 'column-lane column-empty')); write into folded P3 (drop from P1): over=['P3'] count 0->1, folded=['P3']
step 10: PASS 'P9,,{x' -> folded=[]; 'P1,P4' -> folded=['P1', 'P4']; page errors=[]
step 11: PASS tooltip(title)='Changes saved by this board since your last ‘rescan’: open to see them and what to tell the Chief of Staff.'; panel children order=['B', 'P.note', 'P.note', 'P.note', 'UL', 'DIV.row']; paragraphs=['What it counts: the changes made from this board (for example moves, new ideas, labels, groups) since you last pressed the button below. Each one is already saved in the planning folder on this machine.', 'Why tell the Chief of Staff: the board never sends it a message. A Chief of Staff session whose watcher (or pull path) runs learns of these changes by itself; one running neither does not.', 'What to do: type ‘rescan’ in the Chief of Staff’s chat; it reads the backlog again and says what moved. Then press the button below to count again from zero.']; entries=['10:30\nguest-checkout: priority P1 → P2', '10:30\nrate-limit-public-api → P2', '10:30\narchive-old-orders: priority P4 → P2', '10:30\nstock-alerts: priority P1 → P3']
step 12: PASS html lang=fr; paragraphs=['Ce que ça compte : les changements faits depuis ce board (par exemple déplacements, nouvelles idées, labels, groupes) depuis la dernière fois que tu as appuyé sur le bouton ci-dessous. Chacun est déjà enregistré dans le dossier de planification sur cette machine.', 'Pourquoi le dire au Chief of Staff : le board ne lui envoie jamais de message. Une session Chief of Staff dont le watcher (ou le chemin de lecture) tourne apprend ces changements toute seule ; une session qui ne fait tourner ni l’un ni l’autre ne les connaît pas.', 'Quoi faire : tape « rescan » dans le chat du Chief of Staff ; il relit le backlog et dit ce qui a bougé. Puis appuie sur le bouton ci-dessous pour recompter à partir de zéro.']; tooltip='Changements enregistrés par ce board depuis ton dernier « rescan » : ouvre pour les voir et savoir quoi dire au Chief of Staff.'; chevron labels={'P1': 'Afficher les post-its de P1', 'P2': 'Masquer les post-its de P2', 'P3': 'Masquer les post-its de P3', 'P4': 'Afficher les post-its de P4'}
step 13: PASS --nav-height=36px (36px); head height=36px; tap folds=['P2'], tap opens=[], tap folds again=['P2'], then P4 folded; panel scrollWidth/clientWidth/viewport/doc=[366, 366, 390, 390]; page errors=[]
step 14: PASS button before='✎ 4 writes since your last ‘rescan’' after='✎ 0 writes since your last ‘rescan’'; toast=['', '● In preparation: 2 CRs in 3-ready', 'Counted from now on.']; home lines=['Written by the board', 'nothing since your last ‘rescan’']
```

Notes on the steps:
- Step 2: the chevron svg transform `matrix(0, -1, 1, 0, 0, 0)` is the -90deg rotation (right-pointing); open rows read `none` (down). The head keeps chip, count (2 before and after) and grill-state counts; the body is `display: none`.
- Step 5: part a was run with two loose P2 post-its selected (bar "2 selected"), fold -> no bar, reopen -> none picked. Part b: one loose P2 post-it plus the marked CR in "Running batch" ("2 selected"), fold -> bar stays with "1 selected", the marked CR still selected.
- Step 6: the head lit (`.column-lane.over` = P2) during the drag; the post-it (guest-checkout) and a group dragged by its handle (api-hardening, from the inbox) both landed in P2 and P2 stayed folded; the count went up each time (post-it 2->3; group of 1, 3->4).
- Step 9: demo P3 is empty; an empty row already hides its body by `.column-empty` (CSS, unchanged), so fold is shown by `column-folded`, `aria-expanded` and the chevron; a write into folded P3 (a drop from P1) raised its count 0->1 and left it folded.
- Step 11/12: the native tooltip cannot be screenshotted; the button's `title` attribute is shown in the step's output and equals `journal.tip` in both languages. Panel children order is B, P.note x3, UL, DIV.row: no note at the bottom.
- Step 13: head height 36px equals `--nav-height` (36px); tap folds and opens; panel `scrollWidth` equals `clientWidth` (366), no horizontal overflow.
- Step 14: count 4 -> 0, toast "Counted from now on.", Home tile reads "nothing since your last ‘rescan’".

## Screenshots (opened and looked at, 9b22d874; paths on screen are made-up or absent, no username or home folder visible in any)

- Step 2: `evidence/triage-folded-p2-pc-en.png`: Triage at PC, English, P2 folded (chevron right, chip P2, count 2, grill count), P1, P3 and P4 open with chevrons down. Shows its claim.
- Step 11: `evidence/journal-panel-pc-en.png`: panel open, heading, three note lines, list of 4 entries, buttons, no bottom note (P1 and P4 folded from step 10 behind it). Shows its claim.
- Step 12: `evidence/journal-panel-pc-fr.png`: the same panel in French with "tu" ("tu as appuyé", "tape", "appuie"). Shows its claim.
- Step 13: `evidence/triage-folded-phone.png`: 390 px, Backlog column scrolled into view, P2 and P4 folded with their counts, P1 and P3 open (P3 holds stock-alerts, from step 9). Shows its claim.
- Extra: `evidence/journal-panel-phone.png`: the panel at 390 px, text wraps and reads whole (shows "nothing" in the list since the phone context had no entries after step 14's rescan).

## PR description pass (#410 as posted, judged at 9b22d874)

- `gh pr view 410 --json headRefOid` = 9b22d87490cbedbbc31b797543989ca79cc396c3. Sections, order, fold (blank lines, nothing after `</details>`), Internal references only in the fold: in place.
- Images: `curl -sL -w "%{http_code} %{content_type}"` on the four user-attachments URLs: 200 image/png each (223675, 211148, 215699, 58497 bytes). Their content matches the four captures looked at above (no username, no home folder).
- Test plan: `gh pr checks 410`: 5 checks pass (check x3, eval-dry-run, scenario); `chantier log 440`: gate pass at 9b22d874, inspector approved at 9b22d874 (note 00:32:28Z), verdict VERIFIED at 9b22d874; test `test_the_fold_and_the_writes_count_explanation_ship` exists (test_board_design.py:365). Browser steps and 42 tests: proved above.
- "Chief of Staff" is a product term here (the board's text names it), defined on first use: accepted.
- FAIL, Known gaps incomplete: it names only "a header comment in `js/ui/column.js` (line 9)" over 100 characters. `git diff de120311 HEAD -U0 -- .../js/ui/column.js | grep '^+' | awk 'length>101'` shows four added lines over 100: the `fold` comment (line 9, 104), the "A lane has no dot..." comment (line 10, 120, the longest), and two code lines (the fold button template and the section template, 155 and 235 chars). The bullet leaves out line 10 and the code lines.

## Verdict

NOT VERIFIED (description only: Known gaps incomplete; the browser and test claims at 9b22d874 stay as proved above)

## Description pass (head 9b22d874)

Command: gh pr view 410 --json body. Sections, fold, four images at 9b22d87, Internal references only in its section: ok. Known gaps long-line fact checked with `git diff -U0 <base>...HEAD` length scan on js/ui/column.js: added lines 9 (104) and 10 (120), template lines 155 and 235: matches the description.

VERIFIED
Head: ca0032cbdb9613ddca52229fb986b6ca687600b4

## Light re-verify after restack onto e2f8fdc1 (judged at ca0032cb)

- CR's own patch unchanged: for both CR commits (6d7c42d2 -> 05089f6f, cdee6c82 -> ca0032cb) `diff <(git show -U0 --format= OLD -- . ':!*.png' | grep -E '^[+-][^+-]') <(same NEW)` printed no difference ("same-nonpng"). `git range-diff` marks commit 2 `!` only for hunk context lines of docs/web-board.md and DESIGN.md (base moved by CR-435).
- Pictures are the CR's: `git diff --stat cdee6c82 ca0032cb -- 'docs/web-board/triage*.png'` is empty (the three Triage pictures byte-identical to the old head); the other pictures come from e2f8fdc1 (base retake).
- Targeted check: `pytest tests/test_board_design.py -q` -> 38 passed.
- Carried from 9b22d874/cdee6c8: browser steps, screenshots, test claims (the patch is unchanged). Description pass and Known gaps: carried; the pushed head will differ by SHA only.
- Gate/CI at the new head not run by me (no `just scenario`, per brief).

VERIFIED
