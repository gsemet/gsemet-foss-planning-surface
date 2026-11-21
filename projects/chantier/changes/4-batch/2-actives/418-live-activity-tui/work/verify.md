# Verify CR-418

Head: 58df3be33df15c12c78f272e8d846d61d52c8d19

Claims at 58df3be:
- The move since a391c1e is a rebase onto CR-422. `git range-diff a391c1eb~3...a391c1eb HEAD~3...HEAD`: the live commit shows `!` with only context hunks adapted (crs.py import of `stack_words`, test_leases.py imports `stack_world`); the new top commit `58df3be test(leases): fold two lines` is a test-only trim. Live source files (clients/tui/*, commands/live.py, declare/live.py, docs) are unchanged in substance. Judged again: the tests below.
- Live and lease tests at the head (`cd skills/chantier/scripts/cli; uv run --no-sync --project ../../../.. pytest tests/test_live_link.py tests/test_live_model.py tests/test_leases.py -q`): `47 passed in 22.01s` (ws, http, --once, lease time left).
- evidence/live-once.txt: carried from a391c1e (captured at 800bd85; no live source file changed by the rebase, per range-diff above); contains no user name (`grep -ci gaeta` -> 0 in the PR body and the capture).
- Review box: log has `r2 approved at 4ed0d56, committed as 800bd85b...`, matching `Review: approved at 800bd85`.
- PR description as posted (`gh pr view 392 --json body`): sections present, consistent with the diff (28 files, live client, three API fields, docs), Known gaps names the one gap. FAILED: its boxes `Verified at a391c1e` and `CI green at a391c1e` name the pre-rebase SHA, not the head 58df3be and with no `carried from` reason.
- CI at 58df3be (`gh pr view 392 --json statusCheckRollup`): ubuntu `just check` SUCCESS, `eval-dry-run` SUCCESS; macos, windows, scenario not yet complete. Not a proof.

NOT VERIFIED
