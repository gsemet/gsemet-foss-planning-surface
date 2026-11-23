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
