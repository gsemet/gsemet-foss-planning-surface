# A stack batch keeps its shape after the Foreman's compactions

A stack batch must keep acting as a stack after the Foreman's context is compacted, through a light
but systematic mechanism that the CLI enforces (Studio's owner: "pas trop lourd mais
systématique"). Two parts carry it: a shape line at each heartbeat, and `asks` refusing a per-CR
ready ask in a stack batch while that ask would leave another PR of the batch behind main. Two
lighter parts back them up: a stack card the Foreman rereads at the reload, and the Chief of Staff
checking each ask against the shape. Specification v6.

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
  a CR truly alone may still ask alone, and so may a CR outside the stack's chain (a fix or held
  CR);
- the stack rules live in one card that a stack batch's Foreman reads at the batch's start and
  rereads after each compaction; the heartbeat's shape line ends with that card's path (`rules:`),
  so a compacted Foreman, which rereads only its startup sections, is led back to it (Q16);
- the Chief of Staff relays no readiness ask that does not fit the batch's shape: it sends it back
  and tells the user in one line.

## Decisions carried (02-answers.md)

- **Q1 (D, refuse unless forced):** `asks` refuses a per-CR `ready-to-merge` ask in a stack batch.
  A fix CR is excepted (and a held CR, Q12; critic run 2's fix 6 makes the exception "the CR is
  not in `chain(b_data)`"). An explicit flag lets the ask through:
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
- **Q6:** grilled enough; spec-writer, then critic; destination the next batch (`3-ready`),
  replaced by Q17: batch-30, on top of CR-428, CR-430 and CR-431.
- **Q7:** replaced by Q10 ("once the first stack is made" no longer holds).
- **Q8 (A):** `--outside-stack` is used only on a Chief of Staff order carrying the user's word; its
  reason is `O-<k>: …`. Q14 says which order.
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
- **Q14 (A, Fable advisor, rule 12):** `--outside-stack` names an open order (`done` unset) whose
  `cr` is the asking CR and whose note does not start with `shape:`. The Foreman asks with the flag
  first, then marks the order done; the Chief of Staff checks that the named order is its own on
  that CR (it may be done by then). See 1, 3 and 4.
- **Q15 (A, Fable advisor, rule 12):** a ready CR refused behind a working or blocked CR's draft PR
  waits: Q11 and the guard stay. The refusal names the shape line's `next` (one helper shared with
  `shape_line`) instead of `take stack`. The Foreman's ask about the blocked CR names the ready CR
  waiting behind it, and the Chief of Staff offers the user `order hold <blocked cr>` or an order on
  the ready CR (the flag). See 1, 2, 3 and 4.
- **Critic run 2, fixes 3-7:** the "ordinary `ready-to-merge` ask" sentence is rewritten to the Q10
  limit in the move (3); `chief-of-staff.md`'s "merge each PR ready to merge as it comes" is
  qualified (4); drop-to-next-batch joins 5 (5); the guard's exception is "the CR is not in
  `chain(b_data)`" (6); the `session-start.md` reload sentence is for a Chief of Staff steering in
  direct mode only (7).
- **Critic run 3, fixes 2-5:** the shape line's `forming` test applies only while no CR of
  `chain` is stacked, so an open stack waiting for its merge reads Q13's `next` (2, see 2); the
  card's shape-line bullet calls the line a reminder, "The first take" and "Each later take" staying
  the reference (3, see 3); the scenario's `early_conflict` stack case changes its check (4, see 6);
  the landing order is known: CR-428, CR-430 and CR-431 land before this CR (5, see 5).
- **Q16 (A, Fable advisor, rule 12):** the shape line ends
  `rules: <skill>/references/foreman-stack.md (reread after a compaction)`, `<skill>` being
  `skill_dir().as_posix()` as `commands/facts.py` builds its `cards:` line (line 111). The card and
  `foreman.md` keep the rule; the line is only a pointer, keyed on the batch's mode and not on a
  role (precedents: `commands/facts.py:111`'s `cards:` line, `commands/access.py:24`'s
  `(driver.md)`). No startup section changes. Known limit: the line makes the card reachable after
  a compaction; it cannot force the read. The guard of 1 stays the hard stop. See 2, 3, 6 and the
  evidence.
- **Q17 (A, the user, 2026-11-21):** the destination is batch-30, on top of CR-428, CR-430 and
  CR-431 (the user: "et tous les inbox en cours de spécification pareil tu mets dans le batch …
  il faut traiter ces P1 et inbox cette nuit"), not Q6's next batch. At this CR's merge the guard
  applies at once to batch-30's remaining CRs (the CLI and cards run live from the main checkout),
  and the Chief of Staff tells the Foreman to read `foreman-stack.md`. See 5.
- **Critic run 4, fixes 2-5:** `chief-of-staff.md`'s "A stack batch" sentence on the CRs handed
  back `ready` before the stack is made is qualified with the shape line's `alone asks` (2, see 4);
  `foreman-stack.md` says how the next stack forms once nothing of a stack remains open (3, see
  3); `foreman-stack` joins the host-tool card list of `test_plugin_files.py` (4, see the
  evidence); the scenario's `early_conflict` stack case is named by its check's text (5, see 6).
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
  - that CR is in `chain(b_data)` (critic run 2, fix 6). A CR not in the chain asks alone: a fix
    CR sits outside every shape, as Q1 says; a held CR is out of the stack on its hold order, which
    already carries the user's word (Q12); and any CR that another change keeps out of the chain
    (park-live-cr's parked CR, hold-live-cr's out-of-order CRs) is excepted the same way, with no
    change here. A release CR is in the chain and is not excepted: in a stack it is the top, and
    its readiness is the complete `stack-ready-to-merge`;
  - `shape_blockers(b_data, <cr>)` is not empty (Q10).

  In Studio's second wave, CR-447's ask at 11:48 and any other ask made while another second-wave
  CR's PR was open are refused, which is what left the other PRs behind main. An ask made while
  its CR was the only open PR of the batch passes, as Q10 wants.

  `pr-in-draft` and `ready-locally` are never refused, because neither invites a merge. Neither is
  `stack-ready-to-merge`, nor any other kind of ask.

- **The refusal's text**, one line on stderr, exit 2, exactly (`<batch>`, `<cr>`, `<next>` and
  the list filled in; `<blockers>` is the blockers' ids joined by `, `, each followed by
  ` (stacked)` when it is stacked):

  ```text
  refused: <batch> is a stack and <cr> is not alone (open: <blockers>): its readiness goes up with the stack's (next: <next>; then the stack driver's hand-back and `asks "stack-ready-to-merge …"`); a CR not in the stack's chain asks alone; `--outside-stack "O-<k>: <why>"` records this ask on an open order on <cr> that carries the user's word
  ```

  `<next>` is the shape line's `next` for the batch, from the same helper (`next_step`, see 2), so
  the refusal and the heartbeat never disagree (Q15). With a ready CR behind a working or blocked
  CR's draft PR, it reads `next: parallel until 2 ready with a PR`: the ready CR waits.

- **The flag `--outside-stack "<reason>"`** (Q8).
  - With the flag, an ask the guard would refuse is recorded. Its recorded text is the ask's text
    followed by ` outside the stack: <reason>`, so the Chief of Staff sees the reason in the line
    the CLI prints (`[foreman→chief-of-staff] ask A-n: ready-to-merge <cr> <link> … outside the
    stack: <reason>`). The `ask` event carries `outside_stack: <reason>`.
  - The reason must start with `O-<k>: ` followed by words, where `O-<k>` is an order of the
    batch (`orders`, `OrderRecord` in `core/records.py`) that is open (`done` unset), whose `cr` is
    the asking CR, and whose `note` does not start with `shape:` (Q14). So the mode order (`cr`
    `-`), another CR's order, a done order and the Chief of Staff's own `shape: through the stack`
    note never let an ask through. Otherwise the flag is refused with exit 1 (`EXIT_USAGE`):

    ```text
    --outside-stack needs a reason "O-<k>: <why>" naming an open order on <cr> that carries the user's word
    ```

  - The flag is also refused with exit 1 when the ask is one the guard would not refuse (another
    word, a CR not in the stack's chain, a batch that is not a stack, or a CR with no blocker):

    ```text
    --outside-stack is only for a per-CR ready-to-merge ask that the stack guard refuses
    ```

    The flag therefore never decorates an ordinary ask.
  - Superseding (`record_ask`) is unchanged: a forced ask is a `("cr", <cr>)` readiness ask like
    any other.
- **The help text** (`declare/batch_status.py`, `asks`): one clause added. In a stack batch, a
  per-CR `ready-to-merge` is refused while another CR of the stack has an open PR or a stacked CR
  is open; a CR not in the stack's chain asks alone; `--outside-stack "O-<k>: <why>"` records it
  on an open order on that CR that carries the user's word.
- **Steering.** The guard does not depend on the actor: a Chief of Staff steering in direct mode
  meets the same refusal.

### 2. The shape line at each heartbeat (CLI)

Files: `skills/chantier/scripts/cli/src/chantier/stacks.py` (a new `shape_line(b_data)`, beside
`stack_line`; a small helper `forming(b_data)` that `stack_due` and `shape_line` share; and a
helper `next_step(b_data) -> str` that computes `<next>` below, shared by `shape_line` and the
guard's refusal, Q15) and `commands/batch_status.py` (`status`).

- With `--refresh`, with or without `--epoch`, and only when the batch's `mode` is `stack`,
  `status` prints one line right after the batch line (the `<batch> running steering … shape
  stack …` line):

  `shape stack: next <next>; stack driver: <driver>; native stack: <native>; alone asks: <alone>; rules: <skill>/references/foreman-stack.md (reread after a compaction)`

  - `<next>` (Q11), from `next_step(b_data)`:
    - `note to the stack driver` when a stack driver is recorded (`stack_agent` set): events then
      go to it as `[foreman→stack] note …`, as the card says;
    - else `take stack` when a take is due: while no CR of `chain` is stacked, `forming(b_data)`
      holds at least `FORMING` (2) CRs (the first take); or a stacked CR of `chain` exists and a CR
      of `chain` that is not stacked (release aside) is `ready` with a PR (a later take). The
      `forming` test does not apply once a CR of `chain` is stacked (critic run 3, fix 2): an open
      stack of two ready CRs waiting for its merge counts two in `forming`, yet has nothing to add
      and reads the next case;
    - else, when a stacked CR of `chain` exists (the stack waits for its merge, nothing to add):
      `take stack at the next ready CR or merge` (Q13: a recorded merge is also a trigger, as
      `foreman.md`'s "Each later take" says);
    - else `parallel until 2 ready with a PR`.

    `forming(b_data)` is `stack_due`'s per-CR test without its batch conditions: the CRs of the
    chain that are neither release nor fix (`_alone`), `ready`, with a PR, and with every open
    dependency `ready` (`_open_after`). `stack_due` keeps its own conditions (running, no stack
    driver, no CR ever stacked) and calls `forming`; its behaviour does not change. The shape line
    does not use "no CR ever stacked" but "no CR of `chain` stacked" (merged CRs leave `chain`): in
    Studio's second wave, after the morning stack merged, it reads `take stack` as soon as two
    second-wave CRs are ready with a PR.
  - `<driver>`: the recorded `stack_agent`, else `none`.
  - `<native>`: `present (<cr>, <cr>…)` listing the CRs of `chain` that have `stacked` set,
    bottom first, else `absent`.
  - `<alone>`, from `shape_blockers(b_data)` (the criterion, batch-wide), counting the CRs of
    `chain` only (Q12: a fix or held CR's PR does not count):
    - `refused` when a stacked CR of `chain` exists or at least two CRs of `chain` have a PR;
    - `allowed for <cr> only` when exactly one CR of `chain` has a PR and none is stacked;
    - `allowed` when no CR of `chain` has a PR.
  - `rules: <skill>/references/foreman-stack.md (reread after a compaction)` (Q16): always the
    line's last part, the same in every state; `<skill>` is `skill_dir().as_posix()`
    (`plugin_files.py`), as `commands/facts.py` builds its `cards:` line. The part points at the
    card; it does not repeat the card's rule.

  With nothing recorded, the line reads exactly (`<skill>` filled in):
  `shape stack: next parallel until 2 ready with a PR; stack driver: none; native stack: absent; alone asks: allowed; rules: <skill>/references/foreman-stack.md (reread after a compaction)`.
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
  - at the batch's start, and again after each compaction (the heartbeat's shape line names this
    card's path in its `rules:` part, Q16, so a compacted Foreman finds it there);
  - at a mode switch to a stack.

  It holds, moved verbatim from `foreman.md` (wording kept, links adjusted, no rule changed but the
  additions named below):
  - the stack batch rules of "Your means", from `A stack batch (`--mode stack`, or a batch switched
    to a stack by `order mode`): until the first stack is made it runs like a parallel batch …`
    through the end of "The five checks of a stack ready to merge". That span covers: the first
    take, each later take, a merge while a stack driver runs, a working CR placed on another, the
    final-order take, deliver by a time, `take stack` and the stack driver's lifecycle,
    its hand-backs and the `stack-ready-to-merge` asks (partial and complete), the anomalies, a
    drop in the stack, heavy CI, the failed-check route, the gaps, inserting a CR, and the five
    checks;
  - the **Stack** branch of the `order merged` bullet (a restack, a folded CR, rebase notes before
    the first stack, nothing left open), plus the "say which one you chose" line that goes with it.

  The moved span's opening sentence (`foreman.md`, around lines 379-383: "until the first stack is
  made it runs like a parallel batch with chains: each CR handed back `ready` on the default branch
  is an ordinary `ready-to-merge` ask (…, even with CRs before it in the order still working)") is
  rewritten to the Q10 limit in the move (critic run 2, fix 3). Suggested text: "until the first
  stack is made it runs like a parallel batch with chains, with one limit: a CR handed back `ready`
  on the default branch asks `ready-to-merge` alone only while no other CR of the stack's chain has
  an open PR and no stacked CR is open (the shape line's `alone asks`); otherwise it waits for the
  stack (see "The stack's asks"). The CLI reads such a CR `ready to merge`, with no remark on the
  record." The status word (`ready to merge`) stays; the clause "even with CRs before it in the
  order still working" goes, since the guard now refuses that case. The rest of the sentence (a
  merge handled by the rebase notes, a CR based on another CR's branch handing back `PR in draft`)
  is kept.

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
  - `--outside-stack "<reason>"` is used only on an open order of the Chief of Staff on that CR
    that carries the user's word for that CR alone (not a `shape:` note). The reason starts with
    that order's id (`O-<k>: <words>`). The Foreman asks with the flag first, then marks the order
    done (`order done O-<k>`): the CLI accepts only an open order (Q14). It is never used to get
    past a refusal on the Foreman's own judgement;
  - a ready CR refused behind a working or blocked CR's draft PR waits (`next: parallel until 2
    ready with a PR`). When the CR in front is blocked, the Foreman's ask about it also names the
    ready CR waiting behind it (`…; <ready cr> waits behind it`), so the Chief of Staff can offer
    the user a way out (see 4). The final-order take ends the wait at the latest: once no CR of the
    stack is working or able to start, `take stack --note "final order"` stacks what is ready, and
    `take stack` asks for no count of ready CRs (`_take_stack`, `commands/driver.py`, checks only
    the mode, the stack driver, the budget and the lease) (Q15);
  - an order note `shape: through the stack` on a CR (the Chief of Staff's, see 4) follows the
    shape line's `next`: with `take stack` or `take stack at the next ready CR or merge`, it is
    taken like any later take, `take stack --epoch <n>` (or `[foreman→stack] note shape: <cr>` to
    a running stack driver), then `order done`; with `parallel until 2 ready with a PR`, `order
    done` and wait (Q15);
  - the heartbeat's `shape stack: …` line is the stack's reminder, not its rule: its `next` names
    the step for any stack event read at that wake, and "The first take" and "Each later take" stay
    the reference (as `foreman.md` says today of `stack: take stack now`, around lines 390-392:
    "this rule stays the reference; the line only reminds it") (critic run 3, fix 3);
  - the shape line's `rules:` part names this card's path (Q16): when this card is not in context
    (after a compaction, or a session that has not read it in this batch), read it whole before the
    next act on the stack;
  - one sentence on a batch with no stack open (critic run 4, fix 3). Suggested text: "Once
    nothing of a stack remains open (each of its CRs merged or cancelled), the batch is again as
    before its first stack: the next stack forms by "The first take" (two CRs ready with a PR),
    which the shape line's `next take stack` reminds; the `stack: take stack now` line does not
    (it is printed only while no CR of the batch was ever stacked)." It may sit in the rewritten
    opening instead; the card check below reads it in either place.
- **`foreman.md`** keeps:
  - **a pointer in place of the moved span**, one bullet: "A stack batch (`--mode stack`, or a
    batch switched to a stack by `order mode`): its rules are in
    [foreman-stack](foreman-stack.md). Read it whole at the batch's start and again after each
    compaction while `status` shows `shape stack`; the heartbeat's shape line names its path
    (`rules:`).";
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
- **`session-start.md`, "5. Reload"**: one sentence after "this role's startup sections only",
  limited to a Chief of Staff steering in direct mode (critic run 2, fix 7): one whose
  `$CHANTIER status` shows `shape stack` then reads the manifest's `batch:stack` readings before
  its next act. A Foreman is led back to the card by the shape line's `rules:` (Q16): after a
  compaction it rereads only its startup sections, which do not hold `foreman.md`'s opening
  paragraph. The reload's "Read only" rule is unchanged. Keep the sentence short: this
  section counts in every role's reload bytes.
- **`chief-of-staff.md`**:
  - the direct-mode steering section ("Steering a batch yourself", which reads `foreman.md`) adds
    `foreman-stack.md` for a stack batch;
  - the links that point at the moved rules are repointed to `foreman-stack.md`: the "Deliver by a
    time" bullet (around line 1060), "The five checks" in "A stack batch" (around lines 1231 and
    1756), and any other link the Driver finds by searching for `foreman.md` near "stack";
  - the go's stack advice (around line 842: "the user may also merge each PR ready to merge as it
    comes, before the stack is made") is qualified "while that CR is the only open PR of the stack"
    (critic run 2, fix 4), so the advice matches the guard.
- **Host specifics** stay out of `foreman-stack.md` and `foreman.md`. If any of the moved text
  names a host's tool or path, it goes to `hosts/claude-code.md` (or `hosts/copilot.md`), and the
  shared card links to it. As read today the moved span names forges (GitHub, GitLab), not hosts,
  so no host card is expected to change.

### 4. The Chief of Staff checks each ask against the shape (card)

File: `skills/chantier/references/chief-of-staff.md`, the "A stack batch" bullet (around line
1226, "the one-action stack merge is not the only path").

Added (Q4, Q9), with the one criterion: each Foreman ask is checked against the batch's shape, not
only for being rebased and green. In a stack batch, read `status --refresh`'s shape line. A per-CR
`ready-to-merge` for a CR of the stack's chain (`stack` lists it; not a fix or held CR), while that
line's `alone asks` is `refused` or `allowed for <another cr> only` (another CR of the stack has an
open PR, or a stacked CR is open), is mismatched unless it carries `outside the stack: O-<k>: …`
where `O-<k>` is the Chief of Staff's own order on that CR, carrying the user's word (Q14: the
Foreman may have marked it done by then, so the check is that the order is yours and on that CR,
not that it is open). A mismatched ask is not offered. The Chief of Staff:

- sends it back: `$CHANTIER order note <cr> --note "shape: through the stack"`;
- tells the user in one line: `<cr> asked alone in a stack batch: sent back through the stack`.

When a Foreman ask about a blocked CR names a ready CR waiting behind it (Q15), the Chief of Staff
offers the user two ways out with the blocked CR's question: `order hold <blocked cr>` (the held CR
leaves the chain, and the ready CR may then ask alone), or an order on the ready CR that carries
the user's word, for the Foreman's `--outside-stack "O-<k>: …"`.

The same bullet's sentence "Before the stack is made on the forge, each CR handed back `ready` on
the default branch is an ordinary `ready-to-merge` ask, offered as mergeable now" is qualified
(critic run 4, fix 2): "…, offered as mergeable now, while that CR is the only open PR of the
stack's chain (the shape line's `alone asks`)". The rest of the sentence (a CR above it, a draft on
another CR's branch, waits) is kept.

A stack's readiness is offered as a `stack-ready-to-merge`, after the native stack is read on the
forge (`forge-stack show`, the five checks). In direct mode the steering session checks its own
asks the same way. (The CLI already refuses such an ask; the check catches one recorded before this
CR or forced without a fitting order.)

### 5. Batch-30, and the cards other CRs edit there (critic run 1, fix 5; critic run 3, fix 5; Q17)

This CR goes into batch-30, on top of CR-428, CR-430 and CR-431 (Q17). Those three edit text that
this CR moves out of `foreman.md`; being below it, they land before it, so the order is known:

- **CR-431 hold-live-cr**: its §8 moves "A held CR" out of the stack batch bullet into a bullet for
  every mode. Once it has landed, "A held CR" is no longer in the moved span: it stays in
  `foreman.md`, where hold-live-cr left it, and this CR moves the rest (§3's list does not name
  it).
- **CR-430 park-live-cr**: it edits inside the moved span, and its tests read `foreman.md` for
  `rebase: <cr> dropped`. Its edits travel with the span into `foreman-stack.md`, as it left them.
- **CR-428 drop-to-next-batch**: it edits "A drop in the stack" (`foreman.md`, inside the moved
  span) to list `3-ready` among the drop destinations. Its edit travels with the span into
  `foreman-stack.md`, as it left it.

Rule: this CR moves the span as those CRs left it, at its rebase onto them, and rewrites none of
their text. Each of their card checks that reads text this CR moves (park-live-cr's
`rebase: <cr> dropped`, drop-to-next-batch's "A drop in the stack" check, and any other the Driver
finds by searching the tests for the moved phrases) is changed by this CR to read `foreman.md` and
`foreman-stack.md` joined.

At this CR's merge (Q17), the guard applies at once to batch-30's remaining CRs (the CLI and cards
run live from the main checkout), and the Chief of Staff tells the Foreman to read
`foreman-stack.md`.

### 6. The scenario (`scenario/run_scenario.py`, `scenario/README.md`)

- **The scripted Foreman** (`Foreman.turn`, around line 767, where a ready CR gets
  `ready-to-merge`/`pr-in-draft`) follows the new card: in a stack batch, a ready CR of the
  stack's chain gets a per-CR `ready-to-merge` ask only when `shape_blockers` is empty for it;
  otherwise it waits for the stack. Without this change, step 13 (`stack_batch`) would hit the refusal.
- **`early_conflict`'s stack case** (`run_scenario.py`, the check "a stack batch: no merge-tree
  runs and no `conflict` ask is sent", which today also requires that the last ask starts with
  `ready-to-merge <second> `) changes its check with the scripted Foreman (critic run 3, fix 4): no
  merge-tree runs, no `conflict` ask, no per-CR ask for `second`, and the stack is due (`status`
  prints the `stack: take stack now` line, or the shape line reads `next take stack`).
- **New checks in `stack_batch`** (step 13):
  - before any CR has a PR: `status --refresh --epoch 1` prints, as its second line,
    `shape stack: next parallel until 2 ready with a PR; stack driver: none; native stack: absent; alone asks: allowed; rules: <skill>/references/foreman-stack.md (reread after a compaction)`,
    with `<skill>` the scenario's skill folder (Q16);
  - the path the `rules:` part names exists (one check, Q16);
  - the checks below compare the part of the line before `; rules:`, and each line they read ends
    with the same `rules:` part;
  - with one CR (`<one>`) ready with a PR and no other open PR: the line ends
    `alone asks: allowed for <one> only`, and `asks ready-to-merge <one> <pr>` is accepted;
  - once two CRs are ready with a PR: the line reads `next take stack` and `alone asks: refused`,
    and `asks ready-to-merge <two> <pr>` exits 2 with the refusal's text and records no ask;
  - with `agents set stack agent-stack`: the line reads `next note to the stack driver; stack
    driver: agent-stack`;
  - after `stack one two three`: the line reads `native stack: present (<one>, <two>, <three>)`;
  - `asks ready-to-merge <two> <pr> --outside-stack "O-1: the user's word"`, where `O-1` is an open
    `order note <two>` (not a `shape:` note, Q14), is recorded, and its printed line ends
    `outside the stack: O-1: the user's word`; then `order done O-1`; `--outside-stack "the user's
    word"` exits 1;
  - `asks pr-in-draft <two> …` is still accepted;
  - a plain `status` prints no `shape stack:` line.

  The Driver orders these checks to fit the step's existing sequence; where the step has no moment
  with exactly one open PR, that case stays with the unit tests.
- **One parallel step** already in the scenario (for example `lost_messages`): `status --refresh`
  there prints no `shape stack:` line. One check.
- **`scenario/README.md`, "Coverage"**: one bullet for the guard and the shape line, its `rules:`
  pointer to `foreman-stack.md` included (Q16), with its `(unit: …)` and `(test: …)` markers, as
  `test_scenario_coverage.py` requires.

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
    CR and for a release CR (both in the chain); accepts it, with no flag, for a CR not in the
    chain: a fix CR and a held CR (Q12, fix 6); accepts `pr-in-draft`, `ready-locally` and
    `stack-ready-to-merge`; accepts `ready-to-merge` for a CR alone, and in a parallel or series
    batch with other open PRs. The refusal's text is compared whole with the fenced text above.
    Q15's rows: a ready CR's ask refused behind a working CR's draft PR and behind a blocked CR's
    draft PR, each refusal showing `next: parallel until 2 ready with a PR`; and the same ready CR
    accepted alone once the blocked CR is held;
  - the flag, parametrized: accepted where the guard refuses with a reason `O-<k>: …` naming an
    open order on the asking CR whose note does not start with `shape:` (the recorded text ends
    `outside the stack: <reason>`, the event carries `outside_stack`); refused (exit 1, the Q14
    text) with an empty reason, a reason without `O-<k>: `, an unknown order, the mode order,
    another CR's order, a done order on the CR, and a `shape:` note on the CR; refused (exit 1) on
    an ask the guard would let through. Use one in-process `asks` call on a prepared stack batch
    for the recorded text and the exit codes;
  - `shape_line`, parametrized: the exact whole line with nothing recorded (above), the `rules:`
    path included, built from `skill_dir().as_posix()` (Q16); in every row, the line ends with
    `; rules: <skill>/references/foreman-stack.md (reread after a compaction)` and that path exists
    in the repository at the head under test; the other rows compare the part before `; rules:`:
    `next take stack` with two CRs ready with a PR; `next take stack` after a merged stack when two
    new CRs are ready (no CR ever stacked is not required); `next take stack at the next ready CR or
    merge` with an open stack and nothing to add (Q13), including an open stack of two ready
    stacked CRs, which `forming` alone would read as a take (critic run 3, fix 2); `alone asks: allowed for <cr> only` when the only
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
    stack`, its go advice ("as it comes, before the stack is made") carries `while that CR is the
    only open PR of the stack`, and its "A stack batch" sentence ("Before the stack is made on the
    forge, each CR handed back `ready` …") carries ``while that CR is the only open PR of the stack's
    chain (the shape line's `alone asks`)`` (critic run 4, fix 2): the check finds each sentence and
    its qualifier within it; `foreman-stack.md` holds `again as before its first stack` and
    `"The first take"` in the same sentence (critic run 4, fix 3); `foreman.md` and
    `foreman-stack.md` joined no longer hold "even with CRs before it in the order still working".
    "A held CR" stays in `foreman.md` (hold-live-cr, below this CR in batch-30). A check on text that
    park-live-cr or drop-to-next-batch edited inside the moved span, theirs or this CR's, reads
    both cards joined (see 5).

  `test_plugin_files.py`'s `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`
  gets `"foreman-stack"` in its card list (critic run 4, fix 4), so the new card is held to the
  same no-host-tool rule as `foreman`.

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
  CLI, the cards and the scenario; and the local `chantier gate` while this CR is batch-30's top.
  `just test` stays within its time budget.

## Out of scope

- No forge read in the shape line or the guard, and no new check of the native stack (the five
  checks stay `forge-stack show`'s).
- No refusal for `pr-in-draft` or `ready-locally`, and no refusal in parallel or series batches.
- No change to `take`, `take stack`, `stack`, `stack_due`'s behaviour or `forge-stack`, nor to the
  stack driver's card (`driver.md`, "Stack driver").
- No rewording of the moved stack rules beyond links, the span's opening sentence rewritten to the
  Q10 limit (critic run 2, fix 3) and the `## The stack's asks` points (the sentence on a batch
  with no stack open included, critic run 4, fix 3); in `chief-of-staff.md`, no rewording beyond
  the links, the qualified go advice (fix 4), the qualified "A stack batch" sentence (critic run 4,
  fix 2) and the check of 4.
- The docs (`docs/use-cases-foreman.md`) are not required. If the Driver judges they name the moved
  rules, one line pointing at the card is enough.

## Open questions

None. The spec v2's two questions are settled by Q12 and Q13, the critic run 2's two findings
by Q14 and Q15, and the critic run 3's finding 1 by Q16 (Fable advisor, rule 12); the destination
by the user's Q17.

Small points settled by the spec-writer (rule 12):

- The criterion uses `stacks.chain` as it stands (open, neither fix nor held, release last) rather
  than repeating its filter, so the guard, the shape line and the Chief of Staff's check cannot
  drift from what the stack itself holds.
- `--outside-stack` on a held CR's ask is refused with the "only for … that the stack guard
  refuses" text, like a fix CR's: the guard never refuses that ask, so the flag would only
  decorate it. v4: the same for any CR not in the chain.
- v4: the refusal no longer names `take stack --epoch <n>`; it names `next: <next>` (Q15), so
  `<n>` leaves its text.
- v4: `take stack` takes a single ready CR (`_take_stack`, `commands/driver.py`, counts no ready
  CRs), so the final-order take does end Q15's wait. The shape line's `next` is not changed for
  the final-order moment (it may still read `parallel until 2 ready with a PR` then): Q15 keeps
  Q11, and the card's final-order rule, read with the line, names the step.
- v4: the order check reads `OrderRecord`'s `cr`, `done` and `note` as they stand; the `shape:`
  test is on the note's start after leading spaces are stripped.
