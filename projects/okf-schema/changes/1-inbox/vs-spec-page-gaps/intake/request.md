# docs: the vs-spec page omits stricter rules and misquotes OKF 0.2

From the OKF 0.2 compliance check of `origin/main` 2f09cef (0.18.1), 2026-11-25. Filed on the
user's yes, not grilled. Spec text: `skills/okf-schema/references/okf-v0.2.md` (the upstream text).

`docs/source/reference/okf-schema-vs-spec.md` lists schema validation, `additionalProperties`,
link style and `links`/`backlinks` only. These rules are stricter than the spec and not listed
(observed):
- E5: `extra_key: [[a, b], c]`, a producer-defined key, fails on "nested list structures in
  frontmatter" (`validator.py:813`).
- E3: a `log.md` with frontmatter fails (`validator.py:988`); the spec forbids frontmatter in
  `index.md` only (section 8).
- E6 (nested `log.md`) and E7 (`generated` without `at`) also differ; each has its own inbox item.

OKF 0.2 section 4.1 says consumers "MUST NOT reject documents with unrecognized fields", and
section 11 says they should treat all other constraints as soft guidance. `AGENTS.md` allows
okf-schema to be stricter than the spec, so these are project choices once declared.

The same page misquotes the spec: it writes "SHOULD NOT reject" where 0.2 section 4.1 says "MUST
NOT reject", and cites cross-linking as section 5 (in 0.2 it is section 6).

The check's suggested fix: add the rules to that page and correct the quote and the section number.
