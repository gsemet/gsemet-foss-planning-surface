# Change Specification: the CR board pane shows the batch's shape (`shape`)

## Goal

In the CR board pane (the Claude Code mod, `hooks/register.tsx`), the user cannot tell whether a
batch runs its CRs in series, in parallel or as a stack. The pane shows it, as one word, on the
batch's line next to "Slots" (shape-Q1, answer A). The slot count itself does not change
(shape-Q2).

## Where the shape comes from today

- The batch's record holds it: `BatchRecord.mode` (`core/records.py`, `mode: str | None`), set at
  `open` and changed by `order mode` while the batch runs.
- `chantier status` prints it through `shape_word` (`status/words.py`): `stack`, `series` or
  `parallel`, else `unknown`; `commands/batch_status.py` prints `shape <word>`.
- The batch's own `STATUS.json` carries it raw as `"mode"` (`status/views.py`, `batch_view`).
- The index the pane reads, `<planning folder>/STATUS.json` (`status/views.py`, `dashboard_view`;
  types `ChantierIndex` / `ChantierBatch` in `types/index.d.ts`), does **not** carry it: each entry
  of `batches` has `batch`, `folder`, `state`, the cost fields, `asks_unread`, `heartbeat`,
  `heartbeat_stopped`, `orders_pending`, `slots` and `crs`, and no `mode`.
- The pane draws the batch's lines in `Batch` (`hooks/register.tsx`, around lines 992-1022); the
  slots line is
  `` <Text>{`Slots ${b.slots.taken}/${b.slots.total}, ${Math.max(0, b.slots.total - b.slots.taken)} free`}</Text> ``,
  drawn only when `b.slots` is present.

(Paths under the CLI are relative to `skills/chantier/scripts/cli/src/chantier/`.)

## What changes

### 1. The index carries the shape (CLI)

`status/views.py`, `dashboard_view`: each entry of `batches` gains `"mode": v["mode"]` (the value
`batch_view` already reads from `d.mode`), placed beside `"slots"`. No new source: it is the
record's value, raw, as the batch's own `STATUS.json` already writes it (null when the record has
none). `SCHEMA` stays 3: the field is an addition, and the pane reads it as optional, as it reads
`slots`.

### 2. The type (`types/`)

`types/index.d.ts`, `ChantierBatch`: add `mode?: string | null` beside `slots?`, with a one-line
comment: the batch's shape from its record (`stack`, `series`, `parallel`), null when the record
has none; absent in an index written before this change.

### 3. The pane (`hooks/`)

`hooks/register.tsx`, `Batch`: the slots line ends with the shape word, joined by ` · ` (the
separator the pane's header line already uses):

- `Slots 2/3, 1 free · parallel` (likewise `series`, `stack`).
- The word follows `shape_word`'s rule: `stack`, `series` or `parallel` as is; a `mode` that is
  null or another value shows `unknown`, as `chantier status` prints `shape unknown`.
- An index with no `mode` field (written by an older CLI) shows the slots line as today, with no
  word, as an index with no `slots` shows no slots line.
- An index with `mode` and no `slots` (not produced by this CLI, but the type allows it) shows the
  word alone on that line.

The word follows the record: after `order mode`, the pane shows the new shape at its next read of
the refreshed `STATUS.json`; no extra refresh is added.

### 4. The docs

`docs/boards.md`, "How to read it" (lines 23-25): the batch's line gives "its slots and its shape
(`Slots 3/3, 0 free · parallel`)" in place of the current `Slots 3/3, 0 free` example.

## Decisions carried from `02-answers.md`

- **shape-Q1 (A):** on the batch's line of the CR board pane, next to "Slots", the batch's shape
  as a word: series, parallel or stack. Carried in sections 3 and 4.
- **shape-Q2:** "Slots 4/1" was a transition (slots cut from 4 to 1 while 4 Drivers still ran),
  not a bug: the count `taken/total` and its `free` figure do not change. No change to `slots` in
  `views.py` nor to its drawing beyond the appended word.
- **Settled, the source:** the shape comes from the batch's record, as `status` prints it, through
  a `STATUS.json` field added beside the ones the pane reads (`mode` in the index); no new source.
  Carried in section 1.
- **Settled, the screenshot:** the PR carries one screenshot of the pane from a real Claude Code
  session at its head, or names its absence in Known gaps, and the Chief of Staff asks the user
  for it. Carried in "Gates" below.

## Out of scope

- Any change to the slot count, its `free` figure, or what `held(d)` counts (shape-Q2).
- The web board (`board/web/`): not touched; no `DESIGN.md` read is owed.
- The batch's own `STATUS.md` / `STATUS.json`, `chantier status` and `history`: they already say
  the shape and are not changed.
- Copilot: it has no pane (`docs/boards.md`: "Nothing of it on Copilot").
- A schema bump of `STATUS.json`.

## Host matrix

The pane exists only on Claude Code; the CLI's field is host-free. No configured value is involved
(the shape is the batch's record, not a configuration key).

- Claude Code, index with `mode`: the pane shows `Slots t/n, f free · <word>`.
- Claude Code, index without `mode` (older CLI): the pane shows the slots line as today.
- Copilot: the index carries `mode`; nothing draws it (no pane).

## Evidence

- **Pane, `hooks/register.test.tsx`:** extend the test "a batch header shows its slots, and
  nothing when the index has none" (around line 877), or add one beside it, over the index's
  batch: `slots {taken: 2, total: 3}` with `mode: 'parallel'` shows `Slots 2/3, 1 free · parallel`;
  with `'series'` and `'stack'` the matching word; with `mode: null` shows
  `Slots 2/3, 1 free · unknown`; with no `mode` shows `Slots 2/3, 1 free` and no ` · `. The test
  draws the shipped `hooks/register.tsx` (the module under test, at the head), not a copy; the
  index is the prepared input, as the existing test does.
- **Index, `scenario/run_scenario.py`:**
  - the check "the index gives each batch its heartbeat and pending orders..." (around line 2592)
    also asserts that each entry of `index["batches"]` has a `mode` equal to the `mode` of that
    batch's own `STATUS.json`;
  - the check "`order mode --note stack` turns a series into a stack at once, and logs it" (around
    line 6163) also asserts that the index (`w.state / "STATUS.json"`) gives that batch
    `mode == "stack"` after the order, so the pane's source follows a live switch.
- **Type:** `types/index.d.ts` checks with the pane (`just mod`, and `just check`).

## Gates (AGENTS.md)

- `just check` passes before hand-back; the Driver runs it in the worktree at the rebased head it
  first pushes.
- The change touches the CLI's `src/` (`status/views.py`): the Driver also runs
  `just eval-dry-run` there before the first push.
- The change touches `hooks/` and `types/`: `just mod` passes before the PR, run by the agent
  itself; an agent that cannot run it stops and says so, with no workaround.
- The change touches the CLI and the scenario: the pipeline's `just scenario (ubuntu-latest)` job
  is green at the PR's head before its PR; when this CR is on top of its batch's stack, it also
  passes `just scenario` locally (`chantier gate`) at its head before the user merges.
- The change alters what the CR board pane draws (`hooks/register.tsx`'s pane, and a `STATUS.json`
  field of `status/views.py` the pane shows): the PR's Deliverables carry one screenshot of the
  pane from a real Claude Code session running the PR's head, showing a batch's line with
  `Slots ... · <word>`, captioned with the head's seven-character SHA. Until it is there, the PR's
  Known gaps names "no screenshot of the pane from a real session", so the ready line quotes it,
  and the Chief of Staff asks the user for one.

## Open questions

None.
