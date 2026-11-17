# Change Specification: a Driver's opening reads cost a third less

No issue.

## Goal

A Driver spends a large part of its context on its opening reads (the cards, the project's rules,
the specification) before it starts its first worker. The request measured about 58k tokens on
batch-16, out of a threshold of 130,000 since CR-236. The goal is to cut that opening cost by
about a third. The Driver reads whole only what it judges it needs, reads the rest by section when
a step needs it, and leaves to its workers what they read themselves. The cost is measured before
and after, on batch-18's transcripts.

Decision (`02-answers.md`, 2026-11-14, DR-Q1, answer A): the target is about a third less than
the ~58k tokens of opening reads. It is measured before and after on batch-18's transcripts. The
Driver reads whole only what it judges, and leaves the rest to its workers.

## The measure today (done while writing this specification)

These figures are context for the Driver and the Verifier. They are not the before measure,
which comes from batch-18 (see "Evidence").

Source: the batch-16 and batch-17 steering session,
`C:/Users/gaeta/.claude/projects/C--Users-gaeta-Projets-chantier/bd1945f6-9982-485f-b29f-477277e80753/subagents/`.
The method is the one "Method" below gives. It covers 39 first Drivers (`chantier:cr-driver`, the
first Driver of their CR; resumed Drivers excluded):

- Opening cost: mean 49.7k tokens, median 49.1k, min 28.4k, max 96.7k.
- Drivers that read `hosts/claude-code.md` at their opening: 54.6k to 75.3k. Most of those that
  did not: 28.4k to 50.1k. The host reference is the largest single item. Some Drivers already
  skip it.
- What a first Driver read, in order: `driver.md` (always, whole), the specification (whole),
  `concepts.md` (most, whole), `hosts/claude-code.md` (about a third, whole), `pr-template.md`
  (most, at the opening), and some `02-answers.md` or `worker.md`.
- The cards have grown since batch-16. In characters, at `ce00ec3`:
  - `driver.md` is 65,255: "Your means" 29,712, "CR driver" 9,860, "Stack driver" 16,336,
    "QA driver" 794, "Release driver" 6,935.
  - `concepts.md` is 43,459: "Words" 27,177, "Starting an agent" 7,497, "Escalation" 2,936,
    "Rules" 5,114.
  - `hosts/claude-code.md` is 61,432. Its "Configuration" part (allow rules, capabilities, auto
    mode) is about 22,400, and the Foreman's and Chief of Staff's sessions part ("Classes of
    session" through "Allow rules to add") is about 18,000.
  - `pr-template.md` is 16,463.
- `$CHANTIER rules` in this project lists nine files: `AGENTS.md`, `CONTRIBUTING.md`,
  `README.md`, `docs/use-cases-direct.md`, `skills/chantier/references/chief-of-staff.md` (1,480
  lines), `scenario/README.md`, `evals/README.md`, `evals/SCORECARD.md` and
  `docs/release-process.md`. Most of them do not touch a Driver's work.

A CR Driver that reads the top of `driver.md`, "Your means" and "CR driver" skips about 24,000
characters of `driver.md`. Reading only the sections of the host reference and of `concepts.md`
that it uses skips about 70,000 more. Together that is about 23k to 25k tokens, more than the
third the target asks for.

## What changes

Only cards: `skills/chantier/references/driver.md`, `skills/chantier/references/concepts.md`,
`skills/chantier/references/hosts/claude-code.md` and `skills/chantier/references/hosts/copilot.md`
(the last one only if it names what a Driver reads; today it does not, so most likely no change).
No CLI, no hook, no type, no agent file (`agents/`, `com.github.copilot/agents/`), no scenario step.

### 1. `driver.md`: an "Opening reads" paragraph, at the top (lines 1-11)

The top paragraph says today: "Read your host's reference with this card ... the project's rules
(`$CHANTIER rules`, read first)". It becomes a short paragraph, or a bullet list right under it,
titled or led by "Opening reads". It says what a Driver reads whole, what it reads by section and
when, and what it leaves to its workers. The Driver judges. These are the card's defaults, not a
gate:

- **Whole, first:** the project's instruction file that `$CHANTIER rules` names first (the
  project's rules rank above every card). From the other files `rules` lists, only what touches a
  Driver's work: git, the branch, the gates, the PR, the forge, CI. Another role's card that the
  list names (here `chief-of-staff.md`) and the project's docs for users are not opening reads.
- **Whole:** this card's top, "Your means" and your own section ("CR driver", "Stack driver",
  "QA driver" or "Release driver"). Another Driver's section is not read.
- **Whole, or by part:** the specification. The Driver needs its goal, its scope and out of
  scope, its decisions and open points, and its evidence, to brief the workers, write
  `pr-body.md` and judge the Verifier's proof. The detail of "What changes" is the Coder's and the
  Inspector's to read. They read the specification themselves (their prompt names it). The Driver
  reads that detail when a brief or a judgment needs it.
- **By section, when the step comes:**
  - `concepts.md`: "Starting an agent" before the first worker's start, "Escalation" only when
    one of its triggers arises (the card already says so), a rule or a word of "Words" when a
    link of this card names it.
  - The host's reference: on Claude Code, "Tools" before the first start, "Auto mode" when the
    host refuses a command, "Compacting" for the context rule, and "The write guard" when a write
    is refused. Its "Configuration" part (beyond "Auto mode"), its sessions part ("Classes of
    session" through "Allow rules to add") and "Heartbeat" are the steering sessions' and are
    not read. On Copilot, the same rule.
  - `pr-template.md`: when the Driver writes `pr-body.md` (at the first push and the PR), not at
    the opening.
  - `worker.md`: only the section of the role whose reply the Driver checks, when that reply
    comes. "Your means" already gives each reply's format.
- **How to read a section:** Grep the heading in the file, then Read with offset and limit, up to
  the next heading of the same level. A section a link names is read in full: never a few lines
  of it.
- **A Driver started again** (a `resume:`, `rebase:`, `context:` or other `Note:`):
  `$CHANTIER handoff <cr>` and `log <cr>` first, then only what the note's step needs. Today this
  Driver often reads the cards whole again.
- A rule a Driver did not read still binds it. When a step is not in what it has read, it reads
  the section that covers it before it acts, never after.

Every heading this paragraph names must exist, with that exact text, in the file it names (the
Verifier checks this, see "Evidence"). Keep the text `` `context: <where it stopped `` in
`driver.md`, because the scenario's card check at `scenario/run_scenario.py:3672-3679` looks for
it.

The links to `concepts.md` elsewhere in `driver.md` stay as they are (lines 24, 91, 98, 163,
278, 409, 484, 507, 723). Each already names a section, a rule or a word. There is one exception:
line 197 links "[ready to merge](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md)" with no section. It gains the section that holds
the word ("Words", the entry that defines "ready to merge"), so that the Driver can read it by
section.

### 2. `concepts.md`, "Starting an agent": the prompt's read line (lines ~337-340)

Today the template's second and third lines say, for every role: "Read
<skill>/references/<driver|worker>.md, section "<Role>", and <skill>/references/concepts.md (a
Driver also <skill>/references/hosts/<host>.md, `claude-code` or `copilot`)".

The Foreman (and the Chief of Staff in direct mode) writes a Driver's prompt from this template.
Change it so that a Driver's prompt says: read `<skill>/references/driver.md`, its top, "Your
means" and section "<Role>", and from `concepts.md` and `hosts/<host>.md` the sections the
"Opening reads" of `driver.md` names, when the step comes. A worker's read line does not change
(out of scope). The template may show the two lines (a Driver's, a worker's) one under the other,
with the same placeholders.

### 3. `hosts/claude-code.md`, "Who reads it, when" (line ~132-133)

"The Foreman and the Drivers read this file with their card (their prompts already name it)"
becomes: the Foreman reads this file with its card; a Driver reads the sections its card's
"Opening reads" names ("Tools", "Auto mode", "Compacting", "The write guard"), when the step
comes. "Auto mode" still tells it what a refusal means and that it is reported, never worked
around.

### 4. Who writes the Driver's prompt

`foreman.md` (line ~113) and `chief-of-staff.md` (direct mode) point to "Starting an agent" for the
prompt and hold no read line of their own (checked: no `references/driver.md` read line in
either). They do not change. If the Driver finds a read line for a Driver there, it changes it to
match section 2.

## Out of scope

- The CLI (`skills/chantier/scripts/cli/`). `facts.py`'s `cards:` line ("driver.md, worker.md,
  concepts.md") names the folder and does not tell a Driver to read anything whole. A new CLI
  command to measure the opening reads is also out: the measure is a short script in the
  Verifier's notes folder (AGENTS.md: a new CLI tool only from measured token-costly behaviour,
  and this measure runs twice).
- Workers' opening reads (Coder, Inspector, Verifier...): their read line in "Starting an agent"
  does not change.
- The Foreman's and the Chief of Staff's opening reads.
- Splitting, shortening or rewriting the cards' text. This CR changes what a Driver reads, not
  what the cards say. A card that is cut in size belongs to another CR.
- What `$CHANTIER rules` lists (two levels of links). It is the project's rules and the CLI's
  behaviour, unchanged.
- Copilot's measure: Copilot gives no per-agent record (`context: not measured`). The rule
  applies there, but only Claude Code is measured.
- The 130,000 threshold (CR-236), unchanged.
- New scenario checks or eval scorecard rows.

## Evidence

### Method (the Verifier writes it as a script in `work/verifier/`, and it goes with the CR's archive as `evidence/opening-reads.py`)

- Source: the batch's steering session folder under
  `~/.claude/projects/<the project's folder name>/<session id>/subagents/`. It holds one
  `agent-<id>.jsonl` and one `agent-<id>.meta.json` per agent.
- A Driver is an agent whose `meta.json` has `agentType` `chantier:cr-driver`. Only the first
  Driver of each CR in the batch counts (its `description` names the CR and no restart: no
  `(resume`, `(rebase`, `(gate`, `(hand-back` or round in brackets). The others are reported
  apart, not in the mean.
- For each `assistant` entry whose `message.model` is not `<synthetic>`, keep the last `usage` per
  `message.id`. A call's prompt is `input_tokens` + `cache_creation.ephemeral_5m_input_tokens` +
  `cache_creation.ephemeral_1h_input_tokens` + `cache_read_input_tokens` (CR-236's method, the sum
  `costs.agent_context` makes).
- The opening cost of a Driver is the prompt of its first call that holds an `Agent` tool use or a
  `$CHANTIER round` command, minus the prompt of its first call.
- The report gives, for each Driver: the CR, the agent id, the start time, the opening cost, and
  the files it read whole or by part before that call (from its Read calls' `file_path`, `offset`
  and `limit`). It also gives the mean and median of each group.

### Before and after, on batch-18

- **Before:** the first Drivers of batch-18 started before this CR's merge. They read the main
  checkout's cards before the change (the plugin runs live from the main checkout). The Verifier
  measures those that have reached their first round by the time it runs. It writes the figures
  in `verify.md`, and the Driver copies them into the PR's Deliverables. When no batch-18 Driver
  has reached its first round yet, `verify.md` says so, and the before measure is taken with the
  after measure at the batch's close.
- **After:** the first Drivers of batch-18 started after this CR's merge and the main checkout's
  fast-forward. The Chief of Staff runs the same script at batch-18's close, before the retro. It
  writes both groups and the ratio in `5-archives/batches/batch-18.md` (the retro), with the
  before figure next to the request's ~58k.
- **The target holds** when the after group's mean is at most about two thirds of the before
  group's mean (default O1).
- **No loss:** the retro also says whether any after-Driver's note, hand-back or worker restart
  traces back to a rule it did not read (a refused command not reported as "Auto mode" says, a
  worker prompt missing a line of "Starting an agent", a `pr-body.md` out of the template). Each
  case is offered as an inbox item.

### At the PR

- `just check` passes (Linux, macOS and Windows in CI).
- `just scenario` passes at the PR's head, as `AGENTS.md` asks for a change to the cards. Its card
  check still finds `` `context: <where it stopped `` in `driver.md`.
- `git diff --stat <base>..HEAD` lists only the cards of "What changes" (and the CR's archive when
  the project asks for it).
- The Verifier quotes, with `git grep -n` at the pushed head:
  - the "Opening reads" paragraph in `driver.md`;
  - the Driver's read line in `concepts.md`, "Starting an agent";
  - the changed line of `hosts/claude-code.md`, "Who reads it, when".
  For each heading the paragraph names, it shows that the heading exists in its file (`git grep
  -n "^## Tools$" -- skills/chantier/references/hosts/claude-code.md`, and the same for each).
- Known gaps: the after measure and the "no loss" check come only at batch-18's close, after the
  merge. The PR's Known gaps names them, so the ready line quotes them.

## Batch-18

To have an after group, this CR merges early in batch-18. The Chief of Staff puts it in the
batch's first wave, and enough CRs remain to start their first Driver after its merge. No
`depends.json`: the other CRs do not need this one, they only measure it.

The CR edits `driver.md`'s top and `concepts.md`'s "Starting an agent". Another CR of batch-18
that edits the same files is a shared file, not a need: the second to land rebases.

## Open questions for the user

- **O1. The target's reference.** The request's ~58k was measured on batch-16, on Drivers that
  read the host reference. Batch-16 and batch-17's first Drivers averaged 49.7k by this method,
  and the cards have grown since. Default: the target is relative to batch-18's own before group
  (the after mean at most about two thirds of it). The ~58k is reported next to it, but it is not
  the bar. The other reading is an absolute bar of about 39k tokens. Which one counts?
- **O2. Too few Drivers after the merge.** If this CR merges late, batch-18 may have few first
  Drivers left to start after it. Default: at least five first Drivers in the after group.
  Otherwise the after measure moves to batch-19, and the retro says so. Is five enough, and is
  moving to batch-19 acceptable?
- **O3. The risk of a rule not read.** A Driver that reads by section may miss a rule that binds
  it (in the project's rules or a card). The card says that a rule not read still binds, and that
  a step not covered by what was read is read before it acts. The retro checks this with "No
  loss". Default: accept that risk for the saving. The alternative is to keep the project's rules
  (every file `rules` lists) as whole opening reads, which keeps part of today's cost in a project
  such as this one.
