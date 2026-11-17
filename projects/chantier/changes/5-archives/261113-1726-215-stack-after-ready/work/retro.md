# Retro

## 2026-11-13: batch-16 (CR-214 to CR-220)

- Drivers ended at about 90k tokens: CR-216 handed back `context:`, CR-215 ended silently with no hand-back: make the Driver hand back `context:` well before its limit, every time, and keep a round's worker reports out of the Driver's context.
- The cr-driver agent has no Edit tool, so the CR-215 Driver rewrote the PR body with Write: give the Driver a narrow way to edit its own work files, or state in the card that Write is the route.
- CR-217's long-gate lock outlived its merged CR (dead pid), so CR-216 waited about 40 minutes and was refused: the gate lock is released when its pid is dead or its CR merged (CR-219's queue to be checked against this).
- CR-220 showed 48 minutes with no activity while its gate was queued, not running, and the ping got a pong: the activity line shows a queued gate as such, so the lost-Driver check skips it.
- The user merged each PR on its own, so the stack driver and `forge-stack` never ran and the Foreman sent rebase notes instead: the Chief of Staff states at the go whether a stack batch merges as one stack or PR by PR, and the Foreman runs that path.
- CR-218's round-2 Coder was the resumed round-1 Coder, not a fresh one: the Driver card says a new round starts a new Coder.
- CR-219's refusal proof omits its command, and its Inspector verdict came as prose rather than JSON: the Driver refuses a proof without its command and an Inspector verdict that is not JSON.
- CR-220's push hit a GitHub 500 and was retried once: keep one retry on a forge 5xx in the Driver card.
- A conflict resolution in CR-220 left a UTF-8 BOM, caught by `just check` in round 2: the conflict-resolver writes files without a BOM and runs `just check` before handing back.
- CR-214 detects gh-stack by its folder, not `gh extension list` as its spec says, and reports P10 on the user's settings as 14 of 16 (was 19 of 19): a follow-up CR aligns the detection with the spec and explains the count.
- CR-215 hands back three gaps (rebuild exits 2 not 4 after 5 unstack tries, the batch-15 base case not reproduced on the old code, the stale-SHA regex matches all-digit tokens), and its Inspector was not re-run after three rebases: a follow-up CR for the exit code; the Driver re-runs the Inspector after any rebase that resolves a conflict.
- CR-215 merged while its Driver was still finishing (`gh pr ready`, body edit), so its `ready` hand-back was refused: the Chief of Staff waits for the ready line before merging, or the CLI accepts a late hand-back on a merged CR as a note.
- Unverified live: CR-216's early `context:` hand-back and shell guard, CR-218's `--plugin-dir` route, CR-220's posting routes; `evals/kit/setup.py` lacks CR-220's campaign: the next real eval covers these, and a follow-up CR adds the campaign to the kit.
