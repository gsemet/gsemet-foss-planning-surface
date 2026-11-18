# Answers

- The user (2026-11-18): "Oui, spécifie les P1", after the standing word of the day "plus de question" (no more questions): no grill; the behaviour choices below are the Chief of Staff's.

## Settled by the Chief of Staff

- **The setting.** Whether a CR's cleaned archive goes in its PR comes from the project's settings (the existing archive setting the investigation names, else one key in `chantier.yaml`), read once into `Repo.archive_in_pr`; `take` and `ship` read that, and stop expecting or refusing on a missing archive when it is off.
- **The default.** With an external planning surface (the CRs kept outside the project's repository), the default is off; in a project that keeps its CRs in its own `.agents/changes`, the default is unchanged. AGENTS.md's "a CR's cleaned archive in its PR when the project asks for it" stays true.
- **The cards.** The Driver's card and the PR template no longer ask for the archive when the setting is off, so nobody has to tell a Driver by hand.
- Spec critic: yes, it changes a CLI refusal and what a Driver ships.
- Settled by the Chief of Staff (2026-11-18, the spec-writer's open question): no `Archive in the PR: yes` line is added to agentic-planning-surface or okf-schema; their CRs live on the surface, so the new default (off) is the intended behaviour for them too.
- Settled by the Chief of Staff (2026-11-18, spec critic finding 1, "plus de question"): A. The default becomes `no` for every external surface even though the line already exists: a project whose CRs live on the surface should not have to declare it. The change is named in the CHANGELOG (or the release notes the project keeps) as a default change, with the `- Archive in the PR: yes` line to keep the old behaviour.
