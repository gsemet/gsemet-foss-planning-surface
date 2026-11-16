# Change Specification: a CR's folder is self-contained

## Goal

Everything a CR needs to be resumed later or elsewhere lives in its folder: the prototypes (in
versions), the scripts and experiments made during a grill or a study, the screenshots kept as
proof, and how to run a prototype again. The stated exceptions are the only things kept out. The
cards stop saying a prototype lives in a temporary folder and is thrown away, the Griller's rule
holds in every mode (not only in a planning surface or a worktree), and a chantier rule ranks
above the host's habit of sending scripts and intermediate results to its scratchpad. No empty
folder is created in advance.

## Decisions carried from `02-answers.md` (2026-11-12)

1. Fix the ambiguities: yes (all of the "Causes found" in `01-intent.md`).
2. No empty folder in every CR: a sub-folder exists only once something goes in it. Neither the CLI
   (`file`, `triage`, `take`, `close`) nor an agent creates `prototypes/`, `experiments/` or
   `evidence/` ahead of use.
3. Prototypes come in versions: `prototypes/01-<idea>/`, `prototypes/02-<idea>/`, … (two digits,
   then a short kebab-case name of the idea).
4. The archive in the PR keeps the retained prototype when it is not too big, zipped if needed.
5. When the folder is very big, the grill asks what to do with it at the end of the
   implementation.
6. Planning: the next batch, not batch-15 (the Chief of Staff's concern; nothing to code).

## The CR folder's layout (writer's choices, within the decisions)

The tree of `concepts.md` ("Change Request (CR)", the `text` block, today lines 46-56) gains two
optional entries and a clearer `evidence/` line, each marked "only once something goes in it":

```text
<slug>/
├── intake/              ← the raw request as received; never edited
├── 01-intent.md         ← the request, summarised and analysed
├── 02-answers.md        ← every answer the user gave about the CR, whoever asked
├── 03-change-spec.md    ← the Change Specification
├── summary.json         ← (unchanged)
├── STATUS.md, STATUS.json ← (unchanged)
├── prototypes/NN-<idea>/ ← each prototype version, with a README.md that says how to run it; only once there is one
├── experiments/         ← scripts, tests, benchmarks, studies and research notes (sources, quotes) made for the CR; only once there is one
├── evidence/            ← proof kept with the CR: screenshots kept on purpose, the Verifier's (work/verifier/evidence/)
└── work/                ← written while it runs: notes, gate logs, the PR body
```

- A script that belongs to one prototype version (its snapshot generator, its data builder) goes
  in that version's folder, not in `experiments/`.
- Each `prototypes/NN-<idea>/` holds a `README.md` of a few lines: what the version tries, the
  command that runs it again (its server command, its port), and what it needs.
- The covered files of a summary are unchanged (`intake/*.md`, `01`-`03`, `delivery.md`):
  `prototypes/` and `experiments/` are not covered, like `evidence/` and `work/`.
- Names in `experiments/` follow concepts' existing advice for subagent files (no `.md` name
  starting with `report`, `summary`, `findings` or `analysis`; a numbered name such as
  `01-benchmark.md`).

## What changes, area by area

### 1. `skills/chantier/references/concepts.md`

- **The tree** (above), with the two optional entries and the `evidence/` wording.
- **A new rule, "A CR's folder holds its work"**, placed right after the tree (or as a bullet of
  "Words" next to "Change Request (CR)"). It says:
  - Whatever an agent makes for a CR (a prototype, a script, a test, a benchmark, a study, a
    research note, a screenshot it keeps, a plan) is written in that CR's folder, in the place the
    tree gives, never in the host's scratchpad or a temporary folder; this rule ranks above the
    host's own instruction to use its scratchpad. Outside any CR's work, the scratchpad stays the
    host's.
  - A sub-folder is created only when its first file is written.
  - The stated exceptions (below, "Kept out by design and leaks stated").
- **The Chief of Staff's subagents** (the paragraph after "Starting an agent"'s table, today line
  374-377): remove "a prototype lives in a temporary folder and is thrown away". Replace with: when
  the work is for a CR, its brief names that CR's folder and the place in it (a
  `prototypes/NN-<idea>/` or `experiments/`), and its result (the study, the report) is written
  there as a file, not only returned in the conversation; when it is for no CR yet, its brief
  names a folder it writes to, and when a CR comes of it, the Chief of Staff moves what it kept
  into that CR's folder. It still never implements: no commit, no push, no PR, nothing in a CR's
  worktree.
- **"Archive"** (today lines 99-102): the cleaned archive's list gains "the retained prototype
  (`prototypes/NN-<idea>/`, zipped if needed), as the grill decided", see 4 below.

### 2. `skills/chantier/references/chief-of-staff.md`

- **"Subagents and the demo"** (today lines 1358-1361): same replacement as concepts' paragraph;
  it may point to concepts rather than restate it.
- **"Backlog and grill"**:
  - One paragraph on a CR's artifacts during a grill: prototypes and experiments go in the CR's
    folder per concepts; a new version of a prototype is a new `prototypes/NN-<idea>/` (the
    earlier ones stay); the user's choice of the retained version is recorded in `02-answers.md`
    at once like any answer (e.g. "Retained prototype: `prototypes/02-<idea>/`").
  - The leaks the asker closes during a grill: an image the user pastes in the chat (no file
    exists) is asked for as a file and saved in `evidence/`, or, if the user does not give it,
    described in `02-answers.md`; a built-in browser screenshot kept as proof is saved on purpose
    in `evidence/`; web research keeps its sources and quotes in an `experiments/` note; a claude.ai
    artifact or an inline visualization that matters to the CR has its source saved in
    `prototypes/NN-<idea>/` (its link, if any, written in that version's `README.md`); a plan-mode
    plan about the CR is written in the CR's folder; the agent's memory is never a CR's place
    (decisions go to `02-answers.md`, as "Record at once" already says).
  - **Size, at "grilled enough?"**: when the CR's folder is very big (see open question 1), the
    restatement says so and the asker adds one question in the same series format ("Asking the
    user: a series"): what to do with it at the end of the implementation (for instance A. keep
    the retained prototype zipped in the PR's archive and the rest in the planning folder only;
    B. keep everything in the planning folder only, nothing in the PR's archive; C. drop the
    non-retained versions at `close`). The answer is recorded in `02-answers.md` and the
    specification carries it.
  - **Files from a Griller in a worktree** (today line 324-326): the Chief of Staff places them
    before telling the user the worktree may be removed; nothing in the paragraph's other steps
    changes.

### 3. `skills/chantier/references/griller.md`

- Move the rule "Prototypes, plans and other artifacts go in the same CR folder, cleanly." out of
  "In a planning surface" into "What you do", so it holds in-project too, pointing to concepts'
  new rule (layout, versions, README, no scratchpad).
- "In a worktree": the files listed gain experiments and evidence; add that the Griller tells the
  user not to remove its worktree until the Chief of Staff has placed its files (the `files for
  <slug>` line, or, with no live Chief of Staff, its message to the user, says so).

### 4. `skills/chantier/references/driver.md`, "The archive in the PR" (today lines 210-217)

- The cleaned archive's list gains the retained prototype: the version `02-answers.md` (or the
  specification) names as retained, copied as `prototypes/NN-<idea>/`; zipped as
  `prototypes/NN-<idea>.zip` when it is above the "not too big" limit (open question 1); when
  `02-answers.md` records a decision on a very big folder, the Driver follows it. No other
  version and no `experiments/` go into the PR's archive (they stay in the planning folder's
  `5-archives/`).
- When the retained prototype is above the "very big" limit and `02-answers.md` records no
  decision, the Driver leaves it out of the PR's archive, says it in a `note`, and the PR's Known
  gaps names it ("retained prototype not in the archive: too big, no decision recorded"), so the
  ready line quotes it and the Chief of Staff asks the user.
- With no retained prototype named, nothing from `prototypes/` goes in (see open question 2).

### 5. `skills/chantier/references/hosts/claude-code.md`

- Next to "The host's scratchpad is outside the worktree" (today line 467): one sentence that the
  host's instruction to send scripts and intermediate results to its scratchpad does not apply
  to a CR's work, which goes in the CR's folder ([concepts](../concepts.md)); a worker still writes
  in its work folder, as today.
- `hosts/copilot.md`: no change unless it names a scratchpad (it does not today).

### 6. Docs

- `docs/planning-modes.md`: "Archives, in two places" (lines 78-82) gains the retained prototype
  in the PR's cleaned archive; "Grillers" (line 86) says the rule holds in every mode.
- `docs/planning-folder.md`: one sentence after the tree or in "What is published": a CR's folder
  may also hold `prototypes/NN-<idea>/` and `experiments/`, created only when used, published with
  the CR like its documents.
- `docs/cr-folder-lifecycle-texts.md` and its SVG: out of scope (see below).

### 7. CLI

No CLI change. `ship`'s check (`commands/delivery.py`, `archive missing from the PR at <path>`)
reads only that the archive folder exists, which still holds. `close` moves the whole folder to
`5-archives/`, prototypes and experiments included. The planning folder's `.gitignore`
(`core/files.py`) is unchanged.

## Kept out by design and leaks stated (written in concepts' new rule)

- Out of the CR folder: secrets, personal data, large binaries that are not the retained prototype
  (a dataset, a video above the forge's limits: the folder names where it is); the batch's own
  files and raw logs (already gitignored; a raw log stays in `work/gates/` or a `*.log` file).
- The agent's memory and the host's settings (`~/.claude/`): never a CR's place.
- What only the conversation holds (a subagent's reply, an inline visualization, a pasted image)
  is lost unless an agent writes it in the folder: concepts' rule says writing it is the agent's
  job, as above.

## Out of scope

- A size check or a zip command in the CLI (no measured cost yet; the agents zip with what the
  project has).
- The docs diagrams (`docs/cr-folder-lifecycle.svg`, `docs/cr-lifecycle.svg` and their texts):
  hand-drawn; a later CR adds `prototypes/` to them.
- Moving existing CRs' scattered files (the "visualization-backend" ones were already moved).
- A guard (the Write guard of `hooks/`) against scratchpad writes: no `hooks/` change.
- Agent files (`agents/`, `com.github.copilot/agents/`): no change.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes (a change to the cards, AGENTS.md).
- A search of `skills/` and `docs/` for "temporary folder and is thrown away" finds nothing; one
  for `prototypes/NN-<idea>/` finds concepts, chief-of-staff, griller and driver.
- `griller.md`'s prototype rule sits in "What you do", not only in "In a planning surface".
- Read-through: each decision of `02-answers.md` is found in the cards (no empty folders; versioned
  prototypes; retained prototype in the PR's archive, zipped if needed; the size question at the
  grill).
- No PR screenshot needed: the CR board pane does not change.

## Open questions for the user

1. **Size limits.** What counts as "not too big" (copied as is into the PR's archive) and "very
   big" (the grill asks what to do)? Proposed: as is up to 1 MB, zipped from 1 MB to 10 MB,
   "very big" above 10 MB.
2. **No retained version named.** When the grill made prototypes but recorded no retained one,
   does the PR's archive take none (proposed), or the highest-numbered version?
3. **Who asks when the folder grows big after the grill** (prototypes added during the batch):
   the Chief of Staff at the Driver's ready, through Known gaps as above (proposed), or the Driver
   blocks with a question?
