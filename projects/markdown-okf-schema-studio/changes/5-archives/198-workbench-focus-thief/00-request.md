# 198 — Stress/integration: find what steals the focus inside the workbench (test environment only)

Type: test environment · Priority: P1 for the 1.0.1 stack (joins only if proven in time) · CoS 2026-10-29.

Context: CR 194 (PR #206) showed that the Linux alert-dropdown failure (run 40796963673 on branch
`change-requests/188-real-input-click-then-find-race`) is a focus move INSIDE the VS Code workbench
(`windowState.focused:true`, page blur, then content patch and the block editor commits on blur per
BLOCK-047), not an OS window blur. Hang logs show `ChatModelSelection` lines (chat/Copilot activity).

1. Diagnose: add to every real-window failure dump the WORKBENCH active element (main window via CDP:
   `document.activeElement` tag/classes/aria-label/id path, focused part — editor, panel, sidebar,
   auxiliary bar, chat, notification toast, quick input) and the VS Code focus context keys if
   reachable. Also list visible notifications/toasts and open views at failure time.
2. If the dump or the logs point at chat, Copilot, notifications, welcome/walkthrough, or similar:
   switch them off in the TEST PROFILE only (user-data-dir settings / disabled extensions / CLI flags
   used by the integration launcher), never in product code. Record the reason per setting.
3. No blanket retries, no raised timeouts, no sleeps.

Proof: `just check`; READY PR from origin/main; normal CI + heavy runs (up to 3) with alert-dropdown
and review-threads green; the dump shown on a forced failure (unit test of the dump builder, or a
deliberately failing throwaway step removed before the final commit). If not proven by assembly
time it stays out of the stack and the backlog item P2/alert-dropdown-window-blur stays open.
