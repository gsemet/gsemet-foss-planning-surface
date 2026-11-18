# Change Specification: the documentation as a Sphinx site on Read the Docs

Origin: verbal (the user, 2026-11-09). Checked against `main` at `3a9afc2c` (v0.13.0 plus two
commits), 2026-11-18.

## Goal

The user's words: a clean documentation, built with Sphinx and published on Read the Docs, laid
out like their other projects (okf-schema), clear and visual, and not reading like AI-written
slop. Concretely:

- The pages of `docs/` become one Sphinx site, theme **Furo** (as okf-schema), in Diátaxis
  sections (tutorials, how-to guides, explanation, reference) (answers 1, 3).
- Every image of `docs/` appears in the site; the README keeps its presentation and its images
  (answer 3).
- "Not slop" is checkable: a short style guide with good and bad examples, and an agent review of
  each page against it (answer 2).
- The site has its own look (Furo, in okf-schema's style), not the landing page's (answer 4).

## Today (main, 3a9afc2c)

The intake's notes predate the CLI's package: chantier now has a Python package in the root
`pyproject.toml` (`chantier`, hatchling, `[tool.uv] no-build = true`, one `dev` group), locked in
`uv.lock`. The CLI's parser is `argparse` (`skills/chantier/scripts/cli/src/chantier/cli.py`,
`_parser()`). There is no Sphinx, no `.readthedocs.yaml`, no `docs` group.

`docs/` holds, flat:

- 13 pages: `agents-and-models.md`, `boards.md`, `costs.md`, `gates.md`, `hosts.md`,
  `planning-folder.md`, `planning-modes.md`, `release-process.md`, `tutorial-claude-code.md`,
  `use-cases.md`, `use-cases-foreman.md`, `use-cases-direct.md`, `web-board.md`.
- 12 diagrams (`*.svg`, `logo.svg` included); each but `batch-pace.svg` and `logo.svg` has a
  `<name>-texts.md` source beside it (the diagram's texts, not a page).
- Screenshots: `docs/*.png` (7) and `docs/web-board/*.png` (written by `just docs-screenshots`,
  `scripts/docs_screenshots.py`, from `docs/demo/`).
- `docs/demo/`: the fictional planning surface the screenshots are taken from (not a page).
- `docs/release-notes/<date>-vX.Y.Z/`: each release's notes and thread, read by
  `scripts/release_notes.py` and staged by `just release` (not pages of the site; see Open
  question 5).

What reads those paths today, and must follow the move:

- `README.md`: images (`docs/*.svg`, `docs/*.png`, `docs/web-board/batch-pc.png`) and its links to
  `docs/*.md`.
- `CONTRIBUTING.md`: `docs/use-cases-direct.md`, `docs/release-process.md` (links), the
  "Repository layout" line for `docs/`.
- `skills/chantier/references/concepts.md:137` (link `../../../docs/planning-modes.md`),
  `chief-of-staff.md:90` (`docs/gates.md`), `chief-of-staff.md:1736` (`docs/release-process.md`),
  `init.md:85` (`docs/gates.md`), `hosts/claude-code.md:637` (`docs/boards.md`, twice).
- `evals/README.md:370` (`../docs/release-process.md`).
- `scripts/release_notes.py:13,99` (messages naming `docs/release-process.md`).
- `docs/release-process.md:42-43`: the release notes' header links
  (`blob/vX.Y.Z/docs/tutorial-claude-code.md`, `blob/vX.Y.Z/docs/use-cases.md`).
- `docs/demo/README.md:11` (`../planning-modes.md`).
- `skills/chantier/scripts/cli/tests/test_plugin_files.py`,
  `test_skill_and_references_links_resolve`: globs `docs/*.md` (flat).
- `chantier rules` lists `docs/use-cases-direct.md` and `docs/release-process.md` as project rules
  today (followed from `CONTRIBUTING.md`); it must list them at their new paths.

Past release notes keep their `blob/vX.Y.Z/docs/...` links: a tag's files never move, so they stay
valid. The planning surface's `AGENTS.md` names "chantier's `docs/planning-modes.md`" in text: not
this CR's PR (see "After the merge").

## What changes

### 1. The site's source: `docs/` itself

- `docs/conf.py`: the Sphinx configuration. The source folder is `docs/`; images stay at their
  paths (the README and `scripts/docs_screenshots.py` keep pointing at them).
- `exclude_patterns`: `_build`, `demo/**`, `release-notes/**`, `**/*-texts.md`, `STYLE.md`,
  `README.md` if one is added.
- Extensions: `myst_parser` (with `colon_fence`, `deflist`, `myst_heading_anchors = 3`),
  `sphinx_design`, `sphinx_copybutton`. No Mermaid, no `sphinx_click` (the parser is argparse;
  see Open question 3 for a CLI reference).
- Theme: `html_theme = "furo"`, with okf-schema's options: `source_repository =
  "https://github.com/gsemet/chantier/"`, `source_branch = "main"`, `source_directory = "docs/"`
  (the "edit this page" and "view source" links); `html_logo` from `logo.svg`; a small
  `docs/_static/custom.css` only where Furo's defaults do not hold (none required).
- `project = "chantier"`; `release` and `version` read from the root `pyproject.toml` with
  `tomllib` at build time. No version is written in `conf.py`, so `scripts/version.py` and
  `just version` are unchanged.

### 2. Pages in Diátaxis sections

Each section is a folder with an `index.md` holding its toctree:
`docs/tutorials/`, `docs/how-to/`, `docs/explanation/`, `docs/reference/`, plus `docs/index.md`
(the site's home) and `docs/installation.md`. Every existing page is carried over (answer 3);
moved with `git mv` so history follows, then edited. The target, which the Driver may refine
within Diátaxis (a page split in two when it mixes kinds, never a page dropped):

| Today | Target | Kind |
| --- | --- | --- |
| README intro, "How Chantier works" | `index.md` (what chantier is, the three how-it-works diagrams, `sphinx-design` cards to the four sections) | home |
| README "Install" | `installation.md` | how-to |
| `tutorial-claude-code.md` | `tutorials/claude-code.md` | tutorial |
| `use-cases.md`, `use-cases-foreman.md`, `use-cases-direct.md` | `how-to/use-cases.md`, `how-to/use-cases-foreman.md`, `how-to/use-cases-direct.md` | how-to |
| `gates.md` | `how-to/gates.md` | how-to |
| `agents-and-models.md` | `how-to/agents-and-models.md` | how-to |
| `release-process.md` | `how-to/release-process.md` (chantier's own release; for contributors) | how-to |
| README "Planning modes", `planning-modes.md` | `explanation/planning-modes.md` | explanation |
| README "Batch modes", "Change Requests Lifecycle", "Detailed lifecycle", "Releases" | `explanation/batches-and-lifecycle.md` (with `batch-modes.svg`, `batch-lifecycle.svg`, `batch-pace.svg`, the four `cr-*.svg`, `release-driver.svg`) | explanation |
| README "What a batch costs", `costs.md` | `explanation/costs.md` | explanation |
| `boards.md` | `reference/boards.md` | reference |
| `web-board.md` | `reference/web-board.md` | reference |
| `planning-folder.md` | `reference/planning-folder.md` | reference |
| `hosts.md` | `reference/hosts.md` | reference |
| README "Use" (what you say, what happens) | `reference/what-you-say.md` | reference |

Within the pages:

- Links between pages are relative Markdown links to the `.md` files (MyST resolves them; the
  repository's link test reads them too). Links to the cards and other repository files outside
  `docs/` become absolute GitHub URLs on `main` (`https://github.com/gsemet/chantier/blob/main/...`):
  a relative link out of the source folder does not build.
- `sphinx-design` where it helps reading: tabs for Claude Code / GitHub Copilot where a page gives
  both hosts' commands; cards on the home and section indexes. No new figure is drawn (Open
  question 4).
- The cards (`skills/chantier/references/`) are not copied into the site: a page that needs a
  card's rule says it in a user's words and links the card.
- The SVGs' `-texts.md` stay beside their SVG, outside the build.

### 3. The README

- It keeps its presentation and its images (answer 3): its sections stay, its images keep showing
  on GitHub (paths unchanged, since images do not move).
- Its links to pages (`docs/*.md`, the "More" list, the tutorial and use-case links) point at the
  published site, `https://<slug>.readthedocs.io/en/latest/<page>.html` (Open question 1), and
  one "Documentation" line near the top names the site.
- No README section is removed in this CR: the parts copied into the site stay in the README too
  (answer 3 allows a move; it does not ask for one).

### 4. The style guide and the review (answer 2)

- `docs/STYLE.md`, outside the site, linked from `AGENTS.md` and `CONTRIBUTING.md`. Short (under
  about 120 lines). It holds:
  - The Diátaxis rule: each page is one kind (tutorial, how-to, explanation, reference), says so
    in its section, and does not mix them.
  - The repository's own style, made checkable: short sentences, exact terms, one meaning per
    word, the user as "you", a claim that can be checked or nothing; a figure or table where a
    flow has more than three steps or a comparison more than two items.
  - The slop markers to refuse, each with one bad and one good example taken or adapted from
    chantier's pages: a generic opening that restates the title; a closing summary that repeats
    the page; filler and hype words (for instance "seamless", "robust", "powerful", "leverage",
    "delve", "effortlessly"); vague hedges ("may help to", "in many cases") where a fact is
    known; triplets of adjectives; bold scattered through prose; emoji in headings; "simply" or
    "just" before a step; a list where a sentence says it.
- In this CR, an agent reviews every page of the site against `docs/STYLE.md`, page by page, and
  the Driver fixes what it finds. Who does it in later CRs is Open question 2.

### 5. The build: `just docs`, inside `just check`

- Root `pyproject.toml`: a `docs` dependency group with `sphinx`, `myst-parser`, `furo`,
  `sphinx-design`, `sphinx-copybutton`; each on a version that supports Python 3.11 and ships a
  pure-Python wheel (`no-build = true` holds); `uv lock` run, `uv.lock` committed. The CLI's
  `dependencies` do not change: `uvx --from <plugin>` installs no group.
- `justfile`:
  - `docs` recipe: `uv run --locked --group docs sphinx-build -W --keep-going -b html docs
    docs/_build/html` (`docs/_build/` is already in `.gitignore`).
  - `check: lint test release-notes docs`.
  - `tools`: also syncs the `docs` group (one `uv sync --locked --group dev --group docs`), so CI
    fetches it in the retried step.
- `-W` makes any warning fail: a page outside every toctree, a broken link between pages, a
  missing image, a bad directive.

### 6. Read the Docs configuration (in the repository)

`.readthedocs.yaml` at the root, version 2:

- `build.os: ubuntu-24.04`, `build.tools.python: "3.13"`.
- uv installed and the `docs` group synced into Read the Docs' environment, by Read the Docs'
  documented uv recipe (`build.jobs`: install uv, `uv venv $READTHEDOCS_VIRTUALENV_PATH`, then
  `UV_PROJECT_ENVIRONMENT=$READTHEDOCS_VIRTUALENV_PATH uv sync --locked --group docs`;
  `--no-install-project` if the build does not import chantier).
- `sphinx.configuration: docs/conf.py`, `sphinx.fail_on_warning: true`.
- No `git fetch --tags` and no `cz changelog`: chantier has no commitizen.

### 7. Paths that follow the move

Every reference listed under "Today" is updated to the new path (cards, `CONTRIBUTING.md`,
`evals/README.md`, `scripts/release_notes.py`'s messages, `docs/demo/README.md`). In
`how-to/release-process.md`, the header line of future release notes links the site's tutorial and
use cases (Open question 1's URL) instead of `blob/vX.Y.Z/docs/...`. `CONTRIBUTING.md`: the
"Repository layout" line for `docs/` and a `just docs` line under "Daily work".

`AGENTS.md`: one rule, "A page under `docs/` follows [docs/STYLE.md](docs/STYLE.md)", plus the
reviewer Open question 2 settles.

### 8. Tests (reading the shipped files)

- `test_skill_and_references_links_resolve` reads every site page: `docs/**/*.md` minus
  `demo/`, `release-notes/` and `*-texts.md` (it globs `docs/*.md` today).
- One new test in `test_plugin_files.py`: every image of `docs/` (`*.svg`,
  `*.png` at the root and in `docs/web-board/`) is named by at least one site page. It reads the
  files as they ship at the head under test.

## Decisions carried from `02-answers.md`

1. Furo, as okf-schema (not pydata): section 1.
2. Style guide with good and bad examples, an agent review per page, Diátaxis sections: sections 2
   and 4.
3. The site replaces `docs/`, everything carried over into Diátaxis; the README keeps its
   presentation and images; some parts may move; the images appear in the docs: sections 2, 3, 8.
4. The visual identity is not shared with `landing-page`: Furo in okf-schema's style, section 1.
5. Set aside on 2026-11-10: lifted by the Chief of Staff starting this spec on 2026-11-18.

The points settled by the spec-writer (no user-visible behaviour) are in `02-answers.md`, "Settled
by the spec-writer (2026-11-18)".

## User steps (outward actions: the user's, never an agent's)

1. Before the PR, on readthedocs.org: import `gsemet/chantier` as a project, under the slug of
   Open question 1 (this installs Read the Docs' GitHub webhook or app on the repository).
2. In the project's settings: turn on "Build pull requests" so the PR gets a Read the Docs build
   and a preview link; set the default version to `latest` (branch `main`).
3. Optional: a custom domain (DNS) is out of this CR.

If the user does step 1 and 2 only after the merge, the first Read the Docs build is after the
merge, and the PR's Known gaps says so.

## Evidence

- `just check` green in the worktree at the pushed head (it now runs `just docs`, with `-W`).
- `just docs` output: 0 warnings; the list of built pages; a screenshot of the home page and of
  one page per section from `docs/_build/html` (the Verifier's evidence).
- The review: one table, page by page, the `docs/STYLE.md` rules each page broke, and the fix
  (in `work/verifier/evidence/`, quoted in the PR body).
- `chantier rules` from the worktree lists the moved pages at their new paths.
- The new image test and the link test pass, reading the shipped files at the head; a renamed
  image name in a page makes the image test fail (shown once, then reverted).
- Read the Docs' build of the PR, green, with its preview link (needs User steps 1 and 2).
- No `just eval-dry-run` owed (no change under `src/` or `evals/kit/`), and no `just mod` (no
  change to `hooks/` or `types/`). `just scenario` is not affected but the CI job runs it as for
  every PR.

### The CI environment

`just check` runs in the `check` job on `ubuntu-latest`, `macos-15-intel` (named `macos-latest`,
`continue-on-error`) and `windows-latest`, with uv from `astral-sh/setup-uv@v6` and `just` from
`extractions/setup-just@v3`, the network on, and an empty uv cache at each run; `just tools` runs
first, retried once. What the local machine has and the runner has not: a warm uv cache (Sphinx,
Furo and the MyST packages already downloaded), possibly a `.venv` holding the `docs` group, and
the developer's own fonts and locale (irrelevant to an HTML build). The job's steps change (the
`tools` and `check` recipes), so, as `CONTRIBUTING.md` says, the Verifier runs `just tools` then
`just check` once on the local machine with `UV_CACHE_DIR` set to a new empty folder outside the
repository, and quotes the output.

Read the Docs' build runs on `ubuntu-24.04`, Python 3.13, with uv installed by the build itself and
no cache. Local proof before the push: in a new empty folder, `uv venv <tmp>/rtd`, then the
`.readthedocs.yaml` install line with `UV_PROJECT_ENVIRONMENT=<tmp>/rtd` and a new empty
`UV_CACHE_DIR`, then `<tmp>/rtd`'s `python -m sphinx -T -W --keep-going -b html docs <tmp>/html`.
Only Read the Docs' first build proves its own image, its uv install step and its Python 3.13
(the local run may use another Python), and the webhook.

## Out of scope

- A custom domain, analytics, versioned docs beyond `latest` and `stable`.
- New figures, Mermaid diagrams, animations (Open question 4).
- Rewriting the cards, or generating pages from them.
- The landing page (`landing-page` CR) and any visual identity shared with it.
- Translating the docs.
- Removing README sections.
- The planning surface's `AGENTS.md` text (see below).

## After the merge (not this PR)

- The Chief of Staff updates the planning surface's `AGENTS.md`, which names
  `docs/planning-modes.md`, to the new path or the site's URL.

## Open questions (for the user, through the Chief of Staff)

1. **The site's address.** The Read the Docs slug sets the URL the README and future release notes
   link to.
   - A. `chantier` (`https://chantier.readthedocs.io`), if the slug is free (recommended).
   - B. Another slug the user picks if `chantier` is taken (for instance `chantier-ai`).
   The user checks it when importing the project (User step 1); the Driver takes the slug given.
2. **Who reviews a docs page against the style guide in later CRs.**
   - A. The Inspector, by one `AGENTS.md` rule: a change to a page under `docs/` is checked page
     by page against `docs/STYLE.md`, each broken rule named in its report (recommended: no new
     agent, both hosts already run it).
   - B. A dedicated review step with a project agent (`docs-reviewer`, written for both hosts)
     declared in `chantier.yaml`, run after the Inspector.
   - C. Only this CR's one-time review; later changes rely on the guide alone.
3. **A CLI reference page.**
   - A. None in this CR: users talk to the Chief of Staff, and the commands they run themselves
     (`chantier board`, `chantier cost`) are in the pages already (recommended).
   - B. A reference page generated from the argparse parser (`sphinx-argparse`), every command.
4. **Visuals beyond the existing images.**
   - A. The existing SVGs and screenshots, plus `sphinx-design` cards and tabs; no new figure
     (recommended: the user's ask is that the images appear; new figures can be their own CR).
   - B. Also Mermaid diagrams or new figures where a page has none.
5. **Release notes in the site.**
   - A. Not in the site: a "Release notes" link to GitHub Releases from the home page
     (recommended: they are GitHub release bodies, centred HTML, and stay where
     `scripts/release_notes.py` reads them).
   - B. A "Release notes" section in the site, one page per release, which means converting their
     HTML header so the build passes `-W`.
