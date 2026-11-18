# Answers

No grill: a retro point of batch-24 (2026-11-18), kept by the retro critic, that the user put
straight into the batch.

## Settled by the Chief of Staff

- The user's word (2026-11-18): "file all six and run them in batch-24" ("Fait les 6 c'est très
  bien. Fait le dans le batch en cours"). This CR is one of the six, run as its request is written.
  The user asked no question and settled no behaviour; each choice below is settled by the Chief of
  Staff, within the request.
- tc-Q1 (why the scenario's reused-pid check fails under load): the CLI takes a recorded process
  for the live one when its creation time is at most the lock's file time plus one second
  (`procs.py`, `CLOCK_MARGIN_S`). The scenario backdates the lock to "now minus 10 s" at each
  write, while its sleeper was started earlier in the section; once more than about 9 s have
  passed since the sleeper started (a loaded machine), the sleeper looks like the recorded process
  and `order merged` signals it. The fix backdates the lock and the stale queue ticket to a fixed
  point well before the sleeper's own creation time (read with `psutil`), so the margin no longer
  shrinks as the section runs. Settled by the Chief of Staff.
- tc-Q2 (the same section's "runs at once" bound): the check "a lock naming a reused pid is not
  waited for" asserts under 10 s; a wrongly waiting gate would wait for the sleeper (120 s). The
  bound goes to 60 s: it still tells a wait from no wait and holds on a loaded machine. Settled by
  the Chief of Staff.
- tc-Q3 (the autosync test): `test_join_observe_reports_early_failure_exactly` passes
  `timeout=60` instead of `timeout=1`; `observe_join` returns as soon as the child exits, so the
  test is no slower on an idle machine. The two sibling tests that use `timeout=0.01` assert that
  the child is still alive (it blocks on stdin) and stay as they are. Settled by the Chief of Staff.
- tc-Q4 (the download retry): CI's `just check` job gets one step before `just check` that only
  fetches the pinned check tools into the runner's caches, run as `just tools || just tools`
  (retried once). `just tools` is a new justfile recipe that uses the pins already at the top of
  the justfile, so each pin stays in one place. `just check` itself is not retried: a failing test
  must still fail the job. Settled by the Chief of Staff.
- tc-Q5 (out of scope): no CLI change (`procs.py`'s margin is right; the scenario's setup was
  wrong), no card change, no new test, no retry of the scenario or eval-dry-run jobs (the request
  names the macOS `just check` download only), no timeout tuning in uv. Settled by the Chief of
  Staff.

## Settled by the Chief of Staff (after the spec critic)

The user is away; the Chief of Staff settles in the user's place, inside the request's intent.

- tc-Q6 (the sleeper's own life): the scenario's sleeper exits by itself after 120 s, and the
  `cancel` and `order merged` checks assert that it lives on; a section slower than that on a
  loaded machine fails them, and the same 120 s may be what failed at CR-336 (that run's detail
  was not kept, so tc-Q1's cause is the probable one). The sleeper sleeps 600 s (it is killed at
  the block's end), and tc-Q2's 60 s bound stays: a wrong wait would last the sleeper's remaining
  life, well over 60 s. Settled by the Chief of Staff.
- tc-Q7 (the other short waits of the autosync group): option (a), recommended by the critic.
  `test_join_drains_large_output_without_deadlock`'s `observe_join(timeout=3)`, and the siblings'
  `watcher.join(timeout=3)` and `proc.wait(timeout=3)`, go to 60 s; each returns as soon as its
  condition holds. The siblings' `observe_join(timeout=0.01)` stay. This narrows tc-Q5's "no other
  timing bound". Settled by the Chief of Staff.
- tc-Q8 (what the retry covers): only the tool and wheel fetches of `just tools` are retried; a
  network read inside `just check` itself (e.g. `uv lock --check`'s index read) is not, and the
  specification says so under "Out of scope". Settled by the Chief of Staff.