# Verify CR-122, round 1, head 4cbc948

The Verifier's report, copied by the Driver: the Verifier wrote no file.

Verdict: PASS.

| Claim | Proof |
|---|---|
| The head is one commit on main, nothing of CR-120 or CR-121 | merge-base with origin/main is 49135f5; `git diff origin/main...HEAD` touches chief-of-staff.md, concepts.md, foreman.md, cli.py, commands.py, scenario/run_scenario.py, scenario/README.md only; `git status` clean |
| No clash with main's 5adff96 and 49135f5 | no overlap in the diff; the tips line and the force-push route do not touch the lines changed |
| Cards say parallel by default, depends.json only for a real need, queue with reason, the plan's CRs at once and slots, `order after` listed | chief-of-staff.md, foreman.md, concepts.md read at 4cbc948 |
| Start base and stack place kept apart | `_start_base`, `_stack_base`, `_stack_ref` in commands.py; `take stack` prints the place, `take` and `handoff` the start base |
| `order after` replaces `after` of a queued CR, no new number; exit 2 on not queued, unknown CR, unknown dependency, self-dependency, cycle (old value restored) | commands.py and the scenario's checks |
| Independent CRs taken at once on the default branch, then stacked; a CR added later starts on origin/main; `order after` with `-` and with an id | scenario transcripts github-20261106-120110.md, gitlab-20261106-120429.md |
| `just check` | 26 passed |
| `just scenario` | github 210/210, gitlab 210/210 |
