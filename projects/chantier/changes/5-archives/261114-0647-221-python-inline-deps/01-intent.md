# Intent: Python dependencies through uv's inline metadata, and the code modularised

chantier's Python already runs through `uv run --script` with an inline metadata block
(`dependencies = []`). The user lifts the "no dependencies" rule: the CLI (and the board server
that grows from `chantier board`) may declare dependencies in that block, uv installing them
with no setup by the user, to simplify and modularise the code (`commands.py` is 3,198 lines
today). `AGENTS.md` changes with it. It runs first, before the board CRs (visualization-backend,
cr-summaries and those after them), so they build on the new structure.
