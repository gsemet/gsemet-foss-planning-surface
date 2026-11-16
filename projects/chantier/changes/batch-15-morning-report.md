# Batch-15 — rapport du matin (2026-11-13, ~03:45)

## Où on en est

15 CRs prêts, 1 mergé, la release CR-212 (v0.9.0) en attente. **Bloqué sur toi** : la remise en
pile des 15 PRs demande 14 force pushes, refusés au Foreman puis à moi par le mode auto.

**Ton action** (dans un terminal, depuis le checkout principal, qui reste sur `main`) :

```
powershell -File C:\Users\gaeta\AppData\Local\Temp\claude\f81ba1603abd10b3\91f1382a-eacd-437e-b5a8-f9e545753a8c\scratchpad\batch15-restack-push.ps1
```

Chaque push est protégé par un lease : il échoue si la branche a bougé. Ensuite, dis-moi « pushé »
(ou lesquels ont échoué) : je préviens le Foreman, et le Stack Driver recible chaque PR sur celle
du dessous, les livre et revérifie. Puis tu merges la pile ; la release CR-212 part ensuite (les
cartes en vigueur la lancent une fois les autres mergés).

## Avancement

| CR | Sujet | État | Tours | PR | Coût |
| --- | --- | --- | --- | --- | --- |
| CR-196 | release-cr-in-batch | prêt | 1/3 | [140](https://github.com/gsemet/chantier/pull/140) | $6.52 |
| CR-197 | driver-ci-from-pr-checks | prêt | 1/3 | [142](https://github.com/gsemet/chantier/pull/142) | $1.58 |
| CR-198 | stop-own-gate | prêt | 2/3 | [139](https://github.com/gsemet/chantier/pull/139) | $3.02 |
| CR-199 | — | **mergé** | 1/3 | [138](https://github.com/gsemet/chantier/pull/138) | $1.09 |
| CR-200 | cost-steering-vs-grill | prêt | 1/3 | [141](https://github.com/gsemet/chantier/pull/141) | $1.96 |
| CR-201 | boot-mode-by-surface | prêt | 1/3 | [144](https://github.com/gsemet/chantier/pull/144) | $2.16 |
| CR-202 | board-refresh-button | prêt | 1/3 | [143](https://github.com/gsemet/chantier/pull/143) | $1.33 |
| CR-203 | rebase-note-check-status | prêt | 1/3 | [145](https://github.com/gsemet/chantier/pull/145) | $0.96 |
| CR-204 | record-inspector-pass | prêt | 1/3 | [146](https://github.com/gsemet/chantier/pull/146) | $0.88 |
| CR-205 | rules-after-claim | prêt | 1/3 | [151](https://github.com/gsemet/chantier/pull/151) | $1.40 |
| CR-206 | ci-job-cold-cache-check | prêt | 2/3 | [148](https://github.com/gsemet/chantier/pull/148) | $1.17 |
| CR-207 | pr-body-from-file-only | prêt | 1/3 | [147](https://github.com/gsemet/chantier/pull/147) | $1.37 |
| CR-208 | autofix-event-vs-driver | prêt | 1/3 | [149](https://github.com/gsemet/chantier/pull/149) | $0.94 |
| CR-209 | audit-direct-false-fails | prêt | 1/3 | [150](https://github.com/gsemet/chantier/pull/150) | $1.49 |
| CR-210 | main-checkout-fast-forward | prêt | 1/3 | [153](https://github.com/gsemet/chantier/pull/153) | $3.27 |
| CR-211 | parallel-rebase-cost | prêt | 2/3 | [152](https://github.com/gsemet/chantier/pull/152) | $2.56 |
| CR-212 | release v0.9.0 | en attente | 0/3 | — | — |

J'ai vérifié chaque PR prête sur son dernier commit : 5 vérifications vertes sur 5, mergeable.
Ces vérifications sont à refaire après la remise en pile (le Stack Driver s'en charge).

## Bilan

| | |
| --- | --- |
| Prêts | 15 |
| Mergés | 1 (CR-199) |
| En attente | 1 (CR-212, release) |
| Bloqués | 0 CR ; la pile attend tes 14 force pushes |
| Points ouverts | PR 143 : bouton Refresh non vu dans un vrai panneau (pour la démo) ; PR 144 : le Foreman parle de « deux défauts esthétiques » que la description ne nomme pas |

## Coût

$41.58 sur $90, en 1 464 appels de modèle.

| Rôle | Coût | Part |
| --- | --- | --- |
| Foreman (Opus) | $9.52 | 23 % |
| Drivers de CR (Sonnet, 24 agents) | $15.70 | 38 % |
| Stack Driver | $0.38 | 1 % |
| Coders | $9.60 | 23 % |
| Inspectors | $2.73 | 6 % |
| Verifiers | $2.64 | 6 % |
| Investigator, Conflict resolver | $1.02 | 3 % |

- Le pilotage (Foreman + Drivers) pèse 62 % de la dépense du batch.
- Côté Drivers de CR, les écritures de cache font 66 % du coût, 67 de leurs 577 appels sont
  arrivés après l'expiration du cache, et 8 Drivers ont été relancés sur un CR qui en avait déjà un.
- Hors budget : le Chief of Staff a coûté $6.69 de pilotage et $1.93 de grill.

## Rétro du Chief of Staff (2026-11-13, matin)

La rétro est déjà encodée dans Chantier : à la pause du batch, une fois tout mergé, le Foreman
écrit `4-batch/retro.md` (`foreman.md` l. 24-33), puis le Chief of Staff propose chaque point dans
l'inbox (`chief-of-staff.md` l. 439-445). Le mode direct suit la même règle (l. 578-584). Les docs
(`use-cases-foreman.md`, `planning-folder.md`) et les SVG (`cr-lifecycle`,
`cr-folder-lifecycle`, `release-driver`) le montrent. Aucun CR n'est nécessaire pour l'encoder.
Les points ci-dessous sont ceux du Chief of Staff ; ceux du Foreman suivront à sa pause.

| # | Problème | Correction durable | Déjà couvert ? |
| --- | --- | --- | --- |
| 1 | Tests longs refusés après 1 h d'attente (CR-196, CR-205), jusqu'à 2 h pour CR-205 ; le refus nomme un détenteur périmé alors que le verrou est vivant | Calibrer la limite sur le nombre de places, ou une file par ordre d'arrivée sans limite ; corriger le message du refus | non |
| 2 | Drivers à court de contexte (CR-200, CR-208) ; 8 Drivers relancés | Mesurer le contexte par Driver, sortir les gros outputs (journaux de tests longs, diffs) dans des fichiers | non |
| 3 | Force pushes refusés au Foreman et au Chief of Staff : la pile a attendu jusqu'au matin | Alerte au démarrage + règle générale « les branches d'un CR sont force-pushables » | **oui** : `forge-permissions-at-start` (P1) |
| 4 | P10 annonce « 19 sur 19 absentes » alors que des règles équivalentes existent | Juger l'équivalence des règles | **oui** : même CR P1 |
| 5 | BOM UTF-8 au début des descriptions de PR (140, 144) | CR-207 (texte écrit avec Write) et le commit `d178c7e` sur main (BOM dans les fichiers suivis) ; à vérifier après le merge | probablement |
| 6 | Un appel `round` égaré a consommé un tour de CR-211 avant tout travail | `round` refuse un tour sans commit ni note depuis le précédent, ou la carte du Driver le dit | non |
| 7 | Merger 16 PRs de bas en haut demande une remise en pile, donc des force pushes, après chaque merge | Laisser l'utilisateur merger plusieurs PRs d'affilée et remettre en pile une seule fois (voir CR-211 `parallel-rebase-cost`) | en partie |
| 8 | Le Foreman a annoncé « deux défauts esthétiques » pour la PR 144, que la description ne nomme pas | Un défaut laissé de côté est nommé dans la description de la PR | non |
| 9 | La release devait d'abord attendre les merges, avant d'être finalement mise en haut de la pile : les cartes en vigueur se contredisent | CR-196 l'aligne une fois mergé | **oui** : CR-196 |

## Points de rétro de la nuit (version d'origine)

1. **File d'attente des tests longs** : un seul passage de tests longs à la fois avec 4 Drivers
   dépasse la limite d'une heure. CR-196 et CR-205 ont été refusés, CR-205 a attendu environ 2 h,
   et le message de refus nomme à tort un détenteur périmé du verrou.
2. **Drivers à court de contexte** : CR-200 et CR-208. Relancés, mais ils comptent dans les 8
   relances de Drivers.
3. **Remise en pile bloquée par le mode auto** : les force pushes du Stack Driver sont refusés au
   Foreman comme au Chief of Staff. La route de 2026-11-06 ne suffit plus en autonomie la nuit,
   d'autant que les 15 PRs, toutes basées sur main, ont des conflits deux à deux.
4. **BOM UTF-8** au début des descriptions de PR (140, 144), le texte étant écrit sous Windows.
   CR-207 corrige peut-être ce point : à vérifier avant de le classer.
5. **Tour consommé par erreur** : un appel `round` égaré a consommé un tour de CR-211 avant
   tout travail.
6. **La release attend les merges** : les cartes en vigueur lancent CR-212 une fois les autres
   mergés, donc la pile du matin n'a pas sa PR de release au-dessus. CR-196 change ce point.
