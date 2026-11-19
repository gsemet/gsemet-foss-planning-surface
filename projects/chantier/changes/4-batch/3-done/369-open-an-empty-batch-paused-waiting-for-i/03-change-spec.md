# Open an empty batch, paused, waiting for its first CR

Short name: `open-empty-batch`. No tracker issue (verbal, the user, 2026-11-18).

## Goal

The user gives the go for a new batch (and its Foreman) before its first CR is specified. Today
`chantier open` refuses with no CR (`items` is `nargs="+"`), so the batch, its Foreman and its stack
wait for the first spec. Wanted: `chantier open` with no CR opens the batch directly paused; CRs
join it with `order add` as their specs become ready, and the first `take` sets it running, as for
any paused batch.

Scope, per `02-answers.md` answer 2 and the spec critic's section: this CR only makes the empty
paused batch, with its display in the CLI, the pane and the web board, in one CR. The wider
"factory" concept (ready CRs joining a batch that stays open on their own, the README section) is
the CR `ready-joins-waiting-batch`, stacked on this one. Here: no auto-join, no batch that stays
open by itself, no README "factory" section. Wording that calls such a batch "a factory batch" is
that CR's.

## Decisions carried from `02-answers.md`

1. `chantier open` with no CR is accepted: the batch is numbered, its record (`batch.json`,
   `events.jsonl`), `brief.md` and STATUS files are written, and it is born `paused`, with no CR.
2. Every option of `open` keeps its meaning: `--slots`, `--budget`, `--mode`, `--direct`,
   `--default-branch`, `--remote`, `--autonomous-releases`, `--grant-fixes`. `--release N` with no
   CR is refused, with the reason that it names an item and there is none.
3. No new flag: no CR given is the empty batch. The output says the batch is paused with no CR and
   names the next step: `order add` for each CR, then start the Foreman (direct mode: `take`).
4. It is the same paused state as a batch whose last CR ended: `order add` joins it and leaves it
   paused; the first `take` sets it running. Nothing new in that path.
5. One batch per project still holds: a second `open` is refused as today, naming the empty batch.
6. Foreman mode: the Chief of Staff may start the Foreman right after an empty `open`. The Foreman
   claims its epoch and waits, with no Driver to start, until an order arrives; it is ready, not
   done. Its cards say so.
7. `close` of a batch that never held a CR is accepted: it archives no CR, its cost is the steering
   spent, and its record and retro say "no CR".
8. `status`, the board and the CR board pane show the empty batch as paused, "no CR yet". The
   watcher refuses a paused batch as today; once the first `take` sets it running, it starts as
   usual.
9. The Chief of Staff's plan for an empty batch shows the mode, slots, budget, team and who steers;
   the floor and the delivery time are "none yet: no CR".
10. A batch opened empty and never steered (no Foreman claimed, no `take`) that the user asks to
    close: `close` accepts it; its cost reads "none: no session steered it", never $0.00. No Known
    gap.
11. `--autonomous-releases N` and `--grant-fixes` with no CR keep today's refusal (they need
    `--release`); the grant comes later with `order add --release`, then `order grant`, as today.
12. Direct mode on a batch opened empty: the Chief of Staff claims the batch (its epoch) just
    before its first `take`, not at `open`, so the wait costs the batch nothing. A Foreman claims
    at its start as today; the wait of a Foreman with no CR counts in the batch's spend.
13. One CR, as specified: the pane and web-board display ship with the CLI part; the pane
    screenshot stays a Known gap until the user gives one.

## What changes

### CLI: the parser (`skills/chantier/scripts/cli/src/chantier/declare/opening.py`)

- `items`: `nargs="*"` instead of `"+"`. Help text: "path to a prepared CR folder or
  specification; none opens the batch paused, with no CR (`order add` joins CRs to it)".
- The command's one-line description: "open a batch: each prepared CR gets its folder, and a branch
  and worktree name; with no CR the batch is born paused".

### CLI: `open` (`commands/opening.py`, `commands/opening_record.py`)

- `release_grant(args)`: with `args.release` set and `args.items` empty, refuse (`EXIT_USAGE`):
  `--release N names the release CR among the CRs given, and none is given: add it later with
  `order add --note <folder> --release` (then `order grant`)`. With items, the current check
  (`1 <= N <= len(items)`) is unchanged.
- `--autonomous-releases` and `--grant-fixes` keep their meaning, which is "need `--release`"
  (decisions 2 and 11): with no CR they are refused by the existing rule ("need --release"),
  since `--release` cannot be given; the grant comes later with `order add --release`, then
  `order grant`.
- `open_batch`: with no items, everything runs as today (configuration read, settings, the
  `check_no_open_batch` rail under `changes_lock`, the record created through `RenderedBatch`,
  `brief.md`, the `open` event with `crs=[]`), then, still inside the `RenderedBatch` block, the
  record is set paused **without pricing** (there is nothing to price and no steering transcript
  yet, so `record_pause`'s `cost_rows` would only fail):
  - `status = "paused"`, `paused = now()`, `heartbeat_stopped = paused`;
  - `spent_usd` stays `None`; `summary = ["Spent: none yet (no CR)"]` (never `$0.00`, never
    "unknown");
  - an event `pause` with `trigger="open, no CR"` (the same event kind `record_pause` logs, so
    every reader of pauses sees it).
  Put this in one small helper next to `record_pause` in `commands/closing.py` (for example
  `record_born_paused(b)`), so the paused state is set in one module.
- `_brief_text`: with no CR, the "CRs, in order" line reads `- CRs, in order: none yet (born
  paused; \`order add\` joins them)`.
- Output, with no CR (decision 3), in this order:
  1. `opened <batch> on <host>: no CR, paused, <slots> slots, <mode>, steering <steering>`
  2. Foreman mode: `next: complete the brief <brief path>, then \`order add --note <folder> --batch
     <batch>\` for each CR, then start the Foreman`. Direct mode (`--direct`, decision 12):
     `next: complete the brief <brief path>, then \`order add --note <folder> --batch <batch>\`
     for each CR; claim the batch, then \`take\``.
  With CRs, the output is unchanged.
- The existing refusals stay, with the empty batch counted as an open batch:
  `check_no_open_batch` already names it (`<batch> is not closed (a paused batch stays until
  close)...`). No change there.

### CLI: what already works and must keep working (decision 4)

- `order add --note <folder> --batch <batch>` on the paused empty batch: `_reopen` in
  `commands/orders.py` leaves it paused and prints `<batch> stays paused: the first \`take\` sets
  it running again`. No change.
- `order add --release` on it: `commands/orders_release.py` adds the release CR with the default
  grant. No change.
- The first `take`: `commands/driver.py` sets it running (`<batch> was paused: running again`).
  No change.
- `pause` on it: refused as today (already paused). No change.
- `foreman set` / `foreman transcript` with `--batch <batch>` on a paused batch: `resolve_batch`
  returns the batch given; the Foreman's prompt always carries `--batch <batch>`, and the Chief of
  Staff's claim in direct mode passes it too. No change.
- `end_of_batch` (`commands/endpause.py`) returns early on a paused batch: an empty batch is never
  paused twice nor cleaned. No change.
- The forge hub and `watch` (`hub/cycle.py`) do not follow a paused batch (decision 8). No change.

### CLI: the spend of an empty batch

`spent_text` (`rails.py`, around line 262) prints `unknown` when `spent_usd` is `None`. For a batch
that holds no CR (`not d.crs`) and has `spent_usd is None`, it prints `none yet` instead. Every
reader that goes through it, or shows the same figure, says `none yet` for such a batch:

- `chantier status`'s batch line (`spent none yet`);
- the header of `4-batch/STATUS.md` (`status/markdown.py`, the spend shown around line 111);
- the pane's title line and the web board's home card (below).

Once a CR has joined, or a priced refresh has recorded a spend (a Foreman waiting with no CR does
spend, decision 12, and `close` prices it), the figure is shown as today.

### CLI: `close` of a batch that never held a CR (decisions 7 and 10)

- `close` (`commands/closing.py`, `commands/close_archive.py`) accepts a paused batch with
  `d.crs == []`: nothing is archived (`0 CRs archived`), no worktree or branch is listed, and the
  final cost is the steering spent, priced from the steering transcripts recorded (`foreman
  transcript`) as today.
- The close record (`5-archives/batches/batch-NN.md`, written by `_close_files` / `write_close`):
  its CR table or list says `no CR` instead of an empty table; `batch-NN.json` holds `"crs": []`.
- The retro: when `4-batch/retro.md` is absent (`read_retro` returns `None`) and the batch never
  held a CR, the record's retro section says `no CR`. A retro written by the Foreman is kept as
  written.
- A batch that never held a CR and that no steering session ever claimed (decision 10: no
  `foreman transcript` recorded, so `foreman_uuid` raises `no Foreman transcript recorded`):
  `close` accepts it instead of refusing. Nothing is priced. The batch's spend, and only it, reads
  `none: no session steered it`, never `$0.00` and never "unknown": the steering/Foreman rows and
  the total of `cost_summary` in the preview and the done lines, the receipt (`cost_receipt`),
  and in `batch-NN.md` the same lines; in `batch-NN.json` `cost_usd` stays `null`
  (`core/batch_records.py`, line ~74) with that cause recorded beside it (the field the record
  already uses for an unpriced cause, else a new one). The Chief of Staff's lines outside the
  budget (`chief_line`, `commands/cost/sessions.py:219`: grill, steering outside the claim
  windows, whole session) stay as today.
- The refusal stays for every other case where nothing can be priced (a batch that held a CR, or
  a steering transcript recorded but unreadable or with no priced call): "never a false $0.00" is
  unchanged there.

### CLI: `status` and STATUS files (decision 8)

- `chantier status` (`commands/batch_status.py`, `_batch_line`): for a paused batch with no CR
  at all (`not d.crs`), the line reads `... spent none yet ... (paused, cost to date), no CR yet`,
  and one more line follows: `no CR yet: \`order add --note <folder> --batch <batch>\` joins one`.
- `4-batch/STATUS.md` (`status/markdown.py`): the header's spend says `none yet`; under
  `## Paused`, a line `- No CR yet.` when the batch never held a CR.
- `STATUS.json` (planning folder's index, `status/views.py`, `dashboard_view`): each batch entry
  carries `crs_total` (the number of CRs the batch ever held, `len(d.crs)`), because its `crs`
  lists only the active ones and cannot tell "no CR yet" from "every CR ended". It is an optional
  added field: **no `SCHEMA` bump** (the pane refuses any other schema, `hooks/register.tsx:306`;
  CONTRIBUTING.md line ~142, `schema` 3). The batch's own STATUS.json (`batch_view`) already holds
  `"crs": []` and `"state": "paused"`; it gains the same `crs_total` for the web board.

### The CR board pane (`hooks/register.tsx`, `types/index.d.ts`)

- `types/index.d.ts` (line ~45, `ChantierBatch`): add `crs_total?: number` (optional: an older
  STATUS.json has none). `spent_usd` is already read through `money()`, which takes `null`.
- `hooks/register.tsx`, `Batch`: a paused batch is folded (`shown = b.state !== 'paused'`), so its
  title line carries the words: for `state === 'paused'` and `crs_total === 0`, the title line is
  `<batch>  none yet<budget> · paused, no CR yet` (the spend reads `none yet` in place of
  `money(null)`'s `-`; no gauge while nothing is spent). Unfolded, its body shows `No CR yet.`
  (dimmed) in place of the two empty sections. A batch without `crs_total` is drawn as today.
- `hooks/register.test.tsx`: one case beside "a paused batch is folded, with its cost on its title
  line": a paused batch with `crs_total: 0` and `spent_usd: null` shows `none yet` and
  `paused, no CR yet` on its title line; one with `crs_total: 2` and no active CR does not.
- `hooks/` and `types/` change: run `just mod` before the PR (AGENTS.md); it covers both.
- AGENTS.md rule (decision 13): this changes what the pane draws and a `STATUS.json` field it
  shows, so the PR's Deliverables carry one screenshot of the pane from a real Claude Code session
  running the PR's head, captioned with the head's seven-character SHA; until then the PR's Known
  gaps names "no screenshot of the pane from a real session".

### The web board (`skills/chantier/scripts/cli/src/chantier/board/web/`)

Read `board/web/DESIGN.md` first and keep it true. The batch payload the board reads carries
`crs_total` (above).

- Keys, in `js/i18n/en-batch.js` and `js/i18n/fr-batch.js`:
  - `batch.no_cr_yet`: en `Paused, no CR yet: order add joins one.`, fr `En pause, aucune CR
    encore : order add en ajoute une.`
  - `batch.spent_none_yet`: en `none yet`, fr `rien encore`.
- The Batch page (`js/views/batch.js`): for the batch in `4-batch/` with state `paused` and
  `crs_total === 0`, show the page's empty state (`empty(t('batch.no_cr_yet'))`, `ui/parts.js`)
  in place of the graph, Gantt and time-card panel. The breadcrumb chip (`ui/header.js`,
  `shownBatchChip`) already shows the paused state; no change there.
- The home page's batch card (`js/views/home-batch.js`, `batchBlock` and `figures`, lines ~54-61):
  for such a batch, the head is unchanged (id, `paused` tag, mode, steering); the bar and its
  legend are replaced by one line `t('batch.no_cr_yet')`; the four figures stay, with: Spent
  `t('batch.spent_none_yet')` and no meter (budget still shown after `/`), Slots `0/<total>`, the
  steering sign `—` (not marked late: nothing is due while no CR is held), Opened as today.

### Cards

- `skills/chantier/references/concepts.md`, "Batch lifecycle" (line ~270, step 1 "Running:
  `open` creates the batch, running"): add that `open` with no CR creates the batch **paused**,
  with no CR: no cost to show, no retro, no close offer at that pause (steps 3 and 4 do not apply
  to it); `order add` joins CRs and the first `take` sets it running, as in step 3.
- `skills/chantier/references/chief-of-staff.md`, "Starting a batch":
  - Step 2 (the plan): a go given before any CR is ready makes an empty batch; its plan shows the
    mode, slots, budget, the team and who steers, and says for the floor and the delivery time
    "none yet: no CR" (decision 9). No cut is proposed.
  - Step 3 (open): `$CHANTIER open` with no folder opens the batch paused, with no CR; `--release`
    is refused then (the release CR joins later with `order add --release`). CRs join it with
    `$CHANTIER order add --note <folder> --batch <batch>` as their specs become ready; each one
    is planned as a CR joining a paused batch is today. The code block shows the folders as
    optional: `$CHANTIER open [<prepared-folder>…] ...`.
  - Step 4: in Foreman mode you may start the Foreman right after an empty `open`; it claims its
    epoch, sends `ready <batch>`, and waits for the first order; its wait counts in the batch's
    spend. Heartbeat per the host matrix below.
- `skills/chantier/references/chief-of-staff.md`, "Steering a batch yourself", "Your number as
  Foreman" (line ~1486): on a batch opened empty, claim it (`foreman set`, `foreman transcript`)
  just before your first `take`, not at `open`, so the wait costs the batch nothing (decision 12);
  the rules re-read follows that claim as for any claim.
- `skills/chantier/references/foreman.md`:
  - Beside "An order that adds work leaves the paused batch paused" (line ~70): a batch born paused
    with no CR is the same paused batch. After your claim, the brief and the rules, send
    `[foreman→chief-of-staff] ready <batch>` and wait: no Driver to start, no retro, no `final`,
    no `pause`. You are ready, not done. The first order's line starts your turn; your first
    `take` sets the batch running.
  - Heartbeat bullet: while the batch is paused with no CR, arm no heartbeat (nothing can move);
    the turn that takes the first CR arms it.
- `skills/chantier/references/hosts/copilot.md`, "Heartbeat": for a batch born paused with no CR,
  the Chief of Staff does not send `/every` on `ready <batch>`; it arms it with the first order it
  sends the Foreman, as it already does after a heartbeat ended. In direct mode, the Chief of Staff
  runs no `/every` until its first `take`.
- `skills/chantier/references/hosts/claude-code.md`, "Heartbeat": one sentence: on a batch born
  paused with no CR, the steering session (the Foreman, or the Chief of Staff in direct mode) arms
  the loop only in the turn of its first `take`.
- The agent files (`agents/`, `com.github.copilot/agents/`) are not touched: the contract lives in
  the cards.

### Docs

- `docs/batch-lifecycle-texts.md` and `docs/batch-lifecycle.svg` (kept in step, as CONTRIBUTING.md
  says for these pairs): "Into running" gains the empty path: `chantier open` with no CR creates
  the batch paused, with no CR; `order add` joins CRs and the first `take` sets it running. The
  page's first paragraph gets the same sentence.

## Host and default matrix

Only the heartbeat and the claim's moment depend on the host or the steering; nothing depends on a
configured value.

- Claude Code, Foreman mode: the Foreman claims at its start; it arms no `/loop` while the batch is
  paused with no CR, and arms it in the turn of its first `take`.
- Claude Code, direct mode: the Chief of Staff claims just before its first `take`; it arms the
  loop in that turn.
- Copilot, Foreman mode: the Foreman claims at its start; the Chief of Staff sends no `/every` on
  `ready <batch>` of an empty batch, and sends it with the first order.
- Copilot, direct mode: the Chief of Staff claims just before its first `take` and runs no
  `/every` until then (unproved, as the host reference already says of direct mode).

## Out of scope

- The factory behaviour (`ready-joins-waiting-batch`): CRs joining by themselves, a batch that
  stays open, its README section.
- Any change to `order add`, `take`, `pause`, the watcher or the forge hub.
- A new flag for `open`.
- Any change to the one-batch-per-project rule.
- A `STATUS.json` schema change.

## Evidence

Tests (`skills/chantier/scripts/cli/tests/`, in-process, parametrized, few; mostly in
`test_opening_and_restore.py` and `test_rail_refusals.py`):

1. `open` with no item, parametrized over `--direct` and Foreman mode and over `--mode`: exit 0;
   `batch.json` has `status: paused`, `crs: []`, `paused` set, `spent_usd: null`, the `--slots` /
   `--budget` given, no Foreman transcript; `events.jsonl` holds `open` (`crs: []`) then `pause`
   (`trigger: "open, no CR"`); `brief.md` says "none yet"; the output's first line says `no CR,
   paused`; the second names `order add --note <folder> --batch <batch>` and, in Foreman mode,
   the Foreman, in direct mode `claim the batch, then \`take\``.
2. Refusals with no item: `--release 1` (exit 2, names `order add --release`);
   `--grant-fixes` and `--autonomous-releases 1` without `--release` (the existing message).
3. A second `open` (with or without items) after an empty `open`: exit 2 naming the empty batch.
4. `order add --note <ready folder> --batch <batch>` on the empty batch: it stays paused, the CR is
   queued; then the claim and `take` with the epoch set it running (one parametrized test can
   chain both).
5. `status` on the empty batch: the batch line shows `spent none yet` (not `unknown`, not
   `$0.00`) and ends `no CR yet`, and the `order add` line follows; `4-batch/STATUS.md`'s header
   says `none yet` and its Paused section `No CR yet.`
6. `STATUS.json` index: the batch entry has `crs_total: 0`; after an `order add`, `1`; its
   `schema` is unchanged.
7. `close` then `close --yes` on an empty paused batch, parametrized: (a) with a recorded
   steering transcript (the tests' prepared transcript, as the existing close tests use): `0 CRs
   archived`, the steering priced; (b) never steered (no transcript recorded): accepted; the
   steering/Foreman rows, the total, the receipt and `batch-NN.md`'s cost lines read `none: no
   session steered it`; `batch-NN.json` has `cost_usd: null` with that cause; no `$0.00` in any of
   them; the Chief of Staff's outside-the-budget lines are the same as `chief_line` prints today
   for that record. Both: `batch-NN.md` says `no CR` in its CRs and retro sections.
8. The refusal is kept: a paused batch that held a CR and has no steering transcript recorded is
   still refused by `close` (`no Foreman transcript recorded`).

`just test` stays within its budget (AGENTS.md: at most 30 s above 18.5 s).

Pane: `hooks/register.test.tsx` case above; `just mod` passes (it covers `hooks/` and `types/`).
The pane test runs against the shipped `hooks/register.tsx`, not a copy.

Cards: if the repository has a structure check that reads the cards (as `just check` does for
other card wording), it reads the shipped `concepts.md`, `foreman.md`, `chief-of-staff.md` and host
references at the head under test; no prepared text.

Scenario (`scenario/run_scenario.py`, `just scenario`): one step before the batch the scenario
opens today, or in a short separate leg: `open` with no CR (born paused, `status` says `spent none
yet` and `no CR yet`), `order add --note` of a prepared CR (stays paused), then the claim and the
first `take` (running), and the rest of the scenario's flow as it is; plus `close --yes` of a
second empty batch after the scenario's own close, never steered, checking `0 CRs archived`, the
`no CR` record and the cost `none: no session steered it`. The CLI change passes the
`just scenario (ubuntu-latest)` job before its PR, and the Driver runs `just check` and
`just eval-dry-run` in its worktree before the first push (AGENTS.md).

Board: per `DESIGN.md`, the Batch page shows `batch.no_cr_yet` and the home card shows the line,
`none yet` under Spent with no meter, `0/<total>` slots and `—` for the sign, in en and fr (the
board's own tests, if any cover these views, extended by one case reading the shipped
`en-batch.js` / `fr-batch.js`).

Known gap the PR names until the user provides it: "no screenshot of the pane from a real
session".

## Open questions

None.
