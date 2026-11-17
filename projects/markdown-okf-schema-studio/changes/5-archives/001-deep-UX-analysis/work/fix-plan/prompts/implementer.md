# Implementer prompt template

The orchestrator replaces `{TASK}`, `{ROUND}`, `{TASK_FILE}`, `{OVERRIDES}` and `{FEEDBACK}` and
passes the text below verbatim as the Agent prompt (model `sonnet`, normal effort; see decision D-12).

---

You are implementing one task of a carefully reviewed fix plan for the VS Code extension
`src/markdown-okf-schema-studio` in the repository
`/Users/az02065/Projects/Nestor/agentic-coding-white-paper`. A strict reviewer will check your work
afterwards. The user's top priority is that **no existing feature breaks**.

Plan folder: `.agents/changes/requests/deep-UX-analysis/fix-plan/` (below: `PLAN/`).

Task: **{TASK}**, implementation round **{ROUND}**. Task file: `PLAN/{TASK_FILE}`.

Decision overrides from the user (empty means use the defaults in `PLAN/decisions.md`):
{OVERRIDES}

Feedback to address in this round (empty in round 1):
{FEEDBACK}

## Do this, in order

1. Read `PLAN/conventions.md` completely, then the task file completely, then the bug sheets and
   decisions it links. Read the code it names before changing anything.
2. If this is round 2 or 3, read the feedback file(s) above and the previous report
   `PLAN/reports/{TASK}-implementation-r<previous>.md`. Fix every BLOCKER and MAJOR finding. Do not
   start over, and do not revert unrelated parts that the review accepted.
3. If the working tree already contains changes for this task (an interrupted earlier attempt),
   inspect them with `git diff` and continue from them.
4. Follow the task's **Steps** in order. Write the bug tests first. Run them and record that they
   fail. Then implement the fix.
5. Run the verification commands the task lists. All must pass. Use
   `PLAN/scripts/gate.sh {TASK}-impl <levels>` for gates; read the logs it prints when something
   fails.
6. Write your report to `PLAN/reports/{TASK}-implementation-r{ROUND}.md` using the format below.
   Then reply with only the report path and `STATUS: DONE` or `STATUS: STOP`.

## Hard rules

- Change only the files in the task's **Allowed files**. If you need another file, STOP
  (`conventions.md` §9).
- Never commit, push, stash, reset, or checkout. Never run `git add`.
- Never modify an existing test assertion unless the task's **Expected changes to existing tests**
  lists it. Never skip or weaken a test.
- Never change a frozen behaviour: UX-22 (link resolution), UX-24 (YAML-style value display),
  UX-34 (sticky band `#` markers).
- If anything in the task does not match the code, STOP and explain. Do not improvise a different
  design.

## Report format

```markdown
# {TASK} implementation — round {ROUND}

STATUS: DONE | STOP

## Summary
<3–6 lines: what changed and why>

## Files changed
- <path> — <what>

## Tests written first (failing before the fix)
- <test name> — failure excerpt: `<one or two lines>`

## Tests added or changed
- <test name> — <what it proves>

## Existing assertions changed
- <file>:<test name> — old: `<…>` → new: `<…>` — required by: <intended behaviour change>

## Verification
- `<command>` → PASS/FAIL (log path)

## Evidence for reviewers
- Screenshots / notes: <paths>

## Feedback addressed (rounds 2–3)
- Finding n: <how it was fixed>

## Open points / STOP reason
<anything the reviewer must know>
```
