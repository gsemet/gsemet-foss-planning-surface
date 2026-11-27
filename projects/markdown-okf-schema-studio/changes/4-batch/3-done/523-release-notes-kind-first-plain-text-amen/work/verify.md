# CR-523 verification

Head: eb493a3735e3a81862e7856a414d736c504722b4

PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/554 (draft). Every claim below was
judged at eb493a3. Commands ran in the worktree unless said otherwise. `W` = this CR's `work/`
folder, `V` = `W/verifier`, `G` = `.agents/guidelines/release-process.guidelines.md`, `CARD` =
`C:/Users/gaeta/Projets/chantier/skills/chantier/references/release-template.md`.

Second judgment at the same head. The first one (NOT VERIFIED) failed claim 7 only, row 7 of the
PR body's dry run. The body on the forge is now edited; claim 7 and the head are judged again,
the other claims are carried. Result in short: claims 0 to 8 pass.
Third judgment at the same head (description pass): the posted body alone, claim 9. Result: pass.

## 0. Head, base and PR head: pass (eb493a3)

- `git rev-parse HEAD` -> `eb493a3735e3a81862e7856a414d736c504722b4`
- `git status --porcelain` -> no output
- `git ls-remote origin refs/heads/chantier/batch-11/cr-523-... refs/heads/main` -> branch
  `eb493a37...22b4`, main `b9b29c5a...515b52c` (the base of the first judgment)
- `gh pr view 554 --json headRefOid,isDraft,state,statusCheckRollup` -> head `eb493a37...22b4`,
  draft, open; run 46002527489: `checks`, `report`, `static`, `static-windows`, `viewer-graph`,
  `visual`, `visual-2` SUCCESS, the other jobs SKIPPED
- First judgment, for the commit itself: one commit over origin/main, type `docs`, no scope,
  trailer `Assisted-by: Claude:Sonnet-5.5` (carried from eb493a3: same head).

## 1. Only the guideline changes: pass (eb493a3)

carried from eb493a3: same head and same origin/main (claim 0), so the same diff.

- `git diff --name-status origin/main HEAD` -> `M .agents/guidelines/release-process.guidelines.md`
- `git diff --stat origin/main...HEAD` -> `1 file changed, 117 insertions(+), 31 deletions(-)`
- `git diff --quiet origin/main HEAD -- scripts docs requirements CHANGELOG.md CONTRIBUTING.md skills src test`
  -> exit 0. So `release_notes.py` (decision 2), the 1.12.1 and 1.13.0 notes (decision 4) and the
  feature-clip guideline are unchanged, and there is no CHANGELOG line.
- `python -I V/compare_guideline.py` (output `V/evidence/compare_guideline.txt`): the intro, "Rules
  of a release", "The release folder", "The version PR on top of a stack", "The version PR body",
  "Publishing" and "Announcement thread" are identical to origin/main. "The steps of a release" and
  "Hero image" differ, as specified (the diff shows one clause in step 3, one paragraph in "Hero
  image").

## 2. Every section of "What changes" and every carried decision: pass (eb493a3)

carried from eb493a3: same head, so the same guideline; the specification's text is what was read.

Command: `git diff origin/main...HEAD`, and G read whole at the head.

| Specification | Lines of G at eb493a3 |
| --- | --- |
| "The kind": five kinds, subtitle, order of several kinds, version mismatch | 218-238 |
| "Writing": heading by kind, one sentence, `Fixed:`/`Restored:`, bad news, performance, banned table, pointer to "Images", setting, earlier bans kept | 249-283 |
| "Structure": title `X.Y.Z`, subtitle 16 words, headings, smaller changes and `Other fixes`, contributors' known issue, "the smaller changes", "Length" | 289-324 |
| "Images": visible change only, crop, gesture, size, before and after, alt text, missing picture, clip GIF exception, file rules kept (one cross-reference now "as above") | 326-351 |
| "Self-check", last subsection, ten questions, no word on the script | 359-375 |
| Step 3 clause pointing to the self-check | 57-59 |
| "Hero image": post 1 only; first highlight takes its own picture | 402-404 |

The old picture rules are all still present (329-338, 342-344; "Nothing comes under the
picture" stays at 250-251).

Decisions 1 to 8: 1 structure order unchanged (287-314); 2 no script change (claim 1); 3 GIF exempt
(342-344); 4 note not rewritten (claim 1); 5 performance (265-267); 6 kinds, labels, one sentence,
budgets, image protocol (218-345); 7 hero (402-404); 8 `## 🛠 Other fixes` (307).

## 3. Same values as the card and the `release-evidence` topic: pass (eb493a3)

carried from eb493a3: same head; the card and topic comparison was made against this guideline.

- `diff <(sed -n 40,48p CARD) <(git show HEAD:G | sed -n 275,283p)` -> no output, exit 0: the
  banned table (header and seven rows) is identical.
  (The script's first output line, `banned rows card 8 guideline 7`, counts the separator row on
  one side only; the `diff` is the proof.)
- `V/evidence/compare_guideline.txt`: the ten questions equal the specification's; nine equal the
  card's word for word; question 9 differs only by "picture", `"Images"` for the topic's name and
  "(a clip GIF excepted)".
- CARD lines 22-81 and `references/topics/release-evidence.md` lines 5-9 read: kinds, order, 16 / 20
  / 40 / 120 / 250 words, 900 to 1200 px and 600 px, alt text, missing picture agree with G.
- Not carried and not in the specification (no failure): the card's "asks no question" on a
  doubtful version (CARD line 32).

## 4. The PR body's rule-by-rule table: pass (eb493a3)

carried from eb493a3: same head, and the body's rule table is byte for byte unchanged (claim 7's diff).

`gh pr view 554 --json body` (copy `V/evidence/pr-body-eb493a37.md`), each row's lines read in G at
the head: 242-244, 220-226, 228-230 and 291-292, 232-233, 235-238, 290, 289-301, 249-255 and
302-304, 337-338, 305-308, 309-317, 256-259, 260-264 / 307-308 / 313-314, 272-283, 268-269,
319-324, 328, 329-332 (exception 342-344), 333, 334-336, 339, 340-341, 402-404, 359-375 and 58-59.
Each line range carries its rule, the values match claim 3, and each "differs" row names why.
`grep -c -i "known gaps" .github/PULL_REQUEST_TEMPLATE.md` -> `0`, which supports the reason of the
"Missing picture" row. Every rule listed by the specification's Evidence 2 has a row.

## 5. `git grep` on the phrase: pass (eb493a3)

carried from eb493a3: same head.

- `git grep -n "what you can now do" -- G` -> `252:  - feature: what you can now do;` (only hit)
- the same on `origin/main` -> lines 226 and 263 (the old rule for every highlight, gone).

## 6. Gates and CI: pass (eb493a3)

carried from eb493a3: same head; the CI re-read in claim 0 shows the same run and results.

- Run here: `just release-notes-check` -> `release-notes: docs/releases-notes/2026-11-27-v1.13.0/release-notes.md ok`, exit 0.
- `just check`, not re-run: `W/just-check-eb493a37.log`, first line `just --unstable --fmt`; node
  suites `fail 0` (56, 5560 of 5568 with 8 skipped, 116), pytest `298 passed` (includes
  `test_guideline_isolation.py` 9 dots), `release-notes ... ok`, ends on `use case diagrams: 94
  StRS checked, all parse`; no `error: recipe` line.
- `just preflight`, not re-run: `W/preflight-eb493a37.log`, first line `rm -rf out .artifacts`;
  line 6 `check-no-merge-commits: passed (1 commits since origin/main, no merge commit)`; ends
  `ci-static: passed` and `preflight: visual, viewer-graph, integration, acceptance, report and
  gallery stages skipped on Windows; CI runs them`.
- The logs' first lines do not name the SHA. What binds them to it: `git reflog --date=iso` shows
  the commit eb493a37 at 13:37:16 and no later move of HEAD; the logs were last written at 13:46:02
  and 13:53:36; the preflight counts one commit over origin/main; the tree is clean.
- `chantier handoff CR-523`: no long gate is declared in chantier.yaml.
- `gh pr checks 554`: `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual`,
  `visual-2` pass; `acceptance`, `gallery`, `integration`, `pages`, `perf-547`, `release`,
  `release-check`, `stress`, `tag-release`, `toc-loop` skipping.
- `gh run view 46002527489 --json headSha,conclusion,event` -> eb493a37...22b4, `success`,
  `pull_request`.
- No visual change, so no screenshot (one Markdown file, claim 1).

## 7. The PR body's dry run on the 1.12.1 note: pass (eb493a3)

- `gh pr view 554 --json body --jq .body > verifier/evidence/pr-body-eb493a37-2.md`, then
  `diff --strip-trailing-cr pr-body-eb493a37.md pr-body-eb493a37-2.md` -> one hunk, `82c82`:
  - was: `... subtitle 18 words for 16; longer highlight, lines and visible part than allowed |`
  - now: `... subtitle 18 words for 16; a highlight and lines longer than allowed |`
- `git diff --quiet origin/main HEAD -- docs/releases-notes/2026-11-24-v1.12.1/release-notes.md`
  -> exit 0 (note not rewritten).
- Row 7, answer "no", against the note read at the head and
  `python -I verifier/count_note_words.py` (re-run): lines 30-32 are a bold lead plus a second
  sentence; subtitle 18 words (limit 16); one highlight (18-23) at 111 words (limit 40), the other
  (24-27) at 37; lines 31, 32, 37, 45, 47 at 23, 26, 27, 28, 21 words (limit 20). Every statement
  of the row holds.
- The failed statement is gone: the row says nothing of the visible part (243 words, within the
  250 of a feature or breaking release, G 319-323), so it agrees with row 10.
- Rows 1 to 6 and 8 to 10, carried from eb493a3: same head, same note, rows byte for byte
  unchanged. My yes/no answers agreed on all ten (1 to 8 no, 9 yes, 10 no), and the three faults
  the specification requires are shown (title `1.12`, subtitle without a kind, bold-lead lines with
  no `Fixed:`).
- Noted, no failure (carried): row 5 also cites line 32 ("as in 1.12.0"), which says 1.12.0 behaved
  correctly, so line 20 alone carries that "no".

## 8. The rest of the PR description: pass (eb493a3)

carried from eb493a3: same head, and the body differs from the judged copy in row 7 only (claim 7's diff).

- Rendering: `gh api graphql ... pullRequest(number:554){bodyHTML}`: sections, three tables, the
  fold and the task list render. Source line wraps render as line breaks, as in recent merged PRs
  (`<br>` counts: 550: 70, 549: 45, 543: 58).
- Summary, "Deliverables" before and after table (against `git diff`; the base rule folded "any known
  issue" under "For contributors"), "Changes", "Impacts" ("No visual change"), blast radius: agree
  with the diff.
- Test plan: grep line 252 (claim 5); local gates and CI (claim 6); "committed unchanged": `git diff
  b9b29c5a eb493a37 | git patch-id --stable` and the same on `evidence/guideline-r1.diff` (written
  before the commit) both give `434aefdd0072e6e3b871cce117f341009c9299a9`; the approval at b9b29c5
  is the CR's note in `STATUS.md`.
- Human decisions against `02-answers.md` (Q2 to Q6 and the performance rule); autonomous decisions
  against the diff and the Chief of Staff gap: agree.
- Known gaps: each of the eight seen in G (215 and 303; 305-307; 305 against 256-257; 176-210; 302;
  260-262 against 316-317; 329 and 373; 347, present on origin/main too).
- Internal references are in their own last section; no role name does the work elsewhere; no image,
  no user name or home path in the body.

## 9. Description pass (third judgment): pass (eb493a3)

The posted description alone, read from the forge. Code, gates and CI are claims 0 to 6 (carried
from eb493a3: same head). Body copy: `V/evidence/pr-body-eb493a37-3.md`.

Head and body

- `git rev-parse HEAD`, `git ls-remote origin <branch> refs/heads/main`, `gh pr view 554 --json
  headRefOid,isDraft,state,updatedAt` -> worktree, branch and PR head `eb493a37...22b4`, main
  `b9b29c5a...515b52c`, open draft; `git status --porcelain` -> no output.
- `diff --strip-trailing-cr pr-body-eb493a37-2.md pr-body-eb493a37-3.md` -> exit 0 (the body of the
  second judgment); against `W/pr-body.md` one added trailing blank line only. `gh api graphql ...
  lastEditedAt` -> `2026-11-27T13:13:55Z`.
- Title `docs: write release notes kind first, in short plain text`: Conventional Commit, no id.

Render and template

- `bodyHTML` (`W/scratch/pr-bodyhtml-description-pass.json`) -> h2: Summary, Deliverables, Changes,
  Impacts, Blast radius, Test plan, Human decisions, Autonomous decisions, Known gaps, Internal
  references; 3 tables, 1 fold, 7 task boxes all checked, 0 images, 13 `br` (source wraps).
- Against `.github/PULL_REQUEST_TEMPLATE.md`: every template section in order, no template comment
  left, one blast grade explained, the six template boxes plus one `git grep` box. `01-intent.md`
  names no GitHub issue, so no `Fixes #N`.
- Against `pull-request.guidelines.md`: Deliverables after Summary with a before and after table;
  Impacts says "No visual change" with the reason; "Autonomous decisions" present; "Internal
  references" last, before the Claude Code line.

Ids, roles, personal data

- Case-insensitive search of the body copy for change, batch, round and question ids, role names,
  process tool and planning words, user name, drive or home paths, e-mail addresses, `STALE`,
  `UNVERIFIED`, image syntax, `Fixes #` and `agent` -> two hits: line 137 (`CR-523 notes-kind`,
  under "Internal references") and line 20 ("answered by the agent": the content of the delivered
  rule, guideline line 361-362, not a delivery role). No personal data, no image.

Test plan, box by box

- Tests "none", requirements "No behaviour change", changelog "No user-facing change": `git diff
  --name-status origin/main...HEAD` -> only `M .agents/guidelines/release-process.guidelines.md`
  (`1 file changed, 117 insertions(+), 31 deletions(-)`).
- `git grep -n "what you can now do" eb493a3 -- <guideline>` -> line 252 only.
- Local gates: claim 6; re-read here: `W/just-check-eb493a37.log` and `W/preflight-eb493a37.log`
  first lines, preflight ending `ci-static: passed` and the Windows skip line.
- Review: `chantier log CR-523` -> `12:37:23Z driver note ... r1 approved at b9b29c5a...515b52c,
  committed as eb493a3735e3...22b4` (the box's two SHAs). `git diff b9b29c5a eb493a37 | git
  patch-id --stable` and the same on `evidence/guideline-r1.diff` -> both `434aefdd...9299a9`.
- CI: `gh pr checks 554` -> the seven named checks `pass`, every other job `skipping`.

Other claims

- Summary and the before column: `git show origin/main:<guideline>` -> title `X.Y`, "as verbs",
  "what you can now do", "any known issue" under "For contributors", no word budget, no picture
  size, no self-check, hero image for "post 1 and the first highlight".
- "Changes" and the after column against `git diff origin/main...HEAD`: each claimed change is
  there; the delivered ones (step 3 clause, version mismatch, missing picture) are in the table or
  its fold.
- Rule table: claim 4 (carried from eb493a3: same head and same body). Template and topic read
  again: kinds, order, 16 / 20 / 40 / 120 / 250 words, 900 to 1200 px, 600 px agree.
- Dry run: the 1.12.1 note read at the head (rows 1 to 6, 8, 9 hold on the quoted lines);
  `python -I V/count_note_words.py` -> subtitle 18, highlights 111 and 37, lines 31, 32, 37, 45, 47
  at 23, 26, 27, 28, 21 (row 7). Row 10: `gh pr view 496 --json body` (version 1.12.1) -> "Commitizen
  would number 1.13.0; the version is the owner's choice", no "probably wrong".
- Human decisions against `02-answers.md` (Q2 to Q6, performance rule). Autonomous decisions against
  `coder/r1.md`, `02-answers.md` and the diff: the three are there, none found missing.
- Known gaps: read in the guideline at the head (lines 176-210, 215, 260-262, 302-307, 316-317,
  329, 347, 373). Last bullet: constitution section 8 (lines 81-83) says project guidelines name no
  process role; line 347 does. No `UNVERIFIED` claim and no accepted failure needs a bullet.

Noted, no failure

- The "Local gates" box names the targets without the counts the template comment asks for; recent
  merged pull requests 552 and 536 give none either.
- The dry run names no SHA of its own; its subject is a published note the PR does not change.
- Known gap 4, "so a regenerated body needs them added again", is an inference: a statement kept in
  `body-sections.md` (guideline 189-199) would survive a regeneration. The gap itself (the section
  does not say where they go) holds.

## Verifier's own anomaly (first judgment)

One command of mine wrote a scratch diff to `/tmp/head.diff`, outside the folders this agent may
write in (a plain copy of the committed diff, no personal data, unused by any claim). The guard then
refused its removal: "refused: a shell write to /tmp/head.diff is outside the folders this agent may
write in (...); the shell follows the same rule as Write and Edit". It is left there.

VERIFIED
