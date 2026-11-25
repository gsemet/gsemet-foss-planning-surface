Head: 1a03994e7bc2fbf1595cd6528a6f3c02a35542e2

# CR-104 "Trust tier: count the actor forms allowed by OKF 0.2": verification

**Verdict: VERIFIED** for the code, the specification and the CR's patch at `1a03994`. The posted
description holds facts and sentences that are stale or false at this head (section "Description
facts at 1a03994"). By the brief they are refreshed after this verdict, so they do not fail it.
No claim about the code or its behaviour was found false.

Judged at `1a03994` (full SHA above). The CR's base is `41fcd6dbebaddff719c2a3f54f610298034d0ad6`
(head of the pull request below). The earlier verification, at `7a33d92` on base `2f09cef`, is
`verifier/verify-7a33d92.md`.

Placeholders: `<worktree>` is the CR's worktree, `<CR>` the CR folder, `<scratch>` a folder under
`<CR>/work/scratch/` removed afterwards. `uv ...` means `uv --directory <worktree> run --no-sync -- ...`.

## State, move, gate, CI

### G1. Head and tree: VERIFIED at 1a03994

```console
$ git rev-parse HEAD
1a03994e7bc2fbf1595cd6528a6f3c02a35542e2
$ gh pr view 69 -R gsemet/okf-schema --json headRefOid,isDraft
1a03994e7bc2fbf1595cd6528a6f3c02a35542e2, draft true
$ git merge-base 41fcd6d HEAD
41fcd6dbebaddff719c2a3f54f610298034d0ad6
$ git status --porcelain                  (before and after all runs)
 M CHANGELOG.md
$ git diff --numstat                      (uncommitted, not part of the head, left as found)
1  0  CHANGELOG.md
$ git diff                                (extract)
+- **show**: accept names without .md and stay inside the bundle
```

### G2. The move: VERIFIED at 1a03994

```console
$ git range-diff 2f09cef..7a33d92 41fcd6d..1a03994
1:  1ae8870 ! 1:  ad55758 fix(validate): count every OKF 0.2 actor form in the trust tier
      only difference: context of the requirements/tiers/log.md hunk (day heading now shared)
2:  7a33d92 = 2:  1a03994 docs: add the trust tier fix to the changelog
$ git diff --stat 2f09cef 41fcd6d         (what the new base brings)
13 files: docs/source/reference/cli.md, requirements (log, StRS-CORE-002, CORE-005, CORE-010,
index), skills/okf-schema/SKILL.md, src/okf_schema/api.py, src/okf_schema/cli.py, tests
(acceptance_core, api, cli_remaining, edge_cases)
```

`validator.py` and `CORE-006` are not in the base change. `api.py` and `cli.py` are, so
`show_bundle`, `show` and `validate-md` claims are judged again.

### G3. Long gate pass at the head: VERIFIED at 1a03994 (cited)

`<CR>/work/gates/20261125-232725.log`:

```text
1:    gate CR-104 branch chantier/batch-01/cr-104-trust-tier-count-the-actor-forms-allowed head 1a03994e7bc2fbf1595cd6528a6f3c02a35542e2
2411: Required test coverage of 95% reached. Total coverage: 95.55%
2412: 1153 passed, 12 skipped in 198.61s
2613: uv run --no-sync -- sphinx-build -W -b html docs/source docs/_build/html
2643: build succeeded.
2646: result: pass at 1a03994e7bc2fbf1595cd6528a6f3c02a35542e2
'warnings summary': 0 | 'Warning:': 0 | 'WinError 1314': 0 | lines starting 'FAILED ': 0
```

`chantier handoff CR-104`: `[x] long gate passed (gate CR-104 preflight; ...)` at the full SHA.

### G4. CI at the head: VERIFIED at 1a03994

```console
$ gh api repos/gsemet/okf-schema/commits/1a03994e7bc2fbf1595cd6528a6f3c02a35542e2/check-runs
preflight (3.10) success, (3.11) success, (3.12) success, (3.13) success
cross-platform (macos-latest) success, cross-platform (windows-latest) success
tag-release skipped                          (head_sha 1a03994 on all seven)
```

## Specification

### R1. Runtime: VERIFIED at 1a03994

`probe.py` (`verifier/probe-41fcd6d.py`) on the base source and the head source; full outputs in
`verifier/evidence/before-41fcd6d.txt` and `after-1a03994.txt`.

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
W10 message, entry 1              literal [{i}], bot:ci       equals specification text: True
```

`generated.by: alice` and `sources[].author: alice` with `verified.by: human:alice`:
`validate-md --strict` exit 0 on base and head. Markers:

```console
$ git grep -n "implements_req SwRS-OKFSCHEMA-CORE-006" 1a03994 -- src
api.py:438, validator.py:356, :595, :736
```

### R2. Documentation, skills, scaffold, example, log: VERIFIED at 1a03994

```console
$ uv python <CR>/work/verifier/texts.py <CR>/03-change-spec.md
ok  (13 lines: feature map row, how-to row, skill W10 row, record-findings example, shipped and
    example schema descriptions, module docstring, W10 title, comment, both fixes, stable code,
    log subheading); none MISSING
day headings 2026-11-25: 1 | first heading: ## 2026-11-25
$ git grep -n "bot:ci" 1a03994 -- . ':!tests'                      (no output, exit 1)
$ git grep -niE "trust|W10|verified\[" 1a03994 -- README.md        (no output, exit 1)
$ git diff --stat 41fcd6d 1a03994 -- README.md pyproject.toml justfile .github uv.lock \
    skills/okf-schema/references src/okf_schema/okfkb src/okf_schema/data/kb/guidelines \
    src/okf_schema/api.py src/okf_schema/cli.py                    (no output)
$ git grep -nE "bot:okf-schema|by: human:alice" 1a03994 -- src
.../knowledge-base.guidelines.md:55: by: human:alice
src/okf_schema/okfkb/finding.py:106: "by": "bot:okf-schema",
```

`requirements/tiers/log.md` holds `### Trust tier actor forms` then CR-101's entry under the one
`## 2026-11-25`. The W10 section of `validation-codes.md` and the skill row (line 367) were read at
the head and match the specification.

### R3. Requirements: VERIFIED at 1a03994

```console
$ uv okfreq update-coverage requirements --check
0 files would change                                                  (exit 0)
$ uv okfreq validate requirements --prose --check-links --project-root .
36 requirements, 0 errors, 0 warnings                                 (exit 0)
$ uv okfreq lint requirements --check --prose --check-links --project-root .
0 indexes would change
0 requirement OKF projections would change                            (exit 0)
$ uv okfreq trace requirements --json       (exit 0, CORE-006)
implemented: api.py, validator.py; tested: test_api.py, test_cli_remaining.py, test_okf2_compliance.py
$ git grep -n "tests_req SwRS-OKFSCHEMA-CORE-006#S5" 1a03994 -- tests
test_api.py:624, test_cli_remaining.py:380, test_okf2_compliance.py:48, :54, :74, :80, :436, :452, :469
$ grep -nE "req_lifecycle|id: S5|Scenario S5" SwRS-OKFSCHEMA-CORE-006.md
11 req_lifecycle: proposed; 40 - id: S5; 84 ### Scenario S5: Count every OKF 0.2 actor form
```

### R4. Tests (evidence items 1 to 4): VERIFIED at 1a03994

```console
$ uv python -B -m pytest -o addopts= -p no:cacheprovider -q --no-header tests/test_okf2_compliance.py \
    tests/test_api.py tests/test_cli_remaining.py tests/test_kb_scaffold.py tests/test_project_contract.py
320 passed in 11.19s
$ ... -v (first four files) -k "actor or trust_tier or verified or shipped_base_schema"
46 passed, 272 deselected          (every named test and case PASSED)
$ uv python <scratch>/basetests.py <base 41fcd6d>/src     (head tests, base source)
module under test: base src (41fcd6d)
13 failed, 305 passed
```

The 13 failures are the renamed tier test, 4 `actor_forms` cases, the bare mapping test, 3
`accepts_okf02_actor_forms` cases, the message index test, the `show_bundle` test, the
`validate-md --strict` test and the shipped schema test.

### R5. Scenario (evidence item 5): VERIFIED at 1a03994

```console
$ uv python -B <CR>/work/verifier/desc2/example.py <scratch>
=== by: reference_agent/gemini-2.5-pro -> exit 0
All files validated successfully (0 errors, 0 warnings).
W10 findings: 0 | 'verified entry [0]': 0
show_bundle trust_tier: machine-confirmed
=== by: alice -> exit 1
  WARNING [W10] File '<scratch>\c.md': verified entry [0] has malformed 'by' value 'alice'. OKF 0.2
  actors are [...] Fix: correct the 'by' value in verified entry [0].
Validation failed: 0 error(s), 1 warning(s) (strict mode).
W10 findings: 1 | 'verified entry [0]': 2
show_bundle trust_tier: machine-confirmed
scratch removed: True
```

From R1's probe: `show_bundle` at head gives `machine-confirmed` for producer/version, `alice`,
`human:` and `human-reviewed` for `human:alice`; at base `unverified` for the first three.
`okf-schema show`: `trust: unverified` at base, `trust: machine-confirmed` at head.

### R6. Examples (evidence item 6): VERIFIED at 1a03994

The head's gate (G3) ran `just refresh-all-examples`; after it the only changed file is
`CHANGELOG.md`, written by `just changelog` (G1). In the same log,
`okf-schema validate --strict --path examples/okfkb-hw-knowledge-base/` prints
`Bundle is conformant (0 errors, 0 warnings).`

"An existing knowledge base keeps its own schema copy after `okfkb update`":
carried from 7a33d92: the move changed nothing under `src/okf_schema/okfkb` or `examples`
(G2 file list).

## PR description, claims other than the dated ones

### S1. Posted body, rendering, privacy, form: VERIFIED at 1a03994

```console
$ gh pr view 69 -R gsemet/okf-schema --json body -q .body | diff --strip-trailing-cr -B - <CR>/work/pr-body.md
(no output, exit 0)
rendered body_html counts: h2 4, h3 7, table 2, li 25, pre 1, checkbox 9, img 0, details 0
grep for login name and home path forms: no match (exit 1)
grep -niwE "driver|coder|inspector|verifier|debugger|investigator|griller|foreman|chantier|batch|round|CR|CR-[0-9]+": no match
grep -nE "STALE|UNVERIFIED|Review:|!\[|<img|user-attachments": no match
```

Sections follow `.github/pull_request_template.md`. No image is attached.

### S2. Behaviour table, "What changes" (but the CHANGELOG bullet), "Unchanged", example, decisions, blast radius: VERIFIED at 1a03994

Table "Before" values hold at `41fcd6d` and "after" values at `1a03994` (R1; the two new probe
outputs are identical to the earlier ones, `diff` prints nothing). Message and index: R1. Docs,
skills, schema: R2. S5, tests, feature map: R2 to R4. `generated.by`, `sources[].author`,
case-sensitive `human:`: R1. `okfkb` writes `bot:okf-schema`: R2. Example command: R5.
Blast radius: R1, R5; the two commits are the tip above `41fcd6d` (G2), and the CR's `src` diff
(`git diff 41fcd6d 1a03994 -- src`, read in full: `validator.py` and one schema line) adds no write.
Decisions: carried from 7a33d92: the move changed no behaviour they name and no answer file.

### S3. "Product surfaces" table (body lines 35-45): VERIFIED at 1a03994

```console
$ git diff --shortstat 41fcd6d 1a03994
15 files changed, 240 insertions(+), 30 deletions(-)       (all 15 status M)
CHANGELOG.md, docs (project-feature-coverage, validate-standalone-files, validation-codes),
examples/.../Base.schema.yaml, requirements (log.md, CORE-006), skills (okf-schema,
okfkb-record-findings), src (data/kb/_schema/Base.schema.yaml, validator.py), tests (api,
cli_remaining, kb_scaffold, okf2_compliance)
$ git diff 41fcd6d 1a03994 -- tests | grep -E "^-[^-]"
-def test_derive_trust_tier_malformed_actor_returns_unverified() -> None:
-    assert _derive_trust_tier(fm) == "unverified"
-def test_validate_okf2_verified_w10_malformed_actor(tmp_path: Path) -> None:
-    """W10: verified entry has malformed `by` actor string."""
-    _validate_okf2_verified(path, {"verified": [{"by": "Alice", "at": "2026-01-01"}]}, report)
-    assert any(f.code == "W10" for f in report.warnings)
```

Every row matches the diff: two existing tests changed, no file added or moved, `pyproject.toml`,
`justfile` and CI untouched (R2). "No recipe refreshes" the example schema: carried from 7a33d92
(R6).

### S4. Autonomous decision (braces in S5): VERIFIED

carried from 7a33d92: the move changed neither `CORE-006` nor the `okfreq` code (G2).

### S5. Known gaps: VERIFIED at 1a03994, first bullet to reword (below)

Bullet 1: no `versionchanged` note records the trust tier change (read `api.py:439-487`: the one
note, `0.18.2`, is about name resolution). Bullet 2: skill row line 367 says "it still counts as
machine-confirmed", the W10 section says the same of any non-empty actor, and `42` is warned W10
and stays `unverified` (R1). No `UNVERIFIED` mark (S1), no uncaptured pair, no accepted failed
claim without a bullet.

### S6. Checklist and Type of Change: VERIFIED at 1a03994

`just preflight` passes with no warning line (G3); tests fail on base and pass on head (R4);
documentation updated (R2). Title `fix(validate): count every OKF 0.2 actor form in the trust
tier`; bug fix and documentation match the diff (S3). Related Issues: `None`.

## Description facts at 1a03994 (for the refresh)

### Line 8

"Before is the base `2f09cef`, after is `7a33d92`." **False at 1a03994**: the base is `41fcd6d`,
the head `1a03994`. All "Before" values of the table hold at `41fcd6d`, all "after" values at
`1a03994` (R1).

### Lines 29-30, CHANGELOG bullet

"`CHANGELOG.md` carries the entries that `just changelog` [...] generates from the commit history:
this fix and the missing `v0.18.1` heading." **False at 1a03994** in its first part: the committed
file lacks one generated entry. The two items it names are there.

```console
$ uv cz changelog --dry-run | diff --strip-trailing-cr -B - <(git show 1a03994:CHANGELOG.md)
6d5
< - **show**: accept names without .md and stay inside the bundle        (exit 1)
$ git diff 41fcd6d 1a03994 -- CHANGELOG.md
adds "- **validate**: count every OKF 0.2 actor form in the trust tier",
"## v0.18.1 (2026-11-25)" and a "### Fix" heading (6 lines)
$ git show 41fcd6d:CHANGELOG.md | grep -c "^## v0.18.1"
0
$ git tag --points-at 2f09cef
v0.18.1
$ uv cz changelog --dry-run | diff --strip-trailing-cr -B - CHANGELOG.md   (uncommitted worktree file)
(no output, exit 0)
```

The missing line is the entry of the pull request below.

### Lines 38-45

All true at `1a03994` against `41fcd6d` (S3). 15 changed files.

### Lines 59-71

| Lines | Posted | Holds at 1a03994 | Proof |
|---|---|---|---|
| 59-60 | example at `7a33d92`: exit 0; `alice` exit 1, one W10 naming `verified entry [0]` twice; tier `machine-confirmed` | same results; only the SHA is stale | R5 |
| 61-62 | preflight at `7a33d92`: 1128 passed, 12 skipped, 95.58% | pass: **1153 passed, 12 skipped, 95.55%**, Sphinx `-W` succeeded | G3 |
| 63-64 | `okfreq validate` at `7a33d92`: 35 requirements, 0, 0 | **36 requirements**, 0 errors, 0 warnings | R3 |
| 65-67 | run at `1ae8870` failed 8, "the base `2f09cef`" the same 8; links now allowed | true as history; **`2f09cef` is no longer the base** (false word at this head) and `1ae8870` is no longer in the branch (now `ad55758`) | below |
| 68-69 | CI at `7a33d92` | same results at `1a03994`; only the SHA is stale | G4 |
| 71-73 | evidence status at `7a33d92` | holds: markers in `validator.py` (also `api.py:438`) and S5 in three test files, marked tests passed, `proposed` | R3, R4 |

```console
$ uv python -B <CR>/work/verifier/logs.py <CR>/work
gate 1ae8870: 8 failed, 1118 passed, 14 skipped; WinError 1314 lines: 8
base 2f09cef, links refused: 8 failed, 1094 passed, 14 skipped
base 2f09cef, links allowed: 1104 passed, 12 skipped
same failing tests, 1ae8870 and base: True 8
symlink probe on this host: file True | directory True
```

The base logs are tied to `2f09cef` by `<CR>/evidence/debugger-symlink-gate.txt`.

### Known gaps

Both facts hold (S5). Bullet 1 reads "without a `.. versionchanged::` note in its docstring":
since the move the docstring does carry a `.. versionchanged:: 0.18.2` note, from the pull request
below, about name resolution. The gap (no note about `trust_tier`) is real; the sentence read
literally is now **misleading** and should say "no note about this change".

### Every sentence false at 1a03994

1. Line 8, "Before is the base `2f09cef`, after is `7a33d92`."
2. Lines 29-30, "carries the entries that `just changelog` [...] generates" (one is missing).
3. Line 66, "the base `2f09cef`" (no longer the base).

Stale but not false (a dated result at an old SHA, with other numbers now): lines 61-64. Stale
SHA only: lines 59, 68, 71.

## Facts for the Driver, not failed claims

- PR 69 still targets `main`, so the forge shows 3 commits and 24 files, 9 of them and one commit
  (`41fcd6d`) from the pull request below, which the description does not mention. Judged against
  the CR's base, as the brief says; the forge stack has to fix it.

  ```console
  $ gh pr view 69 -R gsemet/okf-schema --json files,commits
  files: 24   commits: 3 (41fcd6d, ad55758, 1a03994)
  ```
- `CHANGELOG.md` stays modified and uncommitted in the worktree (G1); not touched.
- `requirements/tiers/log.md`, "Verification" of the trust tier entry, still records the run of
  `1ae8870` on the old base (1118 passed, 14 skipped, 8 failed): true history, not this head.
- Own scratch folder and the detached base worktree were removed; older files in `work/scratch/`
  were left.

## Verdict not recorded by the CLI

Run from the CR's worktree at `1a03994`, after this note was written:

```console
$ chantier verdict CR-104 VERIFIED --batch batch-01
error: CR-104: the worktree has uncommitted work: a verdict binds to a head, commit first
(exit 2)
```

The uncommitted work is the `CHANGELOG.md` line of G1, which the brief forbids restoring, staging,
committing or changing. Nothing was worked around: no verdict is recorded at `1a03994`.
