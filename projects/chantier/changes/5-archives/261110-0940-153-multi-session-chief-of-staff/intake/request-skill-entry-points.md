# Two skill entry points: Chief of Staff with a Foreman, Chief of Staff direct

## The user's words (2026-11-10, French, verbatim)

> Les points d'entrée du skill du plugin doivent changer. Il faut
> /chantier:chief-of-staff-with-foreman and chief-of-staff-direct. Attention de bien réutiliser
> le maximum de skill (l'un peu appeler l'autre).
>
> Raison une petite CR pour ça

## What is asked

- Replace the plugin's single entry point (`/chantier:chantier`, `skills/chantier/SKILL.md`) by
  two: `/chantier:chief-of-staff-with-foreman` and `/chantier:chief-of-staff-direct`.
- The steering mode is chosen by the skill the user invokes, not discussed in the plan.
- Reuse as much as possible: no duplicated text. One skill may call the other (e.g. the direct
  skill loads the common Chief of Staff body and adds its "Steering a batch yourself" part).
- A small CR.

## Chief of Staff notes

- Today: one skill folder `skills/chantier/` holds `SKILL.md`, the cards (`references/`), the CLI
  (`scripts/cli/`) and the assets; the mode is picked at `preflight`/`open` (`--direct`), and
  `chief-of-staff.md` step 2 proposes direct mode by host or batch size.
- To settle in the grill:
  - where the shared body lives (one skill folder with the cards and the CLI, the two entry
    skills thin; or one skill calling the other);
  - whether `/chantier:chantier` stays as an alias or goes away (an existing user's habit, the
    docs, the init tour, `plugin.json`, `marketplace.json`, release notes mention it);
  - whether step 2's proposal of direct mode remains (e.g. the Foreman skill on a host that cannot
    start a Foreman session);
  - the `$CHANTIER` path each skill computes (it points at the CLI in the skill's folder today);
  - Copilot (`com.github.copilot/`): same two entry points?
  - `tests/test_structure.py` checks that may name the skill.
- Meets the P1 `multi-session-chief-of-staff` (the role a session takes at start, Planners,
  "usual set-up: one Chief of Staff in direct mode"): order the two, or fold this into it.
