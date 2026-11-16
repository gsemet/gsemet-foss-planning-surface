The gate lock and the activity line tell the truth

From batch-16's retro (points 3 and 4), reviewed by an advisor.

- Point 3: CR-217's long-gate lock outlived its merged CR (dead pid), so CR-216 waited about 40 minutes
  and was refused. After a dead gate, the next one waits up to an hour on the suite's process whatever
  the CR's status (commands.py around 2188-2198). `cancel` already stops a CR's suite (around 2560);
  `order merged` (rails.py around 266) does not. Fix: `merged` does the same. Also check the liveness
  test against Windows pid reuse.
- Point 4: CR-220 showed 48 minutes with no activity while its gate was queued, not running, and the
  ping got a pong. `activity` prints `gate running` only for the lock holder (commands.py around
  1423-1429) and ignores CR-219's tickets in `.long-gate.queue/`. Fix: print `gate queued behind <cr>`,
  and the lost-Driver check of foreman.md (around 278-279) skips it like `gate running`.
- Lands: CLI, one line in foreman.md. `just scenario` applies.