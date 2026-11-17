# Change Specification: a project's rule may name a pipeline job as its long gate

## Goal

The local long gate paces a batch: `just scenario` takes 9.5 min on the user's quiet Windows
machine (573 s), 11 min loaded, and the long gates run one at a time; batch-18 ran about 30 of
them. The forge runs the same scenario job in 1m43 on ubuntu. The user wants a project to be able
to say "our long gate is this pipeline job, green at the PR's head", so a Driver waits on the
forge instead of on the local lock. For this project, the long gate becomes the pipeline's
scenario job; Windows coverage, which found the real defects (the gate race, os error 32), is kept
by one local `just scenario` per batch on the stack's top before the user merges.

The change is in the cards and this project's `AGENTS.md` only. The CLI does not change.

## Decisions carried from 02-answers.md

1. The fix is the request's, by the user's word ("oui les 6", then "lance le tout dans le batch
   actuel"). The CR joins batch-18 (a stack), second in the stack.
2. Generality: the rule works the same on both hosts (Claude Code, GitHub Copilot) and both
   forges (GitHub, GitLab). A path not proved on Copilot or on a real GitLab carries the mark
   "unproved" in its card line.
3. Windows coverage default (A): one local `just scenario` per batch on the stack's top before the
   user merges. The alternative (a Windows leg in CI) is named in the open points with its cost.
4. The CLI does not change: the cards carry the generic rule, this project's `AGENTS.md` the job's
   name.

## What changes

### 1. `skills/chantier/references/concepts.md` (the generic rule)

In the long gate paragraph ("`$CHANTIER`" bullet, around the `--no-gate` sentence, lines 354-356),
add one sentence, the definition every other card points to:

> A project's rule may name a pipeline job as its long gate (for instance "the long gate is the
> pipeline's `<job name>` job, green at the PR's head"): its Driver runs no `gate`, pushes and
> opens the PR after the approved round, waits for that job green at the PR's head, and hands back
> `--no-gate "<the rule>"`; the steering session reads that job's state at the PR's head on the
> forge (`gh pr checks <pr>` on GitHub; `glab ci status --branch <branch>` on GitLab, unproved).
> The Copilot host's path is unproved.

The mark "unproved" stays until the user's trial on a real GitLab and on Copilot (decision 2).

### 2. `skills/chantier/references/driver.md` (the Driver's side)

In "The long gate" bullet (lines 190-217), next to "A CR the rules exempt hands back with
`--no-gate "<the rule>"`", add one sentence:

> When the project's rules name a pipeline job as the long gate ([concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md)), run no
> `gate`: push and open the PR after the approved round (the first push starts the gate, so no
> wait before it; `ship`'s `off: no long gate passed at <sha>` is then expected), read CI as the
> "CI" bullet says, and once that job is green at the PR's head with the `VERIFIED` verdict there,
> hand back `ready <link> … --no-gate "<the rule>"`, quoting the rule; a red run of that job is a
> red CI job, a round. A rebase needs no gate carry: the job runs again at the pushed head.
> (GitLab and Copilot: unproved.)

And in "Your end" (lines 395-397), widen "only where the project's rules declare none or exempt
this CR" to "only where the project's rules declare none, exempt this CR, or name a pipeline job
as the long gate".

Nothing else in the Driver's flow moves: the fast gate, the rounds, the Verifier, the PR body's CI
box and the note `CI: gh pr checks <n> at <sha7>: …` stay as they are. A rule that also asks the
stack's top for a local run (section 4) is met by that CR's Driver with `$CHANTIER gate` as any
long gate, and that CR hands back with no `--no-gate`.

### 3. `skills/chantier/references/foreman.md` (the steering session's check)

In "The user's boundaries", the check of a hand-back that says `no long gate: <reason>` (lines
83-91), add one case after "It holds when the rules say the project has no long gate, or exempt
this CR":

> or name a pipeline job as the long gate and that job is green at the PR's head: read it on the
> forge (`gh pr checks <pr>`, the job by its name, state pass; `glab ci status --branch <branch>`
> on GitLab, unproved), and send the CR back with `take <cr> --note "long gate: <job> not green at
> <sha7>"` when it is not, with no ask. When the rules also ask a local run on the stack's top
> (section 4), the stack's top handed back with `--no-gate` goes back with `take <cr> --note "long
> gate: the stack's top runs <command> locally"`, with no ask.

The ask then reads `ready-to-merge <cr> <link> no long gate: <the rule>` as today. The Chief of
Staff in direct mode follows the same card, so it inherits the check.

### 4. `skills/chantier/references/chief-of-staff.md` (two consistency edits)

These keep the Chief of Staff's own checks from refusing what the new rule orders:

- Line 84: "Once the project's rules say there is no long gate, or exempt a kind of CR" becomes
  "... or exempt a kind of CR, or name a pipeline job as the long gate".
- The force-push judgement (lines 1092-1103): add, beside the `ci: beside the long gate` and
  early-push exceptions, "Likewise when the project's rules name a pipeline job as the long gate:
  skip this gate check (the steering session checks that job at the PR's head)". Without it, a
  routed force push of a pipeline-gated CR would be answered `push refused <branch>: no long gate
  passed at <sha>`.

The batch estimate ("The gates", line 848) needs no edit: a CR handed back `--no-gate` already
does not count, and the stack's top's local run is a CR still to pass its long gate.

### 5. `docs/gates.md` (the user's page)

After the exemption paragraph (lines 27-30), add a short paragraph and an example line:

```markdown
- Long gate: the pipeline's `test` job, green at the PR's head.
```

saying that a project whose CI runs the long suite faster than the machine may name that job as
its long gate; the Driver then waits for it on the forge and quotes the rule with `--no-gate`, and
the Foreman (or the Chief of Staff steering) reads the job's state at the PR's head. It names the
gap: a project with no CI, or whose runner is the same slow machine, gains nothing. GitLab and
Copilot: unproved.

### 6. `AGENTS.md` (this project)

Replace the line "The long gate is `just scenario`: a change to the CLI, the cards or the scenario
passes it before its PR; a change to the docs or the eval kit alone needs none." with:

> The long gate is the pipeline's `just scenario (ubuntu-latest)` job, green at the PR's head: a
> change to the CLI, the cards or the scenario passes it before its PR; a change to the docs or the
> eval kit alone needs none. Windows coverage: in each batch, the CR on top of the stack also
> passes `just scenario` locally (`chantier gate`) at its head before the user merges; when a CR
> joins on top, the local run moves to it.

The job name is the one `.github/workflows/ci.yml` declares (`name: just scenario
(ubuntu-latest)`, job id `scenario`), the name `gh pr checks` prints. `just eval-dry-run`, which
CI runs and the local gate missed (it cost CR-253 a round), is covered by the existing rule that a
red CI job is a round: a Driver hands back only on green CI.

## The CI job's environment

No CI job is added or changed. The rule reads the existing `scenario` job: `ubuntu-latest`, fresh
runner, `astral-sh/setup-uv@v6` and `extractions/setup-just@v3`, a git identity set by the job, no
uv cache from the user's machine, network on, no forge credentials beyond the checkout's read
token. What that job does not cover and the local machine does: Windows (paths, file locks, os
error 32, process stops), the user's loaded-PC timings. That is why the stack's top keeps one local
Windows run (decision 3).

## Out of scope

- Any CLI change: no new flag, no forge read by the CLI, no new `gate` mode. The board and
  `STATUS.json` keep showing a `--no-gate` CR as `exempt: <rule>` (`status/gate.py`); the word
  "exempt" for a pipeline-gated CR is a known gap of this CR, not fixed here.
- `init.md`'s long-gate proposal (step 5): it does not learn to propose a pipeline job.
- A Windows leg in CI (the alternative, open point 1).
- Projects with no CI, or a runner on the same slow machine: they gain nothing and keep the local
  gate.
- The Copilot agent files: they carry no gate text; the cards are shared by both hosts.

## Evidence

- `just check` passes (lint, tests, release notes) on Linux, macOS and Windows (CI's `check`
  matrix).
- This CR changes the cards, so it passes the long gate. Until it merges, the rule in force is the
  main checkout's `AGENTS.md` (`$CHANTIER rules`), so this CR passes `just scenario` locally as
  today, unless the user says otherwise (open point 3).
- A read of each edited card line: concepts.md, driver.md, foreman.md and chief-of-staff.md name
  the same rule in the same words, each with the GitLab and Copilot "unproved" mark.
- Grep check: no card still says `--no-gate` is only for "none or exempt" without the pipeline case
  (`Grep "declare none or exempt"` under `skills/chantier/references/`).
- First real proof, after the merge: the next CR of batch-18 above this one hands back `--no-gate
  "<the AGENTS.md rule>"` with the scenario job green at its head, and the Foreman's ask carries
  `no long gate: …`; the stack's top runs `chantier gate <cr> "just scenario"` locally. The Driver
  notes the `gh pr checks` line it read. No scenario step is added (the CLI does not change).

## Open questions

1. Windows coverage alternative: a `windows-latest` leg of the `scenario` job in `ci.yml` instead
   of the local run on the stack's top. Cost: a Windows runner is slower than ubuntu (likely
   several minutes, not measured here) and runs on every PR push, and the job becomes a CI change
   whose first run alone proves it on the runner (paths, file locks, uv cache cold). The default
   stays A (decision 3); does the user want B instead, or both?
2. A non-stack batch (parallel or series with no forge stack): which CR carries the one local
   Windows `just scenario`? Proposed: the last CR the user will merge (a series' last, a parallel
   batch's last handed back), or a follow-up run on main; the answers name only the stack's top.
3. This CR's own long gate: run `just scenario` locally as the current `AGENTS.md` says (the
   proposed default), or does the user accept the pipeline job already for this CR?
