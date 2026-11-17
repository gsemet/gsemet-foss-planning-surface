# Change Specification: docs-lifecycle

## Goal

The docs say what chantier is on `main` today (ac5e453 and before), in the user's words: a batch
is **running**, then **paused**, then **closed** on the user's word; it is steered by a
**Foreman** or, in **direct mode**, by the Chief of Staff itself, with the same lifecycle; and the
rest of 2026-11-07's work (init, the spec-writer, the paused batch that takes new CRs, the board's
slots, the PR template) is in the README and in every out-of-date page of `docs/`. A new diagram
shows the batch lifecycle, `how-chantier-works` and `how-chantier-works-simple` show both
steerings, and the use cases are split into one document per configuration. The new and
changed SVGs are approved by the user, as prototypes, before the CR starts; the Driver delivers
them.

This is a docs-only CR: no card, agent file, CLI, scenario or test changes.

## Sources of truth (read before writing)

The docs describe what these say; where a doc and a source differ, the source wins and the doc
changes. Never describe behaviour the sources do not hold.

- `skills/chantier/references/concepts.md`: **Batch**, **Batch lifecycle** (the three words,
  "hold" for `order slots --note 0`), **Steering session**, **STATUS**.
- `skills/chantier/references/chief-of-staff.md`: "Backlog and grill" (restatement, "grilled
  enough?", the spec-writer in the background, `work/specifying`), "Starting a batch" (when direct
  mode is proposed, `preflight --direct`), "While it runs" (Completion report, the pause,
  Closing), "Steering a batch yourself" (all of it).
- `skills/chantier/references/init.md`, `spec-writer.md`, `pr-template.md`.
- `skills/chantier/references/hosts/claude-code.md` and `hosts/copilot.md` (direct mode rows,
  heartbeat in direct mode).
- `git log --since=2026-11-07 main`: e967a31 direct mode, 38505fa init, 0fec176 board slots,
  f273ea2 spec-writer, 424ca89 landed batch paused, c913e43 PR template, ac5e453 batch lifecycle.

Words: only **running**, **paused**, **closed** for a batch's state; "hold" for slots at 0; never
"land", "landed" or "epoch" in user-facing text (the CLI command names `foreman set --epoch` may
appear only where a command line is quoted, and none needs to be here). A CR is named by number
and slug together ("CR-142 grill-rules") where the docs name one.

## What changes

### 1. New diagram: `docs/batch-lifecycle.svg` and `docs/batch-lifecycle-texts.md`

A new SVG, in the style of the existing ones (`docs/how-chantier-works.svg`,
`docs/cr-lifecycle-simple.svg`): same `font-family` stack with the emoji fonts, `#f8fafc`
background, an emoji header (`<text>` title at font-size 30, subtitle at about 17.5), the same
slate and orange palette, a `<title>` and a `<desc>`, UTF-8, plain SVG with no script and no
external reference.

Content (all of it, nothing more):

- Header: "Life of a batch" (with an emoji, e.g. 📦), subtitle: one batch at a time, running,
  paused, closed on your word.
- Three state boxes, and only these: **running**, **paused**, **closed**.
- Transitions, each labelled with what triggers it and the command:
  - into running: your go on the plan, then `chantier open` (Foreman mode) or `chantier open
    --direct` (direct mode); `open` is refused while a batch is not closed.
  - running → paused: every CR merged or cancelled; the steering session removes the merged CRs'
    worktrees and branches, then `chantier pause`. At the pause: the cost to date is computed and
    shown, the batch's `STATUS.md` is its exit report, the Completion report goes to you.
  - paused → running: new work, `chantier order add` (or `order qa`); it pauses again at the end,
    with the cost to date grown.
  - paused → closed: only on your word ("close the batch"): `chantier close` (the check: refused,
    naming the cause, while anything runs or the final cost cannot be priced; otherwise the final
    cost and what goes), then `chantier close --yes` on your yes: the batch folder is deleted,
    the dropped CRs' worktrees and branches are removed with git. Without a yes, everything stays.
  - A note on paused: it stays paused, however long, until you say "close the batch".
- The two steerings as a variant on the same diagram, not a second diagram: a band or legend that
  says the states and transitions are the same with a 👷 Foreman or with the 🤵 Chief of Staff in
  direct mode, and one difference marked on the running state: a running **direct** batch is
  strict (`order add` and `order qa` refused, except a release CR and its fixes); a paused batch,
  of either steering, takes new CRs.
- A small note, outside the states: "hold" (`order slots --note 0`: no new Driver starts) is not
  a state.

`docs/batch-lifecycle-texts.md` follows the existing companions exactly
(`docs/cr-lifecycle-simple-texts.md` is the model): a `# <title>` line, one paragraph equal to the
SVG's `<desc>`, then one `## <part>` section per area of the drawing, each holding a ```` ```md ````
block with every visible text of that area, as drawn.

### 2. Changed diagrams (SVG and `-texts.md` together, always in step)

Each changed SVG's `<desc>` and its companion's first paragraph are updated together and stay
equal; every text drawn is in the companion, and every companion text is drawn.

- **`docs/how-chantier-works.svg` and `docs/how-chantier-works-texts.md`: both modes.**
  - Keep the four lanes (MAIN SESSION, NESTED SESSION, DRIVERS, WORKERS) and the Foreman path as
    drawn. Add the direct-mode variant: a dashed path from the 🤵 Chief of Staff to the Drivers,
    labelled so it reads "direct mode: the Chief of Staff steers the batch itself, no Foreman
    session", and mark the Foreman box/lane as "Foreman mode".
  - Add the ✍️ Spec-writer (or another fitting emoji) as the Chief of Staff's agent in the main
    session: "writes the Change Specification, in the background, on your word".
  - "Coding Agents" box: Foreman mode in Claude Desktop or a Copilot SDK host; direct mode in any
    Claude Code entry point or a Copilot agent session.
  - `<desc>` and the companion's paragraph: say that on your go the Chief of Staff starts one
    Foreman session per batch, or steers the batch itself in direct mode; that the spec-writer
    writes the specifications; and where each mode runs (as above). The CLI box keeps "open,
    take, ship, pause".
- **`docs/how-chantier-works-simple.svg` and a new `docs/how-chantier-works-simple-texts.md`:
  both modes.** Today it shows the Foreman path only and has no companion (its `<title>` is "How
  chantier works (simple)"). Add the direct-mode variant the same way as in
  `how-chantier-works.svg` (a dashed path from the 🤵 Chief of Staff to the Drivers, "direct mode:
  the Chief of Staff steers the batch itself, no Foreman session"; the Foreman marked "Foreman
  mode"), kept simple: no spec-writer box unless it fits without crowding. Update its `<desc>`
  (today: "On your go it starts one Foreman session per batch of changes, …") to say the Chief of
  Staff starts one Foreman session per batch or steers the batch itself in direct mode. Write the
  companion in the same pattern as the others: `# <title>`, the `<desc>` paragraph, one
  `## <part>` section per area with every drawn text in a ```` ```md ```` block.
- **`docs/cr-lifecycle.svg` and `docs/cr-lifecycle-texts.md`.**
  - Spec loop: "🤵 writes the spec" is false now; the spec is written by the spec-writer agent,
    started by the Chief of Staff on your word that the CR is grilled enough (after the Chief of
    Staff's restatement). Say so in the box.
  - Legend: 👷 Foreman becomes "👷 Foreman (🤵 Chief of Staff in direct mode)", or an equivalent
    legend line, so every Foreman box reads as "the steering session".
  - Pause lane: keep it; it already says `chantier pause`, cost to date, your word later to close.
    Make sure it reads "the batch is paused; new work sets it running again" (one short line).
  - Footer: add one line naming the batch lifecycle diagram (`docs/batch-lifecycle.svg`) only if
    it fits the existing footer style; otherwise leave the footer.
- **`docs/cr-lifecycle-simple.svg` and `docs/cr-lifecycle-simple-texts.md`.**
  - "who drops it, clarifies it or writes the spec" (desc) and the Spec box: the spec-writer
    writes the spec; you approve it.
  - "BUILD · 👷 Foreman runs the batch": add "or 🤵 the Chief of Staff, in direct mode".
- **`docs/cr-folder-lifecycle.svg` and `docs/cr-folder-lifecycle-texts.md`:** change only a text
  made false by 2026-11-07's work. If `03-change-spec.md` is labelled as written by the Chief of
  Staff anywhere, it becomes the spec-writer's. Otherwise untouched.
- **`docs/batch-pace.svg`:** untouched in this CR (the user's word), though its subtitle no
  longer matches the paused batch.

### 3. The README (`README.md`)

- Intro (lines 5-7): one "Foreman" coordinates the work underneath, **or** the Chief of Staff
  itself in direct mode.
- "## How Chantier works": name the simple diagram first,
  `![How chantier works, in short](docs/how-chantier-works-simple.svg)`, then the existing
  detailed one, as the CR lifecycle section does (simple, then detailed).
- **The README does not name `docs/batch-lifecycle.svg`** (the user's word: they add it later).
  No "Batch lifecycle" section with its image; the batch lifecycle is told in words where the
  README already speaks of the pause and close.
- "What is Chantier?":
  - Step 2: after the grill, the Chief of Staff restates the CR and asks whether it is grilled
    enough; on your word a **spec-writer** agent writes `03-change-spec.md` in the background,
    which the Chief of Staff reviews against your answers before showing it to you.
  - Step 3: keep direct mode, and add one sentence: direct mode is less dynamic than Foreman mode
    (a running batch takes no new CR, and the Chief of Staff, busy steering, holds no grill in
    that session) but has the same lifecycle; see [direct mode](https://github.com/gsemet/chantier/blob/main/docs/use-cases-direct.md).
  - Step 5: the Driver writes the PR description from the default template shipped in the skill
    (`skills/chantier/references/pr-template.md`) unless your project has its own template, which
    ranks above it.
  - Step 6: "The Foreman reports back" also covers the Chief of Staff in direct mode.
- "Use" table: "run the P1s" row: "then a Foreman starts on your go, or the Chief of Staff steers
  in direct mode"; "drop CR-103" row: "an order for the steering session (the Foreman, or the
  Chief of Staff in direct mode)"; new rows: "it is grilled enough" (the spec-writer writes the
  specification in the background) and "close the batch" (the check and the final cost, then
  closing on your yes).
- "The CR board": add that each live batch shows its slots (`Slots 2/4, 2 free`).
- "Change Request lifecycle" paragraph on the pause: "the Foreman stays idle" becomes "the
  steering session stays idle"; the worktree sentence names the steering session (the Foreman,
  or the Chief of Staff in direct mode) as the one that removes a merged CR's worktree.
- "Supported hosts": keep the table for Foreman mode and say so; add direct mode: it runs on any
  Claude Code entry point (the Desktop app, the terminal, VS Code, a Remote Control session with
  no Foreman to reuse) and in a Copilot agent session, checked by `chantier preflight --direct`,
  with the same heartbeat in the Chief of Staff's own session. "Preflight refuses everything else
  (a VS Code tab, the terminal, …)" becomes: Foreman mode refuses them and the plan proposes
  direct mode there; an unattended run and a linked worktree are refused in both modes.
- "Costs and budgets": in direct mode the steering is one `Chief of Staff (steering)` line,
  counted in the batch's spend and budget as a Foreman's is; the rest of the Chief of Staff's
  session stays apart.
- "Install" / "Use" links: the use cases link points to `docs/use-cases.md` (now the common page,
  see 4) and names the two configuration documents.
- "Repository layout": `docs/` holds "diagrams and the user docs" (tutorial, use cases).

### 4. Use cases: one document per configuration

The configurations are the two steerings:

| Configuration | Where it runs | File |
| --- | --- | --- |
| Foreman mode | Claude Desktop (nested session), a Copilot agent session | `docs/use-cases-foreman.md` |
| Direct mode | any Claude Code entry point, a Copilot agent session | `docs/use-cases-direct.md` |

Copilot is not a third configuration: each document ends with its own "On GitHub Copilot"
section.

- **`docs/use-cases.md` becomes the common page.** It opens with "Choose your configuration": the
  table above, one line each on when the plan proposes direct mode (the host cannot start a
  Foreman session, or the batch has few CRs) and that your go decides, and the links. It keeps the
  situations that do not depend on the steering, updated:
  - "Start on a new project": "init" / "I am new here": `chantier init` creates the five stage
    folders, then a guided tour of your project, in the chat or as an HTML page, which writes
    nothing in the project except what you say yes to. The existing "prepare yourself" text
    stays as the other way in.
  - "Turn ideas into ready work": grill with recommended answers, every answer recorded at once
    in `02-answers.md`, the restatement and "grilled enough?" (you decide), then the spec-writer
    in the background; a specified CR waits in the inbox or backlog until you prioritise and pick
    it.
  - "Your pull requests' description": the default PR template (sections, English, no internal
    reference outside "Internal references"); your project's own template ranks above it; ask
    for your own template and it becomes a CR.
  - "Use your own agents", "Know what it costs" (with the steering line of direct mode; fix the
    two sentences that say `close` needs a Foreman: it needs a recorded steering transcript, the
    Foreman's or, in direct mode, the Chief of Staff's), "When chantier says no" (the Desktop
    app or a Copilot agent session is needed for Foreman mode only).
  - The batch lifecycle in three lines, with the image link `batch-lifecycle.svg`.
- **`docs/use-cases-foreman.md`** takes, adapted, the sections that are about running a batch
  with a Foreman: "Run a batch overnight", "Build independent pull requests", "Build a stack of
  pull requests", "Steer a running batch" (table and orders paragraph), "Ask for user testing",
  "Make a release", "Recover after a restart", the pause and close (paused, new work sets it
  running again, closed on your word), and "On GitHub Copilot" (heartbeat `/every`). It says what
  makes this mode dynamic: CRs join while it runs (`order add`), QA during the run, and your
  Chief of Staff session stays free: you grill, file, triage and discuss there while the batch
  runs.
- **`docs/use-cases-direct.md`** covers the same situations for direct mode, from
  chief-of-staff.md "Steering a batch yourself":
  - What it is: no Foreman session; the Chief of Staff starts the Drivers on the free slots and
    steers the batch from your session, with the same limits (slots, budget, rounds), folders,
    `STATUS.md`, reports, costs and boundaries.
  - **Less dynamic than Foreman mode, with the same lifecycle:** running, paused, closed on your
    word, exactly as in Foreman mode (the batch lifecycle diagram applies as is). While it runs
    the batch is strict: no CR joins it (`order add` and `order qa` are refused), except a release
    CR and its fixes; once paused it takes new CRs, which set it running again.
  - **No grill in the same session:** while the batch runs, the Chief of Staff answers only
    "status?", "what did it cost?", your answers to a blocked CR of the batch and orders on the
    batch ("I merged #42", "drop CR-140", "stop the batch", more rounds, slots or budget); any
    other request is noted word for word and handed back when the batch completes; an idea is
    filed in the inbox at once, without a grill. To grill meanwhile, open another session
    yourself on the same repository: there, a Chief of Staff grills, files, specifies and
    prioritises your own ideas into the backlog, beside the batch. Those CRs join the batch
    through the steering session once it is paused (you say so there; it runs `order add`), or
    wait for the next batch.
  - Where it runs and the preflight (`preflight --direct`), the heartbeat in your own session,
    the cost (`Chief of Staff (steering)`, in the budget), `close` (it counts only your Drivers'
    session files as running, not your own), switching to Foreman mode on your word (only where
    a Foreman can start; a Foreman batch never switches back), the release in direct mode (a
    release CR joins a running direct batch; its PR is merged by the steering session on your
    approval or grant), and "On GitHub Copilot".
  - Unproved paths stay marked as the host references mark them ("not yet proved").
- Every link to `docs/use-cases.md` (README, tutorial) still resolves; links to sections that
  moved are updated.

### 5. The tutorial (`docs/tutorial-claude-code.md`)

It stays a Foreman-mode walk in the Desktop app, corrected:

- "You need": the Desktop app is needed for Foreman mode; in a terminal or VS Code the plan
  proposes direct mode instead (link `use-cases-direct.md`); "refuses to start a batch, on
  purpose" goes.
- Step 1: "ten agents" becomes twelve (`agents/` holds twelve files today: coder,
  conflict-resolver, cr-driver, debugger, demo-explorer, inspector, investigator, qa-driver,
  release-driver, spec-writer, stack-driver, verifier); count them again at implementation.
- Step 3: add "init" (`/chantier:chantier init`): the folders and a guided tour.
- Step 4: the grill, the restatement and "grilled enough?", then the spec-writer writes
  `03-change-spec.md` in the background; the Chief of Staff shows it to you after checking it
  against your answers.
- Step 5: the plan names who steers (Foreman mode by default); the direct-mode sentence adds that
  direct mode is less dynamic, has the same lifecycle, and holds no grill in that session.
- Step 7: the PR description follows the default template unless your project has one. The
  pause and close text already matches ac5e453; check it says "paused" and "close the batch".
- Step 8: the spec-writer runs on Opus 5.5 (README Models table).
- "If something goes wrong", first bullet: in the terminal or VS Code, Foreman mode is refused;
  say so and that direct mode is offered there.

### 6. The SVGs are approved before the CR starts

The user reviews the new and changed SVGs before the CR starts, not before its PR (the user's
word, replacing the earlier stop before the PR). The SVGs concerned are the new
`docs/batch-lifecycle.svg` and the changed `docs/how-chantier-works.svg`,
`docs/how-chantier-works-simple.svg`, `docs/cr-lifecycle.svg`, `docs/cr-lifecycle-simple.svg`,
and `docs/cr-folder-lifecycle.svg` if a text of it is made false; `docs/batch-pace.svg` is not
among them (untouched).

- Before the CR starts, the Chief of Staff has them prototyped in a temporary folder, from
  sections 1 and 2 above, shows them rendered to the user, and the user's corrections go into
  this specification.
- The approved SVGs are the reference the Driver delivers:
  the five approved prototypes are in this CR's `work/approved-svgs/` (`batch-lifecycle`,
  `how-chantier-works`, `how-chantier-works-simple`, `cr-lifecycle`, `cr-lifecycle-simple`, each
  as `.svg` with its rendered `.png`), approved by the user on 2026-11-07 as they are;
  `cr-folder-lifecycle.svg` stays unchanged.
- The Driver puts each approved SVG in `docs/` under its name, changing it only where a text
  must match its `-texts.md` companion or a fact of the sources above, and says so in a `note`.
  The companions are written from the delivered SVGs. Where this section and sections 1 and 2
  differ, the approved prototypes win.
- The Driver then opens the PR as usual: no stop for a review of the SVGs before it.
## Out of scope

- Any change to the cards, `SKILL.md`, the agent files, the CLI, the scenario, the tests, the
  board mod or `evals/`.
- `docs/batch-pace.svg`, left as it is (the user's word).
- New behaviour: the docs describe only what `main` does.
- A Copilot tutorial.

## Evidence

Run at the pushed head, outputs in the Verifier's evidence:

1. `just check` passes (the project's gate; AGENTS.md: a docs-only change needs no
   `just scenario`).
2. Each SVG in `docs/` parses as XML: `uv run --no-project python -c "import glob,
   xml.etree.ElementTree as E; [E.parse(f) for f in glob.glob('docs/*.svg')]; print('ok')"`.
3. Companions in step: a short script (in the CR's `work/`, not committed) that, for each SVG
   with a `-texts.md` (now including `how-chantier-works-simple` and `batch-lifecycle`), prints
   the `<desc>` against the companion's first paragraph (equal) and each drawn text (the joined
   text of each `<text>`) not found in the companion, after removing Markdown markers (`#`, `**`,
   backticks). The output shows no difference, or only differences the Verifier judges as
   markup. Every SVG in `docs/` except `batch-pace.svg` has a companion.
4. Words: `git grep -n -i -E "\bland(ed|s|ing)?\b|epoch" -- README.md docs/` returns nothing
   about a batch (a CR "lands in one Markdown file" in `cr-lifecycle` is not a batch and may
   stay).
5. Links: every relative link and image in `README.md` and `docs/*.md` resolves to a file in the
   repository (a short command or script, output kept).
6. Content checks, by grep with output: `README.md` names `docs/how-chantier-works-simple.svg`
   and does not name `docs/batch-lifecycle.svg`; `docs/use-cases-foreman.md` and
   `docs/use-cases-direct.md` exist and `docs/use-cases.md` links both; `use-cases-direct.md`
   says "same lifecycle", that the batch is strict while running, and that the user opens another
   session to grill; `how-chantier-works.svg` names direct mode and the spec-writer;
   `how-chantier-works-simple.svg` names direct mode; `cr-lifecycle.svg` and
   `cr-lifecycle-simple.svg` no longer say the Chief of Staff writes the spec;
   `git diff --stat main -- docs/batch-pace.svg` is empty.
7. Each delivered SVG matches its approved prototype: for each, a `diff` (or `fc /n` on Windows)
   between the approved prototype and `docs/<name>.svg`, output kept; any difference is one the
   Driver's `note` names and explains.
