# uv sync blocked by other projects' chantier.exe on the same .venv

In batch-29, `uv sync --locked` of chantier's main checkout was blocked (os error 32 on Windows) by other projects' chantier.exe processes running from the same `.venv`: Studio's watcher, then a Studio gate, which the user had to approve killing mid-run. The same failure happened in batch-17, with another cause.

Wanted: a sync of chantier's checkout is never blocked by, and never kills, another project's chantier process.

Source: batch-29 retro, kept point 3 (the retro critic kept it).
