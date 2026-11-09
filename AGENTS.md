# Agent instructions

## Git autosync

This project has strong rules for file synchronization. You HAVE to follow the [autosync guidelines](.agents/guidelines/autosync.guidelines.md) when you have this project in your environment.
Use can request starting or stopping autosync with `start autosync` or `stop autosync` in their chat.

## Project bundles and validation

Each `projects/<name>/` with an `index.md` at its root is an OKF bundle. Its documents are
validated by [okf-schema](https://github.com/gsemet/okf-schema) against the shared schemas of
[`_schemas/`](_schemas/), never against a `_schema/` of its own.

- **Mandatory:** after you create, edit, move or delete any file under `projects/` or `_schemas/`,
  run `just validate` (or `just validate <name>` for one project) before you end your turn, and
  fix every error and warning it reports. A turn that changed these files is not finished until
  `just validate` passes. Autosync publishes within seconds, so validate as soon as an edit is
  done.
- Every Markdown document of a bundle has a frontmatter `type` that names a schema of `_schemas/`
  (`<type>.schema.yaml`), plus `title` and `description`. Lists in frontmatter are inline
  (`[a, b]`), never block style. A folder holding Markdown has an `index.md`; only the bundle's root
  `index.md` has a frontmatter (`okf_version`). `log.md` sits at the bundle root only.
- Write Markdown files in UTF-8 **without** BOM: a BOM hides the frontmatter (E1).
- A new kind of document gets its schema in `_schemas/` first. A schema change is checked against
  every bundle (`just validate`), since all projects share it.

## Change requests

A change request is a folder `projects/<name>/changes/<stage>/<issue>-<slug>/`:

- `intake/`: the issue as received from its tracker (GitHub, GitLab or Jira): the raw JSON of the
  issue, its comments and timeline, and `attachments/` with every image or file it links, under a
  readable name that keeps the tracker's id. Never edited.
- `index.md`: the folder's contents and the link to the issue.
- `01-intent.md` (`type: cr-intent`): the pre-analysis, the current understanding of the subject
  for the operator and for agents. Its frontmatter carries what matters at a glance (issue, kind,
  priority, reporter, area, requirements, how well it is understood, open questions,
  attachments); its body shows the attachments and says what is known, what is open and the next
  step.
