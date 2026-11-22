# Diagnosis: `just scenario (ubuntu-latest)` red at 9808e1d

Cause: this CR's diff. It adds the op `dashboard.get` (protocol.py OP_ARGS, ops.py HANDLERS), so
`protocol.OPS` goes from 20 to 21. The scenario's surface-board unit asserts the welcome frame
holds exactly 20 ops. Topics stay 6 (not touched).

Evidence
- CI log (work/scratch/ci.log): all units ok except `surface-board (github): 298/299 checks`;
  the one failed check: "the WebSocket with the cookie from the board's own origin gets `welcome`:
  protocol 1, the 20 ops and 6 topics, the server's PID as the probe's".
- scenario/run_scenario.py:1682: `len(welcome.get("ops", [])) == 20`.
- Local, in the worktree: `len(protocol.OPS), len(protocol.TOPICS)` prints `21 6`.
- Not flaky: deterministic count. Not the base: main has 20 ops.
- `just check` passes because the unit tests (test_server_api_calls.py, edited by this CR) were
  updated; the scenario was not.

Fix (in this CR)
1. scenario/run_scenario.py:1681-1682: "the 20 ops" -> "the 21 ops", `== 20` -> `== 21`.
2. scenario/README.md:459: "the 20 ops" -> "the 21 ops".
Then re-run only the surface-board unit if the scenario has an entry for one unit, else `just scenario`.
Not run locally by me (the Driver's gate is running).
