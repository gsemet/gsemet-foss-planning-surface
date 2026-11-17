# 142 — A `[[toc]]` marker renders a clickable table of contents

Type: feat · Priority: P1 · From backlog: `02-backlog/P1/toc-marker`

## Intent (user)

See [01-intent.md](../01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "rajoute tout ça dans les requêtes à faire dans une stack … livre-moi tout ça sur la stack en cours, dans des nouvelles PR; s'il y a des changements impactants tu peux t'organiser pour optimiser les livraisons". List these in the PR body under "Autonomous decisions".

## Scope change (user, 2026-10-27 23:xx): use the real TOC syntaxes, not `[[toc]]`

The user asked where `[[toc]]` comes from. Checked sources:

- **GitLab** (GitLab Flavored Markdown, docs.gitlab.com/user/markdown): `[[_TOC_]]` or `[TOC]` on a
  line of its own, in Markdown files, wikis, issues, MRs and epics.
- **GitHub**: no marker at all; GitHub shows an automatic "Outline" menu for files with two or more
  headings. A `[TOC]` line stays literal text on GitHub.
- `[TOC]` is also what Markdown Preview Enhanced and Typora use. `[[toc]]` is not a standard
  syntax: **drop it**.

New expected behaviour (replaces the marker syntax of `01-intent.md`; everything else stays):

- `[TOC]` and `[[_TOC_]]` (case-insensitive, alone on their line, outside code) render the
  document's headings as a nested, clickable table of contents in read mode.
- MyST's `{contents}` directive (Sphinx/docutils), with `:depth:` and `:local:`, renders the same
  list; this is the way to limit the depth (no `depth=` option on the bracket markers).
- The palette icon and `/toc` insert `[TOC]` (works on GitLab, MPE and Typora; readable on GitHub).
- Edit mode: an admonition-like block titled with the literal marker (`[TOC]`, `[[_TOC_]]`, or the
  `{contents}` opening line), per CR 140's rule.
- Docs and SwRS use these syntaxes; a work in progress on `[[toc]]` is renamed, not kept as an alias.
