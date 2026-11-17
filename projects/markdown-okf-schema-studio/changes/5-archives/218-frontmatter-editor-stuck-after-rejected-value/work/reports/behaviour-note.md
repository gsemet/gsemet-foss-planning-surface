# Behaviour change — a refused front-matter value no longer strands the field editor

## Today (reproduced in headless Chromium, visual harness, mock host refusal)

- Enter on `priority` = 7 posts the save; the control is disabled while the save runs, so focus drops to
  BODY. The refusal ("Schema validation failed: must be <= 5") re-enables the control but focus stays on BODY.
- Typing `4` + Enter goes nowhere. Escape does nothing: the document Escape handler only acts inside the
  properties section. A click on `title` opens nothing because one editor is already open.
- If the author clicks back into the input and then clicks `title`, the blur posts the same refused 7
  again. The editor goes to "Saving frontmatter…" and `title` still does not open.

## After (proposal)

1. After a refused save, focus returns to the field control (caret at the end; a list editor gets its
   own focus), so a corrected value + Enter saves at once. Focus is not taken back if the author has
   already moved focus to another control.
2. Escape closes the refused editor without a save, from the control or from anywhere in the properties
   section. The field shows its saved value.
3. While the editor still holds the refused text, a blur posts nothing again. A click on another field's
   value or key cell closes the refused editor without a save, discards the refused text and opens the
   clicked field in the same click. This is the rule BLOCK-041 already applies to a click on a block.
4. If the author changes the text after the refusal, leaving or Enter saves the new text once, as today.

## Requirements touched (all proposed; no approved requirement changes)

- SwRS-MDOKFSTUDIO-FMEDIT-019 (proposed): refusal scenario gains "focus returns to the control" and the
  click-another-field row; its known issue is removed.
- SwRS-MDOKFSTUDIO-BLOCK-041 (proposed): "Open a field editor" row gets the refused-editor exception;
  its known issue is removed.
