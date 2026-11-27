# Answers

Short name: `ci-split`

1. The owner's instruction (2026-11-27, Chief of Staff session of batch-09), verbatim: "Oui découpe la
   CI maintenant juste après celle que tu fini il faut pouvoir aller vite."

   Applied by the Chief of Staff: a CR of its own, in the running batch, after CR-517 and before
   CR-518. No question was asked: the invariants of the intent (same tests, same repetitions, same
   gates, same local targets) are the Chief of Staff's reading of "split", and the way to share the
   work between jobs is the specification's to choose.

2. Choices of the Chief of Staff for the specification:
   - Keep the change small: split what the two jobs already do; reuse the targets and the report merge.
   - Prefer a split that keeps each stress scenario's rounds in one VS Code window (share the
     scenarios between jobs, not the rounds).
   - The heavy run that proves the change is made on this CR's own branch (it measures the split).

3. The owner's night instruction still holds for this CR: at most 6 rounds.

4. Ruling of the Chief of Staff on the specification's open question 2 (2026-11-27): if a part
   measures clearly above 11 min, it is the Coder's call within this CR, from the measured run (move
   a suite to the other part, or add a third part), with the same tests, repetitions, gates and local
   targets, and the choice written in the PR.

5. Ruling of the Chief of Staff on the specification's open question 1 (2026-11-27), told to the
   owner: the visual jobs stay out of this CR, as the intent says; a heavy run of about 13 to 14 min
   is accepted. In the heavy run 45951664534 of CR-517 `visual-2` took 7.8 min and `static-windows`
   12 min (`visual-2` 11.9 min and `static-windows` 7 min in run 45893802335), so splitting the
   visual jobs alone would not surely shorten a run.

6. The owner's instruction (2026-11-27), verbatim: "Fait ce qu'il faut pour merger ce qui reste
   rapidement et on clos le batch vite. On fera les teste visuels lourd dans un second batch". Whether
   this CR leaves batch-09 is being confirmed (close-Q1); it is not added to the batch meanwhile.

7. The owner's instruction (2026-11-27), verbatim: "Il faut rebase. Après en P1 tu mets une CR sur
   un plan d'optimisation des check locau et CI. Parallisarion, test lourd que après merge ou
   optionnellelenr sur les PR". Applied by the Chief of Staff: this CR leaves batch-09 for the
   backlog P1, next to that plan (`local-dev-ci-judges`). Its specification's place (a stack above
   CR-517, below CR-518) is to be read again against `main` when it is taken.

Spec critic: yes (it changes which jobs gate a release tag, in several files that must agree).

Critic, 2026-11-27: 4 findings; 4 applied as fixes (the job-name commands of the release and
contributing guides, the `ci-stress` signature in two documents, a "What CR-519 then adapts" list,
the unproved matrix-result claim now to be proved), 0 asked.

Destination: running batch batch-09.
