# CR-103 verification

Head: 6572527608200cb688c0ae0224427e8b8bb44539

Base: 1a742d714439595753a3b0b416f9cc04183015a3. First verification. Windows, Python 3.12.10.
Every claim below is judged at `6572527` unless it says carried.
`<S>` is `work/scratch/v1`, removed at the end; the scripts and logs are kept in `work/verifier/`.

Verdict: NOT VERIFIED. The code does what the specification says; two bullets of the
description's Known gaps are wrong.

## Failed

### F1. Known gaps: "On a non-blocking standard output that is full, show retries without pause"

False for the default (buffered) standard output. It holds only under `python -u`.

Command: `<S>/vh/Scripts/python.exe -I nonblocking.py` (real `show` process, real non-blocking
pipe, 4000000 byte file, nobody reads for 3 s), head wheel:

```text
default (buffered) stdout
  while full: ended by itself with exit code 120 while nobody read
  exit code: 120
  received 4096 of 4000000 bytes
  stderr last line: BlockingIOError: [Errno 11] write could not complete without blocking
python -u (raw) stdout
  while full: still running after 3 s with a full pipe
  exit code: 0
  received 4000000 of 4000000 bytes
  stderr last line: (empty)
```

Same script on the base wheel (not a regression of the default case):

```text
default (buffered) stdout
  exit code: 120
  received 4096 of 4000000 bytes
  stderr last line: BlockingIOError: [Errno 11] write could not complete without blocking
python -u (raw) stdout
  exit code: 0
  received 2108 of 4000000 bytes
```

Wording that matches: on a full non-blocking standard output, `show` fails with
`BlockingIOError` after a partial output (as before this change); under unbuffered output it
retries without pause until every byte is written. Windows only; POSIX not run.

### F2. Known gaps: the Windows harness ran "against a wheel built from an earlier state"

No longer holds. The harness passed at `6572527` (`evidence/acceptance-windows.txt`, replaced):

```text
$ uv run --no-sync -- python -X utf8 <S>/acceptance_windows.py . <S>/v1/vh <S>/v1/ah
package under test: <S>\v1\vh\Lib\site-packages\okf_schema\__init__.py
pass: test_inspection_reports_matching_concepts_and_changes_no_file
pass: test_init_then_new_creates_a_valid_bundle_that_keeps_the_authored_concept
exit 0
```

Still true: the acceptance tests skip on Windows (CI windows-latest: SKIPPED). Both pass in CI
run 45719431446 on macos-latest and preflight 3.10 to 3.13 (see C6).

## Proved claims

### C1. `show` prints the stored file; scenario of the specification

`uv run --no-sync -- python -X utf8 work/scratch/scenario_run.py . <S> evidence/scenario-run.txt`
-> every CHECK pass, `Result: 0 failed check(s)`, exit 0. Covers init, new, show identical to
the file, `trust: unverified`, flow style and comment kept after lint, `trust: human-reviewed` +
`stale: true` with the same sha256 before and after, broken/plain/latin1 shown identical with
empty stderr, `trust latin1` exit 2 with one error line.

### C2. Before and after, resolution and messages unchanged

`python -I probe.py 1a742d7... 6572527... work/verifier/evidence`
(`work/verifier/evidence/before-after.md`). Base `show styled`:
`b"---\r\ntype: concept\r\ntitle: 'Quoted'\r\ntags:\r\n- alpha\r\n- beta\r\n...at: '2026-11-01T10:00:00+00:00'\r\nstale_after: '2020-01-01'\r\n---\r\ntrust: human-reviewed\r\nstale: true\r\n\r\nBody\r\n\r\n"`,
identical False. Head: `identical to the stored file: True` for styled, plain, broken, latin1,
exit 0, 0 stderr lines. Base `trust`: `Error: No such command 'trust'.` Head `trust`:
`trust: human-reviewed` / `stale: true`; plain and broken `trust: unverified`; latin1 exit 2,
`Error: Concept file is not valid UTF-8: <probe>\bundle\latin1.md`. `missing`, `missing.md`,
`sub`, `../outside.md`: exit 2 with identical messages on base `show`, head `show` and head
`trust`. `bundle content and times unchanged: True` for each of the four runs.

### C3. API: `raw` added, other fields unchanged; help summaries

`python -I api_compare.py` (base and head wheels):

```text
lf, crlf, cr, mixed, bom, plain, broken, empty: other fields equal=True raw==stored bytes=True
latin1: other fields equal=True ... head={'error': 'UnicodeDecodeError'}
help --help 0 ['show  Print a concept file exactly as stored.', "trust  Print a concept's trust tier and staleness."]
```

### C4. New tests pass at head and fail on the base code (one passes there by design)

Head: `uv run --no-sync -- python -m pytest tests/test_api.py tests/test_cli_remaining.py
--no-cov -p no:cacheprovider -o addopts= -q` -> `220 passed`.
Base sources with the head test files (`run_base.py`, `base-tests.log`, package under test =
base worktree `src`): `34 failed, 186 passed`: 4 in `test_api.py` (3 new `raw` tests and the
extended no-frontmatter test), all new `show` and `trust` tests, and the two defensive
error-handling tests.
The one new test that passes on the base: `test_show_bundle_refuses_a_file_that_is_not_utf8`
(it guards unchanged behaviour), so "they fail on the previous code" needs that exception.
Acceptance: head test functions against the base wheel stop at
`okf-schema trust ... concepts/clock` ... `returned non-zero exit status 2`.

### C5. Local gates

Carried from `3776ca4` for `just preflight`: `git rev-parse <sha>^{tree}` gives
`0c0362a0e783780999c806763a5ea6f658c1d0b6` for `e161d98`, `3776ca4` and `6572527`.
Gate log `work/gates/20261126-000130.log`, first line
`gate CR-103 branch chantier/batch-01/cr-103-show-print-the-stored-file-new-trust-com head 3776ca46619bc72572da989997e44c5fc9192be5`;
`1186 passed, 12 skipped`, `Total coverage: 95.62%`, ruff `All checks passed!`, mypy
`Success: no issues found in 28 source files`, `sphinx-build -W` `build succeeded.`, no pytest
warnings summary.
At `6572527`: `okfreq update-coverage requirements --check` -> `0 files would change`, exit 0;
`okfreq validate requirements --prose --check-links --project-root .` ->
`36 requirements, 0 errors, 0 warnings`, exit 0; `okfreq lint requirements --check
--check-links --project-root .` -> `0 indexes would change`, exit 0.
`@tests_req` markers: 005#S5 9, 006#S6 7, 006#S7 1, 006#S8 1; CORE-005 and CORE-006 list
`src/okf_schema/cli.py`; CORE-005, 006, 010 stay `proposed`.

### C6. CI

`gh pr checks 73`: cross-platform macos-latest and windows-latest, preflight 3.10 to 3.13
`pass`, tag-release `skipping`. `gh run view 45719431446`: headSha `6572527...`, success.
Log: macOS and the four preflight jobs `1198 passed`; Windows `1186 passed, 12 skipped`.
`test_show_show_does_not_translate_newlines_in_a_real_process` and
`test_show_show_writes_every_byte_through_short_writes` PASSED in all six jobs.

### C7. Review box

`chantier log CR-103`: `r2 approved at 1a03994..., committed as e161d989e23d...`.
`git show <c> | git patch-id --stable` gives `49d76ca16bf8e7ca04dac72089f831bfe3824f84` for
`e161d98`, `3776ca4` and `6572527`. Remote branch head = `6572527`.

### C8. Other description claims

- Autonomous decision, `TIER`: a scratch copy of `requirements/` with `<tier>` in CORE-006,
  `okfreq validate <copy> --prose` -> `W002 ...SwRS-OKFSCHEMA-CORE-006.md: body has no filled
  EARS expression` (none with `TIER`, C5).
- Autonomous decision, loop: `r2_short_write_check.py` -> real unbuffered console writes
  `[12287, 12287, 12287, 10784, 16177, 16178]`, total 80000, pipe identical True. Base `-u`
  non-blocking run (F1): exit 0 with 2108 of 4000000 bytes.
- Known gap, containment sentence: CORE-010 S3 THEN reads `the concept is shown as before`
  under `WHEN the user shows it or prints its trust tier`.
- Known gap, version: `grep -rn "versionchanged:: 0.18.2" src` -> `api.py:489`, `cli.py:740`.
- Known gap, impossible date: head `trust` exit 1 `ValueError: day is out of range for month`;
  `show` exit 0; `list` exit 1 with the same error on base and head.
- #69: `gh pr view 69` -> MERGED, `fix(validate): count every OKF 0.2 actor form in the trust tier`.
- Unaffected surfaces: `git diff --stat 1a742d7 HEAD -- justfile .github pyproject.toml
  CHANGELOG.md src/okf_schema/data examples README.md` -> empty; README has no `show` or `trust`
  command; the only grep hit in those folders is an archived note under `.github/changes/archives/`.
- Changes match `git diff --stat` (14 files); Human decisions match `02-answers.md` Q1-Q4, Q9-Q13.
- Format: sections and fold render-ready, no image, no internal reference outside the last section.

## Observations (not failures)

- Forge body differs from `work/pr-body.md` in one item: the forge still has `- [ ] CI green`
  (compared with `gh pr view 73 --json body`). Post the file when fixing F1 and F2.
- `requirements/tiers/log.md` entry says `1185 tests pass`; at the head it is 1186.
- The parser traceback of the date gap also happens for another bad scalar
  (`count: !!int abc` -> `trust` exit 1 `ValueError`; base `show` failed the same way).
- A file starting with a byte order mark reads as no frontmatter (`trust: unverified`), same
  `show_bundle` values as the base.
- Worktree at the end: `git status --porcelain` empty, HEAD `6572527`; base worktree removed.
