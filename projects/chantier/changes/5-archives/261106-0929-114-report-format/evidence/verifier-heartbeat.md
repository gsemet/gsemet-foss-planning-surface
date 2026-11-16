# CR-114 verifier gap 2: scratch repo p2 (remote git@gitlab.example.com), worktree CLI at 4959358
$ chantier foreman transcript aaaa-1111 --batch 1 --epoch 1
transcript aaaa-1111
[exit 0]
-- 1. set a real heartbeat (status --refresh WITH epoch 1)
$ chantier status --refresh --batch 1 --epoch 1
batch-01 open parallel live 0/4 queued 2 foreman 1 e1 heartbeat 0 min spent $3.00
CR-101 queued r0/3 -
CR-102 queued r0/3 -
spent $3.00
[exit 0]
heartbeat in batch.json: heartbeat=2026-11-06T09:26:24Z spent_usd=3.0 epoch=1
-- 2. status --refresh with NO epoch
$ chantier status --refresh --batch 1
batch-01 open parallel live 0/4 queued 2 foreman 1 e1 heartbeat 0 min spent $3.00
CR-101 queued r0/3 -
CR-102 queued r0/3 -
spent $3.00
[exit 0]
heartbeat in batch.json: heartbeat=2026-11-06T09:26:24Z spent_usd=3.0 epoch=1
-- 3. compare
heartbeat before=2026-11-06T09:26:24Z after=2026-11-06T09:26:24Z unchanged=True
-- 4. the Foreman spends more (one more 1M-input line appended to the fake transcript), then refresh with NO epoch
batch.json: heartbeat=2026-11-06T09:26:24Z spent_usd=3.0
$ chantier status --refresh --batch 1
batch-01 open parallel live 0/4 queued 2 foreman 1 e1 heartbeat 0 min spent $5.00
CR-101 queued r0/3 -
CR-102 queued r0/3 -
spent $5.00
[exit 0]
batch.json: heartbeat=2026-11-06T09:26:24Z spent_usd=5.0
-- 5. exit codes with a stale epoch still refused? (epoch 0)
$ chantier status --refresh --batch 1 --epoch 0
[exit 3]
batch.json: heartbeat=2026-11-06T09:26:24Z spent_usd=5.0
