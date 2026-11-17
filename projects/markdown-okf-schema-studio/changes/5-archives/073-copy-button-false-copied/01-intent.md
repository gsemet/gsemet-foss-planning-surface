# The copy button shows "Copied" when nothing was copied

Current behaviour (specified as such in SwRS-MDOKFSTUDIO-CODE-026 and CODE-027, flagged
"Known issue"):

- The page shows "Copied" as soon as the code-block copy button is clicked.
- The host refuses the copy silently when the text is not a string or exceeds 1 000 000 UTF-16
  code units (`src/core/protocol/pageToHost.ts`, `previewCopyText` validator).
- The host also drops the copy when the page's document version or render request is no longer
  current (`src/session/pageMessages.ts`, `PAGE_MESSAGE_GATES.previewCopyText` = `render` gate),
  for example when text was typed since the page rendered. The clipboard is unchanged, but the
  button still says "Copied".

## Expected

- The host answers every copy request (`previewCopyResult`: copied / refused + reason), and the
  page shows "Copied" only on success, otherwise a short refusal text.
- Copy edits nothing, so it should not need the stale-render gate: relax it to the panel/context
  check only.
- Tests: unit (validator + dispatcher gate), page (label follows the answer), one real-window
  check. Update CODE-026/027 in the same change (remove "Known issue").

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
