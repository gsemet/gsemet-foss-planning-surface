# Answers

## The user's word (2026-11-22)

The user, looking at batch-30's Graph tab, asked for four fixes to the web board's batch Graph tab
(`intake/request.md`), and said "Oui met la dans le batch en cours" ("Yes, put it in the running
batch") to these four points as listed:

1. Draw only the transitive reduction of the waits: a wait implied by a chain of other waits is not
   drawn, and the hidden waits stay discoverable (for instance on hover or in the card).
2. Fold the merged (done) CRs: a chip "N merged" that expands.
3. Order the cards within a level to reduce crossings (a simple barycentre pass).
4. Fit: the graph uses the width (no sideways scroll for a normal batch at desktop width, the side
   panel considered), and its canvas height follows its content.

Placement: batch-30 (running), before CR-447 docs-gardening; one Driver, within 3 rounds, today.

There was no further grill. The Spec-writer settles the detail and lists the behaviour questions it
left open at the end of `03-change-spec.md`, each with the option it built.

## Chief of Staff's decisions on the writer's open points (2026-11-22)

Option A on all six, as the spec builds, to keep the CR within 3 rounds today (the user may
change any of them): the fold resets at each page load; cancelled CRs fold with the merged ones;
icon-only state badge below 240px; desktop target 1600×900; hidden waits shown by the hover
highlight and the count's tooltip; the Gantt keeps every declared wait.
