Head: 3246872064d441e5a1a5916bc81cef87ffabd0f6

# Verify CR-409 typed waits, at 3246872 (full SHA above)

VERIFIED

## Claims judged at 3246872

1. Behaviour (spec 4 to 7, 9, 11.1). `uv run --no-sync --project . pytest skills/chantier/scripts/cli/tests/{test_waits,test_board_waits,test_forge_hub_waits,test_validate,test_startup_manifest,test_store_command_table,test_event_types,test_scenario_coverage}.py -q -p no:cacheprovider` -> `171 passed in 28.50s`. PASS.
2. AGENTS.md (spec 8, as replaced by the Chief of Staff's 2026-11-20 no-count decision): `git diff main...HEAD -- AGENTS.md` shows "Four named" -> "Named", Third/Fifth ordinals, `wait` item, hub and budget sentences extended. PASS.
3. Review box: `chantier log CR-409` has "r4 inspector approved at 3246872064d4..." (14:38:59Z), the SHA the box cites. PASS.
4. PR description as posted: `gh pr view 380 --json headRefOid` = 3246872064d441e5a1a5916bc81cef87ffabd0f6; the body's SHAs (lines 80-84) all read `3246872`, none stale; body equals work/pr-body.md (diff: one trailing blank line). Summary, Deliverables, Changes match the diff (45 files); Known gaps hold the GitLab approval gap, test-time growth (inbox item), fakes, scenario budgets. No image. PASS.
5. Long gate at 3246872: `gh pr checks 380`: check macos/ubuntu/windows pass, eval-dry-run pass, `just scenario (ubuntu-latest)` pass. PASS.
6. GitLab approval proof (spec 5.3): not shipped, accepted, in Known gaps with the inbox item. PASS.

## Evidence

No visual change, no pane change, no screenshot owed. After = claim 1's output at 3246872.
