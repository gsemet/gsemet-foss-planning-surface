# `order merged` stops the CR's gate before it moves the folder

Filed 2026-11-15 by the Chief of Staff from batch-18's retro (kept by the retro critic and by a Fable review), on the user's word "lance le tout dans le batch actuel".

Problem: `_finish_stopped` in gate.py raises FileNotFoundError when `order merged` moves the CR's folder while its long gate runs (proved in batch-18 CR-266's work/diagnosis.md; it cost a gate rerun and a debugger, and the scenario's gates unit E4 fails now and then). The same ordering caused CR-253's WinError 32 (os error 32) when its folder moved while a process still held it.

Fix: `order merged` stops the CR's running gate and waits for that process to end before it moves the folder. No try/except in `_finish_stopped`, and no log outside the CR's folder (a CR's folder stays self-contained, CR-257). Host- and forge-neutral, POSIX and Windows.

Order in the batch: first (small, and it makes the scenario trustworthy).
