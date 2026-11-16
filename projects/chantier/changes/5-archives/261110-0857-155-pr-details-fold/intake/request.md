# The default PR template folds its bulk under a collapsed details block

## The user's words (2026-11-09, French, verbatim)

> nouveau sujet: j'aimerais faire comme ce tweet, dans le modele par default de PR fourni par
> chantier
>
> Simon Willison @simonw: I've recently started hiding the bulk of my AI-generated GitHub PR
> descriptions behind a collapsed <details><summary> HTML tag (thankfully supported by GitHub
> Markdown) and I think it's a useful pattern for making PR slop a little bit less exhausting
>
> note ca dnas un P1 et on grille un tout petit peu dessus

## Chief of Staff notes

- The default template is `skills/chantier/references/pr-template.md` (v0.8.0): Summary,
  Deliverables, Changes, Impacts, Blast radius, Test plan, Autonomous decisions, Internal
  references; every section kept and filled; the Inspector's audit checks them in order.
- GitHub and GitLab both render `<details><summary>`; a blank line is needed after
  `</summary>` for the Markdown (and Mermaid) inside to render.
- A project's own template still ranks above this one; only the default changes.
