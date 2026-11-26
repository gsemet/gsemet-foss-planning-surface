# CR-512 verification: description pass on the posted body, second post

Head: 54d1da6268e9a4fbe059c6cdb8b1160d94b4b558

Verdict: **VERIFIED** at `54d1da6`, base `chantier/batch-09/cr-505-strs-acceptance-tests-acceptance-job-and`
(`9d7e788a479dec70fd882d295bf0d5e78f4f6b98`). Draft pull request
https://github.com/gsemet/markdown-okf-schema-studio/pull/536.

The full verification note at this head (specification claims, matrix, gates, first description
check, notes) is kept whole in `W/verifier/verify-54d1da6-full.md`. Its claims stand; this pass
checks the description only, and replaces its "One thing is left" paragraph and its "How the line
should read" column as the state of the description. No gate, test or CI run was run or re-run.

`WT` is the CR worktree, `W` the CR's `work/` folder, `S` = `W/scratch/artifacts-54d1da6` (CI job
logs, local only), `B` the posted body saved with `gh pr view 536 --json body --jq .body`
(temporary file in `W/scratch`, removed after the pass). Git commands ran with `git -C WT`.

| Claim | Command, at `54d1da6` | Output |
| --- | --- | --- |
| Head, base, state | `git rev-parse HEAD`; `git status --porcelain --untracked-files=all`; `gh pr view 536 --json headRefOid,baseRefName,baseRefOid,isDraft,state,updatedAt,title` | head `54d1da62...` in both; status empty; base `chantier/batch-09/cr-505-...` at `9d7e788a...`; draft, `OPEN`; updated 11:59:52Z; title "test: cover the editor reopening after a header-cell paste" |
| Posted body is the source file | `diff --strip-trailing-cr B W/pr-body.md` | only `110d109`, one trailing empty line of `B` |
| Renders | `gh api repos/gsemet/markdown-okf-schema-studio/pulls/536 -H "Accept: application/vnd.github.full+json" --jq .body_html` | nine `<h2>`, Summary to Internal references; table with header and 11 rows; mermaid section with its source; seven checked task boxes; the footer link. No fold, as the project's template (`.github/PULL_REQUEST_TEMPLATE.md`) has none |
| SHA marks | search of `B` for `e76c084`, `89cae5f`, `8df99ce`, `STALE`, `UNVERIFIED`, "second run" | one match, line 26, "at `54d1da6` (carried from `e76c084`)", the valid carried form. The rows "CI real-window suite" and "repeated alone in CI" and the Test plan lines (new test, requirements, local gates, review, verified, CI green) name `54d1da6`, each as the full note's "How the line should read" column gives it; the sentence on the visual job's second run is gone |
| No image, no username or home folder, internal references only last | search of `B` for image syntax, `<img`, the username, drive and home paths, `CR-<n>`, "batch" | `CR-512` and `CR-489` on lines 106-107, under "Internal references"; the only other match is the `https://` footer link |
| Review box | `$CHANTIER log CR-512` | 11:31:02Z "move e76c084..54d1da6 (restack) inspector approved at 54d1da6268e9..." |
| Verified box | same log | 11:58:50Z `driver verdict result=VERIFIED head=54d1da6268e9...` |
| CI green box: pull request checks | `gh run view 45810700393 --json attempt,event,headSha,status,conclusion,jobs`; `gh pr checks 536` | attempt 1, `pull_request`, `54d1da62...`, completed, success; static, static-windows, visual, viewer-graph, report, checks pass; real VS Code jobs skipped there |
| CI green box: two manual runs with the real VS Code jobs | `gh run view` 45811051488 and 45811056179, same fields | both attempt 1, `workflow_dispatch`, `54d1da62...`, completed, success; integration, acceptance, stress, static, static-windows, visual, viewer-graph, report, checks, gallery success; release-check, toc-loop, release, tag-release, pages skipped |
| CI real-window suite, 2 runs | search of `S/run-45811051488-integration.log` and `S/run-45811056179-integration.log` | each: checkout `54d1da6268e9...`, `STEP done: real-input` (424559 ms; 420828 ms), `ci-integration: passed` |
| Repeated alone in CI, 11 of 11 | search of `S/run-45811056179-stress.log` | `STUDIO_STRESS_SCENARIOS: table-grid-paste-header`, `PASS stress 1/11` to `11/11`, "ci-stress: passed (11 rounds)" |
| Product code identical to `3478f09` (main) | `git diff --name-only 3478f099 54d1da62 -- src sphinx`; `git diff --name-only 3478f099 origin/main -- src sphinx` | both empty |
| Changes and Impacts match the delivery | `git diff --stat 9d7e788a 54d1da62` | 8 files, 122 insertions, 11 deletions: clip notes and script, clip guideline, requirement and its log, `run.ts`, `tableGridPaste.ts`, `stressPlan.ts`; no product file, no media |
| Remaining claims (other table rows, local gates, requirements, new test, changelog, diagram, blast radius, autonomous decisions, known gaps complete) | carried from the earlier pass at the same head: neither head nor base moved, and the body equals the file it judged but for the SHA marks and the CI line | `W/verifier/verify-54d1da6-full.md`, "Every proof of the body" |

## Notes (none changes the verdict)

- The log line of the earlier verdict (11:58:50Z) records `base=54d1da62...`, equal to the head,
  while the pull request's base is `9d7e788`.
- No file-editing tool was available in this pass: the earlier `verify.md` was copied unchanged to
  `W/verifier/verify-54d1da6-full.md` (`cmp`: no difference) before this file was written.
