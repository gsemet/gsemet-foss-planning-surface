# Change Specification: the documentation as a Sphinx site on Read the Docs

Origin: verbal (the user, 2026-11-09). Checked against `main` at `3a9afc2c` (v0.13.0 plus two
commits), 2026-11-18. Revised the same day after the spec critic's pass.

## Goal

The user's words: a clean documentation, built with Sphinx and published on Read the Docs, laid
out like their other projects (okf-schema), clear and visual. Concretely:

- The pages of `docs/` become one Sphinx site, theme **Furo** (as okf-schema), in Diátaxis
  sections (tutorials, how-to guides, explanation, reference) (answers 1, 2, 3).
- Every image of `docs/` appears in the site (answer 3).
- The README keeps its presentation and its images; its long sections move to the site, and each
  keeps a short paragraph with a link to it (answer 3; "Settled by the Chief of Staff (spec-critic's
  findings)").
- The site has its own look (Furo, in okf-schema's style), not the landing page's (answer 4).

The "not slop" part of answer 2 (the style guide `docs/STYLE.md`, the page-by-page review, and the
Inspector's `AGENTS.md` rule) is split out to `1-inbox/docs-style-guide-and-anti-slop-review-of`,
stacked on this CR. This CR moves the pages, builds the site, sets up Read the Docs and rewires the
links.

## Order: after batch-28's docs CRs

This CR starts once CR-370 (factory mode), CR-374 (refusals explained) and CR-376 (agentless
surface launch) have merged (`depends.json` names the three). It joins batch-28 stacked after them.
The Driver starts from `main` with the three merged, and re-reads every path and line number below
there: the numbers here are at `3a9afc2c` and move with those CRs.

## Today (main once 370, 374 and 376 merged)

The CLI is a Python package in the root `pyproject.toml` (`chantier`, hatchling, `[tool.uv]
no-build = true`, one `dev` group), locked in `uv.lock`. Its parser is `argparse`
(`skills/chantier/scripts/cli/src/chantier/cli.py`, `_parser()`). There is no Sphinx, no
`.readthedocs.yaml`, no `docs` group.

`docs/` holds, flat:

- 13 pages: `agents-and-models.md`, `boards.md`, `costs.md`, `gates.md`, `hosts.md`,
  `planning-folder.md`, `planning-modes.md`, `release-process.md`, `tutorial-claude-code.md`,
  `use-cases.md`, `use-cases-foreman.md`, `use-cases-direct.md`, `web-board.md`.
- 13 diagrams (`*.svg`): `batch-lifecycle`, `batch-modes`, `batch-pace`, `cr-folder-lifecycle`,
  `cr-lifecycle-line`, `cr-lifecycle-simple`, `cr-lifecycle`, `how-chantier-works`,
  `how-chantier-works-simple-direct`, `how-chantier-works-simple-foreman`, `logo`,
  `planning-modes`, `release-driver`. Each but `batch-pace.svg` and `logo.svg` has a
  `<name>-texts.md` source beside it (the diagram's texts, not a page).
- Screenshots: `docs/*.png` (7) and `docs/web-board/*-pc.png` / `*-phone.png` (written by `just
  docs-screenshots`, `scripts/docs_screenshots.py`, from `docs/demo/`).
- `docs/demo/`: the fictional planning surface the screenshots are taken from (not a page).
- `docs/release-notes/<date>-vX.Y.Z/`: each release's notes and thread, read by
  `scripts/release_notes.py` and staged by `just release` (not pages of the site).

Images no page or README names today: `batch-pace.svg`, `logo.svg`, and 8 phone screenshots
(`config-phone.png`, `costs-phone.png`, `editor-phone.png`, `home-phone.png`, `kanban-phone.png`,
`new-phone.png`, `panel-phone.png`, `project-phone.png` in `docs/web-board/`).

What the three CRs before this one add, and this CR carries over:

- CR-370: a README section `## Factory mode` after "Batch modes"; in `docs/use-cases.md` a
  paragraph linking that README section; one sentence each in `use-cases-foreman.md` and
  `use-cases-direct.md`; `batch-lifecycle-texts.md` and `batch-lifecycle.svg` updated together.
- CR-374: `use-cases-direct.md`, `tutorial-claude-code.md`, `batch-lifecycle-texts.md` and
  `batch-lifecycle.svg` reworded.
- CR-376: `web-board.md` and `planning-modes.md` (a section "With no agent") changed.

What reads the pages' paths, and must follow the move (line numbers at `3a9afc2c`):

- `README.md`: images (`docs/*.svg`, `docs/*.png`, `docs/web-board/batch-pc.png`) and its links to
  `docs/*.md` (the intro, "Planning modes", "What a batch costs", "The CR board", "Install",
  "Use", "More"; CR-370's "Factory mode" if it links a page).
- `CONTRIBUTING.md`: `docs/use-cases-direct.md` (line 30), `docs/release-process.md` (line 376),
  both links; the "Repository layout" line for `docs/` (line 176).
- `skills/chantier/references/concepts.md:137` (link `../../../docs/planning-modes.md`, in
  "Words"), `chief-of-staff.md:90` (`docs/gates.md`), `chief-of-staff.md:1736`
  (`docs/release-process.md`), `init.md:85` (`docs/gates.md`), `hosts/claude-code.md:637`
  (`docs/boards.md`, twice).
- `evals/README.md:370` (`../docs/release-process.md`).
- `scripts/release_notes.py:13,99` (messages naming `docs/release-process.md`).
- `docs/release-process.md:41-43` (the release notes' header links:
  `blob/vX.Y.Z/docs/tutorial-claude-code.md`, `blob/vX.Y.Z/docs/use-cases.md`) and `:50` (each
  highlight's doc link, `blob/vX.Y.Z/...`).
- `docs/demo/README.md:11` (`../planning-modes.md`).
- `skills/chantier/scripts/cli/tests/test_plugin_files.py`,
  `test_skill_and_references_links_resolve`: globs `docs/*.md` (flat) and skips every link that
  starts with `http`.
- `chantier rules` lists `docs/use-cases-direct.md` and `docs/release-process.md` as project rules
  today (followed from `CONTRIBUTING.md`); it must list them at their new paths.

Past release notes keep their `blob/vX.Y.Z/docs/...` links: a tag's files never move, so they stay
valid. The planning surface's `AGENTS.md` names "chantier's `docs/planning-modes.md`" in text: not
this CR's PR (see "After the merge").

## What changes

### 1. The site's source: `docs/` itself

- `docs/conf.py`: the Sphinx configuration. The source folder is `docs/`; images stay at their
  paths (the README and `scripts/docs_screenshots.py` keep pointing at them).
- `exclude_patterns`: `_build`, `demo/**`, `release-notes/**`, `**/*-texts.md`.
  (`docs/STYLE.md` and its exclusion belong to the split CR.)
- Extensions: `myst_parser` (with `colon_fence`, `deflist`, `myst_heading_anchors = 3`),
  `sphinx_design`, `sphinx_copybutton`. No Mermaid, no `sphinx_click`, no `sphinx-argparse`.
- Theme: `html_theme = "furo"`, with okf-schema's options: `source_repository =
  "https://github.com/gsemet/chantier/"`, `source_branch = "main"`, `source_directory = "docs/"`
  (the "edit this page" and "view source" links); `html_logo = "logo.svg"`; a small
  `docs/_static/custom.css` only where Furo's defaults do not hold (none required).
- `project = "chantier"`; `release` and `version` read from the root `pyproject.toml` with
  `tomllib` at build time. No version is written in `conf.py`, so `scripts/version.py` and
  `just version` are unchanged.

### 2. Pages in Diátaxis sections

Each section is a folder with an `index.md` holding its toctree:
`docs/tutorials/`, `docs/how-to/`, `docs/explanation/`, `docs/reference/`, plus `docs/index.md`
(the site's home) and `docs/installation.md`. Every existing page is carried over (answer 3), with
the three CRs' changes; moved with `git mv` so history follows, then edited. The target, which the
Driver may refine within Diátaxis (a page split in two when it mixes kinds, never a page dropped):

| Today | Target | Kind | Images it shows |
| --- | --- | --- | --- |
| README intro, "How Chantier works" | `index.md` (what chantier is, `sphinx-design` cards to the four sections, a "Release notes" link to GitHub Releases) | home | `how-chantier-works.svg`, `how-chantier-works-simple-foreman.svg`, `how-chantier-works-simple-direct.svg`, `direct-mode-session.png` |
| README "Install" | `installation.md` | how-to | |
| `tutorial-claude-code.md` | `tutorials/claude-code.md` | tutorial | as today |
| `use-cases.md`, `use-cases-foreman.md`, `use-cases-direct.md` | `how-to/use-cases.md`, `how-to/use-cases-foreman.md`, `how-to/use-cases-direct.md` | how-to | as today |
| `gates.md` | `how-to/gates.md` | how-to | |
| `agents-and-models.md` | `how-to/agents-and-models.md` | how-to | |
| `release-process.md` | `how-to/release-process.md` (chantier's own release; for contributors) | how-to | |
| README "Planning modes", `planning-modes.md` | `explanation/planning-modes.md` | explanation | `planning-modes.svg` |
| README "Batch modes", "Factory mode" (CR-370), "Change Requests Lifecycle", "Detailed lifecycle", "Releases" | `explanation/batches-and-lifecycle.md` (one section each, "Factory mode" among them) | explanation | `batch-modes.svg`, `batch-lifecycle.svg`, `batch-pace.svg`, `cr-lifecycle-line.svg`, `cr-lifecycle-simple.svg`, `cr-folder-lifecycle.svg`, `cr-lifecycle.svg`, `release-driver.svg` |
| README "What a batch costs", `costs.md` | `explanation/costs.md` | explanation | |
| README "The CR board", `boards.md` | `reference/boards.md` | reference | the `board-mod-*.png` and `status-report-done.png` as today |
| `web-board.md` | `reference/web-board.md`, with a new section "On a phone" | reference | every `docs/web-board/*.png`: the ones named today, plus the 8 phone screenshots above in "On a phone" |
| `planning-folder.md` | `reference/planning-folder.md` | reference | |
| `hosts.md` | `reference/hosts.md` | reference | |
| README "Use" (what you say, what happens) | `reference/what-you-say.md` | reference | |

`logo.svg` is the site's logo through `conf.py`'s `html_logo`, and needs no page.

Within the pages:

- Links between pages are relative Markdown links to the `.md` files (MyST resolves them; the
  repository's link test reads them too). CR-370's link in `use-cases.md` to the README's "Factory
  mode" section becomes the site's section,
  `../explanation/batches-and-lifecycle.md#factory-mode`.
- Links to the cards and other repository files outside `docs/` become absolute GitHub URLs on
  `main` (`https://github.com/gsemet/chantier/blob/main/<path>`): a relative link out of the source
  folder does not build.
- `sphinx-design` where it helps reading: tabs for Claude Code / GitHub Copilot where a page gives
  both hosts' commands; cards on the home and section indexes. No new figure is drawn.
- The cards (`skills/chantier/references/`) are not copied into the site: a page that needs a
  card's rule says it in a user's words and links the card.
- The SVGs' `-texts.md` stay beside their SVG, outside the build.
- No CLI reference page; no release notes in the site, a link to GitHub Releases from the home page.

### 3. The README

The long sections move to the site; the README keeps its presentation, its images, and for each
section a short paragraph (a few lines) with a link to the site's page or section that now holds
the detail. The detailed prose lives only in the site.

- Kept as is: the title, the tagline and the intro bullets (the presentation), each with its
  links rewired; `## Develop` (already short, links `CONTRIBUTING.md` and `evals/README.md`).
- Every image the README shows today stays in the README, under its section (paths unchanged).
- Each of "How Chantier works", "Planning modes", "Batch modes", "Factory mode", "What a batch
  costs", "Change Requests Lifecycle", "Detailed lifecycle", "Releases", "The CR board" and "Use":
  its images, a short paragraph, a link to its place in the site (table above). "What a batch
  costs" keeps no table; "Use" keeps no table.
- `## Install` keeps its heading (the anchor `#install` is linked by every release's header and by
  `scripts/release_notes.py`'s `INSTALL_LINK`), the four install commands, and a link to
  `installation.md` on the site for the rest.
- "More" becomes "Documentation": one line naming the site, then one link per section index.
- Every link to a page points at the published site, `https://chantier.readthedocs.io/en/latest/<page>.html`
  (slug `chantier`; if the slug is taken at import, the user gives another and the PR's links
  follow it before merge).

### 4. The build: `just docs`, inside `just check`

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

### 5. Read the Docs configuration (in the repository)

`.readthedocs.yaml` at the root, version 2:

- `build.os: ubuntu-24.04`, `build.tools.python: "3.13"`.
- uv installed and the `docs` group synced into Read the Docs' environment, by Read the Docs'
  documented uv recipe (`build.jobs`: install uv, `uv venv $READTHEDOCS_VIRTUALENV_PATH`, then
  `UV_PROJECT_ENVIRONMENT=$READTHEDOCS_VIRTUALENV_PATH uv sync --locked --group docs`;
  `--no-install-project` if the build does not import chantier).
- `sphinx.configuration: docs/conf.py`, `sphinx.fail_on_warning: true`.
- No `git fetch --tags` and no `cz changelog`: chantier has no commitizen.

### 6. Paths that follow the move

- Every reference listed under "Today" is updated to the new path: the cards, `CONTRIBUTING.md`
  (its two links stay relative repository links, to `docs/how-to/use-cases-direct.md` and
  `docs/how-to/release-process.md`, so `chantier rules` follows them), `evals/README.md`,
  `scripts/release_notes.py`'s messages, `docs/demo/README.md`.
- `concepts.md:137` becomes `../../../docs/explanation/planning-modes.md`. That line is in
  "Words", outside every section the startup manifest measures (`## Startup core` of each card,
  and the reload's `startup-core.md`, `role-core.md`, `startup-manifest.json` and
  `session-start.md` "5. Reload"), so it spends nothing against `STARTUP_LIMIT` (12 544 bytes;
  at `3a9afc2c` the Chief of Staff's reload on Copilot measures exactly 12 544, and CR-375 and
  CR-379 spend against it). The same holds for `chief-of-staff.md:90,1736`, `init.md:85` and
  `hosts/claude-code.md:637`. The Driver edits no startup-measured section.
- `CONTRIBUTING.md`: the "Repository layout" line for `docs/` (the site's source, in Diátaxis
  folders, with the diagrams, screenshots and release notes) and a `just docs` line under "Daily
  work".
- `docs/how-to/release-process.md`, for future release notes, pins every link to the docs to the
  release's version on the site, `https://chantier.readthedocs.io/en/vX.Y.Z/<page>.html`:
  - the header's tutorial link (`/en/vX.Y.Z/tutorials/claude-code.html`) and use-cases link
    (`/en/vX.Y.Z/how-to/use-cases.html`), instead of `blob/vX.Y.Z/docs/...`; the Install link
    (`https://github.com/gsemet/chantier#install`) and "Full changes" are unchanged;
  - each highlight's doc link: a site page at `/en/vX.Y.Z/...`; a link to a file that is not a site
    page (a card, a script) stays `blob/vX.Y.Z/...`.
  - It says the version's docs exist once Read the Docs has built the tag (User step 3).
- No `AGENTS.md` change in this CR.

### 7. Tests (reading the shipped files)

In `skills/chantier/scripts/cli/tests/test_plugin_files.py`, reading the files as they ship at the
head under test, never a copy:

- `test_skill_and_references_links_resolve` reads every site page: `docs/**/*.md` minus
  `demo/`, `release-notes/`, `_build/` and `*-texts.md` (it globs `docs/*.md` today), plus the
  files it reads today. It stops skipping every `http` link: it maps two URL forms back to
  repository files and asserts they exist:
  - `https://chantier.readthedocs.io/en/latest/<page>.html` → `docs/<page>.md`, and
    `https://chantier.readthedocs.io/en/latest/<dir>/` (or the site's root) →
    `docs/<dir>/index.md` (or `docs/index.md`); the anchor is already cut by the test's pattern;
  - `https://github.com/gsemet/chantier/blob/main/<path>` (and `tree/main/<path>` for a folder) →
    `<path>` from the repository's root.
  Any other `http` link is skipped, as today. The site's base URL is one constant in the test, so
  a different slug changes one line.
- One new test: every image of `docs/` (`*.svg` and `*.png` at its root, `docs/web-board/*.png`)
  is named by at least one site page (a Markdown image or a MyST `image`/`figure` directive,
  resolved from the page's folder), except `logo.svg`, accepted when `docs/conf.py` sets
  `html_logo = "logo.svg"`.

## Decisions carried from `02-answers.md`

1. Furo, as okf-schema (not pydata): section 1.
2. Diátaxis sections: section 2. The style guide with good and bad examples and the per-page agent
   review go to `1-inbox/docs-style-guide-and-anti-slop-review-of` (the split).
3. The site replaces `docs/`, everything carried over into Diátaxis: section 2. The README keeps
   its presentation and images; its long sections move to the site, each with a short paragraph
   and a link: section 3. The images appear in the docs: sections 2 and 7.
4. The visual identity is not shared with `landing-page`: Furo in okf-schema's style, section 1.
5. Set aside on 2026-11-10: lifted by the Chief of Staff starting this spec on 2026-11-18.

The Chief of Staff's settlements: slug `chantier`, followed by the PR's links if taken (sections 3,
7, User step 1); no CLI reference page and no new figure (section 1, 2); release notes not in the
site, a link to GitHub Releases (section 2); release-note docs links pinned to `/en/vX.Y.Z/` for the
header and the highlights (section 6, User step 3); the split (Goal); this CR after 370, 374, 376
(Order). The Inspector's rule (Q2) and the backticked mention of `docs/STYLE.md` in `AGENTS.md` and
`CONTRIBUTING.md` belong to the split CR. The points settled by the spec-writer are in
`02-answers.md`, "Settled by the spec-writer (2026-11-18)"; its `docs/STYLE.md` points moved to the
split CR.

## User steps (outward actions: the user's, never an agent's)

1. Before the PR, on readthedocs.org: import `gsemet/chantier` as a project under the slug
   `chantier` (another, if taken: then tell the Chief of Staff, the PR's links follow it). This
   installs Read the Docs' GitHub webhook or app on the repository.
2. In the project's settings: turn on "Build pull requests" so the PR gets a Read the Docs build
   and a preview link; set the default version to `latest` (branch `main`).
3. Turn on tag builds: an automation rule that activates each new tag matching `vX.Y.Z` (Read the
   Docs' "Activate version" action on a semver tag), so each release's `/en/vX.Y.Z/` exists for its
   notes' links.
4. Optional: a custom domain (DNS) is out of this CR.

If the user does steps 1 to 3 only after the merge, the first Read the Docs build is after the
merge, and the PR's Known gaps says so.

## Evidence

- `just check` green in the worktree at the pushed head (it now runs `just docs`, with `-W`).
- `just scenario` green: the CR changes cards (the long gate of `AGENTS.md`; the pipeline's
  `just scenario (ubuntu-latest)` job at the PR's head). If this CR is the top of batch-28's stack,
  the local run (`chantier gate`) at its head too.
- `just docs` output: 0 warnings; the list of built pages; a screenshot of the home page, of one
  page per section, and of `reference/web-board.md`'s "On a phone" from `docs/_build/html` (the
  Verifier's evidence).
- The README rendered on GitHub at the head (one screenshot): every image still shows, each
  section is a short paragraph with its link.
- `chantier rules` from the worktree lists the moved pages at their new paths.
- The startup measure unchanged: `test_startup_manifest.py`'s `startup-bytes` lines (run with
  `-s`) identical before and after the change, and every one at or under `STARTUP_LIMIT`.
- The link test and the new image test pass, reading the shipped files at the head. Shown once,
  then reverted: a site URL in the README naming a page that does not exist makes the link test
  fail; a renamed image name in a page makes the image test fail.
- Read the Docs' build of the PR, green, with its preview link (needs User steps 1 and 2).
- No `just eval-dry-run` owed (no change under `src/` or `evals/kit/`), and no `just mod` (no
  change to `hooks/` or `types/`).

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
(the local run may use another Python), and the webhook; only the first release after the merge
proves the tag build and its `/en/vX.Y.Z/` links.

## Out of scope

- The style guide `docs/STYLE.md`, the page-by-page anti-slop review and the Inspector's
  `AGENTS.md` rule: `1-inbox/docs-style-guide-and-anti-slop-review-of`.
- A custom domain, analytics; versions other than `latest` and each release tag.
- Past release notes' links (they stay `blob/vX.Y.Z/...`, valid at their tag).
- New figures, Mermaid diagrams, animations; a CLI reference page; release notes in the site.
- Rewriting the cards, or generating pages from them.
- The landing page (`landing-page` CR) and any visual identity shared with it.
- Translating the docs.
- The planning surface's `AGENTS.md` text (see below).

## After the merge (not this PR)

- The Chief of Staff updates the planning surface's `AGENTS.md`, which names
  `docs/planning-modes.md`, to the new path or the site's URL.

## Answered questions

1. **The first pinned links of a release.** Settled by the Chief of Staff, 2026-11-18: A, so
   `docs/how-to/release-process.md` adds the step. A release's notes link `/en/vX.Y.Z/`, which exists only
   once Read the Docs has built the tag, a few minutes after the tag is pushed.
   - A. `docs/how-to/release-process.md` adds one step: after the tag, the Release Driver checks
     that `https://chantier.readthedocs.io/en/vX.Y.Z/` serves before publishing the notes and the
     thread, and waits for it (recommended: no broken link at publication).
   - B. No step: the links are briefly broken until the tag's build ends.
