# Answers

- 2026-11-26, the owner, on the next release: "Après les 3 restantes (Recommandé)" (add the release to the batch once CR-505, CR-507 and PR 529 are merged).
- 2026-11-26, the owner: "Oui, avec les 4 (Recommandé)" (the release ships the four anomaly fixes; the acceptance follow-ups do not delay it).
- 2026-11-26, the owner, batch09-Q1: "A. Suite au batch suivant (Recommandé)".
- 2026-11-27, the owner (Chief of Staff session), verbatim: "Monitor juste la pipeline main et fix si
  nécessaire. Prépare une release". Applied: this CR joins batch-09 as its release CR, the earlier
  condition (CR-505, CR-507 and PR 529 merged) being met.
- 2026-11-27, asked: release113-Q1 "version 1.13.0?" (recommended: yes) and release113-Q2 "a docs
  diagram in the release notes?" (recommended: no). No answer yet.

Short name: `release113`

- 2026-11-27: `order add --release` to batch-09 was refused, exact text: "order add --release: CR-478
  is already the release CR of batch-09; a batch has one. Put the second release in the next batch,
  once this one is closed".

- 2026-11-27, the owner (Chief of Staff session), verbatim: "Met le CR de release en ready pour le
  prochain batch. En attendant monitor bien la CI et assure toi que tout soit vert pour la release (CI
  lourd). Fox dans une nouvelle CR si nécessaire dans ce batch". Applied: this CR stays in 3-ready for
  the next batch; batch-09 stays open until the heavy CI of `main` is green, and a fix it needs is a
  new CR in batch-09.

Destination: next batch (3-ready), as its release CR.

Spec critic: no (the project's procedure rules; the specification only fixes the scope, the version
and the notes' options).

- 2026-11-27, close-Q2 (Chief of Staff session): "do I close batch-09?", choices "A. yes (recommended)", "B. not yet". Answer, verbatim: "Ok pour Q6. Laisse le batch en pause si un fix est nécessaire pour la ci lourde". Applied: batch-09 is not closed and stays paused, so a fix the heavy CI needs can join it. State at the answer: the heavy run 45958381383 on b1e23cc, the head of `main`, is green.

- 2026-11-27, close-Q3 (Chief of Staff session): "the heavy CI is green: do I close batch-09?", choices "A. yes, close (recommended)", "B. no, keep it paused". Answer, verbatim: "Oui". Applied: `close --yes`.
