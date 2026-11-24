Short name: `copy-raw`

# Answers

1. copy-raw-Q1 (2026-11-24): **Precision at the edges.** Character-precise, and the opening or closing characters of a container are added when the selection starts or ends inside it. The owner's words (free answer): "Au caractère prêt, et il faut éventuellement rajouter les caractères de clôture ou d'ouverture (admonition, tables…) si on commence ou fini au milieu".
2. copy-raw-Q2 (2026-11-24): **An inline element cut at an edge.** Cut exactly at the point, but add the closing (or opening) characters so the Markdown stays balanced. The owner's words (free answer): "Couper exactement au point mais rajouter les caractère de clôture". Example: a selection starting at "r" of `**world**` copies `**rld**`.
3. copy-raw-Q3 (2026-11-24): **Clipboard formats.** A. text/plain carries the raw Markdown, text/html the rendered HTML.
4. copy-raw-Q4 (2026-11-24): **Where.** A. Everywhere in the page, read and edit mode, except inside a text input or field being edited, which keeps the native copy.
5. copy-raw-Q5 (2026-11-24): **Generated content and UI.** A. Copy the source that produces it (a rendered Mermaid diagram gives its fence, a generated table of contents its directive, the frontmatter properties table its YAML); UI chrome (comment bubbles, buttons, line numbers, toolbars) is never copied.
6. copy-raw-Q6 (2026-11-24): **A table cut at an edge.** A. The rows touched, whole, preceded by the header row and the delimiter row.
7. copy-raw-Q7 (2026-11-24): **A nested list cut at the start.** A. Keep the item's marker and bring the first item to level 0; the next items keep their relative indentation.
8. copy-raw-Q8 (2026-11-24): **Grilled enough?** D. Not yet: a point is left to grill.
9. copy-raw-Q9 (2026-11-24, the point left after Q8): **Requirements and edge tests.** The owner's words: "Il faut bien capturer les requirements et faire les tests au limites, exemple nested admonition avec liste etc." The CR captures the behaviour in okfreq requirements (a StRS use case and SwRS per rule: character-precise cut, inline balancing, container fences, table header, list level, generated content, UI skipped, clipboard formats, scope), and its tests cover the edges: nested containers (an admonition in an admonition, a list inside an admonition, an admonition inside a list item), a selection starting or ending in each nesting level, code fences inside containers, tables inside admonitions, a cut inside nested inline markers (bold inside a link), a selection across several containers, and a whole-document selection that round-trips to the source.
10. copy-raw-Q10 (2026-11-24): **Grilled enough?** B. Specify, for the running batch batch-09. The owner's words: "Si tu as bien prévu de bien tester c'est bon tu peux lancer en spec dans le batch en cours". Spec critic: yes.

Destination: running batch batch-09.
