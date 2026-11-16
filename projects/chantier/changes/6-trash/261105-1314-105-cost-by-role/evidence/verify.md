# CR-105 verify
Head: cd7cb117624c600f4eee4c7c4aebc558a85e9caa
1. One line, Foreman / Drivers / workers with amounts and shares, from parent links: diff of commands.py `_cost_summary` read; fixture output: Foreman $0.33 (26%), Drivers $0.67 (51%), workers $0.31 (23%) (fixture-split.txt).
2. Amounts add up to total and shares to 100: 2000 random transcript-row fixtures through _cost_summary, bad 0 (fixture-split.txt).
3. Scenario asserts it on fake transcripts (worker added under each Driver): gate log work/gates/20261105-131430.log, github and gitlab 158/158 passed.
4. Old line gone: git grep "orchestration" only hits plugin keywords; status/STATUS.md/cost share _cost_summary; README, docs, cli help updated.
5. CI green at head (per caller). Nit: one blank line before `def cost` instead of two in commands.py (style only; CI green).
VERIFIED
