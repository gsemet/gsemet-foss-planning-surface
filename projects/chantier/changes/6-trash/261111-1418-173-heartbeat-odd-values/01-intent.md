# Intent: the heartbeat says something true in direct mode

- **The defect** (batch-09, 2026-11-10): in direct mode, `status --refresh --epoch 1` printed
  values that were not true:
  - "heartbeat 170 min" right after the steering session had refreshed;
  - "heartbeat 0 min" at other times;
  - 439 min while the loop was stopped (2026-11-11).
- **The fix** (`02-answers.md`): in direct mode, "heartbeat N min" is the minutes since the
  steering session's last `status --refresh --epoch`, the same meaning as in Foreman mode. The
  Investigator first finds where the odd values came from.
- **Runs in the next `real` eval:** the PR opens as a draft, and nobody merges it.
