# Answers: forge-connectors

The request comes from planning-server-Q24 (`2-backlog/P3/planning-server/02-answers.md`): polling
with a registry of who is interested, issues read by an outside poller, a plugin system for
connectors. The answers below settle the open questions of this CR's first specification.

## 2026-11-20, settled by the Chief of Staff (the user asks no questions)

1. **Adding a connector:** a module in chantier's package plus one line in the plugin table.
   It needs no install step and keeps "uv is the only tool"; entry points and executables named
   in `chantier.yaml` are out of scope.
2. **Who reads issues:** only the outside poller (the user's words in Q24); the registry lists the
   issues the CRs' `issue:` lines name; the hub's query budget does not change.
3. **The poller's entry:** `chantier journal add` accepts only `issue@1`.
4. **An event on an issue no CR names:** refused, nothing written.
5. **Order with Part A:** this CR lands after `typed-journal-events` (`depends.json`).
6. **The `review` fact:** read in this CR (GitHub `reviewDecision` when asked; GitLab answers
   "unproved"), so that Part E only consumes it.
7. **An issue event wakes the watcher:** the poller decides, default yes.
8. **Credentials:** the connectors keep using the user's own `gh` and `glab` logins; no token,
   no HTTP library.
9. **AGENTS.md:** the four changes of §7.1 are approved as written (the hub's budget sentence
   around the registry, budget unchanged; one journal line for the outside poller; `interests`
   and `journal add` as named exceptions citing Q24; the PRs page through the connector, budget
   unchanged).

Note for Part E (`typed-waits`): its E.3 names `board/forge_read.py`, which this CR removes; its
own specification follows this CR's connector seam.

## 2026-11-20, the spec critic's first pass (11 points), settled by the Chief of Staff

Seven text fixes (1, 3, 4, 5, 6, 9, 10) go to the writer without a question. The four that touch
behaviour:

- **Critic 2, the hub's read budget:** unchanged, one query per project and cycle. A project
  whose interests span more than one forge repository gets the refusal in its hub entry, as
  today; AGENTS.md keeps "one query per project". The PRs page and the hub agree.
- **Critic 7, an issue two CRs name:** moves to `outside-poller` (below). There, the line names
  every CR folder that names the issue, in a field `folders`, not `cr`; and `journal add`
  refuses a payload with any key outside its list (`cr`, `type`, `source`, `audience`
  included), exit 1, nothing written.
- **Critic 8, GitHub's `reviewDecision`:** proved with one read on a real PR, with and without
  required reviews, recorded in this CR's evidence before it ships; null maps to `unknown`, not
  `none`.
- **Critic 11, the bundle:** split. This CR keeps the connectors, the registry, the hub and
  `review` (what Part E needs). The outside-poller half (`interests`, `journal add`,
  `issue@1`, the `issues` provider, AGENTS.md edits 2 and 3, its doc and scenario case) goes to
  a new inbox CR, `1-inbox/outside-poller`, after `typed-journal-events`. FC-2, FC-3, FC-4 and
  FC-7 move with it.
