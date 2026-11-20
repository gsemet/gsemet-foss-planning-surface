Short name: `blank-runs`

Carried from `empty-block-reachable/02-answers.md` (Q1 owner's words, Q3, Q5) and its first spec's
section 2; decided by the Chief of Staff under the owner's autonomy rule (2026-11-20).

1. blank-runs-Q1: **Owner's words.** "en mode edition il faudrait que les ligne vide au dela que 1 (qui
   sert de delimiter en md) soit representé par un petit block vide, selectable par le clavier et
   clicable. et il faut rajouter un bouton a gauche Supprimer le block."
2. blank-runs-Q2: **What it is.** One blank-lines block per run of two or more blank lines between two
   blocks, at the start of the body and at its end. About one line high, edit mode only. Arrows stop on
   it; Enter or a click opens an insertion editor that replaces the run (Cancel or empty Done leaves the
   run as it was); Delete, Backspace or its Delete block button removes the extra lines and keeps one
   separator (all of the run at the top of a file without frontmatter and at the end of the body).
3. blank-runs-Q3: **Built on `empty-block-reachable`.** Reuses its `createDeleteBlockButton` and
   `deleteSelection()`; this CR lands after it in the stack.
4. blank-runs-Q4: **Blank** is the shared `isBlank` of `src/core/mapping/blockRange.ts` (no restated
   regex), so a line of U+00A0 that renders as a paragraph is never part of a run.
5. blank-runs-Q5: **Folded sections.** A run whose preceding block is folded shows nothing.
6. blank-runs-Q6: **Selection.** A block selection never starts or ends on a blank-lines block; copy or
   cut of one alone does nothing.
7. blank-runs-Q7: **Line endings** kept (BLOCK-234).
8. Spec critic: yes, on Fable (owner's rule): it changes what the writer sees and does in edit mode.

Spec critic (Fable), 2026-11-21 ~00:40: 9 points, 5 fixes, 4 questions decided by the Chief of Staff
under the owner's autonomy rule:
9. blank-runs-Q9: **`isBlank` scope** (narrows Q4). This CR adds one exported CommonMark blank test
   (spaces and tabs only) in `blockRange.ts`, used by `blankRuns` and the run checks only; existing
   callers keep `trim()` until backlog `blank-line-check-unicode-spaces` moves them to it (that item
   now names this function). Not a restated regex: one function, two callers groups for one night.
10. blank-runs-Q10: **Keys on a focused block.** As empty-block-Q10: Delete and Backspace act only on a
    selected blank-lines block (arrows); a focused one (Tab) takes Enter and its Delete block button.
11. blank-runs-Q11: **Runs inside lists and containers** stay out of scope (named in Out of scope and in
    the first SwRS); an inbox item is filed for runs between list items.
12. blank-runs-Q12: **Ctrl/Cmd+V on a selected blank-lines block** pastes in place of the run, like typing
    in it (one separator on each side).
