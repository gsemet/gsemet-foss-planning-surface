---
type: cr-change-spec
description: Change Specification of driver-force-push-own-branch.
---

# A Driver force-pushes only its own branch; batch-23's refusal with the rule set recorded

## Goal

In batch-23 the host refused a Driver's lease-protected force push of its own `chantier/`
branch (CR-318). The refusal went Driver → Foreman → Chief of Staff → the user. The user's
retro point: let that push through on the `chantier/` branches a Driver owns.

The allow rule was already set, and no allowed form of the command avoids the classifier
(push-Q11). So this CR:

- records the proof in the host's reference;
- keeps the Driver's `git -C` push, which a Driver uses on its own CR's branch only;
- keeps today's route for a refusal, with no question to the user when the push is legitimate.

## The decisions (`02-answers.md`)

| # | Decision | Where it lands |
| --- | --- | --- |
| D1 (push-Q6) | Preflight's P10 names an allow rule for `git push --force-with-lease` on `chantier/` branches. The Chief of Staff adds it to `~/.claude/settings.json` only on the user's yes, like P10's other rules | Area 1 (already in place: kept) |
| D2 (push-Q6) | A Driver force-pushes only its own CR's branch | Area 3 |
| D3 (batch-Q8) | This CR goes into the next batch, with the six retro points of batch-23 (this one among them) and the four board CRs of 2026-11-17 | planning only; nothing in the code |
| D4 (push-Q10, kept by push-Q11) | The CR records in the host's reference that the rule was set and the classifier refused the push anyway | Area 2 |
| D5 (push-Q11, replaces push-Q10's trial) | The Driver keeps the `git -C` push. No in-worktree push and no trial of it: that would be a chain (`cd`/`Set-Location`; `git push`), which `concepts.md` rule 8 and `hosts/claude-code.md` ("Auto mode", batch-15) forbid, and which matches no allow rule | Area 3 (Push unchanged) |
| D6 (push-Q10, kept by push-Q11) | A refused force push keeps today's route (Driver, Foreman, Chief of Staff), with no question to the user when it is legitimate | Area 3 (route unchanged), Area 4 |
| D7 (push-Q10, the Chief of Staff) | The stack driver's restack of the stack's branches stays as it is | Area 3 |

## What the code already holds, and what batch-23 proved

Read before writing this specification (code read-only, at `33a2305`):

- **P10 already names the rules of D1.**
  - `SAMPLES` in `skills/chantier/scripts/cli/src/chantier/commands/permissions.py` holds three
    force-push commands and their rules under the capability `batch`: `git push --force-with-lease
    -u origin chantier/*`, `git -C * push --force-with-lease -u origin chantier/*` and `git push
    --force-with-lease=chantier/* origin *chantier/*`. Each comes as `Bash(…)` and `PowerShell(…)`.
  - They are also in `RECOMMENDED_ALLOW`, in the table "Allow rules" of
    `skills/chantier/references/hosts/claude-code.md` (rows 3 to 5, lines 247-249), in its
    pasteable block, and in the row "Every batch" of its table "Capabilities and their commands".
  - `tests/test_cli_runs.py` (around lines 255-275) checks that the block and the table match
    `SAMPLES`.
- **The rules were set.** The user's `~/.claude/settings.json` held them during batch-23, in both
  forms.
- **CR-318's refusal is on record.** Its Driver recorded it as `driver.md` asks (the CR's archived
  `STATUS.json`, note):

  ```text
  refused: git -C C:\Users\gaeta\Projets\chantier.worktrees\batch-23-CR-318 push
  --force-with-lease -u origin chantier/batch-23/cr-318-cr -> Permission for this action was
  denied by the Claude Code auto mode classifier. Reason: [Destructive or Unwanted Actions].
  ```

- **The rule matched, and the classifier refused anyway.** That exact command matches the rule
  `git -C * push --force-with-lease -u origin chantier/*` as P10 matches it. Checked with
  `permissions.rule_matches`: `True` for both the `PowerShell(…)` and the `Bash(…)` form. P10
  said "allowed", the rule was set, and the host's auto-mode classifier refused the command
  anyway, in a subagent.
- **This contradicts the host reference.** `hosts/claude-code.md`, "Auto mode", says an allow rule
  "resolves a matching command at once, before the classifier (documented)" (line 387, and again
  at lines 406 and 410). For a Driver, batch-23 showed otherwise. The label "Destructive or Unwanted
  Actions" is not among the labels that section lists.

## What changes

### Area 1: P10 and its rules (D1): kept, no code change

- `permissions.py`: `SAMPLES`, `RECOMMENDED_ALLOW` and P10's lines stay as they are. The three
  force-push rules remain in the capability "every batch". No rule is added or widened.
- `chief-of-staff.md`, "The question" and "On the yes": the rules are still added only on the
  user's yes, merged, never replaced (AGENTS.md's single write in `~/.claude/settings.json`).
- No change to `preflight.py`, `declare/preflight.py` or the tests' expectations.

### Area 2: the host reference (`skills/chantier/references/hosts/claude-code.md`) (D4)

1. Table "Allow rules", row `git -C * push --force-with-lease -u origin chantier/*` (line 248):
   - "chantier's use" keeps its history ("the same from outside the worktree, the form refused 4
     times as "Git Destructive"").
   - "Risk accepted" gets: "a Driver pushes only its own CR's branch (`driver.md`, Push); the
     rule's `*` does not enforce that, the card does". Add the same sentence to row 247.
   - "Mark" keeps "documented (rule form)" and gets: "; **refused with the rule set**: batch-23,
     CR-318, a Driver in auto mode, `Permission for this action was denied by the Claude Code auto
     mode classifier. Reason: [Destructive or Unwanted Actions].`".
2. Table "Capabilities and their commands", row "Every batch", column "Mark" gets: "a Driver's
   `git -C` force push was refused with its rule set (batch-23, CR-318); a refusal goes the route
   of `driver.md`".
3. Section "Auto mode":
   - First bullet (line 387): after "Allow, ask and deny matches resolve at once in auto mode,
     without the classifier", add: "Seen otherwise for a subagent. In batch-23 (CR-318), the
     classifier refused a Driver's `git -C <worktree> push --force-with-lease -u origin
     chantier/...` that the user's allow rule matched (P10 said allowed). Whether the classifier
     judges a subagent's command despite a matching allow rule is **unproved**, not documented. A
     refusal goes the route of `driver.md`."
   - Second bullet (lines 390-393): add "Destructive or Unwanted Actions" (batch-23) to the labels
     seen and not documented ("Merge Without Review", "Create Public Surface").
   - Batch-15 bullet (lines 403-407): "An allow rule resolves a matching command before the
     classifier" becomes "An allow rule resolves a matching command before the classifier (except
     batch-23, CR-318, above)". The rest of the bullet stays: a loop, a script or a chain matches
     no prefix rule; one command per branch.
   - Bullet "What a trial before the go can and cannot prove", sub-bullet "an allow rule resolves
     a matching command at once…" (line 410): add "for the steering session; for a Driver, see
     batch-23 above".
   - The alert the Chief of Staff gives at its first turn (lines 420-423): after "Without the
     rules below, an unattended batch waits for you at the first one", add "; with them, a
     Driver's force push may still be refused (batch-23). It then goes to the Chief of Staff, who
     runs a legitimate one without asking you".

### Area 3: the Driver's push (`skills/chantier/references/driver.md`) (D2, D5, D6, D7)

- Bullet "Push" (lines 268-270): the commands stay as they are. The plain push stays `git -C
  <worktree> push -u <remote> <branch>`, and the rewrite (a rebase) stays `git -C <worktree> push
  --force-with-lease -u <remote> <branch>` (D5). Add after them: "`<branch>` is your own CR's
  branch, the one your `take` / `handoff` prints, never another CR's (the stack driver restacks
  the stack's branches by its own rule, below)" (D2, D7).
- Bullet "A force push the host refuses" (around line 510): unchanged (D6). The route
  (record the exact refusal, the `next after push` note, `handback … blocked waits: push …`, the
  push line) stays the way out of a refusal, with or without a matching allow rule. Step 1's "It
  is what proves afterwards a missing allow rule or the classifier on a matching rule" stays:
  batch-23 is the second case.
- The stack driver's lines (restack, "Who moves a branch", around lines 655-901): unchanged (D7).

### Area 4: the Chief of Staff (`skills/chantier/references/chief-of-staff.md`) (D6)

- "A refused force push" (around line 1129), step 3: after "The user hears nothing at the time",
  add: "even when the Driver's push was refused with the allow rules set (batch-23): a legitimate
  push is never a question for the user". Steps 1, 2, 4 and 5 are unchanged.
- "On the yes" (around line 104): after "Then run `$CHANTIER preflight` again and say what P10
  says now", add: "Say also that a Driver's force push was refused once with these rules set
  (batch-23); a refused one comes to you, and you run it when it is legitimate."
- Nothing else changes there.

### Hosts and agent files

- Copilot: `hosts/copilot.md` is unchanged. P10 does not run there, and its force-push sentence
  (line 75) stays. The own-branch sentence in `driver.md` holds on both hosts (one card).
- `agents/` and `com.github.copilot/agents/` are unchanged: the contract lives in the cards.

## Out of scope

- An in-worktree push or a trial of it (push-Q11: a chain, forbidden by `concepts.md` rule 8 and
  `hosts/claude-code.md`, and matching no allow rule).
- A new or wider allow rule, a hook (`hooks/`) or any other way to make the host accept the push
  ("no workaround", AGENTS.md).
- The stack driver's restack (D7).
- The force-push route's steps and the Chief of Staff's judgement, beyond the sentences of Area 4.
- Why CR-318's push reached the user (dropped by the user).
- The CLI: no new check and no new P10 line.
- Copilot's permissions.

## Evidence

- `just check` passes on Linux, macOS and Windows. Only the cards change, so the existing
  `test_cli_runs.py` comparisons of the pasteable block and the tables with `SAMPLES` must still
  pass: no rule is renamed, added or reordered.
- `just scenario (ubuntu-latest)` green at the PR's head (a change to the cards).
- `git diff main -- skills/chantier/scripts/` is empty.
- `git grep -n "Destructive or Unwanted Actions" -- skills/chantier/references/hosts/claude-code.md`
  shows the first Auto mode bullet, the labels bullet and the Mark of row 248, each with
  "batch-23". Row 248 still holds "refused 4 times".
- `git grep -n "except batch-23, CR-318" -- skills/chantier/references/hosts/claude-code.md` shows
  the batch-15 bullet.
- `git grep -n "own CR's branch" -- skills/chantier/references/driver.md skills/chantier/references/hosts/claude-code.md`
  shows the Push bullet and the "Risk accepted" cells of rows 247 and 248.
- `git diff main -- skills/chantier/references/driver.md` changes no push command (the `git -C`
  forms stay).
- The PR body quotes CR-318's refusal note verbatim. It also shows the matcher check: a one-line
  `uv run --no-sync python -c "from chantier.commands.permissions import rule_matches …"` printing
  `True True` for the refused command against both forms of `git -C * push --force-with-lease -u
  origin chantier/*`.

## Open questions

None.
