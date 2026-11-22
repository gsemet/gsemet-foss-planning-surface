# Verify CR-451

Head: 0ae00e3aac3779c8e2dac8a14a3f2a008234da3a

All claims judged at 0ae00e3 (pushed head of PR 423, verified equal to `git rev-parse HEAD` and `gh pr view 423` headRefOid), on Windows 11.

1. P1-P5 and W1-W2 pass at 0ae00e3.
   Command (cli dir, worktree src first on PYTHONPATH): `PYTHONPATH=$PWD/src uv run --no-sync --project <main> python -m pytest tests/test_triage_moves.py tests/test_startup_manifest.py -v -rs`
   Output: test_triage_moves.py 9 passed (brief hold, lasting hold [triage][abandon], other errors x2, cards, w1, w2 not skipped); with test_startup_manifest.py "47 passed in 3.20s". (A first run without PYTHONPATH imported the main checkout's older source and failed: a harness artefact, not the CR.)
2. Real lasting hold, CLI, scratch git repo under work/scratch (removed). A hidden PowerShell child with working directory inside `1-inbox/scratch-probe-request`; `chantier triage 1-inbox/scratch-probe-request --priority P2` (worktree src):
   Output: `error: cannot move CR folder ...1-inbox\scratch-probe-request to ...2-backlog\P2\scratch-probe-request: refused for 10 s, the folder is likely held; nothing moved. On Windows a folder cannot move while a process holds it: a shell or a program whose working directory is inside it, or a file of it open in an editor or a viewer. Leave it (cd elsewhere, close the file) and run the command again; the board need not stop. ([WinError 32] ...)` ; `exit=4 elapsed=11s`; folder still in inbox (Test-Path True).
   After the child was stopped, the same command: `triaged .agents/changes/2-backlog/P2/scratch-probe-request (P2)`, exit 0.
3. Diff matches spec (read `git diff main...HEAD`): retry_held + HELD_WAIT_S in core/files.py, FolderStore.move uses it and builds the text from HELD_WAIT_S, remove keeps retry, startup-core.md paragraph and concepts.md pointer.
4. PR description as posted (gh pr view 423): renders, Summary/Deliverables/Changes match the diff, no images, Known gaps names W3. Its Test plan still holds `<sha7>` placeholders and unchecked boxes: the Driver fills them (Verified, Review box per `log`: "r2 approved at d8594e5, committed as 0ae00e3") at hand-off; not claimed as fact now.
5. Gate: `log` shows `gate result=pass head=0ae00e3aac3779c8e2dac8a14a3f2a008234da3a command=just scenario`; CI note: all 5 checks pass.
6. W3 with a running board: UNVERIFIED. My card forbids a background shell, so `chantier board` could not be kept running for the check; the board's own handle past 10 s was not observed. Only the CLI half (claim 2) was run. Keep W3 in Known gaps.

VERIFIED
