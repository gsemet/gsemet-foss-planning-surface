# Diagnosis: CI red on test_the_seat_is_one_file_held_until_taken_over_on_purpose

Not a Linux/Windows difference: the test depends on the ambient `CLAUDE_CODE_SESSION_ID`.

## Reproduction (here, Windows, Git Bash)
cd C:/Users/gaeta/Projets/chantier.worktrees/batch-28-CR-384
env -u CLAUDE_CODE_SESSION_ID uv run --no-sync --project C:/Users/gaeta/Projets/chantier pytest skills/chantier/scripts/cli/tests/test_cli_runs.py -k seat_is_one -q
-> fails exactly as CI (`assert [] == ['watch']`, test_cli_runs.py:45). With the variable set (any
Claude Code session, as the Driver's shell has it) it passes.

## Cause
- `seat.py::_take` (l.147) takes `transcript = own_transcript(detect_host())`; `own_transcript`
  (plugin_files.py:94) reads `CLAUDE_CODE_SESSION_ID` (claude) from the process environment.
- `_own_watch_line` (seat.py:89-93) returns `not_running_line(repo)` only if `kept and kept == session_key()`;
  with no env var transcript is None -> kept == "" -> `[]`. No `watch:` line.
- `tests/conftest.py` (l.82-91) clears CHANTIER_HOST, CLAUDE_CODE_ENTRYPOINT, COPILOT_*, AI_AGENT, ...
  but NOT `CLAUDE_CODE_SESSION_ID`. The test sets only `CHANTIER_HOST=claude`. On a developer machine
  inside Claude Code the variable leaks in from the real session (so it passed locally); on CI it is
  absent. Other tests are unaffected as they do not need an own transcript.
- Note the leak also means the local run took a real session id as the Chief transcript.

## Suggested fix (not applied)
In the test: `monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "sess-1")` next to the CHANTIER_HOST line
(test_cli_runs.py ~l.34). Then transcript "sess-1", session_key() "sess-1", no watcher lock ->
`watch: not running...` line is emitted, `out[1:]` is `[": "...]` split -> ["watch"]. Beware: with a
transcript set, `_record_transcript` prints `<batch>: Chief of Staff transcript ...` lines only if
batches exist (none in this repo: repo.batch_ids() empty), so the assertion holds.
Also add `"CLAUDE_CODE_SESSION_ID"` to the tuple of cleared vars in conftest.py (l.82-90) so no test
depends on the ambient session (any test needing it sets it explicitly).

## Other jobs (gh pr checks 351, at time of check)
ubuntu check: fail (this cause). eval-dry-run ubuntu: pass. macos/windows check and scenario: pending.
Windows/macOS CI have no session variable either, so they will fail the same test; scenario not yet known.
