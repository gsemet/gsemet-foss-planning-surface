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
