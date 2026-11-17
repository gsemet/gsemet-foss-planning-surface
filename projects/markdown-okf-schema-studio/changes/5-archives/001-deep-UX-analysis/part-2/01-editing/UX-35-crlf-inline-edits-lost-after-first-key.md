# UX-35 — In CRLF documents, inline edits stop being saved after the first keystroke

| Field | Value |
| --- | --- |
| Severity | High |
| Confidence | Reproduced (spy change log shows a single applied edit) |
| Area | Inline block editing, line endings |
| Modes | Side preview (Open With uses the same path) |
| Evidence | [p2-crlf-after.jpg](../evidence/p2-crlf-after.jpg) |
| Related | STAB-07 (`../../deep-analysis-review/07-stability-and-correctness.md`), reproduced in the UI: `> [!NOTE]` renders as a plain blockquote in CRLF files |

## Use case

An author on a Windows-configured repository (CRLF line endings, common in Renault/Ampere
projects with `core.autocrlf`) edits a two-line block from the preview.

## Steps to reproduce

1. QA workspace `synth/crlf.md` (generated with CRLF endings by `setup-workspace.sh`).
2. Side preview, edit mode on, click the blockquote "A GitHub alert in a CRLF document".
3. Type ` Edited.` then Enter and `New line inside.`, then click elsewhere.

## Observed

- The first keystroke (a space) is written to the buffer (document version 2).
- No further change reaches the document: the textarea keeps "Edited. / New line inside.", and
  the editor's status line reads **"The preview is stale. Reopen the block before saving."**
- The source editor shows only the trailing space. If the user closes the editor or the preview
  re-renders, the typed text is gone.

## Where it comes from

- A `<textarea>` normalizes `\r\n` to `\n` in its value; `postBlockEditSave` sends the LF text
  (`src/webview/scrollSync.ts` L1480-L1482, only the trailing line ending is restored).
- VS Code normalizes the inserted text to the document's CRLF. On the next keystroke,
  `drainActiveBlockEdit` (`src/extension.ts` L1122-L1126) compares the CRLF range text with the
  LF `lastSavedText`, concludes "the source block changed", and clears the edit. Every later save
  is then rejected as stale (`handlePreviewEditSave`, L1158-L1165).

## Suggested direction

Normalize to the document EOL in one place: convert the textarea text to the document's line
ending before saving, and compare normalized strings in `drainActiveBlockEdit`. Add the same rule
to frontmatter patches and table serialization (which already keep `lineEnding`).

## Test to add

Real-input E2E on a CRLF fixture: type several characters including Enter in a multi-line block;
assert the buffer contains all of them with CRLF endings and no status error.

## Done when

Inline editing behaves identically in LF and CRLF documents.
