# SC16 + SC17 + SC18: `chantier retro draft` drafts the retro from the batch's events; one launcher that picks the mode and runs the CLI; Role data in `roles.yaml` and a `just roles` check of the wrappers

This CR carries children 16, 17, 18 of the program `simplify-cards-and-prompts` in ONE Driver, ONE PR, in this order, as the owner asked on 2026-11-25 ("regroupe les CR entre elles pour en faire des plus grosses"). Each part below is the full Change Specification of one child, unchanged: do them in order, one after the other, commit by commit. Where a part says "child N's branch", "on child N" or "waits for child N" and child N is another part of this CR, it means the earlier part of this same branch, not another PR. The gates of the parts are all owed, run once at the PR's head (the strictest part decides which long gate). If the context runs short, hand back with the exact state at about 100k tokens: parts done, parts left. The answers of every part are appended to this folder's `02-answers.md`.


---

# PART 1 of 3: SC16: `chantier retro draft` drafts the retro from the batch's events

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


---

# PART 2 of 3: SC17: one launcher that picks the mode and runs the CLI

Child 17 of 28 of the program CR `simplify-cards-and-prompts`. The program's `03-change-spec.md`
("Child 17", "Rules for every child") and its `02-answers.md` answers 17 to 22 rank above this
file. One Driver and one PR, in the running stack batch (batch-31). Code read: `origin/main` at
`8a960d34`. Short forms used below:

- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`;
- `<plugin root>` is the folder that holds `.claude-plugin/plugin.json` (chantier's checkout, or a
  host's plugin copy); `<skill folder>` is `<plugin root>/skills/chantier`.

## Goal

Each of the four `SKILL.md` files (`skills/chantier`, `skills/chief-of-staff`, `skills/griller`,
`skills/status`) carries the same `$CHANTIER` paragraph, about 2.3 KB (study-fable-v2). Every
steering session reads it and then works out the launch by hand:
- is this chantier's own checkout, and is the session's project chantier: dev or plugin mode;
- in the dev mode, `uv sync --locked --check`, naming the holders of `.venv`, the sync, or
  `sync pending: held by …`;
- the exact form to type, with `--skill` in the plugin mode.

This child moves that work into code: one launcher shipped with the plugin. It picks the mode,
runs the dev mode's checked sync when asked and prints `sync pending: held by …` itself, and
runs the CLI by the one method AGENTS.md describes. An agent then types one fixed form:

```
uv run --script "<plugin root>/skills/chantier/scripts/chantier.py" [--project <folder>] <command> ...
```

Nothing uses the launcher yet. The four `SKILL.md` keep their paragraph. Child 23 writes the
one line that names the launcher, in the unloaded set, and child 24 swaps it in. This child
ships the launcher, its tests, and a trial in a real session showing that the host's allow rule
matches it as it matches today's form.

## Place in the chain

- **Base:** child 16's branch (`sc16-retro-draft`), the previous CR of the stack. Nothing of
  child 16 is used here.
- **Uses from earlier children:** nothing. `src/launch.py` and `src/plugin_files.py` are as on
  `origin/main`.
- **Built on this branch:** child 18 (`roles-data-check`). It uses nothing from this one.
- **Depends on this child:**
  - child 23 (`cards-host-and-shared`) writes, in `cards-next/skills/`, the four `SKILL.md` texts
    with one line that names the launcher. It also writes the host topic that holds the launcher's
    allow rule. It reads the form from `launch.launcher_line` and `launch.launcher_rule`
    (section 2) and the sync's lines from section 4;
  - child 24 (`cards-swap`) brings in those texts. It adds the launcher's P10 sample and its
    rule to `src/commands/allow_samples.py` and to the host card's table and JSON block. It also
    decides whether `plugin_files.cli_command` (the `cli:` fact, the briefs) prints the launcher
    form (section 6);
  - child 28 (the real run) runs the new cards, which type the launcher.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Program child 17, Scope | A launcher shipped with the plugin decides the dev or plugin mode | sections 1, 2, 3 |
| Program child 17, Scope | It checks `uv sync --check` and prints `sync pending: held by …` itself | section 4 |
| Program child 17, Scope | It runs the CLI by the one method AGENTS.md describes: `uvx --from <plugin root>`, or in the dev mode `uv run --no-sync --project` | section 3 |
| Program child 17, Scope | The four `SKILL.md` keep their paragraph until child 23 | section 6, "Out of scope" |
| Program child 17, Evidence | Pytest of the mode choice on prepared folders | section 7 |
| Program child 17, Evidence | A trial in a real session shows the host's allow rule matching the launcher as it matches today's `uv run` form, recorded in the PR | section 8 |
| Program child 17, Evidence | An unmatched or refused launcher is not worked around: the child hands back blocked | section 8 |
| Program child 17, Must not | Change the run method; install anything | sections 3, 4, "Must not" |
| Program child 17, Risk | P10's samples change with the launcher; one new rule may be asked by preflight; the ready ask names it | section 6 |
| Program child 17, Risk | AGENTS.md: the run-method paragraph names the launcher | "AGENTS.md" |
| Answer 18 | Tools first: only additions; every intermediate `main` keeps working with the old cards | no card, no existing output changed |
| Program rules, "Card text" | No child before 19 edits an existing card's text | section 6 |
| Answer 22, F17 | A claim about the host or a tool not proved here is marked "unproved" | sections 3, 4, 8 |
| Answer 22, F20 | The PR states the seconds its tests add to `just test` | "Gates and evidence" |

On P10, the program says the samples change "with the launcher". This child carries that as the
launcher's rule text (`launch.launcher_rule`), ready for P10. It does not add a sample row.
`tests/test_cli_runs.py::test_the_allow_rules_json_block_lists_exactly_what_preflight_checks`
ties `SAMPLES` to the table and JSON block of `references/hosts/claude-code.md`. A new row would
force an edit of that card, which the program's "Card text" rule forbids before child 19. Child
1 (CR-487, `push`) made the same choice. While no card types the launcher, a rule asked for it
would cover no command. So P10 starts asking for it at the swap (child 24), and the ready ask
says so (section 6).

## What changes

### 1. The launcher file (`skills/chantier/scripts/chantier.py`, new)

A short script with an inline metadata block, as `scripts/version.py` has:

```
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

`requires-python` is the same as the root `pyproject.toml`'s (a test checks it). The script holds
no logic. It puts `Path(__file__).resolve().parent / "cli" / "src"` first on `sys.path`, imports
`chantier.launcher`, and calls `raise SystemExit(main(sys.argv[1:]))`. The plugin root is
`Path(__file__).resolve().parents[3]`.

The launcher runs as `uv run --script "<path>"`, never from the project's `.venv`. A script with
inline metadata gets uv's own environment, so the launcher never holds `<plugin root>/.venv`,
even in chantier's checkout. This follows uv's documentation; it is **unproved** here until
the scenario step (section 7) and the trial (section 8) show it. With `dependencies = []`, it
needs no package. It needs a Python of at least 3.11, which uv finds or fetches once, as `uvx`
does today. With uv's cache warm, it needs no network (shown with `UV_OFFLINE=1`, sections 7
and 8).

Add `"skills/chantier/scripts/chantier.py"` to `[tool.mypy] files` in `pyproject.toml`.
`just lint` already formats and checks `skills/` with ruff.

### 2. The one source of the texts (`src/launch.py`)

`launch.py` stays standard-library only (a test checks it, section 7). Add:

- `LAUNCHER = Path("skills/chantier/scripts/chantier.py")`: the launcher's path from the plugin
  root.
- `launcher_line(root: Path) -> str`: `uv run --script "<root>/skills/chantier/scripts/chantier.py"`,
  written with forward slashes and quoted, as `dev_launch` and `plugin_launch` are.
- `launcher_rule(root: Path) -> str`: `f"{launcher_line(root)} *"`. P10 and child 23's host topic
  read this rule text, and the trial proves it.
- `project_is_chantier(cwd: Path, project: str | None) -> bool`: the launcher's half of the mode
  rule, with no `Repo`. It runs read-only `git rev-parse` calls through `subprocess` (no
  `chantier.core` import). It answers what `is_chantier_project(Repo.find(cwd, project))`
  answers:
  - `CHANTIER_ROOT`, when set, replaces `cwd`, as in `Repo.find`;
  - with `project`:
    - a bare name (one part, not absolute) is taken as `<git top of cwd, or cwd>/projects/<name>`;
    - another relative path is taken from `cwd`, then resolved;
    - the answer is whether the folder's name is `chantier`, by its name alone, as the
      `SKILL.md` paragraph and `is_chantier_project` say for a surface;
  - without `project`: take the root as the parent of `git rev-parse --path-format=absolute
    --git-common-dir` (so a worktree of chantier counts as chantier). Then:
    - when the root has no `.agents/changes/` and its `projects/` holds exactly one project
      (`checkout.yml` or `changes/` inside, as `surface_projects` says), the answer is whether
      that project's name is `chantier`;
    - with several projects, the answer is `False` (the CLI refuses with its `--project` line
      anyway);
    - otherwise the answer is the manifest test of `is_chantier_project`: the root's
      `.claude-plugin/plugin.json` or `.github/plugin/plugin.json` has `name` `chantier`;
  - outside a git repository, the answer is `False`.

  Refactor `is_chantier_project`'s manifest test into a helper that both functions call, so the
  manifest rule is written once. `is_chantier_project`'s behaviour does not change.

### 3. The mode and the run (`src/launcher.py`, new, standard-library only)

`main(argv: list[str]) -> int`, and the pure functions it calls (tests call them with prepared
folders and a fake process runner):

- **The mode.** `dev` when `<plugin root>/.git` exists (a folder or a file) and
  `project_is_chantier(cwd, project)` holds. This is `plugin_files.is_dev_mode`'s rule. `plugin`
  in every other case: a host's plugin copy, or another project's session even when run from
  chantier's checkout.
- **The root options.** The launcher reads the CLI's root options that come before the first
  word that is not an option: `--project <v>` and `--project=<v>`; it also skips `--profile` and
  `--skill`, which take a value. It reads them and leaves them in place: the argument list goes
  to the CLI unchanged.
- **The command it runs**, as a list with no shell:
  - dev: `uv run --no-sync --project <plugin root> chantier <argv...>`;
  - plugin: `uvx --from <plugin root> chantier --skill <skill folder> <argv...>`. `--skill` is
    added only when `argv` does not already carry it.

  The prefix tokens are built from the same strings as `launch.dev_launch` and
  `launch.plugin_launch`, so the forms cannot drift. A test checks that the joined, quoted list
  equals `plugin_files.cli_command(repo)` for the same folders (section 7).
- **The run.** The CLI inherits standard input, output and error. The launcher adds nothing to
  standard output on a run, buffers nothing (a `watch --stream` stays live), and exits with the
  CLI's exit code.
  - On POSIX it replaces itself with `os.execvp`, so no process of its own is left between the
    host and the CLI.
  - On Windows it runs the command with `subprocess.run` and returns its code. On Ctrl-C it waits
    for the child, which gets the same console signal.

  When `uv` or `uvx` is not found, it prints one line, `chantier launcher: uv is not on PATH
  (uv is the one tool chantier needs)`, and exits 127. It tries nothing else.
- **`--print`**, as the first argument only: it prints the launch form that the run would use,
  and runs nothing. That is `plugin_files.cli_command`'s text for the same folders, `--project
  "<absolute folder>"` included when `--project` was given. It exits 0. The tests, the scenario
  and the trial read it.
- **`--sync`**, as the first argument only: section 4.
- The launcher never runs `uv sync` outside `--sync`. In the dev mode an ordinary call runs no
  check, as today's `--no-sync` form does. Only the steering session syncs, at the moments the
  cards name.

### 4. The dev mode's checked sync (`--sync`, in `src/launcher.py`)

These are steps 1 to 4 of `references/sync-checkout.md`, done by the launcher itself. Steps 5
and 6 stay with the steering session: the user told once after 3 minutes, and the offer to stop
its own board and watcher. They need the session's judgement and its seat.

- In the plugin mode it prints `plugin mode: no sync (only chantier's own checkout syncs)`,
  exits 0, and runs nothing.
- In the dev mode:
  1. It runs `uv sync --locked --check --project <plugin root>`. Exit 0: it prints `in sync`
     and exits 0. Exit 1 with uv's text `The environment is outdated`: step 2. Any other exit is
     an ordinary sync failure, never `sync pending`: it prints uv's text and exits with uv's
     code.
  2. It names the holders of `<plugin root>/.venv` by the commands of the host row "Name the
     holders of the checkout's environment" (`references/hosts/claude-code.md`), read-only:
     - on Windows: `powershell.exe -NoProfile -NonInteractive -Command` with `Get-CimInstance
       Win32_Process | Where-Object { $_.ExecutablePath -like '<root with backslashes>\.venv\*' }
       | Select-Object ProcessId, ParentProcessId, CommandLine`, its output read as JSON
       (`ConvertTo-Json`);
     - elsewhere: `ps -eo pid,ppid,args`, keeping the lines that hold `<plugin root>/.venv/`.

     It reads them as the row says. A `chantier` process and its `python` child are one holder,
     named by the top process's PID. Each holder is written `PID <n> <subcommand> <project>`,
     with the subcommand and the `--project` value taken from its command line. A `serve` with
     `--stop-idle` and no `--seat` is written `PID <n> serve <project> (started by webui)`. It
     never stops a holder.
  3. With no holder, it runs `uv sync --locked --project <plugin root>`. On success it prints
     `synced` and exits 0. When it fails with os error 32 (a holder the listing missed), it goes
     to step 4 with `an unlisted process`. Any other failure: uv's text, uv's code.
  4. With any holder, it prints `sync pending: held by <holders>` (holders joined by `, `) and
     exits 0. The session goes on unsynced: its next ordinary call runs the `--no-sync` form.
     Its next `--sync`, at a later turn, starts again from step 1.

`sync pending` exits 0 because it is not a failure: `startup-core.md` routes failures, and the
paragraph keeps `sync pending` out of them. The three lines `in sync`, `synced` and `sync pending:
held by …` are fixed texts. Child 23 quotes them, and the tests assert them.

Unproved here: the Windows listing run from Python rather than typed into the `PowerShell` tool
(the row's listing was exercised by hand on 2026-11-21); the macOS and Linux listing (untested,
as the row says).

### 5. What does not change

- The four `SKILL.md` files, every card under `references/`, the hook and the agent wrappers.
- `plugin_files.cli_command`, `sync_command`, `sync_check_command` and every CLI output: the `cli:`
  fact, the briefs and the Driver prompts keep today's forms.
- `src/commands/allow_samples.py`, `src/commands/permissions.py` (`PROBES`, `_PLUGIN_FORM`,
  `_DEV_FORM`, `_stale`) and P10's output.
- The run method: the dev mode still runs `uv run --no-sync --project`, and the plugin mode
  `uvx --from <plugin root> chantier --skill <skill folder>`. The launcher only chooses between
  them and runs them.

### 6. For the swap, and the ready ask

The PR's body has a section "For child 24", and the ready ask quotes its first point:

- **No new allow rule is asked yet.** P10 starts asking for `Bash(<launcher_rule>)` and
  `PowerShell(<launcher_rule>)` from child 24 on, when the cards type the launcher. That is the
  one new rule a user who granted today's rules will add, asked by preflight as today.
- Child 24 adds one `SAMPLES` row, `("batch", "any", f"{launcher_line(<plugin root>)} status",
  launcher_rule(<plugin root>))`, filled by `fill_rule` and `fill_sample` like the other chantier
  rows. It also adds the matching line to the host card's table and JSON block.
- Child 24 reviews `permissions.py`:
  - a user's broad `uv run --script * *` (already in `PROBES`) then reads "replaced by" the
    launcher's rule;
  - `_stale` learns the launcher's form for a rule that names a moved plugin.
- Whether the old forms (dev, sync, check, plugin) stay as rules once no card types them is
  child 24's call.
- Whether `cli_command` prints the launcher form is child 24's call: the `cli:` fact and the
  briefs carry it verbatim.

### 7. Tests (`tests/test_launcher.py`, new)

All in-process, with prepared folders under `tmp_path`, and no `uv`, `uvx` or `powershell`
started. The process runner is a fake that returns prepared outputs and records the commands.

- **The mode choice.** Parametrized over the cells of `tests/test_launch_modes.py`'s
  `LAUNCH_CELLS` (`claude`, `copilot`, `surface-chantier`, `plain`, `other-name`, `broken`,
  `surface-studio`, `none`), plus:
  - a surface whose only project is `chantier`, with no `--project`;
  - a surface with two projects;
  - a bare `--project chantier` inside a surface;
  - a worktree of a chantier-manifest repository;
  - `CHANTIER_ROOT` set to another folder;

  each crossed with a plugin root that holds `.git` and one that does not. For each, it asserts:
  - the launcher's mode;
  - that `project_is_chantier` equals `is_chantier_project(Repo.find(...))`, and the mode equals
    `plugin_files.is_dev_mode(...)`, with `CHANTIER_SKILL_DIR` pointed at the prepared plugin
    (the parity that guards the two halves against drift);
  - that `--print`'s line equals `cli_command(repo)`, `--project` included, also with a space in
    the path;
  - the argument list of the run: the root options left in place, `--skill` added once, the
    rest unchanged.
- **The sync.** The fake runner gives each case:
  - check exit 0: `in sync`, no sync run;
  - outdated with no holder: `synced`, the sync run once;
  - outdated with a board and its `python` child plus a `webui`-started server:
    `sync pending: held by PID 10 serve chantier, PID 30 serve chantier (started by webui)`,
    no sync run, exit 0;
  - the sync failing with os error 32: `sync pending: held by an unlisted process`;
  - another failure: uv's text and code;
  - the plugin mode: its line, nothing run.

  It also asserts that an ordinary call runs no `uv sync` in either mode.
- **The shipped files, read from the repository at the head under test.**
  - `skills/chantier/scripts/chantier.py`: its metadata block says `dependencies = []`, and its
    `requires-python` equals `pyproject.toml`'s;
  - `src/launcher.py` and `src/launch.py`: they import only modules in
    `sys.stdlib_module_names`, plus `chantier.launch` from `launcher.py`. This is an AST read of
    the files.
- **The missing `uv`.** The fake runner raises `FileNotFoundError`: one line, exit 127.

**Scenario** (`scenario/run_scenario.py`): a new section function `launcher_modes`, added to the
unit that already runs preflight's P10 step, inside its time budget. It runs the shipped launcher
for real with `uv run --script`, `UV_OFFLINE=1` in its environment:
- in the sandbox project (not chantier), `--print` equals the `cli:` fact's form;
- with `--project <a prepared surface>/projects/chantier`, `--version` runs the dev form and
  prints `chantier <version>`, exit 0;
- in the sandbox, `--sync` prints the plugin-mode line, exit 0;
- `<checkout>/.venv` is unchanged across the three calls, which proves on ubuntu that the
  launcher does not run from it. The check reads the modification time of
  `<checkout>/.venv/pyvenv.cfg` and the listing of `.venv/`.

Add its bullet to `scenario/README.md`'s Coverage list, ending `(unit: <that unit>, test:
test_launcher.py::<the mode test>)`. Whether ubuntu's runner has uv's cache warm enough for
`UV_OFFLINE=1` is proved only by the first CI run.

### 8. The trial in a real session (recorded in the PR)

The Driver runs it on its own machine and records it in the PR under "Trial". It runs before
the PR is called ready.

- **The settings.** A scratch settings file in the session's scratch folder, never
  `~/.claude/settings.json` and never the project's settings. It holds the filled rules
  `Bash(<launcher_rule(<plugin root>)>)` and `PowerShell(<launcher_rule(<plugin root>)>)`, plus,
  as the control, today's filled rule of the same mode: `dev_rule` in chantier's checkout for
  the chantier project.
- **The session.** Claude Code headless (`claude -p`), started in a scratch folder outside the
  repository, with `--permission-mode dontAsk`. This is the cell the host card proved for
  today's forms: main session, `dontAsk`. It uses `--settings <scratch file>`, plus whatever
  flags keep the user's own allow rules out (recorded).
- **The commands.** The prompt asks the session to run, one command each, exactly:
  - `<launcher_line> --project "<surface>/projects/chantier" --version` with the `Bash` tool;
  - the same with the `PowerShell` tool, when the session has it;
  - today's `<dev_launch> --version` with each tool.
- **What it records:**
  - the Claude Code version (`claude --version`), the system, the permission mode and the exact
    flags;
  - each command's verdict: run, or refused with the refusal quoted;
  - a negative control: the same session with the scratch settings minus the launcher's rules
    must refuse the launcher. That shows the rule is what lets it through.
- **Pass:** the launcher runs exactly where today's form runs, and the negative control refuses
  it. Auto mode and a Driver (subagent) stay **unproved**, as for today's forms. Copilot is
  **unproved**: no trial. When the Driver can, it adds one auto-mode try and records the verdict
  as information.
- **Fail:** the rule does not match, the host refuses, the negative control cannot be shown, or
  `claude -p` itself is refused to the Driver. The child hands back blocked with the transcript's
  lines. No other path form, no wrapper and no broader rule is tried.
- **Also recorded:**
  - the launcher's overhead: the median of 5 `--version` calls through the launcher against 5
    through today's form, in each mode on the Driver's machine;
  - one stop check. Through the launcher, start a long CLI command in a scratch in-project
    repository (`serve --ui none`), then stop the launcher's top process (the `uv run --script`
    one) the way the host stops a background shell. Then list whether a `chantier` process
    from it is left.

  A `chantier` process left behind does not block this child, which nothing uses yet. It goes
  in the PR's Known gaps ("the launcher leaves the CLI running after its stop on <system>"), the
  ready ask quotes it, and child 24 must not switch the cards until it is fixed.

## Out of scope

- Any edit of the four `SKILL.md`, `references/sync-checkout.md`, `references/startup-core.md`
  or any other card (children 23 and 24).
- P10's samples, the recommended rules and the host card's table (child 24, section 6).
- Steps 5 and 6 of `sync-checkout.md` (the 3-minute message, the offer to stop the session's own
  board and watcher).
- Copilot's allow rules for the launcher.
- A launcher on PATH, a `bin/` folder, a shell or `.cmd` wrapper. The one form is `uv run
  --script "<path>"`, the same text in `Bash` and `PowerShell`.
- Any change to how the board, the hub or the watcher are started.

## Must not

- Change the run method: the launcher runs exactly the dev form or the plugin form, chosen by
  today's rule. In the dev mode it never runs `uvx --from <checkout>`, and in the plugin mode it
  never runs `uv sync`.
- Install anything: no `uv tool install`, no PATH or profile change, no package in the
  launcher's metadata. The one write is `uv sync --locked` under `--sync`, in chantier's own
  checkout, which the cards run today.
- Stop, kill or signal a holder of `.venv`.
- Add a line to the CLI's output on a run, or change any existing output.
- Edit a card, a hook, a wrapper, or a version by hand.

## Gates and evidence

- `just test` passes with `tests/test_launcher.py`. `tests/test_launch_modes.py` and
  `tests/test_allow_rules.py` pass unchanged.
- The added `just test` seconds are measured before (at the base) and after (at the head) on the
  same machine and go under the PR's Deliverables. Expected: under 1 s (about 30 parametrized
  cases of pure functions on small prepared folders, with a few `git init`s).
- `just check` and `just eval-dry-run` (a change under `src/`) run in the worktree at the rebased
  head before the first push.
- The long gate `just scenario (ubuntu-latest)` is green at the PR's head, since the CLI's
  package and the scenario change. The local Windows `chantier gate <cr> scenario` is owed only
  while this CR is the stack's top; it moves to the CR that joins above it.
- The trial of section 8, recorded in the PR. Without its pass, the child hands back blocked.
- No `hooks/` or `types/` change, so `just mod` is not owed. No journal type, so no `just
  journal-schemas`.
- The shipped-file checks read `skills/chantier/scripts/chantier.py`, `src/launcher.py`,
  `src/launch.py` and `pyproject.toml` from the repository at the head under test (section 7).
- Matrix (install × project × host). The launcher's code acts the same on both hosts; the
  allow-rule match depends on the host:
  - chantier's checkout, project chantier: dev form (tests, scenario);
  - chantier's checkout, another project: plugin form from the checkout (tests, scenario);
  - plugin copy (no `.git`), project chantier: plugin form (tests);
  - plugin copy, another project: plugin form (tests);
  - Claude Code, main session, `dontAsk`: the rule matches (the trial, section 8);
  - Claude Code, auto mode or a Driver: **unproved** (one auto-mode try recorded when possible);
  - Copilot: **unproved**, no trial.

## AGENTS.md

Edit the repository's root `AGENTS.md` (as on `origin/main`):

- **The run-method bullet** ("The CLI is one Python package … One method runs it, `uvx --from
  <source> chantier`: …"): after the sentence that ends "then `uv run --no-sync --project` runs
  the local code, live;", add:

  > The plugin ships one launcher, `skills/chantier/scripts/chantier.py`, run as
  > `uv run --script "<plugin root>/skills/chantier/scripts/chantier.py" …` from uv's own
  > environment, never the checkout's `.venv`. It picks the mode by this rule and runs the CLI by
  > this one method, adding `--skill` in the plugin mode. With `--sync`, in the dev mode only, it
  > runs the checked sync: the check, the holders named read-only, the sync when there are none,
  > else `sync pending: held by …`. It stops no process, installs nothing, has no dependency of
  > its own, and runs no `uv sync` but under `--sync`. It is built on study-fable-v2's measure
  > (the `$CHANTIER` paragraph, about 2.3 KB in each of the four skills) and the user's answers
  > simplify-cards-Q18 and Q22.

- **The no-setup bullet's "chantier writes only …" sentence:** add "and, through the launcher's
  `--sync` in the dev mode, uv's sync of chantier's own checkout's `.venv`", so the sentence stays
  true.

## Risk

- The long gate is owed (the CLI's package and the scenario).
- The trial may fail. The host may not match a `uv run --script "<path>" *` rule as it matches
  today's `uv run --no-sync --project "<path>" chantier *`, or its classifier may treat the form
  as a package-manager run. The child then hands back blocked, and children 23 and 24 keep
  today's paragraph until the owner decides.
- One more process per CLI call (uv's script environment and a Python start). The trial
  measures the cost. See the open question.
- On Windows the launcher stays as the CLI's parent (no `exec` there). Whether stopping it, or
  the host stopping its shell, ends the CLI is **unproved** until section 8's stop check.
- The mode rule is now written twice: once in `launch.project_is_chantier` and once in
  `Repo.find` plus `is_chantier_project`. The parity test guards it, but a change to `Repo.find`'s
  project choice must update both.
- P10 asks for no launcher rule until child 24. A user who adds the rule early, from this
  child's PR, gets no warning about it either way.

## Open questions

1. **The launcher's overhead.** Each CLI call through the launcher starts one more Python, in
   uv's script environment, before the CLI's own. The trial records the median added time on the
   Driver's machine. Above what figure, if any, should child 24 keep today's paragraph rather than
   switch the cards to the launcher? Until you answer, the figure is only reported, and child 24
   switches whatever it is.


---

# PART 3 of 3: SC18: Role data in `roles.yaml` and a `just roles` check of the wrappers

Child 18 of 28 of the program `simplify-cards-and-prompts`. The program's `03-change-spec.md`, its
`02-answers.md` (answers 17-22) and its `work/study-*.md` rank above this specification. F9, Q3 and
the other short ids are the program's findings and questions, carried as the program settled them
(answer 22). The owner's confirmation of answer 22 at wake is pending; this child does not depend
on anything beyond it.

## Goal

The roles become one data file that the CLI and a check read, instead of tables spread through the
code and the tests. `skills/chantier/roles.yaml` holds the 18 roles: each one's name, kind, who
starts it, its tools per host, what it writes, its reply format, its card, its first line, its
description and its host specifics. `brief` (child 10) and `help --for` (child 7) read this file in
place of their current tables, and their output does not change. A new `just roles` target checks
that the hand-written wrappers of both hosts agree with the data and that their bodies are
identical. The wrappers stay hand-written (Q3). Loading a project's own roles is a later CR with its
own grill (F9).

This child only adds things to the plugin. No card, wrapper or AGENTS.md text changes, and no role
is added, removed or renamed.

## Place in the chain

- **Base: child 17's branch** (`launcher`), in the single stack batch. Rebase on it before the
  first push.
- **Reads what children 7 and 10 built** (both are below it in the stack):
  - child 10's `src/brief_roles.py` (the `RoleData` dataclass and the `ROLES` tuple of 18 roles,
    with `name`, `card`, `wrapper`, `first`, `unit`, `writes`, `rows`). Child 10's spec says child
    18 replaces it, keeping `brief`'s bytes per role;
  - child 7's `src/commands/help.py`, whose `--for <role>` checks the role against the manifest's
    `roles` map (`references/startup-manifest.json`), and child 7's test that each topic's roles
    are in that map.

  If either file is not in the stack at this child's base, the Driver stops and says so. There is
  no fallback and no hand-made copy.
- **Relies on child 9's AGENTS.md wording**: "the CLI knows roles only as data
  (`skills/chantier/roles.yaml`, read by `brief`, `help --for` and `msg steering`)". That is why
  this child adds no AGENTS.md line (see open question 1 on `msg steering`).
- **Depended on by:**
  - children 19 to 23, which write the unloaded `cards-next/` set and run
    `brief <role> --cards skills/chantier/cards-next`. `brief` reads the role table from
    `roles.yaml` from here on, and `--cards` still changes only where the cards and the floor are
    read from;
  - child 24 (the swap), whose wrapper bodies change "only where a role's first line or card path
    changed, by hand, identical on both hosts, checked by `just roles`". Child 24 edits
    `roles.yaml` (`card`, `first`, `reply`) together with the wrappers, and `just roles` proves
    the two agree;
  - child 26, whose card gates are pytest gates. It may read `roles.yaml` for each role's card,
    but this child adds no budget or history lint (those are child 26's).

## Decisions carried

| Source | Decision | Where here |
| --- | --- | --- |
| Answer 12 (Q12) | Outside roles may be review steps, critics or workers that write in the worktree, never a steering role. This program keeps only the role kinds in its data | the `kind` field, with five values |
| Answer 22, F9 | Child 18 keeps `roles.yaml`, the lint and the wrapper check as a `just` target. Project roles are a later CR | the `just roles` target and `scripts/roles_check.py`; no `roles:` key in a project's `chantier.yaml` |
| Answer 22, Q3 | Wrappers stay hand-written; `roles build` becomes a check | `--write` prints the expected wrapper and writes nothing |
| Program, child 18 | `brief` and `help --for` read the data, with the same output | sections 3 and 4; the byte evidence |
| Program, child 18 | It replaces the "bodies identical" half of `tests/test_plugin_files.py` | section 6 |
| Program, Must not | No `roles:` key in a project's `chantier.yaml` (it collides with `src/playbook/config.py`'s `ROLES_MOVED`, line 35), no written wrappers, no role added, removed or renamed | Out of scope |
| Program, Risk | The long gate is owed. No AGENTS.md change | Gates; AGENTS.md change |
| Program, rules for every child | State the seconds added to `just test`; mark unproved claims; no version edited by hand | Acceptance evidence |

## What changes

Paths are from the repository root. `src/` is `skills/chantier/scripts/cli/src/chantier/` and
`tests/` is `skills/chantier/scripts/cli/tests/`.

### 1. `skills/chantier/roles.yaml` (new)

The file is YAML, UTF-8, with LF line endings. It has a short header comment saying what reads it
(`brief`, `help --for`, `scripts/roles_check.py`), that the wrappers are hand-written and checked
against it, and that it lists the plugin's roles only. Its shape:

```yaml
version: 1
roles:
  - name: coder
    kind: worker              # steering | driver | worker | review-step | critic
    started_by: [driver]      # role names, a kind (any role of that kind), user, surface-server
    writes: worktree          # none | worktree | cr-folder
    reply: coder.md#Your part # <file>[#<heading>] under references/, or none
    card: coder.md            # path relative to skills/chantier/references/
    first: 'chantier coder for <cr> "<title>" of batch <batch>, in the project <root>.'
    description: 'Implements one round of one chantier CR in its worktree; never commits. Started by a Driver.'
    unit: cr                  # cr | order | stack | folder | none (brief's unit, from child 10)
    rows: [ending]            # child 8's capability ids that brief prints (from child 10)
    hosts:
      claude:
        wrapper: agents/coder.md
        tools: [Bash, PowerShell, Read, Edit, Write, Grep, Glob]
      copilot:
        wrapper: com.github.copilot/agents/chantier-coder.agent.md
        tools: [execute, read, edit, search]
```

What each field means:

- **`name`**: the role id. It is the agent type for the 15 roles with a wrapper, and
  `chief-of-staff`, `griller` or `foreman` for the three without.
- **`kind`**: one of the five values, as the program names them. Nothing in this child acts on
  `kind`: it is data, kept for the later project-roles CR (answer 12).
- **`started_by`**: who starts the role, taken from the wrapper description's "Started by…"
  sentence. For the three roles without a wrapper, it comes from the cards. Each token is a role
  name of the file, a kind name (meaning any role of that kind), `user` or `surface-server`.
- **`writes`**: the value child 10's `RoleData.writes` holds for the role, unchanged.
- **`reply`**: where the role's card states its reply format. A role that answers only the user
  (the three steering roles) has `none`.
- **`card`**: child 10's `RoleData.card`, unchanged. It is relative to `skills/chantier/references/`,
  so the two skill roles keep `../../chief-of-staff/SKILL.md` and `../../griller/SKILL.md`.
- **`first`**: the wrapper's `Prompt starts with:` text, the same on both hosts. It is `null` for
  the three roles without a wrapper.
- **`description`**: the wrapper's `description` cut before ` Prompt starts with:`. This is the
  cut `plugin_files.plugin_role_descriptions` already makes. For the three roles without a
  wrapper, it is one plain sentence, which nothing compares with a file.
- **`unit`** and **`rows`**: child 10's `RoleData.unit` and `RoleData.rows`, unchanged. They are
  carried here so that `brief` keeps no table of its own.
- **`hosts`**: the host specifics. For each of `claude` and `copilot`, `wrapper` is the
  repository path of the agent file (`null` for the three roles without one) and `tools` is the
  frontmatter's tool list, in the file's order. Tools are given per host because the two hosts
  name them differently (`Bash` against `execute`). A role without a wrapper has `tools: []`.

**How to fill the file.** Every value that child 10's `brief_roles.py` or a shipped wrapper already
holds is copied from there, never retyped from memory. The table below is the expected result at
`origin/main`'s wrappers and cards. Where it differs from `brief_roles.py` at the base or from a
wrapper, the shipped file wins and the PR names the difference.

| name | kind | started_by | writes | card | reply | unit |
| --- | --- | --- | --- | --- | --- | --- |
| chief-of-staff | steering | user | (child 10) | `../../chief-of-staff/SKILL.md` | none | none |
| griller | steering | user | (child 10) | `../../griller/SKILL.md` | none | none |
| foreman | steering | chief-of-staff | (child 10) | `foreman.md` | none | none |
| cr-driver | driver | foreman, chief-of-staff | cr-folder | `driver.md` | `driver.md#Means: your end` | cr |
| release-driver | driver | foreman, chief-of-staff | none | `driver.md` | `release-driver-end.md#Release driver: the end` | cr |
| stack-driver | driver | foreman, chief-of-staff | none | `driver.md` | `driver.md#Means: your end` | stack |
| qa-driver | driver | foreman, chief-of-staff | none | `driver.md` | `driver.md#Means: your end` | order |
| investigator | worker | driver | worktree | `investigator.md` | `investigator.md#Your part` | cr |
| coder | worker | driver | worktree | `coder.md` | `coder.md#Your part` | cr |
| debugger | worker | driver | worktree | `debugger.md` | `debugger.md#Your part` | cr |
| conflict-resolver | worker | driver | worktree | `conflict-resolver.md` | `conflict-resolver.md#Your part` | cr |
| verifier | worker | driver | worktree | `verifier.md` | `verifier.md#Your part` | cr |
| inspector | review-step | driver | worktree | `inspector.md` | `inspector.md#Your part` | cr |
| demo-explorer | worker | chief-of-staff | (child 10) | `demo-explorer.md` | `demo-explorer.md#Your part` | none |
| spec-writer | worker | chief-of-staff | (child 10) | `spec-writer.md` | `spec-writer.md#End` | folder |
| spec-critic | critic | chief-of-staff, griller | (child 10) | `spec-critic.md` | `spec-critic.md#Reply` | folder |
| retro-critic | critic | foreman, chief-of-staff | (child 10) | `retro-critic.md` | `retro-critic.md#Reply` | none |
| board-griller | worker | surface-server | (child 10) | `griller.md` | `griller.md#Started from the board` | folder |

The roles are listed in the file in this order. `rows` and every "(child 10)" cell are copied from
`brief_roles.py`. The `kind` column is this specification's reading of each wrapper's description,
and open question 2 asks the owner to confirm it.

### 2. `src/roles_data.py` (new): the one reader

- A frozen dataclass `Role` with the fields above (`hosts` as a mapping from host to a small frozen
  `HostSpec(wrapper: str | None, tools: tuple[str, ...])`).
- `load_roles(path: Path | None = None) -> tuple[Role, ...]` reads
  `plugin_files.skill_dir() / "roles.yaml"` with `ruamel.yaml` (`YAML(typ="safe", pure=True)`, as
  `plugin_files.plugin_role_descriptions` does). The `path` argument is for the tests' prepared
  cases. The result is cached per path.
- The loader checks the file's shape and raises `ChantierError(..., EXIT_PRECONDITION)` naming the
  role and the field when the check fails. The rules:
  - `version` is 1;
  - every field is present;
  - `kind`, `writes` and `unit` hold allowed values;
  - names are unique;
  - each `started_by` token is a name, a kind, `user` or `surface-server`;
  - `first` and both `wrapper` values are either all set or all `null`.

  The message ends "the plugin files are out of step", the wording `driver_prompt.driver_row` uses.
- `role(name) -> Role | None` and `names() -> tuple[str, ...]`, in the file's order.
- The module knows no role by name. Its docstring says the roles are data read from `roles.yaml`
  (child 9's wording).

### 3. `brief` reads `roles.yaml`

- `src/brief_roles.py` is removed. Every caller of its `ROLES` or `RoleData` (child 10's
  `src/commands/brief.py` and `tests/test_brief.py`) reads `roles_data.load_roles()` instead. The
  fields keep their names and meaning: `wrapper` becomes `role.hosts[host].wrapper is not None`.
- Child 10's unknown-role refusal (`unknown role '<x>'; roles: <list>`) lists `roles_data.names()`.
  It is the same 18 names in the same order: the file's order is child 10's `ROLES` order, and the
  Driver keeps it so.
- What the Drivers take from `driver_prompt.driver_table()` (team, rewrites, and the
  `concepts.md` table that `take` reads) stays read from there, as child 10 does. `roles.yaml`
  does not replace the `concepts.md` table: `take` still reads that table until child 24.
- No byte of a brief file or of a short prompt changes, for any role, unit or host (evidence 2).

### 4. `help --for` reads `roles.yaml`

- In child 7's `src/commands/help.py`, the role check of `--for <role>` reads `roles_data.names()`
  instead of the manifest's `roles` map. The refusal becomes
  `no role <role>; roles: <the 18 names>`.
- The output is unchanged for each of the 18 roles: its topics, or the line
  `no topic for <role>; help lists them all`. `help` with no argument and `help <topic>` are
  unchanged.
- The one visible difference: the manifest's map also holds `router` and `status`, two skills that
  are not roles. `help --for router` and `help --for status` now refuse, where they printed "no
  topic for …" before. Open question 3 asks the owner to confirm this.
- Child 7's test "each topic's role is in the manifest's `roles` map" checks against
  `roles_data.names()` instead.

### 5. `scripts/roles_check.py` (new) and `just roles`

- **Recipe**, in `justfile`, beside `journal-schemas`:

  ```
  # Check the hand-written agent files of both hosts against skills/chantier/roles.yaml (writes nothing)
  roles *args:
      {{run-cli}} scripts/roles_check.py {{args}}
  ```

  `run-cli` is `uv run --locked python`, so the script imports `chantier.roles_data` from the
  locked project: one parser for the CLI and the check. The recipe is not added to `check`,
  because `tests/test_roles_data.py` already runs the same checks on the shipped files in
  `just test`, which `just check` and CI run on the three systems.
- **Not a CLI command.** The script writes nothing anywhere: no file in the plugin, no planning
  folder, no git. It reads only files under `--root <dir>`, which defaults to the repository root
  found from the script's own path. The tests pass a prepared copy.
- **The checks.** Each failure prints one line: `roles: <role> (<host>): <what>`. The checks are:
  1. `load_roles()` on `<root>/skills/chantier/roles.yaml` passes its shape check.
  2. **Wrapper set.** Each host folder (`agents/`, `com.github.copilot/agents/`) holds exactly the
     wrapper paths the data names for that host: no file without an entry, no entry without its
     file.
  3. **Frontmatter**, per role and host, read with `ruamel.yaml` from the block between the first
     two `---` lines:
     - `name` is the role (claude) or `chantier-<role>` (copilot);
     - `description` equals `<description> Prompt starts with: \`<first>\``;
     - the tools equal `hosts.<host>.tools` in order: on claude, the comma list split on `, `; on
       copilot, the YAML list.
  4. **First line in the body.** The body holds ``My prompt must start with `<first>` `` and the
     text ``does not start with `chantier <role>`` (a prefix: the coder's body closes the backtick
     there, the board-griller's goes on with `` for the board` ``).
  5. **Card in the body.** When the body has a line `Your card is \`<x>\``, `<x>` is the
     basename of `card`. This is the "card path changed" guard that child 24 counts on.
  6. **Bodies identical.** For each role, the bytes after the frontmatter are identical on the two
     hosts.
  7. **Card exists.** `<root>/skills/chantier/references/<card>` is a file.
  8. **Reply format exists.** When `reply` is not `none`, its file exists under `references/`.
     With `#<heading>`, a line `# <heading>` or `## <heading>` exists in it, with the same text.
- **Output.** On success: `roles: 18 roles, 15 wrappers on 2 hosts agree` (the counts come from
  the data), exit 0. On failure: every problem line, then `roles: <n> problem(s)`, exit 1. A
  missing or unreadable `roles.yaml` exits 1 with one line naming it.
- **`--write <role> [--host claude|copilot]`.** Prints the wrapper the data expects, for one host or
  for both (each preceded by `=== <path>`), and writes nothing. The expected wrapper is:
  - the committed frontmatter, with `name`, `description` and the tools rewritten from the data in
    the file's own syntax, and every other key (`model`, `model-policy`, `background`,
    `autoCompactWindow`, `strict-tools-list`, `user-invocable`) kept as committed;
  - then the claude host's committed body, with the first-line texts of check 4 and the card name
    of check 5 replaced by the data's values.

  When everything agrees, the output equals the committed bytes. An unknown role exits 1, and so
  does a role without a wrapper (with the line `<role> has no wrapper`). This is the "`roles build`
  as a check" of Q3: a person editing a wrapper by hand copies from it, and nothing writes for them.
- The script is covered by `ruff` (`just lint` runs on `scripts`). It follows the repository's
  script style (`scripts/journal_schemas.py`): a module docstring, `main(argv) -> int`, and
  `if __name__ == "__main__": raise SystemExit(main(sys.argv[1:]))`.

### 6. `tests/test_plugin_files.py`: the "bodies identical" half leaves

- `test_both_hosts_give_a_role_the_same_body_and_their_own_frontmatter` drops what `just roles`
  now checks:
  - the body identity;
  - the `name` and `description` equalities;
  - the `Prompt starts with:` and `My prompt must start with` assertions.

  It keeps the BOM check, the two refusal sentences ("a message to me gets this same answer…",
  "Any later message…"), the models, `model-policy`, `user-invocable`, `strict-tools-list`, the
  `Agent`/`agent` tool rule and `background`. It is renamed
  `test_each_host_gives_a_role_its_own_frontmatter`.
- `test_the_board_griller_has_the_same_body_on_both_hosts_and_refuses_another_prompt` drops the
  body identity, the name, the description and the first-line assertion. It keeps the models,
  `model-policy`, `user-invocable`, the tools rule and `## Started from the board`.
- The tuples `DRIVERS`, `WORKERS`, `CHIEF_ROLES`, `ROLES` and `ALL_ROLES` stay. Other tests in the
  file use them, and replacing them is not in this child's scope.

### 7. `tests/test_roles_data.py` (new)

Described under Acceptance evidence, item 1.

### 8. Docstrings

Child 9 left this rewording to children 10 and 18: the docstrings that say "the CLI knows no
role" in `src/plugin_files.py` (`plugin_roles`, `worker_prompt_lines`, `agent_problems`),
`src/driver_prompt.py` (`driver_prompt_lines`) and `src/commands/__init__.py` (line 14) now say
that the CLI reads roles only as data: the agent files, or `roles.yaml` for `brief` and `help`.
Only comments change; no code changes.

## Out of scope

- A `roles:` key, or any project role, in a project's `chantier.yaml` (F9; the key collides with
  `src/playbook/config.py`'s `ROLES_MOVED`). The later project-roles CR has its own grill.
- Writing or generating a wrapper (Q3). `--write` only prints.
- Adding, removing or renaming a role (program, answer 1), and any change to a wrapper, a card,
  `startup-manifest.json`, `concepts.md`'s Driver table or a `SKILL.md`.
- Other readers of the wrappers, which keep reading the agent files: `plugin_files.plugin_roles`,
  `plugin_role_descriptions`, `chief_prompt_lines`, `worker_prompt_lines`, `agent_problems`,
  `driver_prompt.driver_row`, the playbook's role lists (`playbook/edit.py`, `layers`, `timing`,
  `limits`) and `rules`. Moving them to `roles.yaml` is not asked. Their output must not change.
- `msg steering` (child 13): it reads no role table, and this child gives it none (open question 1).
- The models, `model-policy`, `background` and the other frontmatter keys that the data does not
  hold: they stay checked by `test_plugin_files.py`.
- `roles lint`, card budgets, the history lint and rule ids (child 26).
- A CLI command: `just roles` is a script only.

## Acceptance evidence

Every check reads the shipped files from the repository at the head under test:
`skills/chantier/roles.yaml`, `agents/`, `com.github.copilot/agents/`, `skills/chantier/references/`.
A prepared copy is used only for the refusals, which the shipped files cannot hold, and each
refusal case is paired with the passing case on the shipped files.

1. **`tests/test_roles_data.py` (new)**, calling `scripts/roles_check.py` in-process through
   `conftest.load_script` and `chantier.roles_data` directly:
   - **The shipped files agree**: `main(["--root", PLUGIN_ROOT])` returns 0 and prints the
     `18 roles, 15 wrappers on 2 hosts agree` line.
   - **The data's frame**: `load_roles()` gives 18 roles; their names are those of child 10's
     brief tests (the 15 wrapper roles plus `chief-of-staff`, `griller`, `foreman`); every `kind`
     is one of the five; every `writes` is one of the three; the 15 wrapper roles on each host are
     exactly the files `test_each_host_ships_one_agent_per_role_and_nothing_else` lists.
   - **Prepared mismatches** (parametrized; each copies `agents/`, `com.github.copilot/agents/`,
     `skills/chantier/roles.yaml` and `skills/chantier/references/` into `tmp_path`, then changes
     one thing). Each returns 1 and prints the expected `roles: <role> (<host>): …` line:
     - a description word changed on one host;
     - a tool removed on copilot only;
     - the bodies differ by one character;
     - the first line changed in the data only;
     - a `Your card is` name that disagrees with `card`;
     - `card` naming a missing file;
     - `reply` naming a missing heading;
     - an extra wrapper file with no entry;
     - an entry whose wrapper file is missing;
     - a `kind` outside the five (the loader's refusal, exit 1, naming the role and the field).
   - **`--write` writes nothing**: a snapshot of the repository's tracked files under `agents/`,
     `com.github.copilot/agents/` and `skills/chantier/` (names and bytes) is unchanged after
     `--write coder`. For every wrapper role and both hosts, `--write <role> --host <h>` prints the
     committed file's bytes after its `=== <path>` line. `--write foreman` exits 1 with
     `foreman has no wrapper`.
   - **No CLI command**: `chantier --help` lists no `roles` command (in-process, `chantier.cli`).
2. **`brief`'s bytes are unchanged for each role.** At the base (child 17's head, before any edit)
   and again at the PR's head, the Driver runs a throwaway script kept in its scratch folder, not
   committed. It calls the CLI in-process on child 10's test fixture (`world` / `stack_world`) and
   records the sha256 of the brief file and of the short prompt:
   - for each of the 18 roles × 2 hosts (`CHANTIER_HOST` `claude` and `copilot`);
   - with the unit child 10's tests use, and without it for the roles that have one;
   - and once with a configured generic agent for one worker.

   The same script records `help --for <role>` for the 18 roles, `help`, and `help --for router`
   (expected to change, section 4). The two lists are identical except the `router` line. The PR
   gives both lists, or their one-line digest, and states the exception. Child 10's
   `tests/test_brief.py` and child 7's help tests pass unchanged, apart from the import switch.
3. **The removed half is covered**: the PR lists the assertions dropped from
   `test_plugin_files.py` (section 6) and names, for each, the `roles_check` check that now makes
   it (checks 3, 4 and 6).
4. **`just roles`** passes on the committed wrappers. Its output is quoted in the PR. A
   hand-made mismatch also makes it fail, shown by running it on a scratch copy and quoted in
   the PR; the committed tree stays untouched.
5. **`just test` seconds** (F20): measured before and after on the same machine, and both numbers
   stated under Deliverables. Expected: about +1 s for `test_roles_data.py` (about 12 cases, each
   a copy of about 100 small files and a parse). The trimmed `test_plugin_files.py` takes a
   little less. The budget is 30 s above 18.5 s (AGENTS.md); the ceiling is still open
   (`2-backlog/P2/test-ceiling-decision`).
6. **Host and default matrix**, one line per cell:
   - claude, shipped defaults: `just roles` on `agents/`; `brief` and `help --for` bytes on the
     claude host (evidence 2).
   - copilot, shipped defaults: `just roles` on `com.github.copilot/agents/`; `brief` bytes on
     the copilot host. These are file checks only; no real Copilot session runs (unproved in a
     real session, as the program says for all Copilot rows).
   - claude, a project's role configured as a generic agent: the worker's brief carries its
     contract lines, with bytes unchanged (evidence 2). `roles.yaml` holds no model or agent, so
     the configuration's path is untouched.
   - copilot, configured: the same, file checks only, unproved in a real session.
7. **Gates**:
   - `just check` passes;
   - `just eval-dry-run` passes (a change under `src/`; child 6's quiz calls `brief`);
   - the long gate `just scenario (ubuntu-latest)` is green at the PR's head (a CLI change);
   - the local `chantier gate <cr> scenario` is owed only if this child is the stack's top when it
     is called ready, per AGENTS.md's stack rule.

   No scenario step is added: `just roles` is not a CLI command, and `brief` and `help` keep the
   steps children 10 and 7 added. `just mod` is not owed, since nothing under `hooks/` or `types/`
   changes.

## AGENTS.md change

None. The wrappers stay hand-written, so the rule "`agents/` … are hand-written, one file per role
and host … their bodies must stay identical" stays true word for word. Child 9 already names
`skills/chantier/roles.yaml` and its readers.

## Open questions

1. **`msg steering` and the AGENTS.md sentence.** Child 9's binding wording says `roles.yaml` is
   "read by `brief`, `help --for` and `msg steering`". The program gives this child only `brief`
   and `help --for`, and child 13's `msg steering` reads no role data: its target is fixed, and its
   audience is the steering session's key or `role:steering`. Once this child lands, AGENTS.md
   overstates by one reader. Default here: leave `msg steering` and AGENTS.md as they are, and name
   the gap in the PR's Known gaps. Should child 9's sentence drop `msg steering` instead (an
   AGENTS.md edit this child would then make), or should `msg steering` read something from
   `roles.yaml`?
2. **The role kinds.** The five kinds are the program's, but the program does not assign them to
   the 18 roles. Default here:
   - steering: Chief of Staff, Griller, Foreman;
   - driver: the four Drivers;
   - review-step: Inspector;
   - critic: Spec critic, Retro critic;
   - worker: every other role, the Verifier, the Spec-writer, the Demo explorer and the board
     Griller included.

   Nothing reads `kind` in this program, but the later project-roles CR will (answer 12: an outside
   role is a review step, a critic or a worker, never steering). Confirm, or move a role, for
   instance the Verifier to `review-step`.
3. **`help --for router` and `--for status`.** Today child 7 accepts every name of the manifest's
   map, including the two skills `router` and `status`, and prints "no topic for …". Read from
   `roles.yaml`, they refuse with the 18 role names. Default here: refuse (they are not roles; the
   program counts 18). Confirm, or keep them accepted, which would put two non-roles in
   `roles.yaml`.

