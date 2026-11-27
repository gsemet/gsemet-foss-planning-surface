# Review comment threads stored in the document as HTML comments

Store the review comment threads in the Markdown file, as HTML comments, in place of the
`.comments.json` file beside it. The owner calls it an important change of requirements. To grill.

The owner's words (2026-11-27, Chief of Staff session of batch-09), verbatim:

"en fait je pense que le fonctionnement actuelle de ce mode de commentaire est pas bon, on modifie un
fichier a coté avec des index vers les debuts/fin. je pense pas qu un agent puisse s en sortir
facilement sans tools special. alors qu'un commentaire HTML avec le tag
`<!-- Threaded-Comment: .... -->`.

On mettrait le fil dans le fichier. C'est un changement de requirements important mais je pense que
c'est ce qu'il faut faire. Pour l'utilisateur ça ne change rien. Il faudra griller ce point, et il
faudra un settings pour l'activer ou desactive (laisser actif par defaut).

Donc, si tu penses que l'on est capable de fixé le bug reporté sans intégrer ce CR, super. sinon il
faudra faire modifier le comportement (requirements, docs,...)"

Earlier, 2026-11-26, during the issue 547 work: "Si c'est le cas on désactivera la feature
commentaire en thread et on fera une CR pour mettre le fil de commentaire dans le fichier au lieu du
json à côté".

Later, 2026-11-27, answer to perf547-Q6 ("every save of a previewed document computes the comment
index, even with no comments file; note it as an idea to grill after batch-09?", choices "A. yes
(recommended)", "B. no, leave it"), verbatim: "Non , je veux supprimer ce fichier de commentaire".
Read by the Chief of Staff: no separate idea about the indexing; the `.comments.json` file goes, which
is this change.

Then, 2026-11-27, same session, verbatim: "Pas de migration des commentaires existant cette feature
n'est pas utilisée". Settles for the grill: existing `.comments.json` files are not migrated.

## Place against issue 547

Chief of Staff's judgement of 2026-11-27: the reported bug can be fixed without this change
(`perf-547-slow-comment-selection` and `perf-547-comment-update-and-author` in batch-09). The three
causes the issue suspects do not come from the JSON file. To confirm with the "after" real-window
runs, not made yet. So this change is not added to batch-09.

## Seen in the repository (main at 1953eaa)

- Today: `<name>.comments.json` holds the threads, each anchored by line, end line, quote, prefix and
  suffix, with a resolved state (`docs/user/review-comments.md`, `src/session/features/comments.ts`).
- The Studio already has inline thread comments kept in the file as one HTML comment opened by
  `<!-- THREAD`, with messages `Author (YYYY-MM-DD HH:MM):` (`src/core/comments/inlineThread.ts`,
  StRS-MDOKFSTUDIO-REVIEW-015): shown as a chip, with Reply and Delete thread; the palette inserts a
  new one. It is anchored at one point of the Markdown, not on a quoted passage, and the module shows
  no resolved state.

- GitHub issue 547 (open, from an outside user, 2026-11-26) describes a document with 9 review
  comment threads in `.comments.json`: someone outside the project appears to use the feature. Told
  to the owner on 2026-11-27.

## To grill

- The tag: the owner's `<!-- Threaded-Comment: ... -->` or the existing `<!-- THREAD`.
- How the commented passage is marked in the file (highlight of the selection), including in a table
  cell, a code block or over several blocks.
- Resolve, reopen, delete; the orphaned list.
- Writing a comment then changes the document itself (unsaved changes, Git diff): when it is written
  and saved, and what happens in Restricted Mode or on a read-only file.
- Existing `.comments.json` files: no migration (owner, above). To confirm: no longer read at all.
- What the setting switches (the whole thread feature, or the storage), and its default: on.
- The writing skill, the user documentation and the requirements to change.
