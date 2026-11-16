## Summary

A change request's folder now holds everything needed to resume it later or elsewhere: prototypes (in versions), experiments, kept screenshots and how to run a prototype again. The cards no longer say a prototype lives in a temporary folder and is thrown away, the Griller's artifact rule holds in every planning mode, and a chantier rule ranks above the host's habit of sending scripts to its scratchpad.

## Deliverables

The CR folder layout in the concepts card gains two optional entries, created only when something goes in them (no empty folder in advance):

```text
<slug>/
├── prototypes/NN-<idea>/  ← each prototype version, with a README.md saying how to run it
├── experiments/           ← scripts, tests, benchmarks, studies, research notes
├── evidence/              ← proof kept on purpose
└── work/
```

Choices made:
- Prototypes come in numbered versions; the retained one is recorded in the answers.
- The PR's cleaned archive carries the retained prototype: as is up to 1 MB, zipped from 1 to 10 MB. Above 10 MB with no recorded decision it stays out and the PR's Known gaps names it. With no retained version named, none is carried.
- Above 10 MB the grill asks, at the end of the grill, what to do with the folder.

## Blast radius

- **1**: local and isolated; a plain `git revert` restores the previous behaviour.
- **2**: several features or shared code; revert is possible but needs checks or follow-ups.
- **3**: wide impact (data, formats, CI, release, public API); rollback is complex or partial.

Grade: 1

Only the agent cards and docs change; no CLI, agent file or hook. A plain `git revert` restores the previous wording.

## Autonomous decisions

- Size limits (1 MB / 10 MB), no prototype when no version is retained, and the Driver naming a folder that grew very big in Known gaps were taken from the recorded defaults of the specification's open points.

## Known gaps

The long gate ran on Windows only; Linux and macOS are covered by CI alone (`just check` on all three, `just scenario` on Linux).

<details><summary>Details</summary>

## Changes

- `skills/chantier/references/concepts.md`: tree, a new rule "A CR's folder holds its work", archive entry, subagents paragraph.
- `skills/chantier/references/chief-of-staff.md`: subagents text, artifacts and leaks during a grill, size question, worktree files.
- `skills/chantier/references/griller.md`: prototype rule moved to "What you do"; worktree section.
- `skills/chantier/references/driver.md`: "The archive in the PR" carries the retained prototype.
- `skills/chantier/references/hosts/claude-code.md`: the host scratchpad instruction does not apply to a CR's work.
- `docs/planning-modes.md`, `docs/planning-folder.md`.

## Human decisions

- No empty folder in advance; prototypes in versions; retained prototype in the PR's archive (zipped if needed); the grill asks what to do when the folder is very big.

## Impacts

None beyond the cards and docs.

## Test plan

- [ ] New or changed tests (they fail on the previous code): No behaviour change (cards and docs only)
- [x] Local gates: `just check` at 54b4756; `just scenario` at 3886afd, carried to 54b4756 over a clean rebase onto main 33fc800
- [x] Evidence: a search of `skills/` and `docs/` for "thrown away" finds nothing at 54b4756; no screenshot, the CR board pane does not change
- [x] Review: approved at ce00ec3 (code pass and body re-inspection), carried from ce00ec3 over clean rebases to 54b4756
- [x] Verified at 54b4756
- [x] CI green at 54b4756: `just check` x3, `just eval-dry-run`, `just scenario`

## Internal references

- CR-257 cr-folder-self-contained
- Archive in the PR: none for this project unless `take` says so.

</details>
