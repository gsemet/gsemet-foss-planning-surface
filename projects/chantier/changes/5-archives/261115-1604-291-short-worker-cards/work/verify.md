# Verify CR-291

Head: 307d8a8c23c38778cbd5fe3d2fa1cfef29e422ca

All claims judged at 307d8a8c23c38778cbd5fe3d2fa1cfef29e422ca.

1. Size. `git show origin/main:.../worker.md | wc -c` = 16873, concepts.md = 52724 (LF blobs; 69,597; the PR's 70,444 is the same two files measured CRLF in the main checkout with autocrlf: `wc -c` there = 17123 + 53321). After (`wc -c`): coder 4232, verifier 10333, inspector 5290, investigator 3482, debugger 3353, conflict-resolver 3544, demo-explorer 3234, review-step 3878. Each smaller. Minor: the PR's before is CRLF bytes, the after LF bytes.
2. Nothing lost. HEAD~1 == origin/main for worker.md (16873 bytes); `git log d6836e4~30..d6836e4 -- worker.md` shows only 857506d and 37c4860, both already in the base text. A line-by-line script of old worker.md sections against the new cards: Investigator, Debugger 0 missing; Coder, Verifier, Conflict resolver, Demo explorer, Inspector: only reworded lines (rule 9 / BOM inlined into ground rules, role-line intro moved to the card head, "extra review steps do not audit the body" moved to review-step.md "You do not audit the PR body"). Preamble parts (rules first, worktree, writes, notes, no commit, no sleep, no stash, scratch planning folder, reply cap, failed-worker rule) read in the coder/verifier/inspector/demo-explorer cards; concepts rules 0,2,5,7,8,9 restated.
3. `git grep -n "worker\.md"` at head: only evals/results/claude-full-2026-11-04.md:96. PASS.
4. `worker_prompt_lines("claude-code", ...)` prints for each role e.g. `Read .../references/verifier.md;` and `the project's rules rank above it: ...`; no concepts.md. `pytest test_cli_runs.py test_plugin_files.py`: 54 passed.
5. PR 244 body matches the diff (36 files: 14 agent files, 8 cards, worker.md removed, plugin_files.py, facts.py, tests, links). Known gaps names the unproved cost effect.

VERIFIED

## Description-only pass (PR 244 body, head 307d8a8c23c38778cbd5fe3d2fa1cfef29e422ca)

Head: 307d8a8c23c38778cbd5fe3d2fa1cfef29e422ca

Judged at 307d8a8: body sizes (69,597 before; 8 after sizes) match `wc -c` of claim 1 above and of the files at HEAD; Changes/Deliverables match the 36-file `git diff --name-status main...HEAD`; Known gaps names the cost effect; Test plan boxes backed by claims 1-5, the gate log (see command output in the pass), `gh pr checks 244`, and the Driver note "r2 approved at d6836e4, committed as 307d8a8" (`chantier log`). VERIFIED.
