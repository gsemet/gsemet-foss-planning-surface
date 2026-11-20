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

## Series 3, 2026-11-20 (not answered: the item was set aside)

Questions asked, not answered: open-at-line-Q9 (remove the user's own `workbench.editorAssociations` entry that names Studio; recommended A, Studio removes it and the notice says so), open-at-line-Q10 (how to reset the feature-introduction notices; recommended A, a palette command), open-at-line-Q11 (edit mode; recommended A, same marker, no block editor opened on its own), open-at-line-Q12 (side preview; recommended A, same marker on a jump, not on every cursor move).

Owner's clarifying question before answering: "attent tu veux dire que je peux pas avoir les deux, l'association md automatique avec studio comme maintenant ET l'ouverture a la ligne lors d'une recherche ?" Answer given: yes, both, but the automatic opening must be done by Studio itself (its own setting) instead of the VS Code association, which loses the line; the text editor may show for a short moment before Studio replaces it (to be measured by trials).

9. **Decision: set aside in P3**, 2026-11-20. Owner's words: "met la de coté en P3 avec le drawback que l'ouverture du text brute risque de tjs boucler sur studio". The drawback to keep in mind when the item is taken up again: with Studio taking over every `.md` opened in a text editor, opening the raw text on purpose risks always looping back to Studio (open-at-line-Q4 asked that a text editor opened on purpose stays, but how to tell it apart reliably is unproved). The grill resumes at open-at-line-Q9.

10. **A setting "open searches in Studio", on by default**, 2026-11-20 (given after the item was set aside). Owner's words: "il faudra un settings \"ouvrir les recherche dans studio\", on par defaut." Open at the resumption: whether this setting replaces the general "open Markdown files in Studio" setting of open-at-line-Q1/Q5 (only an opening at a line, from a search or another jump, goes to Studio, which would avoid the raw-text loop) or comes in addition to it.
