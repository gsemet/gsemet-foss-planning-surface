Short name: `stack-merge-check`

1. stack-merge-check-Q1 (2026-11-26, night, decided by the Chief of Staff under the owner's overnight grant: "tu as toute latitude pour finaliser la stack cette nuit: tu peux passer les contexts a 300K des driver, faire 10 rework max"; ask A-20): **A new change in the stack above CR-501**, below CR-500, CR-504, CR-505, CR-507 and CR-509, not a pull request on `main`. No ready pull request moves, and every change above checks out the fixed script.
2. stack-merge-check-Q2 (Chief of Staff): **The check stays as strict.** A merge commit carried by any branch of the stack still fails it, the bottom one and the ones below the checked pull request included as far as git alone can tell. No skipped job, no `continue-on-error`, no check turned off for stacks. Tests prove both directions on the chain shape observed in run 45741461955.
3. stack-merge-check-Q3 (Chief of Staff): **Proof.** The unit tests, and the green CI run of this pull request itself above the bottom of the native stack (the live case). If what git alone can tell leaves a hole, name it in Known gaps.
4. stack-merge-check-Q4 (Chief of Staff): **Order.** It sits directly above CR-501; this replaces heavy-ci-Q4's "as low as possible" for CR-509, which sits above it. Up to 10 rounds; context hand-back at 300,000 tokens (order O-131).

Spec critic: no, it changes one CI script and its tests.

Destination: running batch batch-09.
