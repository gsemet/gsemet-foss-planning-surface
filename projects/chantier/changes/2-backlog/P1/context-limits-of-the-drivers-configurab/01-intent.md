# Intent: context limits of the Drivers

Filed 2026-11-25 from the owner's words in chat (`intake/request.md`). Grilled the same day (`02-answers.md`, Answers 1 to 6). Answer 10 (2026-11-27) changes what is asked.

## Why

The Drivers hand back `blocked context` long before the host would compact them. The owner wants them to compact themselves, to keep one limit only as a safety net for a missing or badly configured autocompact, and to read and set both.

## Asked

- The Drivers compact themselves. A setting places the autocompact around 400,000 tokens by default, configurable by the user, as far as the host allows it.
- A maximum context ends a Driver that passes it, 500,000 tokens by default, configurable by the user, and said to be for a missing or badly configured autocompact.
- The settings are in the project's `chantier.yaml` and on the board's Configuration page, Limits tab.
- A command lists the context limits, each with its value and source.
- Incoherent settings warn without blocking.

## Out of scope

The limits that are not about context (rounds, slots, budget, lease, heartbeat, watcher wake, `specifying.parallel`), and the model's real window.

## Where it goes

The backlog, P1.
