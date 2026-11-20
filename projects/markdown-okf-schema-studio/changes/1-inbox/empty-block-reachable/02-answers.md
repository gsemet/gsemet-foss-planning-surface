Short name: `empty-block`

1. empty-block-Q1: **Solution chosen by the owner (2026-11-20).** "pour le bloc vide, en mode
   edition il faudrait que les ligne vide au dela que 1 (qui sert de delimiter en md) soit
   representé par un petit block vide, selectable par le clavier et clicable. et il faut rajouter
   un bouton a gauche Supprimer le block."
   - In edit mode, blank lines beyond the one that separates two blocks are shown as a small
     empty block, reachable from the keyboard and clickable (it can be selected, edited, deleted).
   - A "Delete block" button is added on the left of a block (for every block, empty or not).
   - This replaces the investigation's option 2 (collapse-only action) and the CoS's option 1
     (auto-delete on Done) as the owner's direction; whether an emptied block on Done is also
     deleted stays open for the grill.

Decided by the Chief of Staff under the owner's autonomy rule (2026-11-20, "tu es maintenant autonome.
plus de question. tu grilles tout seul avec un fable"):

2. empty-block-Q2: **Done on an empty block.** A new block left empty on Done writes nothing (no extra
   blank lines); an existing block emptied on Done is deleted with its separator, so one blank line
   stays between its neighbours. The empty gap block then only shows blank lines that were already in
   the file (the file's format is kept: Studio never removes them by itself).
3. empty-block-Q3: **What the gap block is.** One gap block per run of two or more blank lines between
   two blocks (and at the end of the body). It is small (about one line high), shown only in edit mode,
   takes the keyboard selection like a block (arrows, Enter opens an editor on those lines to type text,
   Delete or the button removes the extra blank lines, keeping one separator). Reading mode is unchanged.
4. empty-block-Q4: **"Delete block" button.** On the left of every body block in edit mode, beside the
   existing handles, with the label "Delete block" (tooltip) and the same keyboard action as Delete on a
   selected block. One source edit, undoable with VS Code's undo. Included blocks and the properties
   table get no button (same refusals as move, BLOCK-127).
5. empty-block-Q5: **Line endings.** Every edit keeps the file's line endings (BLOCK-234).
6. Spec critic: yes, on Fable (owner's rule): it changes what the writer sees and does in edit mode.

Spec critic (Fable), 2026-11-21 ~00:00: 12 points, 6 fixes, 6 questions decided by the Chief of Staff
under the owner's autonomy rule:
7. empty-block-Q7: **List followed by blank lines.** Delete drops the trailing blank lines of the span
   before planning, as a move does. Cut and copy stay as they are; a backlog item is filed for them.
8. empty-block-Q8: **Insertion after a list.** Fixed here: an insertion anchored on a blank line writes
   one separator (BLOCK-094).
9. empty-block-Q9: **Which emptied editors delete on Done.** Top-level blocks and list items; trailing
   blank lines of the range are dropped before planning; blocks inside an item or a container keep
   today's behaviour.
10. empty-block-Q10: **Keys.** Delete and Backspace, only on an explicit block selection or a selected
    blank-lines block (never on a merely focused block or a focused control).
11. empty-block-Q11: **Selection one level down** (cell, list item, inner block): Delete does nothing.
12. empty-block-Q12: **Split in two.** This CR keeps A (Done on an empty block, the insertion fix) and C
    (the Delete block button and keys). B (the blank-lines block in edit mode) is split off as
    `1-inbox/empty-block-blank-lines-block`, built on this CR's button; it follows this CR in the stack.
