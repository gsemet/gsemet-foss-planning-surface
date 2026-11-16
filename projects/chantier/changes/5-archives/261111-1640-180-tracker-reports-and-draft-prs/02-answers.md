# Answers: tracker-reports-and-draft-prs

## Decisions of 2026-11-11

Decided by a Fable advisor on the user's delegation: "Grille tout avec une session fable je ne sais pas te répondre…"

1. **The `issue:` link is kept, as the one new piece of record.** A CR that comes from a tracker
   issue carries an `issue: <link>` line from its intent to its specification and its PR body;
   the Chief of Staff or a Griller records it at filing or at the grill. A CR with no issue
   skips everything below. Reason: every other rule hangs on it, and it costs one line.
2. **The PR body carries the forge's closing keyword** (`Closes <reference>`) when the issue
   lives on the PR's own forge (GitHub, GitLab). For any other tracker (Jira…), the project's
   own rules say the form; with no such rule the body carries the plain link and closes
   nothing. Reason: generic; chantier hardcodes no tracker's syntax.
3. **The issue closes through that keyword at the merge; no agent closes or reopens an issue by
   hand.** Reason: the forge does it, and it is true only once merged.
4. **The grill comment is kept, shrunk to text:** when the grill ends, the Chief of Staff shows
   the user a short comment (what was understood, the scope in two to five bullets, what is
   left out) and posts it on the user's yes. No attached plan, no HTML demo. Reason:
   attachments depend on the tracker and nobody asked to read them there.
5. **The "PR opened" comment is dropped.** Reason: the closing keyword already makes the forge
   show the PR on the issue; a second message is noise.
6. **"Released in <link>" is kept:** once a release is published, the Chief of Staff offers the
   list of the issues it ships, and one yes covers the whole list. Reason: it is what the
   issue's reporter waits for; one approval keeps it light.
7. **Only the Chief of Staff posts on an issue, only text the user approved, and only where the
   forge's CLI it already uses reaches the tracker.** Where it does not (Jira, no access), it
   gives the user the text to post and posts nothing. A Driver, the Foreman and a Griller never
   comment on an issue. Reason: a comment is a message in the user's name; no workaround.
8. **A comment is written for the tracker's readers:** no CR number, batch, agent role or cost,
   as the PR template already asks. Reason: issues are often public.
9. **Rule 5 (draft until mergeable) is already on main and is not changed; the stacked
   "ready on its own" is dropped.** A PR is ready only when its CR is handed back `ready` and
   its base is the default branch; in a stack the new first PR already turns ready once
   retargeted and green. Reason: a ready PR based on another CR's branch can be merged into
   the wrong branch, and a draft can be reviewed just as well; "ready" keeps one meaning in
   the reports.
10. **The Foreman's asks do not carry the `issue:` link, and the CLI does not change.** The
    Chief of Staff reads the link in the CR's folder. Reason: the record already holds it; the
    CLI knows no tracker.
11. **The item is cards only:** `chief-of-staff.md`, `griller.md`, `spec-writer.md`,
    `pr-template.md`, a line in `driver.md` and in `concepts.md`. `tracker-grill-summary`, which
    it was said to replace, exists nowhere: nothing to remove. Reason: checked in
    `intake/what-main-has.md`.

## Confirmed by the Chief of Staff on the user's delegation (2026-11-11)

- In a stack, the current rule stays: a PR turns ready only once on the default branch, not as
  soon as it is green on another CR's branch (it could be merged into the wrong branch). This
  departs from issue #101's rule 5 on purpose.

## The specification's open question (2026-11-11)

Settled by the Chief of Staff on the user's delegation ("Grille tout avec une session fable je
ne sais pas te répondre…").

- **A grill run by a Griller:** the Griller writes the proposed comment in
  `work/issue-comment.md` and tells the user the Chief of Staff will offer it; the Chief of
  Staff offers it when it next reads that CR's folder. Reason: one poster, the Chief of Staff,
  and the text is never lost.
