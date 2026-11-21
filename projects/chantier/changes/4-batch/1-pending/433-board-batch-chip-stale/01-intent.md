# A batch CR's card shows its batch folder, not its old 3-ready chip

Seen 2026-11-21 from the phone: the board's batch graph drew the chip `3-ready` on batch-30's CRs
(CR-425, CR-426, CR-430...), which were in `4-batch/2-actives` and `4-batch/1-pending` on disk. The
user read it as the CRs not having moved into the batch.

Intent: a CR in the batch never shows `3-ready` (or any backlog bucket) on its card. Its card shows
where it really is in the batch (`1-pending`, `2-actives`, `3-done`), in the place of the old
priority chip. The backlog views keep their priority chips. A small bug fix.
