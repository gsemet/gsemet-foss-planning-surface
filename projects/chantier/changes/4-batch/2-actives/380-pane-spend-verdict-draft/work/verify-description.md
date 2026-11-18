# Verify CR-380 PR description (description-only pass)

Head: 924d0d713866bdc5122e1ef381d4a77645040276

Judged at 924d0d7 (`gh pr view 343` headRefOid = the head; worktree HEAD the same). Body read from `gh pr view 343 --repo gsemet/chantier --json body`. No verdict command recorded for this pass.

- Audit 1-2 (sections, order, fold): Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps visible in order; one Details block holding Changes, Impacts, Test plan, Internal references; blank lines after summary and before the closing tag; nothing after it. No Issues References (spec: "No tracker issue"), correct. No images, so none to resolve and none can show a username.
- Audit 3 (internal refs): only "CR-380 pane-spend-verdict" in Internal references; no role names elsewhere. Pass.
- Audit 4 (Deliverables): text table visual, real names (`draft_clause`, `spend-age.js`, `Verdict` step) exist in the diff. Pass.
- Audit 5 (matches the diff): `git diff origin/<base>...HEAD --stat` (base = chantier/batch-28/cr-377-...) lists 15 files: docs/boards.md, hooks/register.tsx and test, types, scenario/run_scenario.py, web board js (spend-age, batch, home-batch, i18n en/fr), driver.py, stacks.py, status/steps.py, status/words.py, test_cli_units.py. Each is named in Changes. Wording in the body matches words.py/stacks.py (`PR in draft: its PR <pr> is out of draft on the forge; it waits on <cr> (<pr>).`; next line "Ready to merge once what is under it is." only when pr_draft is False). Pass.
- Audit 6-7: grade 1 with explanation; Autonomous decisions match 02-answers (cost_at age, shared helper). Pass.
- Audit 8: 02-answers holds no user decision (the user asked no questions); Human decisions correctly omitted.
- Audit 10 / Known gaps: names the missing pane screenshot and the web board screenshots; Evidence box says none captured with the same reason. Pass.
- Test plan SHAs: all `924d0d7`. Review box: `$CHANTIER log` has "r1 approved at 8a88c556, committed as 924d0d71" (cites the round's committed SHA). Verified: verify.md at 924d0d7. CI: `gh pr checks` all 5 jobs green at 924d0d7 (per the brief; PR head confirmed).

VERIFIED

## Second description pass (images added)

Head: 924d0d713866bdc5122e1ef381d4a77645040276

Judged at 924d0d7 (`gh pr view 343` headRefOid and worktree HEAD both 924d0d713866bdc5122e1ef381d4a77645040276; tree clean). Body re-read with `gh pr view 343 --json body`; only change vs pr-body.md is the two image URLs replacing the relative paths.

- Images resolve: `curl -sL` of both user-attachments URLs gave `200 image/png` (133041 and 195044 bytes).
- Look, image 1 (home batch card): opened as an image; shows the shop-api fictional demo, English, batch-03 card with muted "computed 3 min ago" under Spent $63.18 / $120.00. No username, no local path, no home folder.
- Look, image 2 (Batch page): shows "$63.18 of $120.00 · computed 3 min ago" in the Spent card; fictional demo, English; no username or path.
- Claims vs head: `batch.spent_age` = 'computed {age} ago' in `i18n/en-batch.js`; `js/model/spend-age.js` exists. The Deliverables text "of $20" is the format example, the demo shows $120.00: not a contradiction.
- Evidence box and Known gaps now name only the missing pane screenshot, consistent with the images present. Sections, fold, internal refs, Changes vs diff, Review box (log: "approved at 8a88c556, committed as 924d0d71"), SHAs: carried unchanged from the previous pass.

VERIFIED
