A critic agent reviews each Change Specification before it is final.

The user (2026-11-14): "Est ce que tu crois qu'un action supplémentaire sur la spec pourrait aider ? Par exemple un sous agent critique qui s'assure que la spec répond à l esprit de la demande, identifie des problème d'incohérence avec le reste du soft ? La spec a souvent levé des questions mais comment être sur qu'elle trouve toutes les incohrence possible ?"

The Chief of Staff's proposal, accepted for a trial on CR-250's spec (answer "A"):
- a fresh agent, not anchored on the grill: it reads only the request, `02-answers.md`, the specification and the repository;
- it looks for: a gap between the specification and the spirit of the request; an inconsistency with the rest of the software (cards, CLI, docs, and the other pending CRs that touch the same files); claims about the real world that are unproved;
- each finding goes back as a question for the user, in the grill's format, through the spec-writer; the critic does not edit the specification.

Evidence: CR-250's spec-writer wrote "no question tool under Remote Control", unproved; the user caught it, not the spec.
Related: the inbox item `retro-critic` (the same principle for retros).
Trial on CR-250 (2026-11-14): an Opus critic with no grill context found 10 points on a spec the user had called grilled enough: 4 needed the user (option count vs the tool's 2-4, where the recommendation goes, two sessions on one item, the closing question's format), 6 were spec-writer or record fixes; no conflict with CR-248 or CR-249.

The user (2026-11-14): "Il faudra mettre à jour la doc et les svg avec ce spec critic." The CR updates the docs and the SVGs that draw the spec step (cr-lifecycle.svg, cr-lifecycle-simple.svg, how-chantier-works*.svg, and the pages that describe the spec), and the new linear lifecycle diagram of the inbox item lifecycle-line-svg, if that one lands first.
