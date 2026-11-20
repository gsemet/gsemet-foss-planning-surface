# Before and after, CR-342

Before (base 72eb59fc, CR-341 branch): no use case diagram exists on the site or in the rule; no before capture (nothing to show).
After (pushed head b971dda8541eb343d17723ae901ce7d572500725 plus a scratch commit adding three sample diagrams, branch `uc-diagrams-sample`, deleted):

- evidence/site-local-001.png (state), site-local-003.png (sequence), site-local-006.png (flowchart): local site build, JavaScript off.
- evidence/site-ci-001/003/006.png: the same pages from the CI-built site (ubuntu, run 44165653094, artifact studio-site-attempt-1).
- evidence/github-svg-001/003/006.png: the diagram as GitHub draws it on the StRS file (the Mermaid iframe element only; a whole-page headless screenshot leaves the cross-origin iframe blank).
Reproduce: add a `### Use case diagram` fence before `### Main paths` in StRS-MDOKFSTUDIO-BLOCK-001/003/006, `just requirements-report`, `fnm exec -- npm.cmd run site`.
All captures show page content only: no local path, no username.
