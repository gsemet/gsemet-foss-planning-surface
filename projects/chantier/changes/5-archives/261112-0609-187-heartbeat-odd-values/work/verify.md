# Verify CR-187 at head 0314e283

Verdict: VERIFIED.

Evidence is the Driver's scenario transcript (scenario/results/github-20261112-003842.md, 578/578, gitlab 578/578 too), the diff read in full, and the PR state. I did not build a separate scratch batch: `open` needs prepared CRs and a fake forge, which the scenario's direct_batch (batch-34) already does at epoch 1.

Plan items, from the transcript (batch-34, direct, epoch 1):
1. Fresh batch: `heartbeat never`. First wake: `heartbeat 0 min`, no gap, one `heartbeat` event. OK.
2. heartbeat set 45 min back: `status` prints `45 min`. `status --refresh` (no epoch): batch.json heartbeat unchanged, prints 45, still one event. OK.
3. `--refresh --epoch 1`: `heartbeat 0 min (45 min since the last)`, event count 2, next `status` `0 min`. OK.
4. Stop with `--epoch 2`: exit 3, batch.json byte-identical. With `--epoch 1`: exit 0, `status` prints `heartbeat stopped`, one `heartbeat_stopped` event, STATUS.json carries the mark. A no-epoch refresh leaves it. OK.
5. Next wake clears the mark: `0 min (0 min since the last)`. OK.
6. `pause` sets the mark (paused batches print `heartbeat stopped`); `open` writes `heartbeat_stopped: None` (never). OK.
7. `lost_messages` check passes, adapted for the gap (`0 min (0 min since the last)`).
8. PR 123: draft, open, base main, first line exact, head = 0314e283, CI green (check x3, scenario). Main checkout is on main.

Code read: `_stop_heartbeat` checks the epoch under the Batch lock, refuses a missing epoch, logs one event. `_refresh` reads `prev` before overwriting and clears the mark. `status` reads old batches with `.get`. board.py and STATUS.json carry the mark. `--help` texts updated.

Cards and docs against spec sections 3 and 4: the single `--epoch` rule (wake and steering commands carry it, the pre-report refresh does not), the heartbeat sentence, and the recorded stop appear in chief-of-staff.md, foreman.md, hosts/claude-code.md, hosts/copilot.md, status-layout.md, README.md, use-cases-direct.md and cr-lifecycle-texts.md. agents/ untouched. OK.

Not shown, marked as such: the real `/loop` and `ScheduleWakeup stop: true` behaviour and a session following the card (only the CLI form and the card text). Also not shown by me: that the new checks fail on main (the spec's "failing on main" item); by reading, the stop form and the wake gap do not exist on main. The no-epoch check is a regression guard, as the investigation said.

Minor, not blocking: the added sentence in docs/use-cases-direct.md is a long line; chief-of-staff.md line 435 and 523 exceed the wrap width.

## Description pass at head 0314e283 (PR 123 body vs diff, verify.md, pr-template.md)

Verdict: NOT VERIFIED (one template fix).

Checked OK: eval first line, head SHA 0314e28 on every proof, 578/578 matches the transcript, files named in Changes exist in the diff (commands.py, status.py, board.py, cli.py, cards, docs, scenario), table rows match the scenario checks, blast radius one grade, real /loop marked UNVERIFIED, layout and fold in order, Internal references last.

Fix:
1. Agent role named outside Internal references: Human decisions says "as in Foreman mode" and Changes says "(Foreman, Claude Code and Copilot hosts)". Reword without the role, e.g. "as in a batch run by a separate steering agent" and "(the batch-steering card and both host cards)". Minor: Summary's "the cards" could read "the agent instructions".

## Description pass 2 at head 0314e283 (posted body re-read)

Verdict: VERIFIED.

Previous defect gone: no role name (Foreman, Driver, Chief of Staff, Inspector) appears outside Internal references; Human decisions says "a batch run by a separate steering agent", Changes says "the batch-steering card and both host cards", Summary says "the agent instructions". Head 0314e283 matches the PR's headRefOid. Nothing else changed: Summary, Deliverables table, Blast radius, Autonomous decisions, fold, Test plan SHAs (0314e28) and the UNVERIFIED /loop mark are as in the first pass, which matched the diff and the transcript.
