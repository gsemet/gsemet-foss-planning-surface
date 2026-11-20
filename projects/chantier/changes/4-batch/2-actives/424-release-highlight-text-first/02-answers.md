# Answers

## 2026-11-20, the bundle

This CR carries two requests on one topic, the release notes rules:

- its own `intake/request.md` (the template: text before the picture, the picture cropped);
- `1-inbox/release-process-notes-align` (align `docs/release-process.md` with the template),
  bundled here and then abandoned. Its request, copied whole so that this CR stands alone:

  > Priority P2. Follow-up of CR-413 (release-notes-writing-rules, batch-29, PR #378), a known
  > gap its Driver named.
  >
  > `docs/release-process.md` (lines 47-51 at CR-413's head) still asks each highlight for a
  > usage example, a link to the doc and a "why it matters" sentence. For chantier's own releases
  > that file ranks above `skills/chantier/references/release-template.md`, so it contradicts the
  > rules CR-413 put in the template ("Never use: ... a closing 'why it matters' line"; a
  > highlight is a heading, a picture, at most two sentences).
  >
  > Align `docs/release-process.md` with the template's "The notes" and "Visible evidence": keep
  > only what is specific to chantier's releases, and point to the template for the writing rules
  > instead of restating them.

Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the two pair on
the same rules, and the first request says the second "can carry it in the same batch"; one CR
keeps the template and the file that ranks above it true together.

## 2026-11-20, settled without the user

The user asks no questions tonight ("tu es maintenant autonome. plus de question. tu grilles tout
seul"). Each point below is: Settled by the Chief of Staff (2026-11-20, the user asks no
questions), by the narrowest choice that meets the requests, with its reason.

1. **The order of a highlight.** Heading, then at most two sentences, then the picture. When the
   picture shows the whole change: no text, the highlight is its heading and the picture. Settled
   by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the user's words ("le
   paragraphe commence par le texte") and the request's "Kept".
2. **Which pictures are cropped.** Every picture of the notes, whatever its source (a Verifier's
   capture, a PR's screenshot, a capture by the Driver, CLI output): only the part where the
   change happens. Settled by the Chief of Staff (2026-11-20, the user asks no questions).
   Reason: the request says "each picture".
3. **Who crops, and with what.** The release Driver, when it builds the highlight's image, with
   the means the project's procedure gives; the template names no tool. Settled by the Chief of
   Staff (2026-11-20, the user asks no questions). Reason: the Driver already builds the joined
   before and after image; the mechanics are always the project's own.
4. **A picture the Driver cannot crop.** It stays whole, and the Driver says so in a `note`; no
   other image is invented in its place. Settled by the Chief of Staff (2026-11-20, the user asks
   no questions). Reason: the project's "no fallback" rule and the template's "no invented
   image".
5. **The thread's image.** No rule of its own: it is one of the notes' pictures, so it is already
   cropped. Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the
   request targets "A highlight" and "Visible evidence" only.
6. **What `docs/release-process.md` keeps of a highlight.** Only what is chantier's own: the
   count (two to four) and the heading's form, `## <emoji> <what the reader can now do>`. The
   short paragraph, the usage example, the link to the doc, the "why it matters" sentence and the
   before/after pair in a two-column table go; the rest is the template's "A highlight", by a
   link. Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: each
   removed line restates or contradicts the template (one joined image, no closing line); the
   emoji heading is in every published chantier release and the template is silent on it.
7. **How far the alignment goes in `docs/release-process.md`.** "Release notes" (item 3 and the
   pointer to the template's writing rules), the sentence on rank in the introduction, and one
   sentence on the crop in "Visuals". The header, the links, Smaller changes, the folded
   sections, the release folder, Images, Anonymisation, the announcement thread and "Which batch"
   stay. Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the
   request names the template's "The notes" and "Visible evidence"; the rest is chantier's own
   mechanics or another section.
8. **No new check.** `scripts/release_notes.py --check` is not changed. Settled by the Chief of
   Staff (2026-11-20, the user asks no questions). Reason: it cannot read pixels, and a check of
   a highlight's order is a new tool with no measured cost.
9. **Published notes.** The release folders under `docs/release-notes/` are not rewritten.
   Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: the rules hold
   from the next release on.
