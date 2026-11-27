# Answers

- 2026-11-26, the owner, on the three paths CR-505 cannot accept: "Écrire les tests (Recommandé)" (another kind of test, in the follow-up before the switch; strict rule unchanged).
- 2026-11-26, the owner, batch09-Q1: "A. Suite au batch suivant (Recommandé)" (batch-09 keeps the 3 open changes, the 4 anomalies and the release; these follow-ups go to the batch after it, opened after batch-09 closes on the owner's word). This replaces the earlier "Dans batch-09", given before the release rule was said.

- 2026-11-27, owner, asked whether to put this item in P1: « Oui, en P1 ».
- 2026-11-27, the owner, widening this item after reading the requirements site: « mon but est que github pages affiche pour tous les StRS tested by et accepted by. » (the goal is that GitHub Pages shows, for every StRS, both "Tested by" and "Accepted by"). The item therefore also covers the walks on the simulated bench, not the acceptance walks alone.

Facts read at `origin/main` `b9b29c5a` (2026-11-27), not decisions:

- 95 live StRS declare 156 paths. 6 have a simulated walk ("Tested by"), 22 an acceptance ("Accepted by"), none has both: 150 simulated walks and 134 acceptances are missing.
- `requirements/guidelines/project.guidelines.md`, "Benches": a `@tests_req` StRS marker may not sit under `test/integration/`; CORE-007, CORE-008 and TRUST-014 are accepted outside VS Code.
- The simulated walks run on every pull request; the real VS Code jobs run on every push to `main` and on a heavy dispatch.

Open points for the grill:

- Whether "every StRS" means every declared path (as the site shows them), and what the three StRS accepted outside VS Code, and the paths TRUST-012 S1 and S2, show under "Tested by".
- What check keeps both columns filled: the stricter okfreq mode named in `docs/how-we-test.md` asks for acceptance of every path, and it says nothing of simulated walks.
- Whether the acceptance job, or the integration job too, runs on every pull request (asked on 2026-11-27, not answered; last `main` run: acceptance 1.4 min, integration 17.7 min).
- 2026-11-27, the owner, asking about reuse: « on ne peut pas remplacer des tests existant par ces tests ? il y a beaucoup de test d'integration. »

Facts for that question (2026-11-27, not decisions):

- 95 live StRS: 38 declare 1 path, 54 declare 2, 2 declare 3, 1 declares 4 (156 paths).
- CR-504's final marker sort (its `evidence/strs-marker-sort.md`) removed 111 StRS marker lines as "partial path" on live StRS: 65 under `test/integration/`, 46 elsewhere, on 73 StRS; the files named still exist at `b9b29c5a`. Of the 68 StRS with no walk today, 59 have at least one such partial test, 9 have none. The sort is per StRS, not per path, and read only tests that carried a StRS marker then.
- The same sort's rule: every step through the product mechanism, every named state and outcome asserted; an injected page message, a test hook or a faked host result does not count. The simulated bench of `test/visual` plays against a mock host.

Open points for the grill:

- Existing tests first: extend or merge partial tests into whole walks, their SwRS markers kept, before writing new ones.
- How a path that goes through the host can count under "Tested by": a simulated bench running the real host logic, or another rule for that column.
- 2026-11-27, the owner, asked whether both columns are filled for every path (156) or once per StRS (95): « Chaque parcours ». Every declared path of every live StRS shows a "Tested by" and an "Accepted by"; this settles the first open point on "every StRS".
- 2026-11-27, the owner, on what cannot be tested: « pour les req qui sont pas testable il y a un systeme de waiver ».

Facts for that point (`origin/main` `b9b29c5a`, 2026-11-27, not decisions):

- The waiver is `acceptance_exemption: true` with a non-blank `acceptance_exemption_reason`, on a whole StRS (`requirements/tiers/_schema/strs.schema.yaml`); the owner's agreement is needed, and being slow or expensive is not a reason (`.agents/skills/okfreq/references/operations.md`). No StRS carries it today.
- The site shows "waived" and the reason in place of "Accepted by"; "Tested by" still shows its files or its count (`test/site/requirementsViewer/pages.ts`, SwRS-MDOKFSTUDIO-CORE-080 S4).
- CR-505 (Q32, D15): a waiver is only for a StRS with no step that can be automated, with no candidate then. The owner's answer of 2026-11-26 above asks for tests, not a waiver, on the three paths CR-505 could not accept.
