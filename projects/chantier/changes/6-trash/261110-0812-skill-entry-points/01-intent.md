# Intent: two skill entry points, the steering mode chosen at invocation

Intake: `intake/request.md` (the user's words of 2026-11-10, in French). Analysed against v0.8.0.

## The request

The plugin's one entry point, `/chantier:chantier`, becomes two:
`/chantier:chief-of-staff-with-foreman` and `/chantier:chief-of-staff-direct`. The skill the user
invokes says how the session's batches are steered. The two share everything they can: one may
call the other, and no text is duplicated. A small CR.

## Today (v0.8.0)

- One skill folder, `skills/chantier/`: `SKILL.md` (introduction, entry points, hard rules), the
  cards in `references/`, the CLI in `scripts/cli/`, the assets. `$CHANTIER` is computed from that
  folder's path.
- The mode is picked when a batch starts: `chief-of-staff.md`, Starting a batch, step 2 proposes
  direct mode (host cannot start a Foreman, or few CRs); `preflight --direct`, `open --direct`.
- The name `/chantier:chantier` appears in `plugin.json`, `marketplace.json`, the docs, the init
  tour and the release notes.

## Batch

To run with the P1 `multi-session-chief-of-staff` in one new batch, in series (user's word,
2026-11-10). Both touch `SKILL.md` and the role a session takes at start.
