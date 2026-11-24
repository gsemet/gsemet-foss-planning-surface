# Verify CR-479

Head: a92dd754ad76d465182c6091e229e9fa8bd531fc

All claims judged at a92dd754.

1. Long gate passed at the head. Command: head and tail of work/gates/20261124-184812.log.
   Output: first line `gate CR-479 ... head a92dd754ad76d465182c6091e229e9fa8bd531fc`, last line `result: pass at a92dd754ad76d465182c6091e229e9fa8bd531fc` (just scenario, including the Foreman's-watcher step). PASS.
2. Unit tests. Command: `uv run --no-sync python -m pytest tests/test_watch_foreman.py tests/test_playbook_timing.py tests/test_watch_events.py tests/test_watcher_autostart.py tests/test_start_reading.py -q` in the worktree's CLI folder.
   Output: `124 passed in 11.64s`. PASS.
3. Shipped Claude Code default is 55m, Copilot 4m. Command: `grep -n steering_wake config/chantier.defaults.yml`.
   Output: `23: steering_wake: 55m`, `64: steering_wake: 4m`. PASS.
4. Message texts say "for the steering session". Command: `grep -n "steering session" hub/schemas.py`. Output: lines 115, 119, 122, 128, 140 carry it. PASS.
5. Chief of Staff's status prints the Foreman's watcher state. Command: `grep -n "foreman watch" -r src`. Output: `hub/lines.py:50: "foreman watch: running" if runs else "foreman watch: not running"`. PASS.
6. CI at the head: just check (ubuntu) and eval-dry-run (ubuntu) SUCCESS (`gh pr view 459`); macOS, Windows and scenario ubuntu still pending at read time (not a failure; the local long gate of claim 1 covers the scenario).
7. PR description (posted, `gh pr view 459 --json body`): sections render, the Summary and Deliverables match the diff (31 files: watcher, autostart, schemas, cards, docs, AGENTS.md, scenario, tests), UNVERIFIED claims are in Known gaps, no images. The `Review: approved at` box is not yet in the body (Test plan still has placeholders `<sha7>`): the Driver fills these at ship; not judged here.
8. UNVERIFIED, as the PR states: the 55-minute wake and the Foreman's watcher waking an idle Foreman session on Claude Code (cards name the trials). Not captured; per the brief they do not change the verdict.

No before/after pair: no UI; the proofs are tests and the gate.

VERIFIED
