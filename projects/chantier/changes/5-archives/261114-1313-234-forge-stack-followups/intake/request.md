forge-stack follow-ups from CR-214 and CR-215

From batch-16's retro (points 10 and 11), reviewed by an advisor.

- CR-214 detects gh-stack by its folder, not by `gh extension list` as its specification says.
- CR-214's P10 reports 14 of 16 commands not allowed (it was 19 of 19): explain or fix the count.
- CR-215: the rebuild exits 2, not 4, after five unstack tries.
- CR-215: the stale-SHA regex matches all-digit tokens.
- CR-215: the batch-15 base case was not reproduced on the old code (the scenario covers it now).
- Lands: CLI and scenario; `just scenario` applies.