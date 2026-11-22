# Verify CR-439 (Help page)

Head: 5569703b28fc0dd9a3f33330f02ddd261c3d8071

All claims judged at 5569703b28fc0dd9a3f33330f02ddd261c3d8071 (worktree clean, equals PR #411's headRefOid).
Verdict: VERIFIED

## 1. Help page in a real browser (Playwright, Chromium, the worktree's code, demo surface of scripts/docs_screenshots.py)
Script: work/scratch/v.py (unpublished). Result, at 5569703:
- 1400 px en: no horizontal overflow; sidebar `Home | Inbox 3 | Help | Triage | Kanban | Batch | PRs | History | Costs | Dashboard | Configuration`; headings `Help / Concepts / Roles`.
- 1400 px fr: sidebar `Home | Boîte de réception 3 | Aide | ...`; headings `Aide / Concepts / Rôles`.
- 360 px en and fr (is_mobile): `overflow False`; same headings; html lang en / fr.
- Bottom bar at 360 px: en `Home / Inbox / 3 / Help / Triage ...` scrollWidth 568 > clientWidth 360 (scrolls sideways, page itself does not overflow); fr 688 > 360. Inbox is second, Help third.
- All 25 topics opened (`&h=<id>`) at 360 px in en and fr: no page overflow for any ("OVERFLOW at" never printed).
- Console errors and page errors over the whole run: `errors: []`.
- (First loads were timing-sensitive in my first attempt only because of a script error; the final run shows Help on the first page.)
Captures: work/verifier/evidence/v-1400-{en,fr}.png, v-360-{en,fr}.png, v-360-{en,fr}-detail.png.

## 2. Links are real
Per language, 16 distinct "Read more" links (rel noopener, target _blank), all `https://github.com/gsemet/chantier...`. Targets exist at the head: docs/{agents-and-models,boards,costs,gates,planning-folder,planning-modes,use-cases-foreman,use-cases}.md are files (`ok` each); anchors exist: README `## Batch modes`, `## Change Requests Lifecycle`, `## Detailed lifecycle`, `## Releases`; docs/use-cases.md `## Choose your configuration`, `## The life of a batch`, `## Turn ideas into ready work`, `## A Chief of Staff and Grillers in remote`. French link text `En savoir plus (page en anglais)`.

## 3. Tests at 5569703
`pytest tests/test_board_help.py tests/test_board_design.py tests/test_code_targets.py -q` -> `44 passed in 3.17s`.
work/check4.log (13:03, commit time 13:03): `1925 passed, 20 skipped` and release-notes ok (just check). The dropped assertion is present (test_board_design passes). `just eval-dry-run` is the Driver's log note (19 of 19), not rerun by me; the diff is not under the CLI's src/ python or eval kit, so it is not owed.

## 4. Evidence screenshots (the four in evidence/, opened as images)
- help-en.png: Help selected in the sidebar with Inbox 3 under Home, 12 concept cards, "Batch and slots" detail open with Read more and Close. Matches the claim.
- help-fr-detail.png: Aide, Boîte de réception 3, "Grill et spécification" detail, French text and "En savoir plus (page en anglais)".
- help-all-projects.png: All projects: Home, Inbox 3, Help only; roles group visible.
- help-360.png: 360 px, bottom bar `Home, Inbox 3, Help ...` with the rest cut at the edge (scrolls), detail in the middle.
No username or home folder visible (paths shown: `/home/demo/planni...`). Permalinks (surface commit 970397e7) for all four: `curl -sIL`: `200 image/png` each.

## 5. PR description (work/pr-body.md)
Summary, Deliverables, Changes, Autonomous decisions match the diff (`git diff --name-only <base> HEAD`: 19 files: help views/topics/i18n/css, router, store, main, host, registry, icons, shell.css, card.css, DESIGN.md, test_board_help.py, test_code_targets.py; the body says 20 files "files" count; `gh pr view 411` reports 19 files: minor miscount, not a claim of behaviour). SHAs named are 5569703. Review/Verified/CI boxes are unchecked, as stated. No role term issue (product terms of a Help page about the roles).
NOTE: the body currently posted on the forge (`gh pr view 411`) is still the 60aacc1 one (diff against pr-body.md shows `60aacc1` and the old permalink 6c8621af): the Driver must post pr-body.md before ready. Judged here: the file, not the posted text.
Minor: "Known gaps: None ... (20 files)" should say 19 (forge count).

## 6. Review box
Unchecked, so no claim to judge. `$CHANTIER log CR-439` shows no approved-pass note at 5569703 yet (inspector phase started at 12:08:33).

## 7. Gate
No long gate pass at 5569703 (`ship` says so); the pipeline's scenario job is the long gate (AGENTS.md); not run by me.

VERIFIED
