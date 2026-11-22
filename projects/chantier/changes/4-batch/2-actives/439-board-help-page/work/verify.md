# Verify CR-439 (Help page)

Head: 60aacc1db6243b447659f32357906624bf97aaff

Verdict: NOT VERIFIED (the PR description as posted is stale; the evidence pictures predate the head).

Method: a throwaway surface (fresh git repo, projects `demo` and `other`) under `work/scratch`, served by `chantier board --host 127.0.0.1 --port 0 --ui <worktree>/.../clients/web`, real Chrome headless driven over the DevTools protocol by my scripts `work/scratch/ver.py` (log `ver4.log`) and `ver2.py` (log `ver3.log`). Board and Chrome stopped, surface and profile deleted afterwards. The previous judgment was at e317196; the move (fixes, then rebase onto main) changed `router.js`, `main.js`, `shell.css` and the batch files, so the router/history claims are judged again.

## Claims (all at 60aacc1 unless stated)

1. Tests. `pytest -q tests/test_board_design.py tests/test_code_targets.py tests/test_board_help.py tests/test_board_title_row.py`: `46 passed in 4.27s`. PASS.
2. Bottom bar at 360 px (spec open question 4 A). `ver2.py` (`ver3.log`): `bnav {"cw":360,"sw":399,"ox":"auto","n":8,...,"labels":[...,"Costs","Configuration"]}`. `overflow-x` is now `auto` (was `visible` at e317196): the 399 px of content scroll inside the 360 px bar, no item is cut off for good. Diff: `git diff origin/main...HEAD -- css/shell.css` adds `overflow-x: auto` on `.bnav` and `flex: 0 0 auto` on `.bnav button`. PASS.
3. History rules (help-Q14), real Chrome, `ver4.log`: (a) Escape, close button and second click each close with the length unchanged (6/6, 8/8, 10/10), Back goes to `?p=demo&v=home`; (b) open then Back: Help with no detail, Back: home; (c) open `batch` then `grill` (`h=grill`, `helpOpen`): Back: Help no detail, Back: home; (d) shared link `&h=batch` (hs null): close leaves `?p=demo&v=help`, Back leaves to about:blank, never the detail; Escape and second click close it in place; (e) reload keeps `helpOpen` and the detail, close: Help no detail, Back: home; unknown `h=nope`: Help with no detail. PASS.
4. All 25 cards open and close by a second click: `cards 25 cards, failures []`; Enter opens and closes, Space opens. PASS.
5. Sidebar: `["home:Home","help:Help","triage:Triage0",...]`, Help right after Home, no count. "Read more": `["https://github.com/gsemet/chantier/blob/main/docs/use-cases.md#turn-ideas-into-ready-work","_blank","noopener","Read more"]`; French `En savoir plus (page en anglais)`, French detail "Batch et slots"; "All projects" with Help selected, title `Help`, no detail; the board stopped after load, a card still opens. PASS.
6. Diff against the specification (`git diff origin/main...HEAD`): registry, `host.js`, `header.js`, router (`topic`, `topicOf`, `closeTopic`, `helpOpen`), store, `main.js`, DESIGN.md, icon, words, topics, `help.css`, `card.css`. Matches. PASS.
7. Screenshots (opened each, in `evidence/`, taken at e317196, carried or not): `help-all-projects.png` now shows `/home/me/planning` (made-up), no username or home folder: PASS. `help-en.png`, `help-fr-detail.png`: as claimed, no home path. `help-360.png` (taken before the bar fix): shows an open card, a detail, and the bottom bar clipped at "Configu"; it shows the old, fixed behaviour, not the head's; its detail is open but the bar claim of this picture is stale. All four pictures are of e317196 (files dated 2026-11-21 23:58, before the fix and the rebase), not of 60aacc1; and none is attached to the PR (below).
8. PR description as posted (`gh pr view 411`, headRefOid 60aacc1): FAIL. It still says in Known gaps "No screenshots of the page yet, and no manual run in a browser of the open/close and history checks" and in Deliverables "Screenshots ... are owed", although the evidence and the history check now exist; the Test plan still holds `<sha7>` placeholders and "Evidence: none yet"; no image is attached. `work/pr-body.md` is the same stale text (dated 2026-11-21 23:58). Also, the PR's file list (`gh pr view 411 --json files`, 31 files) holds files the Summary, Deliverables and Changes never mention: `docs/web-board.md`, `docs/web-board/batch-*.png`, `panel-pc.png`, `css/batch-nav.css`, `css/views/batch.css`, `js/views/batch-head.js`, `js/views/batch.js` (the batch title row, commits 512620ed, 62e80eea, c1b52ac6, which sit between main and this CR's own commits 98559806, 3204d55f, 60aacc1d; base is main). Either the PR is stacked on another CR and its base is wrong, or the description must name them.
9. Review box: placeholder `<sha7>` in the posted body; not checked.

## Failed

- PR description is stale and unclean: Known gaps and Deliverables say the screenshots and browser run are owed, Test plan holds `<sha7>` placeholders and "Evidence: none yet", no image attached (claim 8, with the unmentioned batch title-row files in the PR's diff).
- Evidence pictures are of e317196, not of 60aacc1 (claim 7): `help-360.png` shows the pre-fix clipped bar; retake the four at the head, with made-up paths, and attach them.

## Description pass, head 60aacc1db6243b447659f32357906624bf97aaff (later pass; supersedes the NOT VERIFIED above)

- Images: `curl -sI` on the four permalinks (media.githubusercontent.com, surface commit 6c8621af): help-en, help-fr-detail, help-all-projects, help-360 each `HTTP/1.1 200 OK`, `Content-Type: image/png`. Opened each: they are the retaken pictures (Help page, shop-api / planning-surface demo, path `/home/demo/...`), no real username or home path; help-360 bottom bar shows Help..Configuration, none clipped. Captions name 60aacc1.
- No placeholder (`<sha7>`, SCREENSHOTS) left in `gh pr view 411 --json body`.
- Test plan SHAs: `gh pr checks 411`: check macos/ubuntu/windows, eval-dry-run, scenario (ubuntu) all pass (run 44998544025). Description says CI green at 60aacc1: true.
- Known gaps: `git log --oneline origin/main..HEAD` holds 512620ed, 62e80eea, c1b52ac6 (CR-435 title-row commits) then 98559806, 3204d55f, 60aacc1d. `git log origin/main | grep 512620ed` count 0 (main lacks them). `gh pr view 408`: OPEN, "feat(board): the Batch page's mode and legend move into the title row". `git diff --name-only origin/main...HEAD | wc -l` = 31: the explanation is true.
- Claims vs code: carried from the earlier pass of this file (same head, code claims passed).

Verdict: VERIFIED
