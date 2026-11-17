# Reproduction of the alert-dropdown flake (CI run 41145454738, stress job, round 40 of 100, alert-dropdown only)
Failure: "Timed out waiting for Warning to change the type. (no redo: no block editor commit on a window blur since the step
started at 579 ms: commit at 722 ms (related=none commit active=body pageFocus=true): not a blur to nowhere in a page that had
lost the focus) Editor state: {"tag":"BODY"}". Full log: /private/tmp/claude-502/cr205-driver/stress1.log (stress job).
Step log (step clock ms): open preview 0, edit mode on 149, paragraph click 463, End 639, alert click 643, type list 729,
steady editor 766, warning click 787. Page clock = step clock - ~141 ms (alert mousedown page 502 <-> alert click step 643).
Page editorTrace (page clock):
 0 page; 218 mousedown svg active=body pageFocus=false; 218 page focus; 340 mousedown p; 342 block editor opened;
 368 block editor focused; 502 mousedown action=alert prevented=true active=textarea pageFocus=true;
 722 block editor blur "related=none commit active=body pageFocus=true"; 723 page blur "active=body pageFocus=false";
 811 content patch; 812 block editor closed.
=> no mousedown option=WARNING ever reached the page; the textarea blurred at ~76 ms after the harness started the WARNING
   click (step clock ~863), page lost focus 1 ms later (element blur first with document.hasFocus() still true, then the window blur,
   the same Chromium task).
Host: windowStates only [{at:927, focused:true}] => the VS Code window NEVER lost OS focus; windowState focused:true, active:true.
Workbench focus dump at failure (main doc read over CDP): focused part webview, active element iframe.webview.ready, hasFocus=true;
no workbench focus move (focusin/out, window-blur/focus) recorded after the step start (last: step start); the outer
webview index.html frame: hasFocus=false, active element body. i.e. the webview frame lost focus INSIDE the window with no
workbench-level event. Harness focusMoves: workbench.action.focusFirstEditorGroup at -3836 and -1006 ms before the step.
Existing redo rule (test/shared/editorBlurInterruption.ts) requires pageFocus=false at the commit AND a host window-state loss,
so it rejected this signature. Other runs: 4 scenarios x60 (save-position, slash-menu, alert-dropdown, toc): 240 clean scenario-rounds.
