# 199 — Real-window harness: focus the Studio editor group, not the first group

Type: test harness · Priority: P1 for the 1.0.1 stack (joins only if proven in time) · CoS 2026-10-29.
Based on CR 198's branch `change-requests/198-workbench-focus-thief` (PR #218, head 31a540b3; test
profile + workbench dumps). PR base: that branch.

Evidence (CR 198 heavy run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40806677284,
stress round 2/20, slash-menu): "/" lost (typed "Second paragraph.tab"); workbench active element
`div.editor-group-container.active.empty` ("Editor Group 1 (empty)") ~1.2 s after the harness's own
`workbench.action.focusFirstEditorGroup`, while Studio sits in another group; webview iframe shows
repeated blur/focus pairs. Same family as the alert-dropdown and slash-menu flakes tonight.

Scope:
1. Replace every harness use of `workbench.action.focusFirstEditorGroup` (and similar group-index
   focus) with focusing the group that holds the Studio webview (e.g. reveal/focus the Studio tab via
   its view column, or `workbench.action.focusActiveEditorGroup` after making the Studio tab active),
   then wait on reported state that the webview inner frame has focus. Find why an empty first group
   exists at all (layout from an earlier scenario?) and close/avoid it if it is a leftover.
2. Move ALERT-PICK-PROBE out of stress: run it once in integration (keep its assertions).
3. Fix the outer webview frame section of the dump ("none attached" on CI).
4. No blanket retries, no sleeps, no raised timeouts.

Proof: `just check`; READY PR (base `change-requests/198-workbench-focus-thief`); TWO heavy runs with
stress green (all scenarios incl. slash-menu, alert-dropdown, review-threads, toc) and the stress
duration reported (budget: 30 min timeout).
