# The automatic reload after a compaction loads the role's skill again

After a compaction of the main loop of a session that loaded a chantier role skill, the
`session.compact` hook (`hooks/register.tsx`, `RELOAD_LINE`) adds one user message telling the model
to follow `session-start.md`, "5. Reload". That reload reads only the short cores (startup-core,
role-core, host-core) and the Reload section: the role's own `SKILL.md` is not injected again, so
the compacted session works from the summary's memory of it.

The user's wish (2026-11-17): the line tells the model to call the Skill tool for the role(s) the
session loaded (the `roles` atom already holds them: `chantier`, `chief-of-staff`, `griller`), with
the argument `reload`, before anything else, e.g. "after a compaction: load the skill
chantier:chief-of-staff with the argument reload now, before any other step". A hook cannot run a
slash command or call a tool itself; the message is the strongest means it has.

The wording, the user's (2026-11-17): plain and short, of the form "You are the <ROLE> in a
chantier session; after this compaction, call the skill <skill> now." (the role and the skill filled
from what the session loaded).

To settle in the grill: which skill when several roles were loaded (the last
one, or each); what the `reload` argument does in `chief-of-staff` and `griller` (today only the
router names it); that a reload still makes no batch change and asks no role.

Gates: a change to `hooks/` passes `just mod` before its PR (AGENTS.md); the pane is not changed.
