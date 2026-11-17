# Report — 040-e2e-t1-real-window-registry

Status: **done** (2026-10-23, PR #32, merge commit ebe7b2b). Merged without waiting for CI (user
decision), follow-up CR 041 (ci-stability).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | 040 — e2e-t1-real-window-registry (coder reports in `reports/`) | PR #32, ebe7b2b |

## Proof of completion

- Last green CI run recorded in the CR header: all pass (STATE); latest branch run 39924099308.
- Reviews: T1-r1.md: Verdict: APPROVE.
- Details of tests, gate counts and screenshots: `reports/` and `reviews/`.
- Note: merged without waiting for CI (user decision); CI instability handled by follow-up CR 041.

## Open items

- None from this CR; CI follow-up in CR 041.

## Orchestration notes

# Night notes (main session)

- 22:55 orchestrator #3 started; drivers 025, 029, 031, 032 live.
- 23:15 finding: a background orchestrator with live background drivers stays dormant until a
  driver returns: its own background `sleep 270` tick and the main session's messages do not wake
  it (status file frozen at 22:55, message at 23:10 unanswered). Drivers keep working. Consequence
  for the guideline (to propose to the user): the tick does not work for a sub-agent with live
  children; supervision must rely on driver headers, and landing/refill happens on driver return.
- Main session watcher (driver headers, refill of the 4 slots, WINDOW-TESTS.lock, interactive
  rm/cp/mv) replaces the orchestrator-status check tonight.
- 23:40 root cause (likely): the orchestrator's parallel driver Agent calls block it until ALL
  drivers of the batch return, so it cannot tick, read messages or refill a free slot. Tonight it
  works in batches of 4 (025/029/031/032, then 033–036, then 037–040). Fix to propose: drivers as
  "lanes" (a driver that finishes claims the next pending CR via the STATE.md driver lock), or the
  orchestrator started per batch by the main session.
- 04:30 a driver header stays unchanged while its coder runs (foreground sub-agent, 25+ min for a feature round): the 15-min stuck rule fires falsely; the coder's worktree activity is the real signal. Watcher threshold raised to 60 min.
