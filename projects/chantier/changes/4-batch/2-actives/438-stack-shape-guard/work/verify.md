# Verify CR-438

Head: e4199b7f136933e037f2c0eacbe9405cf24c6f6c

Local worktree head (not pushed), clean tree. Description pass not done (PR on the forge is at an older head).

Claims, all judged at e4199b7:

1. Criterion `shape_blockers` (chain order; other CR's PR; stacked incl. self; fix, held, merged, cancelled ignored), refusal text, `--outside-stack` (Q14 order check, exit 1 texts, recorded text and `outside_stack` event), no refusal of other asks or non-stack modes, guard for chain CRs only.
   Command: `uv run --no-sync --project . pytest skills/chantier/scripts/cli/tests/test_stack_shape.py skills/chantier/scripts/cli/tests/test_stack_due.py skills/chantier/scripts/cli/tests/test_plugin_files.py skills/chantier/scripts/cli/tests/test_startup_manifest.py skills/chantier/scripts/cli/tests/test_came_back.py skills/chantier/scripts/cli/tests/test_stack_chain_cards.py skills/chantier/scripts/cli/tests/test_release_tag.py skills/chantier/scripts/cli/tests/test_scenario_coverage.py -q`
   Output: `169 passed in 17.78s`. Code read in `stack_shape.py` and `rails_release.py` matches the spec text (note: `shape_blockers`, `next_step`, `shape_line` live in the new `stack_shape.py`, not `stacks.py`; `forming` is in `stacks.py`; behaviour as specified).
2. Shape line (exact empty-state line, `rules:` path ends every line and exists, `next` cases, `alone asks` values, none for parallel/series, `stack_due` unchanged): covered by `test_the_shape_line*` in the same run (passed), and by the scenario unit `stack`.
3. Cards: `foreman-stack.md` holds the five checks, `--outside-stack`, `shape: through the stack`, the final-order take, "again as before its first stack" with `"The first take"` in the same sentence; `foreman.md` links it, lost "A folded CR" and the final-order take, keeps "A held CR"; manifest `batch:stack`; `session-start.md` Reload names it; `chief-of-staff.md` holds the check and both qualifiers; `foreman-stack` in test_plugin_files card list. Proof: `test_the_shipped_cards` (passed in the run above) plus greps showing each phrase at its place.
4. Scenario: `uv run --no-sync --project . python scenario/run_scenario.py --unit stack --unit series-deps --unit qa-driver`
   Output: `ok stack (github): 228/228 checks`, `ok series-deps (github): 77/77`, `ok qa-driver (github): 77/77` (guard, shape line, flag, early_conflict stack case, no shape line on a plain status).
5. `just check` at this tree: passed per the Driver's brief (1924 tests); not rerun by me. `just eval-dry-run` and the pipeline's `just scenario` at the pushed head are not mine here.

Not judged: the PR description, images, the Review box (no pushed head).

VERIFIED
