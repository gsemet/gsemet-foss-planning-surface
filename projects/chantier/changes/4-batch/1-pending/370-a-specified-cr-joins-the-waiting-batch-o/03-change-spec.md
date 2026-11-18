# Factory mode: a CR made ready joins the open batch on its own

Short name: `ready-joins-waiting-batch`. No tracker issue (verbal, the user, 2026-11-18).
Stacked on `open-empty-batch` (`1-inbox/open-an-empty-batch-paused-waiting-for-i`, declared in this
folder's `depends.json`), merged below it: this specification assumes `chantier open` with no CR
already opens a batch born paused, with no CR (its `03-change-spec.md`), and builds on its helpers,
output, tests and card text.

## Goal

The user opens a batch to take work as it gets specified, and gives the go once. Today each CR
whose specification becomes final still needs its own `order add` and the user's go. Wanted, in
the user's words: "dès qu'une idée est en ready elle part dans le batch qui reste toujours
ouvert". This mode is called **factory**: in a factory batch, a CR moved to `3-ready` with
`triage <folder> --ready` joins the batch in the same call, as `order add` would, with no separate
go; the batch never ends by itself, and it closes only on the user's word. The README documents it.

## Decisions carried from `02-answers.md`

1. The name is **factory** everywhere: the record field, the order `order factory off|on`, the
   status word `factory: on` (answer 2; it replaces every "auto-join" of the answers).
2. A batch opened with no CR is a factory batch; `open --factory` with CRs makes one too. Without
   either, `open` makes no factory, and today's path is unchanged for it.
3. The trigger: `triage <folder> --ready` while the project's batch is a factory batch (running or
   paused) moves the CR to `3-ready` and adds it to that batch in the same call, exactly as `order
   add --note <folder> --batch <batch>` would: same checks, same refusals, same order line. A
   refusal of the add leaves the CR in `3-ready` and says why; nothing else changes.
4. The go: the user's go for the factory batch covers each CR that joins it this way; no go per CR.
5. The user's word can stop it: `order factory off|on --batch <batch> --note "<the user's words>"`,
   recorded in the batch's log.
6. Never automatic: a release CR (it needs `--release` and its own go), and a CR put in `3-ready` by
   any other path than `triage --ready` (the board's move, a folder moved by hand). Those keep
   `order add` (but see decisions 17 and 19 for the Chief of Staff's own adds).
7. The order line `triage` prints is relayed to the Foreman verbatim, as for `order add`, by the
   session that ran it: the Chief of Staff, or a Griller, who sends it to the Chief of Staff to
   relay. In direct mode the Chief of Staff takes the CR as usual.
8. CRs join in the order they become ready; in a stack batch each joins on top, as `order add` does.
9. The budget is unchanged: a CR may join past the budget; no Driver starts past it, as today.
10. `status`, the board and `brief.md` say when a batch is a factory (`factory: on`).
11. A factory batch never ends by itself: when its last CR ends it pauses as today (worktrees and
    branches cleaned), waiting for the next ready CR, and the Chief of Staff offers no retro and no
    close then. The retro and the close happen only on the user's word (`close` as today).
12. The README gets a section "Factory mode": what it is, how to open one, what joins on its own and
    what does not (a release), how to stop it (`order factory off`), how it ends (the user's
    `close`). The use-cases docs name it too.
13. Until this CR is merged the Chief of Staff applies the concept by hand to batch-28 (each CR it
    marks ready joins at once with `order add`; no close offered). Nothing to build for that; the
    Driver changes nothing about batch-28's record.
14. `order factory on` turns any open batch into a factory, one opened with CRs and no `--factory`
    included; "without either, a batch is not a factory" (decision 2) is about `open` only.
15. `order factory off` makes the batch an ordinary one: the retro and the close offer come at its
    last CR's end, or at once if it is already paused with every CR ended.
16. A release in a factory batch: when a release CR joins (`order add --release`), the factory
    turns off by itself, as `order factory off` does; the batch ends after the release as an
    ordinary one, and the Chief of Staff opens a new factory batch after its close.
17. A CR that reaches `3-ready` without joining (a Griller in a worktree, another machine through
    autosync): the Chief of Staff, when it places or sees it, runs `order add` on its own; the
    factory's go covers it. A release CR is still excluded.
18. A CR made ready with no specification (automatable) joins like any `triage --ready`.
19. CRs already in `3-ready` when a batch becomes a factory (empty `open`, `open --factory`, `order
    factory on`): the Chief of Staff adds them with `order add` at once, the factory's go covering
    them, and names them to the user. Release CRs excluded.
20. A release given at `open --factory --release N`, and `order factory on` while a release CR
    of the batch has not ended: both refused, each refusal giving the reason and the way out.

## What changes

All CLI paths below are under `skills/chantier/scripts/cli/src/chantier/`.

### The record (`core/records.py`)

- `BatchRecord` gains `factory: bool = False`. A record without the field (every batch opened
  before this CR) reads as not a factory.

### One helper for the factory switch (`commands/orders_apply.py` or a small new module)

- `set_factory(b, on, why)`: sets `b.record.factory`, logs `b.log("factory", None, factory=on,
  note=why)`, and rewrites the ` Factory: on.` / ` Factory: off.` token of `brief.md`'s first
  bullet (only that token; when absent, it appends the bullet `- Factory: on|off.`). Used by `order
  factory` and by a release joining (decision 16), so the switch is one code path.
- `ready_not_joined(repo)`: the folders of `3-ready`, sorted by name. Used for the lines of
  decisions 17 and 19 below.

### `open` (`declare/opening.py`, `commands/opening.py`, `commands/opening_record.py`)

- New flag `--factory` (`store_true`), help: "a factory batch: each CR made ready with `triage
  --ready` joins it on its own, and it stays open until the user's `close`; an `open` with no CR is
  one already".
- `new_record` sets `factory=True` when `args.factory` or `args.items` is empty (decision 2).
  `--factory` combines with `--direct`, `--mode`, `--slots`, `--budget`. With `--release N`: refused
  (decision 20), `EXIT_USAGE`, "a release CR ends a factory batch: open
  without --factory, or open the factory and add the release later with `order add --release`, which
  turns the factory off").
- `_brief_text`: its first bullet ends with ` Factory: on.` or ` Factory: off.` (always present, so
  `set_factory` can rewrite it). With no CR, the "CRs, in order" line that `open-empty-batch` writes
  reads `none yet (born paused; each CR made ready with \`triage --ready\` joins on its own)`.
- Output: the first line gains `, factory` after the steering when the batch is one (`opened
  batch-NN on claude: no CR, paused, 4 slots, stack, steering foreman, factory`). The `next:` line
  of an empty `open` (from `open-empty-batch`) becomes: `next: complete the brief <path>, then start
  the Foreman (direct mode: steer it yourself); each CR made ready with \`triage <folder> --ready\`
  joins it on its own (factory)`. With CRs and `--factory`, the existing next line gains the same
  last clause.
- When the batch is a factory and `3-ready` holds folders not among the CRs just opened (decision
  19): one more line, `3-ready holds <n> CRs not joined: <folder>, ...: the factory's go covers
  them: \`order add --note <folder> --batch <batch>\` each, a release CR excepted`.
- The `open` event in `events.jsonl` carries `factory: true` when it is one.

### `triage --ready` joins (`commands/intake.py`, `declare/intake.py`)

- `triage` keeps calling `move_item` (`lifecycle/backlog.py`) for the move. Then, only when
  `args.ready` and the project's batch (`repo.batch_folders()`, the one `4-batch/`) has
  `factory == True`, it runs the same path as `order add --note <the moved folder> --batch <batch>`
  by the Chief of Staff (actor `chief-of-staff`, no epoch): factor the body of `order()` in
  `commands/orders.py` for kind `add` into a function both call (for example
  `add_order(repo, batch, folder, actor, origin)`), so the checks, refusals, `_reopen` line,
  `apply_order` / `_add` (`add_cr`, `declare_dependencies`, `join_release`, the stack waiver) and
  `_record_order` are the very same code, never a copy. The move and the add are two lock sections
  (`changes_lock` around the move, then the add's own `changes_lock` + `RenderedBatch`), so a refused
  add leaves the move done.
- A CR in `3-ready` with no `03-change-spec.md` joins with its `intake/request.md` as its
  specification, as `prepared_cr` already allows for `3-ready` (decision 18).
- The joining stays in the `triage` command only: `move_item` itself does not join, so the board's
  move to `3-ready` (`board/write_api.py`, which calls `move_item`) joins nothing (decision 6; the
  board never edits a batch). `triage --priority` and `--inbox` never join.
- The order recorded is an ordinary `add` order (`OrderRecord`, kind `add`, `cr` `-`, `note` the
  folder), with one more key on its `order` event in `events.jsonl`: `origin: "triage --ready"`.
  The Foreman reads it in `status` like any order and ends it with `order done`.
- Output, on success, in this order: `triaged <3-ready path>`, then exactly the lines `order add`
  prints (`[chief-of-staff→foreman] order O-k: add <folder>`, `added CR-n, queued[...]`, and on a
  paused batch `<batch> stays paused: the first \`take\` sets it running again`), then one line
  `factory <batch>: CR-n joined on its own; relay the order line to the Foreman (direct mode: take
  it)`.
- On a refused add (any `ChantierError` of the add path: a release CR already started, a
  `depends.json` naming an unknown slug or a cycle, a closing batch): stdout keeps `triaged
  <3-ready path>`; stderr says `not joined <batch>: <the refusal's text>; the CR waits in 3-ready
  (\`order add --note <folder> --batch <batch>\` once fixed)`; the exit code is the refusal's.
  Nothing else changes (no order, no event).
- The `triage` help text names it: `--ready`: "the CR waits in 3-ready for the next batch; in a
  factory batch it joins that batch at once, as `order add` would".
- A release CR never joins this way: the CLI cannot tell one (a CR is a release only by
  `--release`); the cards keep it out (below). A CR already in `3-ready` cannot be triaged `--ready`
  again (the move is refused today: `3-ready already holds <name>`), so it joins only by `order add`.

### `order factory off|on` (`declare/orders.py`, `commands/orders.py`, `commands/orders_apply.py`)

- New kind `factory`; the positional is `on` or `off`; `--note` (the user's words) is required.
  Usage on any other form: `order factory on|off --note "<the user's words>"` (`EXIT_USAGE`). The
  kind is not in `CR_ORDERS`; `_normalise_args` leaves the positional as given.
- Handler `_factory`: refuses a batch already in that state (`<batch> is already a factory batch` /
  `<batch> is not a factory batch`, `EXIT_PRECONDITION`) and a closing batch (as `_mode` does);
  `on` while a release CR of the batch has not ended: refused (decision 20, `EXIT_PRECONDITION`),
  "a release CR is in <batch>: it ends the factory; open a new factory batch after the close").
  Else `set_factory`. Turning on any open batch is accepted (decision 14).
- The order is recorded **done at once** (`done=now()`, `applied: true`): the CLI did its whole
  part, and an open order is a cause `running()` in `rails.py` (line ~72, through `check_idle`)
  gives to refuse `close`, so an undone `factory` order would block the close of a batch no
  Foreman ever steered. The order line is still printed and relayed to the Foreman (it changes how
  the Foreman ends the batch); the Foreman sends no `order done` for it.
- Effect lines: `factory on: each CR made ready with \`triage --ready\` joins <batch> on its own;
  it stays open until the user's \`close\``, plus, when `3-ready` holds folders, the `3-ready holds
  <n> CRs not joined` line of `open` (decision 19). `factory off: ready CRs no longer join <batch>;
  it ends as any batch: at its last CR's end, the retro, then the close offer` (decision 15).
- `order factory off` on a batch that is paused with every CR merged or cancelled: one more line,
  `every CR is merged or cancelled: next: the retro (with its critic), then offer the close`, the
  line `end_of_batch` prints today. On a batch that never held a CR (`not d.crs`), that line is
  instead `no CR ever joined <batch>: next: offer the close (\`chantier close\`, then \`close --yes\`
  on the user's yes); no retro` (no retro, no retro critic).

### A release joining turns the factory off (`commands/orders_apply.py`, `_add`)

- In `_add`, the `w.release` branch: once `add_release` has succeeded on a factory batch,
  `set_factory(b, False, "release CR <id> joined")` and one more line, `factory off: the release CR
  <id> joined; <batch> ends after the release as an ordinary batch; after its close, open a new
  factory batch` (decision 16). `--fix-for` adds (fixes of the release) change nothing here.

### The end of the last CR (`commands/endpause.py`)

- `end_of_batch`: the cleanup and the pause are unchanged (decision 11). Its last `next:` line
  depends on the record: a factory batch prints `next: factory <batch> waits for its next ready CR
  (\`triage <folder> --ready\`): no retro and no close now; they come on the user's word (\`order
  factory off\`, then the retro and the close offer)`; any other batch prints today's line.
- `pause --epoch <n>` and `close` (`commands/closing.py`) are unchanged: `close` takes no factory
  check (the user's word and the cards order it).

### `status`, STATUS files (`commands/batch_status.py`, `status/views.py`, `status/markdown.py`, `core/surface_batches.py`)

- `_batch_line`: after `shape <...>`, ` factory: on` when the record's `factory` is true; nothing
  when false.
- For a factory batch, one more line when `3-ready` holds folders (decision 17): `factory: 3-ready
  holds <n> CRs not joined: <folder>, ...: \`order add --note <folder>\` each, a release CR
  excepted`.
- `open-empty-batch`'s line `no CR yet: \`order add --note <folder> --batch <batch>\` joins one`
  reads, for a factory batch, `no CR yet: \`triage <folder> --ready\` joins one on its own`.
- `batch_view` gains `"factory": d.factory`. `batch_markdown` adds ` · factory: on` after the shape
  in its header line when true.
- `surface_batches.py`'s one line per project gains `, factory on` when true.
- The CR board pane (`hooks/register.tsx`) draws nothing new: it does not read `factory`. No pane
  change, so no screenshot is owed by this CR (the pane's "no CR yet" is `open-empty-batch`'s).

### The web board (`board/state.py`, `board/web/`)

Read `board/web/DESIGN.md` first and keep it true.

- `board/state.py`: `VIEW_KEYS` gains `"factory"`; the PRs page's `batch` dict (line ~230,
  `("id", "state", "mode", "steering")`) gains it too.
- `js/views/batch.js`, the mode strip (`${words.name} · ${steeringWord(batch)}`): ` · factory: on`
  when `batch.factory`. `js/views/home-batch.js`, the card's `sub` (`mode · steering`): the same.
- The empty state `open-empty-batch` adds (`batch.no_cr_yet`, Batch page and home card) gets a
  factory variant, `batch.no_cr_yet_factory`, used when `batch.factory`: en `Paused, no CR yet:
  each CR made ready with triage --ready joins on its own.`, fr `En pause, aucune CR encore :
  chaque CR passée en ready avec triage --ready la rejoint d'elle-même.`
- i18n: `batch.factory_on`, en `factory: on`, fr `factory : activée`, and the key above, in the
  en and fr files that hold the batch page's words (`steering.*` is in `js/i18n/en.js`, `fr.js`).

### Cards (`skills/chantier/references/`)

- `chief-of-staff.md`:
  - The entry-points table (line ~29, beside the `final` row): a row "the Foreman's `ready
    <batch>` at a factory batch's pause | the progress and completion report; no retro, no close
    offer: the batch waits for its next ready CR | While it runs".
  - "Backlog and grill" (the `triage --ready` sentence, line ~318) and the command list (line
    ~199): in a factory batch, `triage --ready` (still only on the user's word) also joins the CR;
    relay the order line it prints to the Foreman verbatim (direct mode: take it as usual); a
    refused join leaves the CR in `3-ready` with the reason: fix it, then `order add`.
  - A CR in `3-ready` that did not join (placed from a Griller's worktree, arrived through
    autosync, named by `status`'s `3-ready holds ... not joined` line): run `order add --note
    <folder>` on your own, the factory's go covering it, and relay its line (decision 17).
  - When a batch becomes a factory (empty `open`, `open --factory`, `order factory on`): add every
    CR the CLI names in `3-ready` with `order add` at once and name them to the user (decision 19).
    In both cases a release CR is excepted.
  - Starting a batch, step 2 (the plan) and step 3 (open): an empty `open` is a factory batch;
    `open --factory` makes one with CRs; the plan says "factory: on" and that the go covers each CR
    that joins it. The `open` usage block gains `[--factory]`. Step "While a batch is not closed...
    new work joins it with `order add`" (line ~794): in a factory batch, by `triage --ready`.
  - A release CR in a factory batch: never moved by `triage --ready` while the factory is on; it
    joins with `order add --note <folder> --release` on its own go (its folder may be in the inbox
    or the backlog); that turns the factory off (the CLI says so): the batch ends after the release
    as an ordinary one, and after its close you offer to open a new factory batch (decision 16).
  - "What you accept while you steer" (lines ~1557, ~1563): `triage --ready` joins no CR to the
    running batch, except a factory batch, where it joins as above.
  - Order list (line ~953): `order factory on|off --note "<the user's words>"`, on the user's word.
  - The pause (Foreman-mode pause, line ~1306; "The pause" of direct mode, line ~1573): at the
    pause of a factory batch, give the progress and completion report as usual, then say the batch
    waits for its next ready CR; offer no retro and no close, and start no retro critic. Ending it:
    on the user's word to end or close a factory batch that held CRs, run `order factory off
    --note "<the user's words>"`, relay its line; if CRs remain, the batch ends as any batch at its
    last CR's end; if none remains, the retro (with its critic) is written now (by the Foreman, who
    sends `final`; in direct mode by you), then the close offer, as today. A factory batch that
    never held a CR: the user's close goes straight to `close` (the check, then `close --yes` on the
    yes), no retro and no critic.
- `foreman.md`:
  - "Your goal": in a factory batch, the end of the last CR pauses the batch, but you write no retro
    and send no `final`: send `[foreman→chief-of-staff] ready <batch>` (the line `open-empty-batch`
    gives an empty batch) and wait for the next order, ready, not done; your first `take` sets the
    batch running again. The retro and `final` come once the batch is no longer a factory (`order
    factory off`, or a release CR joining) and every CR has ended. Its retro section is headed with
    the date and the CRs since the last section of `4-batch/retro.md` (all the batch's CRs when
    there is none).
  - Orders: an `add` order whose event says `origin: "triage --ready"` is an ordinary `add`; a
    `factory` order is done at once by the CLI: no `order done` for it.
  - Heartbeat: none while a factory batch is paused; the turn of the first `take` after it arms it
    (the same rule `open-empty-batch` gives a batch born paused with no CR).
- `griller.md`: "Never" keeps `order`, with one exception named: in a factory batch your `triage
  --ready` (on the user's word) records an `add` order itself; send its order line, verbatim, as
  `[griller→chief-of-staff] <the order line>` by the host's means, for the Chief of Staff to relay;
  with no live Chief of Staff, tell the user (the Foreman still sees the order in `status`). A
  refused join: tell the user the reason; the CR waits in `3-ready`. In a worktree you run no
  `triage`: the Chief of Staff places the files and adds the CR (decision 17).
- `routing.md`: the Griller → Chief of Staff row (line ~14) gains `<the order line>` (the `add`
  order its `triage --ready` printed in a factory batch, passed as printed); the Foreman → Chief of
  Staff row's `ready <batch>` notes "(also at a factory batch's pause)". Line ~32 ("Grillers send
  nothing else") stays true with the row extended.
- `hosts/copilot.md`, "Heartbeat" (line ~61), and `hosts/claude-code.md`, "Heartbeat": the
  sentences `open-empty-batch` adds for "a batch born paused with no CR" are widened to "a batch
  born paused with no CR, or a factory batch at its pause": on Copilot the Chief of Staff sends no
  `/every` on that `ready <batch>` (it tells the user to delete the `/every` at the pause, as at
  every pause) and arms it with the next order; on Claude Code the Foreman arms its own `/loop` only
  in the turn of its first `take`.
- `concepts.md`, "Batch lifecycle": a factory batch (opened empty, with `--factory`, or by `order
  factory on`) takes each CR made ready with `triage --ready` at once; at its last CR's end it is
  paused with no retro and no close offer; it ends on the user's word (`order factory off`, then
  the retro and the close; a batch that never held a CR goes straight to the close), or after a
  release CR it took, which turns the factory off.
- The agent files (`agents/`, `com.github.copilot/agents/`) are not touched.

### Docs

- `README.md`: a section `## Factory mode` after "Batch modes": what it is (a batch that stays
  open; each CR the user makes ready joins it on its own, on the go given once); how to open one
  ("open an empty batch", or ask for a factory: `open --factory`, or `order factory on` on the open
  batch); what joins on its own (a CR made ready with `triage --ready`, specified or automatable)
  and what does not (a release CR, which joins with its own go and turns the factory off; a CR moved
  on the board, which the Chief of Staff adds itself); how to stop it (`order factory off`, on your
  word); how it ends (your `close`: the retro, then the close). One sentence on the budget: CRs may
  join past it, no Driver starts past it.
- `docs/use-cases.md` ("The life of a batch" or "Turn ideas into ready work"): one paragraph naming
  the factory mode and linking the README section. `docs/use-cases-foreman.md` and
  `docs/use-cases-direct.md`, "When the batch is paused, and when you close it": one sentence each
  on a factory batch's pause (no close offer; ends on your word).
- `docs/batch-lifecycle-texts.md` (sections "Paused", "Paused to running", "Paused to closed",
  lines ~97-130) and `docs/batch-lifecycle.svg`, changed together as CONTRIBUTING.md asks for these
  pairs: "Paused" gains `a factory batch: no close offered; it waits for its next ready CR`;
  "Paused to running" gains `or, in a factory batch, triage --ready`; "Paused to closed" gains `a
  factory batch: order factory off, then the retro and the close`.

### `open-empty-batch`'s tests and scenario leg, updated here

- Its test 1 (`open` with no item: the output's second line names `order add` and the Foreman)
  now expects the factory `next:` line (`triage <folder> --ready` joins on its own) and
  `factory: true` in `batch.json`.
- Its test 5 (`status` on the empty batch: `no CR yet` and the `order add` line) now expects the
  factory form `no CR yet: \`triage <folder> --ready\` joins one on its own` and `factory: on` on
  the batch line.
- Its scenario leg: if it opens the scenario's main batch empty, that batch is a factory: its last
  CR's end prints the factory `next:` line, so the leg runs `order factory off --note "<words>"`
  before the scenario's retro and close steps, and any check on the end's `next:` line expects the
  factory form there. Its separate empty batch closed with `close --yes` needs no change (a batch
  that never held a CR goes straight to the close, and the `factory` order is done at once).

## Host and default matrix

Only the heartbeat at a factory batch's pause depends on the host; nothing depends on a configured
value.

- Claude Code, Foreman mode: at a factory pause the Foreman stops its `/loop` as at every pause and
  arms it again only in the turn of its first `take` after it.
- Claude Code, direct mode: the Chief of Staff does the same in its own session.
- Copilot, Foreman mode: at a factory pause the Chief of Staff tells the user to delete the
  `/every`, as at every pause, sends none on the Foreman's `ready <batch>`, and arms it with the
  next order it sends.
- Copilot, direct mode: the Chief of Staff runs no `/every` while the factory batch is paused,
  until its first `take` (unproved, as the host reference already says of direct mode).

## Out of scope

- The board joining a CR (its move to `3-ready` never joins; it edits no batch).
- A release CR joining on its own; any change to `--release`, `order grant` or the release rails
  beyond the factory turning off when a release joins.
- Any change to `take`, `pause`, `close`, the watcher, the forge hub or the pane.
- Joining from a folder moved into `3-ready` by hand or by the board, other than the Chief of
  Staff's own `order add` (decisions 17 and 19).
- batch-28's record (decision 13 is the Chief of Staff's by hand).

## Evidence

Tests (`skills/chantier/scripts/cli/tests/`, in-process with the `chantier` fixture, parametrized,
few; in `test_triage_moves.py`, `test_opening_and_restore.py`, `test_batch_end.py`):

1. `triage <inbox folder> --ready`, parametrized over: factory batch running, factory batch paused,
   non-factory batch, no batch. Factory: the CR is queued in the batch, one `add` order recorded
   with its `order` event's `origin: "triage --ready"`, output as specified (the paused case also
   prints `stays paused`); the others: only `triaged <path>`, no order. One factory case uses a CR
   with only `intake/request.md` (no `03-change-spec.md`): it joins.
2. A refused join, parametrized over two causes (a `depends.json` naming an unknown slug; the
   batch's release CR started): the folder is in `3-ready`, the exit code is the refusal's, stderr
   names `not joined` and `order add`, no order and no `add` event recorded.
3. `triage --priority` / `--inbox` on a factory batch: no join. `move_item` called as the board
   does (`board/write_api.py`'s path) to `3-ready`: no join.
4. A stack factory batch: two `triage --ready` in a row; the second CR's `order` is above the
   first (joins on top).
5. `open` with no item and `open --factory <folder>`: `factory: true`; `open <folder>` without the
   flag: `false`; `brief.md`'s first bullet holds `Factory: on.` / `Factory: off.`; with a folder
   left in `3-ready`, the `3-ready holds ... not joined` line names it. `open --factory --release
   1 <folder>` refused.
6. `order factory off` then `on`, with `--note`: the record flips, `brief.md`'s token is
   rewritten, a `factory` event and an order with `done` set are recorded; a repeat, a missing
   note, or `maybe` are refused. On a paused batch with every CR ended, `off` prints the `next: the
   retro...` line; on a batch that never held a CR, the `no CR ever joined ... no retro` line.
7. `close` (the check, then `--yes`) of an empty factory batch after `order factory off`, with the
   steering transcript the close tests prepare: accepted (the done `factory` order is no cause in
   `running()`).
8. `order add --release` on a factory batch: the record's `factory` turns false, the `factory off:
   the release CR ... joined` line is printed, `brief.md` says `Factory: off.`.
9. `end_of_batch` (`test_batch_end.py`): the last CR merged in a factory batch pauses and cleans as
   today and prints the factory `next:` line, never "offer the close"; a non-factory batch prints
   today's.
10. `status`: `factory: on` on the batch line only when true; the `3-ready holds ... not joined`
    line for a factory batch with a folder in `3-ready`; `STATUS.json` `factory`; STATUS.md header.
11. `open-empty-batch`'s tests 1 and 5, updated as above.

The card and docs checks, if `just check` holds any on these words, read the shipped
`chief-of-staff.md`, `foreman.md`, `griller.md`, `routing.md`, the host references, `README.md`
and `docs/batch-lifecycle-texts.md` at the head under test, never a copy.

Board: per `DESIGN.md`; the board's tests that read `VIEW_KEYS` / the batch strip extended by one
case for `factory: on` and one for the factory empty state.

Scenario (`scenario/run_scenario.py`): in the `direct` unit (`direct_batch`, or a new case in that
unit's list), after an empty `open --direct` (from `open-empty-batch`): `triage <inbox folder>
--ready` joins it (queued, still paused), the first `take` sets it running, the CR merges, the batch
pauses with the factory `next:` line; `order factory off --note ...` then prints the retro line;
`close --yes` closes it. Plus `open-empty-batch`'s leg adapted as above. Map each check to its
bullet in `scenario/README.md`'s coverage list (`(unit: direct)`), and adjust the unit's budget
literal if needed. The CLI and cards change passes the `just scenario (ubuntu-latest)` job before
its PR; the Driver runs `just check` and `just eval-dry-run` in its worktree at the rebased head
before the first push (AGENTS.md). `just test` stays within its budget.
