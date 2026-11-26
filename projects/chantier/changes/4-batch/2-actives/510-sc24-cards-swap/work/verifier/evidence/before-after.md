# CR-510: before and after

- Before: base `ea11a9e05c3e682bf83ee2bb4e546de9b9db2dba` (origin/main), a detached worktree (`<base>`).
- After: pushed head `b85be4cbeac5dac2208e26aeb440a9f6676e6ce3`, the CR's worktree (`<head>`).
- Captured 2026-11-26. Text captures only (no UI change in this CR). Local paths are made up:
  `<tree>` is the code tree under test, `<project>` the throwaway project.

## How to reproduce

For each case: a new `git init` project with one `AGENTS.md`, host `claude`
(`CHANTIER_HOST=claude`, no session or `CHANTIER_*` variable inherited), no `chantier.yaml` unless
stated. Prepare a batch of that mode (`file`, `open`, `foreman set`), then run the commands shown,
with the tree under test's own CLI (`uv run --locked --project <base> chantier` for the before,
`uv run --no-sync --project <head> chantier` for the after), the project as the working folder.

## 1. A CR Driver's start (`take CR-101 --note why --epoch 1`)

Shows: the prompt skeleton and the workers' opening lines give way to one `brief` command.

Before (excerpt; six `<role> prompt, opening lines` blocks, a `worker writes line` block, then):

```text
cards: <tree>/skills/chantier/references/ (driver.md, concepts.md; ...)
coder prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
  chantier coder for CR-101 "One" of batch batch-01, in the project <project>.
  Read <tree>/skills/chantier/references/coder.md;
  the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
...
cr-driver prompt (copy it whole, without the two leading spaces, and fill each <…>; add no line and drop none):
  chantier cr-driver for CR-101 "One" of batch batch-01, in the project <project>.
  Read <tree>/skills/chantier/references/startup-core.md, the host core, role core, and the short startup section named by <tree>/skills/chantier/references/startup-manifest.json; defer the rest until an action names it.
  Card: <tree>/skills/chantier/references/driver.md: its Startup core now, each other section when its step comes, as the card's opening says;
  ...
  Team: <the team: lines, as printed, then the review steps>
  Note: why
```

After:

```text
brief: `brief <role> <cr>` gives each role its card, the floor and its facts; the project's rules rank above them: `rules`
...
workers: $CHANTIER brief <role> CR-101 --batch batch-01 (roles: coder, conflict-resolver, debugger, inspector, investigator, verifier)
lease: 1 (pass --lease 1 on your commands; renew at each wake: lease CR-101 renew --lease 1)
brief: uvx --from "<tree>" chantier --skill "<tree>/skills/chantier" brief cr-driver CR-101 --lease 1 --batch batch-01
next: run it and pass its output, unchanged, as the Driver's whole prompt
```

Brief files in the git folder after `take`, before any `brief`: none. Running the printed command
at head prints:

```text
chantier cr-driver for CR-101 "One" of batch batch-01, in the project <project>.
writes: <project>/.agents/changes/4-batch/2-actives/101-one
worktree: <project>.worktrees\batch-01-CR-101 branch chantier/batch-01/cr-101-one base origin/main
Read <project>/.git/chantier/briefs/proj/batch-01/CR-101-cr-driver.md whole, first.
```

## 2. `handoff CR-101 --lease 1`

Before: the same six `<role> prompt, opening lines` blocks and the `worker writes line` block.

After: one line, `workers: $CHANTIER brief <role> CR-101 --batch batch-01 (roles: ...)`.

## 3. The stack Driver (`take stack --note why --epoch 1`, a stack batch of two CRs)

Before: `stack-driver prompt (no writes: line: ...)` followed by the skeleton, with
`Team: <the team: lines, as printed, then the review steps>` and `Note: why`.

After:

```text
lease: stack 1 (pass --lease 1 on stack <crs>, ...)
brief: uvx --from "<tree>" chantier --skill "<tree>/skills/chantier" brief stack-driver stack --lease 1 --batch batch-01
next: run it and pass its output, unchanged, as the Driver's whole prompt
```

No brief file before `brief`; its brief (9,573 bytes on this fixture) holds
`Team: the plugin's agents` and `Note: why`.

## 4. The QA Driver (`order qa --note "test it"`)

Before: `qa-driver prompt (no writes: line: ...)` followed by the skeleton, with `Note: test it`.

After:

```text
lease: 1 of O-1 (renew at each wake: lease O-1 renew --lease 1; ...)
brief: uvx --from "<tree>" chantier --skill "<tree>/skills/chantier" brief qa-driver O-1 --lease 1 --batch batch-01
next: run it and pass its output, unchanged, as the Driver's whole prompt
```

No brief file before `brief`; its brief (6,144 bytes on this fixture) holds `Note: test it`.

## 5. `Team:` and review steps (after only)

Project with a `## chantier` section in `AGENTS.md` holding `security-review` and `foreman`
entries. The CR Driver's brief at head holds:

```text
Team: the plugin's agents; review step security-review: look for secrets in the diff.; review step foreman: a foreman entry.
Note: why
```

Before: the skeleton printed `Team: <the team: lines, as printed, then the review steps>` for the
starting session to fill, so there is no filled line to capture at the base. The `foreman:` entry
printing as a review step is in the PR's Known gaps.

## 6. Matrix cell 2: a generic agent configured for the Coder on Claude Code

`chantier.yaml`: `hosts: claude: roles: coder: agent: general-purpose`. The record holds
`"coder": {"agent": "general-purpose", "start": "named"}` at both SHAs.

- Before: no line of `take` holds `contract`.
- After: `brief coder CR-101` writes a 5,055-byte brief starting `# Coder`, with one `=== floor`
  and 0 lines holding `contract (a generic agent`.

The contract lines are absent at both SHAs.

## 7. The hook's reload message (`hooks/register.tsx`)

Before: `You are ... a chantier session; after this compaction, call your chantier skill again with the argument reload.`

After: ``You are ... a chantier session; after this compaction, run your brief again (`brief <role>` through your skill's `$CHANTIER` command; the Foreman with `--epoch <n>`) and read the file it names whole; the floor, in that brief, holds.``

(Source: `git diff ea11a9e HEAD -- hooks/register.tsx`.) `just mod`: base 118 pass, 0 fail; head
119 pass, 0 fail; the same 14 TypeScript warning messages at both.

## 8. Old start reading and new brief, bytes

Old column: `e7_bytes.py` (the quiz's old-card boot) on `git archive` of the base. New column:
`pytest -q -s skills/chantier/scripts/cli/tests/test_brief_bytes.py` at head.

| Role | Base | Head |
| --- | --- | --- |
| cr-driver | 27,834 | 9,773 |
| release-driver | 26,404 | 9,531 |
| stack-driver | 34,714 | 9,179 |
| qa-driver | 24,776 | 6,032 |
| coder | 14,226 | 3,939 |
| verifier | 24,229 | 5,448 |
| chief-of-staff | 202,936 | 24,351 |
| foreman | 91,612 | 22,125 |
| griller | 22,294 | 6,441 |

## Not captured

- A transcript of a real Claude Code session after `/compact`: the Verifier runs no interactive
  session. The PR's Known gaps names it.
- A real batch run, a Copilot session, any quiz or evaluation: not run (owner's decision for the
  evaluations); named in the PR's Known gaps.
