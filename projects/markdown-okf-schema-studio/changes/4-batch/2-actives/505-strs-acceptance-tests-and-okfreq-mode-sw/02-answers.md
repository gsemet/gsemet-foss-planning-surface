# Answers

1. acceptance-Q1 (2026-11-25, Chief of Staff, owner's word "no question"): **Scope and decisions come from CR-504 (`strs-path-validation`, CR-A):** its section "Handed to the next CR (CR-B)" and its Q27-Q42 (okfreq 0.18 design, budget Q37, no waivers D15). This CR stacks after CR-504 and depends on it (`depends.json`).
2. acceptance-Q2 (Chief of Staff): **Delivery in this CR is as large as the Driver can make it in 3 rounds; if the Driver reports that it cannot finish, the Chief of Staff splits it per e2e group (first group adds the acceptance job).** The mode switch and the D11 gate land last.

3. acceptance-Q3 (2026-11-25, Chief of Staff, spec-critic round 1): **Every finding of `work/critic-r1.md` is applied as stated.** CORE-076 is updated by this CR (no SwRS-for-tooling exception); the job wiring docs land in commit 1; the Foreman counts rounds (one coder to Inspector cycle) and decides a partial delivery.

4. acceptance-Q4 (2026-11-25, Chief of Staff, ask A-16 of CR-504): **CR-505 also repairs what CR-504 leaves as Known gaps:** (D) the 136 `@tests_req` fragment blocks dropped without adding the scenario or moving the marker, and (E) the wrong fragments (3 of 16 sampled), so every fragment is re-read against its test and the uncovered counts are recomputed.

Grilled enough (2026-11-25): by the Chief of Staff, the design being already grilled in CR-504.
Destination: running batch batch-09. Critic: yes.

Owner's overnight grant (2026-11-25, near midnight, the owner to the Chief of Staff: "je vais aller au lit. tu as toute latitude pour finaliser la stack cette nuit: tu peux passer les contexts a 300K des driver, faire 10 rework max"): the Chief of Staff decides alone to get the stack finished tonight; a CR may take up to 10 rounds; a Driver or stack driver hands back for context only at 300,000 tokens.
