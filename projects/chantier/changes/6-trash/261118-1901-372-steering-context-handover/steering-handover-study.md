# Handing a long batch's steering to a fresh session: a costed study

CR-372, batch-28, round 2. A study and a proposal; it changes nothing in the chantier repository.
Figures come from the archived records of batch-17 to batch-27 (`changes/5-archives/batches/batch-NN.md`
and `.json`) and from the session transcripts, read in place and read-only under `~/.claude/projects/`
(the chantier repository's folder and the planning surface's folder). Every script and figure-only
data file is in `experiments/`; each script holds its command at the top and reruns. No transcript
text and no raw transcript is copied; a wake's cause is a fixed label (see part 2).

Vocabulary. "Chief of Staff" here means the Chief steering a direct batch (batch-19, 21, 22), or, in a
Foreman batch, the Chief's own outside-the-budget steering. "Foreman" means the Foreman session of a
Foreman batch. A "wake" is a user record that is not only tool results; a call's "context" is its
input + 5-minute write + 1-hour write + cache read tokens (the cost code's definitions,
`costs/transcripts.py`, read and re-implemented in `03-steering-calls.py`, nothing imported).
Prices are the cost code's at v0.13.0: Opus 5.5 input 4, write 5 (5 min) / 8 (1 h), read 0.20, output
20 dollars per million tokens; Sonnet 5.5 2, 2.5 / 4, 0.10, 10.

## Limits of this study (read first)

- Batch-20 is not recorded: no `.md` in the archive, its `.json` is `running` with `cost_usd: null`
  (host `copilot`, direct). No transcript was identified for it. Its row below says "not recorded".
- The records keep no transcript ids and `$CHANTIER cost` cannot read a closed batch, so each session was
  identified by window overlap and checked by an exact match: my script reproduces the records'
  wakes, average context and peak context exactly for batch-17, 18, 19, 21, 22, 23, 24, 26 and 27
  (`02-session-by-batch.csv`, `03-steering-calls.csv`). Batch-25 joins two sessions (below).
- The archived records give no steering claims, so a steering window is taken as the batch's whole
  opened..closed window (assumption). The "grill" turns (a spec-writer or spec-critic started, or a
  write to `01-intent.md`, `02-answers.md`, `03-change-spec.md`, `work/specifying`) leave the steering
  figures, as the record does.
- The record's steering dollars include the steering session's own subagents; the transcript's main
  row does not, so mine are a little lower: batch-17 $49.79 against $50.47, batch-22 $14.94 against
  $15.99. Batch-27 differs by far more ($5.54 against $12.67; 182 calls against 412): the gap is not
  reconciled (that Foreman session has 62 subagents, among them 3 retro-critics; I did not split their
  time); read batch-27's share as uncertain by that gap.
- No Copilot steering session was available (batch-20 is Copilot). Copilot rows in part 5 and part 6
  come from the cards and say "unproved" where the cards do.
- Every loss range quoted in parts 4 and 7 is from `09-replay-by-kind.csv` (and `11-replay-130k*.csv`
  for the Driver's 130k): a bound is a sum over the jobs of one kind for one option and one yes delay;
  -449.78 and -46.45 are the largest losses of the 4 context and 3 wake thresholds (context 180k, delay 0),
  and 0.00 means the trigger never fired. The yes delay and the Drivers' restart cost are assumptions
  (part 4), so these are replay figures, not measurements.
- Quality (does a fresh session steer better than one at 250k tokens?) is not measured and not priced.

## Part 1. Steering share by batch, batch-17 to batch-27

Source: the record's lines "Foreman $X (N%)" / "Chief of Staff, steering the batch $X (N%)", and
"Foreman: W wakes, context A tokens on average, P at its peak". From batch-23 on, the same figures are
in the `.json`'s `cost_receipt.steering` (`usd`, `calls`, `wakes`, `context_avg`) and
`cost_receipt.split`. Two compaction columns, each from its own source: "Compactions (record)" is the
`.md`'s line "N compactions since the batch opened" (the whole Chief session, so it is not the steering
session's own count); "Compactions (transcript)" is what the steering transcript shows within the
batch window (`compact_boundary` records, `05-compactions.csv`). The two differ because they count
different sessions and windows. Rows "Chief, outside the budget" give, for a Foreman batch, the record's
line "Chief of Staff, steering the batch (outside the budget): $X since the batch opened (N calls)", with
the cost and the calls only (the record keeps no wakes or context for it; "since the batch opened", so
not windowed to the Foreman's span).

| Batch | Steered by | Steering $ (share of total) | Total | Wakes | Avg context | Peak | Compactions (record) | Compactions (transcript) |
|---|---|---|---|---|---|---|---|---|
| batch-17 | Foreman (stack) | $50.47 (22%) | $229.22 | 312 | 189,870 | 266,705 | 11 | 6 |
| batch-17 | Chief, outside the budget | $59.25 (not a share of the total) | not applicable | not recorded | not recorded | not recorded | not applicable | not recorded |
| batch-18 | Foreman (parallel) | $41.38 (22%) | $183.92 | 226 | 166,848 | 265,766 | 6 | 5 |
| batch-18 | Chief, outside the budget | $49.39 (not a share of the total) | not applicable | not recorded | not recorded | not recorded | not applicable | not recorded |
| batch-19 | Chief (direct) (parallel) | $7.55 (100%) | $7.55 | 16 | 133,476 | 263,775 | 2 | 2 |
| batch-20 | direct, Copilot | not recorded | not recorded | not recorded | not recorded | not recorded | not recorded | not recorded |
| batch-21 | Chief (direct) (parallel) | $4.00 (56%) | $7.10 | 9 | 187,068 | 257,695 | 2 | 2 |
| batch-22 | Chief (direct) (stack) | $15.99 (26%) | $61.78 | 61 | 180,750 | 266,181 | 3 | 3 |
| batch-23 | Foreman (stack) | $7.29 (11%) | $63.94 | 75 | 176,158 | 265,553 | 2 | 1 |
| batch-23 | Chief, outside the budget | $8.45 (not a share of the total) | not applicable | not recorded | not recorded | not recorded | not applicable | not recorded |
| batch-24 | Foreman (stack) | $15.77 (14%) | $117.11 | 167 | 178,467 | 266,614 | 6 | 4 |
| batch-24 | Chief, outside the budget | $30.21 (not a share of the total) | not applicable | not recorded | not recorded | not recorded | not applicable | not recorded |
| batch-25 | Chief and Foreman (joined row) (parallel) | $3.98 (45%) | $8.91 | 14 | 197,182 | 261,128 | 1 | see below |
| batch-25 | Chief, outside the budget | $2.74 (not a share of the total) | not applicable | not recorded | not recorded | not recorded | not applicable | not recorded |
| batch-26 | Foreman (parallel) | $3.93 (23%) | $17.30 | 28 | 212,653 | 262,303 | 1 | 0 |
| batch-26 | Chief, outside the budget | $5.20 (not a share of the total) | not applicable | not recorded | not recorded | not recorded | not applicable | not recorded |
| batch-27 | Foreman (parallel) | $12.67 (48%) | $26.40 | 52 | 172,831 | 266,305 | 1 | 1 |
| batch-27 | Chief, outside the budget | $6.95 (not a share of the total) | not applicable | not recorded | not recorded | not recorded | not applicable | not recorded |

The batch's mode (stack or parallel) is in the second column after the steering session, from the record's header line.

Reading it.

- Direct batches (Chief): $4.00 to $15.99, 9 to 61 wakes, a share of 26% to 100% (batch-19 has no
  Drivers: its whole cost is steering). Their cost per wake is high, $0.25 to $0.42 (transcript main
  row, `07-job-summary.csv`), on Opus, with 2 to 3 compactions each.
- Foreman batches: $3.93 to $50.47 (11% to 48%); the long ones (batch-17, 18, 24) are the large
  figures, 167 to 312 wakes. Cost per wake $0.09 to $0.18.
- The context sits near its ceiling almost all the time: the average at a wake is 133k to 213k tokens
  and the peak 258k to 267k in every window. The host compacts at 266,779 to 273,084 tokens
  (`05-compactions.csv`: 22 compactions), not at the 162k to 170k that `hosts/claude-code.md`
  ("Compacting") measured on 2026-11-13. Calls at or above 150k tokens are 40% to 97% of the calls
  and 35% to 92% of the steering dollars of a window (`07-job-summary.csv`).
- Batch-25 moves: its joined row, 14 wakes, is 12 Foreman wakes (session `cc65c0a9`, $2.13 and 60
  calls in the transcript, 10:19 to 11:09) and 2 Chief wakes (10:10 and 10:18, context about 247k,
  before the Foreman started; the sum matches the record to 9 tokens). The Chief took the batch back
  by the CR-353 switch to direct mode from about 11:09 (a compaction at 10:57 in the Chief's session).
  The window split is inferred from these figures; the record has no claim list. Batch-25 is left out
  of the replay.
- The Chief's outside-the-budget steering in a Foreman batch is the "Chief, outside the budget" rows of
  the table (calls: batch-17 1,054, 18 760, 23 192, 24 486, 25 55, 26 94, 27 134). The Chief's session
  (`91f1382a`, 399 MB) is one session across batch-19 to batch-22 and beyond, whole-session cost
  $829 to $1,110 in the records, so a Chief seat hand-over is the same question as the Chief's long life.
- Batch-22's own retro asks for this study (its steering share, 25%, context averaging 180,000, peak
  266,181, 60 wakes, 3 compactions), "high across batches".

## Part 2. Where the steering cost goes

Source: `07-job-summary.csv`, `07-cost-by-context-band.csv`, `07-wake-causes.csv`
(from `03-steering-calls.csv`, 3,244 priced calls). The cost of a wake's "episode" is that of the
calls from the wake to the next wake.

By token class (share of the steering dollars of a window): cache reads 53% to 66%, cache writes 20% to
34%, output 12% to 19%, fresh input about 0%. Cache writes are largest in the direct sessions (29% to
34%), whose turns are fewer and later. Expired caches are almost nil: 0 or 1 call per session
(the gap rule of the cost code: over 300 s after a 5-minute write, 3,600 s after a 1-hour write); at
most $1.17 and 8% of a window.

By context band, cost per call (batch-17 Foreman, Opus): $0.046 at 100k to 150k, $0.052 at 150k to 200k,
$0.0625 at 200k to 250k, $0.067 at 250k and above. Sonnet windows (batch-23 to 27): $0.02 to $0.045 a call.
So the price of a call rises only about 45% between a 120k and a 260k context: the cache-read price of
the extra tokens is small beside the writes and the output a call carries anyway.

By cause of the wake (fixed labels), over the Foreman windows (872 wakes, $123.37 of episodes) and
the direct windows (86 wakes, $22.72):

| Cause | Foreman wakes (share) | Foreman cost share | Chief (direct) wakes (share) | Chief cost share |
|---|---|---|---|---|
| Chief to Foreman cross-session message | 220 (25.2%) | 30.1% | not applicable | not applicable |
| Subagent hand-back (Drivers, workers) | 213 (24.4%) | 27.6% | 28 (32.6%) | 30.7% |
| Task end: own task | 157 (18.0%) | 5.5% | 10 (11.6%) | 2.2% |
| Task end not started by this session (a leftover task; proxy) | 90 (10.3%) | 9.2% | 6 (7.0%) | 3.3% |
| `/loop` command | 61 (7.0%) | 7.9% | 9 (10.5%) | 6.7% |
| After a compaction or reload | 30 (3.4%) | 6.4% | 6 (7.0%) | 18.6% |
| Agent messages (other, stack to Foreman) | 69 (7.9%) | 5.9% | 6 (7.0%) | 4.3% |
| Heartbeat (`status --refresh`) | 21 (2.4%) | 1.1% | 0 | 0 |
| User turn | 2 (0.2%) | 1.7% | 21 (24.4%) | 34.2% |
| Other cross-session and other system | 9 (1.0%) | 4.6% | 0 | 0 |
| Chief's watcher end (`$CHANTIER watch`, a task end whose command was a `watch`) | 0 | 0 | 0 | 0 |

- The Chief's watcher-end wakes: the classifier (`03-steering-calls.py`, label "task end: watcher") found
  none in the steering windows, in direct or Foreman batches: no row of `07-wake-causes.csv` carries it.
  The ends of a watcher the session started would otherwise sit in "task end: own task", and the ends of
  one it did not start in the leftover class (a proxy), so this study cannot price the watcher's wakes
  apart; it is not measured, not zero in the sessions.
- Hand-backs plus cross-session messages (Chief to Foreman, and the reverse) are 55% to 75% of a
  Foreman window's cost in the largest batches; the Drivers' hand-backs are the work the steering
  session exists to do, so a threshold cannot remove that cost, only reprice it.
- Leftover-task wakes: batch-24 has 33 wakes ("task end not started by this session", 20% of its cost)
  and 33 more of "own task"; the retro counted 75 leftover wakes: the two classifications differ (mine
  is a proxy: a notification whose tool-use id is not among the session's own tool uses).
- The wake count is a poor trigger: wakes are cheap when the context is small and the leftover
  and heartbeat wakes inflate the count; the compaction rhythm (about one per 40 to 60 wakes in
  batch-17 and 18) already tracks the context.

## Part 3. What a fresh session costs to start

Source: `04-fresh-starts.csv` (the first 80 calls of fresh sessions: tools, `chantier` subcommand
words, base names of files read; no text), `08-fresh-start-figures.csv`,
`10-startup-sizes.csv`. "Ready" is the first call that starts steering work (a `ScheduleWakeup`, an
Agent or SendMessage call, or the `/loop` wake); the figures are those of the call before it.

- The first call's context is 69k to 79k tokens: the host's own base (system prompt, tools, memory),
  before any chantier text.
- Startup text proper is small: the manifest's cores for a Foreman are 1,650 + 174 + 237 + 133 + 468 +
  751 bytes (`10-startup-sizes.csv`, bytes divided by 4 for a rough token count: about 0.5k tokens)
  plus `AGENTS.md` (9,187 bytes, about 2.3k). A Chief's role file (`skills/chief-of-staff/SKILL.md`)
  is 2,898 bytes. The 76k to 137k jump to the ready point is therefore the work of getting the state:
  the CLI's `rules`, `status`, `seat`, `foreman transcript`, the cards read on demand
  (`foreman.md` 75,897 bytes, `chief-of-staff.md` 158,347, `concepts.md` 63,781 are only partly read) and the
  transcript tail.

| Session | Calls to ready | Context at ready | Cost to ready |
|---|---|---|---|
| Foreman, batch-17 | 12 | 153,769 | $1.32 |
| Foreman, batch-18 | 11 | 149,950 | $1.29 |
| Foreman, batch-23 and 24 | 25 | 194,095 | $1.14 |
| Foreman, batch-25 | 11 | 171,635 | $0.72 |
| Foreman, batch-26 | 49 | 212,941 | $1.79 |
| Foreman, batch-27 | 28 | 151,972 | $0.91 |
| Foreman median (n=6) | | 162,702 | $1.216 |
| Chief (planning-surface session) | 23 | 128,339 | $0.67 |
| Chief after `seat take` (11 Nov to 12 Nov) | 22 | 172,625 | $1.87 |
| Chief fresh start | 20 | 154,413 | $1.60 |
| Two other fresh Chief sessions | not reached in 80 calls | not recorded | not recorded |
| Chief median (n=3) | | 154,413 | $1.602 |

- A fresh session lands at 150k to 195k tokens, about as high as the context at which a threshold would
  trigger. A compaction instead lands at 85k to 114k for the first call after it, 90k to 127k at the
  10th call (`05-compactions.csv`, 22 compactions; `compact_boundary` shows the summary itself is
  only 17k to 38k tokens and the host's base brings the rest). So a fresh start is 50k to 80k tokens
  heavier than the compaction it would replace, and costs $0.7 to $1.9 more.
- A Driver restart (every running Driver dies with the steering session, since Drivers are its
  subagents): 218 of 256 Driver rows reach a 15th call; median cost to it $0.44, median context at it
  about 81k (`06-drivers.csv`). Work in progress of the Driver is not priced.
- The measured Chief starts are few (3 usable, 2 not reaching ready); treat the Chief figure as
  indicative: $0.67 to $1.87.

## Part 4. Threshold options costed by replay

Script: `09-replay.py` (reads `03`, `05`, `06`, `08`; outputs `09-replay.csv`, `09-replay-by-kind.csv`,
`09-calibration.csv`, and `-no-driver` variants). Rerun: `python 09-replay.py` and
`python 09-replay.py --no-driver-cost`.

Method. Each steering session of a window is replayed call by call. The context after a call grows as
it did; the host compacts at 266,500 tokens (the context drops to the job's mean measured first-call-after
level, 84k to 113k; the next call rewrites the whole context; $0.12 per compaction, the cost code's
figure). A call is re-priced from the simulated context: input and output as recorded; cache writes as
recorded, except a call that rewrote its whole context, which rewrites the simulated one; the rest is read.
Options:

- `none`: today (compaction only).
- `context X`: at a wake whose context is at or above X (180k, 200k, 230k, 250k), the steering session
  offers a hand-over.
- `wakes N`: after N wakes since the start or the last hand-over (30, 60, 100), counting all wakes, or
  all except task-end wakes (the leftover and own-task wakes).
- The offer waits for the user's yes for D: 0, 30 minutes, 2 hours, 8 hours. The hand-over happens at
  the first wake at or after offer time + D; until then the old session goes on as recorded.
  "Refused" is `none`. The yes delay is an assumption, not a measurement: no record keeps how long the
  user took to answer a given question.
- At a hand-over: the new session starts at the measured ready context (Foreman 162,702, Chief
  154,413) and pays the measured start (Foreman $1.216, Chief $1.602); plus the old session's last turn
  (3 calls at its context, plus 3,000 output tokens each); plus the messages (the offer and the yes: 2
  wakes of the old session at its own dollars per wake; a Foreman's offer reaches the user through
  the Chief, so also 2 Chief wakes, $0.277 each, the direct sessions' mean); plus every Driver running at
  that time (`06-drivers.csv` time ranges) restarted at $0.44 (the `-no-driver` variant: none lost, a
  lower bound). Not priced: a restarted Driver's lost work, the user's time, any quality difference.
- Batch-25 is left out (joined row); Foreman jobs: batch-17, 18, 23, 24, 26, 27; direct jobs: batch-19,
  21, 22.

Calibration (`09-calibration.csv`): the replayed `none` against the transcript's main row is within
-4.5% to +9.7% for every job (batch-17 $53.28 against $49.79, batch-18 $45.32 against $41.37, batch-22
$15.24 against $14.94, batch-26 $3.48 against $3.48). Replayed `none` totals: Foreman jobs $130.83,
direct jobs $24.41. Every option is compared with `none` replayed, so this bias cancels in a saving.

Result (saving in dollars summed over the jobs of the kind; a negative saving is a loss; the number
of hand-overs is in the CSV). Yes delay: 0, 30 minutes, 2 hours, 8 hours. Across all the options of
`09-replay-by-kind.csv` (context 180k to 250k, wakes 30 to 100, with or without the leftover wakes, the
four delays, Drivers restarted at $0.44), the saving runs from -449.78 (Foreman, context 180k, delay 0,
120 hand-overs) to 0.00 (a trigger that never fires) for the Foreman jobs, and from -46.45 (direct,
context 180k, delay 0, 16 hand-overs) to 0.00 for the direct jobs; the table's rows are a selection
(its largest loss is -236.26, context 200k at delay 0, not the CSV's largest).

| Kind | Option | 0 | 30 min | 2 h | 8 h |
|---|---|---|---|---|---|
| Foreman (6 batches, none $130.83) | context 250k | -106.45 | -81.03 | -41.66 | -12.60 |
| Foreman | context 200k | -236.26 | -133.24 | -65.08 | -13.98 |
| Foreman | wakes 60 | -44.11 | -32.12 | -23.14 | -9.60 |
| Foreman | wakes 100, no leftover wakes | -13.71 | -11.12 | -10.37 | 0.00 |
| Chief, direct (3 batches, none $24.41) | context 250k | -16.81 | -9.58 | -7.87 | -1.90 |
| Chief, direct | context 200k | -29.36 | -17.73 | -8.24 | -1.90 |
| Chief, direct | wakes 60 | -2.38 | 0.00 | 0.00 | 0.00 |
| Chief, direct | wakes 100 | 0.00 | 0.00 | 0.00 | 0.00 |

- No option saves, for any delay: every row is a loss or zero (the `batches_that_save` column is 0 in
  every row). Zero means the trigger never fired. The cheapest losing rows are those that fire least.
  With no Driver lost (`09-replay-by-kind-no-driver.csv`) the losses are smaller and still every
  context or wake option loses: context 250k at 30 minutes, Foreman -50.42 and Chief -9.14; wakes 100,
  Foreman -11.05.
- Why: a hand-over costs $2.2 to $4.9 each at the context-250k trigger (Drivers dominate: $0.44 each,
  several live at the long batches' hand-over time, plus the start, the old turn and the messages),
  whereas a compaction costs $0.12 and lands lower (85k to 114k) than the hand-over's 154k to 163k.
  The recurring price difference between a 160k and a 100k context is the cache read of 60k tokens at
  $0.20 per million tokens (Opus): 60k tokens × $0.20/MTok = $0.012 a call on Opus, $0.006 on Sonnet: a hand-over would pay its
  $1.2 to $1.6 start after 100 to 270 calls, and the other costs after more, before the next compaction
  cycle (a compaction cycle is about 40 to 60 wakes, and 100 to 150 calls).
- At delay 0 the replay hands over repeatedly (a context option at 180k re-fires 17k to 26k tokens after a
  hand-over at 154k to 163k): those rows count hand-overs the user's yes would limit, and show the cost
  is per hand-over, not an artefact of the wait. A longer wait lowers the loss only by firing less:
  waiting never turns a loss into a saving, because the old session's calls are at their recorded
  price whatever the wait.
- A threshold set "just before compaction" (250k) loses as much as the others: the new session is
  heavier than the compaction it dodged.
- Would the best threshold differ by kind? No: both kinds' best option is `none` (the Chief's `wakes
  100` rows are zeros because they never fire). The Chief's loss per hand-over is lower (3 jobs, fewer
  Drivers), the Foreman's is larger (more Drivers in flight, a longer chain of messages through the Chief).

The Driver's own threshold. `driver.md` ("Your means") has a Driver hand back `blocked context: ...` at
130,000 tokens. Applied to a steering session as the replay's "context 130k" option
(`11-driver-threshold-replay.py`, `11-replay-130k.csv`, `11-replay-130k-no-driver.csv`; same jobs, same
costs, saving against `none` replayed; `none` sums $130.84 and $24.41 there, a rounding of the same
jobs):

| Kind | Variant | 0 | 30 min | 2 h | 8 h |
|---|---|---|---|---|---|
| Foreman (6 batches) | Drivers restarted | -3,247.32 (848 hand-overs) | -365.37 (109) | -85.77 (28) | -15.60 (5) |
| Foreman | no Driver lost | -1,914.87 | -240.30 | -63.03 | -11.66 |
| Chief, direct (3 batches) | Drivers restarted | -283.64 (97) | -39.05 (14) | -13.55 (5) | -1.90 (1) |
| Chief, direct | no Driver lost | -235.97 | -33.80 | -12.24 | -1.90 |

- At 130k the trigger sits below the 154k to 163k a fresh session lands at, so at delay 0 it fires at
  almost every wake after a hand-over (848 and 97 hand-overs): the figures at delay 0 are an upper bound
  of the loss, which the user's yes would limit; at 8 hours (5 and 1 hand-overs) the loss is -15.60 and
  -1.90, no better than the 180k to 250k rows. A Driver's threshold works because a Driver restarts to
  81k and $0.44 (part 3); a steering session restarts to 150k to 195k and $0.7 to $1.9, above 130k.
  So the Driver's threshold does not carry over: its comparison is a Driver restart against a steering
  hand-over, not a like-for-like threshold.

Not tested by the replay: a hand-over that follows a compaction (it would be later, and heavier than
the compacted session); a hand-over whose start is cheaper than measured (a smaller handoff file, a
leaner first read); the unproved hosts.

## Part 5. What a fresh session reads to take over, against the existing procedures

The takeover has two existing procedures for the same session kinds, plus the restart path; the
mechanism a threshold would need is mostly there. Files: `skills/chantier/references/` unless noted.

| Need | Existing procedure and where | Reuse for a hand-over |
|---|---|---|
| Chief seat moves to a new session | `chief-of-staff.md`, "Handing the seat over": only on the user's word; a running Driver is never stopped or moved (the old session finishes it, `order slots --note 0`); message `[chief-of-staff→chief-of-staff] your turn, you are the Chief of Staff`; the new session answers `I have the batch`, runs `seat take <own id> --over <old id>`; a direct batch: it claims the next epoch; a Foreman batch: it sends the Foreman `chief-of-staff <session id>` (`routing.md`; `foreman.md`) | the user's-yes gate, the message pair and `seat take` are the offer and the take |
| Foreman replaced by a fresh Foreman | `chief-of-staff.md`, "Switching to Foreman mode" (stop live Drivers, start the Foreman at the next epoch with "Resume: …"); `hosts/claude-code.md` row `start_session` (a new Foreman from a remote client is unproved) | the start and the resume line |
| Steering switched from Foreman to the Chief | "Switching to direct mode", steps 1 to 9: trigger; pre-check `chief_transcript` (`seat take`); ping the Foreman (`foreman get`, `status --refresh`, `[chief-of-staff→foreman] ping`); `[chief-of-staff→foreman] switch to direct mode` and wait for `switched to direct mode <batch>: stopped …`; a Foreman that does not answer is stopped by `mcp__ccd_session_mgmt__stop_session` on the user's yes (Copilot: none; the user stops it; stopping from the phone is unproved); `close --batch` without `--yes` to check each old Driver ended; claim the next epoch (`foreman set <id> --epoch <n>`, `foreman transcript <id> --epoch <n>`); restart by the restart path with `resume: switch to direct mode`; one line to the user | steps 2, 6, 7 and 8 are the pieces a same-kind hand-over reuses; steps 3 to 5 are what the old steering session would do in its own hand-over |
| Restart after an app restart | `chief-of-staff.md` "Recovery"; `foreman.md`: after an app restart, at a new epoch, every `working` CR, the recorded stack driver and every open QA order with an agent id are restarted at once, by `agents set <cr> - --epoch <n>`, `handoff <cr>`, `take <cr> --note "resume: <cause>" --epoch <n>`, a new Driver, `agents set <cr> <id> --epoch <n>` | the Driver restart a hand-over pays ($0.44 each); `blocked context:` and `context: closing:` go through it too |
| What a session reads at start | `session-start.md` section 5 "Reload": the manifest cores and the role's startup sections only, with `seat` and `status`, no order, heartbeat or `uv sync`; the watcher paragraph: the yes holds once per session, started with `$CHANTIER watch --after <n>` | the first read (about 3k tokens of text, `10-startup-sizes.csv`) is small; the rest of the 76k to 137k jump is state reading |
| What the new session needs from the old | the heartbeat is `status --refresh --epoch <n>` (a `/loop` in dynamic mode with `ScheduleWakeup`, `hosts/claude-code.md` "Heartbeat"); `foreman transcript <id> --epoch <n>`; `$CHANTIER rules`; the board, the watcher and the epoch ride only on the commands the card lists | the epoch claim fences the old session out |
| Driver self-restart | `driver.md` "Your means": `handback <cr> blocked context: …` at 130,000 tokens; the closing hand-off `context: closing: VERIFIED at <sha7>; next: …` | a Driver already has a context threshold; a steering threshold copies its shape |
| After a compaction | `hosts/claude-code.md` "Reload after a compaction": the mod's message after every compaction of a role session | the reload is automatic; a hand-over would add a second path |

Copilot: `hosts/copilot.md` has the Foreman's start via `create_session`; a message to another session
of the user by `send_message` to its link ("hand-over", unproved); "is the seat's session alive" is "not
known"; no row starts a fresh Chief; a Driver is stopped by `write_agent`. So on Copilot a Chief
hand-over has no proved means; a Foreman hand-over has the start but not the check that the old session
is gone.

Per kind, what the new session reads (spec item 5), from today's cards:

- Chief of Staff, direct batch: `$CHANTIER seat` and `seat take <own id> --over <old id>`; the next
  epoch (`foreman set <id> --epoch <n>`, `foreman transcript <id> --epoch <n>`, "Steering a batch
  yourself"); `$CHANTIER rules` and the rule files it lists; the batch's state (`status`, `asks`, the
  STATUS files, `brief.md`); the startup manifest's cores for the role; the heartbeat it arms
  (`status --refresh --epoch <n>`); the watcher again (`$CHANTIER watch --after <n>`, from the `watch:`
  line of `status`; the user's yes holds once per session, `session-start.md`, so a fresh session asks
  it again).
- Foreman: `foreman set <session id> --epoch <n>`, then `foreman transcript`; its brief; the same
  rules and state; the Foreman's cores (`foreman.md`, `concepts.md`, `hosts/claude-code.md` startup
  sections); the heartbeat; the restart of every `working` CR, the recorded stack driver and every
  open QA order ("After an app restart, at a new epoch"; "The restart path"; "Recovery").
- For both: the decisions not yet written that only the old session's context holds: nothing in
  today's procedures moves them; a hand-over would need the old session to write them first.

What each existing procedure lacks for a hand-over in the middle of a running batch: "Handing the seat
over" waits for every running Driver to finish (no steering in the meantime, the old session keeps
the batch); "Switching to direct mode" stops the Foreman and restarts the Drivers (a move across
kinds, with the wait for `switched to direct mode`); Recovery assumes the old session is gone; the
reload after a compaction keeps the session. Running Drivers are background children of the
steering session and die with it (`foreman.md`); their `Steering:` line names the old session; the
board stops when the seat moves; the watcher belongs to its session; in a Foreman batch the Foreman
must be told `chief-of-staff <session id>` if the Chief moves. The Driver's own hand-back
(`driver.md`, 130,000 tokens) is the nearest comparison: a Driver restart costs a median $0.44 to
its 15th call at about 81k tokens, against $0.7 to $1.9 and 150k to 195k for a steering session.

What a fresh session reads, in order, for the cheapest hand-over built on those pieces: the startup
cores (about 3k tokens), `seat` and `status`, `$CHANTIER rules`, the old session's last hand-off
(a file the old session writes before it stops), `foreman transcript` for the Foreman, the CRs'
handoffs for each Driver to restart. The measured start already includes this reading
($0.72 to $1.79 for a Foreman, $0.67 to $1.87 for a Chief); it is not much lower than a card-driven start.

## Part 6. Risks

- Work in flight is lost: every running Driver, worker and watcher belongs to the old session and dies
  with it (Drivers are subagents of the steering session); the Chief seat card's choice, "the old
  session finishes the work", means the hand-over waits for the Drivers or restarts them at $0.44 each
  and the lost work. The Foreman's hand-over restarts every Driver at once (as after an app restart).
- The wait for the yes is a stall: until the user answers, the old session either keeps steering at its
  current price or stops (and the batch waits). A Foreman's offer reaches the user through the Chief
  (an `asks` line), which adds a Chief wake each way ($0.277) and a delay; a refused or late yes makes
  the option `none` plus the cost of the offer. The user's yes cannot be given from every host
  (stopping a session from the phone is unproved; Copilot has no `stop_session`).
- Two sessions steering at once: the epoch fences commands (a refused command exits 3), but a
  hand-over window where both exist is the exposure the cards' ordering (claim the next epoch last, after
  `close` shows each old Driver ended) closes; any new path must keep that order.
- A gap in forge events: a hand-over is a pause; the forge hub's merges and red CI land in
  `forge-journal.jsonl` and the new session's watcher must start with `$CHANTIER watch --after <n>` so
  nothing between the two is missed.
- Cost attribution: two `main` rows for one batch (the two sessions) in the cost code, which names
  steering by claims and windows; batch-25 shows what a split costs the record: one joined row, a
  label "Chief of Staff, steering the batch and Foreman", not two figures.
- A fresh start is not cheaper in context than a compaction (part 3), so a threshold set below
  compaction trades a lighter-but-lossy summary for a heavier-but-lossless re-read, at a price; any
  quality gain is unmeasured.
- Hosts: the remote-client start of a Foreman and the stop from a phone are unproved on Claude Code;
  Copilot has no proved hand-over means (part 5).
- Measurement risks of this study: the steering windows are the whole batch (assumption); batch-20 has
  no transcript identified; the leftover-task class is a proxy; the Chief fresh starts are 3 usable
  samples; the yes delays are assumed, not observed; the Foreman figures in the records that include
  subagents differ from my main rows (batch-27 unreconciled).

## Part 7. Recommendation (a proposal)

1. Do not add a steering hand-over at a context or wake threshold. On the replay of the recorded
   batches, no option saves, for any yes delay from 0 to 8 hours: each costs more than `none` or never fires
   (over the context 180k to 250k and wakes 30 to 100 options of `09-replay-by-kind.csv`, the saving
   runs from -449.78 to 0.00 on the six Foreman batches and from -46.45 to 0.00 on the three direct
   batches, -449.78 and -46.45 being context 180k with no wait; 0.00 is a trigger that never fires;
   the Driver's 130k, replayed in part 4, loses -15.60 to -3,247.32 and -1.90 to -283.64), against a
   replayed steering total of $130.83 and $24.41. The cause is structural, not tunable: a hand-over's start
   ($0.7 to $1.9) plus the old session's closing turn, the messages and the Drivers it kills ($0.44 each)
   exceeds what it saves, and the host's compaction (about $0.12) already lands the session at a
   lower context (85k to 114k) than a fresh session reaches (150k to 195k).
2. The cheapest levers for the steering share are elsewhere (to be studied before they are built):
   the host's `autoCompactWindow` (`hosts/claude-code.md` recommends 300000; the measured compaction
   point is already 267k), the number of wakes (hand-backs plus cross-session messages are 55% to
   75% of a Foreman window's cost in the long batches), and the leftover-task wakes (90 of 872 Foreman
   wakes and 9.2% of their cost, a proxy figure).
3. If the user still wants a hand-over for a quality reason (a session that steers worse near 250k), keep
   it opt-in and per session, on the user's word, as "Handing the seat over" already is for the
   Chief, and extend it rather than add a new path: the pieces to reuse are the user's-yes gate and
   message pair, `seat take --over`, the epoch claim, `close` to check each old Driver ended, and the
   restart path with `resume: <cause>`; the only new piece is the old session's offer at a context
   point, and a closing hand-off file. Expected saving: none; expected cost per hand-over $2.2 to
   $4.9 (Foreman and Chief, with Drivers in flight) or $0 extra at no running Driver. Quality is
   unmeasured; a measurement would need paired batches.
4. Open points for the user: whether the quality argument matters at all; whether a Copilot Chief
   hand-over should be proved first; batch-20's transcript, if it still exists.

This is a proposal: the CR does not decide it.

## Files (`experiments/`)

| File | What |
|---|---|
| `01-transcript-index.py` / `.csv` | index of 2,710 transcripts (top-level and subagents): first and last time, calls, wakes, peak context, compactions, claim epochs, batch ids named |
| `02-session-by-batch.py` / `.csv` | calls and peak context per batch window per session (how steering sessions were found) |
| `03-steering-calls.py` / `.csv` | the cost code's parsing re-implemented; one row per priced call of each steering session |
| `04-fresh-starts.py` / `.csv` | tools, `chantier` subcommand words and file base names of fresh sessions' first 80 calls |
| `05-compactions.py` / `.csv` | the 22 compactions: pre and post tokens, context after |
| `06-drivers.py` / `.csv` | Driver subagents per batch window: calls, peak, cost to the 15th call |
| `07-analysis.py` and `07-*.csv` | job summary, cost by context band, wake causes |
| `08-fresh-start-figures.py` / `.csv` | ready point per fresh session and medians |
| `09-replay.py` and `09-*.csv` | the replay (part 4) and its calibration, with a `-no-driver` variant |
| `10-startup-sizes.py` / `.csv` | bytes of the startup cores from the startup manifest |
| `11-driver-threshold-replay.py` and `11-*.csv` | the replay of the Driver's 130,000-token threshold on a steering session (part 4) |
