# chantier validate: check a planning folder

Asked by the user on 2026-11-17, in a Chief of Staff session on the Markdown OKF-Schema Studio
project, while moving its backlog into the planning surface.

The planning surface should not define its own validation of change requests: the format belongs
to chantier, and must stay compatible with the board. Today chantier has no command that checks a
whole planning folder; the surface's `just validate` only places each CR from its folder and runs
`chantier summary lint`.

Wanted: a `chantier validate` command (with `--project` in a surface) that checks:

- the stage and priority folders: every CR in a stage folder, P1..P4 only under `2-backlog`;
- the shape of a CR folder (`intake/`, `01-intent.md`, `02-answers.md`, `03-change-spec.md`,
  `summary.json`, `evidence/`, `work/`), and no CR nested inside another;
- the format of `summary.json`, as the board reads it;
- links between Markdown files of the planning folder that no longer resolve (e.g. after a stage
  rename);
- an exit code for gaps and another for errors, so a surface can call it from `just validate`.

Once it exists, the surface's `scripts/validate-bundles.py` calls it instead of its own placement
check.

Seen while running chantier from GitHub: the `v0.9.0` tag cannot run with
`uvx --from git+https://github.com/gsemet/chantier@v0.9.0` (no `pyproject.toml` at its root);
`v0.11.0` can.
