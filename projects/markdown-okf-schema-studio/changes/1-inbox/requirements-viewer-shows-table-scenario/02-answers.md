Short name: `table-scen`

Decided by the Chief of Staff under the owner's autonomy rule (2026-11-20, "tu es maintenant autonome.
plus de question. tu grilles tout seul avec un fable").

1. table-scen-Q1: **Show the table, do not convert it.** The card shows the source table as a table
   with its own headers (Input | Outcome, or whatever headers the source uses). Converting rows to
   GIVEN/WHEN/THEN would invent wording.
2. table-scen-Q2: **Mixed scenarios.** A scenario with list steps and a table shows the steps first,
   then the table, in source order. Other prose under a scenario heading (a note line) is shown as a
   paragraph, not dropped.
3. table-scen-Q3: **Requirements files are not rewritten.** Only the viewer changes; no SwRS text moves.
4. table-scen-Q4: **Guard.** A test over the real bundle checks that no rendered scenario card is empty.
5. Spec critic: yes, on Fable (owner's rule): it changes what readers of the published site see.

Spec critic (Fable), 2026-11-20 23:5x: 5 points, 3 fixes, 2 questions decided by the Chief of Staff
under the owner's autonomy rule:
6. table-scen-Q6: **`<br>` in a cell.** Nothing special: every cell is escaped text; the `<br>` rule and
   the `x<br>y` fixture cell are dropped (the only `<br>` in the bundle is an element name in code, CORE-071).
7. table-scen-Q7: **HTML entities.** Decode the basic entities (`&lt;`, `&gt;`, `&amp;`, `&quot;`) before
   escaping, in table cells, notes and steps, so the card shows what GitHub shows; the 7 step lines that
   use them change their display.
