## Version PR for chantier v0.13.0

Makes v0.13.0 ready to tag: the release folder `docs/release-notes/2026-11-18-v0.13.0/`, the claims file `evals/results/claims-v0.13.0.md`, and the commit `release: v0.13.0` made by `just release minor` (0.12.0 to 0.13.0). The version is the release specification's: a minor bump, since the release adds features (the forge hub and `chantier watch`, the switch to direct mode) and changes one default (the CR archive out of the PR on an external planning surface), with no incompatible interface change.

**No eval campaign ran before this release** (the user's word, 2026-11-18). In the claims file, a claim that a named check of `just scenario` or `just test` proves is `scenario only` (7 of 12) and every other claim is `not exercised` (5); none is `exercised`. The notes say so under For contributors. The forge hub's wake of a session was observed once on Claude Code in the batch the captures come from; the notes keep it on trial, and unproved on GitHub Copilot.

Every `feat:` and `fix:` commit since v0.12.0 (12, out of 14 commits) appears once in the notes; the map of each commit to its place is kept with the release's working files. The tag, the GitHub release and the thread are not part of this PR: after the merge, the steering session runs them on the user's approval, and the user posts the thread.

**Images:** `watch-wake-pc.png` is rendered with headless Chrome from the batch's conversation excerpt and the real output of `chantier watch`; `logo-pc.png` is the logo PR's own capture. Both were read before the commit; neither shows a local path or a user name.

**CI:** `just check` passed locally at the head (`just release` runs it; it includes `scripts/release_notes.py --check`). No `just scenario`: this PR changes no CLI, card or scenario.

**Known gaps:** `just copilot-models` was not run for this release: the specification limits the PR to the version files, the release folder and the claims file, and `just check` passed with the agent files' models as they are.
