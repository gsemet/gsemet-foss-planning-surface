**batch-32** · Foreman · stack · slots 2/4 · 0 CRs done · spent $24.86 of none

⚪ not started or dropped · 🟡 working · 🟠 waiting · 🟣 ready locally · 🟤 PR in draft · 🟢 ready to merge · 🔴 blocked · ✅ merged

| CR | Subject | State | PR | Cost |
| --- | --- | --- | --- | ---: |
| CR-515 cards-inventory-last-reading | dernière lecture de l'inventaire des règles | 🟡 working, Round 2/3 | - | $15.06 |
| CR-516 cards-delete-pages-chief | pages d'aide mortes, côté Chief of Staff | 🟠 waiting: CR-515 | - | - |
| CR-517 cards-delete-pages-crew | pages d'aide mortes, côté Foreman et Driver | 🟠 waiting: CR-515 | - | - |
| CR-518 cards-delete-aggregate-topics | sujets qui ne font que réafficher | 🟠 waiting: CR-516, CR-517 | - | - |
| CR-519 cards-one-page-per-theme | une page par thème | 🟠 waiting: CR-518 | - | - |
| CR-520 brief-host-row-names | démarrage des sessions allégé | 🟠 waiting: CR-519 | - | - |
| CR-521 help-lists-role-commands | `--help` groupé, commandes par rôle | 🟠 waiting: CR-520 | - | - |
| CR-522 tui-resize-columns | colonnes de `live` plus larges | 🟢 ready to merge | [PR](https://github.com/gsemet/chantier/pull/490) | $7.23 |
| CR-523 tui-mouse-resize | redimensionnement à la souris | 🟡 working, Round 1/3 | - | $0.15 |
| CR-524 release-card-cleanup | version 0.16.0 | 🟠 waiting: toutes les autres CR | - | - |

**Notes**
- CR-522 : CI verte sur la tête 3412cd9 (check sur macOS, Linux et Windows, eval-dry-run, scenario sur Linux). Aucune carte modifiée.
- CR-522 : selon le Foreman, un Driver a ouvert la capture d'écran, ce que sa carte interdit, et n'y a vu ni nom d'utilisateur ni dossier personnel. Non vérifié par le Chief of Staff.
- CR-515 : au tour 2 ; son premier Driver a passé la main à la règle des 130 000 tokens.
- Chaîne : CR-520 après CR-519 (nouveaux noms de pages) ; CR-521 après CR-520 (mêmes fichiers).
- Délai de livraison : inconnu, aucune durée de test long enregistrée ; chaîne la plus longue CR-515 → CR-517 → CR-518 → CR-519 → CR-520 → CR-521 → CR-524.
- Pile : pas encore de pile, 1 PR sur 2 rendue prête.

| Who | Cost | Share | Calls |
| --- | ---: | ---: | ---: |
| Foreman | $2.414 | 10% | 71 |
| Driver chantier:cr-driver | $4.117 | 17% | 106 |
| Worker chantier:investigator | $8.267 | 33% | 193 |
| Worker chantier:coder | $4.912 | 20% | 100 |
| Worker chantier:inspector | $2.600 | 10% | 66 |
| Worker chantier:verifier | $2.590 | 10% | 74 |
| Total | $24.900 | 100% | 610 |

Orchestration (steering + Drivers): 27% of the batch's spend

| Outside the batch's spend | Cost | Detail |
| --- | ---: | --- |
| Chief of Staff, steering the batch | $0.89 | hors budget, depuis l'ouverture du batch (21 appels) |
| Chief of Staff, grill and specifications with the user | $37.34 | hors budget, depuis l'ouverture du batch (780 appels, 23 spec-writers, 10 spec critics) |
| Chief of Staff, whole session | $72.89 | contexte 190 638 tokens ; non comptés : 3 compactions depuis l'ouverture, sans trace (environ $0.12 chacune) |

**For you:**
- 🟢 ready to merge CR-522 tui-resize-columns https://github.com/gsemet/chantier/pull/490 — test long levé, validé par CR-523. Manques : avec un seul projet suivi, `live --once` sans taille de terminal (120 colonnes, par exemple dans un tube) n'affiche plus les cadres Projects et Agents (la colonne de gauche demande 122 colonnes) ; le scénario complet n'a pas tourné en local sous Windows (il passe en CI sur Linux), ce passage est laissé à la PR empilée dessus ; en `--once`, la raison d'un élément bloqué peut être coupée (le cadre Tasks compte une ligne pour un élément qui en prend deux).
- context-limits-Q9 attend toujours votre réponse.
