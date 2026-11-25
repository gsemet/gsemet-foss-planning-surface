# SC15: The early conflict check as a command

Child 15 of 28 of the program CR `simplify-cards-and-prompts`. The program's `03-change-spec.md`,
"Child 15", its `02-answers.md` (answers 17 to 22) and its `work/study-*.md` rank above this file.
One Driver and one PR, in the running stack batch (batch-31). Code read: `origin/main` at
`8a960d34`. Short forms used below:

- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`;
- `scenario/` is the repository's root `scenario/` folder;
- `the card` is `skills/chantier/references/foreman-conflict.md` as it ships at the base.

## Goal

The owner's words (answers 1, 17 and 18): the cards are far too heavy; what a tool can do moves
into the CLI, and the tools land before the rewrite. The Foreman's early conflict check of a
parallel batch is 3,789 bytes of card (`foreman-conflict.md`, study-fable-v2 section 3; study-fable
4.2 (e): "3.5 KB that fix a `git merge-tree` command, its exit codes, the note to record and the
ask to send"). This child turns that check into one command, `chantier conflicts <cr> --epoch N`:
it runs the pairs, records the notes and prints the one ask. Child 21 (the Foreman's new card)
then replaces the piece with one line naming the command.

This child only adds things: one command and one `core/git.py` helper. No card text changes
(program rule: no child before 19 edits a card). The old card keeps working on every
intermediate `main`: a Foreman on the old cards still types the `git merge-tree` itself, and the
scenario's scripted Foreman keeps doing so.

## Place in the chain

- **Base:** child 14's branch (`sc14-judge-asks`), the previous CR of the stack. Children 1 to 14
  are below it.
- **What it uses from below:**
  - nothing of child 14's code (`judge` words a readiness ask; `conflicts` prints a different ask);
  - child 3's rule that a refusal names the next command, followed by every refusal added here
    (child 3's gate scans only `rails.py`, `rails_release.py`, `rails_idle.py` and
    `core/leases.py`, so the new texts are outside its scan; they follow the rule anyway);
  - child 1's edit of AGENTS.md's git-exceptions bullet (the push subcommand). This child adds
    its own clause to the same bullet. Rebase conflicts are line-level only.
- **Shared files with neighbours:** `src/cli.py` (`_MODULES`, `FULL_OUTPUT`), `src/core/git.py`,
  `AGENTS.md`, `scenario/run_scenario.py` and `scenario/README.md`. Each child adds its own lines.
- **What depends on it:**
  - child 16 (`retro-draft`) sits on top of it;
  - child 21 (the Foreman's family of cards) and child 22 (the Chief of Staff in direct mode, who
    gets the Foreman's tools: answer 13) write the one line that sends the Foreman to
    `conflicts` at a ready hand-back of a parallel batch;
  - child 24 (the swap) removes `foreman-conflict.md` with the old set;
  - child 25's review checks that each rule of the old piece is found again in the command, its
    output or its refusals;
  - child 28 sees the command run (or not) in a real parallel batch, if the campaign has one.

## Decisions carried

| Source | Decision | Where |
| --- | --- | --- |
| Program, Child 15, Scope | `chantier conflicts <cr> --epoch N` runs the early conflict check the card describes; it records notes on the CRs and prints one ask | sections 1, 2 |
| Program, Child 15, Scope | The git read is `git merge-tree --write-tree`; it needs git 2.38 or later, which the repository does not pin; it writes objects and no ref. The command checks `git --version` first and refuses on an older git with the version needed | sections 1, 3 |
| Program, Child 15, Scope; Pending items (F15) | Distinct from `1-inbox/pr-conflict-detect-and-rebase-order`: no shared code, stays Foreman-run, read-only on the forge (it reads no forge at all) | "Relation to the server's conflict scan" |
| Program, Child 15, Must not | No ref, no branch, no worktree touched; no rebase started | sections 1, 5 (test 5), "Out of scope" |
| Program, Child 15, Risk; AGENTS.md lines rule | AGENTS.md: the git exception with its object writes, and the tool's line with its source | section 6 |
| Program rules | New command: a scenario step and a coverage bullet. The added `just test` seconds stated. Long gate owed. No version edit. No card edited | sections 4, 5, 7, "Gates and evidence" |
| Program rules (F17) | A claim not proved here is marked "unproved": the `merge-tree` form on the CI runners' git | "Risk" |
| Answer 11 (simplify-cards-Q11) | The CLI words the ask; the steering session sends it. The command never decides the switch to a stack | sections 1, 2 |
| Answer 13 (simplify-cards-Q15) | In direct mode the Chief of Staff runs the Foreman's tools, so it runs `conflicts` with its own `--epoch` | section 1 |

**On "the batch's other working CRs"** (the program's scope line): the card's pairs are the other
CRs that are `ready` with an unmerged PR on the default branch. The program says the command runs
"the early conflict check that `foreman-conflict.md` describes", so the card's selection is the
one implemented (section 2); a CR still `working` has no PR to check against.

## What changes

### 1. The command `chantier conflicts` (new `src/declare/conflicts.py`, handler in new `src/commands/conflicts.py`)

**Form:**

```
chantier conflicts <cr> --epoch N [--batch B]
```

- Declared with `add_command(sub, "conflicts", "chantier.commands.conflicts:conflicts", <help>,
  BATCH_EPOCH)`, with one positional `cr` (normalized as other commands do, `core.ids`).
- Help string: "the Foreman's early conflict check of a parallel batch, at a ready hand-back: the
  CR against each other ready PR on the default branch, by `git merge-tree` only; notes each
  conflict on the CR and prints the one ask to send".
- `from chantier.declare import conflicts` and `conflicts` added to `_MODULES` in `src/cli.py`;
  `"conflicts"` added to `FULL_OUTPUT` (one line per pair plus the ask can pass `MAX_LINES`).
- A profile's `cli.run` runs it like any command not in its refused list (it then reads the
  server machine's clone). No change there.

**What it does, in this order:**

1. `require_epoch(args.epoch, "conflicts <cr> --epoch <n>")` (`core/batch.py`). A missing
   `--epoch` exits 2, as every steering command does.
2. **The git version** (section 3). An older or unreadable git refuses here, before anything is
   read or written.
3. `RenderedBatch(repo, find_cr_batch(repo, args.cr, args.batch), actor="foreman")`, then
   `check_epoch(b, args.epoch)` (a stale steering session exits 3). Everything below runs inside
   that block, so the "already noted" test and the note it guards are one step under the
   lifecycle lock. The git reads are a few milliseconds per pair, well under the lock's 30 s
   bound (`store/folder.py`).
4. **The batch's mode.** When `b.record.mode` is not `parallel` (`series` or `stack`), it prints
   one line and exits 0, running no git and writing nothing:
   `conflicts: not run: <batch> is a <mode> batch, where the PRs sit on one another; a conflict there is the stack driver's anomaly`.
   A `None` mode reads as `parallel` (a batch with no mode named is parallel, scenario 13b).
5. **The CR itself.** The CR must be `ready` with a PR (`c.status == "ready"` and `c.pr`). Else
   it refuses, exit 2 (`EXIT_PRECONDITION`), nothing written:
   `conflicts: <cr> is <status>[ with no PR]: the check runs at its ready hand-back with a PR; run conflicts <cr> --epoch <n> once it is handed back ready`.
6. **The pairs** (section 2). With no candidate, one line, exit 0:
   `conflicts: <cr>: no other ready PR on <default branch> to check against`.
7. **One read per pair,** from `repo.root` (the main checkout, or in external mode the project's
   clone, the one `take` names), with each CR's recorded `branch` (as `handoff <cr>` prints it):

   ```
   git merge-tree --write-tree --name-only --no-messages <cr's branch> <other's branch>
   ```

   run through a small wrapper over `subprocess.run` that returns the exit code, stdout and
   stderr (the existing `core.git.git` raises on any non-zero exit and so cannot tell exit 1 from
   a failure; `core.git.is_ancestor` is the model to follow: same environment, `check=False`).
   - Exit 0: no conflict.
   - Exit 1: a conflict. The lines after the first (the tree id) are the conflicting paths,
     deduplicated in their order.
   - Any other exit (a missing ref, a git that refuses): the pair is **not run**; the first line
     of git's stderr (else stdout, else `git exited <code>`) is kept.
   - No other command ever: no trial merge in a checkout, no `git merge`, no `git rebase`, no
     worktree, no `fetch` (the card's "never fall back").
8. **The notes,** on the CR given, through the same path as `note` (`c.append("notes", text)`,
   `b.touch(c)`, `b.log("note", c.id, note=text)`, as `commands/driver_notes.py` `note` does):
   - per conflicting pair: `early conflict: with <other id>: <paths>`, at most five paths joined
     with `, `, then ` and <k> more`;
   - per pair not run: `early conflict check: not run against <other id>: <git's first line>`.

   The note texts are the card's, word for word, so a pair noted by a Foreman on the old card
   and a pair noted by the command are the same note, and each sees the other's as "already
   noted". They hold the bare id (a record line, not a message to a person).
9. **The ask.** When at least one pair conflicts, it builds the card's one ask for this hand-back,
   covering every new conflicting pair:
   `conflict <cr name> with <other name>[, <other name>…]: <paths>; switch to a stack?`, where
   `<paths>` is every conflicting path of those pairs, deduplicated in order, and each CR is named
   by number and slug together, `CR-<n> <slug>` (concepts.md, "A CR's name": the ask goes to the
   user). The slug is the CR folder's name without its number prefix (`Path(c.path).name`, the
   part after the first `-`); a CR with no `path` gets `slugify(c.title)`, the helper
   `came_back.py` already uses. The ask holds no other proposal.

   The command **prints** the ask; it does **not** record it (the program: "prints one ask"; the
   steering session sends it, as answer 11 keeps the sending with it, and as child 14's `judge`
   prints unless `--record`). The steering session sends it with the printed `asks` line.

**Output** (exit 0 whenever the check ran, conflicts or not):

1. `conflicts: <cr> against <n> ready PR(s): <c> in conflict, <k> clean, <s> skipped (already noted or chained), <f> not run`
2. One line per pair checked, in the record's `order`:
   - `<cr> x <other>: clean`
   - `<cr> x <other>: conflict in <paths, as in the note>; noted`
   - `<cr> x <other>: not run: <git's first line>; noted`
3. One line per skipped pair: `<cr> x <other>: skipped: already noted` or `skipped: chained`.
4. When at least one new conflict: `next: asks "<the ask>"`.
   With none, no ask line, and nothing more to do.

### 2. Which pairs (the card's "Which pairs", in `src/commands/conflicts.py`)

The CR given, against each other CR `o` of the batch such that:

- `o.id != c.id`, `o.status == "ready"` and `o.pr` is set (not merged, not cancelled: those have
  other statuses);
- `o`'s PR targets the default branch: `o.pr_base` is the default branch
  (`repo.config["default_branch"]`), or `o.pr_base is None` (never read by `ship`; in a parallel
  batch a PR's base is the default branch unless it started on another CR's branch, tested next).

A candidate is **skipped as chained** when either CR's base is the other's branch:

- `o.id in c.after` or `c.id in o.after` (the `after` list holds the `depends.json` dependencies
  and the `order after` ones);
- `c.start_on == o.branch` or `o.start_on == c.branch`;
- `c.pr_base == o.branch` or `o.pr_base == c.branch`.

A candidate is **skipped as already noted** when either CR holds a note that starts with
`early conflict: with <the other's id>` followed by `:` or a space (the card: "a pair already
noted on either CR gives neither a note nor an ask again"). A pair noted only as "not run" is
checked again (it gave no answer).

### 3. The git version (`src/core/git.py`)

- New `def version() -> tuple[int, int, int] | None`: runs `git --version` (through the same
  environment as `git`), parses `git version <a>.<b>.<c>…` (Windows prints
  `git version 2.56.0.windows.4`), and returns `None` when git is absent or the text does not
  parse.
- `MERGE_TREE_WRITE = (2, 38, 0)` in `src/commands/conflicts.py`.
- Refusal, exit 2, nothing read or written, one line:
  - older: `conflicts: git <a.b.c> is older than 2.38, which git merge-tree --write-tree needs: update git, then run conflicts <cr> --epoch <n> again`;
  - unreadable: `conflicts: cannot read git's version (git --version: <text or "not found">): git 2.38 or later is needed`.
- The check runs on every call, also in a series or stack batch, before the mode is read, so its
  refusal is the same whatever the batch.
- With the check first, the card's "a git older than 2.38" case becomes a refusal instead of a
  "not run" note per pair: no note is recorded for it.

### 4. Scenario (`scenario/run_scenario.py`, `scenario/README.md`)

In section 13b ("The three modes: parallel by default, series, the switch to a stack"), the early
conflict check's block (the `two_ready`, `hand_back`, `merge_trees` and `conflict_asks` helpers,
unit `series-deps`), after the scripted Foreman's checks and before the stack case
(`two_ready(("Early stacked first", …), "--mode", "stack")`):

- `fm, first, second = two_ready(("Early cmd first", "Early cmd second"))`, then
  `hand_back(first, 1)` and `hand_back(second, 2)` with **no** `fm.turn()` in between, so the
  scripted Foreman's own check does not run.
- `code, out = w.chantier("conflicts", second, "--epoch", 1)`. Check: exit 0; the CR `second`
  holds the note `early conflict: with <first>: shared.py`; the last line is
  `next: asks "conflict <second> <slug> with <first> <slug>: shared.py; switch to a stack?"`; the
  batch has no new ask (`w.batch()["asks"]` unchanged: the command prints, it does not record);
  the mode is still `parallel` and both CRs `ready`; `git for-each-ref` of the world's repository
  is the same before and after.
- A second `w.chantier("conflicts", second, "--epoch", 1)`: exit 0, the pair `skipped: already
  noted`, no `next:` line, one note only.
- In the stack world that follows (after its two hand-backs), `w.chantier("conflicts", second,
  "--epoch", 1)`: exit 0, `conflicts: not run: … is a stack batch …`, no note added.

The README's early-conflict-check bullet gains: "`chantier conflicts <cr> --epoch <n>` gives the
same note and prints the same ask, records no ask, notes a pair once, and runs nothing in a stack
batch" with `(test: test_conflicts.py::<the conflict test>)` and
`(test: test_conflicts.py::<the old-git test>)`. `tests/test_scenario_coverage.py` checks that
both names exist. The `series-deps` unit's budget holds: the steps add a few git calls and a few
CLI calls.

The scripted Foreman's `early_conflicts` is **not** changed: it follows the old card, which stays
the shipped card until the swap (child 24 switches it to the command).

### 5. Tests: new `tests/test_conflicts.py`, few and parametrized

They call the CLI in-process (`conftest.Chantier`, the `repo` fixture), on a parallel batch of
three CRs opened with `batch_helpers.open_batch` and set `ready` with a PR and a branch through
`write_record`. Each CR's branch is made in the prepared repository with `conftest.sh` (`git
branch`, a commit on a scratch worktree or with `git commit-tree`/`update-ref` from the test, as
`test_carry_ship.py` does): CR A and CR B change line 1 of `shared.py` differently; CR C changes
another file. The checks read the shipped `src/` at the head (no copy of the command).

1. **A conflicting pair and a clean one** (one test): `conflicts B --epoch 1`, with A and C ready:
   - exit 0; B's notes end with `early conflict: with A: shared.py`; A's and C's notes unchanged;
   - the output holds `B x A: conflict in shared.py; noted`, `B x C: clean`, and the last line
     `next: asks "conflict B <slug> with A <slug>: shared.py; switch to a stack?"`;
   - no ask is recorded (`record(repo)["asks"]` unchanged); one `note` event logged;
   - run again: `skipped: already noted`, no `next:` line, still one such note;
   - a note `early conflict: with B: shared.py` written on A by hand (as an old-card Foreman
     would) also makes the pair skipped when the check runs for A.
2. **Paths over five:** a pair conflicting in seven files gives the note
   `early conflict: with A: f1.py, f2.py, f3.py, f4.py, f5.py and 2 more`, and the ask names all
   seven.
3. **Pairs left out,** parametrized: `o` in `c.after`; `c.start_on == o.branch`; `o.pr_base` a
   branch other than the default; `o` `working`; `o` `merged`. Each gives no git call for that
   pair (the wrapper monkeypatched to count) and the right `skipped` or absent line.
4. **Not run and refusals,** parametrized:
   - a CR whose recorded branch does not exist: exit 0, the note
     `early conflict check: not run against <o>: <git's first line>`;
   - the CR given `working`, or `ready` with no PR: exit 2, record unchanged;
   - a `stack` and a `series` batch: exit 0, `not run: … is a <mode> batch`, record unchanged;
   - a missing `--epoch`: exit 2; a stale one: exit 3.
5. **Old git** (the program's "refusal on a faked old git version"), parametrized over
   `git version 2.37.1`, `git version 2.37.1.windows.1` and an unparseable text: `version` is
   monkeypatched (`chantier.core.git` level, through the subprocess call's output, so the parser
   is the one tested); exit 2, the line names `2.38`, the record and `events.jsonl` are unchanged,
   and no `merge-tree` ran. One parametrized case `git version 2.56.0.windows.4` parses as
   `(2, 56, 0)`.
6. **Must not, checked once** in test 1: before and after the command, `git for-each-ref`,
   `git worktree list --porcelain`, `git status --porcelain` and `git stash list` of the prepared
   repository are identical (no ref, no branch, no worktree, no index change), and no rebase is in
   progress (`.git/rebase-merge` and `.git/rebase-apply` absent).

**`just test` seconds:** an estimate of +1.5 to +3 s on Windows (about 6 test functions with
their parameters; each `merge-tree` and branch setup is a git subprocess of 30 to 80 ms on
Windows). The Driver measures `just test` before and after on the same machine and states both
figures in the PR's Deliverables (F20).

### 6. AGENTS.md

Two edits (program rule "AGENTS.md lines"):

1. **The git-exceptions bullet** ("The CLI has named git exceptions: the surface server's writer,
   … and the batch's end cleanup (above). The rest of the CLI keeps no git write."): before its
   last sentence, add a clause, beside the one child 1 adds for the push subcommand:

   > and `conflicts`'s read, `git merge-tree --write-tree --name-only --no-messages` (after a
   > `git --version`), one per pair, in the main checkout or the project's clone: it writes the
   > merged trees' objects to the object store, and no ref, branch, index or worktree file

2. **A named-exception paragraph** after `access`'s:

   > `conflicts`: the Foreman's early conflict check of a parallel batch (the Chief of Staff's in
   > direct mode), `conflicts <cr> --epoch <n>` at a CR's ready hand-back: one `git merge-tree
   > --write-tree` per pair of that CR and another CR ready with a PR on the default branch (a
   > pair chained or already noted is skipped), one note on the CR per conflicting pair, and the
   > ask printed for the steering session to send; it refuses on a git older than 2.38, records
   > no ask, switches no mode, starts no rebase, reads no forge and sends nothing to a Driver; it
   > shares no code with the server's scan of PRs left in conflict after a merge; built on the
   > measure of study-fable and study-fable-v2 (the check's card piece, `foreman-conflict.md`,
   > 3,789 bytes, read at a ready hand-back of a parallel batch) and the user's answers
   > simplify-cards-Q18 and Q22 (the tools first, child 15 of the program).

The planning-folder writes stay within "chantier writes only in the planning folder": the notes
go in the batch's record. The object writes are outside the planning folder, which is why the
git-exceptions bullet names them.

### 7. Docs

No doc names the Foreman's commands one by one; `docs/` gets no change. The release notes of the
version that ships it are the release's.

## Relation to the server's conflict scan (`1-inbox/pr-conflict-detect-and-rebase-order`)

This child **leaves** that item; it absorbs none of it.

- **That item** (split from CR-484 `pr-conflict-rebase-order`, pr-conflict-Q1 A, 2026-11-24):
  after a merge, the forge hub scans the running batch's open PRs or MRs, journals one the forge
  shows CONFLICTING, the watcher carries the line, and the Foreman starts a rebase Driver. It is a
  forge read, after a merge, against the default branch, by the server, with a journal line and
  a rebase order. It waits on CR-484 (in batch-31, `2-actives`), which makes the hub read the
  forge for a running batch at all (one serving process per surface, the watcher linked to the
  hub's process).
- **This child:** a local git read, before any merge, PR against PR, run by the steering session
  at a ready hand-back of a parallel batch, with a note and a printed ask, and never a rebase.
- **No shared code:** `conflicts` touches neither `hub/`, `board/` nor `connectors/`, adds no
  journal type, and reads no forge state (`board/prs.py`'s mergeable state is the other item's).
  The two can both report one pair of PRs; that is by design: one before the merge (switch to a
  stack?), one after it (rebase now).
- **Re-read:** the program's pending-items row stands: the item is re-read after CR-484 and this
  child have merged, with no change asked of it here.

## Out of scope

- Recording the ask (`asks`), switching the mode (`order mode --note stack`), sending a `take`, a
  rebase note or a message to a Driver: the steering session's and the Chief of Staff's, as the
  card says.
- Any check in a `series` or `stack` batch: there a conflict is the stack driver's
  `anomaly <cr> conflict: …`.
- A check of a PR against the default branch, or after a merge: the other item's.
- A forge read, a `fetch`, a trial merge, a rebase subcommand (program, Out of scope: 1 refusal in
  721 rebases).
- Any card, wrapper, hook or `references/` text; the scripted Foreman of the scenario (it follows
  the old card until child 24).
- Pinning a git version in the repository or the CI (the program: "which the repository does not
  pin").

## Gates and evidence

- `just check` before the first push, and `just eval-dry-run` (a change under `src/`).
- `tests/test_conflicts.py` green; `tests/test_scenario_coverage.py` green with the two names.
- The long gate `just scenario (ubuntu-latest)` green at the PR's head (a CLI and scenario
  change). The local Windows `chantier gate <cr> scenario` is owed only while this CR is the
  stack's top when presented.
- The PR's Deliverables state the `just test` seconds before and after, and the local
  `git --version` the tests ran on.
- **Host and defaults matrix:** none. The command is plain git, the same on both hosts and
  forges, and reads no configured value but the default branch, the remote and the record.

## Risk

- **Long gate owed** (CLI and scenario).
- **AGENTS.md:** a new git exception (object writes) and a tool line; a reviewer reads both.
- **Unproved (F17):** the `merge-tree --write-tree --name-only --no-messages` form on the CI
  runners' git (ubuntu-latest, macos-15-intel, windows-latest in `just check`; ubuntu-latest in
  the scenario job) is unproved until CI runs; their gits are expected to be 2.39 or later, but
  nothing here pins them. On the user's Windows machine git is 2.56.0. A red job there on the git
  version is the refusal working, not a test to loosen: the child hands back blocked and says so.
- **Unproved (F17):** the command's run by a real Foreman (or a Copilot one) is unproved until
  the new cards name it (children 21, 22) and a real parallel batch runs it.
- **Unreachable objects:** each run leaves loose tree and blob objects in the object store until
  git's own garbage collection drops them. A few kilobytes per pair; named in AGENTS.md.
- The old card stays the shipped text until the swap, so until then no Foreman uses the command
  unless told. Nothing breaks.

## Open questions

None. The program's specification and the card settle the behaviour. Three choices made here
belong to the implementation, and the PR names them:

- the command prints the ask and does not record it (the program's "prints one ask");
- the git version check runs first, on every call, so an old git refuses instead of leaving a
  "not run" note per pair;
- a PR whose base `ship` never read (`pr_base` None) counts as on the default branch, unless the
  pair is chained.
