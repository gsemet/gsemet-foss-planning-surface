# CR-166 verification result

Verdict: VERIFIED (PR 102, head 6fb0521, checked at that head)

- `just check` in the worktree: 37 passed, release-notes ok.
- Four moments: chief-of-staff.md Tips (first use, after a status, end of a batch, during a release) and status-layout.md Tips.
- One short 💡 line, last line after "For you:", once per moment and per session: both files.
- "plus de conseils" turns tips off for the session: both files.
- "auto" = merge, tag, publication for this release only; announcement stays a draft (chief-of-staff Releases, driver.md sentence). Never covers announcement, fixes, order confirm, budget raise.
- Approval question lists "auto", not a tip, holds when tips are off: chief-of-staff.md.
- Entry-points row added. Five steps match the spec (handoff k, budget first, order grant releases=k+1, send to Foreman or back to a Driver, one-line tell).
- session-start.md and init.md sentences present. No CLI or agent file changed.
- PR description matches the diff (cards changed, Q1-Q4 recommended answers, blast radius 1).

Minor notes, not blocking: the init.md and session-start.md added sentences are single long lines (not wrapped like the rest); the PR test-plan checkboxes are unticked.
