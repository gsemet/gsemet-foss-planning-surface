# CR-103 posted description pass

Head: a2723b7a0cdea34d9fe3601f3081b21ea424d07d

Base: 125952dc04a949cc78810e2340ef57d9ffa6ba5e. Description of PR 73 only. The full
verification at this head stays in `work/verify.md`, unchanged and not run again.

Verdict: VERIFIED. No failed claim.

## D1. Posted body and forge (a2723b7)

`gh pr view 73 --json ...`: OPEN, draft, `headRefOid a2723b7a...`, `baseRefOid 125952dc...`
(CR-102's branch), `mergeable MERGEABLE`, title
`feat(cli): print concepts as stored and add a trust command`.

`edits.py` on `gh pr view 73 --json body` and the GraphQL `userContentEdits`:

```text
lastEditedAt 2026-11-25T23:58:42Z
latest edit == posted body: True
posted lines == pr-body.md lines: True
starts with BOM: False
username or home -> []
image -> []
marks -> []            (STALE, UNVERIFIED)
literal backslash-n -> []
sha-like: ['1a742d7', '6572527', 'a2723b7']
<details> 1
</details> 1
<summary>Details</summary> 1
headings: Description, Type of Change, Checklist, Related Issues, Blast radius, Autonomous
  decisions, Known gaps, Changes, Human decisions, Impacts, Test plan, Internal references
internal refs before last section -> []
```

Line diff of the edit of 23:45:31Z (the body the earlier pass read: its verdict is 23:53:35Z)
to 23:58:42Z: the caption line added; the boxes "New or changed tests", "Evidence" and
"Verified" checked with their SHAs; `work/verifier/evidence/before-after.md` added to Internal
references. No other line changed.

`gh api repos/gsemet/okf-schema/pulls/73` (`body_html`): sections render as headings, the
diagram as a code block with the caption as its own paragraph, task boxes, one `<details>`
holding Changes to Internal references. No image.

## D2. Project template (a2723b7)

`.github/pull_request_template.md` has Description, Type of Change, Checklist (4 items),
Related Issues: all present, in that order, filled. `03-change-spec.md` line 3
`issue: .../issues/58`; body `Fixes #58`. The added sections follow Related Issues.

## D3. Caption "Before at `1a742d7`, after at `a2723b7`."

- After: `evidence/scenario-run.txt` says `Run at head a2723b7a...`: `show` output
  byte-identical (also broken, plain, Latin-1, empty stderr), `trust: unverified`, then
  `trust: human-reviewed` + `stale: true`, `Result: 0 failed check(s)`.
- Before: `work/verifier/evidence/before-show.txt` and `before-trust.txt`, wheel of
  `1a742d7`: rewritten frontmatter with `trust:` and `stale: true` lines;
  `Error: No such command 'trust'.`
- `git merge-base --is-ancestor 1a742d7 a2723b7` -> exit 0.
  `git diff --stat 1a742d7 125952d -- src/okf_schema/cli.py
  src/okf_schema/_internal/models.py src/okf_schema/_internal/yaml.py
  tests/acceptance_support.py` -> empty: the before still describes the current base.

## D4. "New or changed tests ... at `a2723b7` (carried from `6572527`)"

`git diff <base> <head> -- src tests docs requirements/tiers/swrs | git patch-id --stable`:
`d8aba34eddde664ae81b51af3e1f1685ecd664db` for `1a742d7..6572527` and `125952d..a2723b7`.
`work/verifier/base-tests.log`: `34 failed, 186 passed`; the 34 names are the 4 changed or new
tests of `test_api.py` and the 30 new ones of `test_cli_remaining.py` seen in
`git diff 125952d a2723b7 -- tests`. The one new test absent from the list is
`test_show_bundle_refuses_a_file_that_is_not_utf8`. The changed acceptance test fails on the
base (`evidence/acceptance-windows.txt`, carried part). Head: `work/verify.md` C2, C3, C8.

## D5. "Evidence: before at `1a742d7`, after at `a2723b7` (carried from `6572527`; ...)"

`before-after.md`: before `1a742d7`, after `6572527`, carried to `a2723b7` with its reason;
`after-show.txt`, `after-trust.txt` name `6572527`. `scenario-run.txt` names `a2723b7`.
Text files only; "No pair is missing."

## D6. "Verified at `a2723b7` (...)"

`chantier log CR-103`: `2026-11-25T23:53:35Z driver verdict result=VERIFIED
head=a2723b7a... base=125952dc...`. `work/verify.md`: `Head: a2723b7a...`, `Verdict: VERIFIED`;
carried from `6572527`: the base-side test run (C8) and description claims (C6, C7, C10).

## D7. Internal references and other proofs

`ls -l work/coder/r1.md evidence/scenario-run.txt evidence/acceptance-windows.txt
work/verifier/evidence/before-after.md` -> all four exist.
`gh pr checks 73`: preflight 3.10 to 3.13, macos-latest, windows-latest `pass`, tag-release
`skipping` (run 45723093438). `gh pr view 70` -> OPEN, head `125952d...`; `gh pr view 69` ->
MERGED. Gate log `work/gates/20261126-003844.log`: first line names `a2723b7a...`, last
`result: pass at a2723b7a...`. Text not edited since: carried from `work/verify.md` C10.

Known gaps: `work/verify.md` has no failed claim, the body no `UNVERIFIED` mark, and
`before-after.md` no missing pair; the bullets are those C5 to C7 judged.

## Refusal and writes outside the writes folders

Write tool, on a script in the session scratchpad:
`refused: C:/Users/gaeta/AppData/Local/Temp/claude/143d8cc0d12f7200/05edfd91-309f-433f-8c7f-e4569f24649b/scratchpad/edits.py is outside the folders this agent may write in (C:/Users/gaeta/Projets/okf-schema.worktrees/batch-01-CR-103; C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/okf-schema/changes/4-batch/2-actives/103-show-as-stored); write there`
The script was then written under `work/scratch/vd`. Before that refusal, two shell redirects
of mine had already written `posted-body.md` and `edits.json` into that session scratchpad,
outside the writes folders (the second command ended on `jq: command not found`). Both files are
left there. No claim above rests on them: both were fetched again into `work/scratch/vd`, which
is removed at the end.
