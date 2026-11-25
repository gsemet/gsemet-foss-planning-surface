# CR-102 verification (batch-01)

Head: 8537709c5c10c77140a62542d794421537448d59

Result: **NOT VERIFIED**. The code and the specification's checks pass at the head. The posted PR
description fails on three claims (C12b, C17 bullet 4, C18).

- Base: `2f09cef3e786d1696e42b5cb305d4a55111e7725`. PR: <https://github.com/gsemet/okf-schema/pull/70>.
- `<W>` is the CR's worktree, `<CR>` the CR folder, `<S>` is `<CR>/work/scratch`. `H` below is the
  head above; every claim was judged at `H` unless it says otherwise. Commands ran from `<W>`.
- Host: Windows 11 (10.0.26200), Python 3.13.18, `okf_schema` imported from `<W>/src`.
- Previous judgment: `work/verifier/matrix-r2.md` at `4b38782`.
- Scripts under `<S>/v` are throwaway and removed at the end; their output is quoted here.

## C0. Head, tree, PR (H) - VERIFIED

    git rev-parse HEAD                  -> 8537709c5c10c77140a62542d794421537448d59
    git status --porcelain              -> (empty)
    git diff --name-only 4b38782 HEAD   -> CHANGELOG.md
    gh pr view 70 --json headRefOid,baseRefOid,state,isDraft
      -> 8537709c... base=2f09cef3... OPEN draft=true

## C1. Long gate (H) - VERIFIED

Not run again. First and last line of `work/gates/20261125-225959.log`:

    gate CR-102 branch chantier/batch-01/cr-102-index-no-broken-links-in-subdirectory-su head 8537709c5c10c77140a62542d794421537448d59
    ...
    result: pass at 8537709c5c10c77140a62542d794421537448d59

    $CHANTIER handoff CR-102
      gates before handback ready, at the PR's head 8537709c5c10c77140a62542d794421537448d59 (...):
        [x] long gate passed (gate CR-102 preflight; ...)

This also covers step 8 of the specification's scenario.

## C2. Specification checks 1 to 23 on the shipped code (H) - VERIFIED

    uv run --no-sync -- pytest -v -rs -o addopts="" -p no:cacheprovider tests/test_api.py
      tests/test_validator.py tests/test_cli_core.py tests/test_cli_remaining.py
      tests/test_internal.py tests/test_edge_cases.py
      -> 496 passed in 5.57s, exit 0   (log: work/verifier/pytest-head.log)

    python -I <S>/v/checkmap.py <CR>/work/verifier/pytest-head.log   (passed/selected per test)
    check 1: test_index_bundle_issue_57_damaged_root_line_gets_generic_summary 1/1
    check 2: test_index_bundle_fresh_bundle_never_copies_a_list_entry 1/1
    check 3: test_index_bundle_rewrites_introduction_links 5/5
    check 4: test_index_bundle_rewrites_links_relative_to_a_nested_parent 1/1
    check 5: test_index_bundle_recomputes_a_damaged_summary 3/3; test_index_bundle_recomputes_damaged_schema_folder_summary 1/1; test_index_bundle_drops_entry_of_a_folder_without_markdown 1/1
    check 6: test_index_bundle_keeps_a_summary_without_the_damage_signature 6/6
    check 7: test_index_bundle_recomputes_the_generic_summary 1/1; test_index_bundle_keeps_a_text_close_to_the_generic_one 1/1
    check 8: test_index_bundle_schema_aware 6/6
    check 9: test_index_bundle_never_uses_a_heading_or_list_entry 8/8
    check 10: test_index_bundle_cuts_a_long_introduction 4/4; test_index_bundle_writes_generic_summary_when_the_cut_leaves_nothing 1/1
    check 11: test_index_bundle_takes_the_whole_introduction 3/3
    check 12: test_index_bundle_keeps_trailing_brackets_of_an_introduction 1/1; test_index_bundle_keeps_type_like_tag_of_a_subdirectory_entry 1/1; test_parse_existing_index_subdirectory_keys 7/7
    check 13: test_index_bundle_subdir_description_from_index_body 1/1; test_index_bundle_subdir_description_oserror 1/1; test_index_bundle_get_subdir_description_truncates_long_desc 1/1; test_index_bundle_parse_existing_index_no_h1 1/1; test_index_bundle_parse_existing_index_with_intro 1/1
    check 14: test_validate_index_reports_broken_link 2/2; test_validate_index_valid_link_no_w2 1/1; test_validate_index_ignores_links_of_the_frontmatter 1/1
    check 15: test_validate_bundle_w2_ignores_anchors 3/3
    check 16: test_validate_bundle_w2_decodes_percent_encoded_paths 3/3; test_index_bundle_decodes_paths_to_detect_damage 2/2; test_is_broken_link 9/9
    check 17: test_validate_bundle_valid_valid_bundle_is_conformant 1/1
    check 18: test_validate_strict_fails_on_broken_reserved_file_link 2/2
    check 19: test_broken_link_doctests_pass 2/2
    check 20: test_index_bundle_keeps_summary_for_every_subdirectory_spelling 3/3; test_index_bundle_recomputes_summary_under_other_spellings 2/2; test_index_bundle_keeps_the_later_line_of_two_subdirectory_spellings 3/3; test_parse_existing_index_subdirectory_keys 7/7
    check 21: test_validate_log_reports_link_to_a_deleted_file 1/1; test_validate_log_existing_link_no_w2 1/1; test_validate_log_log_valid_dates_no_w5 1/1
    check 22: test_stats_bundle_counts_broken_links_like_w2 1/1; test_stats_bundle_counts_broken_links 1/1; test_link_edge_cases_external_links_only 1/1
    check 23: test_stats_ignores_anchors_and_encoding_of_valid_links 1/1; test_stats_stats_shows_broken_links_in_health 1/1

## C3. Changed doctests (H) - VERIFIED

    uv run --no-sync -- pytest -v -o addopts="" -p no:cacheprovider --doctest-modules
      src/okf_schema/_internal/utils.py src/okf_schema/api.py src/okf_schema/validator.py
      -k "find_broken_links or is_broken_link or _is_damaged_summary or _check_broken_links or validate_log or validate_index"
      -> find_broken_links, is_broken_link, _is_damaged_summary, _check_broken_links,
         validate_index, validate_log: PASSED
      -> 6 passed, 14 deselected

## C4. Specification scenario, steps 1 to 7b, worktree CLI (H) - VERIFIED

    python -I <S>/v/scenario.py ...   (git-initialised folder under <S>; log: work/verifier/scenario-head.log)
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

## C5. Host matrix: link rewriting (check 3), percent decoding (checks 16, 22) (H) - VERIFIED

    gh run view 45709925120 --json headSha,conclusion,jobs
      -> 8537709c5c10c77140a62542d794421537448d59 success; preflight 3.10-3.13, cross-platform
         macos-latest and windows-latest: success; tag-release: skipped
    gh pr checks 70  -> the six test jobs pass, tag-release skipping
    job logs: each checked out "867d00e Merge 8537709c... into 2f09cef3..."
    grep -oE "(PASSED|FAILED|SKIPPED|ERROR) tests/...::(<the three tests>)(\[...\])?" <job log> | sort | uniq -c

| Job | check 3 rewrites (5 cases) | check 16 decodes (3 cases) | check 22 stats (1) |
| --- | --- | --- | --- |
| macos-latest | 5 PASSED | 3 PASSED | 1 PASSED |
| windows-latest | 5 PASSED | 3 PASSED | 1 PASSED |
| ubuntu 3.10, 3.11, 3.12, 3.13 | 5 PASSED each | 3 PASSED each | 1 PASSED each |

Windows on this host: C2 of this file, at `H` (same tests). The CLI cells C2, C4 and C6 of
`matrix-r2.md`: carried from 4b38782: the move to `H` changes `CHANGELOG.md` only.

## C6. Scaffold guidance holds no W2 or `okf-schema index` wording (H) - VERIFIED

    grep -rnE "\bW2\b|okf-schema index|Broken cross-link|x-okf-summary" src/okf_schema/data
      -> no output, exit 1 (14 tracked files)
    git grep -n -E "index\.md|okfkb index|[Rr]egenerat|[Bb]roken|summar" -- src/okf_schema/data
      -> index generation appears only in requirements.guidelines.md 284-301, about the navigation
         that `okfreq lint` generates, not bundle index summaries

## C7. Description renders and equals work/pr-body.md (H) - VERIFIED

    gh pr view 70 --json body > <S>/posted-body.md ; diff with work/pr-body.md
      -> one trailing blank line only (updatedAt 2026-11-25T22:06:44Z)
    gh api repos/gsemet/okf-schema/pulls/70 -H "Accept: application/vnd.github.html+json" --jq .body_html
      -> h2 Description, Type of Change, Checklist, Known gaps, Related Issues; h3 Behaviour changes,
         Surfaces, Example, Validation; text and shell code blocks; one mermaid block; task lists;
         #57 linked; no image, no fold, no STALE or UNVERIFIED mark

## C8. Description, introduction (base H and 2f09cef) - VERIFIED (base side by source, not by a run)

    git grep -n ... 2f09cef -- src ; git show 2f09cef:src/okf_schema/_internal/utils.py
      -> _get_subdir_description returns the first non-heading line of the subdirectory index.md
         with the list marker stripped; validate_index checks E3 only, validate_log E3/W5/W18 only;
         find_broken_links: resolve_link (no anchor strip, no decoding) then exists()
    gh issue view 57  -> "- [api](./api/) — [Health Check](health-check.md)  [API Endpoint]";
      "`validate` reports no W2 for it"
    git grep -n -E "(is_broken_link|find_broken_links)\(" H -- src
      -> validator.py:741 find_broken_links (W2); api.py:963 is_broken_link (stats): one check

## C9. Before/after block and flowchart (H) - VERIFIED

The `after` line is the output of C4 step 1 and 2; the `before` line is the issue's output (C8).
Flowchart branches: schema summary (check 8), kept as authored (checks 6, 7, 12, 20), damaged or
generic recomputed (checks 5, 7), introduction rewritten and cut at 120 (checks 3, 10, 11), generic
sentence (checks 2, 9, 10).

## C10. Behaviour changes, four bullets (H) - VERIFIED

    bullet 1: checks 10, 11 (C2)
    bullet 2: checks 5, 7, 12, 20 (C2); scenario steps 2, 4, 6 (C4)
    bullet 3: checks 14, 18, 21 (C2); python -I <S>/v/probes.py and probe_req.py:
      okfkb validate after broken links -> W2 'gone-index.md' (index.md), W2 'gone-log.md' (log.md), exit 1
      okfreq validate .agents/requirements, before 0 warnings -> W2 'gone-index.md' (tiers/index.md),
      W2 'gone-log.md' (tiers/log.md)     (logs: work/verifier/probes-head.log, probe-okfreq-head.log)
    bullet 4: checks 15, 16, 22, 23 (C2); scenario steps 5, 7b (C4)

## C11. CHANGELOG and diff scope (H) - VERIFIED

    git diff --stat 2f09cef HEAD -> 16 files, +1222 -75: CHANGELOG.md, docs/source/reference/{cli,validation-codes}.md,
      requirements (log.md, CORE-001, CORE-004), skills/okf-schema/SKILL.md, utils.py, api.py,
      validator.py, tests/fixtures/bundle/valid/index.md, five test files
    git diff 2f09cef HEAD -- CHANGELOG.md -> adds "index: write subdirectory summaries without broken
      links" under Unreleased and the heading "## v0.18.1 (2026-11-25)" over the older entries

## C12a. Surfaces, content of the list (H) - VERIFIED

    git diff -U0 2f09cef HEAD -- docs skills requirements tests
      -> cli.md: index and stats sections; validation-codes.md: W2, a note near it, the scope table;
         SKILL.md: two rows near line 136 and the row at 359; CORE-004 adds S3; CORE-001 adds S4;
         tests_req markers 001#S4 (10), 004#S3 (21), 005#S1 (2); one log entry, no approval field;
         fixture index.md: damaged line replaced by the generic sentence
    git diff ... validator.py -> validate_log(path, report, bundle_root: Path | None = None)
    grep -niE "W2|broken|index" docs/source/explanation/project-feature-coverage.md
      -> lines 25 and 27 only (okfreq navigation and showcase)
    uv run --no-sync -- okf-schema index --help -> "Regenerate all index.md files in an OKF bundle." and Args
    python -I <S>/v/scan_examples.py <W>
      -> 15 index.md/log.md files, 25 links, internal: 0 anchored, 0 encoded, 0 slash-prefixed, 0 broken

## C12b. Surfaces, "the new `is_broken_link` and `find_broken_links`" (H) - NOT VERIFIED

    git grep -n -E "def (is_broken_link|find_broken_links)\(" 2f09cef H -- src
      2f09cef:src/okf_schema/_internal/utils.py:81:def find_broken_links(
      8537709:src/okf_schema/_internal/utils.py:97:def is_broken_link(
      8537709:src/okf_schema/_internal/utils.py:142:def find_broken_links(

`find_broken_links` exists at the base: it is changed, not new. Only `is_broken_link` is new.

## C13. Example block (H) - VERIFIED

    python -I <S>/v/probes.py  (issue 57 bundle)
      okf-schema index --path i57/bundle -> "1 updated, 0 created, 1 unchanged", generic line, exit 0
      okf-schema validate --strict --path i57/bundle -> runs, exit 1 on W1/W3 of the `new` concept
The description claims no result for these commands.

## C14. Validation section (H) - VERIFIED

    work/gates/20261125-225959.log
      line 2475  TOTAL 4710 144 2022 139 96%
      line 2480  1187 passed, 12 skipped in 127.33s
      lines 7, 10, 21 All checks passed!; requirements lint, changelog, ty, mypy, examples refresh,
      requirements report present; line 2681 sphinx-build -W; line 2711 build succeeded
    git diff --stat HEAD -- examples      -> empty
    git diff --quiet 2f09cef HEAD -- examples -> exit 0
    git ls-files --eol examples/okfreq-examples -> rewritten files i/lf w/crlf (14)
    okfreq validate requirements --prose --check-links --project-root .
      -> 35 requirements, 0 errors, 0 warnings, exit 0

## C15. Type of change, checklist, related issue (H) - VERIFIED

Bug fix and documentation: C11. "just preflight passes": C1. Tests added: C2, C11. Docs updated:
C12a. "No new warnings" is left unchecked. `Fixes #57`: issue 57 is open and is this defect (C8).

## C16. Known gaps, bullets 1 to 3 (H) - VERIFIED

    1. CI windows-latest log: 12 SKIPPED, all in tests/test_acceptance_{core,okfkb,okfreq}.py,
       test_lint_and_index_are_deterministic_and_preserve_authored_content (StRS CORE-002#S2) among them.
       The bullet is true. It can be narrowed: the same 12 tests PASSED in the macos-latest log and
       in each of the four Linux logs of run 45709925120 (Linux and macOS: "1199 passed").
    2. probes.py, api/notes(1).md: validate --strict -> W2 'notes(1' in api/index.md, exit 1; same
       after another index run
    3. probes.py: "- [api](./api/) — See [guide](guide.md)." kept by index, W2 'guide.md';
       validation-codes.md 343-344 ("... copied with its links, run `okf-schema index`: it repairs
       the line") and the SKILL.md index row word it more broadly

## C17. Known gaps, bullet 4 (H) - NOT VERIFIED

First half true: `cli command index|stats|validate: versionchanged: no`. Second half ("two private
summary helpers have no `Examples` section") is false:

    python -I -B <S>/v/docstrings.py 2f09cef3e786d1696e42b5cb305d4a55111e7725
    new private  src/okf_schema/_internal/utils.py:39  _is_external_link  Examples: NO
    new private  src/okf_schema/_internal/utils.py:87  _link_path_for_check  Examples: NO
    new private  src/okf_schema/api.py:1043  _cut_summary  Examples: NO
    new private  src/okf_schema/api.py:1007  _extract_introduction  Examples: NO
    new private  src/okf_schema/api.py:1002  _generic_subdir_description  Examples: NO
    new private  src/okf_schema/api.py:1059  _is_damaged_summary  Examples: yes
    new private  src/okf_schema/api.py:1022  _rewrite_summary_links  Examples: NO
    new private  src/okf_schema/api.py:1142  _subdir_entry_key  Examples: NO
    new private  src/okf_schema/validator.py:722  _check_broken_links  Examples: yes
    new private functions: 2 with Examples, 7 without

Five new private summary helpers in api.py lack the section (seven new private functions in all),
not two.

## C17b. Known gaps, bullets 5 to 9 (H) - VERIFIED

    python -I <S>/v/probes.py   (log: work/verifier/probes-head.log)
    5. multi-line comment -> "- [api](./api/) — hidden maintainer note -->"
    6. "[![i](a.png)](b.md) badge." -> "[![i](api/a.png)](b.md) badge." (outer not rewritten); long
       text cut to "...[![i](api/a.png)](bbb..."; missing outer target: bundle conformant
    7. "[w](sub\file.md)" -> "[w](api/sub\file.md)"
    8. W2 'a%00.md' and W2 'https%3A//example.invalid/x'
    9. directory of subdirectories: no group/index.md, generic parent line; bare schema:
       "- [typed](./typed/) — " (empty summary)

## C18. Known gaps is complete (H) - NOT VERIFIED

`work/verifier/evidence/before-after.md` says no before capture was taken, for each of its three
pairs. The posted Known gaps has no bullet for it. Cause:

    git -C <W> worktree add --detach <S>/v/b 2f09cef3e786d1696e42b5cb305d4a55111e7725   -> exit 128
    error: unable to create file skills-evals/results/iteration-30.06.26-20.12/bootstrap-knowledge-base/with_skill/workspace/_schema/Sensor.schema.json: Filename too long
    (many more lines of the same kind)
    fatal: Could not reset index file to revision 'HEAD'.

This is the card's stop for a path too long for Windows: no other folder or method was tried. The
failed command left no worktree (`git worktree list` shows no base worktree).

## Observations, not claims of the description

- The docs and docstrings say 0.19.0 for this change. A `fix` alone bumps the patch number, so
  0.19.0 holds only if the release also carries a `feat`.
- Scenario step 4: `index` removed the blank line between the two introduction paragraphs of
  `api/index.md`. Not compared with the base by a run; no claim of this CR covers it.
