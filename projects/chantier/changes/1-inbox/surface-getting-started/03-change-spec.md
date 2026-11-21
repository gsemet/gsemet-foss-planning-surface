# Getting started on a new, empty planning surface

Spec v1 (2026-11-21), from `intake/request.md` and `01-intent.md`. No grill was held (the user
delegated tonight's questions); every open choice is a numbered question at the end, and the text
below is written on each question's recommended option, marked "(provisional, Qn)". The Chief of
Staff takes the questions to the user or to the advisor the user named.

## 1. Goal

A person with a code repository and no planning surface yet turns chantier on in external mode by
following one page, from an empty git repository to a first batch, and never meets a refusal the
page did not prepare them for. The writer's "the default branch cannot be read" refusal (CR-404)
stays, but it has three explicit ways out, and both the refusal and the page name them.

## 2. What changes

### 2.1 The guide (provisional, Q1)

A new page, `docs/getting-started-surface.md`, titled "Getting started: a new planning surface".
It is a numbered walk, each step with the exact command(s), what to expect, and the refusal a
skipped step produces (quoted from the CLI as it ships at this CR's head):

1. **Create the surface repository** on the forge (GitHub or GitLab, empty, no README), clone it,
   or `git init` and `git remote add origin <url>`.
2. **Its first commit and push:** a surface `AGENTS.md` (a short example: the surface's rules,
   "agent sessions never stage, commit, pull or push here: the surface server's writer publishes"),
   `git add`, `git commit`, `git push -u origin <branch>`; the page notes that this is the only
   push by hand (the surface's own files later are committed by hand and pushed by the writer).
3. **The surface's branch:** the three explicit sources of section 2.2, in their order, with
   `git remote set-head origin -a` first (what a `git clone` does on its own and a
   `git remote add` does not), then the stated branch in the root `chantier.yaml`, then the
   checkout's upstream (set by step 2's `push -u`). The page says that with none of them the
   writer blocks as `not-a-branch` and quotes its text.
4. **The project's folder:** `projects/<name>/` with `project.md` (prose, the one fixed line
   `- Archive in the PR: yes|no`), `checkout.yml` (`repo:`, `worktrees:`, defaults `.repo/` and
   `.worktrees/`), then `$CHANTIER init` (with `--project projects/<name>`) for the stage folders
   and their `.gitignore`; clone the code where `checkout.yml` says.
5. **The project's `chantier.yaml`** (optional): `projects/<name>/chantier.yaml`, and the root
   `chantier.yaml` for all projects; a minimal example (`batch.slots`), a link to
   [agents and models](agents-and-models.md#the-layers) for the layers, and the board's
   Configuration page as the other way to write it.
6. **The `planning:` line** in the code repository's `AGENTS.md`, `chantier` section:
   `- planning: <surface url>, projects/<name>`, read by the Chief of Staff (not the CLI): a
   session started in the code repository is sent to the surface.
7. **How `$CHANTIER` runs** for the project: plugin mode, `uvx --from <the plugin's folder>
   chantier --project projects/<name>`, from the surface's checkout (the page takes its wording
   from the `cli:` line and from CR-436's plugin-mode rule once merged, section 6).
8. **Start the surface server:** `$CHANTIER board --seat <session id>` (the Chief of Staff starts
   it on the user's yes; by hand, with no `--seat`, it serves until stopped), it listens on
   127.0.0.1 unless `board.host: network` or `--host` (CR-426), and the link carries the key.
9. **Check the `writer:` line:** `$CHANTIER status` (or `seat`) prints it; `synced` or `pending`
   is right; `blocked: not-a-branch`, `no-upstream`, `staged`, `nested-repo`, `foreign-autosync`
   each with its way out (CR-404's table, C.10), the first one sending back to step 3.
10. **The first `open`:** start the Chief of Staff in the surface's checkout (never in the code
    clone), `$CHANTIER preflight` and what its surface checks say (P11 the surface on its branch,
    P12 the configuration, P13 no hand pull/push rule and no other autosync), the host's
    permission to write in the clone and its worktrees (outside the surface's folder: Claude Code
    additional working directories), at least one CR in `3-ready`, and the writer running (with
    no server every command that writes in the surface is refused with "start the surface server
    ($CHANTIER board --seat <session id>)").

Links to the page:

- `docs/planning-modes.md`, "Setting one up": its four steps are replaced by one paragraph and a
  link to the new page (no step kept in two places).
- `docs/planning-modes.md`, "The surface's writer": one sentence on where the branch comes from,
  linking step 3.
- `README.md`, "Planning modes": the sentence "The full account (...) is in planning modes" gains
  "; to start one from nothing, [getting started](docs/getting-started-surface.md)".

No card changes: `init.md` keeps its tour; the Chief of Staff, asked to set up a surface, may send
the user to the page (it is a doc, no contract).

### 2.2 The surface's branch: three explicit sources (provisional, Q2 to Q6)

Today the writer (`writer/cycle.py`: `_preconditions`, step 2, and `_conflict_over`, step 1) and
preflight's P11 (`commands/preflight.py`, `_check_surface`, through `core/git.py`'s
`default_branch`) read the surface's branch from `origin/HEAD` only.

After this CR, one function, `surface_branch(root) -> (branch, source)` (in `writer/git_ops.py`
or a small module beside it; the name is the Driver's), resolves it from these sources, in this
order, the first one set wins (provisional, Q4):

1. **Stated:** the surface root's `chantier.yaml` (or `chantier.yml`), key `surface:` with one key
   `branch: <name>` (provisional, Q3). Read from the surface root's file only.
2. **`origin/HEAD`:** as today (`symbolic-ref refs/remotes/origin/HEAD`).
3. **Upstream:** the upstream of the branch the checkout is on (`branch.<b>.remote` and
   `branch.<b>.merge`), when it has one: the branch is `<b>` (provisional, Q5).

With none set (no statement, `origin/HEAD` unset, HEAD detached or on a branch with no upstream),
the writer blocks as `not-a-branch`, its text naming the three ways out, in the same order:

```text
the surface's branch cannot be read: run `git remote set-head origin -a` in the surface's
checkout, or state it in the surface's chantier.yaml (surface: branch: <name>), or set the
checked-out branch's upstream (git branch -u origin/<name>)
```

(one line in the code; the wording is the Driver's within these three named fixes). When a
source gives a branch and HEAD is elsewhere, the existing text stays ("HEAD is on X, not on the
default branch Y") and names the source: "(from chantier.yaml)", "(from origin/HEAD)",
"(from the upstream)".

Who uses the resolution (provisional, Q6): the writer's step 1 (`_conflict_over`) and step 2
(`_preconditions` / `blocking.blocking`, whose `default` argument becomes the resolved branch and
its source), and preflight's P11 (`_check_surface`, run on `repo.surface_root`). `core/git.py`'s
`default_branch` stays for its other callers, which read the code repository
(`commands/opening_record.py`, `commands/orders.py`): unchanged.

The configuration check (`playbook/config.py`, `_KEYED` and the top-level keys' message):

- `surface` becomes a known top-level key, holding one key, `branch`, one branch name (a scalar
  with no whitespace; `default` resets it, as for every key).
- In a project folder's `chantier.yaml` or the code repository's, `surface:` is refused by the
  check (P12, `validate`, the board's save) with "surface: the surface's branch is stated in the
  surface root's chantier.yaml only" (provisional, Q3): one writer per surface, one branch.
- The board's Configuration page does not show or edit it (the server's `config.put` keys are the
  two limits and the roles: unchanged).

The writer reads the stated branch at each cycle (a change of the file takes effect at the next
cycle, with no restart), like its other reads of step 2.

`AGENTS.md` (the repository's) is unchanged: no new git command, no new write.

## 3. Out of scope

- A guessed branch (`main`, `master`, the branch HEAD is on with no upstream): never.
- The code repository's default branch (`batch.json`'s `default_branch`, `open --default-branch`).
- A surface `AGENTS.md` line as a source (provisional, Q3: the CLI does not read `AGENTS.md`
  lines; the `planning:` line is the Chief of Staff's).
- Creating the forge repository, running `git init`, `set-head` or any push for the user: the CLI
  gains no git write; the page shows the commands.
- The in-project mode's getting started (`docs/tutorial-claude-code.md` covers it).
- A Copilot-specific walk: the page names the Claude Code additional working directories, and
  says the Copilot equivalent is in [hosts](hosts.md) (untested there, as that page says).

## 4. Evidence

Tests (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized, within the
`just test` budget):

- `test_writer_cycle.py`: one parametrized test over the resolution, on the writer rig's real git
  checkout: (a) stated in the root `chantier.yaml`, `origin/HEAD` unset, no upstream: resolved,
  source "chantier.yaml"; (b) `origin/HEAD` set: resolved from it; (c) only the upstream of the
  checked-out branch: resolved from it; (d) stated and `origin/HEAD` disagree: the stated one wins
  (Q4); (e) none: `not-a-branch`, the text holds `git remote set-head origin -a`,
  `chantier.yaml` and `git branch -u`. The existing
  `test_an_unknown_default_branch_names_the_command_that_reads_it` is folded into (e).
- A config-check test (beside the `board` key's): `surface: {branch: plan}` accepted in the
  surface root's file; refused in a project folder's file with the text above; a value with
  whitespace refused.
- A P11 case: a surface with `origin/HEAD` unset and the branch stated, HEAD on it: P11 passes and
  names the source; HEAD elsewhere: P11 warns.
- A docs check (`just check` runs no link check of `docs/` today): one test reads
  `docs/getting-started-surface.md`, `docs/planning-modes.md` and `README.md` from the repository
  as they ship, at the head under test, and asserts that the page exists, is linked from the two
  others, and quotes the writer's `not-a-branch` text as `writer/blocking.py` ships it (read from
  the shipped module's constant, not a copy), so the page cannot drift from the refusal.
- The config-check test sits in `test_playbook_config.py`.

Walk-through (the Verifier, before the PR): follow the page from step 1 on a scratch folder
outside the repository, with a local bare repository as the remote (`git init --bare`), so
`origin/HEAD` is unset as on a hand-made remote: the board's `writer:` line shows
`blocked: not-a-branch` with the three fixes before step 3, and `synced` after each of the three
fixes taken alone (three runs); `open` refuses with no server and passes its surface checks after
step 8. Recorded in `evidence/` with the commands and outputs.

`just check`, `just eval-dry-run` (the change is under the CLI's `src/`), and the pipeline's
`just scenario (ubuntu-latest)` job at the PR's head (a CLI change). No `hooks/` or `types/`
change, no pane change (no screenshot owed).

Host and default matrix: the change depends on a configured value versus none (the stated
branch), not on the host:

| Cell | Expected |
| --- | --- |
| no `surface:` key, `origin/HEAD` set | as today: branch from `origin/HEAD` |
| no `surface:` key, `origin/HEAD` unset, upstream set | branch from the upstream |
| no `surface:` key, nothing set | `not-a-branch`, three fixes named |
| `surface: branch:` stated in the root file | branch from it, whatever the others say |
| `surface:` in a project folder's file | refused by the check (P12, `validate`) |

## 5. Files

- `docs/getting-started-surface.md` (new); `docs/planning-modes.md`; `README.md`.
- `skills/chantier/scripts/cli/src/chantier/writer/git_ops.py` (or a module beside it: the
  resolution), `writer/cycle.py`, `writer/blocking.py`, `commands/preflight.py`
  (`_check_surface`), `playbook/config.py` (+ a small check module as `board_check.py` is),
  `playbook/layers.py` (reading the root layer's `surface` key).
- Tests as section 4.

## 6. Overlaps with batch-30 (running)

- **CR-447 `docs-gardening`** (pending, last of the batch, `depends.json` after every other CR):
  it inventories `docs/`, the README and `docs/planning-modes.md`. If this CR joins batch-30, it
  should land before CR-447 so the gardening reads the new page: add `surface-getting-started` to
  CR-447's `after` list (the Chief of Staff's `order add`), and this CR's `depends.json` names none
  of it. If it does not join, CR-447 does not need it.
- **CR-436 `sync-blocked-by-others`** (active): sets the rule that a project other than chantier
  runs in plugin mode (`uvx --from`); step 7 takes its wording from it, so this CR comes after
  CR-436. Both touch `commands/preflight.py`, in different functions (P5 versus P11): textual
  only.
- **CR-426 `board-exposure`** (done): the board's 127.0.0.1 default, `board.host: network`,
  `--host` and the key; step 8 describes the merged behaviour.
- **CR-443 `gate-hold-narrowing`** and **CR-449 `board-griller`** (pending): both edit
  `playbook/config.py` (CR-443 the `long_gate.commands` key and the top-level keys' message;
  CR-449 `start_refusal`). The new `surface` key edits the same `_KEYED` table and message:
  a textual conflict, resolved at rebase; no behaviour overlap.
- **CR-439 `board-help-page`** (active): Help cards link README and docs pages; it may later link
  the new page. No dependency.
- **CR-446 `live-several-boards-and-keys`** (pending): edits `docs/boards.md` and
  `docs/server-api.md` only: no overlap.
- **CR-437 `sync-lock-wait`**, **CR-450 `push-refusal-ladder`**: preflight's P5 and the allow
  rules' texts, not P11 or the writer's branch: no overlap found.
- The request's priority is P3 ("later"); joining batch-30 is the Chief of Staff's call.

## 7. Open questions

- **getting-started-Q1. Where the guide lives.** (A, recommended) A new page
  `docs/getting-started-surface.md`, linked from `docs/planning-modes.md` (whose "Setting one up"
  becomes a link) and the README's "Planning modes". (B) Grow "Setting one up" in
  `docs/planning-modes.md` in place, no new page. (C) A section of `docs/tutorial-claude-code.md`
  (host-specific; overlaps CR-443's edits there).
- **getting-started-Q2. Part 2 in this CR or apart.** (A, recommended) In this CR: the guide
  shows the three sources, so they ship together and the page is proved against them. (B) This
  CR is the guide only (docs-only, no long gate), showing `git remote set-head origin -a`; part 2
  becomes an inbox CR of its own.
- **getting-started-Q3. Where the branch is stated.** (A, recommended) The surface root's
  `chantier.yaml`, key `surface: branch: <name>`, refused in any other `chantier.yaml`: the CLI
  already reads and checks that file, the CLI reads no `AGENTS.md` line. (B) A line in the
  surface's `AGENTS.md` (`- branch: <name>`), read by the CLI: a first `AGENTS.md` line the CLI
  reads. (C) Both, the file winning.
- **getting-started-Q4. When sources disagree.** (A, recommended) The first set wins, in the order
  stated, `origin/HEAD`, upstream: a statement is the user's own word, `origin/HEAD` the forge's
  default. (B) Stated and `origin/HEAD` both set and different: the writer blocks
  (`not-a-branch`, "the sources disagree") until one is changed.
- **getting-started-Q5. What "the checkout's tracked branch" means.** (A, recommended) The branch
  the checkout is on, when it has an upstream, used only when the two sources above are unset;
  this accepts any branch with an upstream on a surface with neither (the page says so). (B) Only
  when that upstream's name equals the local branch's name (`main` tracking `origin/main`), else
  no source. (C) Drop this source: two sources only (against the request's wording).
- **getting-started-Q6. Does preflight's P11 follow the same resolution?** (A, recommended) Yes:
  P11 and the writer read one branch, P11 naming its source. (B) No: P11 keeps `origin/HEAD` only
  (and stays silent when it is unset, as today).
