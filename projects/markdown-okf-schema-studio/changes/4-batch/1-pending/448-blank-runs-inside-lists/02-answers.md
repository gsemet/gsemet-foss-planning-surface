
## Grill, 2026-11-21

Decided by the Chief of Staff under the owner's autonomy rule (owner, 2026-11-20: "tu es maintenant autonome. plus de question. tu grilles tout seul avec un fable"; 2026-11-21: "Ensuite les autres P1 et inbox de Studio?").

- br-Q1 Scope: a run of two or more blank lines between two items of the same list, and inside a list item. Quotes and admonitions are in scope only if the same mechanism serves them without a new one; otherwise the spec splits them into an inbox item.
- br-Q2 Same blank-lines block as CR-444 (look, keys, Delete keeps one blank line, Enter or click writes a block in its place), shown inside the list where the run is.
- br-Q3 Removing a run inside a list keeps the list one list (a single blank line between items stays a loose list as today); no change to the list's other text.
- br-Q4 Markdown keeps its original format (Studio's DNA): only the removed blank lines change in the file.

## Owner's answers, 2026-11-21

- br-Q1 confirmed by the owner: "Lists, then others if free" (quotes and admonitions only if the same mechanism covers them, otherwise a separate inbox item).
- br-Q5 (a block typed in place of a blank-lines block inside a list item). Owner, 2026-11-21: "Indent to the item": the host indents the typed lines to the item's content column, so "More" stays inside the item; a line typed at the item's own level ("- c") still adds an item.
- Quotes and admonitions split into 1-inbox/blank-runs-inside-quotes-admonitions (filed 2026-11-21).

## Owner's answers, 2026-11-21 (Fable spec critic's questions)

- br-Q6 (marker followed by a tab, or two markers on a line). Owner: "Compute as CommonMark": a tab runs to the next stop of 4; for `- - a` the innermost item's column; the block stays in the item; tests for both.
- br-Q7 (`- c` typed in a run inside an item, with more content of the item after). Owner: "Nested list in the item": written at the content indent, nothing after it changes item; a sibling item is added only from a run between items.
- Owner, 2026-11-21: "Ready + run with Foreman": moved to 3-ready and run in a stack with the existing Foreman.
