# CR-101 verification

Head: 41fcd6dbebaddff719c2a3f54f610298034d0ad6

Verdict: NOT VERIFIED (description pass on the text posted at 22:13:47Z, section 17; one claim failed). Sections 1 to 13 stand.

- Base: `2f09cef3e786d1696e42b5cb305d4a55111e7725`. PR: https://github.com/gsemet/okf-schema/pull/68.
- Every claim below is judged at head `41fcd6dbebaddff719c2a3f54f610298034d0ad6` (written "head"). None is carried.
- Host: Windows 11, Python 3.12.10, symbolic links permitted.
- Paths: `<worktree>` is the CR worktree, `<disposable>` and `<probe>` are throwaway folders.
- Evidence files are in `work/verifier/evidence/`; `before-after.md` lists the pairs. The scenario
  steps of the specification were run again at the head (the older files in `evidence/` are not
  relied on).

## 1. Pushed head, clean tree: VERIFIED

```text
$ git rev-parse HEAD
41fcd6dbebaddff719c2a3f54f610298034d0ad6
$ git ls-remote origin refs/heads/chantier/batch-01/cr-101-show-resolve-concept-names-without-md-st
41fcd6dbebaddff719c2a3f54f610298034d0ad6  refs/heads/chantier/batch-01/cr-101-...
$ git status --porcelain --untracked-files=normal     (after all checks)
(empty)
$ gh pr view 68 --repo gsemet/okf-schema --json headRefOid,baseRefName,baseRefOid,state,isDraft
41fcd6dbebaddff719c2a3f54f610298034d0ad6 / main / 2f09cef3e786d1696e42b5cb305d4a55111e7725 / OPEN / true
```

## 2. Long gate passed at the head: VERIFIED

First line of `work/gates/20261125-224210.log`, then its test and result lines:

```text
gate CR-101 branch chantier/batch-01/cr-101-show-resolve-concept-names-without-md-st head 41fcd6dbebaddff719c2a3f54f610298034d0ad6
================ 1129 passed, 12 skipped in 113.53s (0:01:53) =================
result: pass at 41fcd6dbebaddff719c2a3f54f610298034d0ad6
$ chantier handoff CR-101
gates before handback ready, at the PR's head 41fcd6dbebaddff719c2a3f54f610298034d0ad6 (...)
  [x] long gate passed (gate CR-101 preflight; ...)
```

## 3. CI green at the head, symlink tests run: VERIFIED

```text
$ gh run view 45707397365 --repo gsemet/okf-schema --json headSha,status,conclusion,jobs
41fcd6dbebaddff719c2a3f54f610298034d0ad6 completed success
cross-platform (macos-latest) success; cross-platform (windows-latest) success;
preflight (3.10), (3.11), (3.12), (3.13) success; tag-release skipped
$ grep -n -E "=+ [0-9]+ passed.*in [0-9.]+s" work/ci-45707397365.log
macos 1141 passed; 3.10 1141 passed; 3.11 1141 passed; windows 1129 passed, 12 skipped;
3.12 1141 passed; 3.13 1141 passed
$ grep test_show_bundle_(refuses_a_symlink|follows_a_symlink|accepts_a_disk_path_spelled|reports_a_symlink_loop) <log>, counted per job
7 PASSED on each of the six jobs, cross-platform (windows-latest) and (macos-latest) included
$ grep -c "test_show_bundle_[a-z_]*symlink[^ ]* SKIPPED" <log>
0
```

## 4. Acceptance test of `show` on the installed package (specification test 14): VERIFIED

The diff adds `inspect("show", "--path", str(bundle), "concepts/clock")` with the assertion on
`"The clock ticks."`. It is skipped on Windows and passes on the other jobs:

```text
$ grep test_inspection_reports_matching work/ci-45707397365.log
1073   cross-platform (macos-latest)    PASSED  tests/test_acceptance_core.py::test_inspection_reports_matching_concepts_and_changes_no_file
4104   preflight (3.10)                 PASSED  (same test)
7521   preflight (3.11)                 PASSED
10335  cross-platform (windows-latest)  SKIPPED
14069  preflight (3.12)                 PASSED
17491  preflight (3.13)                 PASSED
```

## 5. A name with or without `.md`, exact file first, a directory never shown: VERIFIED

`before-show.txt` / `after-show.txt` (`okf-schema show --path my-knowledge-base/bundle <name>`):

```text
api/health-check  before: Error: Concept not found, exit 2     after: concept shown, exit 0
api (directory)   before: Traceback ... PermissionError, exit 1 after: Error: Concept not found: <disposable>\my-knowledge-base\bundle\api, exit 2
.                 before: Traceback ... PermissionError, exit 1 after: Error: Concept not found, exit 2
```

"Exact file first" and "`api` reads `api.md` beside `api/`" are tests 2 and 3, passing (claim 9).

## 6. Names read from the bundle root; absolute disk path inside accepted: VERIFIED

```text
/api/health-check                      before: not found C:\api\health-check, exit 2   after: shown, exit 0
/etc/passwd                            after: Error: Concept not found: <disposable>\my-knowledge-base\bundle\etc\passwd, exit 2
<disposable>\...\api\health-check.md   after: shown, exit 0
api/../api/health-check.md             after: shown, exit 0
```

Any terminal folder: `test_show_show_reads_names_from_the_bundle_root` (changes the working folder)
passes (claim 9).

## 7. Paths and links leaving the bundle refused without being read; exit 2, no traceback: VERIFIED

```text
$ okf-schema show --path my-knowledge-base/bundle <name>     (after-show.txt)
../../secret.md, <disposable>\secret.md, leak.md   before: SECRET-MARKER printed, exit 0
                                                   after: Error: Concept path is outside the bundle: <name> (bundle: ...), exit 2
../../secret, ../../missing, leak, \api\health-check   after: same "outside the bundle" error, exit 2
$ uv run --no-sync --project <worktree> -- python -X utf8 -B probe.py     (after-probe-names.txt)
'../..', 'away/secret', 'away/missing', 'rel-leak', 'chain', 'dangling.md', 'junction/secret.md',
'junction', absolute outside, UNC and other-drive names:
  api: FileNotFoundError: Concept path is outside the bundle ...
  cli: exit=2 exception=SystemExit files_read=0 outside_read=0
'', '.', '/', 'sub', 'dangling', 'loop', 'loop/x', 'NUL', 'CON', 'a*b', very long names:
  api: FileNotFoundError: Concept not found ...
  cli: exit=2 exception=SystemExit files_read=0 outside_read=0
```

The probe ran on Windows only; POSIX behaviour rests on the tests of claims 3 and 9. In the code,
`target.read_text` comes after `_require_inside_bundle(bundle, _real_path(target), concept_path)`
(`src/okf_schema/api.py`, `show_bundle`); that helper carries
`# @implements_req SwRS-OKFSCHEMA-CORE-010`, and `show_bundle` carries CORE-005 and keeps CORE-006:

```text
$ grep -rn -E "@implements_req SwRS-OKFSCHEMA-CORE-(005|006|010)" src
src/okf_schema/api.py:135:# @implements_req SwRS-OKFSCHEMA-CORE-010
src/okf_schema/api.py:399:# @implements_req SwRS-OKFSCHEMA-CORE-005
src/okf_schema/api.py:437:# @implements_req SwRS-OKFSCHEMA-CORE-005
src/okf_schema/api.py:438:# @implements_req SwRS-OKFSCHEMA-CORE-006
src/okf_schema/cli.py:705:    # @implements_req SwRS-OKFSCHEMA-CORE-005
src/okf_schema/validator.py:722:# @implements_req SwRS-OKFSCHEMA-CORE-006
src/okf_schema/_internal/utils.py:210:# @implements_req SwRS-OKFSCHEMA-CORE-005
```

## 8. Specification scenario steps and `show --help`: VERIFIED

`after-scenario-powershell.txt` and `after-scenario-git-bash.txt`:

```text
PS> show api/health-check, /api/health-check        concept shown, exit 0
PS> show /etc/passwd, api                           Concept not found (path inside the bundle), exit 2
PS> show ../../secret, \api\health-check            Concept path is outside the bundle, exit 2
PS> show .   (bundle.md beside the bundle)          Concept path is outside the bundle: ., exit 2
bash$ show /api/health-check                        outside the bundle: C:/Program Files/Git/api/health-check, exit 2
bash$ MSYS_NO_PATHCONV=1 show /api/health-check     concept shown, exit 0
PS> show --help   "The concept name starts from the bundle root (a leading ``/`` is allowed), the
                  ``.md`` extension is optional, and a path outside the bundle is refused."
                  Examples: ... concepts/clock.md and ... concepts/clock, exit 0
```

## 9. Tests: present, pass at the head, fail on the previous code: VERIFIED

Specification tests 1 to 14 and the edge-case change are in the diff
(`tests/test_api.py`, `test_cli_remaining.py`, `test_edge_cases.py`, `test_acceptance_core.py`;
`# pragma: no cover` removed from the `show` except line in `cli.py`).

```text
Both runs: pytest tests/test_api.py tests/test_cli_remaining.py tests/test_edge_cases.py
           -k "show_bundle or show_show or parent_references"   (full command: line 2 of each file)
head sources, `uv run --no-sync -- pytest` (after-tests.txt):
  37 passed, 189 deselected (symlink cases and link loop PASSED)
base sources, head tests, `python -B -m pytest -o pythonpath=src` (before-tests.txt):
  22 failed, 15 passed, 189 deselected
$ uv run --no-sync -- pytest tests/test_api.py tests/test_cli_remaining.py tests/test_acceptance_core.py tests/test_edge_cases.py --no-cov -p no:cacheprovider -rs -q -k "show or path_edge_cases or inspection" -v
43 passed, 1 skipped, 189 deselected   (skip: acceptance test, "run the installed POSIX console scripts")
$ uv run --no-sync -- pytest --doctest-modules src/okf_schema/api.py -k "show_bundle or _require_inside_bundle" --no-cov -p no:cacheprovider -q
2 passed, 5 deselected
```

## 10. Requirements: VERIFIED

```text
$ uv run --no-sync -- okfreq update-coverage requirements --check
0 files would change                                   (exit 0)
$ uv run --no-sync -- okfreq validate requirements --prose --check-links --project-root .
36 requirements, 0 errors, 0 warnings                  (exit 0)
$ uv run --no-sync -- okfreq lint requirements --check --check-links --project-root .
0 indexes would change / 0 requirement OKF projections would change   (exit 0)
$ uv run --no-sync -- okfreq trace requirements --json   (exit 0; missing_ids [], warnings [])
implemented CORE-010: src/okf_schema/api.py
implemented CORE-005: _internal/utils.py, api.py, cli.py
tested CORE-010: tests/test_api.py, test_cli_remaining.py, test_edge_cases.py
tested CORE-005: tests/test_api.py, test_cli_remaining.py
$ grep -rn "@tests_req SwRS-OKFSCHEMA-CORE-010" tests
#S1 test_api.py 734, 748, 766, 826, test_cli_remaining.py 159
#S2 test_api.py 787, 846
#S3 test_api.py 767, 788, 837, 867, test_edge_cases.py 280
$ git diff 2f09cef 41fcd6d -- requirements/...
CORE-005: + depends_on CORE-010, scenarios S3 and S4, S2 widened with "a directory",
          criteria extended, Links "Depends on: SwRS-OKFSCHEMA-CORE-010"; description unchanged
StRS-OKFSCHEMA-CORE-002: derived_by + CORE-010; swrs/core/index.md lists CORE-010
$ cat requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-010.md
proposed, derives from StRS-OKFSCHEMA-CORE-002, description equal to the normative sentence,
S1 to S3, known issue line, the Q13 and Q14/Q16 boundary lines, verification notes
```

## 11. Requirement log entry: VERIFIED (see point A)

`requirements/tiers/log.md`, entry `## 2026-11-25`, names both requirements, the change, the reason
and verification results, and no ticket. Its preflight figures match the first gate run at this
head:

```text
work/gates/20261125-222650.log
gate CR-101 branch ... head 41fcd6dbebaddff719c2a3f54f610298034d0ad6
=========== 8 failed, 1112 passed, 21 skipped in 102.02s (0:01:42) ============
result: FAIL just preflight (exit 1) at 41fcd6d
log.md: "`just preflight` stops at its test step: 1112 tests pass, 21 are skipped, and 8 tests of
other capabilities fail because this host does not permit symbolic links (WinError 1314)."
```

## 12. Human documentation, packaged skill, unaffected surfaces: VERIFIED

```text
$ git diff --stat 2f09cef 41fcd6d
13 files changed, 670 insertions(+), 12 deletions(-)
(docs/source/reference/cli.md, 5 files under requirements/tiers/, skills/okf-schema/SKILL.md,
api.py, cli.py, 4 test files)
$ git diff 2f09cef 41fcd6d -- docs/source/reference/cli.md skills/okf-schema/SKILL.md
cli.md: CONCEPT_PATH forms, `.md` optional, both errors, exit 2, one example per form, absolute-path
recognition, limits: letter case, leading `\` on Windows, Git Bash and MSYS_NO_PATHCONV=1
SKILL.md row: "`.md` is optional; names start from the bundle root (a leading `/` is allowed);
paths and symlinks leaving the bundle are refused (exit 2)"
$ git diff 2f09cef 41fcd6d -- src/okf_schema/data examples docs/source/tutorials docs/source/explanation .github justfile pyproject.toml uv.lock CHANGELOG.md README.md
(empty)
$ git grep -n -E "okf-schema show|show --path" 41fcd6d -- src/okf_schema/data examples docs/source/tutorials skills README.md
docs/source/tutorials/getting-started.md:89   show ... api/health-check
docs/source/tutorials/knowledge-graph.md:94   show ... runbooks/service-unavailable
skills/okf-schema/SKILL.md:135                (the table row above)
$ git grep -n -i -w show 41fcd6d -- docs/source/explanation/project-feature-coverage.md
line 31, CORE-006: "... covers `stale` in `list`/`show`."   (unchanged behaviour)
pyproject.toml: include = ["src/okf_schema", "skills"], "skills" = "okf_schema/skills" (skill shipped)
```

## 13. Commit: VERIFIED

```text
$ git log --format="%H%n%B" 2f09cef..41fcd6d      (one commit)
fix(show): accept names without .md and stay inside the bundle
... Paths and symbolic links that leave the bundle are refused.
Assisted-by: Claude:Sonnet-5.5 / Co-Authored-By trailer; no "!", no "BREAKING CHANGE:", no version bump
```

## 14. Description, `work/pr-body.md`: VERIFIED

| Statement | Proof (head unless said) |
|-----------|--------------------------|
| Before: extensionless name not found, directory traceback, `../` or link reads outside | `before-show.txt` at base 2f09cef (claims 5, 7) |
| The tutorials use that form | claim 12, `git grep` |
| The four behaviour bullets | claims 5, 6, 7 |
| Behaviour to know: outside reads now fail; `\` on Windows; Git Bash; documented | claims 7, 8, 12 |
| CORE-010 proposed, `show` only; CORE-005 scenarios and dependency | claim 10 |
| Reference and packaged skill updated; unaffected surfaces | claim 12 |
| Type: bug fix and documentation | claims 12, 13 |
| `just preflight` passes | claim 2 |
| Tests added that prove the fix; documentation updated | claims 9, 12 |
| Autonomous decisions: `realpath`, loop test; placeholders | below |
| Known gap: other commands follow outside links | below |
| Fixes #56 | `gh issue view 56`: OPEN, "`okf-schema show` fails on extensionless concept names used in the Getting Started tutorial" |

```text
$ uv run --no-project --no-python-downloads --python <v> -- python -B loop.py
3.11.18 | Path.resolve() raised RuntimeError | os.path.realpath() returned
3.12.10 | Path.resolve() raised RuntimeError | os.path.realpath() returned
3.13.18 | Path.resolve() returned | os.path.realpath() returned
$ gh api "repos/python/cpython/contents/Lib/pathlib.py?ref=3.10" -H "Accept: application/vnd.github.raw" | grep -A14 "def resolve(self"
if e.errno == ELOOP or winerror == _WINERROR_CANT_RESOLVE_FILENAME:
    raise RuntimeError("Symlink loop from %r" % e.filename)
(3.10 is not installed here: read from its source, not run)
test_show_bundle_reports_a_symlink_loop_as_not_found PASSED (after-tests.txt)

$ okfreq validate requirements --prose      (on a copy with "<path> (bundle: <bundle>)" in CORE-010)
36 requirements, 0 errors, 5 warnings, among them
W002 ...SwRS-OKFSCHEMA-CORE-010.md: body has no filled EARS expression
(the other 4 are W004, the copy holding no tests; the real tree: 0 warnings, claim 10)

$ okf-schema <command> --path kb/bundle     (after-other-commands.txt; bundle/leak.md links outside)
validate: reads leak.md   list: leak.md Concept OUTSIDE-MARKER
backlinks: api/health-check.md <- leak.md   lint --check: Would lint: ...leak.md
index: writes "[OUTSIDE-MARKER](leak.md)" into index.md
```

The body keeps the project's template (which has no SHA field; the proofs above are at the head),
adds Autonomous decisions and Known gaps, carries no image, no STALE and no UNVERIFIED mark. The
"no new warnings" box is unchecked, so nothing is claimed by it. No evidence pair is missing and no
claim failed, so no further Known gaps bullet is owed.

## 15. Description as posted on PR 68: VERIFIED (see point B)

```text
$ gh pr view 68 --repo gsemet/okf-schema --json headRefOid,updatedAt,body
41fcd6dbebaddff719c2a3f54f610298034d0ad6  2026-11-25T21:50:35Z
$ diff --strip-trailing-cr work/pr-body.md <(gh pr view 68 --repo gsemet/okf-schema --json body --jq .body)
(one added line under Known gaps, and a trailing blank line)
+- **UNVERIFIED:** the installed-package inspection check. The acceptance tests are skipped on Windows; its new assertion needs a non-Windows run.
```

Otherwise the posted text is the file judged in claim 14: it renders as plain sections and lists,
holds no image, matches the diff, and its one UNVERIFIED item sits in Known gaps.

## Points for the Driver (no claim failed)

- A. The log entry (claim 11) records the run made while the host refused symbolic links. It is
  accurate for that run, but does not mention the later passing gate at the same head. Changing it
  would move the head.
- B. The posted body still marks the acceptance check UNVERIFIED; claim 4 now proves it. Post
  `work/pr-body.md` (or the final body) before the description pass.

## 16. Description pass, PR 68 as posted after the edit: NOT VERIFIED

Replaces the judgments of sections 14 and 15 on the description, and settles point B. Judged at
head `41fcd6dbebaddff719c2a3f54f610298034d0ad6`; the head has not moved, so sections 1 to 13 are
the proofs cited here (code claims, gate and CI not run again).

```text
$ gh pr view 68 --repo gsemet/okf-schema --json headRefOid,updatedAt,isDraft,body
41fcd6dbebaddff719c2a3f54f610298034d0ad6  2026-11-25T22:10:19Z  isDraft true
$ diff --strip-trailing-cr work/pr-body.md <(gh pr view 68 --repo gsemet/okf-schema --json body --jq .body)
101a102
>            (one trailing blank line only)
$ gh api repos/gsemet/okf-schema/pulls/68 -H "Accept: application/vnd.github.html+json" --jq .body_html
9 h2 sections, 3 task lists, one 3-column table with 7 rows, "Fixes #56" linked, no image
```

### 16.1 FAILED: "still accept an absolute disk path inside the bundle"; a delivered change is unmentioned

The Description states this without exception, and "Behaviour to know" and "Known gaps" are
silent on it. On a case-insensitive file system such as macOS, an absolute path whose bundle part
is spelled in another case than the real path of `--path` was read before and is now answered
"Concept not found". The PR documents this itself, and the user accepted it as a limit (answer 13),
but the description lists the other two limits of the command reference only (leading `\`, Git
Bash), then says "The command reference documents these limits".

```text
$ git diff 2f09cef 41fcd6d -- docs/source/reference/cli.md        (section "Limits", first bullet)
+- Following links does not change letter case. On a case-insensitive file system
+  such as macOS, an absolute `CONCEPT_PATH` whose bundle part is spelled in
+  another case than the real path of `--path` (...) is not recognized as inside the bundle:
+  it is read from the bundle root and reported as `Error: Concept not found: ...`.
$ git grep -n -A3 -F "target = bundle / concept_path" 2f09cef -- src/okf_schema/api.py
392:    target = bundle / concept_path        (an absolute path replaces the bundle)
393-    if not target.exists():               (true for another letter case on such a file system)
$ grep -i case work/pr-body.md
(no match)
02-answers.md, 13: "the refusal of an absolute path spelled in another case than `--path` is
accepted and written in the command reference."
```

Basis: the command reference, the base code and the head code (`_is_disk_path_in_bundle` compares
real paths, letter case kept). Not run on macOS. A wording proved by the diff: under "Behaviour to
know" or "Known gaps", "the command reference documents that on a case-insensitive file system
such as macOS, an absolute path whose bundle part is spelled in another letter case than the real
path of `--path` is not recognized and is reported as not found".

### 16.2 Every other statement: VERIFIED

| Posted statement | Proof |
|------------------|-------|
| Description, first paragraph | `before-show.txt` (base 2f09cef); tutorials: claim 12 |
| Bullets 1, 3, 4, and the rest of bullet 2 | claims 5, 6, 7 |
| Behaviour to know: outside reads fail; `\`; Git Bash; documented | claims 7, 8, 12 |
| CORE-010 and CORE-005 | claim 10 |
| Reference and skill updated; unaffected surfaces | claim 12; `grep` of `examples/` for a `show` run or `show_bundle`: no match |
| Deliverables: intro and table rows 1 to 7 | `before-show.txt`, `after-show.txt` (SHAs, link, exit codes match each row) |
| Deliverables: `bundle.md` beside `bundle` | `after-scenario-powershell.txt`; test `root_with_a_file_beside_it_is_outside` PASSED |
| Type of Change; Checklist ticks | claims 2, 9, 12, 13; "no new warnings" unticked, nothing claimed |
| Autonomous decisions (both) | claim 14 outputs, same head |
| Known gap 1: other commands follow links | `after-other-commands.txt` |
| Known gap 2: log entry and the later run | claim 11; gate 20261125-222650 FAIL and 20261125-224210 pass, both at 41fcd6d |
| Test plan: 22 of 37 fail at base, 37 pass at head | `before-tests.txt` "22 failed, 15 passed"; `after-tests.txt` "37 passed" |
| Test plan: preflight, 1129 passed, 12 skipped acceptance | gate log lines 1, 46-68 (12 SKIPPED, all `test_acceptance_*`), 2364, 2601; `tests/conftest.py:16` skips on win32 |
| Test plan: evidence before 2f09cef, after 41fcd6d | `before-after.md` header; "Every pair of the evidence plan was captured" |
| Test plan: Review approved at 41fcd6d | note 21:26:46 "r1 approved at 2f09cef..., committed as 41fcd6d" (`log CR-101`) |
| Test plan: Verified at 41fcd6d | event 22:07:51 "verdict result=VERIFIED head=41fcd6d..." (cancelled by this pass until a later VERIFIED) |
| Test plan: CI green, jobs, tag-release, symlink and acceptance tests | claims 3, 4; `ci.yml:85` `if: ... github.ref == 'refs/heads/main'`; 14 symlink or link-loop tests PASSED on each of the six jobs; the 12 Windows skips are all acceptance |
| Related Issues; Internal references | claim 14 (issue 56); the nine named files exist in `work/verifier/evidence/` |
| Form: project template kept; no STALE, no UNVERIFIED, no image; CR name only in Internal references | posted body and `.github/pull_request_template.md` |

## 17. Description pass, PR 68 as posted at 22:13:47Z: NOT VERIFIED

Judged at head `41fcd6dbebaddff719c2a3f54f610298034d0ad6`; the head has not moved.

```text
$ gh pr view 68 --repo gsemet/okf-schema --json headRefOid,updatedAt,isDraft
41fcd6dbebaddff719c2a3f54f610298034d0ad6  2026-11-25T22:13:47Z  isDraft true
$ git rev-parse HEAD ; git ls-remote origin refs/heads/chantier/batch-01/cr-101-...
41fcd6dbebaddff719c2a3f54f610298034d0ad6   (both; git status --porcelain: empty)
$ diff before.md now.md      (userContentEdits: revision judged in section 16, and the newest)
22,23c22,26   only the "Behaviour to know" paragraph: one sentence added, "these limits" rewrapped
$ diff posted.md now.md      same
$ gh api .../pulls/68 body_html: 9 h2, 1 table, no img, no STALE, no UNVERIFIED
```

### 17.1 FAILED: "On a case-insensitive file system such as macOS, an absolute path ... in another letter case ... is not recognized as inside the bundle and is reported as not found"

The sentence covers every case-insensitive file system. On Windows (NTFS, case-insensitive) such a
path is recognized and the concept is shown. Section 16.1 proposed this wording; it is too broad.

```text
$ uv run --no-sync -- python -B probe_case.py     (throwaway under work/scratch, removed; bundle
  folder "mixedcasebundle", show_bundle(bundle, <parent>/MIXEDCASEBUNDLE/<name>))
clock.md -> '# Clock'
clock -> '# Clock'
$ uv run --no-sync -- python -B -c "... PurePosixPath / PureWindowsPath equality of KB and kb"
posix False
windows True
```

The macOS case rests on the code (`_is_disk_path_in_bundle` compares real paths; POSIX equality
keeps letter case) and the base code (`target = bundle / concept_path`, section 16.1); not run on
macOS. A narrower wording that matches these proofs: "On macOS with its default case-insensitive
file system, ... (on Windows such a path is still read)". The command reference
(`docs/source/reference/cli.md`, "Limits") uses the same broad phrase "such as macOS"; the
description repeats it faithfully. Changing the reference would move the head.

The rest of the paragraph is VERIFIED: outside reads now fail, `\` on Windows, Git Bash (claims 7,
8, 12); "documents these limits": the three bullets of "Limits" and "Errors" in
`git diff 2f09cef 41fcd6d -- docs/source/reference/cli.md`.

### 17.2 Unchanged statements: VERIFIED, carried from section 16.2

Same head, and the diff above shows no other text changed.
