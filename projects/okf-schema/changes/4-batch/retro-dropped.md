## 2026-11-26: CR-101, CR-102, CR-103, CR-104, CR-105

Dropped and merged points, each with the retro critic's reason. Numbers are those of the critic's brief.

- 1, dropped. [project] This Windows host refused symbolic links (WinError 1314), so 8 tests failed and `just preflight` could not pass until the user enabled Developer Mode. Why: already covered by the open item `1-inbox/symlink-tests-skip`; Developer Mode is on now.
- 6, merged with 5. [chantier] A broad file listing matched virtual environments left in another CR's `work/scratch`. Why: one occurrence and one cause of the Driver context cost of point 5.
- 13, dropped. [chantier] The cards of the chantier checkout changed while the batch ran. Why: one occurrence, no cost or defect shown.
- 14, dropped. [chantier] The Chief of Staff told the user a merge would publish the release. Why: one occurrence, corrected inside the batch; the release then ran by the project's procedure.
- 16, merged with 15. [chantier] CR-101's round 2 Coder set TEMP inside the worktree. Why: a workaround for the same missing scratch folder.
- 17, dropped. [chantier] Verifiers changed their shell folder into a CR's work folder. Why: the startup core already forbids it; both calls did nothing.
- 19, merged with 18. [chantier] Two Verifiers could not create a detached worktree of the base on Windows. Why: same two occurrences and same cause as point 18.
- 20, dropped. [chantier] `handback ready` refused the gaps text placed after `--lease`. Why: one refusal, fixed at once, no cost.
- 21, dropped. [chantier] `status` still lists CR-105's release drafts under `2-actives/`. Why: one stale path, no lost work or wrong decision.
- 23 to 29, merged with 15. [chantier] Seven refused writes to the session scratchpad. Why: each is one instance of the refusal of point 15.
- 30, dropped. [chantier] The host's auto mode refused the steering session removing the project's virtual environment. Why: one refusal, the action is already blocked and nothing was lost.
- 31, dropped. [project] The CI-started Release run failed at note generation. Why: already covered by the open item `1-inbox/release-notes-without-copilot`.
- 33, merged with 2. [project] `just preflight` rewrote 14 files with line-ending changes only. Why: the same gate leaving the tree dirty as point 2.
- 35, merged with 5. [chantier] The first release Driver handed back `context:` before the push. Why: the same Driver context problem as point 5.
