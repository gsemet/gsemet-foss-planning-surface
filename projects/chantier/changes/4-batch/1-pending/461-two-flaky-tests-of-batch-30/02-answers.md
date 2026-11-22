# Answers

1. Q: When? User, 2026-11-22: P1, next batch; then, the release needing a green `main`:
   "Corriger puis release". It joins batch-30 below the release CR.

## Settled by the Chief of Staff (2026-11-22)
- Diagnosis of `[only-two]` (read in the code, to be proved by the Driver): in
  `commands/live.py`, `once()` reads `_missing(models)` under the lock, then checks `failed`
  without it. The last reader thread feeds its first item and `_check_only` raises inside the
  lock, but `failed.append` runs after the lock is released. The main loop can see nothing
  missing and no failure, print the screen and exit 0. The fix makes the `--only` refusal
  deterministic once every board has answered (for instance `_check_only(models)` again under
  the lock after the loop), with no sleep and no retry in the test.
- `test_w2_...`: find the cause (timing, port reuse, file lock) and fix it the same way; if it
  cannot be proved within the CR's rounds, hand back with the evidence and leave it named in
  Known gaps rather than hide it.
