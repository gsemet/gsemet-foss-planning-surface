---
type: cr-change-spec
description: Change specification of round-one-host-default-matrix, from the batch-24 retro point, the choices settled by the Chief of Staff on 2026-11-17 and the spec critic's finding.
---

# Change specification: round-one-host-default-matrix

## Goal

From the retro of batch-24, put in the batch by the user on 2026-11-17. CR-331 (escalation-gaps)
took 6 rounds, cost the batch's most ($9.00), and needed two grants of rounds from the user.
Each round, the Coder and the Inspector covered only the configured case on Claude Code. The
Verifier found the Copilot shipped-default case at round 4, after a push. Round 5 fixed it on a
hand-built shape, so it failed again; it passed at round 6 (`4-batch/3-done/331-escalation-gaps/work/verify.md`,
sections "5", "5 again"). This CR makes that case visible from round 1. When a CR behaves
differently by host or by shipped default versus configured value, its specification names the
host and default matrix. Round 1's Coder and Inspector briefs carry it. A Verifier probes it at
the committed head before the CR is ever pushed (so before round 1's `ship`).

## Today

- `skills/chantier/references/spec-writer.md`, "Output", list "A rich specification holds"
  (lines 24-37): it asks for evidence, but not for a matrix.
- `skills/chantier/references/driver.md`, "CR driver", the round paragraph (about lines
  601-640). Round 1 runs `coder`, `pr-body.md`, `inspector`, commit, rebase, the checks, the long
  gate, push, PR, `ship`, CI, and then the first `verifier`, at the pushed head. The checklist
  copies the specification's file edits only.
- `skills/chantier/references/inspector.md`, "Your part": a missing test is already `blocking`,
  but nothing names a host or default case.
- `skills/chantier/references/verifier.md`: "Evidence is a command run at the pushed head"
  (ground rules, line 28), and every start runs `$CHANTIER verdict` (line 80).
- The CLI needs nothing new. `phase <cr> verifier [detail]` is accepted at any step
  (`core/phases.py`), and no command checks when a Verifier runs. The probe writes no
  `verify.md` and runs no `verdict`, so the CLI's verdict and hand-back checks never see it.

## Decisions carried from 02-answers.md

- **The user (2026-11-17):** "remet les 5 dans le batch et on continue". This CR joins the batch
  with no grill.
- **matrix-Q1 (Settled by the Chief of Staff):** a CR has a matrix when what it changes behaves
  differently on Claude Code and Copilot, or with a shipped default and a user-configured value.
  The Spec-writer judges this. A CR with neither has no matrix, and nothing below applies to it.
- **matrix-Q2 (Settled by the Chief of Staff):** the matrix has one cell per combination that
  applies: each host, shipped default or configured value, and a host's refusal where one
  exists. Each cell gives the result it must show and the real flow that proves it: the CLI's own
  commands from a real state, with no user file for the shipped-default cell. A shape built by
  hand that the real flow does not produce proves no cell.
- **matrix-Q3 (Settled by the Chief of Staff):** the Driver puts the matrix in the evidence plan.
  From round 1 it also goes in the Coder's checklist (one line per cell) and in the Inspector's
  prompt. For the Inspector, a cell with no test, or one tested only on a hand-built shape, is
  `blocking`.
- **matrix-Q4 (Settled by the Chief of Staff):** after each round's commit, while the CR has never
  been pushed, a Verifier probes every cell at the committed head. This happens before the rebase
  and the long gate. A `NOT VERIFIED` probe is the next round, under the same round limit. The
  probe grants no round and uses none.
- **matrix-Q5 (Settled by the Chief of Staff):** the probe writes `work/verifier/matrix-r<n>.md`
  with a `Head:` line. It runs no `verdict` and no gate, captures no before/after and checks no PR
  description. The Verifier at the pushed head still runs. It is given the last probe file and
  the move, judges again the cells the move touched, and carries the others.
- **matrix-Q6 (Settled by the Chief of Staff):** if a specification written before this change
  names no matrix but the CR plainly depends on the host or on shipped defaults, the Driver writes
  the matrix into the evidence plan itself. The rest follows from there.
- **matrix-Q7 (Settled by the Chief of Staff):** cards only. No CLI change and no agent file
  change.

## What changes

All edits are in `skills/chantier/references/`. The agent files (`agents/`,
`com.github.copilot/agents/`) are not touched: the cards hold the contract.

1. `concepts.md`, "Words": add a new bullet right after "**Change Specification:**" (line 145):
   - **Host and default matrix:** the cases a CR must prove one by one, because what it changes
     behaves differently on each host (Claude Code, Copilot) or with a shipped default and with a
     value the user configured. There is one cell per combination that applies, including a
     host's refusal where one exists. Each cell gives the result it must show and the real flow
     that proves it: the CLI's own commands from a real state, with no user file for a
     shipped-default cell. A record or configuration shape built by hand, which the real flow
     does not produce, proves no cell. The specification names the matrix in its evidence. A CR
     with neither dependency has none.

2. `spec-writer.md`, "Output", list "A rich specification holds": add after the CI-job bullet
   (line 35):
   - When what the CR changes depends on the host or on a shipped default versus a configured
     value: its host and default matrix ([concepts](concepts.md), "Words"), in the evidence, one
     line per cell. Name no matrix when there is no such dependency.

3. `driver.md`, "CR driver", the round paragraph (about lines 601-640):
   - The checklist sentence (about line 604): when the specification or the evidence plan names
     a host and default matrix ([concepts](concepts.md), "Words"), the checklist also carries
     one line per cell from round 1: the cell, the result it must show, and the real flow that
     proves it. From round 2 on, the existing rule applies (only the items marked `open` or left
     unmarked). The Inspector's prompt carries the whole matrix every round.
   - The plan sentence (about line 602, "You answer for the CR's evidence plan"): a specification
     that names no matrix while the CR plainly depends on the host or on shipped defaults gets one
     in the plan, written by the Driver.
   - After the round's commit note (`r<n> approved at …, committed as <sha>`, about line 624) and
     before the rebase: while the CR has never been pushed and has a matrix,
     `$CHANTIER phase <cr> verifier matrix probe`, then a `verifier` whose `Note:` says
     `matrix probe` and gives the matrix. Its reply is checked as a Verifier's (first line,
     `Head:` equal to the committed head), but `Proof:` names
     `<work folder>/verifier/matrix-r<n>.md`, and no `verify.md` or `verdict` is expected from it.
     Record `$CHANTIER note <cr> "matrix probe <VERIFIED|NOT VERIFIED> at <sha7>"`. A
     `NOT VERIFIED` probe is the next round (`$CHANTIER round`, with the failed cells in its
     brief). Past the limit, it is `blocked rounds:` as for any round. A `VERIFIED` probe goes on
     to the rebase as today.
   - The first `verifier` at the pushed head is given the last `matrix-r<n>.md` as its previous
     judgment, with the move (the committed head to the pushed head, and the old and new base),
     as for any later `verifier`.

4. `inspector.md`, "Your part", after the `blocking` paragraph (line 68-70): when the
   specification or your prompt names a host and default matrix ([concepts](concepts.md),
   "Words"), each cell needs a test or a check in the diff that runs its real flow. A cell with
   none, or one tested only on a record or configuration shape built by hand, is `blocking`.

5. `verifier.md`:
   - Ground rules, the "Evidence is a command run at the pushed head" bullet (line 28): add
     "except a matrix probe (below), run at the committed head before the CR's first push".
   - "Your part": a new paragraph after the "Delta assessment" paragraph (line 112). With
     `matrix probe` in your note, prove each cell of the matrix your prompt gives, at the
     worktree's committed head (not pushed). Use each cell's real flow from a real state: the
     CLI's own commands on a scratch project or on the project's test fixtures, under the scratch
     rules above, and with no user file for a shipped-default cell. A hand-built shape proves no
     cell. Write `<work folder>/verifier/matrix-r<n>.md`, with a `Head:` line and each cell as a
     claim (SHA, command, output). Run no `$CHANTIER verdict` and no gate, capture no
     before/after, and check no PR description. Reply with the template, with `Proof:` naming
     that file.
   - Delta assessment: a previous `matrix-r<n>.md` given to you counts as a previous judgment, so
     its cells are carried or judged again by the same rule.

6. `concepts.md`, "Rules", rule 5 (line 641, "**Evidence is a command run at the pushed head, with
   its output.**"): after its first sentence, insert "(except a matrix probe, run at the committed
   head before the CR's first push: [verifier](verifier.md))".

No other card changes. In particular, `coder.md` (the checklist and its `done` / `open:` marks
already carry the cells), `spec-critic.md` and the CLI stay as they are.

## Out of scope

- Any CLI change: no new command, no refusal, no record of the probe. The probe leaves no
  verdict; the verdict that counts stays the pushed-head Verifier's.
- The round limit and who grants rounds (`order rounds` stays the user's).
- The docs' diagrams (`docs/*.svg` and their `-texts.md`): they show the main flow, which is
  unchanged. The probe only applies to a CR with a matrix.
- Matrices other than host and shipped-default versus configured (for example by operating
  system): CI and the Windows gate already cover those.
- Overlap: `driver-stops-background-tasks` (same batch) also edits `driver.md`. The overlap is in
  the text only; whichever merges second rebases.

## Evidence and gates (AGENTS.md)

- `just check` green in the worktree at the rebased head before the first push (Linux, macOS and
  Windows in CI). `just eval-dry-run` is not owed: this is a cards-only change.
- `just scenario (ubuntu-latest)` green at the PR's head before the PR turns ready (a change to
  the cards). If this CR is on top of the batch's stack, it also passes the local Windows
  `just scenario` (`chantier gate`) at its head before the user merges.
- No `just mod` (no `hooks/` or `types/`), and no screenshot (the pane is not touched).
- The Verifier proves each edit by command and output at the pushed head:
  - a Grep shows the "Host and default matrix" word in `concepts.md` and links to it from
    `spec-writer.md`, `driver.md`, `inspector.md` and `verifier.md`;
  - the round paragraph of `driver.md` puts the probe after the commit note and before the
    rebase, only while the CR is unpushed;
  - `verifier.md` states the pushed-head exception and the no-`verdict` rule of the probe;
  - a Grep shows rule 5 of `concepts.md` ("Evidence is a command run at the pushed head") carrying
    the matrix-probe exception and its link to `verifier.md`;
  - `git diff --name-only <base>..HEAD` lists only files under `skills/chantier/references/`
    (plus the release notes or changelog file, if the project's rules ask for one);
  - `uv run --no-sync --project . chantier phase --help` shows that `phase` takes `verifier` with a
    free detail (`commands/driver.py` `phase` logs it in the event's note; it is not kept as the
    step's detail for `verifier`), so the probe's step needs no CLI change.
- This CR has no host or default matrix of its own: it changes no behaviour that depends on the
  host or on shipped defaults, so it runs no probe.

## Open questions

None. Every choice the request left open is settled in `02-answers.md`.
