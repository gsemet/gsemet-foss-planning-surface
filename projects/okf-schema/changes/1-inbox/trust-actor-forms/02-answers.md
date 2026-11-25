Short name: `trust-forms`

# Answers

## 2026-11-25: facts from the OKF 0.2 compliance check (code on `origin/main` 2f09cef, 0.18.1)

- `skills/okf-schema/references/okf-v0.2.md` is the upstream specification text, verbatim.
- `_ACTOR_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*:.+$")` requires a colon
  (`src/okf_schema/validator.py:65`); `_derive_trust_tier` skips every other actor
  (`validator.py:378-379`), so `reference_agent/gemini-2.5-pro` gives `unverified` and W10
  (`validator.py:616-624`).
- The W10 message lacks the `f` prefix on a part holding `[{i}]` (`validator.py:622`).
- OKF 0.2 sections 5.3 and 7: any actor not starting with `human:` is machine-confirmed; the
  forms are `<producer>/<version>`, `human:<id>` and `process:<id>`.
- `docs/source/reference/validation-codes.md:526-548` and
  `src/okf_schema/data/kb/_schema/Base.schema.yaml:32` document another form (`bot:ci`).

## 2026-11-25: user's decisions

1. show-raw-Q12, asked while grilling CR 58: **Fix the trust tier in the `trust` command's CR?**
   "B. CR séparé": a separate fix, stacked before CR 58 in the same batch. The options shown
   described the fix as: every `by` that does not start with `human:` counts as machine; W10
   accepts the forms of the specification; the documentation is corrected (the words of option
   A, kept for the separate CR).

The preview of option A shown to the user: `alice` is read machine-confirmed and warned W10.

Destination: running batch batch-01.

Spec critic: yes, it changes what `validate` reports and the trust tier.
