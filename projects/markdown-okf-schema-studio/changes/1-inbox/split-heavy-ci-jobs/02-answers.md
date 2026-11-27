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

Spec critic: yes (it changes which jobs gate a release tag, in several files that must agree).

Destination: running batch batch-09.
