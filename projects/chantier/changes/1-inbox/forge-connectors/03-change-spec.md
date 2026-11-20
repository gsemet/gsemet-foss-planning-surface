# Change Specification: forge connectors as plugins, polling only what is awaited

Origin: verbal (2026-11-20, the user's answer planning-server-Q24, in `planning-server`'s grill).
No tracker issue.

Its decisions come from the user's words recorded in
`../../2-backlog/P3/planning-server/02-answers.md` ("2026-11-20, the user: forge monitoring and
connectors", and planning-server-Q24), from this CR's own `02-answers.md` (nine points settled by
the Chief of Staff on 2026-11-20, cited below as FC-1 to FC-9), from the project's `AGENTS.md`,
and from the code as it is at `8bd198b1`. It lands after `typed-journal-events` (Part A;
`depends.json`, FC-5).

## 1. Goal, in the user's terms

> Pour le monitoring sur les forge il faudra nécessairement faire du polling mais il faut une
> système pour savoir qui est intéressé. Pour les d'événements sur les issues je penses que je
> ferais un polling extérieur. Il faudra un système de plugin pour facilement rajouter des
> connecteurs

- **Polling, with a registry of who is interested.** chantier keeps polling the forge (no
  webhook), but the poll reads only what someone waits for. Each interest names its subject (a PR
  or MR, an issue), the facts wanted, and who wants them. A project nobody waits on is not read.
- **Issues are polled from outside.** chantier's forge hub does not read issues. An outside
  poller (the user's own script, cron job or service) learns from chantier which issues are
  awaited, polls its tracker (Jira, GitHub, GitLab, any other), and writes what it finds into the
  project's journal through one CLI entry.
- **Connectors as plugins.** Reading a forge goes through one connector interface. GitHub and
  GitLab are the two connectors shipped; adding one is one module and one line in a table.
- **Typed waits depend on it** (`1-inbox/typed-waits`, Part E of `planning-server`'s
  `experiments/03-change-spec-all-parts.md`): a wait is an interest, and its forge read goes
  through a connector. §8 lists what Part E gets from this CR.

## 2. Decisions carried

| Decision (source, date) | Where it lands |
| --- | --- |
| Forge monitoring needs polling (Q24 grill, 11-20) | §3: the hub keeps its 20 s cycle; no webhook (§10) |
| A system to know who is interested; the poll reads only what someone waits for (11-20) | §4: the interest registry; §3.3: the hub reads only the registry's PR subjects |
| Events on issues: polled from outside, not by chantier's hub (11-20) | §5: the hub reads no issue; `interests` lists the awaited issues; `journal add` is the entry |
| A plugin system to add connectors easily (11-20) | §3: `connectors/`, one module and one table line per connector |
| Q24: a CR of its own, `forge-connectors`: a connector interface as plugins, the interest registry, an entry for an outside poller that writes into the journal; typed waits depend on it (11-20) | this CR; §8 |
| Typed waits stay generic: GitHub PR and GitLab MR alike (11-10) | §3.2: facts named by what they are, never by the forge |
| Q23: GitLab approvals are unproved; one read on a real MR (Free and Premium) before the GitLab half of `approval` ships (11-20) | §3.2: the GitLab connector answers `review: unproved`; Part E proves and turns it on |
| AGENTS.md: the hub reads the forge read-only, with the user's own `gh` or `glab`, at most once every 20 s, one query per project of the surface whose running batch has a PR the record does not hold merged or cancelled; the PRs page at most once every 10 s per project and batch shown | §3.3, §7.1: the hub's budget stays one query per project and cycle for what is awaited today; the page's budget does not change |
| AGENTS.md: every journal line goes through the one append function | §5.2: `journal add` calls `journal.append` |
| AGENTS.md: a new CLI tool comes from measured token cost, or is a named exception | §7.1: `interests` and `journal add` named as exceptions on the user's answer Q24 |
| AGENTS.md: no fallback | §3.1: a link no connector claims is an error, never read another way |
| FC-1: a connector is a module in chantier's package plus one line in the plugin table; no install step; entry points and executables named in `chantier.yaml` out of scope | §3.1, §10 |
| FC-2: only the outside poller reads issues; the registry lists the issues the CRs' `issue:` lines name; the hub's budget unchanged | §4.2 `issues`, §5 |
| FC-3: `journal add` accepts only `issue@1` | §5.2 |
| FC-4: an event on an issue no CR names is refused, nothing written | §5.2 |
| FC-5: this CR lands after `typed-journal-events` (`depends.json`) | header; §4.2, §5.2 write `name@N` types and Part A's `source` list gains `poller` |
| FC-6: the `review` fact is read in this CR (GitHub `reviewDecision` when asked; GitLab `unproved`), so Part E only consumes it | §3.2, §8 |
| FC-7: an issue event wakes the watcher as the poller says, default yes | §5.2 `wakes`, §5.3 |
| FC-8: the connectors use the user's own `gh` and `glab` logins; no token, no HTTP library | §3.1, §3.2 |
| FC-9: the four `AGENTS.md` changes of §7.1 approved as written | §7.1 |

## 3. Connectors

### 3.1 The package

New package `skills/chantier/scripts/cli/src/chantier/connectors/`. It replaces
`board/forge_read.py`, which is removed; its code moves, split by forge, with no change of
behaviour for what it reads today.

- `connectors/base.py`:
  - `Facts`: the dict of one PR or MR as the board judges it, exactly today's keys (`state`,
    `conflicting`, `checking`, `checks`, `base`, `head`, `merged_on_default`, `merged_at`,
    `closed_at`, `opened_at`, `updated_at`), plus `review` when asked (§3.2).
  - `Place`: a frozen dataclass `(connector: str, host: str, repository: str)`: one forge
    repository, the unit of one query.
  - `Connector`: a `typing.Protocol` with
    - `name: str` (`github`, `gitlab`), `program: str` (`gh`, `glab`), `word: str` (`PR`, `MR`);
    - `claims(link: str) -> bool`: whether the link is one of its review requests (the shape
      tests of today: `GITLAB_LINK` for GitLab, `pr_parts` for GitHub);
    - `place(link: str) -> Place` and `number(link: str) -> int`;
    - `read(place: Place, numbers: list[int], facts: frozenset[str]) -> dict[int, Facts]`:
      **exactly one** call of its program, read-only, for every number; `facts` is the set of
      optional facts asked (today only `review`); with none asked, the query text is byte for
      byte today's.
- `connectors/run.py`: today's `forge_read.run` (the program on PATH, `TIMEOUT_S` 20 s, the
  forge's one line on failure, JSON with no `errors`), plus one guard: it runs only an argv
  whose first two words are `api graphql` and whose `query=` text starts with `query` (no
  `mutation`); anything else raises `AssertionError` (a code fault, never a user error). Every
  connector calls the forge through it.
- `connectors/github.py`: `github_query`, `GITHUB_FIELDS`, `GITHUB_CHECKS`, `github_state`,
  `_github_rows`, `DEFAULT_HISTORY` from today's `forge_read.py`, and the `CONNECTOR` object.
- `connectors/gitlab.py`: `gitlab_query`, `GITLAB_FIELDS`, `GITLAB_CHECKS`,
  `GITLAB_UNCOMPUTED`, `gitlab_state`, `_gitlab_rows`, and the `CONNECTOR` object.
- `connectors/__init__.py`:
  - `CONNECTORS = (github.CONNECTOR, gitlab.CONNECTOR)`: **the plugin table**. Adding a
    connector is one module that implements `Connector`, one line here, its fake forge for the
    tests (§9) and its row in `docs/hosts.md` (§7.2).
  - `connector_for(link) -> Connector`: the first that claims the link; none raises
    `ChantierError("no connector reads <link>: chantier reads GitHub and GitLab", EXIT_PRECONDITION)`.
    No fallback (AGENTS.md).
  - `read(links: list[str], facts: frozenset[str] = frozenset()) -> dict[int, Facts]`: today's
    `forge_read.read`, through the connector: all links of one `Place` (else today's
    `NOT_ONE_REPOSITORY` refusal), one call. **The one test seam** that replaces
    `forge_read.read` in the tests (`forge_world.py`, `test_board_prs*.py`, `test_forge_hub.py`).

Callers updated: `hub/cycle.py`, `board/prs.py` (`answer` passes `connectors.read` to
`ForgeReads.get`), the tests named above, and the module docstrings that name `forge_read`
(`board/prs.py`, `hub/cycle.py`). `board/forge_kind.py` and the Driver-side forge commands
(`commands/forge_base.py`, `forge_stack*.py`) do not change (§10).

### 3.2 Facts: what a connector may read

A connector reads only, through its program's GraphQL API, and only these facts of the review
requests it is asked about (and, for GitHub, today's two repository fields: the default branch's
workflow folder and its last `DEFAULT_HISTORY` commits, which the facts need):

| Fact | GitHub (`gh api graphql`) | GitLab (`glab api graphql`) | Asked by |
| --- | --- | --- | --- |
| `state`, `conflicting`, `checking`, `base`, `head`, times | today's fields | today's fields | always |
| `checks` (green, failing, running, none) | `statusCheckRollup` of the head | `headPipeline.status` | always |
| `merged_on_default` | `mergeCommit.oid` in the default branch's history | always null (today) | always |
| `review` (`approved`, `changes-requested`, `required`, `none`) | `reviewDecision` (`APPROVED`, `CHANGES_REQUESTED`, `REVIEW_REQUIRED`, null), added to the query only when asked | `unproved`, with no field added to the query, until Part E's proof (planning-server-Q23) | an interest asking `review` (none in this CR; Part E's `approval` waits) |

A connector never reads an issue, a comment, a user, a diff or a file content, and never writes.
Everything it reads goes into `Facts`; nothing else is kept.

### 3.3 The hub reads through the registry

`hub/cycle.py`'s `Hub.cycle(now)` becomes, for each project (`Hub.projects()`, unchanged):

1. `wanted = interests.collect(repo)` (§4). Keep the interests the hub reads (`kind == "pr"`).
   None: the project is not read (no forge call, no change to its `hub` entry), as today when no
   batch runs or every PR is held merged or cancelled.
2. Group them by `Place` (`connector_for(link).place(link)`); per group, the union of the facts
   asked. A link no connector claims: the project's entry carries that refusal's text as its
   `error` (as a failed read does today) and the other groups go on.
3. Per group, one `connectors.read(links, facts)` call. Today every interest of a project is in
   one repository (a batch's PRs are, `NOT_ONE_REPOSITORY`): one query per project and cycle, as
   AGENTS.md says. A failed call: the entry's `error` and `error_at`, as today; the other groups go
   on.
4. Each provider judges its own interests against the facts read and returns journal events
   (§4.2); the cycle appends them all in one `journal.append(repo, events, "hub")`.

The cycle's 20 s (`hub/times.py`), the election, the `hub` entry's shape, the `forge hub:` line
of `status` and the watcher do not change.

The board's PRs page keeps its own read (`board/prs.py`), through `connectors.read`, with its 10 s
TTL per project and batch shown: it is not an interest of the registry (it reads what the user
looks at, a closed batch included), and its budget is AGENTS.md's, unchanged.

## 4. The interest registry

### 4.1 What an interest is

New module `skills/chantier/scripts/cli/src/chantier/hub/interests.py`:

- `Interest`: a frozen dataclass
  - `kind`: `pr` (a review request: a GitHub PR or a GitLab MR, read by the hub through its
    connector) or `issue` (a tracker issue, read by an outside poller only, §5);
  - `ref`: the PR or MR link, or the issue's link as the CR's `issue:` line holds it;
  - `facts`: a frozenset; for `pr`: `state`, `checks` (always read) and optionally `review`; for
    `issue`: `events`;
  - `by`: who waits, in words a person reads: `batch-29 CR-3` (a batch's CR), `2-backlog/P2/login-fix`
    (a CR folder by its stage path), and later Part E's `batch-29 CR-3 w2`;
  - `provider`: the name of the provider that declared it.
- `Provider`: a `Protocol` with `name: str`, `collect(repo: Repo) -> list[Interest]` and
  `judge(repo, interests, facts: dict[str, Facts]) -> list[event]` (facts by link; a provider of
  `issue` interests judges nothing and returns `[]`).
- `PROVIDERS`: the tuple of the providers, in order. **Adding a kind of waiter is one module and
  one line here** (Part E adds its `waits` provider so).
- `collect(repo) -> list[Interest]`: every provider's interests, in order; two interests on the
  same `ref` stay two (their `by` differ); a provider that raises `ChantierError` or `OSError` is
  skipped for that cycle with its text in the project's `hub` entry `error`.

The registry is **derived, never stored**: each call reads the record and the planning folder
again (no file to drift, nothing to clean when a CR ends). Reading it writes nothing.

### 4.2 The providers this CR ships

- `hub/batch_prs.py`, provider `batch`: today's `running_batch`, `to_read`, `state_of` and
  `events_of`, moved from `hub/cycle.py` with no change of judgment. `collect`: when the batch in
  `4-batch/` is running and `to_read` holds, one `pr` interest per CR of the batch with a PR (the
  same set as today's `state_of`, merged CRs included: the landed rule `prs.landed_with` needs
  the chain's bases, and they cost no extra query), `facts` `{state, checks}`, `by`
  `<batch> <cr>`. `judge`: `merged@1` and `checks-red@1` (Part A's types; this CR lands after it, FC-5), by
  today's rules.
- `hub/issue_refs.py`, provider `issues`: `collect`: one `issue` interest per CR folder of
  `1-inbox/`, `2-backlog/P1`...`P4/`, `3-ready/` and `4-batch/` (its three stages) whose intent or
  specification has an `issue:` line (`summaries/origin.py`, `issue_url`), `facts` `{events}`,
  `by` the folder's path relative to `changes/`; `5-archives/` and `6-trash/` are not read.
  The tracker word is `origin.py`'s kind (`jira`, `gitlab`, `github`), else `other`. `judge`:
  nothing; the hub never reads an issue.

## 5. The outside poller

An outside poller is not chantier: the user's own program, run by the user's means (cron, a
scheduled task, a service). chantier gives it two CLI entries and nothing else; it never starts,
stops or supervises a poller.

### 5.1 `chantier interests`

New command (`declare/interests.py`, handler `hub/interests.py:show`, `NO_BATCH`): read-only, no
network, no lock, exit 0.

```
chantier --project <p> interests [--kind pr|issue] [--json]
```

- Text: a first line `interests of <project>: <n>`, then one line per interest, in `collect`'s
  order: `pr <link> (<connector>): state, checks for <by>` / `issue <link> (<tracker>): events
  for <by>`; with none, `interests of <project>: 0 (the forge hub reads nothing for it)`.
- `--json`: `{"schema": 1, "project": "<name>", "interests": [{"kind", "ref", "connector" (pr) or
  "tracker" (issue), "facts": [...], "by": "...", "read_by": "hub" | "outside"}]}`, sorted keys,
  UTF-8. This is the outside poller's input: it polls only these `issue` refs.

### 5.2 `chantier journal add`

New command (`declare/journal.py`, handler `hub/journal_add.py`, `NO_BATCH`): the one entry by
which an outside poller writes into the journal.

```
chantier --project <p> journal add issue@1 --json <payload | ->
```

- `-` reads the payload from stdin (no shell quoting on Windows). The payload of `issue@1`:
  `tracker` (`jira`, `github`, `gitlab` or `other`), `ref` (the issue's link), `event` (one of
  `opened`, `commented`, `changed`, `closed`, `reopened`), `at` (the tracker's time of the event,
  ISO 8601), `text` (one line, 300 characters at most: what happened, the poller's words),
  `wakes` (boolean, default true). The CLI adds `cr` (the `by` of the matching interest).
- It goes through `journal.append(repo, [event], "poller")`: the one append function (AGENTS.md),
  under the project's lifecycle lock, its `seq` and its duplicate rule. `poller` is a new
  `source` value, added to Part A's list (`hub/journal.py` `SOURCES`), and `issue@1` a type this CR
  publishes in Part A's `hub/schemas.py` and `hub/schemas.json` (its model with
  `extra="forbid"`, its entry in the published file). The audience is `["project"]`.
- Once per `(ref, event, at)`: a duplicate is skipped and prints `journal: already there (seq
  <n>)`, exit 0. A new line prints `journal: seq <n> issue@1 <event> on <ref> (<cr>)`, exit 0.
- Refusals, nothing written:
  - a type other than `issue@1`: `journal add: <type> is not written from outside; an outside
    poller writes issue@1`, exit 2 (the hub's and the board's types stay theirs);
  - a payload its model refuses (a missing or extra field, an unknown `event`, a `text` of two
    lines or over 300 characters): `journal add: issue@1 payload refused: <pydantic's first
    error, one line>`, exit 1;
  - a `ref` no `issue` interest names: `journal add: <ref> is no CR's issue (chantier
    interests --kind issue lists them): nothing written`, exit 2: an event nobody waits for is not
    kept.
  - not valid JSON: `journal add: --json is not JSON: <the parser's one line>`, exit 1.
- In external mode it writes the project's `forge-journal.jsonl`, which is local and never
  published: no surface writer (Part C) is needed for it.

### 5.3 How the line is read

- `journal.event_text` for `issue@1`: `tracker saw <event> on <ref> (<cr>): "<text>"; for the
  Chief of Staff: tell the user in one line, record nothing`.
- `chantier watch` prints it and ends on it as on a merge when `wakes` is true; with `wakes`
  false it rides along with the next waking line (as a `board@1` line that does not wake).
- `status` does not list `issue@1` lines (there is nothing to record, so nothing to clear).

## 6. Messages, every one

| Where | Text |
| --- | --- |
| `connector_for`, no connector | `no connector reads <link>: chantier reads GitHub and GitLab` (in the `hub` entry's `error`; on the PRs page as its error line) |
| `interests`, text | `interests of <project>: <n>`; `pr <link> (<connector>): <facts> for <by>`; `issue <link> (<tracker>): events for <by>`; `interests of <project>: 0 (the forge hub reads nothing for it)` |
| `journal add`, written | `journal: seq <n> issue@1 <event> on <ref> (<cr>)` |
| `journal add`, duplicate | `journal: already there (seq <n>)` |
| `journal add`, refusals | the four texts of §5.2 |
| watcher, `issue@1` | `tracker saw <event> on <ref> (<cr>): "<text>"; for the Chief of Staff: tell the user in one line, record nothing` |

Every existing text (`forge saw merged ...`, `forge saw checks red ...`, the `forge hub:` line, the
PRs page's error line for a failed read) is unchanged.

## 7. Project rules, cards and docs

### 7.1 `AGENTS.md` (chantier's own; changes named)

1. The hub's budget sentence. Today: "at most once every 20 s, one query per project of the
   surface whose running batch has a PR the record does not hold merged or cancelled". Becomes:
   "at most once every 20 s, through the connector of its forge (GitHub with `gh`, GitLab with
   `glab`), one query per project and forge repository of the surface for which the interest
   registry holds a review request it reads, and only those: today, the PRs of a project's
   running batch while one of them is not held merged or cancelled". The rest of that paragraph
   (what it appends, records nothing, runs no git, messages no agent) is unchanged.
2. The journal: after "every journal line, the CLI commands' included in their own process, goes
   through the one append function", add: "an outside poller (the user's own program, never
   started by chantier) writes into it only through `journal add`, only `issue@1` lines, and only
   for an issue a CR's `issue:` line names".
3. "The CLI's scope": name `interests` and `journal add` as exceptions to "a new CLI tool comes
   from measured token-costly behaviour", built on the user's answer planning-server-Q24
   (2026-11-20).
4. The PRs page's sentence: "it reads the forge, read-only, with the user's own `gh` or `glab`"
   gains "through the connector of its forge"; its budget is unchanged.

### 7.2 Docs (every file this CR makes false)

- **New `docs/forge-connectors.md`**: what a connector reads (§3.2's table), the interest
  registry (who waits for what, derived each cycle), the budget (§7.1, 1), "Adding a connector"
  (the `Connector` protocol, the plugin table, the fake forge and the docs row it owes), and
  "Writing an outside poller": the contract (`interests --kind issue --json`, then one `journal
  add issue@1 --json -` per event, a duplicate harmless, a refusal printed), one short Python
  example that loops over the interests with a placeholder `fetch_events(ref)` the user writes for
  their tracker, and the rules (read-only on the tracker is the poller's business; chantier never
  starts it; one line of `text`, no personal data needed).
- `README.md`, the docs list (after "Supported hosts"): `- [Forge connectors](docs/forge-connectors.md): how chantier reads a forge, and an outside poller for issues.`
- `docs/hosts.md`: the forge table gains a column, `Connector` (`github`, `gitlab`), and one
  sentence under it: chantier's own reads of a forge (the hub, the PRs page) go through a
  connector, read-only; issues from any tracker come from an outside poller
  ([forge connectors](forge-connectors.md)).
- `docs/planning-folder.md`, "The event journal": the first paragraph adds "and the issue events
  an outside poller writes"; the `source` row adds `poller` (an outside poller, through `journal
  add`); Part A's types table gains the `issue@1` row (written by an outside poller,
  wakes a watcher when `wakes`); the "Every line written today is for `["project"]`" sentence names it.
- `docs/web-board.md`, "Starting the board", the forge hub's sentence ("it reads the forge,
  read-only, every 20 s with your own `gh` or `glab`") adds "only the PRs a running batch waits
  for (`chantier interests` lists them)".
- SVGs: none changes. Searched every `docs/*.svg` and `docs/*-texts.md` for hub, watcher, journal,
  poll, `gh`, `glab`, Jira: the only hits are the intake's sources ("a Jira issue, a GitLab or
  GitHub issue", in `cr-folder-lifecycle`, `cr-lifecycle`, `cr-lifecycle-simple`), still true (a
  request is still filed from an issue; the poller reports events on it, it files nothing). No
  diagram draws the hub or the forge reads; this CR adds none.
- Searched and unaffected: `docs/boards.md` (the pane's `STATUS.json` fields do not change: no
  screenshot owed), `docs/planning-modes.md`, `docs/use-cases*.md`, `docs/gates.md`,
  `docs/costs.md`, `docs/tutorial-claude-code.md`. `docs/release-notes/` is history; the
  release's notes are a new file, as the release process says.

### 7.3 Cards

- `skills/chantier/references/session-start.md`, "The board": "it reads the forge every 20 s
  with the user's own `gh` or `glab`" adds "only the PRs a running batch waits for".
- `skills/chantier/references/chief-of-staff.md`, "The watcher": the list of what it prints adds
  `tracker saw` (an outside poller's issue event); *A watcher's end* adds: "A `tracker saw ...`
  line: one line to the user that says it, no tool call, record nothing." Off the common path
  where the card keeps watcher detail.
- `skills/chantier/references/concepts.md`: two words, **Connector** (the module that reads one
  forge, read-only; GitHub and GitLab ship) and **Interest** (what someone waits for on a forge or
  a tracker; `chantier interests` lists them; the hub reads only those).
- `agents/` and `com.github.copilot/agents/`: no change (no role changes).

## 8. What Part E (`typed-waits`) gets

- The provider seam: Part E adds `hub/waits.py`, provider `waits`, one line in `PROVIDERS`:
  `collect` gives one `pr` interest per open `approval`, `pipeline` or `merge` wait of a running
  batch's CR with a PR (`facts` `{state, checks}`, plus `review` for `approval`; `by`
  `<batch> <cr> <wait id>`), and `judge` returns its `wait-cleared@1` lines. Being in the same
  repository as the batch's PRs, they ride in the same query: AGENTS.md's budget (§7.1, 1) holds
  with no new sentence; Part E adds its interests to that sentence's "today" list.
- The facts it needs, read by the connectors: `state == "merged"` (`merge`), `checks` and `head`
  (`pipeline`: met when the head is the wait's sha and the checks are green), `review`
  (`approval`): GitHub's `reviewDecision`; GitLab answers `unproved`, so Part E's `approval` on
  GitLab stays cleared by hand until its proof (planning-server-Q23), after which Part E fills
  GitLab's `review` in `connectors/gitlab.py` (the field of the approvals it proves).
- Part E's E.3 names `board/forge_read.py`; it becomes `connectors` (its specification follows).
- E.7 question 1 (the hub reading backlog CRs' waits) is an interest with no running batch: a
  `collect` for backlog `waits.json`; it would change §7.1's "today" list, and is Part E's
  question, not this CR's.

## 9. Evidence

- `tests/test_connectors.py` (new; `test_board_forge_read.py`'s cases move into it, parametrized
  over the two connectors): a link is claimed by its connector and by no other; a link neither
  claims raises the §6 text; the argv is `api graphql` with a `query` and no `mutation`; with no
  optional fact asked, the query text equals today's (a golden string per forge, kept in the test);
  with `review` asked, the GitHub query holds `reviewDecision` and each of its four answers maps to
  §3.2's word, the GitLab query is unchanged and every MR's `review` is `unproved`; a recorded
  answer gives today's `Facts` (the moved cases); `run.py`'s guard raises on a prepared argv with a
  mutation (a case the shipped code cannot produce, paired with the shipped connectors' argv
  checked above).
- `tests/test_forge_hub.py`: every existing test passes, the seam now `connectors.read`; new,
  parametrized: a project whose only interests are `issue` ones makes no forge call; two
  providers' interests on one repository make one call (a test provider added to `PROVIDERS` by
  `monkeypatch`); a batch PR link no connector claims puts the §6 text in that project's entry and
  the other projects are read.
- `tests/test_interests.py` (new): `interests` lists the running batch's PRs (none when paused or
  every PR held merged or cancelled), the `issue:` lines of CR folders in `1-inbox`, `2-backlog`,
  `3-ready` and `4-batch`, none of `5-archives` or `6-trash`; the text and `--json` forms; it
  writes nothing (the tree's fingerprint unchanged, as `test_validate.py` does).
- Part A's `tests/test_event_types.py` covers `issue@1` once its model and its `schemas.json`
  entry are added (the shipped file, read at the head under test).
- `tests/test_watch_events.py` (or a new `test_journal_add.py`), parametrized: `journal add
  issue@1` appends one line with `source: poller` and `cr` filled; the same `(ref, event, at)`
  again writes nothing and prints the duplicate text; `merged@1` refused (exit 2); a ref no CR
  names refused (exit 2); bad JSON, an unknown `event`, a two-line or 301-character `text` (exit
  1); every refusal writes nothing; `watch --once --after <n>` prints the `tracker saw` line.
- Cards and docs guarded as they ship: `test_plugin_files.py` and `test_startup_manifest.py` read
  the shipped cards at the head under test; no prepared copy.
- `just check`, `just test` within its budget (AGENTS.md: at most 30 s above 18.5 s), `just
  eval-dry-run` (the change is under the CLI's `src/`).
- Scenario, `just scenario`, green on the pipeline's `just scenario (ubuntu-latest)` job, and
  locally on Windows (`chantier gate`) when this CR is the top of its batch:
  - unit `surface-board`, case `forge_hub`: its existing checks hold (one `api graphql` call per
    project with an open PR, no mutation); one check added: every PR the hub's calls name is in
    that project's `interests --json`.
  - unit `surface-board`, new case `outside_poller`: a CR filed with an `issue:` line (a Jira
    link) is listed by `interests --kind issue --json`; the scenario, as the poller, runs
    `journal add issue@1 --json -`; a running watcher ends and prints the `tracker saw` line; the
    same add again writes nothing; a ref no CR names is refused and the journal is unchanged; the
    forge calls are unchanged by it (the hub read no issue). The unit's time budget is raised by
    the case's measured time, if it needs it.
- Forge matrix (the change depends on the forge, not on the host or a configured value):

| Forge | Cell | Expected |
| --- | --- | --- |
| GitHub | the hub with a running batch, no `review` asked | one query per cycle, today's text |
| GitHub | an interest asks `review` (test provider) | the same one query, with `reviewDecision` |
| GitLab | the hub with a running batch | one query per cycle, today's text |
| GitLab | an interest asks `review` | the same query; `review: unproved` |
| any | a link no connector claims | no call for it; the entry's error names it |
| none (issues) | an outside poller's `issue@1` | one line, no forge call |

- No CI job is added or changed.

## 10. Out of scope

- Webhooks, or any push from a forge: polling only (the user's words).
- The hub reading issues, comments or any tracker: the outside poller does (the user's words).
- A Jira, Gitea or other connector: the interface and the table make one easy; none ships here.
- Loading connectors from outside chantier's package (Python entry points, executables named in
  `chantier.yaml`) (FC-1).
- A token or an HTTP library for the forge (FC-8).
- The Driver-side forge commands (`forge-stack`, `ship`'s and `take`'s base reads in
  `commands/forge_base.py`, `forge_stack*.py`), which write to the forge: they keep calling `gh`
  and `glab` directly.
- `board/forge_kind.py` (the board's PR/MR word).
- Typed waits themselves, `wait-cleared@1`, and the GitLab approval proof: Part E.
- Narrowing the batch's PR set below today's (merged bases are kept for the landed rule; they
  cost no query).
- Starting, supervising or shipping an outside poller.

## 11. Open questions for the user

None. The nine questions of the first draft are settled in this CR's `02-answers.md` (FC-1 to
FC-9), each as recommended; §2 carries them.
