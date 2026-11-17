# A stopped Driver resumes without the user's word

Three Drivers (CR-299, CR-303, CR-304) stopped at once around a compaction of the steering session; `SendMessage` refused to resume them ("stopped and won't be resumed … only launch a new agent if the user explicitly asks"), so the batch waited on the user. Long-term fix: document `take <cr> --note "resume: <cause>"` as the steering session's own path after an outside stop, covered by the batch's go, and have the heartbeat detect a Driver recorded but stopped.

From the retro of batch-22 (2026-11-17, kept by the retro critic; record: 5-archives/batches/batch-22.md). The user asked to treat every kept point in the next batch. Priority: P1, the user's word.
