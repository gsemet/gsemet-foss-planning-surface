# A ready CR sent back to its Driver can be handed back again

## Goal

In batch-09 (2026-11-10), CR-163 was handed back ready with PR 99. CR-162 (PR 100) then merged
and PR 99 had conflicts, so CR-163 went back to its Driver to rebase. The Driver rebased, passed
the gates and pushed, but `handback` refused it with "CR-163 is ready: no Driver to hand it back".
The rebase never reached the batch record as a round of work: the CR stayed `ready` the whole
time, and its only trace is an `order note` ("rebase onto main after CR-162 (PR 100) merged: PR
99 conflicts, on the user's word"), not a `take`.

The user's decisions (`02-answers.md`):

- A ready CR that goes back to its Driver (for a rebase or a fix) is reopened by `take <cr>
  --note "<why>"`. It goes back to `working` and counts no round. The Driver passes both gates
  again at the new head (a passed long gate and a `VERIFIED` verdict, since CR-171) and then
  hands back ready again.
- `handback ready` refuses when the worktree's head differs from the head `ship` recorded. The
  Driver runs `ship` again, then the gates at the new head.
- After the `take`, the steering session resumes the Driver that handed the CR back. A new
  Driver starts only when the old one does not answer.

## What already holds (read on main at 1e99343; keep it as it is)

The reopen mechanism the user chose already exists. Do not rewrite it. The scenario must prove
it end to end (see Evidence).

- `skills/chantier/scripts/cli/src/chantier/rails.py`, `check_take`: takes a `ready` or
  `blocked` CR only with `--note`. A missing note is refused with "…a Driver takes it back only
  with `--note` saying why (an answer, a change, a rebase, a red check)". The CR needs a free
  slot, because a ready CR holds none (`held`). A `working` CR is taken again (a resume) with no
  slot check.
- `skills/chantier/scripts/cli/src/chantier/commands.py`, `take`: on a `ready` or `blocked` CR
  it appends the note `back to a Driver: <note>`, sets `status` to `working` (`blocked_reason`
  cleared), and logs a `take` event with the note. It keeps `pr`, `head` and `agent` and never
  touches `round`. So a reopen counts no round.
- `handback ready` (same file) checks the two gates at the head `ship` last recorded (`c["head"]`,
  the first 7 characters of the SHA) with `gate_passed` and `last_verdict`. Gate and verdict
  events bind to a head, whatever the CR's status. So work done before the `take` (a gate or a
  verdict at the rebased head) still counts after it.
- `driver.md` ("Your means", "CR driver") already covers the rest of the Driver's side. A Driver
  handed back a ready CR turns the PR back to a draft first. A rebase is followed by `ship`, the
  long gate and CI at the new head, and a `verifier` given the move. A clean rebase starts no
  `coder` round.
- `foreman.md` already sends a ready CR back with `take <cr> --note "rebase: …"` after an
  `order merged`, and for a ready PR that stopped merging.

Three gaps remain, and this CR closes them:

1. Nothing steers the actor towards `take` when the work arrives some other way (an `order note`
   relayed as a message, a Driver resumed after its hand-back), and the CLI's refusal names no
   way out.
2. A Driver that rebases and pushes without running `ship` again is accepted on the old head's
   gate and verdict.
3. The cards say a CR taken back gets "a new CR Driver", where the user wants the Driver that
   handed it back resumed.

## What changes

### 1. CLI: `handback` on a ready or blocked CR names the `take`

`skills/chantier/scripts/cli/src/chantier/commands.py`, `handback`, the check
`if c["status"] not in LIVE` (currently line 1485).

- For a CR in `ready` or `blocked` (the two statuses `take --note` reopens), the refusal reads
  exactly:

  `<CR> is <status>: no Driver holds it until the steering session takes it back (take <CR> --note "<why>"), then hand back again`

  `<CR>` is the CR's id as stored (for example `CR-163`), not the argument as typed.
- For any other status (`queued`, `merged`, `cancelled`), the message stays as it is:
  `<cr> is <status>: no Driver to hand it back`.
- The exit code stays 2 (`EXIT_PRECONDITION`, the `ChantierError` default). Nothing is
  written to the state or the log on a refusal.

### 2. CLI: `handback ready` refuses a worktree head that `ship` did not record

`commands.py`, `handback`, the `ready` path of a CR that is not a release, right after the
check `if not c.get("pr")` (currently line 1502) and before the gate and verdict checks.

- Read the worktree's head: `_worktree(c)` (which already refuses, exit 2, when the worktree is
  missing), then `git rev-parse HEAD` in it.
- When that full SHA does not start with the recorded `c["head"]`, refuse with exit 2
  (`EXIT_PRECONDITION`), alone (not mixed with the gate and verdict lines, which would be about
  the wrong head):

  `refused: the worktree's head <short> is not the head ship recorded (<recorded>): ship <CR> <pr link> again, then the long gate and a verdict VERIFIED at the new head`

  `<short>` is the first 7 characters of the worktree's SHA, `<recorded>` is `c["head"]`, `<pr
  link>` is `c["pr"]`, `<CR>` the stored id.
- Compare by prefix, as above: `ship` stores 7 characters while `gate` and `verdict` store
  `git rev-parse --short`, so an equality test on strings of different lengths would be wrong.
- The check holds for every `handback ready` with a PR, with or without `--no-gate`, and
  whatever the CR's history. A release CR (`kind == "release"`) returns earlier and is not
  checked. `handback blocked` is not checked.
- Nothing is written to the state or the log on this refusal.

### 3. CLI: `order note` on a ready or blocked CR names the `take`

`commands.py`, `_apply_order`, branch `kind == "note"` (currently line 957). Today it returns
`noted on <cr>: the Foreman reads it in `status``. For a CR in `ready` or `blocked`, add one
line after it:

`<CR> is <status>: no Driver works on it until the Foreman takes it back (take <CR> --note "<why>")`

For a CR in another status, and for a note with no CR (`-`), the output is unchanged. The order
is recorded as today (not `applied`, since the Foreman relays it). This line is what keeps the
batch-09 path, an order note relayed straight to an ended Driver, from happening again. In
direct mode the Chief of Staff reads it as the Foreman's part, as the cards already say.

### 4. Card: `skills/chantier/references/foreman.md`

Keep each edit to the card's voice and wrap the lines at the card's width (about 100
characters), as fde3da8 did. Direct mode needs no separate edit: `chief-of-staff.md`, "Steering
a batch yourself", already tells the Chief of Staff to do what `foreman.md` says.

a. In "The user's boundaries", the bullet "**Orders are the user's word:**". Its end currently
   reads "…send a ready or blocked CR back to a Driver with `--note` saying why; its Driver turns
   the PR back to a draft". Make it say:

   - Work on a ready or blocked CR (an order note asking for a rebase or a fix, an answer, a red
     check, a dependency merged) reaches a Driver only through `take <cr> --note "<why>"`. Never
     send it as a message to the Driver that handed the CR back before that `take`.
   - The `take` reopens the CR to `working` and counts no round.
   - Its Driver runs `ship` at the new head, then passes the long gate and a `VERIFIED` verdict
     there before `handback ready`.

b. Who runs a ready CR once taken back. In "Your means", the two places that say "a new CR
   Driver" for a ready CR taken back: the `order merged <dependency>` bullet ("…`take <cr>
   --note "rebase: <dependency> merged"`, a new CR Driver…") and its **Parallel** sub-bullet
   ("…with `take <cr> --note "rebase: <merged cr> merged"` (a new CR Driver, a slot…"). Also the
   **Series** sub-bullet's `take <cr> --note "rebase: …"` and the bullet about a ready PR that
   stopped merging. For a CR taken back from `ready`, they say instead:

   - After the `take`, resume the Driver that handed the CR back (the agent id `agents set`
     recorded, still in the CR's record): send it `[foreman→driver <cr>] note taken back: <the
     take's note>` by the host's means (`SendMessage` on Claude Code, `write_agent` on Copilot),
     and record it again with `agents set <cr> <id> --epoch <n>`, so the log shows the resume.
   - It does not answer (the host refuses the message, or no `[driver <cr>→foreman]` line from it
     by the next heartbeat wake): `agents set <cr> - --epoch <n>`, then a new CR Driver as for a
     Driver that ended without its hand-back, with `take <cr> --note "resume: <the take's
     note>"` (the CR is `working`: no new slot).
   - The `take` still comes first: it is what holds the slot (or makes the CR wait for one, like
     a queued CR, when none is free).

   A CR taken back from `blocked` keeps today's rule (a new CR Driver): see the open question.

### 5. Card: `skills/chantier/references/driver.md`

a. In "Your means", the bullet "Your end:", add:

   - A hand-back refused with `<cr> is ready` or `<cr> is blocked` means the CR was not taken
     back after its earlier hand-back. Keep the commits, the gate and the verdict, which bind to
     the head. Pass the refused line, as printed, to the steering session (`[driver
     <cr>→foreman] …`, by the host's means) and wait for its `taken back:` note, then hand back
     again.
   - A hand-back refused with `the worktree's head … is not the head ship recorded`: `ship` at
     this head, then the long gate and a new `verifier` given the move, then hand back again.

b. In "Your means", the bullet on `[foreman→driver <cr>] note <text>`, add: a `note taken back:
   <why>` received after your own `handback ready` means the steering session took the CR back
   for you. The CR is yours again: `handoff <cr>` for where it stands, then go on from `<why>`
   as from a prompt's `Note:` (a `rebase:` as the "CR driver" section says). Any other note
   received after your hand-back, with no `taken back:`, is not work to start: pass it to the
   steering session as the refused line above.

c. "Your end:" says "Then end: ending frees your slot." Add that a Driver that handed back
   ready may be resumed later by a `taken back:` note.

The agent files (`agents/`, `com.github.copilot/agents/`) do not change: the contract lives in
the cards.

## Out of scope

- How `take`, `round`, `gate`, `verdict` and `ship` work today, and `handback ready`'s gate and
  verdict checks, beyond the two messages of 1 and 3 and the head check of 2.
- `STATUS.md`'s Progress steps. A reopen already shows as the note `back to a Driver: <why>` and
  in `log <cr>`; a resume shows as an `agent` event. No new step is added.
- The stack driver (`take stack`) and the Release driver: the stack driver restacks without
  taking CRs back, and a release CR's hand-back keeps its own path (no head check).
- An uncommitted worktree at `handback ready`: `ship` already reports it; this CR adds no check.
- A Driver that ended without its hand-back: the existing "handoff, then a new Driver with
  `--note "resume: …"`" rule stands.

## Evidence

### `just check`

`just check` passes on Linux, macOS and Windows (CI on the PR). `tests/test_structure.py` needs
no change unless a structure check reads one of the edited lines.

### `just scenario`

`just scenario` passes for `--forge github` and `--forge gitlab`. Every existing `handback ready`
(`World.ready` and the direct calls) stays green: where one runs after a commit with no `ship`
since, the scenario ships first, as a Driver would; no check is loosened.

Extend `scenario/run_scenario.py`, function `handback_proofs` (section "12b"), after its last
check (the `ship` accepting a bare number, around line 1946). At that point the CR is `ready`
with a gate and a `VERIFIED` verdict at its head. Add these steps, each with its own
`check(...)`:

1. `handback <cr> ready <link>` again → exit 2. The stderr contains `is ready`, `take <cr>
   --note` and `then hand back again`. The CR stays `ready` and no `handback` event is added.
2. `order note <cr> --note "rebase: main moved"` → its output contains `take <cr> --note`.
3. Record the CR's `round` and `agent`. Run `fm.take(cr, "rebase: main moved")`, or `take <cr>
   --note …` with the epoch. The CR is `working`. Its `round` and `agent` are unchanged. Its last
   note starts with `back to a Driver: rebase:`. `log <cr>` shows a `take` line with `note=rebase:
   main moved`.
4. Simulate the rebase with a new commit (the section's `commit` helper) and no `ship`.
   `handback <cr> ready <link>` → exit 2, stderr containing `is not the head ship recorded` and
   `ship <cr>`, and neither `no long gate passed` nor `no verdict VERIFIED`. The same with
   `--no-gate "<rule>"` → exit 2 with the same head line.
5. `ship` (the section's helper). `handback <cr> ready <link>` → exit 2, naming both `no long
   gate passed` and `no verdict VERIFIED` at the new head.
6. `gate <cr> <GATE>`, then `verdict <cr> VERIFIED`, then `handback <cr> ready <link>` →
   accepted. The CR is `ready` and its `round` is still the one recorded in step 3.
7. The blocked side, kept short: take the CR again with a note, `handback <cr> blocked
   question: x`, then a second `handback <cr> blocked question: y` → exit 2, with stderr
   containing `is blocked` and `take <cr> --note`.

The scenario's existing check "a ready CR goes back to a Driver only with a note saying why"
(about line 1815) stays green unchanged.

The resume of the Driver (4b, 5b) is card behaviour between agents: the scenario does not run
agents and does not prove it. The eval run below is where it is seen.

### By hand

`uv run --script skills/chantier/scripts/cli/chantier.py handback <cr> ready <link>` on a ready
CR in a scratch batch prints the new refusal; on a working CR whose worktree has a commit after
its `ship`, it prints the head refusal.

## The eval run: this PR is never merged

This CR runs in the `real` eval campaign (`evals/real/RUNBOOK.md`). It stops at an open PR.

- The PR opens as a draft. Its Driver turns it ready only once it can merge (base on the
  default branch, CI green, evidence in), as the runbook and `driver.md` say. On another base it
  stays a draft.
- The first line of its body is exactly:
  `**Eval run: do not merge.** The maintainer decides what happens to this PR.`
- Nobody merges it or enables auto-merge: not a Driver, not the Foreman, not the Chief of Staff.
  The batch stops at `ready`. What happens next is the user's word (`order merged` or `order
  drop`).

## Open questions

None. The question below was settled by the user on 2026-11-11 ("Ready seulement", in
`02-answers.md`): the resume covers a CR taken back from `ready` only, and a CR taken back from
`blocked` gets a new CR Driver, as this specification says.

1. *(settled)* **Resuming after a blocked hand-back.** The answer to Q2 is about the Driver "that handed the
   CR back", asked for a ready CR. Does the same rule (resume it, a new Driver only when it does
   not answer) also hold for a CR taken back from `blocked` (an answer, a `waits:` that landed, a
   red check)? This spec applies it to `ready` only and keeps "a new CR Driver" for `blocked`. A
   `blocked stopped` or `blocked driver ended twice` CR could not be resumed in any case.
