# CR-262 verify, round 1

Head: 93a67aa8c55da651fd2ee5326cc3c75e3d5ab63e (93a67aa). Base: 33fc800 (detached worktree `C:\Users\gaeta\Projets\chantier.worktrees\verify-262-base`).
Verdict: NOT VERIFIED (one claim fails: C3, a selected Triage card keeps a blue border).

Method. A headless Chromium (Playwright) drives `chantier board` of each checkout on throwaway copies, in the scratchpad, never on the repo's planning folder: `real` = a copy of this repository's `.agents/changes` (minus images; batch-18 running, 147 merged), `demo` = a copy of each checkout's `docs/demo` (mobile-app: no batch running). Scripts: `work/verify-shoot.py`, `verify-extra.py`, `verify-title.py`, `verify-sel.py`. Facts: `evidence/facts-*.json`, `evidence/extra-*.json`. Screenshots: `evidence/<view>-<lang>-<source>-<before|after>-<sha7>.png`.

| # | Claim | Result | Command / output (at 93a67aa unless "base") |
| --- | --- | --- | --- |
| 1 | `just check` passes | PASS | `just check`: ruff 168 files formatted, mypy no issues in 147 files, `uv lock --check` ok, biome "Checked 98 files ... No fixes", `100 passed in 35.79s`, release-notes ok |
| 2 | A1 seven columns, EN | PASS | real: Inbox 0, Backlog 12, Grill 3, 3-ready 0, In progress 7, Handed back 3, Done 147 (20 drawn, foot "127 more"); demo: 3,2,1,1,0,0,4. Base real: Intake, Grill 15, 3-ready, In progress, Handed back (5 columns, no Done) |
| 3 | A1 FR: no English name for progress, handed, done | PASS | demo FR: Inbox, Backlog, Grill, 3-ready, En cours, Rendus, Terminé; empty word "vide"; count line "7 items · 4 mergés" (Inbox, Backlog, Grill, 3-ready are the spec's own names) |
| 4 | A1 Grill holds spec-stage items; Inbox holds raw inbox | PASS on data present | demo: Inbox 3 raw, Grill 1 (crash-on-launch, has 02-answers). Real copy now holds 3 grill items (not the 15 of 2026-11-14): the plan's fast-scenario etc. are merged/in batch, so the "Grill = fast-scenario, baseline..." shot cannot be taken (the PR says so) |
| 5 | A2 priority filter: 5 toggles, P3+P4 off hides only their items | PASS | `pf_present` = inbox,P1,P2,P3,P4. Real: Backlog 12 -> 3, Grill 3 -> 1; Inbox, 3-ready, In progress 7, Handed 3, Done 147 unchanged. Demo: Backlog 2 -> 1; priority tags left: Inbox,P2,P1,3-ready,CR-*; FR label "Priorités" |
| 6 | A3 header figures equal the column counts | PASS | real head: header "0 inbox, 3 in grill, 7 in progress, 3 handed back" = columns 0/3/7/3; unchanged after the toggle. Home shows 6 working + 1 queued = 7. Base real header "15 in grill" = old Grill |
| 7 | A4 title prefers summary.json | PASS | demo copy with `deep-links/summary.json` title "SUMMARY TITLE differs from request" (request.md heading "Open product links in the app"): `verify-title.py` head -> `P2 deep-links => SUMMARY TITLE differs from request`; base -> `Open product links in the app`. (cr-folder-self-contained is now a batch CR, not a backlog item: it cannot show the case on the real folder.) |
| 8 | B1 Costs earlier batches, click unfolds / folds | PASS | real: rows batch-17 ... batch-01 (17), click batch-17 -> 32 CR rows, second click -> 0. Demo (no batch running): rows batch-02, batch-01; unfold 2, refold 0 |
| 9 | B1 no batch: "No batch running" plus table and last merged | PASS | demo-mobile-after Costs shots EN and FR |
| 10 | B2 Home: Earlier batches block, activity names last closed batch, merged CRs with batch | PASS | demo Home: "No batch is running. Last closed batch: batch-02, 2026-06-12, 2/2 CRs merged, $16.25."; Earlier batches lists batch-02, batch-01 with "see the costs"; Last merged shows batch-02/batch-01 beside each CR, without the "Change Specification:" lead. Real: block present while batch-18 runs (activity block shows the running batch, as specified) |
| 11 | B3 In grill tile, non zero, "{n} specified" | PASS | real: In grill 3 "0 specified"; demo: In grill 1 "0 specified" (the one grilled item is at stage grill, not spec). Tile is not zero |
| 12 | B4 Waiting for you counts blocked CRs only | PASS | tile "0 blocked CRs" in EN, "0 CR bloqués" FR; `asks_unread` removed from `waitingForYou` (diff of model/semantics.js). The "44 questions" figure: tried, not reproducible (0 unread asks in the copy) |
| 13 | B5 Home stuck on "Loading..." | NOT REPRODUCED | tried once more: 8 fresh headless loads of Home/Kanban/Triage/Costs, EN and FR (new browser context each, no cookie): Home drew every time. Consistent with the PR's Known gap; no refresh change |
| 14 | C1 Triage card = Kanban card | PASS | Triage card html is `class="card pi"` with `.row-tags`, `.ttl`, `.desc`, `.meta` and the stage word; screenshots triage-*-after |
| 15 | C2 hover tilt and lift, drag fade, drop targets | PASS | hover `transform: matrix(0.999945,-0.0104718,0.0104718,0.999945,0,0)` (= rotate(-0.6deg)), shadow `rgba(30,30,50,0.12) 0 6px 16px`; drag P3 -> P4 on a demo copy: P4 gains `app-icon-refresh`, folder moved (`git status`: D P3/app-icon-refresh, ?? P4/), journal line `{"kind":"move","items":["app-icon-refresh"],"text":"app-icon-refresh: priority P3 -> P4"}`; `.pi.drag` count 0 after the drop. Note: a drop on the middle of a row that already holds a card groups (existing behaviour) |
| 16 | C3 no blue outline on a selected card, still reads as selected | **FAIL** | `.pi.sel` outline is `none`, check mark and held shadow are present, keyboard `:focus-visible` ring stays (`solid 2px rgb(42,98,201)`). But the selected card keeps a blue 1px border: `verify-sel.py` -> `selected (click) {'border': '1px solid rgb(59, 111, 224)', 'outline': 'none', ...}` against unselected `1px solid rgb(230, 231, 234)`. Source: `web/css/widgets.css` lines 135-138 `.card.sel { border-color: var(--blue); box-shadow: 0 0 0 2px var(--halo); }` untouched by the change (blame: be83035). The screenshot `triage-selected-en-demo-mobile-after-93a67aa.png` shows the blue edge. The user's "détourage en bleu" is outline-like; Q4's default says "no outline, no blue". Base: `outline solid 2px rgb(59,111,224)` |
| 17 | C4 Triage word in both languages | PASS | sidebar shows "Triage" EN and FR |
| 18 | `status/views.py`, `STATUS.json`, hooks untouched | PASS | `git diff 33fc800 93a67aa --stat -- status hooks`: empty |
| 19 | Docs: web-board.md names columns, filter, tiles, earlier batches; demo batch records | PASS | docs/web-board.md lines 27, 42-50, 63; docs/demo mobile-app batch-01/02 present (Home and Costs shots show them) |

## Other observations (not failing)

- The sidebar project line still reads "0 in intake" / "en intake" (`project.line`, en.js:18, fr.js:18), and All projects keeps "Intake · grill" (`overview.*`, not toured). The spec renames `kanban.intake*` and `stats.intake` only, so this is not a failure, but the user's "should be called inbox" complaint still shows in the sidebar.
- The real planning folder no longer holds the grill items the spec names, so Inbox/Grill/Costs-no-batch shots come from the demo project (`docs/demo`, mobile-app), as the PR says. Real-folder shots (Kanban, Triage, Costs, Home) come from a copy of this repository's planning folder taken on 2026-11-15 with batch-18 running.
- The PR body's Test plan still says "UNVERIFIED: the long gate has not run"; the caller says `just scenario` passed at this head and CI is green, so the PR body is stale on that line (I did not re-run `just scenario`).

## Evidence

All in `C:/Users/gaeta/Projets/chantier/.agents/changes/4-batch/2-actives/262-board-ui-review/evidence/`:
- Real planning-folder copy: `*-real-before-33fc800.png` (base) and `*-real-after-93a67aa.png` (head) for `kanban`, `kanban-p3p4-off`, `triage`, `triage-hover`, `triage-selected` (head only meaningful), `costs`, `costs-unfolded` (head), `home`, each `-en-` and `-fr-`.
- Demo (mobile-app, no batch running): `*-demo-mobile-before-33fc800.png` and `*-demo-mobile-after-93a67aa.png`, same views and languages.
- Facts: `facts-<real|demo-mobile>-<before|after>-<sha7>.json`, `extra-*.json`.


# CR-262 verify, round 2

Head: 63a6138ad3526272daaecd2f4a6bb8c6239ed467 (63a6138). Move judged: 93a67aa..63a6138 (postit.css, en.js, fr.js). Verdict: VERIFIED.
Script: `work/verify-sel2.py` (headless Chromium on the head's `chantier board`, demo copy `mobile-app`). Output: `evidence/facts-sel-63a6138.txt`.

| # | Claim | Result | Command / output |
| --- | --- | --- | --- |
| 1 | `just check` passes at 63a6138 | PASS | `just check`: ruff ok, mypy no issues in 147 files, `uv lock --check` ok, biome 98 files no fixes, `100 passed in 23.62s`, release-notes ok |
| 16 | C3 a selected Triage card has no blue (EN and FR) | PASS | unselected `borderColor rgb(230, 231, 234)`, `boxShadow none`, outline none; selected (`card pi sel`) `borderColor rgb(230, 231, 234)`, `boxShadow rgba(30, 30, 50, 0.12) 0px 6px 16px 0px` (neutral held lift), outline none; same in FR. Previously `1px solid rgb(59,111,224)` + halo |
| 16b | check mark kept | PASS | `.pi.sel` contains `.chk` (EN, FR) |
| 16c | keyboard focus ring kept | PASS | focus + Tab/Shift+Tab: `:focus-visible` true, `outline solid 2px rgb(42, 98, 201)` (EN, FR) |
| 20 | sidebar line says inbox | PASS | EN `no batch · 3 inbox`; FR `pas de batch · 3 inbox` (was "intake"/"en intake") |
| other | all other claims (2-15, 17-19) | carried | carried from 93a67aa: the move touched only `.card.pi.sel` in postit.css and the `project.line` string; `git diff 93a67aa..63a6138 --stat` = 3 files, 4 insertions, 3 deletions |

Evidence: `evidence/triage-selected-en-after-63a6138.png`, `evidence/triage-selected-fr-after-63a6138.png`, `evidence/facts-sel-63a6138.txt` (the 93a67aa selected-card "after" shots were replaced).

# CR-262 verify, round 3 (move 63a6138..af97942, rebase onto c5e2498)

Head: af97942. Verdict: VERIFIED.
Judged again: the merged Kanban card and docs/web-board.md paragraph.
- kanban-cards.js: CR card keeps `${stateTag(c)}${nextTag(c)}` and the step span (CR-261), done card and shared item card from this CR; imports `nextTag, stateColor, stateTag` all used; `card.next` "next to start" key present in en.js. PASS
- docs/web-board.md line 45: seven columns, priority filter, and CR-261's sentence (step, "waits for the user", "next to start"); no conflict markers in the tree (git grep empty). PASS
- Gates given by the caller at af97942: just check, just scenario, CI green. Not re-run.
- Other claims: carried from 63a6138: unchanged by the move (round 2 VERIFIED; C3 border fixed in 3e3ec33, checked there).
