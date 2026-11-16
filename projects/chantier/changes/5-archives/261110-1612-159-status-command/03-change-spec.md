# Change Specification: status-command

## Problem

The Progress and Completion reports have a fixed shape, approved by the user. It lives in
`skills/chantier/references/chief-of-staff.md`, section "While it runs", bullet "Reports", inside a
card of about 500 lines. After a context compaction, the Chief of Staff keeps only a summary of
that card and answers "status" in free text. The user follows batches through these reports,
often on Remote Control, and reads them at a glance; a report in another shape is a defect.

## The change

1. **A short report card**, `skills/chantier/references/report.md`.
   - It holds the whole report format now in `chief-of-staff.md`:
     - the icons and their legend line, copied from `status`'s label;
     - Progress: the header line, the table columns, the explanation under the table of a 🟠 or
       🔴 CR, the cost table, and the last line, **For you**;
     - Completion: the header, the table columns, the cost table and `cost --explain`, what the
       batch did not prove, and **For you**;
     - the Tips line;
     - "MR" on a GitLab remote, and "PR" elsewhere;
     - naming each CR by its number and its slug;
     - running `status --refresh` with no epoch before a report.
   - `chief-of-staff.md` keeps one line in its place, pointing to `report.md`.
   - No rule is lost or changed in the move.
2. **A `/chantier:status` command**, `skills/status/SKILL.md`, built like `skills/griller/`, with
   its paths through the common skill at `../chantier/`. When invoked, it:
   - reads `report.md` only, not the main skill, `chief-of-staff.md` or the introduction;
   - runs `$CHANTIER status --refresh` with no epoch, `$CHANTIER status` and `$CHANTIER cost`
     for the active batch, or for each active batch when there are several;
   - writes the Progress report in the user's language, in the shape `report.md` gives;
   - with no active batch, says so in one line and shows the backlog count from `STATUS.md`.
   - It changes nothing: no order, no heartbeat, no epoch.
3. **Where it is offered:**
   - `report.md`'s Tips may name `/chantier:status`;
   - the README's command list and `docs/` name it where the other skills are listed.

## Out of scope

A CLI `status --report` printing the table (the user's choice: not in this CR). Changes to
`status` or `cost` output.

## Depends on

`changes-tree-v2` (CR-158): the skill reads the paths of the new tree (the index at
`.agents/changes/STATUS.md`).

## Acceptance

- `report.md` exists and holds every rule of the former "Reports" bullet; `chief-of-staff.md`
  points to it.
- `skills/status/SKILL.md` exists, loads as `/chantier:status`, reads only `report.md`, and runs
  the three commands with no epoch.
- `just check` passes (structure tests: a new skill, a new card); `just scenario` passes (cards
  change).
- Evidence: one `/chantier:status` output on a scenario batch, in the report's shape.
