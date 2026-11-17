# QA skill: harden the no-op sweep

Low · Code review · from the QA Drivers change (#237) · P3

| Point | Detail |
| --- | --- |
| Untested path | `scripts/noop-sweep.mjs`: the `goBack()` / abort path has never run in a live window. |
| Fragile read | One failed doc-id read aborts the whole sweep. Re-read once after about 250 ms before giving up. |

**Done when.** The abort path ran once in a real window during a campaign, and a single failed read no longer
stops the sweep.
