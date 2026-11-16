# CR-136 before and after

Text output is the form: this CR has no UI beyond the status text. Base 6f79dd3 (detached worktree, removed) against head b7e3517, same probe (`probe.py`) in a throwaway repository with the scenario's fake forge. Raw files: `evidence/before-base.txt`, `evidence/after-head.txt`. The label is the same string in the batch `STATUS.md` and `STATUS.json`, the index, and the CR's own pair (`ONE STRING EVERYWHERE : True` on every state).

| State | Before (base) | After (head) | `take` says |
| --- | --- | --- | --- |
| queued, free slot, no waits | 🟡 queued | ⚪ queued | (starts) |
| queued, working CR + open QA order hold all slots | 🟡 queued | 🟠 queued | no free slot for CR-102: 2 of 2 held (CR-101 working, O-1 qa) |
| queued, `order done` frees the slot | 🟡 queued | ⚪ queued | |
| queued, slots 1 held by a working CR | 🟡 queued | 🟠 queued | no free slot: 1 of 1 held |
| queued with waits | 🟡 queued, waits for CR-102 queued | 🟠 queued, waits for CR-102 queued | waits for CR-102 queued |
| queued, spent budget | 🟡 queued | 🟠 queued (Now: "Waiting for the budget.") | budget spent: $2.00 of $1.0 (exit 5) |
| queued, budget raised | 🟡 queued | ⚪ queued | |
| queued release behind other CRs | 🟡 queued, waits for CR-105 queued | 🟠 same | waits for CR-105 queued |
| queued release, user's word pending | 🟡 queued, waits for the user's confirmation | 🟠 same | needs the user's confirmation |
| queued release with a pending fix | 🟡 queued (no waits shown) | 🟠 queued, waits for CR-108 queued, CR-109 queued | waits for CR-108, CR-109 |
| release, fixes ended | 🟡 queued | ⚪ queued | |
| working | 🟡 working Round 1/3 | 🟡 working Round 1/3 | |
| blocked `waits: the stack driver` | 🔴 blocked Blocked 1/3 | 🟠 blocked Waits 1/3 (severity red; Next: "Waits for the stack driver; the Foreman takes it back when that lands.") | |
| blocked `question:` | 🔴 blocked Question 1/3 | 🔴 blocked Question 1/3 | |
| ready | 🟢 ready Notify 1/3 | 🔵 ready Notify 1/3 | |
| merged | 🟢 merged | ✅ merged | |
| dropped | ⚪ dropped | ⚪ dropped | |

The board prints `label` unchanged: `claude plugin test .` runs a test that draws each of these labels (22 pass, 0 fail). The board in a real pane is not shown by tests and was not seen.
