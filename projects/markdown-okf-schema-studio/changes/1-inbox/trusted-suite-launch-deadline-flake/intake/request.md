# Heavy integration job hits the trusted suite launch deadline

The heavy `integration` job timed out once without a related change.

- Run 45774743144, head 5a8a593 (CR-505, https://github.com/gsemet/markdown-okf-schema-studio/pull/532),
  2026-11-26. Attempt 1 failed: `LAUNCH TIMEOUT: trusted-suite.js exceeded its 900000 ms deadline
  (STUDIO_LAUNCH_TIMEOUT_MS); last heartbeat step: myst-diagnostics`. Attempt 2 of the job passed.
- Passing runs are close to the limit: 852 s on main 3478f09 (run 45773405420), 854 s on attempt 2.
- Log: CR-505's `work/ci-45774743144.log`.

CR-509 (https://github.com/gsemet/markdown-okf-schema-studio/pull/529, batch-09, not merged yet)
splits the trusted suite into two launches, which targets this deadline. Its own recorded gap: the
whole integration step stays 6 to 12 % under its 1200 s limit.

Project rules (`.agents/guidelines/ci.guidelines.md`, rules 9 and 12): a job that passes on re-run
without a change is a bug to fix, proved by repetition; the re-run does not close it.

Asked: after CR-509 is merged, check that this timeout is gone (repeated heavy runs) and fix what
remains. Not grilled.

Origin: Foreman ask A-32, 2026-11-26.
