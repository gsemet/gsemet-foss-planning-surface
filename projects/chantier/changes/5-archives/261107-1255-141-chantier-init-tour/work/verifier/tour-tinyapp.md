### chantier, in one sentence

- **close:** closes a finished batch, on your yes.

You give your requests to one counterpart, and a team of agents carries them out: each change
becomes a pull request. Three things stay yours: what to do, when to start, what to merge.

### The story of one request

Let us follow a real gap in tinyapp: the README promises `tinyapp --version`, but nothing in
`src/tinyapp/cli.py` handles it, and `just test` does not cover it.

1. **You tell the Chief of Staff**, the chief of cabinet: it listens and never codes. "File
   this": it becomes a **Change Request (CR)**, a folder in `.agents/changes/1-inbox/`.
2. **It grills you:** a few questions, each with its recommended answer ("read the version from
   `pyproject.toml`, or hard-code it?"). Your answers become the **specification**: what the CR
   changes, and nothing more.
3. **You prioritize it** ("make it a P1"): it moves to `2-backlog/P1/`.
4. **You say "run the P1s".** It shows the plan and waits for your go. Then it opens a
   **batch**, the CRs started together (`batch-01`), and starts the **Foreman**, the site
   foreman: another session that spreads the work without laying a single brick.
   Where the host cannot start a Foreman session, or for a small batch, the Chief of Staff
   steers the batch itself in **direct mode**: it starts the Drivers and holds no grill or
   discussion until the batch completes. The plan names it, and your go approves it.
5. **A Driver**, the team lead, takes the CR in a free **slot**. It creates the branch
   `chantier/batch-01/101-version-flag` and its worktree beside the repository. Then come the
   **rounds**: the **Coder** writes, the **Inspector** reviews without having written, three
   times at most.
6. The Driver runs the long gate (`just test`), pushes, opens the PR and reads the CI. The
   **Verifier**, who wrote nothing, proves on the pushed code that the specification holds.
   The CR is **ready**.
7. **You review and merge:** chantier never merges your PRs. You say "I merged #12" and the
   folder moves to `4-archives/`.

```text
you <-> Chief of Staff --orders--> Foreman --> Driver (one per CR) --> Coder . Inspector . Verifier
              ^                      | questions     | CR done
              +------ reports <------+<--------------+
   (direct mode: the Chief of Staff starts the Drivers itself, no Foreman)
```

```text
1-inbox -priority-> 2-backlog/P1..P4 -launch-> 3-requests/batch-01 -your merge-> 4-archives
   +------------------------- drop ------------------------------------------> 5-trash
```

```text
Coder -> Inspector x -> Coder -> Inspector ok -> long gate -> PR -> CI -> Verifier -> ready -> your merge
```

### What you will read

```text
.agents/changes/3-requests/batch-01/101-version-flag/
|-- intake/request.md    your request, as is
|-- 01-intent.md         summarized and analyzed
|-- 02-answers.md        your answers
|-- 03-change-spec.md    the specification
`-- work/                notes, gate logs, PR text
```

"status?":

| CR | State | PR | Spend |
|---|---|---|---|
| CR-101 version flag | working, round 2 of 3 | - | $... |

### Money and your decisions

- **Budget:** a dollar ceiling for the team. Once reached, no further Driver starts.
- **Slots:** CRs running at once (4 by default). **Rounds:** retries per CR (3 by default).
- **Yours alone:** prioritize, say go, merge, publish a release, raise a limit.
- "What did it cost?" gives the measured detail.

### Getting started here

- **Gate:** tinyapp has a `justfile` with `test`, no lint and no CI workflow. Missing, a Driver
  cannot know what "green" means and the long gate is a guess. Proposed `AGENTS.md` text:
  "Run `just test` before handing back." Written only on your yes. The merge method and commit convention are unwritten too; I can
  propose their lines next.
- **CI:** none, so the Driver reads nothing after the push. I can file a CR in the inbox to add
  one, only on your yes.
- **`.gitignore`:** `.agents/` is neither tracked nor ignored. Add `.agents/changes/` yourself:
  your `main` stays clean, and the CRs stay on your machine.
- **Example CR:** `tinyapp --version`. Shall I file it in the inbox?

**Phrases to say:** "file this: ...", "make it a P1", "run the P1s", "status?", "drop CR-101",
"I merged #12", "what did it cost?".

**Glossary:**
- **Stack:** the PRs of a batch piled on one another.
- **Fast gate:** the quick check after each round.
- **Long gate:** the full suite, once before the PR. **Investigator:** maps the code first.
- **Debugger:** finds why a check is red.
- **Conflict resolver:** rebases and resolves conflicts.
- **Release CR:** publishes what is merged, per the project's procedure.
- **Grant:** what you allow for a release unasked. **STATUS.md:** the batch's state, kept by the CLI.
- **close:** closes a finished batch, on your yes.
