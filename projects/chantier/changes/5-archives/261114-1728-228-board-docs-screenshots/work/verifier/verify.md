# Verify CR-228 (first verification)

Head: 073cfc5b12b2111eedbd0b70a9fbfc8ffd2b97da

Verdict: NOT VERIFIED

## Claims

1. `just docs-screenshots` runs on this machine (Windows 11, scratch HOME/USERPROFILE/CLAUDE_CONFIG_DIR/TEMP, Chromium downloaded to scratch): OK at 073cfc5. Command `just docs-screenshots`, exit 0, 23 files written, ~87 s.
2. Two runs in a row give identical PNGs: OK at 073cfc5. SHA-256 of the 23 PNGs after run 1 and run 2 compared with Compare-Object: no difference.
3. FAILED at 073cfc5: a run leaves `git status` clean. After the run, `git status --short` shows 12 modified files (batch, costs, editor, panel, picker, project, each pc and phone); the other 11 PNGs are byte-identical to the committed ones. The spec says clean "or any pixel change explained in the PR"; the PR explains nothing. Cause (looked at committed vs fresh batch-pc.png): the committed pictures were taken before commit 99c1cd4 (ready locally / PR in draft / ready to merge). Committed batch-pc.png shows "Handed back ready 3", legend "handed back", "PRs to review 1"; the fresh one shows "Handed back ready 0", "0 to review", legend "ready to merge / PR in draft / ready locally", "PR in draft, not to merge yet". 99c1cd4 is the parent of 073cfc5 and changed the board, so the PR's "Taken at `073cfc5`" caption and the "SHA in the captions" are false for these 12 files. Fix: rerun the command at the head and commit the 12 PNGs (carried 11 are identical).
4. FAILED at 073cfc5: docs/web-board.md matches the board as shipped. It says "The colour is the state: blocked, working, handed back, waits, queued, merged" and describes PRs to review / "Drafts, not to review yet" (Batch section, line 33-37); the board at head draws the legend blocked, working, ready to merge, PR in draft, ready locally, waits, queued, merged, and "PRs in draft, not to merge yet". "Handed back ready" tile and the Kanban "Handed back" column wording to be rechecked against the same change. The page predates 99c1cd4 and must be updated with the new states and the new screenshots.
5. After a run, nothing changes under docs/demo/ nor in the repo's planning folder: OK at 073cfc5. `git status --short docs/demo` empty; the only changes were the 12 PNGs, restored with `git checkout -- docs/web-board` (worktree clean again, HEAD 073cfc5).
6. `chantier preflight` (main checkout) does not see docs/demo/: OK at 073cfc5 (preflight passed; docs/demo lives only on the branch). Also `Repo.find()` run from the worktree's docs/demo resolved to C:\Users\gaeta\Projets\chantier and its `.agents\changes`, not the demo folder.
7. README shows docs/web-board/batch-pc.png in place of the pane image, with the web board link and More-list entries (README lines 170-174, 253-261); `just check` passes (exit 0, 72 passed, link test included): OK at 073cfc5. The README image is itself one of the 12 stale PNGs (see 3).
8. docs/web-board.md launch statements vs code, spot check: OK at 073cfc5. `--host`, `--port` (0 = any, default 8765), `--clock`, `--new-key` exist in declare/board.py; default host 0.0.0.0 in board/address.py.
9. PR body vs diff: FAILED. The Deliverables says pictures "Taken at 073cfc5" (false for 12 files, see 3); Known gaps does not name that the pictures lag the board; the body's embedded images are the stale ones. Otherwise the file list matches the diff (README, boards.md, agents-and-models.md, docs/web-board*, demo, script, justfile; 23 PNGs counted). The Test plan has `<sha7>` placeholders left, to fill at the end.

## Failed claims
3 (PNGs stale against the board at head, not explained), 4 (page text predates the ready-locally / PR-in-draft states), 9 (PR body says taken at head).

No before/after evidence captured: this is a docs CR, the pictures are the evidence and were judged above.


# Second verification (delta 073cfc5..6860065)

Head: 686006575ea537e723ab6245d4982f70f1aadc3c

- Screenshots reproducible (judged at 6860065): `just docs-screenshots` run once with scratch HOME, USERPROFILE, CLAUDE_CONFIG_DIR, TEMP: exit 0, 23 files written, then `git status --short` printed nothing (the 23 committed PNGs are byte-identical to the regenerated ones, so none is stale). batch-pc.png opened: shows ready to merge / PR in draft / ready locally legend, "PRs in draft, not to merge yet", Handed back ready tile, as the page says.
- docs/web-board.md Home/Batch/Kanban wording (judged at 6860065): matches en.js labels ('ready to merge', 'PR in draft', 'ready locally', 'To review', 'Waiting for you', 'Next batch', 'Written by the board', 'PRs in draft, not to merge yet', 'PRs to review'); the Kanban section (Intake, Grill, 3-ready, In progress, Handed back) was not touched by the move.
- PR body (judged at 6860065): `gh pr view 199` headRefOid = 6860065...; body says Taken at 6860065, image URLs name the full 6860065 SHA, no placeholder SHA; Summary, Deliverables and Changes match the diff (23 PNGs, web-board.md, boards.md, agents-and-models.md, README, demo, script, recipe); Known gaps covers the French UI, writes not captured, costs, one autosync state, Windows fonts, batch-pace.svg, partial docs pass, release notes, waived long gate. Review box "approved at 073cfc5": driver note "r4 inspector approved at 073cfc5" in `chantier log`; the move's commit is the round's.
- Carried from 073cfc5 (the move touched only web-board.md wording and the 12 PNGs): demo folder not taken for this repo's planning folder, script behaviour, no change under docs/demo/ (also seen: git status clean after run), links, README change, boards.md pass.
- Gates: `just check` passed at 073cfc5 per log (run 20261114-172204-4620); the Driver's long gate at the head is running and not run by me; CI 5/5 at 073cfc5 per log (CI at 6860065 is the Driver's to confirm).

VERIFIED