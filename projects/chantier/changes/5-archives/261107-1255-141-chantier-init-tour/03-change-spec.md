# Change Specification: `/chantier:chantier init`, a guided tour for a newcomer

## Goal

A person who has never heard of chantier types `/chantier:chantier init` (or "chantier,
initialise this project") in their repository. chantier creates the five empty stage folders,
then gives a didactic tour of how this project will work with chantier from now on, told as the
story of one real change of this project, and ends with what the person can say and what the
project should improve for chantier to work well. The tour writes nothing in the project.

The approved reference is `reference-tour.md` in this folder: the tour run on the chantier
repository itself, which the user called perfect. Match its tone, structure, depth and length.

## What changes

### 1. The CLI: `chantier init`

- A new command `init` that creates, under the repository root, the five stage folders of
  `.agents/changes/` (`1-inbox`, `2-backlog`, `3-requests`, `4-archives`, `5-trash`), empty, with
  no `.gitkeep`. It uses the existing layout (`lifecycle.stage_layout`) and root discovery
  (`Repo.find`).
- Idempotent: folders that exist are left as they are; it prints which folders it created and
  which already existed, ten lines at most.
- Outside a git repository it exits 2 with a message saying no git repository was found and
  that chantier needs one. In a linked worktree it exits 2, by the same test as preflight's P7,
  saying init runs in the main checkout.
- It writes nothing else: no `.gitignore`, no `AGENTS.md`, no state file. It runs no git
  command that changes anything.
- The repository's rules in `AGENTS.md` (chantier writes only in `.agents/changes/`; a CLI tool
  comes from measured token cost) are not changed by this CR: the user chose to add this command
  now and to revisit the rules later.

### 2. The card: `skills/chantier/references/init.md`

A new reference card the Chief of Staff reads when the user asks for init. It says:

1. **Run `$CHANTIER init`.** On exit 2 for no git repository: explain what chantier needs (a git
   repository, a remote on GitHub or GitLab, `gh` or `glab` logged in, `uv`), offer `git init`,
   run it only on the user's yes, then run `init` again. Nothing else is created on the user's
   behalf.
2. **Read the project, lightly:** `$CHANTIER rules` (the instruction file and what it links),
   the README, the build files (`package.json`, `justfile`, `Makefile`, `pyproject.toml` and the
   like), the CI workflows, the tree on two levels. No code reading, no gate run.
3. **Ask once: in the chat or as an HTML page?** The chat is the default. On Remote Control, the
   HTML page is sent as a file.
4. **Give the tour, in the user's language,** in this order and with these rules:
   - The thread is the story of one CR of this project, from the request to the archive: filed
     in `1-inbox`, grilled with a question and its recommended answer, specified, prioritized
     into `2-backlog/P<n>`, run in a batch by the Foreman, taken by a Driver in a slot on its
     branch and worktree, rounds of Coder then Inspector, long gate, PR, CI, Verifier, ready,
     the user's merge, `4-archives`. The example CR is a real, small improvement the Chief of
     Staff picks from what it read; its paths, branch name and gate commands are this project's.
   - The batch's steering, as chantier works (this CR lands after `direct-mode`): a batch is
     steered either by the **Foreman**, a separate session, or by the Chief of Staff itself in
     **direct mode** (no Foreman session; the Chief of Staff starts the Drivers and holds no
     grill or discussion until the batch completes; no CR joins the batch while it runs). Say
     when each is used: direct mode where the host cannot start a Foreman session or for a
     small batch, the plan names it and the user's go approves it. The story follows the
     Foreman; one or two sentences after step 4 give direct mode, and the first diagram notes
     it. Present it as how chantier works, never as something new.
   - Each concept appears when it serves, in bold. A role is first an image of the building site
     (chief of staff, foreman, team lead, workers), then its exact term.
   - About ten core terms in the story: CR, specification, batch, Chief of Staff, Foreman,
     Driver, slot, round, Coder, Inspector, Verifier, ready. The others go to the glossary.
   - Three diagrams, generated for this project: who talks to whom (the user, the Chief of
     Staff, the Foreman, a Driver per CR, its workers; orders down, questions and hand-backs
     up); the five folders and what moves a CR between them; one CR over time (rounds, gate,
     PR, CI, Verifier, the user's merge). In the chat they are text diagrams.
   - Two previews of what the user will read: the CR's folder tree with this project's real
     paths, and a `status` table. Money in it is shown as `$…`: the tour gives no cost figure.
   - Money and decisions: the budget, slots (4 by default) and rounds (3 by default) explained
     as mechanics, with no figure; what only the user does (prioritize, say go, merge, release,
     raise a limit); "what did it cost?" gives the measured detail.
   - No comprehension check and no quiz.
5. **End the tour with**, in this order:
   - **Getting started here:** what the Chief of Staff saw of the project's harness and what it
     proposes to improve, each with its impact on the team when missing. A rule (a gate, the
     merge method, the commit convention) is proposed as the exact `AGENTS.md` text, written only
     on the user's yes, section by section. Work that needs code (tests, CI) is proposed as a CR
     filed in the inbox, only on the user's yes. The `.gitignore` line is explained only (keep
     `.agents/changes/` out of git so the main checkout stays clean and the CRs stay local; the
     user adds `.agents/changes/` themself). The example CR is offered for the inbox.
   - **Phrases to say:** "file this: …", "make it a P1", "run the P1s", "status?", "drop
     CR-<n>", "I merged #<n>", "what did it cost?".
   - **Glossary:** one line per term not in the story (stack, fast gate, long gate,
     Investigator, Debugger, Conflict resolver, release CR, grant, `STATUS.md`, `close`, direct
     mode if the story's sentences need a reminder, and any
     other the user will read in reports).
6. **Length:** about the reference's, under 100 lines in the chat, glossary included.
7. **Re-run** on a project that already has the folders: the command changes nothing, the
   improvements are assessed again and what changed is said, and the tour is offered, not
   imposed.

### 3. The HTML template: `skills/chantier/assets/tour.html`

- A fixed, self-contained HTML page (inline CSS, no network, readable on a phone, light and dark):
  title, table of contents, and named slots the Chief of Staff fills: the story, the three
  diagrams (inline SVG it generates), the two previews, money and decisions, getting started
  here, phrases to say, glossary.
- The Chief of Staff copies it to `<system temp>/chantier-tour-<project folder name>/index.html`,
  fills the slots and opens it (or sends it as a file). Nothing is written in the project.

### 4. The entry points

- `skills/chantier/SKILL.md`: a row in the Entry points table, "init, a guided tour, 'I am new
  here'" → `$CHANTIER init`, then the tour → [init](references/init.md).
- The first-turn introduction stays as it is, except: when the project has no `.agents/changes/`,
  it ends with one line offering init ("new here? say init for a guided tour"). When the user's
  first request is init, the introduction is skipped: the tour covers it.

## Out of scope

- Any other CLI change, a `.gitignore` written by chantier, a change to the repository's rules,
  a dedicated `/chantier:init` command, running gates during init.
- Rewriting the tutorial or the README around init (a mention may be added where they list the
  commands, to stay true).

## Done when

- `chantier init` creates the five folders in a fresh repository, prints them, changes nothing
  on a second run, and exits 2 with a clear message outside git.
- The card, the template and the Entry points row exist; the Claude Code and Copilot hosts read
  the same card (no agent file changes).
- `just check` passes, and `just scenario` passes as `AGENTS.md` requires for a CLI and card
  change.
- A Verifier runs init on a scratch repository (a small project with a README and a build file)
  and shows the chat tour follows section 2: the story of a real CR of that project with its real
  paths, the three diagrams, the two previews, the two ways a batch is steered (Foreman or direct
mode) as chantier's current working, no cost figure, the ending in order, and under
  100 lines.
