# Change Specification: release-driver-diagram

## Goal

A new docs diagram, `docs/release-driver.svg`, with its companion `docs/release-driver-texts.md`,
that shows on a timeline what a release driver does, from the owner's "release" to the archive,
with a real release (another project's patch release) as an anonymised example. Like the other
`docs/` diagrams, it shows the **target**: what chantier should do. Each step it shows that
chantier's cards do not do yet is listed below and becomes an inbox item. The README links it from
its releases part.

A docs-only change: no card, agent file, CLI or test changes.

## Decisions carried from `02-answers.md`

1. **Target, to align** (answer 1): the SVG draws the target. The comparison with the cards
   (below, "Comparison with the cards") lists each step the cards do not do yet; each becomes an
   inbox item, filed by the Chief of Staff, not by this CR's Driver.
2. **Where** (answer 2): `docs/release-driver.svg` and `docs/release-driver-texts.md`, linked
   from the README's releases part.
3. **Anonymised** (answer 3): generic labels; no project name, no repository, no PR, run or commit
   numbers, no tag value, no quote of the owner (in any language), no date. Durations and counts
   stay as small annotations where they name nothing.

## What changes

### 1. `docs/release-driver.svg` (new)

**Style**, as `docs/planning-modes.svg` and `docs/cr-lifecycle.svg`:

- `<svg xmlns=... viewBox="0 0 W H" width="W" height="H">` with the same `font-family` stack
  (`Inter, Segoe UI, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji, Noto Color
  Emoji`); about 1720 wide, the height as needed.
- A `<title>` ("What a Release driver does") and a `<desc>` that tells the whole story in prose
  (who does what, in order, the gates, the outputs, the fix path, the loop, the footnote). The
  `<desc>` is word for word the prose paragraph of the texts file.
- Its own background `<rect width="100%" height="100%" fill="#f8fafc"/>`, so it reads the same on
  a light or a dark page; mid-tone strokes (`#94a3b8`, `#64748b`, `#334155`), arrow markers as in
  the other SVGs.
- **Every text 14 px or more** (stricter than some older diagrams, as the request asks).
- Header: `🚚 What a Release driver does` (28–30 px, bold, `#0f172a`) and one subtitle line
  (`#475569`), e.g. "From the owner's "release" to the archive, on a real patch release."
- The colour code of `cr-lifecycle.svg`'s legend: owner green (`#dcfce7` / `#16a34a`), Chief of
  Staff dark blue (`#1e3a8a`), Foreman orange (`#ea580c`), drivers white with an orange stroke,
  CI and forge neutral grey. A small legend in the same style, plus the marks used below
  (diamond = owner touchpoint, bar = CI run, dashed = not needed in the example).
- Emoji as elsewhere: 👤 owner, 🤵 Chief of Staff, 👷 Foreman, 🚚 Release driver, 🚜 CR driver.

**Lanes**, top to bottom, each a labelled horizontal band:

1. 👤 Owner
2. 🤵 Chief of Staff (👷 Foreman, with one)
3. 🚚 Release driver
4. 🚜 CR drivers (fix CRs)
5. CI (the project's heavy CI)
6. Forge and registry (tag, release, package registry, pages)

**Time axis**: relative, no clock time and no date (answer 3). Zero is the owner's first merge of
the stack; ticks every 30 minutes up to about +4 h 30. Before zero, a compressed break (a zig-zag
or a gap) labelled "the night before: the stack's PRs opened as drafts" in the CR drivers lane.
Positions follow the example's real timing, converted to offsets from the first merge (the first
merge at 0; the last stack merge at about +3 h; the heavy run on the default branch's head
about +3 h to +3 h 25; the version PR opened at about +3 h 40; merged at about +3 h 55; the last
heavy job done and published at about +4 h 17; deploys checked about +4 h 30).

**Content**, generic labels, the example's values as small annotations:

1. **Owner touchpoints, four green diamonds only:**
   - merges the stack (annotation: "six PRs, over about 3 h");
   - "is a release worth it?" → "yes, now" (on the Chief of Staff's proposal: the version from
     what was merged; annotation: "7 user-visible fixes → a patch");
   - reviews the notes and the thread in the version PR, says "publish" (the approval of the
     merge, or "auto");
   - posts the announcement thread (never an agent).
   - A bracket across the owner lane from the notes review to the publication: "owner asked
     nothing".
2. **Gates, as bars in the CI lane:**
   - the heavy run on the default branch's head, green on that exact commit before the version
     commit exists (annotation: "about 22 min");
   - the version push run, its jobs fanning out as parallel bars: static (3 min), static on
     Windows (4 min), visual (13 min), integration (12 min), stress (22 min);
   - then tag, package and publish, pages (the last two may sit in the forge lane, linked to the
     CI bar that produces them).
3. **Outputs** in the forge and registry lane: the tag, the forge release with its images, the
   package registry's version, the pages.
4. **The Release driver's own work** in its lane: the release CR folder; the notes and the thread
   from the changelog or the commits; the version commit; the version PR; the CI watch and the
   deploy checks (tag, release, registry, pages); `release published`; `retro.md`; `handback
   ready`. The **merge of the version PR** is drawn in lane 2 (the steering session merges a
   release PR after `release go`, as `foreman.md` says), not in the Release driver's lane.
   The **Chief of Staff's `report.md`** (its latest Progress report, a source for the notes'
   captures) is drawn in lane 2 at the version confirmation, as `chief-of-staff.md` "Releases" says.
5. **The fix path, dashed**, labelled "not needed in the example": a red heavy job → the
   Release driver writes `fix-<n>.md` and hands back → the Foreman starts a fix CR (at most three
   fixes per release, under the user's fix grant, else the user's go) → a CR driver codes it in
   lane 4 → the Foreman merges it under the grant, else the owner → the Release driver starts a
   new attempt on the fresh base, from the procedure's first step (heavy run again). This follows
   `driver.md` "Release driver" and `foreman.md`; it differs from the request on purpose (the
   request had "at most 3 rounds" and the Release driver merging the fix).
6. **Two steps drawn like the others, with no tag** (the diagram shows the target, so nothing
   marks novelty; decision 5):
   - the version PR body shows the rendered notes and thread, separated by `---` rules;
   - the archive gets a `retro.md` whose fixes the owner picks at the end.
7. **A loop arrow** from the archive back to the intake: "retro and owner remarks become process
   CRs" (annotation: "in the example: two process PRs the same day").
8. **Footnote:** "In the example the Chief of Staff did the Release driver's work itself, in
   direct mode. The target: once the other CRs are merged and the owner has confirmed the version,
   the steering session (the Foreman, or the Chief of Staff in direct mode) starts a Release
   driver."
9. **Annotations block** (counts and durations only): first stack merge to published about
   4 h 20; heavy run on the default branch to published 1 h 16; version PR open to merge 14 min;
   version push to registry 23 min; owner: 4 messages; fix CRs 0; red jobs 0; retries 0; notes:
   13 changes, three highlights.

Nothing in the SVG may contradict `docs/cr-lifecycle.svg`'s release part.

### 2. `docs/release-driver-texts.md` (new)

The form of `docs/planning-modes-texts.md` and `docs/how-chantier-works-texts.md`:

- `# What a Release driver does`;
- one prose paragraph, identical to the SVG's `<desc>`;
- then one `##` section per group of the SVG (Header, Legend, Lanes, Time axis, Owner touchpoints,
  Gates, Outputs, Release driver, Fix path, Loop, Footnote, Annotations), each with its
  exact texts in a ```` ```md ```` block.

### 3. `README.md`

The README has no section titled "Releases": its releases part is item 7 of "What is Chantier?"
("A Release driver releases, when you ask.") and the release bullet of "Detailed lifecycle".
Decided (decision 1): a new `## Releases` section right after `## Detailed lifecycle`
and before `## What is Chantier?`, in the form of the other diagram sections: one or two
sentences (a release is a CR the Release driver runs by your project's procedure; you approve each
irreversible action, or say "auto"), then
`![What a Release driver does](docs/release-driver.svg)`.

## Comparison with the cards

Read: `skills/chantier/references/driver.md` "Release driver", `foreman.md` (the release lines of
"Your means" and "The user's boundaries"), `chief-of-staff.md` "Releases",
`release-template.md`, `concepts.md` "Release CR", and the agent file `agents/release-driver.md`.

| Diagram step | In the cards today | Result |
| --- | --- | --- |
| Owner merges the stack | `ready` asks; the user merges | exists |
| "Is a release worth it?" → "yes, now" | Foreman asks `release <cr>: the others have ended, confirm the version`; the Chief of Staff grills the version from what was merged, `order confirm` | exists, when a release CR joined the batch |
| Heavy run on the default branch's head before the version commit | the Chief of Staff asks to plan one when the procedure has none; the procedure runs it | exists (the project's) |
| Notes and thread, version commit | `release-template.md`, the procedure | exists |
| Version PR "draft until mergeable" | `driver.md`: "opened ready, not as a draft" | **differs**: the diagram draws the card's form, opened ready (decision 2) |
| **Version PR body shows the rendered notes and thread, `---` separated** | nowhere: drafts go by `note --draft` and `status`'s `draft <path>` | **gap: inbox item G1** |
| Owner reviews and says "publish" | `release go`, `order approve`, "auto"; the user's merge is the go | exists |
| Merge of the version PR | the steering session after `release go` | exists (drawn in lane 2) |
| Tag, publish, pages, deploy watch | `release go` per action, "any watch of the deploys it names" | exists |
| Release driver's `report.md` at the archive (the example's) | `report.md` is the Chief of Staff's Progress report, written at `order confirm`; the Driver ends with `release published` and `handback ready <link>` | **differs**: the diagram keeps the cards' form, no end report by the Release driver (decision 3) |
| `retro.md`, its fixes picked by the owner | `driver.md`: `<work folder>/retro.md`; `chief-of-staff.md`: offered once in the Retro, each filed point an inbox item; `work/` moves to `5-archives` at `close` | exists |
| Fix CR path | `fix-<n>.md`, `order add --fix-for`, three fixes per release, grant, new attempt | exists (drawn as the cards say) |
| The Foreman starts the Release driver once the stack is merged | `foreman.md`: once the others are merged or cancelled and the user confirmed | exists, when a release CR joined the batch |
| Loop: retro and remarks become process CRs | the Retro offered, each point an inbox item | exists |
| Owner posts the thread | "never posted by an agent" | exists |

Of the three steps `02-answers.md` named as not done yet, the comparison finds one gap (the
rendered notes in the version PR); `retro.md` and the Foreman starting the Release driver once
the others are merged are already in the cards; nothing more is wanted there (decision 4).

## Inbox items (the Chief of Staff files them, not this CR's Driver)

- **G1. The version PR's body shows the rendered release notes and thread.** The Release driver
  puts the notes, then the thread, rendered (images included), in the version PR's body,
  separated by `---` rules, so the owner reviews them where they approve. Touches
  `driver.md` "Release driver" and `release-template.md` "Where they go" (both hosts' agent files
  are unchanged: the contract is in the cards); for chantier itself, `docs/release-process.md`.
- No other item: decisions 2 to 4 keep the cards' form.

## Out of scope

- Any change to the cards, the agent files (`agents/`, `com.github.copilot/agents/`), the CLI or
  the tests: the gaps go to the inbox.
- Changing the other diagrams, `docs/release-process.md` or `CONTRIBUTING.md`.
- Any data of the example beyond durations and counts; any link to the example's project.
- A rendered PNG committed to the repository.

## Evidence

- `just check` passes (Linux, macOS, Windows, by CI).
- No `just scenario`: a docs-only change (AGENTS.md); the Driver hands back with
  `handback --no-gate` quoting that rule.
- The SVG parses as XML (`python -c "import xml.etree.ElementTree as E; E.parse('docs/release-driver.svg')"`).
- No `font-size` below 14 in the SVG (a search for `font-size="1[0-3]` and smaller finds none).
- `<desc>` equals the texts file's prose paragraph (compared by a short script, output in the PR).
- Anonymisation: a case-insensitive search of both new files for the example's project name, its
  repository, `#3`, the run and commit numbers of `intake/request.md`, `1.6.1`, `1.6.0`, the
  owner's quoted words and the date finds nothing; the output goes in the PR.
- Renders: the SVG opened in a browser (headless Chrome screenshot) on a light page and on a dark
  page, both PNGs in the PR's Deliverables; the Verifier reads them (lanes readable, no overlap,
  the four diamonds, the dashed fix path, the loop arrow, the footnote).
- The README renders the image (the link resolves on the PR's branch).


## Open questions

None: the five the spec-writer raised are settled in `02-answers.md` (decisions 1 to 5).
