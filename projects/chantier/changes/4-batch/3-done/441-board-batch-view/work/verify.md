# CR-441 verify

Head: 91b2c1f4a8ddd4fc2a3d5be3bcbe88776cf193e7

All browser claims below were judged at 819b848 by my own run: `work/scratch/vrun.py` (Playwright on the
worktree's demo, served by `docs_screenshots.py`'s own server, scratch under `work/scratch/vw`, removed).
Command: `uv run work/scratch/vrun.py <worktree> work/scratch work/verifier/evidence`; raw output
`work/verifier/vrun.log`; pictures `work/verifier/evidence/v-*.png` (made-up demo data, no username or home path).

## Claims

1. One head into CR-148, tip on the middle of its left edge (819b848). Output:
   `heads, arrows in base: [4, 6]`; `elements with marker-end in graph svgs: 0`;
   `end [1186, 87.59375]`, `nh: 1`, head `d = M1178,83.59375 L1186,87.59375 L1178,91.59375 z` (tip dx 0, dy 0;
   8 long, 8 tall). PROVED.
2. The three arrows into CR-148 (from CR-141, CR-145, CR-146) end at that point (819b848): their `d` all end
   `L1186,87.59375`, equal to `end`. PROVED.
3. Top layer on hover of CR-148 (819b848): arrows `CR-141>CR-148`, `CR-145>CR-148`, `CR-146>CR-148`, one head,
   stroke and fill `rgb(29, 92, 99)`, head stroke `none`; top layer z-index 2 over `.lvl` 1, pointer-events none;
   base layer keeps its lit/dim classes (hl 4, dim 6). Unlit: top layer children 0. PROVED.
4. Keyboard focus (819b848): focus on CR-146 gives top `['CR-146>CR-148', 'head CR-148']`; CR-145 gives its
   in and out arrows and both heads; CR-141 gives `CR-141>CR-148`. Picture `v-after-cr146-focus.png`
   (and the Driver's `evidence/after-graph-cr148-hovered-arrows-from-cr141-and-cr146-over-the-cards.png`, opened:
   lit arrow drawn over the CR-145 card and across the dimmed cards). PROVED. Note: the pictures crop the graph
   at 330 px scroll, so CR-148's head itself is outside them; the head is proved by claims 1 and 3.
5. Tooltips (819b848), en and fr, tip inside the viewport (iw 1400): en stack `This batch's mode.` right 1243.0;
   en series `To switch, ask the Chief of Staff to "change the batch to series"` right 1302.6; en parallel right 1368;
   fr stack `Le mode de ce batch.` right 1242.4; fr series
   `Pour changer, demande au Chief of Staff : « passe le batch en série »` right 1295.6; fr parallel right 1368.
   Left edges all > 0. Keyboard focus on a mode word shows its tip (`True`). Series word has `tabindex 0`,
   `aria-describedby mstip-series`. Pictures `v-tip-*-{en,fr}.png` (fr series opened and read: legible, inside). PROVED.
6. Click on Series changes nothing (819b848): `click Series unchanged (url, text, batch.json): True True True`. PROVED.
7. Closed batch (mobile-app batch-01) (819b848): `closed: words 3 [None, None, None] [None, None, None] tips 0`;
   `v-closed.png` opened: no tooltip after hover. PROVED. (`top layer: 1`: the closed graph holds the second layer, as spec section 2 says.)
8. 375 px (819b848): `phone: none 1 [375, 375, 375]` (switch hidden, one head, no horizontal scroll). PROVED.
9. Gantt unchanged: `git diff <base>...HEAD -- .../js/views/batch-gantt.js` prints nothing. PROVED.
10. Tests (819b848): `pytest test_board_graph_arrows.py test_board_design.py` gives `39 passed`. The spec put the test in
    `test_board_design.py`; the Driver used a new file for the line limit and says so in Autonomous decisions: accepted.
11. Gate: `work/gates/20261122-023135.log` first line `gate CR-441 branch chantier/batch-30/cr-441-... head 819b8480171ae1c830874d22dd41025d83e298a0`;
    `$CHANTIER log`: `gate result=pass head=819b8480... command=just scenario`, `just check` and `just eval-dry-run` pass at 819b848,
    CI green (5 checks) at 819b848 (Driver's notes; CI not re-read by me).
12. Review box: `$CHANTIER log` shows `r1 approved at 9b22d87490cb..., committed as 819b8480`; the box is still the
    placeholder `<sha7>` in the PR, to fill with 819b848 / 9b22d87 as the checklist requires.

## PR description (posted body, read with `gh pr view 415`)

- Renders: sections, details fold, five images with `github.com/user-attachments` URLs (not relative paths). I opened the
  Driver's before/after hovered files and the tooltip files: they show the claim (lit arrows over cards; fr tip legible);
  no username or home path on screen. PASS.
- Matches the diff: files and the pictures list match `git diff --stat` (batch-cards-pc, batch-gantt-pc, batch-graph-pc, batch-pc,
  batch-phone, kanban-pc, kanban-phone, panel-pc). PASS.
- Narrowing needed, minor: "whatever its number of sources (2 or 7)" was measured only for 3 sources; it follows from
  `drawEdges` drawing one head per `data-to`, not from a 2 or 7 measure. Not a failure.
- Known gaps names the closed-batch arrows. PASS. Review/Verified/CI boxes are unticked placeholders, for the Driver.

VERIFIED

## Description pass (posted body of PR 415), head 819b8480171ae1c830874d22dd41025d83e298a0

- Command: `gh pr view 415 --repo gsemet/chantier --json body`. Sections Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps, a `<details>` fold with Changes, Human decisions, Impacts, Test plan, Internal references: renders; no relative paths; no username or home folder in the text.
- Images: five `user-attachments/assets/...` URLs, `curl -sL` each returns 200 image/png (169, 171, 166, 217, 217 kB). Images not opened, as the brief says.
- Test plan SHAs: `gh pr checks 415`: all five jobs pass at the head; `chantier log CR-441`: "approved at 9b22d87..., committed as 819b8480" matches the box "approved at 9b22d87, committed as 819b848"; Verified at 819b848 matches the earlier verdict at this head.
- "measured with three": evidence/measures.md, "arrows into CR-148: 3 (expected 3)", one head. Matches.
- Known gaps names the closed-batch pictures gap; evidence claims match measures.md.

VERIFIED (description pass)

## Move 819b848 -> 607a628faae899b57646e513c1e3e5b2343c90ad (restack onto CR-440 83b3a9a0, conflict resolved)

Head: 607a628faae899b57646e513c1e3e5b2343c90ad

- Code and test unchanged (607a628f): `git diff 819b848~1 819b848 -- <cli>/src <cli>/tests/test_board_graph_arrows.py | git patch-id --stable`
  and the same for `git diff 83b3a9a0 607a628f` both print `8d2a13c93fc1397eb4238b52f500bcf8576810c9`. Claims 1-10 (browser, tooltips, Gantt, closed batch,
  phone) carried from 819b848: the product code's patch is identical; the base change (CR-440, Triage/store/watch) touches
  none of the graph, batch-head, CSS or i18n files (`git diff --stat 83b3a9a0 607a628f` lists only the CR's own files).
  Claim 10 rerun at 607a628f: `pytest tests/test_board_graph_arrows.py tests/test_board_design.py -q` -> `39 passed`.
- Touched by the move: `scripts/docs_screenshots.py` (graph tab added to the shots, selector accepts the `node-open-c:` key
  that the Graph cards carry, comment wrapped) and 7 regenerated PNGs, `docs/web-board.md` (graph picture and the two
  paragraphs). `git diff 83b3a9a0 607a628f -- scripts docs/web-board.md` read: matches the PR's claims.
- Pictures opened at 607a628f: `batch-graph-pc.png` (Graph tab, levels, arrows, no hover), `batch-pc.png` (Kanban default),
  `panel-pc.png` (panel from a Kanban card, CR-145 files), `batch-phone.png` (switch hidden), `batch-gantt-pc.png`: each shows its
  screen, legible, made-up demo data (shop-api), no username or home path. PASS. Note: the graph picture's arrowheads are single
  per target, none at CR-148 (cropped below); the head itself is proved by claim 1.
- Gate/Review/CI: the gate pass and review are at 819b848; the Driver's notes for 607a628f are the Driver's to cite (CI
  at the new head not re-read by me; the PR body's SHAs must be moved to 607a628 by the Driver).

VERIFIED

## Light re-verify after restack onto ca0032cb, head 91b2c1f4a8ddd4fc2a3d5be3bcbe88776cf193e7

- Patch unchanged: `git range-diff cdee6c82..ab4bb9fa ca0032cb..91b2c1f4` shows `1: ab4bb9fa ! 1: 91b2c1f4` with only
  context-line differences (a hunk header in docs/web-board.md, a context line in scripts/docs_screenshots.py); no `+`/`-` line of the CR changed.
- Pictures are the CR's: for the 7 pictures the CR changes (batch-cards-pc, batch-gantt-pc, batch-graph-pc, batch-pc, batch-phone,
  kanban-phone, panel-pc), `git rev-parse 91b2c1f4:<f>` equals `ab4bb9fa:<f>` for each (same blob). The CSS, JS, tests of the CR also same blobs.
- Tests at 91b2c1f4: `pytest test_board_graph_arrows.py test_board_design.py` gives `40 passed`.
- Browser claims 1-8 and gate: carried from 819b848 / ab4bb9f: the CR's code blobs (batch-graph.js, batch-head.js, css, test) are identical; the
  base change (CR-440 Triage fold) touches the Triage view, not the batch graph. Not re-run (no `just scenario`, per brief).

VERIFIED
