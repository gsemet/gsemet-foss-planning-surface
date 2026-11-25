Short name: `show-names`

# Answers

## 2026-11-25: facts checked before the grill

- Reproduced on `origin/main` 2f09cef (0.18.1), Python 3.13: `show api/health-check` answers
  "Concept not found"; `show api/health-check.md` works.
- Same run: `show api` (a directory) ends in a `PermissionError` traceback (Windows).
- From the code, not run: `show_bundle` joins `bundle / concept_path` with no containment check,
  so a `../` path outside the bundle is read (`src/okf_schema/api.py:392`).
- `backlinks_bundle` appends `.md` to a target that does not end with it
  (`src/okf_schema/api.py:841`).
