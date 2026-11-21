# Answers

No grill held: the user delegated tonight's spec questions to a Fable advisor ("plus de question", 2026-11-21).

store-reads-Q1 (2026-11-21, Fable advisor): **What this CR takes: everything the board, `status` and the hub reach, plus the run-time proof (a).** 107 calls, CR-419's size, so it fits 3 rounds, and it is what the proof needs to pass.
store-reads-Q2 (2026-11-21, Fable advisor): **The 20 `commands/` modules left: nothing is filed (b).** The surface server reaches none of them and moving them has no measured need; the PR's Known gaps names the 20 modules and their 60 calls.
store-reads-Q3 (2026-11-21, Fable advisor): **The configuration stays read by `playbook/`, directly (a).** Its files are outside the store's root (CR-402's answer 2); the store keeps only the project file's write.
store-reads-Q4 (2026-11-21, Fable advisor): **The gate's held lock files: the holder's text stays a direct read, exempt by name in both tests (a).** It is an OS lock, not the plan's content; the listing and the `stat` go through the store.
store-reads-Q5 (2026-11-21, Fable advisor): **The run-time proof: a pytest module in `just test`, in-process, on a prepared surface (a).** AGENTS.md puts structure checks on a prepared state in `tests/`; the proof observes three calls, not a batch.
Destination (2026-11-21, Fable advisor): joins batch-30 tonight, at most 3 rounds, no `depends.json` (shared files only); CR-447 waits for it.

Spec final (2026-11-21, the Chief of Staff): v2, store-reads-Q1..Q5 applied (Fable advisor), no further critic (the v2 adds no behaviour over the critic-read v1); destination batch-30, no depends.json; CR-447 waits for it.
