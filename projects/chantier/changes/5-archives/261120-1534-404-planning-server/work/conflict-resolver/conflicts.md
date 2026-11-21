# Conflicts: CR-404 rebased on dc80a81b (only commit d69752e6 conflicted)

- AGENTS.md: main's text kept (Third lease, Fourth, Fifth wait, no count); the writer added as "Sixth", and the git-exceptions bullet is the writer's, with no count ("named git exceptions").
- docs/planning-folder.md: type and source rows and the "written today" sentence carry both `wait-cleared@1` and `sync-*@1`/`writer`.
- scenario/run_scenario.py: surface-board budget 700, cases list has `typed_waits` and `surface_writer`.
- commands/batch_status.py: imports only `wait_view` (autosync lines/reading are gone with CR-404's removal of `_autosync_lines`); `journal.lines(..., wait_view.open_keys(d))` then the writer lines.
- hub/journal.py: docstring lists all types; `lines` keeps main's `cleared`, `writer_lines` added after it.
- hub/schemas.py: `WaitCleared1` and the Sync* models/texts both kept.
- hub/schemas.json: union of both sides' entries, sorted keys, as `just journal-schemas` writes.

Fast gate: not run by the resolver (the Driver runs `just check`); only an import check of batch_status and hub.schemas, which passed.
