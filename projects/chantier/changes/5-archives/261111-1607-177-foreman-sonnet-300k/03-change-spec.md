# Change Specification: Sonnet by default for the Foreman and the Drivers, escalation on named trouble, a 300K auto-compact window

## Goal

The user's words: "Je voudrais recommander l'utilisation de sonnet 5.5 avec un autocompact à
300K" and "J'aimerais que on l'utilise un maximum et quand il y a un soucis il y a une escalade
vers un modèle plus puissant."

On Claude Code, chantier runs the Foreman and every Driver on Sonnet 5.5 by default. When a task
hits one of five named troubles, it goes to a new agent on a stronger model, and the report says
so. The recommended auto-compact window for the Foreman's and the Chief of Staff's sessions is
300K. The rule is written generically: the cards speak of "the default model" and "the
escalation model" printed by the CLI, never of a model name. Only the host reference, the
README, the tutorial and the CLI's model table name actual models.

Context: batch-09 cost $93.53, with steering at 46 %, Drivers at 17 % and workers at 36 %.

## Decisions carried from `02-answers.md`

1. On Claude Code, Sonnet 5.5 by default for the Foreman, the stack driver and the release
   driver. They join the CR and QA drivers and the workers, which already run Sonnet. The
   Spec-writer stays on Opus 5.5.
2. The Chief of Staff's session stays on Opus 5.5 (a recommendation: it is the user's session).
3. Escalation to Opus 5.5 on named triggers, written in the cards: a CR blocked twice; the rounds
   used up with the Inspector still `FIX-REQUIRED`; a red check the Debugger could not explain;
   a conflict the resolver could not settle; a restack that failed. The task then goes to a new
   agent on Opus, and the report says so. Never a silent swap.
4. The recommended auto-compact window is 300K for both the Foreman's and the Chief of Staff's
   sessions.
5. Left to the Chief of Staff: the effort stays `medium`; Copilot is untouched ("laisse copilot
   dans son coin"); the escalation model is the host's default, one for all roles (a per-role
   `escalate` key in `chantier.yaml` is left for later, see "Settled decisions" 7).

## What changes

### 1. Agent files (Claude Code only)

- `agents/stack-driver.md` and `agents/release-driver.md`: `model: claude-opus-5-5` becomes
  `model: claude-sonnet-5-5`. `autoCompactWindow: 200000` stays.
- `agents/spec-writer.md` stays `claude-opus-5-5`.
- `com.github.copilot/agents/*` are not touched: no model, no body change. The bodies of both
  hosts stay identical, because only the Claude frontmatter changes.

### 2. The Foreman's session (Claude Code)

- `skills/chantier/references/hosts/claude-code.md`, Tools row "Start the Foreman's session":
  `model: "claude-sonnet-5-5"`, `effort: "medium"` (kept). Mark: the start with this model is
  **unproved** until it is seen. The trial is batch-11, where the Foreman was switched to Sonnet
  5.5 after its `ready` (CR-174), plus the first batch started with the new row: the transcript
  shows `claude-sonnet-5-5`, and `effort: "medium"` is accepted with it. Record the date once
  seen.
- Same file, row "Models": the Spec-writer runs Opus 5.5. The Foreman, every Driver and the
  workers run Sonnet 5.5, unless the project's `chantier.yaml` sets a model. A task under
  escalation (concepts, "Escalation") runs the escalation model that the CLI prints. Keep the
  existing marks; the stack, release and Foreman parts are unproved until the trial above.
- `hosts/copilot.md`: unchanged (its Foreman stays `claude-opus-5.5`).

### 3. Escalation: the rule (cards)

Add a section **"Escalation"** to `skills/chantier/references/concepts.md`, after "Starting an
agent". The section is generic, with no model name:

- An agent's model is fixed when it starts. Escalation is a **new** agent for the same task,
  started with the escalation model that `$CHANTIER playbook` printed (see 4), passed as
  printed like any model. It is never a change of a running agent's model, never a retry of the
  same agent, and never a model typed from memory (rule 2, "No fallback").
- It happens only on one of the five triggers below, by the parent named for each:

  | Trigger | Who sees it | The new agent on the escalation model |
  | --- | --- | --- |
  | A CR blocked twice: two hand-backs `blocked` of the same CR that show trouble in the work (`refused`, `infra:` after its one re-run, `driver ended twice`, `stopped`). A hand-back that waits on the user or on another thing never counts (`question:`, `approval:`, `merge:`, `waits:`, `fix:`, `budget:`), nor does `rounds:`, which has its own trigger below | the Foreman (in direct mode the Chief of Staff), from `log <cr>` / the hand-backs | the CR's next CR Driver, with `take <cr> --note "escalate: blocked twice: <reasons>"` |
  | The rounds used up with the Inspector still `FIX-REQUIRED` | the CR Driver hands back `blocked rounds:` as today; the round limit stays the user's (`order rounds`); escalation never grants a round | once the user grants more rounds, the CR's next Driver is told `escalate: rounds` and starts the Coder of each new round on the escalation model |
  | A red check the Debugger could not explain (its `diagnosis.md` names no cause with evidence) | the Driver that started it (CR or stack) | a new `debugger` on the same check, given the first `diagnosis.md` |
  | A conflict the resolver could not settle (it stopped with no resolution, other than "two product intents in conflict", which stays a question for the user) | the Driver that started it (CR or stack) | a new `conflict-resolver` on the same rebase, given the first `conflicts.md` |
  | A restack that failed (the stack driver's `anomaly` on rebasing or pushing the stack, not a red check that needs code) | the Foreman | the next stack driver, `take stack` started on the escalation model |

- **Said, never silent:** before it starts the escalated agent, the parent records
  `$CHANTIER note <cr> "escalated: <trigger>; <role> on <model as printed>"` (for the stack, on
  each CR concerned). The Foreman's retro (`4-batch/retro.md`) gives one line per escalation, and
  its outcome. `cost` already shows the model of each transcript.
- **Once per trigger and per task:** if the escalated agent fails the same way, the existing
  route applies (hand-back `blocked`, then the ask to the Chief of Staff). It never escalates
  again and never swaps back. The parent knows from the CR's `escalated:` note.
- **No escalation printed** (a host that cannot set a model at start, such as Copilot today,
  see 4): the trigger takes the existing route. The note says
  `no escalation on this host`. It is not a stop and not a look-alike.

Point to the section from the cards where each trigger arises. Add one line each, with no new
procedure:

- `driver.md`: "Your means" (the escalation line of `$CHANTIER playbook --batch <batch>`, read
  only when a trigger arises, as printed); CR driver (Debugger,
  conflict resolver, `escalate: rounds` note); Stack driver (Debugger, conflict resolver);
  Release driver (none: it starts no children).
- `foreman.md`: "Your means" (a CR blocked twice; a restack that failed; `take ... --note
  "escalate: ..."`; recording in the retro).
- `chief-of-staff.md`, "Steering a batch yourself": the same as the Foreman in direct mode, if
  that section does not already inherit `foreman.md` as written.
- `worker.md`: nothing. A worker does not know it is escalated; its prompt is the same.

### 4. Escalation: what the CLI prints (`playbook.py`)

The parent must pass a printed value (concepts, "Starting an agent"), so the CLI prints the
escalation model. This is not a new command, and it is one line in one place: an escalation is
rare, so the parent reads it when a trigger arises, and `take`, `round` and `handoff` print
nothing more than today.

- `playbook.py`: one default escalation model per host, taken from the host's table (Claude
  Code: the `opus` entry; Copilot: none, because `SETS_MODEL_AT_START["copilot"]` is `False`).
  Keep it next to `MODELS` so a release changes both together. It is the same for every role;
  `chantier.yaml` has no key for it in this CR.
- Printed: `$CHANTIER playbook` and `playbook --batch <batch>` end with one line
  `escalate: <start> (<id>, <name>)`, or `escalate: (none on this host)`. The role lines and the
  `team:` lines do not change. The exact text is the Driver's to choose.
- The CLI knows no trigger and no role meaning: it prints a value; the cards say when it is used.

### 5. Auto-compact recommendation

- `hosts/claude-code.md`, "Compacting", **Recommendation**: `autoCompactWindow` 300000 (was
  400000) in `~/.claude/settings.json` for the Chief of Staff's and the Foreman's sessions. The
  JSON block becomes `{ "idleCompaction": true, "autoCompactWindow": 300000 }`. Keep the
  unproved note: sessions set to 300000 compacting around 165 to 170k tokens. It now concerns
  the recommended value itself, so the trial named there settles the recommendation. Add that the
  window is capped at the model's context window (documented, already in the list): if Sonnet
  5.5's window is below 300K, the cap applies, and the trial records it.
- `docs/tutorial-claude-code.md` (lines about 216-224): 400,000 becomes 300,000 in the text and
  the JSON block.

### 6. Docs and rules text

- `README.md`, "Models" table, Claude column: Foreman `Sonnet 5.5, effort medium`; Stack and
  release drivers `Sonnet 5.5`; Spec-writer `Opus 5.5`; Chief of Staff `your session (Opus 5.5
  recommended)`. The Copilot column is unchanged. Below the table, replace "The roles that
  judge ... run Opus, except the CR driver ..." with this: by default every role but the
  Spec-writer runs Sonnet 5.5 on Claude Code. The roles that judge keep cards with goals and
  boundaries, not procedures. On a named trouble a task goes to a new agent on the escalation
  model (Opus 5.5 by default), and the report says so. On Copilot the models are its agent files'
  models. Add the 300K recommendation where the README speaks of compaction, if it does.
- `docs/tutorial-claude-code.md` (lines about 212-214): the same defaults and one sentence on
  escalation.
- `CONTRIBUTING.md` line 58: drop the model names from the "judge freely" sentence. It becomes
  "the Foreman and the Drivers judge freely", so the rule no longer depends on a model.
- Diagrams `docs/how-chantier-works.svg` / `how-chantier-works-texts.md` ("a nested session ·
  Opus 5.5 · one per batch") and `docs/how-chantier-works-simple-foreman.svg` / `-texts.md`
  ("one session per batch of changes · Opus 5.5 · orchestrates"): remove the model from the
  line, so the diagrams stay host-neutral. Keep the texts file and the SVG in step.

### 7. Structure test

`skills/chantier/scripts/cli/tests/test_structure.py`: `OPUS_ROLES` holds both hosts today
(lines 23, 125, 126). Split it:

- Claude: `{"spec-writer"}`.
- Copilot: `{"stack-driver", "release-driver", "spec-writer"}`, unchanged.

Keep the other assertions. Add no test of the workflow (AGENTS.md: structure only).

## Out of scope

- Copilot: models, agent files, `hosts/copilot.md`, the Copilot column of the README.
- The Chief of Staff's model (stays a recommendation of Opus 5.5) and the Spec-writer's.
- The effort: stays `medium` for the Foreman; still no effort for agents.
- Setting the Foreman's model in `chantier.yaml` (the Foreman is a session, not a plugin agent;
  CR-169 left it out).
- An escalation of the steering session itself (a Foreman that cannot read a hand-back): it was
  a candidate trigger and was not picked. No `set_session_model` use.
- Any new CLI command, and any CLI knowledge of the triggers.
- An `escalate` key in `chantier.yaml` (a per-role or per-project escalation model), and any
  escalation field in the `team:` lines of `take`, `round` and `handoff`: later, on a real need.
- Changing the agents' own `autoCompactWindow: 200000`.

## Evidence

- `just check` passes (Linux, macOS, Windows), with the split `OPUS_ROLES`.
- `just scenario` passes, with steps added in `scenario/run_scenario.py` next to the existing
  playbook steps (around lines 1620-1700):
  - `playbook` and `playbook --batch` end with `escalate: opus (claude-opus-5-5, Claude Opus
    5.5)` on Claude Code, with and without a `chantier.yaml`, and with `escalate: (none on this
    host)` on Copilot.
  - The `stack-driver` and `release-driver` lines show `model=(its file's)`, with the files at
    `claude-sonnet-5-5`.
- Read-back: `hosts/claude-code.md` rows 18 and 33, the Compacting recommendation, the README
  table, the tutorial and CONTRIBUTING say the same defaults. `grep -i opus` in the cards
  (`skills/chantier/references/*.md`, outside `hosts/`) finds no model name in the escalation
  rule.
- Trial, recorded by the Chief of Staff in `hosts/claude-code.md` with its date: batch-11's
  Foreman transcript (CR-174) shows `claude-sonnet-5-5` from its switch on, and the steering at
  the batch's end. The first batch started with the new row shows the Foreman, stack and release
  drivers on `claude-sonnet-5-5`. The first escalation seen shows its note, its retro line and an
  Opus transcript in `cost --explain`.

## Settled decisions

Decided by a Fable advisor on the user's delegation (2026-11-11), numbered as in
`02-answers.md`.

6. **"A CR blocked twice" counts** the hand-backs `blocked` that show trouble in the work:
   `refused`, `infra:` after its one re-run, `driver ended twice`, `stopped`. It does not count
   the ones that wait on the user or on another thing (`question:`, `approval:`, `merge:`,
   `waits:`, `fix:`, `budget:`), nor `rounds:`, which has its own trigger: one trouble never
   pays for two escalations.
7. **The `escalate` key in `chantier.yaml`: later.** This CR has one escalation model per host,
   the same for every role. No project has asked for another one, and the cards name no model,
   so the rule already works in any project.
8. **Once per trigger and per task: confirmed.** An escalated agent that fails the same way
   takes the existing route (`blocked`, then the ask); it never escalates again and never swaps
   back.
9. **The CLI prints the escalation model in one place:** one last line of `playbook` and
   `playbook --batch`. `take`, `round` and `handoff` are unchanged: an escalation is rare, and
   a parent reads the line when a trigger arises.
10. **The structure test's `OPUS_ROLES` is split per host, as written in 7:** the two hosts'
    agent files now differ in model, and the test must say so.

## Open questions

None.
