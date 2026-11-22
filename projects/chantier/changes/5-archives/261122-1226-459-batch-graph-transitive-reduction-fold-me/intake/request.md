# Batch graph: transitive reduction, fold merged CRs, fewer crossings

The user (2026-11-22), looking at batch-30's Graph tab (31 CRs, CR-447 waiting for 30): the
batch view's dependency graph is hard to read on a typical DAG. Seen on the board (an older build
than main; CR-441's one-arrowhead-per-CR was not in it):
1. CR-447's 30 declared waits draw 30 long edges across the whole graph; most are implied by a
   chain (CR-447 → CR-458 → CR-457 → CR-456): draw the transitive reduction only.
2. The 26 merged CRs take most of the columns; the dozen in flight matter: fold the merged ones.
3. Cards within a level are not ordered to reduce crossings.
4. With the "PR à revoir" side panel, only two and a half levels fit and the graph scrolls
   sideways, while a large empty area sits below (the canvas is much taller than its content).
The user: "Oui met la dans le batch en cours" (batch-30, before CR-447).