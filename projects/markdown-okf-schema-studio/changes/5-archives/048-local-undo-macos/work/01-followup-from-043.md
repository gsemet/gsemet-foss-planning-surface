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
