Lessons of batch-17's refused force pushes (2026-11-13), for batch-17's retro: chantier points, so each is offered as a GitHub issue draft (CR-231's rule).

What happened: after CR-224, CR-230 and CR-231 merged, the Drivers of CR-231 and CR-236 rebased and their force push was refused by the host (auto mode's classifier). Each went Driver → Foreman → Chief of Staff. The Chief of Staff asked the user each time (against `chief-of-staff.md`, which says the push is judged and run with no ask), and CR-236's Driver ran out of context (about 71,000 tokens) while it waited, so the Foreman restarted it with a new Driver that had to read everything again.

Causes found:
1. **P10's warn at the batch's start was not put to the user.** Preflight said "14 of 16 commands … are not allowed"; the user's settings lacked the `git -C * push --force-with-lease -u origin chantier/*` form among others. Fixed for this user on 2026-11-13 (15 rules added, `gh release create` left out on purpose); CR-238 (allow-rules-ask) makes the Chief of Staff ask and add them.
2. **The refusal's exact command and text were not recorded.** CR-236's note says only "Force push refused by host"; concepts rule 7 asks for the exact text. Without it the cause (a missing rule, or the classifier on a matching rule) cannot be proved.
3. **A Driver waiting for a push spends its context.** It should hand back (`blocked`, with the push line and its next steps in the record) as soon as it sends the push line, and be restarted by the Foreman once `pushed` comes back, instead of waiting in its turn.
4. **The Chief of Staff asked the user for a push the card says it runs alone.** The user (2026-11-13): agreed that the Chief of Staff pushes without asking once its checks pass, as the card says.
