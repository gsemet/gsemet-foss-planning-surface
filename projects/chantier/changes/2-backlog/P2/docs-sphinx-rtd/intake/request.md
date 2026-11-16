# Rewrite the documentation as a Sphinx site on Read the Docs

## The user's words (2026-11-09, French, verbatim)

> J'ai besoin que l'on reprenne la doc et qu'on en fasse une propre en Sphinx avec readthedoc.
> Planifie ça dans une CR que l'on fera plus tard. Regarde les autres projets perso comment
> j'aime faire (sur github).
>
> Par contre, il faut trouver un moyen de faire des documentation claire, avec des sections
> diataxis peut être. Mais souvent la doc générée par IA est trop inclaire, on voit que c'est
> écrit par IA (slop) et pourtant je pense qu'on peut faire quelque chose de visuel et très bien
> fait.

## Chief of Staff notes (what the user's other projects do)

Three of the user's recent repositories share one setup: `gsemet/okf-schema`,
`gsemet/ai-guidelines`, `gsemet/copilot-session-usage`.

- `.readthedocs.yaml` v2: ubuntu-24.04, Python 3.13, `uv sync` with the `dev` (and `docs`)
  groups, `git fetch --tags`, `pre_build: uv run cz changelog`, `sphinx.configuration:
  docs/source/conf.py`; ai-guidelines adds `fail_on_warning: true`.
- `docs/source/` laid out by Diátaxis: `tutorials/`, `how-to/`, `explanation/`, `reference/`,
  each with an `index.md`, plus `index.md`, `installation.md`, `changelog.md`.
- Markdown through MyST (`colon_fence`, `deflist`, heading anchors 3); `sphinx_design`,
  `sphinx_copybutton`, `sphinxcontrib.mermaid` (okf-schema), `sphinx_click` for a CLI reference.
- Theme: Furo (okf-schema, copilot-session-usage) or pydata-sphinx-theme (ai-guidelines), with
  `source_repository` / edit-page links, `_static/custom.css` and `_static/changelog.js`.
- okf-schema keeps hand-made SVG figures in `_static/`, each with a `.prompt.md` beside it.

chantier today: loose Markdown and SVGs in `docs/` (how-chantier-works, the CR and batch
lifecycles, use cases, a Claude Code tutorial, the release process), each SVG with a
`-texts.md` source; no Python package, a single-file CLI run by `uv run --script`.

## Open questions for the grill

- Which theme (Furo or pydata), and is the site's visual identity shared with the landing page
  (separate CR)?
- What "not slop" means as checkable rules: a style guide, a reviewer card, a lint, examples
  of good and bad pages?
- Which visuals: the existing SVGs, Mermaid, sphinx-design cards and tabs, animated figures?
- How the CLI reference is generated (argparse, no click), and how pages stay in sync with the
  cards in `skills/chantier/references/`.
- Where the docs build runs in `just check` and in CI; RTD project and domain.
- What becomes of the current `docs/` files and the README.
