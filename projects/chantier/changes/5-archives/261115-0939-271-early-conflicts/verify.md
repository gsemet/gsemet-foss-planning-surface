# Verify CR-271

Head: 97f8bf1530b40864b29aeba3c30ab3b389d1b74d

Verdict: VERIFIED

- Cards vs spec (97f8bf1): git diff origin/main...HEAD touches foreman.md (+49), chief-of-staff.md (+11), run_scenario.py, scenario/README.md, docs/use-cases-foreman.md; pr-body.md matches the diff (5 files, cards/scenario/docs only).
- `just scenario --unit series-deps` at 97f8bf1: series-deps (github) 73/73 checks, 421 commands. WARN only: 316.7 s over its 260 s budget (machine load; a budget warning, not a failure; the PR body says the section was kept in this unit for the unit count).
- Audit: evals/kit/audit.py:88 GIT_WRITES = git("commit|push|rebase|merge") + r"\b(?!-)"; run: `git merge-tree --write-tree a b` -> no match; `git merge --ff-only` -> match.
- `git diff --stat origin/main...HEAD -- hooks types commands agents com.github.copilot rails.py`: empty. No just mod needed.
