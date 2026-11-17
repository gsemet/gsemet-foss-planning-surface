# Little updated in Block Editor

![image.png](image.png)

Need:
- move the status line to the same line that the done/revert
- rename revert => Cancel
- Esc needs to do the same than Cancel (also in table cells; this replaces the UX-01 fix, where Esc keeps the text)
- Home/End move the caret to the start/end of the edited block (today on macOS they scroll the whole preview; in a table cell, End shifts the table ~440 px)

text is too big, use 1 size smaller

Edit mode in table cell does not use this editor, use with without the status bar (keep only the buttons, expanding vertically the cell). Ensure the table cell edit use the same text font and size




Display the following inline style even in edit mode:
- bold
- italic
