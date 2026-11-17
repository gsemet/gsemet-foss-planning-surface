# Hotkey in edit mode

Make the edition mode browsable in edit mode.

edit mode on an empty file, enter to enter in edit mode, ctrl+enter (cmd+enter) to validate, escape to cancle.
Allow to navigate in block edit with up/down.

allow to move blocks

fix also the fact we cannot add a block just after a figure, or if a figure is at the end of the document

when editing a panel, Ctrl+z (or the vscode shortcut for undo) is not respected.

on a text selection, using `_` or `*` replace the text instead of adding 1 before and 1 after and keep the text, then retyping on * readd another.

When editing a cell on a table, the arrow key does not move cell to cell but block to block -> should be cell to cell first.

Beware when editing a paragraph, when on the second line, and moving up to the first, instead of just going to the first line it actually switch the edition block to the one on top.
Same on keydown on the second line. I suspect it comes from the wordwrap inside the edit box.

Ctrl+/ (or cmd+/, or the vscode shortcut equivalent) to create a TODO item at the cursor position. When clicking on it, it expands and displays the multiline TODO text (like in a TODO admonition).


