# Flaky real-window paste-url and drop-files tests

See intake/request.md.

## Grill, 2026-11-21 (owner's answers, asked by the Chief of Staff)

- pu-Q1 (if the cause is not found). Owner: "Même règle que t45": ship what is proved plus traces in the CI log; no automatic retry, no quarantine. Both scenarios join the default `just ci-stress` scenarios (as the request says).
- Owner, 2026-11-21: "Et tout ça partira dans le batch en cours": once final and ready, added to the running batch-07.

## Owner's answers, 2026-11-21

- pu-Q2 (stress time budget, asked with flaky-realinput-t45). Owner: "t45 à la demande, 11 tours": 11 default rounds for the 21 default scenarios; every guard holds unchanged.
- Settled by the Chief of Staff from the Fable critic (not behaviour): the two fixed pauses are replaced now (pasteUrl.test.ts:104-115 click-retry loop → setEditMode, one click, waitForEditor as editKeys/saveKey do; dropFiles.test.ts:107 → waitFor on the drop marker), consistent with CI rule 12 and the owner's "no fixed waits" on the sibling CR-452; only these two of the 126 pauses. No product trace in reportStaleEdit (as decided for CR-425). A red proof run with no cause: already answered by pu-Q1 (both still join, trace in the PR, follow-up filed; a high measured rate comes back as a blocked handback). Option (c) on the budget dropped.
