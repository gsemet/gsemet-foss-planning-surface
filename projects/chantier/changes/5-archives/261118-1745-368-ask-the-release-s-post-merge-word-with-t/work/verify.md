Head: 73f246fd21ab143f2d192c32009045038cb4bfba

Each claim judged at 73f246fd (head).

1. release_go change (rails_release.py): `git diff 380eca4f HEAD -- rails_release.py` shows `if c.pr and not granted` -> merge kept, then `if c.pr: why = granted_why` ahead of merged_pr/procedure/approvals; budget/fix refusals untouched; approval spending untouched when no PR. Docstrings of release_go and commands/release.py updated. Matches spec.
2. New test fails on base: detached worktree of 380eca4f with head's test file copied in, PYTHONPATH on base src:
   `pytest test_rail_refusals.py -k merge_go` -> `1 failed, 1 passed`; failing case [True]: `go: merge https://example.com/pr/9 (the user approved: tag v1)` (no "without asking"). At head: `2 passed`. Worktree removed.
3. `just test` at head: `629 passed in 30.49s` (within budget).
4. Cards: diff read against spec sections 1-3. chief-of-staff.md Releases paragraph holds When / ready line / leaves out / recording / no word / redo / wait before and after / auto; the approval-ask line says order approve before or after merge, confirm only for no-PR procedure; the two ready-ask paragraphs (ready-to-merge, stack complete) carry the clause. foreman.md: take note with approved list from `approvals unused:`, held (wait), grant spends none, order done for approve on ready release, blocked keeps take. driver.md: bullet rewritten with five sub-bullets, publication bullet kept, top bullet gains "spends no approval". All present.
5. Scenario: run_scenario.py diff shows Foreman._order skip for approve on ready release, candidates skip, BACK_NOTES skips `wait:`, release unit hand loop narrowed to non-approve plus a no-Driver check and the grant-merge-go check, release_on_stack check 9 extended and six checks (14.) added; README release bullet extended, `(unit: release)` kept. CI `just scenario (ubuntu-latest)` pass at head (run 44357847812).
6. agents/ unchanged: `git diff --stat 380eca4f HEAD -- agents com.github.copilot | wc -l` -> 0.
7. CI at head: gh pr checks 333: check macos/ubuntu/windows, eval-dry-run, scenario all pass.
8. PR description: read via gh; renders, Summary/Deliverables/Changes match the diff, Known gaps present, no image, no internal role names. Review box `approved at 73f246f`: log note "r1 approved at 380eca4f..., committed as 73f246fd" proves it.
9. Not run by me: just check / eval-dry-run locally (CI green at head).

VERIFIED
