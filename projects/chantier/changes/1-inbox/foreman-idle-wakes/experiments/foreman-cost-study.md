# Coût du Foreman : étude des sessions du 11 au 21 novembre 2026

Étude en lecture seule, faite le 2026-11-21 par un sous-agent Fable, pour la question foreman-idle-Q4.

## Verdict

- **Couper les réveils à vide ne suffit pas.** Ils pèsent 17 % du coût du Foreman (19 % en batch-29). Les supprimer tous fait passer sa part de 25 % à 21 % (batch-29) et de 36 % à 33 % (batch-28). Le doute de l'utilisateur est fondé.
- **Le coût n'est pas pour autant inhérent.** Environ un tiers l'est (les événements à traiter). Le reste vient de la façon dont chaque événement est traité : 4 appels par réveil, chacun relisant 180 000 tokens, sur Opus.
- **Le premier levier est le modèle.** Les batches 23 à 27 avaient un Foreman Sonnet, les batches 28 et 29 un Foreman Opus, deux fois plus cher par token. Avec Sonnet, sans rien changer d'autre, batch-29 serait à 14 % et batch-28 à 22 %.
- **Cible proposée :** moins de 15 % pour un batch d'au moins 15 CRs avec un Foreman Sonnet ; moins de 20 % avec Opus, tous les autres leviers appliqués. Pour un petit batch de CRs peu chers, aucune cible en part ne tient : mesurer plutôt en dollars par CR (0,50 $ sur Sonnet, 1,00 $ sur Opus).

## 1. Par batch

Coût du Foreman = son propre transcript, re-tarifé avec la table de prix du CLI. Il recoupe le reçu des batches 17, 18, 28 et 29 à 1,5 % près.

| Batch | Modèle | CRs | Batch $ | Foreman $ | Part | Réveils | Appels | Contexte moyen | Réveils à vide | Part sans eux | Part si Sonnet |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 11 | Sonnet | ? | ? | 6,08 | ? | 65 | 200 | 163k | 29 (1,36 $) | | |
| 12 | Sonnet | ? | ? | 1,50 | ? | 12 | 42 | 143k | 5 (0,28 $) | | |
| 15 | Opus | ? | ? | 16,74 | ? | 90 | 293 | 180k | 43 (3,61 $) | | |
| 16 | Opus | ? | ? | 7,93 | ? | 36 | 131 | 198k | 17 (1,64 $) | | |
| 17 | Opus | 32 | 229,22 | 49,79 | 22 % | 312 | 893 | 190k | 118 (10,4 $) | 18 % | 12 % |
| 18 | Opus | 42 | 183,92 | 41,37 | 22 % | 225 | 729 | 167k | 93 (7,1 $) | 19 % | 13 % |
| 23 | Sonnet | 16 | 63,94 | 6,51 | 10 % | 75 | 225 | 176k | 27 (0,9 $) | 9 % | 10 % |
| 24 | Sonnet | 29 | 117,11 | 14,60 | 12 % | 168 | 455 | 178k | 65 (1,7 $) | 11 % | 12 % |
| 25 | Sonnet | 1 | 8,91 | 2,13 | 24 % | 12 | 60 | 189k | 3 (0,1 $) | 23 % | 24 % |
| 26 | Sonnet | 5 | 17,30 | 3,48 | 20 % | 28 | 102 | 213k | 10 (0,5 $) | 18 % | 20 % |
| 27 | Sonnet | 10 | 26,40 | 5,54 | 21 % | 51 | 182 | 173k | 13 (0,5 $) | 19 % | 21 % |
| 28 | Opus | 20 | 122,40 | 44,19 | 36 % | 157 | 642 | 184k | 53 (5,9 $) | 33 % | 22 % |
| 29 | Opus | 36 | 243,54 | 59,71 | 25 % | 291 | 983 | 185k | 114 (11,1 $) | 21 % | 14 % |

Batches 13, 14, 19 à 22 : mode direct, pas de Foreman. Batches 11 à 16 : aucun coût total archivé.

Le « 48 % » de batch-27 est un effet de comptage : le transcript du Foreman coûte 5,54 $ (21 %). La ligne « Foreman » du reçu (12,67 $, 412 appels) compte aussi des agents qu'il a lancés et qui ne sont pas des CR Drivers (3 release-drivers Opus, 4,28 $ ; 3 retro-critics, 0,91 $).

### Par type de réveil (13 batches, 1 522 réveils, 259,58 $)

| Type de réveil | Réveils | $ | Part | $/réveil | Appels/réveil | Batch-29 : réveils, $ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Heartbeat (`/loop`), rien de neuf | 178 | 24,50 | 9,4 % | 0,14 | 2,9 | 36 ; 6,25 |
| Heartbeat suivi d'une action | 14 | 4,72 | 1,8 % | 0,34 | 5,5 | 5 ; 1,50 |
| Avis de l'hôte « Driver waiting on its own background work », sans action | 283 | 13,54 | 5,2 % | 0,05 | 1,2 | 52 ; 2,95 |
| Même avis, suivi d'une action | 6 | 0,99 | 0,4 % | 0,16 | 3,3 | 0 |
| Message d'un Driver en cours (note de progrès), sans action | 66 | 3,59 | 1,4 % | 0,05 | 1,2 | 18 ; 1,42 |
| Message d'un Driver en cours, suivi d'une action | 68 | 10,12 | 3,9 % | 0,15 | 3,0 | 12 ; 1,90 |
| Fin d'un Driver avec ligne `hand-back` (ready, blocked, draft) | 315 | 66,41 | 25,6 % | 0,21 | 4,0 | 55 ; 15,54 |
| Autre fin de Driver, suivie d'une action (relais de clôture, rapport du stack driver) | 137 | 34,40 | 13,3 % | 0,25 | 4,3 | 49 ; 12,63 |
| Fin de Driver sans action | 22 | 1,03 | 0,4 % | 0,05 | 1,2 | 3 ; 0,19 |
| Ordre du Chief of Staff (`order O-n`) | 229 | 44,27 | 17,1 % | 0,19 | 4,1 | 31 ; 8,62 |
| Message du Chief of Staff, suivi d'une action | 108 | 28,65 | 11,0 % | 0,27 | 4,8 | 18 ; 4,48 |
| Message du Chief of Staff, sans action | 41 | 2,38 | 0,9 % | 0,06 | 1,4 | 5 ; 0,24 |
| Reprise après compaction | 27 | 12,99 | 5,0 % | 0,48 | 4,8 | 5 ; 3,13 |
| Démarrage de la session | 10 | 10,28 | 4,0 % | 1,03 | 13,7 | 1 ; 0,55 |
| Autre (fin d'agent, tâche de fond, hôte) | 18 | 1,74 | 0,7 % | 0,10 | 2,5 | 1 ; 0,29 |
| Événement du watcher | 0 | 0 | 0 % | | | 0 |

Le watcher ne réveille jamais le Foreman : il réveille le Chief of Staff, qui relaie par un message ou un ordre.

**Classement.** Un réveil est un enregistrement `user` qui n'est pas un résultat d'outil (la règle du CLI). Son type vient de son texte : `<command-name>/loop` (heartbeat), `<agent-message>` avec ou sans `[Subagent hand-back]` (Driver), `<cross-session-message>` du Chief of Staff avec ou sans `order O-n`, `<task-notification>`. Plusieurs messages arrivés avant le même appel font un seul réveil, classé par priorité (ordre, fin de Driver, message, avis, heartbeat). « Sans action » ou « à vide » : le tour n'a lancé aucun agent, envoyé aucun message, arrêté aucune tâche, ni lancé de commande chantier qui écrit (`take`, `agents set`, `order done`, `note`, `gate`...).

## 2. Où va le coût d'un tour

| Poste | Part (13 batches) | Batch-29 |
| --- | ---: | ---: |
| Lecture du cache : le contexte relu à chaque appel | 59 % | 35,21 $ |
| Écriture du cache (tarif 1 h) : ce qui entre dans le contexte | 25 % | 13,83 $ |
| Sortie : raisonnement, briefs, relais | 16 % | 10,66 $ |
| Entrée hors cache | 0 % | 0,01 $ |

- **La lecture du cache est le produit contexte × appels, pas contexte × réveils.** Un réveil utile fait 4 appels en moyenne (983 appels pour 291 réveils en batch-29). Chaque appel coûte 0,036 $ sur Opus à 180k tokens, avant tout travail.
- **Le contexte a un plancher élevé.** La session démarre à 75k tokens avant toute lecture de carte : le prompt de l'hôte et ses 59 outils (124 000 caractères de définitions). Elle remonte à 95k-105k après chaque compaction et monte jusqu'à 265k. La moyenne de 180k est le milieu de cette dent de scie. Environ 40 % des lectures de cache paient donc le prompt et les outils de l'hôte.
- **Ce qui entre dans le contexte** (en caractères) : les sorties du Foreman lui-même 32 %, les messages de réveil 30 %, les cartes 11 %, les sorties des commandes chantier 12 % (dont `status` 4 %), le reste du shell 6 %, les retours d'agents 3 %.
- **Les relectures de `status` ne comptent presque pas en contenu** (41 000 tokens sur 1,73 million en batch-29, 3 appels à `cost` en tout). Leur coût est l'appel lui-même : 88 appels à `status`, environ 3,2 $ (5 %).
- **Chaque heartbeat injecte le texte de la commande `/loop`**, environ 9 000 caractères : 325 000 caractères en batch-29, la première source de messages de réveil. Il avance donc aussi les compactions.

## 3. Inhérent, évitable, leviers

**Inhérent.** Un CR produit 3 à 6 événements à traiter (prise et démarrage, relais de clôture, hand-back, ordre de merge) : 4,8 par CR en batch-29. Traité au minimum (2 appels à 100k tokens, un message court), un événement coûte environ 0,10 $ sur Opus et 0,05 $ sur Sonnet. Pour batch-29 : environ 20 $ sur Opus, soit un tiers des 59,71 $ et 10 % du batch.

**Évitable.** Les réveils à vide (17 à 19 %), et surtout le surcoût de chaque événement utile : 4 appels au lieu de 2, un contexte de 180k au lieu de 100k à 130k, et le modèle.

Estimation sur batch-29 (59,71 $, 25 %) et batch-28 (44,19 $, 36 %), leviers cumulés dans l'ordre :

| Levier | Gain sur le Foreman | Batch-29 | Batch-28 |
| --- | ---: | ---: | ---: |
| Aujourd'hui | | 25 % | 36 % |
| A. Plus aucun réveil à vide (borne haute : un heartbeat de 20 minutes en garde une partie, et l'avis « Driver waiting » vient de l'hôte) | 13 à 19 % | 21 % | 33 % |
| B. Moins d'appels par événement : une commande CLI par événement au lieu de 3 ou 4, pas d'appel séparé pour `ScheduleWakeup`, `wrap_up`, `update_plan` (119 usages de ces trois outils en batch-29) | environ 13 % | 18 % | 30 % |
| C. Contexte plus petit : compaction ou Foreman neuf vers 170k, hand-backs plus courts (net du coût des compactions en plus, 0,5 à 1,4 $ chacune) | environ 5 % | 17 % | 28 % |
| D. Foreman sur Sonnet (prix divisés par deux) | 50 % | 9 % | 16 % |
| D seul, sans A, B ni C | 50 % | 14 % | 22 % |

Les gains de B et C sont des estimations, non mesurées. A et D sont calculés sur les transcripts.

## 4. Réponse à la cible « moins de 15 % »

- **Par les réveils à vide seuls : non.** Gain de 3 à 4 points.
- **Avec un Foreman Opus : non, même avec A, B et C** (17 à 18 % sur un grand batch, 28 % sur un batch comme le 28).
- **Avec un Foreman Sonnet : oui pour un grand batch.** C'est déjà mesuré : 10 % et 12 % aux batches 23 et 24, sans aucun des autres leviers. La qualité du pilotage sur Sonnet reste à juger : le rétro de batch-24 note un `take stack` manqué.
- **Pour un petit batch de CRs peu chers : non, quel que soit le levier.** Les batches 25 à 27 sont à 20-24 % sur Sonnet : le démarrage coûte 0,4 à 0,9 $ et un CR n'y coûte que 1,4 à 2,7 $.

Mesure plus stable que la part : le coût du Foreman par CR. Sonnet : 0,41 à 0,55 $ (batches 23, 24, 27). Opus : 0,99 à 2,21 $ (batches 17, 18, 28, 29).

## Méthode et limites

- Dix transcripts de Foreman (sessions 4215b12b, bf484d59, bd1945f6, 446cff2e, 1b6c0af3, cc65c0a9, 993a179a, 62abbcd1, 872ef130, bc951dfe), lus par script, un appel par identifiant de message, prix de `costs/transcripts.py`. Une session qui couvre deux batches est coupée à l'ouverture du second.
- `chantier cost --batch` refuse un batch clos (« unknown batch ») : les totaux viennent des `batch-NN.json` archivés.
- « Sans action » est une règle sur les outils appelés : un tour qui lit, juge et décide à raison de ne rien faire compte comme à vide. La part à vide est donc une borne haute.
- Un réveil qui porte plusieurs messages est compté une fois, sous le type de plus haute priorité.
- L'appel de compaction lui-même ne laisse pas de trace dans le transcript : il n'est pas compté (35 compactions).
- Non mesuré : l'effet de Sonnet sur la qualité du pilotage ; le gain réel de B et C ; le détail des 75k tokens de départ au-delà du prompt et des outils ; le coût du Chief of Staff qui pilote le batch (38,57 $ hors budget en batch-29), qui fait aussi partie de l'orchestration.
- La « part si Sonnet » divise le coût du Foreman par deux, les prix Sonnet étant la moitié des prix Opus pour chaque poste. Elle suppose le même nombre d'appels.
- Les scripts (`parse.py`, `report.py`, `subs.py`) sont dans le dossier temporaire de la session et ne sont pas gardés.
