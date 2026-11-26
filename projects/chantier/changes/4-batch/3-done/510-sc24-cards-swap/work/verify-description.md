# CR-510: description pass

Head: 4380df52776791c42253d49e971a6a38aaf9517e

**VERIFIED.** The posted description of PR 488 is true, consistent with the proof at this head
(`verify.md`, `verifier/evidence/before-after.md`) and with the diff, and follows the PR template
in every place that changed. Only the description was judged; `verify.md` is unchanged. No gate,
test suite, quiz, eval run or campaign was run.

Conventions: `<wt>` the CR's worktree; `<CR>` the CR folder; `BASE` = `ea11a9e`, `OLD` =
`b85be4c`, `HEAD` = `4380df5`. All rows judged at 4380df5. "Script" is a throwaway check under
`<CR>/work/scratch/v3/`, removed at the end of the pass; it read
`gh pr view 488 --repo gsemet/chantier --json headRefOid,baseRefOid,isDraft,state,body,statusCheckRollup`
and the rendered body (`gh api repos/gsemet/chantier/pulls/488`, full media type). The body judged
by the earlier proof is `work/pr-body.md` at the planning surface's commit `9e3f0dab`.

## The posted body and what changed

| # | Claim | Command and output | Verdict |
| --- | --- | --- | --- |
| 1 | Head and base unchanged, checks green | `git rev-parse HEAD` in `<wt>` -> HEAD; `git status --short` -> empty. Script -> `head HEAD base BASE draft True OPEN`; `just check` ubuntu, macos, windows, `just scenario`, `just eval-dry-run`: all `SUCCESS` | VERIFIED |
| 2 | The posted body is `work/pr-body.md` | Script -> `posted == pr-body.md: True 17215 17215` | VERIFIED |
| 3 | It changed only in the places the brief names | Script -> `judged body chars (verify.md: 15876): 15876`; seven hunks: Deliverables `+17 lines`; Known gaps one line replaced, one added; Test plan three lines replaced (new tests, evidence, verified); Internal references one line replaced (row 5) | VERIFIED |

## The changed places

| # | Claim | Command and output | Verdict |
| --- | --- | --- | --- |
| 4 | Deliverables, "Before, at `ea11a9e`" excerpt | Script: each of the three quoted lines -> `before line in probe-base.log: True` (the raw `take` output at BASE, `work/scratch/v1/probe-base.log`); omitted lines are marked `...`; same text as pair 1 of `before-after.md` | VERIFIED |
| 5 | Deliverables, "After, at `4380df5` (carried from `b85be4c`)" excerpt | Script, `<cr>` and `<batch>` filled with the fixture's ids -> `after block, placeholders filled, contiguous in probe-head.log: True`; pair 1, carried from OLD (`verify.md` M2: the one commit since only adds topic link lines). Matches the table row "print the lease and the `brief` command" | VERIFIED |
| 6 | Test plan, new tests: the three pass at 4380df5, the prepared stale-name case fails as expected, not run on the previous code; box unticked | `git diff --name-status BASE HEAD -- skills/chantier/scripts/cli/tests` -> `A` `test_brief_bytes.py`, `test_card_homes.py`, `test_card_names.py`; `verify.md` Gates (2748 passed at HEAD) and acceptance 7 (18 passed); `evidence/e8-card-names.md` -> the scan over the prepared source `1 failed`, as expected (`verify.md` acceptance 8, carried). No run of the three on BASE is recorded: a search of `work/` for their names finds the Coder's and Verifier's head runs only, and `work/scratch/v2/tests-base.log` holds no `passed` or `failed` line | VERIFIED |
| 7 | Test plan, "Evidence: before at `ea11a9e`, after at `4380df5` (the command captures carried from `b85be4c`)", ticked | `before-after.md` head: base BASE, after HEAD; pairs 1 to 7 carried from OLD, pair 8 printed again and pair 9 new at HEAD | VERIFIED |
| 8 | Test plan, "Verified at `4380df5` (claims the topic links cannot change carried from `b85be4c`); the bound on the added test time is not proved", ticked | `verify.md`: `VERIFIED` at HEAD, carried rows rest on M2; acceptance 9 `bound NOT PROVED`; the `**UNVERIFIED:**` bullet is in Known gaps | VERIFIED |
| 9 | Known gaps, "The new tests were not run against the previous code." | as row 6 | VERIFIED |
| 10 | Known gaps, `topics/wakes-p1.md` added to the cards that describe output no longer printed | `skills/chantier/references/topics/wakes-p1.md` line 5 at HEAD: "printed outside Driver prompt blocks, `take`'s and `order qa`'s included"; those blocks are gone (rows 4 and 5, `before-after.md` pairs 1 and 4) | VERIFIED |
| 11 | Checklist row 5, "done, but for the two `AGENTS.md` sentences named in Known gaps" | `git grep -n -E "foreman-conflict\|planning folder only and records\|driver\.md\|startup-core\|startup-manifest\|reload-rules\|session-start\|opening lines\|chief-of-staff-[a-z-]+\.md\|foreman-[a-z-]+\.md\|driver-[a-z-]+\.md" HEAD -- AGENTS.md` -> line 251 (`foreman-conflict.md`) and line 263 (what `brief` reads), the two that Known gaps names; `git diff --stat BASE HEAD -- AGENTS.md CONTRIBUTING.md` -> `CONTRIBUTING.md` only | VERIFIED |

## Template

| # | Claim | Command and output | Verdict |
| --- | --- | --- | --- |
| 12 | Sections, order, fold and rendering | Script -> ten rendered `h2` in the template's order (no source ticket, so no Issues References), 3 tables, 1 `details` opened and closed, blank line after `</summary>` and before `</details>`, 6 fence lines (3 blocks, 3 rendered `pre`), 0 images | VERIFIED |
| 13 | SHAs, marks, internal references, private paths | The new excerpt captions and Test plan items name their SHA; script -> `STALE marks: 0 \| UNVERIFIED marks: 1` (its bullet is in Known gaps), `internal refs outside Internal references: []`, `private path in posted body: False` | VERIFIED |

## Observations (no effect on the verdict)

- The attribution line "Generated with Claude Code" follows `</details>`, where the template says
  nothing follows. It is unchanged since the earlier proof and was not judged again.
- The "Verified" item names one unproved point. The matrix cell not met (F5), the quizzes not run
  and the `/compact` transcript not captured are not repeated there; each has its Known gaps bullet.
- This pass's first listing command changed into the CR folder, against the brief's instruction
  (a read-only `ls` and `wc`; nothing was written by it).
