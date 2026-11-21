# Change Specification: AGENTS.md names the CLI's forge calls

Short name: `agents-md-names-cli-forge-reads`. No issue (origin: verbal; split out of
`take-base-from-forge`, its answer Q11, by the Chief of Staff on 2026-11-20). Version 1,
2026-11-21.

Sources: `intake/request.md`, `01-intent.md`, the parent's
`5-archives/261121-0330-422-take-base-from-forge/02-answers.md` (Q11) and `03-change-spec.md`
("The network rule (AGENTS.md), settled"). No grill was held and there is no `02-answers.md`: the
user delegated the night's spec questions (2026-11-21, "plus de question"). Every choice below
that the request leaves open is a numbered question at the end (forge-reads-Q1 to Q5), and this
version is written on the recommended option of each, as **provisional** text until the user (or
the advisor the user named) answers.

## Goal

The project's rules say when the CLI talks to the forge, and they say it truly. Today AGENTS.md
says the CLI needs no network once uv's cache holds its packages except for three named parts,
and that "the agents do the work, git and the forge included"; CONTRIBUTING.md, a card and two
docstrings go further and say the CLI runs no forge command. The CLI in fact calls the forge, with
the user's own `gh` or `glab`, from `ship`, `take`, `round`, `handoff` and `forge-stack`, and
`forge-stack` writes on the forge. After this CR, every text that states the rule names those
calls, what they read or write, and their limits; no code behaviour changes (forge-reads-Q1).

## Inventory: every forge call the CLI makes today

Read at `main` 33d10454 (2026-11-21), under `skills/chantier/scripts/cli/src/chantier/`. Found by
grepping the calls of `gh` and `glab` (`shutil.which("gh"|"glab")`, `connectors/run.py`) and every
caller of `forge_base`, `forge_stack_gh.gh`, `forge_stack_gitlab.glab` and `connectors.read`.

| # | Who calls | What it does on the forge | Code | Named in AGENTS.md today |
| --- | --- | --- | --- | --- |
| 1 | the surface server, a batch's PRs | read-only GraphQL, through the connectors | `board/prs.py` → `connectors.read` | yes ("the server's read of a batch's PRs") |
| 2 | the forge hub | read-only GraphQL, through the connectors | `hub/cycle.py` → `connectors.read` | yes ("the forge hub") |
| 3 | `ship` | reads the PR's base branch and draft state, once per call, for every CR (`gh api -X GET repos/<o>/<r>/pulls/<n>`, or `glab api projects/<p>/merge_requests/<iid>`) | `commands/delivery.py` (`ship`, `read_state`) → `commands/forge_base.py` (`pr_state`) | no |
| 4 | `take` (each CR it prints), `round`, `handoff` | read the base branch of a **stacked** CR's PR (a CR of a `stack` batch's chain with a PR recorded), once per such CR printed; no call for any other CR | `commands/driver.py` (`take`, `round_`), `commands/facts.py` (`handoff`) → `cr_facts` → `_base_of`, `_landed_line` → `forge_base.stacked_read` | no (the request names `take` and `handoff`; `round` was missed, and `forge_base.py`'s docstring misses it too) |
| 5 | `forge-stack create\|show\|rebuild\|unstack` | reads the batch's PRs or MRs and the forge's stacks; **writes**: creates a stack (`POST repos/<o>/<r>/stacks`, GitHub), dissolves one (`POST .../stacks/<n>/unstack`), retargets a PR's base (`PATCH .../pulls/<n>` with `base=`) or an MR's target branch (`PUT .../merge_requests/<iid>` with `target_branch=`, GitLab) | `commands/forge_stack.py`, `forge_stack_gh.py`, `forge_stack_gitlab.py` | no (and the scope bullet's "the agents do the work, git and the forge included" says otherwise) |

Not forge calls, left unnamed:

- `commands/permissions.py` `_gh_names_stack`: `gh extension list`, a listing of the local `gh`'s
  installed extensions for preflight's P10 (whether to allow `gh stack`). It asks the forge for
  nothing; whether `gh` itself touches the network for it was not exercised here.
- `wait`, `interests`, `journal add`: they call `connectors.connector_for` (the shape of a link),
  never `connectors.read`; no forge call.
- `board/address.py`: an HTTP call to the board's own local address, not the forge.
- `writer/git_ops.py`: the writer's `git fetch` and `push`, already named.

Every failure of #3 and #4 blocks nothing: a failed read prints `base ? (not read from <link>:
<the forge's text>)` (`forge_base.UNREAD`) and `ship` records the PR with no base and `draft not
read`. A failure of #5 exits 3 (`EXIT_EXTERNAL`) with the forge's text.

## What changes

Text only. All paths are relative to chantier's repository root. Find each place by its quoted
text, not by line number: batch-30's CRs edit the same bullets (see "Destination and overlaps").

### 1. `AGENTS.md`, the no-setup bullet (the network clause)

Replace "and the CLI needs no network once uv's cache holds its packages, except the server's read
of a batch's PRs, the forge hub and the surface server's writer, whose fetch and push need it
(below))" with (provisional, forge-reads-Q1 A):

> and the CLI needs no network once uv's cache holds its packages, except the server's read of a
> batch's PRs, the forge hub, the surface server's writer, whose fetch and push need it, and the
> forge calls of `ship`, `take`, `round`, `handoff` and `forge-stack`, made with the user's own
> `gh` or `glab` (below))

### 2. `AGENTS.md`, the CLI-scope bullet ("The CLI's scope: ...")

a. Replace "The agents do the work, git and the forge included;" with "The agents do the work, git
and the forge included, but for the forge calls named below;".

b. Add one named exception, as its own sentence group, just before "The surface server's writer,
a thread of the same process" (provisional, forge-reads-Q2 A and Q3 A):

> The forge calls of the batch's commands, with the user's own `gh` or `glab`, and the network for
> them: `ship` reads the base branch and the draft state of the PR it records, once per call, and
> `take`, `round` and `handoff` read the base branch of a stacked CR's PR (a CR of a `stack`
> batch's chain with a PR recorded), once per such CR they print; a failed read prints
> `base ? (not read from <link>: …)` and blocks nothing; `forge-stack` (`create`, `show`,
> `rebuild`, `unstack`) reads the batch's PRs or MRs and the forge's stacks, and writes only
> stacks and bases: it creates a stack (GitHub), dissolves one and retargets a PR's base or an
> MR's target branch, and nothing else on the forge (no PR opened, closed, merged, approved or
> commented). Built on the record's drift from the forge in batch-17 and batch-18 (`ship`'s read,
> CR-270 `ship-reads-forge`) and on the stack batches (`forge-stack`, CR-234, CR-245, CR-313),
> named in this rule after the fact (`agents-md-names-cli-forge-reads`).

### 3. `CONTRIBUTING.md`

- "What is chantier?": "The agents do the work, git and the forge included." gains ", but for the
  forge calls of `ship`, `take`, `round`, `handoff` and `forge-stack` (AGENTS.md names them)".
- The "A CLI" item: "It runs no git command that changes anything (it reads the head, the remote
  and the status to say what is off) and no forge command: the agents have `git`, `gh` and `glab`
  and do the work." becomes "... and no forge command but the reads of `ship`, `take`, `round` and
  `handoff` and the stacks and bases `forge-stack` makes, with the user's own `gh` or `glab`
  (AGENTS.md names them): the agents have `git`, `gh` and `glab` and do the rest."

### 4. `README.md`, "Install"

After "working on a repository also needs `git` and the forge's CLI, logged in: `gh` for GitHub,
`glab` for GitLab", add: "; the CLI uses it too, and the network, when it reads a PR's base or
draft state (`ship`, and `take` for a stacked CR) and in `forge-stack`".

### 5. The card and the shipped docstrings (forge-reads-Q4 A)

- `skills/chantier/references/concepts.md`, the `$CHANTIER` item: "no forge command beyond
  `forge-stack` (it calls the user's own `gh` or `glab`)" becomes "no forge command beyond
  `forge-stack` and the reads of `ship`, `take`, `round` and `handoff` (a PR's base, and for
  `ship` its draft state; they call the user's own `gh` or `glab`)".
- `skills/chantier/scripts/cli/src/chantier/commands/__init__.py`, module docstring: "and no forge
  command at all. One named exception, in `board/`:" becomes "and no forge command but `ship`'s,
  `take`'s, `round`'s and `handoff`'s reads of a PR's base (`forge_base.py`) and `forge-stack`'s
  stacks and bases. One named exception, in `board/`:" (the rest unchanged).
- `skills/chantier/scripts/cli/src/chantier/lifecycle/moveout.py`, `close_pr_clause` docstring:
  "(the CLI runs no forge command)" becomes "(the CLI closes no PR)".
- `skills/chantier/scripts/cli/src/chantier/commands/forge_base.py`, module docstring: "and the
  base alone for `take` and `handoff` (a stacked CR)" becomes "and the base alone for `take`,
  `round` and `handoff` (a stacked CR)".

## Out of scope

- Any change of behaviour: no forge call added, removed or moved; no command's output changes.
- Moving these calls out of the CLI (forge-reads-Q1 B), which would be its own CR.
- The "`uv` is the only tool to install" clause of the same bullet (the README already says `git`
  and `gh` or `glab` are needed to work on a repository); the other descriptions of the hub, the
  board and the writer.
- The docs under `docs/` (`docs/forge-connectors.md` describes the connectors, which this CR does
  not touch).
- A test guarding the wording (forge-reads-Q5 A).

## Destination and overlaps (batch-30, running)

Five of batch-30's CRs edit the same bullets of `AGENTS.md` or the same paragraphs of
`CONTRIBUTING.md`; none adds, removes or moves a forge call of the inventory:

| CR | Shared place |
| --- | --- |
| CR-443 `gate-hold-narrowing` (pending) | AGENTS.md's no-setup bullet (the same bullet as section 1: it adds the long gate's `chantier.yaml` entry and drops the `.lease-hold.*.run` clause) and the `lease` exception of the scope bullet; README |
| CR-449 `board-griller` (pending) | AGENTS.md's scope bullet (a new named exception for the server's Griller, and "never messages an agent" reworded) and the role rule |
| CR-429 `board-fingerprint-cache` (active) | AGENTS.md's scope bullet (the server's, hub's and watcher's sentences); CONTRIBUTING's same hub and watcher sentences |
| CR-436 `sync-blocked-by-others`, CR-437 `sync-lock-wait` (active) | CONTRIBUTING's "A CLI" item and the "In this checkout" paragraph; AGENTS.md's "The CLI is one Python package" bullet (not one this CR edits) |
| CR-447 `docs-gardening` (pending) | CONTRIBUTING's "How the project is built" (the "A CLI" item, section 3), README |

Also: CR-428 `drop-to-next-batch` edits a message in `commands/forge_stack_gh.py` (`held_outside`),
a file this CR does not edit; CR-442 and CR-438 touch the stack's checks, not its forge calls.

Each conflict is textual: the Driver rebases on whichever of these lands first and keeps their
sentences, adding only this CR's clauses. The CR fits batch-30's end (on top of those it shares a
place with), or the next batch; the Chief of Staff chooses.

## Evidence

- **Inventory check, at the PR's head.** The Driver runs, from the repository root,
  `rg -n '"gh"|"glab"|connectors\.read\(|stacked_read\(|read_state\(|read_base\(|pr_state\(|\bgh\(|\bglab\(' skills/chantier/scripts/cli/src/chantier --glob '!clients/**'`
  and confirms in the PR's Deliverables that each hit falls in one row of the inventory (or the
  "Not forge calls" list); a new caller found there stops the CR and goes back to the Chief of
  Staff, since the rule would name it too.
- **Word check.** `rg -n -i "no forge command|forge included|needs no network" AGENTS.md
  CONTRIBUTING.md README.md skills/chantier/references skills/chantier/scripts/cli/src` at the
  head shows only the sentences this CR wrote (and no unqualified "no forge command").
- **Gates (AGENTS.md).** With forge-reads-Q4 A the CR changes a card and docstrings under the
  CLI's `src/`: `just check` and `just eval-dry-run` in the worktree at the rebased head before the
  first push, and the pipeline's `just scenario (ubuntu-latest)` green at the PR's head (a card
  change). With Q4 B or C (docs only) `just check` alone, and no long gate.
- No host or default matrix: nothing here depends on the host or on a configured value. No CR
  board pane change, no screenshot owed.

## Open questions

Each is written with options, the recommendation first; this version follows the recommendation.

**forge-reads-Q1. Name the calls, or move them out of the CLI?**
- **A (recommended): name them** in AGENTS.md (and where the rule is repeated), and change no
  code. The calls exist on measured grounds (the record's drift from the forge, CR-270), the
  parent CR already relies on `ship`'s recorded base and draft state, and the request asks for no
  code change.
- B: move them out: `ship` takes the base and draft state from the Driver, `take`/`round`/
  `handoff` print the record's base only, and `forge-stack` becomes agent instructions. A new CR
  with code, card and scenario work; this CR closes having filed it. It reopens the drift CR-270
  fixed.
- C: name them now (A) and file an inbox item to move them out later.

**forge-reads-Q2. Does the rule name `forge-stack`'s writes, not only its reads?**
- **A (recommended): yes**, as a named exception in the scope bullet, with the limit "only stacks
  and bases, nothing else on the forge". The request's frame is the network sentence, but the
  scope bullet's "the agents do the work, git and the forge included" is the larger untruth.
- B: the network sentence only (section 1), the scope bullet untouched: shorter, but the rule
  stays wrong about writes.
- C: the writes go to their own CR.

**forge-reads-Q3. What basis does the new exception cite?** AGENTS.md gives each named exception
its basis (a measured cost or the user's answer).
- **A (recommended):** the measured drift behind `ship`'s read (batch-17 and batch-18, CR-270) and
  the stack CRs behind `forge-stack` (CR-234, CR-245, CR-313), "named in this rule after the fact".
- B: "with no measured cost", like `wait` and `access`.
- C: no basis sentence.

**forge-reads-Q4. How far does the correction reach?**
- **A (recommended):** AGENTS.md, CONTRIBUTING.md, README.md, the card `concepts.md` and the three
  docstrings (`commands/__init__.py`, `lifecycle/moveout.py`, `commands/forge_base.py`), all of
  which state the rule wrongly or miss `round`. It owes `just eval-dry-run` and the pipeline's
  `just scenario` (a card change).
- B: AGENTS.md, CONTRIBUTING.md and README.md only (docs: `just check` alone); the card and the
  docstrings stay wrong until another CR.
- C: AGENTS.md only.

**forge-reads-Q5. A test that keeps the rule and the code in step?**
- **A (recommended): none.** The inventory check above is run once by the Driver; a wording test
  is brittle and the test suite is kept small (AGENTS.md's time budget).
- B: one structure test that lists the modules that call `gh` or `glab` against a fixed list in
  the test, so a new forge call fails `just test` until AGENTS.md is reviewed.
