# The steering session reads `status` before a rebase note, and takes a ready CR instead of messaging it

## The problem

In real-direct run 1 (2026-11-12, PR 137) the steering session sent a `rebase:` note as a message
to CR-101's Driver, believing the CR was `working`. The Driver had just handed it back ready. By
its card the Driver could not start work on a note with no `taken back:`, so it passed the note
back and waited for a formal take-back: one exchange lost, and a rebase delayed.

## Where it shows

- `skills/chantier/references/foreman.md` already has both paths: a `ready` or `blocked` CR goes
  back to a Driver only through `take <cr> --note "<why>"`, then the Driver is resumed with
  `note taken back: <the take's note>`; a `working` CR gets the message `[foreman→driver <cr>]
  note rebase: …`. What is missing is the moment of the choice: nothing says to read the CR's
  state just before sending, so the session acts on a state it read at its last wake.
- `skills/chantier/references/chief-of-staff.md`, "Steering a batch yourself": direct mode
  follows the Foreman's card for the Drivers, so the same gap is there.
- `skills/chantier/references/driver.md` handles the late note correctly (it passes it up and
  waits); that is the safety net, and it is what cost the exchange.

## What would fix it

In the steering card (foreman.md, which direct mode follows):

- Just before sending a note that carries work to a Driver (a `rebase:` first of all), read
  `$CHANTIER status` and choose the path from the state it shows now.
- `ready` (or `blocked`): no message; `take <cr> --note "<the note>"` and the take-back path the
  card already gives. `working`: the message, as today.

## Out of scope

- The Driver's rule for a note received after its hand-back: unchanged, it stays the net for the
  rare case where the hand-back lands between the `status` and the message.
- Any CLI change (no command that sends or refuses a note: messaging is the host's).
- The order in which CRs are rebased after a merge, and the stack driver's restack.
- The agent files of both hosts.
