Head: 8566cca

# Verification of CR-233 (PR 173)

Verdict: VERIFIED

1. Reading pass. Grep "one action" in skills/chantier/references at 1cac70b: concepts.md:12, :108; foreman.md:161, :170, :220; chief-of-staff.md:387, :567, :572; driver.md:410. Each offers the one-PR-at-a-time merge beside it, or (foreman 161, 220, cos 572) refers to the user's merge action recorded after the fact, not a merge path. `is merged: no Driver` is found at driver.md:279 and foreman.md:233. concepts.md "Ready to merge" now holds in every mode, a verified stack is "a second way".
2. Consistency. driver.md:279 and foreman.md:233 quote `<cr> is merged: no Driver to hand it back`; CLI driver_checks.py:155 raises f"{cr} is {c.status}: no Driver to hand it back". Same text. The Chief of Staff card does not quote it (the PR body says so; the spec's own CoS items do not ask for it).
3. Per-card items present in the diff: CoS (ready ask on default branch mergeable now; "you can merge" only after ready/stack-ready; user merge before ready recorded with `order merged`; series and stack bullets; plan at the go); Foreman (stack start like parallel until the stack driver takes it; restack vs rebase notes; "merged early" line; the choice stated in one clause); Driver (end rule in "Your end"; Stack driver opening); concepts (Ready to merge, Stack).
4. Scenario check: scenario/run_scenario.py:3165-3175 (end of handback_proofs). Gate log work/gates/20261114-044912.log: "github: 696/696 checks passed", "gitlab: 677/677 checks passed", "result: pass at 1cac70b765f4ae618f9dea9233a493b201ea34e6". Transcripts scenario/results/github-20261114-050946.md:6195 and gitlab-20261114-052848.md:6125 show the new check ticked [x]. Only the log was read; no new gate started.
5. `git diff --stat origin/chantier/batch-17/cr-237-...HEAD`: scenario/run_scenario.py, chief-of-staff.md, concepts.md, driver.md, foreman.md only (73+, 19-). No CLI code, no agents/, no com.github.copilot/.
6. PR body (`gh pr view 173`, headRefOid 1cac70b): table by card, scenario snippet, Known gaps and Autonomous decisions match the diff. Test plan boxes for gates/review/verified/CI are still unticked: the caller ticks them.

Notes (not blockers): formatting of a few edited lines is ragged (long lines in driver.md 279-283, foreman.md 170, chief-of-staff.md 570-572, concepts.md 108-109). `handoff` exited 2 for me, so I read the gate log directly.

## Pass on the posted description at 1cac70b765f4ae618f9dea9233a493b201ea34e6
- `gh pr view 173 --json headRefOid`: 1cac70b765f4ae618f9dea9233a493b201ea34e6 (head unchanged).
- Posted body vs work/pr-body.md: equal after CRLF normalisation and trim (71 lines each, no diff).
- `gh pr checks 173`: 5/5 pass (check x3 OS, eval-dry-run, scenario) on run 43556874137.
- Audit (pr-template.md "The audit"): sections in order, Known gaps filled, one Details fold after Autonomous decisions holding Changes, Human decisions, Impacts, Test plan, Internal references last; CR name only in Internal references; role names only as product terms of card changes; Deliverables has table and code visual; Changes match diff (4 cards + scenario check); Blast radius one grade; Test plan boxes carry SHAs matching head.
verdict CR-233 VERIFIED (head 1cac70b)


## Second verification at 8566cca (move 1cac70b..8566cca, docs only)
Head: 8566cca
- Diff touched README.md, CONTRIBUTING.md, docs/use-cases-direct.md, use-cases-foreman.md, batch-modes(-texts), batch-pace.svg, release-driver(-texts): no code, cards or scenario.
- Read every changed line: each says a stack is merged in one action from the top PR or one PR at a time from the bottom, release last; README adds "a PR handed back ready is mergeable at once". Consistent with concepts.md "Ready to merge" and the cards.
- The three SVGs (batch-modes, batch-pace, release-driver) parse as valid XML.
- just check at 8566cca: ruff, mypy, lock, pytest 63 passed, release-notes ok.
- carried from 1cac70b: claims 1-6 (cards, consistency, scenario gate 696/696 and 677/677, diff scope, PR body), since cards, CLI and scenario are unchanged by the move.
verdict CR-233 VERIFIED (head 8566cca)

## Description pass at 8566cca
Head: 8566cca (gh pr view 173: headRefOid 8566cca; CI 5/5 SUCCESS; files list matches the Changes section; claims on gates, scenario check and SHAs true).
Failed claims (pr-template.md: no round in the body outside Internal references; audit item 3):
- Deliverables: "The docs (round 2): ..." names a round.
- Test plan, Review item: "round 2 (docs) approved at 1cac70b" names a round.
Minor: Human decisions "The change is delivered into the batch already running" is a batch reference, not a decision that shapes the change.
Fix: drop "(round 2)" and say "docs review approved at 1cac70b"; drop or reword the batch bullet.
verdict CR-233 NOT VERIFIED (head 8566cca)

## Description pass 2 at 8566cca
Head: 8566cca (gh pr view 173: headRefOid 8566cca; gh pr checks 173: 5/5 pass).
- The two round references and the batch bullet of the previous pass are gone: no "round", no CR/batch id, no `.agents/changes/` path outside Internal references; role names only as product terms of card changes; "batch" only as the product's own word.
- Sections in order, one Details fold, Human decisions matches 02-answers.md item 3, Known gaps filled, no Issues References (spec has no issue line).
- Changes list matches the diff (4 cards, 9 docs files incl. two -texts.md, scenario check); scenario snippet matches run_scenario.py handback_proofs; driver_checks.py claim matches; Test plan SHAs match the log (gates 1cac70b, docs just check 8566cca, review 1cac70b committed as 8566cca).
Head: 8566cca


## Restack verification at e894eb3 (move 8566cca..e894eb3, rebase onto main febd917)
Head: e894eb3 (gh pr view 173: headRefOid e894eb31ec42..., MERGEABLE)
- `git range-diff origin/main...8566cca origin/main..HEAD`: fe01dae vs 1cac70b differs only in context lines of chief-of-staff.md (main's floor/delivery-time wording from 4c1dd31); e894eb3 vs 8566cca is `=` (identical patch). No conflict markers in skills/chantier/references (Grep).
- `rg`-equivalent Grep: `is merged: no Driver to hand it back` at driver.md:279 (foreman.md carries it as before, in the unchanged patch).
- `just check` at e894eb3: mypy ok (77 files), uv lock ok, pytest 63 passed, release-notes ok.
- Claims 1-6 (cards, consistency, scenario 696/696 and 677/677, diff scope, PR body) carried from 1cac70b/8566cca: the patch is identical; main's only new content is a chief-of-staff floor paragraph, not touched by this CR. CI at e894eb3: check x3 pass, eval-dry-run pass, scenario pending when read.
- Description: the body still says "Verified/CI green at e894eb3 (pending)" boxes, which the caller ticks; no round or CR id outside Internal references.
verdict CR-233 VERIFIED (head e894eb3)
