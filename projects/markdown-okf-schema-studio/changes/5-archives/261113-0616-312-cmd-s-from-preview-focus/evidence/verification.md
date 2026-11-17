# CR-312 verification at aed1a0ad

Verdict: VERIFIED (one non-blocking note).

## Heavy CI run 43344012200 (head aed1a0ad)
integration, stress, visual, static, static-windows, report, checks all green. Integration log:
"STEP start: save-key" / "STEP done: save-key (7536 ms)" (test/integration/saveKey.test.ts, real window).
That scenario presses MOD+s inside the autosave delay and asserts: not dirty, text holds typed value,
dirty mark stays off after 800 ms, for
- block editor (textarea keeps focus and value),
- table cell editor (textarea keeps focus and value),
- frontmatter field (title: Fieldtyped saved, field closed),
- custom editor (decision 5), "Tail. customTyped" saved and clean.

## Local targeted unit runs (tsc then node --test), 59 tests, 0 fail
- test/session/saveCommand.test.ts: no focused preview does nothing; slow autosave applied before save;
  editor stays active; frontmatter pendingSaves waited; page not ready saves at once; page never answers
  saves after bounded wait; one save only.
- test/page/runtimeSaveKey.test.ts: cell autosave posted before save request, editor open; frontmatter
  flush then save request; refused plain save re-flushed; no result after bounded wait.
- test/core/protocol hostToPage/pageToHost: new messages validated.
- test/security/package-contract.test.ts: command, key binding (ctrl+s / mac cmd+s), when clause with
  activeWebviewPanelId preview OR activeCustomEditorId editor, absent from the palette ("when": "false").

## package.json (decision 5)
keybinding when = "activeWebviewPanelId == 'markdown-okf-schema-studio.preview' || activeCustomEditorId == 'markdown-okf-schema-studio.editor'".

## Note
work/pr-body.md still contains "Custom editor (decision on the binding): RESULT_PLACEHOLDER". Fill it before
the PR is marked ready. The integration test does not show that the native save alone would have failed, so the
recorded reason for adding the clause must come from the coder's check.
