# A project's CoS or Griller does not grill another project's CR

Short name: `own-project-grill`. Cards only; no CLI change. Bound for the running batch batch-31.

## Goal

In a planning surface with several projects, a Chief of Staff or a Griller works on its own
project's CRs. By default it does not grill, specify, order or run a CR of another project of the
surface. It may file (relay) an item into another project's inbox on the user's word; it then says,
in one line, that the CR waits for that project's own Chief of Staff or Griller, and offers no
grill, specification, batch or order for it. Only the user's explicit word for that CR (for
example "grill it here") lifts the default.

What happened (`intake/request.md`): okf-schema's Chief of Staff filed two CRs in chantier's inbox
on the owner's word, then offered to grill them. Their grill belonged to chantier's own sessions.

## Words

- **The session's project:** the project whose folder `$CHANTIER`'s `--project` holds for the
  session (`session-start.md`, "2. The seat and the role": "the Chief of Staff first learns its
  project ... the seat is that project's"). In-project mode has one project: the rule never
  applies there.
- **Another project's CR:** a CR folder under another `projects/<name>/changes/` of the same
  surface.

## What changes

All three edits are in `skills/chantier/references/` and in the cards only (answers Q1, Q2). The
text below is the content to carry; the Driver may adjust the wording to the card's style, but
keeps the phrase **"waits for that project's own Chief of Staff or Griller"** verbatim in each of
the three places (the checks read it).

### 1. `session-start.md`, "## 2. The seat and the role"

After the opening paragraph ("In a surface with several projects, the Chief of Staff first learns
its project ... the seat is that project's."), add a paragraph that holds for the Chief of Staff and
the Griller alike:

> The session's CRs are that project's too. By default it does not grill, specify, order or run a
> CR of another project of the surface: it may file (relay) an item into another project's inbox on
> the user's word (`file` with that project's `--project`), then says in one line that the CR waits
> for that project's own Chief of Staff or Griller, and offers no grill, specification, batch or
> order for it. Only the user's explicit word for that CR ("grill it here") lifts the default
> ([chief-of-staff](chief-of-staff.md), "Backlog and grill").

### 2. `chief-of-staff.md`

- **"## Backlog and grill"**, right after the paragraph that starts "`file` keeps the request as
  received in `intake/request.md`", add a paragraph "**Another project's CR.**" carrying the rule:
  in a surface with several projects, a CR of another project is that project's; filing (relaying)
  one there is allowed on the user's word, with the skill's command and that project's
  `--project <absolute folder>` for that `file` alone (`$CHANTIER` keeps the session's own
  `--project`); `file` then prints its usual `filed <folder>; write the intent and grill the CR
  here`, whose "grill the CR here" is not followed for another project's CR: say instead, in one
  line, that the CR waits for that project's own Chief of Staff or Griller, and offer no grill,
  specification (`spec-writer`, `spec-critic`), `triage`, batch or `order` for it. Only the user's
  explicit word for that CR lifts the default, and only for that CR.
- **"## Never"**, add one bullet: "Grill, specify, order or run a CR of another project of the
  surface without the user's explicit word for that CR (filing one there on the user's word is
  allowed; "Backlog and grill")."

### 3. `griller.md`

- **"## Never"**, add one line, in the card's style: "Grill, specify or triage a CR of another
  project of the surface without the user's explicit word for that CR: you may file (relay) one
  there on the user's word, then say it waits for that project's own Chief of Staff or Griller, as
  [chief-of-staff](chief-of-staff.md)'s "Backlog and grill" says."
- **"## Started from the board"** is not changed: the board starts that run on the CR a holder of
  the private key chose, which is the user's word for that CR. This also keeps the board Griller's
  startup reading (`startup-manifest.json`, `startup_sections["board-griller"]`, under its
  `limit`) unchanged.

### What `file` prints (answer Q3)

The one line "the CR waits for that project's own Chief of Staff or Griller" is the cards'
instruction, said by the session, not a line printed by `file`: the CLI knows no role and not the
session's own project (Q2, Q3), so it cannot tell a relay from an ordinary filing.
`lifecycle/backlog.py`'s `file_idea` return line is not changed (see the open questions).

### The CLI (answer Q2)

No refusal is added. The CLI already reads a CR folder argument against its `--project`'s planning
folder (`Repo.planning_path` in `core/repo.py`, through `project_path`), so a command on another
project's CR with the session's own `$CHANTIER` is refused as today. No file under
`skills/chantier/scripts/cli/src/` changes.

## Decisions carried from `02-answers.md`

| Answer | Where in this specification |
| --- | --- |
| Q1 A: the rule lives in the Chief of Staff card, the Griller card and `session-start.md`'s seat and role part | What changes, 1 to 3 |
| Q2 A: cards only, no CLI refusal | The CLI |
| Q3 A: one line, the CR waits for that project's own Chief of Staff or Griller, nothing offered; card instruction or `file` output left to the specification within Q2 | What `file` prints: the cards' instruction |
| Item 4: only the user's explicit word for that CR lifts the default; filing into another project's inbox stays allowed on the user's word | What changes, 1 to 3 |
| Q4 A: specify for the running batch batch-31 | Header; the CR's `work/running-batch` mark |

## Out of scope

- Any CLI refusal or new CLI output (`file`, `order`, `open`, `triage`, `summary`): Q2.
- The board Griller's brief and its "Started from the board" section.
- The Copilot and Claude Code agent wrappers (`agents/`, `com.github.copilot/agents/`): their
  bodies do not carry this rule and do not change.
- The skills' `SKILL.md` startup cores (`skills/chief-of-staff/`, `skills/griller/`,
  `skills/chantier/`).
- A row in the Chief of Staff's "Refusals to say before they are met": nothing is refused to the
  user; the user's ask for that CR is the word that lifts the default.
- In-project mode (one project): unaffected.
- `docs/`: no page states which project's CRs a session works on; none changes.

## Evidence

- **Checks on the shipped cards.** In
  `skills/chantier/scripts/cli/tests/test_startup_manifest.py`, add three entries to `MOVED_IN`,
  each reading the card from the repository as it ships, at the head under test (through `_text`,
  no prepared text):
  - `("waits for that project's own Chief of Staff or Griller", START, "2. The seat and the role")`
  - `("waits for that project's own Chief of Staff or Griller", CHIEF_CARD, "Backlog and grill")`
  - `("waits for that project's own Chief of Staff or Griller", REFS / "griller.md", "Never")`
  `_text` joins whitespace, so a phrase wrapped across lines still matches.
- `just check` green at the pushed head (Linux, macOS, Windows in CI); the startup manifest tests
  in it confirm every startup reading stays within `limit` (the board Griller's section is
  unchanged; the other edited sections are not startup readings).
- The long gate `just scenario` (ubuntu-latest), green at the PR's head: a change to the cards
  passes it before its PR (`AGENTS.md`). No `just eval-dry-run` (no change under the CLI's `src/`
  or `evals/kit/`), no `just mod` (no change to `hooks/` or `types/`).
- No host or default matrix: the rule does not depend on the host or on a configured value.

## Open questions

1. `file` prints `filed <folder>; write the intent and grill the CR here` for every filing, a relay
   into another project included, where its "grill the CR here" invites exactly the offer this CR
   forbids. This specification keeps the line and has the cards say it is not followed for
   another project's CR. Should the printed line instead become neutral (for example `filed
   <folder>`, the next step left to the cards), a CLI output change that touches no refusal and
   no role? Recommendation: keep it as specified (cards only), as Q2 chose.
2. The user's explicit word for another project's CR ("grill it here"): does it lift the default
   for that CR's whole path in this session (grill, then specification, then `triage`), or only
   for what the word names (a grill, but the specification needs its own word)? This
   specification says "for that CR" and leaves the reach to the word as given.
