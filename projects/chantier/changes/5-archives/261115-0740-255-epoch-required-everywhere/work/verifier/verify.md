# Verify CR-255

Head: c5e249891eeeb5bb286c3d90d9475f02ae43263b

Claims (all judged at c5e2498 unless stated):

1. Gate pass at head: work/gates/20261115-050230.log first line `gate CR-255 ... head c5e249891eeeb5bb286c3d90d9475f02ae43263b`, last line `result: pass at c5e2498...` (just check, just scenario, just eval-dry-run all pass in `$CHANTIER log CR-255`, 04:19:00Z). PASS.
2. Code (git diff eb14e28 HEAD, cli/src): `require_epoch` in core/batch.py raises EXIT_PRECONDITION (2) before RenderedBatch in take, take stack, pause, order done, agents set, foreman set/transcript, status --stop-heartbeat; `foreman set` with no session id stays exit 1; check_epoch still returns on None; stale and claim/transcript messages say `Foreman n°`. PASS.
3. Refusal writes nothing, message names the command and has no word "epoch" outside the flag:
   command: `uv run --no-sync --project . pytest skills/chantier/scripts/cli/tests -q -x -k "steering or slots or ready_cr or the_plugin_runs"`
   output: `22 passed, 112 deselected in 6.09s` (the 8 parametrized STEERING cases assert exit 2, usage text, `Foreman n°`, no `epoch` outside `--epoch`, batch.json and events.jsonl byte-identical). PASS.
4. Stale wording in scenario: run_scenario.py:946-947 checks code 3, `Foreman n°1`, `Foreman n°2`, no ` epoch `. PASS.
5. Cards: chief-of-staff.md:790 (first line `Foreman n°<n> of batch`), :1310-1319 (number as Foreman, gate --first, refuses without), concepts.md:318 (exit codes), foreman.md:4, :148, :530 (list with gate --first), report rule in chief-of-staff.md. PASS.
6. Scenario new step: delivered as a parametrized pytest instead of a scenario step; declared in the PR's Autonomous decisions. Accepted.
7. PR #213 description (gh pr view 213, headRefOid c5e2498): FAIL. Its Test plan says "Local gates at bc46f8c", "Evidence at bc46f8c", "Verified at bc46f8c", "CI green at bc46f8c", "Review: approved at bc46f8c". The branch was rebased on CR-259 and the head is now c5e2498; no proof is carried with a reason and none names the head. The Review note at bc46f8c exists in the log, but the rebase and two later fix commits (ed52c64, c5e2498) are not mentioned.

NOT VERIFIED
