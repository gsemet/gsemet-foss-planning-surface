# CR-102 verification (batch-01)

Head: 125952dc04a949cc78810e2340ef57d9ffa6ba5e

Result: **VERIFIED**. Every claim below holds at the head. The three claims that failed at 8537709
(C12b, C17 bullet 4, C18) are corrected in the posted description.

- Base: `1a742d714439595753a3b0b416f9cc04183015a3`. PR: <https://github.com/gsemet/okf-schema/pull/70>.
- `<W>` is the CR's worktree, `<CR>` the CR folder, `<S>` is `<CR>/work/scratch`. `H` is the head
  above; every claim was judged at `H` unless it says `carried from`. Commands ran from `<W>`.
- Host: Windows 11 (10.0.26200), Python 3.13.18, `okf_schema` imported from `<W>/src`.
- Previous judgment: Head 8537709c5c10c77140a62542d794421537448d59, base 2f09cef, NOT VERIFIED.
- Scripts under `<S>/v125` are throwaway and removed at the end; their output is kept in
  `work/verifier/*-125952d.log` or quoted here.

## C0. Head, tree, PR (H) - VERIFIED

    git rev-parse HEAD (= origin branch)  -> 125952dc04a949cc78810e2340ef57d9ffa6ba5e
    git status --porcelain                -> (empty)
    gh pr view 70  -> OPEN, draft, MERGEABLE, base main 1a742d7, head 125952d

## M. The move 8537709..125952d (H) - VERIFIED

    git range-diff 373fded..01d676b 1a742d7..125952d  -> three commits all "="
    tree of 01d676b and of 125952d                    -> b05dd83f1ea77dcae6d7ce0bdac2c230c54ad4c4
    git range-diff 1a03994..d9e1b30 373fded..dfcef0a  -> both "="
    against 2f09cef..8537709: commit 1 no longer touches CHANGELOG.md, context moves in log.md,
      SKILL.md, test_api.py; one added commit 125952d (the `show` changelog line)
    git diff --stat 2f09cef 1a742d7 -> 24 files: `show` (api.py, cli.py), trust tier (validator.py),
      schema, docs, requirements, tests; not utils.py, nothing under skills-evals/
    git diff --numstat 1a742d7 H -- CHANGELOG.md requirements/tiers/log.md skills/okf-schema/SKILL.md
      -> 2/0, 18/0, 3/3 (the only removed lines are the three rewritten SKILL.md rows);
         no conflict marker

The move touches the shipped code's base, so the code claims were judged again at `H`.

## C1. Long gate (H) - VERIFIED

Not run again. First, total, summary and last lines of `work/gates/20261126-000836.log`:

    gate CR-102 branch chantier/batch-01/cr-102-index-no-broken-links-in-subdirectory-su head 125952dc04a949cc78810e2340ef57d9ffa6ba5e
    TOTAL   4729   146   2028   140   96%
    1236 passed, 12 skipped in 135.64s
    result: pass at 125952dc04a949cc78810e2340ef57d9ffa6ba5e

    $CHANTIER handoff CR-102
      gates before handback ready, at the PR's head 125952dc...:
        [x] long gate passed (gate CR-102 preflight; ...)
      note: gate left only a line-ending rewrite of CHANGELOG.md (empty content diff, tree clean)

This also covers step 8 of the specification's scenario. Generated diffs of the preflight:
`git status --porcelain` empty; `git diff --stat H -- examples` empty;
`git diff --quiet 1a742d7 H -- examples` exit 0.

## C2. Specification checks 1 to 23 on the shipped code (H) - VERIFIED

    uv run --no-sync -- pytest -v -rs -o addopts="" -p no:cacheprovider tests/test_api.py
      tests/test_validator.py tests/test_cli_core.py tests/test_cli_remaining.py
      tests/test_internal.py tests/test_edge_cases.py
      -> 523 passed in 7.48s, exit 0   (log: work/verifier/pytest-125952d.log)

    checkmap.py over that log (passed/selected per named test) -> "0 names missing or not fully passed"
    check 1 1/1; 2 1/1; 3 5/5; 4 1/1; 5 3/3,1/1,1/1; 6 6/6; 7 1/1,1/1; 8 6/6; 9 8/8; 10 4/4,1/1;
    11 3/3; 12 1/1,1/1,7/7; 13 five tests 1/1; 14 2/2,1/1,1/1; 15 3/3; 16 3/3,2/2,9/9; 17 1/1;
    18 2/2; 19 2/2; 20 3/3,2/2,3/3,7/7; 21 three 1/1; 22 three 1/1; 23 two 1/1

## C3. Changed doctests (H) - VERIFIED

    uv run --no-sync -- pytest ... --doctest-modules src/okf_schema/_internal/utils.py
      src/okf_schema/api.py src/okf_schema/validator.py
      -k "find_broken_links or is_broken_link or _is_damaged_summary or _check_broken_links or validate_log or validate_index"
      -> 6 passed, 16 deselected, exit 0

## C4. Specification scenario, steps 1 to 7b, worktree CLI (H) - VERIFIED

    scenario.py in a fresh git-initialised folder under <S> (log: work/verifier/scenario-125952d.log)
    step 1  index -> "- [api](./api/) — Auto-generated index for concepts in `api`."; 2nd run "0 updated, 0 created, 2 unchanged"
    step 2  damaged line -> index -> generic line; validate --strict: only W1/W3 of the `new` concept,
            conformant (0 errors, 0 warnings) once it has a description and generated.at
    step 3  link nope.md -> "[W2] Broken cross-link 'nope.md' in '<project>\kb\bundle\index.md'", exit 1; index keeps the line
    step 4  root line first reset to generic -> "- [api](./api/) — See the [check](api/health-check.md) first. Second paragraph, in progress [draft]";
            validate --strict passes; 2nd run unchanged
    step 5  [x](my%20file.md) to an existing file -> validate --strict passes
    step 6  "* [API](api/) - Les endpoints" -> "- [api](./api/) — Les endpoints"; 2nd run unchanged
    step 7  log.md created (none existed), link deleted.md -> W2 'deleted.md', exit 1; link removed -> passes
    step 7b [top](#top) -> "2 links", "Health: 100% — all clear"; + [gone](missing.md#part) ->
            "3 links (1 broken)", "Health: 90% — 1 broken link"; validate names 'missing.md#part'
    == 17 checks ok, 0 failed

The first two runs of the script failed on the script's own edit of the concept (a duplicate
`description` key); the run above is the fixed script on a fresh folder.

## C5. Host matrix: link rewriting (check 3), percent decoding (checks 16, 22) (H) - VERIFIED

    gh run view 45718843170 --json headSha,conclusion,jobs -> 125952d success; preflight 3.10-3.13,
      cross-platform macos-latest and windows-latest: success; tag-release: skipped
    ci.py over work/ci-45718843170.log: every job checked out "77366de Merge 125952dc... into 1a742d71..."

| Job | check 3 (5 cases) | check 16 (3 cases) | check 22 (1) | suite |
| --- | --- | --- | --- | --- |
| macos-latest | 5 PASSED | 3 PASSED | 1 PASSED | 1248 passed |
| windows-latest | 5 PASSED | 3 PASSED | 1 PASSED | 1236 passed, 12 skipped |
| ubuntu 3.10, 3.11, 3.12, 3.13 | 5 PASSED each | 3 PASSED each | 1 PASSED each | 1248 passed each |

## C6. Scaffold guidance holds no W2 or `okf-schema index` wording (H) - VERIFIED

    grep -rnE "\bW2\b|okf-schema index|Broken cross-link|x-okf-summary" src/okf_schema/data
      -> no output, exit 1 (14 tracked files)
    git grep -n -E "index\.md|okfkb index|[Rr]egenerat|[Bb]roken|summar" -- src/okf_schema/data
      -> Base.schema.yaml:15, knowledge-base.guidelines.md 46/51, requirements.guidelines.md 17,
         264, 284-301 (navigation of `okfreq lint`); none describes bundle summaries or W2

## C7. Description renders and equals work/pr-body.md (H) - VERIFIED

    gh pr view 70 --json body ; diff --strip-trailing-cr with work/pr-body.md
      -> one trailing blank line only (updatedAt 2026-11-25T23:12:32Z, head 125952d)
    gh api repos/gsemet/okf-schema/pulls/70 -H "Accept: application/vnd.github.html+json" --jq .body_html
      -> h2 Description, Type of Change, Checklist, Known gaps, Related Issues; h3 Behaviour changes,
         Surfaces, Example, Validation; text and shell blocks; one mermaid block; task lists; #57
         linked; no image, no fold
    grep of the body for role names, STALE, UNVERIFIED, images, home folder paths -> no match

## C8. Description, introduction (base 1a742d7 and H) - VERIFIED (base side by source, not by a run)

    git show 1a742d7:src/okf_schema/api.py, git diff 1a742d7 H -- src/okf_schema/api.py
      -> the base fallback returns the first non-heading line of the subdirectory index.md with the
         list marker stripped
    git show 1a742d7:src/okf_schema/validator.py -> find_broken_links runs for concepts only;
      validate_index checks E3, validate_log E3/W5/W18
    git show 1a742d7:src/okf_schema/_internal/utils.py -> resolve_link (no anchor strip, no
      percent decoding) then exists()
    gh issue view 57  -> "- [api](./api/) — [Health Check](health-check.md)  [API Endpoint]";
      "`validate` reports no W2 for it"
    at H: is_broken_link is called by stats (api.py) and by find_broken_links, which W2 uses: one check

## C9. Before/after block and flowchart (H) - VERIFIED

The `after` line is the output of C4 steps 1 and 2; the `before` line is the issue's output (C8).
Flowchart branches: schema summary (check 8), kept as authored (checks 6, 7, 12, 20), damaged or
generic recomputed (checks 5, 7), introduction rewritten and cut at 120 (checks 3, 10, 11), generic
sentence (checks 2, 9, 10).

## C10. Behaviour changes, four bullets (H) - VERIFIED

    bullet 1: checks 10, 11 (C2); its one exception, a linked image, is stated under Known gaps (C17b)
    bullet 2: checks 5, 7, 12, 20 (C2); scenario steps 2, 4, 6 (C4)
    bullet 3: checks 14, 18, 21 (C2); probes.py (log: work/verifier/probes-125952d.log):
      okfkb validate after broken links -> W2 'gone-index.md', 'gone-log.md', exit 1
      okfreq validate .agents/requirements: 0 warnings before, "0 requirements, 0 errors,
      2 warnings" after (W2 on tiers/index.md and tiers/log.md), exit 0
    bullet 4: checks 15, 16, 22, 23 (C2); scenario steps 5, 7b (C4)

## C11. CHANGELOG and diff scope (H) - VERIFIED

    git diff --stat 1a742d7 H -> 16 files, +1215 -75: CHANGELOG.md, docs/source/reference/{cli,
      validation-codes}.md, requirements (log.md, CORE-001, CORE-004), skills/okf-schema/SKILL.md,
      utils.py, api.py, validator.py, tests/fixtures/bundle/valid/index.md, five test files
    CHANGELOG.md: base Unreleased/Fix holds only the validate line; the head adds the index line and
      the show line (a371f73 is on the base); `cz changelog --dry-run` matches the head

## C12a. Surfaces, content of the list (H) - VERIFIED

    git diff 1a742d7 H -- docs skills requirements tests
      -> cli.md: index and stats sections; validation-codes.md: W2, compatibility note, scope line;
         SKILL.md: index, stats and W2 rows; CORE-004 adds S3; CORE-001 adds S4; markers 001#S4 (10),
         004#S3 (21), 005#S1 (2); one log entry, no approval field; fixture index.md: damaged line
         replaced by the generic sentence; new tests in the five test files
    grep -niE "W2|broken|index" docs/source/explanation/project-feature-coverage.md
      -> lines 25 and 27 only (okfreq navigation and showcase)
    okf-schema index --help -> "Regenerate all index.md files in an OKF bundle." and Args
    static.py -> 15 index.md/log.md files in examples, 25 links, internal: 0 anchored, 0 encoded,
      0 slash-prefixed, 0 broken

## C12b. Surfaces, runtime bullet (H) - VERIFIED (failed at 8537709, corrected)

    base 1a742d7: only find_broken_links exists (utils.py:81)
    H: is_broken_link (utils.py:97) is new; find_broken_links (utils.py:142) calls it (utils.py:183)
    grep -n -A4 "^def validate_log" validator.py -> (path, report, bundle_root: Path | None = None);
      base: (path, report)
    index_bundle, stats_bundle, validate_index, validate_log: changed in the diff

## C13. Example block (H) - VERIFIED

    probes.py, issue bundle: okf-schema index --path kb/bundle -> generic root line, exit 0
    okf-schema validate --strict --path kb/bundle -> conformant, exit 0
The description claims no result for these commands.

## C14. Validation section (H) - VERIFIED

    bullet 1, 2: C1 (1236 passed, 12 skipped, 96%; style, lint, requirements lint, changelog, ty,
      mypy, examples refresh, requirements report and sphinx -W "build succeeded" in the log;
      checkout clean)
    bullet 3: C5
    bullet 4: okfreq validate requirements --prose --check-links --project-root .
      -> 36 requirements, 0 errors, 0 warnings, exit 0

## C15. Type of change, checklist, related issue (H) - VERIFIED

Bug fix and documentation: C11. "just preflight passes": C1. Tests added: C2, C11. Docs updated:
C12a. "No new warnings" is left unchecked. `Fixes #57`: issue 57 is open and is this defect (C8).

## C16. Known gaps, bullets 1 to 3 (H) - VERIFIED

    1. gate log and CI windows-latest: 12 skipped, in tests/test_acceptance_{core,okfkb,okfreq}.py,
       the test of StRS-OKFSCHEMA-CORE-002#S2 (test_acceptance_core.py:152) among them; macOS and
       the four Linux logs report 1248 passed, 0 skipped, that test PASSED
    2. probes: api/notes(1).md -> W2 'notes(1' in api/index.md, exit 1; same after another index run
    3. probes: "- [api](./api/) — See [guide](guide.md)." kept by index, W2 'guide.md';
       validation-codes.md:343-344 and the SKILL.md:136 index row word the repair more broadly

## C17. Known gaps, bullet 4 and the private functions bullet (H) - VERIFIED (failed at 8537709, corrected)

    static.py against 1a742d7:
      cli commands index, stats, validate -> versionchanged: no
      new private functions without Examples (7): utils _is_external_link, _link_path_for_check;
        api _generic_subdir_description, _extract_introduction, _rewrite_summary_links,
        _cut_summary, _subdir_entry_key
      with Examples (2): _is_damaged_summary, _check_broken_links
Five summary helpers in api.py and two link helpers in utils.py: as posted. The nested closure
`rewrite` is not a module function.

## C17b. Known gaps, the other bullets (H) - VERIFIED

    version: validation-codes.md:346 and the new docstring notes say 0.19.0; the base `show` notes
      say 0.18.2 (api.py, cli.py)
    log entry: requirements/tiers/log.md says 1187 tests passed and 95.68% coverage, the figures of
      the gate logs of 8537709 (work/gates/20261125-225323.log, -225959.log), not of C1
    probes-125952d.log:
      multi-line comment -> "- [api](./api/) — hidden maintainer note -->"
      "[![i](a.png)](b.md) badge." -> "[![i](api/a.png)](b.md) badge." (outer not rewritten); long
        text cut to "...[![i](api/a.png)](bbbbbbbb..."; missing outer target: bundle conformant
      "[w](sub\file.md)" -> "[w](api/sub\file.md)"
      W2 'a%00.md' and W2 'https%3A//example.invalid/x'
      directory of subdirectories: no group/index.md, generic parent line; bare schema:
        "- [typed](./typed/) — " (empty summary)

## C18. Known gaps is complete (H) - VERIFIED (failed at 8537709, corrected)

The one uncaptured item of `work/verifier/evidence/before-after.md` (the before of all three pairs)
now has its bullet. Its facts: `carried from 8537709: the move changed no file under skills-evals/
(git diff --quiet 2f09cef 1a742d7 -- skills-evals, exit 0) and the scratch folder is the same`.
The after captures were taken again at `H`; they hold no user name or home folder path. No
`**UNVERIFIED:**` or STALE mark is posted, and no failed claim is left to accept.

## Observations, not claims of the description

- Behaviour bullet 3: `okfreq validate` reports the new W2 but still exits 0 (its warnings never
  change the exit status); "validate --strict can start failing" does not make `okfreq validate`
  fail.
- The log entry under `requirements/` still carries the older run's figures; Known gaps says so.
