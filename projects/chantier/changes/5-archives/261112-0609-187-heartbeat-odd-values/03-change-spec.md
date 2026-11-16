# Change Specification: the heartbeat says something true in direct mode

## Goal

In direct mode (the Chief of Staff steers the batch from its own session, `open --direct`), the
"heartbeat N min" that `chantier status` prints showed values that were not true (batch-09,
2026-11-10 and 2026-11-11):

- "heartbeat 170 min" right after the steering session had refreshed;
- "heartbeat 0 min" at other times;
- 439 min while the loop was stopped (batch-09 retro, `5-archives/261111-1247-171-batch-09-retro-fixes/retro.md`).

The user's decisions (`02-answers.md`, 2026-11-11):

- In direct mode, "heartbeat N min" is **the minutes since the steering session's last `status
  --refresh --epoch`**, with the same meaning as in Foreman mode. The Investigator first finds
  where the values 170 and 0 came from; the fix makes the printed value match that meaning at
  every reading.
- **A wake's own line** shows the gap since the wake before, e.g. "heartbeat 0 min (31 min since
  the last)".
- **The refresh before a report** in direct mode carries no epoch: only the loop's wakes move the
  heartbeat.
- **A stopped loop is marked:** the steering session records the stop of its loop, and `status`
  shows "heartbeat stopped" instead of a growing age.

## What the code does today (read on main 1e99343)

These are leads for the Investigator, not conclusions. It confirms or refutes each one with a
reproduction before anything is changed.

- **One writer.** `heartbeat` in `batch.json` is written only by `_refresh` in
  `skills/chantier/scripts/cli/src/chantier/commands.py` (lines 1147-1149: `b.data["heartbeat"] =
  now()` and the `heartbeat` event), and only when `--epoch` is given. `open` sets it to `None`
  (line 665). No other module writes it; `state.py` writes `batch.json` only through `Batch`,
  under its lock.
- **One reader in the CLI.** `status` (lines 1181-1196) calls `_refresh` first, then reads the
  batch and prints `heartbeat {age_minutes(...):.0f} min` (`age_minutes` in `state.py` line 158,
  UTC on both sides). So `status --refresh --epoch <n>` prints the age of the heartbeat it has
  just written: its own line always says "heartbeat 0 min". Lead for the value 0.
- **Refreshes with no epoch.** The cards make the Chief of Staff run `status --refresh` with no
  epoch before a report: `skills/chantier/references/chief-of-staff.md` line 26 ("status?") and
  line 286, `skills/chantier/references/status-layout.md` line 11,
  `skills/chantier/references/session-start.md` line 163. Such a refresh records no heartbeat.
  In direct mode it is the steering session that runs it, so the session is seen refreshing while
  the heartbeat keeps its age. Meanwhile `chief-of-staff.md` lines 485-488 ("Steering a batch
  yourself", "Your epoch") tell the same session to carry `--epoch <n>` on every `status
  --refresh`. One session, two rules. Lead for the value 170.
- **The loop stopped.** `skills/chantier/references/hosts/claude-code.md` lines 48-53: the
  steering session's `/loop` wakes every 30 min and ends with `ScheduleWakeup stop: true` after
  `pause` or on an idle wake. After that the age grows with nothing to reset it (the 439 min).
  The CLI does not know today that the loop ended. `foreman.md` lines 152-160 say the same for a
  Foreman. `hosts/copilot.md` lines 36-44 run the same command through `/every`, which the Foreman
  cannot end (the user deletes it).
- **Other readers.** `status.py` line 281 copies the timestamp into `STATUS.json`; the board,
  `hooks/register.tsx` lines 568-580, shows "Foreman silent for N min" from it while a CR is
  `working`.

If the Investigator finds another cause (a wrong session, a wrong checkout or planning folder, a
lost write, a clock), it records it in the CR's notes with its reproduction, and the fix covers
it.

## What changes

### 1. The investigation, first

- Reproduce each value in a scratch batch opened with `open --direct` (the scenario's
  `direct_batch` in `scenario/run_scenario.py`, from line 914, shows how: `foreman set
  uuid-chief --epoch 1`, then `status` calls; an older heartbeat is set by editing `batch.json`,
  as its `edit(...)` helper does).
- Record in the CR's notes, for 170, 0 and 439: the command that printed it, what `batch.json`
  held, and whether the value was the true age of the last `status --refresh --epoch` or not.

### 2. The CLI

The end state, in both modes (direct and Foreman), whatever the cause:

- **What moves the heartbeat.** `heartbeat` in `batch.json` is the time of the last `status
  --refresh --epoch <n>` accepted for the batch's current epoch. Nothing else moves it: not
  `status --refresh` with no epoch, not `status`, not another command.
- **An ordinary reading.** Every `status` line prints "heartbeat N min", N the whole minutes since
  that time at the moment of reading, or "heartbeat never" before the first one.
- **A wake's own line.** The line printed by `status --refresh --epoch <n>` itself shows the
  heartbeat it has just recorded and the gap since the one before, in this form: "heartbeat 0 min
  (31 min since the last)", 31 the whole minutes between the previous heartbeat and this one. On
  the batch's first wake (no previous heartbeat), it prints "heartbeat 0 min" alone. The previous
  value is the one `batch.json` held before this wake overwrote it.
- **A stopped loop.** The steering session (the Foreman, or the Chief of Staff in direct mode)
  records in the batch that it has ended its loop. From then on every `status` line prints
  "heartbeat stopped" in place of "heartbeat N min". The next accepted `status --refresh --epoch
  <n>` (the loop armed again) clears the mark and records a new heartbeat; its line follows the
  rule above. Recording the stop:
  - carries `--epoch <n>` and is refused on a stale epoch (exit 3), like every steering command;
  - is written under the batch's lock and logged as one event in `events.jsonl`;
  - is a form on an existing command (the Driver picks it, e.g. an option of `status` or the
    stop recorded by `pause`, which ends the loop at once), not a new command (`AGENTS.md`: no
    new CLI tool without a measured token cost). A new field in `batch.json` holds the mark.
  - `STATUS.json` (`status.py` line 281) carries the mark next to `heartbeat`, so its readers can
    tell a stopped loop from a silent one.
- A cause the Investigator finds that breaks any of this (section 1) is fixed in the CLI, in the
  module that holds it.
- `--help` texts of `status` and `--refresh` (`cli.py` lines 105-112) say what the heartbeat
  measures and how the stop is recorded, if they change.

### 3. The cards

- **One rule for the steering session in direct mode.** `chief-of-staff.md` "Steering a batch
  yourself" (lines 485-488): `--epoch <n>` goes on the loop's wakes (`status --refresh --epoch
  <n>`) and on the other steering commands (`take`, `agents set`, `order done`, `order merged`,
  `cancel`, `pause`), never on the refresh before a report, which stays `status --refresh` with
  no epoch, as lines 26 and 286 and `status-layout.md` line 11 already say. One sentence says what
  the session's own "heartbeat N min" measures: the minutes since its loop's last wake.
- **Recording the stop.** Wherever a card or host reference tells the steering session to end its
  heartbeat, it also tells it to record the stop with the CLI form chosen in section 2:
  `foreman.md` lines 154-160 (right after `pause`, and on an idle wake), and the "Heartbeat"
  sections of `hosts/claude-code.md` (lines 48-53, before `ScheduleWakeup stop: true`) and
  `hosts/copilot.md` (lines 36-44: when the Foreman ends its heartbeat, and in direct mode when the
  Chief of Staff does; while an `/every` still fires, its next wake clears the mark, which is
  true). `chief-of-staff.md` line 435 ("a stale heartbeat says something only while a CR is
  `working`") names "heartbeat stopped" as the loop that ended on purpose.
- No change to `agents/` or `com.github.copilot/agents/` (no role changes); if one becomes
  needed, both hosts change together, bodies identical (`AGENTS.md`).

### 4. Docs

`docs/use-cases-direct.md` line 88 ("The batch's heartbeat runs in your own session") and
`README.md` lines 406 and 442: add or fix a sentence on what "heartbeat N min" and "heartbeat
stopped" mean only where they say otherwise or nothing today. `docs/cr-lifecycle-texts.md` line
203 ("/loop · chantier status --refresh") gets `--epoch <n>` if it shows the loop's command.

## The eval run

This CR runs in the `real-foreman` eval campaign (`evals/real-foreman/RUNBOOK.md`), in a batch steered by a new
Foreman session that the user starts (`02-answers.md`).

- The PR opens as a **draft**.
- The first line of its body is exactly:
  `**Eval run: do not merge.** The maintainer decides what happens to this PR.`
- **Nobody merges it**, and nobody enables auto-merge. As the runbook says, its Driver turns it
  ready once it can merge (base `main`, CI green, evidence in); on another base it stays a draft.
  The CR stops at `ready`. Whatever comes next is the user's word.
- Work on a branch in the CR's worktree; the main checkout stays on `main` and untouched
  (`AGENTS.md`, eval rules).

## Out of scope

- The board's wording ("Foreman silent for N min" in direct mode, `hooks/register.tsx`), unless
  the cause is there; it only gains the stop mark through `STATUS.json`.
- The loop's period, its stop conditions, and how a host arms it.
- The spend recorded by `status --refresh` (`spent`, `_record_costs`).
- A session that dies without recording a stop: its heartbeat keeps aging, which is the true
  signal ("No wake ever arriving is a stop").
- Any version bump (`just version` is the release's).

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes, with new checks in `direct_batch` (`scenario/run_scenario.py`), on a
  direct batch at epoch 1:
  - with `heartbeat` set N minutes ago (N at least 30) in `batch.json`, `status` prints
    "heartbeat N min" (within one minute);
  - `status --refresh` with no epoch leaves `heartbeat` unchanged and still prints about N;
  - `status --refresh --epoch 1` records a new heartbeat (and its event in `events.jsonl`), and
    its own line prints "heartbeat 0 min (N min since the last)" (within one minute); a
    following `status` prints "heartbeat 0 min";
  - on a batch's first wake, the line prints "heartbeat 0 min" with no gap;
  - recording the stop with `--epoch 1` makes `status` print "heartbeat stopped", logs its event,
    and shows the mark in `STATUS.json`; recording it with a stale epoch exits 3 and changes
    nothing;
  - the next `status --refresh --epoch 1` clears the mark and prints "heartbeat 0 min (... since
    the last)";
  - a check for each cause the Investigator found, failing on main and passing on the branch.
  The existing check of `lost_messages` ("a wake ... records the heartbeat", line 3022) keeps
  passing, adapted only for the wake line's new gap.
- The Investigator's notes name the source of 170, 0 and 439.
- The PR: a draft, its first line as above, not merged.

## Open questions

None: the three questions of the earlier version are settled in `02-answers.md` ("the
spec-writer's open questions"), and the form of the stop's record is the Driver's to pick within
section 2.
