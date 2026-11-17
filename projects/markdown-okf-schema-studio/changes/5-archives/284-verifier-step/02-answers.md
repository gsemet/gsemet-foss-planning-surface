---
title: Grill answers, verifier step
date: 2026-11-11
---

# Grill answers

Owner's answers, 2026-11-11.

| Question | Answer |
| --- | --- |
| Fix the missing screenshots and template misses for good | "Rajoutes juste un vérifier simple qui vérifie la même chose que dans Chantier." |
| Switch to the Chantier process | No: add the step to this project's lifecycle guideline. |
| What the Verifier checks | What Chantier's Verifier checks: at the pushed head, each claim of `03-change-spec.md` proved by a command and its output (notes and green CI are not proof); before/after evidence (before on a detached worktree of the base, after at the head) for a visible change, or one line "no visible change" with the reason; the posted PR body (template sections, Impacts with the evidence, Autonomous decisions when the coder chose). |
| Who | A fresh sub-agent, never the round's coder or Inspector; never edits code; Sonnet. |
| When | After CI is green (step 9), before the PR turns ready (step 10). `NOT VERIFIED` on the code is a round (counts in the round limit); on the body or the evidence, the driver fixes them and runs the Verifier again. |
| Investigator | Not added ("simple"): the Verifier picks the capture technique from the project's rules (headless visual run or e2e). |
| Where the rule lives | In the guideline only. `task.md` links to the step and never restates the screenshot condition. |
| Chantier | Not touched. |
| Tracker issue | none. |
| Run | Outside the stack, its own draft PR from `origin/main`. |

## Scope

- `.agents/guidelines/change-requests-lifecycle.guidelines.md`: a Verify step in the Lifecycle
  table, the role in "Roles and models", the output path (`work/verifier/`), the step in the driver
  prompt and stack mode if they list steps, `rules.md` template if needed.
- `.agents/guidelines/pull-request.guidelines.md`: Impacts takes the Verifier's before/after or the
  "no visible change" line.
- Process text only; no product code, no requirements change, no heavy CI run. Blast radius 1:
  Inspector on Sonnet.
