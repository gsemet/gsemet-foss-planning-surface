Head: 23a83079cf5b6ea43dc505dfdb8ea686efbe2460
Verdict: VERIFIED

1. pytest tests/test_cli_units.py -k verdict (last_verdict_head asserts): 1 passed.
2. `python scenario/run_scenario.py --unit gates` at 23a8307: gates 86/86 checks ok. Transcript shows:
   - ready line "long gate and verdict carried from 645e250 (clean rebase onto main)", event has gate_from and verdict_from (check [x]).
   - conflict: "no long gate passed ... (the pass at 2a8306f does not carry: the replay conflicts)" and "no verdict VERIFIED ... (the verdict VERIFIED at 2a8306f does not carry: the replay conflicts)".
   - commit after verdict: "no verdict VERIFIED ... does not carry: the rebase changed the patch".
   - handoff boxes "[x] verdict VERIFIED carried from 645e250".
3. PR body vs diff (git diff origin/main): every file in Changes exists in the diff; _verdict_missing, GateBasis.verdict_carried/verdict_from, last_verdict_head match. Description pass: no stale claim; "Verified at <sha7>" and "CI green" boxes are open placeholders (expected).

## Description pass (posted body of PR 240)

Head: 23a83079cf5b6ea43dc505dfdb8ea686efbe2460
Verdict: VERIFIED

Read from the forge (gh pr view 240). Sections in template order (Issues References omitted, no source ticket). Proofs name SHAs: dc0f563 (exists) carried to 23a8307, "Verified at 23a8307" matches the 86/86 gates run above. No stale proof. CR id, round and .agents paths only under Internal references. Changes list matches the diff.

## Fresh Verifier pass at 23a83079cf5b6ea43dc505dfdb8ea686efbe2460

Head: 23a83079cf5b6ea43dc505dfdb8ea686efbe2460
Verdict: VERIFIED

- Reran `python scenario/run_scenario.py --unit gates` at 23a8307 (clean tree): header "unit gates on github: 86/86 checks passed" (transcript scenario-20261115-160712-32336.md). The FAIL lines in it are the scenario's intended failing gates.
- Previous claims 2 and 3 and the description pass carried from the earlier pass at the same head (no move).
