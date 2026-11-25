## Description

A concept verified by an actor written as OKF 0.2 allows, such as
`reference_agent/gemini-2.5-pro`, was read as `unverified` and warned W10, because every actor
needed a colon. The trust tier now follows the specification (sections 5.3 and 7): every
non-empty actor that is not `human:<id>` counts as machine.

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

Unchanged: `generated.by` and `sources[].author` are still not checked, `okfkb` still writes
`bot:okf-schema`, and the `human:` match stays case-sensitive.

### Blast radius

2 of 3: the trust tier that `show` and the Python API report changes for actors that read as
`unverified` before. A plain revert restores the previous behaviour; no data is rewritten.

### Autonomous decisions

- The body of scenario S5 writes `{producer}/{version}` and `{prefix}:{identifier}` instead of
  angle brackets, because the requirement prose check reads those angle-bracket words as
  unfilled placeholders and warns. Docs, skills and messages keep the angle brackets.

### Known gaps

- `just preflight` has not passed yet.

## Type of Change

- [x] Bug fix
- [ ] New feature
- [ ] Breaking change
- [x] Documentation update
- [ ] Refactoring

## Checklist

- [ ] I have run `just preflight` and all checks pass
- [x] I have added tests that prove my fix is effective or my feature works
- [x] I have updated the documentation accordingly
- [ ] My changes generate no new warnings

## Related Issues

None
