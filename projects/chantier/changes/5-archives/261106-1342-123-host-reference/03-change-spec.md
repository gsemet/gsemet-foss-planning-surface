# Each host has its reference, and the user gets exact instructions for what only they can do

## Problem

What chantier knows of a host is scattered in the cards, and what it knows of remote sessions is
one sentence: "the user can start it and paste this prompt". In batch-06 the user picked the
`chantier` entry under "Remote Control": it names the main checkout, shows no worktree option, and
the session landed in a worktree. There the Write tool refuses the main checkout, where
`.agents/changes/` lives, so Drivers were blocked after money was spent.

## Change

### One reference per host

- `skills/chantier/references/hosts/claude-code.md` and `.../hosts/copilot.md`.
- What is proper to a host moves there from the cards: session tools and their arguments, the
  heartbeat, the tool table of `foreman.md`, the reuse of a Foreman. A card keeps what the role
  judges and names the host's reference. Copilot's lines move as they are.
- Each behaviour is marked **proved** (where and when), **documented** (with its link) or
  **unproved** (with the trial that settles it). Nothing unproved is told to the user as a fact.
- The Chief of Staff, the Foreman and the Driver read their host's reference with their card.

### Classes of session, in `claude-code.md`

| Class | How it is known | Can start a session | Fit for a Foreman |
| --- | --- | --- | --- |
| Desktop, typed at the keyboard | no Remote Control notice | yes | yes, it starts it alone |
| Desktop, driven by Remote Control | the host's Remote Control notice | no: refused, the message must be typed in the desktop app | it reuses the last Foreman, or the user acts |
| Session on the main checkout | `git rev-parse --git-dir` equals `--git-common-dir` | n/a | yes |
| Session in a worktree | they differ | n/a | no: Write refuses the main checkout, `change_directory` is refused, `request_directory` does not help (proved, batch-06) |
| Cloud | the host's environment | n/a | no: no main checkout |

### At the desktop, nothing for the user

`start_session` as today. The user only gives the go.

### A "For you" block

Whenever a step is the user's, the Chief of Staff gives one fixed block, in the user's language:

1. **Where:** the device and the app.
2. **Do:** each choice by its label on screen, in order.
3. **Paste:** the text in its own code block, complete: no placeholder left.
4. **You should see:** what comes next and within how long; otherwise, say what you see.

`claude-code.md` holds the block for each case: a new Foreman from a remote client, a reused
Foreman, a closed session, `/compact`. Before giving it, the Chief of Staff says what a choice
costs when it has one (a reused Foreman carries its context; a worktree session blocks writes).

### A Foreman in a worktree asks

The Foreman's first act, before it claims its epoch, is the worktree check. In a worktree it takes
no CR and sends `ask`; the Chief of Staff tells the user the impact (Write refused in
`.agents/changes/`, so no Driver can leave its work and evidence there) and gives the "For you"
block to start again on the main checkout. The reference names no way around the refusal. A user
may allow one for a batch: that word stays in that batch, is sent with the user's own words, and
never becomes a rule.

## To prove before the remote block is written

Documented, not proved here: desktop docs say Worktree is off by default and is set per
environment; `claude remote-control --spawn same-dir` keeps the folder and `--spawn worktree`
isolates. Not documented: creating a session from a phone on a Desktop host, and its options.

One trial settles it, on the user's word: from the remote client, pick the "Remote Control" entry
and, in a second try, the "Local" group's or a saved environment with Worktree off; in each,
run `git rev-parse --git-dir --git-common-dir`. The block records the path that lands on the main
checkout. If none does, the block says a new Foreman needs the desktop, and offers the reuse.

## Out of scope

No new CLI command: the worktree check is a git command the Foreman runs. No new Copilot finding.

## Done when

- Both references exist; `tests/test_structure.py` checks they do; no host tool name is left in a
  card outside its pointer; Copilot's text is unchanged in substance.
- `just scenario` passes, with a Foreman started in a worktree stopping before it claims its epoch.
- Each "For you" block of `claude-code.md` was followed once by hand, or is marked unproved.
