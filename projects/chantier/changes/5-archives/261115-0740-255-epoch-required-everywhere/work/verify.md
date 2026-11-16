# Verify CR-255

Head: bc46f8cdbbd101da714ed1d3350c4b85fa6ef264

Rerun at this head with the earlier evidence script (evidence/verify_run.py, scratch project in %TEMP%\verify255b, CLI from the worktree). The long gate and CI were not rerun, as told.

1. SHA bc46f8c, `chantier take CR-102` (no --epoch): exit 2, `error: take CR-102 --epoch <n>: the steering session's command; <n> is your number as Foreman of the batch (Foreman n°<n>)`; batch.json and events.jsonl hashes before = after (script RESULT files-identical=True, no "epoch" word outside the flag).
2. SHA bc46f8c, each without --epoch: `pause`, `agents set CR-101 <id>|-`, `agents set stack <id>`, `order done O-1`, `foreman transcript <uuid>`, `foreman set <session>`, `status --stop-heartbeat`, `take stack` all exit 2 with their own `--epoch <n>` form, files identical. Plain `status` exit 0; `status --refresh` without --epoch is not refused (exit 4 only from the scratch batch's missing Foreman transcript).
3. SHA bc46f8c, stale wording after Foreman n°2 claimed: `status --refresh --epoch 1` and `take CR-102 --epoch 1` exit 3 `stale Foreman: Foreman n°1 of batch-01, which is now at Foreman n°2; stop now`; `foreman set local_f1b --epoch 1` exit 3 `Foreman n°1 of batch-01 cannot be claimed: the batch is at Foreman n°2; stop now`.

Not checked: PR body, cards text, scenario diff.
