# The release Driver's end steps as a checklist

## Goal

Once a release is out, the release Driver finishes its run without being told: it records the
publication (`release published`), writes `work/retro.md` and hands back `ready`. In batch-22 the
post-merge release Driver of v0.11.0 (CR-307) tagged and published, then stopped with these three
steps undone until the user asked (retro of batch-22, kept by the retro critic; record:
`5-archives/batches/batch-22.md`). The long-term fix the retro names: the release Driver's card
lists its end steps as a checklist in its hand-back part.

This is a card change only: the release Driver's contract, which both hosts (Claude Code and
Copilot) read from the same card.

## What changes

### The card: `skills/chantier/references/driver.md`, section `## Release driver`

Today the end is one prose bullet among the others (the bullet that starts "A release out:",
lines 989-993 at `3df17b9`): `release published`, the procedure's checks and deploy watches,
`<work folder>/retro.md`, `handback ready`. It reads as one more rule, not as the steps that close
the run.

1. Replace that bullet with a sub-section at the end of `## Release driver`, a level-3 heading so it
   stays inside the section the startup manifest loads for the release Driver:

   ```md
   ### Release driver: the end
   ```

   (the exact wording of the heading is the Driver's; it must be `###`, under `## Release driver`
   and above `## Startup core`).

2. Its body opens with one line saying when it applies and that it is not optional: once the
   release is out (the procedure's publication step done), every item below, in this order, before
   the host's hand-back; the run is not over while one is undone, and none waits for a word from
   the steering session or the user, except as the section's existing bullets already require (a go
   the procedure itself asks for: `handback blocked approval: <step>`; a failure: "Half-done
   irreversible work: stop").

3. Then the checklist, as a Markdown task list (`- [ ]`), one item per step, carrying today's text
   with nothing dropped and nothing added beyond the opening line:

   - [ ] `$CHANTIER release published <cr> --note "<version> <link>"`.
   - [ ] The procedure's checks, and any watch of the deploys it names (a package registry, pages).
   - [ ] `<work folder>/retro.md`: what went wrong or slowly, the long-term fix for each, one line
     `- [<tag>] <problem>: <long-term fix>`, the tag `project` or `chantier` as the Foreman's retro
     defines it in `foreman.md`.
   - [ ] `$CHANTIER handback <cr> ready <release link or tag>`, then the host's hand-back, as
     "Your means" orders it (its first line is the line `handback` printed).

4. The other bullets of `## Release driver` stay as they are. The bullet "A step fails on the
   product..." (the `fix-<n>.md` and `blocked infra:` rules) stays a bullet of the section, above
   the new sub-section, so the checklist is the last thing in the section. A step of the checklist
   that fails follows those same rules (a product failure: `fix-<n>.md`; the infrastructure: one
   re-run, then `blocked infra:`), and the bullet's existing text already covers it: no new rule.

### The agent files: unchanged

`agents/release-driver.md` and `com.github.copilot/agents/chantier-release-driver.agent.md` hold
no contract (AGENTS.md: a role's contract lives in the cards). Both read the same card, so the
change reaches both hosts with no edit to either file; their bodies stay identical.

### The startup manifest: unchanged

`skills/chantier/references/startup-manifest.json` loads `## Your means` and `## Release driver`
of `driver.md` for the `release-driver` action. A `###` sub-section inside `## Release driver` is
part of that section's span (`_section_span` in
`skills/chantier/scripts/cli/tests/test_startup_manifest.py` ends a section only at a heading of
level 1 or 2), so the release Driver reads the checklist with the rest of its section. The
release Driver's startup bytes do not change (`## Release driver` is an action reading, not a
mandatory section).

## Decisions carried from `02-answers.md`

- The change is the one the retro names: the release-driver card lists its end steps
  (`release published`, `work/retro.md`, `handback ready`) as a checklist in its hand-back part.
- It changes a role's card (the release Driver's contract), on both hosts: one shared card, read by
  both.
- Priority P1, in the next batch (the user, 2026-11-17).

## Out of scope

- Any CLI change: no new refusal (for example `handback ready` refused on a release CR with no
  `release published`), no new printed hint. The CLI says what it refuses; this CR changes what the
  role judges.
- The other roles' cards, the Foreman's and the Chief of Staff's handling of a release Driver.
- The other retro points of batch-22 (each is its own inbox item).
- The docs diagrams and their texts (`docs/cr-lifecycle*`, `docs/how-chantier-works*`): they draw
  the release Driver's steps at a level this change does not alter.
- `release-template.md` and the release procedure in `CONTRIBUTING.md`.

## Evidence

- The diff touches `skills/chantier/references/driver.md` only, inside `## Release driver`: the
  four end steps are a `- [ ]` list under a `###` heading, the last thing before `## Startup core`;
  the old "A release out:" bullet is gone; every element of its text is in the list (`release
  published` with its `--note "<version> <link>"`, the checks and deploy watches, `retro.md` with
  its line format and tags, `handback ready <release link or tag>`).
- `just check` passes on the branch (Linux, macOS and Windows in CI), including
  `test_startup_manifest.py` (the manifest still finds `## Release driver` and `## Your means`; the
  startup budgets hold).
- `just scenario (ubuntu-latest)` is green at the PR's head (AGENTS.md: a change to the cards
  passes it before its PR).
- `git diff --stat` shows no change under `agents/` or `com.github.copilot/agents/`, and none in
  `startup-manifest.json`.
- No `hooks/` or `types/` change, so no `just mod`.
