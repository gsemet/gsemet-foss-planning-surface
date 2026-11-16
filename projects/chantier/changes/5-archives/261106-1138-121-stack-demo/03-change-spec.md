# The Chief of Staff offers a guided demo of a ready stack

When a stack is ready, the Chief of Staff reports its cost and offers a demo of what the stack
delivers. A subagent prepares it; the Chief of Staff then guides the user, who tries each change
themselves. This CR changes the cards and adds one agent; the CLI gets no new command. It builds on
CR-113 and CR-114, and runs after batch 05.

## The Chief of Staff's subagents

`chief-of-staff.md` changes "You own no background agent": the Chief of Staff may start subagents
for an exploration, a prototype or a study, whose result is a report or a study, in this session.
They never start an implementation: no commit, no push, no PR, nothing in a CR's worktree, and a
prototype lives in a temporary folder and is thrown away. Implementation still goes through a CR and
the Foreman. Their cost is in the Chief of Staff's line, as CR-113 measures it, outside the budget.
It still never messages a Driver.

## The offer

At the last `ready` of a stack, when no CR of the batch is working, the report of CR-114 ends with
the offer of a demo. Nothing starts without the user's yes, and a no ends it. The Chief of Staff has
no timer: this happens on the Foreman's message.

## The study

On a yes, the Chief of Staff starts a new agent, `demo-explorer`, one file per host, whose card is a
section of `worker.md`. It reads, in this order:

1. The PRs or MRs, with the forge's CLI: description, diff, comments, attached images and videos.
2. The batch's CRs: the specification, `02-answers.md`, `work/`, the Verifier's `evidence/`.
3. The code, only if these leave a question: the stack's highest worktree if it still exists,
   else a clean detached worktree at the top of the stack, which it removes at its end.

It writes `demo/demo.md` in the batch's folder, in the user's language:

- What is delivered, by feature; the bugs fixed; the important architectural impact.
- The evidence for each, with its link or path; before and after screenshots when there are some.
  It says what has none, and invents nothing.
- For each change, a walkthrough: the setup, where to click or what to run, what was there before,
  what the user should see now.
- What the walkthroughs need: a fixture or a small ephemeral environment, and how to remove it.

## The demo

The Chief of Staff shows the summary, then guides one change at a time and waits for the user's
result. It prepares the fixture or the environment outside the repository's tracked files and
removes it at the end. The code under demo is the top of the stack, not yet merged, so the demo also
serves the decision to merge. How to run the project comes from its `AGENTS.md`; nothing written is
a question for the user.

A problem found: the user decides. It becomes `order note <cr>`, a round of fixes, or goes to the
inbox when the CR's rounds are spent or the idea is new.

## Out of scope

- The Drivers and the Verifier do not change: producing before and after evidence is CR
  `delivery-evidence`, and the study reads what that CR leaves in `work/` once it exists.
- The QA driver stays as it is, on the default branch's head.
- A parallel batch: the offer is for a stack.

## Done when

- `chief-of-staff.md`, `worker.md`, `concepts.md` and `routing.md` say this, `SKILL.md` has an entry
  point for "demo", and `agents/` and `com.github.copilot/agents/` have identical bodies.
- `tests/test_structure.py` knows the new agent if it lists them.
- `just check` and `just scenario` pass.
