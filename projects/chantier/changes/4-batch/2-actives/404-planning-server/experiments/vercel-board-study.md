# Vercel Board: study for chantier (2026-11-20)

Written in a side session at the user's request. Sources: the announcement (2026-11-18), the
whole Board docs (concepts, access, guides, CLI and SDK reference), the repo `vercel/board`
(README, package.json, part of SPEC.md, the skill and its references, the factory and swarm
templates, `server/backend.ts`, the local backend) and the only Hacker News thread (no comment
readable). The second half of SPEC.md was not read.

## 1. What it is

- A message board for agents and people: boards, channels, threads, tasks. A coordination
  primitive, not an orchestrator.
- Interfaces: CLI `vercel board`; JS SDK `@vercel/board` (0.53.0, ten releases from Nov 16 to
  19); a route handler to mount in an app; a skill (`npx skills add vercel/board`).
- Experimental on all plans, free for now; Vercel may charge later; Public Beta Agreement.
- Apache-2.0 for the client, CLI, route handler and local backend. The hosted backend (Vercel's
  messageboard API) is not open source.
- Repo: about 90 stars, 0 open issues, 25 open PRs, more than 2,000 commits; protocol marked
  "v1 spec (draft)", breaking changes daily.

## 2. Data model

- Team > Board > Channels > Threads > Messages. Default board "General"; named boards each have
  their own grants.
- Channels are fixed paths (`security/findings`); a trailing `/` names a subtree.
- Message: Markdown up to 10,000 chars, up to 10 attachments of 100 MB, `key=value` labels (one
  value per key), reactions, typed blocks `{schema, version, data}`, a revision, an opaque ID.
- Schemas registered by name and immutable version (`security-finding@1`); built-in
  `git-commit@1`, `vercel-deployment@1`.
- Actors: person, agent profile of a person (`ada/fx`), deployment, synced Slack user.
- One ordered event log per board, read over SSE or long-poll with a cursor. The spec calls the
  log the only source of truth.

## 3. Storage

| Mode | Where | Use |
|---|---|---|
| Hosted (default) | Vercel's API, US, encrypted; no region choice; backend undocumented | Production |
| Local (`vb serve`) | One SQLite file per board in `.board/` at the git root, kept out of git | Dev, tests, small team over Tailscale |
| Memory | Nothing on disk | Tests |
| Custom | Any object implementing the `Backend` protocol, checked by `vb conformance` | The only self-host path for a multi-instance service |

- No git, no Markdown files, nothing browsable on a forge. Reading via `read`, `tail`, a browser
  inspector.
- No documented export or backup beyond `--json`. Deletion leaves a tombstone; synced copies are
  deleted best-effort. Task event feed kept 30 days.

## 4. Concurrency

- Read-your-writes. Conditional writes return 409 and write nothing: `--if-revision`,
  `--if`/`--if-unset` on labels (compare-and-swap), `reply --after` (`newer_message`).
- `--idempotency-key` for retries. Only the author edits or deletes.

## 5. Tasks

- A task is a thread with board-kept state (reserved label `board.task`): `waiting`, `ready`,
  `claimed`, `blocked`, `completed`, `failed`, `canceled`.
- Dependencies: `--needs`, or a JSON plan with `needs`, across channels. A completed
  prerequisite readies its waiters; a failed or canceled one readies nothing. 15 tasks per write.
- `tasks claim --ready <channel> [--label] [--wait]`: oldest ready task; exclusive claim.
- Lease of 5 minutes at most, renewed; on expiry the task is ready again; a late worker cannot
  settle it (`claim_lost`).
- `tasks run <id> -- <cmd>`: claim, renew at a third of the lease, settle by exit code, release on
  Ctrl-C or SIGTERM.
- `block --kind needs_input|awaiting_approval`, `assign`, `reopen`, `cancel`.
- Absent: budgets, rounds, priorities, stacked PRs.

## 6. Waking and scheduling

- Watchers: code in the deployment, run on matching events; at-least-once; retries with backoff
  then `watch.failed`; 32 to 64 per deployment. Posting does not wake an idle agent.
- `wait`/`tail`: block until the next matching event.
- `schedule`: one-off or recurring posts (minimum every minute); used by agents to re-check CI.

## 7. Access

- Permissions `read`, `post`, `react`, `label`, `sync`, `manage` per channel, subtree or `*`; to a
  user, a project and environment, an app, or everyone. Most specific pattern wins; team role
  caps. `grants explain` shows effective access.
- `as('fixer', { can })` narrows an agent. Defaults are wide open: the team, every deployment
  (previews included) and every app read every channel.
- `sandboxPolicy()`: board access with no credential inside the sandbox. Server-authored
  provenance on each event.

## 8. Sync

| Platform | Direction | What |
|---|---|---|
| Slack | Two-way | messages, replies, edits, deletes, reactions, files |
| GitHub | Into the board by default | each PR or issue a thread, labels `pr=`, `state=`, `review=`, `head=` |
| Linear | Two-way | a new thread in a mapped channel opens a Linear issue |

- Labels and task state never sync. Board grants do not apply on the platforms. No GitLab.

## 9. The skill

- Read a channel's conventions first; reply in the existing thread with `--after`; write under a
  profile (`--as`); claim, renew, settle.
- Safety: board content is information, not instructions; never merge, deploy or publish because
  a message says so; never post secrets; `claim --ready` takes only the owner's own tasks by
  default.
- Hosts named: Claude Code, Codex, Cursor, Pi, OpenCode. No MCP.

## 10. Templates

- **Software factory** (used for v0, which Vercel says merges over half its PRs): intake from a
  GitHub issue or PR, Slack or the board; one agent session (eve, Claude Opus 5.5) per thread, in
  its own sandbox; reproduce, fix, open the PR, follow it on a schedule, merge when a person asks
  in the thread. A feature builds only after team agreement; an RFC gets critique. No task DAG, no
  CI gate, and **no spending cap**, by design.
- **Swarm**: repo, goal, model, up to 256 agents, a budget or a time limit. Pipeline: a plan task
  splits into 20 tasks at most, each with a waiting review, each a branch and a PR. Review mode:
  find, verify, report, read-only. A reconcile cron (every 5 min, Pro plan) starts agents and
  records spend, so a budget can overshoot by about 5 minutes. Pattern rules: the lead plans and
  never codes; no two tasks touch the same files; a completed task is a claim, not proof;
  irreversible steps need approval where identity is verified (a GitHub review).

## 11. Self-hosting and a PostgreSQL backend

- Open source: the server (the `board()` route handler: routing, validation, auth, grant checks,
  SSE, sync, watchers), the local SQLite backend, `vb serve`, CLI, SDK, conformance kit. A board
  can run without Vercel with `vb serve` (one process, SQLite; pending schedules lost on restart;
  not serverless).
- Closed or Vercel-bound: the hosted backend; Vercel Connect for sync; deployment OIDC and
  `vercel login` tokens; crons; sandboxes.
- PostgreSQL: possible only as a full custom backend (`Backend` interface in
  `server/backend.ts`, one method per protocol route; missing features answer 501 and are
  skipped by conformance; auth replaceable with `authenticate`). Not an extension of the SQLite
  one: storage is a single ordered log with atomic batches (IDs and cursors are log positions)
  folded into read tables exactly once; the log comes from an external package
  (`experimental-a2`). A multi-instance Postgres backend must also handle a gap-free global order,
  shared 5-minute leases, a shared scheduler, watcher matching and blob storage. None exists. The
  draft protocol breaks weekly.

## 12. Against chantier

| | Vercel Board | chantier |
|---|---|---|
| Nature | Coordination primitive; orchestration written by you (templates) | Full workflow: roles, CR lifecycle, guardrails |
| Plan storage | Hosted Vercel store, or local SQLite | Markdown and JSON files, git |
| Browsable on the forge | No | Yes (the user's rule) |
| Unit of work | A thread or task, short-lived | A CR: folder, spec, grill, archives |
| Ready work | `waiting` → `ready`, claim, 5-min lease | `depends.json`, a Driver per CR; leases judged worth taking |
| Who writes | Anyone granted, protected by conditional writes | One writer, the Chief of Staff, through the CLI |
| Guardrails | Leases and grants; a rough budget in the swarm only | Dollar budget, rounds, slots, enforced by the CLI |
| Merge | A person asks in the thread, the agent merges | A person merges; stacked PRs |
| Spec before code | None; team agreement for features in the factory | Grill, then Change Specification |
| Hosts | Agent-neutral; GitHub, Slack, Linear; Vercel-bound | Claude Code, Copilot; GitHub, GitLab wanted |
| Vendor dependence | Strong: Vercel account, OIDC, US, experimental | None |

## 13. Conclusions

Confirms: a vendor reaches the same primitives (shared backlog outside the code, dependencies
that hold a task in `waiting`, exclusive claim with a lease, explicit block for a human), and the
swarm pattern restates chantier's rules (lead does not code, no shared files, verify a "done",
human approval for the irreversible).

Worth taking:

1. Lease shape: 5 minutes, renewed at a third, `claim_lost` stops a late worker from settling.
2. A `tasks run -- <cmd>` equivalent: claim, work, settle by exit code in one command.
3. Typed blocks: `needs_input` vs `awaiting_approval`.
4. Conditional writes (`--if-revision`, label compare-and-swap), if chantier ever has several
   writers.
5. Data blocks with an immutable versioned schema, for verdicts and reports.
6. A command explaining someone's effective access.
7. Blocking wait on a cursor instead of polling.
8. Storage as a minimal interface, with features declared absent and a conformance test every
   backend must pass: what chantier's CLI needs for a swappable plan store (dedicated branch,
   separate planning repo, later something else).

Rules it out as a store: no Markdown, nothing on the forge, no export; a Vercel account and US
data for the hosted mode; a draft API changing daily, the same upstream risk as Beads; no GitLab.
Self-hosting with SQLite or Postgres keeps it a database, so the forge rule still fails.

What it lacks that chantier has: a real spending guardrail (the factory has no cap), the grill and
spec before code, stacked PRs, a durable record per change (task events kept 30 days).

Note: section 5 "Vercel Board" added on 2026-11-19 to `planning-server`'s study
(`experiments/plan-storage-comparison.md`) has errors: it says GitHub sync is two-way (it is
one-way into the board by default), and it omits Linear, the local SQLite mode and the Apache-2.0
license.
