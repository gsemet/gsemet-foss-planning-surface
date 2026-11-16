# Intent: a planning server owned by the Chief of Staff

2026-11-10, the user, after a study of Beads and similar tools (in a Chief of Staff side session).
A follow-up of `planning-repo` (P1, the external planning surface), to take up after it; it does
not replace it. Related: `remote-board` (inbox, a read-only progress board) and
`planning-surface-positioning` (P1).

## What the user wants

- **An external planning surface for real use.** The user's words: putting the plan in the
  project hits its limits very fast; an external planning surface is needed, even if heavier.
- **One writer: the Chief of Staff.** In chantier the only writer is the Chief of Staff, Grillers
  included. It can therefore be the guarantor of a server that does the writes, the push and the
  rebase of the surface, and serves the ticket tracking.
- **One Chief of Staff per project**, several projects in one surface repository
  (`projects/<name>/`, as in `planning-repo`).
- **The CLI does the persistence**, the sync of the surface included. The agents still do git and
  the forge on the project's code.
- **Multi-session** (Chief of Staff, Grillers, the Foreman and its Drivers), on several hosts.
- **Generic:** a GitHub PR or a GitLab MR; Claude Code, Codex, GitLab Duo, Copilot.
- **Configuration:** the "no setup" rule holds for the target project only. The external surface
  may take a YAML/JSON configuration. Coding rules stay in each project's `AGENTS.md`.
- **Minor outside contributions without chantier:** someone must be able to contribute to a
  project without chantier. It would be good if the contribution still ended as a report in the
  archives.

## The study (2026-11-10), for the grill

- **Beads** (`gastownhall/beads`, MIT; v1.0 in April 2026, 1.3.x by Sept. 2026):
  - A Go binary, `bd`, on a Dolt database in `.beads/`. Embedded mode has one writer; several
    writers need a `dolt sql-server`.
  - `issues.jsonl` is only an export. The sync is `bd dolt push/pull` to `refs/dolt/data` on the
    git remote.
  - Fields: description, design, acceptance, notes, `--spec-id`, metadata, external-ref. Priority
    0-4. Statuses open/in_progress/blocked/deferred/closed. Dependencies blocks/parent-child/related.
  - `bd ready`; `--claim`; `heartbeat`/`reclaim` leases.
  - Gates `human`, `gh:pr`, `gh:run`, `timer`; `merge-slot`.
  - Contributor routing to a separate planning repo; `bd repo sync`; `bd github sync`;
    `beads-mcp`.
- **Mapping to chantier:** CR = bead; intent/spec/answers = description/design+acceptance/comments;
  P1-P4 = priority; `depends.json` = `blocks`; `take`'s rule = `bd ready`; slot = claim; ask =
  human gate; merged/dropped = closed.
  - Nothing in Beads holds chantier's budget, rounds, cost, Foreman epochs, STATUS or stack: that
    frame stays chantier's.
- **Main blocker, the user's word: upstream churn.**
  - The storage changed (JSONL, then Dolt) and the repository moved (steveyegge, then
    gastownhall).
  - v1.2.2 was a recovery release that re-shipped v1.1.2, with a data-downgrade risk.
  - Yegge abandoned Gas Town and reusable harnesses (August 2026, "The Shape of Things to Come").
    He runs a private harness, Wheelhouse, but keeps Beads as his work ledger, on a shared Dolt
    server.
  - His thesis: share the primitives (task graph, worker protocol); keep roles, lifecycle and
    "done" in the project.
- **Leaning:**
  - Do not depend on Beads as the store.
  - Keep the storage behind the CLI, so a backend (the git surface, a server, Beads someday) can
    be swapped.
  - Borrow its model where it pays.
- Others seen: Backlog.md (one Markdown file per task, MCP); tbd (a dedicated sync branch);
  Gas City (Gas Town as an SDK); SupSpec, DevFleet, `stacked-mr`, `gh-stack` (spec DAG to PRs,
  stacks).

## Points for the grill

1. **The writer is a CLI process; the Chief of Staff is its guarantor.** The Chief of Staff starts
   and owns a `chantier serve`, standard library only. It applies the writes, commits, rebases and
   pushes the surface, and exposes the tracking over HTTP/MCP. `seat.json` names who guarantees it
   and where it is reached. The Chief of Staff's LLM stays on the path of decisions (orders), not
   of writes: a hand-back or a Griller's answer must not wait for its turn.
2. **`$CHANTIER` as a thin client** once a surface is configured: the same commands, the write
   sent to the server.
   - With the server down, the write is refused, with no fallback.
   - Today Grillers, the Foreman and the Drivers write through the CLI themselves
     (`griller.md`: `file`, `triage`, `01-intent.md`, `02-answers.md`).
   - With no surface configured, the in-project mode is unchanged.
3. **Lifetime:** a chat session is not a daemon. What happens when the Chief of Staff's session
   ends or compacts, and who restarts the server.
4. **Reach:** one machine (localhost) first; then a team (several machines, authentication), where
   the guarantor is a role, not a laptop.
5. **Several Chiefs of Staff push one surface repository** (one per project): commits touch
   separate `projects/<name>/` sub-trees, so a rebase is trivial. To check against
   `planning-repo`'s obsidian-git autosync.
6. **What is committed:** the append-only `events.jsonl` and the Markdown people write. The
   STATUS files are derived: regenerated after a pull, never merged.
7. **Leases** (`heartbeat`/`reclaim`), worth taking (the user): replace the "session file written
   in the last 5 minutes" heuristic, for Drivers and for the server itself.
8. **Gates**, lower priority: a CR records what it waits for, typed by the fact, never by the forge
   (a human answer, a merged review request, a green pipeline). Any agent on any host can then
   ask what blocks a CR.
9. **An archive report for a PR/MR merged outside chantier**, built from the forge (title, link,
   author, what changed). To square with `planning-repo`, where outside CRs come through a PR on
   the surface.
10. **Beads as an optional backend or bridge** (export of `ready` and claims, intake from
    `bd ready --json`): only on a measured need.

## Rejected

- **Hash IDs** (the user): the slug and the number are enough, and they stay sorted.

## Constraint from `remote-board` (CR-182, 2026-11-11)

One HTTP server per planning folder: any page this item adds goes into `chantier board`; it
takes the board's start and stop rule (tied to the seat) or replaces it for both, never a second
rule beside it; any authentication is added to the board's server.
