# SC16: `chantier retro draft` drafts the retro from the batch's events

Child 16 of 28 of the program CR `simplify-cards-and-prompts`. The program's `03-change-spec.md`
("Child 16", "Rules for every child") and its `02-answers.md` answers 17 to 22 rank above this
file. One Driver and one PR, in the running stack batch (batch-31). Code read: `origin/main` at
`8a960d34`. Short forms used below:

- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`.

## Goal

Today the steering session (the Foreman at a pause, the Chief of Staff in direct mode) writes the
batch's retro by hand. It reads `status --notes`, `events.jsonl`, the CRs' `work/` notes and
`cost --explain`, then finds what went wrong: an ask, a block, a refusal, a Driver restarted, a
red gate, a cost far over the others (`foreman.md`, the retro bullet of the pause). This child
gives that reading to the CLI. `chantier retro draft --epoch N` lists those facts from the
batch's events as draft retro points. Each point carries the three fields of the M5 ladder
(answer 9) that the author fills: `home:`, `count:` and `why not code:`.

The CLI only drafts. The author judges each point, writes its fix and its tag, fills its fields,
and the Retro critic still judges it. The CLI files no point and never overwrites the author's
text.

## Place in the chain

- **Base:** child 15's branch (`conflicts-check`), the previous CR of the stack. Nothing of
  child 15 is used here.
- **Uses from earlier children:**
  - child 11: `numbered_events(store, folder)` in `src/core/records.py`, which numbers each
    physical line of `events.jsonl` from 1 (the batch's event sequence), and the `--since <seq>`
    semantics of `status` (`0` means everything; a sequence past the last line is refused). If
    `numbered_events` is not in the base, add it exactly as child 11 specifies, with
    `read_events` unchanged;
  - child 12: its `next` names "`next:` line" as one rung of the M5 ladder. Nothing changes
    there.
- **Depends on this child:**
  - child 21 (Foreman cards) and child 22 (Chief of Staff cards, direct mode) write the new
    retro step around this command: run `retro draft`, judge and fill each point, then the
    Retro critic;
  - child 27 makes `chantier validate` check `home:`, `count:` and `why not code:` in a
    `retro.md`. It reads the point format fixed here (section 3) and decides what it does with
    the draft section (open question 1).
- No card changes in this child (answer 18: no child before 19 edits a card).

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Program child 16, Scope | `chantier retro draft --epoch N` drafts points from the batch's events: asks, blocks, refusals, Driver restarts, red gates and cost outliers | sections 1, 2 |
| Answer 9 (M5), program child 16 | Each point carries `home:` (the ladder: CLI, refusal, `next:` or state line, help topic, card line), `count:` and `why not code:`, left for the author | section 3 |
| Program child 16, Scope | It prints the draft, or writes it to `retro.md`'s draft section only when that file has none | sections 1, 4 |
| Program child 16, Must not | Files no retro point; overwrites no author's text | section 4, "Must not", the tests |
| Answer 22, F14 | The retro draft is its own child, split from the conflicts check | this CR |
| Answer 18 | Tools first: only additions; every intermediate `main` keeps working with the old cards | no card, no existing output changed |
| Answer 22, F20 | The PR states the seconds its tests add to `just test` | "Gates and evidence" |
| Program rules | A new command adds a scenario step and a coverage bullet; the long gate is owed; AGENTS.md gains the tool's line with its source | sections 6, 7, "AGENTS.md" |

The program says "prints the draft, or writes it". This specification reads it as: printing is
the default and writes nothing; `--write` writes the draft section, and only when `retro.md` has
none. A command run by mistake then changes no file.

## What changes

### 1. The command (`src/declare/retro.py`, `src/commands/retro.py`, `src/cli.py`)

- **Parser.** New `src/declare/retro.py` with `register(sub)`. It calls
  `add_command(sub, "retro", "chantier.commands.retro:retro", <summary>, BATCH_EPOCH)`
  (`src/commands/registry.py`) and adds:
  - `action`, `choices=["draft"]`, as `forge-stack` declares its actions;
  - `--since`, `type=int`, `metavar="SEQ"`: the batch's event sequence to start after (child
    11's meaning; `0`: every event). Without it, the window is the current pause's (below);
  - `--write`, `action="store_true"`: append the draft section to `4-batch/retro.md` when the
    file has none.

  The summary reads: "draft: the retro's draft points from the batch's events (asks, blocks,
  refusals, Driver restarts, red gates, cost outliers), each with `home:`, `count:` and `why not
  code:` for the author; printed, or appended to `retro.md` with `--write` when it has no draft
  section; it files no point".
- **Registration.** Add `retro` to the `from chantier.declare import (...)` list and to
  `_MODULES` in `src/cli.py`, and to `FULL_OUTPUT`: a draft cut at ten lines would drop points.
- **Handler.** New `src/commands/retro.py`, `retro(args) -> list[str]` (or `(lines, code)`):
  1. `repo = Repo.find()`; `batch = resolve_batch(repo, args.batch, paused=True)`
     (`src/core/batch.py`), so the paused batch is read, as `cost` does.
  2. `require_epoch(args.epoch, "retro draft --epoch <n>")`, always: this is a steering
     command. Then compare `args.epoch` with `read_batch(...).foreman_epoch` using the same text
     and exit code as `check_epoch` (stale: `EXIT_CONFLICT`). Without `--write`, nothing is
     written and no `RenderedBatch` is opened.
  3. Read the numbered events (`numbered_events`) and pick the window (below).
  4. Build the points (section 2) with a pure function, then the text (section 3).
  5. Print it. With `--write`, write it as section 4 says.
- **The window.** The events whose sequence is above a start `s`:
  - with `--since <seq>`: `s = seq`, refused as `status --since` refuses (below 0, or past the
    last line: `EXIT_USAGE`, a text that names `retro draft --since 0`);
  - else, when the batch is paused (`d.status == "paused"`): `s` is the sequence of the
    second-to-last `pause` event, or 0 when there are fewer than two. The window then covers
    the work up to and including the pause just made;
  - else (a running batch): `s` is the sequence of the last `pause` event, or 0.

  The window's CRs are the CR ids of its events (`e.cr` set and not `stack`), in first-seen
  order.

### 2. The points (`src/commands/retro_draft.py`, new)

A pure function `draft_points(numbered, costs) -> list[Point]` reads only the window's numbered
events and an optional per-CR cost map. It reads no forge and no git, and writes nothing. A
`Point` holds a kind, the CR (or None), the problem text and the sequences it rests on. Points
come in the order of the kinds below, then by first sequence:

1. **Asks.** One point per `ask` event: `ask <e.ask> to the user[ on <cr>]: <e.text>`, the text
   cut at 160 characters with `…` when longer.
2. **Refusals.** One point per distinct text, grouped across the window:
   - a `note` event whose `note` starts with `refused:` (the record that `driver-refused.md`
     asks for);
   - a `handback` event whose `result` is `blocked` and whose `note` starts with `refused`.

   Text: `refused on <crs>: <the text after "refused:" or "refused", stripped> (<k> times)`.
3. **Blocks.** One point per `handback` event whose `result` is `blocked` and that is not a
   refusal above: `<cr> handed back blocked: <note>`, cut at 160 characters.
4. **Driver restarts.** One point per CR with at least one `take` event carrying
   `restart: true` (`src/commands/driver.py` logs it on a new Driver for a CR already working):
   `<cr>: <k> Driver restart(s)`, then ` (last note: <the last such take's note, cut at 120>)`
   when it has a note.
5. **Red gates.** One point per CR and gate name with at least one `gate` event whose `result`
   is `fail` (a `stopped` gate is not red): `<cr>: long gate `<e.name or e.command>` failed <k>
   time(s) at <the distinct heads, 7 characters, in order>`.
6. **Cost outliers.** From `costs`, a map from CR id to dollars, restricted to the window's
   CRs. When it holds at least 3 CRs, a CR whose dollars are at least `OUTLIER_FACTOR` (a
   module constant, `2.0`) times the median of those CRs gets one point: `<cr>: $<usd, 2
   decimals>, <x.x> times the median $<median, 2 decimals> of the window's <n> CRs`.

Each point keeps the sequences it rests on, printed as `(events <seq>, <seq>, …)` at the end of
its problem text, so the author and the Retro critic find the evidence.

**The cost map** (`src/commands/cost/command.py`). Move the top of `cost()` (the "no ...
transcript recorded" refusal, `cost_rows(repo, d, d.host, foreman_uuid(d))`) into a function
`batch_rows(repo, d) -> list[dict]` that `cost()` then calls; `cost`'s output and refusals stay
byte for byte. `retro` calls `batch_rows`, then `cost_groups(repo, batch, rows, "cr")` and keeps
each CR key's dollars (index 1), dropping the `foreman` and `other` keys. Then:

- when `batch_rows` raises `ChantierError`, the draft gets no cost point and prints the line
  `cost: not read (<the error's text>)`;
- when `sum_unpriced(rows)` is not empty, it gets no cost point and prints
  `cost: not all priced (<not_priced(un)>); no outlier judged`.

Reading the cost reads the host's local transcripts, as `cost` does: no network.

### 3. The text

Printed, in this order:

1. `retro draft: <batch>, events <s+1>..<last>, CRs <ids or "none"> (<p> points)`;
2. the `cost:` line of section 2, when there is one;
3. the draft block, exactly the bytes that `--write` appends:

```
<!-- chantier retro draft: facts from events.jsonl; judge, tag and fill each point, or delete it -->
## Draft: <YYYY-MM-DD, UTC, today>: <CR ids, comma-separated, or "no CR">

- [<tag>] <problem> (events <seq>, …): <long-term fix>
  - home: <CLI | refusal | next: or state line | help topic | card line>
  - count:
  - why not code:
<!-- end of chantier retro draft -->
```

   - `<tag>`, `<long-term fix>` and the `home:` choice list are left as written above, angle
     brackets included, for the author. `count:` and `why not code:` end with the colon. The
     line form `- [<tag>] <problem>: <long-term fix>` is the one `foreman.md` sets today.
   - With no point, the block holds one line in place of the points:
     `- no ask, refusal, block, Driver restart, red gate or cost outlier in events <s+1>..<last>`,
     with no fields.
4. without `--write`, the last line:
   `next: judge each point, then the Retro critic; `retro draft --write --epoch <n>` appends this
   block to 4-batch/retro.md when it has none`.

All text is UTF-8, `\n` line ends, on every system.

### 4. `--write` (`src/commands/retro.py`)

- The file is the batch's `retro.md` (`repo.batch_dir(batch) / "retro.md"`, the file
  `read_retro` in `src/core/batch_records.py` reads and `close` archives).
- "Has a draft section" means the file holds the line that starts
  `<!-- chantier retro draft:`.
- The check and the write run under the batch's lock, as `RenderedBatch` takes it, so a
  concurrent writer of the batch is serialised. No event is logged and `batch.json` is not
  written.
- The file has a draft section: refused, nothing written, exit `EXIT_PRECONDITION`:
  `retro draft --write: 4-batch/retro.md already has a draft section; `retro draft --epoch <n>`
  prints this one`.
- The file is missing or has none: the block of section 3 is appended. The file's bytes before
  the write stay its first bytes, unchanged. When the file is not empty and does not end with a
  blank line, one or two `\n` are added first, so the block starts after one blank line.
- Output: the lines 1 and 2 of section 3, then
  `written: 4-batch/retro.md (<p> points appended after <n> bytes of your text)`; the block itself
  is not printed again.

### 5. What is not read

The draft reads only `events.jsonl` and, for the cost, the transcripts `cost` reads. It does not
read the CRs' `work/` notes, `forge-journal.jsonl` (a red CI line), the host's refused commands
in transcripts, or `retro-dropped.md`. The author still reads them, as the cards say today.

### 6. Scenario (`scenario/run_scenario.py`, `scenario/README.md`)

In the `parallel` unit's `scenario` function, in section "11. Event log", after the check
"events.jsonl holds the whole story" (the batch is paused, `fm` is the scripted Foreman):

- `retro = w.folder() / "retro.md"`; remember whether it exists and its bytes.
- Run `retro draft --epoch <fm.epoch> --batch <w.name>`. Check that:
  - exit 0, and the first line starts with `retro draft: <w.name>, events `;
  - the output holds the `<!-- chantier retro draft:` line and the end line;
  - every line that starts `- [<tag>] ` is followed by the three lines `  - home: `,
    `  - count:`, `  - why not code:`;
  - for each `gate` event with `result` `fail` in the window, a point names its CR and
    `failed`;
  - `retro.md` is as before (absent, or the same bytes): "`retro draft` without `--write`
    writes nothing".
- Write `retro.md` with `"## Author\n\n- my own line\n"`, then run `retro draft --write
  --epoch <fm.epoch> --batch <w.name>`. Check exit 0, a `written: ` line, and that the file
  starts with the author's bytes and holds the draft block once.
- Run `retro draft --write` again. Check exit 2, a text naming `retro draft --epoch`, and the
  file's bytes unchanged.
- Run `retro draft` without `--epoch`. Check exit 2.
- Restore `retro.md` as it was before the step (remove it if it was absent), so section 11b
  (`close_batch`, which writes its own `retro.md`) runs as before.
- `scenario/README.md`, "## Coverage": one bullet:
  `- `retro draft` (unit: parallel): the retro's draft points from the paused batch's events,
  each with home:, count: and why not code:, a red gate named; nothing written without
  `--write`; `--write` appends after the author's text once and is refused when a draft section
  exists (test: test_retro_draft.py::<the points test>)`. `tests/test_scenario_coverage.py`
  checks that the unit and the test exist.

### 7. Tests (`tests/test_retro_draft.py`, new)

Prepared records only, built with `batch_helpers.record` and `write_record` and the in-process
`chantier` fixture, as the other command tests do; the events are written as `events.jsonl`
lines. No git, no network, no transcript.

- **Points, parametrized over prepared events** (the pure function), each case giving the
  expected problem texts whole:
  - an `ask` event (with and without a CR; a long text cut with `…`);
  - two `note` events with the same `refused: <cmd> -> <text>` on two CRs (one point, `2
    times`), and a `handback blocked` whose note starts `refused` (counted as a refusal, not a
    block);
  - a `handback blocked` with another note (a block);
  - two `take` events with `restart: true` on one CR (`2 Driver restarts`, the last note);
  - `gate` events `fail`, `fail` at two heads, `pass` and `stopped` on one CR (one point, `2
    times at <h1>, <h2>`; `stopped` and `pass` not counted);
  - a cost map of 4 CRs with one at three times the median (one point), one of 2 CRs (no
    point), and one with no CR above the factor (no point);
  - no problem event: the one "no ask, refusal, …" line, with no fields.
  Each case asserts the `(events …)` sequences.
- **The window.** A batch with three `pause` events: paused, the default window starts after
  the second; running (a later `reopen`), it starts after the third; `--since 0` covers all;
  `--since -1` and a sequence past the last line exit 1 and name `retro draft --since 0`.
- **The fields.** Every point of a draft with points is followed by the three field lines,
  byte for byte as section 3 gives them.
- **The cost lines.** With `batch_rows` patched to raise the `no Foreman transcript recorded`
  error: the `cost: not read (…)` line and no cost point. With it patched to return rows that
  `cost_groups` and `sum_unpriced` read (a prepared input: the transcripts are the host's files):
  the outlier point; with an unpriced row, the `cost: not all priced` line.
- **Read-only.** Without `--write`, the bytes of `batch.json`, `events.jsonl` and (absent or
  present) `retro.md` are equal before and after.
- **`--write`, parametrized over the file's state:** missing; empty; author text ending with a
  blank line; author text with no final newline. Each time the file starts with the original
  bytes, holds one blank line before the block, and the block once. Then a second `--write`
  exits 2 and the file's bytes are unchanged; a file that already holds a draft section and
  author text after it is left byte for byte.
- **Refusals.** A missing `--epoch` exits 2; a stale one exits 3; nothing is written.
- **Files no point.** After `--write`, the planning folder's `1-inbox/`, `2-backlog/` and
  `forge-journal.jsonl` are unchanged, and `events.jsonl` has no new line.

## Out of scope

- Judging a point: its tag, its fix, its `home:` rung, its `count:` (runs seen in the last
  `just behaviour` measure, M7, child 5) and its `why not code:` stay the author's.
- Filing a point (an inbox item, an issue), starting the Retro critic, or writing
  `retro-dropped.md`.
- Any change to `close`, `pause`, `status`, `cost`'s output, `read_retro` or the batch's record.
- `chantier validate`'s check of the three fields (child 27).
- Red CI from `forge-journal.jsonl`, the host's refused commands from transcripts, rounds past
  the first and cache expiries (section 5; open question 2).
- Any card, hook or wrapper text; a new journal type (so `just journal-schemas` is not run); any
  version edit.

## Must not

- File a retro point, log an event, or write any file but `4-batch/retro.md` with `--write`.
- Overwrite, reorder or reformat an author's text in `retro.md`: the write only appends, and
  only when the file has no draft section.
- Read the forge or run git.
- Judge a point: no tag, no fix, no field filled.

## Gates and evidence

- `just test` passes with `tests/test_retro_draft.py`.
- The added `just test` seconds are measured before (at the base) and after (at the head) on the
  same machine and go under the PR's Deliverables. Expected: under 1 s (about 20 parametrized
  cases of a pure function and about 15 in-process command calls on small prepared records).
- `just check` and `just eval-dry-run` (a change under `src/`) run in the worktree at the rebased
  head before the first push.
- The long gate `just scenario (ubuntu-latest)` is green at the PR's head, since the CLI and the
  scenario change. The local Windows `chantier gate <cr> scenario` is owed only while this CR is
  the stack's top; it moves to the CR that joins above it.
- No host or default matrix: the events part acts the same on both hosts and with any
  configuration. The cost part reads the transcripts `cost` reads on the batch's host; its
  host dependence is `cost`'s own, unchanged, and the tests patch `batch_rows`.
- No check guards a shipped file: the tests assert the CLI's output on prepared records.
- No `hooks/` or `types/` change, so `just mod` is not owed.

## AGENTS.md

Add one named exception in the CLI-scope bullet, beside the lines for `wait`, `access`, `live`
and `judge`:

> `retro draft`: it drafts the batch's retro points from the batch's `events.jsonl` (asks,
> refusals, blocks, Driver restarts, red long gates) and, from the spend `cost` reads, the CRs'
> cost outliers, each point with the `home:`, `count:` and `why not code:` fields left for its
> author; it prints the draft, or, with `--write`, appends it to `4-batch/retro.md` only when
> that file has no draft section, never touching the author's text; it reads no forge, runs no
> git, logs no event and files no point; built on the user's answers simplify-cards-Q9 (M5) and
> Q22 (F14), with no measured cost.

## Risk

- The long gate is owed (CLI and scenario).
- `close` archives `4-batch/retro.md` whole (`history.close_markdown`). A draft section written
  and left unfilled reaches `5-archives/batches/batch-NN.md` as is, with its markers and
  placeholders. Until the card children tell the author to judge it, nothing writes it: the old
  cards never run `retro draft`. See open question 1.
- The draft section is one per file: at a second pause of the same batch, a draft section of the
  first pause still in the file refuses `--write`, and the author uses the printed draft.
- Refusals are drafted only when recorded as `refused:` notes or `handback blocked refused`; a
  refusal no one recorded is not seen.

## Open questions

1. **An unfilled draft at the close.** `close` writes `retro.md` whole into the batch's record,
   so a draft section left as written (markers, `<tag>`, empty fields) would be archived. Should
   `close` refuse while `retro.md` holds the `<!-- chantier retro draft:` line (the author then
   deletes the markers once the points are judged), or should child 27's `validate` only flag
   it? Until you answer, `close` is unchanged and the block is visibly marked as a draft.
2. **Sources beyond the batch's events.** The program names the batch's events, so the draft
   leaves out red CI on a ready PR (`forge-journal.jsonl`), the host's refused commands (in
   transcripts, which `foreman.md` asks one retro line each for), rounds past the first and
   cache expiries. Should a later CR add any of them to the draft?
