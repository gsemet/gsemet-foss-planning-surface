Short name: `index-links`

# Answers

## 2026-11-25: facts checked before the grill

- Reproduced on `origin/main` 2f09cef (0.18.1), Python 3.13: with `api/index.md` present and no
  summary yet for `api` in the root `index.md`, `okf-schema index` writes
  `- [api](./api/) — [Health Check](health-check.md)  [API Endpoint]` in the root.
- Cause: `_get_subdir_description` returns the first non-heading line of the subdirectory's
  `index.md`, list entries included (`src/okf_schema/api.py:1013`). So `okf-schema` writes these
  summaries itself.
- The copied text is then preserved as an authored summary; the next run also removes its trailing
  `[API Endpoint]`, so the output changes between two runs with no source change.
- A fresh bundle gets "Auto-generated index for concepts in `api`." only because the root is
  written before `api/index.md` exists.
- `validate` checks no link in any `index.md` (`validate_index` only raises E3,
  `src/okf_schema/validator.py:863`).
- W2 today reports `a.md#part` and `#top` as broken links (anchors are not stripped,
  `src/okf_schema/_internal/utils.py:38`).
- An existing index entry wins over the concept's frontmatter description: after the description
  changes, `index` keeps the old text. OKF 0.2 section 8 says entries SHOULD carry the concept's
  description.
- Scan of the 27 `index.md` under `examples/`, `requirements/`, `src/`, `docs/`, `skills/`: one
  broken link, in `docs/source/index.md` (Sphinx, not a bundle).
