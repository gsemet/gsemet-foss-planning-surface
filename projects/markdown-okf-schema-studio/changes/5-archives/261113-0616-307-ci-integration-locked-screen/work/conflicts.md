# Conflicts: CR-307 restack onto CR-306

One conflict, in `.agents/guidelines/release-process.guidelines.md`, step 5 of the release process.
CR-305 added the "version PR on top of a stack" sentence. CR-307 added the locked-screen rule
(dispatch the heavy run at once when `ci-integration` stops). Both kept, in that order.

`requirements/tiers/log.md` and the generated indexes did not conflict. `just check` passes.
New head: d41cbd0534f1f369fad7c3defd4edee04d113f8c (not pushed).
