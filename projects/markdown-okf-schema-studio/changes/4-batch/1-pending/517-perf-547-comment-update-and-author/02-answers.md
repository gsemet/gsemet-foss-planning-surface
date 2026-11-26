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
