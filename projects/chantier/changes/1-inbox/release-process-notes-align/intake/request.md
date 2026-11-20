# release-process.md: align the notes rules with CR-413's template

Priority P2. Follow-up of CR-413 (release-notes-writing-rules, batch-29, PR #378), a known gap its Driver named.

`docs/release-process.md` (lines 47-51 at CR-413's head) still asks each highlight for a usage example, a link to the doc and a "why it matters" sentence. For chantier's own releases that file ranks above `skills/chantier/references/release-template.md`, so it contradicts the rules CR-413 put in the template ("Never use: ... a closing 'why it matters' line"; a highlight is a heading, a picture, at most two sentences).

Align `docs/release-process.md` with the template's "The notes" and "Visible evidence": keep only what is specific to chantier's releases, and point to the template for the writing rules instead of restating them.
