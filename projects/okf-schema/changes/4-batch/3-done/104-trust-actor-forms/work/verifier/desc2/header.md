Head: 7a33d920b46188821c4ebf73d008fbc12dcdf750

# CR-104 "Trust tier: count the actor forms allowed by OKF 0.2": verification

**Verdict: VERIFIED.** Second pass, on the posted PR description alone, after it was edited and
posted again. The two claims that failed in the first pass (D1, D2) now hold (P2, P3).

Every claim is judged at `7a33d92` (full SHA above). Base is
`2f09cef3e786d1696e42b5cb305d4a55111e7725`. The head and the base did not move between the two
passes, so the sections from "State and gates" on are carried from the first pass
(`carried from 7a33d92: no move of the head or the base`). Their description claims S1 to S9 are
re-checked below where the edit changed them.

Placeholders: `<worktree>` is the CR's worktree, `<CR>` the CR folder, `<scratch>` a folder under
`<CR>/work/scratch/` that was removed afterwards. `uv ...` means
`uv --directory <worktree> run --no-sync -- ...`. Files of this pass are in
`<CR>/work/verifier/desc2/`.

## Description pass (posted body)

### P1. Posted body, rendering, privacy, form: VERIFIED

```console
$ gh pr view 69 -R gsemet/okf-schema --json headRefOid -q .headRefOid
7a33d920b46188821c4ebf73d008fbc12dcdf750
$ git rev-parse HEAD; git status --porcelain | wc -l
7a33d920b46188821c4ebf73d008fbc12dcdf750
0
$ gh pr view 69 -R gsemet/okf-schema --json body -q .body | diff --strip-trailing-cr -B - desc2/posted-body.md
(no output, exit 0)
$ diff --strip-trailing-cr -B desc2/posted-body.md <CR>/work/pr-body.md
(no output, exit 0)
$ gh api repos/gsemet/okf-schema/pulls/69 -H 'Accept: application/vnd.github.html+json' -q .body_html   (counted)
h2: 4, h3: 7, table: 2, li: 25, pre: 1, checkbox: 9, img: 0, details: 0
$ grep -niE "<login or home path forms>" desc2/posted-body.md
(no output, exit 1)
$ grep -niwE "driver|coder|inspector|verifier|debugger|investigator|griller|foreman|chantier|batch|round|CR|CR-[0-9]+" desc2/posted-body.md
(no output, exit 1)
$ grep -cE "STALE|UNVERIFIED|Review:" desc2/posted-body.md
0
$ grep -nE '!\[|<img|user-attachments' desc2/posted-body.md
(no output, exit 1)
```

Sections follow `.github/pull_request_template.md`. Both tables, the lists and the code block
render. The source's hard-wrapped lines show as line breaks between words, all text legible. No
image is attached.

### P2. Each result names its SHA (was D1): VERIFIED

```console
$ grep -noE '\b[0-9a-f]{7,40}\b' desc2/posted-body.md
8:2f09cef
8:7a33d92
59:7a33d92
61:7a33d92
63:7a33d92
65:1ae8870
66:2f09cef
68:7a33d92
71:7a33d92
```

Line 8 dates the before/after table, 59 the example command, 61 `just preflight`, 63 `okfreq
validate`, 68 CI, 71 the evidence status: all at the head or the base. Lines 65 and 66 report an
earlier failed run at `1ae8870` and the base, as history that the head's pass supersedes.

### P3. "new tests, and two existing trust tier tests updated" (was D2): VERIFIED

```console
$ git diff 2f09cef 7a33d92 --numstat -- tests
16  0  tests/test_api.py
36  0  tests/test_cli_remaining.py
20  0  tests/test_kb_scaffold.py
87  6  tests/test_okf2_compliance.py
$ git diff 2f09cef 7a33d92 -- tests | grep -E "^-[^-]"
-def test_derive_trust_tier_malformed_actor_returns_unverified() -> None:
-    assert _derive_trust_tier(fm) == "unverified"
-def test_validate_okf2_verified_w10_malformed_actor(tmp_path: Path) -> None:
-    """W10: verified entry has malformed `by` actor string."""
-    _validate_okf2_verified(path, {"verified": [{"by": "Alice", "at": "2026-01-01"}]}, report)
-    assert any(f.code == "W10" for f in report.warnings)
```

Exactly two existing tests changed. The first is renamed and now expects `machine-confirmed`; the
second is parametrized and asserts `[codes] == ["W10"]` and no error (R4, D2 extract of the first
pass). The rest of the row: all 15 changed files are modified, none added or moved, and
`pyproject.toml`, `justfile` and CI have no diff (S2).

### P4. Example command result at `7a33d92`: VERIFIED

```console
$ uv python -B desc2/example.py <scratch>
=== by: reference_agent/gemini-2.5-pro -> exit 0
All files validated successfully (0 errors, 0 warnings).
W10 findings: 0 | 'verified entry [0]': 0
show_bundle trust_tier: machine-confirmed
=== by: alice -> exit 1
  WARNING [W10] File '<scratch>\c.md': verified entry [0] has malformed 'by' value 'alice'. [...]
  Fix: correct the 'by' value in verified entry [0].
Validation failed: 0 error(s), 1 warning(s) (strict mode).
W10 findings: 1 | 'verified entry [0]': 2
show_bundle trust_tier: machine-confirmed
scratch removed: True
```

### P5. `just preflight`, `okfreq validate`, first run, base, links: VERIFIED

```console
$ grep ... <CR>/work/gates/20261125-224645.log
gate CR-104 ... head 7a33d920b46188821c4ebf73d008fbc12dcdf750
Required test coverage of 95% reached. Total coverage: 95.58%
1128 passed, 12 skipped in 104.77s
uv run --no-sync -- sphinx-build -W -b html docs/source docs/_build/html
build succeeded.
result: pass at 7a33d920b46188821c4ebf73d008fbc12dcdf750
$ uv okfreq validate requirements --prose --check-links --project-root .
35 requirements, 0 errors, 0 warnings
$ uv python -B <scratch>/logs.py <CR>/work          (copy of verifier/logs.py)
gate 1ae8870: 8 failed, 1118 passed, 14 skipped; result: FAIL; lines with WinError 1314: 8
base 2f09cef, links refused: 8 failed, 1094 passed, 14 skipped
base 2f09cef, links allowed: 1104 passed, 12 skipped
same failing tests, 1ae8870 and base: True 8
symlink probe on this host: file True | directory True
```

The base logs are tied to `2f09cef` by `<CR>/evidence/debugger-symlink-gate.txt` (S5).

### P6. CI at `7a33d92`: VERIFIED

```console
$ gh api repos/gsemet/okf-schema/commits/7a33d920b46188821c4ebf73d008fbc12dcdf750/check-runs
preflight (3.10) success, (3.11) success, (3.12) success, (3.13) success
cross-platform (macos-latest) success, cross-platform (windows-latest) success
tag-release skipped                                    (head_sha 7a33d92 on all seven)
$ sed -n 83,85p .github/workflows/ci.yml
  tag-release:
    needs: [preflight, cross-platform]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

### P7. Evidence status at `7a33d92`: VERIFIED

```console
$ git grep -nE "implements_req SwRS-OKFSCHEMA-CORE-006|tests_req SwRS-OKFSCHEMA-CORE-006#S5" 7a33d92 -- src tests
implements_req: api.py:375, validator.py:356, :595, :736
tests_req S5: test_api.py:621, test_cli_remaining.py:323,
              test_okf2_compliance.py:48, :54, :74, :80, :436, :452, :469
$ uv okfreq trace requirements --json        (exit 0, CORE-006)
implemented: api.py, validator.py; tested: test_api.py, test_cli_remaining.py, test_okf2_compliance.py
$ uv pytest -o addopts= -p no:cacheprovider -v --no-header tests/test_okf2_compliance.py \
    tests/test_api.py tests/test_cli_remaining.py -k "actor or trust_tier or verified"
45 passed, 219 deselected          (every S5-marked test listed PASSED)
$ grep -n "req_lifecycle" SwRS-OKFSCHEMA-CORE-006.md
11:req_lifecycle: proposed
```

### P8. Summary, table, changes, surfaces, decisions, blast radius: VERIFIED

Carried from 7a33d92 (no move): the behaviour table and message (R1), `show` and the API (R5),
docs, skills, schema, README and guideline (R2), requirement and feature map (R3), examples (R6),
delivered files all mentioned (S2), decisions and blast radius (S4), autonomous decision (S7).
Re-run at the head for the `CHANGELOG.md` bullet:

```console
$ uv cz changelog --dry-run | diff --strip-trailing-cr -B - CHANGELOG.md
(no output, exit 0)
$ sed -n 21,34p justfile     (extract of the preflight recipe)
    just changelog
$ git status --porcelain | wc -l
0
```

### P9. Known gaps and checklist: VERIFIED

Both bullets hold (S8). D1 and D2 were fixed, not accepted, so they need no bullet; no
`UNVERIFIED` mark (P1) and no uncaptured pair (`verifier/evidence/before-after.md`). Checklist
boxes: S9, with the gate log of P5.

## Wording notes (not failed claims)

- "two existing trust tier tests": by the test file's section headers, the second one
  (`test_validate_okf2_verified_w10_malformed_actor`) sits under `_validate_okf2_verified` and
  checks W10, not the tier. It carries the same S5 marker, and the parenthesis describes each
  change correctly.
- "teach the OKF 0.2 forms instead of `bot:ci`": at the base, `bot:ci` itself was in the two
  schema files and `validator.py`; the reference page, how-to row and skills showed
  `<prefix>:<identifier>` or `bot:collector` (`git grep -nE "bot:[a-z]" 2f09cef`). At the head
  `git grep -n "bot:ci" 7a33d92 -- . ':!tests'` finds nothing (exit 1) and all four teach the
  OKF 0.2 forms.

