# A fresh preview gets no keyboard focus until it is clicked

Found by CR 152 (2026-10-28, PR #164). In the CDP-driven test window, a newly opened preview does
not receive keyboard focus until the page is clicked: arrow keys go to the workbench. The heavy
integration test `windowSwitchKeys` only passed because its edit-mode toggle click focused the page;
when a previous test left edit mode on, the click never happened and keyboard block selection failed.
Recorded as a Known issue (SwRS BLOCK-004).

## To do

- Check in a normal VS Code window whether a new preview (and a preview opened in edit mode) takes
  keyboard focus on open; if not, decide whether the panel should focus the page on reveal.
- Make integration scenarios independent of the edit-mode state remembered by the workspace.
