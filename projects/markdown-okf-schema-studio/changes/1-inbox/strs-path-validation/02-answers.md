# Answers

Short name: `strs-validation`

## Series 1, 2026-11-23 (owner, through the Griller)

1. strs-validation-Q1: **V&V wording.** A, acceptance. Owner's words: "Ok pour acceptance, comment tu nommerais le marqueur ?" An automated end-to-end test of a StRS path is an acceptance test (verification at the StRS level), not a validation by the user. The marker's name is asked in series 2.
2. strs-validation-Q2: **Steps no test can do.** Not settled; the owner challenges the premise: "si on maîtrise les entrants et les assertions, je ne vois pas quel comportement humain ne peut pas être simulé. « Lire les notes de versions », comme on sait ce que l'on a donné en entrée on peut imaginer des asserts pour simuler les vérifs de l'homme non ?" Follow-up in series 2.
3. strs-validation-Q3: **Anti-duplicate rule.** A: one nominal path per test, run end to end in one go, the final result asserted (plus the steps no SwRS covers), never edge cases or errors.
4. strs-validation-Q4: **Status.** Two scores per StRS, in the owner's words: "« tested » (SwRS liées), et « accepted » (les chemins)". Exact definitions confirmed in series 2.

## Series 2, 2026-11-23

5. strs-validation-Q5: **Marker name.** `@accepts_req`. The path fragment is not settled, owner's words: "Par contre je ne suis pas sûr pour le #path, c'est comme les tests_req quand il y a plusieurs transitions". Follow-up in series 3.
6. strs-validation-Q6: **Human steps.** A: the human act is a simulated input (e.g. "release notes approved"); the test asserts the system's gate (blocked without it, proceeds with it) and the checkable content, never a judgment. A method other than Test is a rare exception, written in the path. (Settles Q2.)
7. strs-validation-Q7: **The 185 existing `@tests_req StRS-...` markers.** A: a read-only audit first, each marker classified (walks a path, single-state snapshot, duplicate of a SwRS test); only those that walk a path move to `@accepts_req`, the others lose their StRS marker.
8. strs-validation-Q8: **Scope.** B: all 151 paths (owner's choice over the recommended pilot). Delivery shape asked in series 3.

## Series 3, 2026-11-23

9. strs-validation-Q9: **Path fragment.** B: no fragment; the marker is `@accepts_req StRS-X`, as `@tests_req` names a SwRS. Consequence for Q4 asked in series 4.
10. strs-validation-Q10: **Delivery.** B: one CR for everything (owner's choice over the recommended split).
11. strs-validation-Q11: **Bench.** Not settled; owner's words: "les StRS sont validés (« accepts_req ») par le vrai banc et donc ça coûte bcp plus cher à exécuter, mais est « testé » par le banc virtuel. Ça permet de faire les 2." Clarified in series 4.
12. strs-validation-Q12: **StRS without "Main paths".** Not settled; the owner asks why they exist, gap or impossibility. Griller's finding, 2026-11-23: of 152 StRS, 58 are retired (56 superseded, 2 deprecated) and have no paths by design; 94 are live (80 proposed, 14 approved), 92 of them with "Main paths" (151 paths); 2 live StRS have none: StRS-MDOKFSTUDIO-TRUST-012 (visible text and the icon speak of the product) and StRS-MDOKFSTUDIO-TRUST-014 (built from pinned dependencies, ships what it loads). 93 live StRS already carry a direct `@tests_req StRS-...`: today almost every live StRS counts as "validated". Follow-up in series 4.

## Series 4, 2026-11-23

13. strs-validation-Q13: **What "accepted" measures.** Back to a path fragment (reverses Q9), owner's words: "Ok on revient sur le fragment mais alors il faudra un frontmatter pour déclarer les paths, et il faudra faire pareil avec les scénarios dans les SwRS. Il y a une grosse migration des req existants à faire". So: `@accepts_req StRS-X#<path>`, paths declared in the StRS frontmatter, the same for SwRS scenarios, and a migration of the existing requirements. Shape asked in series 5.
14. strs-validation-Q14: **Benches.** C (over the recommended A): a path that passes on the simulated bench is "tested", a path that passes on the real VS Code bench is "accepted". Reconciliation with Q4 ("tested" = linked SwRS) asked in series 5.
15. strs-validation-Q15: **TRUST-012 and TRUST-014** (the two live StRS with no path). A: each gets a short path that starts from the built deliverable (the VSIX); rule with no exception: every live StRS has at least one path.
16. strs-validation-Q16: **Destination of the idea.** A: read-only audit first (step one of the CR), then the project CR, then the okf-schema feature request (forge-neutral), backed by the CR's real figures.

Griller's findings, 2026-11-23: live SwRS = 443 (of 1051), with 2549 `### Scenario` headings (3907 in all); headings vary ("Scenario: Nominal", "Scenario (boundary): ...", "Scenario: Restricted Mode"). okfreq comes from the `okf-schema>=0.17.0` package (pyproject `requirements` group), not from this repository; its config knows two markers (`implements`, `tests`), and the frontmatter schema (`requirements/tiers/_schema/base.schema.yaml`) has `additionalProperties: false` in places. 14 live StRS are `approved` (approval_lock): changing them needs the owner's recorded agreement.

## Series 5, 2026-11-23

17. strs-validation-Q17: **Frontmatter shape.** Not settled; owner's words: "Il faudrait trouver une formulation qui soit utilisable pour les StRS sur les paths et les SwRS sur les scénarios". One shared declaration for StRS paths and SwRS scenarios; proposal in series 6.
18. strs-validation-Q18: **SwRS scenarios.** A: declared in the same migration (scripted from the headings); the fragment on `@tests_req` stays optional: `@tests_req SwRS-X` with no fragment still covers the whole SwRS.
19. strs-validation-Q19: **Counters.** B, two counters (the option's wording was unclear: its meaning is confirmed in series 6).
20. strs-validation-Q20: **Order.** B: the okf-schema feature request first; the project CR waits for okfreq to support the marker and the declarations (reverses the order of Q16 for the CR; the audit's place is confirmed in series 6).

## Series 6, 2026-11-23

21. strs-validation-Q21: **One declaration.** B: one frontmatter field `scenarios:` for both tiers (StRS paths and SwRS scenarios), each with a stable short id (e.g. `S1`, never reused), no `kind`: the tier says what it is (StRS = path, SwRS = transition scenario). Fragment `#S<n>` on both markers. (Supersedes the field shape of Q13/Q17.)
22. strs-validation-Q22: **The two counters** (Q19 restated). A: per StRS, "tested" = its paths have a test on the simulated bench, "accepted" = its paths have a test on the real VS Code bench. SwRS coverage stays okfreq's usual coverage shown on each SwRS, not recounted in the StRS. (Supersedes Q4's "tested = linked SwRS".)
23. strs-validation-Q23: **Audit.** A: a sample audit now, in this Griller session (about 30 markers across every folder, each classified "walks a path / single-state snapshot / SwRS duplicate"), written in `experiments/`; the okf-schema request rests on it; the full sort of the 185 stays in the CR.
24. strs-validation-Q24: **Approved StRS.** A: one agreement, recorded in the CR, for the scripted migration that declares existing paths as `scenarios:` (metadata only); any change to the normative text of an approved StRS goes back to the owner one by one. Owner's agreement for that migration: given 2026-11-23 (this answer).

Griller's sample audit (Q23), 2026-11-23, in `experiments/02-audit-sample.md` (31 of the 185 markers, 1 in 6; two rows checked again by hand): 13 walk a path (4 of them a one-step path, which is the same check as its SwRS), 1 a partial path, 6 single-state snapshots (all visual), 8 duplicate one SwRS transition (6 of them integration tests that stop after step 1), 3 other (TRUST-014 has no path; 2 test a flow that is not one of the StRS's paths). By bench: 8 of the 13 path rows run in real VS Code. Read on the 185: about 4 markers in 10 would move to `@accepts_req`, about 1 in 4 would count as "accepted"; today 93 live StRS count as validated. Simulated paths stub the host step (rows 23, 26).
