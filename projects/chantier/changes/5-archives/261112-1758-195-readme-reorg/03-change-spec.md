# Change Specification: README reorganisation

## Goal

The user, in their words: "the README is very complicated". Make `README.md` read in one go:
an introduction that says what a Change Request is and how chantier works in batches, why one
picks direct or Foreman mode, and that chantier respects the project's rules; the "How chantier
works" diagrams in a new order; and the detailed end moved to pages under `docs/`, with a link
left in the README. "The rest (sections, images) is good": it stays as it is. No content is lost.

Timing: run after the reproducible-evals work (batch-13) is done.

## What changes

All paths are from the repository's root. Repository text in English; files UTF-8 without a
byte-order mark.

### 1. `README.md`, the introduction (lines 1-16 today)

Keep the title and the tagline ("The construction site for your Software Factory."). Rewrite the
bullet list so it says, in this order:

- **Change Requests beside your tracker.** Keep today's content (one more level over the
  tracker's issues; small requests accepted and prioritised here; the `[more](#change-requests-lifecycle)`
  link) and add: a Change Request is a folder whose content varies, from one line of text to
  several HTML prototypes; the agents read it and find the request's intent. Then **one sentence
  alone, with no list of examples**: CRs are fungible in the plan, they can be handled, split,
  and so on.
- **Working in batches** (new bullet): chantier is not continuous delivery (1 intent = 1 PR =
  1 release). It is n CRs → m PRs (normally close to n) → p batches (1, 2, 3…) → 1 release.
- **One person to talk to.** Unchanged.
- **Direct or Foreman.** Keep what it says (the Chief of Staff steers a batch itself, or a nested
  Foreman session does; a CR added while the batch runs is queued and taken when a slot frees)
  and add why pick one: direct mode is simpler to use remotely, from a phone; Foreman mode lets
  you grill future topics with the Chief of Staff naturally while the Foreman runs the batch.
- **Respect the project's rules.** Replaces "Zero configuration". Say: your changes must be able
  to land without chantier; chantier is there to industrialise. Keep the rest of today's bullet:
  your `AGENTS.md`, and an optional `chantier.yaml` at the project's root (the agent and model of
  each role, the skills it needs), are the only configuration; everything chantier writes is
  Markdown and JSON in the planning folder (`.agents/changes/` or the project's folder of an
  [external planning surface](https://github.com/gsemet/chantier/blob/main/docs/planning-modes.md)).

### 2. `README.md`, "How Chantier works" (lines 18-36 today)

Order of the three diagrams: the detailed one (`docs/how-chantier-works.svg`) first, then Foreman
mode (`docs/how-chantier-works-simple-foreman.svg`), then direct mode
(`docs/how-chantier-works-simple-direct.svg`). Each keeps its caption paragraph (the Foreman one
before its image, the direct one before its image). The "The same, in detail:" lead-in no longer
fits: replace it with a lead-in that introduces the detailed diagram first and the two simpler
views after it. Keep the paragraph "The difference that matters most…", after the two simple
diagrams. No SVG file changes.

### 3. `README.md`, what stays unchanged

"Planning modes", "Batch modes", "Change Requests Lifecycle", "Detailed lifecycle", "Releases",
"What is Chantier?", "Install", the "Use" table, "Repository layout" and "Develop" stay, with
their images and text, except the link edits below.

### 4. The detailed end moves to `docs/`

Move each of these blocks out of `README.md`, verbatim, to a new page under `docs/`. The only
edits allowed in the moved text are: a top-level `#` title per page, heading levels lowered by
one where needed, relative links rewritten for the new location (`docs/x.svg` → `x.svg`,
`#batch-modes` → `../README.md#batch-modes`, `#the-remote-board` → the new page's link,
`CONTRIBUTING.md` → `../CONTRIBUTING.md`, and so on), and a short opening line saying what the
page covers.

| README block today | New page |
| --- | --- |
| "### The CR board (Claude Code)" and "### The remote board" (lines 231-265) | `docs/boards.md` |
| "### Your gates" (lines 267-295) | `docs/gates.md` |
| "### Your own agents" and "### Models", with its "No fallback" paragraph (lines 297-357) | `docs/agents-and-models.md` |
| "### Change Request lifecycle" (the planning folder's layout, the external layout, what is published, STATUS files, worktrees, pause and close; lines 359-427) | `docs/planning-folder.md` |
| "## Supported hosts" (hosts, forges, Windows; lines 429-464) | `docs/hosts.md` |
| "## Costs and budgets" (lines 466-491) | `docs/costs.md` |

`docs/planning-folder.md` links to [planning modes](https://github.com/gsemet/chantier/blob/main/docs/planning-modes.md) for the full account
of an external surface; it does not merge into `docs/planning-modes.md` (that page keeps its own
text, unchanged).

### 5. The links left in `README.md`

- After the "Use" table, a short section (for example "## More") with one line per moved page:
  the page's link and what it holds (the CR board and the remote board; your gates; your own
  agents and the models; the planning folder's layout and a batch's pause and close; supported
  hosts, forges and Windows; costs and budgets).
- In the "Use" table, the row "our long gate is `npm test`" links to `docs/gates.md` instead of
  `#your-gates`.
- "Repository layout": the `docs/` line also names the reference pages (for example "diagrams,
  the user docs (tutorial, use cases, reference pages), release notes").
- No README link points to an anchor that no longer exists.

### 6. Links elsewhere that point at a moved section

- `docs/tutorial-claude-code.md` line 53-54: "The README's [Your gates](https://github.com/gsemet/chantier/blob/main/README.md#your-gates)"
  becomes a link to [Your gates](https://github.com/gsemet/chantier/blob/main/docs/gates.md) (wording adjusted, same meaning).
- The cards name the README's moved sections (see Decisions):
  `skills/chantier/references/chief-of-staff.md` line 76 ("(README, "Your gates")"),
  `skills/chantier/references/init.md` line 76 ("Point to the README's "Your gates""),
  `skills/chantier/references/hosts/claude-code.md` line 371 ("`README.md`, the CR board" and
  "documented in the README"). Each becomes the new page (`docs/gates.md`, `docs/boards.md`),
  the reference only, nothing else in the card.

## Out of scope

- Any change to the SVGs, to the `*-texts.md` diagram sources, to `docs/planning-modes.md`,
  `docs/use-cases*.md` (they hold no link to a moved anchor) or the release notes.
- Rewriting the moved text: it moves as it is (see the allowed edits above).
- "What is Chantier?" and the other sections that stay: no rewrite.
- The CLI, the agents, the scenario, the evals.
- The tagged README of a past release (`docs/release-notes/…` links to `v0.8.0`): unchanged.

## Evidence

- `just check` passes (its `test_skill_and_references_links_resolve` checks every relative link
  of `README.md`, `docs/*.md` and the cards resolves to a file).
- No content lost: a short check (a script in the CR's `work/` folder, or by hand) that every
  non-blank line of the README's removed blocks (lines 231-491 of today's README, at the base
  commit) is found in one of the six new pages, modulo the link rewrites listed in section 4.
- No dangling anchor: a search of the repository (outside `.agents/` and the release notes) for
  `README.md#your-gates`, `#your-gates`, `#the-remote-board`, `#the-cr-board`,
  `#your-own-agents`, `#models`, `#supported-hosts`, `#costs-and-budgets`,
  `#change-request-lifecycle` returns nothing; `#change-requests-lifecycle` and `#batch-modes`
  still resolve in the README.
- The README read top to bottom: the introduction holds the five bullets of section 1, the CR
  one with the fungibility sentence alone; the three diagrams are in the order detailed,
  Foreman, direct.
- Long gate: `just scenario` passes at the PR's head, since the cards' references change
  (Decisions, 1).

## Decisions

1. The cards' references (section 6) are updated in this CR, so no card points at a section
   that moved; the change then touches the cards, and the long gate (`just scenario`) runs
   before the PR (Chief of Staff, 2026-11-12).
