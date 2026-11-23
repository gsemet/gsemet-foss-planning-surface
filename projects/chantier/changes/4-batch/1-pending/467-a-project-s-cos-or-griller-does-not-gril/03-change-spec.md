# A project's CoS or Griller does not grill another project's CR

Short name: `own-project-grill`. Cards only; no CLI change. Bound for the running batch batch-31.

## Goal

In a planning surface with several projects, a Chief of Staff or a Griller works on its own
project's CRs. By default it does not grill, specify, triage, order or run a CR of another project
of the surface. It may file (relay) an item into another project's inbox on the user's word. It
then says, in one line, that the CR waits for that project's own Chief of Staff or Griller. It
offers no grill, specification, batch or order for it, and writes nothing more in it. Only the
user's explicit word for that CR (for example "grill it here") lifts the default, for that CR's
grill, specification and triage; launches stay outside that word.

What happened (`intake/request.md`): okf-schema's Chief of Staff filed two CRs in chantier's inbox
on the owner's word, then offered to grill them. Their grill belonged to chantier's own sessions.

## Words

- **A session's own project:** the one its `$CHANTIER`'s `--project` names; for the Chief of
  Staff, the seat's (`session-start.md`, "2. The seat and the role"). In-project mode has one
  project: the rule never applies there.
- **Another project's CR:** a CR folder under another `projects/<name>/changes/` of the same
  surface.
- **A relay:** a `file` into another project's inbox, on the user's word, run with the skill's
  command and that project's `--project <absolute folder>` for that `file` alone (`$CHANTIER` keeps
  the session's own `--project`).

## What changes

All edits are in `skills/chantier/references/`, cards only (Q1, Q2, Q7). The text below is the
content to carry; the Driver may fit the wording to each card's style, but keeps verbatim:

- the phrase **"waits for that project's own Chief of Staff or Griller"** in each of the three
  places below (the checks read it);
- the opening of the `session-start.md` paragraph and the board parenthesis of the `griller.md`
  line, as quoted below (the critic's findings, recorded in `02-answers.md`).

### 1. `session-start.md`, "## 2. The seat and the role"

After the opening paragraph ("In a surface with several projects, the Chief of Staff first learns
its project ... the seat is that project's."), add a paragraph that holds for the Chief of Staff and
the Griller alike:

> A session's CRs are its own project's (the one its `--project` names; for the Chief of Staff,
> the seat's). By default it does not grill, specify, triage, order or run a CR of another project
> of the surface. It may file (relay) an item into another project's inbox on the user's word, then
> says in one line that the CR waits for that project's own Chief of Staff or Griller, offers no
> grill, specification, batch or order for it, and writes nothing more there. Only the user's
> explicit word for that CR ("grill it here") lifts the default, for its grill, specification and
> triage, never for a launch ([chief-of-staff](chief-of-staff.md), "Backlog and grill").

### 2. `chief-of-staff.md`

- **"## Backlog and grill"**, right after the paragraph that starts "`file` keeps the request as
  received in `intake/request.md`", add a paragraph "**Another project's CR.**" carrying:
  - In a surface with several projects, a CR of another project is that project's.
  - A relay is allowed on the user's word: the skill's command with that project's
    `--project <absolute folder>` for that `file` alone; `$CHANTIER` keeps the session's own
    `--project`.
  - `file` prints its usual `filed <folder>; write the intent and grill the CR here` (unchanged,
    Q7); for another project's CR its "grill the CR here" is not followed.
  - Say instead, in one line, that the CR waits for that project's own Chief of Staff or Griller;
    offer no grill, specification (`spec-writer`, `spec-critic`), `triage`, batch or `order` for it.
  - After the relay, nothing more (Q6): no `01-intent.md`, no `summary set`. This is an exception
    to the summary rule of the paragraph above ("A CR's summary ... applies to your own writes
    too") for the `intake/request.md` that `file` wrote: the other project's own Chief of Staff or
    Griller writes the intent and closes the summary.
  - Only the user's explicit word for that CR ("grill it here") lifts the default (Q5): for that
    CR's whole path in this session, its grill, its specification (`spec-writer`, `spec-critic`)
    and its `triage`, with the skill's command and that project's `--project`. A launch (`order
    add`, a batch, `open`) stays outside that word: it needs the other project's batch.
- **"## Never"**, add one bullet: "Grill, specify, triage, order or run a CR of another project of
  the surface without the user's explicit word for that CR (a relay into its inbox on the user's
  word is allowed; a launch stays the other project's; "Backlog and grill")."

### 3. `griller.md`

- **"## Never"**, add one line: "Grill, specify or triage a CR of another project of the surface
  without the user's explicit word for that CR (a run started from the board: the CR its brief
  names is that word). You may file (relay) one there on the user's word, then say it waits for
  that project's own Chief of Staff or Griller and write nothing more there, as
  [chief-of-staff](chief-of-staff.md)'s "Backlog and grill" says."
  The parenthesis "(a run started from the board: the CR its brief names is that word)" is kept
  verbatim (critic's finding).
- **The paragraph "Whenever you write a covered file of a CR"** (in "## What you do"), add at its
  end: "A relay into another project's inbox is the exception: no `summary set` there; that
  project's own Chief of Staff or Griller closes it." (Q6.)
- **"## Started from the board"** is not changed: the Never line above covers the board run. This
  keeps the board Griller's startup reading (`startup-manifest.json`,
  `startup_sections["board-griller"]`, under its `limit`) unchanged.

### What `file` prints (Q3, Q7)

The line "the CR waits for that project's own Chief of Staff or Griller" is the cards'
instruction, said by the session; `file` does not print it. The CLI knows no role and not the
session's own project, so it cannot tell a relay from an ordinary filing. `file`'s line in
`lifecycle/backlog.py` (`file_idea`) is unchanged.

### The CLI (Q2)

No refusal is added. The CLI already reads a CR folder argument against its `--project`'s planning
folder (`Repo.planning_path` in `core/repo.py`, through `project_path`), so a command on another
project's CR with the session's own `$CHANTIER` is refused as today. No file under
`skills/chantier/scripts/cli/src/` changes.

## Decisions carried from `02-answers.md`

| Answer | Where in this specification |
| --- | --- |
| Q1 A: the rule lives in the Chief of Staff card, the Griller card and `session-start.md`'s seat and role part | What changes, 1 to 3 |
| Q2 A: cards only, no CLI refusal | The CLI |
| Q3 A: one line, the CR waits for that project's own Chief of Staff or Griller, nothing offered | What changes, 1 to 3; What `file` prints |
| Item 4: only the user's explicit word for that CR lifts the default; a relay stays allowed on the user's word | What changes, 1 to 3 |
| Q4 A: specify for the running batch batch-31 | Header; the CR's `work/running-batch` mark |
| Q5 A: the word lifts grill, specification and triage for that CR; launches stay outside | Chief of Staff card's paragraph and Never; `session-start.md` paragraph |
| Q6 A: after a relay, nothing more; no intent, no `summary set`; the cards say it is an exception to the summary rule | Chief of Staff card's paragraph; `griller.md`'s summary paragraph and Never line |
| Q7: `file`'s line unchanged; the cards say its "grill the CR here" is not followed for another project's CR | Chief of Staff card's paragraph; What `file` prints |
| Critic: the `griller.md` Never line carries the board parenthesis | `griller.md`, Never |
| Critic: the `session-start.md` paragraph opens with "A session's CRs are its own project's (the one its `--project` names; for the Chief of Staff, the seat's)" | `session-start.md` |

## Out of scope

- Any CLI refusal or new CLI output (`file`, `order`, `open`, `triage`, `summary`): Q2, Q7.
- `concepts.md`'s "A CR's summary": the exception lives in the two cards that apply the rule (Q1).
- The board Griller's brief and its "Started from the board" section.
- The agent wrappers (`agents/`, `com.github.copilot/agents/`) and the skills' `SKILL.md` startup
  cores: they do not carry this rule.
- A row in the Chief of Staff's "Refusals to say before they are met": nothing is refused to the
  user; the user's ask for that CR is the word that lifts the default.
- In-project mode (one project): unaffected.
- `docs/`: no page states which project's CRs a session works on.

## Evidence

- **Checks on the shipped cards.** In
  `skills/chantier/scripts/cli/tests/test_startup_manifest.py`, add these entries to `MOVED_IN`,
  each reading the card from the repository as it ships, at the head under test (through `_text`,
  which joins whitespace, so a phrase wrapped across lines matches; no prepared text):
  - `("waits for that project's own Chief of Staff or Griller", START, "2. The seat and the role")`
  - `("A session's CRs are its own project's (the one its `--project` names; for the Chief of Staff, the seat's)", START, "2. The seat and the role")`
  - `("waits for that project's own Chief of Staff or Griller", CHIEF_CARD, "Backlog and grill")`
  - `("waits for that project's own Chief of Staff or Griller", REFS / "griller.md", "Never")`
  - `("(a run started from the board: the CR its brief names is that word)", REFS / "griller.md", "Never")`
- `just check` green at the pushed head (Linux, macOS, Windows in CI); its startup manifest tests
  confirm every startup reading stays within `limit` (the board Griller's section is unchanged; the
  other edited sections are not startup readings).
- The long gate `just scenario` (ubuntu-latest), green at the PR's head: a change to the cards
  passes it before its PR (`AGENTS.md`). No `just eval-dry-run` (nothing under the CLI's `src/` or
  `evals/kit/`), no `just mod` (nothing under `hooks/` or `types/`).
- No host or default matrix: the rule does not depend on the host or on a configured value.
