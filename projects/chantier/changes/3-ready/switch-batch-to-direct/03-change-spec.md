# Change Specification: switch a Foreman batch to direct mode, with CRs in flight

Short name: `direct-switch`. Answers: `02-answers.md` (direct-switch-Q1 to Q12, and the points
settled by the Chief of Staff).

## Goal

On the user's word ("passe le batch en direct", "switch the batch to direct mode"), the Chief of
Staff takes over a running or paused Foreman batch and steers it itself, whether its Foreman is
alive or not. Nothing in flight is lost: queued CRs stay queued, each CR whose Driver the switch
stopped restarts by the existing restart path, and the PRs, branches and worktrees are kept. Two
Drivers never hold one CR. Afterwards `status`, `STATUS.md`, `cost` and the board say "direct"; the
old Foreman's and its Drivers' calls stay counted; a replaced Foreman never blocks `close`. A batch
switched to direct can go back to Foreman mode by the existing switch, unchanged, and back again.

The case behind it: Studio's batch-06, whose Foreman stopped at the usage limit (heartbeat 9 hours
old) with 5 CRs in flight and 4 PRs open; today the Chief of Staff can neither take over nor close
without dropping the work, because "a Foreman batch never becomes direct".

## Decisions carried from the grill

1. **Q1, the command.** No new command and no flag. The Chief of Staff's own claim of the next
   Foreman number on a Foreman batch makes it direct: `$CHANTIER foreman set <its session id>
   --epoch <n+1>`, then `$CHANTIER foreman transcript <its transcript id> --epoch <n+1>`. The flip
   happens in `foreman transcript`, mirroring today's direct-to-Foreman flip in the same function,
   logs a `steering` event `direct` in the batch's journal (`events.jsonl`), and is said in the
   command's output. The old number becomes stale (exit 3), as any later claim makes it today.
   **How the CLI knows the claimer is the Chief of Staff** (left to this specification, from what
   the record already holds): the claimed transcript equals the batch record's `chief_transcript`.
   That field is what today's opposite flip already compares against (`seat.py`, `_transcript`:
   `args.value != b.record.chief_transcript`); `open` writes it from the opening session's own
   transcript (`opening_record.new_record`, `chief=`), and `seat take` refreshes it on every
   non-closed batch when the seat moves (`seat._record_transcript` / `_set_chief`). The seat's
   session id (`seat.json`) is not used: the batch record does not hold it, and the comparison
   stays on the same key as the existing flip.
2. **Q2, a Foreman that is not answering.** Its heartbeat is late by the board's test
   (`board/web/js/model/semantics.js`, `heartbeat()`, lines 217-227: the minutes since the last
   heartbeat exceed the batch's steering wake plus `HEARTBEAT_MARGIN_MIN`, 5 minutes; the steering
   wake is the `steering wake` of `$CHANTIER playbook`'s `timing:` line, and `status --refresh`
   prints `heartbeat N min`) **and** one `ping` gets no `pong` within 5 minutes. The user's word
   alone is enough, with no wait.
3. **Q3, who stops a live Foreman's Drivers.** The Foreman itself: it notes each CR
   (`switch to direct mode: Driver stopped; the Chief of Staff restarts it`), stops each of its
   Drivers by the host's stop, answers that it is done, and stops. Stopping the Foreman's session
   from outside stays the path for a Foreman that is not answering.
4. **Q4, back to Foreman mode.** Yes, through the existing switch to Foreman mode, unchanged. The
   rule "a Foreman batch never becomes direct" goes away.
5. **Q6, a Foreman that ended its heartbeat on purpose.** If it then does not answer a ping, the
   time it ended its heartbeat counts as its last heartbeat for Q2's test. That time is read from
   `heartbeat_stopped` (in `batch.json`, and in `STATUS.json` / the board's state, which copy it);
   `status --stop-heartbeat` sets it, and `pause` sets the same field (`commands/closing.py`), so on
   a paused batch it is the pause's time.
6. **Q7, a Foreman that answers the ping but never confirms the hand-over.** The Chief of Staff
   waits; only the user's word moves it to the "not answering" path. No timer of its own.
7. **Q8, the board's cost receipt after a switch.** `cost/sessions.chief_outside` (which leaves
   out the Chief of Staff's steering outside its claim window on a direct batch) is left as today
   in this CR; a separate small CR is filed for it.
8. **Q9, the round-trip fix** (section 2 below) is kept in this CR.
9. **Q10, knowing an old Driver has ended** (after a Foreman stopped from outside). Before
   restarting each CR, the Chief of Staff reads its old Driver's transcript ending with `close`'s
   check (`$CHANTIER close --batch <batch>`, no `--yes`: it lists each held agent's state, from
   `rails.running` / `transcript_endings`); it restarts only the CRs whose old Driver is shown
   ended, and asks the user about any shown running. The cards do not claim that stopping a
   session ends its Agent children.
10. **Q11, the batch records another Chief of Staff transcript.** Before anything is stopped, the
    Chief of Staff compares its own session's transcript with the batch record's
    `chief_transcript`; if they differ it runs `$CHANTIER seat take <its session id>` and checks
    again; if they still differ it stops and tells the user.
11. **Q12, Remote Control with a silent Foreman.** The Chief of Staff says the stop needs the
    machine (stopping a session from the phone is unproved), names the session and waits. The
    live-Foreman path stays available under Remote Control.
12. **Settled by the Chief of Staff: stopping another session.** On the Claude Desktop host the
    Chief of Staff can stop another session (the session management's stop tool,
    `mcp__ccd_session_mgmt__stop_session`): a Foreman that is not answering is stopped by the user,
    or by the Chief of Staff on the user's yes. The tool is not named in the repository yet; this
    CR adds it to the host reference.
13. **Settled by the Chief of Staff.** The repository keeps no changelog (release notes are written
    at release time, `docs/release-process.md`): this CR edits none. The PR is a draft until CI is
    green; the user merges it by rebase.

## What changes

### 1. The CLI: `foreman transcript` flips Foreman to direct

File: `skills/chantier/scripts/cli/src/chantier/commands/seat.py`, function `_transcript`.

- Keep the existing flip (`steering == "direct"`, a `chief_transcript` recorded, the claimed
  transcript differs from it: steering becomes `foreman`, event `steering` with
  `steering="foreman"`).
- Add its mirror: when `b.record.steering == "foreman"`, `b.record.chief_transcript` is set, and
  the claimed transcript (`args.value`) equals it, set `b.record.steering = "direct"` and log
  `b.log("steering", None, steering="direct", transcript=args.value)`, before the existing
  `foreman-transcript` event, as the existing flip does.
- The output says the switch: besides `transcript <uuid>`, one more line, for example
  `steering direct: the Chief of Staff steers <batch> as Foreman n°<n>` (the exact words are the
  Driver's; they never contain the word "epoch", per `chief-of-staff.md`). The existing
  Foreman flip's output is not changed.
- No new refusal. With no `chief_transcript` recorded, nothing flips (as today for the opposite
  way); the card's pre-check (below) prevents that case.
- Nothing else in the record changes at the flip: `foreman`, `foreman_epoch`,
  `foreman_transcript` are set by the claim as today; `chief_transcript(s)` unchanged; `brief.md`
  keeps the "Steering:" line written at `open` (as after today's switch to Foreman mode).

Every reader already reads `steering` from the record at each call, so nothing else is needed for
the words: `status` (`commands/batch_status.py`, `steering_word`), `STATUS.md`
(`status/markdown.py`), `STATUS.json` (`status/views.py`), the board (`board/state.py`, the web
`semantics.js` `steeringWord`, `home-batch.js`), the surface list (`core/surface_batches.py`),
`history.py`, `cost` (`commands/cost/command.py`, `sessions.py`) and the Driver prompt skeleton
printed by `take` (`driver_prompt.py`: "Steering: the Chief of Staff" once direct). The evidence
checks each of the user-facing ones.

### 2. The CLI: a steering session that claims again is the current one, and priced per window (Q9)

A switch back and forth (direct, then Foreman, then direct again with the same Chief of Staff
transcript, or a reused Foreman transcript under Remote Control) must keep `cost` and `close`
right. Today it does not, because `_transcript` records a claim only for a transcript never seen
(`if args.value not in b.record.foreman_transcripts`):

- `cost`: `pricing.steering_window` finds a transcript's window by `names.index(uuid)` (its first
  claim only) and ends it at the next claim; a second steering stint of the same transcript falls
  outside every window, so the Chief of Staff's renewed steering would leave the batch's spend for
  the "outside the budget" line.
- `close`: `rails.running` and `costs/endings.transcript_endings` treat the **last** of
  `foreman_transcripts` as the current Foreman; with no new entry, the replaced Foreman stays
  "current" and its transcript, if it reads as running (a session stopped on a tool call at the
  usage limit), blocks `close`.

Required behaviour (the means are the Driver's):

- A claim (`foreman transcript ... --epoch <n>`) whose transcript differs from the last recorded
  claim's records a new claim (`ClaimRecord(transcript, since=now())`), even when that transcript
  claimed before; the same transcript claiming again right after itself (a reused Foreman at a new
  number) records none, as today.
- The current steering session, for `close`, is the last claim's transcript; every earlier one is
  "replaced" (listed apart, never a cause, as `rails.running`'s docstring says). The held agents'
  transcripts are still found under every steering session, the replaced ones included, so
  `close`'s check shows the old Foreman's Drivers' states (Q10 relies on it).
- Each steering transcript is priced over each of its windows (its claim to the next claim, the
  last open-ended; a Foreman's first window from the batch's opening, as today), summed: in
  `commands/cost/pricing.py` (`steering_window`), `commands/cost/sessions.py` (`cost_rows`,
  `_chief_session`) and wherever else a single window per transcript is assumed. A batch with one
  claim per transcript (every batch today) prices exactly as before.
- `chief_outside` (the board's receipt) is not changed (Q8).

### 3. The Chief of Staff's card: `skills/chantier/references/chief-of-staff.md`

- **"Starting a batch", the steering rules (around line 776).** Replace "a Foreman batch never
  becomes direct (see Switching to Foreman mode)" by: a batch keeps its steering until the user's
  word switches it (see "Switching to Foreman mode" and "Switching to direct mode"); going to the
  phone or coming back changes no running or paused batch.
- **Entry points table.** One row: the user asks "switch the batch to direct mode", "take over the
  batch" → the switch, on a running or paused Foreman batch → section
  [Steering a batch yourself](#steering-a-batch-yourself) (its "Switching to direct mode" bullet).
- **"Steering a batch yourself", "Switching to Foreman mode" bullet (around line 1555).** Delete
  its last sentence ("A Foreman batch does not switch to direct mode.", which spans lines 1564-1565)
  and add that the switch can be undone by the switch to direct mode.
- **New bullet "Switching to direct mode"**, right after "Switching to Foreman mode", in the same
  style. Its content:
  1. **Trigger.** The user's word only, on a running or paused Foreman batch, Foreman alive or not.
     It needs nothing a Foreman needs (no preflight P1/P2; it works under Remote Control, in a
     terminal, on both hosts).
  2. **Pre-check, before anything is stopped (Q11).** Compare this session's own transcript id
     (the host's reference says where it is) with the batch record's `chief_transcript` (in
     `batch.json`). If they differ, run `$CHANTIER seat take <your session id>` (it records this
     session's transcript on the batch) and compare again. If they still differ, or the
     transcript is unknown, the CLI could not tell this claim from a Foreman's: stop, and tell the
     user why; no workaround.
  3. **Is the Foreman answering?** `$CHANTIER foreman get`, `$CHANTIER status --refresh` (no
     epoch) for `heartbeat N min`, then `[chief-of-staff→foreman] ping`. Not answering (Q2): the
     heartbeat is late by the board's test (older than the batch's steering wake plus 5 minutes)
     and no `pong` came within 5 minutes; or the user said so (no wait). A Foreman whose heartbeat
     is "stopped" (a loop it ended on purpose, or the batch's pause): the time in
     `heartbeat_stopped` counts as its last heartbeat (Q6).
  4. **A live Foreman.** Send `[chief-of-staff→foreman] switch to direct mode`. Wait for its
     `switched to direct mode <batch>: stopped <what>` line (below). Start nothing until then. A
     Foreman that answered the ping but sends no such line: keep waiting; only the user's word
     moves it to the "not answering" path (Q7). This path works under Remote Control too.
  5. **A Foreman not answering.** Its session is stopped by the user, or by you on the user's yes
     where your host's reference names the means (Claude Desktop: `mcp__ccd_session_mgmt__stop_session`,
     the row added below; Copilot: none recorded, so the user stops it). Under Remote Control
     (Q12): say the stop needs the machine (stopping a session from the phone is unproved), name
     the session and wait. In every case name the session to the user (its title and the id
     `foreman get` prints) and wait until it is stopped.
  6. **Has each old Driver ended? (Q10)** Before any restart, run `$CHANTIER close --batch
     <batch>` (the check, never `--yes`): it lists each held agent's transcript state. Restart
     only the CRs (and the stack driver, QA orders) whose old Driver is shown ended; for any shown
     running or unreadable, ask the user, and restart it only once the user says it is stopped.
     Never assume that stopping a session ended its Agent children. On the live-Foreman path the
     Foreman's `switched` line names what it stopped; the same check confirms them.
  7. **Claim.** Then: `$CHANTIER foreman set <your session id> --epoch <n+1>` (`n` from
     `foreman get`), then `$CHANTIER foreman transcript <your transcript id> --epoch <n+1>`; the
     output's steering line confirms the switch. No such line: stop and tell the user (the batch
     is still a Foreman batch at Foreman n°<n+1>). Then, as after any claim of yours: `$CHANTIER
     rules` and the rule files, your title `[<code>] 💬 Project · CoS (Batch <nn>)`, and your
     heartbeat, as "Steering a batch yourself" says. The old Foreman's number is stale: any
     command it still sends is refused (exit 3) and it stops.
  8. **Resume.** At once, by the restart path, with `resume: switch to direct mode`, for each
     Driver step 6 showed ended: every `working` CR, the recorded stack driver and every open QA
     order with an agent id (`agents set <cr> - --epoch <n+1>`, `handoff <cr>`, `take <cr> --note
     "resume: switch to direct mode" --epoch <n+1>`, a new Driver from the printed skeleton,
     `agents set <cr> <id> --epoch <n+1>`; the stack driver by `take stack --note ...`). A Driver
     of a Foreman stopped from outside counts as stopped from outside: no question to the user,
     counting toward nothing. A CR the old Driver handed back `blocked stopped` with the switch's
     note is taken back the same way and counts toward nothing. No round is counted, no second
     slot taken, the budget applies (exit 5 is a `budget` ask). Queued CRs stay queued; CRs handed
     back `ready` or `blocked` stay as they are; PRs, branches and worktrees are kept.
  9. **Said to the user.** One line: the batch is direct from now on, which CRs restarted (and
     which wait for the user's word that their old Driver is stopped), and that the old Foreman's
     spend stays in the batch's cost. Never the word "epoch" ("Foreman n°3 is stale: the Chief of
     Staff steers batch-06").
- **"Recovery" bullet (around line 1377).** Add after "start a new Foreman with the next epoch":
  or, on the user's word, switch to direct mode ("Switching to direct mode").

### 4. The Foreman's card: `skills/chantier/references/foreman.md`

- **New rule, next to the `chief-of-staff <session id>` hand-over line (around line 710):** on
  `[chief-of-staff→foreman] switch to direct mode`: start no Driver; for each live Driver you own
  (CR, release, stack, QA order), `$CHANTIER note <cr> "switch to direct mode: Driver stopped; the
  Chief of Staff restarts it"` for a CR or release CR, then stop it by the host's stop (your host's
  reference, "Stop a Driver"); do not clear the recorded ids and do not restart anything (the Chief
  of Staff's restart path clears them, as in the switch to Foreman mode); record the heartbeat's
  stop (`$CHANTIER status --stop-heartbeat --batch <batch> --epoch <n>`) and cancel the armed wake
  as your host's reference says; then send `[foreman→chief-of-staff] switched to direct mode
  <batch>: stopped <cr> <cr>… [stack] [O-<k>…]` (`none` when no Driver ran) and stop: no further
  command, no wake (your session is not ended by you; the user may close it).
- **"A Driver stopped from outside", "Which stops" (around line 629):** add "a switch to direct
  mode" to the steering session's own stops, which this rule never restarts.
- **"Keeping its own stops apart" (lines 632-639):** after "it clears the id it recorded for it in
  the same turn", add: "except a switch of mode (to Foreman or to direct mode), whose restart path
  clears them".
- **"After a switch to Foreman mode" (around line 600):** unchanged.

### 5. Other cards

- `skills/chantier/references/concepts.md`, "Steering session" (lines 343-346): replace "switches
  to Foreman mode when a later epoch is claimed by another transcript; a Foreman batch never
  switches to direct mode" by both flips: a later claim by a transcript other than the recorded
  Chief of Staff transcript makes a direct batch a Foreman batch; a later claim by the recorded
  Chief of Staff transcript makes a Foreman batch direct.
- `skills/chantier/references/routing.md`: in the "Chief of Staff → Foreman (also …)" row, add
  `switch to direct mode`; in the "Foreman → Chief of Staff" row, add `switched to direct mode
  <batch>: stopped <cr>…|none`.
- `skills/chantier/references/concepts.md` (around line 539, the restart causes): add `switch to
  direct mode` beside `switch to Foreman mode`.
- `skills/chantier/references/driver.md` (around line 603): "when the steering session's stop
  comes with a switch to Foreman mode" becomes "with a switch of mode (to Foreman or to direct
  mode)".
- `skills/chantier/references/session-start.md` (Titles table, around line 153): the direct-batch
  title row holds "from `open --direct`, the hand-over or a switch to direct mode".
- `skills/chantier/references/hosts/claude-code.md`, Tools table (lines 21-49): one row "Stop
  another session (a Foreman not answering, on the user's yes)": `mcp__ccd_session_mgmt__stop_session`
  with the session's id; mark: unproved (trial: the first switch to direct mode with a Foreman not
  answering, the Foreman's session shown stopped afterwards); from Remote Control, unproved.
  `hosts/copilot.md` names no such means: the user stops the session.
- `skills/chantier/references/hosts/claude-code.md` (Offering options table, around line 621) and
  `chief-of-staff.md`'s Offering options checklist (around line 1410): one row "Switch to direct
  mode": needs only the Chief of Staff's own session; with a Foreman not answering, its session's
  stop needs the machine (unproved from Remote Control); otherwise yes on desktop, Remote Control
  and terminal; unproved until a real switch runs (trial: the first real switch, its events
  showing the `steering` event `direct` and each `resume: switch to direct mode` take).
- The agent files (`agents/`, `com.github.copilot/agents/`) are not touched: the contract lives in
  the cards.

### 6. Docs

- `docs/use-cases-direct.md`, "Switch to Foreman mode" (line 108): drop "A Foreman batch never
  switches back to direct mode."; say it can switch back, and link the new section.
- `docs/use-cases-foreman.md`: a short section "Switch to direct mode" (after "Recover after a
  restart"): the user's word, live or silent Foreman (a silent one's session stopped by the user,
  or by the Chief of Staff on the user's yes on Claude Desktop, from the machine), the Drivers
  restarted once shown ended, nothing lost, the old Foreman's spend kept.

### 7. Alignment with the batch-takeover CR

The inbox CR `batch-takeover` (`projects/chantier/changes/1-inbox/batch-takeover/03-change-spec.md`,
line 215) says the batch's steering "never changes". Whichever of the two CRs merges second aligns
the text: that phrase becomes "the batch's steering, until the user's word switches it". This CR
does not edit that specification; its Driver names the alignment in the PR when batch-takeover has
merged first, and the CR notes it otherwise.

## Out of scope

- A new command, flag or order kind for the switch (Q1).
- Any change to the existing switch to Foreman mode (Q4), beyond removing its "never direct"
  sentence.
- The board's cost receipt (`chief_outside`) after a switch (Q8): a separate CR.
- A means to stop another session on Copilot.
- A changelog entry (none kept); release notes (at release time).
- `brief.md`'s "Steering:" line after a switch (it records the opening, as today).
- The CR board pane: no field of `STATUS.json` changes (only the value of `steering`), so no
  screenshot is owed.

## Host and default matrix

The claimer is recognised by its transcript id, read from the host's environment
(`seat.own_transcript`: `CLAUDE_CODE_SESSION_ID`, `COPILOT_AGENT_SESSION_ID`). Stopping a silent
Foreman's session also depends on the host and the surface.

| Cell | Evidence |
| --- | --- |
| Claude Code, Chief of Staff transcript recorded | scenario step and in-process test below (env `CLAUDE_CODE_SESSION_ID`) |
| Copilot, Chief of Staff transcript recorded | the in-process test, parametrized with `CHANTIER_HOST=copilot` and `COPILOT_AGENT_SESSION_ID`; `cost` there stays "not measured on this host", unchanged |
| Either host, no Chief of Staff transcript recorded | in-process test: the claim leaves `steering` `foreman`, prints no steering line, logs no `steering` event |
| Claude Desktop at the machine, a silent Foreman stopped by the Chief of Staff | card text only; unproved until the trial named in the host reference's new row |
| Claude Code under Remote Control, a silent Foreman | card text only: the stop needs the machine (unproved from the phone); the live-Foreman path stays available |
| Copilot, a silent Foreman | card text only: the user stops its session |

## Evidence

All CLI checks call the shipped code in-process (tests) or through the scenario; the card checks
below read the shipped card files from the repository at the head under test, not a copy.

1. **In-process test** (`skills/chantier/scripts/cli/tests/test_cli_runs.py`, one parametrized test
   over the host cells above, kept within `just test`'s time budget): open a Foreman batch with a
   Chief of Staff transcript recorded; a Foreman claims n°1; the Chief of Staff claims n°2 with its
   own transcript: `batch.json` `steering` is `direct`; `events.jsonl` holds a `steering` event
   with `steering: direct` and the transcript; the output holds the steering line; `status`'s first
   line says ` steering direct (the Chief of Staff) `; `status --refresh --epoch 1` exits 3; the
   next `take` skeleton says "Steering: the Chief of Staff". The no-transcript cell: no flip.
2. **Scenario** (`scenario/run_scenario.py`, unit `direct_batch`, after the existing "a Foreman
   takes the batch over" step around line 2411): the Chief of Staff (`uuid-chief`) claims n°3:
   steering `direct`, a second `steering` event, `foreman_claims` transcripts
   `["uuid-chief", "uuid-foreman", "uuid-chief"]`, n°2 refused (exit 3), `status` and `STATUS.md`
   say direct, `cost` prices the Chief of Staff's two windows inside the batch's spend and the
   Foreman's window between them (a seeded call in each window lands on the right row; no call of
   the second stint on the "outside the budget" line), and `close` does not name
   `transcript uuid-foreman` as a cause while its seeded file ends on a tool call (replaced, listed
   apart). Then one Foreman-opened batch switched to direct with a CR `working` under the old
   Foreman, its Driver's seeded transcript under the old Foreman's session: `close` (no `--yes`)
   shows that Driver's state (running when its file ends on a tool call, ended once it ends on a
   final reply), as Q10 relies on; after the claim, the restart path (`agents set <cr> - --epoch
   2`, `handoff`, `take <cr> --note "resume: switch to direct mode" --epoch 2`) is accepted, the CR
   keeps its branch, worktree and PR, a queued CR stays queued, and the board state
   (`board/state.py`, the batch's `steering`) is `direct`.
3. **Cost unit test** (`tests/test_costs.py` or `test_cost_receipt.py`): `steering_window` (or its
   successor) with repeated claims of one transcript returns each window; a record with one claim
   per transcript prices as before.
4. **Card checks**, reading the shipped files: no card or doc contains "never becomes direct",
   "never switches to direct mode", "never switches back to direct mode" or "A Foreman batch does
   not switch" (grep across line breaks, since that sentence spans two lines in
   `chief-of-staff.md`, for example `rg -U "A Foreman batch does not switch\s+to\s+direct"`);
   `chief-of-staff.md` has a "Switching to direct mode" bullet; `concepts.md`'s "Steering session"
   names both flips; `routing.md` names `switch to direct mode`; `hosts/claude-code.md` names
   `mcp__ccd_session_mgmt__stop_session`. These may be grep lines in the PR's evidence rather than
   new tests, as the project's rules prefer few tests.
5. `just check` green; `just eval-dry-run` green (a change under the CLI's `src/`); the pipeline's
   `just scenario (ubuntu-latest)` job green at the PR's head before it leaves draft; the Windows
   local `chantier gate` as AGENTS.md says for the CR on top of the batch.
