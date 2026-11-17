# Palette: the block editor closes right after a click (focus bounce)

Stress `palette` intermittently fails with "Timed out waiting for Heading 2 to prefix the line.
Editor state: BODY":

- main 0941cc09, heavy run 43582068953 attempt 1, round 10 of 20 (attempt 2 green);
- branch heavy run 43536948441 attempt 1 (v1.9.0 release);
- same signature on `alert-dropdown`: stress 43416264245 (round 15/20), integration 43576429177.

CR-326's diagnostics (its A-10): the block editor loses focus about 290 ms after a click, in a
window VS Code reports as focused (`window.state.focused=true`); the active element goes through
`body`, then the workbench re-focuses the webview iframe. Not proven whether it is the test host
(late window activation) or VS Code moving the focus, which a user could hit. Related:
SwRS-MDOKFSTUDIO-BLOCK-047. CR-326 archive:
`.agents/changes/4-archives/261114-0947-326-flaky-real-window-integration-steps`.
