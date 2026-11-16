# CR-196 verify (head 77eff0c)

- Evidence items 1-16: each exists as a `check` in scenario/run_scenario.py (14d `release_on_stack` for 1-13 and 15; section 14 parallel for 14; 14c for 16). Their pass in `just scenario` is NOT run by the Verifier (the Foreman's gate is running); the gate log was still waiting for CR-200 at read time.
- Docs rg: no match in the worktree (outside .agents) for the six quoted sentences.
- docs/batch-pace.svg parses as valid XML (1240x556); `<desc>` matches the drawing (no "runs last, alone"); old frame text gone.
- evidence/batch-pace-before.png and -after.png: after shows the release as a CR above the slots with waits-for arrows, in a slot, top of the stack, release mark on main after the merge; batch-07 release inside lane after the merges; legend and batch-08 kept. Matches the spec.
- CLI exercise on a scratch repo: skipped (the scenario covers it).

Verdict: VERIFIED, on the static checks; the scenario gate pass remains the gate's.

## Move 77eff0c -> 163249f

- Diff: audit.py C11 now accepts a release-go result of ask or merge; rails.py logs release-go with result=merge (lines 261, 264), so the change matches the CLI.
- CI on PR 140 was all pending at read time (check x3, eval-dry-run, scenario). Not waited for.
- Verdict: VERIFIED, on the diff.
