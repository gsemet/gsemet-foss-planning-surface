# Intent

The user follows a batch through the Chief of Staff's messages, often on a phone. Today each report
has its own shape. They want the same progress table and the same completion table every time,
without a rigid script: fixed columns, free text around them.

The spend in a report must also be current: `status` and `STATUS.md` showed $0.43 and $0.08 while
`cost` gave $1.97 and $1.58. `spent_usd` is only recorded by `status --refresh`, so at each
heartbeat; `status --refresh` from the Chief of Staff, with no epoch, brought it up to date
(proved on batch 05, 2026-11-06).
