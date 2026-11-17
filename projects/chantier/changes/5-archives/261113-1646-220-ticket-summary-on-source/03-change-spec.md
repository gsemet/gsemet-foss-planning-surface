# Change Specification: ticket-summary-on-source

Post the grill summary, a plan and a demo on the source ticket, on the user's yes, and name the
ticket in the PR's `## Issues References` section.

No `issue:` line: this CR comes from the user's chat (`intake/request.md`), not from a tracker
issue.

## Source of the decisions

The grill is `intake/request.md`: the user's own text of 2026-11-13, decided, and its section
"2026-11-13, the user's question to the Chief of Staff": all three trackers in scope; the
project's rules first; Jira's access method not fixed; the PR's `## Issues References` section
and its default forms. There is no `01-intent.md` or `02-answers.md`; the request is the decision
record. The user ordered it done now.

This CR **changes four decisions of CR-180 tracker-reports-and-draft-prs** (its `02-answers.md`,
2026-11-11, decided by an advisor on the user's delegation). The user's own request of 2026-11-13
wins:

- decision 4 ("text only: no attached plan, no HTML demo"): a plan and a demo are now posted;
- decision 5 ("the PR opened comment is dropped"): a one-line follow-up is now proposed;
- decisions 2 and 3 (the PR body's `Closes <reference>` line, and the issue closed by it at the
  merge): the closing line moves into a `## Issues References` section, with a closing verb on every
  tracker (`Closes #<n>` on GitHub and GitLab, `Closes <KEY>-<n>` on Jira), so the issue closes
  at the merge. The user first chose a bare `#<n>`, then, told on 2026-11-13 that it would not
  close the issue, chose the verb.

It also replaces the current "give the user the text to post" route for a tracker chantier cannot
reach with "skip and say so in one line" (request, "Rules"). Every other CR-180 decision stays:
the `issue:` line, no agent closes or reopens an issue by hand, "Released in", only the Chief of
Staff posts, no internal terms in a comment.

## Goal, in the user's terms

When a change comes from a ticket (GitHub, GitLab or Jira) opened by someone else, the reporter
learns what was accepted before any code: at the end of the grill, chantier drafts a short
comment, a plan and (when it makes sense) a demo page, shows them to the user, and posts them on
the ticket only after the user's explicit yes for that ticket. When the PR opens, it proposes a
one-line follow-up with the PR link, under the same rule, and the PR names the ticket in its own
section. The project's own rules (its `AGENTS.md` and what `$CHANTIER rules` lists) rank above
every default below.

## What changes

Cards, docs and the eval kit only. The CLI (`skills/chantier/scripts/cli/`), the agent files
(`agents/`, `com.github.copilot/agents/`), `hooks/` and `types/` do not change.

### 1. `skills/chantier/references/chief-of-staff.md`

**a. Intake (the ticket paragraph at the end of "Backlog and grill", today lines 157-159).**
Unchanged in substance: the source ticket is recorded as the existing `issue: <link>` line under
the title of `01-intent.md`. The link carries the tracker and the number; no other field is
added. Add: a Jira ticket's link is its browse URL (`https://<site>/browse/<KEY>-<n>`).

**b. Replace the "Tracker comments" block (today lines 188-210) with a "Ticket summary" block**
holding the steps below, in this order. A CR with no `issue:` line skips the whole block, and the
Chief of Staff says so in one line only when the user asked about the ticket.

1. **When.** When the user says a CR with an `issue:` line is grilled enough (the same moment as
   today's grill comment), in the same turn as the spec-writer's start.
2. **Can chantier write to that tracker?** Decided before any draft, from what the session has:
   - GitHub: `gh`, already used by the session, reaching the issue (`gh issue view <link>`).
   - GitLab: `glab`, reaching the issue (`glab issue view <id>`).
   - Jira, and any other tracker: the access method is not fixed (an MCP server, a CLI or another
     tool). The project's rules say which, when they do. Otherwise the Chief of Staff looks for
     the capability it has (the session's MCP tools for that tracker, an installed CLI) and uses
     the one it finds, provided it reads the ticket. The card names no Jira CLI and no MCP
     server. A configuration that fixes the method may come later; it is out of this CR's scope.
   - No capability found, or no access: **skip** the step and tell the user in one line, naming
     what is missing (for example "no way to write to Jira found in this session (no MCP tool, no
     CLI): nothing drafted for <KEY>"). Nothing is drafted, nothing is posted.
3. **The project's rules first.** Read what `$CHANTIER rules` lists for any rule on tickets: the
   tracker, its access method and project key, the reference form and closing keyword (for
   instance "tickets in this project use `Closes JIRAJPT-1245`"), the comment's language, a
   comment template. Where a rule speaks, it is followed; the defaults of this block apply only
   where the project says nothing.
4. **Draft, in the CR's `work/` folder** (UTF-8, no BOM, written with the host's Write tool):
   - `work/issue-comment.md`, **the comment**: accepted or not; the scope in two to five bullets;
     what is left out; the line "No date yet; the pull request will be linked here." When the plan
     and the demo go as separate artifacts or attachments, one line links them (filled after they
     are posted, step 7). Written for the reporter: no CR number or slug, batch, round, agent
     role, cost, requirement ID or `.agents/changes/` path.
   - `work/issue-plan.md`, **the plan**: the grill's decisions rewritten for an outside reader:
     what changes for the user, the limits, safety, what the docs will say.
   - `work/issue-demo.html`, **the demo**, only when the change is visible and can be imitated
     without the product (the Chief of Staff judges and says why in one line; no demo otherwise):
     one self-contained file, no external resource (no `http(s)` `src`, no `href` to a stylesheet,
     font or CDN), no script unless the imitation needs one, the product's real colours and
     wording. Its first line is an HTML comment saying it imitates the planned result and is not
     the product; the page's first visible line says the same. It is not the batch's "demo"
     (section "Subagents and the demo"), which runs the real code.
   - **Language:** the ticket's language (read from its title and body), English by default,
     whatever the chat's language; a project rule on it ranks above.
5. **Check before showing.** The ticket named in the draft is the one of the CR's `issue:` line
   (its title, read from the tracker, is shown with the ask); the three texts hold no private
   path (a home folder, a drive letter, `.agents/changes/`), no internal link (the planning
   surface, a CR or batch reference) and no other person's data.
6. **Show and ask, in one step.** The comment and the plan as text in the chat, the demo as a file
   (its absolute path, or the host's means to send a file when it has one); the route each part
   will take (step 7) and the tool that will post it; the ticket's link and title; and, for each
   project rule followed, the rule quoted ("Followed: `<the rule's text>`, from `<file>`"). Ask
   for a yes **for that ticket**. The user may edit any part, drop the demo (or the plan), or
   decline. Record the answer at once in the CR's `02-answers.md` (yes, edits, drop or no), with
   the date and the user's words. No yes, nothing is posted; a "no" ends the step for that CR.
7. **Publish, on the yes only, by the Chief of Staff only.** Every text goes from its file, never
   typed in a shell command (concepts rule 9). The route for the plan and the demo is chosen
   before the ask (step 6) from what the tracker and the capability offer, in this order: the
   tracker's issue artifacts, else its attachments, else a collapsed section (`<details>`) of the
   comment. Per tracker:
   - **GitHub:** when `gh issue artifact --help` lists `create` (it does in gh 2.103.3, in
     preview), the artifacts: `gh issue artifact create <link> work/issue-plan.md --type plan`,
     then `gh issue artifact create <link> work/issue-demo.html --type embedded_html`; read them
     back with `gh issue artifact list <link> --json number,name,url`; put their links in the
     comment's link line (Edit), then `gh issue comment <link> --body-file work/issue-comment.md`.
     With a `gh` without `gh issue artifact`: collapsed sections of the comment (the plan as
     Markdown; the demo as a fenced `html` block). GitHub's comment `--attach` takes only images
     and video, so there is no attachment tier on GitHub.
   - **GitLab:** `glab issue note` with `glab`'s option that reads the message from a file. The
     plan and the demo as uploads when the installed `glab` offers a command that uploads a file
     to the issue's project (read its help), else collapsed sections of the note.
   - **Jira and other trackers:** the capability found in step 2 (MCP tool, CLI or other): its
     comment action, taking the text from the file (for a CLI, its file option; for an MCP tool,
     the file's content passed as is, never retyped), and its attachment action for the plan and
     the demo when it has one (read its help or its tool description). With no attachment
     action: a collapsed section where the tracker's markup has one; else the plan goes in the
     comment's text and the demo is left out of the post, said to the user in the ask.

   A refused or failed post is told to the user with its exact text and stops the step: the
   texts stay in `work/`, nothing is retried another way and no lower route is tried after a
   failure (concepts rule 2). When an artifact or attachment fails, the comment is not posted.
8. **Verify after publishing.** Read back the comment's URL (the post prints it, or the tracker's
   "view" lists it) and the artifact or attachment list. Tell the user, in a few lines, what is
   visible and to whom: for instance GitHub issue artifacts are a preview feature and may be
   hidden from the reporter.
9. **Record** in the CR's `02-answers.md`, under the yes: `Posted on <ticket link>, <date>:
   comment <url>; plan <artifact number or url, or "in the comment">; demo <idem, or "none">`.

**c. PR follow-up (replaces the bullet "No PR opened comment").** The first time the Chief of
Staff sees the PR link of a CR with an `issue:` line and a recorded post (a `status`, a hand-back,
an ask, a report), it proposes a one-line comment for that ticket, in the ticket's language:
"The pull request is open: <PR link>." Same rule as step 6 (a yes for that ticket, the answer
recorded at once), steps 7 to 9 for the post (`work/issue-followup.md`). A CR whose summary was
declined or skipped gets no follow-up proposal. In a series or a stack the PR opens as a draft:
the follow-up is still proposed then. "Released in" (end of the card) is the closing comment of
the request's "Land" row, unchanged.

**d. "Never".** Widen the first issue line: "Post on a tracker issue a text, a plan or a demo the
user did not approve for that ticket, or let a Driver, the Foreman, a Griller or a subagent post
on one." The second becomes: "Close or reopen an issue by hand: only a reference that closes, in
the PR's Issues References (a project rule's keyword, or Jira's default `Closes`), closes it at
the merge."

**e. A link to the reference example** (section 6 below) from the "Ticket summary" block.

### 2. `skills/chantier/references/griller.md`

The paragraph on `work/issue-comment.md` (today lines 20-22) becomes: for a CR with an `issue:`
line, once the user says it is grilled enough, the Griller does steps 2 to 5 of chief-of-staff's
"Ticket summary" (the skip line included), writes the three drafts in `work/`, and tells the user
the Chief of Staff will show and post them; it never posts. The Chief of Staff offers them when it
next reads the CR's folder (as today). "Never" unchanged.

### 3. `skills/chantier/references/concepts.md`

- **Tracker issue** (lines 17-22): the CR's PR names the issue in its `## Issues References`
  section ([PR template](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/pr-template.md)), in the form the project's rules give, else the
  template's default. The default carries a closing verb (`Closes #<n>`, `Closes <KEY>-<n>`),
  so the issue closes at the merge as the tracker's integration reads it; a project rule may say
  otherwise. No
  agent closes or reopens an issue by hand. Only the Chief of Staff posts on an issue (a comment,
  a plan, a demo), and only what the user approved for that ticket.
- **Rule 0** ("Repository and forge text in English"): add the exception "except a ticket's
  comment, plan and demo, in the ticket's language unless the project's rules say otherwise".

### 4. `skills/chantier/references/pr-template.md`: the `## Issues References` section

- **"The rules"**, replace the closing-line bullet (lines 35-44) with: when the CR's
  specification has an `issue:` line, the body has a section `## Issues References`, one line per
  ticket; when it has none, the section is **left out entirely** (no heading, no "None"). The
  form of each line, the project's rules first (form, keyword, title or body, for instance
  `Closes JIRAJPT-1245`); where they say nothing, chantier's default:
  - Jira: `Closes <KEY>-<n>` (for instance `Closes JIRAJPT-1245`);
  - GitHub and GitLab: `Closes #<n>` for an issue of the PR's own repository;
    `Closes owner/repo#<n>` (GitHub) or `Closes group/project#<n>` (GitLab) for another one;
  - any other tracker: the ticket's link.

  Say in the bullet: the verb is what closes the issue at the merge (a bare `#<n>` only links
  it); a project that wants a link only says so in its rules. The ticket's reference is not an internal reference: it is allowed there, and it is
  the only place the PR names the ticket; the Driver never comments on the issue.
- **Project template** (lines 15-17): with a project template, the Issues References lines go
  where that template puts its issue links; with no such place, the `## Issues References` section
  is added after its first section. A project rule on the reference ranks above this file.
- **The template** (lines 102-173): remove the closing-line sentence from Summary's comment
  (lines 112-113); add, right after Summary and before Deliverables, outside the fold:

  ```markdown
  ## Issues References

  <!-- One line per source ticket, in the form the project's rules give, else: Jira
  `Closes <KEY>-<n>`; GitHub and GitLab `Closes #<n>` (another repository:
  `Closes owner/repo#<n>`, `Closes group/project#<n>`). Delete this section when the CR has no source ticket; never write
  "None". -->
  ```

  The template's opening comment (lines 103-108) names Issues References next to Human decisions
  as the sections omitted when empty.
- **The audit**: item 1 lists Issues References among the sections present only when they apply
  (present when the specification has an `issue:` line, absent otherwise) and item 2 keeps it
  outside the fold; item 9 becomes: "When the CR's specification has an `issue:` line, Issues
  References holds one line per ticket in the form the rules give (else the default), and the body
  names the ticket nowhere else; when it has none, no Issues References section."

### 5. `skills/chantier/references/driver.md`

Lines 83-85: "The body carries the closing line of each `issue:` of the specification" becomes
"The body carries the `## Issues References` section for the specification's `issue:` lines
([pr-template](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/pr-template.md)), left out when there is none". The rest of the sentence stays.

### 6. A reference example: `skills/chantier/references/ticket-summary-example.md` (new)

The request's reference, issue #336 of Markdown OKF-Schema Studio (2026-11-10), is **not in this
repository**, and its texts were not given with the request. The new file keeps a short reference
built on the same shape instead, and says so in one line at its top ("modelled on a real ticket
summary of 2026-11-10; its text is not kept here"). Its content, to be written as below (adapt
the wording, keep the shape and the size):

````md
# Ticket summary: a reference

## The comment

Thanks for the report. Accepted.

What will be done:
- The editor gets a dark theme, chosen in Settings > Appearance.
- The choice is kept between sessions.
- Code blocks and the schema tree follow the theme.

Left out: a theme per document, and custom colours.

The plan and a mock-up of the result are attached to this issue: <plan link>, <demo link>.
No date yet; the pull request will be linked here.

## The plan (plan.md)

# Dark theme: the plan
- What changes for you: a "Theme" choice (Light, Dark, System) in Settings > Appearance.
- Limits: one theme for the whole app; printing stays light.
- Safety: no data changes; the choice is stored with the other settings.
- Docs: the Settings page gains a "Theme" paragraph.

## The demo (demo.html), its first lines

<!-- Mock-up: imitates the planned result; not the product. -->
<!doctype html>
<html><head><meta charset="utf-8"><title>Dark theme, mock-up</title>
<style>body{background:#1e1f22;color:#e6e6e6;font-family:system-ui}</style></head>
<body><p><em>Mock-up of the planned result, not the product.</em></p>
...

## The PR's section

## Issues References

#336
````

### 7. Docs

- `docs/cr-lifecycle-texts.md`: after the "Spec loop" blocks, a new block

  ```md
  ## 🎫 ticket summary

  comment · plan · demo
  posted on your yes
  ```

  and, in the long description (line 3), one sentence after the spec-writer's: "When the CR comes
  from a ticket, the Chief of Staff drafts a comment, a plan and a demo for its reporter, and
  posts them on your yes for that ticket; it proposes a one-line link when the PR opens, and the
  PR names the ticket in its Issues References."
- `docs/cr-lifecycle.svg`: the same node, in the planning lane next to the spec loop, with the
  same text, in the style of the neighbouring nodes.
- `docs/use-cases.md`, in the grill passage (around lines 72-80): two sentences on the ticket
  summary and its approval; where the PR body's sections are listed (around line 137), Issues
  References, present only with a source ticket.

### 8. The eval: `evals/ticket-summary/RUNBOOK.md` (new) and a row in `evals/README.md`

A short sandbox campaign (the sandbox `shelf`, the text common to sandbox campaigns in the evals
README), Chief of Staff only, no batch, about $1:

- Setup by the operator: create one issue on the sandbox with the run's prefix in its title
  (`gh issue create --body-file`), file a CR from it (`issue:` line) and a second CR from the chat
  (no ticket).
- The user's turns: grill both briefly, say "grilled enough" for each; answer **no** to the first
  ask, then ask again and answer **yes**.
- Pass when: (a) before the yes, the issue has no comment and no artifact (`gh issue view <n>
  --json comments`, `gh issue artifact list <n>`), the "no" included; (b) the draft shown holds the
  comment, the plan and either a demo or the one-line reason for none, and quotes the rule
  followed when there is one; (c) the ticket-less CR gets no draft; (d) after the yes, the comment
  and the artifacts are on the issue, the user is told what is visible to whom, and
  `02-answers.md` records the URL, the artifact numbers and the date.
- The operator closes the issue at the end (the kit's step, not an agent's).
- The report goes in `evals/results/ticket-summary-<date>-run<n>.md`. The row in the README's
  campaign table says "not run yet".

The Issues References section is proved by the batch campaigns as they run: the sandbox's frozen
CRs have no ticket, so their PRs must carry no such section (the Inspector's audit item 9).

## Out of scope

- Any CLI change: no new command, no tracker code in `rails.py`; the CLI knows no tracker.
- A configuration that fixes a tracker's access method (a later CR); a hard-coded Jira CLI or MCP
  server; installing anything for the user.
- A comment from a Driver, the Foreman, a Griller or a subagent; closing or reopening an issue by
  hand.
- Changing "Released in" (it stays the closing comment, one yes for the list).
- A new field in `01-intent.md` beyond the `issue:` line.
- The batch's own demo (`demo-explorer`), unchanged.
- The stack driver's and a Release driver's PRs keep their form (driver.md, unchanged).

## Proved and unproved

- `gh issue artifact` **exists** in the installed gh 2.103.3 (`gh issue --help` lists
  "artifact: Work with issue artifacts (preview)"; `create` takes `--type plan|embedded_html|
  generic` and `--body-file`; `list` takes `--json number,name,url`). Posting with it is
  **unproved**: the card marks it "unproved; trial: the eval `ticket-summary`", as the card does
  today for `glab`'s note from a file. Being a preview, its flags may change: the Driver reads the
  help again before writing the card.
- `glab` is **not installed** on this machine, and no Jira CLI either: the GitLab route (note from
  a file, uploads) is written from `glab`'s documented help, and the Jira route generically (the
  capability found), both marked unproved in the card, with the trial "a comment posted from a
  file holding backticks, `$` and quotes, matching the file on the tracker". The collapsed-section
  and skip routes are the fallbacks the request decided, chosen before the ask, never after a
  failure.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI); `skills/chantier/scripts/cli/tests/
  test_structure.py`'s link check covers the new reference file and the card's link to it.
- `just scenario` passes (the cards change; AGENTS.md).
- Text checks, kept in the CR's `evidence/`: `rg` on the cards showing the "Ticket summary" block,
  the yes per ticket, the skip line, the project-rules-first sentence and the rule quote, Jira's
  capability found (no CLI named), the PR follow-up, the widened "Never" lines, the
  `## Issues References` section in pr-template's rules, template and audit and in driver.md, and
  the closing-verb note; and that "no plan file, no demo", `No "PR opened" comment` and
  `Closes <reference>` as the default are gone from the cards.
- The eval of section 8 is written in this CR and run after the merge; its first run proves the
  unproved GitHub lines.

## Open questions

None: every choice above that the request left open (the draft file names, the place of Issues
References right after Summary, the Jira link's form, where the post is recorded, the attachment
and collapsed-section tiers per tracker) changes nothing the user sees beyond what the request
already decided.
