# Grill answers

Short name: `copy-edges`. These answers come from the grill of `copy-selection-raw-markdown` (short name `copy-raw`), split off on copy-raw-Q17; they are repeated here with their origin ids.

1. copy-edges-Q1 (= copy-raw-Q1, 2026-11-24): **Precision.** Character-precise, adding the opening or closing characters of containers (admonitions, tables) when the selection starts or ends inside one.
2. copy-edges-Q2 (= copy-raw-Q2): **A cut inside inline formatting.** Cut exactly at the point but add the closing markers: selecting from "wo" in `**world**` gives `**rld**` style balancing (the cut text wrapped in its markers).
3. copy-edges-Q3 (= copy-raw-Q6): **A table cut at an edge.** A. The rows touched, whole, preceded by the header row and the delimiter row.
4. copy-edges-Q4 (= copy-raw-Q7 and copy-raw-Q16): **A nested list cut at the start.** Keep the item's marker and bring the list to level 0; every item is shifted by the indentation of the shallowest item selected, so relative depths are kept (Q16 B, against the recommendation).
5. copy-edges-Q5 (= copy-raw-Q11): **A heading cut at the start.** A. Keep the heading marker: `## llo`.
6. copy-edges-Q6 (= copy-raw-Q13): **An edge the alignment cannot place.** A. Snap that edge to the whole source element.
7. copy-edges-Q7 (= copy-raw-Q9): **Requirements and edge tests.** The owner's words: "Il faut bien capturer les requirements et faire les tests au limites, exemple nested admonition avec liste etc." okfreq SwRS per balancing rule, and tests at the edges: an admonition in an admonition, a list inside an admonition, an admonition inside a list item, a selection starting or ending at each nesting level, code fences inside containers, tables inside admonitions, a cut inside nested inline markers (bold inside a link), a selection across several containers.
8. copy-edges-Q8 (= copy-raw-Q17, 2026-11-24): **Grilled enough?** Specify, for the running batch batch-09, stacked on copy-selection-raw-markdown. Spec critic: yes (what the owner gets in the clipboard, several constructs at once; the base CR's critic already ran on the joint spec, so this run checks the split's seams).

9. copy-edges-Q9 (2026-11-24, spec open question 1): **List shift and indented code.** A. The first copied item's marker line is capped at 3 columns so it stays a list item; the other lines follow Q4 (shift by the shallowest item).
10. copy-edges-Q10 (2026-11-24, spec open question 2): **A setext heading cut at the end.** A. Add its underline line so it stays a heading.
11. copy-edges-Q11 (2026-11-24, spec open question 3): **A selection entirely inside one code block.** A. The code text alone, no fence lines (the common case is copying a snippet to use it). A selection that leaves the code block still gets the fences per Q1.

12. copy-edges-Q12 (2026-11-24, the owner on their own after Q11): **Balancing only at a broken edge, and opt-in.** The owner's words: "Mais c'est pareil pour une sélection entièrement dans un admonition: on recopie pas l'admonition. C'est que quand on casse le bordure et que le résultat risque d'être inconsistant que l'on rajoute les delimiteurs manquants. Met une option opt-in pour ça et pense à faire une req et des tests claire sur ces cas. C'est je pense une feature qui sera très appréciable". So:
    - A selection entirely inside a container (admonition, directive, code block, table cell, list item, inline span) copies its content only, never the container's delimiters (generalises Q11).
    - Missing delimiters (closing inline markers, container fences, table header and delimiter rows, heading marker or setext underline, list level) are added only when the selection crosses a construct's boundary, so that the cut text would otherwise be inconsistent Markdown.
    - Adding them is opt-in: a new setting, off by default. Off, the copy is the verbatim cut of the base CR (CR-480). The setting goes through the project's settings registry and documentation.
    - Requirements: an SwRS for the setting (off and on), one per balancing rule with "inside only → no delimiters" and "boundary crossed → delimiters added" as explicit rows; tests cover each case with the setting off and on, nested edges included (Q7).
13. Chief of Staff routine (2026-11-24, on Q12): snapping an edge the alignment cannot place (Q6) is placement, not a delimiter: it applies with the setting off or on.

Destination: running batch batch-09.
