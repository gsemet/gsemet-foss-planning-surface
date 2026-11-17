# Agent instructions

## Git autosync

Agent sessions do **not** run the surface's autosync (2026-11-17): do not join its group, start
it, stop it or approve its incidents, even when the user says `start autosync`; say so and point
to the board. The goal is that chantier's web board (`chantier board`) owns the autosync: it joins
the group itself and shows Start, Stop and Approve, on the user's click only, as chantier's
`docs/planning-modes.md` ("The surface's autosync") describes. The tool and its rules stay in
[autosync guidelines](.agents/guidelines/autosync.guidelines.md), for the board and for the user.

Until then, commit by hand: stage only your own paths, commit, `git pull --rebase`, `git push`.
Never force-push, never stage what another session changed.

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
