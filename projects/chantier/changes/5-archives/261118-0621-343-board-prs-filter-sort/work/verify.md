# CR-343 verification (second pass)

Head: 997f12222e633f6893a69eedaabb25326b111dc7

Previous pass: NOT VERIFIED at e616f7a (kept as `verify-1.md`). The move e616f7a..997f122 touched `router.js`,
`header.js`, `picker.js`, `batch-graph.js`, `overview.js` and the word files (`pr.tag` / `mr.tag`).
Method: a scratch planning surface under `work/scratch` (projects gh1 GitHub links, gl1 GitLab links, gl2 gitlab
origin without link, gh0 closed records only), a stub `gh`/`glab` that logs each call, the worktree's board served
with `chantier board`, headless Chrome over CDP. Paths on captures are made up. Raw logs: `work/verifier/logs/`
(`s2.log`, `s2b.log`, `sA.log`, `sB.log`). Images: `<folder>/evidence/`, notes `work/verifier/evidence/before-after.md`.
Everything I served is stopped; the scratch surface is removed.

Tests at the head (`git rev-parse HEAD` = the Head above, clean tree):
`uv run --no-sync python -m pytest tests/test_code_targets.py tests/test_board_prs_batches.py
tests/test_board_forge_kind.py tests/test_board_forge_read.py tests/test_board_prs.py -q` -> `74 passed in 11.00s`.

## 1. Navigator, one forge read per batch change: VERIFIED at 997f122
Re-run quick (the router changed). Log `sA.log`: gh1 PRs page on the running batch: 1 forge call
(`gh [10,11,12,13]`). Navigator "‹" to batch-04: url `?p=gh1&v=prs&b=batch-04`, tag "closed, read once", 1 call at
once (`gh [100,101,102]`), none in the next 14 s. "Latest": back on batch-05, one more read. Image:
after-1-closed-batch.png, after-1-running-batch.png (in `work/verifier/evidence/`).

## 2. State filters, sorts, dates, address: VERIFIED at 997f122
- Reload of a copied address (`s2.log`): fresh load of `?p=gh1&v=prs&b=batch-04&st=merged&sort=opened` ->
  chips `merged` and `opened` pressed, rows `#100 opened 15 d ago`, `#101 opened 22 d ago` (merged only, newest
  first); `location.reload()` gives the same. `?b=batch-04&st=draft&sort=cr` -> chips draft / CR number, no
  row (no draft in that batch). `?st=open&sort=activity` on the latest batch -> chips open / last activity,
  `#10 active 3 d ago`, `#11 active 5 d ago`. Image: after-2-reload.png.
- A real project change (`s2b.log`): from gh1 with `b=batch-04&st=merged&sort=opened`, click gl1 in the project
  picker -> `?p=gl1&v=prs`, chips `all`, `batch order`, latest batch. st/sort/b are cleared.
  Image: after-2-project-change-gl1.png.
- Same project: PRs -> Costs keeps `b=batch-04` and drops st/sort (`?p=gh1&v=costs&b=batch-04`); Costs -> PRs
  gives `?p=gh1&v=prs&b=batch-04`, chips all / batch order; back twice returns to
  `?...&st=merged&sort=opened` with the chips; forward goes to Costs.
- Carried from e616f7a: chip clicks add no history entry, all sorts and states, unknown values read as absent
  (the move touched `apply()`'s order of keys only; the fresh-load results above cover it).

## 3. No batch running: VERIFIED at 997f122
`sA.log`: gh0 (closed records, no running batch): shows batch-04, tag "closed, read once", navigator present, 1 call, still 1
call 12 s later. gl2 (no history): "No batch running.", no navigator. Images: after-3-no-batch-running.png,
after-3-no-history.png.

## 4. MR wording and `!n` on GitLab: VERIFIED at 997f122
- Batch page node cards (`sA.log`, text of each `.node .nm`): gl1 running batch `r0/3 MR` x4 (en) and `MR` x4 (fr);
  gl1 closed batch-04 `r1 MR $1.00` x3 (en and fr). GitHub: gh1 running `PR` x4, gh1 closed batch-04 `PR` x3.
  Images: after-4-gl1-batch-en.png, after-4-gl1-batch-fr.png, after-4-gl1-batch-closed-en.png.
- Overview header stat, all projects on GitLab (gl1 + gl2, `sB.log`): en `3 MRs to review`, table
  `MRs to review`, note "opens the MR to review"; fr `3 MR à revoir`. Mixed surface with GitHub projects
  (`sA.log`): `6 PRs to review` / `6 PR à revoir`, headings PR. Images: after-4-overview-allgitlab-en/fr.png,
  after-4-overview-mixed-en/fr.png.
- MR PRs page rows `!70 !71 !73 !72`, sidebar "MRs", title "MRs" (after-2-project-change-gl1.png).
- Carried from e616f7a: Home, Kanban, Costs, events feed, `pv.nomatch`, gl2 origin-only; the move did not touch
  them. Gap (named): GitLab `createdAt`/`updatedAt` and GitLab PRs page ran only against a stub `glab`.

## 5. AGENTS.md: VERIFIED
carried from e616f7a: `AGENTS.md` is not in `git diff --name-only e616f7a6 997f1222`; one hunk, same words as
spec section 7.

## 6. pr-body.md against the diff: VERIFIED at 997f122
`gh pr view 305 --json body` equals `work/pr-body.md` (diff of the two: only a trailing blank line). Its Changes
lists every file group of `git diff --name-only 1690ec4f 997f1222` (prs.py, routes.py, forge_read.py,
forge_kind.py, state.py, the web js including overview.js, header.js, picker.js, batch-graph.js and the `pr.tag` /
`mr.tag` keys, prs.css, postit.css, the four tests, AGENTS.md, docs). Known gaps carries the two real gaps
(no browser capture marked UNVERIFIED; GitLab fields not exercised on a real project). No image is attached to the
description, so none shows a username or home folder. No Review box claimed yet. Note for the Driver: the two
"no browser capture" UNVERIFIED lines can be narrowed now that `<folder>/evidence/` holds captures at 997f122.

## Result
VERIFIED at 997f12222e633f6893a69eedaabb25326b111dc7.

## Description pass at 997f12222e633f6893a69eedaabb25326b111dc7: VERIFIED
Command: `gh pr view 305 --json body,headRefOid` -> headRefOid 997f12222e633f6893a69eedaabb25326b111dc7.
- Summary, Deliverables, Changes match `git diff --stat 1690ec4 HEAD` (32 files; board py, web js/css, i18n MR files, tests, AGENTS.md, docs/web-board.md); nothing delivered unmentioned.
- Images: the three attachments downloaded (HTTP 200) and opened. Before (GitLab "PRs", no navigator/chips), after ("MRs", `!n`, navigator, State and Sort chips), GitHub sorted by opened (opened 3 d, 6 d, 7 d, 8 d). Each shows its caption; no username, no home folder (paths are not on screen). Sorted-by-opened caption names 997f122 as captured.
- Mermaid block and Details fold well formed; Known gaps names the stub-only GitLab claim (matches before-after.md "Not captured"); no STALE mark.
- Review box: `$CHANTIER log 343`: "r3 approved at e616f7a+uncommitted, committed as 997f122" proves `approved at 997f122`.
- Test plan: `just check` at 997f122 noted in the log ("just check pass at 997f122"); eval-dry-run at e616f7a stated as such (CLI src moved after, first-push gate was e616f7a). CI at 997f122: `gh pr checks 305` -> check x3 OS, eval-dry-run, scenario all pass.
- Role names: only "Chief of Staff" inside quoted UI text of the product; no doer-of-work reference outside Internal references.
Verdict: VERIFIED
