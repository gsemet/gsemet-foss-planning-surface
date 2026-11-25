## Description

A concept verified by an actor written as OKF 0.2 allows, such as
`reference_agent/gemini-2.5-pro`, was read as `unverified` and warned W10, because every actor
needed a colon. The trust tier now follows the specification (sections 5.3 and 7): every
non-empty actor that is not `human:<id>` counts as machine.

Before is `a371f73` on `main`, after is `373fded`.

| `verified[].by` | Trust tier before | Trust tier after | W10 after |
|---|---|---|---|
| `reference_agent/gemini-2.5-pro`, `langchain.agents/0.3` | unverified | machine-confirmed | no |
| `process:nightly-check`, `bot:okf-schema` | machine-confirmed | machine-confirmed | no |
| `acme.ci:nightly` | unverified | machine-confirmed | no |
| `alice` | unverified | machine-confirmed | yes |
| `human:` (no identifier) | unverified | machine-confirmed | yes |
| `human:alice` | human-reviewed | human-reviewed | no |
| not a string, or empty | unverified | unverified | W10 or E9, as before |

What changes:

- W10 accepts `<producer>/<version>` and `<prefix>:<identifier>`, with a dot allowed in the
  producer and the prefix. Its message lists the accepted forms and now prints the entry index
  everywhere (it showed a literal `{i}`).
- The validation code reference, the how-to table, the packaged skills and the `okfkb`
  scaffold schema teach the OKF 0.2 forms instead of `bot:ci`. Existing knowledge bases keep
  their own copy of the schema.
- Requirement `SwRS-OKFSCHEMA-CORE-006` gains scenario S5, with tests and a feature map row.
- `CHANGELOG.md` gains the entry for this fix and the missing `v0.18.1` heading, both generated
  from the commit history by `just changelog`, a `just preflight` step.

Unchanged: `generated.by` and `sources[].author` are still not checked, `okfkb` still writes
`bot:okf-schema`, and the `human:` match stays case-sensitive.

### Product surfaces

| Surface | Change |
|---|---|
| Runtime | `src/okf_schema/validator.py` |
| Human documentation | validation code reference, standalone-file how-to, feature and evidence map. `README.md` is unaffected: it holds no trust tier or W10 text. |
| Agent skills | packaged skills `okf-schema` (W10 row) and `okfkb-record-findings` (actor example). The bundled OKF 0.2 reference is the upstream text, left verbatim. |
| Scaffold guidance | `src/okf_schema/data/kb/_schema/Base.schema.yaml`. The packaged knowledge base guideline already uses `human:alice`. |
| Examples | `examples/okfkb-hw-knowledge-base/_schema/Base.schema.yaml`, edited by hand because no recipe refreshes it. Their `bot:okf-schema` actors stay valid. |
| Requirements | `SwRS-OKFSCHEMA-CORE-006` S5 and the requirements log. |
| Verification and packaging | new tests, and two existing trust tier tests updated (one renamed with its expected tier changed, one parametrized with a stricter assertion). `pyproject.toml`, `justfile` and CI are unaffected: no file, dependency, command or job is added or moved. |

### Example command

For a file whose frontmatter has
`verified: [{by: reference_agent/gemini-2.5-pro, at: "2024-01-02T00:00:00Z"}]`, with a
`concept.schema.json` in the schemas directory:

```
uv run -- okf-schema validate-md --input c.md --schemas-dir <dir> --strict
```

### Validation results

- Example command at `373fded`: exit 0, no warning. With `by: alice`: exit 1, one W10 naming
  `verified entry [0]` twice. `show_bundle(...).trust_tier` is `machine-confirmed` for both.
- `just preflight` on Windows, run on these same files before the rebase onto `main`: pass. 1153
  passed, 12 skipped, coverage 95.55%, Sphinx build succeeded with warnings as errors.
- `okfreq validate requirements --prose --check-links --project-root .` at `373fded`:
  36 requirements, 0 errors, 0 warnings.
- A first `just preflight` run on an earlier state of this branch, then based on `2f09cef`,
  failed 8 symbolic link tests because the host refused to create links (`WinError 1314`);
  `2f09cef` itself failed the same 8. Symbolic links are now allowed on that host.
- CI at `373fded`: the preflight jobs on Python 3.10 to 3.13 and the macOS and Windows jobs
  pass; the release tagging job is skipped, as it runs on pushes to `main` only.

Evidence status at `373fded`: marker linkage is defined for the requirement in `validator.py`
and for S5 in the tests; the marked tests were executed and passed on these same files before
the rebase onto `main`; no stakeholder approval is claimed, the requirement stays `proposed`.

### Decisions taken by the maintainer

- `<prefix>:<identifier>` stays accepted beside the specification's forms.
- An actor in no recognized form counts as machine-confirmed and is still warned.
- A dot is allowed in the producer and in the prefix.
- `human:` with no identifier counts as machine-confirmed and is still warned.

### Blast radius

2 of 3: the trust tier that `show` and the Python API report changes for actors that read as
`unverified` before. A plain revert restores the previous behaviour; no data is rewritten.

### Autonomous decisions

- The body of scenario S5 writes `{producer}/{version}` and `{prefix}:{identifier}` instead of
  angle brackets, because the requirement prose check reads those angle-bracket words as
  unfilled placeholders and warns. Docs, skills and messages keep the angle brackets.

### Known gaps

- `show_bundle` reports a different `trust_tier` for some actors without a
  `.. versionchanged::` note about this change in its docstring.
- `CHANGELOG.md` lacks the entry that `just changelog` generates for the `show` fix already
  merged into `main`.
- The skill row and the validation code reference say an unrecognized actor still counts as
  machine-confirmed; a `by` that is not a string (for example `42`) is warned W10 and does not
  count.

## Type of Change

- [x] Bug fix
- [ ] New feature
- [ ] Breaking change
- [x] Documentation update
- [ ] Refactoring

## Checklist

- [x] I have run `just preflight` and all checks pass
- [x] I have added tests that prove my fix is effective or my feature works
- [x] I have updated the documentation accordingly
- [x] My changes generate no new warnings

## Related Issues

None

🤖 Generated with [Claude Code](https://claude.com/claude-code)
