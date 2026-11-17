# 029 — E2E campaign B5: visual scenarios for extension states

From backlog P2/e2e-campaign-rest (copy in `00-intent-backlog.md`). Plan: P9 `plan.md` section 6
"B5" and section 0 (safety rules), in archives/021-feature-session-007-020/p9-e2e/.

## Decisions (user, 2026-10-22)

1. The P2 item is split into 4 CRs, one PR each, in this order: B5 (this CR) → T1 → T2 → F.
2. High contrast is removed from B5 (no HC scenarios, no HC theme in the harness).
3. For T1/T2/F (not this CR): the real-window tests must be runnable locally at least at the end of
   the development, and several runs may happen in parallel (isolation required).
4. T1 restarts from the plan on current main, using the parked patch only as a reference.
