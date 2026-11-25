Short name: `show-raw`

# Answers

## 2026-11-25: facts checked before the grill

- Reproduced on `origin/main` 2f09cef (0.18.1), Python 3.13: `show` re-serializes the
  frontmatter (flow mappings and lists become block style, a datetime is rewritten and quoted,
  YAML comments are dropped) and prints `trust: <tier>` on stdout between the closing `---` and
  the body (`src/okf_schema/cli.py:766`), plus `stale: true` when stale.
- A file with no frontmatter is shown with an invented block `---`, `{}`, `---`.
- A file whose frontmatter is not valid YAML is shown with `{}`: the stored frontmatter does not
  appear at all, exit code 0, nothing on stderr.
- No test, tutorial or skill reads the `trust:` line of `show` (searched in `tests/`, `docs/`,
  `skills/`, `examples/`, `scripts/`). `SwRS-OKFSCHEMA-CORE-006` names `stale: true` in a
  scenario; `SwRS-OKFSCHEMA-CORE-005` covers `show`.
- The Python API `show_bundle` returns `ConceptDetail(frontmatter, body, trust_tier, stale)`,
  without the stored text.
- CR 56 changes the same function and command; this item stacks on it.
