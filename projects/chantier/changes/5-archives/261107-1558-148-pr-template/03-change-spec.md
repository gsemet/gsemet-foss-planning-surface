# Change Specification: a default PR description template, shipped in the skill

## Goal

A CR's pull request (or GitLab merge request) gets a full description that a reader outside the
team can follow and that a reviewer can audit quickly, section by section, instead of the two or
three sentences Drivers write today (PRs #80 and #81 of batch-08). chantier ships one default
template for it, taken over from the markdown-okf-schema-studio template ("it was really good"),
as a reference of its skill. A CR Driver writes the description from it; the Inspector checks it.
A project's own template and rules rank above it. When a user wants a customised version in their
project, the Chief of Staff files it as a CR, and a Driver delivers the guideline and the template
by PR.

## Decisions carried over (from `02-answers.md`)

1. The template takes over the markdown-okf-schema-studio template and its rules, easy to audit.
2. chantier adds no template to its own `.github/`: the template ships in the skill, as a
   reference.
3. It lives in a new reference, `skills/chantier/references/pr-template.md`, which `driver.md` and
   the Inspector's card (`worker.md`) name.
4. Sections, in this order: Summary, Deliverables, Changes, Impacts, Blast radius (graded 1 to 3),
   Test plan, Autonomous decisions; every one filled, "None" rather than deleted. Written for an
   external reader; an optional "Internal references" section comes last.
5. Only the CRs' PRs follow it, on GitHub and on GitLab alike. The stack driver's and the release
   driver's PRs keep their current form.
6. The project's own template (GitHub or GitLab) and rules rank above it.
7. The CR Driver applies it. The Inspector alone checks it, reading `pr-body.md` with the diff. No
   CLI check.
8. Screenshots are attached by the method `driver.md` already describes for the Verifier's
   evidence (the forge's own CLI, `gh pr edit --attach` on GitHub).
9. On the user's request, a customised guideline and template are written in the user's project;
   the agent chooses where ("let the agent do it on its own").
10. batch-08's open PRs stay as they are: no rewrite of an open PR body.
11. The CR's name ("CR-142 grill-rules") goes only in the "Internal references" section of a CR's
    PR: not in the PR title, not in the body's text.
12. When the Inspector blocks only on `pr-body.md`, the Driver fixes the description and runs a new
    Inspector in the same round; no round is counted.
13. A customised template for a user's project is delivered as a CR: the Chief of Staff files it,
    a Driver delivers the guideline and the template by PR.

## What changes

### 1. New reference: `skills/chantier/references/pr-template.md`

Plain English, in the cards' style (short, exact, one meaning per word). It holds five parts.
Relative links in it must resolve (`test_skill_and_references_links_resolve` checks every
`](…)` in `references/*.md`, inside code blocks too): put no relative link in the template block.

**a. Scope and precedence** (a few lines):

- It is the description of a CR's PR, on GitHub and on GitLab (merge request), written by the CR
  Driver in `<work folder>/pr-body.md` and checked by the Inspector. A fix CR is a CR: its PR
  follows it too. A stack driver opens no PR; a release PR keeps its form.
- The project ranks above it: a template file the forge reads (GitHub: `pull_request_template.md`
  in the root, `docs/` or `.github/`, any case, or a template in `.github/PULL_REQUEST_TEMPLATE/`;
  GitLab: `.gitlab/merge_request_templates/`, `Default.md` when there are several and the rules
  name none), or a template or PR rule that the project's rules (`$CHANTIER rules`) give. Then
  the project's template is used as written, and this file only fills where the project is
  silent.

**b. The rules** (taken over from the studio's `pull-request.guidelines.md` and rule 10 of its
`ci.guidelines.md`, adapted to chantier's roles):

- Title and body in English, for a reader outside the team: reviewers, stakeholders, future
  maintainers. They do not know the backlog, and `.agents/changes/` is not in git.
- Explain the change from the reader's side: what was wrong or missing, what the PR changes, what
  they will notice. Name features by what they do, not by internal ids. Define a project term on
  first use.
- No internal reference in the title or the body text: no CR name, number or slug, no batch,
  round or order, no agent role (Driver, Coder, Inspector…), no path under `.agents/changes/`.
  The CR's name ("CR-142 grill-rules") and any other reference that helps maintainers go in the
  last section, "Internal references", and nowhere else.
- The title says what changes; where the project's rules give no style, a Conventional Commit
  subject (`feat: …`, `fix: …`).
- Every section is kept and filled; "None" rather than a deleted section.
- Deliverables, right after Summary: what the reader gets, shown with one or more small visuals,
  each next to the one or two sentences it supports; one kind, sometimes several, rarely all:
  - a Mermaid `flowchart` of the modules or layers that change, arrows for the calls or allowed
    imports (about 10 nodes at most);
  - a Mermaid `sequenceDiagram` of one real flow, before and after when the order is the fix;
  - a before/after tree or table (files moved or split, sizes, settings);
  - before/after screenshots for a visible change (they go in Impacts, see below);
  - a 5 to 15 line code sketch of the new interface, message or registration a contributor will
    reuse, with `...` for the rest.

  Only the calls, files, props and boundaries the reviewer needs, with real names checked against
  the diff. A one-line fix may write "None"; a structural change never does.
- Impacts: what users and developers will notice. The Verifier's before/after screenshots go
  there, side by side, attached as `driver.md` says (the forge's own CLI). A file the forge's CLI
  cannot upload is named under "Internal references" (its path is under `work/`), not in the
  text. With nothing visible: one line, e.g. "No visual change".
- Blast radius: one grade kept, explained in one or two lines (what could break, how to roll
  back).
- Autonomous decisions: each decision an agent took without the user (in the investigation, a
  round, a conflict resolution), one bullet each, with its reason; "None" when there is none.
- The body describes the PR as it is now, not its history: it is updated whenever the scope
  changes (a new round, a dropped item, a rebase that changes what the PR holds).

**c. The template**, in a fenced `markdown` block, to copy into `pr-body.md`:

```markdown
<!-- Title and body in English, for a reader outside the team: no internal ids (CR, batch,
round, agent roles, .agents/changes/ paths). Put such references, the CR's name first, in the
last section "Internal references". Fill every section; write "None" rather than delete one. -->

## Summary

<!-- Why: the user problem or limitation this solves, in two or three sentences. -->

## Deliverables

<!-- What the reader gets, with small visuals each next to the sentence it supports: a Mermaid
flowchart of the modules or calls that change (about 10 nodes), a sequence diagram of one real
flow (before and after when the order is the fix), a before/after tree or table, or a 5-15 line
code sketch of the new interface. Real names, checked against the diff. A one-line fix may write
"None"; a structural change never does. -->

## Changes

<!-- What: the key mechanisms and files, as a short list. Not a diff summary. -->

## Impacts

<!-- What users and developers will notice. For a visible change: before/after screenshots side
by side. Otherwise one line, e.g. "No visual change". -->

## Blast radius

<!-- Keep one grade and explain it in one or two lines: what could break, how to roll back. -->

- **1**: local and isolated; a plain `git revert` restores the previous behaviour.
- **2**: several features or shared code; revert is possible but needs checks or follow-ups.
- **3**: wide impact (data, formats, CI, release, public API); rollback is complex or partial.

Grade: <!-- 1 | 2 | 3 -->

## Test plan

- [ ] New or changed tests (they fail on the previous code) <!-- or "No behaviour change" -->
- [ ] Local gates: <!-- the commands run and their results -->
- [ ] Evidence: <!-- the before/after in Impacts, or why there is none -->
- [ ] Review
- [ ] CI green

## Autonomous decisions

<!-- Each decision taken without the user, one bullet with its reason; or "None". -->

## Internal references

<!-- Always last: the CR's name (number and slug, e.g. "CR-142 grill-rules"), work files,
anything only the maintainers need. -->
```

The studio's Test plan item on requirements (SwRS, `just requirements-update`) is specific to
that project and is left out; an Evidence item replaces it, as chantier's Verifier produces the
before/after.

**d. The audit** (what the Inspector checks, one line each, so a defect names its section):

1. Every section of the template present, in order, each filled or "None"; Internal references
   last.
2. No internal reference, the CR's name included, in the title or outside Internal references.
3. Deliverables has at least one visual, unless the change is a one-line fix; the names in it
   exist in the diff or the code.
4. Changes and Impacts match the diff and the specification (nothing claimed that the diff does
   not do, nothing the diff does left out).
5. Blast radius has one grade and its explanation.
6. Autonomous decisions lists the decisions the round's notes record as taken without the user,
   or says "None".

With a project template, the audit is: that template's sections, filled as it asks, and the
project's PR rules.

**e. A customised version** (a short paragraph): when the user asks for their own version, the
Chief of Staff files it as a CR (`$CHANTIER file`), grilled and specified like any CR; a CR
Driver delivers it by PR. The CR writes a guideline (the rules) and a template in the user's
project, starting from this file and the user's wishes, at the place the agent judges right unless
the user's answers name one (for instance the forge's template file, and a guideline next to the
project's other rules), and links the guideline from the project's instruction file so
`$CHANTIER rules` lists it: what `rules` does not reach, a Driver does not read. Once merged, the
project's version ranks above this file.

### 2. `skills/chantier/references/driver.md`

- "Your means", the PR bullet (lines 34-42 today, "the title and body follow the project's rules
  and template"): replace that clause with: a CR Driver writes the title and
  `<work folder>/pr-body.md` from the project's PR template and rules, else from
  [pr-template](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/pr-template.md), and keeps the body and the PR's description current with the
  scope (`gh pr edit --body-file`, `glab mr update --description`); `glab mr create --draft`
  takes the body with `--description`. The stack driver's and a Release driver's PRs keep their
  form, by the project's rules.
- "The evidence" bullet (lines 49-52): the before and after go in the description's Impacts
  section; a file the forge's CLI cannot upload stays in `work/` and the description names it in
  its Internal references section.
- "CR driver" section (lines 85-93): each round becomes a `coder`, then the Driver writes or
  updates `pr-body.md`, then the `inspector` on the round's diff and `pr-body.md`, then each
  review step. Add: a `FIX-REQUIRED` whose blocking items are all on `pr-body.md` (written
  `pr-body.md: …`) is not a new round: the Driver fixes `pr-body.md` itself and starts a new
  `inspector` in the same round, with no `$CHANTIER round` and no `coder`. A blocking item on the
  code, alone or with body items, is the next round, as today. After the Verifier, the evidence
  goes in Impacts and the Test plan boxes are updated (`gh pr edit --body-file` again).

### 3. `skills/chantier/references/worker.md`, section "Inspector"

Add: on a CR's round, read `<work folder>/pr-body.md` with the diff and audit it against the
project's PR template and rules, else against [pr-template](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/pr-template.md) (its audit list). A
missing `pr-body.md` or a failed audit item is `blocking`, written `pr-body.md: <section>: …`.
The extra review steps do not audit the body.

### 4. `skills/chantier/references/chief-of-staff.md`, section "The project"

Add two or three lines: on the user's request for their own PR template, file a CR for it
(`$CHANTIER file`, section "Backlog and grill"), grilled and specified like any other; a CR Driver
delivers the guideline and the template by PR, as [pr-template](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/pr-template.md) part "A
customised version" says. The Chief of Staff does not write them in the main checkout itself. And
`SKILL.md`, "Entry points" (the table at line 57): one row, "my own PR template" → `$CHANTIER
file` a CR for the guideline and the template, section "The project".

### 5. `skills/chantier/references/concepts.md`

The "A CR's name" bullet (lines 32-35) lists "PR titles and bodies where the project allows".
Replace that item: in a CR's PR, the CR's name goes only in the description's Internal references
section, never in the title or the body's text, unless the project's rules say otherwise.

### 6. Docs

- `README.md`, the tree (line ~280): add `pr-template` to the list of references (and the missing
  `spec-writer`, `init` while there).
- `CONTRIBUTING.md`, "How the project is built" (line ~11): name `pr-template.md`, the default PR
  description a CR Driver writes and the Inspector audits.

### 7. Scenario

`scenario/run_scenario.py`, constant `BODY` (line 43): the scripted Driver's body follows the
template: the eight section headings, in order, Summary holding `{title}.`, the middle ones
"None", Blast radius `Grade: 1`, Internal references holding the CR's name. The scripted PR title
(line 169) is the CR's title and stays so. No other scenario change: no model runs there, so
the Inspector's audit is not scripted.

### Unchanged

- The CLI (`skills/chantier/scripts/cli/`), including the `cards:` line of `_facts` in
  `commands.py` and the `round` command: the template is reached through the links in
  `driver.md` and `worker.md`, and a description-only fix simply calls no `round`.
- The agent files in `agents/` and `com.github.copilot/agents/`: a role's contract stays in its
  card.
- chantier's own `.github/`: no `PULL_REQUEST_TEMPLATE.md` is added.

## Out of scope

- Rewriting the bodies of open PRs (batch-08's included): they stay as they are.
- The stack driver's and the release driver's PRs, and the QA driver (no PR).
- A CLI check of the body, or a structure test of its sections.
- The studio's screenshot method (raw blobs pushed to a side `-assets` branch): chantier keeps the
  forge's own upload of `driver.md`.
- Choosing the place of a customised version in a user's project: the agent of that CR decides
  at the time.
- A Chief of Staff writing a customised template directly in a user's main checkout.

## Evidence

Run in the CR's worktree, at the pushed head:

1. `just check`: passes (the link test resolves the new `pr-template.md` links from `driver.md`,
   `worker.md`, `chief-of-staff.md`, `SKILL.md`, and has no dangling link inside
   `pr-template.md`).
2. `just scenario`: passes on both forges (`--forge github`, `--forge gitlab`), since cards and the
   scenario change.
3. `rg -n "pr-template" skills/chantier` shows the links in `driver.md`, `worker.md`,
   `chief-of-staff.md` and `SKILL.md`.
4. `rg -n "Summary|Deliverables|Changes|Impacts|Blast radius|Test plan|Autonomous decisions|Internal references" skills/chantier/references/pr-template.md`
   shows the eight headings of the template block in that order.
5. `rg -n "PR titles and bodies" skills/chantier/references/concepts.md` finds nothing; the "A
   CR's name" bullet names Internal references.
6. `rg -n "pr-body.md" skills/chantier/references/driver.md` shows the description-only fix in
   the same round, with no `round` and no `coder`.
7. `git diff --stat origin/main` lists no file under `skills/chantier/scripts/cli/`, `agents/`,
   `com.github.copilot/agents/` or `.github/`.
8. This CR's own PR is written from the new template (sections filled, its CR name only in
   Internal references, not in the title): the first application, visible to the reviewer.
