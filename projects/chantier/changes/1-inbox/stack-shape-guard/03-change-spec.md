# A stack batch keeps its shape after the Foreman's compactions

A stack batch must keep acting as a stack after the Foreman's context is compacted, through a light
but systematic mechanism that the CLI enforces (Studio's owner: "pas trop lourd mais
systématique"). Two parts carry it: a shape line at each heartbeat, and `asks` refusing a per-CR
ready ask in a stack batch while that ask would leave another PR of the batch behind main. Two
lighter parts back them up: a stack card the Foreman rereads at the reload, and the Chief of Staff
checking each ask against the shape. Specification v3.

## Goal

The incident, from Studio's record (`projects/markdown-okf-schema-studio/changes/4-batch/events.jsonl`):
batch-07 was a stack batch (mode stack from order O-5). Its morning stack, CR-439 to CR-445, merged
whole at 07:24. The same batch then went on with a second wave, run by the same Foreman after
several compactions. It shipped each new CR as its own PR on main, each with its own per-CR
`ready-to-merge` ask (A-14 for CR-449 at 10:24, A-16 for CR-451 at 11:18, A-17 for CR-447 at
11:48), and sent a stack ask only at 15:14 (A-21). For those CRs it ran no `take stack`, started no
stack driver and made no native stack. Each merge by the owner left the other open PRs behind main.
So when the second wave began, no stacked CR was open any more: what the second wave lacked was a
stack of its own, not respect for an existing one.

The cause: after a compaction the Foreman rereads only its startup sections. The stack rules sit
deep in `foreman.md` ("The user's boundaries" and "Your means"), so the shape survived as a word
but not as a procedure. After this CR:

- the Foreman's heartbeat shows the stack's state in one line, every time;
- the CLI refuses a per-CR ready ask while another CR of the stack's chain has an open PR or a
  stacked CR is still open, so a forgotten procedure stops at the CLI and does not reach the user;
  a CR truly alone may still ask alone, and so may a fix or held CR, which sit outside the stack;
- the stack rules live in one card that a stack batch's Foreman reads at the batch's start and
  rereads after each compaction;
- the Chief of Staff relays no readiness ask that does not fit the batch's shape: it sends it back
  and tells the user in one line.

## Decisions carried (02-answers.md)

- **Q1 (D, refuse unless forced):** `asks` refuses a per-CR `ready-to-merge` ask in a stack batch.
  A fix CR is excepted (and a held CR, Q12). An explicit flag lets the ask through:
  `--outside-stack "<reason>"` (the name is this spec's choice; the brief left it to the spec).
- **Q2 (A):** at each `status --refresh`, in stack batches only, one line with a fixed format,
  `shape stack: next …; stack driver: …; native stack: …`. Q11 and the critic's fix 4 complete it
  (see 2).
- **Q3:** superseded by Q5.
- **Q4 (A):** one line in the Chief of Staff's card: each Foreman ask is checked against the batch's
  shape (in a stack batch: a stack ask and a native stack), not only for being rebased and green.
- **Q5 (B):** a separate card, `foreman-stack.md`, read at the reload of a stack batch. Its stack
  rules move out of `foreman.md`, which keeps a pointer to it. The manifest
  (`startup-manifest.json`) names it.
- **Q6:** grilled enough; spec-writer, then critic; destination the next batch (`3-ready`).
- **Q7:** replaced by Q10 ("once the first stack is made" no longer holds).
- **Q8 (A):** `--outside-stack` is used only on a Chief of Staff order carrying the user's word; its
  reason is `O-<k>: …`.
- **Q9 (A):** a mismatched ask at the Chief of Staff is sent back to the Foreman
  (`shape: through the stack`) and the user is told in one line ("CR-12 asked alone in a stack
  batch: sent back through the stack").
- **Q10 (A):** the guard refuses while another CR of the batch has an open PR, or a stacked CR is
  still open. A CR truly alone (no other open PR in the batch) may still ask alone.
- **Q11 (A):** the shape line's `next` reads `parallel until 2 ready with a PR` before a stack can
  form, then `take stack` once that threshold is met (the same as `stack_due`'s).
- **Critic run 1, fix 4:** one criterion, Q10's, used by the CLI guard, the shape line and the
  Chief of Staff's check (below, "The criterion").
- **Q12 (Fable advisor, rule 12):** only the CRs of `stacks.chain(b_data)` count. A fix CR's or a
  held CR's open PR never blocks. A held CR, like a fix CR, asks alone with no `--outside-stack`
  (its hold order already carries the user's word), and never counts, even with `stacked` still
  set. The release CR stays in the count and its per-CR ask stays refused.
- **Q13 (Fable advisor, rule 12):** while a stack waits for its merge, the shape line's `next`
  reads `take stack at the next ready CR or merge` (`foreman.md`, "Each later take", names a
  recorded merge as a trigger).
- **Rule 12:** no more questions to the user on this CR; this version leaves none open.

## The criterion (one function, three readers)

File: `skills/chantier/scripts/cli/src/chantier/stacks.py`, a new function beside `stack_due`:

`shape_blockers(b_data: BatchRecord, cr: str | None = None) -> list[CrEntry]`

It returns, in `chain` order, the CRs that make a per-CR ready ask for `cr` a stack matter:

- every CR of `chain(b_data)` other than `cr` that has a PR recorded (`pr` set);
- every CR of `chain(b_data)` with `stacked` set, `cr` itself included (a CR already in the native
  stack never asks alone).

`chain` (in `stacks.py` today) already holds only the open CRs (not `merged` or `cancelled`) that
are neither a fix CR nor held (`is_held`), the release CR last. So a fix CR and a held CR never
appear in the list, a held CR not even with `stacked` still set, and the release CR does.

With `cr=None` it answers for the batch as a whole (no CR left out), which the shape line uses.
The guard refuses when the list is not empty for the asking CR; the shape line shows it; the Chief
of Staff's check reads the shape line. No other definition of "the batch has made a stack" stays in
the spec, the CLI or the cards: v1's "at least one CR, merged ones included, has `stacked`" is
dropped.

Q12 bounds Q10's "another CR of the batch" to the stack's chain: a fix CR's or a held CR's open
PR sits on main, outside the stack, and never blocks.

## What changes

### 1. The guard: `asks` refuses a per-CR `ready-to-merge` in a stack batch (CLI)

Files: `skills/chantier/scripts/cli/src/chantier/rails_release.py` (the refusal, beside
`CR_READINESS` and `readiness_key`, calling `stacks.shape_blockers`),
`commands/batch_status.py` (`asks`, which calls it before `record_ask`) and
`declare/batch_status.py` (the new flag and the help text).

- **The refusal.** `asks <text>` refuses with exit 2 (`EXIT_PRECONDITION`) and records nothing
  when all of these hold:
  - the batch's `mode` is `stack`;
  - the text's first word is `ready-to-merge`, and its second word names a CR of the batch (the
    same match as `readiness_key`, through `normalize_cr`);
  - that CR's `kind` is not `fix` and it is not held (`not is_held(cr)`): a fix CR sits outside
    every shape, as Q1 says, and a held CR is out of the stack on its hold order, which already
    carries the user's word (Q12); a release CR is not excepted: in a stack it is the top, and its
    readiness is the complete `stack-ready-to-merge`;
  - `shape_blockers(b_data, <cr>)` is not empty (Q10).

  In Studio's second wave, CR-447's ask at 11:48 and any other ask made while another second-wave
  CR's PR was open are refused, which is what left the other PRs behind main. An ask made while
  its CR was the only open PR of the batch passes, as Q10 wants.

  `pr-in-draft` and `ready-locally` are never refused, because neither invites a merge. Neither is
  `stack-ready-to-merge`, nor any other kind of ask.

- **The refusal's text**, one line on stderr, exit 2, exactly (`<batch>`, `<cr>`, `<n>` and the
  list filled in; `<blockers>` is the blockers' ids joined by `, `, each followed by ` (stacked)`
  when it is stacked):

  ```text
  refused: <batch> is a stack and <cr> is not alone (open: <blockers>): its readiness goes up with the stack's (`take stack --epoch <n>`, the stack driver's hand-back, then `asks "stack-ready-to-merge …"`); a fix or held CR is outside the stack; `--outside-stack "O-<k>: <why>"` records this ask on an order carrying the user's word
  ```

  `<n>` is the batch's current epoch as `take stack` takes it.

- **The flag `--outside-stack "<reason>"`** (Q8).
  - With the flag, an ask the guard would refuse is recorded. Its recorded text is the ask's text
    followed by ` outside the stack: <reason>`, so the Chief of Staff sees the reason in the line
    the CLI prints (`[foreman→chief-of-staff] ask A-n: ready-to-merge <cr> <link> … outside the
    stack: <reason>`). The `ask` event carries `outside_stack: <reason>`.
  - The reason must start with `O-<k>: ` followed by words, where `O-<k>` is an order recorded in
    the batch (`orders`). Otherwise the flag is refused with exit 1 (`EXIT_USAGE`):

    ```text
    --outside-stack needs a reason "O-<k>: <why>" naming an order of <batch> that carries the user's word
    ```

  - The flag is also refused with exit 1 when the ask is one the guard would not refuse (another
    word, a fix or held CR, a batch that is not a stack, or a CR with no blocker):

    ```text
    --outside-stack is only for a per-CR ready-to-merge ask that the stack guard refuses
    ```

    The flag therefore never decorates an ordinary ask.
  - Superseding (`record_ask`) is unchanged: a forced ask is a `("cr", <cr>)` readiness ask like
    any other.
- **The help text** (`declare/batch_status.py`, `asks`): one clause added. In a stack batch, a
  per-CR `ready-to-merge` is refused while another CR of the stack has an open PR or a stacked CR
  is open; a fix or held CR is outside the stack; `--outside-stack "O-<k>: <why>"` records it on
  an order carrying the user's word.
- **Steering.** The guard does not depend on the actor: a Chief of Staff steering in direct mode
  meets the same refusal.

### 2. The shape line at each heartbeat (CLI)

Files: `skills/chantier/scripts/cli/src/chantier/stacks.py` (a new `shape_line(b_data)`, beside
`stack_line`, and a small helper `forming(b_data)` that `stack_due` and `shape_line` share) and
`commands/batch_status.py` (`status`).

- With `--refresh`, with or without `--epoch`, and only when the batch's `mode` is `stack`,
  `status` prints one line right after the batch line (the `<batch> running steering … shape
  stack …` line):

  `shape stack: next <next>; stack driver: <driver>; native stack: <native>; alone asks: <alone>`

  - `<next>` (Q11):
    - `note to the stack driver` when a stack driver is recorded (`stack_agent` set): events then
      go to it as `[foreman→stack] note …`, as the card says;
    - else `take stack` when a take is due: `forming(b_data)` holds at least `FORMING` (2) CRs, or
      a stacked CR of `chain` exists and a CR of `chain` that is not stacked (release aside) is
      `ready` with a PR (a later take);
    - else, when a stacked CR of `chain` exists (the stack waits for its merge, nothing to add):
      `take stack at the next ready CR or merge` (Q13: a recorded merge is also a trigger, as
      `foreman.md`'s "Each later take" says);
    - else `parallel until 2 ready with a PR`.

    `forming(b_data)` is `stack_due`'s per-CR test without its batch conditions: the CRs of the
    chain that are neither release nor fix (`_alone`), `ready`, with a PR, and with every open
    dependency `ready` (`_open_after`). `stack_due` keeps its own conditions (running, no stack
    driver, no CR ever stacked) and calls `forming`; its behaviour does not change. The shape line
    does not use "no CR ever stacked": in Studio's second wave, after the morning stack merged, it
    reads `take stack` as soon as two second-wave CRs are ready with a PR.
  - `<driver>`: the recorded `stack_agent`, else `none`.
  - `<native>`: `present (<cr>, <cr>…)` listing the CRs of `chain` that have `stacked` set,
    bottom first, else `absent`.
  - `<alone>`, from `shape_blockers(b_data)` (the criterion, batch-wide), counting the CRs of
    `chain` only (Q12: a fix or held CR's PR does not count):
    - `refused` when a stacked CR of `chain` exists or at least two CRs of `chain` have a PR;
    - `allowed for <cr> only` when exactly one CR of `chain` has a PR and none is stacked;
    - `allowed` when no CR of `chain` has a PR.

  With nothing recorded, the line reads exactly:
  `shape stack: next parallel until 2 ready with a PR; stack driver: none; native stack: absent; alone asks: allowed`.
- A plain `status` (no `--refresh`), and any batch that is not a stack, prints no such line. The
  existing `stack: take stack now: …` line (`stack_line`) is unchanged and still printed when due.
- The line is read from the record only: no forge read and no write. "Native stack" here means what
  the record holds as placed by the stack driver (`stacked`): the line is a reminder, not a check.
  The five checks on the forge stay with `forge-stack show`.

### 3. The card `foreman-stack.md` and the reload (cards, manifest)

Files: `skills/chantier/references/foreman-stack.md` (new), `foreman.md`,
`startup-manifest.json`, `session-start.md` (section "5. Reload") and `chief-of-staff.md`.

- **The new card** `skills/chantier/references/foreman-stack.md`, headed `# Foreman: a stack
  batch`. Its opening says who reads it and when:
  - the Foreman of a stack batch (a batch whose `status` line shows `shape stack`, by `--mode
    stack` or by `order mode --note stack`), and the Chief of Staff steering one in direct mode;
  - at the batch's start, and again after each compaction;
  - at a mode switch to a stack.

  It holds, moved verbatim from `foreman.md` (wording kept, links adjusted, no rule changed but the
  additions named below):
  - the stack batch rules of "Your means", from `A stack batch (`--mode stack`, or a batch switched
    to a stack by `order mode`): until the first stack is made it runs like a parallel batch …`
    through the end of "The five checks of a stack ready to merge". That span covers: the first
    take, each later take, a merge while a stack driver runs, a working CR placed on another, the
    final-order take, a held CR, deliver by a time, `take stack` and the stack driver's lifecycle,
    its hand-backs and the `stack-ready-to-merge` asks (partial and complete), the anomalies, a
    drop in the stack, heavy CI, the failed-check route, the gaps, inserting a CR, and the five
    checks;
  - the **Stack** branch of the `order merged` bullet (a restack, a folded CR, rebase notes before
    the first stack, nothing left open), plus the "say which one you chose" line that goes with it.

  The moved span's opening sentence ("until the first stack is made it runs like a parallel
  batch") gains, right after it, the Q10 limit: a CR handed back ready asks alone only while no
  other CR of the batch has an open PR and no stacked CR is open (the shape line's `alone asks`).

  Suggested level-2 sections, so that later readings can name them: `## The stack's asks`,
  `## The stack grows`, `## The stack driver`, `## After a merge`, `## The five checks`. The Driver
  may rename them; the manifest names the whole file.

  **New text in `## The stack's asks`**, the only rules this CR adds to the card:
  - while another CR of the stack has an open PR, or a stacked CR is open (`alone asks: refused`
    or `allowed for <other cr> only` on the shape line), a CR's readiness reaches the Chief of
    Staff only through the stack: no per-CR `ready-to-merge` for a CR that is not a fix or held
    (the CLI refuses it), but the next `take stack` and, at the stack driver's hand-back, the
    `stack-ready-to-merge` ask; a CR truly alone may still ask alone, and a fix or held CR asks
    alone with no `--outside-stack` (a held CR's hold order already carries the user's word);
  - `--outside-stack "<reason>"` is used only on an order of the Chief of Staff that carries the
    user's word for that CR alone. The reason starts with that order's id (`O-<k>: <words>`). It
    is never used to get past a refusal on the Foreman's own judgement;
  - an order note `shape: through the stack` on a CR (the Chief of Staff's, see 4) is taken like
    any later take: `take stack --epoch <n>` (or `[foreman→stack] note shape: <cr>` to a running
    stack driver), then `order done`;
  - the heartbeat's `shape stack: …` line is the stack's reminder: its `next` is the step for any
    stack event read at that wake.
- **`foreman.md`** keeps:
  - **a pointer in place of the moved span**, one bullet: "A stack batch (`--mode stack`, or a
    batch switched to a stack by `order mode`): its rules are in
    [foreman-stack](foreman-stack.md). Read it whole at the batch's start and again after each
    compaction while `status` shows `shape stack`.";
  - **a pointer in place of the Stack branch** of the `order merged` bullet: "**Stack:** see
    [foreman-stack](foreman-stack.md), "After a merge".";
  - **the opening paragraph** (the line that says "and again after a compaction: reread only those
    startup sections, not whole cards") gains one clause: in a stack batch, also
    `foreman-stack.md` whole (the manifest's `batch:stack` reading);
  - **"A mode switch"**, which covers every mode, stays in `foreman.md`, taken out of the stack
    list into its own bullet of "Your means". Its "to a stack" branch adds: "read
    [foreman-stack](foreman-stack.md) before the first `take stack`";
  - the short stack mentions in "The user's boundaries" (the stack's top and the long gate, the CR
    of a stack whose readiness reaches the user through the stack), the release driver's
    `take stack` first, and the lost-Driver rules for the stack's unit. These stay where they are,
    each with a link to `foreman-stack.md` where it says "below".
- **`startup-manifest.json`**: a new action `"batch:stack": ["foreman-stack.md"]`, the reading of
  a stack batch. It goes in `actions`, not in `startup_sections` or `reload`: the whole card (about
  16 KB) does not fit the 12,544-byte startup and reload limit that `test_startup_manifest.py`
  measures for every role. The reload's own readings stay within that limit, and the card is read
  as an action right after the reload's `status`. The `version` stays 2: no new key kind is added.
- **`session-start.md`, "5. Reload"**: one sentence after "this role's startup sections only". A
  Foreman, or a Chief of Staff steering in direct mode, whose `$CHANTIER status` shows
  `shape stack` then reads the manifest's `batch:stack` readings before its next act. The reload's
  "Read only" rule is unchanged. Keep the sentence short: this section counts in every role's
  reload bytes.
- **`chief-of-staff.md`**:
  - the direct-mode steering section ("Steering a batch yourself", which reads `foreman.md`) adds
    `foreman-stack.md` for a stack batch;
  - the links that point at the moved rules are repointed to `foreman-stack.md`: the "Deliver by a
    time" bullet (around line 1060), "The five checks" in "A stack batch" (around lines 1231 and
    1756), and any other link the Driver finds by searching for `foreman.md` near "stack".
- **Host specifics** stay out of `foreman-stack.md` and `foreman.md`. If any of the moved text
  names a host's tool or path, it goes to `hosts/claude-code.md` (or `hosts/copilot.md`), and the
  shared card links to it. As read today the moved span names forges (GitHub, GitLab), not hosts,
  so no host card is expected to change.

### 4. The Chief of Staff checks each ask against the shape (card)

File: `skills/chantier/references/chief-of-staff.md`, the "A stack batch" bullet (around line
1226, "the one-action stack merge is not the only path").

Added (Q4, Q9), with the one criterion: each Foreman ask is checked against the batch's shape, not
only for being rebased and green. In a stack batch, read `status --refresh`'s shape line. A per-CR
`ready-to-merge` for a CR that is neither a fix nor held, while that line's `alone asks` is
`refused` or `allowed for <another cr> only` (another CR of the stack has an open PR, or a stacked
CR is open),
is mismatched unless it carries `outside the stack: O-<k>: …` naming an order of the user's word.
A mismatched ask is not offered. The Chief of Staff:

- sends it back: `$CHANTIER order note <cr> --note "shape: through the stack"`;
- tells the user in one line: `<cr> asked alone in a stack batch: sent back through the stack`.

A stack's readiness is offered as a `stack-ready-to-merge`, after the native stack is read on the
forge (`forge-stack show`, the five checks). In direct mode the steering session checks its own
asks the same way. (The CLI already refuses such an ask; the check catches one recorded before this
CR or forced without a fitting order.)

### 5. Cards that other ready CRs edit (critic fix 5)

Two CRs in `3-ready` edit text that this CR moves out of `foreman.md`:

- **hold-live-cr**: its §8 moves "A held CR" (`foreman.md`, today inside the stack batch bullet)
  into a bullet for every mode. If hold-live-cr lands first, "A held CR" is no longer in the moved
  span: it stays in `foreman.md`, and this CR moves the rest. If this CR lands first, hold-live-cr
  takes "A held CR" from `foreman-stack.md` and places its every-mode bullet in `foreman.md`.
- **park-live-cr**: it edits inside the moved span, and its tests read `foreman.md` for
  `rebase: <cr> dropped`.

Rule: whichever of the CRs lands second re-applies its edit in the card that holds the text at its
rebase, and a test that reads moved text reads both cards (`foreman.md` and `foreman-stack.md`
joined), so it holds whatever the landing order.

### 6. The scenario (`scenario/run_scenario.py`, `scenario/README.md`)

- **The scripted Foreman** (`Foreman.turn`, around line 767, where a ready CR gets
  `ready-to-merge`/`pr-in-draft`) follows the new card: in a stack batch, a ready CR that is
  neither a fix nor held gets a per-CR `ready-to-merge` ask only when `shape_blockers` is empty for it; otherwise it
  waits for the stack. Without this change, step 13 (`stack_batch`) would hit the refusal.
- **New checks in `stack_batch`** (step 13):
  - before any CR has a PR: `status --refresh --epoch 1` prints, as its second line,
    `shape stack: next parallel until 2 ready with a PR; stack driver: none; native stack: absent; alone asks: allowed`;
  - with one CR (`<one>`) ready with a PR and no other open PR: the line ends
    `alone asks: allowed for <one> only`, and `asks ready-to-merge <one> <pr>` is accepted;
  - once two CRs are ready with a PR: the line reads `next take stack` and `alone asks: refused`,
    and `asks ready-to-merge <two> <pr>` exits 2 with the refusal's text and records no ask;
  - with `agents set stack agent-stack`: the line reads `next note to the stack driver; stack
    driver: agent-stack`;
  - after `stack one two three`: the line reads `native stack: present (<one>, <two>, <three>)`;
  - `asks ready-to-merge <two> <pr> --outside-stack "O-1: the user's word"` (O-1 an order of the
    batch) is recorded, and its printed line ends `outside the stack: O-1: the user's word`;
    `--outside-stack "the user's word"` exits 1;
  - `asks pr-in-draft <two> …` is still accepted;
  - a plain `status` prints no `shape stack:` line.

  The Driver orders these checks to fit the step's existing sequence; where the step has no moment
  with exactly one open PR, that case stays with the unit tests.
- **One parallel step** already in the scenario (for example `lost_messages`): `status --refresh`
  there prints no `shape stack:` line. One check.
- **`scenario/README.md`, "Coverage"**: one bullet for the guard and the shape line, with its
  `(unit: …)` and `(test: …)` markers, as `test_scenario_coverage.py` requires.

## Evidence

- **Unit tests**, in a new file `skills/chantier/scripts/cli/tests/test_stack_shape.py`. Keep it
  well under the 400-line limit (`test_code_targets.py`, `MAX_FILE_LINES`), few and parametrized,
  on `BatchRecord`/`CrEntry` built in memory as `test_stack_due.py` does:
  - `shape_blockers`, parametrized: empty for a CR alone (no other open PR, nothing stacked open);
    names another open CR with a PR; names an open stacked CR, the asking CR included; names the
    release CR's open PR; ignores merged and cancelled CRs, stacked or not (Studio's second wave
    after the morning stack merged: the merged stacked CRs do not count, the second wave's open PRs
    do); ignores a fix CR's and a held CR's open PR, and a held CR with `stacked` still set (Q12);
  - the guard, parametrized: in a stack batch with a blocker, refuses `ready-to-merge` for a change
    CR and for a release CR; accepts it for a fix CR and for a held CR, with no flag (Q12);
    accepts `pr-in-draft`, `ready-locally` and
    `stack-ready-to-merge`; accepts `ready-to-merge` for a CR alone, and in a parallel or series
    batch with other open PRs. The refusal's text is compared whole with the fenced text above;
  - the flag, parametrized: accepted where the guard refuses with a reason `O-<k>: …` naming an
    order of the batch (the recorded text ends `outside the stack: <reason>`, the event carries
    `outside_stack`); refused (exit 1) with an empty reason, a reason without `O-<k>: `, an
    unknown order, or on an ask the guard would let through. Use one in-process `asks` call on a
    prepared stack batch for the recorded text and the exit codes;
  - `shape_line`, parametrized: the exact line with nothing recorded (above); `next take stack`
    with two CRs ready with a PR; `next take stack` after a merged stack when two new CRs are
    ready (no CR ever stacked is not required); `next take stack at the next ready CR or merge`
    with an open stack and nothing to add (Q13); `alone asks: allowed for <cr> only` when the only
    other open PRs are a fix CR's and a held CR's (Q12); `note to the stack driver` with a
    recorded driver; `native stack: present (…)` with merged stacked CRs left out; each
    `alone asks` value; `[]` for a parallel or series batch;
  - `stack_due` unchanged: `test_stack_due.py` passes as is;
  - **the shipped cards**, read from the repository at the head under test, not from a copy:
    `startup-manifest.json`'s `actions["batch:stack"] == ["foreman-stack.md"]`, and the file
    exists; `foreman-stack.md` holds "The five checks of a stack ready to merge", the
    `--outside-stack` rule and `shape: through the stack`; `foreman.md` no longer holds "A folded
    CR" and does hold the link `[foreman-stack](foreman-stack.md)`; "The final-order take" is in
    `foreman-stack.md` and not in `foreman.md`; `session-start.md`'s "5. Reload" names
    `batch:stack`; `chief-of-staff.md` holds `shape: through the stack` and `sent back through the
    stack`. A check on a span that hold-live-cr or park-live-cr also moves reads both cards joined
    (see 5).

  `test_startup_manifest.py` (377 lines) gets no new rows: its existing measurement covers the new
  action (every action reading must resolve) and the reload limit, which the `session-start.md`
  sentence must keep.
- **`test_release_tag.py`** reads `tag done: steering session` from `foreman.md`. That phrase
  belongs to the release path and stays in `foreman.md`. If the Driver finds it inside the moved
  span, the test reads both cards.
- **Cards on both hosts**: no agent file changes (`agents/`, `com.github.copilot/agents/`). The
  cards are shared, and `foreman-stack.md` is read through the manifest on both hosts.
- **Gates** (`AGENTS.md`): `just check`; `just eval-dry-run`, because the change touches the CLI's
  `src/`; `just scenario` (ubuntu-latest) green at the PR's head, because the change touches the
  CLI, the cards and the scenario; and the local `chantier gate` if this CR is the batch's top.
  `just test` stays within its time budget.

## Out of scope

- No forge read in the shape line or the guard, and no new check of the native stack (the five
  checks stay `forge-stack show`'s).
- No refusal for `pr-in-draft` or `ready-locally`, and no refusal in parallel or series batches.
- No change to `take`, `take stack`, `stack`, `stack_due`'s behaviour or `forge-stack`, nor to the
  stack driver's card (`driver.md`, "Stack driver").
- No rewording of the moved stack rules beyond links, the Q10 limit after the span's opening
  sentence and the four `## The stack's asks` points.
- The docs (`docs/use-cases-foreman.md`) are not required. If the Driver judges they name the moved
  rules, one line pointing at the card is enough.

## Open questions

None. The spec v2's two questions are settled by Q12 and Q13 (Fable advisor, rule 12).

Small points settled by the spec-writer in v3 (rule 12):

- The criterion uses `stacks.chain` as it stands (open, neither fix nor held, release last) rather
  than repeating its filter, so the guard, the shape line and the Chief of Staff's check cannot
  drift from what the stack itself holds.
- `--outside-stack` on a held CR's ask is refused with the "only for … that the stack guard
  refuses" text, like a fix CR's: the guard never refuses that ask, so the flag would only
  decorate it.
