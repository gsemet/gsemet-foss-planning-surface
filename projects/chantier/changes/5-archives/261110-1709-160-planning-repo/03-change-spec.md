# External planning surface: chantier plans in a git repository of its own

## Goal

Today chantier plans inside the project, in `.agents/changes/`. This CR adds a second, fully
supported mode: the **external planning surface**. The planning part (file, triage, grill,
answers, specification, the batch's CR folders, the archives, the trash) lives in a separate git
repository, the *surface*, which holds one folder per project. The project's own repository gets
only the code and, if its maintainer wants, each CR's cleaned archive in the CR's PR.

The surface is a small, isolated workspace shared through git by a very small active team (2 to
4 people at most) working around one subject. It works like an Obsidian vault with obsidian-git:
every change is pushed to the default branch as fast as possible, like OneDrive. It is always
worked on its default branch, never in a worktree. Only the project's code gets worktrees.

The two modes are **in-project** (the default, today's behaviour, unchanged for a project that
declares nothing) and **external**. Every command, card, agent and host works the same in both,
and `just scenario` covers the external mode.

The user's real surface is the model: <https://github.com/gsemet/gsemet-foss-planning-surface>
(local clone `C:/Users/gaeta/Projets/gsemet-foss-planning-surface`). This CR also writes the docs
and draws the diagrams that explain the planning modes: what runs on the default branch and what
runs in a worktree, the remote limits, the Grillers' files, outside contributors, the surface's
nature and its place next to a tracker.

## Depends on

`changes-tree-v2` (P1, its own CR, `depends.json`). This specification uses its tree in both
modes:

```text
<planning folder>/
├── 1-inbox/<slug>/
├── 2-backlog/P1…P4/<slug>/
├── 3-ready/<slug>/                        CRs waiting for the next batch (a specification is not required to go there)
├── 4-batch/1-pending|2-actives|3-done/<number>-<slug>/     the CRs of the one current batch
├── 5-archives/<YYMMDD-HHMM>-<number>-<slug>/
└── 6-trash/<YYMMDD-HHMM>-<number>-<slug>/
```

and its rule that a running batch's own files (`batch.json`, `events.jsonl`, the STATUS files)
stay local to the steering machine. Wherever `changes-tree-v2` puts those local files, this CR
makes them ignored by the surface's git (below, "Local files"). Where this specification names a
folder, it is `changes-tree-v2`'s name; if that CR renames one, its name wins. Two of its rules
matter here:

- a CR may go to `3-ready` on the user's word without a specification (`open` and `order add` then take
  its `intake/request.md` as its specification, as `changes-tree-v2` says);
  nothing in this CR assumes a CR in `3-ready` is specified;
- a merged CR moves to `5-archives` when `changes-tree-v2` says (at once, or from
  `4-batch/3-done/` at `close`): "the archive" below is that move, whenever it happens.

Wording: "the `3-ready` folder" (CRs waiting for the next batch) and "a PR ready to merge" (a CR
handed back `ready`) are two different things. Every text this CR writes keeps them apart: never
"a ready CR" for a CR in `3-ready`; say "a CR in `3-ready`".

## Decisions carried from the grill (`02-answers.md`)

| # | Decision | Where it lands below |
| --- | --- | --- |
| 1 | The surface's tree is chantier's tree in both modes (via `changes-tree-v2`). | Depends on |
| 2 | Archives in both places: the archive in the surface's `5-archives`, with a pointer to the delivering PR and whether the archive was also delivered in that PR; a surface setting per project says whether the maintainer wants the archive in the PR. | Archives |
| 3 | The surface's own rules win for its sync; chantier taking the sync over between several Chiefs of Staff is `planning-server` (P3), not here. | Syncing the surface; Out of scope |
| 4 | A running batch's own files (`batch.json`, `events.jsonl`, STATUS) stay local (ignored by git). | Local files |
| 5 | No OKF for chantier's folders. | Out of scope; After the merge |
| 6 | Split into three CRs; this is the second, "on the surface's existing autosync". | Syncing the surface |
| 7 | CR folders keep chantier's number; a tracker issue is a link inside the CR. | The surface's layout |
| 8 | No migration command; chantier's own planning stays in-project for now. | Out of scope |
| 10 | One batch at a time per project. | The CLI |
| 11 | `planning-surface-positioning` merged here: its content goes into the docs. | Docs |
| 2026-11-07 | The clone defaults to `projects/<name>/.repo/`, the worktrees to `projects/<name>/.worktrees/`, or elsewhere by configuration (a relative path). | The surface's layout |
| 2026-11-07 | Without sync rules in the surface's `AGENTS.md`, the Chief of Staff commits and pushes the surface after each step that changes it. | Syncing the surface |
| 2026-11-07 | The Driver adds the CR's cleaned archive to its PR before the hand-back, in the project's repository, same format. | Archives |
| 2026-11-10 | The surface is always on its default branch; the Chief of Staff and the Griller run there; only the project's code gets worktrees. With a surface, "the main checkout" of the start check is the surface's checkout. | Sessions; Cards |
| 2026-11-10 | Explain the planning modes, the remote limits (the user's finding), Grillers' artefacts going to the Chief of Staff, outside contributors by a PR on the surface, the surface's nature (Obsidian-like, 2-4 people). | Docs; Hosts |
| closing | `3-stash` is named `3-ready`; keep it apart from "a PR ready to merge". | Wording above |
| spec Q1 | The surface declares (its `projects/<name>/`); the project's `AGENTS.md` may hold an optional pointer line, which the Chief of Staff reads and the CLI does not. | Declaring and finding |
| spec Q2 | A running CR's folder is pushed to the surface regularly; the archive is made at the end; only the report and the evidence are published, never detailed logs. This is apart from answer 4, which stands. | Local files; Archives |
| spec Q3 | The cleaned archive in the PR keeps `intake/`, `evidence/`, `01-intent.md`, `02-answers.md`, `03-change-spec.md`, the delivery file and `STATUS.md`; no `work/`, no detailed logs. | Archives |
| spec Q4 | This CR draws the external mode in the README and docs diagrams; the user reviews their renders in the PR. | Docs; Evidence |
| spec, left to the Driver | The archive setting is a line in `project.md`, `yes` when absent. A Griller in a surface worktree does not join the autosync; its files go to the Chief of Staff. No archive in the PR in in-project mode in this CR. The fallback sync (commit and push after each step) when a surface has no autosync. | Archives; Syncing the surface; Out of scope |

## The surface's layout

The surface is a git repository with, per project:

```text
<surface>/
├── AGENTS.md                      the surface's own rules (its sync, among others)
└── projects/<name>/
    ├── project.md                 the project: its remote, its default branch, its rules; the archive setting
    ├── checkout.yml               where the project's clone and worktrees are, relative paths
    └── changes/                   the planning folder: the tree above
```

- `checkout.yml` has two keys, `repo:` and `worktrees:`, each a path relative to
  `projects/<name>/` (the user's: `repo: ../../../chantier/`, `worktrees:
  ../../../chantier.worktrees/`). A missing file or key means the defaults
  `projects/<name>/.repo/` and `projects/<name>/.worktrees/`. The CLI reads this file with a
  tiny parser of its own (`key: value` lines, `#` comments; no dependency).
- `project.md` is the user's prose. It gains one fixed line that the CLI reads, the archive
  setting: `- Archive in the PR: yes` or `- Archive in the PR: no`; absent means `yes`.
- The surface's `projects/<name>/changes/` is the **planning folder**. In-project, the planning
  folder is `<project>/.agents/changes/`. Every card and doc that says `.agents/changes/` for the
  planning folder says "the planning folder" instead, and names both places once (in
  `concepts.md`).
- CR folders keep chantier's number (`156-diagrams-modes-griller`); a tracker issue, when there
  is one, is a link inside the CR (`intake/`, `01-intent.md`), not part of the folder's name.

## Declaring and finding the surface

The surface declares its projects: its `projects/<name>/` (with `checkout.yml` and `changes/`)
is the declaration, and the CLI needs nothing else. The project's repository is untouched, and
in-project mode is unchanged for any project whose planning folder is `.agents/changes/`.

The project's `AGENTS.md` may hold one optional pointer line in its `chantier` section, for
example `- planning: https://github.com/gsemet/gsemet-foss-planning-surface, projects/chantier`.
The Chief of Staff reads it and the CLI does not. A session started in the project's own
checkout that finds it says, in its first message, "this project plans in the surface at …;
start the session there", and does no planning in-project. The cards and the docs give the line's
form; the user writes it.

How the CLI finds the planning folder (recommendation; the exact option name is the Driver's):

1. A global option before the command, `--project <folder>`, names the project's folder in the
   surface (`<surface>/projects/<name>`, absolute; a bare `<name>` is accepted when the current
   directory is inside the surface). With it, the planning folder is `<folder>/changes/`, the
   clone and worktrees come from `<folder>/checkout.yml`, and the mode is external.
2. Without it, `Repo.find` works as today. If the git root it finds holds `projects/*/checkout.yml`
   or `projects/*/changes/` and no `.agents/changes/`, it is a surface: a command that needs a
   project exits 2 with `this is a planning surface with projects <a, b, c>: pass --project
   <name>` (one project only: that one is taken). `preflight` lists the projects and passes.
3. Otherwise, in-project as today.

Every `cli:` line the CLI prints (`take`, `round`, `handoff`) carries the option in external
mode, so a Driver or worker in a project worktree reaches the same planning folder without any
environment variable (concepts rule 9 forbids a leading assignment). The Chief of Staff's own
`$CHANTIER` is the skill's command plus `--project <absolute folder>` once its project is known
(`SKILL.md` and `session-start.md` say so).

`$CHANTIER rules` in external mode lists the project's instruction file (from the clone) and
what it links, then the surface's `AGENTS.md` and what it links, each under a heading line
(`project:` / `surface:`), so both rank above the cards: the project's for its code, the
surface's for the surface (its sync).

## Sessions: what runs where

| Session | In-project | External |
| --- | --- | --- |
| Chief of Staff | the project's main checkout, default branch | the surface's checkout, its default branch; one session per project (several projects of one surface may each have their own) |
| Griller | the project's main checkout; or a worktree that is never merged, its files sent to the Chief of Staff | the surface's checkout; or a surface worktree, never merged, its files sent to the Chief of Staff |
| Foreman | the project's main checkout | the surface's checkout (the batch's state is there); it removes merged CRs' worktrees with `git -C <clone>` |
| Driver, workers | the CR's worktree of the project | the CR's worktree of the project, under `checkout.yml`'s `worktrees` |
| Spec-writer and other subagents of the Chief of Staff | as their parent | as their parent; they write in the planning folder of the surface |

- The seat is per project: its file sits in the project's planning folder (local, below). A
  Chief of Staff in a surface asks the user once which project it plans when the surface has
  several and the user did not say (the router's question gains this when needed), and its title
  uses that project's name: `[env] Chantier [Chief of Staff]`, not the surface's folder name.
- `preflight` in external mode: P6 and P7 check the surface's checkout (the session's folder is
  the surface's root, not a linked worktree); P8 finds the project's instruction file in the
  clone; a new line says the surface's checkout is on the default branch of its remote (a warn
  otherwise: the surface is always worked on its default branch); a clone missing at
  `checkout.yml`'s path fails, naming the path and the remote from `project.md`, and the Chief of
  Staff clones it on the user's word (the agents do git). P10 reads the surface's
  `.claude/settings.*` as it reads the project's today.
- The project's clone is the "main checkout" for git only: `git fetch`, `git worktree add` and
  `git worktree remove` run there (`git -C <clone>`). No chantier session runs in it and nothing
  of chantier is written there, except by a Driver in its own worktree (the archive, below).
- `costs.transcript_path` finds a session's transcript from the session's own folder: in external
  mode that is the surface's root, not the project's (its fallback by session id stays).

## Local files and what is published

Two kinds of files never reach the surface's git, even with an autosync that commits every
~10 s.

1. **The batch's own files (answer 4):** those of `changes-tree-v2` (`batch.json`,
   `events.jsonl`, `brief.md`, the STATUS files, the batch's lock), plus `.lifecycle.lock`,
   `.long-gate.lock`, `.batch-number` and the seat (`seat.json`). They stay on the steering
   machine.
2. **Detailed logs (spec Q2):** the long gate's logs (`work/gates/`, `*.log`) and any other raw
   log a role writes under a CR's `work/` (transcript extracts, command output dumps). They stay
   local, and so never reach the archive in the surface or in the PR.

The rest of a running CR's folder **is** pushed to the surface regularly, by the surface's sync,
while the CR is in `4-batch/`: its documents (`intake/`, `01`–`03`, `depends.json`), its
`evidence/`, and the reports in `work/` (the PR body `work/pr-body.md`, the retro, the notes a
role writes for the user). The roles keep raw output in the ignored log files and write only
reports and evidence elsewhere; the cards say so (driver.md, worker.md: "a log goes in
`work/gates/` or a `*.log` file, never in a file that is published").

- The CLI keeps both kinds ignored by writing a `.gitignore` inside the planning folder (its own
  folder, so the rule "chantier writes only in the planning folder" holds; it never edits the
  surface's root `.gitignore`). It writes or completes that file before it writes any of them
  (`init`, `file`, `open`, `take`, `gate`, `seat take`), so no autosync cycle can see one first.
- In-project mode: the same `.gitignore` is written (harmless when `.agents/changes/` is not in
  git), so both modes behave alike.
- CR numbers are counted from the tracked folders (`4-batch/`, `5-archives/`, `6-trash/`) and
  `.batch-number`, per project, so a second machine continues the numbering from what it pulled.

## Syncing the surface

- The surface's own rules win. When its `AGENTS.md` says how it syncs (the user's surface runs a
  git autosync, `scripts/ai-autosync-git.py`, with one leader per checkout), every chantier
  session in the surface's checkout follows it as written: the Chief of Staff, the Grillers and
  the Foreman join it as the surface's rules say. chantier adds no sync of its own and runs no
  git command on the surface beyond what those rules ask.
- When the surface's `AGENTS.md` says nothing about sync, the Chief of Staff commits and pushes
  the surface after each step that changes it (a file, a grill answer, a specification, `open`, a
  merge recorded, `close`), and during a batch at each hand-back it hears, with explicit paths
  (`git add -- <path>`), a plain push to the default branch, a rebase on a rejected push, and no
  force push (concepts rule 8). A Griller in the surface's checkout does the same for its own
  writes.
- Several Chiefs of Staff on several projects of one surface work through the surface's autosync
  as any two sessions do there today; chantier coordinating their pushes and rebases is
  `planning-server` (P3).
- A Griller in a surface worktree (remote) does not join the surface's autosync and commits
  nothing there: its files go to the Chief of Staff, who places them in the surface's checkout.
  The docs give the sentence for the surface's `AGENTS.md`, since its rules rank above the cards
  ("After the merge").

## Archives

The archive is made at the end, when the CR moves to the surface's
`projects/<name>/changes/5-archives/<YYMMDD-HHMM>-<number>-<slug>/` (per `changes-tree-v2`): the
whole CR folder as the surface holds it, that is without the detailed logs, which were never
published. When the user's merge is recorded (`order merged`, or the Foreman's), the CLI writes a
short `delivery.md` in the CR's folder, which travels with it into the archive:

```markdown
# Delivery

- PR: <link>
- Merged: <UTC time>
- Archive in the PR: yes, at <path in the project's repository> | no (project setting) | no (missing from the PR)
```

The **archive in the PR**, when the project's `project.md` line says `yes` (or is absent):

- `take` and `handoff` print one more line in external mode: `archive: in the PR at
  .agents/changes/5-archives/<YYMMDD-HHMM>-<number>-<slug>/` (the stamp is the time of `take`'s
  first run for the CR, kept in the record so it never changes) or `archive: not in the PR`.
- Before each hand-back `ready`, the CR Driver writes the cleaned archive in its worktree at that
  path and commits it with the change. It holds: `intake/`, `evidence/`, `01-intent.md`,
  `02-answers.md`, `03-change-spec.md`, the delivery file (`delivery.md`: what the PR delivers,
  from the PR body's summary, with the PR link once known) and `STATUS.md` (the implementation
  report, as it stands). It holds no `work/` and no detailed log. The Driver keeps it current at
  each later round.
- `ship` (read-only git, as today) says what is off when the setting asks for the archive and the
  head does not hold that folder: `archive missing from the PR at <path>`. It records what it saw;
  the `delivery.md` line in the surface comes from the last `ship`.
- `pr-template.md`: the archive folder is part of the diff; the description names it only in its
  Internal references section, as any `.agents/changes/` path; the Verifier's check of the
  description against the diff takes the archive folder as expected, not as an unexplained file.
- If the project ignores `.agents/changes/` (the in-project advice of `init.md`), the archive
  cannot be committed: the Driver says it in a `note` and hands back with the PR as it is; the
  Chief of Staff asks the user (no `git add -f` without the user's word).

In-project mode is unchanged by this CR: the archive stays in the local `5-archives/` and is not
added to the PR.

## The CLI (`skills/chantier/scripts/cli/src/chantier/`)

Recommendations; the structure is the Driver's.

- `state.py`, `Repo`: separate the **project root** (the git repository of the code: `root`,
  `git_dir`, `default_branch`, `remote`, the worktrees) from the **planning folder**
  (`changes`). In-project, `changes` is `root/.agents/changes` and `worktrees` is
  `<root>.worktrees` as today; external, both come from the project's folder in the surface and
  its `checkout.yml`, and the surface's root is known too (for `rules`, preflight, the transcript
  folder). `Repo.find` resolves the mode as in "Declaring and finding".
- Paths recorded in `batch.json` (`cr["path"]`, `origin`) are relative to the planning folder,
  not to the project root; `project_path` checks "inside the planning folder" for CR folders,
  and "inside the project root" where it checks a project path. A batch opened before this change
  (paths starting `.agents/changes/`) still reads (in-project, both readings agree).
- `lifecycle.stage_layout`, `changes_lock`, `commands.init`, `file_cr`, `triage`, `abandon`,
  `add_cr`, `_facts`, `rules`, `seat`, `gate`, `ship`, `preflight`, `open_batch`, `close`,
  `status.write_dashboard`: work from the planning folder and the project root as above.
- `open` reads the remote and the default branch from the project's clone; the brief's "Project
  instructions" line names the project's file and, in external mode, the surface's.
- `_facts` (and so `take`, `handoff`): absolute paths for the specification, the folder and the
  worktree (already absolute); one more line in external mode, `clone: <path>` (where the Driver
  runs `git worktree add`), and the `archive:` line.
- `gate` keeps writing its log in `work/gates/` (ignored, above).
- `init` in external mode (with `--project`, or the only project): creates the missing stage
  folders and the planning folder's `.gitignore`; it writes neither `project.md` nor
  `checkout.yml` (the user's) and refuses a surface checkout that is a linked worktree (as P7).
- `order merged` (and the Foreman's): writes `delivery.md` in external mode.
- One batch at a time per project: unchanged rail, now per planning folder; two projects of one
  surface may each run one.
- Output: `take`, `handoff` stay full output; every other command keeps its ten-line limit.
- No new dependency; POSIX and Windows paths (`checkout.yml` paths with `/` or `\`, resolved
  with `Path`), UTF-8 everywhere.

## The CR board (`hooks/register.tsx`)

The board reads the STATUS index from the git root of the session's folder. In a surface it reads
each project's index under `projects/*/changes/` (the path `changes-tree-v2` gives) and shows
one section per project, the project's name as its heading. Still read-only, still only `git
rev-parse` as a process. Its file links point into the surface.

## Cards and skills (`skills/`)

- `references/concepts.md`: "Planning folder" and "Planning surface" in Words (the two modes,
  the two places, the surface's layout, `checkout.yml`, the project's clone, the optional pointer
  line); the CR's description says "a folder in a stage of the planning folder"; what is
  published and what stays local; the seat's path; the worktree name `<worktrees>/<batch>-<cr>`
  (from `checkout.yml` in external mode); `$CHANTIER` carries `--project` in external mode; the
  Spec-writer's first line unchanged.
- `references/session-start.md`: section 1 says, as settled now, that with a surface "the main
  checkout" is the surface's checkout on its default branch, that the project's clone hosts no
  session, and that a session in a project whose `AGENTS.md` points to a surface says so and
  plans nothing there; section 2: in a surface with several projects, the Chief of Staff learns
  its project first (the user's word, or the only one) and its seat is that project's; section 3:
  the title's Project is the project's name; section 4 (introduction): "Zero configuration" says
  the planning folder is in the project (`.agents/changes/`) or in an external surface.
- `references/chief-of-staff.md`: the surface's sync (its rules, else commit and push after each
  step); the clone missing at `checkout.yml`'s path is cloned on the user's word; merged and
  dropped CRs' worktrees removed with `git -C <clone>`; files from a Griller in a worktree placed
  in the planning folder; outside contributors' CRs arrive by a PR on the surface, which the user
  reviews and merges on the forge, and a CR so merged into `1-inbox` or `2-backlog/P<n>` is read
  like any other.
- `references/griller.md`: in a surface, the Griller runs in the surface's checkout and writes
  there directly, on the surface's sync rules; "In a worktree" applies to a surface worktree (no
  commit, no PR, no autosync, files to the Chief of Staff, which places them); prototypes, plans
  and other artefacts go in the same CR folder, cleanly, and reach the Chief of Staff, never
  merged.
- `references/foreman.md`: runs in the surface's checkout in external mode; removes merged CRs'
  worktrees and branches with `git -C <clone>`.
- `references/driver.md`: `git worktree add` from the clone that `take` names (`git -C
  <clone>`); the archive in the PR (above) before each hand-back `ready` when `take` says so; the
  Verifier's detached worktree under the same worktrees folder; logs only in ignored log files.
- `references/worker.md`: a raw log goes in a `*.log` file or `work/gates/`, never in a published
  file; reports and evidence as today.
- `references/init.md`: in a surface, `init` creates the named project's folders; the tour says
  where the planning folder is; the `.gitignore` advice applies to in-project mode only.
- `references/pr-template.md`: the archive folder in the diff, named in Internal references.
- `references/spec-writer.md`, `routing.md`: only the wording "`.agents/changes/`" → "the
  planning folder" where it means it.
- `skills/chantier/SKILL.md`, `skills/chief-of-staff/SKILL.md`, `skills/griller/SKILL.md`:
  "everything chantier writes goes to the planning folder (`.agents/changes/`, or the project's
  folder of an external surface), and, when the project asks for it, a CR's archive in its PR";
  `$CHANTIER` with `--project` in a surface.
- `agents/*.md` and `com.github.copilot/agents/*.agent.md`: change only if a body names
  `.agents/changes/`; any change is made on both hosts together, bodies identical.

## Hosts

- `references/hosts/claude-code.md`, "Classes of session": record **as the user's own finding
  (2026-11-10)**, not as a proved trial: a remote session cannot be started outside a worktree,
  which blocks chantier's planning on the default branch; so the Chief of Staff is started
  locally (desktop, no worktree), then put in remote (Remote Control). Nested sessions are a
  problem in remote too. In remote the setup is therefore: reuse the Chief of Staff's session
  (direct mode), plus, optionally, Griller sessions in worktrees that are never merged. Replace
  the line "Whether a remote session can start without a worktree: unproved" with this finding,
  and rewrite the "A Chief of Staff and Grillers in remote" block to it (start locally, then
  Remote Control; Grillers in never-merged worktrees). The rows already proved stay as they are.
- Same reference, new rows: a session in the surface writes in the project's clone and
  worktrees, which are outside its folder; the host must allow those folders (Claude Code:
  additional working directories). Unproved until tried: the trial is a Chief of Staff in a
  surface whose Driver creates a worktree from the clone and commits there. Give the "For you"
  block to add the folders, marked unproved.
- `references/hosts/copilot.md`: the same folder access, unproved; the remote finding is Claude
  Code's, so Copilot says nothing of it beyond "not tried".

## Docs and diagrams

- `README.md`:
  - the opening bullet "Zero configuration" and the "What is Chantier?" CLI paragraph: the
    planning folder is in the project (`.agents/changes/`) or in an external surface;
  - a new section **Planning modes**, after "How Chantier works": the two modes; what runs on
    the default branch (the Chief of Staff, the Foreman, the Grillers: the project's main
    checkout in-project, the surface's checkout in external mode) and what runs in a worktree
    (each CR's Driver and workers, in the project; a Griller in a never-merged worktree, in
    remote); the remote limits, said as the user's finding; the diagram below; a link to the full
    page;
  - "Change Requests Lifecycle": next to the existing tracker sentence, the positioning: the
    planning folder (in the project or external) is the tactical, short-term plan, the closest
    to the work site; Jira, GitLab work items or GitHub issues keep the strategic, long-term plan,
    or serve as the interface for outside customers and support;
  - "Change Request lifecycle": the tree as `changes-tree-v2` leaves it, with the external
    layout beside it, what is published and what stays local, and the archive's two places.
- A new page `docs/planning-modes.md` (linked from the README and `docs/use-cases.md`):
  - in-project and external, side by side; what each session runs on (the table of "Sessions");
  - the surface: a git repository, one folder per project (`project.md`, `checkout.yml`,
    `changes/`), always on its default branch; an isolated, multi-user workspace for a very small
    active team (2 to 4 people), working around one subject, that works like an Obsidian vault
    with obsidian-git: every change pushed to the default branch as fast as possible, like
    OneDrive; its own sync rules win;
  - the optional pointer line in the project's `AGENTS.md`, and its form;
  - what stays local (a running batch's own files, detailed logs) and what is pushed while a CR
    runs (its documents, its reports, its evidence);
  - archives in both places, the `project.md` setting, `delivery.md`, what the archive in the PR
    holds;
  - Grillers: prototypes, plans and other artefacts written cleanly in the CR folder; from a
    worktree they go to the Chief of Staff, never merged, and the Griller does not join the
    surface's autosync there;
  - outside contributors: they submit a CR, into `1-inbox` or a priority of `2-backlog`, only by a
    PR on the surface; the maintainer reviews and merges it;
  - remote: the user's finding (start the Chief of Staff locally, then Remote Control; direct
    mode by reusing that session; Grillers in never-merged worktrees);
  - privacy: a public surface exposes the requests, the grills, the reports and the evidence; the
    user chooses the surface's visibility;
  - setting one up: create the project's folder, `project.md`, `checkout.yml`; clone the project
    where `checkout.yml` says; start the Chief of Staff in the surface; `init`.
- **Diagrams (spec Q4):** this CR draws the external mode in the README's and the docs' diagrams.
  The docs' SVGs say what chantier should be, so they show both modes:
  - a new `docs/planning-modes.svg` (with its `docs/planning-modes-texts.md`, as the other
    diagrams have): the surface with its project folders, the project's clone and worktrees, and
    which session runs where, on the default branch or in a worktree, in-project and external,
    with the remote setup;
  - `docs/how-chantier-works.svg`, `docs/how-chantier-works-simple-direct.svg`,
    `docs/how-chantier-works-simple-foreman.svg`: the planning folder shown as "in the project or
    in a surface";
  - `docs/cr-folder-lifecycle.svg` (and `docs/cr-lifecycle-simple.svg` where it names the
    folder): the archive's two places, in the surface and, by the setting, in the PR;
  - each `*-texts.md` beside a changed SVG updated with it.
  The diagram's tree uses `changes-tree-v2`'s names. The PR carries a PNG render of each new or
  changed SVG (in the description, uploaded by the forge's CLI, per driver.md's evidence rule) so
  the user reviews them there.
- `docs/use-cases.md`, `docs/tutorial-claude-code.md`: one line each pointing to the new page.
- `CONTRIBUTING.md`: the list of what the CLI writes names the planning folder in both modes.
- `AGENTS.md` (this repository's rules), the line "chantier writes only in `.agents/changes/`"
  becomes: "chantier writes only in the planning folder (`.agents/changes/`, or the project's
  folder of an external planning surface), as plain JSON and Markdown, and a CR's cleaned archive
  in its PR when the project asks for it". This is a project rule: say it in the PR description.

## After the merge (not in the PR)

These are edits in the user's surface, a different repository; the Chief of Staff proposes them
and makes them only on the user's word:

- rename `projects/*/changes/3-stash` to `3-ready` (`agentic-planning-surface` still has the
  older `1-inbox … 3-batches, 4-archive, 5-trash`: the user decides);
- the surface's `AGENTS.md`: drop the OKF rules for chantier's folders (answer 5), use the stage
  names of `changes-tree-v2`, drop the `<issue>-<slug>` naming for chantier's CR folders
  (answer 7), and add the sentence that a session in a worktree of the surface does not join the
  autosync (it sends its files to the Chief of Staff);
- each `project.md`: the archive line, when the user wants `no`;
- the project's `AGENTS.md` (chantier's own, later): the optional pointer line, once chantier's
  planning moves to the surface (not now: answer 8).

## Out of scope

- chantier taking over the surface's sync between several Chiefs of Staff (pushes, rebases, the
  autosync itself, multi-checkout coordination): `planning-server` (P3).
- OKF frontmatter, `index.md` files and `just validate` for chantier's folders (answer 5).
- Any migration command, in either direction; chantier's own planning stays in-project (answer 8).
- The tree itself (`changes-tree-v2`).
- Archives in the PR in in-project mode.
- Managing PRs on the surface (outside contributors): the maintainer uses the forge; docs only.

## Evidence

- `just check` passes on Linux, macOS and Windows. `tests/test_structure.py` stays structural; at
  most it gains the external variant of
  `test_the_plugin_runs_with_no_setup_and_writes_only_in_agents_changes` (renamed to "the
  planning folder"): in a temporary surface with one project, `preflight` passes, `open` and
  `take` work, and `git status --porcelain -uall` of the surface shows only files under the
  project's `changes/` and none of the local files; the project's clone stays clean. The links
  test covers the new doc page.
- `just scenario` gains an external run, on both forges, beside the in-project run (unchanged
  checks still pass):
  - a temporary surface repository with a bare origin, two projects (`projects/demo`,
    `projects/other`), `checkout.yml` pointing to a clone outside the surface, and the clone with
    its own bare origin;
  - at the surface's root: a command without `--project` exits 2 naming both projects; `init
    --project demo` creates the folders and the `.gitignore`; with one project only, none is
    needed;
  - a clone missing at `checkout.yml`'s path: `preflight` fails naming the path;
  - `file`, `triage`, `open`, `take` (its `cli:` line carries `--project`, its `clone:` and
    `archive:` lines), the scripted Driver creates the worktree under `checkout.yml`'s
    `worktrees`, `round`, `gate`, `ship` (once without the archive: `archive missing from the
    PR`; then with it), `handback`, `order merged`, `pause`, `close`, all run from the project
    worktree for the Driver's calls and from the surface for the steering calls;
  - after each step, `git status --porcelain -uall` of the surface lists no `batch.json`,
    `events.jsonl`, STATUS file, lock, `.batch-number`, `seat.json`, `work/gates/` file or
    `*.log`, and does list the running CR's documents, `evidence/` and `work/pr-body.md`; the
    project's clone gains nothing but what the scripted Driver committed on its branch;
  - the archive in the PR: the Driver's branch holds the cleaned archive with `intake/`,
    `evidence/`, `01`–`03`, `delivery.md` and `STATUS.md`, and no `work/`;
  - the archive in the surface: in `5-archives`, with `delivery.md` naming the PR and "Archive in
    the PR: yes, at …", and no gate log; the second project, its `project.md` set to `no`, gets
    "no (project setting)" and `archive: not in the PR` in `take`;
  - `rules` lists the project's `AGENTS.md` then the surface's;
  - two projects of one surface each open a batch at once; a second `open` on the same project
    is refused;
  - the seat: one per project.
- `scenario/README.md` lists the external run's checks; the line "nothing written outside
  `.agents/changes/`" says "outside the planning folder".
- The diagrams: a PNG render of each new or changed SVG in the PR's description, for the user's
  review.
- The host trials (folder access, the remote finding) are recorded as unproved or as the user's
  finding, never as proved by this PR.

## Open questions

None: the user answered the specification's questions on 2026-11-10 (`02-answers.md`, "The
specification's open questions"), and the points left to the Driver carry their recommendation
above.
