# Change Specification: an outside poller writes issue events into the journal

Origin: verbal (2026-11-20, the user's answer planning-server-Q24, in `planning-server`'s grill;
split off `forge-connectors` by its spec critic the same day). No tracker issue.

Its decisions come from the user's words recorded in
`../../2-backlog/P3/planning-server/02-answers.md` ("2026-11-20, the user: forge monitoring and
connectors", and planning-server-Q24), from `../forge-connectors/02-answers.md` (FC-2, FC-3, FC-4
and FC-7, and the spec critic's point 7, cited SC-7, which moved here with the split, SC-11), from
this CR's own `02-answers.md` (three points settled by the Chief of Staff on 2026-11-20, cited
OP-1 to OP-3), from
Part A's specification and answers (`../typed-journal-events/03-change-spec.md` and
`02-answers.md`), which rank for the `issue@1` type, from the project's `AGENTS.md`, and from the
code as it is at `8bd198b1`. Its first text is `forge-connectors`' specification at surface commit
`7fd03eab` (§4.2 `issues`, §5, §7.1 edits 2 and 3, "Writing an outside poller", the scenario case
`outside_poller`); this file is self-contained: a Driver needs nothing else, but the two CRs it
builds on (§2).

## 1. Goal, in the user's terms

> Pour les d'événements sur les issues je penses que je ferais un polling extérieur.

- **Issues are polled from outside.** chantier's forge hub never reads an issue. An outside poller
  (the user's own program: a script, a cron job, a scheduled task, a service) asks chantier which
  issues are awaited, polls its tracker (Jira, GitHub, GitLab, any other) for them, and writes what
  it finds into the project's journal through one CLI entry.
- **Who waits for an issue** is a CR whose intent or specification names it on its `issue:` line.
  An event on an issue no CR names is refused: nobody waits for it.
- **The Chief of Staff hears of it** as of a merge: the session's watcher prints the line and
  ends on it, unless the poller says the event wakes no one.

chantier gives the poller two entries, `chantier interests` and `chantier journal add`, and
nothing else: it never starts, stops, supervises or ships a poller.

## 2. Dependencies

`depends.json`: `{"after": ["typed-journal-events", "forge-connectors"]}` (OP-1).

- **`typed-journal-events` (Part A)**: this CR publishes one type, `issue@1`, as
  one entry of `hub/schemas.py`'s `PUBLISHED` (its model, its wake rule, its text, its duplicate
  key, one example payload) and its entry in the shipped `hub/schemas.json` through `just
  journal-schemas`, and adds one source, `poller`, to `hub/journal.py`'s `SOURCES`. It changes no
  reader or writer of Part A otherwise.
- **`forge-connectors`**: this CR reuses its interest registry and provider seam (`hub/interests.py`:
  `Interest`, `Provider` with `kinds`, `PROVIDERS`, `collect(repo, kinds)`) and adds one provider,
  `issues`, of kind `issue`. The forge hub calls `collect(repo, kinds={"pr"})` (forge-connectors
  §3.3, its SC-6), so it never calls this provider: the hub's reads and budget do not change.
  `forge-connectors` also creates `docs/forge-connectors.md` and the concepts word **Interest**,
  which this CR extends.

## 3. Decisions carried

| Decision (source, date) | Where it lands |
| --- | --- |
| Events on issues: polled from outside, not by chantier's hub (Q24 grill, 11-20) | §4: the hub never collects `issues`; §5, §6: the two entries |
| Q24: an entry for an outside poller that writes into the journal (11-20) | §6 `journal add` |
| FC-2: only the outside poller reads issues; the registry lists the issues the CRs' `issue:` lines name; the hub's budget does not change | §4 (provider `issues`, never collected by the hub); §9.1: AGENTS.md's hub sentences untouched |
| FC-3: `journal add` accepts only `issue@1` | §6.2 refusal 1 |
| FC-4: an event on an issue no CR names is refused, nothing written | §6.2 refusal 4 |
| FC-7: an issue event wakes the watcher as the poller says, default yes | §6.1 `wakes`; §7.1 wake rule |
| SC-7: the line names every CR folder that names the issue, in a field `folders`, not `cr`; `journal add` refuses a payload with any key outside its list (`cr`, `type`, `source`, `audience` included), exit 1, nothing written | §6.1 (`folders` filled by the CLI), §6.2 refusal 3, §7.1 model |
| SC-11: the outside-poller half of `forge-connectors` (`interests`, `journal add`, `issue@1`, the `issues` provider, AGENTS.md edits 2 and 3, its doc and scenario case) is this CR, after `typed-journal-events` | this CR |
| SC-3 and SC-4 (moved here): AGENTS.md's watcher sentence and the "Two named exceptions" sentence of "The CLI's scope" are this CR's | §9.1 edits 2 and 3 |
| Part A: a published type is one `PUBLISHED` entry (model, wake, text, duplicate key, example) plus its `schemas.json` entry by `just journal-schemas`; a new source is one more value of `SOURCES` | §7.1 |
| Part A, answer 1: a model fixes each field's JSON type and only the formats that cannot change; open sets stay plain strings | §7.1: the published model is open; the entry's closed lists live in `journal add`'s input check (§6.1, OP-2) |
| Part A, critic 1: from a CLI command a refused event stays a code fault (`ValueError`) | §6.1: the entry checks the payload before `append`, so `append` never refuses it but by a code fault |
| AGENTS.md: every journal line goes through the one append function | §6.1: `journal.append(repo, [event], "poller")` |
| AGENTS.md: a new CLI tool comes from measured token cost, or is a named exception | §9.1 edit 3: `interests` and `journal add` named, citing Q24 |
| AGENTS.md: no fallback | §6.2: an unknown issue, an unknown type, a refused payload are refused, never written another way |
| Critic (11-20, brief): `interests` says what it prints when a provider raises | §5 |
| OP-1: `forge-connectors` joins `depends.json` (its registry, provider seam and `connector_for`) | §2 |
| OP-2: the published `issue@1` model keeps its fields plain strings (Part A's answer 1); `journal add`'s own input check holds the closed lists, so a new word is a CLI change, never an `issue@2` | §6.1 step 3, §7.1 |
| OP-3: `interests` when a provider fails: the partial list plus one failure line per provider, exit 2; `journal add` then refuses and writes nothing | §5, §6.2 refusal 5 |

## 4. The `issues` provider

New module `skills/chantier/scripts/cli/src/chantier/hub/issue_refs.py`, provider `issues`, kinds
`{"issue"}`, one line added to `PROVIDERS` in `hub/interests.py` (after `batch`).

- `Interest.kind` gains the value `issue` (forge-connectors defines only `pr` and leaves the field
  for this kind). An `issue` interest: `ref` the link of the CR folder's `issue:` line, exactly as
  written; `facts` `{"events"}`; `by` the folder's path relative to the planning folder's
  `changes/`, with `/` separators (`1-inbox/export-columns`, `2-backlog/P2/login-fix`,
  `4-batch/2-actives/3-login-fix`); `provider` `issues`.
- `collect(repo)`: one interest per CR folder of `lifecycle/stages.py`'s `cr_folders(stage_layout(repo))`
  (`1-inbox/`, `2-backlog/P1`...`P4/`, `3-ready/`, `4-batch/1-pending`, `2-actives`, `3-done`, in
  that order, each stage by name; `5-archives/` and `6-trash/` are not read) whose
  `summaries/origin.py`'s `issue_url(folder)` is not None (the first `issue:` line of
  `01-intent.md`, else of `03-change-spec.md`). A folder with no such line gives none.
- The tracker word of an interest: today's private `_kind_of(host, path)` of `summaries/origin.py`,
  made public as `tracker_of(url) -> str | None` (no change of rule; `origin_of` calls it), giving
  `jira`, `gitlab` or `github`; None gives `other`. It is a field of the `Interest`'s output only
  (`interests` and its JSON); `Interest` gains an optional `tracker: str | None` (None for `pr`).
- `judge`: returns `[]`; nothing is read for it.
- Two CR folders naming one issue give two interests (their `by` differ), as forge-connectors'
  `collect` keeps two interests on one `ref`.
- Reading it writes nothing, takes no lock and needs no network. A file it cannot read
  (`OSError` from `issue_url`) propagates as a failure of the provider (§5).

## 5. `chantier interests`

New command: parser `skills/chantier/scripts/cli/src/chantier/declare/interests.py`
(`add_command(sub, "interests", "chantier.hub.interests:show", HELP, NO_BATCH)`), registered in
`cli.py`'s tuple of modules, and added to `cli.py`'s `FULL_OUTPUT` (its list is useless cut at ten
lines). Read-only, no network, no lock.

```
chantier --project <p> interests [--kind pr|issue] [--json]
```

HELP: "what the CRs of this project wait for: the running batch's PRs or MRs, which the forge hub
reads, and the issues the CRs' issue: lines name, which only an outside poller reads; --json is
the poller's input".

It calls a new `collect_each(repo, kinds) -> tuple[list[Interest], list[tuple[str, str]]]` of
`hub/interests.py`: `collect`'s interests, in its order, plus one `(provider name, one line)` per
provider that raised `ChantierError` or `OSError` (the error's first line), whose interests are
then absent; any other exception is a code fault and propagates. `kinds` is `{"pr", "issue"}`, or
the one `--kind` gives. `collect` (the hub's call) is unchanged.

**Text** (UTF-8, one line each):

- first: `interests of <project>: <n>`, `<n>` the interests listed;
- then one line per interest, in order:
  - `pr <link> (<connector>): <facts, comma-separated, sorted> for <by>`, `<connector>` the name of
    `connectors.connector_for(link)`, or `no connector` when it is None;
  - `issue <link> (<tracker>): events for <by>`;
- with none and no failure: the first line is `interests of <project>: 0 (nothing awaited)`;
- then one line per failure: `interests: <provider> not read: <one line>`.

**`--json`**: one JSON object, keys sorted, UTF-8, `ensure_ascii=False`, one line:

```json
{"errors": [], "interests": [{"by": "2-backlog/P2/export-columns", "facts": ["events"], "kind": "issue", "read_by": "outside", "ref": "https://acme.atlassian.net/browse/PAY-12", "tracker": "jira"}], "project": "demo", "schema": 1}
```

- each interest: `kind`, `ref`, `facts` (sorted), `by`, `read_by` (`hub` for `pr`, `outside` for
  `issue`), and `connector` (the name, or null) for `pr`, `tracker` for `issue`;
- `errors`: `[{"provider": "<name>", "text": "<one line>"}]`, empty with none.

**Exit**: 0 when every provider answered (with or without interests); 2 (`EXIT_PRECONDITION`)
when one failed, after printing everything above (the list is incomplete; a poller that reads
exit 2 knows it) (OP-3).

`--kind` other than `pr` or `issue`: argparse's usage error, exit 2 as argparse gives.

## 6. `chantier journal add`

New command: parser `skills/chantier/scripts/cli/src/chantier/declare/journal.py`
(`add_command(sub, "journal", "chantier.hub.journal_add:needs_action", HELP, NO_BATCH)` with one
action `add`, declared as `declare/summary.py` declares its actions: `--project` accepted after
it), handler `skills/chantier/scripts/cli/src/chantier/hub/journal_add.py:add`, registered in
`cli.py`. HELP: "append one event an outside poller read on a tracker to this project's journal:
only issue@1, only for an issue a CR's issue: line names; --json - reads the payload from stdin".

```
chantier --project <p> journal add <type> --json <payload | ->
```

### 6.1 What it does

1. `<type>` must be `issue@1` (refusal 1).
2. The payload: the `--json` value, or with `-` the whole of stdin, read as bytes and decoded
   `utf-8-sig` (a leading BOM, as PowerShell may write, is dropped). Parsed with `json.loads`
   (refusal 2).
3. Checked by the entry's input model, `IssueInput` in `hub/journal_add.py` (not published;
   `ConfigDict(extra="forbid", frozen=True)`), the poller's list and nothing else (refusal 3):
   - `tracker`: one of `jira`, `github`, `gitlab`, `other`;
   - `ref`: a non-empty string, the issue's link as `interests` prints it;
   - `event`: one of `opened`, `commented`, `changed`, `closed`, `reopened`;
   - `at`: the tracker's time of the event, a string `datetime.fromisoformat` reads (ISO 8601;
     `Z` accepted, Python 3.11), kept as given;
   - `text`: one line (no `\r` or `\n`), 1 to 300 characters: what happened, in the poller's words;
   - `wakes`: a strict boolean, default `true`.
   Any other key is refused, `cr`, `type`, `source`, `audience`, `folders`, `v`, `seq` and `t`
   included (SC-7): the CLI fills `folders`, `append` the header.
4. The interests: `collect_each(repo, {"issue"})`. A failure of the `issues` provider: refusal 5.
   `folders` is the `by` of every `issue` interest whose `ref` equals the payload's `ref` (exact
   string equality), in `collect`'s order. None: refusal 4.
5. The event `{"type": "issue@1", "audience": ["project"], tracker, ref, event, at, text, wakes,
   folders}` goes through `journal.append(repo, [event], "poller")`: the one append function, under
   the project's lifecycle lock, its `seq`, its duplicate rule. `poller` is the new value of
   `SOURCES`. Having passed step 3, the event is one the published model accepts; a `ValueError`
   from `append` is a code fault (Part A, critic 1) and is not caught.
6. Output, exit 0:
   - written: `journal: seq <n> issue@1 <event> on <ref> (<folders, joined by ", ">)`;
   - a duplicate (same `ref`, `event` and `at` already in the journal, whoever wrote it, whatever
     its `folders`): `append` writes nothing; the handler reads the journal and prints `journal:
     already there (seq <n>)`, `<n>` the `seq` of the line with the same duplicate key.

The journal is the project's `forge-journal.jsonl` at the planning folder's root: local, ignored
by git, never published (in external mode, the project's folder of the surface). Writing it needs
no network, no surface writer (planning-server's Part C writes published paths only) and no seat.

### 6.2 Refusals, nothing written

Checked in the order of §6.1; the first that applies is printed, on stderr as every
`ChantierError`:

| # | Case | Text | Exit |
| --- | --- | --- | --- |
| 1 | a type other than `issue@1` (FC-3) | `journal add: <type> is not written from outside; an outside poller writes issue@1` | 2 |
| 2 | not JSON, or stdin not UTF-8 | `journal add: --json is not JSON: <the parser's or decoder's one line>` | 1 |
| 3 | a payload `IssueInput` refuses: not an object, a missing field, a key outside the list (SC-7), an unknown `tracker` or `event`, an `at` that is no ISO time, a `text` of two lines, empty or over 300 characters, a `wakes` that is no boolean | `journal add: issue@1 payload refused: <field>: <pydantic's first error's message>` (`<field>` the error's `loc` joined by `.`, or `payload` for the whole) | 1 |
| 4 | a `ref` no `issue` interest names (FC-4) | `journal add: <ref> is no CR's issue (chantier interests --kind issue lists them): nothing written` | 2 |
| 5 | the `issues` provider failed | `journal add: the CRs' issue: lines could not be read (<one line>): nothing written` | 2 |

Exit codes are `core/errors.py`'s: 1 `EXIT_USAGE`, 2 `EXIT_PRECONDITION`.

## 7. The type `issue@1` and the line

### 7.1 Its `PUBLISHED` entry (Part A's form)

In `hub/schemas.py`:

- **Model** `IssueV1` (`ConfigDict(extra="forbid", frozen=True)`, as Part A's models): `tracker:
  str`, `ref: str`, `event: str`, `at: str`, `text: str`, `wakes: bool`, `folders: list[str]`,
  every field required, no pattern, no enum (Part A, answer 1: these are open sets or plain
  texts; the closed lists of §6.1 are the entry's, so a new tracker or event word needs no
  `issue@2`; OP-2).
- **Wake rule**: by the field `wakes` (as `board@1`).
- **Text** (`issue_text`, which `event_text` calls for the name `issue`): `tracker saw <event> on
  <ref> (<folders, joined by ", ">): "<text>"; for the Chief of Staff: tell the user in one line,
  record nothing`.
- **Duplicate key**: `("issue", ref, event, at)`.
- **Example payload**: `{"tracker": "jira", "ref": "https://acme.atlassian.net/browse/PAY-12",
  "event": "commented", "at": "2026-11-20T09:14:00Z", "text": "a comment asks to keep the old
  column order", "wakes": true, "folders": ["2-backlog/P2/export-columns"]}`.
- `schemas.json`: its entry added by running `just journal-schemas` once (it prints
  `schemas.json: added issue@1`); no existing entry changes.

The line, version 2, as Part A writes it:

```json
{"v":2,"seq":57,"t":"2026-11-20T09:15:02Z","type":"issue@1","source":"poller","audience":["project"],"tracker":"jira","ref":"https://acme.atlassian.net/browse/PAY-12","event":"commented","at":"2026-11-20T09:14:00Z","text":"a comment asks to keep the old column order","wakes":true,"folders":["2-backlog/P2/export-columns"]}
```

### 7.2 How it is read

- `chantier watch` prints its text and, with `wakes` true, ends on it as on a merge (20 s after
  the last waking line, no sooner than `events.wake_every`); with `wakes` false it rides along with
  the next waking line, as a `board@1` line that does not wake. `watch --once --after <seq>` (the
  pull path) prints it as any line past the cursor.
- `status` lists no `issue@1` line (`journal.lines` lists only `merged@1` and the slots
  `config@1` line): there is nothing to record, so nothing to clear.
- An earlier chantier reading the journal sees a version 2 line (Part A's rollout): it counts it
  for `seq` and wakes no one. A chantier with Part A but not this CR sees a type it does not know:
  `status` prints Part A's `forge-journal.jsonl: line <n> is of type issue@1, unknown to this
  chantier: update it`.
- The hub, the board and the PRs page do nothing with it.

## 8. Messages, every one

| Where | Text |
| --- | --- |
| `interests`, text | `interests of <project>: <n>`; `interests of <project>: 0 (nothing awaited)`; `pr <link> (<connector>): <facts> for <by>` (`no connector` when none claims the link); `issue <link> (<tracker>): events for <by>`; `interests: <provider> not read: <one line>` |
| `journal add`, written | `journal: seq <n> issue@1 <event> on <ref> (<folders>)` |
| `journal add`, duplicate | `journal: already there (seq <n>)` |
| `journal add`, refusals | the five texts of §6.2 |
| watcher, `watch --once` | `tracker saw <event> on <ref> (<folders>): "<text>"; for the Chief of Staff: tell the user in one line, record nothing` |

Every existing text is unchanged.

## 9. Project rules, cards and docs

### 9.1 `AGENTS.md` (chantier's own; the user's merge of the PR is their approval)

Three edits, each made at the CR's rebased head, so that they compose with the pending CRs that
edit the same sentences (`planning-server`, `typed-waits`, `driver-leases`, `explain-access`,
`forge-connectors`):

1. **The journal** (forge-connectors' §7.1 edit 2 of `7fd03eab`, FC-9). After "every journal
   line, the CLI commands' included in their own process, goes through the one append function"
   add: "; an outside poller (the user's own program, never started by chantier) writes into a
   project's journal only through `journal add`, only `issue@1` lines, and only for an issue a
   CR's `issue:` line names".
2. **The watcher's sentence** (SC-3). The parenthesis of "reads only its project's journal (the
   hub's lines and the board's), never the forge" gains, as its last item, "an outside poller's
   `issue@1` lines", joined by the list's own "and". Today it becomes "(the hub's lines, the
   board's and an outside poller's `issue@1` lines)"; after planning-server's C.11 edit ("(the
   hub's lines, the board's and the writer's)") it is "(the hub's lines, the board's, the
   writer's and an outside poller's `issue@1` lines)". Whichever lands later rebases and keeps the
   other's item.
3. **"The CLI's scope", the named exceptions** (forge-connectors' §7.1 edit 3 of `7fd03eab`;
   SC-4). This CR adds one item, in the same form and place as the other named commands' items
   stand at its rebased head (`driver-leases`' `lease`, `typed-waits`' `wait`, `explain-access`'s
   `access`, those that have landed); with none landed, the item is a sentence of its own right
   after "never from speculation". It reads: "`interests` and `journal add`: `interests` lists,
   read-only, what the CRs wait for (the running batch's PRs or MRs, read by the forge hub, and the
   issues the CRs' `issue:` lines name, read by an outside poller only); `journal add` is the one
   entry by which an outside poller appends an `issue@1` line to a project's journal; built on the
   user's answer planning-server-Q24 (2026-11-20: issues polled from outside), with no measured
   cost". When the sentence states a count ("Two named exceptions", "Three ...") or orders its
   items ("First", "Second", ...), the count becomes the number of items the text names once this
   one is in, counted again at the rebased head (this item counts as one), never incremented from a
   remembered number, and this item takes the next ordinal, as `explain-access`' §6.3 states the
   same rule.

Not changed: the write list ("chantier writes only in the planning folder"; the journal is in it),
the no-setup and network sentence (no network), the git exceptions (no git), the hub's sentences
and its budget (FC-2: the hub never collects `issues`), "the CLI knows no role" (no role named).

`CONTRIBUTING.md`, the surface server's paragraph (it mirrors AGENTS.md): "reads only its
project's journal (the hub's lines and the board's writes)" takes edit 2's item ("the hub's lines,
the board's writes and an outside poller's `issue@1` lines", composed as above), and "every journal
line, the CLI commands' included in their own process, goes through the one append function" takes
edit 1's clause. "A new CLI tool comes only from measured token-costly behaviour of the agents"
gains ", or is one of AGENTS.md's named exceptions".

### 9.2 Cards

- `skills/chantier/references/chief-of-staff.md`, **The watcher** (off the common path, as the
  card keeps watcher detail):
  - its first sentence, "It prints the project's forge events (`forge saw merged`, `forge saw
    checks red`) and what the user does in the board (`board wrote`, `config changed on the
    board`)", adds "and the issue events an outside poller writes (`tracker saw`)";
  - *A watcher's end*, after the `board wrote` sentence: "A `tracker saw ...` line (an outside
    poller's issue event): one line to the user that says it, no tool call, record nothing.";
  - *The pull path*: "Tell its `board wrote` and role `config@1` lines as above" (Part A's words)
    becomes "Tell its `board wrote`, `tracker saw` and role `config@1` lines as above".
- `skills/chantier/references/concepts.md`, the word **Interest** forge-connectors adds ("a PR or
  MR someone waits for; the forge hub reads only those") becomes: "a PR or MR, or a tracker issue
  a CR's `issue:` line names, that someone waits for; `chantier interests` lists them; the forge
  hub reads only the PRs and MRs, an outside poller (the user's own program) the issues, and
  writes their events with `chantier journal add`".
- `hosts/claude-code.md`, `hosts/copilot.md`, `session-start.md`, `routing.md`,
  `startup-manifest.json`: unchanged (no new trial: an `issue@1` line wakes the watcher by the
  same rule as a `board@1` line, already covered by their rows' trials; the Driver checks no text
  of theirs is made false).
- `agents/` and `com.github.copilot/agents/`: no change (no role changes).

### 9.3 CLI texts

- `declare/watch.py`'s HELP: "the forge's (merges, CI red on a PR ready to merge) and the board's
  writes (backlog, configuration)" adds ", and the issue events an outside poller writes".
- `hub/watch.py`'s module docstring: "the forge's (merges, CI red) and the board's writes" adds
  "and an outside poller's issue events".
- `hub/journal.py`'s module docstring (as Part A rewrites it): `poller` among the sources (an
  outside poller, through `journal add`), `issue@1` among the published types.

### 9.4 Docs (every file this CR makes false or must name it)

- **`docs/forge-connectors.md`** (created by `forge-connectors`): the registry section adds the
  `issue` kind (read by an outside poller only, never by the hub); a new section **"Writing an
  outside poller"**:
  - the contract: run `chantier --project <p> interests --kind issue --json`, poll your tracker
    for each `ref` (once per `ref`: two CRs may name one issue), then one `chantier --project <p>
    journal add issue@1 --json -` per event, the payload on stdin; a duplicate is harmless (`already
    there`); a refusal is printed and nothing is written; exit 2 of `interests` means its list is
    incomplete (its `errors`);
  - the payload table (§6.1 step 3) and the line it gives (§7.1);
  - the rules: chantier never starts, stops or supervises the poller; read-only on the tracker
    and its credentials are the poller's business; chantier sets no rate; keep `at` as the tracker
    gives it (the duplicate key is `ref`, `event`, `at`); `text` one line, no personal data needed;
    run from the project's root, or the surface's root with `--project <name>`;
  - one short Python example (UTF-8, standard library only), with a placeholder `fetch_events` the
    user writes for their tracker:

    ```python
    import json
    import subprocess
    import time

    CHANTIER = ["uvx", "--from", "<chantier's plugin folder>", "chantier", "--project", "<project>"]

    def fetch_events(tracker: str, ref: str) -> list[dict]:
        """Yours: this issue's events since your last poll, each {"event", "at", "text"}."""
        return []

    while True:
        out = subprocess.run([*CHANTIER, "interests", "--kind", "issue", "--json"],
                             capture_output=True, text=True, encoding="utf-8")
        refs = {i["ref"]: i["tracker"] for i in json.loads(out.stdout)["interests"]}
        for ref, tracker in refs.items():
            for e in fetch_events(tracker, ref):
                payload = json.dumps({"tracker": tracker, "ref": ref, **e})
                subprocess.run([*CHANTIER, "journal", "add", "issue@1", "--json", "-"],
                               input=payload, text=True, encoding="utf-8")
        time.sleep(300)
    ```
- `README.md`, the docs list line forge-connectors adds: "how chantier reads a forge, and how to
  add a connector" becomes "how chantier reads a forge, how to add a connector, and an outside
  poller for issues".
- `docs/hosts.md`, the sentence forge-connectors adds under the forge table: adds "issues of any
  tracker come from an outside poller ([forge connectors](forge-connectors.md#writing-an-outside-poller))".
- `docs/planning-folder.md`, "The event journal" (with Part A's text in place):
  - the first paragraph: "the forge's (...) and the board's writes" adds "and the issue events an
    outside poller writes";
  - the `source` row adds "`poller` (an outside poller, through `chantier journal add`)";
  - Part A's "Type | Written by | Wakes a watcher" table gains the row `issue@1` | an outside
    poller, through `chantier journal add`, only for an issue a CR's `issue:` line names | when
    `wakes` (default true);
  - "Every line written today is for `["project"]`" names `issue@1` by an outside poller.
- `docs/web-board.md`, "Starting the board", the forge hub's sentence (as forge-connectors leaves
  it, "... only the PRs a running batch waits for") adds "(`chantier interests --kind pr` lists
  them); it never reads an issue".
- `scenario/README.md`, "Coverage": one bullet for the new case (§10.2), naming its unit and
  tests, as `test_scenario_coverage.py` checks.
- **SVGs: none changes.** Searched every `docs/*.svg` and `docs/*-texts.md` for journal, watcher,
  hub, poll, tracker and issue: the hits are the intake's sources ("a Jira issue, a GitLab or
  GitHub issue" in `cr-folder-lifecycle`, `cr-lifecycle`, `cr-lifecycle-simple`) and
  `planning-modes`' "the tracker keeps the strategic, long-term plan": all still true (a request
  is still filed from an issue; a poller reports events on an issue a CR already names, it files
  nothing). No diagram draws the journal, the hub or the watcher; this CR adds none, so no
  `-texts.md` or `<desc>` changes.
- Searched and unaffected: `docs/boards.md` (the pane's `STATUS.json` fields do not change: no
  screenshot owed), `docs/planning-modes.md`, `docs/use-cases*.md`, `docs/gates.md`,
  `docs/costs.md`, `docs/tutorial-claude-code.md`. `docs/release-notes/` is history.

## 10. Evidence

### 10.1 Tests (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized)

- **New `test_outside_poller.py`**, on a prepared planning folder (a CR in `1-inbox/` and one in
  `2-backlog/P2/` naming one Jira link, one in `3-ready/` naming a GitHub issue, one in
  `5-archives/` and one in `6-trash/` naming a third link, one with no `issue:` line):
  - `interests --kind issue --json`: the two folders of the Jira link (two interests, one `ref`),
    the GitHub one, nothing of `5-archives` or `6-trash`, trackers `jira` and `github`, `read_by`
    `outside`, `errors` empty, exit 0; the text form's first line and one line per interest; an
    unplaceable link gives `other`; `interests` with no `--kind` also lists a running batch's PRs
    (`read_by` `hub`, through forge-connectors' `batch` provider; a link no connector claims shows
    `no connector`); with nothing awaited, `interests of <p>: 0 (nothing awaited)`; it writes
    nothing (the tree's fingerprint unchanged, as `test_validate.py` checks);
  - a failing provider (an `issue_url` patched to raise `OSError`: a case the shipped files cannot
    produce, named as such): `interests` prints the others and `interests: issues not read: ...`,
    `errors` in the JSON, exit 2; `journal add` refuses with refusal 5, nothing written;
  - `journal add issue@1 --json -` (stdin, with and without a UTF-8 BOM) on the Jira link writes
    one version 2 line, `source` `poller`, audience `["project"]`, `folders` the two folders in
    order, `wakes` true by default, and prints the written text; the same `(ref, event, at)` again
    (another `text`) writes nothing and prints `already there (seq <n>)`;
  - parametrized refusals, each exit code and text of §6.2 and the journal absent or unchanged:
    `merged@1` (2); not JSON (1); each extra key `cr`, `type`, `source`, `audience`, `folders`
    (1); a missing `ref`; an unknown `event` and `tracker`; `at` `yesterday`; a two-line, an empty
    and a 301-character `text`; `wakes` `"yes"` (1); a ref no CR names, and the archived CR's ref
    (2).
- **`test_watch_events.py`**: a watcher's `poll` ends on an `issue@1` line with `wakes` true and
  prints its text; with `wakes` false it does not end on it and prints it with the next waking
  line; `watch --once --after <n>` prints it; `status` prints no line for it.
- **`test_forge_hub.py`**: with only `issue` interests in a project (CRs with `issue:` lines, no
  running batch), a hub cycle makes no forge call and the `issues` provider's `collect` is never
  called (a spy on it).
- **Part A's `test_event_types.py`** covers `issue@1` with no change to the test: it is one entry
  of `PUBLISHED`, its example appends, an extra or a missing field raises, a second append is
  skipped (its duplicate key is not none), and the shipped `hub/schemas.json`, read from the
  repository at the head under test, holds its normalized form. `just journal-schemas` at the PR's
  head prints nothing and leaves `git status` clean.
- **`test_event_audience.py`**'s `test_no_role_is_named_and_the_journal_has_one_writer` keeps
  holding: `journal_add.py` writes only through `journal.append`.
- Cards and docs as they ship: `test_plugin_files.py`, `test_startup_manifest.py` and
  `test_scenario_coverage.py` read the shipped cards, `scenario/README.md` and the runner at the
  head under test; no prepared copy.
- **Test budget**: `just test` stays within AGENTS.md's (at most 30 s above 18.5 s); this CR's
  tests add at most 2 s, measured by the Driver (`just test` before and after, on the same
  machine) and recorded in the PR's evidence.

### 10.2 Scenario

`just scenario`, green on the pipeline's `just scenario (ubuntu-latest)` job at the PR's head, and
locally on Windows (`chantier gate`) when this CR is the top of its batch's stack.

New case `outside_poller` in unit `surface-board` (`scenario/run_scenario.py`, `UNITS`), on a
`SurfaceWorld` with the fake `gh`:

1. Two CRs filed with the same `issue:` line (a Jira link): one in `1-inbox/`, one triaged to
   `2-backlog/P2/`. `interests --kind issue --json` lists the link twice, `tracker` `jira`,
   `read_by` `outside`, exit 0.
2. A watcher started in the background with the test times (as `forge_hub` does,
   `CHANTIER_HUB_TEST_TIMES`); the scenario, as the poller, runs `journal add issue@1 --json -`
   with the payload on stdin: exit 0, `journal: seq <n> issue@1 commented on <link> (1-inbox/...,
   2-backlog/P2/...)`; the watcher ends and its output holds the `tracker saw commented on <link>
   (...)` line.
3. The same add again: `journal: already there (seq <n>)`, the journal unchanged.
4. A ref no CR names: exit 2, refusal 4's text; a payload with a `cr` key: exit 1; type `merged@1`:
   exit 2; the journal unchanged after each.
5. No `gh` call during the case (the fake `gh`'s call log unchanged): the hub read no issue.

Its budget: the case runs in under 20 s on the pipeline (one watcher end at the test times); the
unit's literal (500 s) is raised by the measured time only if the unit's measured total passes it,
the measure recorded in the PR's evidence.

### 10.3 Gates

`just check`; `just test` within its budget; `just eval-dry-run` (the change is under the CLI's
`src/`); `just scenario` as above. No CI job is added or changed.

### 10.4 Matrix

Host and default matrix: none. What this CR changes depends neither on the host (Claude Code or
Copilot: the watcher's wake is the host's, unchanged, and an `issue@1` line wakes by the same rule
as a `board@1` line) nor on a configured value (no configuration key). The one default is the
payload's `wakes` (true), proved both ways in §10.1. The stdin read is portable (bytes decoded
`utf-8-sig`), proved on Windows by the local `chantier gate` run and in §10.1 with a BOM.

## 11. Out of scope

- The hub, the board or any chantier process reading an issue, a comment or any tracker (FC-2).
- Starting, supervising, scheduling or shipping a poller; a poller in chantier's package.
- `journal add` for any type but `issue@1` (FC-3); a CLI entry to write a forge or board event.
- Events on an issue no CR names (FC-4), or on a CR of `5-archives/` or `6-trash/`.
- Any action on an `issue@1` line beyond telling the user: no record, no order, no status line.
- Reading more than the first `issue:` line of a CR (today's `issue_url`).
- Matching links loosely (case, trailing slash, `http` versus `https`): the `ref` is the CR's line,
  exactly as `interests` prints it.
- The connectors, the registry's `pr` side, the hub's budget, the `review` fact: `forge-connectors`.
- Typed waits on an issue: `typed-waits` (Part E).

## 12. Open questions for the user

None. The three questions of the first draft are settled in this CR's `02-answers.md` (OP-1 to
OP-3), each as recommended; §3 carries them.
