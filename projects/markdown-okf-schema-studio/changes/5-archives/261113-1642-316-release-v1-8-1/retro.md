# Retro: release v1.8.1

- Gate 1 failed on `tsc: command not found`: the new worktree had no `node_modules` (the main checkout had none to link). Fix: the worktree setup of local-worktree.guidelines.md runs `just dev` before the first gate.
- Local real-window integration failed because another app took window focus, and report and gallery failed after it, so preflight showed 3 failed stages for one cause. Fix: run a release's local integration unattended per local-worktree.guidelines.md, or skip it locally and dispatch the branch heavy run at once, as the guideline already allows for a locked screen.
- The notes needed a steering correction (the sentences about the token) and an amend. Fix: the notes draft of a publishing-only release states the facts from the change's specification, reviewed by the Chief of Staff before the version commit.
- The merge needed a new Driver to watch the version push. Fix: none needed; a release PR is merged by the steering session by design.
- `$CHANTIER` held in a shell variable did not run under zsh (no word splitting). Fix: the Driver card says to call the CLI as a function or write it out in full.
- Which Marketplace policy matched cannot be seen from CI. Fix: the owner removes the unused policy once "Last used" shows which one the release uses.
