# Offer only options the user can take where they are

## The user's words (2026-11-10, batch-09)

- "Attention tu me recommande de passer en mode foreman alors que je suis en remote"
- "Il faut que tu encodes quelques part une check-list de ce que tu peux proposer comme option en
  fonction de l'environnent, agent de codage,… et surtout le pourquoi"

## What happened

In one afternoon, the Chief of Staff offered the user, on Remote Control, three options they
could not take from their phone:

1. **Switching to Foreman mode,** offered as a second choice when planning-repo was refused. A
   Foreman is a separate session the user cannot steer from Remote Control.
2. **"Run `claude plugin test .` in a terminal that has `claude`",** offered twice for PR 95. The
   user has no terminal on the phone.
3. **Running the board server with `--host 0.0.0.0` themself.** That needs the machine.

## The request

A checklist, in the cards, of the options the Chief of Staff (and the Foreman) may offer,
depending on:

- the surface: Remote Control on a phone, the desktop app, a terminal CLI;
- the coding agent's host: Claude Code, a Copilot SDK host;
- the session: the main checkout, a worktree session, an eval;
- the steering mode: direct or Foreman.

Each entry gives the reason, so that an agent can judge a case the list does not name.

## A first draft (to grill)

| Option | Not offered when | Why |
| --- | --- | --- |
| Switch to Foreman mode | the user is on Remote Control | the Foreman is a separate session they cannot see or steer from there |
| "Run this command in a terminal" | the user is on Remote Control | they have no shell; the Chief of Staff runs it, or says it cannot and why |
| Open a local URL or file (`localhost`, a path) | the user is on Remote Control | the machine is not reachable; send the file (SendUserFile) or a forge link |
| A terminal-dialog slash command (`/permissions`, `/config`) | the desktop app or Remote Control | they open a terminal panel that is not there; use the app's own UI |
| Restart the app, `/reload-plugins`, open in an editor | the user is on Remote Control | it needs the machine |
| Review PNG renders, merge a PR | never refused | the forge works on a phone |
| A host feature (scheduled wake, start a session, a Monitor) | the host lacks it | No fallback: say it is missing; do not offer a look-alike |
| Work in the main checkout | an eval runs, or the session is a worktree session | AGENTS.md: the main checkout does not change during an eval; fail fast |

The general rule: before offering an option, check that the user can take it from where they are
now. When no option fits, say so; do not offer one they cannot take.

## Also seen (not this item)

`order add` on a paused direct batch resumes it, so a second CR is refused until the next pause:
only one CR can join per pause.
