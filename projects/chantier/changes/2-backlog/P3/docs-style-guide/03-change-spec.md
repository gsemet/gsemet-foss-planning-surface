# Change Specification: a docs style guide and an anti-slop review of every page

Origin: verbal (the user, 2026-11-09, on `docs-sphinx-rtd`); split from `docs-sphinx-rtd` by the
Chief of Staff, 2026-11-18. Checked against `main` at `3a9afc2c`, 2026-11-18, and against the
pages' paths that `docs-sphinx-rtd`'s specification gives (this CR is stacked on it,
`depends.json`).

## Goal

The user's words (docs-sphinx-rtd's intake): AI-written docs are often unclear and read as AI
slop; chantier's docs should be clear, visual and well made. The user chose "a guide, a review
and examples" (docs-sphinx-rtd, answer 2). Concretely:

- A short style guide, `docs/STYLE.md`, with a good and a bad example for each rule.
- One review of every page of the Sphinx site against it, in this CR, with the fixes.
- Later CRs keep the pages to the guide: one `AGENTS.md` rule has the Inspector check a changed
  page under `docs/` against it (docs-sphinx-rtd, Q2, A).
- The guide does not cost every role a read on every CR: `AGENTS.md` and `CONTRIBUTING.md` name it
  as a path in backticks, never as a Markdown link.

## Today

On `main` (`3a9afc2c`): no style guide. `CONTRIBUTING.md:253-254` says "Repository text is in
English." and "Write code and docs in the style of the surrounding files: short sentences, exact
terms." `AGENTS.md` has one comparable rule for another folder: "A change under
`skills/chantier/scripts/cli/src/chantier/board/web/` reads its `DESIGN.md` first and keeps it
true" (a backticked name, not a link).

After `docs-sphinx-rtd` (this CR's base): `docs/` is a Sphinx site (`docs/conf.py`, MyST, Furo,
`sphinx-design`, `sphinx-copybutton`), built by `just docs` (`sphinx-build -W --keep-going`)
inside `just check`. Its pages, by that CR's table (its Driver may have refined it within
Diátaxis; the pages at this CR's base are the ones reviewed):

- `docs/index.md`, `docs/installation.md`;
- `docs/tutorials/index.md`, `tutorials/claude-code.md`;
- `docs/how-to/index.md`, `how-to/use-cases.md`, `how-to/use-cases-foreman.md`,
  `how-to/use-cases-direct.md`, `how-to/gates.md`, `how-to/agents-and-models.md`,
  `how-to/release-process.md`;
- `docs/explanation/index.md`, `explanation/planning-modes.md`,
  `explanation/batches-and-lifecycle.md`, `explanation/costs.md`;
- `docs/reference/index.md`, `reference/boards.md`, `reference/web-board.md`,
  `reference/planning-folder.md`, `reference/hosts.md`, `reference/what-you-say.md`.

Not site pages: `docs/demo/`, `docs/release-notes/`, the SVGs' `*-texts.md`.

Why a backticked path: `chantier rules` (`skills/chantier/scripts/cli/src/chantier/commands/rules.py`)
lists the project's instruction file and the local Markdown files it links, two levels deep
(`MD_LINK` matches `](<path>.md)` and `[x]: <path>.md`); every role reads that list before its
card. A link to `docs/STYLE.md` from `AGENTS.md` (level 1) or from `CONTRIBUTING.md` (level 2,
linked from `AGENTS.md`) would put the guide in every role's reading. A path in backticks is not
followed.

The pages today: the classic filler words are rare (a search for "simply", "seamless",
"leverage", "robust", "in short" finds one, in a `-texts.md`). The weaknesses are of another kind,
for instance `docs/gates.md` (to be `how-to/gates.md`): a subtitle that restates the title and is
then said again; sentences of 50 words and more; the agents' internals (`handback ready`, `ship`,
patch-ids) in a page for the user. The guide is written for those, as well as for the classic
markers.

## What changes

### 1. `docs/STYLE.md` (new)

Plain Markdown, outside the site (see section 4 for the build), under about 150 lines. Its reader
is the agent or person who writes or reviews a site page. Each rule has a short id (`S1`, `S2`,
...) that the review table and the Inspector's items cite, one line saying the rule, and, where
the rule is about prose, one **bad** and one **good** example, taken or adapted from chantier's own
pages (the bad one quoted from the page as it was before this CR's fixes, where one exists).

The rules it holds, at least:

- **One kind per page (Diátaxis).** A page is a tutorial, a how-to guide, an explanation or a
  reference, sits in that section's folder, and does not mix kinds: a how-to does not stop to
  explain the design; an explanation gives no steps to follow; a reference lists, it does not
  argue. A page that needs both kinds links the other page.
- **The reader is the user of chantier**, called "you". What the agents do among themselves (CLI
  subcommands only agents run, record fields, card rules) appears only where the user sees its
  effect, said in the user's terms, with a link to the card on GitHub for the detail.
- **The opening says what the page gives you**, in one or two sentences, and is not a restatement
  of the title; no second introduction after it.
- **No closing summary** that repeats the page; a page ends on its last useful line (or a "Next"
  link).
- **Short sentences**: one idea each; a sentence over 35 words is split.
- **Exact terms, one meaning per word**: the words of chantier's glossary
  (`skills/chantier/references/concepts.md`, "Words") with their meaning there; a term the user
  has not met yet is said in plain words, or linked, at its first use on the page.
- **A claim that can be checked, or nothing**: a number, a command, a file, a named behaviour; no
  vague hedge ("may help to", "in many cases", "it is worth noting") where the fact is known.
- **No filler or hype words**: a listed set, at least "seamless", "robust", "powerful",
  "leverage", "delve", "effortlessly", "comprehensive", "cutting-edge", "streamline", "unlock".
- **No "simply", "just" or "easily" before a step.**
- **No triplets of adjectives**, no "not only ... but also" rhetoric.
- **Bold only for a term at its definition or a label in a list item**; never scattered through
  prose. No emoji in headings or prose.
- **A sentence where a sentence says it**: no bullet list of fragments for one idea; a list for
  items of the same kind.
- **A figure or table where it reads better**: a flow of more than three steps, or a comparison of
  more than two items, gets a figure (an existing SVG) or a table.
- **Visual elements with a purpose**, as the site's extensions allow: `sphinx-design` tabs where a
  page gives the same step for Claude Code and GitHub Copilot; cards on the home and section
  indexes; an admonition (`note`, `warning`) only for what the reader must not miss, at most a
  few per page; every image with alt text saying what it shows.
- **Commands are copyable**: one command per code block line, in a fenced block with its language,
  the prompt sign left out (so `sphinx-copybutton` copies what runs).

The Driver may add rules found during the review (section 2), each with its example; it does not
drop one of the above.

### 2. The review of every site page, with the fixes

- In this CR, every page listed under "Today" (every `.md` under `docs/` that the site builds, at
  this CR's base) is reviewed against `docs/STYLE.md`, page by page, and fixed.
- The review is recorded as one table, one row per page: the page, the rules it broke (ids), and
  what was changed. The table goes in the CR's `work/verifier/evidence/` and is quoted in the PR
  body.
- A fix changes how a page says things, not what chantier does: no page added, removed, renamed or
  moved (the README and the release notes link the site's page paths), no image added or removed
  (docs-sphinx-rtd's image test holds). Within a page, sections may be reordered, merged or split,
  and prose may become a table, a figure reference or tabs, by the guide.
- A statement found false against the cards or the CLI at the base is not rewritten here: it is
  named in the PR's Known gaps, for an inbox item.
- The section `index.md` pages and the home are reviewed as pages too.

### 3. `AGENTS.md`: the rule for later CRs

One new line, next to the `DESIGN.md` rule, in this sense (the Driver keeps the file's wording
style):

> A change to a page of the docs site (under `docs/`, but not `docs/demo/`,
> `docs/release-notes/` or a `*-texts.md`) follows `docs/STYLE.md`: its Driver reads the guide
> first; the Inspector reads it and checks each changed page against it, each broken rule a
> `blocking` item that names the rule's id.

- `docs/STYLE.md` is written in backticks, never as `[...](docs/STYLE.md)` nor as a reference
  link.
- Whether a broken guide rule is `blocking`: yes. The rule makes the guide a project rule, and the
  Inspector's card (`inspector.md`, "Your part") holds "a project rule broken" as `blocking`; style
  the project has no rule on stays `minor`. No card changes.

### 4. `CONTRIBUTING.md` and the build

- `CONTRIBUTING.md:254`: the line on style keeps its words for code and adds that a docs page
  follows `docs/STYLE.md` (backticked path, no link). The "Repository layout" line for `docs/` (as
  `docs-sphinx-rtd` leaves it) names `STYLE.md` as the docs' style guide, backticked.
- `docs/STYLE.md` stays out of the site: `docs-sphinx-rtd`'s `docs/conf.py` excludes it in
  `exclude_patterns` (its spec did); if the merged `conf.py` does not, this CR adds `"STYLE.md"`
  there. A file under the source folder that is in no toctree and not excluded fails `just docs`
  (`-W`), so the build itself proves the exclusion.
- The repository's link test (`test_skill_and_references_links_resolve`, which after
  `docs-sphinx-rtd` reads `docs/**/*.md` minus the non-pages) reads `docs/STYLE.md` too if its glob
  takes it; any link in the guide must then resolve. No change to that test is required.

### 5. One test (reading the shipped files)

In `skills/chantier/scripts/cli/tests/test_plugin_files.py`, one test reads the repository's
shipped `AGENTS.md`, `CONTRIBUTING.md` and `docs/STYLE.md` at the head under test, and checks:

- `docs/STYLE.md` exists;
- `AGENTS.md` and `CONTRIBUTING.md` each name `` `docs/STYLE.md` `` in backticks;
- `chantier rules`' link walk does not reach it: `linked()` from
  `chantier.commands.rules`, run on the repository's `AGENTS.md` with the repository root and depth
  2 as `rules()` does (`seen` starting with `AGENTS.md`), leaves no path ending in
  `docs/STYLE.md` in `seen`.

It reads the shipped files only; no prepared text (no refusal case is needed). It adds well under
a second to `just test`.

## Decisions carried from `02-answers.md`

- Split from `docs-sphinx-rtd`; the user's words on style there hold here: sections 1 and 2
  (answer 2 of that CR: guide, review, examples; Diátaxis sections).
- The Inspector checks a changed docs page against the guide through one `AGENTS.md` rule
  (docs-sphinx-rtd Q2, A): section 3.
- The guide is a backticked path, not a link: sections 3, 4 and 5.

The points settled by the spec-writer (no user-visible behaviour) are in `02-answers.md`, "Settled
by the spec-writer (2026-11-18)".

## Evidence

- `just check` green in the worktree at the pushed head (it runs `just docs` with `-W`, the tests
  and the lint).
- The review table (section 2), every site page in it, in `work/verifier/evidence/` and quoted in
  the PR body.
- `chantier rules` run from the worktree: its output, quoted, does not list `docs/STYLE.md`.
- The new test passes at the head, reading the shipped files; shown failing once when
  `AGENTS.md`'s backticked path is turned into a Markdown link (then reverted).
- Two screenshots from `docs/_build/html`, before (base) and after (head), of one page that the
  review changed most, for the user to see the difference.
- Read the Docs' build of the PR green, with its preview link (set up by `docs-sphinx-rtd`).
- No host and default matrix: nothing here depends on the host or a configured value.
- No CI job changes. No `just eval-dry-run` owed (no change under the CLI's `src/` or
  `evals/kit/`), no `just mod` (no change to `hooks/` or `types/`). The pipeline's
  `just scenario (ubuntu-latest)` job runs on the PR as on every PR.

## Out of scope

- The README's prose (it keeps its presentation and links the site; `docs-sphinx-rtd`).
- `docs/demo/`, `docs/release-notes/`, the SVGs' `*-texts.md` and their figures.
- The cards (`skills/chantier/references/`), `CONTRIBUTING.md`'s prose beyond the lines above.
- A lint or script that checks the guide's rules mechanically (the user chose a guide, a review
  and examples).
- A new agent or card for docs review, and any change to the Inspector's card.
- New figures, new pages, page moves, the site's build or theme (`docs-sphinx-rtd`).
- Fixing a false statement found in a page (named in Known gaps, section 2).

## Open questions

None. The behaviour points were settled by the user on `docs-sphinx-rtd` and by the Chief of Staff
on the split.
