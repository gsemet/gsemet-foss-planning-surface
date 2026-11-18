# Verify CR-350

Head: d17106548d4cae08ce6c4c0f467f1e2006b8b49f

All claims judged at d1710654.

1. Diff matches spec changes 1-3. `git diff <base>...HEAD`: scenario (sleeper 600 s, `born` via psutil, lock and ticket at `born - 60`, bound `< 60`), test_board.py (observe_join x2 and watcher.join x2, proc.wait x2 at 60; the 0.01 waits untouched), justfile `tools` recipe as specified, ci.yml step (bash, `just tools || just tools`) between the Git identity step and `just check`. 4 files, no other change. Pass.
2. `just test -k test_join`: `4 passed in 3.79s`. Pass.
3. `just check`: `565 passed in 32.71s`, release-notes ok. Pass.
4. `gh pr checks 311`: just check (ubuntu 43s, macos 2m21s, windows 1m51s), eval-dry-run, scenario (ubuntu-latest) all pass at run 44256490947; CI log shows the step "Fetch the check tools (retried once)" running `just tools || just tools` under bash. Pass.
5. Local Windows scenario (%TEMP%/scenario350.log, finished): `ok  parallel (github): 249/249 checks, 206.6 s`, no FAIL line; section 19 is inside that all-green run. CI scenario (ubuntu) green. Pass. (The log prints only the summary, not per-check names.)
6. PR 311 description: renders, Summary/Deliverables/Changes match the diff, no images, Known gaps names the untestable retry. Test plan boxes are pending placeholders for the Driver.
7. Not provable: a real download timeout and retry (shape only), as the spec says. The empty-UV_CACHE_DIR `just tools` then `just check` run was not asked of me and not run.

VERIFIED

## Description pass (PR 311) at d17106548d4cae08ce6c4c0f467f1e2006b8b49f

Head: d17106548d4cae08ce6c4c0f467f1e2006b8b49f

- Description vs diff (git diff b69d4b14 HEAD --stat: ci.yml, justfile, run_scenario.py, test_board.py): Summary, Deliverables, Changes match; no change missing or unmentioned. Judged at d171065.
- Internal references (CR-350, batch-24) only in the Internal references section; no role name outside it. Judged at d171065.
- Known gaps present; no UNVERIFIED claim, no uncaptured evidence pair. Renders (fold with blank lines, no images).
- Test plan: local Windows scenario exit 0 with the four reused-pid checks ticked (scenario/results/scenario-20261118-080748-33952.md lines 13946-13962); gh pr checks 311: all five pass. Review box: Driver note "r1 committed as d171065" after inspector approval, matches.

VERIFIED
