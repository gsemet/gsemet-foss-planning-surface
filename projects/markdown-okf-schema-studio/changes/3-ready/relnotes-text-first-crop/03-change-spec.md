# Release notes highlights: text first, picture cropped

Short name: `relnotes-crop`. Origin: the owner, verbal, 2026-11-20 (no tracker issue).

## Goal

The next release notes read better: each highlight says what changed in words first, then shows it,
and the picture shows only the place where the change happens. The owner said, after the 1.10.0
notes: the paragraph starts with the text, and the image is cropped on the point of attention. The
rule is written in Studio's release guideline so the next release (the one at the top of the
batch-07 stack) follows it.

## What changes

One file: `.agents/guidelines/release-process.guidelines.md` (repository
`markdown-okf-schema-studio`), section `## Release notes`. Nothing else in the repository changes.

### 1. The section intro (the paragraph under `## Release notes`)

Today: "The notes show what the release brings to the user, in pictures first; what the release is
stays in the folded sections." "In pictures first" now reads as the opposite of the new order.
Reword it so it keeps its meaning (the highlights, with their pictures, come before the folded
sections) without saying the picture comes first, for example: "The notes show what the release
brings to the user in a few highlights, each with its picture; what the release is stays in the
folded sections."

### 2. `### Writing`, first bullet: text first

Today: "Each highlight is a heading that says what you can now do, then a picture, then at most two
sentences." New rule: a highlight is its heading (what you can now do), then at most two
sentences, then the picture. Nothing comes under the picture, except the short Markdown example of
a new syntax (see item 5).

### 3. `### Writing`, the rule on a picture that shows the whole change

Today: "When the picture shows the whole change, write no text under it." With the text first,
"under it" no longer applies. Keep its meaning: when the picture shows the whole change, the
highlight has no sentence: its heading, then the picture.

### 4. `### Writing`, a new bullet: crop on the point of attention

Add, next to the before | after bullet:

- Each picture is cropped to the part of the screen where the change happens: no toolbar, no empty
  margin, no unrelated content around it (for example, no floating toolbar or frontmatter table
  when the change is in a list).
- A joined before | after image crops both halves to the same region, at the same scale, so the
  eye compares the same place.
- A capture of a gesture (a drag, a hover) keeps the element and what the gesture acts on, not the
  blocks around it (for example, the list and its handles, not the alerts below it).

The two examples come from the owner's request about 1.10.0 (`edit-one-list-item.png`, where the
floating toolbar and the frontmatter table take a third of the frame, and
`list-item-handles-drag.png`); write them in the guideline as general examples, with no release
number needed.

The other bullets of "Writing" stay as they are: the joined before | after image with no repeated
description of the before, settings named as settings with their default and where to turn them
on, and the "Never use" list.

### 5. `### Structure`, item 3 (the highlight sections)

Today: "`## <emoji> <what you can now do>`, each with one picture and at most two sentences,
following "Writing". A new syntax may add a short Markdown example under the picture." New text:
each with at most two sentences, then one picture cropped on the change, following "Writing"; a
new syntax may add a short Markdown example under the picture.

### 6. `### Images`, one sentence

The paragraph says the joined image is made from the Verifier's before and after captures "with any
tool". Add one sentence: the captures are cropped as "Writing" says (same region, same scale for
both halves) before they are joined. This points to "Writing" and does not restate the rule.

The owner's example, for the Driver's reading only (it does not go in the guideline):

    ## ✏️ Edit one list item, not the whole list

    A click on the list itself, outside its items, still edits the whole list.

    ![Left, a click on a list item opens the whole list in the editor; right, the same click opens only that item](edit-one-list-item.png)

## Decisions carried from `02-answers.md`

1. relnotes-crop-Q1, scope: Studio's guideline only. Past release notes, including
   `docs/releases-notes/2026-11-20-v1.10.0/release-notes.md` and its images, stay as they are. The
   generic part (text first, crop) for chantier's `release-template.md` is a note the Chief of
   Staff sends to the chantier Chief of Staff; it is not part of this PR.
2. relnotes-crop-Q2, tooling: `just release-notes-check` runs `scripts/release_notes.py --check`,
   whose `validate_notes` checks only the title naming the version and that each image is a file
   next to the notes. It does not check the order heading, picture, text. So no tooling change:
   `scripts/release_notes.py`, `test/build/test_release.py` and the justfile stay as they are.
3. Spec critic: none (a guideline wording change with no product behaviour behind it).

## Decided in the spec

The answers leave these points open; each is decided here as the option most consistent with the
project and the answers.

1. **"In pictures first" in the section intro is reworded** (item 1), since it would contradict the
   new order. Its meaning (highlights before the folded sections) is kept.
2. **A picture that shows the whole change means no sentence** (item 3): heading, then picture. This
   is the old rule "no text under it" carried into the new order, as the request asks to keep it.
3. **The Markdown example of a new syntax stays under the picture** (items 2 and 5): it is an
   example of what to type, not a sentence about the change, and the request does not ask to move
   it.
4. **The crop rule also gets one sentence in `### Images`** (item 6), because that paragraph is
   where the joined image is made; the rule itself stays in "Writing".
5. **The announcement thread (`tweet.md`) and the hero image are out of scope.** The request names
   only the release-notes highlights; the hero image already has its own framing rule.
6. **No requirement change.** No behaviour in `src/` or `scripts/` changes, so no SwRS is touched and
   no `@implements_req` / `@tests_req` marker moves (`SwRS-MDOKFSTUDIO-CORE-078` on
   `scripts/release_notes.py` stays as it is). No `requirements/tiers/log.md` entry.
7. **No `CHANGELOG.md` line**: a `docs` change with no user-facing change ("No user-facing change"
   in the PR template). Commit type `docs`, no scope (scopes are for `feat` and `fix` only), for
   example `docs: release notes highlights start with text, pictures cropped on the change`.
8. **No link to the process guideline** is added to `release-process.guidelines.md`:
   `test/build/test_guideline_isolation.py` fails when a project rule links to
   `change-requests-lifecycle.guidelines.md`.

## Out of scope

- Rewriting or re-cropping the notes or images of any past release (1.10.0 included).
- Any change to `scripts/release_notes.py`, its tests, the justfile or CI.
- chantier's `release-template.md` (a separate note to chantier, sent by the Chief of Staff).
- The announcement thread, the hero image, the version PR body.

## Evidence

The guideline is read from the repository at the head under test.

1. `.agents/guidelines/release-process.guidelines.md`, section `## Release notes`, at the PR head:
   - "Writing" says a highlight is its heading, then at most two sentences, then the picture;
   - "Writing" says each picture is cropped to the part of the screen where the change happens (no
     toolbar, empty margin or unrelated content), and that a joined before | after image crops both
     halves to the same region at the same scale;
   - "Writing" still holds the joined before | after rule, the whole-change rule (now: no sentence),
     the setting rule and the "Never use" list;
   - "Structure" item 3 gives sentences, then one cropped picture, then the optional Markdown
     example;
   - "Images" says the captures are cropped before they are joined;
   - the intro no longer says "in pictures first";
   - no other section of the file changes (`git diff main -- .agents/guidelines/release-process.guidelines.md`
     touches only `## Release notes`).
2. `git diff --stat main` lists only that file.
3. `just check` passes (it runs `release-notes-check` on the 1.10.0 notes, unchanged, and the build
   tests, including `test/build/test_guideline_isolation.py`).
4. `just preflight` passes; on Windows its static stage, as AGENTS.md says ("Completion gate"),
   with CI running the other jobs.
5. Reading check: the owner's example above follows the new "Writing" and "Structure" item 3 as
   written, word for word in order (heading, one sentence, picture).

## Open questions

None.
