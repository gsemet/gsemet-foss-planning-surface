# Answers

Short name: `perf547b`

This CR comes from `perf-547-slow-comment-selection`, split on the owner's word. The owner's answers
below were given there (its items 1, 3 and 5), on 2026-11-26.

1. perf547-Q1, the owner's free answer, verbatim: "Il y a des recommendations de fix dans le ticket
   tu les as pris en compte? Dès que possible tu fix dans le batch en cours et tu fais une analyse de
   perf en fenêtre réelle (relance 2 ou 3 fois pour avoir un peu de stabilité). Tu vas en profiter de
   ce fix pour rajouter la campagnes de PKI demander"

2. perf547-Q3, "does the fix go as one CR or two?", answer, verbatim: "A. Deux CR (reco.)" (two CRs:
   1) measure, `:has()` rules, comment button; 2) changed threads only and the Git author name,
   stacked above, in batch-09).

3. perf547-Q5, "where is the wait for the Git author name measured?", answer, verbatim: "A. En CI
   (reco.)" (a test folder as a Git repository with a user name; the report says so).

4. The owner's instruction (2026-11-26), verbatim: "Durant le dev, si le codeur est bloqué ou a du mal
   avec le mode commentaire (pas les commentaires HTML, les commentaires en thread), dis le moi. Je
   pense que ça peut être une raison pour une charge inutile, surtout que les gros doucement (ça doit
   calculer un index). Si c'est le cas on désactivera la feature commentaire en thread et on fera une CR
   pour mettre le fil de commentaire dans le fichier au lieu du json à côté"

5. perf547b-Q1 (2026-11-26), "do you want the indexing time of the comment threads measured on its own
   in this CR, on the ticket's document and on one four times as large?", choices "A. yes, measure it
   (recommended)", "B. not now: only report if the coder struggles with it". Answer, verbatim: "A".

Destination: running batch batch-09.

Spec critic: no (the two points were in the specification the critic checked before the split; the
split changes no behaviour of them).

6. The owner's instruction for the night (2026-11-27, Chief of Staff session), verbatim: "ok je te
   laisse finaliser la nuit. mode stack. plus de question, je suis off. tu peux faire jusqu a 6 retry
   part tache. fini par une pipeline long uniquement sur le dernier commit."

   Applied by the Chief of Staff: round limit 6; no question to the owner; one heavy CI run only, at
   the last commit of the final stack, which covers this CR's "a heavy CI run of the head is green"
   (no heavy run at this CR's own head). Targeted measure dispatches stay.

7. livraison-Q1 (2026-11-27, Chief of Staff session), question: "le correctif de performance (CR-516
   terminée, CR-517 en vérification finale) peut partir sans attendre la campagne de KPI et sa page
   (CR-518, CR-519, pas commencées). La CI lourde dure environ 20 min. Je le livre maintenant ?",
   choices "A. Livrer maintenant (reco.)" (once CR-517 is verified: a heavy CI on its head, then the
   owner merges PR 549 and PR 550; CR-518 and CR-519 follow with a second heavy CI), "B. Une seule CI
   à la fin". Answer, verbatim: "A. Livrer maintenant (reco.)".

   Applied by the Chief of Staff: replaces, for CR-516 and this CR, the single heavy run of item 6. One
   heavy CI at this CR's final head once verified (it covers CR-516, under it); then both PRs leave
   draft for the owner to merge, in order. CR-518 and CR-519 keep their one heavy run at CR-519's head.
