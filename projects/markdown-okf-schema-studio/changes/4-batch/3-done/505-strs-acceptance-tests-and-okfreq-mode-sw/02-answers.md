# Answers

1. acceptance-Q1 (2026-11-25, Chief of Staff, owner's word "no question"): **Scope and decisions come from CR-504 (`strs-path-validation`, CR-A):** its section "Handed to the next CR (CR-B)" and its Q27-Q42 (okfreq 0.18 design, budget Q37, no waivers D15). This CR stacks after CR-504 and depends on it (`depends.json`).
2. acceptance-Q2 (Chief of Staff): **Delivery in this CR is as large as the Driver can make it in 3 rounds; if the Driver reports that it cannot finish, the Chief of Staff splits it per e2e group (first group adds the acceptance job).** The mode switch and the D11 gate land last.

3. acceptance-Q3 (2026-11-25, Chief of Staff, spec-critic round 1): **Every finding of `work/critic-r1.md` is applied as stated.** CORE-076 is updated by this CR (no SwRS-for-tooling exception); the job wiring docs land in commit 1; the Foreman counts rounds (one coder to Inspector cycle) and decides a partial delivery.

4. acceptance-Q4 (2026-11-25, Chief of Staff, ask A-16 of CR-504): **CR-505 also repairs what CR-504 leaves as Known gaps:** (D) the 136 `@tests_req` fragment blocks dropped without adding the scenario or moving the marker, and (E) the wrong fragments (3 of 16 sampled), so every fragment is re-read against its test and the uncovered counts are recomputed.

Grilled enough (2026-11-25): by the Chief of Staff, the design being already grilled in CR-504.
Destination: running batch batch-09. Critic: yes.

Owner's overnight grant (2026-11-25, near midnight, the owner to the Chief of Staff: "je vais aller au lit. tu as toute latitude pour finaliser la stack cette nuit: tu peux passer les contexts a 300K des driver, faire 10 rework max"): the Chief of Staff decides alone to get the stack finished tonight; a CR may take up to 10 rounds; a Driver or stack driver hands back for context only at 300,000 tokens.

5. acceptance-Q5 (2026-11-26, Chief of Staff, ask A-28, partial delivery): **Where the rest of the acceptance tests goes: "Dans batch-09".** One follow-up CR per e2e group joins the running batch, the coverage-mode switch and its gate in the last one. The owner chose it knowing that batch-09 then stays open long (Driver estimate: 25 to 35 rounds in all, up to 15 groups).

6. acceptance-Q6 (2026-11-26, Chief of Staff): **The three paths this CR cannot accept (TRUST-012 S1 and S2, TRUST-014 S1): "Écrire les tests (Recommandé)".** Another kind of test (driving the real window, a real install) is written in a follow-up, before the switch. The strict marker rule is unchanged.

7. batch09-Q1 (2026-11-26, Chief of Staff; changes acceptance-Q5's batch only): **"A. Suite au batch suivant (Recommandé)".** Chantier's release CR waits for every other CR of its batch, so the follow-ups (one CR per group, the three paths of acceptance-Q6, the switch last) go to the batch after batch-09, opened after batch-09 closes on the owner's word. batch-09 keeps CR-505, CR-507, CR-509, the four inbox anomalies and then the release.
