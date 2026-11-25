Head: 373fded7c3c4267dd7b58a2de484928f12f35ce2

# CR-104 "Trust tier: count the actor forms allowed by OKF 0.2": verification

**Verdict: VERIFIED** at `373fded`. The move from `1a03994` changed no file. The posted
description changed since it was last judged and was judged again; its dated lines (8 and 59-71)
still name old SHAs and are refreshed after this verdict (section "Facts at 373fded").

Base: `origin/main` `a371f73c2d925f217de47e4455f7eff455e8bb24`. Previous report, `VERIFIED` at
`1a03994` on base `41fcd6d`: `verifier/verify-1a03994.md` (full commands and outputs of the carried
claims). No gate was run in this worktree.

Placeholders: `<worktree>` is the CR's worktree, `<CR>` the CR folder. `uv ...` means
`uv --directory <worktree> run --no-sync -- ...`.

## Judged at 373fded

### M1. Head, tree, remote and PR: VERIFIED at 373fded

```console
$ git rev-parse HEAD
373fded7c3c4267dd7b58a2de484928f12f35ce2
$ git status --porcelain                      (at start and after the runs: no output)
$ git ls-remote origin <CR branch> refs/heads/main
373fded7c3c4267dd7b58a2de484928f12f35ce2   <CR branch>
a371f73c2d925f217de47e4455f7eff455e8bb24   refs/heads/main
$ gh pr view 69 --json headRefOid,baseRefName,isDraft,commits,files
head 373fded, base main, draft true, commits 13c3799 + 373fded, 15 files
$ git diff --name-status a371f73 373fded      (all 15 status M, the same 15 paths as the forge)
CHANGELOG.md, docs (project-feature-coverage, validate-standalone-files, validation-codes),
examples/.../Base.schema.yaml, requirements (log.md, CORE-006), skills (okf-schema,
okfkb-record-findings), src (data/kb/_schema/Base.schema.yaml, validator.py), tests (api,
cli_remaining, kb_scaffold, okf2_compliance)
$ git diff --shortstat a371f73 373fded
15 files changed, 240 insertions(+), 30 deletions(-)
```

The previous report's note that the forge showed 3 commits and 24 files no longer holds.

### M2. The move changed no file and not the patch: VERIFIED at 373fded

```console
$ git range-diff 41fcd6d..1a03994 a371f73..373fded
1:  ad55758 = 1:  13c3799 fix(validate): count every OKF 0.2 actor form in the trust tier
2:  1a03994 = 2:  373fded docs: add the trust tier fix to the changelog
$ git show <commit> | git patch-id --verbatim        (commit by commit)
3d23e568dc40fd13c8fe02c14757c6a5488a36e7  ad55758 and 13c3799
5b805476c80fa928386988be7e5ec0a156b175a0  1a03994 and 373fded
$ git rev-parse 41fcd6d^{tree} a371f73^{tree} 1a03994^{tree} 373fded^{tree}
1bb1122f0160bfdf63bfc5c6fb12036794354e6f   (41fcd6d)
1bb1122f0160bfdf63bfc5c6fb12036794354e6f   (a371f73)
d9165904cb6f3cdc95488dbfc4adb02bea1cffea   (1a03994)
d9165904cb6f3cdc95488dbfc4adb02bea1cffea   (373fded)
$ git diff --name-only 41fcd6d a371f73 | wc -l      0
$ git diff --name-only 1a03994 373fded | wc -l      0
$ gh pr view 68 --json state,headRefOid,mergeCommit,mergedAt
MERGED, head 41fcd6d, merge commit a371f73, 2026-11-25T22:43:09Z
```

Old and new base trees are identical, and so are old and new head trees. Every claim that rests
on file content is carried.

### M3. Long gate: VERIFIED, carried from 1a03994

Carried: same head tree and base tree (M2); `chantier handoff CR-104` shows
`[x] long gate passed carried from 1a03994 (clean rebase onto main)`.
`<CR>/work/gates/20261125-232725.log`:

```text
1:    gate CR-104 branch chantier/batch-01/cr-104-trust-tier-count-the-actor-forms-allowed head 1a03994e7bc2fbf1595cd6528a6f3c02a35542e2
2411: Required test coverage of 95% reached. Total coverage: 95.55%
2412: 1153 passed, 12 skipped in 198.61s
2643: build succeeded.
2646: result: pass at 1a03994e7bc2fbf1595cd6528a6f3c02a35542e2
```

### M4. Example command and `show_bundle` (spec evidence 5): VERIFIED at 373fded

```console
$ uv python -B <CR>/work/verifier/desc2/example.py <CR>/work/scratch/v373
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

### M5. Requirement checks and markers: VERIFIED at 373fded

```console
$ uv okfreq validate requirements --prose --check-links --project-root .
36 requirements, 0 errors, 0 warnings                                   (exit 0)
$ uv okfreq update-coverage requirements --check
0 files would change                                                    (exit 0)
$ git grep -n "implements_req SwRS-OKFSCHEMA-CORE-006" 373fded -- src
api.py:438, validator.py:356, :595, :736
$ git grep -c "tests_req SwRS-OKFSCHEMA-CORE-006#S5" 373fded -- tests
test_api.py:1, test_cli_remaining.py:1, test_okf2_compliance.py:7
$ git grep -n "req_lifecycle" 373fded -- <CORE-006>
11:req_lifecycle: proposed
```

### M6. CHANGELOG bullet (body lines 29-30) and Known gaps bullet 2 (lines 97-98): VERIFIED at 373fded

Both were rewritten after the previous judgment.

```console
$ git diff a371f73 373fded -- CHANGELOG.md
+- **validate**: count every OKF 0.2 actor form in the trust tier
+
+## v0.18.1 (2026-11-25)
+
+### Fix
+
$ git show a371f73:CHANGELOG.md | grep -c "^## v0.18.1"
0
$ git tag --points-at 2f09cef
v0.18.1
$ justfile, recipe preflight, line 29
    just changelog                      (recipe changelog, line 120: cz changelog)
$ uv cz changelog --dry-run | diff --strip-trailing-cr -B - <(git show 373fded:CHANGELOG.md)
6d5
< - **show**: accept names without .md and stay inside the bundle        (exit 1)
```

The two named additions are generated entries and are in the file. The only generated line it
lacks is the `show` fix of PR 68, which is what Known gaps says.

### M7. Posted description: rendering, privacy, form: VERIFIED at 373fded

```console
$ gh pr view 69 --json body --jq .body | diff --strip-trailing-cr -B - <CR>/work/pr-body.md
(no output, exit 0)
$ gh api .../pulls/69 (body_html), element count
h2 4, h3 7, table 2, li 26 (9 + 17), pre 1, checkbox 9, img 0, details 0
$ grep -niE "<login name>|[A-Z]:[\\/]Users|/home/|/Users/"          (no match, exit 1)
$ grep -niwE "driver|coder|inspector|verifier|debugger|investigator|griller|foreman|chantier|batch|round|CR|CR-[0-9]+"   (no match, exit 1)
$ grep -nE "STALE|UNVERIFIED|Review:|!\[|<img|user-attachments"      (no match, exit 1)
$ grep "^#" .github/pull_request_template.md
Description, Type of Change, Checklist, Related Issues   (all four in the body)
```

Login name and home folder's last part are the same word here. No image, no Review box.

### M8. Known gaps complete: VERIFIED at 373fded

Three bullets. No `**UNVERIFIED:**` claim (M7 grep). `verifier/evidence/before-after.md` names no
pair as not captured. The one description sentence the previous report found false and not exempt
(the CHANGELOG sentence) is rewritten and its gap listed (M6). Bullets 1 and 3 rest on `api.py`,
`validator.py`, the skill and the code reference, unchanged since `1a03994` (M2): carried.

## Carried from 1a03994 (or earlier): the move changed no file (M2)

| Claim | Verdict | Judged at, and proof (full output in `verifier/verify-1a03994.md`) |
|---|---|---|
| Runtime: actor pattern, tier, W10 message, `generated.by` and `sources[].author` unchecked | VERIFIED | 1a03994, R1: `probe.py` on base and head source |
| Docs, skills, scaffold, example schema, log heading; `README.md`, `pyproject.toml`, `justfile`, CI unaffected | VERIFIED | 1a03994, R2: `texts.py` all lines found; `git grep "bot:ci"` outside tests: no output; `git diff --stat` of the unaffected paths: no output |
| Requirements lint and trace | VERIFIED | 1a03994, R3: `okfreq lint --check`: 0 would change; `okfreq trace`: CORE-006 implemented and tested |
| Tests, spec evidence 1-4 | VERIFIED | 1a03994, R4: 320 passed; head tests on base source: 13 failed, 305 passed |
| Examples, spec evidence 6; an existing knowledge base keeps its schema copy | VERIFIED | 1a03994 and 7a33d92, R6 |
| Description: behaviour table, "What changes" other bullets, "Unchanged", blast radius | VERIFIED | 1a03994, S2 |
| Description: decisions of the maintainer; autonomous decision (braces in S5) | VERIFIED | 7a33d92, S2 and S4 |
| Description: "Product surfaces" table | VERIFIED | 1a03994, S3; file list and shortstat again at 373fded (M1) |
| Description: checklist, type of change, related issues | VERIFIED | 1a03994, S6 (preflight carried, M3) |
| Description lines 65-67: the earlier 8 symbolic link failures | VERIFIED | 1a03994, `logs.py` over the gate and base logs, files not touched by the move |
| Before and after pairs (`41fcd6d` to `1a03994`) | VERIFIED | 1a03994; hold for `a371f73` to `373fded`, identical trees; not captured again |

## CI at 373fded (reported, not a claim of the description yet)

```console
$ gh pr checks 69 --repo gsemet/okf-schema                 (2026-11-25T22:58:21Z, exit 0)
preflight (3.10) pass 4m2s, (3.11) pass 4m43s, (3.12) pass 2m55s, (3.13) pass 4m59s
cross-platform (macos-latest) pass 2m18s, cross-platform (windows-latest) pass 3m55s
tag-release skipping
run 45716966043
$ gh api repos/gsemet/okf-schema/commits/373fded7c3c4267dd7b58a2de484928f12f35ce2/check-runs
head_sha 373fded on the six listed before tag-release appeared (3.13 then in progress)
```

Earlier reads in this pass showed jobs still pending (`exit 8`); at the last read none is pending
or failed. `tag-release` is skipped: the workflow runs it on pushes to `main` only.

## Facts at 373fded for the description refresh (not failed)

| Body lines | Posted | At 373fded |
|---|---|---|
| 8 | base `41fcd6d` "the head of the pull request below this one", after `1a03994` | base `a371f73` (`main`, the merge of PR 68, same tree as `41fcd6d`), after `373fded`; all table values hold (M2) |
| 59-60 | example at `1a03994` | run again at `373fded`: same results (M4) |
| 61-62 | preflight at `1a03994` | not run at `373fded`; pass carried from `1a03994` after a clean rebase: 1153 passed, 12 skipped, 95.55%, Sphinx `-W` succeeded (M3) |
| 63-64 | `okfreq validate` at `1a03994` | run again at `373fded`: 36 requirements, 0 errors, 0 warnings (M5) |
| 65-67 | history of the first run | still true, names no SHA to change but `2f09cef` as history |
| 68-69 | CI at `1a03994` | see "CI at 373fded" |
| 71-73 | evidence status at `1a03994` | markers and `proposed` seen at `373fded` (M5); marked tests executed at `1a03994`, carried (M2) |
| 97-98 (not dated) | "the `show` fix of the pull request below" | true (M6), but that pull request (#68) is now merged into `main`: the wording is dated, as on line 8 |
