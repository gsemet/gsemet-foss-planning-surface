**batch-32** · Foreman · stack · slots 2/4 · 0 CRs done · spent $4.90 of none

⚪ not started or dropped · 🟡 working · 🟠 waiting · 🟣 ready locally · 🟤 PR in draft · 🟢 ready to merge · 🔴 blocked · ✅ merged

| CR | Subject | State | PR | Cost |
| --- | --- | --- | --- | ---: |
| CR-515 cards-inventory-last-reading | dernière lecture de l'inventaire des règles | 🟡 working | - | $2.71 |
| CR-516 cards-delete-pages-chief | pages d'aide mortes, côté Chief of Staff | 🟠 queued, waits for CR-515 | - | - |
| CR-517 cards-delete-pages-crew | pages d'aide mortes, côté Foreman et Driver | 🟠 queued, waits for CR-515 | - | - |
| CR-518 cards-delete-aggregate-topics | sujets qui ne font que réafficher | 🟠 queued, waits for CR-516, CR-517 | - | - |
| CR-519 cards-one-page-per-theme | une page par thème | 🟠 queued, waits for CR-518 | - | - |
| CR-520 brief-host-row-names | démarrage des sessions allégé | 🟠 queued, waits for CR-519 | - | - |
| CR-521 help-lists-role-commands | `--help` groupé, commandes par rôle | 🟠 queued, waits for CR-520 | - | - |
| CR-522 tui-resize-columns | colonnes de `live` plus larges | 🟡 working | - | $1.09 |
| CR-523 tui-mouse-resize | redimensionnement à la souris | 🟠 queued, waits for CR-522 | - | - |
| CR-524 release-card-cleanup | version 0.16.0 | 🟠 queued, waits for every other CR | - | - |

**Notes**
- Test long `scenario` : dispensé en local sur les CR du dessous (O-15), validé par le test du haut de la pile.
- Délai : inconnu, aucune durée de test long enregistrée dans ce batch. Chaîne la plus longue : CR-515 → CR-517 → CR-518 → CR-519 → CR-520 → CR-521 → CR-524.
- Un autre batch (markdown-okf-schema-studio batch-11) tourne et lit les cartes en direct : choisir le moment de la fusion.

| Who | Cost | Share | Calls |
| --- | ---: | ---: | ---: |
| Foreman | $1.098 | 22% | 25 |
| Driver chantier:cr-driver | $0.486 | 10% | 20 |
| Worker chantier:investigator | $2.572 | 51% | 68 |
| Worker chantier:coder | $0.882 | 17% | 19 |
| Total | $5.038 | 100% | 132 |

Orchestration (steering + Drivers): 32% of the batch's spend

| Outside the batch's spend | Cost | Detail |
| --- | ---: | --- |
| Chief of Staff, steering the batch | $0.09 | outside the budget, since the batch opened (4 calls) |
| Chief of Staff, grill and specifications with the user | $36.65 | outside the budget, since the batch opened (768 calls, 23 spec-writers, 10 spec critics) |
| Chief of Staff, whole session | $71.40 | context 241,399 tokens; not counted: 2 compactions since the batch opened, which leave no record (about $0.12 each) |

**For you:** nothing
