# Follow-ups of CR 043

## Real-window captures removed by the re-scope (decision 7)

Implemented, then removed from the branch. The code is in commit bc414d4 (PR #36 history), and
CI run 39963915074 passed all of them once in the integration job:

- standalone read-only (`trust-security`): standalone suite moved onto the CDP browser-suite list,
  capture of a file outside the workspace.
- MyST conf.py warning (`myst`): capture with the Problems view open.
- label rename from the anchor icon (`myst`).
- Back/Next across documents (`toolbar-navigation`).
- Refresh Preview command and the Cmd/Ctrl+K Shift+V keybinding (`lifecycle-sync`, 1 capture + 1
  assertion-only).
- doubleClickToSwitchToEditor (`toolbar-navigation`, assertion-only): the host holds a block edit
  only from its first autosave, so the "nothing revealed in edit mode" check is ordered on that
  autosave (fix in bc414d4).

## Product observations from the captures

- The conf.py MyST warning is only in the preview's status region, which a successful render keeps
  visually hidden (`[data-sphinx-preview-status="success"]` is screen-reader only). The Problems
  view and the editor squiggle show it. A visible hint in the preview may be wanted.
- An image pasted at the end of a paragraph (`Text. ![image.png](image.png)`) renders above the
  paragraph text in the preview (seen on the image-paste capture). To check whether this is
  intended.

## Local run on macOS: undo never restores the buffer (pre-existing)

- `npm run test:integration` on this Mac uses `/Applications/Visual Studio Code.app` (1.143.0; CI
  downloads 1.143.1). Every undo step fails there: `checkboxToggle.test.ts` "one undo to restore the
  original source" (3 of 3 runs) and real-input "one undo to restore the paragraph".
- Reproduced on origin/main (scratch worktree, `--trusted-only`): not caused by this change.
- Diagnostic: the page has the focus (`document.hasFocus()` true, active element
  `div.native-edit-context`), the document is the active editor, and even
  `executeCommand("undo")` leaves the buffer unchanged. CDP focus emulation did not help.
  Suspects: the native EditContext of 1.143.0 on macOS. Next step: run against 1.143.1
  (`vscodeExecutablePath` override) to confirm.
- Because the checkbox test runs first, the trusted suite stops before the real-input suite.
  The four new tests were run locally in isolation through the stress mode: 5 of 5 rounds each.

## README images (F check): not refreshed

- Committed `images/readme/` is byte-identical to B0 (pixel diff 0 on all 15).
- From the CI artifacts of run 39966448771 (Linux): all 15 differ from B0 (mean abs diff 3 to 21 per
  channel): font rendering differs between Linux CI and the macOS run that made B0. CI cannot
  produce byte-equal README images; the check needs a macOS render.
- From the local macOS visual run: 12 of 15 match B0 within antialiasing (under 0.6 % of pixels).
  `toolbar-expanded`, `schema-properties` and `edit-frontmatter` differ by about 8 %: the toolbar
  has a new review-comments button (a product change on main since B0, not in this PR).
- `images/` not committed. Follow-up: refresh the README images from a macOS run in a docs PR.
- The pixel comparison ran in an ephemeral `uv run --with pillow` environment (downloaded Pillow
  into the uv cache, outside the project).
