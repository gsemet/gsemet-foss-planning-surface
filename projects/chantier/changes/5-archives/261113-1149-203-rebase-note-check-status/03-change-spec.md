# The steering session reads `status` before a note that carries work, and takes a ready CR instead of messaging it

## Goal

When the steering session (a Foreman, or the Chief of Staff in direct mode) is about to send a
Driver a note that carries work, a `rebase:` note first of all, it reads the CR's state just
before, with a plain `$CHANTIER status`, and chooses the path from what that read shows now, not
from the state it read at its last wake. A CR found `ready` or `blocked` gets no message: it is
taken back with `take <cr> --note "<the note>"` and the take-back path the Foreman's card already
gives. A CR found `working` gets the message, as today.

This closes the race seen in real-direct run 1 (2026-11-12, PR 137, finding 8 of
`evals/results/real-direct-2026-11-12-run1.md`): after PR #4 merged, the Chief of Staff sent
CR-101's Driver a plain `note rebase:` just after that Driver had handed back ready. The Driver,
by its card, refused to start work on a note with no `taken back:` and asked for a `take`: one
exchange lost and a rebase delayed.

## Decisions carried from `02-answers.md`

1. **Scope of the rule:** every note that carries work to a Driver (a `rebase:` note, an order
   note, an answer), with the `rebase:` note named as the first case. One sentence covers all of
   them.
2. **The read:** a plain `$CHANTIER status`, with no `--refresh` and no `--epoch`. It moves
   nothing and is not a wake: it must not count as a heartbeat.
3. **Both steerings:** the rule holds for the Foreman and for the Chief of Staff in direct mode.
   It is written once, in the Foreman's card, and direct mode visibly inherits it (a line in
   `chief-of-staff.md`, "Steering a batch yourself").
4. **The path for a CR found `ready`:** the whole take-back path as the Foreman's card has it
   (note the Driver's agent id, `agents set <cr> - --epoch <n>`, `take <cr> --note "<the note>"
   --epoch <n>`, the Driver resumed with `[foreman→driver <cr>] note taken back: <the take's
   note>`, `agents set <cr> <id> --epoch <n>` again; a Driver that does not answer goes by the
   existing "does not answer" step). No second, shorter path for a rebase. A CR found `blocked`
   keeps the existing path too (`take <cr> --note`, a new CR Driver).
5. **The Driver's side is unchanged:** a note with no `taken back:` received after its hand-back
   is still passed up and waited on (`driver.md`, the `[foreman→driver <cr>] note <text>` bullet).
   That stays the net for a hand-back that lands between the `status` and the message.
6. **No CLI change:** no command that sends a note or refuses one on a ready CR. Messaging is the
   host's and the CLI knows no role.
7. **The remaining window is accepted:** a hand-back between the read and the message is seconds
   wide, costs one exchange when it happens, and loses no work.

## What changes

Cards only, both in `skills/chantier/references/`. Both hosts read the same cards, so no
host-specific text is needed. Keep the cards' style: plain English, lines wrapped near 100
characters, CLI commands in backticks.

### `skills/chantier/references/foreman.md`

1. **"Orders are the user's word" bullet** (section "Your rules", the bullet that ends "...before
   `handback ready`", around lines 56-66). It already says that work on a ready or blocked CR
   reaches a Driver only through `take <cr> --note "<why>"`, never as a message. Add the moment of
   the choice, in substance:

   > Just before you send a Driver a note that carries work (a `rebase:` first of all, an order
   > note, an answer), read the CR's state with a plain `$CHANTIER status` (no `--refresh`, no
   > `--epoch`: it is a check before an action, not a wake, and records no heartbeat), and choose
   > the path from the state it shows now, never from the one read at your last wake: `ready` or
   > `blocked`, no message, `take <cr> --note "<the note>"` and the take-back path below;
   > `working`, the `[foreman→driver <cr>] note <text>` message. A hand-back that lands between
   > that read and the message is caught by the Driver, who passes the note back: then take the
   > CR back as for `ready`.

   The last sentence states the accepted window and what the steering session does when the
   Driver passes a note back (the take-back path); it adds no new path.

2. **The `order merged` bullet, "Parallel" and "Series" sub-bullets** (around lines 143-153).
   Where they choose between `take <cr> --note "rebase: …"` for a `ready` or `blocked` CR and the
   `note rebase:` message for a `working` one, make the state the one the `status` read just
   before sending shows, by a short back-reference to the rule above (for instance "the state
   from the `status` read just before sending, as above"). Do not restate the rule.

3. **"A CR taken back from `ready`" bullet** (around lines 155-169). Its first step already reads
   `status` for the Driver's agent id. Say that this may be the same read as the one before the
   note, so the session does not run `status` twice. No other change to the path.

4. **"Your means", the `$CHANTIER status` bullet and the `--epoch` list** (around lines 77-81 and
   238-242): no change. A plain `status` already carries no `--epoch`; check that nothing added
   above contradicts the list of commands that carry it.

### `skills/chantier/references/chief-of-staff.md`

Section "Steering a batch yourself", next to the "A dependent draft PR" bullet (around lines
546-547), add one bullet that makes the inheritance visible, in substance:

> **A note that carries work to a Driver.** The Foreman's rule applies to you: just before you
> send one (a `rebase:` first of all), read a plain `$CHANTIER status` and choose from the state
> it shows now: `ready` or `blocked`, `take <cr> --note` and the take-back path; `working`, the
> message.

No other text in this file changes; the rule itself lives only in `foreman.md`.

## Out of scope

- `skills/chantier/references/driver.md`: the Driver's rule for a note received after its
  hand-back is unchanged (decision 5).
- Any CLI change (`skills/chantier/scripts/cli/`, `rails.py`): decision 6.
- The order in which CRs are rebased after a merge, and the stack driver's restack (the "Stack"
  sub-bullet stays "unchanged: the stack driver restacks").
- The agent files of both hosts (`agents/`, `com.github.copilot/agents/`): untouched.
- `routing.md`, the host references, the scenario's script and the eval kit: untouched.
- No new path for a rebase on a ready CR (decision 4).

## Evidence

Run in the CR's worktree, at the pushed head:

1. `just check`: passes (structure tests and the release-notes check), as `AGENTS.md` requires.
2. `just scenario`: passes on both forges (a change to the cards needs it before its PR, per
   `AGENTS.md`). The scenario runs the CLI with no model, so it proves the change breaks nothing;
   it does not exercise the new sentence.
3. The text itself, shown with its output in the PR:
   - `git diff --stat origin/main...HEAD` lists only `skills/chantier/references/foreman.md` and
     `skills/chantier/references/chief-of-staff.md` (plus the CR's archive files if `take` asks
     for them).
   - A search in `foreman.md` for the new rule (for instance `rg -n "plain .\$CHANTIER status"
     skills/chantier/references/foreman.md`) shows the sentence in the "Orders are the user's
     word" bullet, and the back-references in the Parallel and Series sub-bullets.
   - A search in `chief-of-staff.md` shows the new bullet under "Steering a batch yourself".
   - A search that the new text adds no `--epoch` or `--refresh` to the read (the `--epoch`
     command lists in `foreman.md` and `chief-of-staff.md` are unchanged in the diff).
4. A reading check by the Verifier against this specification: each of the seven decisions above
   is carried in the cards' text, and no other behaviour changed.

## Open questions

None.
