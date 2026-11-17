# Change Specification: one rule for a worker reply that breaks its format

No issue.

## Goal

In batch-16 the rules for the workers' replies already existed, and they were broken anyway. A
round-2 Coder was resumed instead of started fresh. A Verifier proved a refusal without its
command. An Inspector gave its verdict in prose. A conflict resolution left a byte-order mark. No
Inspector ran again after three rebases that resolved conflicts. The source is batch-16's retro,
points 6, 7, 8, 9 and the Inspector part of 11, reviewed by an advisor.

The user wants one Driver-side rule instead of more specific ones: a reply that breaks its format is
a failed worker. The Driver starts it once more with the same brief. It never reads meaning into the
reply and never resumes the worker by message. Two smaller rules come with it: `conflicts.md` names
the fast gate it ran and the result, and a forge 5xx or network failure runs the same command once
more and then becomes `blocked infra:`.

Decisions (`02-answers.md`, 2026-11-13): the proposal as filed is the scope ("ok pour tout").
Points the request leaves open take this specification's defaults, listed at the end. The CR joins
the running batch-17.

## What changes

Only the cards: `skills/chantier/references/driver.md`, `skills/chantier/references/worker.md`,
and one line of `skills/chantier/references/concepts.md` (default D1). No CLI, no hook, no type,
no agent file (`agents/`, `com.github.copilot/agents/`): the CLI knows no role, and the agent files
only name the cards. The cards are host-neutral, so both hosts read the same text.

### 1. `driver.md`, "Your means": a reply out of format is a failed worker

Add a bullet right after the one on starting children (the bullet that ends at line ~36,
"…and you do your part without it."). It covers every worker the Driver starts. It says, in the
card's own style:

- Each worker's reply has the format its section of worker (`worker.md`) names. Before acting on a
  reply, the Driver checks it against that format:
  - Inspector, and each extra review step: the reply is the JSON object alone, parseable, with
    `verdict` exactly `APPROVE` or `FIX-REQUIRED` and `head` a commit SHA. Prose, prose around the
    JSON, or a verdict word outside the JSON fails.
  - Verifier: the reply is `VERIFIED` or `NOT VERIFIED` and the claims that failed. `verify.md`
    exists with its `Head: <sha>` line. Each claim in it names the SHA it was judged at (or
    `carried from <sha7>: <reason>`), the command it ran and that command's output. A claim
    without its command, output and SHA is a proof out of format, and so is a claim given as prose
    ("refused", "passes") with no command. The verdict is recorded at that head (`$CHANTIER
    handoff <cr>` shows the last verdict).
  - Conflict resolver: `conflicts.md` exists, with each conflicted hunk and the choice made, and
    the fast gate's command and result (section 3).
  - Coder, Investigator and Debugger: their output file exists (`r<n>.md`, `investigation.md`,
    `diagnosis.md`), and every gate it claims names its command and result.
- A reply out of format is a failed worker. The Driver never reads a verdict, a pass or a choice
  into it, never fixes it, and never asks the worker by message to fix it. Instead it records
  `$CHANTIER note <cr> "restart: reply out of format: <what is missing>"` and starts one new
  worker of the same role with the same brief, as for a refused first line (no `round`). The new
  worker's brief also says what the failed reply lacked. For a Coder, this new start is the
  restart of a failing coder of "CR driver": it counts as that round's one restart.
- A second reply out of format from the restarted worker (default D2): a Coder's is the next round
  (`$CHANTIER round`), as the "CR driver" section already says of a second failed coder. Any
  other role's is `handback <cr> blocked question: <role> replied out of format twice: <what is
  missing>`. The stack driver sends `[stack→foreman] anomaly <cr> <role> replied out of format
  twice: <what is missing>`.
- A worker is never resumed by a message (on Claude Code, `SendMessage` to its agent id). Only a
  new start continues its task. A new round is always a new child, never the previous round's
  Coder resumed.

The bullet on line ~28-31 ("A worker refused for its first line, or ended by a host failure, gets
one new start…") stays as it is. The new bullet refers to it for the form of the new start.

### 2. `driver.md`, "Your means": a forge 5xx or network failure

Add one bullet next to the Push bullet (after line ~95, before "Open or edit the PR yourself"),
for every Driver that runs `git`, `gh` or `glab` against a remote:

- A remote command (`git fetch`, `git push`, `gh`, `glab`) that fails with a forge server error
  (an HTTP 5xx) or a network failure (no route, a reset or timed-out connection, a name that does
  not resolve) runs the same command once more, at once and with no `sleep`. Before re-running a
  command that creates or moves something (`git push`, `gh pr create`, `glab mr create`, `gh pr
  edit`), the Driver first checks whether the first attempt took effect (`git ls-remote <remote>
  <branch>`, `gh pr list --head <branch>`, or the forge's equivalent) and does not run it again
  if it did (default D3). The Driver notes it: `$CHANTIER note <cr> "infra re-run: <command>:
  <exact error>"`. If the second attempt fails the same way, the CR Driver and the Release driver
  end with `handback <cr> blocked infra: <command>: <exact error>`. The stack driver sends `[stack→foreman] anomaly
  <cr> infra: <command>: <exact error>`.
- A refusal (an HTTP 4xx, a denied permission, a protected branch, a failed lease) is not an
  infrastructure failure. It keeps its own routes (`blocked refused`, the force-push route, a
  failed lease examined), with no re-run.

The CI rule ("an infrastructure failure gets one re-run", line ~163) is about a CI job, and the
Release driver's "On the infrastructure: one re-run, then `blocked infra:`" (line ~525) is about a
step of the procedure. Both stay. The new bullet is the same rule for a single command.

### 3. `worker.md`, "Conflict resolver": `conflicts.md` names the fast gate

At line ~149, change the output sentence so that `conflicts.md` holds each conflicted hunk and the
choice made, and also the fast gate's command, as run, and its result (the pass or the failing
lines). With no fast gate in the project's rules, it says so in one line. A `conflicts.md` without
this line is a reply out of format (section 1). The no-BOM check before `git rebase --continue`
stays as written.

### 4. `worker.md`, the shared paragraph and the Verifier

- In the shared paragraph (line ~20-21, "replies in at most ten lines, or in the format its
  section names"), add: a reply out of that format is a failed worker, which the Driver starts
  again rather than reads ([driver](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/driver.md)). The worker's reply is the whole of its output to
  its Driver.
- In "Verifier" (line ~91-92), make the existing rule explicit for a refusal or a negative claim:
  "each claim with the SHA it was judged at, the command and the output that prove it" also holds
  for a claim that something is refused, absent or unchanged. Its proof is the command that shows
  the refusal and that command's output. A claim without them is out of format.

### 5. `driver.md`, "CR driver": the Inspector after a resolved conflict

Point 11 of the retro (no Inspector run again after three rebases that resolved conflicts) is
covered by the paragraph at line ~305-311, which is clarified (default D4). A rebase during which a
`conflict-resolver` ran is always a change of the CR's patch. The `inspector` on that change is
due without reading a range-diff to decide it. Each such rebase gets its own `inspector` before the
next push, and its pass is recorded as `move <old7>..<new7> (conflict) inspector approved at
<head>`. Several rebases since the last push are inspected once, on the patch as it stands after
the last of them, against the head of the last pass.

### 6. `concepts.md`, the restart causes

In "An agent that ends before its part is done" (line ~317-320), the list of causes gains `reply
out of format: <what is missing>` (default D1), so that the Driver's `restart:` note uses a cause
the list already names. Rule 3 ("A fresh child per round", line ~376) stays as it is. The "One way,
never both" bullet already limits a resume by message to the Foreman's `taken back:` note, so it
stays too.

## Out of scope

- Any CLI change: no check of a reply's format, of a restart or of a re-run in `rails.py` or
  `commands.py`. The CLI knows no role.
- A new escalation trigger: a worker that replies out of format twice does not escalate (default
  D2 routes it to the user).
- A BOM check written into `conflicts.md` per resolved file (default D5: not added). The rule
  against adding a byte-order mark stays where it is, and the Inspector after a resolved conflict
  (section 5) reviews the resolved patch.
- New eval scorecard rows (`evals/SCORECARD.md`) and new scenario checks (default D6).
- The Release driver's procedure and the CI wait rules, apart from the shared bullet of section 2.

## Batch-17 and CR-221

This CR touches no CLI file: only `driver.md`, `worker.md` and `concepts.md` of
`skills/chantier/references/`. CR-221 splits the CLI into modules and does not touch these cards,
so this CR does not wait for it. No other CR of batch-17 changes `driver.md` or `worker.md`.
CR-224, CR-226 and CR-227 edit other parts of `concepts.md`, which is a shared file and not a
need: a rebase settles it.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes. A change to the cards takes the long gate (`AGENTS.md`). Its card-text
  check at `scenario/run_scenario.py:2840-2847` still finds `` `context: <where it stopped `` in
  `driver.md`.
- The diff shows each of sections 1 to 6 at the places named, and nothing else changed:
  `git diff --stat <base>..HEAD` lists only the three cards, and the CR's archive when the project
  asks for it.
- The Verifier quotes, with `git grep -n` at the pushed head, the lines that carry each rule:
  `reply out of format` in `driver.md`, `worker.md` and `concepts.md`; `infra re-run` and
  `blocked infra:` in the new bullet of `driver.md`; the fast gate in `worker.md`'s "Conflict
  resolver". It reads each one against this specification.
- Nothing runs to show before and after: this is a change to card text alone. The before/after is
  the cards' diff.

## Open points, with the default taken

- **D1.** Add `reply out of format: <what is missing>` to the restart causes of `concepts.md`.
  The request names only `driver.md` and `worker.md`. Default: add it (one line), so that the
  `restart:` note names a cause from the list.
- **D2.** A second reply out of format from the restarted worker. Default: for a Coder, the next
  round (the existing rule for a second failed coder). For any other role, `blocked question:`
  for the CR Driver and an `anomaly` for the stack driver. No new escalation trigger.
- **D3.** Before re-running a command that creates or moves something after a 5xx or a network
  failure, check whether the first attempt took effect, so that no PR is opened twice. Default:
  check first. The re-run waits no time (no `sleep`, rule 8).
- **D4.** The missed Inspector after a resolved conflict (retro point 11). Default: clarify the
  existing paragraph so that a `conflict-resolver` run always triggers the Inspector, with no
  range-diff judgment, before the next push. Several rebases since the last push are inspected
  once, on the patch after the last of them.
- **D5.** A per-file BOM check line in `conflicts.md`. Default: not added. Only the fast gate
  line, which the request names, is added.
- **D6.** A scenario check on the new card text, like the one at `run_scenario.py:2840`. Default:
  none. Tests stay few, and the evidence is the cards' diff.
