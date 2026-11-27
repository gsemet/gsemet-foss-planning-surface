# Answers

Short name: `perf-kpi-pages`

This CR comes from `perf-kpi-real-window-tests`. The owner's answers below were given there, on
2026-11-26.

1. perf-kpi-Q5, "what form does the shown score take?", answer, verbatim: "A. ms et ratio (reco.)"
   (median time and the ratio measured / maximum: 1 or less means met).

2. perf-kpi-Q8, "is the scores page on GitHub Pages a CR of its own, above the KPI job, in
   batch-09?", answer, verbatim: "A. Deux CR (reco.)".

The text before the earlier questions said, with no objection: unless told otherwise, the Pages site
shows the latest run only, with no history.

Destination: running batch batch-09.

Spec critic: no (the page was in the specification the critic checked before the split).

3. The owner's instruction for the night (2026-11-27, Chief of Staff session), verbatim: "ok je te
   laisse finaliser la nuit. mode stack. plus de question, je suis off. tu peux faire jusqu a 6 retry
   part tache. fini par une pipeline long uniquement sur le dernier commit."

   Applied by the Chief of Staff: round limit 6; no question to the owner; one heavy CI run only, at
   the last commit of the final stack. This CR is the top: that run is this specification's "heavy run
   on the branch", and its run id goes in the PR's test plan.

4. livraison-Q1 (2026-11-27, Chief of Staff session), "deliver the performance fix (CR-516, CR-517)
   now, without waiting for CR-518 and CR-519?", answer, verbatim: "A. Livrer maintenant (reco.)".
   CR-516 and CR-517 get their own heavy CI and are merged first; item 3 stays for CR-518 and this CR:
   one heavy run at this CR's head, the second of the night's work.

5. fin-batch-Q1 (2026-11-27, Chief of Staff session), "how do I finish batch-09?", answer, verbatim:
   "Mais fini tout les 3 autres." Read by the Chief of Staff: CR-517, CR-518 and this CR stay in
   batch-09 and are finished; the rigor is unchanged.

6. local-Q1 (2026-11-27), "lighten the local tests for CR-518 and CR-519?", answer, verbatim: "Oui
   découpe la CI maintenant juste après celle que tu fini il faut pouvoir aller vite." Applied: no
   visual tests on the owner's PC (CI runs them), `just check` once per round and not re-run by the
   reviewer, targeted tests during the work (replaces "the rigor is unchanged" of item 5).

7. The owner's instruction (2026-11-27), verbatim: "Fait ce qu'il faut pour merger ce qui reste
   rapidement et on clos le batch vite. On fera les teste visuels lourd dans un second batch". Which
   CRs leave batch-09 is being confirmed (close-Q1).

8. close-Q1 (2026-11-27, Chief of Staff session), "do I take CR-518 and CR-519 out of batch-09?",
   choices "A. yes, to the next batch (recommended)", "B. no, finish them in batch-09". Answer,
   verbatim: "Les 2 dernière je ferais plus tard sur les tests de perf en pages, met en P1". Applied:
   this CR leaves batch-09 for the backlog P1.

Destination: backlog P1 (item 8; replaces the running batch).
