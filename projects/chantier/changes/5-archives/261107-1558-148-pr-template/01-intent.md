# Intent: a default PR description template, shipped in the skill

## Problem

PR descriptions written by Drivers are two or three sentences (PRs #80, #81 of batch-08). The
Driver card (`driver.md`) says only that "the title and body follow the project's rules and
template"; a project with no template and no PR rule (chantier itself) gets a terse body.
Nothing reviews `pr-body.md`: the Inspector reviews the diff only. The before/after evidence of
the Verifier is the only visual, and a Driver that runs no Verifier leaves none.

## Source

The markdown-okf-schema-studio project's rules, which the user found very good:

- `.agents/guidelines/ci.guidelines.md`, rule 10: every PR uses
  `.github/PULL_REQUEST_TEMPLATE.md` (Summary, Deliverables, Changes, Impacts, Blast radius graded
  1 to 3, Test plan), in English; every section filled, "None" rather than deleted; written for a
  reader outside the team, no internal ids.
- `.agents/guidelines/pull-request.guidelines.md`: a body for an external reader (no CR numbers,
  roles, round numbers or `.agents/changes/` paths in the text; an optional last "Internal
  references" section); a Deliverables section right after Summary with one or more small
  visuals (a Mermaid flowchart of about 10 nodes, a sequence diagram before and after, a
  before/after tree or table, before/after screenshots, a 5-15 line code sketch), real names
  checked against the code; a one-line fix may skip it, a structural change never; screenshots in
  Impacts; "Autonomous decisions" lists what an agent decided without the user; the body is kept
  current with the scope.

## Wanted

A default PR description template that chantier ships as a reference in its skill (not in
chantier's own `.github/`), easy to audit, taken from the markdown-okf-schema-studio template.
A project's own template and rules rank above it. When a user asks for a customised version in
their project, the agent writes a guideline and a template there.
