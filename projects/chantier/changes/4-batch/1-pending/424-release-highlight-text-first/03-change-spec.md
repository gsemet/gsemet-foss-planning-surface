# Release highlights: text first, cropped picture, one set of rules

Change Specification, written 2026-11-20 from `intake/request.md` and `02-answers.md` (no
`01-intent.md`; the user asks no questions, the Chief of Staff settled the open points). No issue.
Priority P2. One batch CR, at most 3 rounds. It bundles the request of
`release-process-notes-align` (copied in `02-answers.md`). A follow-up of CR-413
(release-notes-writing-rules, PR #378). Text only: one card and one doc, no code.

## Goal

In the user's words: "j aimerais que le paragraphe commence par le texte, et que l'image soit
cropper sur le point d attention". A release highlight reads heading, text, picture, and its
picture shows only the place where the change happens. And chantier's own release process stops
contradicting the template: `docs/release-process.md`, which ranks above the template for
chantier, no longer asks a highlight for a usage example, a link to the doc and a "why it
matters" sentence; it keeps what is chantier's own and points to the template for the writing
rules.

## Decisions carried (02-answers.md)

Each is: Settled by the Chief of Staff (2026-11-20, the user asks no questions).

- The bundle: this CR carries both requests; `release-process-notes-align` is abandoned.
1. A highlight is its heading, then at most two sentences, then the picture; when the picture
   shows the whole change, no text: heading and picture.
2. Every picture of the notes is cropped to the part where the change happens, whatever its
   source.
3. The release Driver crops, with the project's means; the template names no tool.
4. A picture the Driver cannot crop stays whole, and the Driver says so in a `note`; nothing is
   invented in its place.
5. The thread's image gets no rule of its own.
6. `docs/release-process.md` keeps, of a highlight, the count and the heading's form `## <emoji>
   <what the reader can now do>`; the paragraph, the usage example, the doc link, the "why it
   matters" sentence and the two-column before/after table go.
7. In `docs/release-process.md` the change touches "Release notes" (item 3 and a pointer), the
   introduction's sentence on rank, and one sentence in "Visuals"; the rest stays.
8. `scripts/release_notes.py` is not changed.
9. The published release folders are not rewritten.

## What changes

### 1. `skills/chantier/references/release-template.md`, "A highlight"

Today (lines 40 to 46): "A heading saying what you can now do, then a picture, then at most two
sentences."; the before and after bullet; "When the picture shows the whole change, no text under
it."; the setting bullet. Rewrite the section so that it says:

- A heading saying what you can now do, then at most two sentences, then the picture.
- The before and after bullet, kept: when the change replaces a visible behaviour, the picture
  puts the before and the after side by side in one image, built from the Verifier's
  before/after, and the text does not describe the before again.
- When the picture shows the whole change, write no text: the highlight is its heading and the
  picture. ("no text under it" goes: the text is no longer under the picture.)
- The setting bullet, unchanged.

### 2. `skills/chantier/references/release-template.md`, "Visible evidence"

Add the crop rule, next to the sentence "The Driver reads each image it produced before it keeps
it":

- Each picture shows only the part of the screen where the change happens: no toolbar, no empty
  margin, no unrelated content. It holds for every source of the list (a Verifier's capture, a
  PR's screenshot, a capture by the Driver, CLI output: only the lines that show the change).
- In a joined before and after image, both halves are cropped to the same region, at the same
  scale.
- The Driver crops when it builds the image, with the means the project's procedure gives (the
  template names no tool), and checks the crop when it reads the image.
- A picture it cannot crop stays whole, and the Driver says so in a `note`; no other image is
  made up in its place.

The rest of the template (Scope and precedence, The notes' structure, Writing rules, The thread,
Where they go) is not changed. The Driver reads the whole file once after its edits and changes
another sentence only where the new order has made it false (for instance a "picture, then text"
wording elsewhere; none was found at main, `4ed0d56c`).

### 3. `docs/release-process.md`, the introduction

Today: "The generic default that other projects get is [release-template]; this file ranks above
it for chantier." Keep the rank and make the split plain: this file holds what is specific to
chantier's releases (the folder, the header, the links, the sections, the sources of the visuals,
the images, the anonymisation, the checks) and ranks above the template there; how the notes are
written (the template's "Writing rules" and "A highlight") and what a picture shows ("Visible
evidence") are the template's, which this file does not restate.

### 4. `docs/release-process.md`, "Release notes"

- Item 3 (today lines 45 to 51) becomes: two to four highlight sections, each headed `## <emoji>
  <what the reader can now do>` and written as the template's "A highlight" says (linked), with
  nothing else asked of it here. Its five sub-bullets go: the short paragraph, the usage or call
  example, the capture or two-column before/after table with a caption row, the link to the doc
  at the tag, the closing sentence on why it matters.
- Add one sentence, before or after the structure, that the writing rules are the template's
  "Writing rules" (linked), not restated here.
- Keep: the opening paragraph (the sources, no CR number or slug, no batch number, no planning
  path, the role names allowed), item 1 (header), item 2 (links), item 4 (Smaller changes), item 5
  (folded sections, the `**Not exercised by an eval.**` bullet), and the closing sentence on
  every `feat:` and `fix:` commit.

### 5. `docs/release-process.md`, "Visuals"

One sentence: each picture is cropped as the template's "Visible evidence" says (linked); with
the rendering described there, the HTML page holds only the part that shows the change, and the
`--window-size` fits it. The sources, the rendering steps and the "headless Chrome is missing"
stop are not changed.

"The release folder", "Images", "Anonymisation", "Announcement thread" and "Which batch" are not
changed.

## Out of scope

- `scripts/release_notes.py` and `just release-notes`: no new check (it cannot read pixels; a
  check of a highlight's order is a new tool with no measured cost).
- The published notes under `docs/release-notes/`: not rewritten.
- The announcement thread's rules, in the template and in `docs/release-process.md`.
- `driver.md` (the Release driver's steps), `docs/release-driver-texts.md`, `CONTRIBUTING.md`
  "Release": none states a highlight's form.
- The Studio project's own guideline, which carries the same rule until this merges.
- The agent files of both hosts.

## Evidence

No test is added: the change is text, no test guards these sentences today, and the tests stay
few. No host or default dependency: no matrix. The Verifier reads the shipped files from the
repository at the head under test (not a copy):

1. `skills/chantier/references/release-template.md`, "A highlight": the order is heading, at most
   two sentences, picture; the whole-change case says heading and picture, no text; the words
   "then a picture, then at most two sentences" and "no text under it" are gone (`grep -n "then a
   picture\|under it" skills/chantier/references/release-template.md` prints nothing).
2. The same file, "Visible evidence": the four crop points (the part where the change happens;
   same region and scale for both halves; the Driver crops and checks; a picture it cannot crop
   stays whole and is noted).
3. `docs/release-process.md`: `grep -n -i "why it matters\|usage or call example\|two-column"
   docs/release-process.md` prints nothing; item 3 links the template's "A highlight"; the
   introduction says which file holds what; "Visuals" holds the crop sentence; items 1, 2, 4 and 5
   and the five other sections read as before (`git diff` shows no change there).
4. The two files agree: no sentence of `docs/release-process.md` asks a highlight for something
   the template forbids or orders differently.
5. `just check` passes in the worktree at the pushed head (its lint and tests, and
   `release-notes`, which still accepts the current version's folder: the published notes are
   not touched).

What only a release proves, named in the PR's Known gaps: the first notes written with these
rules (text before the picture, the pictures cropped).

## Gates (the project's `AGENTS.md`)

- `just check` in the worktree at the rebased head, before the first push.
- No `just eval-dry-run`, no `just mod` (no CLI source, no eval kit, no hook).
- The long gate: `release-template.md` is a card, so the pipeline's `just scenario
  (ubuntu-latest)` job is green at the PR's head; the local `just scenario` only when this CR is
  on top of the stack.
- Repository text in English.

## Open questions

None: the user asks no questions (2026-11-20); the points are settled in `02-answers.md`.
