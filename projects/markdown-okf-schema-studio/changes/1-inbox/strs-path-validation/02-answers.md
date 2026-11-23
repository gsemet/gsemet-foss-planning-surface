# Answers

Short name: `strs-validation`

## Series 1, 2026-11-23 (owner, through the Griller)

1. strs-validation-Q1: **V&V wording.** A, acceptance. Owner's words: "Ok pour acceptance, comment tu nommerais le marqueur ?" An automated end-to-end test of a StRS path is an acceptance test (verification at the StRS level), not a validation by the user. The marker's name is asked in series 2.
2. strs-validation-Q2: **Steps no test can do.** Not settled; the owner challenges the premise: "si on maîtrise les entrants et les assertions, je ne vois pas quel comportement humain ne peut pas être simulé. « Lire les notes de versions », comme on sait ce que l'on a donné en entrée on peut imaginer des asserts pour simuler les vérifs de l'homme non ?" Follow-up in series 2.
3. strs-validation-Q3: **Anti-duplicate rule.** A: one nominal path per test, run end to end in one go, the final result asserted (plus the steps no SwRS covers), never edge cases or errors.
4. strs-validation-Q4: **Status.** Two scores per StRS, in the owner's words: "« tested » (SwRS liées), et « accepted » (les chemins)". Exact definitions confirmed in series 2.
