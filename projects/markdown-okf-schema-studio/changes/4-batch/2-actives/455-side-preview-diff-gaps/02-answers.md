# Side preview next to a diff: scroll, replace preview, title button

See intake/request.md.

## Grill, 2026-11-21 (owner's answers, asked by the Chief of Staff)

- dg-Q1 (which file). Owner: "Le vrai fichier": Studio's editor title button shows on a diff editor of a .md file and opens the preview of the real file (the modified side); 'Open Preview to Side' from the search-and-replace preview opens the real file's preview; the side preview follows the diff editor's scroll.
- Owner, 2026-11-21: "Et tout ça partira dans le batch en cours": once final and ready, added to the running batch-07.

## Owner's answers, 2026-11-21 (Fable spec critic's questions)

- dg-Q2 (diff with no real file: staged, timeline). Owner: "Ouvrir le fichier réel": the button opens the preview of the working-tree file at that path, with no scroll following; refuse only when no such file exists.
- dg-Q3 (marker when a search click with a replace text opens the replace preview). Owner: "Oui, sur le vrai fichier": same arrow and band on the real file's line, if the jump can be detected on a diff side; specified in side-preview-jump-marker, stacked after this CR.
- dg-Q4 (a diff becomes the active editor). Owner: "Oui, tout diff": the side preview switches to the diff's real file by itself, as it already does for a git diff.
- dg-Q5 (scroll impossible because of VS Code). Owner: "Livrer le reste": the button and the command ship; the scroll becomes a written known limitation plus a new inbox item.
- Settled by the Chief of Staff from the critic: preview→diff reveal and caret mark behave as with a text editor, under the existing settings, aimed at the real file's side (observe today's behaviour first; LIFE-108); multi-file diff and merge editors out of scope (no input class in the API); replace preview previews the real file (left side), no question; in a compare of two real .md files, the preview shows the side with the cursor, as today.
