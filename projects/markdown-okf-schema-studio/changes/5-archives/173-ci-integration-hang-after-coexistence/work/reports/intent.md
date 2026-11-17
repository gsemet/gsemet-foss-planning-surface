# Heavy CI: integration hangs right after the stock coexistence check

Seen in 2 of the last 5 heavy runs: 40752707297 (#183 head 9964ac3d) and 40774494253 (#185 head
81af33d7). Last output is `{"stockPreview":"pass",...,"coexistence":"pass"}`, then only VS Code
chat noise (`ChatModelSelection`, `AgentHost`) until the 30-min job timeout. On green runs the next
line ~1 s later is `PASS checkbox screenshot: gfm/r01-task-reading-unchecked` (next VS Code launch).
Same heads passed on re-run, so it is intermittent and not linked to the changes.

Wanted: a per-step timeout with a process/screenshot dump at the hang point, then the root cause
(new VS Code chat/agent-host startup? second instance launch?). Release confidence depends on it.
Logs: /private/tmp/claude-502/cr169-heavy1-integration.log, /private/tmp/claude-502/cr171-heavy-integration.log.
