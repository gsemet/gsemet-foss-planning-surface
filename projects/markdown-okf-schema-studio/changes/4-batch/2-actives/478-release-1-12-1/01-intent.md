# Release v1.12.1

Release 1.12.1 on top of batch-09's stack, by the project's release procedure
(`.agents/guidelines/release-process.guidelines.md`, "The version PR on top of a stack"; "How to
Release" in CONTRIBUTING.md).

It ships the batch's three open CRs: the revert of 1.12.0's opening watcher (`raw-text-opens-studio`,
the urgent fix: "Open With > Text Editor" is replaced by Studio in 1.12.0), CR-475
`save-guard-never-hangs` and CR-476 `blank-line-block-per-line`. CR-474 (PR #491) is already on
`main` and ships in it too.
