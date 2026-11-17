# 028 — Known issues K1 (overflow) and K3 (Mermaid error duplication)

Backlog intent copied to `00-intent-backlog.md` (P1/known-issues-k1-k3-k4, now empty and removed).

## Decisions (user, 2026-10-22)

1. Scope: K1 and K3 together in one PR.
2. Mermaid error: keep the generic message and add a collapsible `<details>` with the Mermaid
   parser's message (line, expected token). Exactly one error element per diagram whatever the
   number of re-renders (theme switch, content replaced).
3. `knownIssue`: remove `P9-B4-K3` from diagrams/v08, v09; on rendering-core/v17, v18 keep only
   `P9-B4-K2` (RTL, P3). Per-assertion `knownIssue` is out of scope (stays in P2 e2e-campaign-rest).
