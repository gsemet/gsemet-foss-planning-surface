# Change Specification: the cost receipt after a steering switch

Short name: `receipt-switch`. Answers: `02-answers.md` (no grill question; three points settled by
the Chief of Staff). Origin: direct-switch-Q8 of CR-353 (`switch-batch-to-direct`, merged as PR 318
at `bdd27e0f`; its specification is in
`5-archives/261118-1107-353-switch-batch-to-direct/03-change-spec.md`, decision 7 and section 2).

## Goal

When a batch has switched steering (Foreman to direct, or back), the web board's cost receipt
shows the same "outside the budget" figure for the Chief of Staff's steering as the `cost`
command's text. Today the text counts what the Chief of Staff spent steering outside its claim
window (for example during the Foreman's stint, before the switch back to direct), and the receipt
leaves it out because the batch is now direct. Both should come from one computation.

## Decisions carried from the answers

1. After a switch (either way), the receipt's `outside.steering` shows the same figure as `cost`'s
   line `Chief of Staff, steering the batch (outside the budget): ...`: same dollars, same calls,
   same calls not priced, and the same "unknown" when the text says unknown.
2. One source for both: the receipt and the text are drawn from one decision on the Chief of
   Staff's read (`chief_read`'s `_Chief`); no second computation.
3. A test covers a switched batch: the receipt's figure equals `cost`'s.

## The cause, in the code

Both outputs already start from the same read, `chief_read(repo, d)` in
`skills/chantier/scripts/cli/src/chantier/commands/cost/sessions.py` (the board through
`board/costs.py`, `compute`; `close` through `commands/closing.py`, which reads it once and passes
it to both). They part in the rule that decides the steering part:

- The text, `_chief_lines(c)` (sessions.py, lines 157-184), decides from the read alone:
  1. no steering call held outside the windows (`not c.steer.held()`) and `c.untimed` > 0: the
     line says `unknown (<n> calls without a time, not placed)`;
  2. else, steering calls held, or no call inside the claim windows (`not c.inside_calls`): the
     line gives the figure, `spend(steer.usd, steer.calls, steer.unpriced)`;
  3. else (nothing outside, the steering all in the batch's spend): no line.
- The receipt, `chief_outside(d, read)` (sessions.py, lines 223-237), decides first on the
  batch's current steering: `d.steering == "direct"` gives `steering: None` whatever the read
  holds; then `not held and inside_calls` gives `None` before the untimed test; then untimed gives
  `{"usd": None, ..., "unknown": "calls without a time"}`; else the figure.

So on a direct batch with steering calls outside the claim window (a switched batch's Chief of
Staff stint before or between Foreman stints, its calls between `open` and its claim, or an
unclaimed Chief of Staff session of the batch) the text prints a figure and the receipt has none;
and with only untimed calls outside and some calls inside, the text says unknown and the receipt
has none. `d.steering` is the batch's steering now, not what the read found, which is why the
switch (CR-353) made the gap visible.

## What changes

### 1. The CLI: one decision for the steering part outside the budget

File: `skills/chantier/scripts/cli/src/chantier/commands/cost/sessions.py`.

- One function (its name is the Driver's, for example `steer_outside(c: _Chief)`) decides, from
  the read alone, the steering part outside the budget, with the text's three cases above, in the
  text's order: unknown (the untimed count), the figure (`c.steer`), or none. It does not read
  `d.steering`.
- `_chief_lines` draws the `STEER_OUT` line from that function's result. Its printed text is
  unchanged in every case (the existing `cost` tests and scenario steps hold as they are).
- `chief_outside` draws `outside.steering` from the same result: none gives `None`; unknown gives
  today's `{"usd": None, "calls": 0, "unpriced": {}, "unknown": "calls without a time"}`; the
  figure gives `_outside_part(c.steer)`. The test on `d.steering` goes. Whether `chief_outside`
  keeps its `d` parameter is the Driver's call (its callers: `commands/cost/receipt.py`,
  `cost_receipt`, and `tests/test_cost_receipt.py`).
- The receipt's JSON shape does not change: `outside` is `{grill, steering}` or `None` beside
  `outside_unknown`; `steering` is `None`, a figure, or the unknown object, as today.
- Docstrings that say "the steering in a Foreman batch" (`chief_outside`, and
  `commands/cost/receipt.py`'s module and `cost_receipt` docstrings where they describe it) say
  instead: the Chief of Staff's steering outside its claim windows, as the text's line.

Consequence, stated so no one reads it as a regression: on a direct batch that never switched, the
receipt now also shows a steering part whenever the text prints one (Chief of Staff calls after
the batch opened but outside its claim window, or no call at all inside it, where the text prints
`$0.00 ... (0 calls)`). A Foreman batch's receipt changes only in the case where the text says
unknown and the receipt said nothing (only untimed calls outside, some calls inside): it now says
unknown.

### 2. The board

No change of behaviour in the web code: `board/web/js/model/receipt.js` (`outsideOf`),
`views/costs-receipt.js` (`outsideCells`, the `Chief of Staff, steering` line) and
`model/spend-by.js` (`chiefRow`) already show `outside.steering` whenever it is present, whatever
the batch's steering.

- `board/web/js/model/receipt.js`, the comment above `outsideOf` (line 75, "the steering in a
  Foreman batch"): say the Chief of Staff's steering outside its claim windows. A change under
  `board/web/`: the Driver reads `board/web/DESIGN.md` first and keeps it true (it names no such
  rule today).
- Closed batches keep the `cost_receipt` their record kept at close: final, not recomputed.

### 3. Docs

- `docs/web-board.md`, line 94: "what lies outside the budget (the grill and the specifications,
  and the steering in a Foreman batch)" becomes "(the grill and the specifications, and the Chief
  of Staff's steering outside its claim window, the same figure as `cost`'s line)", or close
  words.
- No card changes: `status-layout.md` (line 153) and `chief-of-staff.md` (line 1468) describe the
  text, which does not change. No changelog (the repository keeps none).

## Out of scope

- Any change to `cost`'s text, to the windows (`pricing.steering_windows`), to `cost_rows` or to
  what CR-353 settled about pricing each stint.
- Rewriting the `cost_receipt` of batches already closed.
- The grill part of the receipt (`outside.grill`), unchanged.
- The CR board pane: no `STATUS.json` field changes, so no screenshot is owed.

## Host and default matrix

None: the decision reads the Chief of Staff's read only. On Copilot `chief_read` returns "not
measured on this host" and both outputs say unknown, as today (the existing test
`test_a_chief_of_staff_that_cannot_be_measured_is_null_with_its_cause_never_zero` keeps it).

## Evidence

1. **In-process test on a switched batch** (`skills/chantier/scripts/cli/tests/test_cost_reading.py`
   with its `CostWorld`, or a test beside it, kept within `just test`'s time budget): a batch whose
   record is direct after a switch (claims `uuid-chief`, then a Foreman's transcript, then
   `uuid-chief` again; `steering: direct`), with at least one timed Chief of Staff call outside its
   windows (after the batch opened and before its first claim, or in the Foreman's stint). Run
   `cost` (text) and compute the receipt the board's way (`board.costs.compute(repo)["receipt"]`,
   or `cost_receipt` with `chief_read`): the text's
   `Chief of Staff, steering the batch (outside the budget): $X since the batch opened (N calls...)`
   line and `receipt["outside"]["steering"]` agree on the dollars (to the cent as printed) and on
   `N`; the receipt's `steering` is not `None`. This is the check that fails today.
2. **The one rule, on prepared reads** (`tests/test_cost_receipt.py`, the parametrized
   `test_the_steering_is_outside_the_budget_in_a_foreman_batch_only`, renamed to what it now
   checks): for `steering` in `direct` and `foreman`, and reads covering the three cases (steering
   held; only untimed outside with calls inside; nothing outside with calls inside), the
   receipt's `outside.steering` is the figure, unknown, or `None` exactly where `chief_line(...,
   read)` prints a figure, `unknown (...)`, or no `STEER_OUT` line; the receipt's figure equals the
   text's. Both sides call the shipped functions; the prepared `_Chief` is the input, not a copy of
   the code.
3. **Scenario** (`scenario/run_scenario.py`, unit `direct_batch`, the step "the Chief of Staff
   takes the batch back from the Foreman", around lines 2452-2482). As written today that step
   seeds both Chief of Staff calls inside its windows (`c-s1` at `at(10)`, after the first claim at
   `t1`; `c-s2` after the third claim), so its text may print no `outside the budget` line at all
   (its `all(...)` check passes on an empty list). Seed one more Chief of Staff call outside its
   windows (for example between the opening `t0` and the first claim `t1`, such as `at(-30)`),
   check that the text prints the `outside the budget` line with it (`(1 calls)`), then compute the
   board's receipt in-process with the same probe pattern as the unit's board-state check (around
   line 2533, here `chantier.board.costs.compute`) and check that its `outside.steering` holds the
   same calls and dollars as that line. The step's other checks (the Chief of Staff's own row
   `(2 calls,`, the Foreman's `(1 calls,`) keep their figures.
4. Existing checks that stay green unchanged: `test_cost_reading.py`'s Chief of Staff lines,
   `test_cost_receipt.py`'s other tests, the scenario's `cost` steps.
5. A grep line in the PR's evidence: `docs/web-board.md` no longer says "the steering in a Foreman
   batch".

## Gates (AGENTS.md)

- Before the first push, in the worktree at the rebased head pushed: `just check`, and `just
  eval-dry-run` (a change under the CLI's `src/`).
- Before the PR leaves draft: the pipeline's `just scenario (ubuntu-latest)` job green at the PR's
  head (a change to the CLI and the scenario).
- If this CR is on top of its batch's stack: the local Windows `just scenario` (`chantier gate`) at
  its head before the user merges.
- No `just mod` (nothing under `hooks/` or `types/`). No pane screenshot (no `STATUS.json` field
  changes). A change under `board/web/` (one comment): read `DESIGN.md` first.
- `just test` stays within its time budget (at most 30 s above 18.5 s on the user's Windows
  machine).

## Open questions

None.
