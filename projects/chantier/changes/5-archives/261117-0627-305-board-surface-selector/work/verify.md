# Verify CR-305

Head: 51a3c8e21296d119657d96f0360322aa0f23c427

Verdict: VERIFIED.

Second pass, after the move ad35ccf..f3af2c0 (`git diff --stat ad35ccf f3af2c0`: `paths.css` +8,
`picker.js` 1 line, `docs/web-board/home-pc.png`, `autosync-pc.png`, `scripts/docs_screenshots.py`
reformatted, no logic). Browser checks re-run at f3af2c0 (after) and f11132b (before, detached
worktree, removed) with `work/verifier/drive.py` over a scratch copy of `docs/demo/` (shop-api `repo:`
long, mobile-app `repo:` removed), 1400x860 and 375x812, en and fr; numbers in
`work/verifier/evidence/{before,after}-measures.json`, pictures next to them.

## Claims

1. Gate pass at the head. SHA f3af2c0. `work/gates/20261116-223253.log` first line:
   `gate CR-305 branch chantier/batch-22/cr-305-... head f3af2c07e6dfbd3199071df20874862e335e9a22`,
   last line `result: pass at f3af2c07e6dfbd3199071df20874862e335e9a22`. OK.

2. Tests of GET /api/board. Carried from ad35ccf: the move touched no Python under `src/` or `tests/`
   (`git diff --stat ad35ccf f3af2c0` lists only css, js, two pngs and the screenshot script); there
   the proof was `pytest -k "two_paths or adds_no_path"` -> `2 passed`. OK.

3. Check 1, the button shows surface name, path and "Planning surface . N projects" (never "All
   projects"), en and fr, both sizes. SHA f3af2c0 (re-judged, it failed at ad35ccf).
   `after-measures.json`: `has_all_projects_text` 0 in the 4 surface runs. Button text: `surface | <path>
   | Planning surface · 3 projects` (pc and phone en), `... | Surface de planification · 3 projets`
   (pc and phone fr). Pictures opened: `after-surface-pc-en-closed.png` shows the line wrapped on two
   lines, "Planning surface · 3" / "projects"; `after-surface-pc-fr-closed.png` shows "Surface de
   planification" / "· 3 projets": N readable at 1400 in both languages. `after-surface-phone-fr-closed.png`
   shows the whole line. The move's `picker.js` also gives the line a `title`. OK.

4. Left bar width unchanged versus the base. SHA f3af2c0. before -> after: `.ws` 211 -> 211, `side`
   240 -> 240 (pc en and fr), table first column 173.75 -> 173.75 (en), 169.53 -> 169.53 (fr),
   `scroll_w` 1400 and 375 unchanged. OK.

5. Check 2, menu and title; check 3, paths per project line, long cut and whole on hover; check 4,
   single in-project board unchanged. Carried from ad35ccf: the move touched only the count line's
   style (`.ws .who > small.sur:not(.pth)`, `.pbtn ...`), which is not in the menu, the title or the
   project lines; re-run measures confirm: `solo-pc-en`/`solo-phone-en` `picker_present` false, same
   widths as before; `overview_titles` unchanged in shape. OK.

6. "All projects" gone from the docs. Carried from ad35ccf: the move changed no text string (diff
   above). OK.

7. Docs pictures. SHA f3af2c0. Opened `docs/web-board/home-pc.png` and `autosync-pc.png` (the two the
   move changed): button reads `planning-surface`, `/home/demo/plannin...`, "Planning surface · 3" /
   "projects" wrapped; nothing of the machine; the autosync popover is open in the second. Opened
   `picker-pc.png` (unchanged by the move): its button is a project, not the surface, so the wrap does
   not touch it. Phone pictures unchanged by the move (`git diff --stat`) and the line fits at 375.
   The "taken twice gives the same" claim is the Coder's run, not repeated (asked not to). OK.

8. PR description (PR 254, head f3af2c0 by `gh pr view`). Summary, Deliverables, Changes match the
   diff. The `Test plan` still has `<sha7>` placeholders and the screenshot bullet says "added after
   verification": for the Driver to fill. The Known gaps names the table's cut folder; the earlier
   gap (cut count line) no longer exists. OK, subject to those placeholders.

## Verdict

VERIFIED at f3af2c07e6dfbd3199071df20874862e335e9a22.

## Description pass (PR 254, head f3af2c07e6dfbd3199071df20874862e335e9a22)

Verdict of this pass: NOT VERIFIED (cancels the VERIFIED above until a later pass says VERIFIED).

- Template audit: sections, order, fold (blank lines, nothing after `</details>`), no internal reference
  outside Internal references, Known gaps filled: OK. Title and Summary/Changes match `git diff --stat
  f11132b HEAD` (18 pictures, paths, js, css, i18n, docs, tests): OK.
- Test plan: `just test` at the head: `271 passed in 46.98s`; `gh pr checks 254`: 3 check, eval-dry-run and
  scenario pass; Review approved at f3af2c0: `log` note "r3 inspector approved at ad35ccf ... committed as
  f3af2c0": OK.
- Images: 8 uploaded URLs, `Invoke-WebRequest` GET -> 200 image/png each. Opened after-desktop, after-menu,
  after-French: they show the claimed picker, paths and French labels.
- FAILED: the "after" pictures show the machine's real path, `C:/Users/gaeta/AppData/Local/Te...` (full
  `C:/Users/gaeta/AppD...` in the button), while the description says the pictures reveal nothing of the
  machine (that holds for the docs pictures only). Retake the uploaded pictures with a neutral path, or
  say so in the description.
## Description pass 2 (PR 254, head f3af2c07e6dfbd3199071df20874862e335e9a22)

Verdict of this pass: VERIFIED (a later pass than the NOT VERIFIED above; the last verdict at this head decides).

- Body read as posted (`gh pr view 254 --repo gsemet/chantier --json body,headRefOid`): head f3af2c0.
  Template audit: Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps, then the fold
  (Changes, Human decisions, Impacts, Test plan, Internal references), nothing after `</details>`; roles
  named nowhere outside Internal references. OK.
- Images: the body has 6 uploaded URLs; each GET -> 200 image/png. Opened all six: before desktop, phone and
  menu show demo data (docs-portal, mobile-app, shop-api), no path; after desktop, phone and menu show
  `planning-surface` and `/home/demo/planning-surface` only, plus `folder projects/<name>/` and `repo .repo`.
  No machine path and no username in any of them. OK.
- Images are the ones at the SHA named: SHA-256 prefixes of the downloaded after pictures equal the
  committed `docs/web-board/home-pc.png` (7D30FC40F11C), `home-phone.png` (060AFA19F289) and
  `picker-pc.png` (4C9FEE1FF027) at f3af2c0. OK.
- Claims match the pictures: button with bold surface name, path, "Planning surface . 3 projects"; title =
  surface name; menu first line = name and path; no "All projects" or "overview . N PRs" in the after
  pictures; `git grep "All projects"` at HEAD in board/, scripts/ and docs/*.md finds only the v0.10.0 release
  notes (history). Left bar 240 px in both pictures. OK.
- Summary, Deliverables, Changes against `git diff --stat f11132b HEAD` (32 files: 18 pictures, state.py,
  routes.py, paths.css, overview.css, index.html, en/fr, header/picker/overview js, docs, screenshot script,
  test_board.py): no claimed change missing, none unmentioned. OK.
- Test plan, Review, CI: carried from the previous pass at the same head (`271 passed`, 3 checks pass, review
  note approved at ad35ccf and committed as f3af2c0); the head has not moved. OK.
- Known gaps: the table's early cut of the folder path; no UNVERIFIED claim and no accepted failure exists. OK.

## Third pass, after the move f3af2c0..51a3c8e (rebase onto 942e14d, conflicts resolved)

Head: 51a3c8e21296d119657d96f0360322aa0f23c427

Verdict of this pass: NOT VERIFIED.

Claims judged again (the CR's own patch is `git diff --stat 942e14d HEAD`: 32 files; the rest of
`f3af2c0..HEAD` is CR-304's base).

- i18n at 51a3c8e. `git diff 942e14d HEAD -- en.js fr.js`: `project.all`, `project.all_sub` replaced by
  `project.folder`, `project.repo`; `git grep -n -E "project\.all|all_sub" HEAD -- skills docs scripts`
  prints nothing: no dangling use. OK.
- Tests at 51a3c8e. `pytest tests/test_board.py -q` -> `27 passed in 6.03s`. OK.
- Picker/header/paths.css at 51a3c8e: `git diff 942e14d HEAD` read; it is the f3af2c0 logic (surface name and
  path, count line wraps, two labelled paths, title = surface name). Nothing of the move touched them
  beyond the rebase. OK (carried from f3af2c0: browser measures, same code).
- Docs pictures at 51a3c8e. Opened `docs/web-board/picker-pc.png` (menu: planning-surface
  `/home/demo/planning-surface`, then each project with `folder`/`repo`; no machine path) and
  `home-phone.png` (button: name, path, "Planning surface . 3 projects"; cards with the two paths). OK.
- `scripts/docs_screenshots.py`: diff vs 942e14d is the surface-path route plus formatter rewraps; no
  logic beyond `fix_surface_path`. OK.
- Gate: `just scenario` is running locally (log `work/gates/20261117-004928.log`, first line
  `gate CR-305 ... head 51a3c8e21296d119657d96f0360322aa0f23c427`, not finished when read; no result line).
  CI at the head: `gh pr checks 254` -> check (macos, ubuntu, windows), eval-dry-run, scenario all `pass`. OK
  for CI; the local pass is not yet cited.
- FAILED, PR description (`gh pr view 254`, headRefOid 51a3c8e): (a) every proof names `f3af2c0`
  (Test plan "Local gates at f3af2c0", "Review", "Verified", "CI green", the after pictures "at f3af2c0"),
  while the head is 51a3c8e and none says `carried from <sha7>` with a reason; (b) Changes says
  "`nav.overview` removed" but `git grep -n "nav.overview" HEAD -- skills` still finds it in `en.js:16` and
  `fr.js:16` (now unused: the title no longer calls it), so the claim is false or the key should go.
  Fix: update the SHAs (or carry them with a reason), and either remove `nav.overview` or drop the claim.

## Verdict

NOT VERIFIED at 51a3c8e21296d119657d96f0360322aa0f23c427 (description only; the code and pictures hold).
## Description pass 3 (PR 254, head 51a3c8e21296d119657d96f0360322aa0f23c427)

Head: 51a3c8e21296d119657d96f0360322aa0f23c427

Verdict of this pass: VERIFIED (later than the NOT VERIFIED above; the last verdict at this head decides).

- Body read as posted (`gh pr view 254 --json body,headRefOid`): headRefOid 51a3c8e. The `nav.overview removed` claim is gone; Changes lists i18n as `project.all`, `project.all_sub` removed and `project.folder`, `project.repo` added, as proved in the third pass. OK.
- Proofs name their SHA: Local gates at 51a3c8e (`pytest --collect-only -q` -> `367 tests collected`; gate log `work/gates/20261117-004928.log` first line `gate CR-305 ... head 51a3c8e2...`, last line `result: pass at 51a3c8e21296d119657d96f0360322aa0f23c427`); Evidence and Review carried from f3af2c0 and the move approved at 51a3c8e (`log`: `driver note ... restack inspector approved at 51a3c8e...`); Verified at 51a3c8e; CI green at 51a3c8e (`gh pr checks 254`: 3 check, eval-dry-run, scenario all pass). OK.
- Images and code: carried from the third pass (same head, pictures `carried from f3af2c0`, same code). OK.
- Known gaps: the table's early cut; nothing UNVERIFIED. OK.
