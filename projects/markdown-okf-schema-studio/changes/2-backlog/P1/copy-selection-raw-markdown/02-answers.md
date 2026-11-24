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

11. copy-raw-Q11 (2026-11-24, spec open question 1): **A heading cut at the start.** A. Keep the heading marker: `## llo`, like the other open containers.
12. copy-raw-Q12 (2026-11-24, spec open question 2): **A selection entirely in UI chrome.** A. Native copy, as today.
13. copy-raw-Q13 (2026-11-24, spec open question 3): **An edge the alignment cannot place.** A. Snap that edge to the whole source element.
14. copy-raw-Q14 (2026-11-24, spec critic F1): **Ctrl+A then copy.** A. The whole source exactly: trailing definitions, comments and the final newline included.
15. copy-raw-Q15 (2026-11-24, spec critic F2): **Side by side, a selection touching an old-side card.** A. The current source only: the old card's text is skipped; native copy when an edge lies in an old card.
16. copy-raw-Q16 (2026-11-24, spec critic F3): **Later list items shallower than the starting item.** B (against the recommendation). Shift every item by the indentation of the shallowest item selected, so relative depths are kept.
17. copy-raw-Q17 (2026-11-24, spec critic F8, bundle): **Split.** A. Two stacked CRs, both in the running batch batch-09: (1) this CR, verbatim raw copy (the `previewSourceText` protocol, the mapping, generated content, UI chrome, scope, clipboard formats); (2) a new CR, edge balancing (inline closing markers, container fences, table header and delimiter, list level and indentation, heading marker), stacked on this one. The edge part is filed as `copy-raw-edge-balancing`; the answers Q2, Q6, Q7, Q11, Q13, Q16 and the edge tests of Q9 go with it.
18. Chief of Staff routine (2026-11-24, spec critic F4-F7, no user question): F4 reword BLOCK-166 row 79 and StRS-MDOKFSTUDIO-BLOCK-016 line 59 to the block-copy handler only; F5 build the E2 frames from the real core renderer's output (tab items carry no source line: mystNode.ts:90-97, mystGridToctree.ts:491) or run the nesting grid in E3; F6 add a context-menu Copy step to E4 or drop the claim, and state text/html is proved in Chromium only; F7 the table of contents source is `{contents}` or the bracket marker (mystToc.ts:164-169), not `{toc}`.

Destination: running batch batch-09.
