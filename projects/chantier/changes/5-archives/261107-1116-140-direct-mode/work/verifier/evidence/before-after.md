# Before / after - CR-140 direct mode

Base: origin/main 337e467 (detached worktree, removed). After: pushed head f83b3ab.
Throw-away repo outside the project's `.agents`, in the session scratchpad (`fx/proj`), env:
CLAUDE_CODE_ENTRYPOINT=cli, CLAUDE_CODE_SESSION_ID=uuid-chief, CHANTIER_CLAUDE_PROJECTS=fx/projects,
fixture transcripts (model claude-sonnet-5-5, 1000 input tokens + N output tokens per call) with
timestamps before the claim (-2 h), inside the steering window, and after the next epoch's claim, plus
a Driver under `uuid-chief/subagents/`. Each pair is reproducible by re-running the listed command
with the env above against the same fixture.

| # | Command | Before (origin/main) | After (f83b3ab) | File |
|---|---------|----------------------|-----------------|------|
| 1 | `preflight --direct` | `unrecognized arguments: --direct`, exit 2 | P1 ok on `cli` entry point, own-check line "P3, P9 ..." (P2 left out), exit 0; without `--direct` P1 FAIL as before | before-origin-main.txt / after-1-open-claim.txt |
| 2 | `open --direct` | `unrecognized arguments: --direct`, exit 2 | `opened batch-01 ... steering direct`, `next: ... then steer it yourself` | same |
| 3 | `foreman set/transcript uuid-chief --epoch 1`, then `status`, `brief.md`, `STATUS.md` | no steering field | status line 1 `steering direct`; brief.md `Steering: direct.`; STATUS.md `steering direct` | after-2-cost.txt, after-2b-STATUS-md.txt, after-2c-brief-md.txt |
| 4 | `cost`, `cost --summary` (chief calls: 100k out before, 200k out inside, Driver 100k out inside) | n/a | one `Chief of Staff (steering)` row $2.002; Driver $1.002; Total $3.004 (= sum, nothing twice); "Chief of Staff" line: $0.00 since opened, $1.00 whole session (the pre-claim call only) | after-2-cost.txt |
| 5 | `order add --note <valid CR>`, `order qa --note ...` on direct batch | n/a (no direct batch) | both exit 2 "a direct batch is strict: switch to Foreman mode to add work" | after-4-orders.txt |
| 6 | `close` with the Chief's own transcript written seconds ago | n/a | not listed among causes; control: a fresh Driver file and an open order are listed and refuse; once the Driver file is old and the order done, `land` then `close` price and `close --yes` closes | after-4b-close.txt |
| 7 | `foreman set uuid-foreman --epoch 2` + `foreman transcript uuid-foreman --epoch 2` | n/a | batch.json `"steering": "foreman"`, events.jsonl `kind: steering`; status line 1 `steering foreman`; `status --refresh --epoch 1` exit 3 "stale Foreman"; `status --refresh --epoch 2` ok; `order add` now accepted | after-3-switch.txt, after-3b-switch-orders-log.txt |
| 8 | cost after the switch | n/a | Foreman $3.002 + Chief of Staff (steering) $2.002 = $5.004; the Chief's post-switch call ($7) is only in the "Chief of Staff" line ($7.00 since opened) | after-3-switch.txt |

Not captured / limits:
- A Copilot direct run is UNPROVED: no Copilot session was available; the Copilot cost path
  (`copilot_session_costs`) has no timestamps and prices the whole session, so the steering-window
  split was not exercised there.
- No real Claude Code Driver or heartbeat; transcripts are synthetic fixtures.
- The structure tests (pytest) were not run by the Verifier (module name clash running from the
  cli folder); `just check` / `just scenario` are the Coder's and CI's claims, not proof here.
