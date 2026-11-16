# Before / after

Before (base origin/main): `cost` refuses on a model with no price ("no Claude price for model ..."). After (6590219): `at least $X over N priced model calls; 1 calls of mystery-model not priced`.
Not captured as separate files: the pair is exercised and asserted by `just scenario` (steps in scenario/run_scenario.py, `unpriced_model`), passed at 6590219 (work/gates/20261111-191010.log). Reproduce: `just scenario` in the worktree; the before is the removed refusal case in tests/test_costs.py on the base.
