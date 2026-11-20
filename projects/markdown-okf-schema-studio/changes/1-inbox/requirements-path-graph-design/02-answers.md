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

Spec critic (Fable), 2026-11-21 ~00:00: 7 points, 2 fixes, 5 questions decided by the Chief of Staff
under the owner's autonomy rule:
- path-graph-Q-c1: **Overlap check scope.** In CI on every real use case page with Main paths (the
  requirements report is generated in `ci-visual` first), plus the frozen shapes for unit-level cases.
- path-graph-Q-c2: **Fonts.** Pin the test fonts as the breakout tests do (`test/page/pinnedFont.ts`) and
  assert on every platform; the layout keeps a width margin for unpinned reader fonts.
- path-graph-Q-c3: **Three paths.** The requirements guideline changes to "one to three paths per StRS";
  the three-path design stays (the owner reviewed BLOCK-014's map).
- path-graph-Q-c4: **IDs in the graph.** The owner, 2026-11-20, on the caption "Step 1 of path 2 in
  BLOCK-014": "utilise StRS-MDOKFSTUDIO-BLOCK-014 a la place pour les liens partout". So every link
  shows the full ID: the caption, the tooltips and the pills. Pills put the full ID on its own line
  (test count on the next) and the layout is widened as needed; the overlap and size checks run again
  on the real maps.
- path-graph-Q-c5: **Explanation length.** Keep the three sentences (the owner saw this wording on
  2026-11-20 and asked nothing shorter); the legend stays.
