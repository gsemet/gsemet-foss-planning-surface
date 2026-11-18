# CR-343 verification

Head: e616f7a61bdda8282fa88f35b4c7b72d7d6725a6

Before-state: base head 1690ec4f (CR-341), served from a detached worktree.
After-state: the pushed head above, served from a scratch planning folder with a stub `gh`/`glab`
(logging each call) and headless Chrome over CDP. Paths on captures are made up (`~`).
Evidence: `<folder>/evidence/*.png`; pairs and notes in `work/verifier/evidence/before-after.md`;
raw logs in `work/verifier/logs/`.

Tests at the head: `test_board_prs_batches.py`, `test_board_forge_kind.py`,
`test_board_forge_read.py`, `test_board_prs.py` run locally: 69 passed.

## 1. Navigator, one forge read per batch change: VERIFIED
Running batch: 1 forge call on open. Switch to closed batch-04: 1 call at once, none in the next 22 s.
Back to the latest batch: one read, then polls every 10 s. Navigator shows on the PRs page.
Evidence: after-1-running-batch.png, after-1-closed-batch.png (log s1-after).

## 2. State filters, sorts, dates, address: NOT VERIFIED
- VERIFIED: filters open / draft / merged (closed only under "all") and sorts opened / activity /
  CR number / batch order work; rows show "opened N d ago", "active N h ago". Chip changes add 0
  history entries; Back leaves the page, forward restores the choice. Unknown `st`/`sort` read as
  absent; unknown `b` shows the latest batch.
- FAILED: a fresh load or reload of a copied address (`?b=batch-04&st=merged&sort=opened`) keeps the
  URL but shows all rows with the chips on "all" and "batch order". Cause: `router.js` `apply()`
  sets `prsState`/`prsSort` from the address, then spreads `reset` last (`prsState: null,
  prsSort: null`) because `now.project` is still null on first load, so `moved` is true.
  Evidence: after-2-reload.png (log s2-after, s2b-after).

## 3. No batch running: VERIFIED
gh0 (no running batch): last closed batch-04 shown with the navigator, one read, tag "closed, read
once". gl2 with no history: "No batch running.", no navigator.
Evidence: after-3-no-batch-running.png, after-3-no-history.png; before-3-no-batch-running.png.

## 4. MR wording and `!n` on GitLab: NOT VERIFIED
- VERIFIED: gl1 (MR links) and gl2 (gitlab origin, no link) say MR/MRs and `!n` on the PRs page,
  Home, Batch header and panels, Kanban, Costs, in English and French; events feed "MR !22 pushed"
  / "MR !22 poussée"; `pv.nomatch` in both languages. A GitHub record still says PR and `#n`. The
  mixed overview keeps PR headings as specified; the all-GitLab overview table and note say MR.
- FAILED: Batch page node cards still show a hard-coded "PR" on GitLab, en and fr
  (`web/js/views/batch-graph.js` lines 36 and 39).
- FAILED: all-GitLab overview header stat still reads "3 PRs to review" (`web/js/ui/header.js`,
  `stats.reviews` through `t`, not `tf`). Evidence: after-4-overview-allgitlab-en/fr.png.
- Gap (named, not a failure): GitLab `createdAt`/`updatedAt` fields and the GitLab PRs page ran
  only against a stub `glab`, not a real GitLab project.

## 5. AGENTS.md: VERIFIED
`git diff 1690ec4f e616f7a6 -- AGENTS.md` is one hunk (+7/-6) changing only the PRs-page sentence;
its word diff equals spec section 7; lines at most 100 columns.

## 6. pr-body.md against the diff: NOT VERIFIED
Changes omits `overview.js`, `prs.css`, `postit.css` and the `test_board_prs.py` edit, all in the
diff. Known gaps says only "no browser capture" and the GitLab fields; it must also carry the
defects above until fixed.

## Result
NOT VERIFIED. Failed: claim 2 (address not applied on first load), claim 4 (batch-graph node cards;
header stat), claim 6 (pr-body.md).

Disclosure: one early probe reached the real GitHub with an invalid query because `gh` resolved to
a scoop shim before my stub (PATH in Windows form); fixed with an msys-style PATH, nothing was
written to any forge.
