# The cost figures are right, shown as computed, and explained

The user, after a batch-06 report showing $41 of orchestration and $4 of coding: "Tu vas faire 1
nouvelle CR qui s'assure que le calcul et l'affichage soit juste. A la fin du batch (ou quand
l'utilisateur demande), il faut expliquer les chiffres qu'ils voient. Pas de sous agent évidement
dans ce cas il faut que tout soit nickel." And before: "il faudra isolé le coût du foreman du coût
des drivers de CR et du driver de release ou QA ou driver autre, potentiellement apporté par un
user."

Found by a critical review of batch-06, recomputed from the raw transcripts:

- The pricing is right: $49.285 over 1232 calls, to the cent. No call is misfiled.
- `chief-of-staff.md`, Cost: the groups are made by hand from `cost --by role`. The Chief of Staff
  drifted from the card: $41.47 of orchestration instead of $19.07, $22.39 in the wrong group.
- The card's own groups mislead: 84% of its "implementation" is Drivers.
- `commands.py`, `_cost_summary`: a Driver is "an agent that started one", so 7 Drivers with no
  worker count as workers ($3.42), and a QA or release driver, which has no Agent tool, always does.
- `_cost_summary` prints every root agent as "Driver", worker calls included, next to a "Drivers"
  figure that has none.
- A Driver is an agent with no parent: the record already says so, with no role name.
- Explaining the figures took a subagent of 136k tokens and 43 tool calls.
