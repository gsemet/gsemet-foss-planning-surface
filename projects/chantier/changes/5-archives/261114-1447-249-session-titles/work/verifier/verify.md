# CR-249 verify

Head: 3c41c3661ef5db085b13cf80fd953aa616da7dfa

All claims judged at 3c41c3661ef5db085b13cf80fd953aa616da7dfa (worktree HEAD, equals `gh pr view 192` headRefOid).

1. Diff matches the spec file by file. `git diff 894806a HEAD`: 7 files (session-start, chief-of-staff, concepts, docs/use-cases, RUNBOOK, test_cli_runs, run_scenario). Parts, table, examples and reason line are in session-start section Titles; Foreman prompt title and the direct CoS title (open --direct / close --yes) in chief-of-staff; agents/, CLI and board untouched. OK.
2. Old forms absent: Grep of `\[Chief of Staff\]|\[Chief of Staff - Batch|Foreman - Batch|\[Griller\]|Project \[role\]|- Direct\]|\[env\] Project` excluding `.agents/**`: 0 matches. OK.
3. Seat fixture round trip: `uv run --locked pytest skills/chantier/scripts/cli/tests/test_cli_runs.py -k seat` gives `1 passed` (title `[Mac] 💬 Proj · CoS` in and out of the `seat` line). CI `gh pr checks 192`: just check macOS, Ubuntu, Windows pass; eval-dry-run pass; just scenario (ubuntu) pass at this head. Long gate waived by the user for batch-17 (CI replaces it; Driver note). OK.
4. Scenario fixtures: both `[remote] proj [Chief of Staff]` became `[Remote] 💬 Proj · CoS` (run_scenario.py hunks at 1158 and 1445); `[remote] surface` untouched. OK.
5. Not applicable: CR-222 board state `seat.title` (CR-222 not on this base; fixture text checked in 4); CR-228 demo `seat.json` (not on this base).
6. PR description (posted, `gh pr view 192 --json body`): renders, emoji and `·` intact; Summary, Deliverables, Changes match the diff; Known gaps lists the no-migration point; no UNVERIFIED claim, no STALE. Test plan still holds the `SHA7` placeholders and unchecked Review/Verified/CI boxes: the Driver fills them (not a content failure). Review: `log 249` has "r1 approved at 894806ac... committed as 3c41c36", matching the later box once filled.

Evidence pairs: none (docs/cards only, no UI); no before-after.md owed.

VERIFIED

## Description pass at 3c41c3661ef5db085b13cf80fd953aa616da7dfa

- Body fetched with `gh pr view 192 --json body,headRefOid`: head 3c41c36, layout matches pr-template.md (Summary, Deliverables, Blast radius grade 1, Autonomous decisions, Known gaps, Details with Changes/Human decisions/Impacts/Test plan/Internal references). Changes list matches the 7-file diff checked earlier.
- Test plan SHAs all 3c41c36; no placeholders left. Review box: `log 249` has "r1 approved at 894806ac..., committed as 3c41c36". CI box: `gh pr checks 192` shows 5 pass (macOS, Ubuntu, Windows check, eval-dry-run, scenario); run 43599839469 headSha = 3c41c36. Evidence box: search done in the earlier pass (0 matches). Verified box: earlier VERIFIED at same head.

VERIFIED
