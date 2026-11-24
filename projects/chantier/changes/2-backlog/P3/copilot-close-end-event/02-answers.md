# Answers

## 2026-11-20, the batch after batch-29

The user: "on va mettre en P1 les taches du batch d apres", and chose one-read-interface, live-activity-tui and copilot-close-end-event for it. Moved to P1.

Short name: `copilot-end`

- copilot-end-Q1 (2026-11-24): **What to do with this CR.** A: demote to P3 until a real Copilot batch exists; `close` already reads leases since e461ffd2, and this machine has no events.jsonl to learn the events from. Read again then, only if the lease proved too slow.
