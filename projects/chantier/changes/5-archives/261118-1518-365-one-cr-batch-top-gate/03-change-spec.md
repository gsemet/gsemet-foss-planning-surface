# Change Specification: the batch's top runs the local gate in a batch with no stack

## Goal

In batch-25, CR-353 was the batch's last CR (no stack) and handed back `ready … --no-gate` (the
pipeline job is chantier's long gate). The project's rule asks "the CR on top of the stack" to also
pass `just scenario` locally (`chantier gate`) at its head before the user merges, but no card says
which CR is "the top" when the batch holds no stack: the ready ask went to the user, and the CR was
sent back for the gate only afterwards.

After this change, a batch with no stack has a top too: **its last open CR other than a release
CR** (a fix CR counts like any CR), or, when the last open CRs are all ready together, the last of
them in the batch's order. That CR's Driver runs the local gate before its first hand-back as the
top (no `--no-gate`); a CR that becomes the top later (another CR merged, dropped or cancelled, or
it was already handed back) gets the run before its ready ask reaches the user; a CR joining by
`order add` takes the run over when it becomes the top. A long-gate waiver (`order waive`) on the
top does not waive that run unless the waiver's words name that gate. The `ready-to-merge` ask of
the top carries the same clause as the partial-stack ask of the sibling CR
partial-stack-ask-windows-gate (`local gate <cr> at <sha7>: passed|failed|not run`), the Foreman
sends it only with `passed` (a `deliver by` time excepted), and the Chief of Staff tells the user
what it says. Every choice comes from `02-answers.md` (the user's word of 2026-11-18 and the points
settled by the Chief of Staff the same day).

Cards only: no CLI, hook, pane, `STATUS.json` or scenario change.

## Order with the sibling CR

This CR and partial-stack-ask-windows-gate (CR-359) touch the same cards (`driver.md`,
`foreman.md`, `chief-of-staff.md`). They run one after the other, never side by side (`order
after`, `02-answers.md`): this CR starts from a default branch that holds CR-359's merge. The line
numbers below are those of today's main (before CR-359); the Driver finds each place by the text
quoted. This CR reuses CR-359's terms ("the rule", "the clause") and its clause form unchanged, and
does not touch what CR-359 adds for the stack (the stack driver's invariant, the partial ask).

## Terms

- **The rule**: a project rule that asks the stack's top for a local run of the long gate (the
  wording of `driver.md`'s long-gate bullet, "A rule that also asks the stack's top for a local
  run"; in chantier, `AGENTS.md`, "Windows coverage"). With no such rule, nothing below applies and
  no ask carries the clause.
- **The batch's top** (new): in a batch whose open CRs stand in no stack on the forge (a parallel
  batch, a series, a one-CR batch, a stack batch before its stack is made), the last open CR other
  than a release CR: the one such CR not merged or cancelled when every other non-release CR of
  the batch is. A one-CR batch's CR is its top from the start. A queued CR counts as open; a fix CR
  counts like any CR; a release CR is never the top (the Release driver keeps its own procedure),
  and an open release CR does not stop another CR from being the last open one. When two or more
  non-release CRs are still open, all handed back `ready`, and no other CR of the batch is working
  or queued, the last of them in the batch's order (the order `$CHANTIER status` lists the CRs in)
  is the top from that moment. In a stack, "the stack's top" keeps its meaning (the top of the
  stack on the forge, and CR-359's mergeable top for a partial stack).
- **The clause**: `local gate <cr> at <sha7>: passed|failed|not run`, as CR-359 defines it:
  `<cr>` the batch's top (number and slug), `<sha7>` its PR's head; `passed`: the last `gate` of
  that CR at that full head passed, or a pass carried to that head (`ship`'s `carried:` line);
  `failed`: the last `gate` there failed; `not run`: neither.
- **A waiver that names the gate**: an `order waive` recorded on the top (`order waive <cr>`) whose
  words (its `--note`, the user's words) name the local run the rule asks of the top. Such a waiver
  waives that run too; any other waiver (a `--follow-up` waiver whose words do not name it) leaves
  the run owed. The words are read in `$CHANTIER status`'s order list (`O-<k> waive <cr> <note>
  follow-up <folder>`, while the order is open); when the order is no longer listed, or its note
  is cut there (40 characters), the CR's own `STATUS.json` holds them in full (`gate.waiver`).

## What changes

### 1. `skills/chantier/references/driver.md`

**The long-gate bullet (~282-284).** Today: "A rule that also asks the stack's top for a local run
is met by that CR's Driver with `$CHANTIER gate` as any long gate, and that CR hands back with no
`--no-gate`." It becomes:

"A rule that also asks the stack's top for a local run is met by that CR's Driver with
`$CHANTIER gate` as any long gate, and that CR hands back with no `--no-gate`. In a batch with no
stack on the forge, the top is the batch's last open CR other than a release CR (every other
non-release CR merged or cancelled; a fix CR counts; a one-CR batch's CR from the start), or, when
the last open non-release CRs are all handed back ready and no other CR is working or queued, the
last of them in `status`'s order: before the `ship` that precedes your ready hand-back, and so
before you take the PR out of draft (the hand-back bullet's order: `ship`, `gh pr ready`, `ship`
again, `handback`), read a plain `$CHANTIER status` (no `--refresh`, no `--epoch`); when your CR is
that top once it is handed back, run the local gate at your pushed head unless a pass or a carried
pass is already there (`ship`'s `carried:` line), in your worktree, clean, before the PR turns out
of draft, and hand back with no `--no-gate`. A `take` note that says `long gate: the batch's top
runs <command> locally` (alone, or after `rebase: <cr> merged; ` in the same note) asks the same
run at the head you push after that `take` (the rebased head). A failure there is a round, as for
any long gate. When your CR is not the top, hand back as the
project's rules say (`--no-gate "<the rule>"` for a pipeline job); if it becomes the top later, the
steering session sends it back for the run. A Release driver is never the top and runs no local
gate for this rule."

**The waiver sentence of the hand-back bullet (~529-531).** Today: "a CR whose `take` or `handoff`
prints `gate: waived (O-<k>, …)` runs no long gate and hands back with no `--no-gate`: the CLI reads
the recorded waiver and prints `long gate waived (O-<k>): validated by CR-<top>'s gate` (or
`follow-up <folder>`) in the line to send;". Add right after it:

"under a rule that asks the top for a local run, a waived CR that is the top (the stack's top, or
the batch's top as the long-gate bullet says) still runs `$CHANTIER gate` at its pushed head before
it takes its PR out of draft for its ready hand-back, unless the waiver's words name that gate: read them in `$CHANTIER status`'s
order list (`O-<k> waive <cr> <note>`), or, when the order is no longer listed or its note is cut,
in your CR's `STATUS.json` (`gate.waiver`); it still hands back with no `--no-gate`;"

No change to the stack driver's section (CR-359 owns it) or to the Release driver's.

### 2. `skills/chantier/references/foreman.md`

**"The user's boundaries", the `--no-gate` check (~98-101).** Today: "When the rules also ask a
local run on the stack's top, the stack's top handed back with `--no-gate` goes back with `take
<cr> --note "long gate: the stack's top runs <command> locally"`, with no ask; the Copilot host's
path is unproved." Add after it:

"In a batch with no stack on the forge, the top is the batch's last open CR other than a release CR
(every other non-release CR merged or cancelled; a fix CR counts; a one-CR batch's CR from the
start), or, when the last open non-release CRs are all handed back ready and no other CR is working
or queued, the last of them in `status`'s order; the same holds for it, checked at two moments:
- at each ready hand-back: read a plain `$CHANTIER status`; when the top, as that hand-back leaves
  the batch, handed back with `--no-gate`, or the record holds no passed or carried long gate at
  its head (`log <cr>`), it goes back with `take <cr> --note "long gate: the batch's top runs
  <command> locally"`, with no ask (the top may be a CR handed back earlier: the last in `status`'s
  order of ready CRs that all wait together);
- when it becomes the top later: on each merge, drop or cancel you record or receive (`order
  merged`, `order drop`, `cancel`) that leaves one non-release CR open, or leaves only ready
  non-release CRs open with none working or queued, read a plain `$CHANTIER status`; the top handed
  back `ready` with no passed or carried long gate at its head goes back with the gate note. After
  a merge, the rebase `take` that the `order merged` bullet sends it (parallel or series) carries
  the gate note in the same `take`, never a second one: `take <cr> --note "rebase: <merged cr>
  merged; long gate: the batch's top runs <command> locally"`; its Driver rebases, and its
  hand-back check (the long-gate bullet of `driver.md`) runs the gate at the rebased head. After a
  drop or a cancel (no rebase take), it goes back with `take <cr> --note "long gate: the batch's
  top runs <command> locally"` (its Driver turns the PR back to draft first, as for any CR sent
  back). A `working` CR needs nothing (it gets the rebase `note` line as today), its Driver checks
  at its hand-back; a `blocked` or queued one is checked at its ready hand-back. A CR added by
  `order add` is open: the top moves to it when it is the top by the definition, and the earlier
  top's pass stays valid but no longer counts as the top's.
The Copilot host's path is unproved (as for the stack's top above).
A fix CR you merge under the grant is merged as the top only with a passed or carried long gate at
its head. The top's `ready-to-merge` ask (or `pr-in-draft` ask) carries the clause after its gaps:
`ready-to-merge <cr> <link>[ gaps: …] local gate <cr> at <sha7>: passed`, and goes only with
`passed`. At a `deliver by <time>` time (the order note, in any mode), a top not yet passed is not
sent back: its ask goes as it stands, with `local gate <cr> at <sha7>: not run` (or `failed`), after
`no long gate: <reason>` when it has one; a gate still running is not stopped. With no such rule,
no clause."

**The waiver check (~105-112).** Today it ends: "A hand-back that says it with no such order on the
CR goes back to its Driver with `take <cr> --note "long gate: no waiver recorded for this CR"`,
with no ask." Add after it:

"Under a rule that asks the top for a local run, a waiver does not waive the top's local run unless
its words name that gate: read them in `status`'s order list (`O-<k> waive <cr> <note>`), or, when
the order is no longer listed or its note is cut, in the CR's `STATUS.json` (`gate.waiver`). A
waived top (the stack's top, or the batch's top as above) whose record holds no passed or carried
long gate at its head (`log <cr>`; `status` shows the CR `waived`, not its pass) goes back with
`take <cr> --note "long gate: the batch's top runs <command> locally"` (`the stack's top` for a
stack), with no ask, at the same two moments; its ask then carries both `long gate waived: …` and
the clause. A top whose waiver names the gate owes no local run and its ask carries no clause."

Also in `foreman.md`:

- **The asks list** (~403): `ready-to-merge <cr> <link> [gaps: …]` becomes `ready-to-merge <cr>
  <link> [gaps: …][ local gate <cr> at <sha7>: passed|failed|not run]`, and the same optional tail
  on `pr-in-draft <cr> <link> on <base>: waits for <what> [gaps: …]`. The `stack-ready-to-merge`
  form is CR-359's, unchanged here.
- **The `order merged` bullet** (~416-434, "On an `order merged <dependency>`"): in its
  **Parallel** and **Series** sub-bullets, add: "When the CR this rebase `take` goes to is now the
  batch's top (as 'The user's boundaries' says) and holds no passed or carried long gate at its
  head, the same `take` carries the gate note: `take <cr> --note "rebase: <merged cr> merged; long
  gate: the batch's top runs <command> locally"`; no separate gate `take`."
- **"Deliver by a time"** (~300-307): it stays under the stack batch's bullets; add one sentence at
  its end: "In a batch with no stack, the same order note sends the batch's top's ask as it stands
  at the time, with its local-gate clause (`not run` or `failed` included), as 'The user's
  boundaries' says."
- No change to the supersede rule (~410-413): a later `ready-to-merge` ask of the same CR still
  supersedes the earlier unread one.

Every `take` form above is `take <cr> --note "…"`, as at `foreman.md:100` (no `--epoch`).

### 3. `skills/chantier/references/chief-of-staff.md`

- **The plain `ready-to-merge` bullet** (~1021-1038, "A plain `ready-to-merge <cr> <link> gaps: …`
  ask"): add, after the gaps sentence: "In a project whose rules ask the stack's top for a local
  run, the ask of a batch's top with no stack carries `local gate <cr> at <sha7>: …`: quote it in
  the user's language before you say the PR can be merged. `passed`: say the local gate ran and
  passed at that head. `not run` or `failed` (a `deliver by` time): say the project's rule asks
  that gate at that head before the merge and it has not passed there; merging anyway is the
  user's choice, recorded as any merge (`order merged`), never questioned or refused." The same
  wording as CR-359's partial-stack sentence in "A stack batch".
  Then, before "In every mode, a `ready-to-merge` ask is offered to the user as mergeable now, on
  its own", make that sentence's exception explicit: "Under that rule, once the last open
  non-release CRs are all ready together and the last of them in `status`'s order is the batch's
  top, offer the others as mergeable only together with that top or before it, and say so."
- **Recording several merges** (the merge-recording sentences, ~1037-1046, "When the user merges a
  PR before its `ready-to-merge` line"): add: "When the user merges several PRs of a batch with no
  stack in one action (or several `forge saw merged` lines come at one `status` or one watcher's
  end), record `order merged` for the others first and the batch's top last."
- **The gates forecast** (~870-874, "**The gates:**"): after "nor does a CR covered by a waiver
  (`order waive`); under a stack waiver the stack's top counts, once." add: "Under a rule that asks
  the top for a local run, the batch's top (or the stack's top) counts, once, whatever its
  exemption or waiver, unless a waiver's words name that gate."
- **Direct mode**: no new text; the Chief of Staff steering a direct batch applies the Foreman's
  bullets of section 2 itself, as for every other Foreman bullet.

### 4. `skills/chantier/references/concepts.md`

- No change: the batch's top is defined in the cards that use it (`driver.md`, `foreman.md`), as
  "the stack's top" is today.

### 5. Agent files and docs

- `agents/` and `com.github.copilot/agents/`: unchanged (the contract lives in the cards).
- `README.md`, `CONTRIBUTING.md`, `docs/`: change only a line that quotes the `ready-to-merge` ask
  form in full, if one does (the Driver greps for `ready-to-merge <cr>` outside `scenario/` and the
  CLI's source).
- `AGENTS.md`: unchanged (its "the CR on top of the stack" reads, after this change, through the
  cards' definition of the top).

## Out of scope

- The CLI: `handback`, `asks`, `status`, `gate`, `order waive` and the pane stay as they are; the
  CLI learns no "top". `status`'s "Long gate" column keeps `exempt: <rule>` for a CR handed back
  with `--no-gate` and `waived …` for a waived CR (the top's local pass is read in `log <cr>`). The
  CLI already accepts a waived CR's hand-back with a gate pass and no `--no-gate`
  (`driver_checks.py`, `handback_refusals`).
- The stack (CR-359): the stack driver's invariant, the partial `stack-ready-to-merge` ask, the
  complete stack's ask.
- The release CR and the Release driver's procedure: unchanged.
- Any Windows-specific wording in the cards: the rule is the project's, read generically.

## Evidence

- `just check` passes (Linux, macOS and Windows, by `AGENTS.md`).
- The pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (the cards change).
- Windows coverage: when this CR is its batch's top (the top of the stack, or the batch's top by
  the new definition), its Driver runs `just scenario` locally with `$CHANTIER gate` at its head (no
  `--no-gate`), per `AGENTS.md`.
- No `just eval-dry-run` (no change under the CLI's `src/` or `evals/kit/`), no `just mod` (no
  change to `hooks/` or `types/`), no pane screenshot (nothing the pane draws changes). No host and
  default matrix: the change depends on the project's rule, not on the host or a shipped default.
- The Driver's review reads the three cards together: the top's definition is the same, word for
  word, in `driver.md`'s long-gate bullet and `foreman.md`'s boundaries bullet ("last open CR other
  than a release CR", a fix CR counting, the all-ready case by `status`'s order); the waiver
  exception is in `driver.md`'s waiver sentence and `foreman.md`'s waiver check, both reading the
  words from `status`'s order list then `STATUS.json`; the clause's form is CR-359's, word for
  word, in `foreman.md`'s boundaries bullet and asks list and in `chief-of-staff.md`; the Foreman's
  check is wired at both moments (each ready hand-back, and a merge, drop or cancel that leaves one
  non-release CR open or only ready ones), and after a merge the gate note rides in the rebase
  `take`, never a second `take`; the Driver reads `status` before the `ship` that precedes its
  ready hand-back; the Chief of Staff records the batch's top last among merges of one action;
  every `take` form is `take <cr> --note "…"`; the gates forecast counts the top once; the `order
  add` case moves the top; the new `foreman.md` bullet says the Copilot host's path is unproved.
- Known gap (the PR names it, so the ready line quotes it): the Copilot host's path is unproved
  (the Foreman's top check, as for the stack's top today); no Copilot batch has run it.
- Known gap (the PR names it, so the ready line quotes it): the behaviour is unproved until a real
  batch with no stack ends under the rule; trial: the top's Driver runs `gate` before its hand-back
  (a `gate` event of that CR at its head before the `handback ready` event in `events.jsonl`), and
  its `ready-to-merge` ask carries `local gate <cr> at <sha7>: passed`; and one batch where the top
  changes after a merge: the Foreman's `take <cr> --note "long gate: the batch's top runs …"` comes
  before any ask of that CR's new head.

## Open questions

None: the three questions of the first run and the spec critic's finding 3 were settled by the
Chief of Staff on 2026-11-18 (`02-answers.md`).
