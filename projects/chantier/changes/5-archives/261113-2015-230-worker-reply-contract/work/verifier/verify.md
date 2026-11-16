Head: 8d9efdb26290ebff7f50da8b960bc11c9507a683

All claims judged at 8d9efdb26290ebff7f50da8b960bc11c9507a683. Command for lines: git grep -n -e "reply out of format" -e "infra re-run" -e "blocked infra:" -e "(conflict)" -e "fast gate" HEAD -- skills/chantier/references

1. Diff scope. Command: git diff --stat origin/main...HEAD
   Output: concepts.md 2 +-, driver.md 52, worker.md 12; 3 files changed, 59 insertions, 7 deletions. Only the three cards. PASS.
2. S1 driver.md bullet after the children bullet (lines 37-58): per-role formats, failed worker, note "restart: reply out of format", D2 second failure, no resume by message. git grep: driver.md:37, :54, :58. PASS.
3. S2 driver.md remote-failure bullet before Push: driver.md:128 `infra re-run: <command>: <exact error>`, :129 `blocked infra:`; D3 ls-remote check, 4xx refusals excluded, CI and Release rules kept. PASS.
4. S3 worker.md Conflict resolver: worker.md:153-155 conflicts.md holds fast gate command and result; no-gate case one line; missing line is out of format; no-BOM check kept. PASS.
5. S4 worker.md shared paragraph (lines 21-23 "failed worker, which the Driver starts again rather than reads") and Verifier (refused/absent/unchanged claim needs command and output). PASS.
6. S5 driver.md:354 `move <old7>..<new7> (conflict) inspector approved at <head>`; conflict-resolver rebase always triggers Inspector; several rebases inspected once. PASS.
7. S6 concepts.md:322 `reply out of format: <what is missing>` added to restart causes; rule 3 unchanged. PASS.
8. No CLI/hook/type/agent file in diff (claim 1). PASS.

Verdict: VERIFIED. Minor note: concepts.md:322 line is longer than the wrapped style; harmless.
