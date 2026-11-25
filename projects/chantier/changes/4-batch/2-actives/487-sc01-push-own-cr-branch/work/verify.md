# Verify CR-487 `chantier push`

Head: 096f073c91a36591bde02b3f5abc0705daeaf023

Judged at 096f073 (git rev-parse HEAD in the worktree; PR 465 head equals it, per `gh pr view 465`).

## Claims

1. Rails (branch recorded, chantier/* only, not default, lease given, lease held, worktree clean, HEAD on branch, unit with no lease, stack unit outside chain, QA order of another CR): each refuses, runs no `git push` (subprocess spy), records no `push` event, leaves the remote branch absent.
   Command: `env -u NO_COLOR uv run --no-sync --project . pytest skills/chantier/scripts/cli/tests/test_push.py skills/chantier/scripts/cli/tests/test_driver_prompt.py skills/chantier/scripts/cli/tests/test_remote_cli.py skills/chantier/scripts/cli/tests/test_scenario_coverage.py -n auto -q`
   Output: `70 passed in 71.75s`. The 10 refusal ids are in `REFUSALS` of test_push.py, with exits 2 and 3 (`claim lost`) checked. Also read in `commands/push.py` at 096f073: `_refuse_branch`, `_refuse_worktree`, `leases.require`, `renewed_in_session(..., required=True)` before the push.
2. Exact git command: `commands/push.py::_run_push` builds `["git","--no-pager","push",f"--force-with-lease={branch}:{expected}",remote,f"HEAD:refs/heads/{branch}"]`, one `subprocess.run`, no loop. `grep -nE '"--force"|--no-verify|"gh"|"glab"|retry|"-u"' commands/push.py` matches only the docstring line 3 ("Never `--force`, never `--no-verify`, no retry, no forge call"): no such argument or call in code. Tests: new branch (empty expectation, `(new branch on origin)`) and update (`was <sha7>`) push to the bare remote at the worktree head, one `push` event with branch, head, expected, unit; lease expiry moves later.
3. Git refusal verbatim, exit 4: `test_a_remote_that_moved_is_refused_by_git_and_nothing_is_recorded` passed (exit 4, "git refused the push", `stale info` or `rejected` in output, remote unmoved, one event only). The lock is not held during the push (read: the push runs between two separate sessions).
4. Profile and server refusal: `NEVER_REMOTE` gains `push` (core/remote_wire.py); `clients/remote.py::forward` raises PUSH with EXIT_USAGE before any server call; `board/cli_run.py` line 52 refuses every `NEVER_REMOTE` command. test_remote_cli.py: `push` through a profile gives code 1, "not through a profile", `server.calls == []`; `cli.run` case `{"argv": ["push", ...]}` expects BAD_ARGS. Both passed in the run above.
5. take's Rewrites line and ship line: `driver_prompt.py::_rewrites_line` now prints `then $CHANTIER push <cr> --lease <n>` (and `--unit stack` for batch branches), rebase half and scope sentence unchanged; `driver.py::_take_stack` lease line adds `push <cr> --unit stack`; `delivery.py::_off_worktree` keeps `is not pushed`/`is at <sha>` and names `chantier push <cr> --lease <n>`. test_driver_prompt.py passed (asserts new half, unchanged rebase half, no `--force-with-lease` in own-branch line).
6. AGENTS.md (diff HEAD~1..HEAD read): git exception bullet gains `push` and the closing sentence stays true; "writes only" sentence and network list name `chantier push`; `cli.run` list and `login` paragraph add `push` beside `gate`; named-exceptions paragraph has the `push` entry with legitimacy statement, sources (Q5, Q22, study-classifier 13 refusals / 12 days / 4 questions / 83 %) and the F21 sentence and answer-8 route.
7. Scenario: `push_own_branch` is in scenario/run_scenario.py and the Coverage bullet is in scenario/README.md (test_scenario_coverage.py passed). CI at 096f073 green on five jobs per the Driver's note in `$CHANTIER log CR-487` (run 45520729424); not rerun by me.
8. Smoke trial: the Driver's record only (5 pushes, no refusal, permission mode not shown); the log shows the `push` event at 096f073 with expected == head (a no-op). Not provable by me; stays "unproved" as the specification says.
9. Long gate: carried from b9e02b6 per the Driver's `carry` event (clean rebase). Not rerun.

## PR description (as posted on PR 465 at 096f073)

Posted body is the draft: it still has `<sha7>` placeholders and an empty "Local gates" line in the Test plan, no Review or Verified SHA, and Known gaps still says the smoke trial is pending although the Driver ran it. The Summary, Deliverables and Changes match the diff. This is for the description pass the Driver planned (trial records, SHAs); it must be fixed there. It does not change the code verdict.

VERIFIED (code, at 096f073)
