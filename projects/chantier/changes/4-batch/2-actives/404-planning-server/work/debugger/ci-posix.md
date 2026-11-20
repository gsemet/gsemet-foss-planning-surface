# CI red on POSIX: test_a_failed_git_step_waits_a_cycle_then_blocks_once_and_resumes

Cause: the test writes the pre-commit hook with `hook.write_text(...)` (test_writer_cycle.py line 222) and never sets
the executable bit. On Linux and macOS git runs a hook only if it is executable; otherwise it skips it (only a hint
"The '.git/hooks/pre-commit' hook was ignored because it's not set as executable"). The commit succeeds, the push
succeeds, state is 'synced'. On Windows (Git for Windows) the exec bit does not exist and hooks run via sh, so it fails as intended.

Fix: in tests/test_writer_cycle.py (skills/chantier/scripts/cli/tests/), after line 222 add `hook.chmod(0o755)`
(no-op on Windows). No writer code change.
