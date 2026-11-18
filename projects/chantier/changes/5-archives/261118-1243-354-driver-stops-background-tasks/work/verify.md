Head: db4ba03eb86f943f6acf355e3052211213093f2c

Judged at db4ba03 (pushed head, PR 320; `git status` clean).

1. TaskStop only in hosts/claude-code.md. Command: `rg -n "TaskStop" skills/chantier/references`. Output: matches only `hosts\claude-code.md` lines 37, 39, 40. Held.
2. Four agents have TaskStop after Monitor, bodies unchanged. Command: `grep -n "^tools:" agents/{cr,stack,qa,release}-driver.md` plus `git diff origin/main --stat -- agents/<f>`. Output: each `tools:` line ends `Monitor, TaskStop`; each diff is 1 insertion, 1 deletion (the tools line only). Held.
3. `just mod` at db4ba03: `82 pass 0 fail`; includes "(pass) a CR driver whose worktree exists starts in it, and a relative path is read against it", "(pass) a CR driver whose worktree does not exist yet starts in the project's root", "(pass) a CR driver with no worktree and no root to read starts in its parent's folder, guarded, with a note", "(pass) a worker with a worktree line keeps starting in its worktree". Held.
4. Sections 2 to 5 passages present with the spec's words (read from `git diff origin/main` at db4ba03): write-guard sentence, start-folder rows (claude-code, copilot), concepts "Starting an agent" insert, CONTRIBUTING and docs/boards wording, rule 8 passage, driver.md 4a to 4d, foreman.md 5a to 5e, section 6 rows. Held. Section 1 code matches the spec: worktreeOf/rootOf helpers, the five-case choice, the note text, Worker cwd.
5. PR description (gh pr view 320): renders, no images, Summary/Deliverables/Changes match the 13-file diff, Known gaps names the unproved trials. Review box `approved at bdd27e0, committed as db4ba03` matches the Driver's log notes ("r1 approved at bdd27e0f, committed as db4ba03e"). "Verified" and "CI green" boxes are for the Driver to tick. Held.
6. CI and long gate: per the brief, CI green with `just scenario` at db4ba03 (not rerun by me).

VERIFIED
