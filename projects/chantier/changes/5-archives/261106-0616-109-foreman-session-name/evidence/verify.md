# CR-109 verify

Head: 1e178a5db0692c347facabc530a53c9af73c02ce (worktree cr-board-CR-109)

1. Claude Desktop title. `git diff origin/main` shows `title: "<your title> - Foreman [batch <NN>]"`, with `<your title>` taken from `get_session("self")`. PASS.
2. Copilot title. The diff shows `title: Foreman [batch <NN>]`. PASS.
3. `<NN>` is defined as the two-digit number of the batch folder `3-requests/<NN>-<batch>/`, as `open` prints it. PASS.
4. Scope. Only `skills/chantier/references/chief-of-staff.md` changed (1 file, +7 -5); no prompt, CLI, agent or test change. PASS.
5. `grep -n "Foreman <batch>" skills` (Select-String over skills/**) finds nothing. PASS.
6. `just check` in the worktree: 26 passed. PASS.
7. `just scenario`: not rerun; the Driver's long gate passed at 1e178a5 and CI is green on PR 46 (per the prompt).

VERIFIED
