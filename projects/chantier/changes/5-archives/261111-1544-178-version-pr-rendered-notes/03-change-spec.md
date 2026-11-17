# Change Specification: the version PR shows the rendered release notes and thread

## Goal

The owner reviews a release where they approve it: in the version PR (the PR a release procedure
opens for the version, which the cards call the release PR). Its body shows, under the PR's own
description, the release notes and then the announcement thread, rendered as Markdown, images
included once they are on the forge, so the review works on a phone too. The rule is generic: it
is the default for any project, under that project's own release procedure, and names no forge,
file layout or size of its own.

The same CR fixes one wording defect of `driver.md` (point 2 of `cr-171-retro-fixes`): a Driver
reads its `team:` lines with `handoff`, never by spending a `round`.

## Decisions carried (from `02-answers.md` and `intake/cr-171-retro-fixes-answers.md`)

| # | Decision | Where it lands |
| --- | --- | --- |
| A1 | When a release has a version PR, its body shows the notes, then the thread, as rendered Markdown, each after a `---` rule, under the PR's own description | `driver.md` Release driver; `release-template.md` Where they go |
| A2 | Default only: a project that says where its notes are reviewed is followed as written; a release with no PR (a tag only) keeps today's drafts and nothing more | same |
| A3 | The draft files stay the source, the body is a copy: `note --draft` and `status`'s `draft <path>` unchanged; the Driver refreshes the body from the files each time they change and before it asks for the merge; it never rewrites a draft from the body; a change the user wants goes to the Chief of Staff or into the file | same |
| A4 | The thread's section is headed as a draft the user posts themselves | same |
| A5 | Images show in the body only once on the forge; an upload keeps its `release go`; anonymised first; until then, and where the forge cannot upload, the body names the image in prose | same |
| A6 | What the forge's body size limit leaves out is named by its path in the body, never cut silently | same |
| A7 | Cards only: `driver.md` Release driver, `release-template.md` Where they go, and for chantier `docs/release-process.md`; no CLI change, no agent-file change | scope |
| A8 / R1 | `driver.md` says a Driver reads its `team:` lines with `handoff` (or keeps those `take` printed); `round` is run only to start a round, just before a Coder | `driver.md` Your means |
| R2 | No CLI change for that point: no new refusal, no "dry" `round` | scope |

Point 3 of `cr-171-retro-fixes` (the `cost` labels) is not in this CR: it goes with
`cost-unknown-model` and `report-template` (its answer 6). Point 1 went to
`worker-write-guard-redesign`.

## What changes

### 1. `skills/chantier/references/driver.md`, "Your means" (the `team:` lines)

Today, line 18-24: "the worker's agent and model as the `team:` lines of `round` print them". A
CR-171 Driver ran `round` only to read those lines and lost one of its rounds.

New wording, same bullet, in substance:

- The `team:` lines are read with `$CHANTIER handoff <cr>`, which prints them and counts nothing,
  or kept from the ones `take` printed in the prompt.
- `$CHANTIER round <cr> --note "<brief>"` is run only to start a round, just before that round's
  Coder; never to read facts.
- The rest of the bullet (exit 5 is `blocked rounds:`, the agent and model passed as printed, a
  refused start is `blocked refused`, a `Needs:` you cannot meet) is unchanged.

`concepts.md` line 188 and 195 already list `take`, `round` and `handoff` as printing the `team:`
lines; they stay as they are (they say where the lines appear, not which command to run for them).

### 2. `skills/chantier/references/driver.md`, "Release driver"

Add one bullet after the drafts bullet (today's "What a person reviews or edits ... `note --draft
<path>`") and before the release PR bullet. In substance:

- When the procedure opens a version PR, its body carries, under the PR's own description, a `---`
  rule, the release notes, a `---` rule, then the announcement thread under a heading that says it
  is a draft the user posts themselves (no agent posts it). Both are the draft files' text, rendered
  by the forge as Markdown. This is the default: a project whose procedure says where its notes are
  reviewed is followed as written; a release with no PR keeps the drafts alone.
- The files are the source and the body a copy. The Driver writes the body from the files with the
  forge's own CLI (`gh pr edit --body-file`, `glab mr update --description`, or the equivalent for
  another forge), when it opens the PR, each time a draft changes, and once more just before
  `handback blocked merge: <pr link>`. It never copies the body back into a file. A change the user
  asks for in the PR is made in the file (by the user, or on the Chief of Staff's word), then the
  body is refreshed.
- Images: one already on the forge (an asset uploaded under its `release go`, or a file the
  procedure committed and pushed with the version PR's branch) is shown from there; one not yet on
  the forge, or that the forge cannot take, is named in prose (`<file name>: <what it shows>`).
  Every image is anonymised before it leaves the machine, as `release-template.md` says. The body
  never links a local path.
- When the whole does not fit the forge's body limit (the forge's own, read from its error or its
  docs, never a figure in the card), the body keeps what fits in that order (description, notes,
  thread) and names each part left out by its path in the PR's branch or the work folder, with a
  line saying the body is not the whole text. Nothing is cut silently.

The release PR bullet ("A release PR is the Foreman's to merge ... `handback blocked merge: <pr
link>`") gains: "the body refreshed from the drafts first, as above".

The PR's own description stays the procedure's (its form is kept "by the project's rules", line
47); the rendered notes and thread are appended under it, never in its place.

### 3. `skills/chantier/references/release-template.md`, "Where they go"

Add, after the first sentence, in substance: when the release has a version PR, the Driver also
shows `release-notes.md` and then `tweet.md` in the PR's body, rendered, each after a `---` rule,
the thread headed as a draft the user posts; the files stay the source and the body is refreshed
from them, as [driver](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/driver.md) says. An image shows in the body once it is on the forge (its
upload is an irreversible action, `release go`), else it is named in prose. What the forge's size
limit leaves out is named by its path. A release with no PR keeps the drafts only.

The "Visible evidence" rule on images (`<img src="...">` or prose, never a Markdown image link to
a file that may not exist) applies to the body as well.

### 4. `docs/release-process.md` (chantier's own procedure, ranks above the template)

In the intro, "This file says what the user reviews in the version PR" gains one sentence: the
version PR's body shows `release-notes.md`, then `tweet.md`, after `---` rules, under the PR's
description; the release folder stays the source, and the body is refreshed from it before the
merge. In "Images", one sentence: in the PR's body, the images committed in the release folder are
linked at the version PR's head commit on GitHub (they are already pushed with the branch,
anonymised and read first), since a bare file name does not render there; on publication
`--prepare` still points the published notes to the release assets.

`CONTRIBUTING.md` "Release" step 3 ("The user reviews the release folder in it") may say "in the
PR's body and its files": a one-phrase change, allowed but not required.

## Out of scope

- Any CLI change: no new command, flag, refusal or `status` line; `note --draft` and `draft
  <path>` stay as they are; no "dry" `round`.
- The agent files on both hosts (`agents/release-driver.md`, `agents/cr-driver.md`,
  `com.github.copilot/agents/*`): unchanged.
- Posting the thread, or any agent posting anything.
- Syncing an edit made in the PR body back to the files.
- The `cost` labels (point 3 of `cr-171-retro-fixes`) and the hook tests (point 1).
- `scripts/release_notes.py`: no change (it checks the folder, not the PR).

## Evidence

- `just check` passes on Linux, macOS and Windows (CI).
- `just scenario` passes (the cards changed); no scenario step is added, as the CLI does not
  change.
- The diff touches only `skills/chantier/references/driver.md`,
  `skills/chantier/references/release-template.md`, `docs/release-process.md` (and optionally
  `CONTRIBUTING.md`); `git diff --stat` shows no file under `agents/`, `com.github.copilot/`,
  `skills/chantier/scripts/` or `scenario/`.
- Text checks, quoted in the PR:
  - `driver.md` no longer contains "`team:` lines of `round`"; it names `handoff` for reading
    them and says `round` is only to start a round.
  - `driver.md` "Release driver" and `release-template.md` "Where they go" both say: body after
    the description, notes then thread, `---` rules, thread headed as a draft the user posts,
    files are the source, refreshed before the merge, images only once on the forge (else in
    prose), size overflow named by path, the project's procedure first, no PR means drafts only.
  - No forge size figure, file name of chantier, or forge-only command appears in the generic
    cards as the only way (the forge's own CLI, `gh`/`glab` as examples).
- The Verifier reads the three cards against this specification, decision by decision (A1 to A8,
  R1, R2), and records each as met or not.

## Open questions

None. The one raised is settled in `02-answers.md`: an image already committed and pushed with
the version PR's branch is on the forge, and the body links it at the PR's head with no new
`release go`; only a new upload needs one.
