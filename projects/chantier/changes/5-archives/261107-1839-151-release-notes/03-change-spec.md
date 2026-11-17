# Change Specification: visual release notes and an announcement thread for each release

## Goal

A release of chantier ships release notes with as much visual evidence as possible, usage and
call examples, and links to the relevant docs, plus an announcement thread of three posts (the
first may be long) with one image. The model is Markdown OKF-Schema Studio ("c'est topissime"):
its `.agents/guidelines/release-process.guidelines.md`, its `docs/releases-notes/` folders and its
`scripts/release_notes.py`. There are two deliverables:

1. **chantier's own release guideline**: the notes, the thread and their images are committed in
   `docs/release-notes/YYYY-MM-DD-vX.Y.Z/` with the version, reviewed by the user in the version
   PR, checked by `just check` (invalid notes fail it), and published as written with
   `gh release create --notes-file` (no more `--generate-notes`), with the images attached to the
   release.
2. **A generic default shipped in the skill**, like `pr-template.md`: visual release notes and a
   three-post thread. The release Driver applies it when the project has no procedure of its own
   for them. The project's own procedure ranks above it.

Release 0.8.0 is the first to use the new procedure. This CR makes no release itself.

## Decisions carried over (from `02-answers.md`)

1. Every release ships release notes with as much visual evidence as possible, usage and call
   examples, and links to the relevant docs. It also ships an announcement thread of three posts
   (the first may be long) with one image. The model is Studio.
2. There are two deliverables: a guideline for chantier's own releases, and a generic model for
   the users' projects (the release Driver's). The generic model also puts screenshots and visible
   evidence of what ships into the notes, to explain it.
3. chantier's visuals are captures of the board and of the reports (from a real batch or the
   scenario), excerpts of a conversation with the Chief of Staff, and CLI output. The docs SVG
   diagrams are not used by default. Everything shown is carefully anonymised: no personal path,
   user name, email, private repository or session id.
4. The mechanics are Studio's: notes, thread and images in `docs/release-notes/YYYY-MM-DD-vX.Y.Z/`,
   reviewed by the user in the version PR, checked by `just check` (invalid notes fail it), and
   published as they are with `gh release create --notes-file` (not `--generate-notes`), with the
   images attached to the release.
5. Post 3 is one sentence (install or update, free, the licence) plus the link to the README's
   Install section.
6. The generic model is a default shipped in the skill, like `pr-template.md`: visual release
   notes and a three-post thread. The release Driver applies it when the project has no release
   procedure of its own, and the project's own procedure ranks above it.
7. chantier's captures come from the release's real batch, anonymised. The release Driver renders
   the batch's `STATUS.md` and report to PNG (headless Chrome), with paths, names and ids
   replaced.
8. Priority is P1, next to docs-lifecycle. Release 0.8.0 is the first to use the new procedure.
9. When the user confirms the release (`order confirm`), the Chief of Staff writes its latest
   Progress report and the conversation excerpts it chooses into the release CR's folder, as
   `report.md` and `conversation.md`. The release Driver renders them from there, anonymised.
10. For chantier, the release CR joins the batch whose work it ships (`order add --release`), so
    the board and `STATUS.md` show that work.
11. A docs SVG diagram is shown in the notes only on the user's word in the release CR's grill.

## What changes

### 1. New guideline: `docs/release-process.md` (chantier's own)

This adapts Studio's guideline to chantier, in the style of the repository's docs (short
sentences, exact terms). `CONTRIBUTING.md` "## Release" links it, so `$CHANTIER rules` reaches it
two levels deep: `AGENTS.md` → `CONTRIBUTING.md` → this file. It has these parts.

**a. Purpose.** The mechanics (version, tag, publication) are in `CONTRIBUTING.md` "## Release".
This file says what the user reviews in the version PR: the notes, the thread and their images, in
`docs/release-notes/YYYY-MM-DD-vX.Y.Z/`. The folder is named by the date of the version PR. That
date may differ from the tag's, and nothing checks it.

**b. The release folder**, as a table:

| File | Content |
| --- | --- |
| `release-notes.md` | The GitHub release notes, with images linked by bare file name |
| `tweet.md` | The announcement thread: three posts |
| Images (`*.png`) | The images of the notes and of the thread, directly in the folder |

**c. Release notes.** They are written for a user of chantier from the commits since the previous
tag (`git log --no-merges vPREVIOUS..HEAD`; chantier has no `CHANGELOG.md`) and from the
specifications, PR descriptions and evidence of the CRs they come from. They contain no CR number
or slug, no batch number and no path under `.agents/changes/`. chantier's role names (Chief of
Staff, Foreman, Driver) are product vocabulary and may be used. The structure, in order:

1. **Header**, centred:
   - `<h1 align="center">chantier X.Y</h1>`;
   - one bold line naming the two or three headline changes, as verbs;
   - one `<sub>` line: `N changes since X.Y'.Z' · Claude Code and GitHub Copilot · MIT`, where N
     is `git rev-list --no-merges --count vPREVIOUS..HEAD` on `main` before the version commit.
2. **Links**, centred, on one line: Install (`https://github.com/gsemet/chantier#install`) · the
   tutorial (`blob/vX.Y.Z/docs/tutorial-claude-code.md`) · the use cases
   (`blob/vX.Y.Z/docs/use-cases.md`) · Full changes (`compare/vPREVIOUS...vX.Y.Z`). Then a `---`
   rule.
3. **Two to four highlight sections**, `## <emoji> <what the reader can now do>`. Each has:
   - a short paragraph saying what changes for the reader;
   - a usage or call example: what the user says to the Chief of Staff (a quoted line), or a CLI
     call with its output in a code block;
   - one capture, or a before/after pair in a two-column table with a caption row;
   - a link to the doc that covers it, at the tag (`blob/vX.Y.Z/...`);
   - one closing sentence on why it matters.
4. **`## 🛠 Smaller changes`**: the smaller visible changes, one bullet each, with a bold lead.
5. **Folded sections**: `<details><summary><b>🐞 All fixes</b></summary>`, then
   `<details><summary><b>🛠 For contributors</b></summary>` (tooling, tests, docs process, known
   issues).

Every `feat:` and `fix:` commit since the previous tag appears exactly once: in a highlight, in
Smaller changes or in All fixes.

**d. Visuals.** All of them come from the release's real batch: the release CR joins the batch
whose work it ships (`order add --release`), so that batch's board and `STATUS.md` show the work.
The sources are:
- the board and the batch's `STATUS.md` (`.agents/changes/3-requests/batch-<n>/STATUS.md`);
- the Chief of Staff's latest Progress report, `report.md` in the release CR's folder;
- excerpts of a conversation with the Chief of Staff, `conversation.md` in the release CR's
  folder (the Chief of Staff writes both at `order confirm`, see section 6);
- CLI output (`$CHANTIER status`, `cost`, …).

The docs SVG diagrams are not used by default: one is shown only on the user's word in the release
CR's grill (the release CR's specification then names it). Rendering works like this:
- the release Driver writes each source as an HTML page in its work folder;
- it applies the anonymisation (part f) to that page;
- it renders the page to PNG with headless Chrome, for example
  `chrome --headless=new --screenshot=<file>.png --window-size=1200,<h> file:///<page>.html`, at a
  width readable in a post;
- it saves the PNG into the release folder.

The HTML sources stay in the work folder and are not committed. If headless Chrome is missing,
nothing else is used in its place: the Driver hands back a `blocked question:` naming what is
missing.

**e. Images.** Images sit directly in the release folder, and the notes and `tweet.md` link them
by bare file name. An image at a URL or in a subfolder fails the check, because a release must
depend on no branch. On publication, `--prepare` points the links to
`https://github.com/gsemet/chantier/releases/download/vX.Y.Z/<file>` and the images are attached
as release assets.

**f. Anonymisation.** No personal path, user name, email, private repository or session id
appears in any text or image. The Driver applies these replacements to every source before
rendering it:

| What | Replaced by |
| --- | --- |
| Home folder (`C:\Users\<name>`, `/Users/<name>`, `/home/<name>`) | `~` |
| Local login name, git user name | `user` |
| Email | `user@example.com` |
| Session id, transcript id (UUID) | `<session>` |
| Repository other than `gsemet/chantier` | `example/app`, unless the user said it is public |

How it is checked:
1. Before rendering, the Driver runs `uv run --script scripts/release_notes.py --scan <page>…` on
   each HTML source (section 3). It must exit 0.
2. The Driver reads each PNG it produced before committing it.
3. `just check` scans `release-notes.md` and `tweet.md` (section 3).
4. The user reviews every image in the version PR.

The scan cannot read pixels, so steps 2 and 4 cover the images, and step 1 covers their sources.

**g. Announcement thread.** `tweet.md` starts with `# Announcement thread for X.Y.Z`, followed by
three posts under `## 1/`, `## 2/` and `## 3/`:
1. **The story** (it may be long). First person, as one would tell a colleague: start from a
   concrete moment of work with chantier that the release improves, then say what is different
   now. At most three changes, in plain words, not a feature list. This post carries the thread's
   only image: an `Image: <file>` line naming one of the notes' captures.
2. **The release notes**: one sentence inviting the reader to the details, then
   `https://github.com/gsemet/chantier/releases/tag/vX.Y.Z`.
3. **Install**: one sentence (install or update, free, MIT), then
   `https://github.com/gsemet/chantier#install`.

Tone: organic. No launch words ("excited to announce", "game changer", "supercharge"), at most two
emoji in the whole thread, and no list of hashtags. Only the user posts: no agent posts the thread.

**h. Which batch.** A chantier release joins the batch whose work it ships (`order add --release
--note <folder>`), rather than running alone with `--release 1`: that batch's board and
`STATUS.md` then show the work the captures explain. At `order confirm` the Chief of Staff writes
`report.md` (its latest Progress report) and `conversation.md` (the excerpts it chooses) into the
release CR's folder. A docs SVG diagram goes into the notes only on the user's word in the release
CR's grill.

### 2. `CONTRIBUTING.md`, section "## Release"

Rewrite the steps as follows (the commands are kept exact):

1. From an up-to-date `main` with green CI, agree on the version. Then, on a new branch, write the
   release folder `docs/release-notes/<today>-vX.Y.Z/` as `docs/release-process.md` says.
2. `just release minor` (or `patch`, `major`). It bumps the version and runs `just check`, which
   now refuses missing or invalid notes. It then stages `docs/release-notes/` and commits
   `release: vX.Y.Z`. It pushes nothing.
3. Push the branch and open the PR. The user reviews the release folder in it. Merge by rebase once
   CI is green.
4. `just tag`.
5. Publish the reviewed notes as they are, with the images attached:

   ```bash
   uv run --script scripts/release_notes.py --prepare vX.Y.Z --output <tmp>/release-notes.md --assets <tmp>/assets
   gh release create vX.Y.Z --notes-file <tmp>/release-notes.md <each file that --prepare listed>
   ```

   A typo found after publication is fixed by editing the release on GitHub. The published text
   may then differ from the file, and that is accepted.
6. The user posts the thread from `tweet.md`.

Remove `gh release create vX.Y.Z --generate-notes`. Add a link to `docs/release-process.md`. In
"How the project is built" (point 1, the list of references), name `release-template.md`: the
default release notes and thread the release Driver writes when the project has none of its own.

### 3. New script: `scripts/release_notes.py`, and the `justfile`

The script is a port of Studio's `scripts/release_notes.py`, in the style of `scripts/version.py`:
- a `uv run --script` header with `dependencies = []`, standard library only;
- `encoding="utf-8"` everywhere and `newline="\n"` on write;
- portable on Linux, macOS and Windows.

It belongs to the repository, not to the chantier CLI: `skills/chantier/scripts/cli/` does not
change. It has three modes, exactly one per run.

- **`--check`**:
  1. Read the current version from the CLI's `__version__`
     (`skills/chantier/scripts/cli/src/chantier/__init__.py`, the same line `scripts/version.py`
     reads). Below 0.8.0, print `release-notes: none needed before 0.8.0` and exit 0.
  2. From 0.8.0 on, require exactly one `docs/release-notes/YYYY-MM-DD-vX.Y.Z/release-notes.md`.
     Otherwise fail with `Expected one docs/release-notes/YYYY-MM-DD-vX.Y.Z/release-notes.md, found
     <n>`.
  3. In `release-notes.md`:
     - the first line starts with `# ` or `<h1` and names `X.Y`;
     - every image (`![..](src)` or `<img src="...">`, Studio's `IMAGE` regex) is a bare file name
       that exists in the folder.
  4. In `tweet.md`:
     - it exists, with `## 1/`, `## 2/` and `## 3/` in order and nothing else at that level;
     - there is exactly one `Image:` line, in post 1, naming a file in the folder;
     - post 2 contains `https://github.com/gsemet/chantier/releases/tag/vX.Y.Z`;
     - post 3 contains `https://github.com/gsemet/chantier#install`.
  5. Scan both text files with the scan's fixed patterns (below).

  On success, print `release-notes: <path> ok`. On failure, print `release-notes: <reason>` to
  stderr and exit 1.
- **`--prepare TAG [--output FILE] [--assets DIR]`**:
  - accepts a stable `vX.Y.Z` tag only;
  - validates the notes as `--check` does;
  - copies each image of the notes and of `tweet.md` into `DIR`;
  - writes the notes to `FILE`, with each image source rewritten to
    `https://github.com/gsemet/chantier/releases/download/<TAG>/<file>`;
  - prints the path of each asset, one per line, so the `gh release create` call names them on
    any shell.

  The defaults are `release-notes.md` and `release-assets`, as in Studio. The caller passes paths
  outside the repository.
- **`--scan FILE...`**: prints `<file>:<line>: <kind>` for each match and exits 1 when there is
  any. It uses two kinds of pattern:
  - **Fixed patterns**, the same on every machine: a home path (`[A-Za-z]:[\\/]Users[\\/]`,
    `/Users/<x>`, `/home/<x>`), an email address, and a UUID.
  - **Local values**, added in `--scan` only and when they are set: the home folder's name, and
    the output of `git config user.name` and `git config user.email`. `--check` leaves these out,
    because CI has other values.

`justfile`:
- add a recipe `release-notes` (`uv run --script scripts/release_notes.py --check`) with a comment
  line;
- make `check` depend on it (`check: test release-notes`);
- in `release`, add `git add docs/release-notes` before the `git commit -am "release: v…"` line,
  so the new folder goes into the version commit.

No structure test is added. `just check` runs the check itself, and the ad-hoc runs below prove
its refusals.

### 4. New reference: `skills/chantier/references/release-template.md` (the generic default)

This reference is written for agents in the cards' style. The release Driver reads it when the
project's procedure is silent on release notes or on an announcement. `release-template.md` has no
role section, as `pr-template.md` has none. Relative links in it must resolve, because
`test_skill_and_references_links_resolve` checks every `](…)` in `references/*.md`, inside code
blocks too. Its skeleton therefore names images in `<img src="…">` form or in prose, never as
`![..](file)`. Its parts:

**a. Scope and precedence.** It is the default form of a release's notes and announcement thread,
written by the release Driver. The project's own release procedure, and what `$CHANTIER rules`
reaches, rank above it. Where the project says how its notes or its announcement are written, the
Driver follows the project as written, and this file only fills where the project is silent. The
mechanics (version, tag, publication, gates) are always the project's own, and this file adds none.

**b. The notes.** The same structure as section 1c, made generic:
- header: product name, version, one bold line of verbs, and a `<sub>` line with N changes since
  the previous version, what it runs on, and the licence;
- a line of links: install, docs, full changes;
- two to four highlights, each with what changes, a usage or call example, the visible evidence,
  a link to the doc, and why it matters;
- smaller changes;
- folded fixes and contributor notes.

They are written for the project's users, with no CR, batch or agent-role reference, as in
[pr-template](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/pr-template.md).

**c. Visible evidence.** Each highlight shows what ships. The sources are:
- the Verifier's before/after in the archived CRs' `evidence/` folders;
- the screenshots in the merged PRs' Impacts sections;
- captures of the product running, made by the Driver;
- CLI output.

When the release CR's folder holds `report.md` or `conversation.md` (section 6), they are
sources too. They are anonymised as in section 1f, with the same replacements and the Driver's own
reading of each image. With nothing visible to show, the highlight says so in one line: no
invented image. A diagram of the project's docs is shown only on the user's word in the release
CR's grill.

**d. The thread.** Three posts:
1. the story, which may be long, with the thread's one image;
2. the link to the release notes;
3. one sentence (install or update, the price, the licence) and the install link.

The tone is that of section 1g. No agent posts: the thread is a draft for the user.

**e. Where they go.** By default the Driver writes `release-notes.md`, `tweet.md` and the images in
`<work folder>/release/` and runs `note --draft` on each text, as [driver](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/driver.md) says. Where
the procedure publishes notes (a forge release, a changelog entry), the Driver uses the reviewed
text there. The images are attached with the forge's own CLI, and that is an irreversible action
(`release go`). Where the procedure publishes no notes, they stay a draft for the user.

### 5. `skills/chantier/references/driver.md`, section "Release driver"

- In the bullet "What a person reviews or edits (release notes, an announcement) goes early in the
  work folder, then `note --draft <path>`", say: "goes early in the work folder, or where the
  project's procedure keeps it (a folder committed with the version), then `note --draft <path>`".
- Add one bullet: the release notes and the announcement thread follow the project's procedure,
  else [release-template](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/release-template.md). Their captures come from the release's batch (its
  `STATUS.md`, the board, CLI output) and from `report.md` and `conversation.md` in the release CR's
  folder when the Chief of Staff wrote them; a docs diagram only when the release CR's
  specification names it. Their images are anonymised before they leave the machine, and the
  thread is never posted by an agent.

### 6. `skills/chantier/references/chief-of-staff.md`, section "Releases"

- After "nothing written, or a gap, is a question for the user", add one sentence: a procedure
  silent on release notes or on an announcement is no gap, because the release Driver then follows
  [release-template](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/release-template.md). Offer the user to write the project's own version in
  the project.
- At the confirmation ("When the Foreman asks for the confirmation, grill the version …"): before
  `$CHANTIER order confirm`, write your latest Progress report and the conversation excerpts you
  choose into the release CR's folder, as `report.md` and `conversation.md`; the release Driver
  renders them from there, anonymised. In the same grill, ask whether a docs diagram should be
  shown in the notes; only the user's yes puts one in, named in the release CR's specification.
- "Prepare it as any CR … open it preferably alone with `--release 1`" stays the default for any
  project. chantier's own choice, to join the batch whose work the release ships (`order add
  --release`), is written in `docs/release-process.md` (section 1, part h), which ranks above the
  card as a project rule.

### 7. Docs

- `README.md`, "Repository layout": add `release-template` to the list of references, and change
  `docs/` to "diagrams, tutorial, release notes".
- `docs/release-notes/` is created by release 0.8.0, not by this CR.

### Unchanged

- The chantier CLI (`skills/chantier/scripts/cli/`, `rails.py` included): no new command. The
  check is the repository's.
- The agent files in `agents/` and `com.github.copilot/agents/`: a role's contract stays in its
  card.
- `.github/workflows/ci.yml`: `just check` already runs on the three systems and now includes the
  notes check.
- `scenario/`: no release is published there. It still runs, because cards change.

## Out of scope

- Making a release: 0.8.0 is the first to use the procedure, as its own release CR.
- Notes for 0.7.0 or earlier versions (the check starts at 0.8.0).
- Studio-only parts: the Marketplace, VS Code requirements, the visual test fixtures and the
  hero-image scenario pipeline (`test/visual/…`, `generate-readme-images.py`), CI publication on
  the version push, requirement ids, the heavy-run monitoring steps. Post 1's image is one of the
  notes' captures.
- The docs SVG diagrams as default visuals.
- Posting the thread anywhere.
- A structure test of `release_notes.py`, or an OCR of the images.

## Evidence

All of this runs in the CR's worktree:

1. `just check` passes. At version 0.7.0 it prints `release-notes: none needed before 0.8.0`.
2. A dry run in a throwaway worktree, not pushed and then removed. Paste the output into the PR's
   Test plan:
   1. `just version 0.8.0` with no notes folder: `just check` fails with `Expected one
      docs/release-notes/YYYY-MM-DD-v0.8.0/release-notes.md, found 0`.
   2. Add a sample folder (a title naming 0.8, one PNG linked by name, a valid `tweet.md`):
      `just check` passes.
   3. Each of these fails `--check`, one at a time:
      - an image in a subfolder, or at an `https://` URL;
      - a missing `## 3/`;
      - two `Image:` lines;
      - post 3 without the install link;
      - `C:/Users/someone/` in `tweet.md`;
      - an email or a UUID in `release-notes.md`.
   4. `--prepare v0.8.0 --output <tmp>/n.md --assets <tmp>/a`: `n.md` links
      `https://github.com/gsemet/chantier/releases/download/v0.8.0/<file>`, the PNG is in
      `<tmp>/a`, and its path is printed.
   5. `--scan` on a file holding the local git user name, a home path and a UUID lists the three
      and exits 1. On a clean file it exits 0.
3. `just scenario` passes on both forges, because cards change.
4. `rg -n "generate-notes" CONTRIBUTING.md` finds nothing, and `rg -n "notes-file|release-process"
   CONTRIBUTING.md` finds the new steps.
5. `rg -n "release-template" skills/chantier` shows the links in `driver.md` and
   `chief-of-staff.md`.
6. `git diff --stat origin/main` lists no file under `skills/chantier/scripts/cli/`, `agents/`,
   `com.github.copilot/agents/`, `.github/` or `scenario/`.
7. CI is green on Linux, macOS and Windows (the script is portable).

## Open questions

None. The three questions of the first draft are answered in `02-answers.md` and folded in
(decisions 9 to 11).
