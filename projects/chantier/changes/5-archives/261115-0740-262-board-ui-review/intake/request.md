# Review the web board's pages with the user, one by one

Filed 2026-11-14 by the Chief of Staff, on the user's word: "Note le en nouvelle CR
"board-oui-review" on fera un tour ensemble de chaque page et je te dirais ce qui ne va pas".
To grill with the user: a tour of each page of `chantier board` (Home, Kanban, Batch, Costs, and
the backlog editing pages), the user saying what is wrong on each.

## What the user saw on the Kanban (2026-11-14, main at fa5b460)

The user's words: "Je vois bcp d intake (qui devrait s'appeler inbox), plein de grill, et zéro
fini dans la vue Kanban".

- The first column is named "Intake"; it holds `1-inbox` and should be named "Inbox".
- The "Grill" column holds the whole backlog, P1 to P4, raw items included (11 cards), so it
  reads as if all of them were being grilled.
- No column shows what is done: merged CRs appear only as a count ("141 merged"), though the
  board's state carries the `merged` list.

## What the Chief of Staff saw on the same day

- The Kanban's header says "0 in progress" while its In progress column holds CR-228, blocked;
  Home says "1 in progress".
- Home's "Waiting for you: 44 questions" counts the Foreman's unread asks to the Chief of Staff,
  not questions for the user.
- In French, column names stay in English ("In progress", "3-ready") beside French ones.
- The card of `cr-folder-self-contained` is titled "Intent": the title comes from a heading of its
  file, not from its request's title.
- Home stayed on "Loading..." at the first load after a restart; a second visit drew it.

## More from the user (2026-11-14, evening, main at ce00ec3)

- "il manque une page par rapport au prototype du board : je n'ai pas la page backlog. il faut
  donc la rajouter." In the prototype (`5-archives/261114-1354-222-visualization-backend/prototype/`)
  the Backlog (lanes P1 to P4, drag up and down) sits in the Triage view; the board has a
  `triage` view (`views/triage.js`, registered in `views/registry.js`), but `fr.js` and
  `fr-write.js` have no `nav.triage` word (only `en-write.js` has it). Not checked on screen.
- "dans la page kanban j'aimerais pouvoir choisir les Priorités affichées (par exemple cacher
  les P3 et P4)."
- "la page coût ne me permet pas de voir les coûts des batches précédents." The closed batches'
  costs are in `5-archives/batches/batch-NN.json`; the Costs view does not read them.

## The page-by-page tour (2026-11-14, evening, main at ce00ec3)

### Home

- "recent activity vide, pas d'info sur les batch fermés et les CR des batches précédents": the
  recent-activity feed is empty (no batch running), and Home says nothing of the closed batches
  or of the CRs of earlier batches (the records in `5-archives/batches/` and the archived CRs).
- "on a pas mal de grill en cours et pourtant je vois que des 0": several CRs are being grilled
  (inbox items with `02-answers.md` or a `03-change-spec.md`: fast-scenario, baseline-and-legacy,
  board-cr-step, worker-reply-length...), yet Home shows only zeros.

The columns are fixed in `skills/chantier/scripts/cli/src/chantier/board/web/js/views/kanban.js`.

**Caveat:** up to the Home notes above, the user toured an old build of the board that uv's cache served (`uvx --refresh --from <checkout>`): it had no Triage view. From the Triage page on, the board runs the live code of main at ce00ec3 (`uv run --project`). The Home notes are to be checked again on the live board.


### Triage (live board, main at ce00ec3)

- "les cartes n'ont pas le même style, titre, etc que dans les autres pages": Triage's post-its do not share the cards' style and title of the other views (Kanban, Home).
- "il y a un détourage lors de la sélection en bleu pas beau": selecting a post-it draws an ugly blue outline (likely the browser's focus ring or the selection's outline).
- Kept: "l'effet pour prendre une carte est sympa je garde" (the pick-up effect of a dragged post-it stays).


### End of the first tour (2026-11-14)

The user: "ok pour l'instant". Home's notes stand on the live board; Kanban adds nothing to the notes above. Batch and All projects were not toured; Costs has the note above (earlier batches' costs). The CR delivers what is noted; a later tour may file more.

