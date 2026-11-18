# Docs style guide and anti-slop review of every page

The user asked, with the move of chantier's docs to a Sphinx site on Read the Docs
(`docs-sphinx-rtd`), for the docs to read well and not like AI slop. The spec-critic of 2026-11-18
found the site's build and the prose rewrite to be two deliveries; the Chief of Staff split them.
This CR is the second: a style guide with good and bad examples (`docs/STYLE.md`), a review of
every page of the site against it with the fixes, and one `AGENTS.md` rule so the Inspector checks
a changed page under `docs/` against the guide in later CRs.

- The guide is named in `AGENTS.md` and `CONTRIBUTING.md` as a path in backticks, never a
  Markdown link, so `chantier rules` does not make every role read it on every CR; the Inspector
  and the Driver of a docs change open it.
- Stacked on `docs-sphinx-rtd` (the pages' new paths).

Source: the user's answers on `docs-sphinx-rtd` (2-backlog/P2/docs-sphinx-rtd/02-answers.md), and
the Chief of Staff's split, 2026-11-18.
Short name: `docs-style-review`
