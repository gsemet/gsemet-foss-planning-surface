# Verify CR-231

Head: 07784001ab18dc8f9c907f1bba0a60b095eb9d7b

All claims judged at 07784001ab18dc8f9c907f1bba0a60b095eb9d7b (worktree clean, `git status --short` empty, local = origin branch head `07784001ab18dc8f9c907f1bba0a60b095eb9d7b`).

## C1 Gate pass at this head (E1/E2: check + scenario, retro sections unchanged and green) - 07784001ab18dc8f9c907f1bba0a60b095eb9d7b
Command: `Get-Content work/gates/20261113-211558.log -TotalCount 1` and `-Tail 4`
Output: first line `gate CR-231 branch chantier/batch-17/cr-231-change-specification-the-batch-retro-spl head 07784001ab18dc8f9c907f1bba0a60b095eb9d7b`; github `695/695 checks passed`; gitlab `676/676 checks passed`; `result: pass at 07784001ab18dc8f9c907f1bba0a60b095eb9d7b`. VERIFIED. CI not waited on (told so).

## C2 E3 diff touches only the six listed files - 07784001ab18dc8f9c907f1bba0a60b095eb9d7b
Command: `git diff origin/main --stat`
Output: docs/use-cases-foreman.md, chief-of-staff.md, concepts.md, driver.md, foreman.md, status-layout.md; 6 files, 94 insertions, 34 deletions. No CLI, agents, hooks, types. VERIFIED.

## C3 Tag in foreman.md, two-lines rule, untagged read as project, no-problem line untagged, escalation takes cause's tag, project->inbox / chantier->GitHub issue - 07784001ab18dc8f9c907f1bba0a60b095eb9d7b
Command: `git diff origin/main -U1 -- skills/chantier/references/foreman.md`
Output: line format `- [<tag>] <problem>: <long-term fix>`; both tags defined; "A cause on both sides is two lines"; "an escalation line takes the tag of its cause"; "one untagged line saying so"; "an untagged line of an earlier pause reads as project"; last sentence offers project as inbox item and chantier as GitHub issue. VERIFIED.

## C4 Same format in direct-mode pause, release retro, concepts.md - 07784001ab18dc8f9c907f1bba0a60b095eb9d7b
Command: `git diff origin/main -U1 -- chief-of-staff.md driver.md concepts.md`
Output: chief-of-staff direct pause uses `- [<tag>]` with both-sides = two lines; driver.md release step uses `- [<tag>] <problem>: <long-term fix>`; concepts.md item 3 says tagged project or chantier, project ones as inbox items, chantier ones as an issue on chantier's repository, before any close. VERIFIED.

## C5 Completion report (status-layout.md, table row) - 07784001ab18dc8f9c907f1bba0a60b095eb9d7b
Command: `git diff origin/main -U1 -- status-layout.md chief-of-staff.md`
Output: `<n>. [<tag>] <problem>: <long-term fix>`, one numbering across both tags; chantier point matching an open issue names its link; For you lists project points to file and chantier points to draft (several per issue) and the project-is-chantier line; table row now "the Retro offered, by route". VERIFIED.

## C6 Two routes in the pause bullet - 07784001ab18dc8f9c907f1bba0a60b095eb9d7b
Output (same diff): project point unchanged with `\ file`; chantier point never filed with file except in chantier's own repo; user may move a point and the CoS says the new route; release retro offered once, each by its tag. VERIFIED.

## C7 Chantier route steps 1-7 - 07784001ab18dc8f9c907f1bba0a60b095eb9d7b
Output (same diff, bullet "The chantier route"): 1 repository = manifest `repository` field, both manifest paths; 2 `gh issue list --repo <owner/name> --state open --search` with skip-and-say when gh absent; 3 draft `4-batch/chantier-issue-<n>.md`, Write tool, UTF-8 no BOM, title first line Bug:/Feature:, version, host, retro line, English; 4 public-repo check list (project name, private path, code/text, CR/slug/batch id, person) with inbox fallback; 5 show and ask per issue, user may edit/regroup/decline/post; 6 `gh issue create --repo ... --body-file` on yes only, only the CoS, fallback path and new-issue link, no label; 7 no record, drafts deleted by close. Also "nothing is drafted unless the user named the point". VERIFIED.

## C8 Project is chantier itself (E5) - 07784001ab18dc8f9c907f1bba0a60b095eb9d7b
Commands: `git remote get-url origin`; `Select-String repository .claude-plugin/plugin.json`; same for `.github/plugin/plugin.json`
Output: `https://github.com/gsemet/chantier` ; `"repository": "https://github.com/gsemet/chantier",` (both manifests). Equal. The card carries the comparison rule and the exact one-line text, default inbox. VERIFIED.

## C9 Docs line - 07784001ab18dc8f9c907f1bba0a60b095eb9d7b
Command: `git diff origin/main -U1 -- docs/use-cases-foreman.md`
Output: "Each point is tagged for the project or for chantier: a project point becomes an inbox item, a chantier point a draft issue on chantier's GitHub repository, each only on your word." VERIFIED.

## C10 E4 worked example against the cards - 07784001ab18dc8f9c907f1bba0a60b095eb9d7b
Command: `Get-Content work/e4-example.md` (checked against C3-C8; pr-body.md worked example not re-judged, PR description is a later pass)
Output: four-line retro, 2 project and 2 chantier, lines 1 and 2 a two-sided split; report numbered 1-4 in one sequence with tags; For you lists project 1,3 and chantier 2,4; draft issue has Bug: title, what happened, fix, version 0.9.0, host, retro line; contains no project name, path, CR/batch id, person; gh command only described, nothing posted; E5 block shows the match. Consistent with the cards. VERIFIED.

## C11 Out of scope respected - 07784001ab18dc8f9c907f1bba0a60b095eb9d7b
Command: `git diff origin/main --stat` (C2): no CLI, agents/, hooks/, types/, scenario change. VERIFIED.

## Before/after
See work/before-after.md: not capturable by command (card-only change, no runtime behaviour); the before/after text is the diff above.

VERIFIED


## Description pass - 07784001ab18dc8f9c907f1bba0a60b095eb9d7b
Command: `gh pr view 167 --json body,headRefOid -q '.headRefOid,.body'`
Output: head 07784001ab18dc8f9c907f1bba0a60b095eb9d7b; body has Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps, Details; renders as plain Markdown with closed code fences and one details block. Every proof SHA is `0778400` except Review (`4c0c6d7`). OK.
Command: `git diff --stat origin/main...HEAD`
Output: 6 files (docs/use-cases-foreman.md, chief-of-staff.md, concepts.md, driver.md, foreman.md, status-layout.md), cards and one doc, no code: matches Changes and "Blast radius 1". OK.
Command: `git diff origin/main -- skills | Select-String 'chantier-issue|Bug:|no label|close'`
Output: draft path `4-batch/chantier-issue-<n>.md`, `Bug:`/`Feature:` title, no label, drafts deleted by `close`: matches Autonomous decisions. OK.
Command: `$CHANTIER log CR-231 --batch batch-17`
Output: `driver note note=move e20fa7b..4c0c6d7 (rebase) inspector approved at 4c0c6d7`; the Review box matches it, carried over a clean rebase (note "rebase onto 2934943 clean, head 0778400"). Gates at 0778400 pass for check and scenario, verdict VERIFIED at 0778400. OK.
Command: `gh pr checks 167`
Output: just check (macos, ubuntu, windows) pass, just eval-dry-run pass, just scenario pass. Matches the CI box. OK.
Known gaps: no live `gh issue create` is the only gap; no pane change so no screenshot needed. Complete. Role names appear only as product terms (the Chief of Staff posts, card names in the worked example) and under file names; Internal references holds the CR id. OK.

VERIFIED
