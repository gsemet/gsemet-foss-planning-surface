# Change Specification: a spec's guard checks run on the shipped files

## Goal

In batch-24, CR-344 (board design system) needed 6 rounds on Opus and a user grant of rounds. The
Inspector found from round 3 that the design tests ran on prepared texts, not the real stylesheets
and js files; nothing in the spec-writer's or critic's card asks a specification to say that such
checks read the shipped files. CR-344's own specification did ask for checks on the real files;
the Coder left them out, and the Inspector caught it only at round 3 (sc-Q6).

After this change, a specification whose checks guard shipped files says that they read the
shipped files. When the spec critic runs, it asks for this. From round 1, the Inspector checks that
each test the specification names reads the shipped files.

The decisions come from `02-answers.md`, all settled by the Chief of Staff on the user's word
("file all six and run them in batch-24", 2026-11-18): sc-Q1 to sc-Q6.

## What changes

Cards only, in `skills/chantier/references/`. The CLI, the hooks, the agent files, the tests and
the docs do not change (sc-Q5).

### 1. `spec-writer.md`, "Output"

In the bullet list "A rich specification holds:", insert one bullet right before "- The evidence
that proves it: the checks and the scenario steps." (today line 39). Wording, or close to it:

> - When a check guards a shipped file (a card, a stylesheet, a script, a page, a hook, a default
>   configuration, a template: it asserts that file's content), the evidence says that the check
>   reads that file from the repository as it ships, at the head under test, not a copy or a text
>   the test prepares. A prepared text is only for a case the shipped file cannot hold (a refusal,
>   a broken input), named as such and paired with a check on the shipped file.

This covers sc-Q1 (what counts) and sc-Q2 (what the specification says).

### 2. `spec-critic.md`, "What you look for"

Kind 1 ("A gap with the request's intent", today lines 22-24): add one sentence at the end of its
text. Wording, or close to it:

> Evidence that does not prove what is asked counts too: a check that guards a shipped file but
> reads a copy or a prepared text where the shipped file would do (`spec-writer.md`, "Output");
> this is about evidence, not an implementation detail.

The closing clause keeps the finding clear of the card's rule against proposing "an implementation
detail the specification leaves to its Driver" (today line 41).

There is still no fifth kind (sc-Q3). "Only these four", the reply's kinds `(intent,
inconsistency, claim or bundle)` and the list in `chief-of-staff.md` ("The spec critic", lines
408-411) stay as they are.

The critic's existing rule on behaviour decides how such a finding is sorted. It does not touch
behaviour, so the critic gives the fix in one line. Step 3 of `chief-of-staff.md` then treats it as
a fix, and step 4 ("the fixes first") sends it to the spec-writer (sc-Q4). Neither card says this
again.

### 3. `inspector.md`, "Your part"

Add one paragraph right after the host and default matrix paragraph ("When the specification or
your prompt names a host and default matrix ...", today lines 72-74). Wording, or close to it:

> From round 1, each test the specification names that guards a shipped file must read that file
> as it ships, at the head under test (`spec-writer.md`, "Output"). A named test missing from the
> diff, or one that checks only a prepared text where the shipped file would do, is `blocking`.

This covers sc-Q6.

### 4. Both hosts

The agent files (`agents/spec-writer.md`, `agents/spec-critic.md`, `agents/inspector.md` and their
Copilot twins in `com.github.copilot/agents/`) only name the cards, so they do not change. The rule
reaches both hosts through the cards.

## Out of scope

- The Coder's and Verifier's cards (sc-Q5, as revised by sc-Q6: the Inspector's card gets the one
  paragraph of §3, nothing else).
- Any CLI rail, lint or new command, and any check that reads test sources (AGENTS.md: no
  speculative CLI tool).
- A new test. The existing structure tests load the cards. A test that only asserts a sentence is
  present would guard wording, not behaviour.
- The backlog item `2-backlog/P3/spec-external-fact-source` also adds a sentence to the spec-writer
  card, but to a different bullet. The two do not conflict.

## Evidence

- `just check` passes in the worktree at the pushed head (AGENTS.md, a cards-only change: no
  `just eval-dry-run` owed).
- The pipeline's `just scenario (ubuntu-latest)` job is green at the PR's head (AGENTS.md: a change
  to the cards passes it before its PR). The local Windows run follows the batch's rule for the CR on
  top of the stack.
- The diff touches only `skills/chantier/references/spec-writer.md`,
  `skills/chantier/references/spec-critic.md` and `skills/chantier/references/inspector.md`: one
  bullet added to the first, one sentence added to kind 1 of the second, one paragraph added to
  "Your part" of the third. `git diff --stat <the CR's base>...HEAD` (its parent in the stack, or
  main) shows three files.
- Reading check, quoted in the PR: replay CR-344's specification (section 8,
  `4-batch/3-done/344-board-design-system/03-change-spec.md` in the planning folder, or its
  archive) against the new spec-writer bullet, and state whether it meets it (it does: it reads
  `<web>` and pairs the prepared texts with checks on the real sheets). Then replay one
  prepared-text-only check, written for the PR, and quote the one-line fix the critic's kind 1
  would give.

No host and default matrix: the change does not depend on the host or on a shipped default versus
a configured value.
