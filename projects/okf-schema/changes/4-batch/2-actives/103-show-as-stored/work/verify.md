# CR-103 verification

Head: a2723b7a0cdea34d9fe3601f3081b21ea424d07d

Base: 125952dc04a949cc78810e2340ef57d9ffa6ba5e. Second verification, after the move
6572527..a2723b7 (base 1a742d7..125952d, rebase with conflicts). Windows, Python 3.12.10.
The previous note is kept as `work/verifier/verify-6572527.md`.
`<S>` is `work/scratch`; `<S>/v2` is removed at the end.

Verdict: VERIFIED. No failed claim. One capture was refused (R1) and its claim is carried (C8).

## R1. Refusal met (path too long)

`git worktree add --detach <S>/v2/b 125952dc04a949cc78810e2340ef57d9ffa6ba5e`, to refresh the
base-side test run at the new base:

```text
Preparing worktree (detached HEAD 125952d)
error: unable to create file skills-evals/results/iteration-30.06.26-20.12/schema-composition-trap/with_skill/workspace/_schema/vehicle-config.schema.json: Filename too long
error: unable to create file skills-evals/results/iteration-30.06.26-20.12/schema-composition-trap/without_skill/workspace/_schema/vehicle-config.schema.json: Filename too long
error: unable to create file skills-evals/results/iteration-30.06.26-22.06/schema-composition-trap/with_skill/workspace/_schema/vehicle-config.schema.json: Filename too long
error: unable to create file skills-evals/results/iteration-30.06.26-22.06/schema-composition-trap/without_skill/workspace/_schema/vehicle-config.schema.json: Filename too long
fatal: Could not reset index file to revision 'HEAD'.
```

No other way was tried. `git worktree list` afterwards shows no `<S>/v2/b`. Nothing was run
against the new base; the base-side proofs below are the ones of `6572527`, carried by C1.

## C1. The move (a2723b7)

`git diff <base> <head> -- src tests docs requirements/tiers/swrs | git patch-id --stable`:
`d8aba34eddde664ae81b51af3e1f1685ecd664db` for `1a742d7..6572527` and for `125952d..a2723b7`.
`git range-diff`: only the context of `requirements/tiers/log.md` and `skills/okf-schema/SKILL.md`
differs.
`git diff --stat 1a742d7 125952d -- src/okf_schema/cli.py src/okf_schema/_internal/models.py
src/okf_schema/_internal/yaml.py tests/acceptance_support.py tests/test_acceptance_core.py
pyproject.toml uv.lock justfile .github README.md src/okf_schema/data examples` -> empty.
`git diff -U0 1a742d7 125952d -- src/okf_schema/api.py`: hunks in imports, `index_bundle`,
`stats_bundle` and the index helpers only. Same on `validator.py`: the W2 link check,
`validate_index`, `validate_log`, `validate_bundle`; `_derive_trust_tier`, `_is_stale` untouched.
Test files of the base: added index and stats tests.

Conflict files: `git diff --numstat 125952d HEAD` -> `22 0 requirements/tiers/log.md`,
`3 2 skills/okf-schema/SKILL.md`, no `CHANGELOG.md`. The skill diff changes only the
management list (`trust` added), the `show` row and the new `trust` row. Conflict marker grep:
no match (exit 1); one `## 2026-11-25` heading, with both entries.

`git ls-remote origin`: CR branch `a2723b7...`, CR-102's branch `125952d...`;
`git merge-base --is-ancestor 125952d HEAD` -> true; `git diff --stat 125952d HEAD` -> 14 files.

## C2. Local gates (a2723b7)

`work/gates/20261126-003844.log`, first line
`gate CR-103 branch chantier/batch-01/cr-103-show-print-the-stored-file-new-trust-com head a2723b7a0cdea34d9fe3601f3081b21ea424d07d`,
last line `result: pass at a2723b7...`: `1269 passed, 12 skipped`, `Total coverage: 95.75%`,
ruff and ty `All checks passed!`, mypy `Success: no issues found in 28 source files`,
`sphinx-build -W` `build succeeded.`; grep for `warnings summary` and Python warning classes:
no match. `handoff`: `gates before handback ready, at the PR's head a2723b7a...`:
`[x] long gate passed (gate CR-103 preflight ...)`.

Run directly at the head, tree clean:
`okfreq update-coverage requirements --check` -> `0 files would change`, exit 0;
`okfreq validate requirements --prose --check-links --project-root .` ->
`36 requirements, 0 errors, 0 warnings`, exit 0;
`okfreq lint requirements --check --check-links --project-root .` -> `0 indexes would change`,
exit 0.

## C3. CI (a2723b7)

`gh pr checks 73`: preflight 3.10 to 3.13 and cross-platform macos-latest, windows-latest
`pass`; tag-release `skipping`. `gh run view 45723093438`: `headSha a2723b7...`,
`event pull_request`, `conclusion success`. `ci.yml`: preflight `ubuntu-latest`, tag-release
only on a push to main. Log: macOS and the four preflight jobs `1281 passed`; Windows
`1269 passed, 12 skipped`. `..._does_not_translate_newlines_in_a_real_process` and
`..._writes_every_byte_through_short_writes` PASSED in all six jobs. The two `show` acceptance
tests PASSED on macOS and preflight, SKIPPED on windows-latest.

## C4. The specification's scenario (a2723b7)

`uv run --no-sync -- python -X utf8 <S>/scenario_run.py . <S>/v2 evidence/scenario-run.txt` ->
every CHECK pass, `Result: 0 failed check(s)`, exit 0 (`evidence/scenario-run.txt`, refreshed):
`show` identical to the file, also for broken, plain and Latin-1 files with empty stderr;
`trust: unverified`; then `trust: human-reviewed` + `stale: true` with the same sha256 before
and after; `trust latin1` exit 2 with one error line.

## C5. Gap bullet: Windows acceptance harness (a2723b7)

`uv build --wheel --out-dir <S>/v2/wh .`, installed in `<S>/v2/s/vh`, then
`uv run --no-sync -- python -X utf8 <S>/acceptance_windows.py . <S>/v2/s/vh <S>/v2/ah`:

```text
package under test: <S>\v2\s\vh\Lib\site-packages\okf_schema\__init__.py
pass: test_inspection_reports_matching_concepts_and_changes_no_file
pass: test_init_then_new_creates_a_valid_bundle_that_keeps_the_authored_concept
exit 0
```

`grep '"show"' tests/test_acceptance*.py`: the command is run in
`tests/test_acceptance_core.py` lines 142, 226, 227, that is in those two functions only.
With the Windows skip of C3, the reworded bullet holds. It also supports the change log's
sentence about the harness (`evidence/acceptance-windows.txt`, refreshed).

## C6. Gap bullet: full non-blocking standard output (a2723b7)

`<S>/v2/s/vh/Scripts/python.exe -I <S>/v2/s/nonblocking.py` (copy of
`work/verifier/nonblocking.py`; real pipe, 4000000 bytes, nobody reads for 3 s):

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

"as before this change": carried from 6572527: the base command (`cli.py`, C1) is unchanged;
base default stdout gave the same exit 120, 4096 bytes and `BlockingIOError`.
Loop with no pause: `cli.py:778-779` `while remaining: remaining = remaining[stdout.write(remaining) or 0 :]`.
Not tested for real: `grep -rnE "set_blocking|O_NONBLOCK|BlockingIOError|PIPE_NOWAIT" tests src`
-> no match; `test_show_show_writes_every_byte_through_short_writes` patches
`click.get_binary_stream` with `_ShortWriteStream`. Windows only: POSIX not run.

## C7. The other Known gaps (a2723b7)

`<S>/v2/s/vh/Scripts/python.exe -I gaps.py` (kept as `work/verifier/gaps.py`):

```text
show_bundle marked: {} unverified
trust marked exit 0 ['trust: unverified', '']
trust unmarked exit 0 ['trust: human-reviewed', '']
== stale_after: 2020-02-30
trust odd exit 1 [''] ValueError: day is out of range for month
show odd exit 0 []
list exit 1 [] ValueError: day is out of range for month
== count: !!int abc
trust odd exit 1 [''] ValueError: invalid literal for int() with base 10: 'abc'
show odd exit 0 []
list exit 1 [] ValueError: invalid literal for int() with base 10: 'abc'
```

- Byte order mark (new bullet): holds. "The reading the API already had": `git show
  125952d:src/okf_schema/api.py` reads with `read_text(encoding="utf-8")` then
  `extract_frontmatter` (mark kept; `yaml.py` unchanged, C1); head decodes with `utf-8` too.
- Impossible date: holds. `docs/source/reference/cli.md:336-338` says no stale line when
  unparseable. "Predates": carried from 6572527 (base `list` failed the same way; parser
  unchanged, C1).
- Change log count (new bullet): `requirements/tiers/log.md` says `1185 tests pass and 12 are
  skipped`; the Test plan says 1269 (C2). Holds.
- Containment sentence: `SwRS-OKFSCHEMA-CORE-010.md` S3, `WHEN the user shows it or prints its
  trust tier`, `THEN the concept is shown as before`. Holds.
- Version: `grep -rn "versionchanged:: 0.18.2" src` -> `api.py:497`, `cli.py:740`. Holds.
- Completeness: F1 and F2 of the previous note are reworded (C5, C6); its byte order mark and
  test count observations now have bullets; no pair is uncaptured; no `UNVERIFIED` mark.

## C8. Test plan "New or changed tests" (box unchecked)

Head: the tests pass (C2, C3). Base side, carried from 6572527: 34 of them fail on the base
code, `test_show_bundle_refuses_a_file_that_is_not_utf8` passes there by design. The move did
not touch what that proof exercises: same CR patch id, and the base's `show`, `trust` (absent),
`show_bundle` and models are those of 1a742d7 (C1). The base did add other tests and index code
to `api.py` and the two test files; they are not part of this claim. Not run again (R1).

## C9. Review box (a2723b7)

`chantier log CR-103`: `2026-11-25T23:37:56Z driver note move 6572527..a2723b7 (conflict)
inspector approved at a2723b7a0cdea34d9fe3601f3081b21ea424d07d`.

## C10. Posted description (a2723b7)

- `gh pr view 73 --json body` against `work/pr-body.md`: only the final newline differs.
  `headRefOid a2723b7...`, base = CR-102's branch, draft, title = commit subject.
- Rendered HTML (`gh api .../pulls/73`, `body_html`): all sections as headings, task boxes,
  one `<details>` closed after Internal references. No image or `<img`; no username or home
  path (grep exit: only `unverified` and the CR line matched the wider pattern).
- Role names, CR name and `work/`, `evidence/` paths: grep matches lines 129-130 only
  (Internal references).
- Stacked-on sentence: `gh pr view 70` -> OPEN, head `125952d...`, the base of #73;
  `gh pr view 69` -> MERGED `fix(validate): count every OKF 0.2 actor form in the trust tier`.
- Checklist: preflight and no new warnings (C2, C3); tests and documentation in the 14 files
  of C1. Test plan: Local gates (C2), Review (C9), CI (C3) are proved.
- Summary, Changes, Autonomous decisions, Human decisions, Impacts, Blast radius: carried from
  6572527: the text was not changed since and the CR's patch is the same (C1).

## Before and after

`work/verifier/evidence/before-after.md`: pairs carried from 6572527 (before 1a742d7), reason
written there (C1); the after behaviour was run again at the head (C4).

## State at the end

`git status --porcelain` empty, HEAD `a2723b7a0cdea34d9fe3601f3081b21ea424d07d`.
