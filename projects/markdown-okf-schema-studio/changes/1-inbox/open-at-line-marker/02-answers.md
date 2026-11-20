# Answers

Short name: `open-at-line`

## Series 1, 2026-11-20

1. open-at-line-Q1: **How Studio gets the line.** A, Studio decides itself to open `.md` files: a Studio setting ("open Markdown files in Studio") replaces the VS Code `workbench.editorAssociations` entry; the text editor opens for a moment at the line, then Studio takes its place at that line, with the marker. (Context given: with the association, `resolveCustomTextEditor` receives no line; only a text editor gets it.)
2. open-at-line-Q2: **Entry points.** A, all of them, no closed list: whatever opens the text editor at a line (search, Quick Open `file.md:42`, Problems panel, terminal links, Ctrl+click, Outline...).
3. open-at-line-Q3: **File already open in Studio.** A, the same Studio tab scrolls to the new line and the marker moves; no new tab.
4. open-at-line-Q4: **Raw text asked on purpose.** A, Studio never replaces a text editor the user asked for on purpose ("Reopen Editor With > Text Editor", a Studio "open source" action): the text editor stays.

## Series 2, 2026-11-20

Retained mockup for the marker: `prototypes/01-arrow-marker/`, option A.

5. open-at-line-Q5: **The setting's default and the first-time notice.** Free answer (not A): the setting is **on by default**. The first time, a notification shows for a few seconds explaining that this behaviour can be changed in the settings. Owner's words: "allumé, la premiere fois une notification s'affiche pendant quelques secondes expliquant que cette association peut être changée dans les settings. met en place un systeme qui permet de reset ces notifications d'introduction de feature car je peux etre amener a en faire d'autres. par contre c'est qu'une fois, apres fermeture ou disparition, ca ne revient plus meme dans les prochaines sessions". So: a reusable "feature introduction" notice system (other features will use it), each notice shown once only, never again after it is closed or disappears, even in later sessions, and a way to reset these notices.
6. open-at-line-Q6: **The marker's look.** A, an arrow in the left margin at the exact height of the line, plus a light band on that line.
7. open-at-line-Q7: **When the marker goes away.** A, it stays until the user clicks in the page, starts an edit, or another line is requested; scrolling does not remove it.
8. open-at-line-Q8: **A line inside a block.** A, as precise as possible: the exact line in a paragraph or a code block, the targeted table row, a folded section or admonition is unfolded to show the line; otherwise the top of the block.
