Head: e8d53acdc80d021eedfe7dabf396252128aef937

Verdict: VERIFIED (judged at e8d53ac)

Claims (all at e8d53ac, worktree clean, base = origin/main a94085d):

1. Tests: `uv run --no-sync pytest tests/test_ready_line.py tests/test_reload_rules.py tests/test_startup_manifest.py -q -s` -> `96 passed in 2.05s`. All startup/reload bytes <= 12544 on both hosts.
2. Byte figures (fallback form, shipped on purpose): chief-of-staff reload 12529 (claude) / 12535 (copilot); foreman reload 9387 / 9568. The same command at a detached worktree of origin/main a94085d prints the identical four figures: unchanged, as the PR says. Room 15/9 bytes < the manifest line, so the fallback is justified; no `reload:rules` action in startup-manifest.json (checked by reading it), `rules:` pointer on `batch:` line, foreman.md opening names it.
3. Real `status` (worktree code, live batch-31): second line `batch: shape parallel; slots 4/4; steering Foreman; rounds 3; budget $88.65 of $100; long gate owed: none; merges: the user; under the grant: the release/fix PR (steering session); rules: .../references/reload-rules.md (reread after a compaction)`; first line unchanged shape; `handed back: 🟢 ready to merge CR-475 release-notes-... https://github.com/gsemet/chantier/pull/451 | long gate CR-475 at 6773a4d: exempt: ...`.
4. Scenario step present: scenario/run_scenario.py checks a `handed back: ` line with CR-101 and pr101, and `batch: shape ` with `merges: the user` (diff read); positional checks moved from line 2 to 3 consistently. CI `just scenario (ubuntu-latest)` pass at the head (gh pr checks 452): also check macos/ubuntu/windows, eval-dry-run pass.
5. File sizes: batch_status.py 362, ready_line.py 128, test_ready_line.py 242, test_reload_rules.py 79 lines (all <= 400); helpers moved to batch_status_orders.py.
6. Cards: reload-rules.md (4 bullets, ~2 KB), chief-of-staff-merge.md (words to the user, plain-ask bullet), status-layout.md bullet, CONTRIBUTING.md list: match spec section 3 (diff read).
7. PR description (work/pr-body.md): consistent with diff, Known gaps present (Copilot unproved, no own-gate wording, long gate pending locally), no images, English. Review box carried from a94085d; not independently checked against `log` beyond the Driver's wording.

Not run: the local full long gate (queued; per the brief); the Windows local scenario run is owed by AGENTS.md before ready to merge. No visual evidence due (no UI); no before/after images.
