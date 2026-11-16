# Verify CR-255

Head: bc46f8cdbbd101da714ed1d3350c4b85fa6ef264 (worktree HEAD, pushed; PR 213)

Method: `evidence/verify_run.py` builds a scenario-like scratch project outside the repo (`%TEMP%\verify255`), opens a 2-CR batch (batch-01), claims Foreman n°1, takes CR-101, then runs each command. Full log: `evidence/verify-run.txt`. CLI from the worktree at the head SHA above. The long gate and CI were not rerun, as told.

## 1. `take <cr>` without `--epoch`
SHA bc46f8c. Command: `chantier take CR-102`
Output: exit 2, `error: take CR-102 --epoch <n>: the steering session's command; <n> is your number as Foreman of the batch (Foreman n°<n>)`
batch.json sha256 before = after = 4ede5e40e000fe76942a72ff112f139eced3016d2890d676a0f7317651ddada9
events.jsonl sha256 before = after = c8f6b11b799d6c74a1a6f469c5c51aecc03ee826a0252a2a25e9695d74b4cb60

## 2. Other steering commands without `--epoch` (SHA bc46f8c)
Each exited 2, stderr named the command's own `--epoch <n>` form, no "epoch" outside the flag, batch.json and events.jsonl hashes unchanged:
- `pause`
- `agents set CR-101 -`, `agents set CR-101 agent1`, `agents set stack agent1`
- `order done O-1`
- `foreman transcript uuid-x`
- `foreman set local_f9`
- `status --stop-heartbeat`
- `take stack`

Exceptions:
- `status` (plain): exit 0.
- `status --refresh` (no --epoch): no refusal; the heartbeat stays `never`. It exited 4 only because the scratch batch has no Foreman transcript file (`spend not updated: Foreman transcript not found`). That is a scratch artifact, not an epoch refusal.
- `order merged CR-102` (no --epoch): exit 0, `[chief-of-staff->foreman] order O-1: merged CR-102`.

## 3. Stale refusal wording (SHA bc46f8c)
After `foreman set local_f2 --epoch 2`:
- `status --refresh --epoch 1` and `take CR-102 --epoch 1`: exit 3, `stale Foreman: Foreman n°1 of batch-01, which is now at Foreman n°2; stop now`
- `foreman set local_f1b --epoch 1`: exit 3, `Foreman n°1 of batch-01 cannot be claimed: the batch is at Foreman n°2; stop now`

Not checked: the PR body (work/pr-body.md), the cards' text and the scenario diff. Only the command claims were run.
