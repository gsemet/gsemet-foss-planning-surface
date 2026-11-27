**batch-32** · Foreman · stack · slots 2/4 · 1 CRs done · spent $41.20 of none

⚪ not started or dropped · 🟡 working · 🟠 waiting · 🟣 ready locally · 🟤 PR in draft · 🟢 ready to merge · 🔴 blocked · ✅ merged

| CR | Subject | State | PR | Cost |
| --- | --- | --- | --- | ---: |
| CR-515 cards-inventory-last-reading | dernière lecture de l'inventaire des règles | 🟡 working, Round 2/3 | - | $21.24 |
| CR-516 cards-delete-pages-chief | pages d'aide mortes, côté Chief of Staff | 🟠 waiting: CR-515 | - | - |
| CR-517 cards-delete-pages-crew | pages d'aide mortes, côté Foreman et Driver | 🟠 waiting: CR-515 | - | - |
| CR-518 cards-delete-aggregate-topics | sujets qui ne font que réafficher | 🟠 waiting: CR-516, CR-517 | - | - |
| CR-519 cards-one-page-per-theme | une page par thème | 🟠 waiting: CR-518 | - | - |
| CR-520 brief-host-row-names | démarrage des sessions allégé | 🟠 waiting: CR-519 | - | - |
| CR-521 help-lists-role-commands | `--help` groupé, commandes par rôle | 🟠 waiting: CR-520 | - | - |
| CR-522 tui-resize-columns | colonnes de `live` plus larges | ✅ merged | [PR](https://github.com/gsemet/chantier/pull/490) | $7.23 |
| CR-523 tui-mouse-resize | redimensionnement à la souris | 🟡 working, Round 2/3 | - | $9.22 |
| CR-524 release-card-cleanup | version 0.16.0 | 🟠 waiting: toutes les autres CR | - | - |

**Notes**
- CR-522 tui-resize-columns : fusionnée le 2026-11-27 à 14:04 UTC. Dépôt principal avancé : `main checkout: fast-forwarded to fbdb53d`.
- Selon le Foreman, les Drivers de CR-515 et CR-523 reçoivent seulement une consigne de rebase ; aucune pile n'est à reconstruire, il n'y en a pas encore sur GitHub.
- Les CR en attente avancent quand les Drivers rendent les précédentes, d'abord CR-515 cards-inventory-last-reading.
- Chaîne : CR-520 après CR-519 (nouveaux noms de pages) ; CR-521 après CR-520 (mêmes fichiers).
- Délai de livraison : inconnu, aucune durée de test long enregistrée ; chaîne la plus longue, 7 niveaux : CR-515 → CR-517 → CR-518 → CR-519 → CR-520 → CR-521 → CR-524.
- Pile : pas encore de pile, 0 PR sur 2 rendue prête.
- Contexte des Drivers : dans batch-32, aucun Driver ne passe la main à cause de la taille de son contexte (consigne du propriétaire) ; aucun autre plafond ne remplace cette limite. Pas encore vérifié : qu'un Driver compacté relise sa fiche.

| Who | Cost | Share | Calls |
| --- | ---: | ---: | ---: |
| Foreman | $3.503 | 9% | 101 |
| Driver chantier:cr-driver | $5.838 | 14% | 133 |
| Worker chantier:coder | $13.289 | 32% | 283 |
| Worker chantier:investigator | $9.823 | 24% | 223 |
| Worker chantier:inspector | $6.152 | 15% | 161 |
| Worker chantier:verifier | $2.590 | 6% | 74 |
| Total | $41.195 | 100% | 975 |

Orchestration (steering + Drivers): 23% of the batch's spend

| Outside the batch's spend | Cost | Detail |
| --- | ---: | --- |
| Chief of Staff, steering the batch | $2.24 | hors budget, depuis l'ouverture du batch (46 appels) |
| Chief of Staff, grill and specifications with the user | $37.68 | hors budget, depuis l'ouverture du batch (788 appels, 23 spec-writers, 10 spec critics) |
| Chief of Staff, whole session | $74.58 | contexte 130 107 tokens ; non comptés : 4 compactions depuis l'ouverture, sans trace (environ $0.12 chacune) |

**For you:** rien pour l'instant.
