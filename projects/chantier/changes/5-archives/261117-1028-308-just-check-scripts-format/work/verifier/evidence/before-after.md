Before (base 3df17b9 + justfile line): `just lint` fails, 3 files would be reformatted (scripts/mod.py, release_notes.py, version.py).
After (eb93500): `uvx ruff@0.17.5 format --check skills scripts` -> 221 files already formatted.
Reproduce: the commands above, from the repository root. Text only, no screenshots.
