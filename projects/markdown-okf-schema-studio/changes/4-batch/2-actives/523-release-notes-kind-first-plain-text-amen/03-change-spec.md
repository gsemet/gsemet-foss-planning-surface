# Release notes: kind-first plain text, amend the guideline

Type: docs · Priority: P2 · Batch: batch-11 (owner, 2026-11-27) · Short name: `notes-kind`

## Goal

A reader of a release note knows at once what kind of release it is. A fix release reads as a fix
release: "Fixed: ..." lines, no "what you can now do", no new ability where something only works
again. Bad news (a removal, a changed behaviour, a known issue) is said plainly in the visible part.
The text is short, and every picture shows only what changed.

Today `.agents/guidelines/release-process.guidelines.md` ("Release notes") asks for the same
feature-release shape whatever ships: a title `X.Y`, a bold subtitle of verbs, highlight headings
that say "what you can now do". That guideline ranks above chantier's `release-template.md` card,
so the card's rules (chantier CR-475, `release-notes-kind-first-plain-text-and`, merged
2026-11-24) cannot reach this repository's notes until the guideline says them. This change
writes them into the guideline, with the same values as the card and the `release-evidence`
topic, and with the owner's decisions of `02-answers.md`.

## Decisions carried (none dropped, none added)

From `02-answers.md` (owner, 2026-11-27, and one Chief of Staff decision) and `intake/request.md`:

1. **notes-kind-Q2**: a fix release keeps today's structure (header, links, highlights, smaller
   changes, folded sections); only the tone of its headings and lines changes to its kind
   ("Fixed: ...", never "what you can now do"), as chantier's card says.
2. **notes-kind-Q3**: no new script check. `scripts/release_notes.py --check` is not extended;
   the rules are the agent's own reading (a self-check list). This replaces any reading of the
   request that would add mechanical checks.
3. **notes-kind-Q4**: a feature clip's GIF is exempt from the new image sizes, as it already is
   from cropping.
4. **notes-kind-Q5**: the 1.12.1 note (`docs/releases-notes/2026-11-24-v1.12.1/release-notes.md`)
   is not rewritten; only the rule changes. This replaces the request's "The 1.12.1 note itself
   also needs a rewrite".
5. **Performance highlight** (the owner's rule for 1.13.0, told with the series, no objection): a
   performance gain the user can see is a highlight with figures, estimated if need be, never only
   a folded line.
6. **From the request**: kind first (feature, fix, restore, breaking, internal), the subtitle
   names it, the title carries the full version; labelled lines "Fixed:", "Restored:",
   "Removed:", "Changed:", "Known issue:"; one sentence per item; word budgets (subtitle 16,
   item 20, visible part 120 for a patch, 250 for a feature); the image protocol (only visible
   changes, cropped to the changed element, 900 to 1200 px wide, at most 600 px high, before and
   after joined, alt text as the caption); the rules stay in step with chantier's card.
7. **notes-kind-Q6** (owner, after the first specification): the hero image serves post 1 of the
   announcement thread only; the first highlight of the notes takes a picture cropped within the
   new bounds.
8. **Chief of Staff, routine gap** (after the first specification): in a fix release the smaller
   changes are headed `## 🛠 Other fixes`.

## What changes

One file: `.agents/guidelines/release-process.guidelines.md`, section "Release notes" and its
subsections, plus the two cross-references named below in the same file. No other file changes.

### "Release notes" (opening paragraph)

Add, before "Writing", a short subsection **"The kind"**, with the card's values:

- Decide the kind from what ships, before writing a line:
  - **feature**: the user can do something they could not do before;
  - **fix**: something that should have worked now works; nothing new;
  - **restore**: it undoes a mistake of an earlier release (a revert, a behaviour put back);
  - **breaking**: something the user relied on is removed or behaves differently and they must act;
  - **internal**: nothing the user sees changes (tooling, tests, docs process).
- The subtitle names the kind in its first words ("A bug-fix release: ...", "Restores ... that
  1.12.0 broke", "A breaking release: ..."). Every highlight and line keeps that tone: a fix
  release has no "you can now", a restore is never shown as new.
- Several kinds: the subtitle names first the one that comes first in this order: breaking,
  feature, restore, fix, internal. Each line keeps its own change's tone.
- When the kind does not match the version agreed in step 1 (a patch whose content needs feature
  wording, a minor that ships only fixes), the notes take the tone of the real kind and the version
  PR's body says the version is probably wrong and why. The owner decides; the agent never changes
  the version itself.

### "Writing"

- Replace "Each highlight is a heading that says what you can now do" with: the heading says the
  change in its kind's words. Feature: what you can now do. Fix: "Fixed: <what works again>".
  Restore: what works again and, in one clause, that the earlier release broke it. Breaking: what
  changed and what you must do. Then at most two sentences, then the picture (unchanged).
- Add: each smaller change and folded line is **one sentence** (no bold lead followed by a second
  sentence). A fix starts "Fixed:", a restore "Restored:" and owns the earlier release's mistake in
  one clause, no apology, no blame. Say the consequence for the user, not the mechanism.
- Add a **"Bad news"** rule: a removal, a change of behaviour the user relies on and a user-facing
  known issue each get a labelled line in the visible part, above the folded sections, starting
  `Removed:`, `Changed:` or `Known issue:`, one sentence, with what the user should do. Never only
  in a folded section, never inside a paragraph about something else, never softened
  ("streamlined", "simplified") when the truth is "removed".
- Add the **performance rule** (decision 5): a performance gain the user can see is a highlight
  with figures (a time, a size, a count, before and after), estimated if need be and then said as
  an estimate; never only a folded line.
- Extend "Never use" with the card's banned constructions, as a table with a before and an after
  for each (the seven rows of the card's "Banned constructions": a fix worded as a new ability, a
  restore shown as new, a closing "why it matters" line, mechanism instead of consequence, bad news
  softened or buried, a sentence about a missing image, feature tone in a fix release). The
  existing items ("Before:"/"Now:" labels, invented scenes, punchy fragments, praise words) stay.
- The picture bullets move to "Images" (below); "Writing" keeps a one-line pointer to it.

### "Structure"

The order is unchanged (decision 1). Item by item:

1. **Header**: the title becomes `<h1 align="center">Markdown OKF-Schema Studio X.Y.Z</h1>`
   (the full version). The bold line becomes the **subtitle**: the kind in its first words, then
   the two or three main changes in the kind's words, at most 16 words. The `<sub>` line and its
   `git rev-list` count are unchanged.
2. **Links**: unchanged.
3. **Highlights**: two to four, `## <emoji> <heading in the kind's words>` (was `<what you can now
   do>`), following "Writing".
4. **Smaller changes**: `## 🛠 Smoother editing` stays for a feature release; in a fix, restore or
   internal release the heading takes the kind's tone (`## 🛠 Other fixes` for a fix release,
   decision 8). The `Removed:`, `Changed:` and
   `Known issue:` lines sit here or right above it, never only in a folded section.
5. **Folded sections**: unchanged, except "For contributors": it keeps the tooling changes and a
   known issue that only contributors meet; a user-facing known issue moves to the visible part.

Add a **"Length"** paragraph, with the card's values and its wording "a judgement, not a check"
(decision 2): subtitle at most 16 words; each smaller change or folded line at most 20; each
highlight's text at most 40 (heading included, picture excluded); the visible part (above the first
folded section, links and HTML tags not counted) at most 120 words for a fix, restore or internal
release and 250 for a feature or breaking one. A release of several kinds takes the budget of the
kind its subtitle names first. Over a budget, cut words, not facts: a fact that does not fit moves
to a folded line.

The rule "every changelog line of the release appears once" stays, with "Smoother editing" read as
"the smaller changes".

### "Images"

Gather here the picture rules, with the `release-evidence` values:

- Only a visible change (a fix too) gets a picture, one per change.
- Each still picture is cropped to the changed element (the existing crop bullets stay: no toolbar,
  no empty margin, no unrelated content; a gesture keeps the element and what it acts on).
- Size: **900 to 1200 px wide, at most 600 px high**.
- Before and after: one joined image, both halves the same region at the same scale (existing).
- The alt text is the caption: one plain phrase on what the picture shows, and no caption line.
- No picture within these bounds: the notes say nothing about it (no "no screenshot" sentence),
  and the version PR's body names `no picture for <change>: <why>`.
- **Clip GIF exception** (decisions 3 and CR-482's feature-clip-Q14): a feature clip's GIF is not
  cropped and is exempt from the sizes; the rest of the rules (alt text, one picture per change)
  hold for it. The existing sentence on the clip's zoom standing in for the crop stays.
- The existing file rules (next to the notes, linked by file name, no absolute URL or subfolder,
  attached as release assets) are unchanged.

### "Self-check" (new, last subsection of "Release notes")

Before the version PR is opened, and again before its body is regenerated after review remarks,
the agent answers yes or no and fixes each "no". The ten questions of the card, worded for this
repository:

1. Does the subtitle name the release's kind in its first words?
2. Does the title carry the full version (`X.Y.Z`)?
3. Does every highlight and line keep the tone of the release's kind?
4. Does every fix start with "Fixed:" and say what works now?
5. Does every restore own, in one clause, the earlier release that broke it?
6. Is every removal, behaviour change and user-facing known issue on a `Removed:`, `Changed:` or
   `Known issue:` line in the visible part?
7. Is each smaller change and folded line one sentence, and is every budget of "Length" kept?
8. Does every line say the consequence for the user, with none of the banned constructions?
9. Does every picture show only the changed element, within the sizes of "Images" (a clip GIF
   excepted), its alt text saying what it shows, with no sentence about a missing picture?
10. Does the version match the kind, or does the version PR say it is probably wrong?

Step 3 of "The steps of a release" gets one clause pointing to this self-check. It says nothing
about `scripts/release_notes.py`, which is not changed (decision 2).

### "Hero image"

Today the hero image "serves post 1 and the first highlight of the notes", at 1200 px in a 16:9 to
4:3 frame, that is 675 to 900 px high, over the new 600 px bound, and not cropped to the changed
element. Decision 7 (notes-kind-Q6): the hero image serves post 1 of the thread
(and the release folder) only; the first highlight takes a picture cropped within the bounds of
"Images". The sentence "It serves post 1 and the first highlight of the notes" becomes "It serves
post 1 of the announcement thread".

### Not touched in the guideline

The steps, the version PR on top of a stack, the version PR body, "Publishing", the announcement
thread (its tone already reuses the banned forms of "Writing", which now include the new table) and
the hero image's visual scenario.

## Out of scope

- Rewriting the 1.12.1 note, or any published note (decision 4). The 1.13.0 note at
  `docs/releases-notes/2026-11-27-v1.13.0/` is not touched either.
- Any change to `scripts/release_notes.py` (decision 2). Its title check (`X.Y` in the first line)
  keeps passing with a title `X.Y.Z`, since `X.Y.Z` contains `X.Y`.
- `docs/demo-video/guidelines/feature-clip-process.guidelines.md`: not edited. The clip GIF's
  exemption from the sizes is written in the release guideline only, next to the existing
  crop exception. This avoids a conflict with `pages-video-gallery` (CR-522, same batch), which
  edits that file.
- `CONTRIBUTING.md` ("How to Release" links to the guideline and says nothing of the notes' shape),
  the writing skill `skills/writing-for-markdown-okf-schema-studio/` (no rendered syntax changes),
  requirements (SwRS-MDOKFSTUDIO-CORE-078 covers `release_notes.py`, which does not change).
- chantier's card and topic: read, not edited.

## Overlap with batch-11

- **CR-522 `pages-video-gallery`**: it edits `feature-clip-process.guidelines.md`; this CR does not
  (see "Out of scope"). Its spec puts the release-notes MP4 copy of 1.13.0 out of its scope; no file
  in common. No conflict expected in the stack.
- **CR-521 (source panels under diagrams and charts)**: it changes `src/`, tests, requirements and
  adds a `CHANGELOG.md` "Unreleased" line; this CR touches none of these. No file in common.

## Delivery

- One commit, type `docs`, no scope (scopes are for `feat` and `fix` only), following
  `.agents/guidelines/git-commit-message.guidelines.md`.
- No `CHANGELOG.md` line: a `docs` change; the PR template's "No user-facing change" box is ticked.
- PR per `.agents/guidelines/pull-request.guidelines.md`, in the batch-11 stack.

## Evidence

1. The diff of `.agents/guidelines/release-process.guidelines.md` at the PR head, showing each
   section above.
2. A table in the PR body, one row per rule of the card's "The notes" and of `help
   release-evidence` (kinds, subtitle and title, labelled lines, one sentence, budgets,
   bad news, banned constructions, image size and crop, alt text, missing picture, self-check),
   with the guideline's line at the PR head that carries it and the values side by side. Every row
   matches, or the PR names the difference and why (a clip GIF exception, the "Smoother editing"
   heading, the hero image).
3. A dry run of the self-check on the 1.12.1 note as it stands, read at the PR head (not
   rewritten): the yes or no of each of the ten questions, in the PR body. It must show at least
   the faults it has today (title `1.12` without the full version, subtitle without the kind,
   bold-lead lines that are not one "Fixed:" sentence), proving the new guideline would catch them.
4. `git grep -n "what you can now do" -- .agents/guidelines/release-process.guidelines.md` at the
   PR head: the phrase appears only as the feature kind's heading, never as the rule for every
   highlight.
5. `just release-notes-check` and `just check` green at the PR head (the 1.13.0 note, unchanged,
   still passes the unchanged script); `just preflight` as the completion gate (on Windows, its
   static stage; CI runs the rest).
