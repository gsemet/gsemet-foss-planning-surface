# 159 — Heavy CI regression: findInPreview replace-all note (HOTFIX)

Source: main session briefing (planner-tick run 7), 2026-10-28.

## Problem

Heavy CI (real-window `integration`) fails on main in `test/integration/findInPreview.test.ts`
(compiled line 206): expects `/cannot be replaced from the preview/`, gets `'Replacing...'`.
The suite stops at the first failure, so every PR's heavy proof is blocked.

Evidence:
- https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40677258004 — head SHA
  2992b50a01f5ce876f1b33859f2b669354c5e359 = main tip "feat: find and replace in the preview"
  (verified with `gh run view --json headSha`).
- https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40693008426 (PR #166 branch).

## Diagnosis (driver, read-only)

TEST race, product correct.
- Host `SourceEditsFeature.handleFindReplace` (src/session/features/sourceEdits.ts) awaits
  `this.apply(document, plan.edits)` and only THEN posts `previewFindReplaceResult`.
- Page `runReplace` (src/page/modules/findBar.ts ~355) sets the note to "Replacing..." and replaces
  it with "Replaced N matches; M matches cannot be replaced from the preview" when the answer
  arrives (routed by own id, survives the re-render).
- The test waits for `notes.getText() !== SOURCE` (true as soon as the edit applies, before the
  answer is posted) and reads the note immediately: it can read the transient "Replacing...".

## Decisions

- Fix the test: wait deterministically for the page's final status (the note no longer
  "Replacing..."), with diagnostics in the failure message; keep the assertion's intent.
- Do not touch tableMoves (PR #167).
- No behaviour change → no SwRS change; TOOLBAR-012 markers stay.
