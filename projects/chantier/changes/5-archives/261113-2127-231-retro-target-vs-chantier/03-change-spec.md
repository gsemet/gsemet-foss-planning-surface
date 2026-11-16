# Change Specification: the batch retro splits the target project from chantier itself

## Goal

The user's words (2026-11-13, `02-answers.md` answer 3, recorded in English): the retro chantier
leaves "must focus on the target project, and when a point impacts how chantier works, it goes
through a feature request or bug report on GitHub". Today every retro point is offered as an inbox
item of the project the batch ran in, even when its cause or fix is in chantier's own cards, CLI,
agents or host use; those points then sit in a backlog that cannot fix them.

After this CR, each retro point carries a tag, `project` or `chantier`. The project's points are
offered as inbox items, as today. chantier's points are offered as a GitHub issue on chantier's
repository: a draft the user posts, or lets the Chief of Staff post, never filed in the project's
backlog. When the project is chantier itself, the Completion report says which route applies.

## Decisions carried from `02-answers.md`

| Decision | Where this spec carries it |
| --- | --- |
| 1. The proposal as filed (`intake/request.md`) is the scope; points it does not settle take this specification's defaults, listed as open points | All sections; "Open points" |
| 2. The CR joins the running batch-17 | "Order in batch-17" |
| 3. Retro points about the target project stay inbox items; points about chantier's way of working go through a feature request or bug report on GitHub; posting an issue stays the user's yes, per point | "The tag", "The chantier route", "Posting" |

## Order in batch-17 (CR-221)

This CR changes cards and one doc page only: no file of `skills/chantier/scripts/cli/`, no
`hooks/`, no `types/`, no scenario check. It does not wait for CR-221 (`python-inline-deps`), and
needs no `depends.json`. The retro's CLI side (`close` keeping `4-batch/retro.md`,
`commands._retro_target`, `_batch_files`) is untouched: a tagged line is still a line of
`retro.md`, kept whole.

## What changes

### 1. The tag (who writes the retro)

A retro line becomes `- [<tag>] <problem>: <long-term fix>`, with `<tag>` one of:

- `project`: the cause or the fix is in the target project (its code, tests, CI, rules,
  `AGENTS.md`, `chantier.yaml`, its forge or infrastructure).
- `chantier`: the cause or the fix is in chantier's own way of working: its cards, its CLI, its
  agent files, its skills, or how it drives the host (Claude Code, Copilot) and the forge.

The writer judges the tag. A point with a cause on both sides is written as two lines, one per
tag, each with its own fix. The line "no problem met" (a batch with no problem) carries no tag.
An escalation line (`concepts.md`, "Said, never silent") takes the tag of its cause like any
other line. Sections already written stay as they are (never rewritten); an untagged line from
an earlier pause is read as `project`.

Edits:

- `skills/chantier/references/foreman.md`, "Your goal" (lines 24-33): the line format becomes
  `- [<tag>] <problem>: <long-term fix>`, with the two tags defined as above and the two-lines
  rule; the last sentence ("The Chief of Staff offers each point to the user as an inbox item")
  becomes: the Chief of Staff offers each `project` point as an inbox item and each `chantier`
  point as a GitHub issue on chantier's repository.
- `skills/chantier/references/chief-of-staff.md`, "Steering a batch yourself", bullet "The pause"
  (lines 813-821): the same line format and tags for the retro the Chief of Staff writes in
  direct mode.
- `skills/chantier/references/driver.md`, the release step (lines 519-522): the release's
  `work/retro.md` uses the same line format and tags.
- `skills/chantier/references/concepts.md`, "Batch lifecycle", item 3 "Paused" (lines 132-137):
  each problem is tagged `project` or `chantier`; the Chief of Staff offers the `project` ones
  as inbox items and the `chantier` ones as an issue on chantier's repository, before any close.

### 2. The Completion report

`skills/chantier/references/status-layout.md`, Completion report (lines 110-118):

- **Retro:** one numbered list, as today, each line `<n>. [<tag>] <problem>: <long-term fix>`.
  The numbering stays one sequence across both tags, so the user answers by number. A `project`
  point that matches an inbox or backlog item names that item (as today); a `chantier` point that
  matches an open issue on chantier's repository names that issue's link (see 4).
- **For you:** which `project` points to file as inbox items (by their numbers), which
  `chantier` points to draft as an issue (by their numbers, several may go in one issue), then
  the rest as today.

`skills/chantier/references/chief-of-staff.md`, row "the `final` message" of the table (line
28): "the Retro offered" becomes "the Retro offered, by route".

### 3. The two routes (the Chief of Staff)

`skills/chantier/references/chief-of-staff.md`, bullet "The pause" of Foreman mode (lines
653-662), which the direct-mode pause (line 820) and the release paragraph (lines 944-947) refer
to:

- A `project` point: unchanged. On the user's word for it, `$CHANTIER file "<the point>"` files
  it in `1-inbox`.
- A `chantier` point: never filed with `$CHANTIER file` (except in chantier's own repository,
  see 5). On the user's word for one point or a group of points, it goes the chantier route (4).
- The user may move a point to the other route ("13 is a project point"): the Chief of Staff
  follows that word, and says the route it now takes.
- A release's `work/retro.md` is offered once, with the batch's, each point by its own tag.

### 4. The chantier route: the draft issue, then the user's yes

A new short block in `chief-of-staff.md`, placed right after the Foreman-mode "The pause"
bullet (or as its sub-list), steps in this order:

1. **The repository.** chantier's repository is the `repository` field of the plugin manifest
   (`<plugin root>/.claude-plugin/plugin.json` on Claude Code, `<plugin root>/.github/plugin/plugin.json`
   on Copilot; both say `https://github.com/gsemet/chantier` today). The card names the field,
   not the URL, so a fork's manifest points to the fork.
2. **Already reported?** When `gh` reaches that repository (`gh issue list --repo <owner/name>
   --state open --search "<key words>"`), a point that matches an open issue is named with that
   issue's link and not drafted again. When `gh` is absent or does not reach it, skip this check
   and say so in one line.
3. **Draft** one file per issue, written with the host's Write tool (UTF-8, no BOM, concepts rule
   9): `4-batch/chantier-issue-<n>.md`, where `<n>` is the number of the first point it carries.
   Its first line is the title (`Bug: …` when chantier did something wrong, `Feature: …` when
   it lacks a means); then the body: what happened (the problem), the long-term fix proposed,
   chantier's version (`$CHANTIER --version`) and the host and its version when known, and one
   line saying it came from a batch retro. One point per issue, or a few points with one cause
   grouped into one issue, as the user chose. The language is English.
4. **Check before showing.** chantier's repository is public: the draft holds no project name,
   no private path (a home folder, a drive letter, the planning folder's path), no code or text
   of the target project, no CR number, slug or batch id, no person's name or data. A point that
   cannot be said without them is said in general terms; if it still cannot, say so and offer it
   as an inbox item instead.
5. **Show and ask, per issue.** The title and body as text in the chat, the repository's link,
   and the tool that will post it. Ask for a yes for that issue. The user may edit, regroup,
   decline, or post it themselves (the file's absolute path is given for that).
6. **Post, on the yes only, by the Chief of Staff only:** `gh issue create --repo <owner/name>
   --title "<title line>" --body-file <the draft without its title line>` (the body in its own
   file, `4-batch/chantier-issue-<n>-body.md`, so no text is typed in the command). Give the
   user the issue's link. When `gh` is absent, not logged in, or refused, nothing is posted: give
   the user the file's path and the repository's "new issue" link, and say what is missing. No
   label is set.
7. **No record.** The drafts stay in `4-batch/` until `close`, which deletes them with the
   batch's other files (`_batch_files`); the retro itself is not rewritten. The link of a posted
   issue is said in the chat only.

Drafting and posting happen at the pause, before any `close`, like the inbox route. Nothing is
drafted unless the user named the point for this route.

### 5. When the project is chantier itself

The project is chantier itself when its forge remote (`git remote get-url origin`) is the
manifest's `repository` (compared without a trailing `.git` or `/`, ignoring case). Then both
routes meet, and the Completion report's "For you" says, in one line, which applies: "This
project is chantier: its `chantier` points are filed here as inbox items, like the project's;
say 'as an issue' for a point to go to GitHub instead." The default route is the inbox (open
point 2).

### 6. Docs

`docs/use-cases-foreman.md`, line 159-160: "each point becomes an inbox item only on your word"
becomes: each point is tagged for the project or for chantier; a project point becomes an inbox
item, a chantier point a draft issue on chantier's GitHub repository, each only on your word.

No SVG changes: the diagrams say `retro.md` and "long-term fixes", still true.

## Out of scope

- Any CLI change: no tag check in `close`, `status` or `file`, no new command to post an issue
  (the agents operate `gh`; a tool would need a measured cost first).
- The agent files (`agents/`, `com.github.copilot/agents/`): the contract stays in the cards.
- Issue templates or labels on chantier's repository.
- A GitLab or other forge for chantier's repository (it is on GitHub).
- Retro points from an eval run (`evals/`), and the Chief of Staff's own retro after a release
  that the user's sessions do outside the cards.
- Re-tagging the retro of a batch already paused before this CR merges (untagged lines read as
  `project`).
- `hooks/`, `types/`, the STATUS files and the pane: unchanged (no screenshot, no `just mod`).

## Evidence

- **E1.** `just check` passes on Windows, then in CI on Linux, macOS and Windows.
- **E2.** `just scenario` passes (AGENTS.md: a change to the cards passes it before its PR); its
  retro steps (sections 11 and 11c) are unchanged and green, which shows a tagged line is kept
  whole by `close`.
- **E3.** `git diff main --stat` touches only `foreman.md`, `chief-of-staff.md`,
  `status-layout.md`, `concepts.md`, `driver.md` (under `skills/chantier/references/`) and
  `docs/use-cases-foreman.md`.
- **E4. A worked example in the PR body.** A sample `4-batch/retro.md` section of four lines
  (two `project`, two `chantier`, one of them a two-line split), the Completion report's Retro
  and "For you" lines it yields per `status-layout.md`, and the draft issue file the card's
  steps 3-4 yield for one `chantier` point, checked against step 4's list (no project name,
  path, CR or batch id). Written by hand from the cards, as the cards' reading; no issue is
  posted on chantier's repository for the proof.
- **E5.** The text of the "project is chantier itself" line, and the remote comparison of step
  5 run in this repository (`git remote get-url origin` against the manifest's `repository`),
  showing the match.

## Open points (defaults taken, for the Chief of Staff to confirm with the user)

1. **Tag spelling.** Default: `[project]` and `[chantier]` at the head of the line. Alternative:
   two sub-headings per pause section.
2. **chantier's own repository.** Default: when the project is chantier, its `chantier` points
   go to its inbox like the others (the backlog there is chantier's), an issue only on the
   user's word. Alternative: always a GitHub issue, so chantier's feedback is public in one place.
3. **Where the drafts live.** Default: `4-batch/chantier-issue-<n>.md`, deleted by `close`, the
   posted link said in the chat only. Alternative: keep the link in the retro (an appended line)
   so the archive shows what was reported.
4. **Kind and labels.** Default: the title starts with `Bug:` or `Feature:`, no label set.
   Alternative: labels (`bug`, `enhancement`) when the repository has them.
5. **Host problems.** Default, as the request lists it: a point caused by the host (Claude Code,
   Copilot) is tagged `chantier`, and the issue says it may belong upstream. Alternative: a third
   route, the host's own issue tracker.
6. **Duplicate check.** Default: open issues only, by key words, skipped without `gh`.
   Alternative: closed issues too.
