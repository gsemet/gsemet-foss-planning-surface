# Diagnosis: surface-board (github), "external_surface ran to the end", Windows

Verdict: caused by this CR's diff. Not a pre-existing failure. It is a timing race in the CR's
edited scenario check, which Windows' slower process start exposes.

## Reproduction

From the CR worktree at e6ff8a6 (about 130 s):

    uv run --locked python scenario/run_scenario.py --unit surface-board

Result at e6ff8a6: 130/131, FAIL, same check as the gate. At a detached worktree of 5eb0c1e
(origin/main), same command: 154/154, ok.

## Failure

Transcript line: `IndexError: list index out of range` in `surface_autosync`
(scenario/run_scenario.py:7018):

    code == 200 and runs()[-2] == ["start", ".", "--enable-only"]

`code == 200` held, so `runs()` (the fake tool's `.argv` log) had fewer than 2 lines when read.
The crash is an exception, so it reports as "external_surface ran to the end" and skips every later
E2 check (154 on main, 131 here).

## Cause

The CR changed `POST /api/autosync/start` (autosync_api.py `_single`): after `start` succeeds it
now calls `spawn_join` and `observe_join(process)`, which waits only 0.25 s and returns None while
the join is still running. The join is an asynchronous `uv run scripts/ai-autosync-git.py join ...`
process. The fake tool logs its argv only once that child has started. The HTTP reply comes back
before then.

The CR also rewrote the check to assert synchronously that `runs()[-1][:2] == ["join", "."]`, and
`runs()[-2]` for the start. On main the check was `runs()[-1] == start`, and the join was awaited
in a 90 s polling loop after board launch. The new code has no wait.

Proof (probe in the scratchpad, `probe/probe1.py`, which calls `run_action("start")`, then
`spawn_join`, then `observe_join` against the fake script in a scratch git repo, and does not touch
the live board or surface):

    start ToolResult(code=0, line='started by user')  0.15 s
    observe diag None at 0.41 s
    log right after observe: ['["start", ".", "--enable-only"]']     <- only 1 line
    join logged after extra 0.26 s                                   <- join line arrives later

So when the reply is sent the log has the start line only. Reading `runs()[-2]` then raises.
Linux (CI) starts `uv run` faster and the join usually logs inside the 0.25 s observe window or
before the next request, so CI passed. It is a race on a fast machine, not a guarantee: the check
is flaky by design.

## Place to fix

scenario/run_scenario.py, `surface_autosync`, the "E2: start in the stopped state ..." check
(about lines 7016-7020): poll (bounded, a few seconds) until `runs()` holds the `join` line before
asserting `runs()[-2]` and `runs()[-1]`, as the pre-CR code did with its polling loop. Do not read
`runs()[-2]` unguarded.

The same race is worth guarding in the approve check (line 7032), which asserts the last two runs
too. There the last run is `start`, with no join, so that one is safe.

Secondary, optional product point: `observe_join`'s 0.25 s wait is only a heuristic for catching an
instantly failing join. If the product should guarantee the participant exists when the reply is
sent, the API must wait for the participant file. The CR's spec decides that.

## Cleanup

My detached worktree of 5eb0c1e under the scratchpad is removed. No project file was changed, the
live board and the planning surface were not touched. The scenario's own `results/` output sits in
the CR worktree (ignored), and the probe sits in the scratchpad.
