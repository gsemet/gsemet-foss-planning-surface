## Summary

A release CR asked in a batch is now a normal CR of that batch. It waits for every other CR, is prepared on top of the stack (or series) once they are ready, and its PR is the top PR. The user reviews the work and the release together and merges from the bottom up; the merge of the release PR is the go for the rest of the release procedure. There is no version confirmation any more: the version is the one settled at filing, else the Release driver picks it and says why in the PR. In a parallel batch the release is prepared after the merges. An approval never lets the steering session merge a release PR; only the explicit grant does. `chantier` names no step of the procedure.

## Changes

- CLI: release waits (ready or merged in an ordered batch, merged in a parallel one), start rail on the top CR's branch, `release go` answers `merge` until the stack and release PR are merged, new `merged_pr` and `procedure` fields (older records give no go), `order confirm` now means the user's word to run a procedure with no release PR.
- Cards, project release procedure and docs say the same; `docs/batch-pace.svg` is redrawn with the release as a CR of the batch.
- Scenario: sections 14, 14c, 15 updated and a new stack-release section.

## Test plan

- [x] `just check`
- [x] `just scenario` (github and gitlab, 615/615)

## Internal references

CR-196 release-cr-in-batch (batch-15)
