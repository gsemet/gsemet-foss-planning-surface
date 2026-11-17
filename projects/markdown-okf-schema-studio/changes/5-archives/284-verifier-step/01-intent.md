---
title: A verifier step before a pull request turns ready
description: Prove the spec at the pushed head and check the posted PR body against the template and the diff, as Chantier's Verifier does.
status: request
date: 2026-11-11
issue: none
---

# A verifier step before a pull request turns ready

> [!NOTE]
> Found 2026-11-11: PR #345 merged with a body that skipped the PR template (only Summary and
> Checks). The Inspector reads the diff only, and the process has no step that checks the posted
> body. Chantier has one: its Verifier, after CI, proves the spec at the pushed head and treats the
> PR description as a claim (renders, matches the diff); its Inspector also reads `pr-body.md`.

## The request

- After CI is green, before `gh pr ready`, a Verifier (fresh agent, not the round's Coder or
  Inspector) proves each spec claim at the pushed head and checks the posted body: every template
  section, Summary/Deliverables/Changes match the diff. `NOT VERIFIED` on the code is a round; on
  the body, the driver fixes the body and checks again.
- The Inspector also reviews the draft PR body with the diff.
- Alternative: switch this project to the Chantier process (one `AGENTS.md` line), which already
  has both.

Meanwhile (owner, 2026-11-11, "arrange toi pour que ça n'arrive plus"): the run's brief requires the
template check before `gh pr ready`, and the Chief of Staff checks each PR body before saying it
is mergeable.

## Second miss: screenshots (2026-11-11)

PRs #346 to #352 (CRs 277 to 282) have no screenshot, while #340 (272) and #341 (273) had them.
The owner asked why, and how to stop it on long sessions.

Causes:

1. **The rule was rewritten by hand in each `task.md`, and it drifted.** CRs 272 and 273:
   "Before and after screenshots, light and dark, named in the report" (no condition). CRs 277 to
   282: "Before and after screenshots if the page changes visibly". Each driver judged its own
   fix "not visible", although every one changes what the user sees in the table editor.
2. **Nothing checks it.** The lifecycle guideline names screenshots in step 1 and in the report,
   but no step blocks `gh pr ready` without them. The Inspector reads the diff only. The Chief of
   Staff checked the body's section headings, not their content.
3. **No capture was planned.** The run brief said "no real VS Code window locally", and nobody
   said how to take the before and after (headless visual run of the base and of the head).
4. **Long sessions keep only what is short and written down.** The Foreman compacts, reads the
   guideline in parts, and the brief holds only owner orders. A rule that lives only in a
   guideline paragraph, or in a sentence copied into each task, is the first to go.

Proposal (what Chantier already does, adapted):

- **Investigator writes an evidence plan** before the first round: kind of change, what shows it
  before and after, the technique (this project's headless visual run or e2e), or one line "no
  visible change" with the reason.
- **Verifier, a fresh agent after CI and before `gh pr ready`:** at the pushed head, proves each
  spec claim with a command and its output; captures the before on a detached worktree of the
  base and the after at the head; checks the posted body (six template sections, Impacts with
  the screenshots or the "no visible change" line, Autonomous decisions when the coder chose).
  `NOT VERIFIED` blocks `gh pr ready`.
- **The rule lives in the guideline, never in `task.md`:** the task links to the Verifier step;
  it never restates the screenshot condition.
- **The Chief of Staff's mergeable check** adds: image links in Impacts for a UI change.

Alternative: switch this project to the Chantier process (one `AGENTS.md` line), which has the
Investigator's evidence plan, the Verifier and the template check today.
