# Change Specification: a spec critic checks an impactful CR's specification before it is final

## Goal

The user, 2026-11-14 (`intake/request.md`, in French): one more step on the specification could
help: a critic subagent that makes sure the specification answers the spirit of the request and
finds inconsistencies with the rest of the software. The specification often raised questions,
but nothing makes sure it finds every inconsistency.

The evidence: CR-250's spec-writer wrote "no question tool under Remote Control", unproved, and
the user caught it, not the specification. The trial on CR-250's specification (2026-11-14): an
Opus critic with no grill context found 10 points on a specification the user had called grilled
enough: 4 needed the user, 6 were spec-writer or record fixes.

So: after a specification is written and before it is final, a fresh **spec critic** (🧐) reads
the request, the answers, the specification and the repository, and looks for three things: a
gap between the specification and the spirit of the request; an inconsistency with the rest of
the software; a claim about the real world that is not proved. It never edits the specification.
It runs on the CRs the one who grills judges impactful; that judgement is said to the user before
"grilled enough?". Its findings go to the one who grills, who has the fixes that need no user
applied first, then asks the user the behavioural ones. The docs and diagrams that draw the
specification step show it.

This CR builds on CR-250 grill-question-format (`4-batch/1-pending/250-grill-question-format`),
which rewrites the grill part of `chief-of-staff.md` "Backlog and grill": the question format,
the references `<short name>-Q<n>`, the text before the question tool, the record, and the
closing "grilled enough?" question. Its Driver implements on CR-250's merged text and contradicts
none of it (see "Order" below).

## Decisions carried from `02-answers.md`

The list numbers of `02-answers.md` and the Q numbers differ from answer 8 on (CR-250 allows it);
each decision gives its reference.

1. **When it runs** (spec-critic-Q1): on the CRs the one who grills judges impactful, whatever
   their subject. Priority is no indicator of criticality, complexity or impact, and no subject is
   known in advance to need it. Not on every specification, not only on request, not only on P1s
   or on CRs that touch the CLI or the hooks.
2. **Who gets the findings** (spec-critic-Q2): the one who grills (the Chief of Staff or the
   Griller). It asks the user the findings that touch behaviour, in the grill's format (CR-250),
   and sends the rest to the spec-writer. The critic never sends anything to the spec-writer
   itself.
3. **Passes** (spec-critic-Q3): one pass per specification. It runs again only if the user's new
   answers change behaviour. It does not loop until no finding is left.
4. **What the user sees** (spec-critic-Q4): the questions, plus one summary line, e.g. "10
   findings, 6 fixed without you, 4 questions". Not the full report.
5. **Saying whether it runs** (spec-critic-Q5): the one who grills says it in the restatement, one
   line just before "grilled enough?", e.g. "critic: yes, it touches the Drivers' contract" or
   "critic: no, two lines of docs". The user can then ask for it or cancel it.
6. **Who judges** (spec-critic-Q6): the one who grills, the Chief of Staff or a Griller, with the
   same criterion.
7. **This CR's own course** (spec-critic-Q7): triaged P1, specified, the critic runs on this
   specification, then the CR joins batch-17 after CR-250 (both touch the grill part of
   `chief-of-staff.md`). This is the Chief of Staff's to carry out; it changes no file of this CR.
8. **The icon** (answer 8, decided in lifecycle-line-Q6): 🧐, used by no other role, wherever a
   doc or diagram draws or names the critic.
9. **The model** (spec-critic-Q8): Opus 5.5 by default; Fable as an option the user can ask for.
10. **The cost** (spec-critic-Q9, confirmed by spec-critic-Q14): on the `grill and
    specifications with the user` line of `cost`, outside any batch's budget, as the
    spec-writer's, with the small change it needs in the CLI's `costs/` code. That change puts a
    second role name (`spec-critic`, beside `spec-writer`) in the CLI's cost code, against
    `AGENTS.md`'s "the CLI knows no role": this CR states it as a named exception (section 10).
11. **Asking for or cancelling the critic** (spec-critic-Q10): no new option at "grilled
    enough?"; CR-250's three options stay; the user says it in the tool's free answer or as a
    correction ("specify, no critic").
12. **No file for the findings** (spec-critic-Q11): the full list lives in the critic's reply
    only, shown to the user on request during the session; `02-answers.md` keeps the critic's yes
    or no. The critic writes no file and has no Write tool.
13. **Specifications the Chief of Staff writes itself** (spec-critic-Q12), a release CR's or a
    fix's: the critic runs on them too when judged impactful; the Chief of Staff applies the fixes
    itself.
14. **When the fixes without the user land** (spec-critic-Q13): before the user sees the critic's
    questions. One spec-writer run applies the findings that need no user first, so the summary
    line's "fixed" is true; a second run folds the user's answers.

Taken from the request and kept, not new decisions: the critic is fresh, with no grill context; it
reads only the request, `02-answers.md`, the specification and the repository, including the
other pending items that touch the same files; it looks for the three kinds of finding above; it
does not edit the specification.

## The new role: `spec-critic`

A new role of the plugin, beside the `spec-writer`: a subagent of the Chief of Staff or of a
Griller, outside any batch, with no worktree, no round and no slot. As `AGENTS.md` asks, its
contract is a card, its agent files are hand-written on both hosts with identical bodies, and the
CLI lists the roles from the agent files (`plugin_roles` in
`skills/chantier/scripts/cli/src/chantier/plugin_files.py`), so `$CHANTIER playbook` and
`chantier.yaml` take the new role's agent and model with no change there.

### 1. New card `skills/chantier/references/spec-critic.md`

Written in the cards' style (what the role judges, not a procedure), the sections:

- **Who you are.** The Spec critic: you check one CR's Change Specification before it is final.
  The one who grills (the Chief of Staff or a Griller) starts you in the background. You have no
  worktree, no round and no slot; you write no file, commit nothing, push nothing.
- **Input.** Your prompt names the CR's folder. Read, in it, `intake/` (the request as received),
  `02-answers.md` (the user's answers) and `03-change-spec.md`. You get no summary of the grill
  and no case for the specification: judge the spirit of the request from the user's own words.
  Then read the repository, read-only: the project's rules first (`$CHANTIER rules`; what touches
  the CR ranks above this card), the files the specification names and the cards, code, docs and
  tests around them, and the other items not yet merged (`1-inbox/`, `2-backlog/`, `3-ready/`,
  `4-batch/1-pending/`, `4-batch/2-actives/`) that touch the same files: their request, answers
  and specification, whichever exist (an inbox item often has no specification).
- **What you look for**, and only that:
  1. **A gap with the request's intent:** something the user asked for that the specification
     drops, narrows or bends; something it adds that nobody asked for; a decision of
     `02-answers.md` lost or changed.
  2. **An inconsistency with the rest of the software:** with a card, the CLI, the hooks, the
     docs, the tests or the scenario (an old rule the specification leaves standing against it
     included), or with another pending item on the same files (two items that would contradict
     each other, or edit the same lines in incompatible ways).
  3. **An unproved claim about the real world:** a statement about a host, a tool, a forge, a
     model or an outside service that the repository does not prove (the host references' marks:
     proved, documented, unproved) and that the specification treats as a fact.
- **What you do not do.** Edit the specification or any file; restyle its prose; propose an
  implementation detail the specification leaves to its Driver; re-ask a question
  `02-answers.md` already settled, unless you show that its answer rests on an unproved claim or
  on an inconsistency the user did not see; repeat or answer the specification's own open
  questions (they go to the user as they are; raise one only if it is itself wrong, e.g. it
  rests on an unproved claim).
- **Reply.** One list of findings, numbered, each with: its kind (intent, inconsistency or claim);
  where (the specification's section, and the file and line it conflicts with, when any); the
  evidence in one or two lines; and whether it touches behaviour (what the software does for the
  user or a role, its scope or its risk) or not. For a finding that touches behaviour, a draft
  question for the user with at most 4 options, the recommended one first (CR-250's shape), so the
  one who grills can ask it. For one that does not, the fix in one line. With nothing found, say
  "no finding". Nothing else: no summary of the specification, no praise. This reply is the only
  copy of the list (decision 12).

### 2. Agent files, both hosts, identical bodies

- `agents/spec-critic.md` (Claude Code) and `com.github.copilot/agents/chantier-spec-critic.agent.md`
  (Copilot), modelled on `agents/spec-writer.md` and
  `com.github.copilot/agents/chantier-spec-writer.agent.md`:
  - `name`: `spec-critic` / `chantier-spec-critic`.
  - `description`, the same on both: e.g. "Checks one chantier CR's Change Specification before it
    is final; read-only. Started by the Chief of Staff or a Griller. Prompt starts with:
    `chantier spec-critic for the Chief of Staff, in the project <root>.`"
  - The body: the same three paragraphs as the spec-writer's, with "Spec critic" and its first
    line; the refusal text "I run inside a chantier batch only. My prompt must start with
    `chantier spec-critic for the Chief of Staff, in the project <root>.`; a message to me gets
    this same answer: start a new agent with that line." and "Any later message gets the same
    answer."
  - The `# chantier-agent: <version>` line copied from the current agent files (not a new
    version: `scripts/version.py` globs the folders and the version test checks it).
  - Tools: read-only, so the role cannot edit the specification: Claude Code `Bash, PowerShell,
    Read, Grep, Glob` (no Write, no Edit); Copilot `["execute", "read", "search"]` (no `edit`).
    Not background-flagged in the frontmatter (only Drivers are; the parent starts it in the
    background, as the spec-writer).
  - Model (decision 9): the spec-writer's, Opus 5.5: `model: claude-opus-5-5` on Claude Code;
    `model: [Claude Opus 5.5, claude-opus-5.5]` with `model-policy: required` on Copilot.
- `skills/chantier/scripts/cli/tests/test_plugin_files.py`: `CHIEF_ROLES` becomes
  `("spec-writer", "spec-critic")`; `CLAUDE_OPUS_ROLES` and `COPILOT_OPUS_ROLES` gain
  `"spec-critic"`. The existing tests then check the pair of files, the identical bodies, the
  first line, the model and the card's existence.

**Fable on request** (decision 9). When the user asks for Fable, for one run or for the project:
for one run, the one who grills starts the critic with Fable (`claude-fable-5-2`, already priced
by the CLI) through the host's model parameter; for the project, the role's model is set in
`chantier.yaml`, as for any role. A host that does not offer Fable (Copilot records none today):
say so to the user and run the default; no look-alike model (`AGENTS.md`, no fallback). The
critic's restatement line names Fable when it is asked for (e.g. "critic: yes, on Fable, …").

### 3. The first line, from `$CHANTIER playbook`

The Chief of Staff and a Griller copy the spec-writer's first line from `$CHANTIER playbook`
(`griller.md` line 18; `commands/rules.py` lines 71-75): a measured fix of batch-09
(`5-archives/261111-1247-171-batch-09-retro-fixes/03-change-spec.md`, lines 376-389). The critic's
first line comes from the same place, so both starters copy it the same way:

- `skills/chantier/scripts/cli/src/chantier/commands/rules.py`, `playbook` with no batch: prints
  `spec-critic prompt, first line: chantier spec-critic for the Chief of Staff, in the project
  <root>.` beside the spec-writer's line, which stays word for word. No second role name is
  written in `rules.py`: the line comes from the agent files (the description's "Prompt starts
  with:" of each agent whose first line is the Chief of Staff's subagent line with `<root>` only,
  `<root>` filled in), and the spec-writer's line is printed the same way; the Driver picks the
  code. The demo explorer's line, which names a batch, is not printed there (unchanged).
- `scenario/run_scenario.py` (the check at line ~2462): checks the critic's line too.
- `skills/chantier/references/concepts.md`, "Starting an agent": the first-lines table gains the
  row `| Spec critic | chantier spec-critic for the Chief of Staff, in the project <root>. |`; the
  row and the playbook say the same.

### 4. `skills/chantier/references/concepts.md`, the rest

- "Who reads what": the Chief of Staff's own subagents name the Spec critic beside the
  Spec-writer and the Demo explorer.
- "An agent that ends before its part is done": the list of agents names the spec critic; its
  restart is recorded on the line of `work/specifying`, as the spec-writer's.
- The paragraph on the Spec-writer gains a sentence: the Spec critic is a subagent of the Chief
  of Staff or of a Griller too, outside any batch; it reads [`spec-critic.md`](spec-critic.md),
  its brief gives the CR folder, it writes nothing and takes no slot and no budget of a batch.

### 5. `skills/chantier/references/routing.md`

The sentence "The Chief of Staff's subagents (the Demo explorer, the Spec-writer) answer the
Chief of Staff alone, in their reply" names the Spec critic too, and says a Griller's spec critic
answers that Griller.

### 6. `skills/chantier/references/chief-of-staff.md`

On CR-250's text of "Backlog and grill", and the old rules elsewhere in the card:

- **The "Say" table** (line 25, "to file, triage or refine an item"): "the `spec-writer` writes
  the specification" gains "and, on an impactful CR, the `spec-critic` checks it".
- **The roles list** (lines 100-102) gains `spec-critic`; "Your own subagents (the
  `spec-writer`, the `demo-explorer`)" (line 122) gains the `spec-critic`.
- **The restatement** ("Shared understanding"): the complete restatement ends with one line on
  the critic, just before the closing "grilled enough?" question: `critic: yes, <why>` or
  `critic: no, <why>`, in the user's language (e.g. "critique : oui, elle touche le contrat des
  Drivers"). The closing question keeps CR-250's three options (decision 11): the user asks for
  or cancels the critic in the tool's free answer or as a correction ("specify, no critic"); that
  word is an answer, recorded at once in `02-answers.md` like any correction. When the user says
  the CR is grilled enough, the critic's yes or no goes into `02-answers.md` with that answer
  (e.g. `Spec critic: yes, it touches the Drivers' contract.`), so a later session knows whether
  it is due.
- **Items grilled before this CR merges** have no `Spec critic:` line: whoever starts their
  spec-writer judges then, by the same criterion, says the critic line to the user in the same
  message as the start (the user may flip it), and records it in `02-answers.md`. A specification
  already final before the merge gets no critic unless the user asks.
- **The criterion** (one paragraph, the same for the Chief of Staff and a Griller): the critic
  runs on a CR whose specification, if wrong, would cost the user most: it changes what a role
  does or may do (a card's contract, the CLI's refusals, a host behaviour), what the user sees or
  decides, an irreversible or shared step (merge, release, push, a tracker post), or several
  areas at once. It does not run on a CR that changes wording, a doc or a test alone with no
  behaviour behind it. The subject and the priority decide nothing by themselves. You judge, and
  say why in the critic line. An automatable CR with no specification gets no critic.
- **The step** (a new short paragraph after the review of `03-change-spec.md`, in this order):
  1. The spec-writer ends; you review its specification against `02-answers.md` as today
     (nothing dropped, nothing invented).
  2. With the critic due, start one `spec-critic` in the background (you or the Griller who
     grills), its first line copied unchanged from `$CHANTIER playbook` (or the Spec critic's row
     of [concepts](concepts.md) "Starting an agent"), with the agent and model the playbook
     prints for it (Fable on the user's word, section 2); the prompt names the card and the CR
     folder and nothing of the grill. `work/specifying` stays the guard of the specification
     from the spec-writer's start until the specification is shown: each agent started on it
     (the critic, the spec-writer's next run) replaces its line with `<time> <agent id> <role>`;
     no other spec-writer or critic starts while it exists; remove it when the last of them ends.
     A refused first line or a host failure: restart once, as for a spec-writer.
  3. Sort its findings: each one that touches behaviour (scope, behaviour, risk: what the user
     would decide) becomes a question for the user; each other one (a record fix, a wrong name,
     a dropped decision, an old rule left standing, an inconsistency whose answer is already
     settled, an unproved claim to mark as unproved with its trial) is a fix. An unproved claim
     that a decision rests on is a question. Every finding takes one of the two ways.
  4. **The fixes first** (decision 14): with any fix, run the spec-writer once with them, before
     the user sees anything of the critic. It applies each, or says why one does not hold; then
     review again against `02-answers.md`. A fix it refuses for a reason you accept is dropped;
     one you do not accept becomes a question.
  5. **Then the user**, in the text before the question tool (CR-250): one summary line, in the
     user's language, counting what is true at that point, e.g. "critique : 10 points, 6 corrigés
     sans vous, 4 questions" (a dropped one is counted too, e.g. "1 écarté"); then the
     questions, in CR-250's format, numbered on in the item's series, together with the
     specification's own open questions. With no question: the summary line, then the
     specification, the fixes already applied. With no finding: "critique : aucun point", then
     the specification. The full list is shown on request, from the critic's reply, while the
     session lasts (decision 12).
  6. **The answers:** record them in `02-answers.md`, then a second spec-writer run folds them,
     as today; review again. Start the critic again only if those answers change behaviour (one
     more pass, the same steps; its summary line says so, e.g. "critique, 2e passage : …").
     Otherwise the specification is final once the user approves it, as today.
- **A release CR's or a fix's specification** (line 162, "stay yours", decision 13): the critic
  runs on it too when you judge it impactful, by the same criterion. With no grill, you judge
  once you have written it and say the critic line in the message that would show it (the user
  may flip it). You apply the fixes yourself (step 4 without the spec-writer), then the user
  sees the summary line and the questions as above.
- **Direct mode, while a batch runs** (line 410, "backlog work and the spec-writer stay open";
  line 851, the spec-writer bullet of "What you accept while you steer"): the critic stays open
  too, like the spec-writer, on a CR grilled before; its questions wait for the pause, like any
  grill question.
- **Cost** (decision 10): line 162 ("its cost is on the `grill and specifications with the user`
  line") names the critic with the spec-writer; lines 804-808 (the turns that leave the steering
  row): "or starts a spec-writer" becomes "or starts a spec-writer or a spec critic".

### 7. `skills/chantier/references/griller.md`

"What you do", the list of what the Griller takes from chief-of-staff's "Backlog and grill", names
the critic line in the restatement, the judgement by the same criterion, and the spec critic
(started as the spec-writer is, its first line copied unchanged from `$CHANTIER playbook` as line
18 says for the spec-writer, its fixes applied first and its questions asked by the Griller). One
mention, not a copy. "Telling the Chief of Staff": `[griller→chief-of-staff] <slug> specified`
is sent once the specification is final for this pass (after the critic, when it ran).

### 8. `skills/chantier/references/spec-writer.md`

- "Input": a run may carry, in its brief, fixes from the spec critic sent by the one who grills;
  apply each, or say in your reply why it does not hold. Never against `02-answers.md`.
- "End": the reply names the fixes applied and those not, with why, in a few lines.

### 9. Other cards with an old rule

- `skills/chantier/references/init.md` (line 45, direct mode: "filing, triage and the spec-writer
  stay open"): names the spec critic with the spec-writer.
- `skills/chantier/references/pr-template.md` (lines 32-34, the roles a PR's text never names as
  the one who did the work): adds Spec critic.
- `skills/chantier/references/hosts/claude-code.md`, Tools table: a row "Start the Spec critic
  (Chief of Staff, Griller)": `Agent`, `run_in_background: true`, `subagent_type:
  chantier:spec-critic`; the `model` parameter as for the Spec-writer, only when `$CHANTIER
  playbook` printed one or the user asked for Fable; no effort. Mark: unproved until a CR's
  specification is checked this way (the CR-250 trial did not use this agent), and Fable through
  the model parameter unproved too; trials: the first impactful CR specified after the merge;
  one critic run on Fable, its transcript showing the model. The "Models" row names the Spec
  critic with the Spec-writer (Opus 5.5). "Not guarded" (the write guard) names the Spec critic
  beside the Spec-writer.
- `skills/chantier/references/hosts/copilot.md`, Tools table: a row "Start the Spec critic (Chief
  of Staff, Griller)": `task`, `mode: background`, `agent_type: chantier-spec-critic`; no model,
  no effort; Fable not recorded on Copilot. The preamble's "no new Copilot finding" admits this
  row as a new line, unproved like the rest (CR-250 adds the same kind of exception for its
  question tool row: write one sentence that covers both).

### 10. The cost: a named exception to "the CLI knows no role"

The CLI already recognises the spec-writer by its agent type
(`costs/sessions.py` lines 75-76, `costs/transcripts.py` line 124) and puts its calls on the grill
line outside a batch's budget. The critic joins it (decision 10), with no new command:

- `AGENTS.md`, the line "The CLI knows no role": names the exception, in one clause: the cost code
  knows the two specification agents by their agent type (`spec-writer`, `spec-critic`), to put
  them on the grill line. Without it the rule would read as broken twice, by the existing match
  and by this one.
- `skills/chantier/scripts/cli/src/chantier/costs/sessions.py`: `is_spec_writer` (and
  `without_spec_writers`, its docstring) match an agent type ending in `spec-writer` or
  `spec-critic`; renamed to say both (e.g. `is_specification_agent`), callers updated.
- `skills/chantier/scripts/cli/src/chantier/costs/transcripts.py`, `_grill_use`: a tool use whose
  `subagent_type` ends in `spec-critic` is grill work, as one ending in `spec-writer`.
- `skills/chantier/scripts/cli/src/chantier/commands/cost/sessions.py`, the grill line's count
  `(<n> calls, <k> spec-writers)`: counts both kinds, e.g. `<k> spec-writers, <c> spec critics`;
  the Driver keeps the line's other words.
- `skills/chantier/references/status-layout.md` (the second table's grill line: "or starts a
  spec-writer", "the spec-writers' own calls") and `docs/costs.md` (line 16) say "a spec-writer
  or a spec critic".
- Tests: `skills/chantier/scripts/cli/tests/test_costs.py` gains the critic's case beside the
  spec-writer's (line ~178); the scenario's cost steps (`scenario/run_scenario.py`, lines ~1329,
  ~1508, ~1579-1590) gain a critic transcript and check it lands on the grill line, outside the
  batch's spend, and that the line's count names it.

### 11. Docs and diagrams that draw the specification step

The user (`intake/request.md`): "Il faudra mettre à jour la doc et les svg avec ce spec critic."
Each SVG kept in line with its `-texts.md` and its `<desc>` (line 3); the critic's icon is 🧐
(decision 8), the same in every diagram and legend.

- `docs/cr-lifecycle.svg` and `docs/cr-lifecycle-texts.md`: in the spec loop, between "✍️
  spec-writer writes" and "👤 you review", the critic ("🧐 spec critic checks the spec ·
  impactful CRs · 🤵 or 🔥 starts it"), its fixes back to the spec-writer before you see it and
  its questions to you; the legend names it; the long description (texts line 3, SVG `<desc>`)
  says the step.
- `docs/cr-lifecycle-simple.svg` and `docs/cr-lifecycle-simple-texts.md`: the 📐 Spec box says 🧐
  the critic checks the spec of an impactful CR before you approve it; the legend names it; the
  description likewise.
- `docs/how-chantier-works.svg`, `docs/how-chantier-works-simple-foreman.svg`,
  `docs/how-chantier-works-simple-direct.svg` and their `-texts.md`: the 🧐 Spec critic shown
  beside the Spec-writer, as the Chief of Staff's (or Griller's) agent ("checks an impactful CR's
  spec; never edits it"); the descriptions likewise.
- `docs/use-cases.md` ("Turn ideas into ready work", lines ~76-92): the restatement's critic line
  and the step (fixes applied first; the critic's questions come with the spec's own, with one
  summary line). "A Chief of Staff and Grillers in remote" (line ~104): the Griller's list names
  the critic.
- `docs/tutorial-claude-code.md` (lines ~102-105): one sentence on the critic of an impactful CR;
  line ~222 (the spec-writer's model) says the critic runs Opus 5.5 too, Fable on request.
- `docs/agents-and-models.md`: the Models table gains a row "Spec critic" (Opus 5.5, Fable on
  request); line 59 ("every role but the Spec-writer runs Sonnet 5.5") names the Spec critic
  too.
- `docs/use-cases-direct.md` (lines ~35-36): the spec critic stays open with the spec-writer
  while the batch runs; its questions wait for the pause.
- `README.md`: the "Say" table row "it is grilled enough" (line ~226) says the critic checks an
  impactful CR's specification after the spec-writer.
- `CONTRIBUTING.md`: "What is chantier?" step 2 (lines ~19-22) names the critic step; the tree
  (line ~131) lists `spec-critic` among the references.
- Not changed: `docs/cr-folder-lifecycle.svg` and its texts (the critic writes no file in the CR
  folder), `docs/release-notes/`, `evals/results/`, the archives.
- `2-backlog/P2/lifecycle-line-svg` (a one-line lifecycle diagram, specified) comes after this CR
  and draws its spec critic step with this CR's name and 🧐; it is not specified or changed here.

### Not changed

- The CLI's other commands, the status views (`spec_state` already reads `work/specifying`), the
  board.
- `hooks/` and `types/`: no prompt of the critic holds a `writes:` line; nothing the pane draws
  changes.
- `driver.md`, `foreman.md`, `worker.md`: no batch role starts or reads the critic.

## The inbox item `retro-critic`: same principle, noted differences

`1-inbox/retro-critic` (answers 1 to 3) applies the same principle to retros; this CR decides
nothing for it. The two agree on: a separate subagent, not the author; given the material and its
evidence, not the author's case; it never rewrites the author's text. The differences, as they
stand in each item's own record:

- **When:** the retro critic always (its request: "toujours une critique"); the spec critic on
  impactful CRs only (spec-critic-Q1).
- **What it does with a point:** the retro critic keeps, merges or drops the author's points; the
  spec critic adds findings, sorted into fixes and questions.
- **What remains of the rest:** a retro point dropped once leaves no trace (retro-critic answer
  1); the spec critic's full list stays in its reply, shown on request during the session
  (decision 12).
- **Its cost:** the retro critic counts in the batch's cost (retro-critic answer 2); the spec
  critic is on the grill line (decision 10).
- **Its model:** the retro request asks "opus ou fable (en fonction du coding agent)"; the spec
  critic runs Opus 5.5, Fable on request (decision 9).

Each is its own role and card (`AGENTS.md`: one agent file per role and host). This CR builds
nothing of the retro critic.

## Order and other pending items on the same files

- **CR-250 grill-question-format** (pending): this CR's text sits inside CR-250's rewritten "Backlog
  and grill" (the restatement, the closing question, the text before the tool, the references,
  the record) and uses its format. It is implemented after CR-250 is merged (spec-critic-Q7
  places it after CR-250 in batch-17); the Chief of Staff records the wait. Both add a sentence
  to `copilot.md`'s preamble: one sentence covers both.
- **CR-223 cr-summaries** (active): edits `spec-writer.md` "Output", the commands block of
  "Backlog and grill" and `griller.md` "What you do". Different lines in the same sections: a
  rebase, no conflict of intent. The critic writes nothing, so it needs no `summary` command.
- **CR-248 ready-wording** (pending): changes the "ready" words in `cr-lifecycle.svg`,
  `cr-lifecycle-simple.svg`, `how-chantier-works.svg` and their texts. Other elements of the same
  files: no conflict of intent.
- `2-backlog/P2/lifecycle-line-svg`: after this CR, see section 11.
- `2-backlog/P3/spec-external-fact-source` (a spec that needs an external fact names its source)
  is the spec-writer's side of the critic's third kind; not done here.

## Out of scope

- The retro critic (`1-inbox/retro-critic`) and the one-line lifecycle diagram
  (`2-backlog/P2/lifecycle-line-svg`).
- A critic on every specification, or a loop until no finding (spec-critic-Q1, Q3).
- Showing the user the critic's full report unasked, or keeping it in a file (spec-critic-Q4,
  Q11).
- A new option at "grilled enough?" (spec-critic-Q10).
- A CLI command, a check or a hook that decides or enforces when the critic runs.

## Evidence

- `just check` passes (Linux, macOS, Windows), per `AGENTS.md`; it runs `test_plugin_files.py`,
  which checks the two `spec-critic` agent files (one per host, identical bodies, the first line
  in the description and the refusal, Opus 5.5) and the card's existence, and `test_costs.py`
  with the critic's case.
- `just scenario` passes before the PR (a change to the cards and the CLI): the playbook prints
  both first lines, the spec-writer's unchanged; a spec critic's transcript lands on the grill
  line, outside the batch's spend, and the line's count names it.
- No `just mod`: nothing in `hooks/` or `types/`.
- Review checklist for the PR: decisions 1 to 6 and 9 to 14 are in `chief-of-staff.md`, with
  `griller.md` pointing to it; `AGENTS.md` names the cost exception and `rules.py` holds no new
  role name; the card says what the critic reads, looks for, never does, and replies; the agent
  files hold no Write or Edit tool; the restatement line, the summary line and the order (fixes,
  then questions, then the answers' run) follow CR-250's format with no contradiction; the old
  rules listed (chief-of-staff.md lines 25, 162, 410, 804-808, 851; init.md 45; pr-template.md
  32-34) are updated; every diagram listed shows the step with 🧐 and agrees with its
  `-texts.md` and `<desc>`; `cr-folder-lifecycle` is unchanged.
- The real trials, after the merge: the first impactful CR grilled with the critic (the
  restatement line, one critic run, the fixes applied before the summary line, the questions as
  specified, the transcript showing `chantier:spec-critic` on Opus 5.5); one run on Fable;
  recorded in `hosts/claude-code.md`'s row.

## Open questions for the user

None.
