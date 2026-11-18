# Verify CR-327

Head: ba53e9579959954c38fefbfbbe9d7cb8f83566f5

Second pass. Previous judgment at e8e5171 (NOT VERIFIED, one failure F1). Move e8e5171..643b29c: three files
(`git diff --stat e8e5171 HEAD`): `router.js` (batchOf), `model/receipt.js` (minutesOf), `views/costs-receipt.js`
(dates, lasted). Base unchanged.

Method: board served from the worktree's code (`chantier board --port 8793`) over a scratch planning folder (copy of
the predecessor's batch-01..23 records and archive folders, fresh `git init`, outside the planning surface), headless
Chrome 157 driven by CDP scripts (`work/verifier/nav3.mjs`, `shots3.mjs`). Chrome only. All judged at 643b29c.

## Judged again at 643b29c

- F1 fixed. `node work/verifier/nav3.mjs <key> <profile>`:
  - `FRESH LOAD b=batch-22  {"id":"batch-22","bs":["‹","›","Dernier"],"url":"?p=chantier&v=costs&b=batch-22"}`;
    after 2 s the address is still `?p=chantier&v=costs&b=batch-22`.
  - `RELOAD {"id":"batch-22",...,"url":"?p=chantier&v=costs&b=batch-22"}`.
  - `FRESH batch page b=22 {"id":"batch-22",...,"url":"?p=chantier&v=batch&b=batch-22"}`.
  - `FRESH kanban b=22 {"bs":[],"url":"?p=chantier&v=kanban"}` (b cleared on a non-batch view).
- Unknown b: fresh `...&v=costs&b=batch-99` -> `{"id":"batch-23","bs":["‹","›(disabled)"],...}`, `pill false`
  (latest, no pill); `b=batch-22` -> `pill@22 true`. Now a direct proof of the unknown-b rule.
- Back/forward and b kept Costs<->Batch, cleared elsewhere (same run): `prev` x2 -> batch-21, `browser back` ->
  batch-22, `browser forward` -> batch-21; `-> batch` keeps `&b=batch-21`; `-> kanban` clears it; `-> costs` ->
  batch-23 with no b; `Latest` click -> `?p=chantier&v=costs`.
- Batch-01 receipt (null dates): `shots3.mjs`: `NaN anywhere false`; head meta shows no dates, no minutes, no
  "maintenant"; the ticket body reads "rôles non enregistrés pour ce batch", total "—". Screenshot
  `evidence/05-costs-batch-01-receipt.png` (looked at). Cosmetic, not a spec point: the head's grey box holds a lone
  "," (mode and steering empty on that old record).
- Copy as image still works at head: button `{"text":"Copy as image","disabled":false,"inTicket":false}`; click;
  clipboard `[{"ty":"image/png","size":559506,"w":936,"h":1534}]` (same as e8e5171). Receipt with dates (batch-22)
  still shows "16 nov., 20:45 -> 17 nov., 07:42 / 10 h 56 min" (evidence/04).

## Carried from e8e5171 (the move touched no file these exercise)

- Costs navigator, previous/next, `‹` to the start (batch-01, `‹` disabled, pill shown), Latest pill logic.
- Batch page of a closed batch: batch-23 graph with levels and arrows, no notice (evidence/06 re-shot at head);
  batch-18 archives-only notice and arrows, batch-01 "Dépendances non enregistrées" notice and 1 node (evidence/02).
- Heading "Detail · per change request" EN/FR; non-secure origin button disabled with tooltip and 127.0.0.1 link
  (evidence/03); board start prints `on this machine:` line and `/api/board` has `local_url`; phone width wraps.

## Not proved

- Edge and Firefox copy (not installed); the PR's Known gaps names it.
- Hover (versus focus) of the tooltip; the live-batch case (none in the scratch folder).
- PR description, not re-read at this head: at e8e5171 its Known gaps said "No screenshot ... yet" while evidence held
  screenshots, and its "a link opens the same batch" was untrue (now true). Test plan boxes unticked, Review box empty
  (not judged here); the Driver must refresh the body.
- Cleanup: the scratch folder outside the planning surface (`C:\Users\gaeta\AppData\Local\Temp\claude\f81ba1603abd10b3\v327`)
  could not be removed by me (a shell write there is refused outside my writes: folders); the board on 8793 is stopped.
  `work/scratch` of the CR folder is deleted.

Screenshots at 643b29c (open as images; no username, no home folder, only page content): `evidence/04-costs-past-batch-pill.png`
(batch-22, pill "Latest"), `evidence/05-costs-batch-01-receipt.png`, `evidence/06-batch-page-closed-graph.png`,
`evidence/07-copy-as-image-button.png`. Earlier, from e8e5171: `work/verifier/evidence/01..03`.

VERIFIED

## Description pass (PR body as posted, judged at 643b29c1504760caf868e7c7ff52bd868b96471a)

Checked: `gh pr view 285 -R gsemet/chantier --json body -q .body` against pr-template.md and this file; the three
screenshots opened as images from evidence/04, 05, 06 (no username, no home folder; they match their captions: batch-22
with Latest pill and Copy as image, batch-01 without duration, batch-23 closed graph; the attached URLs themselves were
not re-downloaded). `gh pr checks 285`: 5 jobs pass. `chantier log`: "r4 approved at e8e5171, committed as 643b29c"
(Review box accepted). Layout, fold, Blast radius, no username/home folder: fine. Spec has no `issue:` line, so no Issues
References: fine.

Failed:
- Test plan, "Local gates: `just check` at 643b29c (the Coder's run)": a role name as the doer outside Internal
  references, and no command/output for it in verify.md (not proved here; CI `just check` pass is proved by gh pr checks).
- Known gaps omits a defect this file records: the batch-01 receipt's grey head box shows a lone "," (mode and steering
  empty on that old record; evidence/05). A cosmetic defect shipped knowingly needs its bullet.
- Deliverables claim "Closed batches record each CR's `order` and `after` list at close" (history.py): this file proves
  only the graph drawn from a record, not the recording itself; carry a proof or mark it UNVERIFIED.

NOT VERIFIED

## Description pass 2 (PR body as posted, judged at 643b29c1504760caf868e7c7ff52bd868b96471a)

Command: `gh pr view 285 -R gsemet/chantier --json body -q .body`; `gh pr checks 285 -R gsemet/chantier`;
`gh run view 44147779452 --json headSha` (= 643b29c1504760caf868e7c7ff52bd868b96471a, equal to `git rev-parse HEAD`);
`grep` of scenario/run_scenario.py lines 3240-3248.
- Local gates: body now says "`just check` at 643b29c: pass on the three systems in CI"; checks show macos, ubuntu, windows
  `just check` all pass. No role name. Fixed.
- batch-01 lone ",": now a Known gaps bullet. Fixed.
- order/after at close: body cites the scenario's close step green in CI; `just scenario (ubuntu-latest)` pass at the head,
  and run_scenario.py:3242 asserts every closed-record CR has an integer `order`, an `after` list equal to the batch's, sorted
  by `order`. Fixed.
- No regression: Summary, Deliverables, Known gaps (UNVERIFIED Edge/Firefox listed), Test plan, fold unchanged.

VERIFIED

## Restack pass (judged at ba53e9579959954c38fefbfbbe9d7cb8f83566f5)

Move 643b29c..ba53e95: restack onto a16ff1b, one conflict in header.js crumbs().
- `git range-diff a111e18...643b29c a16ff1b...ba53e95`: commits 2 and 3 identical (`=`); commit 1 differs only in the
  header.js crumbs() hunk: chip is `chip ${shown.icon}` (base's hue class, previously `chip ${shown}`) with the CR's
  `shownBatchChip`, plus a main.js context line from the base. Nothing else changed in the CR's patch.
- Chip rendering read at head: closed record -> icon `queued` (grey: crumbs.css `.chip.queued` = `--state-queued-tint` =
  `--chip`, as before); running -> `working`, paused -> `queued`. Classes match crumbs.css. Not re-driven in a browser:
  the change is one class name whose CSS exists; no visual proof captured at this head (screenshots 04-07 carried).
- `just check` at ba53e95 (run by me): ruff clean, `449 passed in 19.24s`, `release-notes ... ok`. Tree clean.
- Carried from 643b29c: all browser proofs above (navigator, receipt, copy as image, back/forward, F1), the move did not
  touch their code beyond the chip class; the PR description (stale SHA lines are the Driver's to mark).

VERIFIED
