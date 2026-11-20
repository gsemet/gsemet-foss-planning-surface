# Change Specification: release notes, short and demo-first

Short name: `relnotes-style`

## Goal

The next release (1.10) and every later one ship notes that show what the release brings the user,
mostly through pictures, with the detail folded. The rules live in the project's release guideline,
complete on their own: chantier's release template is not updated in time.

## Base

`main` (docs only, no code). Must merge before the 1.10 release CR runs.

## What changes

### A. `.agents/guidelines/release-process.guidelines.md`, section "Release notes"

Rewrite the section:

1. A "Writing" paragraph with the approved prompt of `02-answers.md` (tone, banned forms).
2. The structure, keeping Studio's own parts unchanged: the centred `<h1>`, the bold line of verbs,
   the `<sub>` line and its `git rev-list` command, the centred links line and `---`.
3. Highlights: two to four `## <emoji> <what you can now do>`; a picture; at most two sentences;
   the three picture rules of the prompt (one joined before|after image for a changed visible
   behaviour; no text when the picture shows it all; settings named as "the setting
   `markdownOkfSchemaStudio.…`", default value, set in the VS Code settings). A new syntax may add a
   short Markdown example under the picture.
4. Remove from the highlight: the explanatory paragraph and the closing "why it matters" sentence.
5. Smaller changes: one line per bullet (keep the bold lead). Folded: `🐞 All fixes`, a
   `🔎 Details` section (how things work, keyboard, defaults, limits) and `🛠 For contributors`.
6. Keep: `<kbd>`, the coverage rule, the "Images" and "Publishing" subsections.
7. In "Images": the joined before|after image is one file in the notes folder, made from the
   Verifier's before and after captures of the merged CRs (any tool; say which in the PR).

### B. Hero image and announcement thread

Unchanged, except the thread's banned words now point to the same "Writing" list.

### C. Changelog

No user-facing change: no CHANGELOG line (internal docs).

## Out of scope

Rewriting past release notes; chantier's release template (sent to chantier's CoS);
`scripts/release_notes.py` (it only checks the title and the images, unaffected).

## Evidence

- The PR body shows the rewritten section and try E from `02-answers.md` as the example it yields.
- `just check` and the docs/format checks green; `just release-notes-check` still green on 1.9.3.

## Gates

Short gate only (docs change); no heavy CI needed.
