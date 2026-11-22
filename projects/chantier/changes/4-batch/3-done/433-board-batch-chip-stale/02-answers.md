Short name: `chip`

# Answers
1. chip-Q1 (2026-11-21): **What a batch CR's card shows instead of the 3-ready chip.** A. No priority chip on a card of a CR in the batch (`4-batch`): its state (working, queued, ready) is already shown beside it.
Restatement (2026-11-21): a CR in the batch shows no priority chip in any board view that draws it as a batch CR (the batch graph first); the backlog views keep their chips.
2. chip-Q2 (2026-11-21, the user's word): **Grilled enough, destination.** "tu peux lancer board-batch-chip-stale tout de suite dans le batch": the spec-writer, then the critic; destination batch-30 at once.
3. chip-Q1 changed (2026-11-21, the user's words): "affiche son dossier quand meme": a batch CR's card shows its real folder in the batch (`1-pending`, `2-actives`, `3-done`) in place of the old priority chip, never `3-ready`. Replaces answer 1's "no chip".
Spec v1 (2026-11-21): written to answer 3 (server sends `stage`, four batch views draw it, `priority_of` removed); one open question.
4. chip-Q3 (2026-11-21, spec open question 1, settled by the Chief of Staff, the user's preference for the simple option): **The Kanban page's batch CR card.** Unchanged, out of scope: its column already shows the state. The user may reopen it.
Spec critic run 1 (2026-11-21, v1), fixes that need no user, for the next writer run: (1) add docs/web-board.md:36 to "What changes" (the top row begins with the batch folder in a grey chip); (2) drop the three `.tag.pri-<folder>` rules: the plain `.tag` is the neutral chip, as `pri-inbox`; Evidence checks chip.css holds no rule for them; (3) overlap bullet: board-batch-kanban reads the row's `stage` for its columns, its cards' chip decided there; board-batch-compact no overlap; (4) test paths under skills/chantier/scripts/cli/tests/. No question for the user; final after this run.
Spec v2 (2026-11-21): critic run 1's fixes 1-4 in; no open question. Final.
