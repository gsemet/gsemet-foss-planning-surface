# Heavy CI: integration hangs right after the stock coexistence check

Seen in 2 of the last 5 heavy runs: 40752707297 (#183 head 9964ac3d) and 40774494253 (#185 head
81af33d7). Last output is `{"stockPreview":"pass",...,"coexistence":"pass"}`, then only VS Code
chat noise (`ChatModelSelection`, `AgentHost`) until the 30-min job timeout. On green runs the next
line ~1 s later is `PASS checkbox screenshot: gfm/r01-task-reading-unchecked` (next VS Code launch).
Same heads passed on re-run, so it is intermittent and not linked to the changes.

Wanted: a per-step timeout with a process/screenshot dump at the hang point, then the root cause
(new VS Code chat/agent-host startup? second instance launch?). Release confidence depends on it.
Logs: /private/tmp/claude-502/cr169-heavy1-integration.log, /private/tmp/claude-502/cr171-heavy-integration.log.

## Status after CR 173 (2026-10-29, PR #193, instrumentation — cause not proven)

- Instrumented now: each trusted-suite scenario is a named step with a budget (`STEP start` /
  `STEP done` in the log); the awaits around the hang point have labelled 60 s timeouts; the
  extension host writes a heartbeat every 5 s; the launcher kills that launch's VS Code process tree
  when the heartbeat is stale for 90 s or a deadline passes (15 min per launch, 26 min stress, 3 min
  reload campaign); the integration step in ci.yml has a 20 min timeout followed by an always-run
  `just ci-hang-dump`.
- Reading a hang: download the integration artifact, open `out/reports/e2e/hang-dumps/`: `ps
  --forest` (is the extension host alive / spinning?), VS Code log tails (last host and renderer
  lines), window and tab state, CDP and X root-window screenshots. The last `STEP start` without a
  `STEP done` names the scenario; a labelled timeout names the await.
- Open question: does the extension host freeze, or does an awaited VS Code call never return?
- Close only when a dump has shown the cause. Not yet exercised on a real hang: xvfb root capture,
  `ps --forest`, the kill on the runner.
