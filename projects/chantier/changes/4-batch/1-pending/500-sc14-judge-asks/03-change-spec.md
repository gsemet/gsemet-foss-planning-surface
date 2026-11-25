# SC14: `chantier judge` words the ask to the user

Child 14 of 28 of the program CR `simplify-cards-and-prompts`. The program's `03-change-spec.md`
("Child 14", "Rules for every child") and its `02-answers.md` answers 17 to 22 rank above this
file. One Driver and one PR, in the running stack batch (batch-31). Code read: `origin/main` at
`8a960d34`. Short forms used below:

- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`.

## Goal

Answer 11 (simplify-cards-Q11), in the owner's terms: `next` is advice for choosing a CR and for
wording; safety steps are refusals, not advice; **the CLI words the ask to the user, and the
Foreman may add one sentence.**

Today the Foreman builds each readiness ask by hand, from about 60 lines of `foreman.md` and
`foreman-stack.md` ("The user's boundaries"). It reads the hand-back, finds the gaps, the draft
base, the gate exemption or waiver, and the local-gate clause, then types `$CHANTIER asks
"ready-to-merge <cr> <link> gaps: …"`. This child adds `chantier judge <cr> --epoch N`. It reads
the record and prints that ask, worded by the CLI from the same facts as the `handed back:` line.
With `--record ["<one sentence>"]`, it records the ask through the same function as `asks`, with
the steering session's sentence appended.

The CLI only words the ask. Sending it, taking the CR back and the merge stay with the steering
session and the user, as AGENTS.md says after child 9.

## Place in the chain

- **Base:** child 13's branch (`msg-steering`), the previous CR of the stack.
- **Uses from earlier children:**
  - child 9: the AGENTS.md sentences say the CLI "never decides a merge or a take-back" and that
    `judge` only words the ask. This child adds `judge`'s own named-exception line and does not
    reword child 9's sentences;
  - child 11: the public `ready_line(repo, d, c, events, stopped)` in `src/status/ready_line.py`,
    and the `judge` kind of `src/status/due.py`. That kind lists a `ready` CR that has no `ask`
    event after its last `handback` event. `judge --record` logs that `ask` event, so the item
    leaves the due list. If `ready_line` is not in the base, add it exactly as child 11 specifies:
    a wrapper of `_line`, with `ready_lines` unchanged;
  - child 12: `next --epoch` already names `judge <cr>` for a CR handed back with no ask. Nothing
    changes there.
- **Depends on this child:** child 15 (`conflicts-check`) is next in the stack and uses nothing
  from here. Card children 21 and 22 (Foreman, Chief of Staff) write the new cards around `judge`:
  "on a hand-back, run `judge <cr>`, then `--record` or take back". No card changes in this
  child.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Answer 11 (Q11) | The CLI words the ask; the steering session may add one sentence; safety steps stay refusals | "1. The command", "2. The wording" |
| Answer 22, F7, and child 9 | `judge` only words the ask; the CLI never decides a merge or a take-back | "Must not"; the `decide:` line |
| Program child 14, Scope | `judge <cr> --epoch N`, declared in `src/declare/judge.py`; reads the hand-back and the `handed back:` line's facts (gaps, owed items, long gate result, waits) | "1", "2" |
| Program child 14, Scope | No ask possible (a blocked hand-back): it prints the facts; the take-back stays the steering session's | "3. When no ask is worded" |
| Program child 14, Scope | `--record ["<one sentence>"]` records through the record `asks` writes, with the sentence appended | "4. `--record`" |
| Program child 14, Must not | Drop no gap and no owed item from the wording | "2"; the tests |
| Answer 18 | Tools first: only additions; every intermediate `main` keeps working with the old cards | `asks` and the `handed back:` line unchanged; no card edited |
| Answer 22, F20 | The PR states the seconds its tests add to `just test` | "Gates and evidence" |
| Program rules | A new command adds a scenario step and a coverage bullet; long gate owed; AGENTS.md gains the tool's line with its source | "5", "6", "AGENTS.md" |

## What changes

### 1. The command (`src/declare/judge.py`, `src/commands/judge.py`, `src/cli.py`)

- **Parser.** New `src/declare/judge.py` with `register(sub)`. It calls
  `add_command(sub, "judge", "chantier.commands.judge:judge", <summary>, BATCH_EPOCH)` and adds:
  - `cr`: the CR (normalised with `normalize_cr`, as other per-CR commands do);
  - `--local-gate`: the steering session judged that the project's rules ask this CR for a local
    long-gate run. The ask then carries the `local gate` clause (section 2);
  - `--record`, `nargs="?"`, `const=""`, `metavar="SENTENCE"`: record the ask; the optional
    sentence is the steering session's one sentence.

  The summary reads: "the steering session's ask to the user for a CR handed back, worded from
  the record (its readiness word, gaps, gate, waits, owed items); `--record` records it as
  `asks` does; it decides no merge and no take-back".
- **Registration.** Add `judge` to the `from chantier.declare import (...)` list in `src/cli.py`
  and to `FULL_OUTPUT`, since an ask cut at ten lines would drop a gap.
- **Handler.** New `src/commands/judge.py`, `judge(args) -> list[str]` (or `(lines, code)`):
  1. `repo = Repo.find()`. The batch is `find_cr_batch(repo, args.cr, args.batch)`, so a paused
     batch is read too.
  2. `require_epoch(args.epoch, "judge <cr> --epoch <n>")` (`src/core/batch.py`), always, since
     this is a steering command.
  3. Read `d = read_batch(...)`, `events = read_events(...)` and
     `stopped = stopped_agents(repo, d, events)` (`src/commands/activity.py`). Check the epoch
     against `d.foreman_epoch` with the same refusal text and exit code as `check_epoch` (stale:
     `EXIT_CONFLICT`). With no `--record`, nothing is written: no `RenderedBatch` is opened.
  4. The CR must be in the batch. If it is not, use the existing `no CR …` refusal form of
     per-CR commands.
  5. Branch on the CR's record status: `ready` (sections 2 and 3), `blocked` (section 3), or
     anything else, which is refused:
     `judge <cr>: <cr> is <status>, not handed back; nothing to word yet; `status` shows the batch`
     (`EXIT_PRECONDITION`, nothing written).
- **Output, in this order:**
  1. `ask: <the ask text>`, or `no ask: <why>` (section 3);
  2. the facts: for a `ready` CR, its `handed back:` line (`ready_line`); for a `blocked` CR, the
     lines of section 3; then, for either, the CR's `wait_line(repo, d, c)`
     (`src/commands/wait_view.py`) when it has open waits;
  3. for a worded ask with no `--record`, the line
     `decide: send it with `judge <cr> --record ["<one sentence>"] --epoch <n>`, or take it back
     with `take <cr> --note "…" --epoch <n>`; the merge is the user's`;
  4. with `--record`, the lines `asks` prints when it records (section 4), in place of the
     `decide:` line.

### 2. The wording (`src/status/judge_words.py`, new; `src/status/ready_line.py`)

A pure function `ask_text(repo, d, c, events, stopped, local_gate: bool) -> str | None` builds
the ask from the record and the events only. It reads no forge and no git, and writes nothing.
It returns None when section 3 applies.

In `src/status/ready_line.py`, add the public names `gaps(events, c)` and
`owed(repo, d, c, events, stopped)`, used by both the line and `judge`. The private `_gaps` and
`_owed` either call them or are renamed to them. The `handed back:` line keeps the same bytes.

The ask is one line, built from these parts in this order and joined by single spaces. A part
with nothing to say is left out:

1. **The word**, from `ready_word(d, c, repo)` (`src/stack_words.py`):
   - `ready to merge` gives `ready-to-merge`;
   - `PR in draft` gives `pr-in-draft`;
   - `ready locally` gives `ready-locally`.

   These are the first words that `readiness_key` (`src/rails_release.py`) knows. A recorded ask
   therefore supersedes the CR's earlier unread readiness ask, as an `asks` ask does.
2. **The CR's name:** `<cr id> <slug>`, the same as the `handed back:` line
   (`f"{c.id} {cr_slug(Path(c.path or '').name)}"`). The id stays the second word, so
   `readiness_key` finds the CR.
3. **The link:** `c.shown_pr()`. None for `ready-locally`.
4. **The draft clause**, for `pr-in-draft` only: `on <pr_base_of(d, c, repo)>: waits for
   <draft_waits(d, c, repo)>`.
5. **The gate clause**, from `gate_view(repo, d, c, events)` (`src/status/gate.py`):
   - `exempt`: `no long gate: <g["waiver"]>`;
   - `waived`: `long gate waived: validated by <validated_by.cr>`, or
     `long gate waived: follow-up <follow_up>`, or `long gate waived` when neither is recorded.

   Other states add no part here.
6. **The gaps:** `gaps: <gaps(events, c)>`, when the last `handback ready` note holds a `gaps:`
   text. Each run of whitespace (newlines included) becomes one space. Nothing else in the text
   changes.
7. **The local gate clause**, only with `--local-gate`:
   `local gate <cr> at <sha7>: passed|failed|not run`. It reads the CR's own gate events at
   `c.head`, apart from any waiver or exemption, because a waiver does not waive a local run
   (`foreman.md`):
   - `passed` when `gate_passed(mine, c.head)` holds;
   - `passed (carried from <sha7>)` for a carry at the head (`carry_at(mine, c.head,
     "gate_from")`, or the hand-back's `gate_from`);
   - `failed` when a `gate` event at the head did not pass;
   - `not run` otherwise, a gate queued or running included.

   With no `c.head`, the clause is `local gate <cr>: not run (no head recorded)`.
8. **The waits**, from `open_counted(c)` (`src/core/waits.py`):
   - `open waits: <what(w); …>`;
   - prefixed `do not merge: ` when one of them is of type `merge`. This is the program's merge
     rule: children 19 to 27 carry a typed merge wait on child 28.
9. **The owed items:** `owed before the merge: <owed(...) joined by "; ">`, the same items as the
   `handed back:` line's: the long gate open at the head, and each order on the CR not done and
   not applied.

The ask never carries an icon: the first word must stay the readiness word.

### 3. When no ask is worded

`ask_text` returns None, and the command prints `no ask: <why>` and the facts, in two cases:

- **A blocked hand-back** (`c.status == "blocked"`):
  - `no ask: <cr> handed back blocked; taking it back or carrying it is yours (`take <cr> --note
    "…" --epoch <n>`, or `asks "blocked <cr> <reason>"`)`;
  - then `blocked: <the note of the CR's last handback event whose result is not ready>`,
    unchanged.
- **A CR in a stack batch's chain that is not alone:** `d.mode == "stack"`, the CR is in
  `chain(d)` (`src/stacks.py`), and `shape_blockers(d, c.id)` (`src/stack_shape.py`) is not
  empty. This is the condition under which `asks` refuses a per-CR `ready-to-merge` today
  (`shape_refusal`). The stack's ask needs the forge read of `forge-stack show` (the stack link,
  the mergeable commit), and `judge` reads no forge. So it prints:
  - `no ask: <cr> is in <batch>'s stack and not alone (open: <ids>); its readiness goes up with
    the stack's: `forge-stack show`, then `asks "stack-ready-to-merge …"``;
  - `for the stack's ask: <cr>=<link>[ gaps: <gaps>] …`, one pair for each CR of `chain(d)`
    whose status is `ready` and that has a PR, in chain order, each with its gaps as in part 6
    above. The Foreman copies them, so no gap is dropped;
  - with `--local-gate`, the stack top's (the last CR of `chain(d)`) local gate clause, as in
    part 7.

  A CR outside the chain (a fix, a held CR) and a CR of the chain with no blockers (alone) get
  the per-CR ask of section 2.

In both cases `--record` is refused, and nothing is written:
`judge <cr> --record: no ask to record (<blocked | in the stack>); `asks "<text>"` records your
own` (`EXIT_PRECONDITION`).

### 4. `--record` (`src/commands/judge.py`, `src/rails_release.py`)

- Open `RenderedBatch(repo, batch, actor="foreman")`, as `asks` does for an ask text. Call
  `check_epoch(b, args.epoch)`, then compute `ask_text` again on `b.record` inside the lock, so
  that the text recorded is the text of the record as it is now.
- The recorded text is the ask, followed by ` | note: <sentence>` when the sentence is not empty.
  The sentence is `" ".join` of one argument and is kept as typed.
- Record through `record_ask(b, text)` (`src/rails_release.py`) with no `outside_stack`. That is
  the function `asks` calls: it appends the `AskRecord`, logs the `ask` event with the CR, and
  supersedes the earlier unread readiness ask. If `check_shape` refuses all the same (a record
  changed between the read and the lock), its refusal goes through unchanged.
- Print what `asks` prints: `[foreman→chief-of-staff] ask <A-n>: <text>`, then
  `<A-k> superseded by <A-n> (marked read)` for each superseded ask.
- `asks` itself is not changed.

### 5. Scenario (`scenario/run_scenario.py`, `scenario/README.md`)

In the `parallel` unit's `scenario` function, section 3: after the check "`status` prints
CR-101's `handed back:` line …" and before `fm.turn()` (at `origin/main`, after
`_, shown = w.chantier("status")`):

- Snapshot `w.batch()["asks"]`, then run `judge CR-101 --epoch <fm.epoch>`. Check that:
  - the first line starts with `ask: ready-to-merge CR-101 ` and holds `pr101`;
  - a `handed back: ` line follows;
  - the last line starts with `decide: `;
  - `w.batch()["asks"]` is unchanged ("`judge` without `--record` records nothing").
- Run `judge CR-101 --record "scenario: one sentence" --epoch <fm.epoch>`. Check that:
  - its first line starts with `[foreman→chief-of-staff] ask A-`;
  - the last ask in `w.batch()["asks"]` has the text `<the printed ask> | note: scenario: one
    sentence`;
  - `status` then prints the `<n> asks unread: `chantier asks`` line;
  - `asks` lists that ask.
- Then mark that ask read (`asks --read <A-n>`), so that the scripted Foreman's own
  `ready-to-merge CR-101 <pr>` ask at the next `fm.turn()` runs as before. The existing checks
  on `fm.asked` stay as they are. If a later check of the unit counts asks or ask ids, the Driver
  moves the step to where it breaks none, and says where in the PR.
- Run `judge CR-103 --epoch <fm.epoch>` on a CR that is not handed back. Check exit 2 (`EXIT_PRECONDITION`) and a text
  that names `status`.
- `scenario/README.md`, "## Coverage": add one bullet:
  `- `judge` (unit: parallel): the ask to the user worded from a handed-back CR's record, nothing
  recorded without `--record`, the recorded ask equal to the printed one with the steering
  session's sentence, shown in `status` and `asks`; a CR not handed back refused (test:
  test_judge.py::<the wording test>)`. `tests/test_scenario_coverage.py` checks that the unit
  and the test exist.

### 6. Tests (`tests/test_judge.py`, new)

The tests use prepared records, built as `tests/test_ready_line.py` builds them (`_cr`,
`_batch`, `_event`, `_ready`) for the pure function, and with `batch_helpers.record` and
`write_record` with the in-process `chantier` fixture for the command. There is no git and no
network.

- **Wording, parametrized over prepared hand-backs.** Each case gives the expected ask string
  whole:
  - ready to merge: a PR out of draft on the default branch;
  - ready, with gaps (a multi-line `gaps:` text collapsed to one line, every word kept);
  - PR in draft: `on <base>: waits for <cr>`;
  - ready locally (no PR): no link;
  - an exemption: `no long gate: <reason>`;
  - a waiver: a hand-back with `gate_waiver` and `follow_up`, giving
    `long gate waived: follow-up <folder>`; and one validated by a top, giving
    `long gate waived: validated by CR-n`;
  - a local-run rule, parametrized over `--local-gate` with passed, carried, failed and not run
    at the head, and without `--local-gate` (no clause);
  - an open order on the CR, giving `owed before the merge: O-1 … is applied (the Foreman)`;
  - a typed merge wait, giving `do not merge: open waits: w1 merge on …`.
- **A stack's top.** A stack batch with three CRs in the chain:
  - the top with another chain PR open: `no ask:` names `forge-stack show`; the `for the stack's
    ask:` line holds every ready chain CR's `<cr>=<link>` with its gaps; with `--local-gate`, the
    top's clause; `--record` exits 2 and records nothing;
  - the top alone (the others merged): a per-CR `ready-to-merge` with the local gate clause.
- **Blocked.** `no ask:` and the `blocked:` note are printed, exit 0. `--record` exits 2, and the
  bytes of `batch.json` and `events.jsonl` are unchanged.
- **Refusals.** A CR that is working, queued or merged, and a CR not in the batch, each exit with
  the code above and name a backticked next command. A missing `--epoch` exits 2 (`EXIT_PRECONDITION`), and a stale
  one exits 3 (`EXIT_CONFLICT`). Nothing is written in any of these cases.
- **Read-only.** With no `--record`, the bytes of `batch.json` and `events.jsonl` are equal before
  and after.
- **`--record`.**
  - The recorded `AskRecord.text` equals the printed `ask:` text, plus ` | note: <s>` when a
    sentence is given; without one, the two are equal.
  - An `ask` event with `cr` set to the CR is logged. After it, child 11's `due()` no longer lists
    the CR's `judge` item.
  - A recorded ask supersedes the CR's earlier unread readiness ask and prints the supersede line.
- **No gap or owed item dropped.** For every ready case above, each `;`-separated item of
  `gaps(events, c)` and of `owed(...)` appears in the ask text.

## Out of scope

- Any change to `asks`, to the `handed back:` line, to `status` or to `STATUS.md` and
  `STATUS.json`.
- Wording the `stack-ready-to-merge` ask: it needs the forge read of `forge-stack show`, and
  `judge` reads no forge (see open question 2).
- Asks other than readiness ones (`question`, `refused`, `budget`, `merged`, `conflict`,
  `heavy-ci`, `writer off`). They stay typed with `asks`.
- Deciding whether a project's rules ask a local run, or whether an exemption or waiver holds.
  That stays the steering session's judgement, and it passes `--local-gate`.
- Taking a CR back, or any merge.
- Any card, hook or wrapper text (answer 18; no child before 19 edits a card).
- A new journal type (so `just journal-schemas` is not run), and any version edit.

## Must not

- Decide a merge or a take-back, or print advice that reads as one. The `decide:` line names both
  choices and says the merge is the user's.
- Drop a gap or an owed item from the wording.
- Read the forge or run git.
- Write anything without `--record`.
- Change what `asks` records or refuses.

## Gates and evidence

- `just test` passes with `tests/test_judge.py`.
- The added `just test` seconds are measured before (at the base) and after (at the head) on the
  same machine and go under the PR's Deliverables. Expected: under 1 s (about 25 parametrized
  cases of a pure function, and about ten in-process command calls on small prepared records).
- `just check` and `just eval-dry-run` (a change under `src/`) run in the worktree at the rebased
  head before the first push.
- The long gate `just scenario (ubuntu-latest)` is green at the PR's head, since the CLI and the
  scenario change. The local Windows `chantier gate <cr> scenario` is owed only while this CR is
  the stack's top. It moves to the CR that joins above it.
- No host or default matrix: `judge` reads the record only and acts the same on both hosts and
  with any configuration.
- No check guards a shipped file: the tests assert the CLI's output on prepared records.
- No `hooks/` or `types/` change, so `just mod` is not owed.

## AGENTS.md

Add one named exception in the CLI-scope bullet, beside the lines for `wait`, `access` and
`live`:

> `judge`: it words the steering session's ask to the user for a CR handed back, from the record
> only (its readiness word, gaps, gate exemption or waiver, local gate clause, open waits and
> owed items, the facts of the `handed back:` line), and prints the facts with no ask for a
> blocked hand-back or a CR of a stack that is not alone; it reads no forge and runs no git, and
> it writes nothing but, with `--record`, the ask that `asks` records, with the steering
> session's one sentence; it decides no merge and no take-back; built on the user's answers
> simplify-cards-Q11 and Q22 (F7), with no measured cost.

Child 9's sentences are not reworded.

## Risk

- The long gate is owed (CLI and scenario).
- A wrong wording misleads the user at each ready CR. The wording is pinned whole, case by case,
  and nothing changes until the card children tell the Foreman to use `judge`. The old cards
  keep `asks`.
- `--local-gate` relies on the steering session's judgement of a prose rule. Without it, the
  clause is missing, though the `handed back:` line printed beside the ask still shows the long
  gate's result.
- The new `ask:` text names the CR as `<id> <slug>`, where the scenario's scripted Foreman types
  `<id> <link>`. `readiness_key` reads only the first two words, so supersession is unchanged.

## Open questions

1. **The local gate clause.** The CLI cannot read a project's prose rule ("each covered PR runs
   the long gate locally"), so this specification adds the clause only on `--local-gate`, passed
   by the steering session. Should `judge` instead print it for every CR that has a head whenever
   the code repository's `chantier.yaml` declares a `long_gate.commands` entry, and leave the
   Foreman to delete it? Until you answer, the flag is built.
2. **The stack's ask.** `judge` words no `stack-ready-to-merge` ask: it would need the forge read
   of `forge-stack show` (the stack link and the mergeable commit), a new forge read that
   AGENTS.md would have to name. For a stack, `judge` prints the per-CR pairs with their gaps,
   which the Foreman copies. Is a later CR wanted for `judge` to word the stack's ask, reading
   the forge?
