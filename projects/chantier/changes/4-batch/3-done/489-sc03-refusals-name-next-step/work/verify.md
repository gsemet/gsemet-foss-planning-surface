Head: 42da1733456f027d7a14c3b9c4bc8294b5e2eaa9

All claims judged at 42da173.

1. Gate passes and prints the M9 line (42da173).
   `uv run --no-sync pytest .../tests/test_refusal_gate.py -s -q` -> `M9: 36 refusals scanned in 4 files, 7 allow-listed`, `4 passed`.
2. Extended assertions and neighbours (42da173).
   `pytest test_rail_refusals.py test_leases.py test_refusal_gate.py test_scenario_coverage.py -q` -> `61 passed`.
3. The gate fails when a tail is removed (42da173, throwaway copy of src and tests under work/scratch/mut, removed after; worktree untouched).
   Removed the `lease {unit}` backticks and the `order slots` backticks in the copy, ran the copy's gate (PYTHONPATH on the copy) -> `1 failed, 3 passed`, naming rails.py:59 (check_slot), leases.py:297 (require), leases.py:343 (claim) as "names no next command and is not allow-listed".
4. Command forms against --help (42da173): `take <cr> [--epoch] [--note]`, `lease <unit>`, `asks [--outside-stack] text`, `close [--stopped NAME]`, `order <kind> [cr]` with kinds add/slots/grant and `--fix-for`, `agents set <cr> <agent>` all exist in the help output; each backticked first word is a parser subcommand (the gate checks it).
5. Diff matches spec table section 1 row by row (STOPPED_HINT, check_idle, the five `_declared` branches, lease_of x2, require, claim, check_slot, both check_take, check_granted_fix, parse_grant x2, check_shape x2); conditions and exit codes unchanged in the diff. Scenario hint edit at run_scenario.py close_refusals is the one spec'd (`"`close --stopped <name>` for each"`). No other exact-text check found by `git grep` for the old hint.
6. CI at head (gh pr checks 470): just check macOS, Ubuntu, Windows, eval-dry-run, scenario (ubuntu) all pass.
7. PR description: Summary, Deliverables, Changes, Autonomous decisions match the diff (new test_refusal_gate.py, four src files, scenario hint, three extended assertions); M9 line equals the real output; Known gaps "None" is consistent (no UNVERIFIED claim). Timing: states 128.54 s before and 117.52 s after with "no measurable added time"; the new gate itself runs in 0.09 s (pytest above), so the statement is honest (the before/after gap is machine noise, not an addition).
   Minor: the spec's dedicated-file choice is disclosed. No images.

VERIFIED
