# Answers

## 2026-11-20, the batch after batch-29

The user: "on va mettre en P1 les taches du batch d apres", and chose one-read-interface, live-activity-tui and copilot-close-end-event for it. Moved to P1.

- one-read-interface now waits on plan-store-interface (CR-402, the `store` package) and planning-server (CR-404), which edit the same files; its former dependency, CR-386, is archived.
