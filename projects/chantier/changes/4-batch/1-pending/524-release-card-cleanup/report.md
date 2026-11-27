**batch-32** · Foreman · stack · slots 2/4 · 0 CRs done · spent $13.65 of none

⚪ not started or dropped · 🟡 working · 🟠 waiting · 🟣 ready locally · 🟤 PR in draft · 🟢 ready to merge · 🔴 blocked · ✅ merged

| CR | Subject | State | PR | Cost |
| --- | --- | --- | --- | ---: |
| CR-515 cards-inventory-last-reading | dernière lecture de l'inventaire des règles | 🟡 working, Round 1/3 | - | $9.58 |
| CR-516 cards-delete-pages-chief | pages d'aide mortes, côté Chief of Staff | 🟠 waiting: CR-515 | - | - |
| CR-517 cards-delete-pages-crew | pages d'aide mortes, côté Foreman et Driver | 🟠 waiting: CR-515 | - | - |
| CR-518 cards-delete-aggregate-topics | sujets qui ne font que réafficher | 🟠 waiting: CR-516, CR-517 | - | - |
| CR-519 cards-one-page-per-theme | une page par thème | 🟠 waiting: CR-518 | - | - |
| CR-520 brief-host-row-names | démarrage des sessions allégé | 🟠 waiting: CR-519 | - | - |
| CR-521 help-lists-role-commands | `--help` groupé, commandes par rôle | 🟠 waiting: CR-520 | - | - |
| CR-522 tui-resize-columns | colonnes de `live` plus larges | 🟡 working, Round 1/3 | - | $2.63 |
| CR-523 tui-mouse-resize | redimensionnement à la souris | 🟠 waiting: CR-522 | - | - |
| CR-524 release-card-cleanup | version 0.16.0 | 🟠 waiting: toutes les autres CR | - | - |

**Notes**
- CR-515 : selon son Driver, 329 règles relues, 93 protectrices, toutes déjà tenues ; rien à remettre. Pas encore relu.
- Chaîne : CR-520 après CR-519 (elle utilise les nouveaux noms de pages) ; CR-521 après CR-520 (mêmes fichiers).
- Délai : inconnu, aucune durée de test long enregistrée ; 7 niveaux, chaîne la plus longue CR-515 → CR-517 → CR-518 → CR-519 → CR-520 → CR-521 → CR-524.
- Pile : no stack yet: 0 of 2 PRs handed back ready.

| Who | Cost | Share | Calls |
| --- | ---: | ---: | ---: |
| Foreman | $1.437 | 10% | 38 |
| Driver chantier:cr-driver | $1.183 | 9% | 32 |
| Worker chantier:investigator | $8.267 | 61% | 193 |
| Worker chantier:coder | $2.388 | 17% | 45 |
| Worker chantier:inspector | $0.375 | 3% | 8 |
| Total | $13.650 | 100% | 316 |

Orchestration (steering + Drivers): 19% of the batch's spend

| Outside the batch's spend | Cost | Detail |
| --- | ---: | --- |
| Chief of Staff, steering the batch | $0.20 | outside the budget, since the batch opened (7 calls) |
| Chief of Staff, grill and specifications with the user | $36.84 | outside the budget, since the batch opened (772 calls, 23 spec-writers, 10 spec critics) |
| Chief of Staff, whole session | $71.70 | context 255,743 tokens; not counted: 2 compactions since the batch opened, which leave no record (about $0.12 each) |

**For you:** nothing
