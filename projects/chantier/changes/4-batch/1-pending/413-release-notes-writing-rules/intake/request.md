# Release notes: shorter, plain, picture-first highlights

Priority P2. From the Studio project's Chief of Staff, at the user's request (2026-11-20): rules the user validated on a trial of Studio 1.10's notes. Studio carries its own copy in its guideline until chantier's template has them.

Target: `skills/chantier/references/release-template.md`, section "The notes" (and "Visible evidence" for the before/after image). They replace, in the current structure, "a usage or call example, ... a link to the doc, and why it matters" for each highlight.

**Release notes: writing**
Write like a maintainer telling a colleague what changed. Use short, complete sentences, plain verbs, and "you". Write for the user: no ticket numbers, no internal terms, no implementation.

**Structure**
- A title.
- One line naming the two or three main changes, as verbs.
- Two to four highlights.
- The smaller changes, one line each.
- Every fix and detail in folded sections.

**Each highlight** is a heading that says what you can now do, then a picture, then at most two sentences.
- When the change replaces a behaviour you can see, the picture puts the before and the after side by side in one image (built from the Verifier's before/after), and the text does not describe the before again.
- When the picture shows the whole change, write no text under it.
- Name a setting as a setting: "the setting `full.name`", with its default value and where to turn it on.

**Never use:** "Before:" or "Now:" labels; invented scenes; punchy fragments ("Two gestures."); praise words (seamless, powerful, effortless, easily); a closing "why it matters" line.

**Coverage:** every changelog line appears once, visible or folded.

Out of scope: the labelled "Before / After" in PR bodies (pr-template) stay as they are; only the release notes change.
