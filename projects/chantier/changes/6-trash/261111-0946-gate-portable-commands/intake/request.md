# `gate` runs several commands the same way on every OS

Batch-09 retro, 2026-11-11 (`4-batch/retro.md`, point 10). The user: the fix must work "quand
chantier sera déployé dans n importe quel type de projet".

## What happened

`gate <cr> "just check; just scenario"` failed on Windows: `gate` runs its command with
`shell=True` (`commands.py`, about line 1654), which is cmd.exe there, and cmd.exe has no `;`.
The Driver lost a round and tokens to find out.

## Proposed fix (to grill)

`gate` takes each command as its own argument (`gate CR-x "just check" "just scenario"`) and
runs them in order, stopping at the first failure, each logged with its result and the head. No
shell syntax to join them, on any OS.
