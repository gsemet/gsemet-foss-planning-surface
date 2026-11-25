Short name: `heavy-ci`

1. heavy-ci-Q1 (2026-11-25, night; the Chief of Staff asked "J'ajoute au batch une demande pour réparer la CI lourde rouge ?"): **Add it to the batch.** User: "Oui, ajoute-la".
2. heavy-ci-Q2 (2026-11-25, decided by the Chief of Staff, owner's word for this batch: "tu me poses pas de question"): **Fix the cause.** Raising `STUDIO_LAUNCH_TIMEOUT_MS` alone, skipping or quarantining tests, or retrying until green is not a fix. If the diagnosis shows the suite is too long for one launch, split it into launches or shards, each within its deadline, and state the measured durations before and after. Every test that runs today still runs.
3. heavy-ci-Q3 (Chief of Staff): **Proof.** The heavy run (`gh workflow run ci.yml --ref <branch> -f heavy=true`) is green at the pull request's head, twice in a row on the same head. A failure that cannot be fixed within the CR is named in Known gaps with its evidence, never hidden.
4. heavy-ci-Q4 (Chief of Staff): **Place in the stack.** As low as the stack driver can put it once ready, so that `main` turns green early; it waits for no other CR.

Spec critic: no, it changes CI and tests only; a product change found by the diagnosis would reopen this.

Destination: running batch batch-09.

Owner's overnight grant (2026-11-25, near midnight, the owner to the Chief of Staff: "je vais aller au lit. tu as toute latitude pour finaliser la stack cette nuit: tu peux passer les contexts a 300K des driver, faire 10 rework max"): the Chief of Staff decides alone to get the stack finished tonight; a CR may take up to 10 rounds; a Driver or stack driver hands back for context only at 300,000 tokens.

Fact added by the Chief of Staff (2026-11-25, after the filing): the push run 45713440510 on `main` at 17b779d is green on every job (integration and stress included). Its `just ci-integration` step ran 1002 s (22:28:36Z to 22:45:18Z), all launches together; the trusted-suite launch deadline is 900 s. So `main` is green at 17b779d, and the failure is intermittent or close to the deadline (not verified). The CR stays: the heavy run is not reliable.
