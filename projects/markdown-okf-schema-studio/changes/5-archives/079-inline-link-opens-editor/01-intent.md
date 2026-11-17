# In edit mode, a link inside a paragraph is followed and also opens the paragraph editor

User decision (2026-10-25): P2, verify first.

Current behaviour (SwRS-MDOKFSTUDIO-BLOCK-014 (was SwRS-MDOKFSTUDIO-BLOCK-024), BLOCK-015, BLOCK-018, Known issue; read from the
handler order, no test): in edit mode a click on a link inside a paragraph posts `previewLink` and
the document click handler then opens the paragraph editor. Enter or Space on a focused inline link
does the same (the keydown listener excludes only properties-table links). Hovering the link
outlines the whole paragraph.

## Expected

- Verify in VS Code first (screenshot).
- A click, Enter or Space on an inline link follows the link only; hovering a link does not
  outline the paragraph. Clicking the paragraph text outside the link still opens the editor.
- Page test for click, keyboard and hover; update BLOCK-015/018/024 in the same change.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
