# Intent: context limits of the Drivers

Filed 2026-11-25 from the owner's words in chat (`intake/request.md`). Grilled the same day (`02-answers.md`, Answers 1 to 6), which narrows the request.

## Why

The Drivers hand back `blocked context` too early, and the limits that decide it cannot be seen or set in one place. The owner wants 200,000 and settings they can read and check for coherence.

## Asked

- The Drivers hand back at 200,000 tokens, with their agents' context window raised above it, measured first.
- The thresholds are set in the project's `chantier.yaml` and on the board's Configuration page, Limits tab.
- A command lists the context limits, each with its value and source.
- Incoherent settings warn without blocking.

## Out of scope

The limits that are not about context (rounds, slots, budget, lease, heartbeat, watcher wake, `specifying.parallel`), and the model's real window.

## Where it goes

The running batch batch-31, after `shortcut-commands`.
