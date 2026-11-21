# A stack batch keeps its shape after the Foreman's compactions

A stack batch must keep acting as a stack after the Foreman's context is compacted, through a light
but systematic mechanism that the CLI enforces (Studio's owner: "pas trop lourd mais
systématique"). Two parts carry it: a shape line at each heartbeat, and `asks` refusing a per-CR
ready ask in a stack batch. Two lighter parts back them up: a stack card the Foreman rereads at
the reload, and the Chief of Staff checking each ask against the shape.

## Goal

The incident (Studio batch-07, shape stack, a Foreman reused for a second wave after several
compactions): after the morning's stack merged, the Foreman shipped each new CR as its own PR on
main, each with its own `ready-to-merge` ask. It ran no `take stack`, started no stack driver and
made no native stack. Each merge by the owner left the other PRs behind main. The cause: after a
compaction the Foreman rereads only its startup sections. The stack rules sit deep in
`foreman.md` ("The user's boundaries" and "Your means"), so the shape survived as a word but not
as a procedure. After this CR:

- the Foreman's heartbeat shows the stack's state in one line, every time;
- the CLI refuses the wrong ask, so a forgotten procedure stops at the CLI and does not reach the
  user;
- the stack rules live in one card that a stack batch's Foreman reads at the batch's start and
  rereads after each compaction;
- the Chief of Staff relays no readiness ask that does not fit the batch's shape.

## Decisions carried (02-answers.md)

- **Q1 (D, refuse unless forced):** `asks` refuses a per-CR `ready-to-merge` ask in a stack batch.
  A fix CR is excepted. An explicit flag lets the ask through. This spec chooses the flag's name
  and wording (the brief leaves them to the spec): `--outside-stack "<reason>"`.
- **Q2 (A):** at each `status --refresh`, in stack batches only, one line with a fixed format:
  `shape stack: next take stack; stack driver: none; native stack: absent`.
- **Q3:** superseded by Q5.
- **Q4 (A):** one line in the Chief of Staff's card: each Foreman ask is checked against the batch's
  shape (in a stack batch: a stack ask and a native stack), not only for being rebased and green.
- **Q5 (B):** a separate card, `foreman-stack.md`, read at the reload of a stack batch. Its stack
  rules move out of `foreman.md`, which keeps a pointer to it. The manifest
  (`startup-manifest.json`) names it.
- **Q6:** grilled enough. Next come the spec-writer and then the critic, and the CR goes to the
  next batch (`3-ready`).

## What changes

### 1. The guard: `asks` refuses a per-CR `ready-to-merge` in a stack batch (CLI)

Files: `skills/chantier/scripts/cli/src/chantier/rails_release.py` (the refusal, beside
`CR_READINESS` and `readiness_key`), `commands/batch_status.py` (`asks`, which calls it before
`record_ask`) and `declare/batch_status.py` (the new flag and the help text).

- **The refusal.** `asks <text>` refuses with exit 2 (`EXIT_PRECONDITION`) and records nothing
  when all of these hold:
  - the batch's `mode` is `stack`;
  - the text's first word is `ready-to-merge`, and its second word names a CR of the batch
    (the same match as `readiness_key`, through `normalize_cr`);
  - that CR's `kind` is not `fix` (a fix CR sits outside every shape: excepted, as Q1 says; a
    release CR is not excepted, because in a stack it is the top and its readiness is the
    complete `stack-ready-to-merge`);
  - **the batch has made a stack**: at least one CR of the batch, merged and cancelled ones
    included, has `stacked` set (the `stack <cr>…` command sets it at the stack driver's
    ordering, and `order mode` away from a stack clears it). This is the reverse of
    `stack_due`'s "no CR placed by `stack`". In Studio's incident, the merged CRs of the morning's
    stack keep their `stacked` flag, so the second wave's per-CR ask is refused.

  Before the batch's first stack, the guard lets the ask through. This keeps the rule already in
  `foreman.md`: until the first stack is made, a stack batch runs like a parallel batch, and a CR
  handed back ready on the default branch is an ordinary `ready-to-merge`. See open question 1.

  `pr-in-draft` and `ready-locally` are never refused, because neither invites a merge. Neither
  is `stack-ready-to-merge`, nor any other kind of ask.

- **The refusal's text** (one line on stderr, exit 2):
  `refused: <batch> is a stack and has made one: <cr>'s readiness goes up with the stack's
  (`take stack --epoch <n>`, the stack driver's hand-back, then `asks "stack-ready-to-merge …"`);
  a fix CR is outside the stack; `--outside-stack "<O-k: why>"` records this ask anyway`.

- **The flag `--outside-stack "<reason>"`.**
  - With the flag, an ask the guard would refuse is recorded. Its recorded text is the ask's text
    followed by ` outside the stack: <reason>`, so the Chief of Staff sees the reason in the line
    the CLI prints (`[foreman→chief-of-staff] ask A-n: ready-to-merge <cr> <link> … outside the
    stack: <reason>`). The `ask` event carries `outside_stack: <reason>`.
  - The flag is refused with exit 1 (`EXIT_USAGE`) when the reason is empty, or when the ask is
    one the guard would not refuse (another word, a fix CR, a batch that is not a stack, or a
    stack batch that has made no stack yet). The usage message reads `--outside-stack is only
    for a per-CR ready-to-merge ask in a stack batch that has made a stack`. The flag therefore
    never decorates an ordinary ask.
  - Superseding (`record_ask`) is unchanged: a forced ask is a `("cr", <cr>)` readiness ask like
    any other.
- **The help text** (`declare/batch_status.py`, `asks`): one clause added. A per-CR
  `ready-to-merge` is refused in a stack batch that has made a stack, except for a fix CR.
  `--outside-stack` records it anyway.
- **Steering.** The guard does not depend on the actor: a Chief of Staff steering in direct mode
  meets the same refusal.

### 2. The shape line at each heartbeat (CLI)

Files: `skills/chantier/scripts/cli/src/chantier/stacks.py` (a new `shape_line(b_data)`, beside
`stack_line`) and `commands/batch_status.py` (`status`).

- With `--refresh`, with or without `--epoch`, and only when the batch's `mode` is `stack`,
  `status` prints one line right after the batch line (the `<batch> running steering … shape
  stack …` line):
  `shape stack: next <next>; stack driver: <driver>; native stack: <native>`
  - `<next>`: `take stack` when no stack driver is recorded (`stack_agent` empty), and
    `note to the stack driver` when one is recorded (events then go to it as
    `[foreman→stack] note …`, as the card says);
  - `<driver>`: the recorded `stack_agent`, else `none`;
  - `<native>`: `present (<cr>, <cr>…)` listing the open CRs of `chain` that have `stacked`
    set, bottom first, else `absent`.

  With nothing recorded, the line is Q2's example exactly:
  `shape stack: next take stack; stack driver: none; native stack: absent`.
- A plain `status` (no `--refresh`), and any batch that is not a stack, prints no such line.
  The existing `stack: take stack now: …` line (`stack_line`) is unchanged and still printed when
  due.
- The line is read from the record only: no forge read and no write. "Native stack" here means
  what the record holds as placed by the stack driver (`stacked`), as the line's job is a
  reminder, not a check. The five checks on the forge stay with `forge-stack show`.

### 3. The card `foreman-stack.md` and the reload (cards, manifest)

Files: `skills/chantier/references/foreman-stack.md` (new), `foreman.md`,
`startup-manifest.json`, `session-start.md` (section "5. Reload") and `chief-of-staff.md`.

- **The new card** `skills/chantier/references/foreman-stack.md`, headed `# Foreman: a stack
  batch`. Its opening says who reads it and when:
  - the Foreman of a stack batch (a batch whose `status` line shows `shape stack`, by `--mode
    stack` or by `order mode --note stack`), and the Chief of Staff steering one in direct mode;
  - at the batch's start, and again after each compaction;
  - at a mode switch to a stack.

  It holds, moved verbatim from `foreman.md` (wording kept, links adjusted, no rule changed but
  the additions named below):
  - the stack batch rules of "Your means", from `A stack batch (`--mode stack`, or a batch
    switched to a stack by `order mode`): until the first stack is made it runs like a parallel
    batch …` through the end of "The five checks of a stack ready to merge". That span covers:
    the first take, each later take, a merge while a stack driver runs, a working CR placed on
    another, the final-order take, a held CR, deliver by a time, `take stack` and the stack
    driver's lifecycle, its hand-backs and the `stack-ready-to-merge` asks (partial and
    complete), the anomalies, a drop in the stack, heavy CI, the failed-check route, the gaps,
    inserting a CR, and the five checks;
  - the **Stack** branch of the `order merged` bullet (a restack, a folded CR, rebase notes
    before the first stack, nothing left open), plus the "say which one you chose" line that
    goes with it.

  Suggested level-2 sections, so that later readings can name them: `## The stack's asks`,
  `## The stack grows`, `## The stack driver`, `## After a merge`, `## The five checks`. The
  Driver may rename them, and the manifest names the whole file.

  **New text in `## The stack's asks`**, the only rules this CR adds to the card:
  - once the batch has made a stack, a CR's readiness reaches the Chief of Staff only through
    the stack: no per-CR `ready-to-merge` for a CR that is not a fix (the CLI refuses it), but
    the next `take stack` and, at the stack driver's hand-back, the `stack-ready-to-merge` ask;
  - `--outside-stack "<reason>"` is used only on an order of the Chief of Staff that carries the
    user's word for that CR alone. The reason starts with that order's id (`O-<k>: <words>`).
    It is never used to get past a refusal on the Foreman's own judgement;
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
  - **the opening paragraph** (the line that says "and again after a compaction: reread only
    those startup sections, not whole cards") gains one clause: in a stack batch, also
    `foreman-stack.md` whole (the manifest's `batch:stack` reading);
  - **"A mode switch"**, which covers every mode, stays in `foreman.md`, taken out of the stack
    list into its own bullet of "Your means". Its "to a stack" branch adds: "read
    [foreman-stack](foreman-stack.md) before the first `take stack`";
  - the short stack mentions in "The user's boundaries" (the stack's top and the long gate, the
    CR of a stack whose readiness reaches the user through the stack), the release driver's
    `take stack` first, and the lost-Driver rules for the stack's unit. These stay where they
    are, each with a link to `foreman-stack.md` where it says "below".
- **`startup-manifest.json`**: a new action `"batch:stack": ["foreman-stack.md"]`, the reading
  of a stack batch. It goes in `actions`, not in `startup_sections` or `reload`: the whole card
  (about 16 KB) does not fit the 12,544-byte startup and reload limit that
  `test_startup_manifest.py` measures for every role. The reload's own readings stay within that
  limit, and the card is read as an action right after the reload's `status`. The `version`
  stays 2: no new key kind is added.
- **`session-start.md`, "5. Reload"**: one sentence after "this role's startup sections only".
  A Foreman, or a Chief of Staff steering in direct mode, whose `$CHANTIER status` shows
  `shape stack` then reads the manifest's `batch:stack` readings before its next act. The
  reload's "Read only" rule is unchanged. Keep the sentence short: this section counts in every
  role's reload bytes.
- **`chief-of-staff.md`**:
  - the direct-mode steering section ("Steering a batch yourself", which reads `foreman.md`)
    adds `foreman-stack.md` for a stack batch;
  - the links that point at the moved rules are repointed to `foreman-stack.md`. These are the
    "Deliver by a time" bullet (around line 1060), "The five checks" in "A stack batch" (around
    lines 1231 and 1756), and any other link the Driver finds by searching for `foreman.md`
    near "stack".
- **Host specifics** stay out of `foreman-stack.md` and `foreman.md`. If any of the moved text
  names a host's tool or path, it goes to `hosts/claude-code.md` (or `hosts/copilot.md`), and
  the shared card links to it. As read today the moved span names forges (GitHub, GitLab), not
  hosts, so no host card is expected to change.

### 4. The Chief of Staff checks each ask against the shape (card)

File: `skills/chantier/references/chief-of-staff.md`, the "A stack batch" bullet (around line
1226, "the one-action stack merge is not the only path").

One line added (Q4): each Foreman ask is checked against the batch's shape, not only for being
rebased and green. Once a stack batch has made a stack (`status --refresh` shows
`native stack: present`, or the record shows a `stack-ready-to-merge` already sent), a CR's
readiness is offered only as a `stack-ready-to-merge`, after the native stack is read on the forge
(`forge-stack show`, the five checks). A per-CR `ready-to-merge` there (a fix CR aside) is offered
only when it carries `outside the stack: O-<k>: …` naming an order of the user's word. Otherwise
it is not offered, and `$CHANTIER order note <cr> --note "shape: through the stack"` sends it back
to the Foreman. In direct mode the steering session checks its own asks the same way.

### 5. The scenario (`scenario/run_scenario.py`, `scenario/README.md`)

- **The scripted Foreman** (`Foreman.turn`, around line 767, where a ready CR gets
  `ready-to-merge`/`pr-in-draft`) follows the new card: in a stack batch where a CR is `stacked`,
  a ready CR that is not a fix gets no per-CR `ready-to-merge` ask. Without this change, step 13
  (`stack_batch`) would hit the refusal once a CR hands back after `stack one two three`.
- **New checks in `stack_batch`** (step 13):
  - before `stack`: `status --refresh --epoch 1` prints `shape stack: next take stack; stack
    driver: none; native stack: absent` as its second line, and a per-CR `asks ready-to-merge
    <one> <pr>` is accepted (no stack made yet);
  - with `agents set stack agent-stack`: the line reads `next note to the stack driver; stack
    driver: agent-stack`;
  - after `stack one two three`: the line reads `native stack: present (<one>, <two>,
    <three>)`, and `asks ready-to-merge <two> <pr>` exits 2 with the refusal's text and records
    no ask;
  - `asks ready-to-merge <two> <pr> --outside-stack "O-1: the user's word"` is recorded, and its
    printed line ends `outside the stack: O-1: the user's word`;
  - `asks pr-in-draft <two> …` is still accepted;
  - a plain `status` prints no `shape stack:` line.
- **One parallel step** already in the scenario (for example `lost_messages`): `status --refresh`
  there prints no `shape stack:` line. One check.
- **`scenario/README.md`, "Coverage"**: one bullet for the guard and the shape line, with its
  `(unit: …)` and `(test: …)` markers, as `test_scenario_coverage.py` requires.

## Evidence

- **Unit tests**, in a new file `skills/chantier/scripts/cli/tests/test_stack_shape.py`. Keep it
  well under the 400-line limit (`test_code_targets.py`, `MAX_FILE_LINES`), few and
  parametrized, on `BatchRecord`/`CrEntry` built in memory as `test_stack_due.py` does:
  - the guard, parametrized: a stack batch with a CR `stacked` refuses `ready-to-merge` for a
    change CR and for a release CR, accepts it for a fix CR, accepts `pr-in-draft`,
    `ready-locally` and `stack-ready-to-merge`, and accepts `ready-to-merge` in a stack batch
    with no CR stacked, in a parallel batch and in a series batch. A merged CR that keeps
    `stacked` counts as a stack made (Studio's second wave);
  - the flag, parametrized: it is accepted where the guard refuses (the recorded text ends
    `outside the stack: <reason>`), and refused (usage) with an empty reason or on an ask the
    guard would let through. Use one in-process `asks` call on a prepared stack batch for the
    recorded text and the exit codes;
  - `shape_line`, parametrized: the exact line for no driver and nothing stacked (Q2's
    example), with a recorded stack driver, and with stacked CRs (merged ones left out of
    `present (…)`); `[]` for a parallel or series batch;
  - **the shipped cards**, read from the repository at the head under test, not from a copy:
    `startup-manifest.json`'s `actions["batch:stack"] == ["foreman-stack.md"]`, and the file
    exists; `foreman-stack.md` holds "The final-order take", "The five checks of a stack ready
    to merge" and the `--outside-stack` rule; `foreman.md` no longer holds "The final-order
    take" or "A folded CR", and does hold the link `[foreman-stack](foreman-stack.md)`;
    `session-start.md`'s "5. Reload" names `batch:stack`; `chief-of-staff.md` holds the Q4
    line (`shape: through the stack`).

  `test_startup_manifest.py` (377 lines) gets no new rows: its existing measurement covers the
  new action (every action reading must resolve) and the reload limit, which the
  `session-start.md` sentence must keep.
- **`test_release_tag.py`** reads `tag done: steering session` from `foreman.md`. That phrase
  belongs to the release path and stays in `foreman.md`. If the Driver finds it inside the moved
  span, the test reads both cards.
- **Cards on both hosts**: no agent file changes (`agents/`, `com.github.copilot/agents/`). The
  cards are shared, and `foreman-stack.md` is read through the manifest on both hosts.
- **Gates** (`AGENTS.md`): `just check`; `just eval-dry-run`, because the change touches the
  CLI's `src/`; `just scenario` (ubuntu-latest) green at the PR's head, because the change
  touches the CLI, the cards and the scenario; and the local `chantier gate` if this CR is the
  batch's top. `just test` stays within its time budget.

## Out of scope

- No forge read in the shape line, and no new check of the native stack (the five checks stay
  `forge-stack show`'s).
- No refusal for `pr-in-draft` or `ready-locally`, and no refusal in parallel or series batches.
- No change to `take`, `take stack`, `stack` or `forge-stack`, nor to the stack driver's card
  (`driver.md`, "Stack driver").
- No rewording of the moved stack rules beyond links and the four `## The stack's asks` points.
- The docs (`docs/use-cases-foreman.md`) are not required. If the Driver judges they name the
  moved rules, one line pointing at the card is enough.

## Open questions

1. **Before the batch's first stack.** As specified, the guard refuses only once the batch has
   made a stack. Before that, a per-CR `ready-to-merge` goes through, as `foreman.md` already
   orders (a stack batch runs like a parallel batch until its first stack). Q1 says "in a stack
   batch" with no such limit. Confirm that the guard starts at the first stack. Refusing from the
   start would make the Foreman use `--outside-stack` routinely for the first CRs of every stack
   batch.
2. **Who may use `--outside-stack`.** As specified, the Foreman uses it only on an order of the
   Chief of Staff that carries the user's word (reason `O-<k>: …`), and the Chief of Staff offers
   a forced ask only with such an order. Confirm, or allow the Foreman's own named reason too.
3. **A mismatched ask at the Chief of Staff.** As specified, the Chief of Staff does not offer it
   and sends `order note <cr> --note "shape: through the stack"`, which the Foreman turns into a
   `take stack`. Confirm that this is the wanted path, rather than telling the user and letting
   them choose.
