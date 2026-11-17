# Verify CR-316

Head: 767a897fc3ffb2aa0466b9dacb1e89421b340e3f

Second verification, given the move a17f0fc..767a897 (clean rebase onto 133a15c, CR-312..314 merged in main).

## Move (judged at 767a897)
- Patch unchanged: `git patch-id --stable` of `git show a17f0fc` and `git show 767a897` both give `d32964f43abd95bbc9705182b0e8437a0c91f8cf`. Worktree clean.
- The base brought changes to what the scenario runs, so the long gate was run again (not carried).
- Long gate: `chantier gate CR-316 "just scenario" --batch batch-23` printed `pass just scenario at 767a897`; log `work/gates/20261117-124340.log`, first line `gate CR-316 branch ...cr-316-... head 767a897fc3ffb2aa0466b9dacb1e89421b340e3f`, `result: pass at 767a897fc3ffb2aa0466b9dacb1e89421b340e3f`. Transcript `scenario/results/scenario-20261117-124340-5936.md`: 0 unchecked `- [ ]` steps (`grep -c -F -- "- [ ]"` = 0).
- CI at this head: Driver's note `gh pr checks 272 at 767a897: all 5 jobs pass`.

## Evidence items 1-12 (close behaviour), judged at 767a897 from that transcript
All steps checked in the run above. Seen in its output: held running agent refuses (`transcript uuid-foreman agent-agent-2 still runs: its last record is a tool's result with no answer yet`, with and without `--yes`); passing `close` lists `not agents of batch-01, not judged (no word needed; their calls are counted only up to now): 2` with the running and the unreadable (`holds no user or assistant record`) agent-agent-5 apart; held cut JSON refuses `cannot be read: its last line is not complete JSON`, `--stopped` refused; held id with no transcript refuses `cannot be read: the file is missing`; record causes (CR queued, open order O-8) unchanged. Other items (4-10, 12) are steps of the same green run, carried in result from a17f0fc with the same patch-id. Item 3's cut-JSON unrecorded case stays the accepted gap, named in the PR's Known gaps.

## PR description (forge body at head 767a897fc3ffb2aa0466b9dacb1e89421b340e3f, `gh pr view 272`)
Matches the diff (12 files, same patch-id). Known gaps names the cut-JSON gap and the Windows-only local run. Review box `approved, carried from 2d2de57`: log note `r1 inspector approved at 2d2de5769f10...` supports it. `Verified at 767a897, carried from a17f0fc` and `CI green at 767a897` boxes are consistent with the gate and the CI note. Renders cleanly; no images. PASS.

## Earlier judgment at a17f0fc (previous pass, VERIFIED)
Unchanged patch; its claims are carried above for the reason given (same patch-id, scenario rerun green at the new head).

VERIFIED
