# Answers

No user question: the intake names the whole change (`just check` runs `ruff check` over
`scripts/`), and the Chief of Staff sent it to the spec-writer with "the user asks no questions".

## Settled by the spec-writer (2026-11-18)

None of these touches a user-visible behaviour; each keeps every script doing what it does today.

- S1. The findings are fixed in the code, not silenced: no rule is dropped from `pyproject.toml`,
  no `per-file-ignores` for `scripts/`, no new `# noqa`. The scripts meet the same rule set as
  `skills/`.
- S2. One finding is removed by deleting a `# noqa`: `copilot_models.py`'s `# noqa: S310` names a
  rule the project does not enable (RUF100).
- S3. `release_notes.py`'s `zip(*[iter(...)] * 2)` gets an explicit `strict=False` (B905), which
  keeps today's pairing exactly (an odd trailing item is dropped as now); `strict=True` would change
  what the check raises on a malformed thread.
- S4. `version.py`'s `subprocess.run` for `check-tag` gets an explicit `check=False` (PLW1510): a
  failing `git log` keeps leading to the "expected release: v..." message, as today.
- S5. `version.py`'s `main` gets to six returns at most (the limit) by moving the `check-tag` branch into its own
  function; the messages and exit codes stay.
- S6. `CONTRIBUTING.md`, "Code standards", says that `scripts/` meets the **Style** target too
  (`ruff format` and `ruff check` clean), so the guide stays true; the other targets (file and
  function size tests, `mypy --strict`) stay for `skills/` only.
- S7. Out of scope: `mypy` over `scripts/`, and `ruff check` over any other folder (`scenario/`,
  `evals/`, `tests/`, `hooks/`).
