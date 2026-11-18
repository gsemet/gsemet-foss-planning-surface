# Verify CR-374, first verification

Head: 4e0de99c2d9513b3464e238f45c12b201ce84f62

Gate: CI at this head, 5 jobs green per the Driver's note (`gh pr checks 336`, includes `just scenario` ubuntu); `just check` 635 passed per the PR's Test plan. Not rerun (brief). Review box: log has "r1 approved at c0bb193a, committed as 4e0de99c" (box cites reviewed c0bb193 plus this commit): matches.

## Claims (each judged at 4e0de99c2d9513b3464e238f45c12b201ce84f62)

1. Stale wording gone. `git grep -n -e "strict while running" -e "no CR joins" -e "batch is strict" -- docs skills` -> no output, exit 1.
2. Hard rule and subsection present. `git grep -n "A refusal is said before it is met" -- skills/chantier/references/chief-of-staff.md` -> lines 55 (the Hard rule) and 1475; `git grep -n "Refusals to say before they are met"` -> lines 62, 1473 (the subsection heading), 1593.
3. Advice wording gone. `git grep -n "prefer a numbered name\|the advice for subagent files" -- skills` -> no output, exit 1.
4. SVG and texts identical. Python check: SVG `<desc>` text is contained verbatim in `docs/batch-lifecycle-texts.md` -> True; the box title "direct mode: while running" is in the texts file -> True; the box lines in the SVG ("order add queues; order qa refused," / "no grill in this session") equal the texts file lines 76-77.
5. Direct box does not overflow: rendered with headless Chrome at 3x (Chrome `--screenshot` of an HTML crop of `docs/batch-lifecycle.svg`); screenshot `work/verifier/evidence/direct-box.png` opened and looked at: title and two lines sit well inside the 288-px dashed box, nothing clipped; no path, username or home folder on screen (the box holds only the made-up diagram text).
6. Rows A-H against code at this head:
   - A: `commands/orders.py` `_qa_row` refuses "a running direct batch takes no QA" (EXIT_PRECONDITION); grill-wait rule is in the card; `order add` queues per concepts.md line 180-181. Matches.
   - B: `orders_release.py` `join_release` voids the procedure word and makes the release wait; `check_release_open` refuses once the release has started, naming `order add --fix-for <rel>` or the next batch. Matches.
   - C: `hosts/claude-code.md` lines 379-391 and concepts.md "Starting an agent" paragraph (diff read). Matches; no code involved.
   - D: concepts.md lines 181-187 (cases, 5 min Copilot, `agents set <cr> - --epoch <n>`), `rails.py` `COPILOT_QUIET_SECONDS = 300`, `closing.py` docstring (refuses with or without `--yes`). Matches. (The row omits the `--stopped NAME` route for a held agent that stopped without hand-back; not a wrong statement.)
   - E: `orders_apply.py` `_confirm`: refuses while `_open_ids` (fixes aside) is not empty, and while `c.pr` is set (release PR not merged). Matches. Wording note: "or give it with the merge go of the release PR" reads as if the CLI accepts the word before the merge; it is asked with the merge go and recorded after the merge (`order confirm` is refused while the PR is unmerged). Minor, not a failure.
   - F: `lifecycle/stages.py` `_specification` message "missing Change Specification: ...; grill the CR first", with the `3-ready` + `intake/request.md` exception. Matches.
   - G: `rails.py` line 353-358 "round limit {limit} reached; hand back blocked, only the user grants more (`order rounds`)"; `records.round_limit` = granted rounds else the batch max_rounds (three by default per the card). Matches.
   - H: `closing.py` docstring: a model with no price does not refuse `close`, the final cost is a floor. Matches.
7. Parts 3 and 4 applied: `git diff HEAD~1` of `docs/use-cases-direct.md`, `docs/tutorial-claude-code.md`, `concepts.md`, `hosts/claude-code.md` read: each edit of the spec is there (strict paragraph replaced, "`order qa` does not, as above", line 114 trimmed, grill sentence added, tutorial line, rule at concepts 524-529, "follow the rule", host line with the concepts link). Hard rule bullet and the "What you accept while you steer" grill line (chief-of-staff.md ~1588-1595) are the three-part form.
8. Scope: diff of HEAD~1 touches 7 files, all cards and docs; no CLI, no `agents/` file.

## PR description (pr-body.md)
- Summary, Deliverables and Changes match the diff at the head; no unmentioned change.
- Fix needed before it is posted as final: Known gaps says "No rendered screenshot of the diagram's direct box" and the Summary carries an `**UNVERIFIED:**` line about it. The screenshot now exists (evidence/direct-box.png, at 4e0de99): attach it to the description (caption with the SHA 4e0de99) and drop that gap and that UNVERIFIED line, as the spec's Evidence asks. The Test plan's Evidence and Verified boxes are the Driver's to tick after this verdict.
- "Rows A to H were checked against the code; none needed correction": agrees with claim 6.
- No image is attached yet; none to look at on the description.

VERIFIED

## Description pass (judged at 4e0de99c2d9513b3464e238f45c12b201ce84f62)

Posted body read with `gh pr view 336 --repo gsemet/chantier --json body`; diff `git diff HEAD~1 --stat` (7 files: chief-of-staff.md, concepts.md, hosts/claude-code.md, 3 docs, SVG).
- Layout: Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps visible; one Details fold (Changes, Human decisions, Impacts, Test plan, Internal references), blank lines after summary and before `</details>`, nothing after. OK.
- Summary, Deliverables (rows A-H, direct-box text) and Changes match the diff; no unmentioned change. SHAs `4e0de99` correct (headRefOid 4e0de99c...).
- Image: user-attachments URL downloaded; md5 29d0c9f484a6ddf3ab7452ebfc47b85d equals work/verifier/evidence/direct-box.png (captured at 4e0de99). Opened: shows only the dashed direct box with diagram text, nothing clipped; no username or home folder. OK.
- Known gaps "None": consistent, no UNVERIFIED claim remains, all evidence captured. No STALE mark.
- Test plan: CI at 4e0de99 all 5 jobs SUCCESS (`gh pr view 336 --json statusCheckRollup`); Review box matches the log note (carried above).
- Roles named (Chief of Staff, card) are product terms of this change. Internal references only in the fold.

VERIFIED
