# Conflicts, round 2: rebase onto origin/main 75a73d59 (CR-410)

Commit 1 (writer) conflicted; commit 2 applied clean. New head 587f5d0f (+ one uncommitted lint fix, below).

- AGENTS.md: "Four named"/"Three named" -> "Named exceptions" (no count; the First..Fourth list kept). Watcher
  paragraph: main's poller text kept, "the writer's" added to the journal's writers, "the server runs no git but its
  writer's" (the CR's, replaces the autosync join). Git-exceptions bullet: the writer's, with "named git exceptions"
  (no count), main's autosync-join text dropped (the writer replaces it, as in the CR). Left as main had them:
  "one named exception" (cost code, PRs page): they are counts too; say if they must go.
- CONTRIBUTING.md: main's poller text plus the writer's; "runs no git but its writer's".
- docs/planning-folder.md: type list has issue@1 and sync-*@1; sources: hub, board, writer, cli, poller; table
  rows of both.
- docs/web-board.md: main's `interests --kind pr` hub text, then the CR's "The writer" bullet.
- scenario/run_scenario.py: surface-board unit lists outside_poller and surface_writer (timeout 700 from the CR);
  both cases registered.
- cli.py: both `sync` and `interests`/`journal` in FULL_OUTPUT and in the parser list.
- hub/journal.py: SOURCES = hub, board, cli, poller, writer; docstrings name both; one docstring line wrapped
  for ruff (E501), uncommitted.
- hub/schemas.py: Issue1 and the Sync* models, texts, and PUBLISHED entries all kept. schemas.json (auto-merged)
  regenerated with `just journal-schemas`: no diff.

Fast gate: `just lint` -> pass (ruff, mypy, biome, uv lock --check) after the wrap fix.
Tests: `uv run --locked pytest skills/chantier/scripts/cli/tests -q -k "writer or journal or hub or schema or surface or poller or interests"` -> 251 passed.
Not run: `just check` in full, `just scenario`.
