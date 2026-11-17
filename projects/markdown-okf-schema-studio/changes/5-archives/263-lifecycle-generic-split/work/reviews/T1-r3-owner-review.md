Verdict: FIX-REQUIRED

Extra critical review on Opus, asked by the owner, at head 167d7c3f. It simulated cold sessions from
`AGENTS.md`. The move is faithful. Line numbers are at that head. This is round 3, the last one.

## Must fix

- B1: a release session never reaches the release role. Add "and when preparing or running a release"
  to the load trigger of the process in `AGENTS.md` (l.35-37).
- B2: lost rule, who opens the release folder. Lifecycle l.294: "Opens and owns", and says it creates
  `03-change-spec.md` and the `STATUS.md` header.

## Fix in the same round

- M1: harden `test/build/test_guideline_isolation.py`: `Chief\s+of\s+Staff`, `rglob`, scan
  `CONTRIBUTING.md`, assert the link sits inside `## Process`, count bare path mentions. Add coder,
  reviewer, orchestrator as roles if no false positive. Reword `CONTRIBUTING.md:514` neutrally.
- M2: constitution l.79-82 contradicts `AGENTS.md`: say the project guidelines name no role, and only
  `AGENTS.md` links the process.
- M3: lifecycle: say that a single CR runs the same tree (Foreman and driver), as this run did.
- M4: Vocabulary: one line each for Chief of Staff ("the session the user talks to", not the Chantier
  tool), Foreman and heartbeat.
- M5: lifecycle l.414: repo-root path in backticks, since that text is copied into `rules.md`.
- M6: heartbeat l.331-332 and rebase rule l.105-106: in stack mode, message the stack driver. l.161:
  remove "merges" from the Chief of Staff, or say the user merges.
- M7: `AGENTS.md:35`: scope "or PRs" to `.agents/changes/` work and say a change may run without a CR.
  `local-worktree` l.11-13 and `pull-request` l.55-56: replace `NNN` by `<id>` or define it.
- M9: PR body: no "Chantier vocabulary" unexplained, no round number, tick `CI green` only when true.
- N4: PR body and report: state that "During a change" went to `project.guidelines.md` and why.
- N5: Stack driver and Conflict resolver rows: no invented count, model or Copilot value that the old
  guideline did not hold; write "as the CR driver" where it holds.

## Not in this round

M8 is the main session's rename at the merge. N3 (`approved_on` in the okfreq skills) is a follow-up.
