## Summary

Chantier's documentation was a flat folder of Markdown pages plus a long README. It is now one Sphinx site (Furo theme) in four sections (tutorials, how-to guides, explanation, reference), built by `just docs` and published on Read the Docs. The README keeps its presentation and images; each long section becomes a short paragraph with a link to the site.

## Deliverables

Layout of `docs/` before and after:

| Before | After |
| --- | --- |
| `docs/*.md` (13 flat pages) | `docs/index.md`, `docs/installation.md`, `docs/tutorials/`, `docs/how-to/`, `docs/explanation/`, `docs/reference/` (each with an `index.md` toctree) |
| README long sections | `explanation/batches-and-lifecycle.md`, `explanation/costs.md`, `reference/what-you-say.md`, and the README's short paragraphs link to them |
| 8 phone screenshots shown nowhere | shown in a new "On a phone" section of `reference/web-board.md` |

- Theme Furo, extensions `myst_parser`, `sphinx_design`, `sphinx_copybutton`; version read from `pyproject.toml` at build time.
- `just check` now also runs `just docs` (`sphinx-build -W --keep-going`): any warning fails.
- `.readthedocs.yaml` builds on Read the Docs with uv and the `docs` dependency group.
- **UNVERIFIED:** the README rendered on GitHub and the first Read the Docs build.

The built site at 2251916, from `just docs` (after only: the site is new). The home page, with the four sections in the sidebar:

![The site's home page](./home.png)

One how-to page (the gates page), in the Furo theme:

![The gates page](./how-to-gates.png)

The new "On a phone" section of the web board reference, which shows the 8 phone screenshots that no page showed before (capture of a copy of the build that hides the page's other sections, for height):

![The web board page, On a phone](./web-board-on-a-phone.png)

## Blast radius

Grade: 2. Docs paths move, so every link to a page changes (cards, `CONTRIBUTING.md`, `evals/README.md`, release-notes script); revert is possible, but links published elsewhere to old `docs/*.md` paths on `main` would break.

## Autonomous decisions

- Costs page merges the README's cost section into `explanation/costs.md`.
- New test helpers live in `tests/docs_site.py` and `tests/test_docs_site.py`, because `test_plugin_files.py` would pass the 400-line limit.

## Known gaps

- The README "Factory mode" section and the use-cases link to it are not carried over: the base does not hold that section yet; to be added after it lands.
- No Read the Docs build yet: it needs the project imported on readthedocs.org and "Build pull requests" turned on; tag builds for `/en/vX.Y.Z/` need an automation rule.
- No screenshot yet of the README rendered on GitHub.
- No `sphinx-design` tabs were added for the two hosts' commands; cards are used on the indexes.
- The `asdf` uv install lines of `.readthedocs.yaml` are untested locally.

<details>
<summary>Details</summary>

## Changes

- `docs/conf.py`, `.readthedocs.yaml`, a `docs` group in `pyproject.toml` and `uv.lock`, `just docs`, `check` and `tools` recipes.
- Pages moved with `git mv` into section folders and relinked; links out of `docs/` are GitHub URLs on `main`.
- `skills/chantier/scripts/cli/tests/test_plugin_files.py`: the link test reads every site page and maps site and GitHub URLs back to files; a new image test checks every docs image is shown by a page.
- Paths updated in the cards, `CONTRIBUTING.md`, `evals/README.md`, `scripts/release_notes.py`, `docs/demo/README.md`; `docs/how-to/release-process.md` pins release-note links to the version's site.

## Human decisions

- Furo as the theme, in the style of the author's other projects, with no look shared with the landing page.
- Diátaxis sections (tutorials, how-to, explanation, reference); every existing page is carried over, none dropped.
- The README keeps its presentation and images; each long section becomes a short paragraph with a link to the site.
- Every image of `docs/` appears in the site.
- The style guide and the page-by-page review are a separate change.

## Impacts

Users read the docs on Read the Docs; contributors run `just docs`. No change to the CLI.

## Test plan

- [x] New or changed tests (they fail on the previous code): link and image tests; a renamed link or image makes them fail
- [x] Local gates at 2251916: `just docs`, `just test` (648 passed), `just check`, and `just tools` then `just check` with an empty uv cache: pass
- [x] Evidence: after at 2251916 (the site is new, no before; startup sizes identical to the base e33fb59)
- [x] Review: approved at 2251916
- [x] Verified at 2251916
- [x] CI green at 2251916: `gh pr checks 346`, check x3, eval-dry-run, scenario (ubuntu) pass

## Internal references

- CR-381 docs-sphinx-rtd.

</details>
