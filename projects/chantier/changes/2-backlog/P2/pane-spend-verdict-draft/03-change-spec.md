# Change Specification: the CR board pane shows the spend's age, the carried verdict and the draft wording

Short name: `pane-spend-verdict`. No tracker issue: the Chief of Staff filed it on 2026-11-15
from the open questions of CR-279, CR-277 and CR-290.

## Goal

What the pane and the web board show should match what the CLI already says:

1. **The spend's age.** `status` says `spent $0.82 of $20, 12 min old`. The pane's batch title
   line, the web board's home batch card and its Batch page show the same figure with no age. They
   gain it.
2. **The draft wording.** The ready line of a `PR in draft` hand-back says the PR's own draft
   state on the forge and the CR (and PR) it waits on. The CR's now line still says
   `PR in draft: <pr> on <base>, waits for <cr>.`, which reads like "this PR is a draft on main".
   It takes the ready line's wording.
3. **The carried verdict.** A verdict carried over a clean rebase gets its own step on the CR's
   page, `Verdict carried from <sha7>`, next to the long gate's `carried from <sha7>` step.

## Already done at `main` (`3a9afc2c`, 2026-11-18): out of scope

- The age in `chantier status` (`commands/batch_status.py` `age_text`), in `4-batch/STATUS.md`
  (`status/markdown.py` `_budget`, `as of <spent_at>`) and in both STATUS.json files
  (`status/views.py`: `batch_view` and `dashboard_view` carry `spent_at`). The web board's Costs
  page already shows `Last computed: <age> ago` (`board/web/js/views/costs.js` `ageLine`).
- The ready line's wording (`commands/driver.py` `_ready_lines`, CR-277).
- `ship`'s `carry` event and its `Carried` step (`status/steps.py` `_carried_note`, `a0918624`),
  whose note `STATUS.md` shows as `- [x] Carried: long gate and verdict from <sha7>`.

## Decisions carried from `02-answers.md`

1. One CR, grouping the three display points of the intake: the spend's age in the pane and the
   web board, the now line in the ready line's wording, a `Verdict carried from <sha7>` step.
2. What `main` already does is scoped out (above).
3. The AGENTS.md pane screenshot rule applies: until the user gives the screenshot, the PR's Known
   gaps names "no screenshot of the pane from a real session".
4. No overlap with CR-369 (`open-empty-batch`, batch-28). It owns `crs_total`, `none yet` and
   `no CR yet`. This CR adds nothing when `spent_usd` is null. Both CRs edit the same functions,
   and whichever lands second rebases on the other.
5. Settled by the spec-writer: the words are the ones the CLI and the board already use. The pane
   reads `spent_at`. The board reads `cost_at`, which already follows the live figure it shows.
   The now line and the ready line share one helper. The verdict step is made from the ready
   hand-back's `verdict_from`, in the form of the long gate's step. No STATUS.json field is added
   and `SCHEMA` is not bumped.

## What changes

### 1. The spend's age

#### The CR board pane (`hooks/register.tsx`, `types/index.d.ts`)

- `types/index.d.ts`, `ChantierBatch`: add
  `/** UTC time of the last write of spent_usd; absent from an older file. */ spent_at?: string | null`.
  Leave `spent_usd`'s type as it is (CR-369's ground).
- `hooks/register.tsx`, `Batch`: the section's title line gains the spend's age, after the gauge,
  in `status`'s words:
  - `spent_usd` set and `minutesSince(b.spent_at, now)` known: ` · <n> min old`, for example
    `batch-28  $0.82 / $20 █░░░░░░░░░ · 12 min old`;
  - `spent_usd` set, `spent_at` absent, null or unreadable: ` · age unknown`;
  - `spent_usd` null (or undefined): nothing is added. CR-369's `none yet` title line for an
    empty batch therefore stays exactly as CR-369 draws it.
  The age is computed at each draw from the pane's `now`, so it grows between two checks with no
  file change. A paused batch (folded) shows it too: its title line is where its cost stays.
- `docs/boards.md`, "How to read it": "each batch has a line (its id, its cost against its budget,
  a gauge)" becomes "(its id, its cost against its budget, a gauge, and how old that cost is:
  `12 min old`)".

#### The web board (`skills/chantier/scripts/cli/src/chantier/board/web/`)

Read `board/web/DESIGN.md` first and keep it true. No rule changes: the new words go through
`t()`, the layout uses existing classes and tokens, and no component is restyled.

- The age is that of the figure shown. The board lays the live figure over the recorded one
  (`js/model/live.js` `withLive`, which also sets `cost_at` to the live reading's time), so the age
  reads `batch.cost_at`, which `board/state.py` `_batch` already sends (the last `cost` event, the
  one `record_costs` logs with each `spent_at`). No server change.
- New keys in `js/i18n/en-batch.js` and `js/i18n/fr-batch.js` (the two files must share their
  keys, `test_code_targets.py`):
  - `batch.spent_age`: en `computed {age} ago`, fr `calculé il y a {age}` (the Costs page's words,
    `costs.computed`);
  - `batch.spent_age_unknown`: en `age unknown`, fr `âge inconnu`.
- One small helper, shared by both views (in `js/views/` or `js/model/`, the Driver's choice): the
  age text of a batch, given `state.now`. With `spent_usd` null it gives nothing. With
  `age(batch.cost_at, now)` known it gives `batch.spent_age`, else `batch.spent_age_unknown`.
- Home page, batch card (`js/views/home-batch.js` `figures`): under the Spent figure (after the
  meter), one muted line with that text. Nothing when the helper gives nothing.
- Batch page (`js/views/batch.js` `figures`): the Spent kpi's sub becomes
  `of $20 · computed 3 min ago` (`batch.of_budget`, then ` · ` and the helper's text when there is
  one).
- Not touched: the Costs page (already done), the closed record's figures (`recordFigures`: a
  final cost has no age), the surface overview (`views/overview.js`; see the open question).
- Keep every script at 300 lines at most (`test_code_targets.py`).

### 2. The draft wording of the now line (`status/words.py`, `stacks.py`, `commands/driver.py`)

- One helper builds the clause the ready line ends with today, `<own> is <state>; it waits <what>`,
  from the record. Move it out of `_ready_lines` into `stacks.py` (or `status/words.py`), for
  example `draft_clause(d, c, repo, prepared) -> str`:
  - `<own>`: `the release PR <pr>` for a prepared release (`c.kind == "release"` with a PR), else
    `its PR <pr>`;
  - `<state>`: `a draft on the forge`, `out of draft on the forge`, or
    `of unknown draft state (draft not read: ship <cr> <pr>)`, from `c.pr_draft`;
  - `<what>`: from `draft_waited`: `on <cr> (<its pr or 'no PR yet'>)`,
    `on the branch <b> (no CR of this batch)`, or `for its turn out of draft`.
  `_ready_lines` calls it, and its output does not change by one character (the scenario's
  checks at `run_scenario.py` ~5733 and ~7509 hold as they are).
- `notify()`, the PR in draft branch: the now line becomes `PR in draft: <clause>.`, for example
  `PR in draft: its PR https://…/pull/12 is out of draft on the forge; it waits on CR-3 (https://…/pull/11).`
  The forge's base is no longer printed there, and `notify` no longer calls `pr_base_of`. The PR
  named is the one the record holds (`c.pr`, as the ready line does). The next line is unchanged
  (`Ready to merge once what is under it is and the PR is out of draft.`). The `Ready to merge`
  and `Ready locally` lines are unchanged.
- Readers: the CR's `STATUS.md` (`**Now:**`), its `STATUS.json` `now`, and the pane's CR page
  (`Now: …`). No code change in the pane.
- The labels (`🟤 PR in draft, waits for <cr>`, `state_label`) are unchanged.

### 3. The carried verdict's step (`status/steps.py`)

- `step_entries`, a ready `handback` event: after the `Long gate` step that `event_step` gives
  (exempt, waived or `carried from <sha7>`) and before `Handed back`, add
  `("Verdict", f"carried from {str(e.verdict_from)[:7]}", "")` when the event has `verdict_from`.
  The hand-back records `verdict_from` whenever the verdict carried, whether `ship`'s `carry`
  event proved it or the hand-back did (`commands/driver_checks.py` `_verdict_missing` and
  `GateBasis.event_keys`), so this is the one source.
- The result, for a CR handed back over a clean rebase with both carried:
  - `STATUS.md`: `- [x] Long gate carried from abc1234`, `- [x] Verdict carried from abc1234`,
    `- [x] Handed back`;
  - the pane's CR page, Steps table: `Verdict | yes | carried from abc1234`, as for `Long gate`.
- A CR handed back on its own `VERIFIED` verdict gets no such step (no `verdict_from`). A release
  CR records no verdict, so it gets none either. `ship`'s `Carried` step is unchanged.

### Cards

No card changes. `status-layout.md` already says `carried from <sha7>` is not a gap. No card
quotes the now line. The agent files (`agents/`, `com.github.copilot/agents/`) are not touched.

## Host and default matrix

The pane exists only on Claude Code. On Copilot only the STATUS files and the web board change,
in the same way. Nothing depends on a configured value. No other matrix.

## Out of scope

- CR-369's empty batch: `crs_total`, `none yet`, `no CR yet`.
- Drawing the steps' notes in the pane (`Note` column). With the new step, the carried head
  already shows in the Verdict column.
- The web board's events list (`js/model/events.js`, `board/state.py` `EVENT_KEYS`): the `carry`
  event keeps showing as its kind, and the ready hand-back shows no `verdict_from`.
- The surface overview's Spent column (open question 1).
- Any change to how the spend is priced or refreshed, to `ready_word`, or to the labels.
- A STATUS.json `SCHEMA` change.

## Evidence

Checks (`just check`, Linux, macOS and Windows; `just test` stays within its time limit):

- pytest, in-process, beside the existing tests of the steps and the words (for example
  `test_cli_units.py`), parametrized and few:
  - `step_entries` on a ready `handback` event with `gate_from == verdict_from == a`: the steps are
    `Long gate | carried from a7`, `Verdict | carried from a7`, `Handed back`. With only
    `verdict_from`: no `Long gate` step, then `Verdict | carried from …`, then `Handed back`. With
    neither: `Handed back` alone.
  - `notify()` for a CR whose word is `PR in draft`, parametrized over `pr_draft` True, False and
    None and over a waited CR with a PR, with none, a non-CR branch, and no wait: the now line
    equals `PR in draft: ` + the same clause `_ready_lines` prints, plus `.`, and contains no
    `on <base>,`.
- `hooks/register.test.tsx`, against the shipped `hooks/register.tsx`, beside "a paused batch is
  folded, with its cost on its title line": with the mocked clock, a batch with `spent_usd: 5.07`
  and `spent_at` twelve minutes before the clock shows `12 min old` on its title line; with no
  `spent_at`, `age unknown`; with `spent_usd: null`, neither.
- `just mod` passes (it covers `hooks/` and `types/`); the Driver runs it before the PR.
- The web board: `test_code_targets.py` (both word files share their keys, scripts within 300
  lines) and `test_board_design.py` pass on the shipped files. If the board's tests render these
  views, one case reads the shipped `en-batch.js` / `fr-batch.js` and checks the home card's and
  the Batch page's age text. Otherwise the PR's Deliverables carry one screenshot of the home card
  and one of the Batch page, at the head, in en.

Scenario (`just scenario`; the pipeline's `just scenario (ubuntu-latest)` job green at the PR's
head; the Driver runs `just check` and `just eval-dry-run` in its worktree before the first
push):

- Section 12f (`gate_carry`, ~line 5127, after the clean CR's `handback ready`): the CR's
  `STATUS.json` `steps` hold `{"name": "Verdict", "verdict": "carried from <old7>"}` after the
  `Long gate` `carried from <old7>` step and before `Handed back`, and its `STATUS.md` has
  `- [x] Verdict carried from <old7>`.
- The stacked-by-hand check (~line 5728-5736): `own_md` no longer holds `on {pb}, waits for {p}`.
  It holds `**Now:** PR in draft: its PR {qlink} is out of draft on the forge; it waits on {p} ({plink}).`,
  that is `out[1]`'s text after `{q} PR in draft: `, plus `.`. The check's title says the now line
  takes the ready line's wording.
- The spend-age check that CR-279 added (~line 3156-3162: `take` refused, then `status` shows
  `, 0 min old`, and the batch's own `STATUS.json` has `spent_at`): it also checks that the
  planning folder's index `STATUS.json` (the pane's source) has the same `spent_at` in that
  batch's entry. The scenario has no pane step.

The pane, on a real session (AGENTS.md): the PR's Deliverables carry one screenshot of the pane
from a real Claude Code session running the PR's head, captioned with the head's seven-character
SHA. It shows a batch title line with its age, and if it can, a CR page with the
`Verdict | carried from` step or the new now line. Until then the PR's Known gaps names "no
screenshot of the pane from a real session".

## Open questions

1. The web board's surface overview (`views/overview.js`, one row and card per project) also
   shows each project's Spent figure. Should it show the age too? That needs `board/state.py`
   `project_line` to carry the batch's `cost_at`. This spec leaves it out: the home card and the
   Batch page are where one project's batch is read. Default if no answer: left out.
