# Retro

## 2026-11-16, batch-21: CR-296 (PR 247)

- [chantier] A batch opened and stopped on another machine cannot be taken over here: batch-20's batch.json, events.jsonl and brief.md were local and unpublished, `pause` refused it because CR-296 was unmerged though nothing ran, so its record stays `running` in 5-archives/batches, the CR had to go back to 3-ready into a new batch-21, and the Driver pushed one head to two branches (batch-20's PR branch and the batch-21 name the CLI expects): a takeover path (`pause` accepts a batch whose remaining CRs are stopped or blocked by the user; what a resume needs is published; a takeover closes or supersedes the old batch's record and lets the CR keep its existing PR branch).
