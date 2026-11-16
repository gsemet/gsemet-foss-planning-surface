Head: 404bd51456c0b0d5d7976626789f6408d7fe1d01 (worktree HEAD, clean)

Move judged: rebase 79cc74a..404bd51 onto cd1a89a (CR-184). Only what the move touched.

1. Resolved hunks. `git range-diff cd1a89a 79cc74a 404bd51`: run_scenario.py call list keeps gate_proof, restore_cr, then driver_liveness (before foreman_in_a_worktree); skills/chantier/references/concepts.md exit-2 sentence keeps CR-184's list (head not the one ship recorded, dirty tree, remote not at head, no passed gate or VERIFIED verdict; gate on a dirty tree) and appends this CR's two take cases. Both coherent, nothing lost.
2. Evidence checks at the new transcripts (scenario/results/github-20261111-234726.md and gitlab-20261111-235520.md): each 568 [x], 0 [ ]. All 8 checks present as [x] in both: activity age per working CR and no longest silent; not measured with the spend's own exit; take of working CR without note refused (2); take with agent recorded refused naming `agents set <cr> -`; status flags no Driver recorded; restart accepted (slots, no round, note, restart logged); restart past budget refused (5); handback blocked context: and fresh Driver takes it back; foreman.md/driver.md card check.
3. CR-184 rails vs take rules. check_take (rails.py 184-206): working without note refused, agent recorded refused, then check_budget (exit 5) BEFORE the slot check, which is skipped for a working CR. So a restart is still budget-refused, holds its slot, counts no round. CR-184's check_round is budget-first then limit; take does not call it, so a restart counts no round and the driver.md budget text agrees. No contradiction.

UNVERIFIED: Foreman following the cards (a judging agent); the PR description SHA placeholders (as in 04-verify).

VERIFIED
