# Change Specification: forge connectors as plugins, and a hub that polls only what is awaited

Origin: verbal (2026-11-20, the user's answer planning-server-Q24, in `planning-server`'s grill).
No tracker issue.

Its decisions come from the user's words recorded in
`../../2-backlog/P3/planning-server/02-answers.md` ("2026-11-20, the user: forge monitoring and
connectors", and planning-server-Q24), from this CR's own `02-answers.md` (nine points settled by
the Chief of Staff on 2026-11-20, cited below as FC-1 to FC-9, and the spec critic's first pass,
settled the same day, cited as SC-1 to SC-11), from the project's `AGENTS.md`, and from the code
as it is at `8bd198b1`. It lands after `typed-journal-events` (Part A; `depends.json`, FC-5).

**Split (SC-11).** The outside poller (the `interests` and `journal add` commands, the `issue@1`
type, the `issues` provider, its AGENTS.md lines, its doc and its scenario case) is no longer in
this CR: it is `1-inbox/outside-poller`, which starts from this specification's earlier text
(surface commit `7fd03eab`). FC-2, FC-3, FC-4, FC-7 and SC-7 moved with it. This CR keeps the
connectors, the interest registry, the hub that reads through them, and the `review` fact: what
Part E (`typed-waits`) needs.

## 1. Goal, in the user's terms

> Pour le monitoring sur les forge il faudra nécessairement faire du polling mais il faut une
> système pour savoir qui est intéressé. [...] Il faudra un système de plugin pour facilement
> rajouter des connecteurs

- **Polling, with a registry of who is interested.** chantier keeps polling the forge (no
  webhook), but the hub reads only what someone waits for. Each interest names its subject (a PR
  or MR), the facts wanted, and who wants them. A project nobody waits on is not read.
- **Connectors as plugins.** Reading a forge goes through one connector interface. GitHub and
  GitLab are the two connectors shipped; adding one is one module and one line in a table.
- **Typed waits depend on it** (`1-inbox/typed-waits`, Part E of `planning-server`'s
  `experiments/03-change-spec-all-parts.md`): a wait is an interest, and its forge read goes
  through a connector. §7 lists what Part E gets from this CR.
- The user's third point, issues polled from outside, is `1-inbox/outside-poller` (SC-11).

## 2. Decisions carried

| Decision (source, date) | Where it lands |
| --- | --- |
| Forge monitoring needs polling (Q24 grill, 11-20) | §3.3: the hub keeps its 20 s cycle; no webhook (§9) |
| A system to know who is interested; the poll reads only what someone waits for (11-20) | §4: the interest registry; §3.3: the hub reads only the registry's PRs |
| Events on issues polled from outside (11-20) | moved to `1-inbox/outside-poller` (SC-11; §9) |
| A plugin system to add connectors easily (11-20) | §3.1: `connectors/`, one module and one table line per connector |
| Q24: a CR of its own; typed waits depend on it (11-20) | this CR; §7 |
| Typed waits stay generic: GitHub PR and GitLab MR alike (11-10) | §3.2: facts named by what they are, never by the forge |
| Q23: GitLab approvals unproved until one read on a real MR (Free and Premium) (11-20) | §3.2: GitLab answers `review: unproved`; Part E proves and turns it on |
| AGENTS.md: the hub reads read-only, with the user's own `gh` or `glab`, at most once every 20 s, one query per project; the PRs page at most once every 10 s per project and batch shown | §3.3, §6.1: both budgets unchanged (SC-2) |
| AGENTS.md: no fallback | §3.1: a link no connector claims is an error, never read another way |
| FC-1: a connector is a module in chantier's package plus one line in the plugin table; no install step; entry points and executables named in `chantier.yaml` out of scope | §3.1, §9 |
| FC-5: this CR lands after `typed-journal-events` | header; §4.2 writes `merged@1` and `checks-red@1` |
| FC-6: the `review` fact is read in this CR (GitHub `reviewDecision` when asked; GitLab `unproved`), so Part E only consumes it | §3.2, §7 |
| FC-8: the user's own `gh` and `glab` logins; no token, no HTTP library | §3.1, §3.2, §9 |
| FC-9: the AGENTS.md changes approved as written; after the split (SC-11) this CR keeps edits 1 and 4, and edits 2 and 3 moved to `outside-poller` | §6.1 |
| SC-1: the read-only guard accepts `api [--hostname <host>] graphql` | §3.1 `run.py`; §8 |
| SC-2: the hub's budget stays one query per project and cycle; a project whose PRs span several repositories gets the refusal in its hub entry, as today | §3.3; §6.1 edit 1 |
| SC-3: AGENTS.md's watcher sentence ("reads only its project's journal (the hub's lines and the board's)") moves to `outside-poller` | §6.1, §9 |
| SC-4: the "Two named exceptions" sentence of "The CLI's scope": this CR adds no CLI command, so it does not touch it; `outside-poller` does | §6.1, §9 |
| SC-5: GitHub claims a link by `PR_LINK` (`commands/forge_stack_gh.py`), not `pr_parts` | §3.1 |
| SC-6: the hub collects only the providers of `pr` interests; its entry's error holds forge-read errors only | §3.3, §4.1 |
| SC-8: `reviewDecision` proved by one real read, with and without required reviews, in the evidence before it ships; null maps to `unknown` | §3.2, §8 |
| SC-9: `tests/test_board.py` and `tests/test_watch_events.py` are callers of the seam too | §3.1 |
| SC-10: the unclaimed-link text is a change (hub entry and PRs page); the batch's other PRs are now read | §3.3, §5 |

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
    - `claims(link: str) -> bool`: whether the link is one of its review requests. GitHub:
      `PR_LINK.match(link)` (`commands/forge_stack_gh.py`); GitLab: `GITLAB_LINK.match(link)`
      (`commands/forge_stack_gitlab.py`). Never `pr_parts`, which answers for both (SC-5);
    - `place(link: str) -> Place` and `number(link: str) -> int`;
    - `read(place: Place, numbers: list[int], facts: frozenset[str]) -> dict[int, Facts]`:
      **exactly one** call of its program, read-only, for every number; `facts` is the set of
      optional facts asked (only `review`); with none asked, the query text is byte for byte
      today's.
- `connectors/run.py`: today's `forge_read.run` (the program on PATH, `TIMEOUT_S` 20 s, the
  forge's one line on failure, JSON with no `errors`), plus one guard: it runs only an argv of the
  form `api graphql ...` or `api --hostname <host> graphql ...` (SC-1; `argv` adds `--hostname`
  for a host other than `github.com` or `gitlab.com`), whose `query=` value starts with `query`
  (no `mutation`); anything else raises `AssertionError` (a code fault, never a user error). Every
  connector calls the forge through it.
- `connectors/github.py`: `github_query`, `GITHUB_FIELDS`, `GITHUB_CHECKS`, `github_state`,
  `_github_rows`, `DEFAULT_HISTORY` and the GitHub half of `argv` from today's `forge_read.py`,
  and the `CONNECTOR` object.
- `connectors/gitlab.py`: `gitlab_query`, `GITLAB_FIELDS`, `GITLAB_CHECKS`, `GITLAB_UNCOMPUTED`,
  `gitlab_state`, `_gitlab_rows`, the GitLab half of `argv`, and the `CONNECTOR` object.
- `connectors/__init__.py`:
  - `CONNECTORS = (github.CONNECTOR, gitlab.CONNECTOR)`: **the plugin table**. Adding a
    connector is one module that implements `Connector`, one line here, its fake forge for the
    tests (§8) and its row in `docs/hosts.md` (§6.2).
  - `connector_for(link) -> Connector | None`: the first that claims the link, else None.
  - `UNCLAIMED = "no connector reads {link}: chantier reads GitHub and GitLab"`.
  - `read(links: list[str], facts: frozenset[str] = frozenset()) -> dict[int, Facts]`: today's
    `forge_read.read`, through the connectors: every link must be claimed (else
    `ChantierError(UNCLAIMED.format(link=<the first unclaimed>), EXIT_PRECONDITION)`) and all of
    one `Place` (else today's `NOT_ONE_REPOSITORY` refusal); one call. No fallback (AGENTS.md).
    **The one test seam** that replaces `forge_read.read` in the tests.

Callers updated: `hub/cycle.py` (then `hub/batch_prs.py`, §4.2), `board/prs.py` (`answer`
passes `connectors.read` to `ForgeReads.get`), the module docstrings that name `forge_read`
(`board/prs.py`, `hub/cycle.py`), and every test that replaces or imports the seam:
`tests/forge_world.py`, `tests/test_board_forge_read.py` (moved into `test_connectors.py`, §8),
`tests/test_board_prs.py`, `tests/test_forge_hub.py`, `tests/test_board.py` and
`tests/test_watch_events.py` (SC-9): every file that names `forge_read` at `8bd198b1`; the
Driver searches it once more at its base and updates any other hit. `board/forge_kind.py` and the
Driver-side forge commands (`commands/forge_base.py`, `forge_stack*.py`) do not change (§9).

### 3.2 Facts: what a connector may read

A connector reads only, through its program's GraphQL API, and only these facts of the review
requests it is asked about (and, for GitHub, today's two repository fields: the default branch's
workflow folder and its last `DEFAULT_HISTORY` commits, which the facts need):

| Fact | GitHub (`gh api graphql`) | GitLab (`glab api graphql`) | Asked by |
| --- | --- | --- | --- |
| `state`, `conflicting`, `checking`, `base`, `head`, times | today's fields | today's fields | always |
| `checks` (green, failing, running, none) | `statusCheckRollup` of the head | `headPipeline.status` | always |
| `merged_on_default` | `mergeCommit.oid` in the default branch's history | always null (today) | always |
| `review` | `reviewDecision`, added to the query only when asked: `APPROVED` → `approved`, `CHANGES_REQUESTED` → `changes-requested`, `REVIEW_REQUIRED` → `required`, null → `unknown` (SC-8: null is what GitHub answers both with no required review and when it cannot tell; it never means "approved") | `unproved`, with no field added to the query, until Part E's proof (planning-server-Q23) | an interest asking `review` (none in this CR; Part E's `approval` waits) |

A connector never reads an issue, a comment, a user, a diff or a file content, and never writes.
Everything it reads goes into `Facts`; nothing else is kept.

The GitHub `review` read ships only once proved (SC-8): before the CR's PR is ready, its Driver
runs one real `gh api graphql` read of `reviewDecision` on a PR of a repository **with** a
required review (a branch protection or ruleset that requires one) and one **without**, and
records in the CR's evidence, for each: the command, the repository's rule, and the answer's
`reviewDecision` (expected: `REVIEW_REQUIRED` or `APPROVED` with, `null` without). An answer
other than expected is a known gap of the PR, and the mapping above is corrected before it ships.

### 3.3 The hub reads through the registry

`hub/cycle.py`'s `Hub.cycle(now)` becomes, for each project (`Hub.projects()`, unchanged):

1. `wanted = interests.collect(repo, kinds={"pr"})`: only the providers of `pr` interests are
   called (SC-6). None: the project is not read (no forge call, no change to its `hub` entry), as
   today when no batch runs or every PR is held merged or cancelled.
2. Its links, the facts asked (the union over the interests), and one partition: the links no
   connector claims (`connector_for` is None) are left out of the read, and the project's entry
   `error` is `UNCLAIMED` for the first of them (`error_at` now). **This is a change (SC-10):**
   today such a link makes `pr_parts` refuse the whole read with `forge-stack reads GitHub pull
   requests and GitLab merge requests: <link> is neither`, so none of the batch's PRs is read;
   now the batch's other PRs are read and judged, and the entry names the unclaimed link.
3. One `connectors.read(claimed, facts)` call for the project: **one query per project and
   cycle**, as AGENTS.md says (SC-2). Claimed links of more than one repository: the call
   refuses with `NOT_ONE_REPOSITORY`, which goes in the entry's `error`, and nothing is read for
   the project, as today. A failed call: the entry's `error` and `error_at`, as today. A
   successful one clears the error only when no link was left out at step 2.
4. Each provider judges its own interests against the facts read and returns journal events
   (§4.1); the cycle appends them all in one `journal.append(repo, events, "hub")`.

The entry's `error` holds forge-read errors only (an unclaimed link, `NOT_ONE_REPOSITORY`, a
failed call) (SC-6). A provider never writes it: each `collect` reads the record as today's
`running_batch` does (an unreadable or absent record gives no interest); an exception that still
escapes is the cycle's, handled by `HubLoop.note_error` as today.

The cycle's 20 s (`hub/times.py`), the election, the `hub` entry's shape, the `forge hub:` line
of `status` and the watcher do not change.

The board's PRs page keeps its own read (`board/prs.py`), through `connectors.read`, with its
10 s TTL per project and batch shown: it is not an interest of the registry (it reads what the
user looks at, a closed batch included), and its budget is AGENTS.md's, unchanged. It applies the
same partition as step 2: an unclaimed link's row is not read, the page's error line shows
`UNCLAIMED`, and the other rows are read (SC-10).

## 4. The interest registry

### 4.1 What an interest is

New module `skills/chantier/scripts/cli/src/chantier/hub/interests.py`:

- `Interest`: a frozen dataclass
  - `kind`: `pr` (a review request: a GitHub PR or a GitLab MR, read by the hub through its
    connector). The field is there for the kinds later CRs add (`outside-poller`'s `issue`);
    this CR defines only `pr`;
  - `ref`: the PR or MR link;
  - `facts`: a frozenset; `state` and `checks` (always read) and optionally `review`;
  - `by`: who waits, in words a person reads: `batch-29 CR-3`, and later Part E's
    `batch-29 CR-3 w2`;
  - `provider`: the name of the provider that declared it.
- `Provider`: a `Protocol` with `name: str`, `kinds: frozenset[str]` (the kinds of interest it
  declares), `collect(repo: Repo) -> list[Interest]` and
  `judge(repo, interests, facts: dict[str, Facts]) -> list[event]` (facts by link).
- `PROVIDERS`: the tuple of the providers, in order. **Adding a kind of waiter is one module and
  one line here** (Part E adds its `waits` provider so).
- `collect(repo, kinds) -> list[Interest]`: the interests of the providers whose `kinds` meet
  `kinds`, in order; two interests on the same `ref` stay two (their `by` differ) and the link is
  read once.

The registry is **derived, never stored**: each call reads the record again (no file to drift,
nothing to clean when a CR ends). Reading it writes nothing.

### 4.2 The provider this CR ships

`hub/batch_prs.py`, provider `batch`, kinds `{"pr"}`: today's `running_batch`, `to_read`,
`state_of` and `events_of`, moved from `hub/cycle.py` with no change of judgment.

- `collect`: when the batch in `4-batch/` is running and `to_read` holds, one `pr` interest per
  CR of the batch with a PR (the same set as today's `state_of`, merged CRs included: the landed
  rule `prs.landed_with` needs the chain's bases, and they cost no extra query), `facts`
  `{state, checks}`, `by` `<batch> <cr>`.
- `judge`: `merged@1` and `checks-red@1` (Part A's types, FC-5), by today's rules.

## 5. Messages

| Where | Text | Today |
| --- | --- | --- |
| a link no connector claims: the `hub` entry's `error` (so `status`'s `forge hub: ...; last read failed at <t>: <error>`), and the PRs page's error line | `no connector reads <link>: chantier reads GitHub and GitLab` | `forge-stack reads GitHub pull requests and GitLab merge requests: <link> is neither`, and no PR of the batch read (SC-10) |

Every other text (`forge saw merged ...`, `forge saw checks red ...`, the `forge hub:` line, the
PRs page's error line for a failed read, `NOT_ONE_REPOSITORY`) is unchanged.

## 6. Project rules, cards and docs

### 6.1 `AGENTS.md` (chantier's own; changes named)

1. The hub's budget sentence. Today: "at most once every 20 s, one query per project of the
   surface whose running batch has a PR the record does not hold merged or cancelled". Becomes:
   "at most once every 20 s, through the connector of its forge (GitHub with `gh`, GitLab with
   `glab`), one query per project of the surface for which the interest registry holds a PR or
   MR, and only those: today, the PRs of a project's running batch while one of them is not held
   merged or cancelled". The rest of that paragraph (what it appends, records nothing, runs no
   git, messages no agent) is unchanged.
2. The PRs page's sentence: "it reads the forge, read-only, with the user's own `gh` or `glab`"
   becomes "it reads the forge, read-only, through the connector of its forge, with the user's
   own `gh` or `glab`"; its budget is unchanged.

Not changed by this CR (SC-3, SC-4, SC-11): the watcher's sentence ("reads only its project's
journal (the hub's lines and the board's), never the forge"), the journal's append rule, and the
"Two named exceptions" sentence of "The CLI's scope": this CR adds no CLI command and no journal
writer. `outside-poller` changes them.

### 6.2 Docs (every file this CR makes false)

- **New `docs/forge-connectors.md`**: what a connector reads (§3.2's table) and never reads, the
  interest registry (who waits for what, derived each cycle; today the running batch's PRs), the
  budget (§6.1, 1), and "Adding a connector" (the `Connector` protocol, the plugin table in
  `connectors/__init__.py`, the read-only guard, the fake forge and the `docs/hosts.md` row it
  owes). `outside-poller` adds its own section later.
- `README.md`, the docs list (after "Supported hosts"): `- [Forge connectors](docs/forge-connectors.md): how chantier reads a forge, and how to add a connector.`
- `docs/hosts.md`: the forge table gains a column, `Connector` (`github`, `gitlab`), and one
  sentence under it: chantier's own reads of a forge (the forge hub, the PRs page) go through a
  connector, read-only ([forge connectors](forge-connectors.md)); a link of another forge is
  named in the hub's error and on the PRs page, never read.
- `docs/web-board.md`, "Starting the board", the forge hub's sentence ("it reads the forge,
  read-only, every 20 s with your own `gh` or `glab`") adds "only the PRs a running batch waits
  for"; "PRs", "A forge error" adds: a PR link of a forge chantier has no connector for shows as
  `no connector reads <link>`, and the other rows are read.
- SVGs: none changes. Searched every `docs/*.svg` and `docs/*-texts.md` for hub, watcher,
  journal, poll, `gh`, `glab`, Jira: the only hits are the intake's sources ("a Jira issue, a
  GitLab or GitHub issue", in `cr-folder-lifecycle`, `cr-lifecycle`, `cr-lifecycle-simple`),
  still true. No diagram draws the hub or the forge reads; this CR adds none.
- Searched and unaffected: `docs/planning-folder.md` (no new journal type or source: the hub
  writes `merged@1` and `checks-red@1` as Part A leaves them), `docs/boards.md` (the pane's
  `STATUS.json` fields do not change: no screenshot owed), `docs/planning-modes.md`,
  `docs/use-cases*.md`, `docs/gates.md`, `docs/costs.md`, `docs/tutorial-claude-code.md`.
  `docs/release-notes/` is history; the release's notes are a new file, as the release process
  says.

### 6.3 Cards

- `skills/chantier/references/session-start.md`, "The board": "it reads the forge every 20 s
  with the user's own `gh` or `glab`" adds "only the PRs a running batch waits for".
- `skills/chantier/references/concepts.md`: two words, **Connector** (the module that reads one
  forge, read-only; GitHub and GitLab ship) and **Interest** (a PR or MR someone waits for; the
  forge hub reads only those).
- `chief-of-staff.md`: no change (no new line reaches the watcher). `agents/` and
  `com.github.copilot/agents/`: no change (no role changes).

## 7. What Part E (`typed-waits`) gets

- The provider seam: Part E adds `hub/waits.py`, provider `waits`, kinds `{"pr"}`, one line in
  `PROVIDERS`: `collect` gives one `pr` interest per open `approval`, `pipeline` or `merge` wait
  of a running batch's CR with a PR (`facts` `{state, checks}`, plus `review` for `approval`; `by`
  `<batch> <cr> <wait id>`), and `judge` returns its `wait-cleared@1` lines. Its links are added
  to the project's one query (§3.3, step 3); a wait whose link is in another repository than the
  batch's PRs makes that project's read refuse with `NOT_ONE_REPOSITORY`, as any second
  repository does (SC-2): Part E's `wait add` decides whether to refuse such a `ref`.
- The facts it needs, read by the connectors: `state == "merged"` (`merge`), `checks` and `head`
  (`pipeline`: met when the head is the wait's sha and the checks are green), `review`
  (`approval`, met on `approved`; `unknown` is never met): GitHub's `reviewDecision`, proved
  (§3.2); GitLab answers `unproved`, so Part E's `approval` on GitLab stays cleared by hand until
  its proof (planning-server-Q23), after which Part E fills GitLab's `review` in
  `connectors/gitlab.py`.
- Part E adds its interests to §6.1 edit 1's "today" list.
- Part E's E.3 names `board/forge_read.py`; it becomes `connectors` (its specification follows).
  E.7 question 1 (the hub reading backlog CRs' waits) stays Part E's.

## 8. Evidence

- `tests/test_connectors.py` (new; `test_board_forge_read.py`'s cases move into it, parametrized
  over the two connectors):
  - a link is claimed by its connector and by no other (GitHub by `PR_LINK`, GitLab by
    `GITLAB_LINK`); a link neither claims gives `connector_for` None and `read` the `UNCLAIMED`
    text;
  - the argv is `api graphql` with a `query` and no `mutation`; on a non-default host (a GitHub
    Enterprise link, a self-managed GitLab link) it is `api --hostname <host> graphql ...` and the
    guard accepts it (SC-1);
  - with no optional fact asked, the query text equals today's (a golden string per forge, kept
    in the test); with `review` asked, the GitHub query holds `reviewDecision` and each of its four
    answers (`APPROVED`, `CHANGES_REQUESTED`, `REVIEW_REQUIRED`, null) maps to §3.2's word
    (`unknown` for null); the GitLab query is unchanged and every MR's `review` is `unproved`;
  - a recorded answer gives today's `Facts` (the moved cases);
  - `run.py`'s guard raises on a prepared argv with a mutation, and on one that is not `api
    [--hostname <host>] graphql` (cases the shipped code cannot produce, paired with the shipped
    connectors' argv checked above).
- `tests/test_forge_hub.py`: every existing test passes, the seam now `connectors.read`; new,
  parametrized: a batch with one PR link of no forge: the entry's `error` is the `UNCLAIMED` text
  and the batch's other PRs are read (one call naming them) and judged; a batch whose PRs span two
  repositories: no read, `NOT_ONE_REPOSITORY` in the entry, as today; two providers' `pr`
  interests on one repository make one call (a test provider added to `PROVIDERS` by
  `monkeypatch`); a provider of another kind only (a test provider with kinds `{"other"}`) is not
  called by the hub and makes no forge call.
- `tests/test_board_prs.py`: a batch with one unclaimed link: the page's error line is the
  `UNCLAIMED` text and the other rows are read.
- The GitHub `review` proof (SC-8, §3.2): the two real reads, recorded in the CR's evidence before
  the PR is ready; no fake forge stands for it.
- Cards and docs guarded as they ship: `test_plugin_files.py` and `test_startup_manifest.py` read
  the shipped cards at the head under test; no prepared copy.
- `just check`, `just test` within its budget (AGENTS.md: at most 30 s above 18.5 s), `just
  eval-dry-run` (the change is under the CLI's `src/`).
- Scenario, `just scenario`, green on the pipeline's `just scenario (ubuntu-latest)` job, and
  locally on Windows (`chantier gate`) when this CR is the top of its batch: unit
  `surface-board`, case `forge_hub`: its existing checks hold (one `api graphql` call per
  project with an open PR, no mutation, the record unchanged), the seam's move proved end to end
  through the fake `gh`.
- Forge matrix (the change depends on the forge, not on the host or a configured value):

| Forge | Cell | Expected |
| --- | --- | --- |
| GitHub | the hub with a running batch, no `review` asked | one query per cycle, today's text |
| GitHub | an interest asks `review` (test provider) | the same one query, with `reviewDecision` |
| GitHub | a non-default host (Enterprise) | `api --hostname <host> graphql`, accepted by the guard |
| GitLab | the hub with a running batch | one query per cycle, today's text |
| GitLab | an interest asks `review` | the same query; `review: unproved` |
| any | a link no connector claims | not read; the entry's error and the page's line name it; the other PRs read |
| any | PRs in two repositories | no read; `NOT_ONE_REPOSITORY` in the entry, as today |

- No CI job is added or changed.

## 9. Out of scope

- Webhooks, or any push from a forge: polling only (the user's words).
- **Moved to `1-inbox/outside-poller` (SC-11):** the outside poller and its entries
  (`chantier interests`, `chantier journal add`), the `issue@1` type and the `poller` source, the
  `issues` provider (the CRs' `issue:` lines), AGENTS.md's journal and named-exception lines and
  its watcher sentence (SC-3, SC-4), the "Writing an outside poller" doc, the `outside_poller`
  scenario case, FC-2, FC-3, FC-4, FC-7, and SC-7 (an issue two CRs name: a `folders` field; any
  key outside the payload's list refused).
- The hub reading issues, comments or any tracker.
- A Jira, Gitea or other connector: the interface and the table make one easy; none ships here.
- Loading connectors from outside chantier's package (Python entry points, executables named in
  `chantier.yaml`) (FC-1).
- A token or an HTTP library for the forge (FC-8).
- More than one query per project and cycle, and reading PRs of several repositories in one
  project (SC-2).
- The Driver-side forge commands (`forge-stack`, `ship`'s and `take`'s base reads in
  `commands/forge_base.py`, `forge_stack*.py`), which write to the forge: they keep calling `gh`
  and `glab` directly.
- `board/forge_kind.py` (the board's PR/MR word).
- Typed waits themselves, `wait-cleared@1`, and the GitLab approval proof: Part E.
- Narrowing the batch's PR set below today's (merged bases are kept for the landed rule; they
  cost no query).

## 10. Open questions for the user

None. The first draft's nine questions are settled in this CR's `02-answers.md` (FC-1 to FC-9),
and the spec critic's eleven points in the same file (SC-1 to SC-11); §2 carries them.
