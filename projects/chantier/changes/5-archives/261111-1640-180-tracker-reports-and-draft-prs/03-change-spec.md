# Report back on tracker issues

issue: https://github.com/gsemet/chantier/issues/101

## Goal

When a change request comes from an issue in the project's tracker (GitHub, GitLab, Jira or any
other), the issue's readers hear what happens to it: what was understood once the grill ends,
the PR on the issue through the forge's own link, the issue closed by the merge, and "Released
in <link>" once a release ships it. It works in any project and on any forge: chantier
hardcodes no tracker's syntax, the project's own rules rank above it, and a CR with no issue
skips all of it. Only the Chief of Staff posts, and only text the user approved.

The second half of the source issue, "draft until mergeable", is already on main and stays as
it is (decision 9): this CR changes nothing about drafts, stacks or turning a PR ready.

## Scope in one look

Cards only, six files under `skills/chantier/references/` (decision 11):

| File | Change |
| --- | --- |
| `concepts.md` | the word "Tracker issue" and its `issue:` line; who may post on an issue |
| `chief-of-staff.md` | record `issue:`; the grill comment; "Released in"; two "Never" lines |
| `griller.md` | record `issue:`; never post on an issue |
| `spec-writer.md` | carry the `issue:` line into the specification |
| `pr-template.md` | the closing line in the body, and its audit line |
| `driver.md` | one line: the PR body's closing line; a Driver never comments on or closes an issue |

No change to the CLI (`skills/chantier/scripts/`), to `foreman.md`, to the agent files
(`agents/`, `com.github.copilot/agents/`), to the host references or to the scenario
(decision 10).

## The `issue:` line (decision 1)

A CR that comes from a tracker issue carries one plain line, `issue: <link>`, where `<link>` is
the issue's full URL (or, for a tracker without URLs, the key the project uses, such as a Jira
key). It is written:

- in `01-intent.md`, by the Chief of Staff or a Griller, at filing (a request filed from a
  ticket) or as soon as the grill learns of the issue;
- in `03-change-spec.md`, by the Spec-writer, copied from `01-intent.md` (or, failing that, from
  `intake/` or `02-answers.md` where the issue is named);
- in the PR body, by the CR Driver, as the closing line below.

Placement: on its own line, directly under the file's `# ` title, after one blank line. Never as
YAML front matter and never as the first non-empty line: the CLI takes a CR's title from the
first non-empty line of `03-change-spec.md`, `01-intent.md` or `intake/request.md`
(`status.py`, `TITLE_FILES` and the loop that reads it), and a `---` or `issue:` first line would
become the title. One CR, one `issue:` line; a CR that answers several issues carries one line
per issue, each `issue: <link>`.

A CR with no `issue:` line skips every rule of this specification.

## Card by card

### `concepts.md`

In "Words", after "Ready to merge", a new entry, about four lines:

- **Tracker issue:** an issue in the project's tracker (GitHub, GitLab, Jira…) that a CR comes
  from, named by an `issue: <link>` line under the title of the CR's `01-intent.md` and
  `03-change-spec.md`. Its PR closes it at the merge through the closing line of the
  [PR template](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/pr-template.md); no agent closes or reopens an issue by hand. Only the Chief of
  Staff posts on an issue, and only text the user approved; a comment carries no CR number,
  batch, agent role or cost (decisions 3, 7, 8).

In the CR folder tree of "Change Request (CR)", the `01-intent.md` comment may add "(and its
`issue:` line)"; optional, the Driver judges whether it fits the tree's width.

### `chief-of-staff.md`

1. **"Backlog and grill"**, the sentence "A ticket (Jira, GitLab, GitHub): read it with what the
   project has, and `file` it as received, with its link." gains: write `issue: <link>` under the
   title of `01-intent.md` (as `concepts.md` says), and add it later if the grill reveals the
   issue (decision 1).
2. **A new paragraph "Tracker comments"**, in "Backlog and grill" after the "Shared
   understanding" paragraph (or as its own short section next to it; the Driver judges), holding:
   - **The grill comment (decision 4).** When the user says a CR with an `issue:` line is grilled
     enough, show the user a short comment for the issue, drawn from the restatement just made:
     what was understood (one or two sentences), the scope in two to five bullets, what is left
     out. Text only: no attachment, no plan file, no demo. Write it in
     `work/issue-comment.md` in the CR's folder, show it, and post it only on the user's yes;
     record the yes (or the user's edits) in `02-answers.md` at once, as any answer.
   - **No "PR opened" comment (decision 5):** the PR's closing line makes the forge show the PR
     on the issue.
   - **How to post (decision 7).** With the forge's CLI the session already uses (`gh`, `glab`),
     when it reaches the issue's tracker: for instance `gh issue comment <link> --body-file
     <file>`, `glab issue note <id> --message …`; read the CLI's help for the exact form. Where
     it does not reach the tracker (Jira or another tracker with no CLI in the session, no
     access): give the user the text to post themselves, and post nothing. A refused or failed
     post is told to the user with its exact text and the text stays in the CR's folder; never
     another tool, never a retry another way (no fallback).
   - **For the tracker's readers (decision 8):** English, as all forge text, unless the project's
     rules say otherwise; no CR number or slug, no batch, round, agent role, cost or
     `.agents/changes/` path. Issues are often public.
3. **"Releases"**, in the paragraph that starts "`status` shows a `draft <path>`" (after "Once
   released"), the "Released in" list (decision 6): once the release Driver has recorded
   `release published` (its note carries the version and the link), list the issues the release
   ships, one line each: the issue's link and the comment "Released in <the release's link>".
   The issues are the `issue:` lines of the CRs whose merge the release contains: the batch's
   `4-batch/3-done/` folders and the `5-archives/` folders merged since the previous release
   (`delivery.md` gives each one's PR and merge time). Show the list; one yes from the user
   covers the whole list; post each as in "Tracker comments" (an issue its CLI cannot reach goes
   to the user as text). No issue in the list: say nothing. "auto" never covers these comments.
4. **"Never"**, two new bullets:
   - Post on a tracker issue a text the user did not approve, or let a Driver, the Foreman or a
     Griller post on one.
   - Close or reopen an issue by hand: the merge closes it through the PR's closing line.

The Foreman's asks are unchanged and carry no `issue:` link: the Chief of Staff reads it in the
CR's folder (decision 10).

### `griller.md`

- In "What you do", the list taken from the Chief of Staff's card gains "the `issue:` line in
  `01-intent.md`" (decision 1).
- In "Never", add: post on a tracker issue, comment on it, close or reopen it (decision 7).
- The grill comment when a Griller ran the grill: see open question 1.

### `spec-writer.md`

In "Output", under "A rich specification holds:", one bullet: the CR's `issue:` line(s), copied
under the specification's title as `concepts.md` places it, when the CR has an issue (decision
1).

### `pr-template.md`

1. **"The rules"**, a new bullet (decision 2): when the CR's specification has an `issue:` line,
   the body's Summary ends with one closing line per issue:
   - the issue is on the PR's own forge (GitHub, GitLab): the forge's closing keyword and the
     reference it reads, `Closes <reference>` (`#<n>` for an issue of the PR's own repository,
     the issue's full link or `<namespace>/<project>#<n>` for another repository of the same
     forge);
   - any other tracker (Jira…): the form the project's rules give; with no such rule, the plain
     link (`Issue: <link>`), which closes nothing.
   The issue's reference is not an internal reference: it is allowed in the body's text. It is
   the only place the issue is named; the Driver never comments on the issue.
2. **"The template"**, the Summary comment gains: "End with one `Closes <reference>` line per
   tracker issue, as the rules say; none when the CR has no issue."
3. **"Scope and precedence"**: with a project template, the closing line goes where that
   template puts its issue link, else at the end of its first section; a project rule on closing
   keywords ranks above this file.
4. **"The audit"**, a ninth line: when the CR's specification has an `issue:` line, the body
   carries its closing line in the form the rules give, and no other text about the issue; when
   it has none, no closing line.

### `driver.md`

One line in the push/PR bullet of the Drivers' common part (the one that starts "Push:" and
says "A CR Driver writes the title and `<work folder>/pr-body.md`"): the body carries the
closing line of each `issue:` of the specification ([pr-template](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/pr-template.md)); a Driver
never comments on, closes or reopens an issue (decisions 2, 3, 7). The stack driver's text
("on another base, a draft") is unchanged (decision 9).

## Decisions carried

1. `issue: <link>` line from intent to specification to PR body: "The `issue:` line".
2. Closing keyword on the PR's own forge, project rule or plain link otherwise: `pr-template.md`.
3. The merge closes the issue, no agent closes or reopens by hand: `concepts.md`,
   `chief-of-staff.md` "Never", `driver.md`, `griller.md`.
4. Grill comment, text only, posted on the user's yes: `chief-of-staff.md` "Tracker comments".
5. No "PR opened" comment: `chief-of-staff.md` "Tracker comments".
6. "Released in", one yes for the whole list: `chief-of-staff.md` "Releases".
7. Only the Chief of Staff posts, approved text only, only where its forge CLI reaches;
   otherwise the text goes to the user: `concepts.md`, `chief-of-staff.md`, `griller.md`,
   `driver.md`.
8. No CR number, batch, role or cost in a comment: `concepts.md`, `chief-of-staff.md`.
9. Draft-until-mergeable unchanged, stacked "ready on its own" dropped: no change to
   `driver.md`'s stack driver, `concepts.md` "Ready to merge" or `foreman.md`.
10. Foreman asks and CLI unchanged.
11. Cards only, the six files named; `tracker-grill-summary` exists nowhere, nothing to remove.

Choices this specification makes within the decisions, for the reviewer: the `issue:` line sits
under the title rather than in front matter (the CLI's title reading); the draft comment lives
in `work/issue-comment.md`; the closing line ends the Summary; the Inspector's audit gains a
line for it; the "Released in" list is drawn from `3-done/` and `5-archives/` via `delivery.md`.

## Out of scope

- Attachments on an issue (a plan, an HTML demo), and a "PR opened" comment (decisions 4, 5).
- Any change to drafts, stacks, "ready to merge", the Foreman's asks or the release Driver's
  hand-back (decisions 9, 10; the request's `foreman.md` and release-driver items are dropped).
- Any CLI command, field, parser or allow rule for issues; any tracker-specific syntax beyond
  the closing keyword's example.
- Closing, reopening, labelling or transitioning an issue by an agent (the forge's merge does
  the closing).
- The docs, the README and the diagrams.

## Evidence

- `just check` passes (structure tests, lint, both hosts' agent bodies still identical since no
  agent file changes).
- `just scenario` passes: this is a card change (AGENTS.md).
- `git diff --stat origin/main` lists only the six cards (and the CR's archive when `take` asks
  for it); nothing under `skills/chantier/scripts/`, `agents/`, `com.github.copilot/agents/`,
  `scenario/` or `foreman.md`.
- `rg -n "issue:" skills/chantier/references` shows the line in `concepts.md`,
  `chief-of-staff.md`, `griller.md`, `spec-writer.md`, `pr-template.md` and `driver.md`.
- `rg -n -i "Released in" skills/chantier/references/chief-of-staff.md` finds the release list;
  `rg -n -i "issue" skills/chantier/references/foreman.md` finds nothing new.
- A read-through of each changed paragraph against the ten decision lines above: each decision
  present, none contradicted; new lines wrapped like their neighbours (about 100 columns).
- The PR of this CR itself carries `Closes #101` at the end of its Summary, as the new
  `pr-template.md` rule asks.

## Open questions

None. The one raised is settled in `02-answers.md`: a Griller writes the proposed grill comment
in `work/issue-comment.md` and tells the user the Chief of Staff will offer it; the Chief of
Staff offers it when it next reads that CR's folder.
