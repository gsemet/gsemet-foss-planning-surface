# CR 205 report: alert-dropdown flake reproduced once (2026-10-31)

## Occurrences since #220/#221 (main 9b53edbe)
Heavy runs with a stress job after that point: 40830553206, 40828891957, 40896825598, 40907458963, 40909738719
(version commit): all stress green, 20 rounds each, no alert-dropdown failure.

## Loops (proof branches, stress_repeat / stress_scenarios dispatch inputs, now deleted)
| Run | Code | Scenarios x rounds | Result |
|---|---|---|---|
| 41145454738 | main 6a2cb9d8 | alert-dropdown x100 | FAILED at round 40 (39 clean) |
| 41145466497 | main | save-position,slash-menu,alert-dropdown,toc x60 | green (60 clean alert-dropdown) |
| 41147040315 | main | alert-dropdown x100 | green (100 clean) |
| 41148934849 | main + CR 203 layout 806ec581 | alert-dropdown x100 | green (100 clean) |
| 41148945236 | same | alert-dropdown x100 | green (100 clean) |
Main-based: 1 failure in 200 rounds. 203 layout: 0 in 200 (the Foreman's own failure on the 203 stack, run 41147405310,
has the identical signature, so the layout neither causes nor visibly raises it).

## Reproduced signature (see repro-facts.md)
The block editor textarea blurs (related=none, commit, pageFocus=true) ~76-87 ms after the harness starts the WARNING click,
and the page blur follows 1 ms later (same Chromium task). No mousedown on WARNING reached the page. The host never recorded a
window focus loss; the workbench recorded no focus move. The webview frame lost focus inside the window by itself.
Not the palette position/scroll: the press never reached the menu, and the identical trace occurs on main.
Not a user problem (CR 198): blur happens before the pick; BLOCK-047 commit-on-leave unchanged.

## Cause
Not found beyond "the webview frame loses keyboard focus inside a focused window while Playwright prepares the click".
No product code in the page or host was seen to move the focus, but the product does move editor-group focus in the
background (groupFocus.ts, groupLock.ts, panel.reveal): ruled out only for the one captured case (no product focus move in the dump).

## Fix attempt, not landed
Round 3 added a test-side single redo for this signature (patch: round-3-unapproved-redo-rule.patch). The Inspector said
CHANGES REQUIRED (round-3.md): "no window loss" is only absence of evidence and would also hide a product-caused focus move;
the rule needs positive proof (no product focus move during the step via previewGroupFocusMovesForTests, no workbench focus
move with the webview still active) and a window-focused-at-step-start check. The 3-round budget was spent, so it was not
committed. The patch plus round-3.md list the required changes.

## Lasting value kept
One commit: stress_repeat / stress_scenarios dispatch inputs (+ safe ci-stress argument handling). A PR for diagnostics alone
is not worth it; the loop knob is worth merging because it reproduced the flake at 1/200.
