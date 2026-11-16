# Change Specification: a refused force push is recorded with its exact text, and its Driver hands back instead of waiting

## Goal

Two lessons of batch-17's refused force pushes (2026-11-13), the ones `02-answers.md` keeps
(PR-Q1, A):

1. **The refusal is recorded exactly.** When the host refuses a Driver's force push, the CR's
   record holds the exact command the Driver ran and the host's exact text, so the cause (a
   missing allow rule, or the classifier on a matching rule) can be proved afterwards. In
   batch-17, CR-236's note said only "Force push refused by host".
2. **A Driver does not spend its context waiting for the push.** Once it sends the push line, the
   Driver hands back `blocked waits:` with the push and its next steps in the record, and ends;
   the steering session restarts a fresh Driver on the CR once the Chief of Staff's answer comes
   back. In batch-17, CR-236's Driver ran out of context (about 71,000 tokens) while it waited,
   and its replacement had to read everything again.

Causes 1 (P10's warn, CR-238) and 4 (the Chief of Staff pushes with no ask once its checks
pass, as its card says) are settled elsewhere and are not in this CR.

## Decisions carried (from `02-answers.md` and `intake/request.md`)

| # | Decision | Where |
| --- | --- | --- |
| D1 | This CR covers only cause 2 (the exact command and text recorded) and cause 3 (the Driver hands back and is restarted) | all areas |
| D2 | The Driver records the refusal with the exact command and the host's exact text (concepts rule 7) | Area 1 |
| D3 | A Driver that sends the push line hands back `blocked` with the push line and its next steps in the record, and is restarted by the steering session once `pushed` comes back, instead of waiting in its turn | Area 2, Area 3 |
| D4 (default) | The hand-back reason is the existing `waits:`: a thing on its way that nobody has to decide (amber, never counted for escalation, the CLI already accepts it). No new reason, no CLI change | Area 2 |
| D5 (default) | Every answer, not only `pushed`, brings the CR back to a fresh Driver, which acts on it as the waiting Driver did before | Area 3 |
| D6 (default) | The Chief of Staff's report line for a push it ran quotes the Driver's recorded refusal, or says none was recorded | Area 4 |

## What changes

Cards only. No CLI change (`handback <cr> blocked waits: …` is accepted and drawn today:
`driver_checks.py` `handback_blocked`, `status/words.py`), no new message in `routing.md` (one
row's parenthesis changes), no agent file change.

### Area 1: `driver.md`, "A force push the host refuses" (line ~329): record the refusal

Before anything else, the Driver records the refusal in one note:
`$CHANTIER note <cr> "refused: <the exact command> -> <the host's exact text>"`: the command as
it ran (its `git -C <path>` form included, flags and refspec as typed), and the host's whole
text as it came (with the classifier's label, such as "Git Destructive", when the host gives
one). Never a summary such as "refused by host". This is the note the Foreman's card already
names (`foreman.md` line ~376); the card says it is the Driver's, written before the push line.

`foreman.md` line ~375-376 ("Record each refusal with `$CHANTIER note …`") is made precise: the
Driver records its own refused push; the Chief of Staff records its own (its step 6, unchanged);
the Foreman records a refusal it meets itself. Whoever sees a refusal records it, once.

`hosts/claude-code.md` line ~331 (Auto mode) gets one clause: the Driver records the refused
command and text before it sends the push line (`driver.md`), so a refusal on a command an allow
rule matches is told apart from one with no rule.

### Area 2: `driver.md`, same bullet: hand back instead of waiting

The bullet today says: send the push line, "then wait: no other push, no other way", and act on
the result (`ship` and go on, look at a failed lease, hand back on `push refused`). It becomes,
for a CR Driver and the Release driver (both hand back with `handback <cr>`):

1. With the work committed: the refusal's note (Area 1); then one note with what is next,
   `$CHANTIER note <cr> "next after push: <the steps left, in order>"` (for instance: `ship`, the
   long gate is already passed at `<sha7>`, read CI, the verifier given the move, turn the PR
   ready, hand back ready), so the fresh Driver starts from it without reading the whole record
   again.
2. `$CHANTIER handback <cr> blocked waits: push <branch> <expected remote sha> <local sha>`, and
   send the line it prints.
3. Send `[driver <cr>→foreman] push <branch> <expected remote sha> <local sha>` (unchanged).
4. End. No other push, no other way, and no wait in the turn.

The rest of the bullet moves to the fresh Driver: it reads the answer in its `take` note (Area 3)
and acts on it as the waiting Driver did: `pushed` → `ship` and go on from the "next after push"
note; `push failed` → look at why (`git fetch`, what the remote gained), never the same push
again; `push refused <branch>: no long gate passed at <sha>` → run the long gate and send the
push line again, handing back `waits:` again as above; any other `push refused` →
`handback blocked refused <exact text>` at once, which goes to the user as today.

The sentence "While the steering session asks the user (a push it judges not right), you keep
waiting" is removed: the CR waits, not the Driver.

The stack driver keeps today's rule (it sends the push line and waits): see Out of scope.

### Area 3: `foreman.md`, the push bullet (line ~367): restart on the answer

The Foreman still passes the push line as it came to the Chief of Staff, not through `asks`, and
pushes nothing itself. What changes is what it does with the answer:

- The answer (`pushed <branch>`, `push failed <branch> <text>`, `push refused <branch>: <text>`)
  no longer goes to a live Driver as a `note push …`. When the CR is `blocked` with
  `waits: push <branch> …`, the Foreman takes it back at once with the restart path's steps (the
  id cleared first) and
  `take <cr> --note "push: <the Chief of Staff's answer, as it came>"`, then a new CR Driver (or
  Release driver), before any queued CR: a blocked CR holds no slot, so it takes the next free one,
  as for a `context:` hand-back. No round is counted.
- An answer that comes before the hand-back has landed (the CR still `working`): wait for the
  hand-back, then take it back as above. A Driver that ended without its hand-back takes the
  lost-Driver path, with the answer in its `resume:` note.
- A Driver of a CR handed back `waits: push` is never pinged, and the CR is not a lost Driver
  (it is `blocked`, not `working`).
- The `blocked waits:` bullet (line ~266) needs no change; this is one case of it.

In direct mode the Chief of Staff is the steering session and does the same (its card's direct
mode, line ~1280: "the Driver hears the result as a note" becomes "the CR goes back to a fresh
Driver with the result as its `take` note", as `foreman.md` says).

`routing.md`: row 12's parenthesis "(the Driver then ends with `handback blocked refused <exact
text>`)" becomes "(the CR's fresh Driver then hands back `blocked refused <exact text>`)"; row 15's
"`note <text>` (the push result too)" drops "(the push result too)". Row 16 is unchanged.

`chief-of-staff.md`, "A refused force push": step 4's "The Driver keeps waiting" becomes "The CR
keeps waiting (its Driver has handed back)". No other change there: the judgement still reads the
local head, the gate and the `handoff` notes, which the hand-back leaves in place.

### Area 4: `status-layout.md`, Notes (line ~91): the report quotes the refusal

The line "pushed for the Driver (host refused its push)" gains the Driver's recorded refusal, as
`handoff <cr>` prints it: `pushed for the Driver (host refused: <the exact command> -> <the
host's exact text>)`, or `pushed for the Driver (no refusal recorded)` when the Driver left no
`refused:` note. The second form makes a missed record visible to the user at the next report.

## Out of scope

- Causes 1 and 4 of the request (CR-238, and the Chief of Staff's card, which already says it
  pushes with no ask).
- The stack driver: its restack pushes several branches in one take, and a hand-back halfway
  through a restack is another shape; it keeps sending the push line and waiting.
- Any CLI change: no check that a `refused:` note exists before a `waits: push` hand-back, no new
  hand-back reason (a new CLI rule comes only from measured cost).
- Rule 7 for refusals other than a force push: unchanged (they already end in
  `handback blocked refused <exact text>`).
- The permission rules and the Chief of Staff's judgement and push command: unchanged.

## Evidence

- `just check` passes (Linux, macOS, Windows).
- Read-through proofs, by the Verifier, at the PR's head with `git grep -n` over
  `skills/chantier/references/`:
  - `driver.md` holds the refusal note with "the exact command" and "the host's exact text", the
    "next after push" note, `handback <cr> blocked waits: push <branch> <expected remote sha>
    <local sha>`, the end with no wait, and the four answers as read from the `take` note;
    `git grep -n "keep waiting\|then wait"` near the push bullet finds no Driver waiting for a push
    (the stack driver's rule excepted, and named as such).
  - `foreman.md` restarts the CR on each answer, before any queued CR, with
    `take <cr> --note "push: …"`, and handles an answer that comes before the hand-back.
  - `routing.md` rows 12 and 15, `chief-of-staff.md` step 4 and the direct-mode line,
    `status-layout.md` line ~91 and `hosts/claude-code.md` line ~331 carry Areas 1 to 4, and no
    card still says the Driver hears the push result as a live note.
- A CLI proof that the shape the cards name is accepted: in a scratch batch (the scenario's
  helpers, or `just scenario`'s workspace), `handback <cr> blocked waits: push chantier/b/cr-1-x
  aaaaaaa bbbbbbb` exits 0, prints `<cr> waits; the Foreman takes it back when that lands`, and
  `status` shows the CR blocked with the `waits` word; `take <cr> --note "push: pushed
  chantier/b/cr-1-x"` then exits 0 with no round counted.
- `just scenario` passes (AGENTS.md asks it of a change to the cards; the scenario's Driver pushes
  itself and does not run the refused-push route, so no scenario step changes).

## Open points

1. **Scope: the stack driver.** It is left waiting (Out of scope), because a hand-back halfway
   through a restack is another shape. Its restack is where most force pushes come from, so it is
   where the context risk is largest. Recommended: keep it out of this CR, and file it as an inbox
   item if a stack batch shows the same loss.
