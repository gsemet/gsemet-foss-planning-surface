# uv sync blocked by other projects' chantier.exe on the same .venv

From the batch-29 retro (kept point 3): other projects running chantier from the chantier checkout's `.venv` hold `chantier.exe` open, so `uv sync` fails on Windows. Intent: a sync is never blocked by, and never kills, another project's chantier process.
