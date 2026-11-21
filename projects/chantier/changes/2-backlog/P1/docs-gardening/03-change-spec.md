# Garden the docs, the README and the SVGs after batch-30

The user's docs (`docs/`), the `README.md` and the SVG diagrams describe chantier as it was days
ago. This CR brings them in line with chantier as batch-30 leaves it, and with what merged since
each page was last brought up to date. It is the last CR of batch-30. Its specification names the
areas to check and the method; the exact list of fixes is fixed by its Driver, at its start,
against what has landed. It writes no behaviour: docs, pictures and diagrams only.

## Goal

In the user's words (2026-11-21): "il faudra que tu lances un gardening de la doc, du readme et
des svg qui sont plus à jour". A reader of the README and of `docs/`, and a viewer of the
diagrams, sees chantier as it runs at the end of batch-30: the right commands, states, roles,
arrows, folders and board views, and nothing that has been removed.

## Decisions carried from `02-answers.md`

1. **Scope (docs-garden-Q1, A).** Everything batch-30 delivers, plus what merged since the docs
   were last brought up to date. The CR runs after every other CR of batch-30, on top of the stack.
2. **The SVGs (docs-garden-Q2, A).** Fix the SVGs that are wrong (states, roles, arrows). Draw a new
   SVG only for a role or a view that no diagram shows (the user's example: the batch Kanban).
3. **Destination.** batch-30, last ("met doc gardening à la fin du batch en cours").
4. **Restatement.** The Driver fixes the exact list against what has merged when it starts; the
   specification does not pre-write the doc text.

## When the Driver starts, and what it reads

- **Order.** This CR is taken last in batch-30. Its branch sits on top of the batch's stack (batch-30
  runs in stack mode), so its base holds every other CR of the batch. The Driver starts when every
  other CR of batch-30 has handed back ready, is merged, or is cancelled or dropped. A CR that joins
  batch-30 later is still a batch-30 CR. It goes below this one, and the Driver checks that CR's
  areas at the next restack, as in "A CR below changes" below.
- **What counts as landed.** A CR of batch-30 counts when it is merged on `main`, or handed back
  ready and present in this CR's base. A CR cancelled or dropped out of batch-30 counts as not
  delivered: the docs describe none of its behaviour, and the Driver removes any text its own PR
  wrote ahead of time if that text reached the base.
- **The baseline, page by page.** A page's baseline is its last commit on `main` when the Driver
  starts (`git log -1 --format=%h -- <file>`). The Driver lists the commits after that baseline
  that change behaviour the page describes. These are commits under
  `skills/chantier/scripts/cli/src/`, `skills/chantier/references/`, `hooks/`, `config/`,
  `agents/` and `clients/`, plus the batch's CR branches below this one. It reads their subjects,
  and their diffs where the subject is not enough. The pages were last touched on different days
  (from 2026-11-14 for `docs/how-chantier-works-simple-*.svg`, `docs/batch-pace.svg` and
  `docs/release-driver.svg`, to 2026-11-21 for `README.md`, `docs/boards.md` and
  `docs/server-api.md`), so there is no single cut-off date.
- **The batch's CRs.** For each CR of batch-30, the Driver reads its `03-change-spec.md` (the
  planning surface's `projects/chantier/changes/4-batch/...`) and its PR's diff. Several of them
  update some docs themselves (for instance `425-factory-redefine` updates the README's factory
  section, `docs/use-cases*.md` and the `batch-lifecycle` pair; `428-drop-to-next-batch` updates
  the three `cr-*lifecycle` pairs and `docs/planning-folder.md`). This CR checks that those edits
  landed and hold together, and does not write them again. It fixes what the CRs left: other pages
  that say the same thing, the diagrams they did not touch, and the screenshots.
- **The inventory.** Before it edits anything, the Driver writes `work/garden-inventory.md` in the
  CR's folder. It has one row per page or picture checked: the file, its baseline commit, the
  commits and CRs that touch it, and a verdict (`holds`, `fixed`, `new`, or `out of scope`, with
  one line of why). The inventory is the CR's working list and its evidence. A page that holds is
  listed too, so the Verifier sees that it was read.

## What changes, area by area

The lists below are where to look, with the changes known when this specification was written.
They are a starting point, not the fix list: the inventory decides the list.

### 1. The README (`README.md`)

Check every section against what landed: "How Chantier works", "Planning modes", "Batch modes",
the section that replaces "Factory mode" (from `425-factory-redefine`: "Running batch or next
batch"), "What a batch costs", "Change Requests Lifecycle", "Detailed lifecycle", "Releases",
"The CR board" (the picture and its caption, line 234 at this specification, after the batch page's
compaction and its Kanban), "Install" (the allow rules of preflight's P10, from
`432-permissions-bypass`), "Use" (the table of what you say and what happens: for instance the
`our long gate is npm test` row, against `gate-hold-narrowing`'s `long_gate.commands` in
`chantier.yaml`, and the `drop CR-103` row, against `428-drop-to-next-batch`'s destinations) and
"More" (one link per page, a new page included).

### 2. The reference pages (`docs/*.md`)

Each page is read against the behaviour that landed. Known areas:

- `docs/web-board.md` and `docs/boards.md`: the board bound to `127.0.0.1` by default,
  `board.host: network`, `board --new-key` and the 30-day cookie (`426-board-exposure`); the
  backlog's last column split into running batch and next batch (`427-board-running-batch-lane`);
  the server reading the planning files on OS notifications, watchers subscribing, and the board a
  watcher starts stopping after its last client (`429-board-fingerprint-cache`); the batch page's
  Kanban / Graph toggle, Kanban by default (`board-batch-kanban`); the mode band and the legend line
  moved into the top rows (`board-batch-compact`); a batch CR's card showing its batch folder
  (`board-batch-chip-stale`).
- `docs/server-api.md`: the key and cookie (`426`), the subscriptions and the file watching
  (`429`), the running-batch move target (`427`), `lease hold` (`gate-hold-narrowing`), and any
  protocol change the batch made (protocol 1 takes additions only).
- `docs/forge-connectors.md` and `docs/planning-folder.md`: the hub, watchers and server lifecycle
  (`429`); `order drop`'s destinations (`428`); the configuration keys the batch added
  (`board.host`, `long_gate.commands`).
- `docs/gates.md`: the long gates named in `chantier.yaml`, `gate` refusing a free command, and
  `lease hold` running nothing (`gate-hold-narrowing`).
- `docs/use-cases.md`, `docs/use-cases-foreman.md`, `docs/use-cases-direct.md`: running batch or
  next batch (`425`); the Foreman parking a CR stuck on an outside wait (`430-park-live-cr`);
  `order hold` and `unhold` on a live CR in every mode (`431-hold-live-cr`); a stack keeping its
  shape (`stack-shape-guard`) and checked as a git chain (`stack-git-chain`).
- `docs/tutorial-claude-code.md` and `docs/hosts.md`: the P10 allow rules with real paths
  (`432`); how the board is reached from a phone (`426`).
- `docs/agents-and-models.md`, `docs/costs.md`, `docs/planning-modes.md`,
  `docs/release-process.md`: read for anything the batch or the earlier merges changed.
- Merged before batch-30 and named by no page at this specification (to confirm, not assumed):
  `chantier wait` (typed waits, 9b55b0a4), `chantier access` (daec1986), leases (`--lease`,
  `lease renew`, e461ffd2) and `order hold` on a ready CR (f9087d67). Each goes where a reader
  would look for it, or the inventory says why it stays in the cards only.

`docs/release-notes/` is history and does not change. `docs/demo/` changes only as far as the
screenshots need (section 4).

### 3. The SVG diagrams (`docs/*.svg` and their `*-texts.md`)

Twelve diagrams besides `docs/logo.svg`, each with a `-texts.md` companion except `batch-pace`
(which has none at this specification): `batch-lifecycle`, `batch-modes`, `batch-pace`,
`cr-folder-lifecycle`, `cr-lifecycle`, `cr-lifecycle-line`,
`cr-lifecycle-simple`, `how-chantier-works`, `how-chantier-works-simple-direct`,
`how-chantier-works-simple-foreman`, `planning-modes`, `release-driver`.

- **Fix what is wrong.** States (parked, held), roles, arrows, commands and folders, against what
  landed. Known areas: the factory batch in `batch-lifecycle` (`425`); `order drop` going to
  `1-inbox/` in `cr-lifecycle`, `cr-lifecycle-simple` and `cr-folder-lifecycle` (`428`: P1-P4,
  `3-ready`, trash); park and hold in `batch-lifecycle`, `cr-lifecycle` and `batch-modes` (`430`,
  `431`); the grilled-enough step's destination choice in the `cr-lifecycle` pairs and
  `how-chantier-works*` (`425`); the server, hub and watchers wherever a diagram draws them
  (`429`).
- **One text, two files.** A diagram's `-texts.md` holds its words (the description, the header,
  the legend, the lanes), and the SVG's `<title>`, `<desc>` and visible text say the same. A fix
  goes into both. The Driver also fixes any drift between the two that it finds. For instance, at
  this specification `cr-folder-lifecycle.svg`'s `<desc>` says ".agents/changes/" where its
  `-texts.md` says "the planning folder (.agents/changes/ or an external surface)", and the
  `<desc>` lacks the texts' sentence on the archive in the PR.
- **A new SVG only for what is missing.** It is drawn only for a role or a view that no diagram
  shows. The batch Kanban (`board-batch-kanban`) is the user's example. The Driver draws it if no
  diagram already shows a batch CR's three folders (`1-pending`, `2-actives`, `3-done`) as the
  board draws them; the inventory names the check either way. A new SVG:
  - follows the existing ones: the same font stack, palette, emoji legend and monospace commands;
  - comes with its `-texts.md`;
  - is linked from the README or a page of `docs/`.
- An SVG stays hand-written, as today. No generator is added.

### 4. The screenshots (`docs/web-board/*.png`)

The batch page's Kanban, its compaction and its chips, and the backlog's running-batch lane,
change what `docs/web-board/batch-*.png` and `triage-*.png` show. A screenshot that a batch-30 CR
already retook and that still matches is kept. The others are retaken with `just docs-screenshots`
(`scripts/docs_screenshots.py`, from `docs/demo/`). If the script needs a new view (the batch
Kanban as the default, the graph behind its toggle) or demo data (CRs in all three batch folders),
the Driver adds it there. If `just docs-screenshots` cannot run on the Driver's machine (no
Chromium, no network for Playwright), the Driver stops and says so: no picture is made another way.
The pane screenshot rule (AGENTS.md) does not apply: this CR changes neither `hooks/register.tsx`
nor `status.py`.

## Out of scope

- Any behaviour change, in the CLI, the cards, the hooks or the web client. A doc that cannot be
  made true without one goes back to the Foreman as a finding.
- `AGENTS.md` (the project's rules, kept by each CR that changes a rule), the cards
  (`skills/chantier/references/`), `clients/web/DESIGN.md`, `scenario/README.md` and the eval docs
  (`evals/`).
- `CONTRIBUTING.md` (see the open question).
- `docs/release-notes/` (history; pinned to their tags).
- The behaviour of a CR cancelled or dropped out of batch-30.

## Evidence

- `work/garden-inventory.md`: every page and picture of sections 1 to 4, each with its baseline,
  the commits and CRs that touch it, and its verdict.
- `just check` passes at the head. Among its tests, `test_skill_and_references_links_resolve`
  (`skills/chantier/scripts/cli/tests/test_plugin_files.py`) reads the shipped `README.md` and
  `docs/*.md` at the head under test and checks that every relative link resolves. A new page or
  SVG is linked, so it is covered.
- For each changed or new SVG, at the head, from the shipped files (no copies):
  - it parses as XML (`python -I -c "import xml.etree.ElementTree as E,sys; E.parse(sys.argv[1])"
    <file>`);
  - its `<desc>` equals the description paragraph of its `-texts.md`, compared by a short script
    the Driver keeps in `work/`, whose output goes in `work/verifier/evidence/`;
  - it is rendered to a PNG at its `viewBox` size (Chromium through Playwright, as
    `docs_screenshots.py` uses), saved in `work/verifier/evidence/`, and looked at for overlapping,
    clipped or overflowing text.
- A search of `README.md` and `docs/*.md` (`*-texts.md` and `*.svg` included) at the head for the
  words that batch-30 removed or renamed: `factory`, `order factory`, `order drop` with `1-inbox`,
  `0.0.0.0`, and any other word the inventory names. Each hit that remains is listed with why it
  holds.
- Retaken screenshots: the `just docs-screenshots` run's output, and the PNGs in the PR's
  Deliverables, captioned with the head's SHA (seven characters).
- Gates (AGENTS.md): a docs-only change owes no `just scenario` before its PR and no
  `just eval-dry-run`. If the Driver changes `scripts/docs_screenshots.py`, that is still not under
  the CLI's `src/` or `evals/kit/`. As the CR on top of batch-30's stack, it passes `just scenario`
  locally (`chantier gate`) at its head before the user merges: the batch's Windows coverage. The
  local run moves to it when it joins on top.

## A CR below changes

If a CR below this one in the stack gets a new round after this CR started, the restack brings its
new head. The Driver re-reads that CR's diff, re-checks the rows of the inventory it touches, and
fixes them in a new commit before it hands back.

## Open questions

1. **`CONTRIBUTING.md`.** Its "How the project is built" section repeats much of what batch-30
   changes (the board, the hub and watchers, `gate`, `lease hold`). It is neither in `docs/` nor
   the README, so the answers leave it out. Should the gardening check it too, or does it stay with
   each CR that changes a rule?
