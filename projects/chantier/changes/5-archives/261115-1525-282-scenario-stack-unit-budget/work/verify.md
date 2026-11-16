# Verify CR-282

Head: c983b93650bf50958085d63223efdcba7dcab3e9

Claims, each judged at c983b93 (round 3 moved the head from e1919e1 by one literal):

1. Spec route "set the budget from fresh measures": `git diff origin/main...HEAD -- scenario/run_scenario.py` shows `UNITS["stack"]` 320 -> 640. Fresh `--jobs 4` times: `grep -n '| stack' work/gates/full4.log work/gates/after-full.log` gives 510.8 s and 480.4 s (README run A 440.2). 510.8 x 1.25 = 638.5, rounded 640: the README's rule. Holds. Hang timeout max(600, 4 x 640) follows by the existing formula, not edited.
2. Every full-run time (440.2, 480.4, 510.8 s) and solo times (264.4, 277.5, 381.0 s; after-stack-1/2.log) are under 640, so no `WARN stack (github)` is expected at the new literal; those logs were taken at the 320 literal, the only change since is the literal (carried from e1919e1: the code path is untouched). 129/129 checks in each. Holds.
3. Round 1 code (in-process commit ids, remove_tree first try at once): diff read at c983b93; checks count unchanged, 129/129 per run. Holds.
4. README refreshed: `sed -n 36,62p scenario/README.md` shows the 640 budget, the lead sentence (date, machine, load), two full runs with every row. Holds.
5. `pytest skills/chantier/scripts/cli/tests/test_scenario_coverage.py -q`: `1 passed`. Only scenario/README.md and run_scenario.py change (`git diff --stat`), as the spec allows.
6. CI at c983b93 (`gh pr view 238 --json statusCheckRollup,headRefOid`): head c983b93650..., 5 of 5 SUCCESS, the ubuntu `just scenario` job being the long gate.
7. PR description (forge): renders, matches the diff (stack_batch, remove_tree, 640 budget, README). Review box 9d4136c matches the log note `r1 inspector approved at 9d4136c`. Known gaps lists the two real gaps. Nit, not a failure: the Test plan's Evidence line says per-case "After" times are still to add.

VERIFIED
