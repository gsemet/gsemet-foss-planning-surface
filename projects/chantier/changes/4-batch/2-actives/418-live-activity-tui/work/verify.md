# Verify CR-418

Head: 800bd85b12db153af645530d9c1b11dad9652933

Claims (all judged at 800bd85):
- New and touched tests pass: `pytest tests/test_live_model.py tests/test_live_link.py tests/test_leases.py tests/test_server_api_calls.py tests/test_server_protocol.py tests/test_scenario_coverage.py -q` -> `57 passed in 16.96s` (real server, ws and http, --once, wrong key, import check; protocol.json not in `git diff --stat main...HEAD`).
- Gate: work/gates/check.log ends `1423 passed, 14 skipped`; just check (ubuntu) SUCCESS on the PR.
- `rich==15.0.0` pinned, and in banned-module-level-imports (pyproject.toml lines 13, 60); tui modules import from chantier only `__version__`, `core.errors` and the package itself (grep of link.py/model.py/screen.py).
- `--url` without `k`: `chantier live --url http://127.0.0.1:1/ --once` -> `error: --url: the link holds no key (?k=...): give the link the board printed`, exit=1. Other refusal lines present in commands/live.py.
- Read-only: link.py sends hello/sub/unsub/poll only (covered by test_live_link.py).
- Docs: docs/server-api.md "terminal client" section, docs/boards.md section, AGENTS.md, README, CONTRIBUTING in the diff.
- Review box: log has `r2 approved at 4ed0d56, committed as 800bd85`.

Failed:
- PR description (as posted): not final. Its Deliverables hold no `live --once` capture (the spec requires it there; Known gaps names the absence, honestly), Test plan keeps `<sha7>` placeholders and unticked boxes, and the Review box has no `approved at` line. Pipeline: macOS, Windows, scenario and eval-dry-run checks had no result at the time of the check, so the spec's scenario-green-at-head gate is not shown.
- Not run by me: live screen in a real terminal (stated in Known gaps); evidence/live-once.txt exists and shows the CR, `working 1` and lease 09:55.

NOT VERIFIED
