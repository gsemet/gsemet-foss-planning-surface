# chantier validate: check a whole planning folder

## The request

The user asked on 2026-11-17 (verbal, in a Chief of Staff session on the Markdown OKF-Schema
Studio project, while moving its backlog into the planning surface) for a `chantier validate`
command that checks a whole planning folder, so that a planning surface stops carrying its own
validation of change requests. The format of a CR belongs to chantier and must stay compatible
with the board.

## Today

- chantier has no command that checks a planning folder as a whole. `chantier summary lint`
  lists the CRs whose `summary.json` is missing, unreadable or late, in the live stages only
  (`1-inbox` to `4-batch`, not `5-archives`, not `6-trash`), and exits 2 when it lists a gap.
- The surface (`gsemet-foss-planning-surface`) carries `scripts/validate-bundles.py`, run by its
  `just validate`: for each project it places every folder holding `01-intent.md` from its path
  (stage, priority; a CR outside a stage folder, a priority folder outside `2-backlog`, a backlog
  item with no `P1`..`P4` folder fail), prints a table of the CRs, then runs `chantier summary
  lint` from the GitHub tag `v0.11.0` through `uvx` and reports its gaps without failing on them.
  Its placement check misses a CR that has no `01-intent.md` yet (a freshly filed one holds only
  `intake/`).
- What the surface holds today (read on 2026-11-18): no CR out of place and no nested CR in any
  project; every `summary.json` reads as the board reads it; broken relative links between
  Markdown files of the live stages exist in two projects (CRs moved from a project's
  `.agents/changes/` into the surface: `../../../../AGENTS.md` and the like), and hundreds in the
  archives of one of them; folders with only `work/` or `experiments/` sit in stages; loose
  Markdown files sit directly in stage folders (`1-inbox/index.md`, run briefs in `5-archives/`).

## What is wanted

`chantier validate` (with `--project` in a surface) checks:

1. the stage and priority folders: every CR in a stage folder, `P1`..`P4` only under
   `2-backlog`;
2. the shape of a CR folder (`intake/`, `01-intent.md`, `02-answers.md`, `03-change-spec.md`,
   `summary.json`, `evidence/`, `work/`), and no CR nested inside another;
3. the format of `summary.json`, as the board reads it;
4. relative links between Markdown files of the planning folder that no longer resolve (for
   instance after a stage rename or a move);
5. one exit code for gaps and another for errors, so a surface's `just validate` can call it.

Once it ships, the surface's `scripts/validate-bundles.py` calls it instead of its own placement
check (a change in the surface, after a chantier release carries the command).

## Analysis

- It is a read-only tool of the CLI, in the CLI's scope ("a few tools"), from a measured need:
  the surface keeps a script of its own that duplicates chantier's layout and drifts from it.
- The layout it checks is the one the cards already define (`concepts.md`, "Change Request",
  "Lifecycle", "Planning folder"; `docs/planning-folder.md`): the command adds no rule of its own.
- The board must keep reading what passes: the summary format check is the board's own read
  (`summaries/store.py`), plus the limits `summary set` enforces.
- Seen on the way, not part of this CR: the `v0.9.0` tag cannot run with
  `uvx --from git+https://github.com/gsemet/chantier@v0.9.0` (no `pyproject.toml` at its root);
  `v0.11.0` can. A published tag is not rewritten.
