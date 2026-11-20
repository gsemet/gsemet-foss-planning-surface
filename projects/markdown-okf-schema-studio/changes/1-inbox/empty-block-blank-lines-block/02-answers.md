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
