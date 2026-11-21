# Answers

No grill held: the user delegated tonight's spec questions to a Fable advisor ("plus de question", 2026-11-21).

board-lock-Q1 (2026-11-21, Fable advisor): **Wait for a held folder on Windows: A, up to 10 s with a growing pause, then the refusal.** It covers a scan, an indexer or a read in flight, and stays well under the lifecycle lock's 30 s; B could hang a CLI command or a board request for half a minute; C leaves brief holds failing as today.
board-lock-Q2 (2026-11-21, Fable advisor): **Naming the holding process: A, no scan.** The message names the kinds of holder and what to do; a psutil scan is slow, misses a shell's working directory (the proven cause) unless `procs.py`'s rule is reversed, and is new Windows-only code with no measured need.
board-lock-Q3 (2026-11-21, Fable advisor): **Which moves get the wait and the refusal: A, every CR folder move, through `FolderStore.move`.** One place, one behaviour; a held folder blocks a batch or archive move exactly as it blocks triage.
board-lock-Q4 (2026-11-21, Fable advisor): **Card sentence on the shell's working directory: A, one sentence in `startup-core.md`.** The proven holder was an agent's own shell, and any role can park a shell in a CR folder.
Destination (2026-11-21, Fable advisor): batch-30; no batch-30 CR edits `store/folder.py` or `startup-core.md`, so no `depends.json`; W3 runs at a head that holds CR-429.
Spec final (2026-11-21, the Chief of Staff): v2, board-lock-Q1..Q4 applied, one critic pass (non-behavioural fixes only); destination batch-30, no depends.json.
