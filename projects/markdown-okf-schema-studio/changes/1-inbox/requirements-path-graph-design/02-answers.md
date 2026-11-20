Short name: `path-graph`

- Owner, 2026-11-20, on the first proposal (one straight row per path, shared states drawn grey
  with "↑ path 1"): "je suis pas fan des nouveau graphe. dans l'idee c'etait que quand les noeuds
  sont les meme entre 2 path ils sont joins". A state shared by two paths is ONE node: the paths
  join at it and split from it (like lines of a metro map), never a copy per row.
- Owner, 2026-11-20: "juste j'aimerais que le 'path' soit un peu mieux defini sans faire un pate
  de text non plus. l'idee c'est une personne non specialiste comprend que plusieurs swrs au sein
  d'un strs et que plusieurs peuvent partager des transitions commun." The graph explains itself
  to a non-specialist in a few words (legend or one short line, no paragraph): a use case (StRS)
  is reached by one or more paths; each step is a behaviour (SwRS) with its tests; paths can
  share steps.

Decided by the Chief of Staff under the owner's autonomy rule (2026-11-20): the CR ships the proven
design of `work/design.md` and `graph-design.patch` (joined nodes, smaller graph, the one-paragraph
explanation of "path"). Links in the graph and its caption use full IDs, as the viewer-ids CR asks;
if that CR lands first this one follows it, else the viewer-ids CR changes them.
Spec critic: yes, on Fable (owner's rule): it changes what readers of the published site see.
