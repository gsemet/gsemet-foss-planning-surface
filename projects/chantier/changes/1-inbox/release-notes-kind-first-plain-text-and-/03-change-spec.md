# Release notes: kind-first plain text and framed images

Short name: `release-notes-style`. Destination: running batch batch-31. Repository:
`C:/Users/gaeta/Projets/chantier`. A cards-only change (plus one structure test): no CLI code, no
agent file, no startup manifest, no version.

## Goal

The user read the markdown-okf-schema-studio 1.12.1 note, an urgent bug-fix release, and it read
like a 1.12.0 feature release: a revert shown as a new feature, block-editing fixes shown as
features, no well-framed image, long and indirect text. A Fable audit of all that repository's
notes (2026-11-24) found the same faults across releases: a fix worded as a new ability (7 of 19
notes), a closing "why it matters" line (9; gone since a written ban in 1.10.0, so a written ban
works), bad news hidden or softened (6: user-facing known issues under "For contributors", a
removed setting mid-paragraph), whole-page or oversized images (6 of 11), mechanism told instead of
consequence (5). The cause is the default template: it asks for verbs in the subtitle and a "what
you can now do" heading whatever ships, and says nothing on the release's kind, bad news, length,
image size, captions, or how the Release Driver reads its own images (while `driver.md` says a
Driver never opens an image).

This CR teaches the Release Driver, in its card, to write the notes kind first, one plain sentence
per change, bad news on labelled lines, within word budgets, with images framed on the changed
element, and to check the result with a ten-question self-check. The notes' structure and format
do not change.

## Files this CR touches (for the Foreman's overlap check)

| File | Where | Overlap in batch-31 |
| --- | --- | --- |
| `skills/chantier/references/release-template.md` | "The notes" and its subsections, "Visible evidence" | none known (CR-471 and CR-474 do not name it) |
| `skills/chantier/references/driver.md` | one bullet of "Means: images and the look" (the "A Driver never opens an image file" bullet) | CR-471 (`slim-cards`) moves that section into a `driver-<moment>.md` piece read by a `driver:pr-extras` action; CR-474 also edits `driver.md`. Edit the bullet wherever it lives at the rebased head, found by its text, not its heading |
| `skills/chantier/scripts/cli/tests/test_release_template_card.py` (new) | structure test of the two shipped cards | none |

Not touched: `startup-manifest.json` (release-template.md stays the `release` action's reading
only, never a startup reading: the 12,544-byte startup limit is untouched), `agents/`,
`com.github.copilot/agents/`, the CLI, `scripts/release_notes.py`, `CONTRIBUTING.md`.
`docs/release-process.md` is touched only if the user says so (open question 1).

## What changes

### 1. `release-template.md`, "The notes"

Keep the section's headings `## The notes`, `### Writing rules`, `### A highlight` and
`## Visible evidence` with these exact names: `docs/release-process.md` links to their anchors
(`#writing-rules`, `#a-highlight`, `#visible-evidence`). Add the new rules as `###` subsections of
"The notes" (names below are the target; the Driver may group them otherwise if no rule is lost and
the three anchors stay). The structure list keeps its five items in order; only the wording of the
title item changes:

- the title: the product name and the **full version** (`X.Y.Z`, never `X.Y`), then the subtitle
  line, which **names the release's kind first**, then the two or three main changes, in the
  kind's words (not "as verbs" whatever ships); the `<sub>` line is unchanged.

#### 1a. New subsection "The kind" (release-notes-style-Q6)

- Before writing a line, the Driver decides the release's kind from what ships, one of five:
  - **feature**: the user can do something they could not do before;
  - **fix**: something that should have worked now works; nothing new;
  - **restore**: it undoes a mistake of an earlier release (a revert, a behaviour put back);
  - **breaking**: something the user relied on is removed or behaves differently and they must act;
  - **internal**: nothing the user sees changes (tooling, tests, docs process).
- The subtitle names the kind in its first words (for instance "A bug-fix release: ...",
  "Restores ... that 1.12.0 broke", "A breaking release: ..."), and every highlight and line keeps
  the tone of that kind: a fix release has no "you can now" heading, a restore is never shown as
  new.
- When the kind the notes need does not match the version (a patch version whose content needs
  feature wording, or a minor version that ships only fixes), the notes take the tone of the real
  kind; the version PR's description says the version is probably wrong and why, and the user
  decides. The Driver does not change the version on its own (driver.md's "The version is the
  specification's ... Never ask for it" stays: this is a statement in the PR, not a question).

#### 1b. "A highlight", changed

- The heading says the change in its kind's words: a feature, what you can now do; a fix,
  "Fixed: <what works again>"; a restore, what works again and, in one clause, that the earlier
  release broke it ("<X> works again; 1.12.0 broke it"); a breaking change, what changed and what
  the user must do. It replaces "a heading saying what you can now do".
- The rest of the subsection stays: at most two sentences, then the picture; the before/after side
  by side for a replaced visible behaviour, with no text describing the before again; heading and
  picture alone when the picture shows the whole change; a setting named as a setting, with its
  default and where to turn it on.

#### 1c. New subsection "One line per change"

- Each smaller change and each folded line is **one sentence**.
- A fix starts with "Fixed:" and says what works now, as the user sees it: "Fixed: the editor keeps
  the cursor in the block you were editing." Never a fix worded as a new ability.
- A restore owns the earlier release's mistake in one clause: "Restored: copy and paste of whole
  blocks, which 1.12.0 broke." No apology paragraph, no blame.
- The consequence for the user, not the mechanism: what they see or can do, not how the code does
  it.

#### 1d. New subsection "Bad news"

- A removal, a change of behaviour the user relies on, and a user-facing known issue each get a
  labelled line in the **visible part** (above the folded sections), starting `Removed:`,
  `Changed:` or `Known issue:`, one sentence each, with what the user should do when there is
  something to do.
- Never only in a folded section (a user-facing known issue is not a contributor's detail), never
  inside a paragraph about something else, never softened ("streamlined", "simplified") when the
  truth is "removed".

#### 1e. New subsection "Length" (release-notes-style-Q7, as judgement, not a check)

- Subtitle at most 16 words; each smaller change or folded line at most 20 words; each highlight's
  text at most 40 words (heading included, picture excluded).
- The visible part (everything above the first folded section, the link line and HTML tags not
  counted) at most 120 words for a fix, restore or internal release, at most 250 for a feature
  release. Breaking: see open question 3.
- Over a budget, cut words, not facts: a fact that does not fit moves to a folded line.

#### 1f. "Writing rules", extended into the banned constructions

Keep the three existing bullets. Add a list of banned constructions, each with a before/after pair
in the card (the pairs below are the target text, modelled on the audit's findings; keep them
short and generic, no real project's name):

| Banned | Before | After |
| --- | --- | --- |
| A fix worded as a new ability | "You can now edit a block without losing your cursor." | "Fixed: the cursor stays in the block you are editing." |
| A restore shown as new | "New: paste whole blocks at once." | "Restored: pasting whole blocks, which 1.12.0 broke." |
| A closing "why it matters" line | "... This means you stay in the flow." | (line removed) |
| Mechanism instead of consequence | "The parser now debounces change events on the block node." | "Typing fast in a long block no longer freezes the editor." |
| Bad news softened or buried | "We streamlined the settings (the `legacy.view` option is gone) and ..." | "Removed: the setting `legacy.view`; the new view is the only one." |
| A sentence about a missing image | "No screenshot: this change has nothing to show." | (sentence removed; the change has no picture) |
| Feature tone in a fix release | subtitle "Faster editing, smarter blocks" for a fix release | subtitle "A bug-fix release: block editing works again" |

The existing bans ("Before:"/"Now:" labels, an invented scene, a punchy fragment, a praise word, a
closing "why it matters" line) stay; the closing line keeps its ban (it worked).

#### 1g. New subsection "Self-check"

Before the notes are final (before `note --draft` on the last version and before the version PR's
body is refreshed from them), the Driver answers ten yes/no questions; each "no" is fixed first:

1. Does the subtitle name the release's kind in its first words?
2. Does the title carry the full version (`X.Y.Z`)?
3. Does every highlight and line keep the tone of the release's kind?
4. Does every fix start with "Fixed:" and say what works now, with no fix worded as a new ability?
5. Does every restore own, in one clause, the earlier release that broke it?
6. Is every removal, behaviour change and user-facing known issue on a `Removed:`, `Changed:` or
   `Known issue:` line in the visible part?
7. Is each smaller change and folded line one sentence, and is every budget of "Length" kept?
8. Does every line say the consequence for the user, not the mechanism, with none of the banned
   constructions?
9. Does every image show only the changed element, within the size of "Visible evidence", its alt
   text saying what it shows, with no sentence about a missing image?
10. Does the version match the kind, or does the version PR say it is probably wrong?

### 2. `release-template.md`, "Visible evidence" (release-notes-style-Q2, Q3, Q5)

Keep the sources list, the anonymisation paragraph and the skeleton paragraph (`<img src="...">`
form, never a Markdown image link to a file that may not exist). Replace the crop list and the
"With nothing visible to show" sentence by the image protocol:

- Only a visible change gets an image; one image per change.
- Crop to the changed element (the control, the panel, the lines of output), never the whole
  window or page; 900 to 1200 px wide, at most 600 px high.
- A before/after is one joined image, both halves the same region at the same scale.
- The alt text is the caption: it says what the image shows, in one plain phrase; no separate
  caption line.
- The Driver crops with the project's own means and names no tool (unchanged).
- A visible change, a fix included, whose sources hold no image: the Driver captures it itself
  with the project's own capture means before the notes are final (Q2).
- When the capture is impossible: the notes go out without that image and say nothing about it;
  the version PR's Known gaps names it as `no picture for <change>: <why>` (Q5). Q2 still holds:
  the project's own capture means are tried first.
- Nothing visible to show: no image and no sentence about it (the current "the highlight says so in
  one line" goes).
- The Release Driver reads each image it produced before it keeps it (Q3; the sentence exists, keep
  it) and checks there: the crop shows the change, the size is within the bounds, the alt text
  matches, and the look of driver.md ("Means: images and the look") passes.
- The current "a picture it cannot crop stays whole, and a `note` says so" goes; what replaces it is
  open question 2.

### 3. `driver.md`, the named exception (release-notes-style-Q3)

The bullet "A Driver never opens an image file (`.png`, `.jpg`, `.gif`, `.webp`): it attaches the
images the Verifier or the Demo explorer names, by path and caption, and judges them from their
reply." gains its one named exception: the Release Driver reads each image it produced, as
[release-template](release-template.md) "Visible evidence" says. Nothing else in `driver.md`
changes. (The look's own "open the image as an image" stays as it is.) After CR-471 lands, the
bullet may sit in another file of the Driver's card pieces: edit it there, by its text.

### 4. The decisions carried

- Q1 (A): only chantier's `release-template.md` (and the `driver.md` exception) change; the OKF
  repository's guideline amendment is filed into that project's inbox for its own Chief of Staff,
  not by this CR's Driver (the Chief of Staff files it; this CR's PR does not touch that repository).
- Q2 (B): the Release Driver captures a missing image itself, with the project's own means, before
  the notes are final (section 2).
- Q3 (A): the Release Driver reads each image it produced; `driver.md` names the exception
  (sections 2 and 3).
- Q4 (A): card only; the mechanical refusals (title version, budgets, banned phrases, image size,
  empty fold) belong to a separate CR on each project's `scripts/release_notes.py --check`. This CR
  changes no script.
- Q5 (B): capture impossible: published without the image, the gap in the version PR's Known gaps,
  the note silent (section 2).
- Q6 (A): the real kind's tone; the version PR says the version is probably wrong; the user decides
  (section 1a).
- Q7 (A): the audit's budgets, as judgement in the card (section 1e).
- Q8 (B): specified for the running batch batch-31.

## Out of scope

- The OKF repository's guideline and its `scripts/release_notes.py --check` (Q1, Q4), and
  chantier's own `scripts/release_notes.py` (Q4).
- The notes' structure and format (title, links, highlights, smaller changes, folded sections,
  `<sub>` line), the thread (`## The thread`) and "Where they go".
- The CLI, the startup manifest and every other card; the agent files on both hosts.
- Rewriting past release notes.

## Evidence

- A new structure test, `skills/chantier/scripts/cli/tests/test_release_template_card.py`, one
  parametrized test that reads the **shipped** files from the repository at the head under test
  (`skills/chantier/references/release-template.md` and `driver.md`, or the piece CR-471 moved the
  bullet into, found by the bullet's text), no prepared copy, and asserts, whitespace-normalised:
  - release-template.md names the five kinds (`feature`, `fix`, `restore`, `breaking`, `internal`)
    and the full version (`X.Y.Z`) in the title;
  - it holds `Fixed:`, `Removed:`, `Changed:`, `Known issue:`;
  - it holds the budgets (16, 20, 40, 120, 250 words) and the image bounds (900, 1200, 600 px);
  - its self-check holds exactly ten numbered questions;
  - the anchors `docs/release-process.md` links still exist (`### Writing rules`, `### A
    highlight`, `## Visible evidence`);
  - "the highlight says so in one line" is gone;
  - the driver card's "never opens an image file" bullet names the Release Driver's exception;
  - and one non-parametrized assertion: `release-template.md` appears in no `startup_sections`
    entry and is not `common` or `role_core` of `startup-manifest.json` (it stays an action
    reading).
  Kept fast (a file read); `just test` stays within its budget.
- `just check` passes in the worktree at the rebased head (Linux, macOS and Windows in CI). A
  cards-only change does not owe `just eval-dry-run`.
- The long gate: a change to the cards passes the pipeline's `just scenario (ubuntu-latest)` job,
  green at the PR's head, before its PR is merged; the local Windows run follows the batch's
  top-of-stack rule (the Foreman's call).
- `test_startup_manifest.py` still passes (no manifest change; the driver.md bullet grows by one
  clause, in a section outside the CR Driver's budgeted readings today).
- No host or default matrix: the change is card text, the same on both hosts and with no
  configured value.
- A reading check in the PR's Test plan: the Driver applies the new rules, as a dry run, to the
  1.12.1 situation of the request (a fix release with a revert and block-editing fixes) and quotes,
  in the PR, the subtitle and three lines the card now produces (a `Fixed:` line, a `Restored:`
  line, a `Known issue:` line), with the self-check's ten answers. Text only, no image.

## Open questions

1. **chantier's own `docs/release-process.md`.** It ranks above the template for chantier's
   releases and contradicts the new rules in three places: highlight headings
   `## <emoji> <what the reader can now do>` (line 47), known issues inside the folded
   "For contributors" section (lines 53-54), and the title `<h1 align="center">chantier X.Y</h1>`
   (minor only, line 38; `scripts/release_notes.py` checks only that the minor is in the title).
   As it stands, chantier's own notes would keep the old faults. Does this CR align those three
   lines with the card (a doc change, no script change), or is that a separate CR?
2. **An image that cannot be cropped to the bounds.** The current rule keeps it whole with a
   `note`. Under the new protocol, is it treated as "capture impossible" (Q5: no image, a Known
   gaps line), or kept whole?
3. **Kinds that mix, and the breaking budget.** When a release holds several kinds (a feature and
   a breaking change, fixes and one feature), which does the subtitle name first (a proposed order:
   breaking, feature, restore, fix, internal)? And which visible-part budget does a breaking release
   take (Q7 names 120 for fix, restore, internal and 250 for feature)?
4. **Q5 with no version PR.** A release whose procedure opens no version PR has no Known gaps: is
   the missing picture named in a `note` and the hand-back report instead?
