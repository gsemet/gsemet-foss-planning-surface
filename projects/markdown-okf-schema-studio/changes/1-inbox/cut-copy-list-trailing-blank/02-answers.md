
## Grill, 2026-11-21

Decided by the Chief of Staff under the owner's autonomy rule (owner, 2026-11-20: "tu es maintenant autonome. plus de question. tu grilles tout seul avec un fable"; 2026-11-21: "Ensuite les autres P1 et inbox de Studio?").

- cc-Q1 Cut and copy drop the trailing blank lines of the block's range before planning, as Delete block and a move do; the copied text holds no trailing blank lines.
- cc-Q2 Same for any block whose range ends on blank lines (not only lists), if the code path is shared.
- cc-Q3 Cut leaves the blank lines as they are rules after the empty-block CR (CR-439): no extra blank lines; the document keeps one separator.
- cc-Q4 Evidence: unit tests on the plan, and the existing real-input cut/copy scenario extended to a list followed by two blank lines.
