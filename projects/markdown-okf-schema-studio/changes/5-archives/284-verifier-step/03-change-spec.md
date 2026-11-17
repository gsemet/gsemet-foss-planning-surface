---
title: Spec, a Verifier step before a pull request turns ready
description: Exact text changes that add a Verify step (Chantier's Verifier, simplified) to the lifecycle and PR guidelines.
status: spec
date: 2026-11-11
---

# Spec: Verifier step

Inputs: `01-intent.md`, `02-answers.md`, `task.md`. The owner's answers are final: a simple
Verifier like Chantier's; no Investigator; no Chantier change; no code, requirements or workflow
change.

## Summary

After CI is green (step 9) and before the pull request turns ready, a Verifier proves the spec at
the pushed head, captures the before/after evidence for a visible change (or writes one line "no
visible change" with the reason) and checks the posted PR body against the template and the diff.
`NOT VERIFIED` on the code is a new round; on the body or the evidence only, the driver fixes
them and runs the Verifier again. Marking the PR ready requires `Verdict: VERIFIED`.

Two files change: `.agents/guidelines/change-requests-lifecycle.guidelines.md` (12 edits, numbered 1 to 11 plus the Step 4 row rule) and
`.agents/guidelines/pull-request.guidelines.md` (3 places). `AGENTS.md`, the constitution,
`ci.guidelines.md`, `stacked-prs.guidelines.md` and `scripts/generate_orchestrator.py` do not change:
the script reads `step:` as free text (`(?P<step>.+?)`), and no other file cites a step number
(searched `AGENTS.md`, `.agents/`, `scripts/`, `justfile`, `docs/` for `Notify`, `step 10`, `step 11`,
`1–11`, `steps 8`).

## Decision: renumber

The Verify step becomes **step 10**; Notify becomes **step 11**; Land becomes **step 12**. Every
reference is listed below (places 4 to 11). No "9b".

Two terms used below, defined once in the new text:

- **Base** of a CR: `origin/main`, or in stack mode the branch below it in the stack (its PR's
  base).
- **Evidence plan**: none is written (no Investigator). The Verifier picks the capture technique
  from the project's rules (see place 3).

## Places changed: `change-requests-lifecycle.guidelines.md`

### 1. Layout tree (lines 58-60)

Current:

```text
│   └── work/
│       ├── coder/T1-r<n>.md      ← coder report, round n
│       └── inspector/T1-r<n>.md  ← Inspector verdict, round n
```

Replace with:

```text
│   └── work/
│       ├── coder/T1-r<n>.md      ← coder report, round n
│       ├── inspector/T1-r<n>.md  ← Inspector verdict, round n
│       └── verifier/             ← Verifier verdict T1-r<n>.md, evidence/ (before-after.md, images)
```

### 2. Roles and models table, new row after Inspector (line 82)

Current last rows:

```text
| Inspector | 1 per round | Sonnet | GPT 6.1 Sol (copilot) | edits files, lives past its round |
```

Add after it:

```text
| Verifier | 1 per run of step 10 | Sonnet | GPT 6.1 Sol (copilot) | is the round's coder or Inspector, edits code, lives past its run |
```

Add one bullet after the "Never move a task up a level" bullet (line 90):

```text
- **Verifier**: a fresh agent started by the driver (the stack driver in stack mode), never the
  round's coder or Inspector, so it does not grade its own work. It reads the project; it never
  edits code. It may create one detached worktree (`git worktree add --detach <path> <base>`) and
  must remove it before it returns. It stays on Sonnet for every blast radius.
```

### 3. Lifecycle table (lines 104-106)

Current:

```text
| 9 CI | driver | Watch the checks ... Never weaken a test. |
| 10 Notify | driver | CI green at the head and the review approved: mark the PR ready for review, then write `status: ready` in the header, then return. A CR sent back for a new round goes back to draft first. |
| 11 Land | Foreman | After the user merges: write `report.md`, ... After moving the folder, run `just orchestrator`. |
```

Step 9 stays as is. Insert a new row after it, then renumber the next two (only the leading
`10 Notify` and `11 Land` labels change, plus the Notify text below):

```text
| 10 Verify | Verifier (sub-agent started by the driver) | CI green at the head and the review approved: start a Verifier, fresh, on the pushed head. It writes `work/verifier/T1-r<n>.md` starting `Verdict: VERIFIED` or `Verdict: NOT VERIFIED`, and proves three things, each one a command run at the pushed head with its output (the notes of the coder and the Inspector, and a green CI, are not proof): (a) every claim of `03-change-spec.md` (each acceptance check and each behaviour the spec states); (b) the evidence of the change, in `work/verifier/evidence/` with a `before-after.md` that lists each pair, what it shows and the command that reproduces it: for a change the user sees, the before on a detached worktree of the base and the after at the head, taken with the technique the project's rules give (for the editor and the preview, the headless visual run of the local gates; otherwise the e2e group that covers it), light and dark when themes matter; or, for a change nobody sees (process text, tooling, internals), one line "no visible change" and the reason; (c) the posted PR body, read with `gh pr view <n> --json title,body` and checked against the diff and [pull-request.guidelines.md](pull-request.guidelines.md): every section of `.github/PULL_REQUEST_TEMPLATE.md` is present and filled; Impacts holds the before/after images or the "no visible change" line; "Autonomous decisions" exists and lists every choice a coder or the driver made without the owner (or says "None"); and Summary, Deliverables and Changes describe what the diff does, no more and no less. `NOT VERIFIED` because of the code (a claim fails) is a new round: step 5, round n+1, counted in the round limit. `NOT VERIFIED` because of the body or the evidence only: the driver fixes it itself (pushes the screenshots as in "Screenshots in the PR" of [pull-request.guidelines.md](pull-request.guidelines.md), `gh pr edit <n> --body-file <file>`), then runs the Verifier again; no round is used. When both causes are present, the code comes first. |
| 11 Notify | driver | CI green at the head, the review approved and `Verdict: VERIFIED` at that head: mark the PR ready for review, then write `status: ready` in the header, then return. A CR sent back for a new round goes back to draft first. |
| 12 Land | Foreman | (unchanged text) |
```

"Verified at that head" means the verdict file names the head SHA it ran on; a push after the
verdict makes it stale, so the driver runs the Verifier again.

Add this sentence at the top of `work/verifier/T1-r<n>.md` format (put it as the next paragraph
after the "Round limit" paragraph, line 111, as a new paragraph):

```text
**Verifier output**: `work/verifier/T1-r<n>.md` starts with `Verdict: VERIFIED` or `Verdict:
NOT VERIFIED`, then the head SHA, then each check as a claim, the command, its output (an excerpt
with the exit status) and pass or fail. A verdict whose SHA is not the current head is stale. The
evidence files are in `work/verifier/evidence/`; if a capture is impossible, `before-after.md`
says why, and that alone is not `NOT VERIFIED` unless the project's rules require the capture.
```

### 4. Round limit paragraph (lines 108-111)

Current: "a round is one coder pass, whether an Inspector verdict or a CI failure triggered it."

Replace with: "a round is one coder pass, whether an Inspector verdict, a CI failure or a `NOT VERIFIED`
on the code triggered it." The rest is unchanged. (A rerun of the Verifier for the body or the
evidence is not a round.)

### 5. `STATUS.md` header, "One writer" (lines 123-125)

Current: "... the CR driver for steps 5–10 (in stack mode: until its branch joins the stack), the stack driver once the branch is in the stack, and the Foreman for step 11."

Replace with: "... the CR driver for steps 5–11 (in stack mode: until its branch joins the stack), the stack driver once the branch is in the stack, and the Foreman for step 12."

### 6. `STATUS.md` header template (line 132)

Current: `· step: <1–11 name> ·`. Replace with: `· step: <1–12 name> ·`.

### 7. Foreman heartbeat step 2 (line 346)

Current: "On a merge: step 11 for that CR". Replace with: "On a merge: step 12 for that CR".

### 8. Driver prompt (lines 378-379)

Current:

```text
> Resume from the `STATUS.md` header and write `driver: <your id>` in it. Run steps 5–10: start a
> coder, then a separate Inspector, per round, in the background; commit, rebase, push, PR; watch
> CI in slices of at most 5 minutes. Rewrite the header at every transition and every slice. Never
> code or review yourself. Return with `status: ready` or `status: blocked` and a question with
> your recommended answer.
```

Replace with:

```text
> Resume from the `STATUS.md` header and write `driver: <your id>` in it. Run steps 5–11: start a
> coder, then a separate Inspector, per round, in the background; commit, rebase, push, PR; watch
> CI in slices of at most 5 minutes; then start a separate Verifier at the pushed head (step 10)
> and mark the PR ready only on `Verdict: VERIFIED`. Rewrite the header at every transition and
> every slice. Never code, review or verify yourself. Return with `status: ready` or
> `status: blocked` and a question with your recommended answer.
```

### 9. Stack-mode sentence under the driver prompt (lines 384-386)

Current: "In stack mode the Foreman replaces "Run steps 5–10 … PR; watch CI in slices of at most 5 minutes" with "Run steps 5–7: ...""

Replace "Run steps 5–10 … PR; watch CI in slices of at most 5" with "Run steps 5–11 … PR; watch CI in
slices of at most 5" (the quoted text must match the new driver prompt: the replaced span now ends
at "mark the PR ready only on `Verdict: VERIFIED`", so write the quote as `"Run steps 5–11 … PR;
watch CI … `Verdict: VERIFIED`"`). The replacement text "Run steps 5–7 ..." is unchanged.

### 10. Stack mode bullets (lines 393-401)

Current bullet 2: "One stack driver owns all the stacked branches. It runs steps 8–10 for every branch: it places the branch in the stack order, restacks, pushes with `--force-with-lease`, opens the PR against the branch below, links the PRs, watches CI and writes the headers of the branches in the stack."

Replace "steps 8–10" with "steps 8–11", and end the sentence with: "..., links the PRs, watches CI, starts the Verifier of each branch (its base is the branch below) and writes the headers of the branches in the stack."

Current bullet 3: "The stack driver marks each PR of the stack ready on its own, as soon as its CI is green at its head and its CR is `ready`, without waiting for the rest of the stack."

Replace with: "The stack driver marks each PR of the stack ready on its own, as soon as its CI is green at its head, its review is approved and the Verifier's verdict at that head is `VERIFIED`, and its CR is `ready`, without waiting for the rest of the stack."

Stack driver prompt (lines 414-416): "Open each PR as a draft and mark it ready on its own, as soon as its CI is green at its head and its CR is `ready`, without waiting for the rest of the stack." Replace with: "Open each PR as a draft; once its CI is green at its head, start a separate Verifier for it (step 10), and mark it ready on its own only when the Verifier wrote `Verdict: VERIFIED` at that head and its CR is `ready`, without waiting for the rest of the stack." A `NOT VERIFIED` on the code goes back to the Foreman as a failing branch, like a red CI (a new round for that CR).

### 11. Sub-agent rules and `report.md`

Sub-agent rules (copy into `rules.md`), add one bullet at the end:

```text
- Verifier: follow step 10 of the lifecycle ("Verify"). The task links to that step; it never
  restates what the Verifier proves or when a screenshot is required.
```

`report.md` "Proof of completion" (line 462), current: "- Tests added (failed before, pass after), local gate counts, CI run id, screenshots."
Replace with: "- Tests added (failed before, pass after), local gate counts, CI run id, the Verifier's verdict with its head SHA (`work/verifier/T1-r<n>.md`), and the before/after evidence (screenshots, or the "no visible change" line)."

## Places changed: `pull-request.guidelines.md`

### 12. Screenshots bullet in "PR body for an external reader" (line 37)

Current: `- Screenshots go in Impacts (see "Screenshots in the PR").`

Replace with:

```text
- Impacts holds the evidence of the change: the before/after the Verifier produced (screenshots,
  see "Screenshots in the PR"), or one line "No visual change" with the reason. Impacts never stays
  at the template's comment; the Verifier fails a body whose Impacts has neither.
```

Line 33 (`screenshots before/after for UI changes`) stays.

### 13. "Draft until mergeable" ready condition (lines 45-46)

Current:

```text
- Mark it ready with `gh pr ready <n>` only when CI is green at its head, the review is approved and
  `ready` is reported.
```

Replace with:

```text
- Mark it ready with `gh pr ready <n>` only when CI is green at its head, the review is approved,
  the Verifier's verdict at that head is `Verdict: VERIFIED` (step 10 of
  [change-requests-lifecycle.guidelines.md](change-requests-lifecycle.guidelines.md)) and `ready`
  is reported.
```

Line 48 (stack, "as soon as it is mergeable") stays: "mergeable" now includes the verdict.

### 14. "Screenshots in the PR" (line 74)

Current first sentence: "Take them from the e2e/visual run of the final code, light and dark when themes matter."

Replace with: "The Verifier takes them (before on a detached worktree of the base, after at the pushed head) from the e2e/visual run, light and dark when themes matter, and leaves them in `work/verifier/evidence/`; the driver pushes them as follows." The bash block and the branch-naming paragraph are unchanged. Add after the last paragraph (line 91): "The driver puts the links in Impacts with `gh pr edit <n> --body-file <file>`, then runs the Verifier again if the body check had failed."

## Rule: `task.md` links, never restates

Add to the lifecycle guideline, in "Step 4 Brief" row (line 99), after "`STATUS.md` header, then run `just orchestrator`.":
"`task.md` links to step 10 for the evidence and the PR body check; it never restates when a screenshot is required (a hand-written copy drifts)."

(This is place 15 of the lifecycle guideline's list; apply it with the others.)

## Unchanged on purpose

- Inspector: still reads the diff only; no Investigator, no evidence plan (owner: "simple").
- "Responsiveness": the Verifier is one run then returns, like the Inspector; no new rule. The
  driver watches the Verifier in the background and keeps writing the header (`step: 10 Verify`).
- Chief of Staff's mergeable check keeps its rule; the Verifier now covers the same ground first.
- Chantier repository: not touched.

## Acceptance checklist

- [ ] The Lifecycle table has `10 Verify`, `11 Notify`, `12 Land`, in that order; step 9 unchanged.
- [ ] `grep -n "Verifier" .agents/guidelines/change-requests-lifecycle.guidelines.md` hits the
      layout tree, the roles table and bullet, step 10, the round-limit paragraph, the driver
      prompt, stack mode, the stack driver prompt, `rules.md` bullets and `report.md`.
- [ ] No stale numbering: `grep -nE "steps? (5–10|8–10)|step 11 for|1–11" .agents/guidelines/change-requests-lifecycle.guidelines.md` returns nothing.
- [ ] Step 10 text states: command and output per spec claim; CI and notes are not proof; before
      on a detached worktree of the base, after at the head; or "no visible change" with the reason;
      PR body check (template sections, Impacts, Autonomous decisions, body matches the diff);
      `Verdict:` first line; `work/verifier/evidence/before-after.md`; code failure is a round;
      body or evidence failure is fixed by the driver and rerun.
- [ ] Step 11 requires `Verdict: VERIFIED` at the head; the Verifier row says Sonnet, fresh, never
      the coder or Inspector, never edits code, removes its detached worktree.
- [ ] `pull-request.guidelines.md`: Impacts takes the Verifier's before/after or the "No visual
      change" line; the ready condition names the Verifier.
- [ ] The Step 4 row says `task.md` links to step 10 and never restates the screenshot condition.
- [ ] `git diff --stat origin/main` lists only the two guideline files.
- [ ] `just check`, and `just preflight` (static stage is enough; the report says which ran).
- [ ] No requirements log entry; no `src/`, `test/`, `requirements/`, workflow change.

## Gates (from task.md)

`just check`; `just preflight` (static stage). No heavy CI run. Blast radius 1: Inspector on
Sonnet. Commit `docs:` per the commit guidelines, with the attribution line of the session. PR
opened as a draft (`gh pr create --draft`), outside the stack, from `origin/main`; `gh pr ready
<n>` only at `ready`. No issue: no `Fixes`, no issue comment.

## PR content

Title: `docs: add a Verifier step that proves the change and checks the PR body before it turns ready`

Summary:

Pull requests were marked ready with a body that skipped the template and with no before/after
screenshot for a visible change, because nothing checked either: the reviewer of the diff does not
read the posted body, and the screenshot rule was copied by hand into each task. This adds a
Verify step after CI where a fresh Verifier proves the change at the pushed head and checks the
body, and marking a PR ready now requires its `VERIFIED` verdict.

Deliverables: a table of the new flow.

| Step | Before | After |
| --- | --- | --- |
| 9 CI | green CI | green CI |
| 10 | Notify: mark the PR ready | Verify: Verifier proves the spec, captures the before/after, checks the body |
| 11 | Land | Notify: mark ready only on `VERIFIED` |
| 12 | none | Land |

Changes:

- Lifecycle guideline: step 10 Verify (renumbering Notify to 11 and Land to 12 and every step
  reference), the Verifier role and its output folder, the driver, stack-driver and `rules.md`
  text, `report.md` proof of completion, and the round limit counting a `NOT VERIFIED` on the code.
- Pull request guideline: Impacts holds the Verifier's before/after or the "No visual change"
  line, the ready condition names the Verifier, and the screenshots section says who takes them.

Impacts: process text only. From the next change on, a pull request cannot be marked ready
without a verdict at its head, an Impacts section with evidence, and a body that matches the diff.
No visual change.

Blast radius: grade 1, two guideline files; a plain `git revert` restores the previous process.

Test plan: `just check` and the static stage of `just preflight`; the acceptance greps above.

Autonomous decisions:

- Renumbered the steps (Verify is 10) rather than naming it 9b, so the header and every reference
  keep one number per step.
- A body or evidence failure does not use a round; a code failure does (the owner's answer).
- A verdict at an older head is stale and the Verifier runs again after any push.
- The Verifier's model stays Sonnet for every blast radius, as the owner asked.

Internal references: none needed beyond the closing line.

Ends with the line: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
