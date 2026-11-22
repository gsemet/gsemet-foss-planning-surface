# Diagnosis: just scenario red at 86544ac (surface-board, github)

## Check 1: welcome counts (caused by this CR)
- scenario/run_scenario.py:1681-1682 hard-codes `len(welcome["ops"]) == 20` and `len(welcome["topics"]) == 6`.
- The CR added `"history.get"` to OP_ARGS and `"history"` to TOPIC_ARGS (board/api/protocol.py). Proof:
  `uv run --no-sync python -c "from chantier.board.api import protocol as p; print(len(p.OP_ARGS), len(p.TOPIC_ARGS))"` in the worktree prints `21 7`.
- The CR's diff touches run_scenario.py only in close_batch (~l.4722); not these counts.
- Fix: run_scenario.py line 1680 text "the 21 ops and 7 topics" and line 1681-1682 `== 21` / `== 7`.
  (Grep found no other "20 ops" text in scenario/, docs/ or skills/.) Check the pytest side too: tests/test_server_api_calls.py was already touched by the CR.

## Check 2: `chantier/` extra entry (flake, not this CR)
- Transcript scenario/results/scenario-20261122-034717-33100.md line 27455: extra entry is `server.json.22612.tmp`.
  PID 22612 is the surface server/hub itself (transcript l.27413: "forge hub: PID 22612, the surface server").
- core/files.py:write_file (l.120-126) writes `<name>.<pid>.tmp` then `os.replace` (retry up to ~1 s on Windows PermissionError). The hub rewrites server.json after each read (last read 02:52:21Z);
  the check (run_scenario.py:2814-2816) lists `git.iterdir()` while the server still runs, so it can catch the transient tmp (a rename held up by a reader on Windows).
- Evidence it is a race, not caused by the CR: the earlier gate run of the SAME head (work/gates/20261122-032724.log) failed check 1 only (298/299); check 2 passed. Nothing in the CR touches hub/, writer/ or core/files.py.
- Not a knock-on of check 1 (that check only reads the welcome frame; it leaves state untouched).
- Minimal fix (optional, to harden the scenario): in run_scenario.py:2814 ignore `*.tmp` names
  (`not x.name.startswith("watch-") and not x.name.endswith(".tmp")`) or poll `until(...)` that no `server.json.*.tmp` remains before the check. Otherwise just rerun: fix check 1, rerun the surface-board unit.

## Reproduction
- Check 1: grep the two lines above; the one-liner gives 21/7.
- Check 2: not reproduced narrowly (timing); proven by the transcript and the other run.
