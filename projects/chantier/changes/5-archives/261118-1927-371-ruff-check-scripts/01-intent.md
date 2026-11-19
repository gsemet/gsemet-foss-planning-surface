# Intent: `just check` runs ruff's lint rules on `scripts/`

## The request

`just check` should run `ruff check` (the lint rules) on `scripts/`, not only the format check.
It was left out of `just-check-scripts-format` (CR-308, merged 2026-11-17, PR #261), which added
only `ruff format --check` over `scripts`.

## Analysis

- Today the `lint` recipe of `justfile` runs `uvx ruff@0.17.5 format --check skills scripts` and
  `uvx ruff@0.17.5 check skills`: the lint rules of the root `pyproject.toml` do not reach the five
  repository tooling scripts (`copilot_models.py`, `docs_screenshots.py`, `mod.py`,
  `release_notes.py`, `version.py`).
- The intake counted 15 findings before CR-308's formatting. At main `3a9afc2c` (2026-11-18),
  `uvx ruff@0.17.5 check scripts` reports 9, of the same eight rules (E501 x2, RUF005, PLR2004,
  PLC0207, PLW1510, PLR0911, RUF100, B905).
- The change is a check of the repository's own tooling: it changes no behaviour of chantier, of
  its CLI, cards or board. The scripts must keep doing what they do.
