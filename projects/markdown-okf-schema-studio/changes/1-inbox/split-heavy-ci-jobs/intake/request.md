# The heavy CI finishes faster: its two long jobs run split in parallel

# The heavy CI finishes faster: its two long jobs run split in parallel

Split the long jobs of the heavy CI so that a heavy run finishes much sooner.

The owner's words (2026-11-27, Chief of Staff session of batch-09), verbatim:

"Oui découpe la CI maintenant juste après celle que tu fini il faut pouvoir aller vite."

Said after the measures below and the Chief of Staff's remark that the heavy CI could be shortened by
splitting its two long jobs.

## Measured (runs 45893802335 and 45838037906 of `main`)

- Whole heavy run: about 20 min. `integration`: 18.2 to 18.8 min. `stress`: 16.1 to 16.3 min.
- Next longest: `visual-2` 11.9 min and `visual` 7.6 min; `acceptance (trust-security)` 1.5 min.
- Inside `integration` (run 45893802335), launches in sequence: compile and bundle about 20 s,
  `scroll-sync-suite` 124 s, `trusted-suite` part 1/2 about 7 min, part 2/2 about 8.2 min, the other
  suites a few seconds each.
- Inside `stress`: one trusted launch of about 15 min (11 rounds x 21 scenarios, capped at the
  24-minute launch deadline), then `untrusted-suite` 24 s.

## Place

batch-09, right after CR-517 `perf-547-comment-update-and-author` and before CR-518
`perf-kpi-real-window-tests`, which adds a heavy job to the same workflow.
