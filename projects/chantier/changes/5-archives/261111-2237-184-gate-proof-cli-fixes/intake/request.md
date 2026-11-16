Gate proof and small CLI fixes (batch-11 retro; folds the inbox items gate-log-commit, driver-budget-refusal and undrop-cr).

1. The gate log does not record the commit it ran at, so a Verifier cannot prove the long gate passed at the pushed head (CR-179). `gate` should record the head commit it ran at, and `handback ready` (or the Verifier) should check that the passed gate matches the head being handed back.
2. `driver.md` says `round` is refused past the budget, but the CLI refuses only on the round limit (found by CR-176). Make the card and the CLI agree; recommended: the CLI also refuses a round once the batch budget is spent, as the card says.
3. There is no CLI way to bring a dropped (6-trash) or abandoned CR back to the inbox; today it needs a hand move. Add one.
