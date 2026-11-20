# Agent instructions

## Publishing the surface

The surface server (`chantier board`, from chantier 0.12 on, 2026-11-20) runs the surface's writer:
it commits the plan's files, rebases on the upstream and pushes, for every project and session of
this checkout. Agent sessions never stage, commit, pull or push here, and never run
`scripts/ai-autosync-git.py`: they write the working tree, and the writer publishes it. Its state is
the `writer:` line of `chantier status` (`synced`, `pending`, `syncing`, `offline`, `conflict` or
`blocked`); `chantier sync now` asks for a cycle at once. With no server running, chantier refuses
to write in the surface and names the command that starts the board. A `conflict` goes to the Chief
of Staff, who resolves the rebase; the writer pushes once it is done. Never force-push.

## Validation

The format of a change request belongs to [chantier](https://github.com/gsemet/chantier): the
surface adds no schema of its own, and checks only what chantier does not check yet.

- **Mandatory:** after you create, edit, move or delete any file under `projects/`, run
  `just validate` (or `just validate <name>` for one project) before you end your turn, and fix
  every error it reports, before you commit.
- `just validate` places each change request from its folder (stage, priority) and runs
  `chantier summary lint`, which lists the change requests whose `summary.json` (read by
  chantier's board) is missing or late; that list fails nothing.
- chantier runs from its GitHub tag through `uvx`, pinned in `scripts/validate-bundles.py`. The
  surface's [`uv.toml`](uv.toml) keeps its tools on the public PyPI; `uvx` reads it only when
  passed `--config-file uv.toml`.
- Write Markdown files in UTF-8 **without** BOM.

## Change requests

A change request is a folder `projects/<name>/changes/<stage>/<issue>-<slug>/`:

- Its files follow chantier's layout (`intake/`, `01-intent.md`, `02-answers.md`,
  `03-change-spec.md`, `summary.json`, `evidence/`, `work/`); chantier's cards describe them.
  Frontmatter is optional: chantier keeps a CR's title, summary and origin (an issue, or verbal)
  in `summary.json`, through `chantier summary set`, never by hand.
- **Stage and priority come from the folder**, and `just validate` derives them and prints them:
  `1-inbox` inbox, `2-backlog/P1`..`P4` backlog with that priority, `3-ready`, `4-batch/1-pending`,
  `2-actives`, `3-done`, `5-archives`, `6-trash`. Moving a CR is changing its stage or priority.
