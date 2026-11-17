# Two chantier sessions on one machine

The user runs two Chief of Staff sessions at once on the same PC, over the same planning surface
(2026-11-17: chantier's batch-23 with a Foreman, and markdown-okf-schema-studio's batch-05). They
step on each other:

- each session may start its own board on the surface, on the same port 8765; an older board
  went on serving and showed chantier as "no batch, 18 inbox" while batch-23 ran;
- both commit by hand in the same surface checkout: `git pull --rebase --autostash` carries the
  other's unstaged work around, and a broad `git add` took the other's files;
- both batches run Drivers, gates and uv processes on one machine (CPU, memory; on Windows a
  running chantier process locks files, os error 32 on `uv sync`);
- two Foremen, two heartbeats, two bills, and neither session knows what the other runs.

The goal: make two (or more) sessions on one machine work well together, and include the fix in
the running batch-23.
