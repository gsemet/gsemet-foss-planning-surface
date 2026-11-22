# take's base on a working CR's draft PR: keep, or start on main?

Priority P3. Split out of `take-base-from-forge` (its answer Q5), 2026-11-20, by the Chief of Staff.

In a stack batch, `take` starts a new CR on the nearest earlier CR of the batch that has a PR, whatever that CR's status and its PR's draft state (the user's answer stack-Q4 of 2026-11-17, `take-base-nearest-pr`: one linear stack, not a tree). In Studio's batch-06, CR-429 was given the branch of CR-424, a working CR with an open draft PR and several rounds still to come (the takeover of an external PR); the Foreman's take note sent CR-429 to origin/main instead, and its retro counts that base as wrong.

A decision for the user: keep the rule as it is, or start a new CR only on a CR handed back ready (else on the default branch), or let the Foreman name the base at the take. `take-base-from-forge` left the rule unchanged; it only leaves out a CR whose PR the forge shows merged.
