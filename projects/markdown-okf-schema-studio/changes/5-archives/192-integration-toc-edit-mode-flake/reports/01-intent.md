# Backlog (P2): integration step `toc` — "Edit mode did not switch to off after 3 clicks"

Seen in heavy run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40784022530
(CR 173 branch, 2026-10-29); the next heavy run of the same code was green. Similar click timeout on
main (b71f run).

- Where: `setEditMode` helper in `test/integration/realInput/harness.ts`, real VS Code window under
  xvfb, trusted suite step `toc`.
- Symptom: three clicks on the Edit toolbar button do not switch edit mode off.
- Not diagnosed: whether the click misses (toolbar collapsed, overlay, focus) or the page ignores it.
- Next step: log the button state (`data-edit-mode`, `aria-pressed`, bounding box, element at the
  click point) before each click; wait on state, not time. Fix test-side unless a product bug shows.
- Rule 12: a flake is fixed, never ignored.

Second occurrence: heavy run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40790025503
(CR 187 branch, scenarioToc in tocWindow.js); rerun green.
