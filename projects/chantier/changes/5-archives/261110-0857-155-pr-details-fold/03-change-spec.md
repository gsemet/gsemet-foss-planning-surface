# Change Specification: pr-details-fold

## Goal

A reviewer reads chantier's default PR description in 30 seconds. Following Simon Willison's
pattern ("hiding the bulk of my AI-generated GitHub PR descriptions behind a collapsed
`<details><summary>` tag"), the default template keeps visible only what a reviewer needs to
judge the PR: why, what it delivers with the choices that matter, how risky it is, and what the
agents decided alone. The bulk folds into one collapsed "Details" block. A new folded section,
Human decisions, shows what the user decided during the grill, beside the Autonomous decisions
the agents took: the user always missed it in a PR.

Only chantier's default template changes. A project's own PR template, or a PR rule its
instructions give, still ranks above it, unchanged (`pr-template.md`, "Scope and precedence").

## The new layout

Visible, in this order:

1. `## Summary`: the why, in two or three sentences.
2. `## Deliverables`: the main visual, and the impactful choices made (see "Deliverables"). For a
   visible change, the before/after screenshots are its main visual, side by side.
3. `## Blast radius`: the grade and its one or two lines.
4. `## Autonomous decisions`: kept visible, right after Blast radius, so the user reviews each one.

Then one fold, holding in this order:

5. `## Changes`
6. `## Human decisions` (new; present only when the CR's `02-answers.md` records at least one
   decision that shapes the change, else omitted, see below)
7. `## Impacts`, without the before/after screenshots, which are in Deliverables
8. `## Test plan`
9. `## Internal references`, still last

The fold's exact form, a blank line after `</summary>` and before `</details>` (without it,
GitHub and GitLab do not render the Markdown, headings and Mermaid inside):

```markdown
<details>
<summary>Details</summary>

## Changes

...

## Internal references

...

</details>
```

Nothing follows `</details>`. Both GitHub and GitLab render `<details><summary>`.

## What changes, by file

### 1. `skills/chantier/references/pr-template.md` (the card)

**"The rules" section:**

- The rule "Every section is kept and filled; "None" rather than a deleted section." gains one
  exception: Human decisions is omitted, never written "None", when the CR has no decision to
  show: it had no grill (for instance a quick fix, or a fix CR, whose specification is a
  `fix-<n>.md` and which has no `02-answers.md`), or it was grilled but its answers hold no
  decision that shapes the change.
- A new rule states the layout: Summary, Deliverables, Blast radius and Autonomous decisions
  visible, in that order; the rest in one `<details><summary>Details</summary>` block, in the
  order of "The new layout" above, with the blank line after `</summary>` and before
  `</details>`; the before/after screenshots of a visible change in Deliverables, outside the
  fold.
- Deliverables (existing rule, extended): besides the visuals, it shows the impactful choices
  made, by kind of change:
  - UI: the important aesthetic and behaviour choices;
  - architecture: the architecture choices;
  - rework or refactoring: the targets set, for instance scores to reach.

  They come with the visuals already asked for (diagram, before/after, code sketch). The bullet
  on before/after screenshots no longer says "they go in Impacts": for a visible change they are
  Deliverables' main visual, side by side, attached as [driver](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/driver.md) says (the forge's own
  CLI).
- Impacts (existing rule, changed): what users and developers will notice, inside the fold; the
  Verifier's before/after screenshots are no longer placed there but in Deliverables, and Impacts
  says in one line what they show. A file the forge's CLI cannot upload is still named under
  Internal references. With nothing visible: one line, e.g. "No visual change".
- Human decisions (new rule): the impactful decisions the user took during the grill, extracted
  from the CR's `02-answers.md` (in the CR's folder, the parent of the work folder): only the
  decisions that shape the change, not every answer; one bullet each. Same rule as the rest of
  the body: no internal reference (no CR, batch, round, agent role, `.agents/changes/` path),
  written for a reader outside the team. Omitted when there is no such decision (no grill, or a
  grill with none).
- Autonomous decisions: the rule is unchanged; only its place moves (visible, after Blast radius).
- The rule on internal references keeps "Internal references" as the last section; it is now the
  last section inside the fold.

**"The template" section:** the block to copy into `pr-body.md` follows the new layout:

- The opening comment says: fill every section and write "None" rather than delete one, except
  Human decisions, omitted when the CR has no decision from the grill to show; keep the fold as
  written.
- Summary, Deliverables, Blast radius (with its grade list and `Grade:` line), Autonomous
  decisions, in that order, visible.
- The Deliverables comment adds the impactful choices by kind of change (UI: aesthetics and
  behaviour; architecture: the architecture choices; rework or refactoring: the targets set) and,
  for a visible change, the before/after screenshots side by side as the main visual.
- Then `<details>`, `<summary>Details</summary>`, a blank line, and Changes, Human decisions,
  Impacts, Test plan, Internal references, each with its comment; then a blank line and
  `</details>`.
- The Human decisions comment: "The decisions the user took during the grill that shape the
  change, from the CR's 02-answers.md, one bullet each, no internal reference. Delete this section
  when there is none (no grill, or no decision that shapes the change); never write "None"."
- The Impacts comment: what users and developers will notice; the before/after screenshots are
  in Deliverables, say here in one line what they show; with nothing visible one line, e.g. "No
  visual change".
- The Test plan checklist and the Internal references comment are unchanged, except the Test
  plan's Evidence item, which points to the before/after in Deliverables instead of Impacts.

The paragraph after the block (the studio's requirements item left out) is unchanged.

**"The audit" section:** the Inspector still checks every section in order, and also the fold
and Human decisions. The list becomes, one line each so a defect names its section:

1. Every section of the template present, in the new order, each filled or "None", except Human
   decisions, present when the CR's `02-answers.md` records a decision that shapes the change and
   absent otherwise; Internal references last.
2. The fold in place: one `<details><summary>Details</summary>` block, after Autonomous
   decisions, holding Changes, Human decisions (when present), Impacts, Test plan and Internal
   references, with a blank line after `</summary>` and before `</details>`, nothing after it;
   Summary, Deliverables, Blast radius and Autonomous decisions outside it; the before/after
   screenshots of a visible change in Deliverables.
3. No internal reference, the CR's name included, in the title or outside Internal references
   (Human decisions included).
4. Deliverables has at least one visual, unless the change is a one-line fix; the names in it
   exist in the diff or the code; it shows the impactful choices the change made.
5. Changes and Impacts match the diff and the specification (unchanged).
6. Blast radius has one grade and its explanation (unchanged).
7. Autonomous decisions lists the decisions the round's notes record as taken without the user,
   or says "None" (unchanged).
8. Human decisions matches the CR's `02-answers.md`: each decision that shapes the change is
   there, nothing dropped, nothing invented; absent only when there is no such decision.

The sentence "With a project template, the audit is: that template's sections, filled as it
asks, and the project's PR rules." is unchanged.

"Scope and precedence" and "A customised version" are unchanged.

### 2. `skills/chantier/references/worker.md`, section "Inspector"

The paragraph "On a CR's round, read `<work folder>/pr-body.md` with the diff and audit it…"
adds that the Inspector also reads the CR's `02-answers.md` (in the CR's folder, the parent of
the work folder) for the Human decisions audit item, when there is one. Nothing else in the card
changes.

### 3. `skills/chantier/references/driver.md`, the evidence bullet

The bullet "The evidence: once the Verifier has left it, you put it in the PR's description, in
its Impacts section, before and after side by side…" says "in its Deliverables section" instead
of "in its Impacts section". The rest of the bullet (the forge's own CLI, `gh pr edit --attach`,
a file the CLI cannot upload named under Internal references) is unchanged. Nothing else in the
card changes: it already sends the Driver to `pr-template.md`, whose rules now name
`02-answers.md`.

### 4. `docs/use-cases.md`, section "Your pull requests' description"

The paragraph lists the new layout: Summary, Deliverables (small visuals, the before/after of a
visible change, and the impactful choices), Blast radius and Autonomous decisions visible;
Changes, Human decisions (what you decided during the grill), Impacts, Test plan and Internal
references folded in one collapsed "Details" block. The rest of the paragraph (English, no CR,
batch, round or agent; the CR's name in Internal references only; the Inspector checks it; the
project's own template ranks above) is unchanged.

### 5. `scenario/run_scenario.py`, constant `BODY`

The scripted Driver's stand-in body follows the new layout so the scenario shows the shipped
form: Summary, Deliverables, Blast radius, Autonomous decisions, then the
`<details>`/`<summary>Details</summary>` fold with Changes, Impacts, Test plan, Internal
references (`{cr}`), with the blank lines as above. The scripted CRs have no grill, so Human
decisions is omitted. Nothing in the scenario reads the body's structure; no other scenario
change.

### Files that need no change

- `README.md` (lines 72-75 name the template file and its precedence, not its sections),
  `CONTRIBUTING.md`, `skills/chantier/SKILL.md`, `concepts.md` (its "Internal references
  section" wording still holds), `release-template.md`, `chief-of-staff.md`.
- `agents/` and `com.github.copilot/agents/`: no role contract changes there.
- The CLI (`skills/chantier/scripts/cli/`): it knows no template; no change, no new test.
- `tests/test_structure.py`: no new test (the template is prose, the structure tests stay few).

## Decisions carried from the grill

- Visible: Summary, Deliverables, Blast radius, Autonomous decisions, in that order (answers 1).
- Folded in one `<details><summary>Details</summary>`: Changes, Human decisions, Impacts, Test
  plan, Internal references, in that order; before/after screenshots of a visible change stay
  outside the fold (answers 1).
- The Inspector keeps checking every section in order, and also the fold (answers 1).
- New folded section Human decisions: the grill's impactful decisions from `02-answers.md`, only
  those that shape the change, no internal reference (answers 2).
- Deliverables shows the impactful choices by kind: UI aesthetics and behaviour, architecture
  choices, rework targets, with the visuals already asked for (answers 3).
- A project's own PR template still ranks above; only chantier's default changes (answers 5).
- A CR with no grill omits Human decisions; it never writes "None" (answers 5, which replaces the
  assumption of answers 4).
- The Inspector checks that Human decisions matches `02-answers.md`: nothing dropped, nothing
  invented (answers 5).
- The before/after screenshots of a visible change go in Deliverables, as its main visual
  (answers 6).
- A grilled CR whose answers hold no decision that shapes the change leaves Human decisions out,
  as a CR with no grill does (answers 6).

## Out of scope

- A project's own PR template or PR rules, and the "A customised version" flow.
- The release PR's form and `release-template.md` (the release notes already fold their own
  parts).
- The stack driver (it opens no PR).
- The CLI, the agent files, the batch brief's "Autonomous decisions" line in `commands.py`.
- Any change to what Autonomous decisions, Changes, Blast radius or Test plan hold.
- Rewriting the descriptions of PRs already open.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes: the change touches cards (`pr-template.md`, `worker.md`, `driver.md`)
  and the scenario, so AGENTS.md requires it before the PR.
- A rendered proof, kept under the CR's `evidence/`: the new template filled with sample text,
  rendered by the forge (for instance the CR's own PR description, which follows the new
  template), shown before (all sections open) and after (four sections visible, "Details"
  collapsed, and expanded with its headings and a Mermaid block rendering inside). The CR's own
  PR is the natural sample: it had a grill, so it carries Human decisions.
- A read of the diff shows: the template block, the rules and the audit list agree on the order;
  the audit holds the fold item and the Human decisions item; the before/after screenshots are
  placed in Deliverables in `pr-template.md` and `driver.md`, and nowhere still in Impacts;
  `worker.md`'s Inspector paragraph names `02-answers.md`; `docs/use-cases.md` lists the new
  layout; `BODY` in `scenario/run_scenario.py` follows it without Human decisions.
