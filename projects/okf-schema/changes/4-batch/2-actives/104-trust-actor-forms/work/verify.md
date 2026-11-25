Head: 7a33d920b46188821c4ebf73d008fbc12dcdf750

# CR-104 "Trust tier: count the actor forms allowed by OKF 0.2": verification

**Verdict: NOT VERIFIED.** The runtime and the specification's evidence items 1 to 6 are VERIFIED.
Two claims of the posted PR description fail (D1 and D2 below).

Every claim is judged at `7a33d92` (full SHA above). Base is
`2f09cef3e786d1696e42b5cb305d4a55111e7725`. Nothing is carried from an earlier judgment.

Placeholders: `<worktree>` is the CR's worktree, `<CR>` the CR folder, `<scratch>` a folder under
`<CR>/work/scratch/` that was removed afterwards. `uv ...` means
`uv --directory <worktree> run --no-sync -- ...`. Helper scripts are in `<CR>/work/verifier/`.
Before and after captures: `<CR>/work/verifier/evidence/` (`before-after.md`).

## Failed claims (PR description)

### D1. "Each proof in the description names its SHA": NOT VERIFIED

```console
$ grep -noE "\b[0-9a-f]{7,40}\b" <CR>/work/pr-body.md
59:7a33d92
```

Only the `just preflight` bullet (line 59) names a SHA. These results name none:

- line 57, "Example command: exit 0, no warning. With `by: alice`: exit 1 ..."
- line 61, "`okfreq validate requirements ...`: 35 requirements, 0 errors, 0 warnings."
- line 63, "A first run at the previous commit failed 8 symbolic link tests ... the base commit
  failed the same 8."
- line 67, "Evidence status: marker linkage ... the marked tests were executed and passed ..."

The facts themselves hold (R3, R5, S5, S6, S7). The SHAs are `7a33d92` (lines 57, 61, 67),
`1ae8870` (previous commit) and `2f09cef` (base).

### D2. "Verification and packaging | new tests only." (line 43): NOT VERIFIED

The diff also changes two tests that existed at the base.

```console
$ git diff 2f09cef..7a33d92 -- tests/test_okf2_compliance.py   (extract)
-def test_derive_trust_tier_malformed_actor_returns_unverified() -> None:
+def test_derive_trust_tier_unrecognized_actor_returns_machine_confirmed() -> None:
-    assert _derive_trust_tier(fm) == "unverified"
+    assert _derive_trust_tier(fm) == "machine-confirmed"
-def test_validate_okf2_verified_w10_malformed_actor(tmp_path: Path) -> None:
+@Parametrization.case(name="capitalized_name", by="Alice")
+@Parametrization.case(name="bare_name", by="alice")
+@Parametrization.case(name="not_a_string", by=42)
+@Parametrization.case(name="human_without_id", by="human:")
+def test_validate_okf2_verified_w10_malformed_actor(tmp_path: Path, by: object) -> None:
-    assert any(f.code == "W10" for f in report.warnings)
+    assert [f.code for f in report.warnings] == ["W10"]
+    assert report.errors == []
```

The changes themselves are what the specification asks (Evidence item 1). Only the description's
wording is wrong.

## State and gates

### G1. Head, tree and base: VERIFIED

```console
$ git rev-parse HEAD
7a33d920b46188821c4ebf73d008fbc12dcdf750
$ git status --porcelain | wc -l          (before and after all runs)
0
$ git merge-base origin/main HEAD
2f09cef3e786d1696e42b5cb305d4a55111e7725
$ git rev-parse origin/main
2f09cef3e786d1696e42b5cb305d4a55111e7725
$ git log --oneline 2f09cef..HEAD
7a33d92 docs: add the trust tier fix to the changelog
1ae8870 fix(validate): count every OKF 0.2 actor form in the trust tier
$ gh pr view 69 -R gsemet/okf-schema --json headRefOid,isDraft -q '.headRefOid, .isDraft'
7a33d920b46188821c4ebf73d008fbc12dcdf750
true
```

### G2. Long gate pass at the head: VERIFIED (cited)

Log `<CR>/work/gates/20261125-224645.log`, first line:

```text
gate CR-104 branch chantier/batch-01/cr-104-trust-tier-count-the-actor-forms-allowed head 7a33d920b46188821c4ebf73d008fbc12dcdf750
2361: Required test coverage of 95% reached. Total coverage: 95.58%
2362: 1128 passed, 12 skipped in 104.77s
2563: uv run --no-sync -- sphinx-build -W -b html docs/source docs/_build/html
2674: build succeeded.
2677: result: pass at 7a33d920b46188821c4ebf73d008fbc12dcdf750
```

`chantier handoff CR-104` checklist, at the full SHA:
`[x] long gate passed (gate CR-104 preflight; ...)`.

CI, informative only: `gh pr checks 69` shows preflight 3.10, 3.11, 3.12, 3.13 and cross-platform
macos-latest and windows-latest `pass`, tag-release `skipping`.

## Specification

### R1. Runtime (specification "What changes" 1): VERIFIED

Probe of the source tree, base then head (`uv python <verifier>/probe.py <src>`; full outputs in
`evidence/before-2f09cef.txt` and `evidence/after-7a33d92.txt`).

```text
base pattern: ^[a-zA-Z][a-zA-Z0-9_-]*:.+$
head pattern: ^[a-zA-Z][a-zA-Z0-9._-]*[:/].+$
by                                base tier, codes            head tier, codes
'reference_agent/gemini-2.5-pro'  unverified [W10]            machine-confirmed []
'langchain.agents/0.3'            unverified [W10]            machine-confirmed []
'acme.ci:nightly'                 unverified [W10]            machine-confirmed []
'process:nightly-check'           machine-confirmed []        machine-confirmed []
'process:finance-nightly'         machine-confirmed []        machine-confirmed []
'bot:okf-schema'                  machine-confirmed []        machine-confirmed []
'alice', 'Alice', 'human:'        unverified [W10]            machine-confirmed [W10]
'human:alice', 'human:ahormati'   human-reviewed []           human-reviewed []
'Human:alice'                     machine-confirmed []        machine-confirmed []
42, True, ['x'], {'a': 1}         unverified [W10]            unverified [W10]
0, '', None                       unverified [E9]             unverified [E9]
no by / absent / [] / str / non-dict entry   unverified       unverified
bare mapping producer/version     unverified                  machine-confirmed
producer/version + human          human-reviewed              human-reviewed
```

W10 for entry 1 at head: `W10 count: 1`, `equals specification text: True`,
`contains '{i}': False | level warnings only, errors: []`. At base: `contains '{i}': True`, the
message ends `verified entry [{i}].` and teaches `bot:ci`.

Markers:

```console
$ git grep -n "implements_req SwRS-OKFSCHEMA-CORE-006" HEAD -- src
HEAD:src/okf_schema/api.py:375
HEAD:src/okf_schema/validator.py:356
HEAD:src/okf_schema/validator.py:595
HEAD:src/okf_schema/validator.py:736
```

### R2. Documentation, skills, scaffold, example, log (specification 2 to 6): VERIFIED

```console
$ uv python <verifier>/texts.py <CR>/03-change-spec.md
ok  feature map row, how-to W10 row, okf-schema skill W10 row, record-findings example,
ok  shipped schema description, example schema description, module docstring W10, W10 title,
ok  W10 example comment, W10 fix human, W10 fix agent, W10 stable code, log subheading
day headings 2026-11-25: 1 | first heading: ## 2026-11-25
```

(The script prints one `ok` line per item, 13 lines, none `MISSING`.) The W10 section it prints
matches the specification's title, description, example, fix and stable code.
The bundled specification agrees with these texts:

```console
$ sed -n '401,407p;489,500p' skills/okf-schema/references/okf-v0.2.md      (extract)
### 5.3 Trust tiers
- `verified` by non-`human:` actors only => **machine-confirmed**.
- `verified` by a `human:<id>` actor => **human-reviewed**.
## 7. Actor convention
- `<producer>/<version>` for agents and tools, for example
- `human:<id>` for a person, for example `human:ahormati`.
- `process:<id>` for an automated process, for example
```

```console
$ git grep -n "bot:ci" HEAD
tests/test_okf2_compliance.py:44, :99, :124, :231, :250      (test inputs only)
$ git grep -niE "trust|W10|verified\[" HEAD -- README.md
(no output, exit 1)
$ git diff --stat 2f09cef HEAD -- README.md pyproject.toml justfile .github uv.lock \
    skills/okf-schema/references src/okf_schema/okfkb src/okf_schema/data/kb/guidelines \
    src/okf_schema/api.py | wc -l
0
$ git grep -nE "bot:okf-schema|by: human:alice" HEAD -- src
src/okf_schema/data/kb/guidelines/knowledge-base.guidelines.md:55:  by: human:alice
src/okf_schema/okfkb/finding.py:106:                "by": "bot:okf-schema",
```

### R3. Requirements (specification 6 and Evidence 6): VERIFIED

```console
$ uv okfreq update-coverage requirements --check
0 files would change                                        (exit 0)
$ uv okfreq validate requirements --prose --check-links --project-root .
35 requirements, 0 errors, 0 warnings                       (exit 0)
$ uv okfreq lint requirements --check --prose --check-links --project-root .
0 indexes would change
0 requirement OKF projections would change                  (exit 0)
$ uv okfreq trace requirements --json        (CORE-006 extract)
implemented: src/okf_schema/api.py, src/okf_schema/validator.py
tested: tests/test_api.py, tests/test_cli_remaining.py, tests/test_okf2_compliance.py
S5 markers: tests/test_api.py:621, tests/test_cli_remaining.py:323, tests/test_okf2_compliance.py:48
$ grep -nE "req_lifecycle|id: S5|Scenario S5" SwRS-OKFSCHEMA-CORE-006.md
11:req_lifecycle: proposed
40:- id: S5
84:### Scenario S5: Count every OKF 0.2 actor form
```

`git grep -n "tests_req SwRS-OKFSCHEMA-CORE-006#S5" HEAD -- tests` gives nine markers: api 621,
cli 323, compliance 48, 54, 74, 80, 436, 452, 469. `requirements/tiers/log.md` holds
`### Trust tier actor forms` with Why, What and Verification under the single `## 2026-11-25`.

### R4. Evidence items 1 to 4, the tests: VERIFIED

At head:

```console
$ uv pytest -o addopts= -p no:cacheprovider -q --no-header tests/test_okf2_compliance.py \
    tests/test_api.py tests/test_cli_remaining.py tests/test_kb_scaffold.py tests/test_project_contract.py
295 passed in 6.14s
$ ... -v ... -k "actor or trust_tier or verified or shipped_base_schema"
46 passed, 249 deselected
```

All named tests and cases show `PASSED`: the renamed test, `actor_forms` (9 cases), bare mapping,
producer and human, `accepts_okf02_actor_forms` (6), `w10_malformed_actor` (4), message index,
`show_bundle_trust_tier_producer_version_actor`,
`validate_md_strict_accepts_producer_version_actor`,
`shipped_base_schema_teaches_okf02_actor_forms`. The diff of the last one reads the shipped schema
through `importlib.resources` and compares the checked-in example, as item 4 asks.

The head's four changed test files against the base source
(`uv python <verifier>/basetests.py <scratch>/b/src`):

```text
module under test: base src (2f09cef)
FAILED test_okf2_compliance.py::test_derive_trust_tier_unrecognized_actor_returns_machine_confirmed
FAILED ...::test_derive_trust_tier_actor_forms[producer_version], [dotted_producer], [unrecognized], [human_without_id]
FAILED ...::test_derive_trust_tier_bare_mapping_producer_version_returns_machine_confirmed
FAILED ...::test_validate_okf2_verified_accepts_okf02_actor_forms[producer_version], [dotted_producer], [dotted_prefix]
FAILED ...::test_validate_okf2_verified_w10_message_names_entry_index
FAILED test_api.py::test_show_bundle_trust_tier_producer_version_actor
FAILED test_cli_remaining.py::test_validate_md_strict_accepts_producer_version_actor
FAILED test_kb_scaffold.py::test_shipped_base_schema_teaches_okf02_actor_forms
13 failed, 280 passed
```

### R5. Evidence item 5, the scenario: VERIFIED

The command, at head, on the specification's file and schema:

```console
$ uv okf-schema validate-md --input <scratch>/c.md --schemas-dir <scratch>/schemas --strict     (reference_agent/gemini-2.5-pro)
All files validated successfully (0 errors, 0 warnings).                          exit 0
$ same command, verified.by: alice
WARNING [W10] File '<scratch>/c.md': verified entry [0] has malformed 'by' value 'alice'. OKF 0.2
actors are '<producer>/<version>' (e.g. 'reference_agent/gemini-2.5-pro'), 'human:<id>' or
'process:<id>'; any '<prefix>:<identifier>' is also accepted. Only a 'human:<id>' actor makes the
concept human-reviewed. Fix: correct the 'by' value in verified entry [0].
Validation failed: 0 error(s), 1 warning(s) (strict mode).                        exit 1
```

At base the first case exits 1 with W10 (`evidence/before-2f09cef.txt`). `show_bundle(...).trust_tier`
at head: `machine-confirmed` for `reference_agent/gemini-2.5-pro`, `alice` and `human:`,
`human-reviewed` for `human:alice`; at base `unverified` for the first three. `okf-schema show`:
`trust: unverified` at base, `trust: machine-confirmed` at head.

### R6. Evidence item 6, examples: VERIFIED

In a scratch clone at `7a33d92` (`<verifier>/examples.py`), so the worktree stays clean:

```text
$ just refresh-all-examples  -> exit 0
git diff HEAD (content) after refresh-all-examples: ''
status entries: 14 modified; 0 untracked      (all under examples/okfreq-examples)
same bytes ignoring CR: True                  (each of the 14)
$ uv run --no-sync -- okf-schema validate --strict --path examples/okfkb-hw-knowledge-base/  -> exit 0
Bundle is conformant (0 errors, 0 warnings).
W10 in output: False
example files carrying 'by: bot:okf-schema': 12
$ just refresh-okfkb-example  -> exit 0      (after putting the old schema description back)
old description still there after `okfkb update`: True
```

`just preflight` is G2.

## PR description, other claims

### S1. Posted body, rendering, privacy, form: VERIFIED

```console
$ gh pr view 69 -R gsemet/okf-schema --json body -q .body | diff --strip-trailing-cr -B - <CR>/work/pr-body.md
(no output, exit 0)
$ gh api repos/gsemet/okf-schema/pulls/69 -H 'Accept: application/vnd.github.html+json' -q .body_html   (counted)
h2: 4, h3: 7, table: 2, li: 24, pre: 1, checkbox: 9, img: 0, details: 0
$ grep -niE "<login or home path forms>" pr-body.md evidence/*
(no output, exit 1)
$ grep -niwE "driver|coder|inspector|verifier|debugger|chantier|batch" pr-body.md
(no output, exit 1)
```

Sections follow `.github/pull_request_template.md` (Description, Type of Change, Checklist,
Related Issues). No image is attached.

### S2. Behaviour table, "What changes", "Unchanged", "Product surfaces" (except D2): VERIFIED

Behaviour table and message: R1. `show` and API: R5. Docs, skills, schema, README, guideline,
`finding.py`: R2. S5, tests, feature map row: R2, R3, R4. Existing knowledge bases and the
hand-edited example: R6. `generated.by` and `sources[].author` unchecked: probe case
`generated.by=alice`, author `alice`, `verified.by=human:alice` exits 0 at base and head.
`human:` case-sensitive: `Human:alice` row of R1. Bundled reference "upstream text, left
verbatim": `<CR>/02-answers.md` line 7 records it as the upstream text; its diff is empty (R2).
Every delivered file is mentioned:

```console
$ git diff --name-status 2f09cef HEAD
M CHANGELOG.md
M docs/source/explanation/project-feature-coverage.md
M docs/source/how-to/validate-standalone-files.md
M docs/source/reference/validation-codes.md
M examples/okfkb-hw-knowledge-base/_schema/Base.schema.yaml
M requirements/tiers/log.md
M requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-006.md
M skills/okf-schema/SKILL.md
M skills/okfkb-record-findings/SKILL.md
M src/okf_schema/data/kb/_schema/Base.schema.yaml
M src/okf_schema/validator.py
M tests/test_api.py
M tests/test_cli_remaining.py
M tests/test_kb_scaffold.py
M tests/test_okf2_compliance.py
```

### S3. `CHANGELOG.md` claim: VERIFIED

```console
$ uv cz changelog --dry-run | diff --strip-trailing-cr -B - CHANGELOG.md
(no output, exit 0)
$ git show 2f09cef:CHANGELOG.md | grep -c "^## v0.18.1"
0
$ git tag --points-at 2f09cef
v0.18.1
```

The head adds the fix entry and the `## v0.18.1 (2026-11-25)` heading, nothing else.

### S4. Decisions, blast radius: VERIFIED

The four decisions match `<CR>/02-answers.md` items 2, 3, 5 and 6 (trust-forms-Q1, Q2, Q4, Q5).
Blast radius behaviour: R1 and R5. Revert and data: two commits on the base (G1), all files `M`
(S2), and

```console
$ git diff 2f09cef HEAD -- src | grep -E "^\+.*(write|open\()"
(no output, exit 1)
```

### S5. Validation results, facts (the missing SHAs are D1): facts VERIFIED

Example command and `show_bundle`: R5. `just preflight` at `7a33d92`: G2. `okfreq validate`: R3.
First run and base (`uv python <verifier>/logs.py <CR>/work`):

```text
gate 1ae8870 (20261125-222513.log): 8 failed, 1118 passed, 14 skipped; coverage 95.46%; result: FAIL; WinError 1314 lines: 8
base 2f09cef, links refused (debugger/base-test.log): 8 failed, 1094 passed, 14 skipped
base 2f09cef, links allowed (debugger/base-test-devmode.log): 1104 passed, 12 skipped
same failing tests, 1ae8870 and base: True 8
symlink probe on this host: file True | directory True
```

The base logs carry no SHA line; the CR's evidence records them as exports of the base:

```console
$ grep -n 2f09cef <CR>/evidence/debugger-symlink-gate.txt
5:  export of base 2f09cef, refused             8 failed, 1094 passed, 14 skipped
6:  export of base 2f09cef, Developer Mode on   1104 passed, 12 skipped
```

### S6. Evidence status: facts VERIFIED

Markers: R3. Marked tests passed: R4 and G2. Lifecycle `proposed`: R3.

### S7. Autonomous decision (braces in S5): VERIFIED

Scratch copy without tests (`<verifier>/prose.py`):

```text
S5 as at head (braces): 35 requirements, 0 errors, 4 warnings      (four W004, no acceptance test in the copy)
S5 with angle brackets: 35 requirements, 0 errors, 5 warnings
  added: W002 SwRS-OKFSCHEMA-CORE-006.md: body has no filled EARS expression
```

Docs, skills and messages keep the angle brackets: R1, R2.

### S8. Known gaps: VERIFIED

Both bullets are true. `git grep -n versionchanged HEAD -- src/okf_schema/api.py` gives only line
301 (another function), and `api.py` is unchanged. The skill row and the W10 section say a warned
actor counts as machine-confirmed (R2), while `42` is warned W10 and stays `unverified` (R1).
No `UNVERIFIED` claim and no uncaptured evidence pair. D1 and D2 are failed, not accepted, so no
bullet is due for them.

### S9. Checklist and Type of Change: VERIFIED

`just preflight` passes (G2); tests fail on base and pass on head (R4); documentation updated (R2);
no new warnings: `logs.py` finds `'warnings summary' lines: 0 | lines with 'Warning:' : 0` in the
head gate log, and Sphinx `-W` succeeded. Related Issues says `None`. The ticked types (bug fix,
documentation) and the title match the diff:

```console
$ gh pr view 69 -R gsemet/okf-schema --json title -q .title
fix(validate): count every OKF 0.2 actor form in the trust tier
```

## Notes, not failed claims

- `requirements/tiers/log.md` "Verification" records the earlier run (1118 passed, 14 skipped,
  8 failed). It is true history; the head's gate pass (G2) supersedes it.
- One slip of this verification: a no-op call changed the shell folder into
  `<CR>/work/scratch/ver`, against the startup-core rule. Nothing ran there and nothing was written.
- Scratch worktree and clone removed; the CR's worktree is clean at the head (G1).
