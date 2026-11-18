# Change Specification: tracker-grill-summary

Post the grill summary, plan and demo on the source ticket.

No `issue:` line: this item comes from the user's own request (verbal), not from a tracker issue.

## Goal, in the user's terms

When a change comes from a ticket opened by someone else, its reporter learns what was accepted
before any code: a short comment, a plan and, when it makes sense, a demo page, posted on the
ticket only after the user's explicit yes for that ticket; a one-line link when the PR opens; the
PR naming the ticket.

## State at main (2026-11-18, `3a9afc2c`): already delivered

CR-220 `ticket-summary-on-source` (merged 2026-11-13, commit `73f78e92`; archive
`5-archives/261113-1646-220-ticket-summary-on-source`) shipped this intent: its request is this
`01-intent.md`'s text, word for word, plus the user's answers of 2026-11-13. Row by row:

| Intent | Where main holds it |
| --- | --- |
| Intake: record the source ticket | `concepts.md`, "Tracker issue" (`issue: <link>` under the title of `01-intent.md` and `03-change-spec.md`); `griller.md`, "What you do" |
| Grill end: draft, show, ask, publish, record | `chief-of-staff.md`, "Ticket summary", steps 1 to 9 |
| Comment, plan, demo; their content and shape | step 4 (`work/issue-comment.md`, `work/issue-plan.md`, `work/issue-demo.html`); `ticket-summary-example.md` |
| Artifacts, else attachments, else collapsed section | step 7, per tracker (GitHub `gh issue artifact` / `gh issue comment --body-file`, GitLab `glab issue note`, Jira and others by the capability found) |
| Always on human approval; nothing from a subagent or Foreman | steps 6 and 7; `concepts.md`, "Tracker issue" ("Only the Chief of Staff posts"); `griller.md`, "Never" |
| Language of the ticket | step 4, "Language" |
| Check before publishing | step 5 |
| Verify after publishing | step 8 |
| Record URL, artifacts, date | step 9 |
| No ticket, or no write access: skip in one line | step 2 and the block's opening lines |
| PR open: follow-up comment | "PR follow-up", after step 9 |
| Two-way link in the PR | `pr-template.md`, `## Issues References` (default `Closes #<n>` / `Closes <KEY>-<n>`, project rules first) |
| Land: closing comment | `chief-of-staff.md`, "Released in" |
| Lifecycle describes the sub-step | `docs/cr-lifecycle-texts.md` and `docs/cr-lifecycle.svg` ("🎫 ticket summary"), `docs/use-cases.md` |
| Trackers: GitHub, GitLab, Jira | all three, by the user's answer of 2026-11-13 (wider than the intent's "start with GitHub") |
| Reference example of issue #336 | `ticket-summary-example.md`, modelled on it (its text is in another project and was not given) |

### How the user's yes is asked (outward action), as main has it

Posting on a forge is an outward action; main keeps the user's yes before each post:

- **Ticket summary**, step 6: in one message the Chief of Staff shows the comment and the plan as
  text, the demo as a file (absolute path, or the host's means to send a file), the route and the
  tool each part will take, the ticket's link and the title read from the tracker, and each project
  rule followed, quoted. It asks for a yes **for that ticket**; the user may edit any part, drop
  the demo or the plan, or decline. The answer goes at once into the CR's `02-answers.md`, with
  the date and the user's words. No yes, nothing posted; a "no" ends the step for that CR.
- **PR follow-up**: proposed once, the first time the Chief of Staff sees the PR link; its own yes
  for that ticket, recorded the same way.
- **Released in**: the list of issues the release ships is shown; one yes covers that list;
  "auto" never covers it.
- Only the Chief of Staff posts; a Griller drafts but never posts; a refused or failed post is
  told with its exact text and not retried another way.

## What changes

Nothing, unless the user answers the open question below with (b) or (c). This specification
names no file to edit by default.

## The one item not delivered

The intent's "Done when" asks: "A test or eval shows: no post without approval; the draft holds the
three parts; a ticket-less item skips the step." Main has the eval written
(`evals/ticket-summary/RUNBOOK.md`, its kit `evals/kit/ticket-summary/`, its dry-run case
`ticket-summary-setup`) but never run: `evals/results/` holds no `ticket-summary-*` report, and
`evals/results/claims-v0.10.0.md` lists the claim as "not exercised". The card marks the GitHub
route "unproved; trial: the eval `ticket-summary`".

Further, the specified backlog item `2-backlog/P3/evals-rework` (its `02-answers.md`, Q3, the
user's answer) removes the `ticket-summary` campaign and its kit and turns the card's line into
"**GitHub** (unproved; no trial planned)". So the user has already accepted that this behaviour
stays unproved by an eval.

## Out of scope

- Any change to the "Ticket summary" block, the PR follow-up, "Released in", `pr-template.md`,
  `concepts.md`, `griller.md` or the docs: they hold the intent.
- Any CLI change: the CLI knows no tracker (AGENTS.md, CLI scope).
- A configuration fixing a tracker's access method.
- Copying issue #336's own texts into the repository.

## Evidence

For the default answer (a): none to produce; the table above is the check, each row readable at
main with `rg -n "Ticket summary|PR follow-up|Released in" skills/chantier/references/chief-of-staff.md`
and `rg -n "Issues References" skills/chantier/references/pr-template.md`.

For (b): the eval's report `evals/results/ticket-summary-<date>-run1.md`, passing its RUNBOOK's
(a) to (d), before `evals-rework` lands; on a pass, the card's "unproved" marker on the GitHub line
is lifted in the same change.

For (c): see the open question; a Driver would need its answer before any code.

## Open questions

1. **tracker-grill-summary-Q1: is anything left to do here?** The intent is delivered by CR-220;
   only its "Done when" proof is missing, and `evals-rework` Q3 already accepts it staying unproved.
   Options:
   - (a) Abandon this item as delivered by CR-220 (recommended: nothing to build, and the user's
     `evals-rework` Q3 answer covers the proof).
   - (b) Run the existing `ticket-summary` eval once (about $1, on the sandbox, the user present for
     the "no" then "yes" turns) before `evals-rework` removes it, and lift the "unproved" marker on a
     pass.
   - (c) Keep the item for a structural test in `skills/chantier/scripts/cli/tests/` that reads the
     shipped `chief-of-staff.md` and asserts the yes-per-ticket rule, the three drafts and the skip
     line. It proves the text, not an agent's behaviour, and adds a test the project's "few tests"
     rule would weigh.
