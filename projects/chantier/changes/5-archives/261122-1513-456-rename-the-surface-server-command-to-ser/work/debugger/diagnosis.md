# CR-456 diagnosis: `serve_and_webui ran to the end` red on CI

Exception (reproduced): `ConnectionRefusedError` at scenario/run_scenario.py:2726
`got1 = fetch(link.port, "/api/board", ...)`, preceded by the failed check "a second surface's server ... takes port"
(`said`/`start` both None).

Cause: `first` is started with `--seat sess-1` (line 2707-2708) but no seat is ever taken
(`seat take sess-1`), so `seat.json` names no session. A board started with `--seat` follows its seats
(board/seats.py) and stops itself, exit 0, at the first seat check (every SEAT_CHECK_S = 10 s) because none
is held. On CI the step is slower (init x2, second board start + 20 s `line()` timeouts), so by 2726 `first`
is gone: port refused. The second board (also `--seat sess-2`, never taken) likewise. Locally the branch is
skipped (port 8765 held) and the rest finishes inside 10 s, so it passes. Also the second's 'takes port'
line was None in the repro only because my repro forced a configured port (fallback applies to the default
port only); that is a repro artefact, not the CI cause.

Evidence: repro3.py: `serve --port F --seat sess-1` alone exits 0 within 12 s; without `--seat` it is alive
at 12 s. (repro.py reproduces the traceback; repro2.py shows first poll 0 after 2 s+.)
Reproduction: `uv run --no-sync --project <worktree> python work/debugger/repro3.py --seat sess-1`.

Fix (minimal): in serve_and_webui drop `"--seat", "sess-1"` (line 2708) and `"--seat", "sess-2"` (2715-2716):
nothing in the step needs a seat (later asserts want `--seat` absent only for the webui-started server).
Alternative: `sw.chantier("seat","take","sess-1","--env","remote","--title","[remote] a","--link","l")` for each
surface before starting, as the unit does at line ~10485.
Not verified: the second-surface branch itself (needs the real 8765 free), so a CI run is the proof.
