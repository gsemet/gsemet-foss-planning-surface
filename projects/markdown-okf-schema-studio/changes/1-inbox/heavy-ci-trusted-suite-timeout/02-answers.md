Short name: `heavy-ci`

1. heavy-ci-Q1 (2026-11-25, night; the Chief of Staff asked "J'ajoute au batch une demande pour réparer la CI lourde rouge ?"): **Add it to the batch.** User: "Oui, ajoute-la".
2. heavy-ci-Q2 (2026-11-25, decided by the Chief of Staff, owner's word for this batch: "tu me poses pas de question"): **Fix the cause.** Raising `STUDIO_LAUNCH_TIMEOUT_MS` alone, skipping or quarantining tests, or retrying until green is not a fix. If the diagnosis shows the suite is too long for one launch, split it into launches or shards, each within its deadline, and state the measured durations before and after. Every test that runs today still runs.
3. heavy-ci-Q3 (Chief of Staff): **Proof.** The heavy run (`gh workflow run ci.yml --ref <branch> -f heavy=true`) is green at the pull request's head, twice in a row on the same head. A failure that cannot be fixed within the CR is named in Known gaps with its evidence, never hidden.
4. heavy-ci-Q4 (Chief of Staff): **Place in the stack.** As low as the stack driver can put it once ready, so that `main` turns green early; it waits for no other CR.

Spec critic: no, it changes CI and tests only; a product change found by the diagnosis would reopen this.

Destination: running batch batch-09.
