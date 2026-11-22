# Verify CR-456

Head: 13e79acc81acbf9ded4f2632f4f16f81ba528f7e

All claims judged at 13e79ac.

1. Evidence tests pass at head. Command (in skills/chantier/scripts/cli): `uv run --no-sync python -m pytest tests/test_serve_webui.py tests/test_command_names.py tests/test_board_running.py tests/test_writer_lines.py tests/test_watch_board.py tests/test_board_exposure.py -q`
   Output: `94 passed in 5.90s`. These cover the stale-name check with its prepared text, the renamed lines, serve_argv/find_pid (serve and board), the default-port cases, per-server cookies, and the four webui cases.
2. `chantier board` is an invalid choice. Command: `uv run --no-sync chantier board`
   Output: `chantier: error: argument cmd: invalid choice: 'board', maybe you meant 'order'? (choose from ... 'serve', 'webui', 'live' ...)`.
3. No stale command form in cards/docs. Command: `git grep -nE '\$CHANTIER board|chantier board [-`a-z]' -- skills AGENTS.md README.md CONTRIBUTING.md docs ':!docs/release-notes'`
   Output: only prose ("another chantier board"), code strings about the process, and the check's own fixtures in test_command_names.py. No command form.
4. Blocked-sync step names a webui-started server. `git grep -n "started by webui" -- skills`: session-start.md line 324 holds `PID <n> serve <project> (started by webui)`; test_command_names.py asserts it (passes in 1).
5. CI at head (`gh pr checks 430`): check x3 OSes, eval-dry-run and `just scenario (ubuntu-latest)` all pass. The CI log (`gh run view 45032755872 --log | grep`) shows `ok  surface-board (github): 320/320 checks`; no FAIL line from the scenario. The local Windows runs (ignored scenario/results) failed only the 5 webui checks at port 8765 (WinError 10049, boards hold it, as the PR's Known gaps says); CI total 320 vs local 319 with 314 passed, so the serve_and_webui checks pass in CI.
6. PR description at head 13e79ac (`gh pr view 430`): headRefOid is 13e79ac; Summary, Deliverables and Changes match the file set (declare/serve.py, webui, binding.py, cookie_name, tests); Known gaps names the scenario step's local limit, which is true (claim 5). Mermaid and table render in Markdown. Review box: log line 62 (r7 inspector approved) and line 63 (`r7 committed as 13e79ac`, the round's head) back it. Note: "Local gates at 13e79ac: just check, eval-dry-run": the log notes just check at 13e79ac; eval-dry-run was last run locally earlier (scenario/ only changed since) and is green in CI at head; accepted. No images.

VERIFIED

## Description pass at 13e79acc81acbf9ded4f2632f4f16f81ba528f7e

Command: gh pr view 430 --json body,headRefOid; gh pr checks 430; chantier log 456.
Output: head 13e79ac; body names 13e79ac in every box; Review box matches note "r7 committed as 13e79ac" (inspector approved d42b8b3, diff only scenario/run_scenario.py); CI all pass; Known gaps names the scenario limit; listed files exist in the diff. VERIFIED.
