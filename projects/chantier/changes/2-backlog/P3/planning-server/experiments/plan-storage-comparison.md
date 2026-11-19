# Study: Beads, Gas Town and chantier (2026-11-10)

Written in a Chief of Staff side session while studying Beads for the external planning surface.
Sources at the end.

- **Beads** facts come from its README, `docs/CLI_REFERENCE.md` and `docs/multi-agent/`.
- **Gas Town** rows partly rest on third-party guides; they are marked where they do.
- The **"chantier, studied"** column is the design of `planning-repo` (P1) and of this CR, not a
  built feature. Its open points are in `01-intent.md`.

## 1. Overview

| | Beads | Gas Town | chantier |
|---|---|---|---|
| What it is | Issue tracker for agents | Multi-agent orchestrator | Change-request workflow, one PR or MR per change |
| Where the plan lives | Dolt database in `.beads/` | Beads | Markdown and JSON folders in the repo |
| Sync across machines | Built in: `bd dolt push` and `pull` through the git remote | Through Beads | 🚧 CRs travel with git like any file, or stay uncommitted. Being rethought |
| Ready work | `bd ready`, claims, leases | The Mayor dispatches to workers (third-party guides) | A CR starts once what it depends on is ready |
| Who does the work | Any agent | Short-lived workers under a coordinator | Chief of Staff, Foreman, one Driver per CR, short-lived workers |
| Guardrails | Not its scope | A watcher on worker health (third-party guides) | Dollar budget, review rounds and slots, enforced by the CLI |
| Merging | Not its scope | Merge queue rebases, tests and merges | A human merges; PRs can be stacked |
| Project rules | Agent instructions point to `bd` | Roles defined by the harness | The project's `AGENTS.md` ranks above chantier |

## 2. Storing and syncing the plan

The user's version (2026-11-10), which replaces the first draft.

| | Beads | chantier today | 🚧 chantier, studied |
|---|---|---|---|
| **Where, on disk** | `.beads/` inside the project's repository | `.agents/changes/` inside the project's main checkout | Outside the project: a planning repository, `projects/<name>/changes/` |
| **Where, on the remote** | The project's own remote, on a hidden ref (`refs/dolt/data`): not main, not a branch. GitHub or another forge cannot display its content. | Nowhere unless committed, then on the project's branch like any file | The planning repository's main branch, its own history, apart from the code |
| **Where finished work ends** | Closed issues stay in the same database | `4-archives/` in the same folder | Back in the project's repository, inside the CR's own PR |
| Format | Dolt SQL database; `issues.jsonl` as an export only | One folder per CR: Markdown, plus JSON state written by the CLI | Same folders; append-only events as additional Markdown and JSON files |
| Who writes | Any agent or person running `bd`; one writer per database unless a Dolt server runs | Every chantier session on the machine, through the CLI, under a file lock | One writer per project: a CLI server whose guarantor is the Chief of Staff. The other sessions talk to the Chief of Staff's session. |
| Who reads | Anyone with the repo and `bd`; MCP server; not on the forge | Sessions on that machine; others only if the folder is committed | Anyone with access to the planning repo; the files are directly readable on the forge |
| When it syncs | Local commit on each write; push at session end or from git hooks | Never on its own | After each write, within 5 minutes at most |
| Who syncs | Each agent or person, with `bd dolt push` and `pull` | Nobody by design: the CLI runs no git write | The CLI server: commit, rebase, push. Conflicts are raised to the Chief of Staff for an automated resolution. |
| Conflicts | Dolt merges cell by cell | A lock on one machine; plain git conflicts across machines | If two sessions have not synced and both try to push, the Chief of Staff resolves to its best guess or asks the user. |
| Outside contributors | Contributor mode routes their issues to a private planning repo | A PR on the project | A CR through a PR on the planning repo; a small code PR without chantier, archived afterwards |
| Setup | Install `bd`, then `bd init` | None | To be defined |

## 3. Where the plan goes on the remote: the options

| Option | Seen in | Browsable on the forge | Touches the code's `main` |
|---|---|---|---|
| Committed with the code, on the current branch | Beads before Dolt (`issues.jsonl`); chantier today if committed | Yes | Yes: conflicts with a protected `main` |
| A dedicated branch in the project's repo | tbd (`tbd-sync`); Beads' former "sync branch" mode (doc not read) | Yes, on that branch | No |
| A hidden ref in the project's repo | Beads now (`refs/dolt/data`) | No | No |
| A separate planning repository | Beads contributor mode (`~/.beads-planning`); chantier `planning-repo` | Yes | No |

The user's ruling (2026-11-10, `02-answers.md`): everything in Markdown, browsable on the forge.
A dedicated branch is acceptable; a separate planning project is better. A hidden ref is ruled out.

## 4. Yegge and the upstream (August 2026)

- Beads reached v1.0 in April 2026 and 1.3.x by Sept. 2026. v1.2.2 was a recovery release that
  re-shipped v1.1.2, with a data-downgrade risk.
- Yegge stepped back from Gas Town and from reusable harnesses ("The Shape of Things to Come",
  August 2026; read through third-party summaries). He runs a private harness, Wheelhouse, and
  keeps Beads as his ledger, on a shared Dolt server.
- Gas City (Gas Town rebuilt as an SDK by Chris Sells and Julian Knutsen) carries on, with Beads.

## 5. Vercel Board (added 2026-11-19)

Vercel announced Board on 2026-11-18 as an experimental primitive: a message store for agents,
used through a CLI (`vercel board`) and a JavaScript SDK (`@vercel/board`). This section rests on
the announcement only; its docs were not read.

| | Vercel Board | 🚧 chantier, studied |
|---|---|---|
| What it is | A message store: boards, channels nested by path, threads; tasks with labels | Change requests as Markdown and JSON folders |
| Where the plan lives | A hosted store; the post does not say which backend. Not in git | A planning repository, or a dedicated branch, in Markdown |
| Browsable on the forge | No; a local viewer (`npx @vercel/board inspect`) | Yes |
| Structured data | Messages validated against a registered schema (for example `security-finding@1`) | JSON state written by the CLI |
| Sync | Two-way with Slack and GitHub issues and pulls, through Vercel connectors | The CLI commits, rebases and pushes |
| Who writes | Any agent or person with a grant, through the CLI or the SDK | One writer per project: the Chief of Staff |
| Ready work | `tasks claim --ready`, with a lease renewed by `tasks renew --lease` | A CR starts once what it depends on is ready; leases judged worth taking |
| Dependencies | Between tasks; a review task opens once its fix is done | `depends.json` |
| Waking agents | Watchers run agent code on a new event or a label change; agents schedule their own follow-ups (`vercel board schedule … --in 5m`) | The Foreman and the Drivers poll or are told by the CLI |
| Access | Grants per user, project and environment (read, post, all), audited per event | The rights of the repository |
| Guardrails | Leases and grants; no budget, round or concurrency limit mentioned | Dollar budget, review rounds and slots |
| Merging | Humans review in the thread; Vercel says its v0 factory merges over half its PRs | A human merges; PRs can be stacked |
| Hosts | Claude Code, Codex, Pi, OpenCode and others named; GitHub only; no MCP mentioned | Claude Code and Copilot today; generic GitHub/GitLab wanted |

What it means for this CR:

- **The same direction, from a large vendor:** a shared, multi-agent backlog outside the code,
  with claims, leases and dependencies. It confirms the need behind `planning-server`.
- **The storage is the opposite choice:** a hosted store with no git and no forge view, tied to
  Vercel. It fails the user's rule that the plan is Markdown browsable on the forge, as Beads' Dolt
  store does.
- **Worth noting:** typed messages with a versioned schema; watchers that wake an agent on an event
  instead of polling; per-project grants with an explanation of the effective access
  (`grants explain`); self-scheduled follow-ups to check CI.
- **Upstream risk:** experimental and new; the same reason that keeps Beads out applies.

## 6. Vercel Board, from its docs (2026-11-20)

Read by a Griller on 2026-11-20: the announcement and `vercel.com/docs/board` (overview,
`cli-reference`, `sdk` for `@vercel/board` 0.50.0, `access`). The npm page answered 403; no source
repository is linked. It corrects section 5 where they differ (GitHub sync is one-way into the board; Linear, the local
SQLite mode and the licence were missing). A sibling Griller's fuller study, with the source code
read: [vercel-board-study.md](vercel-board-study.md).

| chantier's constraint | What Board offers | Verdict |
|---|---|---|
| The plan is Markdown browsable on GitHub or GitLab | A hosted store (United States only); messages hold Markdown text, but there is no export to files or git; only attachments download | Fails |
| No setup beyond `uv` | A Vercel account and team, `vercel login` or a `BOARD_TOKEN`; the Vercel CLI from npm; the SDK needs Node.js 22.18+ | Fails |
| Offline once cached | Hosted by default; a local mode (`vb serve`, one process, one SQLite file per board in `.board/` at the git root, kept out of git); custom backends through a `Backend` interface checked by `vb conformance` | Possible, but still a database, not files |
| Windows, macOS, Linux | Not stated | Untested |
| Claude Code and Copilot hosts | Claude Code, Codex, Cursor, Pi and others named; Copilot never; JavaScript SDK only, no documented REST API, no MCP server | Copilot missing; a Python CLI would shell out to Node |
| GitHub and GitLab | GitHub sync, one way into a channel per the SDK docs (the post says two-way); GitLab never mentioned; Slack and Linear both ways | GitLab missing |
| One writer per project | Any principal with a grant writes; grants per user, project, environment, app (`read`, `post`, `react`, `label`, `sync`, `manage`, `all`), `grants explain` | Wider than needed; grants are a good idea |
| Budgets, rounds, slots | None; rate limits per login, unnumbered | Stays chantier's |
| Ready work, leases | `tasks claim --ready --wait`, leases up to 5 minutes renewed, `tasks needs` for dependencies, `block`, `fail`, `reopen` | Close to the CR's leases (point 7) |
| Waking agents | Watchers (up to 32 per deployment) run code on events; `schedule --in/--at/--every`, 1 minute at the shortest; turn-end hooks for Claude Code | chantier 0.14.0 already has its watcher and addressed journal |
| Typed data | Versioned JSON Schemas `name@N`, never changed once published | Worth borrowing for the journal's lines |
| Stability, price, licence | "Experimental. Behavior, APIs, and limits may change"; SDK 0.53.0 after ten releases in a week; free while experimental, may be charged later; Public Beta Agreement; Apache-2.0 for the client, CLI and local backend, the hosted backend closed | Same churn risk as Beads, worse for the hosted mode |

Since section 5, chantier 0.14.0 shipped what this CR first meant by "a server": one elected
surface server per planning surface (the board and the forge hub, `chantier/server.json`) and an
addressed, typed event journal (`forge-journal.jsonl`) read by each session's watcher. What
remains of this CR is the single writer that commits, rebases and pushes the surface, leases, and
gates.

## Sources

- https://github.com/gastownhall/beads
- https://raw.githubusercontent.com/gastownhall/beads/main/docs/CLI_REFERENCE.md
- https://raw.githubusercontent.com/gastownhall/beads/main/docs/multi-agent/coordination.md
- https://raw.githubusercontent.com/gastownhall/beads/main/docs/multi-agent/routing.md
- https://github.com/jlevy/tbd/wiki
- https://blog.gascity.com/authors/steve/
- https://vanja.io/yegge-agent-city-four-claims/
- https://www.developersdigest.tech/blog/yegge-continuous-thunderdome
- https://newreleases.io/project/github/gastownhall/beads/release/v1.3.0-rc.1
- https://codex.danielvaughan.com/2026/04/08/gas-town-multi-agent-factory/
- https://vercel.com/blog/introducing-vercel-board
- https://vercel.com/docs/board
- https://vercel.com/docs/board/cli-reference
- https://vercel.com/docs/board/sdk
- https://vercel.com/docs/board/access
