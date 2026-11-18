# batch-27: Completion report

Parallel batch, 4 slots, $60 budget, steered by a Foreman. Seven CRs, all merged, none dropped.

| CR | What it delivers | PR | State |
| --- | --- | --- | --- |
| CR-359 | The partial-stack ask says whether the local gate ran at the mergeable top | 324 | ✅ merged |
| CR-360 | `work/gates/` ignored at any depth of the planning folder | 325 | ✅ merged |
| CR-361 | The summary lint hint gives a path `summary set` can read | 327 | ✅ merged |
| CR-362 | A document's front matter is never a CR's title, and the panel hides it | 326 | ✅ merged |
| CR-363 | A session whose chantier CLI cannot run stops at once | 328 | ✅ merged |
| CR-364 | A CR's archive stays out of the PR unless the project says yes | 330 | ✅ merged |
| CR-365 | In a batch with no stack, the batch's top runs the local gate | 329 | ✅ merged |

| Cost | USD |
| --- | --- |
| Total | 15.21 of 60 |
| Foreman | 4.14 (27%) |
| Drivers | 6.46 (43%) |
| Workers | 4.61 (30%) |

- Local Windows `just scenario` (`chantier gate`): passed at the batch's top, CR-364, 7a6f279.
- The forge hub saw every merge: `chantier watch` printed `forge saw merged: CR-364 ... order
  merged CR-364` and woke the idle Chief of Staff about 27 s after the merge.
- Retro: nothing worth changing (4 points dropped by the critic).
