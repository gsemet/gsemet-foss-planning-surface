# Progress report: batch-30 (2026-11-22)

**batch-30, stack batch, Foreman mode: 36 CRs merged, 2 joining (a flaky-test fix, then the
release v0.15.0).**

| | |
| --- | --- |
| Merged | 36 PRs, in stacks merged in one go on the forge |
| Spend | $293.07 over 12,026 model calls |
| Foreman | $34.21 (12%) |
| Drivers | cr-driver $80.44 (27%), stack-driver $10.31 (3%) |
| Workers | coder $104.27 (35%), verifier $25.26 (9%), inspector $17.08 (6%), conflict-resolver $8.00 (3%), others $8.04 |
| Orchestration (steering + Drivers) | 44% of the spend |

What the batch shipped, in the user's words: the web board as the place to steer (Inbox,
History, Dashboard, Help, the batch graph and Kanban, the Griller's panel), CLI commands run
remotely through the surface server with a private and a public read-only key (`serve`,
`webui`, `login`), and stack batches that keep their shape.

Eval before the release: real-foreman run 4 (2026-11-22), five CRs merged in one native stack
merge, $9.88 of a $20 budget, about 54 minutes, passed with findings (audit 464/473, judge 6/6).
