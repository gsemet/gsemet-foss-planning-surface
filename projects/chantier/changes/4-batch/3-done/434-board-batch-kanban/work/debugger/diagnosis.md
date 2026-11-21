# Diagnosis: just scenario red at 140c12a (surface-board, github)

Verdict: a timing flake of the surface-board unit under load; not caused by CR-434's diff.

Evidence
- Diff vs base touches only web client JS, its doc and tests/test_board_design.py (git diff --stat base..HEAD);
  nothing under writer/, scenario/ or git code.
- Failing run: transcript scenario-20261121-210751-30412.md line 2310: at the conflict check the seat said
  "writer: synced, pushed 21:16" with events ['sync-blocked@1','sync-resumed@1'] and no sync-conflict@1.
  The writer was blocked briefly (blocking.py precondition) and resumed; the conflict episode was never seen,
  so the scripted Chief of Staff step `git rebase --continue` (run_scenario.py:9918) exited 128 (no rebase in
  progress), failing "surface_writer ran to the end" (second failure is a consequence of the first).
- Same gate run: other units over budget (parallel 369.9>350 s, series-deps 383.7>380 s): machine was loaded.
- Rerun alone at the same head (no code change):
  uv run --locked python scenario/run_scenario.py --unit surface-board --forge github
  -> ok surface-board (github): 299/299 checks, 540.1 s (budget 660), transcript scenario-20261121-212301-27504.md.

Place to fix (not CR-434): the scenario's surface_writer case (scenario/run_scenario.py ~9900-9920) races the
writer's cycle: the check and the `rebase origin/main` step assume the writer is in conflict by the time the
test acts; under load the writer's state differs. Rerun the gate (surface-board alone passes).
