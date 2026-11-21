# Change Specification: AGENTS.md names the CLI's forge calls

Short name: `agents-md-names-cli-forge-reads`. No issue (origin: verbal; split out of
`take-base-from-forge`, its answer Q11, by the Chief of Staff on 2026-11-20). Version 2,
2026-11-21: `02-answers.md` (forge-reads-Q1 to Q5, all A, and the destination) applied.

Sources: `intake/request.md`, `01-intent.md`, `02-answers.md`, the parent's
`5-archives/261121-0330-422-take-base-from-forge/02-answers.md` (Q11) and `03-change-spec.md`
("The network rule (AGENTS.md), settled"). No grill was held: the user delegated the night's spec
questions to a Fable advisor (2026-11-21, "plus de question"), whose answers `02-answers.md`
records.

## Goal

The project's rules say when the CLI talks to the forge, and they say it truly. Today AGENTS.md
says the CLI needs no network once uv's cache holds its packages except for three named parts,
and that "the agents do the work, git and the forge included"; CONTRIBUTING.md, two cards and two
docstrings go further and say the CLI runs no forge command or reads no forge. The CLI in fact
calls the forge, with the user's own `gh` or `glab`, from `ship`, `take`, `round`, `handoff` and
`forge-stack`, and `forge-stack` writes on the forge. After this CR, every text that states the
rule names those calls, what they read or write, and their limits; no code behaviour changes
(forge-reads-Q1 A, `02-answers.md`).

## Inventory: every forge call the CLI makes today

Read at `main` 33d10454 (2026-11-21), under `skills/chantier/scripts/cli/src/chantier/`. Found by
grepping the calls of `gh` and `glab` (`shutil.which("gh"|"glab")`, `connectors/run.py`) and every
caller of `forge_base`, `forge_stack_gh.gh`, `forge_stack_gitlab.glab` and `connectors.read`.

| # | Who calls | What it does on the forge | Code | Named in AGENTS.md today |
| --- | --- | --- | --- | --- |
| 1 | the surface server, a batch's PRs | read-only GraphQL, through the connectors | `board/prs.py` → `connectors.read` | yes ("the server's read of a batch's PRs") |
| 2 | the forge hub | read-only GraphQL, through the connectors | `hub/cycle.py` → `connectors.read` | yes ("the forge hub") |
| 3 | `ship` | reads the PR's base branch and draft state, once per call, for every CR (`gh api -X GET repos/<o>/<r>/pulls/<n>`, or `glab api projects/<p>/merge_requests/<iid>`) | `commands/delivery.py` (`ship`, `read_state`) → `commands/forge_base.py` (`pr_state`) | no |
| 4 | `take` (each CR it prints), `round`, `handoff` | read the base branch of a **stacked** CR's PR (a CR of a `stack` batch's chain with a PR recorded); `cr_facts` calls `stacked_read` in `_base_of` and again in `_landed_line` (`commands/facts.py` :65, :75), so at most twice per such CR printed; no call for any other CR | `commands/driver.py` (`take`, `round_`), `commands/facts.py` (`handoff`) → `cr_facts` → `_base_of`, `_landed_line` → `forge_base.stacked_read` | no (the request names `take` and `handoff`; `round` was missed, and `forge_base.py`'s docstring misses it too) |
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
(below))" with (forge-reads-Q1 A, `02-answers.md`):

> and the CLI needs no network once uv's cache holds its packages, except the server's read of a
> batch's PRs, the forge hub, the surface server's writer, whose fetch and push need it, and the
> forge calls of `ship`, `take`, `round`, `handoff` and `forge-stack`, made with the user's own
> `gh` or `glab` (below))

### 2. `AGENTS.md`, the CLI-scope bullet ("The CLI's scope: ...")

a. Replace "The agents do the work, git and the forge included;" with "The agents do the work, git
and the forge included, but for the forge calls named below;".

b. Add one named exception, as its own sentence group, just before "The surface server's writer,
a thread of the same process" (forge-reads-Q2 A and Q3 A, `02-answers.md`):

> The forge calls of the batch's commands, with the user's own `gh` or `glab`, and the network for
> them: `ship` reads the base branch and the draft state of the PR it records, once per call, and
> `take`, `round` and `handoff` read the base branch of a stacked CR's PR (a CR of a `stack`
> batch's chain with a PR recorded) for each such CR they print; a failed read prints
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
draft state (`ship`, and `take`, `round` and `handoff` for a stacked CR) and in `forge-stack`".

### 5. The cards and the shipped docstrings (forge-reads-Q4 A, `02-answers.md`)

- `skills/chantier/references/concepts.md`, the `$CHANTIER` item: "no forge command beyond
  `forge-stack` (it calls the user's own `gh` or `glab`)" becomes "no forge command beyond
  `forge-stack` and the reads of `ship`, `take`, `round` and `handoff` (a PR's base, and for
  `ship` its draft state; they call the user's own `gh` or `glab`)".
- `skills/chantier/references/driver.md`, twice (~214, in the long-gate item, and ~514, in the
  `ship --conflict` item): "The CLI reads no forge: you read CI at the new head, which must be
  green." becomes "The CLI reads no CI: you read CI at the new head, which must be green." (the
  rest of each item unchanged; `ship` reads a PR's base and draft state on the forge, never its
  CI).
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
- `hub/watch.py`'s docstring ("reads no forge", said of the watcher's `--once`): true, left as it
  is.
- A test guarding the wording (forge-reads-Q5 A).

## Destination and overlaps (batch-30, taken late)

`02-answers.md`: batch-30, taken late, after CR-443, CR-449 and CR-429; no `depends.json`, the
overlaps are shared text only. Six of batch-30's CRs edit the same bullets of `AGENTS.md`, the
same paragraphs of `CONTRIBUTING.md` or a sentence this CR's rule makes false; none adds, removes
or moves a forge call of the inventory:

| CR | Shared place |
| --- | --- |
| CR-443 `gate-hold-narrowing` (pending) | AGENTS.md's no-setup bullet (the same bullet as section 1: it adds the long gate's `chantier.yaml` entry and drops the `.lease-hold.*.run` clause) and the `lease` exception of the scope bullet; README |
| CR-449 `board-griller` (pending) | AGENTS.md's scope bullet (a new named exception for the server's Griller, and "never messages an agent" reworded) and the role rule |
| CR-429 `board-fingerprint-cache` (active) | AGENTS.md's scope bullet (the server's, hub's and watcher's sentences); CONTRIBUTING's same hub and watcher sentences |
| CR-436 `sync-blocked-by-others`, CR-437 `sync-lock-wait` (active) | CONTRIBUTING's "A CLI" item and the "In this checkout" paragraph; AGENTS.md's "The CLI is one Python package" bullet (not one this CR edits) |
| CR-447 `docs-gardening` (pending) | CONTRIBUTING's "How the project is built" (the "A CLI" item, section 3), README |
| CR-442 `stack-git-chain` (pending, `4-batch/1-pending/442-stack-git-chain`) | its spec (~162) and its answer stack-chain-Q8 say "the CLI reads no forge at `ship`", which `ship`'s base and draft read (inventory #3) makes false; any of it that lands in a card, a message or a docstring reads "no forge read of the CR below's merge at `ship`". Whichever of the two CRs lands second makes the landed text read so; the word check below catches it. Its card edits sit near section 5's `driver.md` sentences |

Also: CR-428 `drop-to-next-batch` edits a message in `commands/forge_stack_gh.py` (`held_outside`),
a file this CR does not edit; CR-438 touches the stack's checks, not its forge calls.

Each conflict is textual: the Driver rebases on whichever of these lands first and keeps their
sentences, adding only this CR's clauses.

## Evidence

- **Inventory check, at the PR's head.** The Driver runs, from the repository root,
  `rg -n '"gh"|"glab"|connectors\.read\(|stacked_read\(|read_state\(|read_base\(|pr_state\(|\bgh\(|\bglab\(' skills/chantier/scripts/cli/src/chantier --glob '!clients/**'`
  and confirms in the PR's Deliverables that each hit falls in one row of the inventory (or the
  "Not forge calls" list); a new caller found there stops the CR and goes back to the Chief of
  Staff, since the rule would name it too.
- **Word check.** `rg -n -i "no forge command|forge included|needs no network|reads no forge"
  AGENTS.md CONTRIBUTING.md README.md skills/chantier/references skills/chantier/scripts/cli/src`
  at the head shows only the sentences this CR wrote, `hub/watch.py`'s true docstring, and any
  CR-442 text in the reworded form above: no unqualified "no forge command" or "reads no forge"
  said of the CLI or of `ship`.
- **Gates (AGENTS.md), forge-reads-Q4 A.** The CR changes cards and docstrings under the CLI's
  `src/`: `just check` and `just eval-dry-run` in the worktree at the rebased head before the
  first push, and the pipeline's `just scenario (ubuntu-latest)` green at the PR's head (a card
  change).
- No host or default matrix: nothing here depends on the host or on a configured value. No CR
  board pane change, no screenshot owed.

## Decisions

From `02-answers.md` (2026-11-21, Fable advisor, the user's delegate):

- forge-reads-Q1 A: name the calls, change no code.
- forge-reads-Q2 A: `forge-stack`'s writes are named in the scope bullet, limited to stacks and
  bases.
- forge-reads-Q3 A: the exception cites the drift behind `ship`'s read (batch-17, batch-18,
  CR-270) and the stack CRs behind `forge-stack` (CR-234, CR-245, CR-313), "named after the fact".
- forge-reads-Q4 A: AGENTS.md, CONTRIBUTING.md, README.md, the cards (`concepts.md`, and
  `driver.md`'s two sentences) and the three docstrings.
- forge-reads-Q5 A: no test; the Driver's one-time inventory check.
- Destination: batch-30, taken late, after CR-443, CR-449 and CR-429; no `depends.json`.

No open question.
