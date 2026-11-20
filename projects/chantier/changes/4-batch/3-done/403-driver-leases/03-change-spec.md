# Change Specification: Driver leases on what `take` gave them

Origin: verbal (2026-11-10, Beads study; grilled 2026-11-20 in `planning-server`). No tracker issue.

Part D of the seven-part split of `planning-server` (planning-server-Q7). Its grill is that CR's:
[`02-answers.md`](02-answers.md) here lists the answers it carries;
`2-backlog/P3/planning-server/experiments/03-change-spec-all-parts.md`, "Part D. Leases", is the
approved reference this specification starts from. Depends on `1-inbox/typed-journal-events`
(Part A; `depends.json`), kept from the split; this CR adds no type to Part A's schema (spec-critic
answer 1, D.7).

## 1. Goal, in the user's terms

Heartbeat and reclaim, borrowed from Vercel Board ("ça vaudrait le coup", 2026-11-10; "tout",
2026-11-20): a Driver, the stack driver and the QA driver each hold a short **lease** on the unit
`take` (or `order qa`) gave them, renewed by their own commands. A live lease protects the unit
from a second Driver. A lease that expired is **not confirmed**, not gone: a Driver waiting for
its worker runs no command and cannot renew, so the steering session checks with the host before
taking the unit again, and gives `--reclaim` once it did. The lease replaces the "Copilot session
file written in the last 5 minutes" heuristic of `close`, until `copilot-close-end-event` lands. A
long CI wait or a long gate does not lose the lease: a background task recorded for the unit, or
its gate running or waiting in the queue, keeps it live.

## 2. Words

- **Lease:** a numbered, time-limited hold of a Driver on its unit (a CR, the stack, or a QA
  order `O-k`), renewed by the Driver's commands, ended by its hand-back, the order's end,
  `agents set <unit> -` on a live lease, a `--reclaim`, or the CR's `cancel` or `order drop`.
  Local to the machine that runs the batch, never published.
- **Unit:** what a lease holds: a CR id, `stack`, or a QA order's id `O-k`.
- **Live / not confirmed / ended:** D.1 below. "Not confirmed" (an expired lease) is never
  "ended" and never "gone": its holder can still renew it as long as nobody took the unit again,
  and only the steering session, after checking with the host, takes the unit from it
  (`--reclaim`). In the code the state may be named `expired`; every text to the user and to an
  agent says "not confirmed".
- **Hold:** a `lease <unit> hold` run: one command the Driver gives, run as a child, keeping the
  lease live while it runs. Not a task runner.
- `TTL`: 10 minutes. `RENEW`: 3 minutes (the interval the cards ask for while a Driver runs
  commands).

Never "epoch" in a text to the user (the CLI flag `--epoch` keeps its name).

## 3. Decisions carried

| Decision (date) | Where it lands |
| --- | --- |
| Heartbeat/reclaim worth it (11-10); leases replace the 5-minute session-file heuristic (11-20, Q3 "tout") | D.1-D.4 |
| Hash IDs rejected (11-10) | a lease is the unit's id and a small number `n` |
| A running batch's state stays local (11-10, planning-repo answer 4) | D.1: in `batch.json`; `batch-takeover`'s `resume.batch` strips it (§5) |
| No Board dependency (11-20, Q1-Q2) | built in chantier; `lease hold` is no task runner (§9) |
| Q7: seven CRs; D needs A | `depends.json` kept; no type added to Part A's schema (spec-critic answer 1) |
| Q8: a lease stays live while a background task recorded for the CR runs (the CI watch), as the long gate | D.1 liveness, D.2 `lease <unit> hold` |
| Q9: `lease` named in AGENTS.md as an exception to the measured-cost rule, citing "tout" | D.5 |
| Q14: leases serve Copilot's `close` until `copilot-close-end-event`; then shown only | D.4 |
| Q16: 10 minutes, renewed every 3, a constant in the code | D.1 |
| Q20: on Claude Code, a live lease is shown only; transcripts stay the source | D.4 |
| Q21: QA orders get leases in this work | D.3 |
| The split carries its docs and SVGs as a list (11-20) | D.6 |
| Spec answer 1: facts `lease: stack <n>`; the stack lease ends when the stack agent is cleared; no `handback stack` | D.3 |
| Spec answer 2: the 45,000-byte cap stays; `claim lost` on the common path, the rest off it | D.5 |
| Spec answer 3: the first `agents set O-k <agent>` after `order qa` keeps lease 1 | D.3 |
| Spec answer 4: a lease renews once when the held child ends | D.2 (`lease hold`) |
| Spec answer 5: times in lease messages are UTC | D.2 |
| Spec answer 6: `cancel` and `order drop` end a live lease | D.2 |
| Spec-critic 1: an expired lease is "not confirmed"; no `lease-expired@1`; the steering session checks with the host, then `--reclaim`; the Driver renews at each wake (later: `driver-wake`'s wake) | D.1, D.2, D.5, D.7 |
| Spec-critic 2: the common path's CI watch line gives the `lease <cr> hold` form, within the bytes the card frees | D.5 |
| Spec-critic 3: a CR's gate waiting in the queue, its process alive, keeps the CR's lease live; a gate run by the stack driver keeps the stack lease live | D.1, D.3 |
| Spec-critic 4: `--lease` only on the stack driver's writing forms; `show` and the bare `stack` need none | D.3 |
| Spec-critic 5: `--lease` required on `release start|go|published` | D.2 |
| Spec-critic 6: `agents set <cr>|<O-k> -` ends the unit's live lease, as `agents set stack -` does | D.2, D.3 |
| Spec-critic 7: Copilot's `close` on leases accepted; `docs/hosts.md` and row D say what is no longer seen | D.5, D.6 |
| Spec-critic 8, 9: the evidence is a rule, not a list; the scenario keeps its budget; expiry from the frozen clock | §7 |

## 4. What changes

### D.1 What a lease is

- A lease starts for a unit at each `take <cr>`, each `take stack`, and each `order qa` (for its
  order `O-k`, D.3). Number `n`: 1 at the unit's first lease, then the unit's last number plus
  one; `taken` and `expires` = now + `TTL`.
- `TTL` (10 min) and `RENEW` (3 min) are constants in a new module
  `skills/chantier/scripts/cli/src/chantier/core/leases.py`, never configured
  (planning-server-Q16). The test seam `CHANTIER_LEASE_TEST_TTL` (seconds) is read only there, as
  `CHANTIER_HUB_TEST_TIMES` is read only in `hub/times.py`. Every "now" goes through
  `core/clock.py` (`now`, and `fix` behind `--clock`), so tests freeze it.
- The lease is in `batch.json` (local, never published), in `core/records.py`: a new record
  `Lease` `{n, taken, renewed, expires, ended}`, and the fields `CrEntry.lease`,
  `BatchRecord.stack_lease` and `OrderRecord.lease`, each a `Lease` or null. A batch opened before
  this version has none: its units work as today, with no `--lease` asked anywhere.
- A lease means something only on the machine that runs the batch: `batch-takeover`'s published
  `resume.batch` strips each CR's `lease`, the record's `stack_lease` and each order's `lease`, as
  it strips worktree paths and session ids; a takeover restores them as null, and the next lease of
  a unit on the new machine is lease 1 (no last number kept). `batch-takeover`
  (`2-backlog/P3/batch-takeover`) has not landed: whichever of the two lands second carries this
  strip (no `resume.batch` code exists today).
- A lease is **live** while `ended` is null and one of:
  - `expires` is in the future;
  - a long gate of the CR runs: a `.long-gate*.lock` slot whose holder names the CR and whose
    process is still that one (`gate_slots.slot_of` and `gate_slots.holder_alive`, the reading the
    gate itself uses; the reference names it "`.long-gate*.run` ... `procs.alive`", which is this
    same slot);
  - a long gate of the CR waits in the queue (spec-critic 3): a ticket in `.long-gate.queue/`
    naming the CR whose process is alive (`gate_queue.read_ticket` and the liveness
    `gate_queue.ticket_cr` reads, with `drop=False`: a reader that only looks deletes nothing);
  - a background task recorded for the unit runs (planning-server-Q8): a
    `.lease-hold.<unit>.<k>.run` record (D.2) names the unit and the lease's number, and its process
    is still that one (`procs.alive_since` against the record's write time, so a reused pid does
    not count; a record with a dead process holds nothing).

  Else it is **not confirmed** (`ended` null, none of the above: it expired) or **ended**
  (`ended` set).
- The stack lease's long gates: the gate names a CR, not `stack`, so a gate the stack driver runs
  keeps the stack lease live by running under `lease stack hold --lease <n> -- <the gate command>`
  (D.2's hold, D.3); a gate held so also counts for the CR it names, by the slot or the ticket.
- A Driver renews at each wake (spec-critic 1): its next command carries `--lease <n>`, or it runs
  `lease <unit> renew`. A Driver waiting for its worker runs no command and has no periodic wake,
  so its lease may expire while it is well: that is why an expired lease is only "not confirmed".
  When `2-backlog/P3/driver-wake` lands, the renewal moves to that wake; whichever of the two
  lands second writes it there.

### D.2 Commands

All refusals change nothing: the record, the log and the folder stay as they were. Every
`HH:MM:SS` and `HH:MM` in a lease text is UTC, like the record's stamps (spec answer 5).

- `take <cr|stack> --epoch <n>` (`commands/driver.py`, `take`; the check in `rails.py`,
  `check_take`, and `_take_stack` for the stack):
  - refuses a unit whose lease is live: exit 3, `<cr> is held: lease <n> live until HH:MM:SS; take
    it again with --reclaim only on the user's word`;
  - refuses a unit whose lease is not confirmed: exit 3, `<cr>: lease <n> not confirmed since
    HH:MM (<k> min ago); check with the host that its Driver ended, then take it with --reclaim`
    (spec-critic 1);
  - `--reclaim` (new flag, `declare/driver.py`) takes it anyway, ends the old lease (`ended`) and
    logs `reclaim` with the old lease's number and its state (`live` or `not confirmed`) in
    `events.jsonl`; the steering session gives it on a not-confirmed lease after its check with the
    host, on a live one only on the user's word;
  - the existing rules stay: a `--note` for a working, ready or blocked CR; `agents set <cr> -`
    first while an agent is recorded (the CLI does not clear the agent itself);
  - on success the output's first line gains `, lease <n> until HH:MM:SS` (`took <cr> (<k> of <s>
    slots held), lease <n> until HH:MM:SS`), and the Driver's facts (`driver_prompt.py`,
    `driver_prompt_lines`) carry the line `lease: <n> (pass --lease <n> on your commands; renew at
    each wake: lease <cr> renew --lease <n>)`.
- `--lease <n>` (new option):
  - required, when the unit has a lease, on `round`, `ship`, `handback`, and on
    `release start|go|published` (`declare/release.py`, `commands/release.py`, `release`;
    spec-critic 5), and on the stack driver's writing forms (D.3);
  - optional on `gate`, `note`, `phase`;
  - a valid one renews the lease (`renewed`, `expires`);
  - missing on a required command: exit 2, `<command> <cr> needs --lease <n> (the number take
    printed)`; nothing recorded;
  - a number that is not the unit's current one, or the current one ended: exit 3, `claim lost:
    <cr> was taken again (lease <m>) at HH:MM; stop now: nothing recorded` (when it was ended with
    no new lease: `claim lost: <cr>'s lease <n> ended at HH:MM; stop now: nothing recorded`);
    nothing recorded;
  - the current one, not confirmed and not taken again: accepted and renewed (the Driver was only
    late); the log records `lease-late` with the minutes;
  - a command run by the steering session (`--epoch`) needs no lease.
- `handback <cr> ready|blocked --lease <n>` ends the lease (`ended`).
- `agents set <cr> -` and `agents set <O-k> -` (`commands/batch_status.py`, `agents`) end the
  unit's live lease, as `agents set stack -` ends the stack lease (spec-critic 6): the steering
  session clears an agent after its reported end, so the restart does not wait. A not-confirmed
  lease is left as it is: the next `take` (or the order's restart, D.3) needs `--reclaim` after the
  host check. The old Driver's next command gets `claim lost`.
- `cancel` (`commands/release.py`, `cancel`) and `order drop` (`commands/orders_drop.py`, `drop`)
  end the lease of the CR they take out of the batch, live or not confirmed (spec answer 6), and
  its old Driver's next command gets `claim lost`.
- `lease <unit>` (new command, declared in `declare/driver.py`; `<unit>` a CR, `stack` or `O-k`),
  read-only but for the removal of dead hold records:
  - `lease <n> of <unit>: live until HH:MM:SS (renewed HH:MM:SS)`, with `, held by <k> background
    task(s)` when a hold runs, `, gate running` or `, gate queued` when a long gate keeps it;
  - `lease <n> of <unit>: not confirmed since HH:MM (<k> min ago)`;
  - `lease <n> of <unit>: ended at HH:MM`;
  - `<unit>: no lease`.
- `lease <unit> renew --lease <n>`: renews, prints the first form; a stale number: the `claim
  lost` refusal.
- `lease <unit> hold --lease <n> -- <command> [args...]` (planning-server-Q8): checks the lease as
  `renew` does (the `claim lost` refusal on a stale number, nothing run), renews it, then runs
  `<command>` as its child process (no shell, as `core/git.py` runs git), writes
  `.lease-hold.<unit>.<k>.run` in the planning folder (`{unit, lease, pid, command, started}`, its
  own pid, `k` the first free number), streams the child's output, removes the record when the
  child ends, renews the lease once at that moment (spec answer 4; a lease ended or taken again
  meanwhile is left as it is), and exits with the child's exit code. It is how a Driver runs its
  CI watch in the background (`lease <cr> hold --lease <n> -- gh pr checks --watch`, `glab ci
  status --live`) and how the stack driver runs a long gate (D.3): the lease stays live while the
  child runs, with no renewal call. A record whose process is gone (a crash) holds nothing and is
  removed by the next `lease`, `take` or `status` that reads it. `IGNORED` (`core/files.py`) gains
  `.lease-hold.*.run`. It runs only what the Driver gives it.
- `status` (`commands/batch_status.py`): a working CR, the stack driver or an open QA order whose
  lease is not confirmed gets `, lease not confirmed since HH:MM (<k> min ago)` on its line.
  `handoff` (`commands/facts.py`) prints the lease line (the `lease <unit>` form).

The Release driver is a CR's Driver (`take <release-cr>`): the same lease and the same rules apply
to its `round`, `ship`, `handback` and `release start|go|published`.

### D.3 The stack's lease and a QA order's lease

- `take stack` (run by the steering session; the stack driver never runs it) starts
  `stack_lease`, and the stack driver's facts carry the line `lease: stack <n>` (spec answer 1).
  `take stack` on a live or not-confirmed stack lease is refused as `take <cr>` is (D.2), naming
  `stack`; `--reclaim` the same way.
- `--lease <n>` is required only on the stack driver's writing forms (spec-critic 4): `stack
  <crs…>`, `stack --out-of-draft` and `stack --draft` (`declare/delivery.py`), and `forge-stack
  create|rebuild|unstack` (`declare/forge_stack.py`), with the same refusals as on a CR Driver's
  `round` (exit 2 when missing, exit 3 `claim lost` on a stale or ended number) and the same
  renewal. `forge-stack show` and the bare `stack` (which prints the stack and writes nothing)
  need none, so the steering session's reads are never refused.
- No `handback stack` command is added: the stack driver ends with its `[stack→foreman]` message,
  and `stack_lease` ends when the steering session clears the stack agent with the existing
  `agents set stack - --epoch <n>` (`commands/batch_status.py`, `agents`: `-` sets
  `stack_agent` to null), when live; a not-confirmed stack lease is left for `take stack
  --reclaim` (D.2). The stack driver's `gate <cr>` and `note <cr>` name a CR, not `stack`: no
  stack lease is asked there; a long gate it runs goes under `lease stack hold --lease <n> --`
  to keep the stack lease live (D.1, spec-critic 3).
- `order qa` (`commands/orders.py`) starts the order's lease (planning-server-Q21):
  `OrderRecord.lease`, lease 1 of `O-k`. The skeleton `order qa` prints (`_qa_skeleton`) carries
  the line `lease: <n> of O-k (renew at each wake: lease O-k renew --lease <n>; run a long test
  under lease O-k hold --lease <n> -- <command>)`. The QA driver renews it as a CR's Driver does
  (it runs no `round` or `handback`, so `lease renew` and `lease hold` are its means). `order done`
  on the order (`_order_done`) ends the lease.
- `take` of an order is not a thing. A QA driver restarted by the Foreman's restart path gets a
  new lease from `agents set <O-k> <agent>` (`commands/batch_status.py`, `agents`) when the
  previous one ended (`lease <n+1> of O-k`, printed by `agents set`); a live or not-confirmed
  lease refuses that `agents set` as `take` refuses (exit 3, the same texts naming `O-k`;
  `--reclaim`, a new flag of `agents set`, with the same rule: after the host check on a
  not-confirmed lease, on the user's word on a live one). The first `agents set O-k <agent>` after
  `order qa` keeps lease 1 (spec answer 3); only a later one, a restart, is refused or starts lease
  `n+1`.

### D.4 `close` on Copilot and on Claude Code

`rails.running` (`rails.py`) on a Copilot batch no longer reads the session files' age:
`COPILOT_QUIET_SECONDS` and the `idle_seconds` call in `rails.running` go (`idle_seconds` itself
stays in `costs/sessions.py`: `commands/activity.py` still reads it). Instead
(planning-server-Q14):

- each held agent (`held_agents`) of a CR, of a QA order, and the recorded stack agent, is a cause
  while that unit's lease is live: `<agent> (<unit>) holds lease <n> until HH:MM:SS`; a
  not-confirmed or ended lease is no cause;
- a held agent of a unit with no lease (a batch opened before this version): `<agent> (<unit>):
  not measured (no lease)`, a cause, as `not measured` is today;
- the current Foreman is a cause while its last heartbeat (`BatchRecord.heartbeat`, written by
  `status --refresh --epoch`) is younger than `TTL`: `Foreman n°<k>: heartbeat <m> min ago (under
  10 min)`. A direct batch has no Foreman: the Chief of Staff's own session never blocks its close
  (as today, and as `docs/use-cases-direct.md` says).

The record causes stay as today (a CR not merged or cancelled, an open order, a recorded stack
agent).

What this no longer sees (spec-critic 7, accepted): a Driver's leftover background work after its
hand-back (the hand-back ended its lease), which the session file's age showed; D.5 and D.6 say it.

This holds until `2-backlog/P2/copilot-close-end-event` lands. From then on Copilot's `close`
reads the agent's end from `events.jsonl`, as that item specifies, and the lease is only shown
beside it, never a cause, as on Claude Code. Whichever of the two lands second carries this: if
that item lands first, this CR ships the shown-only form on Copilot directly.

On Claude Code, `close` keeps reading the transcripts' ends, the exact source; a live lease is
shown beside them in `close`'s output, never a cause (planning-server-Q20).

### D.5 Cards and project rules

The contract is in the cards: no agent file (`agents/`, `com.github.copilot/agents/`) names the
5-minute rule or a Driver's liveness (searched), so none changes.

- `skills/chantier/references/driver.md`:
  - on the CR driver's common path (the opening, the sections `startup-manifest.json` lists under
    `actions["cr-driver"]`, and `## CR driver`): only the lease line of the facts, `--lease <n>`
    on the named commands, the CI watch line in the form `lease <cr> hold --lease <n> -- <the
    watch>` (spec-critic 2), and "`claim lost`: stop at once, record nothing more, tell the
    Foreman" (a Driver must act on it at once), at most 600 bytes together;
  - in a trigger-read level-2 section the card's links name, not listed in the manifest (a new
    `## Means: ...` section), read when it applies: renew at each wake (`--lease` on the next
    command, or `lease <cr> renew --lease <n>`; with `driver-wake`, at its wake); any other wait
    longer than 3 minutes that runs a command (a review, a worker's run) under `lease <cr> hold
    --lease <n> -- <command>`; what "not confirmed" means (a late command is accepted while nobody
    took the CR again); reclaim (the steering session's, after its host check, or on the user's
    word for a live lease);
  - `## QA driver`: the order's lease, renewed or held the same way;
  - `## Stack driver`: the `lease: stack <n>` line, `--lease <n>` on its writing forms (`stack
    <crs…>`, `--out-of-draft`, `--draft`, `forge-stack create|rebuild|unstack`), its long gates
    under `lease stack hold`, and the same renewal and hold while it waits;
  - `## Release driver`: `--lease <n>` on its `round`, `ship`, `handback` and `release
    start|go|published`, and its long waits (CI, the publication) renewed or held as above.
- The cap: `4-batch/3-done/398-retro-batch-28-drivers-end-before-closin` has landed;
  `test_startup_manifest.py`, `test_cr_driver_common_path_reads_at_most_the_card_budget`, caps the
  common path at 45,000 bytes (`CR_DRIVER_COMMON_PATH_LIMIT`), and at `main` 8bd198b1 it measures
  about 44,950 bytes: about 50 bytes free. The cap does not rise (spec answer 2): the ~600 bytes
  this CR adds on the common path, the CI watch line's `hold` form among them, are paid by
  tightening the common path's existing text, dropping no rule; the rest of the lease text is off
  the common path, above.
- `skills/chantier/references/foreman.md`: `take` refused for a live lease: `--reclaim` only on
  the user's word through the Chief of Staff; `agents set <cr>|<O-k>|stack -` after an agent's
  reported end ends its live lease, so the restart does not wait; the `lease not confirmed` mark of
  `status` is not a Driver gone (a Driver waiting for its worker cannot renew): check its end with
  the host's means, and only once it ended take the CR again with `--reclaim --note "resume: lease
  not confirmed"` (a QA order: the restart path with `--reclaim`, D.3; the stack: `take stack
  --reclaim`).
- `skills/chantier/references/chief-of-staff.md` (direct mode): the same as the Foreman's. And the
  5-minute heuristic's texts say the lease instead: "Closing" (the clause "on Copilot, a session
  file written in the last 5 minutes, and `not measured` refuses too") and the refusal table's
  row **D** (its "on Copilot, an agent whose session file was written in the last 5 minutes counts
  as running" and its way out "on Copilot, wait until 5 minutes after its last write"): on
  Copilot, until `copilot-close-end-event`, a held agent whose lease is live (wait for its
  hand-back or its expiry, at most 10 minutes), a unit with no lease `not measured`, the Foreman's
  heartbeat under 10 minutes; and what is no longer seen until then: a Driver's leftover
  background work after its hand-back (spec-critic 7).
- `skills/chantier/references/concepts.md`: the word "lease" (a new entry in "Words", with "not
  confirmed"); the "Batch" word's `close` clause "on Copilot, a session file written in the last
  5 minutes; `not measured` refuses" says the lease instead.
- `AGENTS.md` (planning-server-Q9):
  - "The CLI's scope" names `lease` (with `take --reclaim` and `lease hold`) as an exception to "a
    new CLI tool comes from measured token-costly behaviour", built on the user's answer of
    2026-11-20 ("tout": all five of Board's ideas);
  - the write list adds the `.lease-hold.*.run` records in the planning folder.
  - The hub's sentence does not change: the hub writes nothing for leases (spec-critic 1).

### D.6 Docs, diagrams and other text made false (the list)

- `docs/planning-folder.md`:
  - the close paragraph (the one ending the batch's lifecycle: "`chantier close` refuses, naming
    the cause, while anything still runs (... whose transcript shows it still runs; ...)") adds: on
    Copilot, until `copilot-close-end-event` lands, a held agent runs while its lease is live, and
    the current Foreman while its heartbeat is under 10 minutes old;
  - "What is published and what stays local": the ignored list gains `.lease-hold.*.run`.
- `docs/use-cases-direct.md`:
  - "When the batch is paused, and when you close it": "In direct mode the check counts only your
    Drivers' session files as something that runs, not your own session" becomes: on Claude Code,
    your Drivers' transcripts; on Copilot, until `copilot-close-end-event` lands, their live
    leases; never your own session;
  - "Switch to Foreman mode": the Foreman restarts a CR at once when its old Driver reported its
    end; when its lease is only not confirmed, once it checked with the host that the Driver ended
    (`take --reclaim`); while it is live, with `--reclaim` only on your word.
- `docs/use-cases-foreman.md`, "Recover after a restart" and "Switch to direct mode": a CR whose
  old Driver's lease is not confirmed is taken again with `take --reclaim` once the steering
  session checked with the host that the Driver ended; while it is live, only on your word.
- `docs/hosts.md`, after the paragraph "On Copilot, chantier runs in the Copilot App ...": on
  Copilot, until `copilot-close-end-event` lands, `close` tells that a Driver, the stack driver or
  a QA driver still runs by its live lease (10 minutes, renewed by its commands), and the Foreman
  by a heartbeat younger than 10 minutes; it no longer sees a Driver's leftover background work
  after its hand-back (spec-critic 7); on Claude Code, by the transcripts, the lease only shown.
- `scenario/README.md`, the closing bullet ("closing on the user's word: `close` refusing ... and
  a Copilot session file written in the last 5 minutes or whose time is not measured"): the
  Copilot cases become §7's lease cases.
- Diagrams: none changes. Every `docs/*.svg` and `docs/*-texts.md` searched for "lease",
  "reclaim", "heartbeat", "session file", "5 min", "still runs": no diagram draws a Driver's
  liveness or the 5-minute rule; `batch-lifecycle`'s "it refuses, naming the cause, while
  anything runs" (SVG and texts) and `cr-lifecycle`'s heartbeat loop (`chantier status
  --refresh`, SVG and texts) stay true. No `<desc>` changes.
- Searched and unaffected: `README.md` (no `close` rule, no restart rule);
  `docs/tutorial-claude-code.md` ("The app restarted during a batch": a new Foreman picks up every
  CR where it was; its `close` text is Claude Code's, the transcripts); `docs/gates.md` (a running
  or queued long gate keeps the lease live; its text holds); `docs/costs.md` (its "expired" is the
  prompt cache's); the "On GitHub Copilot" sections of both use-case pages (no `close` rule
  there); `docs/boards.md`, `docs/web-board.md` (D changes no `STATUS.json` field the pane shows
  and no board view); `docs/release-notes/` (history; the next release's notes are written by the
  release process); `docs/planning-folder.md`'s event journal types table (no type added).

### D.7 Messages

- No journal type is added: the hub writes no line for a lease (spec-critic 1), and nothing else
  writes `lease-expired@1`; the reference's `lease-expired@1` is dropped. A lease that is not
  confirmed shows in `status` (D.2), where the steering session reads it.
- The refusals and lines of D.2-D.4, word for word as written there.

## 5. Out of scope

- A lease on a backlog CR or a grill: leases are a batch's, from `take` or `order qa`.
- A configured TTL (planning-server-Q16: a constant).
- The lease as a `close` cause on Claude Code (planning-server-Q20), and on Copilot once
  `copilot-close-end-event` lands (Q14).
- `lease hold` as a task runner (Board's `tasks run -- <cmd>`): it runs one command only to keep a
  lease live; no schedule, no conditional write, no per-principal grant.
- The lease shown on the board, in `STATUS.md` / `STATUS.json` or in the CR board pane: the
  reference names only `status`'s printed lines, `handoff` and `close` (no pane change, so no
  screenshot owed).
- A hub or watcher event for a lease that is not confirmed (spec-critic 1).
- A periodic wake of a Driver: `2-backlog/P3/driver-wake`'s.
- `access` (Part F, `1-inbox/explain-access`) and typed waits (Part E): they read the lease, they
  are not built here.
- Typed versions for the batch's own `events.jsonl` (`reclaim`, `lease-late` are plain log kinds).
- Several machines: a lease is local; a takeover starts at lease 1.

## 6. Host and default matrix

Depends on the host (how `close` tells a held agent runs), on no configured value (every time is a
constant with a test seam).

| Host | Cell | Expected |
| --- | --- | --- |
| Claude Code | `close` with a held Driver whose lease is live and whose transcript ended | passes: the transcript decides; the lease is shown |
| Claude Code | a Driver's `round` with a stale lease | exit 3, `claim lost` |
| both | `take` of a CR whose lease is not confirmed, without `--reclaim` | exit 3, the "check with the host" text |
| Copilot, before `copilot-close-end-event` | `close` with a held Driver (or QA driver) whose lease is live | refused: `<agent> (<unit>) holds lease <n> until ...` |
| Copilot, before `copilot-close-end-event` | `close` with every lease not confirmed or ended, the Foreman's heartbeat older than 10 min | passes |
| Copilot, before `copilot-close-end-event` | `close` on a batch opened before this version | refused: `not measured (no lease)` |
| Copilot, after `copilot-close-end-event` | `close` with a live lease and the agent's end in `events.jsonl` | passes: the end decides; the lease is shown |
| both | a CI watch run under `lease hold` past the TTL | the lease stays live |
| both | a long gate waiting in the queue past the TTL, its process alive | the lease stays live |

## 7. Evidence

- `skills/chantier/scripts/cli/tests/test_leases.py` (new), parametrized, on a prepared batch.
  Expiry comes from the frozen clock (`core/clock.py`), never from sleeping (spec-critic 9). It
  covers:
  - `take` starts lease 1; a second `take` with the lease live, then not confirmed, is refused
    (exit 3, each text); with `--reclaim` it starts lease 2, ends lease 1 and logs `reclaim`;
  - `round`, `ship`, `handback`, `release start|go|published`, and the stack driver's writing forms
    without `--lease` exit 2; `forge-stack show` and the bare `stack` need none; with lease 1 after
    lease 2 started, exit 3 `claim lost` and `batch.json` unchanged; a not-confirmed current lease
    is accepted and logs `lease-late`; `handback` ends it;
  - `lease <unit>` prints each of its four forms; a live long gate, and a live ticket in
    `.long-gate.queue/`, keep an expired lease live; a live `lease hold` keeps an expired lease
    live, its record is removed at the child's end, the child's end renews the lease once
    (`expires` = the child's end + `TTL`) and the exit code is the child's; a hold record with a
    dead pid holds nothing; `lease hold` with a stale number runs nothing;
  - `order qa` starts lease 1 of `O-k`, `order done` ends it; the first `agents set O-k <agent>`
    keeps lease 1, a later one after an ended lease prints lease 2, with a live or not-confirmed
    one exits 3;
  - `take stack` starts `stack_lease` and its facts carry `lease: stack <n>`;
  - `agents set <cr>|<O-k>|stack -` ends a live lease and leaves a not-confirmed one; `cancel` and
    `order drop` end a lease; the old Driver's next command gets `claim lost`;
  - every time in a lease text is UTC; a batch with no lease needs no `--lease`.
- `tests/test_rail_refusals.py`: the Copilot `close` causes of D.4 (a live lease, a not-confirmed
  one, no lease, a QA order's lease, the Foreman's heartbeat under and over 10 minutes, a direct
  batch's own heartbeat never a cause); on Claude Code a live lease is no cause. (No unit test
  holds the session-file cases today: they are the scenario's, below.)
- `tests/test_startup_manifest.py` stays green on the shipped `driver.md` and
  `startup-manifest.json`, read from the repository at the head under test (the 45,000-byte cap);
  `tests/test_plugin_files.py` stays green.
- The rule for the rest (spec-critic 8): every test, the dry run and the scenario that runs a
  lease-guarded command (`round`, `ship`, `handback`, `release start|go|published`, the stack
  driver's writing forms of `stack` and `forge-stack`, and an `agents set O-k` restart) on a batch
  this version opens passes `--lease` (or `--reclaim` where it restarts a unit), the number `take`,
  `order qa` or `agents set` printed. `just test` stays within its budget (AGENTS.md: at most 30 s
  above 18.5 s).
- `evals/kit/dry_run.py`: its scripted Drivers, which run `take`, `round`, `ship`, `handback` and
  the Release driver's `release`, follow that rule; `just eval-dry-run` passes.
- Scenario (`scenario/run_scenario.py`): every scripted Driver follows that rule (the World's
  `take` helper keeps the number `take` printed); in unit `parallel`, one case runs a stale lease
  (`claim lost`) and one runs a CI watch under `lease hold` past the shortened TTL
  (`CHANTIER_LEASE_TEST_TTL`) and is not expired; in `close_refusals` (unit `parallel`, case
  `close_batch`, where the Copilot close cases are today), the Copilot session-file cases are
  replaced by a Copilot batch's `close` refused while a lease is live and passing once it is not
  confirmed, and refused `not measured (no lease)` for a held agent with none. Unit `parallel`
  stays within its 260 s budget (`UNITS["parallel"]`); expiry comes from the frozen clock or the
  shortened TTL, never from a sleep longer than that TTL (spec-critic 9).
- `just check`; `just eval-dry-run` (the change is under the CLI's `src/` and the eval kit);
  `just scenario`, green on the pipeline's `just scenario (ubuntu-latest)` job, and locally on
  Windows (`chantier gate`) when this CR is the batch's top. No CI job is added or changed. No
  change under `hooks/` or `types/`.

## 8. Rollout

- A batch opened before this version keeps working with no lease and no `--lease`; on Copilot
  its `close` refuses `not measured (no lease)` while an agent is held: clear it with `agents set
  <x> - --epoch <n>` once it ended.
- The next release's notes say: Drivers, the stack driver and the QA driver hold a 10-minute lease
  renewed by their commands; a restart of a CR whose Driver reported its end does not wait; a
  lease that expired is only "not confirmed": the steering session checks with the host, then
  takes the CR with `take --reclaim`; on Copilot `close` reads leases in place of the 5-minute
  session-file rule (a Driver's leftover background work after its hand-back is no longer seen);
  `lease <unit> hold -- <command>` keeps a lease live through a long CI watch or gate.
- Mixed versions: nothing new in the journal, so nothing to read for an earlier chantier.

## 9. Self-containment notes for the Driver

- Seams: `rails.py` (`running`, `held_agents`, `check_take`), `commands/driver.py` (`take`,
  `_take_stack`, `round_`, `handback`), `declare/driver.py` (the parsers; `lease` goes here),
  `declare/delivery.py` (`ship`, `stack`), `declare/gate.py`, `declare/forge_stack.py`,
  `declare/release.py` and `commands/release.py` (`release`, `cancel`), `commands/orders.py`
  (`_qa_skeleton`, `_order_done`), `commands/orders_drop.py` (`drop`), `commands/batch_status.py`
  (`status`, `agents`), `commands/facts.py` (`handoff`), `driver_prompt.py`
  (`driver_prompt_lines`), `gate_slots.py` (`slot_of`, `holder_alive`), `gate_queue.py`
  (`read_ticket`, `ticket_cr`, `QUEUE`), `procs.py` (`alive_since`), `core/records.py`,
  `core/files.py` (`IGNORED`), `core/clock.py`, `core/errors.py` (exit 2 `EXIT_PRECONDITION`, 3
  `EXIT_CONFLICT`).
- `agents set <unit> -` ends only a live lease (spec-critic 6, "after a reported end"); a
  not-confirmed lease is ended only by `--reclaim`, `cancel` or `order drop`, so the host check
  before `--reclaim` is never skipped by a clearance.
- Portability: the hold's child with no shell; paths with forward slashes in messages; a record
  written atomically (as `gate_run.run_write`, `os.replace` with retries on Windows).

## 10. Open questions for the user

None. The six questions of the first draft and the spec critic's nine points were answered on
2026-11-20 (`02-answers.md`) and are folded above.
