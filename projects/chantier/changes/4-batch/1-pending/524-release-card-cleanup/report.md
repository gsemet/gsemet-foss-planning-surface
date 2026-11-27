**batch-32** · Foreman · stack · slots 3/4 · 1 CRs done · spent $57.24 of none

⚪ not started or dropped · 🟡 working · 🟠 waiting · 🟣 ready locally · 🟤 PR in draft · 🟢 ready to merge · 🔴 blocked · ✅ merged

| CR | Subject | State | PR | Cost |
| --- | --- | --- | --- | ---: |
| CR-515 cards-inventory-last-reading | dernière lecture de l'inventaire des règles | 🟠 waiting: rendue, attend la pile | [PR](https://github.com/gsemet/chantier/pull/491) | $28.95 |
| CR-516 cards-delete-pages-chief | pages d'aide mortes, côté Chief of Staff | 🟡 working, Round 1/3 | - | $0.87 |
| CR-517 cards-delete-pages-crew | pages d'aide mortes, côté Foreman et Driver | 🟡 working, Round 1/3 | - | $0.86 |
| CR-518 cards-delete-aggregate-topics | sujets qui ne font que réafficher | 🟠 waiting: CR-516, CR-517 | - | - |
| CR-519 cards-one-page-per-theme | une page par thème | 🟠 waiting: CR-518 | - | - |
| CR-520 brief-host-row-names | démarrage des sessions allégé | 🟠 waiting: CR-519 | - | - |
| CR-521 help-lists-role-commands | `--help` groupé, commandes par rôle | 🟠 waiting: CR-520 | - | - |
| CR-522 tui-resize-columns | colonnes de `live` plus larges | ✅ merged | [PR](https://github.com/gsemet/chantier/pull/490) | $7.23 |
| CR-523 tui-mouse-resize | redimensionnement à la souris | 🟡 working, CI 2/3 | [PR](https://github.com/gsemet/chantier/pull/492) | $14.19 |
| CR-524 release-card-cleanup | version 0.16.0 | 🟠 waiting: toutes les autres CR | - | - |

**Notes**
- CR-515 cards-inventory-last-reading : ne pas fusionner. Le board l'affiche en vert, mais elle attend qu'une deuxième CR soit rendue avec sa PR pour former la pile. Ses réserves seront citées au moment de la fusion.
- CR-523 tui-mouse-resize : PR en brouillon, ne pas fusionner. Test long passé à d8397a4, mais ce point ne contient pas CR-515 : il devra être refait sur un point qui la contient. L'essai de la souris à la main n'est pas fait.
- CR-522 tui-resize-columns : `main checkout: fast-forwarded to fbdb53d`.
- Chaîne : CR-520 après CR-519 (nouveaux noms de pages) ; CR-521 après CR-520 (mêmes fichiers).
- Plancher : au moins environ 2,6 h (chaîne : 6 niveaux × (16 min de test long + 10 min de CI) ; verrou : 1 test long × 16 min) ; livraison pas avant 18 h 50 environ. Chaîne la plus longue : CR-517 → CR-518 → CR-519 → CR-520 → CR-521 → CR-524. Le calcul compte un test long par niveau, alors que seule la CR du haut en lance un.
- Pile : pas encore de pile, 1 PR sur 2 rendue prête.

| Who | Cost | Share | Calls |
| --- | ---: | ---: | ---: |
| Foreman | $5.139 | 9% | 145 |
| Driver chantier:cr-driver | $10.959 | 19% | 230 |
| Worker chantier:coder | $15.029 | 26% | 322 |
| Worker chantier:investigator | $9.823 | 17% | 223 |
| Worker chantier:verifier | $8.861 | 16% | 261 |
| Worker chantier:inspector | $7.132 | 12% | 175 |
| Worker chantier:debugger | $0.300 | 1% | 10 |
| Total | $57.243 | 100% | 1366 |

Orchestration (steering + Drivers): 28% of the batch's spend

| Outside the batch's spend | Cost | Detail |
| --- | ---: | --- |
| Chief of Staff, steering the batch | $2.84 | hors budget, depuis l'ouverture du batch (63 appels) |
| Chief of Staff, grill and specifications with the user | $38.09 | hors budget, depuis l'ouverture du batch (798 appels, 23 spec-writers, 10 spec critics) |
| Chief of Staff, whole session | $75.59 | contexte 197 086 tokens ; non comptés : 4 compactions depuis l'ouverture, sans trace (environ $0.12 chacune) |

**For you:** deux décisions : la place de la règle N1 (CR-517 cards-delete-pages-crew), et les 2 tests qui échouent avec `NO_COLOR=1`.
