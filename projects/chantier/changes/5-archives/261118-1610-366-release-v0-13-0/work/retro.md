# Retro: CR-366, release v0.13.0

- [chantier] Steps 4 and 5 (tag and publication) needed a second Driver start after the merge, because the grant held every irreversible action for the user's word and the first Driver ended waiting for it: let the steering session collect the user's word for the post-merge steps (tag, publish) together with the merge go, so one Driver runs the procedure to its end.
- [chantier] `handoff CR-366` printed `PR: none; head -` although PR 331 was opened, green and merged (only notes carry it): have the release Driver's PR go through `ship` like a CR Driver's, or have `handoff` read the release's merged PR, so the record shows the PR a release shipped.
