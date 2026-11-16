# Change Specification: diagrams-modes-griller

This CR sets chantier's presentation straight:

- the docs diagrams show the two steering modes as two separate pictures, and show the Griller,
  marked optional, wherever the Chief of Staff appears;
- the README, the docs and the Chief of Staff's first-turn introduction carry the same four
  messages;
- the release template points at the PRs' Deliverables section.

Sources, in order of authority:

- `02-answers.md`: every section, among them "Scope widened" and "Grill of the widened scope"
  (2026-11-10).
- `intake/request.md`: the diagrams, the user's words of 2026-11-10.
- `intake/request-readme-intro.md`: the release template and the README intro. It was the inbox
  item `release-template-deliverables`, merged into this CR.

`multi-session-chief-of-staff` is merged on `main` (PR #92, archived as
`4-archives/261110-0940-153-multi-session-chief-of-staff/`). It created the Griller, the
`/chantier:griller` and `/chantier:chief-of-staff [direct]` skills and the two modes' wording, and
it rewrote the README intro, `SKILL.md`, `session-start.md`, `griller.md` and `chief-of-staff.md`.
This CR starts from that head. Where a diagram or a text of this CR differs from the cards on
`main`, the cards win and the diagram or text changes.

This CR changes docs and two cards' text: `references/session-start.md` section 4 and
`references/release-template.md`. It changes no CLI, scenario, test, agent file or board.

## Goal

In the user's terms:

- In the README, two variants of the main diagram, one **without** a Foreman (direct mode) and
  one **with** a Foreman, instead of one picture with two arrows.
- Next to them, one plain sentence on how the modes differ: once a batch runs in direct mode, a
  CR, specified or not, can join only when every other CR is handled and the batch is paused; in
  Foreman mode a CR can join while the batch runs.
- In the detailed diagram, the Foreman box is split in two, one half per mode:
  - **Foreman:** a nested session. Not recommended in remote, but it allows a fully dynamic and
    natural conversation with the Chief of Staff.
  - **Direct:** the Chief of Staff plays the Foreman's role. It works in a remote session but
    cannot grill during the implementation: use a dedicated Griller session.
- The **Griller** appears on the other diagrams, marked optional.
- The README, the docs and the Chief of Staff's first-turn introduction keep the four important
  messages:
  1. **CR and tracker.** A CR is one more level of abstraction over a tracker's issues (Jira,
     GitHub, GitLab…). It lets small requests outside the tracker be accepted and prioritised. The
     tracker holds the strategic vision, external requests and long-term planning.
  2. **One person to talk to.** That person is the Chief of Staff. Nothing starts without the
     user's go, and the user merges.
  3. **Direct or Foreman.** These are the two modes. Each says when a CR may join a running batch.
  4. **Zero configuration.** `AGENTS.md` is the only configuration. Everything chantier writes is
     Markdown and JSON in `.agents/changes/`.
- The planning area named is only the one in the project, `.agents/changes/`.
- The release template finds the screenshots in the merged PRs' Deliverables section.
- The docs and the other diagrams agree with all of this.

## Decisions carried from `02-answers.md`

| # | Decision | Where |
| --- | --- | --- |
| A1 | This CR owns the SVGs and their `docs/*-texts.md` companions, `batch-lifecycle-texts.md` included. `multi-session-chief-of-staff` left them out and is merged; the diagrams draw what it shipped | Areas 1-5 |
| A2 | No dependency on `claude-code-config` or `pr-details-fold` (they touch no SVG). `landing-page` and `docs-sphinx-rtd` reuse the diagrams later | Out of scope |
| A3 | README: both variants of the simple diagram, one under the other, **direct first, then Foreman** (the user's choice), each with one line saying when to pick it. Direct: works in remote, grill in a Griller session. Foreman: a nested session, at the desktop, natural conversation with the Chief of Staff | Areas 1, 5 |
| A4 | The Griller, marked optional, on every diagram where the Chief of Staff appears: both how-it-works diagrams (the two simple variants and the detailed one), the simple and detailed CR lifecycles, and the CR folder lifecycle. **Not** on the batch lifecycle or the batch pace | Areas 1, 2, 3, 4 |
| A5 | The detailed diagram's Foreman box is split in two, one half per mode, using the request's texts | Area 2 |
| A6 | The drawings are reviewed in the PR, from PNG renders; there is no prototype step first. The Griller's emoji (🔥 proposed) and the label of the split box's band are settled in that review | Review, Evidence 6 |
| A7 | In `batch-lifecycle.svg`, "grill in another session of yours" becomes "grill in a Griller session", with no box drawn, in its `<desc>` and in `batch-lifecycle-texts.md` too | Area 5 |
| A8 | README, beside the two simple diagrams, one plain sentence on the difference: in direct mode a CR (specified or not) joins only once all the others are handled and the batch is paused; in Foreman mode a CR may join while the batch runs (`order add`) | Area 5 |
| B1 | The inbox item `release-template-deliverables` is merged into this CR. `release-template.md` points at the merged PRs' Deliverables section, not Impacts | Area 8 |
| B2 | The README, the docs and the Chief of Staff's first-turn introduction (`session-start.md` section 4) are set straight and keep the important messages | Areas 6, 7, 9 |
| B3 | The CR/tracker explanation goes in the README's Change Requests section, replacing the paragraph "A "Change Request" is an idea, a bug…". It does **not** go at the top of the README (the user's choice over the recommendation) | Area 6 |
| B4 | The CR/tracker message: a CR is one more level of abstraction over a tracker's issues (Jira, GitHub, GitLab…) that lets small requests outside the tracker be accepted and prioritised. The tracker holds the strategic vision, external requests and long-term planning | Areas 6, 7 |
| B5 | Planning area: only the in-project one (`.agents/changes/`). The external planning surface is **not mentioned** anywhere this CR writes ("Ne pas en parler"). The P1 `planning-repo` adds it when it ships | Areas 6, 7, 9, Evidence 7 |
| B6 | The introduction, in the README and in the Chief of Staff's first turn, keeps all four messages: CR and tracker; one person to talk to (the Chief of Staff; nothing starts without the user's go; the user merges); direct or Foreman (the two modes, and when a CR may join a running batch); zero configuration (`AGENTS.md` only; Markdown and JSON in `.agents/changes/`) | Areas 6, 7 |

## The words drawn and written (from `multi-session-chief-of-staff`, on `main`)

Use these words. They can be shortened to fit but never contradicted:

- **Griller:** another session of yours that grills, triages and specifies the inbox and the
  backlog beside the Chief of Staff. It never opens, steers or closes a batch, is usually short,
  and is optional. It is started by `/chantier:griller`.
- **Chief of Staff:** the only session that opens and runs batches. It is started by
  `/chantier:chief-of-staff` (Foreman mode), by `/chantier:chief-of-staff direct` (direct mode),
  or by the router `/chantier:chantier`, which asks.
- **Foreman mode:** one nested Foreman session per batch steers it. The Chief of Staff's session
  stays free to grill, file, triage and discuss while the batch runs (dynamic and natural), and a
  CR may join the batch while it runs (`order add`). It needs a host that can start a nested
  session (Claude Desktop, a Copilot SDK host) and is not recommended in a remote session.
- **Direct mode:** there is no Foreman session; the Chief of Staff steers the Drivers itself. It
  works in a remote session, in any Claude Code entry point and in a Copilot agent session. While
  the batch runs, that session holds no grill, triage or discussion (new ideas go to the inbox):
  grill in a Griller session. No CR joins the batch until every other CR is handled and the batch
  is paused. A release CR is the one exception.
- The seat (`seat.json`), the session titles and the hand-over are not drawn: they are
  implementation details of that CR.

Emoji: the Chief of Staff stays 🤵 and the Foreman stays 👷. The Griller gets one emoji, the same
on every diagram and companion. Draw it with 🔥 (a grill). The PR review settles it (A6), and a
change there is applied everywhere at once. An optional element keeps the existing optional style,
one of:

- the dashed yellow box of "➕ your agents" (`fill="#fef9c3" stroke="#ca8a04"
  stroke-dasharray="5 3"`);
- a dashed outline in the box's own colour.

Either way, the word "optional" is drawn.

## The rules every SVG follows

These are the rules CR-150 docs-lifecycle set, unchanged:

- The same style as the existing SVGs:
  - the `font-family` stack with the emoji fonts and a `#f8fafc` background;
  - an emoji header: a `<text>` title at font-size 30 and a subtitle at about 17.5;
  - the slate, blue (`#1e3a8a`) and orange (`#ea580c`) palette;
  - a `<title>` and a `<desc>`;
  - UTF-8 and plain SVG: no script, no external reference, written by hand like the existing
    ones.
- Each SVG has a companion `docs/<name>-texts.md`, in the pattern of
  `docs/cr-lifecycle-simple-texts.md`:
  - a `# <title>` line;
  - one paragraph equal to the SVG's `<desc>`;
  - one `## <part>` section per area of the drawing, each with a ```` ```md ```` block holding
    every visible text of that area, as drawn.
- An SVG and its companion change together:
  - every drawn text is in the companion;
  - every companion text is drawn;
  - `<desc>` equals the paragraph.

  `batch-pace.svg` has no companion and still gets none.
- No text overlaps another or runs out of its box, and arrows end on their box's edge.
- Words: a batch is only **running**, **paused** or **closed**; never "land" or "epoch".

## Area 1: the simple diagram becomes two variants

Remove `docs/how-chantier-works-simple.svg` and `docs/how-chantier-works-simple-texts.md` with
`git rm`. The README's line 11 is their only reference. Create the two files below, each with its
companion.

### `docs/how-chantier-works-simple-direct.svg` (+ `-texts.md`)

- Title and header:
  - `<title>`: "How chantier works (simple, direct mode)".
  - Header: "🏗️ How chantier works", with a subtitle saying it is direct mode, e.g. "Direct
    mode: the Chief of Staff steers the batch itself."
- No nested-session lane: the lanes are MAIN SESSION, DRIVERS and WORKERS. The Driver may name
  the first band "YOUR SESSIONS" if the Griller sits in it. Either way, the drawing must not make
  the Griller look like part of the Chief of Staff's session.
- The top of the picture:
  - You ⇄ 🤵 Chief of Staff, named `/chantier:chief-of-staff direct`. Its box says "your session
    · plays the Foreman's role" or similar, with a "direct mode" pill where today's "Foreman
    mode" pill is.
  - 📐 AGENTS.md and ✍️ Spec-writer stay as they are today.
- The Chief of Staff starts the four Drivers directly, with solid arrows like the Foreman's today.
- 🔥 Griller, optional, beside the Chief of Staff and linked to You. Its text: "another session of
  yours · grills and specifies while the batch runs · `/chantier:griller`". In this variant the
  Chief of Staff's session holds no grill while the batch runs, and the Griller's text says so.
- These stay as they are today:
  - the Drivers;
  - the workers bus;
  - the workers;
  - the "Any role can run your own agent" note.
- `<desc>`: today's simple `<desc>`, rewritten for direct mode. It says there is no Foreman
  session, that the Chief of Staff starts the Drivers, and that an optional Griller session grills
  while a batch runs.

### `docs/how-chantier-works-simple-foreman.svg` (+ `-texts.md`)

- Title and header:
  - `<title>`: "How chantier works (simple, Foreman mode)".
  - The same header, with a subtitle such as "Foreman mode: a Foreman session steers each
    batch."
- Start from today's simple diagram. Remove its dashed direct-mode path
  (`M404,230 V266 H240 V430`) and its four-line note "🤵 direct mode: …".
- Keep everything else:
  - the lanes;
  - You, AGENTS.md and the Spec-writer;
  - orders and asks;
  - the Foreman box with its "Foreman mode" pill;
  - the Drivers and the workers.
- The Chief of Staff box shows `/chantier:chief-of-staff`. Its text may add that it stays free to
  talk while the batch runs.
- 🔥 Griller, optional, placed as in the direct variant. Its text drops the "while the batch runs"
  reason, since here the Chief of Staff grills too: "another session of yours · grills and
  specifies the backlog · `/chantier:griller`".
- `<desc>`: today's, without the direct-mode clause and with the optional Griller added.

Both variants keep the same width and the same positions for what they share, so they read as one
picture in two states when shown one under the other in the README.

## Area 2: `docs/how-chantier-works.svg` (+ `how-chantier-works-texts.md`)

- **Split the Foreman box into two halves**, side by side where the box is today (x 270–710, in
  the NESTED SESSION band). Each half has its title and two or three short lines:
  - Left, orange: **👷 Foreman mode**:
    - "a nested session · Opus 5.5 · one per batch";
    - "fully dynamic, natural talk with the Chief of Staff";
    - "not recommended in remote".
  - Right, blue: **🤵 direct mode**:
    - "the Chief of Staff plays the Foreman's role";
    - "works in a remote session";
    - "no grill while the batch runs: use a 🔥 Griller session".
- Remove the dashed direct path (`M300,230 V242 H250 V400`) and the four-line note on the left,
  "🤵 direct mode: the Chief of Staff steers the batch itself, no Foreman session". The split box
  now says this.
- Connections:
  - The 📋 orders / 🙋 asks arrows go to the Foreman half only.
  - The direct half gets one line from the Chief of Staff marked as the same session (e.g. "same
    session"), so a reader does not take it for a nested session.
  - The drivers bus starts from both halves, one drop from each to the bus at y 404.
- The band's label: "NESTED SESSION" may stay only if the direct half is clearly not nested.
  Otherwise, rename the band (e.g. "STEERING"). The Driver draws one choice, and the PR review
  settles it (A6).
- 🔥 Griller, optional:
  - placed in the top area beside the Chief of Staff, linked to YOU. It goes in the free space to
    the Chief of Staff's left or above it, near YOU;
  - shows `/chantier:griller` and one line: "another session of yours · grills and specifies the
    backlog, beside the Chief of Staff".
- The Chief of Staff box names `/chantier:chief-of-staff` (and `direct`).
- Unchanged:
  - the CR box, AGENTS.md, the Drivers, the workers and the harness note;
  - the storage and the CLI column;
  - the Spec-writer. It may also say "started by the Chief of Staff or a Griller" if it fits;
  - the "Coding Agents" box, whose two lines stay true. Its "direct mode" line may add "remote".
- `<desc>` and the companion's paragraph:
  - describe the two modes as above;
  - replace "(Foreman mode), or steers the batch itself in direct mode, with no Foreman session";
  - add the optional Griller.

## Area 3: the CR lifecycle diagrams

### `docs/cr-lifecycle-simple.svg` (+ `-texts.md`)

- Legend: add "🔥 Griller (optional)".
- The PLAN phase title is today "PLAN · 🤵 Chief of Staff, with you". Add the Griller, e.g. "PLAN ·
  🤵 Chief of Staff, or a 🔥 Griller (optional), with you".
- The Griller may do both Triage ("🤵 with 👤 you") and the Spec box ("✍️ spec-writer writes
  …"). Mark it where it fits, e.g. "🤵 or 🔥 with 👤 you".
- BUILD stays "👷 Foreman runs the batch / or 🤵 the Chief of Staff, in direct mode". There is no
  Griller in BUILD or MERGE.
- `<desc>`: "you triage it with the Chief of Staff (or a Griller, optional) …; the spec-writer,
  started by the Chief of Staff or a Griller, …".

### `docs/cr-lifecycle.svg` (+ `cr-lifecycle-texts.md`)

- Legend: add "🔥 Griller (optional)" beside "🤵 Chief of Staff".
- The Griller goes in the PLANNING lane only:
  - Triage ("with you");
  - the spec loop: "🤵 starts it on your word" becomes "🤵 or 🔥 starts it on your word";
  - the clarification loop: "🤵 grills you" shows that the Griller may grill too;
  - if it fits, a small note in the lane: "🔥 Griller, optional: another session of yours, same
    planning, never a batch".
- From "🤵 opens the batch" onward, everything stays with the Chief of Staff or the steering
  session, with no Griller there:
  - opening the batch;
  - being asked by the Foreman;
  - orders;
  - the report and the cost.
- `<desc>` and the companion's paragraph: the triage, grill and spec sentences name the optional
  Griller beside the Chief of Staff.

## Area 4: `docs/cr-folder-lifecycle.svg` (+ `-texts.md`)

No Chief of Staff is drawn on this diagram today, but A4 puts the Griller wherever the planning
roles are.

- Add one small note under the 1-inbox and 2-backlog stages, next to `01-intent.md`,
  `02-answers.md` and `03-change-spec.md`. It may be one note for both stages or one each.
- The note reads: "written with you by 🤵 the Chief of Staff, or a 🔥 Griller (optional)".
- Nothing else changes.
- `<desc>` and the paragraph gain the same clause.

## Area 5: the README's diagrams and the batch lifecycle

### "## How Chantier works" (README lines 9-15 today)

Replace the single simple image with the following, in this order:

```md
## How Chantier works

**Direct mode** (`/chantier:chief-of-staff direct`): the Chief of Staff steers the batch itself;
it works in a remote session; to grill while a batch runs, open a Griller session.

![How chantier works, in direct mode](docs/how-chantier-works-simple-direct.svg)

**Foreman mode** (`/chantier:chief-of-staff`): a nested Foreman session steers each batch, at the
desktop; your Chief of Staff stays free for a natural, dynamic conversation while it runs.

![How chantier works, in Foreman mode](docs/how-chantier-works-simple-foreman.svg)

The difference that matters most: once a batch runs in direct mode, a new CR, specified or not,
joins it only when all the other CRs are handled and the batch is paused; in Foreman mode a CR
can join while the batch runs.

The same, in detail:

![How chantier works](docs/how-chantier-works.svg)
```

The wording may change, but each part must stay:

- direct mode comes first, with one line each on when to pick a mode (A3);
- each image's alt text names its mode;
- the difference sentence is plain and sits with the two simple diagrams, before the detailed one
  (A8).

### `docs/batch-lifecycle.svg` (+ `batch-lifecycle-texts.md`)

- No Griller box and no "optional" mark (A4).
- In the direct-mode band, the third line "grill in another session of yours, and file your ideas
  to the backlog" becomes "grill in a Griller session, and file your ideas to the backlog" (A7).
- Make the same change in the other places that carry it:
  - in `<desc>`, "so you grill in another session of yours" becomes "so you grill in a Griller
    session";
  - in the companion's paragraph;
  - in the companion's "Two steerings" block.
- Nothing else changes.

`docs/batch-pace.svg` is untouched.

## Area 6: the README's introduction and Change Requests section

### The introduction (README lines 1-7 today)

Keep the `# Chantier` title and the tagline "The construction site for your Software Factory."
Replace the paragraph of lines 5-7 with a short introduction that carries the four messages
(B6), each in one or two sentences, before "## How Chantier works". This is the recommended text,
whose wording the Driver may adjust:

```md
- **Change Requests beside your tracker.** A Change Request (CR) is one more level over your
  tracker's issues: small requests are accepted and prioritised here, without entering the
  tracker ([more](#change-requests-lifecycle)).
- **One person to talk to.** You talk to the Chief of Staff, in your own session. It keeps the
  backlog and asks the questions a change needs. Nothing starts without your go, and you merge
  the pull requests.
- **Direct or Foreman.** The Chief of Staff steers a batch itself (direct mode), or a nested
  Foreman session steers it (Foreman mode). In Foreman mode a CR can join a running batch; in
  direct mode, only once the batch is paused.
- **Zero configuration.** Your `AGENTS.md` is the only configuration. Everything chantier writes
  is Markdown and JSON in `.agents/changes/`, in your project.
```

What the introduction must hold:

- **The four messages, in this order.** The one-line nested-session context ("Modern coding
  agents … provide nested sessions") may stay as a lead-in sentence if it fits.
- **The anchor.** The link to the Change Requests section must resolve. It is checked under
  Evidence 4.
- **The optional Griller.** It may be named in the second message as "optional: a Griller session
  grills beside it". It must not make the Chief of Staff look like one of two people to talk to.

### "## Change Requests Lifecycle"

Replace the paragraph "A "Change Request" is an idea, a bug, a report, an issue, that you want to
study." (line 19 today) with the CR/tracker explanation (B3, B4). It holds:

- a CR is one more level of abstraction over a tracker's issues (Jira, GitHub, GitLab…);
- it lets small requests outside the tracker be accepted and prioritised;
- the tracker keeps the strategic vision, external requests and long-term planning.

This is the recommended text:

```md
A Change Request (CR) is one more level of abstraction over your tracker's issues (Jira, GitHub,
GitLab…). Your tracker keeps the strategic vision, the external requests and the long-term
planning; CRs let the small requests that never reach it (an idea, a bug, a report, an issue you
want to study) be accepted and prioritised too. A CR may also come from one of the tracker's
issues.
```

Then rewrite line 21 ("Chantier translated this into a markdown file…") so that it names the
planning area as the project's own folder only (B5). For example: "Each CR is a folder of
Markdown files in your project's planning area, `.agents/changes/`, which moves from stage to
stage during planning, study, implementation, QA, release and archive." The rest of the section
(the two images, the free-file and external-tools paragraphs) stays.

### "## What is Chantier?" and the rest of the README

These are read after the introduction is rewritten. Fix only a sentence that contradicts the four
messages or the diagrams:

- Line 46, "You only ever talk to the **Chief of Staff**", stays true with the optional Griller.
  Add the Griller only if the Driver finds the sentence misleading; keep it to one clause.
- Item 3 already says a direct batch takes no CR while it runs. It stays consistent with the
  difference sentence.

No new section. Install, Use, Supported hosts, Costs and Repository layout stay as they are,
unless a link or an image name changed.

## Area 7: the Chief of Staff's first-turn introduction

### `skills/chantier/references/session-start.md`, section 4

Rewrite the bullet list so that the four messages lead (B6). Keep the rest of the section as it
is on `main`:

- the once-per-session rule, the skip on `init` and the "new here? say init" line;
- the paragraph "A Griller gives the same introduction…", with the remote-session line.

Keep it about ten lines. The recommended list:

- **Change Request (CR):** one more level over the project's tracker issues (Jira, GitHub,
  GitLab…). It lets small requests outside the tracker be accepted and prioritised; the tracker
  keeps the strategic vision, external requests and long-term planning. A CR gets:
  - a folder in `.agents/changes/` (the request, its analysis, the user's answers, the
    self-contained Change Specification written before any code);
  - a branch and a worktree its Driver creates.

  It ends as one pull request.
- **One person to talk to, the Chief of Staff (me):** the only session that opens and runs
  batches. It keeps the backlog and asks the questions a CR needs. Nothing starts without the
  user's go. The user reviews and merges each PR; only a release's PR or fix is merged for them,
  on their word. (A Griller says "the Chief of Staff" of another session instead.)
  - A **Griller** is another session of yours that grills and specifies the backlog beside it,
    optional, never running batches.
- **Direct or Foreman:** a batch (`batch-<n>`) is steered either:
  - by a **Foreman**, a separate session that reports back to me, where a CR may join while the
    batch runs;
  - or by me in **direct mode**, where a CR joins only once every other CR is handled and the
    batch is paused, and I hold no grill while it runs (use a Griller).
- **Zero configuration:** the project's `AGENTS.md` is the only configuration (I learn how it
  builds, tests and merges from it). Everything chantier writes is Markdown and JSON in
  `.agents/changes/`.
- **Drivers and workers:** keep today's bullet, shortened if the length needs it.
- **What to ask:** keep today's bullet.

The bullets "Change Specification", "Batch", "Foreman" and "The flow" are folded into the four
above. No sentence of the section names an external planning surface (B5). Section 1's line on
the P1 `planning-repo` is a start-check rule, not the introduction: it stays as it is.

The card holds no host tool name (`test_structure.py`,
`test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`).

### The other places that carry the introduction

- `skills/chantier/SKILL.md` (the router) already says the zero-configuration message (lines
  16-18). It stays as it is.
- `skills/griller/SKILL.md` stays as it is.
- `skills/chief-of-staff/SKILL.md`: its `description` opens with "Chief of Staff for a
  change-request team on Claude Desktop or a Copilot SDK host", which contradicts direct mode
  (any Claude Code entry point, a remote session). Reword only that clause, for example: "Chief
  of Staff for a change-request team (Foreman mode on Claude Desktop or a Copilot SDK host,
  direct mode anywhere)". The body stays.
- `skills/chantier/references/init.md` (the tour): unchanged. It skips the introduction and has
  its own story.

## Area 8: `skills/chantier/references/release-template.md`

In "Visible evidence", line 34 "the screenshots in the merged PRs' Impacts sections" becomes "the
screenshots in the merged PRs' Deliverables sections" (B1). This is where `pr-template.md` puts
the before/after screenshots since PR #90. Nothing else in the file changes.

## Area 9: the other docs

Read each file below as it stands on `main`, and fix only a sentence that contradicts the
diagrams, the four messages or B5. A contradiction can be:

- a mode described differently;
- a link or image name that changed;
- a stale count.

Add no section to any of them.

- `docs/tutorial-claude-code.md`:
  - Line 32 says "This installs one skill (the Chief of Staff) and twelve agents". The plugin now
    ships three skills: the router `chantier`, `chief-of-staff` and `griller`. Say so; the twelve
    agents stay.
  - Line 72 ("introduces chantier in a few lines") stays.
- `docs/use-cases.md`, "Choose your configuration": add the one-sentence join rule of A8 after
  "what differs is how dynamic the batch is while it runs", in the same plain words as the
  README. This is the docs' entry point for the two modes.
- `docs/use-cases-direct.md`, `docs/use-cases-foreman.md`: check only. They already carry the
  join rule and the Griller on `main`.
- `docs/release-notes/` is history: unchanged.

## Review

The user reviews the drawings in the PR, from the PNG renders of Evidence 6, with no prototype
step before the Driver starts (A6).

- The PR shows each new or changed SVG rendered.
- The review settles the Griller's emoji and the split box's band label.
- A correction made in the review goes into the SVG and its companion together.

## Out of scope

- The CLI, the scenario, the tests, the agent files (both hosts), the board mod and `evals/`.
- The cards other than `session-start.md` section 4 and `release-template.md` line 34:
  - `concepts.md`, `chief-of-staff.md`, `griller.md`, `init.md`, `pr-template.md`;
  - `session-start.md` sections 1-3.
- The diagrams that the init tour generates (`init.md`, `assets/tour.html`).
- `docs/batch-pace.svg`, and a Griller box on `batch-lifecycle.svg` (A4).
- The seat, the titles, the hand-over and the fork how-to, in any diagram.
- Any mention of an external planning area or planning surface (B5). It belongs to the P1
  `planning-repo`.
- `landing-page` and `docs-sphinx-rtd` (P2): they reuse these diagrams later (A2).
- No version bump.

## Evidence

Run at the pushed head, with the outputs in the Verifier's evidence.

1. `just check` passes (Linux, macOS and Windows in CI).
2. `just scenario` passes. This CR edits two cards (`session-start.md`, `release-template.md`),
   and `AGENTS.md` says a change to the cards passes the scenario before its PR.
3. Every SVG parses: `uv run --no-project python -c "import glob, xml.etree.ElementTree as E;
   [E.parse(f) for f in glob.glob('docs/*.svg')]; print('ok')"`.
4. Companions are in step. A short script in the CR's `work/` (not committed) checks, for each
   `docs/*.svg` except `batch-pace.svg`:
   - that a `-texts.md` exists;
   - that `<desc>` equals the companion's first paragraph;
   - each drawn text (the joined text of each `<text>`) not found in the companion once Markdown
     markers are removed.

   The output shows no difference, or only markup that the Verifier names.
5. Links: every relative link, image and in-page anchor in `README.md` and `docs/*.md` resolves.
   `git grep -n how-chantier-works-simple.svg` returns nothing.
6. A PNG render of each new or changed SVG, in `evidence/`, made with any renderer the Verifier
   has (named with its version).
   - The renders are checked by eye for overlaps and cut-off texts.
   - They are shown in the PR for the user's review (A6), as the project's PR template asks for
     visual changes.
7. Content, by grep, with the output kept:
   - **The README's images.** `README.md` names `how-chantier-works-simple-direct.svg` before
     `how-chantier-works-simple-foreman.svg`, then `how-chantier-works.svg`.
   - **The difference sentence.** Between the two simple images and the detailed one,
     `README.md` holds the difference sentence (it names direct mode, "paused" and Foreman mode).
   - **The README's introduction.** Before "## How Chantier works", `README.md` holds the four
     messages:
     - "tracker";
     - "Chief of Staff", "go" and "merge";
     - "direct", "Foreman" and "paused";
     - "AGENTS.md" and ".agents/changes/".
   - **The Change Requests section.** It holds "Jira", "GitHub", "GitLab", "tracker",
     "prioritised" and "long-term". `README.md` no longer holds "is an idea, a bug, a report".
   - **No external planning area.**
     `git grep -n -i -E "planning.surface|planning-repo|external planning" -- README.md docs/`
     returns nothing. The same pattern on section 4 of `session-start.md` returns nothing.
   - **The first-turn introduction.** `session-start.md` section 4 holds "tracker", "Jira",
     "Griller", "paused", "AGENTS.md" and ".agents/changes/".
   - **The release template.** `release-template.md` holds "Deliverables sections" and no longer
     "Impacts sections".
   - **The detailed diagram.** `how-chantier-works.svg` no longer holds the path
     `M300,230 V242 H250 V400`. It holds "Foreman mode", "direct mode", "not recommended in
     remote", "remote session" and "Griller".
   - **The Griller.** "Griller" and "optional" appear in each of these and in its companion:
     - `how-chantier-works-simple-direct.svg`;
     - `how-chantier-works-simple-foreman.svg`;
     - `how-chantier-works.svg`;
     - `cr-lifecycle-simple.svg`;
     - `cr-lifecycle.svg`;
     - `cr-folder-lifecycle.svg`.
   - **The batch lifecycle.** `batch-lifecycle.svg` and `batch-lifecycle-texts.md` hold "grill in
     a Griller session" and no longer hold "another session of yours". `batch-pace.svg` holds no
     "Griller", and `git diff --stat <base> -- docs/batch-pace.svg` is empty.
   - **The words.** `git grep -n -i -E "\bland(ed|s|ing)?\b|epoch" -- README.md docs/` finds
     nothing new about a batch.
