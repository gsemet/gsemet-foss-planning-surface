driver: driver-041-opus · updated: 14:56
status: ready · step: 10 Notify · round: 4/6
head: 9d2e885 · PR: #35 · run: 39955908306 pass (all required + stress 120/120)
next: user merges PR #35 · question: —

- [x] 1 Pick · [x] 2 Grill · [x] 3 Opened, worktree markdown-okf-schema-studio-wt-041, branch `fix/ci-stability` · [x] 4 Brief · [x] 5 Code (r2) · [x] 6 Review (r2 APPROVE) · [x] 7 Commit 36bdf5f, c2e040c (r3 APPROVE) · [x] 8 PR #35 updated · [x] 9 CI green (39955908306 on 9d2e885) · [x] 10 Notify · [ ] 11 Land

## Was blocked (driver-041-opus, round 3/3; resolved in round 4)

- r2 fixed case 2 (Ctrl/Cmd+A forwarded to the workbench) and the waits; r3 limited apt/browser
  installs to the visual job with a .deb cache (cache filled in 39945708423 a2: 46 archives).
- 39945708423 on c2e040c: a2 green, a3 green, a4 red: stress round 1/20 `table-tab`, "Timed out
  waiting for Tab in the new row ... textarea to have the caret"; host panelActive false; trace:
  content patch closes the cell editor at 704 ms, page blur (active=body) at 836 ms. Integration and
  visual green in a4.
- Diagnosis (inferred): same class as case 2: Tab is forwarded to the workbench while VS Code's
  250 ms focus poll does not yet report the re-rendered webview focused, so the workbench moves focus
  out of the preview (panelActive false). Fix: keep Tab/Shift+Tab inside the page while a cell
  editor is open (like selectAllKey), and/or a host-reported "webview focused" signal before keys.
