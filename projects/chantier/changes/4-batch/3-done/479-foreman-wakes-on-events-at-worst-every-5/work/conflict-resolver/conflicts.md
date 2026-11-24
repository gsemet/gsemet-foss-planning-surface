# Conflicts: rebase onto da6fd2f4 (CR-479)

Only the first commit (2d555738) conflicted; the next two applied cleanly.

- hub/autostart.py: main added `DEV_PROJECT`, `dev_build`, `other_dev_build`; the CR added `kept`,
  `open_record`, `records_foreman`, `foreman_batch`. Kept both, one after the other.
- hub/watch.py imports: kept the CR's (`ChantierError` only, the Foreman watch_reads names, no `read_wake_rules`),
  because the `watch` handler now lives in `watch_cmd.py`.
- hub/watch.py `connect`: kept main's `self.waiting = False`, then the CR's Foreman refusal when no board is recorded.
- hub/watch.py `watch()`: removed from watch.py (moved by the CR to `watch_cmd.py`); main's refactor
  (`checked(repo, args)` replacing the inline argument checks) was carried into `watch_cmd.py`.
- tests/test_start_reading.py: kept main's CR-478 comment; the AFTER figures re-measured at the new
  base: chief-of-staff 202_396 / 111_492, foreman 91_019 / 83_545 (the Drivers unchanged).

Fast gate, as run: `env -u NO_COLOR just check` in the worktree: 2568 passed, 20 skipped;
release-notes check ok.
