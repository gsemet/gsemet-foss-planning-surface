# 040 — e2e-t1-real-window-registry

From backlog `P2/e2e-campaign-rest` (files copied here as `backlog-*` / images).

## Problem

P9 T1: real-window captures are written ad hoc by each suite; no registry, duplicates, inconsistent names.

## Decisions (user grill, 2026-10-22 night plan)

1. Follow plan.md section 6 "T1" (archives/021-feature-session-007-020/p9-e2e/plan.md) restarted on current main; the parked patch (archives/021-.../p9-e2e/parked/T1-wip.patch) is a reference only, never applied as is.
2. Decision: T1 includes run isolation so several real-window runs can run in parallel: unique user-data dir, extensions dir, CDP port, evidence folder and run id per run. Prove it by running two suites at the same time once (respect the WINDOW-TESTS lock otherwise; the proof run holds the lock for both).
3. Keep LATEST pointers, INDEX.md, manifest fields and run folder prefixes as the plan requires; README images compared with --check.

Night rules: blocked on a real product decision → apply the driver's recommendation and list it in the PR under "Décisions prises en autonomie" (Autonomous decisions).
