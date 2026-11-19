# bug: chantier open crashed on a scratch repo during the v0.14.0 release demo

Seen 2026-11-19 by CR-388's release Driver (Foreman's ask A-43): a scratch demo of `open` (a batch
with no CR, factory mode) crashed in the CLI on a scratch repository, so the factory highlight of
the v0.14.0 notes has no capture. Not investigated: the traceback and the scratch setup are in
CR-388's `work/` folder, if the Driver kept them.

Change: reproduce on a fresh scratch repository, find the cause, fix it, and cover it with a test.
