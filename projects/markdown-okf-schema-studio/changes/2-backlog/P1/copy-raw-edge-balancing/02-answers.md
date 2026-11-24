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

Destination: running batch batch-09.
