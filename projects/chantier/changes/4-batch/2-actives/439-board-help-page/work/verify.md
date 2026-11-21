# Verify CR-439 (Help page)

Head: e317196e2c35d4f4cf40d0234341397123f2952d

Verdict: NOT VERIFIED (two failed claims: the phone's bottom bar, the "All projects" screenshot).

Method: a throwaway surface (git repo, projects `demo` and `other`) under `work/scratch`, served by `chantier board --host 127.0.0.1 --port 0 --ui <worktree>/.../clients/web` from its folder (never the live surface or 127.0.0.1:8765); real Chrome headless driven over the DevTools protocol by my own script `work/scratch/ver.py` (log `work/scratch/ver.log`, second probe `ver2.py`/`ver2.log`). Board stopped, Chrome profile and throwaway surface deleted afterwards. All claims judged at e317196.

## Claims

1. Tests at e317196. Command: `pytest -q tests/test_board_design.py tests/test_code_targets.py` (in the CLI folder). Output: `33 passed in 3.66s`. PASS.
2. Sidebar: Help right after Home, no count (`ver.log`, "sidebar views"): `["home:Home","help:Help","triage:Triage0",...]` (Triage and Kanban carry counts, Help none). PASS.
3. History rules (help-Q14), from Home then Help, real Chrome (`ver.log`; `hs` is `history.state`):
   - (a) open `batch` (hs `helpOpen`, `h=batch`), close by Escape: `?p=demo&v=help`, length unchanged (6 to 6); Back: `?p=demo&v=home`. Same with the close button (8 to 8, Back: home) and with a second click (10 to 10, Back: home). PASS.
   - (b) open, Back: `?p=demo&v=help` no detail; Back again: `?p=demo&v=home`. PASS.
   - (c) open `batch`, then `grill` (`h=grill`, hs `helpOpen`, length 14 for both): Back: Help with no detail; Back: home. PASS.
   - (d) shared link `&h=batch` (loaded after about:blank, hs null): detail open; close button: `?p=demo&v=help`, length unchanged (14); Back: `about:blank`, never the detail. Escape and a second click close it in place the same way. PASS.
   - (e) open, reload: same detail (`h=batch`, hs `helpOpen` kept); close: Help no detail; Back: home. PASS.
   - an unknown `h=nope`: Help with no detail. PASS.
4. Every card (25 ids) opens (detail with paragraphs) and closes by a second click: `25 cards, failures []`. Enter opens, Enter on the open card closes, Space opens. Escape, button, second click, Back covered by claim 3. PASS.
5. "Read more" link: `["https://github.com/gsemet/chantier/blob/main/docs/use-cases.md#turn-ideas-into-ready-work","_blank","noopener","Read more"]`; French `En savoir plus (page en anglais)`. PASS.
6. "All projects": Help selected, title `Help`, no detail; sidebar shows Home and Help only. French detail renders on project `other` ("Batch et slots", chantier's names kept). Board stopped after the page loaded: a click on a card still opens the detail (`Grill et spécification`). PASS.
7. Diff against the specification (`git diff c5af034b HEAD`): registry entry after `home` with `offline`, no `count`; `host.js` ready for `offline`; `header.js` title; `router.js` `topic`, `topicOf`, `href`, the `helpOpen` mark, `replaceState(history.state ...)`, `closeTopic()`; `main.js` `configure(..., topicIds())` and Escape; store field; DESIGN.md section. Matches. PASS.
8. Phone bottom bar (spec open question 4 A: "if the bar no longer fits 360 px ... `.bnav` gets `overflow-x: auto`"). Command: `ver2.py` at 360 px wide. Output: `bnav {"cw":360,"sw":399,"ox":"visible","n":8,"lastRight":398.7,...,"labels":[...,"Costs","Configuration"]}`. The bar is 399 px of content in 360 px with `overflow-x: visible`; the Configuration button is cut off and cannot be reached, and `help-360.png` shows the clip ("Configu"). `css/shell.css` is unchanged by the PR (`git diff --stat c5af034b HEAD -- css/shell.css` is empty). FAIL: Help pushes the bar over its width and no overflow rule was added.
9. Screenshots (opened each): `help-en.png`, `help-fr-detail.png` (detail, "Read more" link, Fermer) and `help-360.png` show the page as claimed, with no username or home folder. `help-all-projects.png` shows, in the sidebar header, `C:/Users/gaeta/Proj...` (the home folder's path, with the user's name `gaeta`, truncated but legible): FAIL (privacy rule: capture again with a made-up path). `help-360.png` shows an open card but its detail is below the fold, so "a detail open" is not visible; the bottom bar shows the clip of claim 8.
10. PR description as posted (`gh pr view 411`, head e317196): renders, sections in order; Summary, Deliverables and Changes match the diff (no claimed change missing, none unmentioned). Its Known gaps say "No screenshots of the page yet, and no manual run in a browser", which is true of the posted body (no image is attached) but out of date against the evidence now in `evidence/`; Test plan still holds `<sha7>` placeholders and "Evidence: none yet". The Driver must update the body once the screenshots and the history check are attached (with the claim 9 capture redone). No role name outside the product's own terms. Not judged `NOT VERIFIED` on its own while it still says the screenshots are owed, but it must not ship so.
11. Review box: not yet in the posted body (placeholder); not checked.

## Failed

- Phone bottom bar overflows 360 px with Help, Configuration unreachable (claim 8).
- `help-all-projects.png` shows the user's home folder path (claim 9).
