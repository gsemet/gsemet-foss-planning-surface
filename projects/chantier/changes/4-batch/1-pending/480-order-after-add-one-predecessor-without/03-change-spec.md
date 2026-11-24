# order after: add or remove one predecessor, name CRs by slug or path

Short name: `order-after`. Destination: the running batch, batch-31 (order-after-Q1, B).

## Goal

Seen in batch-30: to make CR-460 also wait for CR-447, the Chief of Staff had to retype every
predecessor CR-460 already had, because `order after <cr> --note <list>` replaces the whole list.
It also had to look up CR ids, because a slug or a ready path is refused. After this CR:

- `--note` still replaces the list, as today (order-after-D1);
- `--add <refs>` adds predecessors and `--remove <refs>` removes them, and both keep the rest of
  the list (order-after-D2);
- a CR of the batch can be named by its id, its folder slug or its path (order-after-D3);
- a refusal lists the accepted forms (order-after-D4).

## Facts at main (3c29dd7c)

- `skills/chantier/scripts/cli/src/chantier/declare/orders.py` declares `order` with `kind`, the
  positional `cr` (default `-`) and the flags `--note`, `--fix-for`, `--follow-up` and `--release`.
  The `--note` help says "after: the CR ids it waits for, comma separated, or - for none".
- `commands/orders.py`:
  - `_normalise_args` splits an `after` note on `,` and runs `normalize_cr` on each part. It runs
    `normalize_cr` on `args.cr` too (`after` is in `CR_ORDERS`).
  - `_word` refuses `order after: unknown CR <cr> in batch <b>` when the target is not a CR id of
    the batch.
  - `_record_order` stores `req.note` (the normalized text) as the `OrderRecord`'s `note`.
    `_ordered` prints `[chief-of-staff→foreman] order O-k: after <cr> <note>`.
- `commands/orders_apply.py`:
  - `_after` refuses an empty note with the usage
    `order after <cr> --note "<CR ids, comma separated, or - for none>"` (exit 1).
  - It refuses the release CR as the target, and a target that is not `queued`, with a stack hint.
  - It calls `_after_ids`, sets `c.after` with `_set_after`, runs `check_cycles` (restoring the old
    list on a cycle), and logs `depends` with `after=ids`.
  - It prints `<cr> now waits for <ids>` or `<cr> waits for nothing`.
- `_after_ids` refuses an unknown id (`order after: unknown CR '<x>' in batch <b>`, exit 2), the
  release CR (a cycle), and the CR itself. It skips a merged CR (met, not recorded) and keeps the
  first occurrence of a duplicate.
- A batch CR's `path` is `4-batch/<state>/<n>-<slug>` (for example
  `4-batch/1-pending/474-the-cli-prints-the-ready-to-merge-line-i`). `lifecycle/stages.py`'s
  `cr_slug(folder_name)` strips the date and number prefixes. `commands/opening.py`'s
  `_dependency` already matches a `depends.json` slug to a batch CR with
  `cr_slug(Path(x.path).name) == slugify(slug)`.
- No module reads an `after` order's `note` back: `grep '"after"'` finds only the handler, the
  normalization and the `CrEntry.after` readers.

## What changes

### 1. Parser (`declare/orders.py`)

- Two new flags on `order`:
  - `--add <refs>`, help: "after: the CRs to add to what it waits for, comma separated; the rest
    stays";
  - `--remove <refs>`, help: "after: the CRs to take out of what it waits for, comma separated;
    the rest stays".
- `--note`'s `after:` help becomes: "after: the CRs it waits for, replacing the list (ids, slugs
  or paths, comma separated), or - for none".
- The `kind` help's `after` reads `after (--note replaces, --add/--remove change one)`.

### 2. Argument checks (`commands/orders.py`)

- `_check_args`:
  - `--add` or `--remove` on any kind but `after` is refused, exit 1 (`EXIT_USAGE`):
    `--add and --remove go with \`order after <cr>\` alone`.
  - On `after`, exactly one of `--note`, `--add` and `--remove` is given. None, or more than
    one, is refused, exit 1, with the usage line below.
  - An empty `--add` or `--remove` value gets the same usage.
- The usage line, one constant shared by `_check_args` and `_after` (it replaces today's text in
  `_after`):
  `order after <cr> --note "<refs>" (replaces the list; - for none) | --add "<refs>" | --remove
  "<refs>"; a ref is a CR of the batch: its id (CR-447, 447), its folder slug, or its path
  (3-ready/<slug>, 4-batch/1-pending/<n>-<slug>), comma separated`.
- `_normalise_args` no longer rewrites the `after` note with `normalize_cr`. The refs are
  resolved against the batch (section 3), inside the lock, where the record is read.
- The target `<cr>` of `order after` is resolved the same way, so `order after <slug> --add
  <slug>` works. `_word`'s unknown-target refusal becomes the shared ref refusal of section 3.
  `normalize_cr` on `args.cr` stays harmless: it changes only digit forms.

### 3. Resolving a ref (`commands/orders_apply.py`)

- A new function resolves one ref to a CR of the batch. It returns the `CrEntry`, or refuses:
  1. the ref, stripped, through `normalize_cr`, matches a CR id of the batch: that CR;
  2. otherwise, `key = slugify(cr_slug(Path(ref).name))`, with trailing `/` or `\` stripped
     first, so `3-ready/<slug>`, `4-batch/1-pending/<n>-<slug>`, a backlog path, an absolute
     path, a bare folder name and a bare slug all work. The CRs with
     `cr_slug(Path(x.path or "").name) == key` are the candidates:
     - exactly one: that CR;
     - more than one: refused, exit 2:
       `order after: <ref> names several CRs of <batch>: <ids>; name it by its id`;
     - none: refused, exit 2:
       `order after: <ref> is not a CR of <batch>; a ref is its id (CR-447, 447), its folder
       slug, or its path (3-ready/<slug>, 4-batch/1-pending/<n>-<slug>)`.
- The match on slugs and paths reuses `cr_slug` and `slugify`, as `opening._dependency` does.
  Nothing is copied.
- `_after_ids` takes a list of refs, resolves each with this function, and keeps its checks
  unchanged: the release CR refused, the CR itself refused, a merged CR skipped (met, not
  recorded), duplicates once. The ref refusal replaces today's `unknown CR '<x>'` message
  (exit 2, as today).

### 4. The three forms (`_after` in `commands/orders_apply.py`)

- `--note "<refs>"` or `--note -`: unchanged meaning. The list becomes exactly the resolved refs
  (D1).
- `--add "<refs>"`: the list becomes the current `c.after`, followed by each resolved ref not
  already in it, in the order given.
  - A ref already in the list changes nothing for that ref.
  - A merged ref is met and not recorded, as today.
  - The checks of `_after_ids` apply to each added ref.
- `--remove "<refs>"`: the list becomes the current `c.after` without the resolved refs.
  - Each ref must still resolve to a CR of the batch (refused as in section 3 otherwise).
  - A ref that is not in the list changes nothing for that ref.
- Each form then runs as today:
  - the release-CR target refusal and the not-`queued` refusal (with its stack hint);
  - `_set_after`, then `check_cycles` (restoring the old list on a cycle, so a refused `--add`
    leaves the list untouched);
  - `b.touch`, and the `depends` log with the resulting `after`.
- The printed line:
  - stays `<cr> now waits for <ids>` or `<cr> waits for nothing`;
  - when the order changes nothing, it ends with `(unchanged)`, for example
    `CR-460 now waits for CR-447, CR-452 (unchanged)`.
- The recorded order (`_record_order`) and the `[chief-of-staff→foreman] order O-k: after <cr>
  ...` line:
  - carry the target's id;
  - carry, as the order's note, the CR's resulting `after` as ids, comma separated, or `-` for
    none, whichever form was typed. Ids, never the typed slugs, so the Foreman reads one list.
  - `_ordered`/`_word` pass this text from the handler to `_record_order`. How is the Driver's
    choice; `Word` may carry it, as it carries `clause`.

### 5. Cards

Find each by its words at the rebased head: CR-471 (running in batch-31) cuts
`chief-of-staff.md` into pieces, so these lines may sit in another file of
`skills/chantier/references/` by then.

- The one line of the Chief of Staff card, today in step 3 of opening a batch:
  "`order after` replaces the CR's whole `after`: when the CR already waits for a real
  dependency, list it too, comma separated." It becomes: "`order after <cr> --add <cr>` adds a
  wait and keeps the others; `--note` replaces the whole list."
- The command list of the same card (today
  `$CHANTIER order after CR-104 --note "CR-102,CR-103"   # what a queued CR waits for; ...`)
  gains one line beside it:
  `$CHANTIER order after CR-104 --add CR-105   # one more wait, the rest kept; --remove takes one out; a ref: id, slug or path`.
- `concepts.md`, the "Words" entry on `after` ("`order after <cr> --note "<ids|->"` replaces the
  `after` of a queued CR (exit 2 on a CR not queued, an unknown CR or a cycle)"): it adds that
  `--add`/`--remove` change one entry, and that a ref is an id, a slug or a path.
- The chain lines ("`order after <cr> --note "<cr>"`, then `order note` ...", and
  "`order after <cr> --note -`") stay as they are. A chain on a CR with real dependencies may
  use `--add`, but the cards need not say it twice.

### Files the CR touches

- `skills/chantier/scripts/cli/src/chantier/declare/orders.py`
- `skills/chantier/scripts/cli/src/chantier/commands/orders.py`
- `skills/chantier/scripts/cli/src/chantier/commands/orders_apply.py` (if it grows past the
  project's limits, the resolver and the three forms may move to a new `commands/orders_after.py`;
  the Driver's call)
- the Chief of Staff card's line and command list above (wherever CR-471 leaves them), and
  `skills/chantier/references/concepts.md`
- `skills/chantier/scripts/cli/tests/` (one new test file) and `scenario/run_scenario.py`

CR-474 touches `commands/batch_status.py`, none of these.

## Out of scope

- Any other `order` kind's arguments. `order note`, `order drop` and the others keep reading
  `<cr>` with `normalize_cr` alone.
- `depends.json` and `open`'s dependency reading (`declare_dependencies`): unchanged.
- The release CR's `after`, which the CLI keeps: still refused as a target.
- A CR that is not `queued`: still refused. A stack's order and bases stay `stack`'s.
- The board and the web client: they show `after` as today.

## Evidence

- **Tests** (`just test`, in-process, on a prepared record): one parametrized file,
  `skills/chantier/scripts/cli/tests/test_order_after.py`, built on `batch_helpers` and
  `conftest.Chantier` as `test_mode_switch.py` is. It holds three CRs A, B, C, all queued, with
  B after A. Each case checks the exit code, `after` in `batch.json`, and the last order's
  `note`:
  - `--add C` on B: B waits for A, C. The order's note is `CR-A, CR-C`. The printed line names
    both.
  - `--add A` on B: unchanged, and the line ends `(unchanged)`.
  - `--remove A` on B: B waits for nothing (`after` absent). The note is `-`.
  - `--remove C` on B (not in the list): unchanged, exit 0.
  - `--add` naming C by its slug, by `3-ready/<slug>`, by its batch path and by an absolute path
    of its folder: the same result as the id.
  - the target named by its slug: accepted.
  - `--note "<slug of C>"`: replaces with C (D1 kept, with slugs).
  - an unknown ref (`CR-999`, `no-such-slug`): exit 2, the list unchanged. The message names
    `CR-999` and the three accepted forms (id, folder slug, path).
  - `--add` that makes a cycle (A `--add` B): exit 2, `cycle` in stderr, A's list unchanged.
  - `--note` with `--add`, and `order after B` with none of the three: exit 1, the usage line.
  - `--add` on `order note`: exit 1.
  - two CRs sharing a slug: exit 2, both ids named. The record is prepared to hold them.
- **Scenario** (`scenario/run_scenario.py`, beside the stack-batch `order after` checks that
  start "`order after` with `-` frees a queued CR"): two steps on the real CLI:
  - `order after <y> --add <slug of x>`: `after == [x]`, and the order line starts
    `[chief-of-staff→foreman] order O-k: after <y> <x>`;
  - `order after <y> --remove <x>`: `after` absent.
  The existing `CR-999` check keeps passing with the new message, since it still names
  `CR-999`. The long gate `just scenario` passes before the PR (a CLI and cards change).
- **Cards**: no check guards the changed lines' text. `just check` passes, the cards' structure
  tests included. `just eval-dry-run` passes (a change under the CLI's `src/`).
- No host or default matrix: the change depends on neither.

## Open questions

None. The answers settle the behaviour. The flag names (`--add`, `--remove`), the recorded note
(the resulting list of ids) and the `(unchanged)` suffix are the agents' call (02-answers.md:
"the command is typed by the Chief of Staff, so its form is the agents' call").
