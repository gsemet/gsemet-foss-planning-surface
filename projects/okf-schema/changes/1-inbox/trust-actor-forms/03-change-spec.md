# Trust tier: count the actor forms allowed by OKF 0.2

A concept verified by `reference_agent/gemini-2.5-pro`, a form OKF 0.2 allows, must read as
`machine-confirmed` with no W10. The trust tier counts every actor that is not `human:<id>` as
machine. W10 accepts the specification's forms. The documentation, skills and scaffold
stop teaching `bot:ci` as the model.

## Goal

The user's words (intake): "a concept verified by an actor written as OKF 0.2 allows, such as
`reference_agent/gemini-2.5-pro`, is read as unverified and warned W10, because the tool requires
a colon in every actor. Per spec sections 5.3 and 7, any actor that does not start with `human:`
counts as machine-confirmed."

After this CR:

- `verified: {by: reference_agent/gemini-2.5-pro, at: ...}` gives the trust tier
  `machine-confirmed` and no W10.
- `process:nightly-check`, `human:alice` and `bot:okf-schema` raise no W10 either (Q1). Only an
  actor in no recognized form, such as `alice`, is warned W10.
- `alice` counts as machine-confirmed (Q2) and is still warned W10.
- A dot is allowed in the producer and in the prefix: `langchain.agents/0.3` raises no W10 (Q4).
- `human:<id>` gives `human-reviewed`, as today. `human:` with no identifier counts as
  machine-confirmed and is still warned W10 (Q5).

Code base: `origin/main` at 2f09cef (0.18.1). The line numbers below come from that commit.

**Stacking.** This CR lands before CR 58 `show-as-stored` (issue 58) in batch-01. CR 58 adds an
`okf-schema trust` command that prints the tier `_derive_trust_tier` returns. CR 58 builds on this
CR and does not touch the derivation. Both CRs edit
`requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-006.md`,
`requirements/tiers/log.md` and `docs/source/explanation/project-feature-coverage.md`. This CR
takes scenario `S5` of CORE-006, so CR 58 uses the next free number, as its specification
already allows. CR 58's log entry shares this CR's day heading. Its staleness row (line 31 of the
feature map) and this CR's new row sit on separate lines.

## Decisions carried from `02-answers.md`

- show-raw-Q12, "B. CR séparé": a separate fix, stacked before CR 58 in the same batch. Every
  `by` that does not start with `human:` counts as machine. W10 accepts the specification's
  forms. The documentation is corrected.
- trust-forms-Q1, "A. Spec + préfixe:id": the specification's forms `<producer>/<version>`,
  `human:<id>` and `process:<id>` are accepted, and any `<prefix>:<identifier>` stays accepted.
  `reference_agent/gemini-2.5-pro`, `process:nightly-check`, `human:alice` and `bot:okf-schema`
  raise no W10. `alice` is warned W10.
- trust-forms-Q2, "A. machine": an actor in no recognized form (`by: alice`) counts as
  machine-confirmed, and W10 is still shown.
- trust-forms-Q3: specify for batch-01, stacked before the `trust` command (issue 58).
- trust-forms-Q4, "A. Autoriser": a dot in the producer (`langchain.agents/0.3`) raises no W10.
  The dot is allowed before `:` too.
- trust-forms-Q5, "A. Machine": `by: "human:"` with no identifier counts as machine-confirmed, not
  human-reviewed. W10 is still shown.
- Fact recorded in the answers: the W10 message lacks the `f` prefix on the part holding `[{i}]`
  (`validator.py:622`). It is fixed here.

## Current behavior (checked on 2f09cef)

- `src/okf_schema/validator.py:64-65`:
  `_ACTOR_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*:.+$")`, commented
  "`<prefix>:<identifier>  e.g. human:alice, bot:ci`". It is used in exactly two places,
  lines 378 and 616. `generated.by` and `sources[].author` are not checked against it.
- `_derive_trust_tier` (`validator.py:355-384`) skips any entry whose `by` does not match
  `_ACTOR_RE` (lines 378-379). So `reference_agent/gemini-2.5-pro` and `Alice` both give
  `unverified`. Its docstring says "Only well-formed actor strings contribute to tier promotion;
  malformed entries are ignored (W10)".
- `_validate_okf2_verified` (`validator.py:584-631`) raises E9 when `by` is falsy. It raises W10
  (lines 616-624) when `by` is not a string or does not match `_ACTOR_RE`. The message text is:
  `"File '{path}': verified entry [{i}] has malformed 'by' value '{by}'. Actor strings must
  follow the format '<prefix>:<identifier>' (e.g. 'human:alice', 'bot:ci'). Fix: correct the
  'by' value in verified entry [{i}]."` The last part (line 622) is not an f-string, so it
  prints a literal `[{i}]`.
- The module docstring line 13 reads "W10 – Malformed actor string in `verified[].by`".
- The following places teach `<prefix>:<identifier>` or `bot:ci` as the form:
  - `docs/source/reference/validation-codes.md:526-549`: the W10 section. It also says
    malformed actors are ignored for the tier.
  - `docs/source/how-to/validate-standalone-files.md:176`: the W10 row.
  - `skills/okf-schema/SKILL.md:367`: the W10 row.
  - `skills/okfkb-record-findings/SKILL.md:45`: `by: <actor, e.g. human:alice or bot:collector>`.
  - `src/okf_schema/data/kb/_schema/Base.schema.yaml:32`, the shipped scaffold:
    `generated.by` description "Actor string identifying the producer (e.g. 'human:alice',
    'bot:ci')". Its checked-in copy is
    `examples/okfkb-hw-knowledge-base/_schema/Base.schema.yaml:32`. `okfkb update` does not
    refresh that copy: `scaffold_kb` copies `SCHEMA_FILES` only at init
    (`src/okf_schema/okfkb/scaffold.py:121-126`).
- Tests that pin the current behaviour, in `tests/test_okf2_compliance.py`:
  - `test_derive_trust_tier_malformed_actor_returns_unverified` (line 48): `Alice` →
    `unverified`.
  - `test_validate_okf2_verified_w10_malformed_actor` (line 398): `Alice` → W10.
- `skills/okf-schema/references/okf-v0.2.md` is the upstream specification text, verbatim. Its
  sections 2, 5.2, 5.3 and 7 define the actor forms and the tier rule. It does not change.

## What changes

### 1. Runtime: `src/okf_schema/validator.py`

- **Actor pattern** (lines 64-65). Replace the comment and pattern with a single pattern that
  accepts both shapes:

  ```python
  # Matches OKF 0.2 actor strings (spec section 7): <producer>/<version> such as
  # reference_agent/gemini-2.5-pro, human:<id>, process:<id>, and any <prefix>:<identifier>.
  _ACTOR_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9._-]*[:/].+$")
  ```

  The `<producer>` and `<prefix>` part is the character class the prefix already used, plus the
  dot (Q4): a letter, then letters, digits, `.`, `_` or `-`. `bot:okf-schema`, `human:alice`,
  `process:nightly-check`, `reference_agent/gemini-2.5-pro`, `langchain.agents/0.3` and
  `acme.ci:nightly` match. `alice`, `Alice`, `""` and `human:` do not.
- **`_derive_trust_tier`** (lines 355-384). The `verified` normalisation stays as it is: absent
  or empty, a bare mapping read as a one-element list, a non-list, a non-dict entry. Only the
  per-entry rule changes:

  ```python
  by = entry.get("by")
  if not isinstance(by, str) or not by:
      continue  # no actor string (E9 or W10): it does not count
  if by.startswith("human:") and by != "human:":
      return "human-reviewed"
  has_machine = True
  ```

  - Any non-empty string that is not `human:<id>` counts as machine (Q2, spec section 5.3),
    whether or not it matches `_ACTOR_RE`.
  - A missing, empty or non-string `by` does not count: it is no actor string (spec section 2:
    "Actor: a string"). E9 or W10 reports it.
  - The `human:` prefix check is case-sensitive, as today.
  - `human:` with nothing after it counts as machine, not human-reviewed (Q5). W10 is still
    raised because it does not match `_ACTOR_RE`.
  - New docstring (Google style, per `.github/guidelines/python-module-documentation.guidelines.md`):
    summary "Derive the OKF 0.2 trust tier from `verified` entries (spec section 5.3)." Then
    state the rule: an entry whose `by` is `human:` followed by an identifier makes it
    `"human-reviewed"`. Any other non-empty string `by`, well formed or not (W10), `human:` alone
    included, makes it `"machine-confirmed"`. An
    entry without a string `by` does not count. Add `Args:` (`frontmatter`: the parsed
    frontmatter mapping) and `Returns:` (one of the three tiers).
- **W10** in `_validate_okf2_verified` (lines 616-624). The condition is unchanged
  (`not isinstance(by, str) or not _ACTOR_RE.match(by)`, now with the new pattern). Every part
  of the message that interpolates (`{path}`, `{i}`, `{by}`) is an f-string. The code block below
  is the exact text:

  ```python
  f"File '{path}': verified entry [{i}] has malformed 'by' value '{by}'. "
  "OKF 0.2 actors are '<producer>/<version>' (e.g. 'reference_agent/gemini-2.5-pro'), "
  "'human:<id>' or 'process:<id>'; any '<prefix>:<identifier>' is also accepted. "
  "Only a 'human:<id>' actor makes the concept human-reviewed. "
  f"Fix: correct the 'by' value in verified entry [{i}]."
  ```

  The severity stays warning and the code stays `W10`.
- Module docstring line 13: "W10 – `verified[].by` actor in no OKF 0.2 form (`<producer>/<version>`,
  `<prefix>:<identifier>`)".
- Markers: add `# @implements_req SwRS-OKFSCHEMA-CORE-006` on the line above `def
  _derive_trust_tier` and above `def _validate_okf2_verified`. Today the module's only CORE-006
  marker is at `validator.py:722`, and `api.py:375` has one too. Keep both.

### 2. Human documentation

- `docs/source/reference/validation-codes.md:526-549`, W10 section:
  - New title: `### W10: Unrecognized Actor String in `verified[].by``.
  - **Description**: a `verified` entry's `by` is in none of the OKF 0.2 actor forms (spec section
    7): `<producer>/<version>` for agents and tools (`reference_agent/gemini-2.5-pro`),
    `human:<id>` for a person, `process:<id>` for an automated process. okf-schema also accepts
    any `<prefix>:<identifier>` (`bot:okf-schema`). A dot is allowed in the producer and the
    prefix (`langchain.agents/0.3`). The warning does not change the trust tier: an entry whose
    `by` is `human:<id>` makes the concept human-reviewed, and any other non-empty actor, warned
    or not, makes it machine-confirmed. To be read as human-reviewed, the actor must be `human:`
    followed by an identifier: `human:` alone counts as machine-confirmed and is warned W10.
  - **Example**: `by: "Alice"`, commented "# no recognized form: counts as machine-confirmed".
  - **How to Fix**: `by: "human:alice"` for a person, `by: "reference_agent/gemini-2.5-pro"` for
    an agent.
  - Keep `Stable code: `W10``.
- `docs/source/how-to/validate-standalone-files.md:176`: the row becomes
  `| **W10** | Verification actors use an OKF 0.2 form | Use `<producer>/<version>`, `human:<id>` or `process:<id>` |`.
- `docs/source/explanation/project-feature-coverage.md`: add one row after the staleness row
  (line 31):
  `| OKF 0.2 trust tier and actor forms (W10) | SwRS-OKFSCHEMA-CORE-006 S1 and S5; `tests/test_okf2_compliance.py` covers each actor form for the tier and for W10, including an unrecognized actor counted as machine; `tests/test_api.py` covers `trust_tier` of `show_bundle`; `tests/test_cli_remaining.py` covers `validate-md --strict` on a `<producer>/<version>` actor. |`
- `README.md`: no W10 or trust-tier text (checked). Unaffected.

### 3. Standalone agent skills

- `skills/okf-schema/SKILL.md:367`: the row becomes
  `| W10 | Actor syntax | A `verified[].by` actor is not `<producer>/<version>`, `human:<id>`, `process:<id>` or `<prefix>:<identifier>`; it still counts as machine-confirmed |`.
- `skills/okfkb-record-findings/SKILL.md:45`: `by: <actor, e.g. human:alice or reference_agent/gemini-2.5-pro>`.
- `skills/okf-schema/references/okf-v0.2.md`: not edited (it is the verbatim upstream text).

### 4. Scaffold guidance

- `src/okf_schema/data/kb/_schema/Base.schema.yaml:32`: `generated.by` description becomes
  `Actor string (OKF 0.2 section 7), e.g. 'human:alice', 'process:nightly-check' or 'reference_agent/gemini-2.5-pro'.`
  It stays a plain YAML scalar on one line, as the current line is (it holds no `: `).
- `src/okf_schema/data/kb/guidelines/knowledge-base.guidelines.md:55` (`by: human:alice`): already
  a spec form. Unaffected.
- `src/okf_schema/okfkb/finding.py:106` writes `by: bot:okf-schema`. That `<prefix>:<identifier>`
  stays accepted (Q1), so it is out of scope.

### 5. Concrete examples

- `examples/okfkb-hw-knowledge-base/_schema/Base.schema.yaml:32`: the same edit as the shipped
  file, by hand, because no recipe refreshes it.
- The examples' `by: bot:okf-schema` values stay valid. `just refresh-all-examples` (run by
  preflight) must produce no other diff.

### 6. Requirements

- `requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-006.md` is `req_lifecycle: proposed`, so its
  body and `scenarios:` can be edited.
  - Add `- id: S5` / `title: Count every OKF 0.2 actor form` to `scenarios:`.
  - Add a body section after S4:

    ```markdown
    ### Scenario S5: Count every OKF 0.2 actor form

    - GIVEN a concept whose `verified[].by` actor is written as `<producer>/<version>`,
      `human:<id>`, `process:<id>`, any other `<prefix>:<identifier>`, or in no recognized form
    - WHEN the concept is validated or inspected
    - THEN a `human:<id>` actor makes it human-reviewed, any other non-empty actor (`human:`
      with no identifier included) makes it machine-confirmed, and only an actor in no
      recognized form raises warning W10
    ```

  - Keep the ID, UUID, other scenarios and authored metadata. Do not hand-edit the generated
    fields (`implemented_in_files`, `tested_in_files`, links).
- Run `okfreq update-coverage requirements`, then `okfreq lint requirements` (navigation), then
  the checks of `requirements/guidelines/project.guidelines.md`, "After editing".
- `requirements/tiers/log.md`: under the day's `## YYYY-MM-DD` heading (one per date, newest
  first; share it with CR 58 and other batch-01 entries), add `### Trust tier actor forms`:
  - Why: OKF 0.2 sections 5.3 and 7.
  - What: CORE-006 gained S5. Any actor that is not `human:<id>` counts as machine-confirmed
    (`human:` alone included). W10 accepts `<producer>/<version>` and `<prefix>:<identifier>`,
    with a dot allowed in the producer and the prefix, and its message now prints the entry
    index.
  - Verification: the commands run.

### 7. Verification and packaging

No change to `pyproject.toml`, `justfile` or CI. No CI job is added or changed. The Driver does
not bump the version. The commit type is `fix(validate)`, per
`.github/guidelines/git-commit-message.guidelines.md`.

## Out of scope

- The `okf-schema trust` command and `show` output (CR 58).
- Checking the actor form of `generated.by` or `sources[].author`. They are not checked today and
  stay unchecked.
- Changing the actor `okfkb` writes (`bot:okf-schema`, `finding.py:106`) or the examples that
  carry it.
- Case-insensitive `human:` matching, or trimming whitespace in `by`.
- Any change to E9.

## Evidence

No host and default matrix: the behaviour depends on neither host nor configured value.

Unit tests follow `.github/guidelines/python-unittest.guidelines.md`: function tests, and
`@Parametrization` for the tables. Each new or changed test that exercises S5 carries
`# @tests_req SwRS-OKFSCHEMA-CORE-006#S5`.

1. `tests/test_okf2_compliance.py`:
   - Rename `test_derive_trust_tier_malformed_actor_returns_unverified` to
     `test_derive_trust_tier_unrecognized_actor_returns_machine_confirmed`. `Alice` →
     `"machine-confirmed"` (Q2).
   - New parametrized `test_derive_trust_tier_actor_forms`, one case per line:
     - `reference_agent/gemini-2.5-pro` → `machine-confirmed`
     - `process:finance-nightly` → `machine-confirmed`
     - `bot:okf-schema` → `machine-confirmed`
     - `langchain.agents/0.3` → `machine-confirmed` (Q4)
     - `alice` → `machine-confirmed`
     - `human:` → `machine-confirmed` (Q5)
     - `human:ahormati` → `human-reviewed`
     - `42` (an int) → `unverified`
     - `""` → `unverified`
   - A bare mapping with `reference_agent/gemini-2.5-pro` → `machine-confirmed`.
   - `[reference_agent/gemini-2.5-pro, human:alice]` → `human-reviewed`.
   - New parametrized `test_validate_okf2_verified_accepts_okf02_actor_forms`:
     `reference_agent/gemini-2.5-pro`, `process:nightly-check`, `human:alice`,
     `bot:okf-schema`, `langchain.agents/0.3` and `acme.ci:nightly` (Q4) each give no warning
     and no error.
   - Extend `test_validate_okf2_verified_w10_malformed_actor` (or a parametrized sibling) with
     `alice`, `42` and `human:` each giving W10.
   - New `test_validate_okf2_verified_w10_message_names_entry_index`: entries
     `[{by: human:alice, at: ...}, {by: alice, at: ...}]` give exactly one W10. Its message
     contains `verified entry [1] has malformed` and ends with
     `Fix: correct the 'by' value in verified entry [1].`, and contains no `{i}`.
2. `tests/test_api.py`: next to `test_show_bundle_trust_tier_human_reviewed` (line 606), add
   `test_show_bundle_trust_tier_producer_version_actor`. A bundle concept with
   `verified: [{by: reference_agent/gemini-2.5-pro, at: '2026-01-01'}]` gives
   `show_bundle(...).trust_tier == "machine-confirmed"`.
3. `tests/test_cli_remaining.py`, in the `validate-md` block (line 286): add
   `test_validate_md_strict_accepts_producer_version_actor`. Use a file with `type`, `title`,
   `description`, `generated: {at: "2024-01-01T00:00:00Z", by: reference_agent/gemini-2.5-pro}`
   and `verified: [{by: reference_agent/gemini-2.5-pro, at: "2024-01-02T00:00:00Z"}]`, plus the
   same minimal concept schema as `test_validate_md_validate_md_exits_0_for_valid_files`, passed
   with `--schemas-dir`. The file writes `verified` as an inline flow list, as above: a
   block-style `verified:` list also raises W7, so `--strict` would exit 1 even after the fix.
   `validate-md --strict` exits 0 and the output has no `W10`. On 2f09cef it exits 1 with W10:
   the intake's scenario, run through the CLI.
4. Shipped-file check, in `tests/test_kb_scaffold.py`: add
   `test_shipped_base_schema_teaches_okf02_actor_forms`.
   - It reads the shipped scaffold as it ships, at the head under test, via
     `importlib.resources.files("okf_schema.data.kb").joinpath("_schema/Base.schema.yaml")`.
     It does not read a copy the test prepares.
   - It asserts that `properties.generated.properties.by.description` contains
     `reference_agent/gemini-2.5-pro` and does not contain `bot:`.
   - It also reads `examples/okfkb-hw-knowledge-base/_schema/Base.schema.yaml` from the
     repository (path from the test file's parents) and asserts the same description is
     identical.
5. Scenario steps, run by the Driver in its worktree and reported:
   - A scratch file `c.md` with the frontmatter of item 3, `verified` written as an inline flow
     list (a block-style list raises W7), and a scratch schemas directory `<dir>` holding the
     same minimal concept schema as item 3 (`validate-md` requires `--schemas-dir`; without it
     it exits 2 with "Missing option"):
     `uv run -- okf-schema validate-md --input c.md --schemas-dir <dir> --strict` exits 0 with
     no W10.
   - With `by: alice`, the same command (`--schemas-dir <dir> --strict`) exits 1 and shows W10 whose message names `verified entry [0]` twice.
   - In a scratch bundle holding that concept, `show_bundle(...).trust_tier` is
     `machine-confirmed` for both actors.
6. Checks: `okfreq update-coverage requirements`, then
   `okfreq validate requirements --prose --check-links --project-root .`, then
   `okfreq lint requirements --prose --check-links --project-root .`, then `just preflight`.
   - After update-coverage, CORE-006 S5 has `@tests_req` markers.
   - `just refresh-all-examples` (in preflight) leaves no diff other than the hand-edited example
     schema.
