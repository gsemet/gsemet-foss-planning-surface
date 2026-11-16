# Change Specification: the spend is fresh when the budget is checked

Short name: `spend-fresh`. Absorbs `2-backlog/P3/status-spend-age`.

## Goal

The budget rail must check the batch's real spend, not a figure recorded long ago. In batch-18's
real-foreman run 2 (2026-11-15), `status` showed "$0.82 of $20" while the real spend passed $11:
only `status --refresh`, `pause` and `close` write `spent_usd`, and `take`, `round` and the other
commands that check the budget read whatever was last written. In a short batch, where no
heartbeat refresh comes between two takes, the budget is never really checked. And a reader of
`status` (and of `STATUS.json`) cannot tell how old the figure is (real-direct run 1, 2026-11-12:
$0.57 shown long after `cost` said $9.57).

So: every command that checks the budget first refreshes the spend from the transcripts, and
`status` and `STATUS.json` say how old the spend figure is.

## What changes

### 1. The spend is refreshed where the budget is checked (CLI)

Today the budget is checked, always on the stored `batch.json` `spent_usd`, at these points:

| Command | Where the check is |
| --- | --- |
| `take <cr> --epoch <n>` | `rails.check_take` -> `check_budget` (`commands/driver.py` `take`) |
| `take stack --epoch <n>` | `check_budget` in `commands/driver.py` `take` |
| `round <cr>` | `rails.check_round` -> `check_budget` (`commands/driver.py` `round_`) |
| `order qa` | `check_budget` in `commands/orders.py` `_qa_folder` |
| `order add --fix-for` (the Foreman's own, under the grant) | `rails_release.check_granted_fix` (`commands/orders_apply.py` `_add`) |
| `release go <cr>` (a release action or a fix's merge) | `over_budget` in `rails_release.release_go` / `fix_go` (`commands/release.py`) |

New behaviour, at each of these points, when the batch has a budget (`budget_usd` set and not 0):

- Before the check, the command reads the spend from the transcripts exactly as
  `status --refresh` does (`cost_rows(repo, d, d.host, foreman_uuid(d))`) and records it with
  `record_costs` (the batch's `spent_usd`, `unpriced`, each CR's `cost_usd`/`cost_unpriced`, a
  `cost` event), plus the paused-batch summary rewrite `_refresh` does today. Factor the spend
  half of `commands/batch_status.py` `_refresh` into one function that `status --refresh` and
  every check point call, so there is one code path for "refresh the spend".
- The refreshed figure is recorded even when the command is then refused on the budget (so
  `status` after a refusal shows the figure the refusal used). Read the transcripts outside the
  `changes_lock`/`RenderedBatch` session that does the command's own work, as `_refresh` does
  today, so the lock is not held while the transcripts are parsed; record the figure in its own
  short session (or in the command's, if it is written before the refusal is raised: the
  Driver's choice, as long as a refused command still leaves the refreshed figure on disk).
- The check then reads the refreshed `spent_usd` (`over_budget`, unchanged).
- The refusal messages stay as they are (`budget spent: <spent> of $<budget>; only the user
  raises it (`order budget`)`, exit 5; `release`'s `no: the budget is spent (...)`, exit 5).
- When the refresh itself fails (any `ChantierError` from `cost_rows`/`foreman_uuid`: no Foreman
  transcript recorded, no priced calls, an unreadable transcript), the command does not stop on
  it: the check runs on the last recorded figure, and the command's output carries one extra line
  `spend not refreshed: <the error's text>; budget checked on <spent_text> (<age>)`, where
  `<age>` is the age text of section 2. (See open question 1: this is the default the spec
  takes; the request's alternative was to refuse.)
- With no budget (`budget_usd` None or 0) nothing is refreshed: no check applies, and the
  commands stay as fast as today. `round` with no budget stays "unchanged whatever the spend".
- The commands that are never refused for the budget (`gate`, `verdict`, `ship`, `note`,
  `handback`) do not refresh.
- The board's `next_to_start` / `status/words.py` display logic keeps reading the stored figure
  (it is a reading, not a check); it is now fresher because each check writes it.

The spend of a direct batch (steered by the Chief of Staff) is refreshed the same way: the same
`cost_rows` call already covers the steering transcripts.

### 2. The spend's age is recorded and shown (absorbs `status-spend-age`)

- `core/records.py` `BatchRecord`: a new field `spent_at: str | None = None`, the UTC timestamp
  (`core.clock.now()`) of the last write of `spent_usd`. `record_costs` sets it, so every writer
  sets it: `status --refresh`, `pause`, `close` (`commands/closing.py`) and the new check points.
  A record from before the change has no `spent_at`: it reads as None.
- `status` (`commands/batch_status.py` `_batch_line`): after the spend and the budget, the
  figure's age, from `core.clock.age_minutes(d.spent_at)`:
  `spent $0.82 of $20, 12 min old` (rounded minutes, as the heartbeat's age is).
  When the spend is `unknown`, nothing is added. When `spent_usd` is set but `spent_at` is None
  (an older record): `, age unknown`. A paused batch keeps its ` (paused, cost to date)` after it.
- `STATUS.json` (`status/views.py` `batch_view`): a new key `spent_at` beside `spent_usd`; the
  dashboard's per-batch entry (`dashboard_view`) carries it too.
- The batch's `STATUS.md` (`status/markdown.py` `batch_markdown`): after the spend, ` as of
  <spent_at>` when `spent_at` is set and the spend is priced (the file already shows its own
  `Updated` time, so a reader sees the gap).
- The CR board pane (`hooks/register.tsx`), `types/index.d.ts` and the web board
  (`board/state.py`, `board/web/js/...`) do not change in this CR (see Out of scope).

### 3. Cards

- `skills/chantier/references/concepts.md`, "Slots, budget, rounds": "`take` and `round` are
  refused (exit 5) once the budget is spent, on the last recorded spend" becomes: refused once the
  budget is spent, on the spend each of them refreshes from the transcripts first (when the batch
  has a budget); `order qa`, the Foreman's granted fix and `release go` check the same refreshed
  figure; when the transcripts cannot be read, the check uses the last recorded spend and the
  command says so.
- `skills/chantier/references/status-layout.md`, Progress, "Header line": the spend is copied as
  `status` prints it, without its age (`, <n> min old`): a report runs right after
  `status --refresh`.
- `skills/chantier/references/foreman.md` and `driver.md`: no change is needed (their budget
  refusals and exit codes stay); the Driver checks and adjusts any sentence there that says the
  budget reads the "last recorded" spend.
- The docstrings of `rails.check_budget` ("the spend is the last recorded one") and `cost`
  (`commands/cost/command.py`: "`status --refresh` and `pause` record it") are updated to say
  the check points record it too.
- Card changes on the agent files: none (`agents/` and `com.github.copilot/agents/` are untouched).

### 4. Close the absorbed item

`2-backlog/P3/status-spend-age` is closed with this CR, as the request says (its request is
carried here, section 2): planning work, not the Driver's. The Chief of Staff runs
`$CHANTIER abandon 2-backlog/P3/status-spend-age` (the request is the user's word for it) when
this CR is delivered; the PR does not touch the planning folder.

## Decisions carried from `02-answers.md`

- The request's scope stands as written (the user, 2026-11-15: planned with the eval study's 19
  kept points, in one parallel batch before the release). Its two parts are both here: the spend
  refreshed where the budget is checked (section 1), and its age shown (section 2), absorbing
  `status-spend-age` (section 4).
- The request's "refresh ... (or refuse on a stale figure)": the spec takes the refresh, as the
  primary wording; refusing on staleness applies only to the refresh's failure, which is open
  question 1.
- Implementation detail is the agents'.

## Out of scope

- The CR board pane (`hooks/register.tsx`) and `types/index.d.ts`: no age shown there (it would
  need `just mod` and a screenshot from a real session; see open question 2).
- The web board (`chantier board`): its batch, home and costs views keep showing `spent_usd`
  without its age; its live cost reading (`board/costs.py`) is unchanged.
- A throttle (skip the refresh when the figure is younger than N minutes): not added; measured
  instead (see Evidence). A follow-up item if the measure shows a cost.
- Any change to how the spend is priced or split (`cost_rows`, `cost_groups`, the Chief of
  Staff's lines outside the budget).
- The heartbeat refresh (`status --refresh --epoch`) and its cadence.

## Evidence

Checks (`just check`, on Linux, macOS and Windows; `just test` stays within its time limit):

- `skills/chantier/scripts/cli/tests/test_rail_refusals.py` (parametrized, in-process, on a
  prepared state with transcripts whose priced spend is known, as `test_cost_reading.py` builds
  them): for `take <cr>`, `take stack`, `round`, `order qa`, `order add --fix-for` (own) and
  `release go`, with a budget below the transcripts' real spend and a stored `spent_usd` far
  below the budget, each command is refused with exit 5 and the budget message, and
  `batch.json`'s `spent_usd` afterwards equals the transcripts' spend and `spent_at` is set.
  The same commands with a budget above the real spend pass.
- Refresh failure: with a budget and no Foreman transcript recorded (or no priced call), `take`
  checks on the stored figure (refused when it is over, taken when under) and prints
  `spend not refreshed: ...`.
- No budget: `round` reads no transcript (the state has none and the command passes) and
  `spent_at` is not touched.
- `test_cost_reading.py`: `status --refresh` and `pause` set `spent_at`.
- `status` line: `, <n> min old` with `spent_at` set, `, age unknown` with `spent_usd` set and
  no `spent_at`, nothing when the spend is unknown; `STATUS.json` carries `spent_at`.

Scenario (`just scenario`, the pipeline's `just scenario (ubuntu-latest)` job green at the PR's
head; this is a CLI and cards change):

- The budget steps that inject `spent_usd` into `batch.json` (around `run_scenario.py` lines
  1583, 3031, 3491, 3838, 5207, 6266) now see that figure replaced by the fixture transcripts'
  real spend (1.608 in the step at line 1197) wherever a check point refreshes it. Each such step
  is rewritten to set the budget against the fixture's real spend (for a refusal: a budget below
  it, with a stored `spent_usd` below the budget, which proves the refresh), never by disabling
  the refresh. The step at 3847 (no budget, `round` unchanged whatever the spend) stays as is.
- A new step: a batch with a budget above the stored spend and below the fixture's real spend;
  `take` of a queued CR is refused with exit 5, and `status` then shows the refreshed figure and
  `, 0 min old`.
- `STATUS.json` of the batch has `spent_at` after the refusal.

Measure, in the PR's Deliverables: the time a refreshing `round` adds, on the largest real
transcript set available (batch-18's real-foreman run 2 in `C:/Users/gaeta/Projets/chantier-eval`),
on the user's Windows machine; when it passes a few seconds, the PR's Known gaps names it.

## Open questions for the user

1. When the spend cannot be refreshed at a budget check (no Foreman transcript recorded yet, no
   priced call, an unreadable transcript), should the command refuse (exit 5, "spend unknown:
   <why>"), or check on the last recorded figure and say so in its output? The spec takes the
   second (the batch is not stopped by a transcript problem; the line shows the figure's age);
   the request's "or refuse on a stale figure" suggests the first is acceptable to you.
2. Should the age also appear in the CR board pane of Claude Code and in the web board? The spec
   leaves both out (the pane would need `just mod` and a screenshot from a real session); say if
   you want it here or as a follow-up item.
