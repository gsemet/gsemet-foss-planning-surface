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

2. trust-forms-Q1: **Actor forms no longer warned W10.** "A. Spec + préfixe:id (recommandé)":
   the specification's forms are accepted and `prefix:id` stays accepted (the option's preview:
   `reference_agent/gemini-2.5-pro`, `process:nightly-check`, `human:alice` and `bot:okf-schema`
   pass; `alice` is warned W10).
3. trust-forms-Q2: **Tier of an actor in no recognized form** (`by: alice`). "A. machine
   (recommandé)": per the specification, every actor that does not start with `human:` counts as
   machine-confirmed; W10 is still shown.
4. trust-forms-Q3: **Grilled enough.** "A. Pour batch-01 (recommandé)": specify it for the
   running batch, stacked before the `trust` command (issue 58).

Destination: running batch batch-01.

Spec critic: yes, it changes what `validate` reports and the trust tier.

## 2026-11-25: after the spec critic, first pass (4 findings fixed without the user; 2 questions, the specification's)

5. trust-forms-Q4: **A dot in the producer** (`langchain.agents/0.3`). "A. Autoriser
   (recommandé)": no W10; the dot is allowed before `:` too (the option's description).
6. trust-forms-Q5: **`by: "human:"` with no identifier.** "A. Machine (recommandé)": it counts as
   machine-confirmed, not human-reviewed; W10 is still shown.
