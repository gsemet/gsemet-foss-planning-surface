# Change spec: name the release report `04-report.md` in the release CR

Commit type `docs:` (no scope: scopes are only for `feat` and `fix`). Priority P1, in batch-02,
before it closes.

## Goal

The release report must have a name a subagent can write. For v1.8.0, the harness refused the
Release driver's Write of `report.md` in the release CR's folder ("Subagents should return
findings as text"), while `retro.md` was accepted. A name with a number in front works. The name
`report.md` also clashed with chantier's own progress report in the same folder: v1.7.1's
`report.md` held both.

The owner decided (`01-intent.md`, `02-answers.md`, 2026-11-13):

- The project's release report is `04-report.md`, in the release CR's folder, next to
  `01-intent.md`, `02-answers.md` and `03-change-spec.md`. The v1.8.0 archive already uses it
  (`.agents/changes/4-archives/261113-0726-313-release-v1-8-0/04-report.md`).
- The project changes only. The chantier side is already fixed.
- The missing "Released in" comment is posted on GitHub (see "GitHub issue comment" and the open
  question below).

## What changes

Read the files on `origin/main` (`git fetch` first). The release-process guideline changed in
v1.8.0.

### `.agents/guidelines/release-process.guidelines.md`

Two mentions, both in "The steps of a release":

- Step 7 (line 89): "The release is archived with a `report.md`: ..." becomes "The release is
  archived with a `04-report.md` in the release CR's folder, next to `01-intent.md`,
  `02-answers.md` and `03-change-spec.md`: ...". Add one short clause with the reason: a subagent
  cannot write some Markdown names, such as `report.md`, but a numbered name works. The rest of the
  step (tag, release URL, CI runs, closed issues, `retro.md` next to it) stays as it is.
- Step 8 (line 98): "write that line in `report.md`" becomes "write that line in `04-report.md`".

`retro.md` keeps its name: the harness accepted it.

### `.agents/guidelines/change-requests-lifecycle.guidelines.md`

One mention, in "Release driver", the "Lists" bullet (line 352): "No issue closed by this release:
the line goes in `report.md`" becomes "... the line goes in `04-report.md`".

The other `report.md` mentions of this guideline are the archive report of every landed CR, not
the release report. They stay (see "Out of scope").

### Search to run before the commit

`git grep -n "report\.md"` on the branch. The release report must not be named `report.md`
anywhere. The hits that must remain, because they name other reports:

| File | What it names |
| --- | --- |
| `.agents/guidelines/change-requests-lifecycle.guidelines.md` lines 50, 76, 128, 178, 231, 264, 497 | the archive report of every landed CR (step 12, section "`report.md` (archive)") |
| `.agents/guidelines/owner-review.guidelines.md` line 12 | the same archive report |
| `scripts/generate_orchestrator.py`, `test/build/test_generate_orchestrator.py` | the same archive report, read for the status table |
| `.agents/skills/markdown-studio-exploratory-qa/` | the QA run report |
| `justfile`, `.agents/skills/okfreq*/` | `requirements-report.md` |

If the search finds another mention of the release report, change it too and name it in the PR
body.

### GitHub issue comment

The comment follows the issue rule of step 8 of the release-process guideline and the wording of
the comments already posted on #334 and #336:

```text
Released in [Markdown OKF-Schema Studio 1.6.0](https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.6.0). Update the extension from the Marketplace or the Extensions view to get it.
```

Post it on **#335** with `gh issue comment 335 --body '...'`, then read it back with
`gh issue view 335 --json comments`. Post nothing on #336 (see Decisions).

## Out of scope

- The chantier plugin (the Release driver card, how a driver hands back its report): the owner
  says it is already fixed.
- The archive `report.md` of ordinary CRs (lifecycle step 12, `scripts/generate_orchestrator.py`,
  the owner-review table): it is not the release report.
- Renaming the `report.md` files of past release archives in `.agents/changes/4-archives/`
  (git-ignored local history).
- `CHANGELOG.md`: a `docs` change adds no line.
- Any requirement (SwRS or StRS): no behaviour of `src/` changes.

## Evidence

- `git grep -n "report\.md"` on the branch: no mention of the release report remains; the
  remaining hits are the ones in the table above.
- `git diff origin/main --stat`: only the two guideline files change.
- `just check`, then `just preflight` green (completion gate, constitution section 4).
- The PR body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR opens as a draft
  (`pull-request.guidelines.md`).
- The comment on #335, read back with `gh issue view 335`.

## Decisions

1. **The issue that gets the comment is #335, not #336** (Chief of Staff, 2026-11-13, checked on
   GitHub). The intent named #336 from a relayed note that had the numbers wrong:
   - #334 and #336 already have "Released in 1.6.0".
   - #335 (closed by PR #337, merge commit `ede6863e`, first tag v1.6.0) has no comment at all.
     The v1.6.0 archive report lists #336 and #334, not #335: that is how it was missed.

   The owner's intent is to fix the missing comment, so it goes on #335 and nothing on #336.
