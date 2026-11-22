# Conflicts: CR-438 rebase onto origin/main

Command: `git -C <worktree> rebase --onto origin/main 62e119cf~1`. Result: one commit, 25fd6177.

## skills/chantier/references/foreman.md (one hunk, lines 376-662)
The CR moved the stack-batch section into the new `foreman-stack.md` and left a pointer bullet.
Main edited one line of that moved section ("Each later take": `to come: <cr below> not shipped at <tip7>`).
Choice: kept the CR's side (the pointer bullet). Re-applied main's line edit in `foreman-stack.md`, so both intents survive.
Main's other foreman.md edits (refused force push section, lease hold, chat line) merged cleanly and are kept.

## Follow-up edit (uncommitted, in the worktree)
`tests/test_stack_chain_cards.py` read "not shipped at" in `foreman.md`; the text now lives in `foreman-stack.md`. The test now reads `foreman-stack.md`.

## Fast gate
`just check`: 4 failed, 1920 passed (before the test edit; log: check.log).
- test_stack_chain_cards: fixed by the edit above (passes alone).
- test_startup_manifest (claude, copilot): chief-of-staff reload 12742 > limit 12544. Not resolved: a size budget (needs a trim or a limit decision).
- test_triage_moves::test_w2_a_shell_inside_the_folder_refuses_then_lets_go: Windows folder-held test, touches no file of this CR. Not investigated.
