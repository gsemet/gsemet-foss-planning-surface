# Change Specification: systematic-retro

## Goal

In the user's terms:

1. **A retro every time.** A retro comes at each release, and as soon as every CR of a batch is
   merged, whether the batch is then paused or closed. It lists each problem met with its
   long-term fix, one line each. The Chief of Staff offers each point to the user as an inbox
   item.
2. **The Chief of Staff's cost, split in two.** The cost reports no longer show one "Chief of
   Staff (steering)" line that reads as if steering alone cost half the batch (batch-08: $20.54 of
   $40.05). They show two lines, each with its measured cost: "grill and specifications with the
   user" and "steering the batch". A part that cannot be measured is shown as unknown, never
   estimated. The split stays right in a long Chief of Staff session with several compactions and
   across several batches in one session.
3. **How the batch runs, said everywhere.** The report, `status` and the batch's `STATUS.md` say
   who steers the batch (direct mode, the Chief of Staff steering it itself, or a Foreman session)
   and its shape (a stack of PRs, or independent PRs, `--parallel`). On batch-08, steered in
   direct mode, `STATUS.md` and `status` said "steering foreman" and the report said neither.

## Decisions carried from `02-answers.md`

- D1. A retro comes at each release, and as soon as every CR of the batch is merged, whether the
  batch is paused or closed (the user chose "Aussi à cette pause"). Each point is offered to the
  user as an inbox item.
- D2. The cost reports split the Chief of Staff's cost into two lines, each with its measured
  cost: "grill and specifications with the user" and "steering the batch". A part that cannot be
  measured is shown as unknown, never estimated.
- D3. The report, `status` and the batch's `STATUS.md` say who steers the batch (direct mode or a
  Foreman) and its shape (a stack or parallel).
- D4 (the user's warning after the restatement). The split stays right across compactions and
  across batches in one session. What chantier cannot see, such as compactions, is shown as
  unknown with its count when known, never as 0 and never silently left out.

## What is known today (read in the code)

- `skills/chantier/scripts/cli/src/chantier/commands.py`:
  - `_cost_rows` prices each steering transcript in its `_window` (a Foreman's from the batch's
    `created`, the Chief of Staff's from its claim in `foreman_claims`, each to the next claim or
    to now: `pause` ends no window). A Chief of Staff's steering transcript becomes one row of type
    `chief-of-staff`, labelled by `_label` with the constant `STEERING = "Chief of Staff
    (steering)"`. That row counts in `spent_usd` and the budget.
  - `costs.without_spec_writers` drops the Chief of Staff's spec-writer subagents from the
    steering rows; they stay on the `Chief of Staff:` line.
  - `_chief_line` prints `Chief of Staff: $<since> since the batch opened, $<whole> the whole
    session, context <n> tokens`, where both figures leave the steering window out. On Copilot,
    or with no Chief of Staff transcript, it prints `Chief of Staff: not measured`.
  - `_cost_summary` (used by `cost --summary`, `status --refresh` on a paused batch, `pause` and
    `close`) prints the split line, e.g. `Chief of Staff (steering) $20.54 (50%), Drivers ...`,
    and ends with `Not counted: compaction calls, which leave no record (about $0.12 each)`,
    without a count. `cost --explain` gives the count (`COMPACTION_USD`).
  - So, in direct mode, everything the Chief of Staff does in its own transcript after its claim
    (its grill with the user during a pause, its review of specifications, its backlog work) is
    priced as steering, and counted in the batch's spend and budget. That is the batch-08 figure.
  - `status` prints `... <mode> ... steering {d.get('steering', 'foreman')} ...`.
- `skills/chantier/scripts/cli/src/chantier/status.py`: `batch_view` stores `mode` and
  `steering` (default `foreman`), and `batch_markdown` writes the header `Updated … · steering
  <steering> · spent …`, with no shape.
- `skills/chantier/scripts/cli/src/chantier/costs.py`: `usage` reads a transcript record by
  record, deduplicates calls by message id, counts `compact_boundary` records in `compactions`
  and tells turns apart (`_wakes`: a user record that is not only tool results starts a turn).
- The `steering` field was added to `batch.json` by commit e967a31 (direct mode, 2026-11-07);
  batch-08 held the direct-mode CR itself, so it was opened by a CLI that wrote no `steering`,
  and every reader defaulted to `foreman`. That default is the batch-08 defect.
- Retro today: only the Release driver writes `<work folder>/retro.md`
  (`skills/chantier/references/driver.md`, "Release driver"), and the Chief of Staff reads it once
  released and offers each proposal as a CR (`chief-of-staff.md`, "Releases", last sentence).
  A batch without a release has no retro.

## What changes

### 1. The retro (cards; no CLI change)

- **When.** At each pause of a batch (every CR merged or cancelled, `pause` run), and at each
  release (the Release driver's `retro.md`, as today). `close` always follows a pause, so a batch
  closed without a release has had its retro at that pause; `close` adds none. A batch paused,
  given more CRs (`order add`) and paused again gets a new retro at the new pause, covering only
  what ran since the previous one.
- **Who writes it.** The steering session, which saw the batch's problems: the Foreman, before
  `pause` and before its `final` line (after `final` it stays idle, so it cannot write it later);
  in direct mode the Chief of Staff, at its pause.
- **Where.** `4-batch/retro.md` (a name the Claude Code write guard accepts:
  `references/hosts/claude-code.md` already lists `retro.md`). One section per pause, headed with
  the date and the CRs it covers; an earlier section is never rewritten.
- **What.** A Markdown list, one line per problem met: the problem, then its long-term fix
  (`- <problem>: <long-term fix>`). What went wrong or slowly: an ask, a block, a refusal of the
  CLI, a Driver restarted, a red gate or CI, a round past the first, cache expiries or a cost far
  over the others (`cost --explain`), an infrastructure failure. The writer reads `status
  --notes`, `events.jsonl`, the CRs' `work/` notes and `cost --explain`; it judges what is a
  problem. A batch with no problem writes one line saying so.
- **A release in the batch.** The Release driver's `work/retro.md` stays as it is. The batch's
  retro at the following pause names its points by reference ("see the release retro") rather than
  copying them, so the user is offered each point once.
- **The offer.** In the Completion report the Chief of Staff lists the retro's points, numbered,
  and offers each as an inbox item; on the user's word for a point, `$CHANTIER file "<the point>"`
  files it in `1-inbox`. A point that matches an item already in the inbox or the backlog is
  named with that item, not offered twice. The user's answer for each point is recorded as any
  decision is (a point filed has its own CR; a point declined is said so in the conversation).
  The offer is made before `close`: `close` deletes `4-batch/retro.md` with the batch's other
  files.
- **Cards to change:**
  - `skills/chantier/references/foreman.md`, "Your goal": the retro in `4-batch/retro.md`
    before `pause` and `final`.
  - `skills/chantier/references/chief-of-staff.md`: "Steering a batch yourself", "The pause"
    bullet (direct mode: write the retro before `pause`); "While it runs", "The pause" bullet
    (Foreman mode: read `4-batch/retro.md` on `final`); "Releases", last sentence (the release
    retro is offered once, with the batch's); the entry-points table row for `final`.
  - `skills/chantier/references/status-layout.md`, "Completion": a "Retro" part after "what the
    batch did not prove", one numbered line per point; the **For you:** line asks which points to
    file.
  - `skills/chantier/references/concepts.md`, "Batch lifecycle", the paused state: a retro at each
    pause.
- **Docs:** `docs/use-cases-foreman.md` (line 113, "Once the release is out ..."), and the texts
  of the lifecycle diagrams that say a retro comes only from the release
  (`docs/cr-lifecycle-texts.md`, the paragraph and the `📝 retro.md` box) say the retro comes at
  each pause too. The SVGs are changed only where their text changes, with their texts file.

### 2. The Chief of Staff's cost, split in two (CLI and cards)

**What counts as "grill and specifications with the user".** It is measured from the transcript,
call by call, with a rule written in the card so the user knows what the figure holds; nothing is
estimated or apportioned:

- every call of a turn of the Chief of Staff's own transcript (a turn as `costs._wakes` defines
  it: from a wake to the next) in which a tool use names, in its input, a CR folder's
  `01-intent.md`, `02-answers.md`, `03-change-spec.md` or `work/specifying` (writing the intent,
  recording an answer, writing or removing the marker, reviewing a specification), or starts a
  subagent whose type ends with `spec-writer`;
- every call of the Chief of Staff's spec-writer subagents (today on the `Chief of Staff:` line,
  through `costs.without_spec_writers`).

Every other call of the Chief of Staff's own transcript in the batch's window is "steering the
batch". A turn is attributed whole: a turn that both records an answer and runs a steering
command counts as grill and specifications.

**The lines.** In every output that prints the Chief of Staff today (`cost`, `cost --by cr`,
`cost --explain`, `cost --summary`, the `summary` that `status --refresh`, `pause` and `close`
write into `batch.json` and the `## Cost` section of `STATUS.md`):

- Direct mode, in the breakdown, in the spend and the budget as today:
  `Chief of Staff, steering the batch: $<x> (<n> calls)`, the steering window's calls minus the
  grill-and-specifications turns. The `STEERING` label and the split line of `_cost_summary`
  use the same words (`Chief of Staff, steering the batch $<x> (<y>%)`).
- Then, outside the spend and the budget, in this order:
  - Foreman mode only: `Chief of Staff, steering the batch (outside the budget): $<a> since the
    batch opened (<n> calls)`, its own calls since the batch's `created` that are not grill and
    specifications, its other subagents included (as today's `since` figure).
  - Both modes: `Chief of Staff, grill and specifications with the user (outside the budget):
    $<b> since the batch opened (<n> calls, <k> spec-writers)`.
  - Both modes: `Chief of Staff, whole session: $<d>, context <n> tokens; not counted: <k>
    compactions since the batch opened, which leave no record (about $0.12 each)`. The count is
    the `compact_boundary` records of the Chief of Staff's transcripts in the batch's window.
- The two lines add up: in Foreman mode, `a + b` is everything the Chief of Staff's transcripts
  priced since the batch opened; in direct mode, the steering row's own calls plus `b` are. The
  whole-session figure stays one number (it spans other batches).
- **Out of the budget.** In direct mode the grill-and-specifications turns leave the steering
  row, so they leave `spent_usd` and the budget, as the spec-writer already does
  (`chief-of-staff.md`: "The spec-writer takes no slot and no budget of any batch"). A batch's
  spend therefore drops by that amount compared with today's figure.
- **Unknown, never 0.** Where a part cannot be measured it is printed `unknown`, with its cause,
  and the lines that can be measured still print:
  - On Copilot (`copilot_session_costs` has no per-call tool content and no timestamps): the two
    Chief of Staff lines say `unknown: not measured on this host`; a direct batch's steering row
    is labelled `Chief of Staff, steering the batch, grill included (not split on this host)`;
    the compaction count says `compactions: not measured on this host`.
  - No Chief of Staff transcript recorded, or one that cannot be read: `unknown (<cause>)`, as
    `_chief_line` does today with `not measured (<cause>)`.
  - A turn whose records carry no timestamp cannot be placed in the window: its calls are not
    split silently; the line says how many calls were left unplaced (`<n> calls without a time,
    not placed`).
- **Across compactions and batches (D4).** The split reads the transcript's records, which stay
  in the file across a compaction; it depends on no state kept in the session. It is bounded by
  the batch's window (`created`, the claims in `foreman_claims`, now or the close), so a session
  that steered batch-08 and then batch-09 puts each turn in the batch whose window holds it.
  Every Chief of Staff transcript of the batch (`state.chief_sessions`, kept by `seat take`)
  is summed, as today. Calls are deduplicated by message id per transcript, as today.
- **Where in the code:** `costs.py` (`usage` or a sibling reads the tool uses of each turn and
  returns the grill-and-specifications share and the compaction count of the window);
  `commands.py` (`_cost_rows`, `_chief_line`, `_label`/`STEERING`, `_breakdown`,
  `_cost_summary`, `cost`); the constant `COMPACTION_USD` stays a note, never added to a total.
- **Cards:** `status-layout.md`, "Cost": the Chief of Staff's lines by their new names, what
  "grill and specifications with the user" holds (the rule above, in one sentence), `unknown`
  stays `unknown`, the compaction count is said with it. `chief-of-staff.md`: "Steering a batch
  yourself", "Your epoch" bullet (the steering row is now `Chief of Staff, steering the batch`,
  and the grill leaves it); "Backlog and grill" ("its cost is on your line" becomes the grill and
  specifications line); "Compacting" (the context size is on the `Chief of Staff, whole session`
  line); "Subagents and the demo" ("in your line of the cost table" names which line).
  `routing.md` line 20 if it names the row.

### 3. Steering and shape, shown (CLI and cards)

- **Words.** Steering: `direct (the Chief of Staff)` or `Foreman`. Shape: `stack` (a stack of
  PRs) or `parallel` (independent PRs). A `batch.json` without `steering` (opened before
  0.8.0, as batch-08) shows `steering unknown`, never `foreman`: the default `'foreman'` in
  `commands.status`, `status.batch_view` and `status.batch_markdown` goes. The same for `mode`.
- **`status`:** its first line says `steering <steering>` and `shape <stack|parallel>` with
  those words (today it prints the mode bare, among other words).
- **`STATUS.md` of the batch** (`status.batch_markdown`): the header line says both, e.g.
  `Updated … · steered by the Chief of Staff (direct mode) · a stack of PRs · spent …`.
  `STATUS.json` keeps `steering` and `mode`, `null` when unknown.
- **The report** (`status-layout.md`): the header line of a Progress report and of a Completion
  report names who steers and the shape, copied from `status`, never judged.
- When the steering changed during the batch (a Foreman took a direct batch over:
  `commands.foreman` logs a `steering` event), the current steering is shown; nothing more.

## Out of scope

- A Griller's session (a fork the user started): its cost is not in the Chief of Staff's
  transcripts and is not priced here.
- Pricing compaction calls: they leave no record; they stay counted, not priced.
- A per-CR `retro.md` in `5-archives` as the docs diagrams show (`docs/cr-folder-lifecycle-texts.md`,
  "5-archives folder (new: retro.md)"); see the open questions.
- The planning dashboard (`changes/STATUS.md`) and `pause`'s and `close`'s first lines: they do
  not change for the steering and shape.
- Any change to the agent files (`agents/`, `com.github.copilot/agents/`): no role's body changes.

## Evidence

- `just check` passes on Linux, macOS and Windows.
- `just scenario` passes, with new or changed checks in `scenario/run_scenario.py`:
  - The cost section (step 9) and the direct batch (step 16, `direct_batch`): a fake Chief of
    Staff transcript with, after its claim, a steering turn, a turn that writes a CR's
    `02-answers.md`, a turn that starts a `spec-writer`, and a spec-writer subagent. Checks:
    `cost` prints `Chief of Staff, steering the batch` without the grill turns; the `grill and
    specifications with the user` line holds exactly the grill turns plus the spec-writer; the
    two add up to the Chief of Staff's priced calls since the batch opened; `spent_usd` holds the
    steering row only; no line reads `Chief of Staff (steering)`.
  - The same transcript with two `compact_boundary` records inside the window and one before it:
    the whole-session line says `2 compactions`; a call repeated after a boundary (same message
    id) is priced once; the split is the same as without the boundaries.
  - A Chief of Staff transcript spanning an earlier batch: its grill turns before `created` are
    in no line of this batch but the whole-session figure.
  - Foreman mode: the two Chief of Staff lines outside the budget, adding up to its calls since
    the batch opened.
  - Copilot (step 10, `copilot_cost`): the two lines say `unknown: not measured on this host`;
    nothing prints `$0.00` for them.
  - `status` and the batch's `STATUS.md`: `steering direct (the Chief of Staff)` and `shape
    stack` on a direct stack batch, `parallel` on a `--parallel` one; a `batch.json` with no
    `steering` field shows `steering unknown`.
  - The existing checks on `Chief of Staff:` (lines around 712, 721, 930-952, 1035, 2640-2652)
    are updated to the new lines.
- `skills/chantier/scripts/cli/tests/test_costs.py`: a unit test of the turn rule (a turn with
  a tool use naming `02-answers.md` is grill and specifications; a turn without is not).
- Cards and docs: read against this specification by the Inspector; no structure test is added
  for the retro (it is agent behaviour).

## Open questions

1. **Grill turns leave the budget in direct mode.** Moving the Chief of Staff's grill and
   specification turns out of the steering row also takes them out of the batch's spend and
   budget (recommended, as the spec-writer already is). Confirm, or keep them in the budget and
   only label them.
2. **"Steering the batch" in Foreman mode.** In Foreman mode the Foreman steers; the Chief of
   Staff's other calls (reports, relaying orders, backlog work) are named "steering the batch"
   here so that two lines add up. Keep that name, or name that line differently in Foreman mode
   (for instance "following the batch")?
3. **Where the retro lives.** Recommended: `4-batch/retro.md`, offered before `close` and deleted
   with the batch's files; the points the user files survive as inbox items. The docs diagrams
   show a `retro.md` in each archived CR folder instead. Keep the batch file only, or also copy
   the retro into the archive?
4. **A retro point about chantier itself in another project.** Recommended: offered as an inbox
   item of the project like any other, the Chief of Staff saying it concerns chantier. Or should
   such a point be offered as a report to chantier's own repository instead?
