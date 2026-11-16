# Change Specification: the Foreman finds a conflict between ready PRs at the second one

## Goal

In a parallel batch, two ready PRs that conflict with each other are found when the second one
is handed back ready, not hours later at a trial merge. Batch-18 found ten such PRs at once (on
`driver.md`, `commands/driver.py`, `scenario/run_scenario.py`, `concepts.md`), and rebuilding them
into a stack cost about 2.5 h, 11 conflict-resolvers, about 9 extra long gates and 14 extra
Driver takes. With this change the Foreman checks each new ready branch against the other ready
PRs of the batch with plain git. On a conflict it sends the Chief of Staff one ask to switch the
batch to a stack (`order mode --note stack`, CR-267), so the later CR is rebased once onto the
earlier one. The user decides; nothing switches by itself.

The change goes in the cards and the scenario only: no CLI command, no CLI code, no hook, no
type. It works the same on both hosts (Claude Code, GitHub Copilot) and both forges (GitHub,
GitLab).

## Decisions carried from `02-answers.md`

1. Source: batch-18's retro, kept by the retro critic and a Fable review; the fix is the user's
   choice. The CR joins batch-18, switched to a stack.
2. Generality: the same on both hosts and both forges. A path not proved on Copilot or on a real
   GitLab carries the mark "unproved" in its card line.
3. Place in the stack: fourth, after `ship-reads-forge`. This is a batch order and needs no
   dependency file. The Driver rebases on what is below it as the stack driver says.
4. On a conflict the Foreman asks the Chief of Staff (one ask). The Chief of Staff decides the
   switch to a stack with the user. Nothing switches automatically.

## What changes

### 1. `skills/chantier/references/foreman.md`

**a. The Foreman's git (the bullet "Never code, review, commit, rebase, push or edit a PR...",
in "The user's boundaries").** Add a third git duty after the cleanup and the fast-forward:
the early conflict check (in "Your means", below), by `git merge-tree` only. It is read-only for
the checkouts: it moves no ref, touches no working tree and no index, and writes only unreferenced
objects to the object store. The sentence "and by no other command" at the end of that bullet
still holds for the main checkout's moves. Reword it so the reader cannot take it to forbid
`merge-tree`.

**b. A new bullet in "Your means": "An early conflict check (parallel batch)".** Put it next to
the chain bullet ("You may chain a queued CR on another..."). It says:

- **When:** the batch's mode, read from `status`, is `parallel`. A CR's Driver hands it back
  `ready` with a PR (`hand-back ready to merge <link>` or `hand-back PR in draft <link>`), and at
  least one other CR of the batch is `ready` with an unmerged PR on the default branch. Run it
  once per such hand-back, after you send that CR's own ask (`ready-to-merge` / `pr-in-draft`),
  which goes up unchanged. A hand-back after a `take <cr> --note` (a rebase, a fix) is a new
  hand-back and is checked again. The check does not run in a `series` or `stack` batch: there
  the PRs are already placed on one another, and a conflict there is the stack driver's
  `anomaly <cr> conflict: …`.
- **Which pairs:** the new CR against each other CR that is `ready`, has a PR whose base is the
  default branch, and is not merged or cancelled. Skip a pair when one CR's base is the other's
  branch (a chain or a dependency: `after`, `depends.json`). Skip a pair already noted (below).
- **The command,** one per pair, from the main checkout (with a planning surface, `git -C
  <clone>`, the clone `take` names), with each CR's branch as `handoff <cr>` prints it:
  `git merge-tree --write-tree --name-only --no-messages <new cr's branch> <other cr's branch>`.
  Exit 0: no conflict, nothing to do. Exit 1: a conflict. The lines after the first (the tree
  id) are the conflicting paths. Any other exit (a missing ref, a git older than 2.38 that does
  not know `--write-tree`): no ask about a conflict. Record `$CHANTIER note <new cr> "early
  conflict check: not run against <other cr>: <git's text, first line>"` and go on. Never fall
  back to another command: no trial merge in a checkout, no `git merge`, no `git rebase`, no
  worktree. A command the host refuses takes the usual route (the `refused <cr> <text>` ask and its
  note, as "Your means" already says).
- **On conflicts:** for each conflicting pair, record `$CHANTIER note <new cr> "early conflict:
  with <other cr>: <paths>"` (up to five paths, then `and <k> more`). This note is the pair's
  source for any later brief, and it marks the pair as noted. Then send **one** ask for this
  hand-back covering every new pair: `$CHANTIER asks "conflict <new cr> with <other cr>[, <other
  cr>…]: <paths>; switch to a stack?"`. Name each CR by number and slug together (concepts, "A
  CR's name"). The ask holds no other proposal. A pair already noted on either CR gives neither a
  note nor an ask again.
- **What it does not do:** it stops no Driver, sends no `take`, no rebase note and no message to
  a Driver, changes no order, and never switches the mode itself. Each PR stays as its hand-back
  left it: a `ready-to-merge` PR stays mergeable on its own. The switch comes only as the Chief
  of Staff's `order mode --note stack`, and the bullet "A mode switch" already covers it, *to a
  stack*. The stack driver orders the CRs from the record (the CRs handed back `ready` at the
  bottom, in the order they became ready: concepts, "Batch modes"), so the later CR is the one
  rebased onto the earlier. Its Driver does that rebase once, on the `anomaly <cr> conflict:
  stacked on <cr>: <files>` route and its `take <cr> --note "rebase: stacked on <cr below>:
  conflict in <files>"`.
- **Marks:** the check itself is plain git and the same on both hosts and forges. Its run by a
  Copilot Foreman is **unproved**. On GitLab the stack it may lead to is the chain of MRs
  merged one at a time from the bottom, as the card already says: **unproved** on a real GitLab
  (trial: one run on a GitLab project).

**c. The asks list (the bullet "`$CHANTIER asks "<text>"` records what the Chief of Staff must
hear...").** Add the plain-words line `conflict <cr> with <cr>[, <cr>…]: <paths>; switch to a
stack?`.

### 2. `skills/chantier/references/chief-of-staff.md`

Add a bullet next to "A chain:" (line 955), headed **An early conflict:**. On the ask `conflict
<cr> with <cr>…: <paths>; switch to a stack?`, tell the user, in their language:

- the PRs, by link and CR name;
- the paths they both change;
- that each PR stays ready to merge on its own, but merging one makes the others conflict, and
  those go back to their Drivers for a rebase after that merge (the parallel rule);
- the offer: switch the batch to a stack, so the later CR is rebased once onto the earlier one.

On the user's yes, run `order mode --note stack` and tell the user what the switch does, as the
bullet "A series batch" already says for `order mode` (the PRs above the bottom go to draft,
"do not merge them meanwhile", named). On a no, record nothing and send the Foreman nothing; the
batch stays parallel. In direct mode the steering session runs the check itself (it reads
foreman.md) and puts the same question to the user. The ask is still recorded with `$CHANTIER
asks`, as `routing.md` already says. The ask counts like any other ask in the report.

### 3. `scenario/run_scenario.py`

The scripted Foreman (`class Foreman`, line 365) does what the card now says, and the scenario
proves it.

- **`Foreman.early_conflicts(d, c)`** (new method), called from `Foreman.turn()` right after the
  `ready-to-merge` / `pr-in-draft` ask of a ready CR (line 577), only when `d["mode"] ==
  "parallel"`. It picks the pairs as the card says, runs `self.git("merge-tree", "--write-tree",
  "--name-only", "--no-messages", <c branch>, <other branch>)` through the recorded `git()`
  helper, writes the `early conflict: with …` note with `w.chantier("note", …)`, sends the one
  `conflict … ; switch to a stack?` ask with `self.ask`, and leaves out a pair already noted.
- **The check at line 1085** ("the Foreman's git in the main checkout is only…"): allow
  `("merge-tree", "--write-tree", …)` too, and say so in its text. It still refuses any other
  verb.
- **Section 4 (CR-102, line 889):** after `fm.turn()`, check that the merge-tree ran for CR-102
  against CR-101 (`login.py` against `export.py`), that no `conflict` ask was sent, and that no
  `early conflict:` note exists: no conflict means no ask.
- **A new section, "Early conflict between two ready PRs",** in the scenario's own world (`w.reset()`,
  `prepare_cr`, `w.start(..., *FROM_AGENTS_MD)` in parallel, as the mode switch section at line
  4811 does). Two CRs edit the same line of one file (for example `shared.py`, `N = 1` against
  `N = 2`), each pushed with its PR and handed back `ready`, and `Foreman.turn()` runs after each.
  Checks:
  1. after the first hand-back: no merge-tree, no `conflict` ask (no other ready PR);
  2. after the second: the asks are `ready-to-merge <second> <pr>` then `conflict <second> with
     <first>: shared.py; switch to a stack?`, and the second CR carries the note `early
     conflict: with <first>: shared.py`;
  3. a further `turn()` with nothing new sends no second `conflict` ask (the pair is noted);
  4. the Chief of Staff's `order mode --note stack` then gives a stack batch, and `take stack`
     orders the first CR at the bottom and the second above it (the earlier ready CR below);
  5. the same two CRs in a batch opened `--mode stack`: no merge-tree runs (`fm.git_main` holds
     none), and no `conflict` ask is sent.
- `scenario/README.md`: one line for the new section in its list of what the scenario covers.

### 4. `docs/use-cases-foreman.md`

One row in the table near line 86, before "Switch to a stack.": what the user sees when two ready
PRs of a parallel batch conflict (the Chief of Staff names them and the files and offers the
switch to a stack; the user's yes is "Switch to a stack.").

## Out of scope

- No CLI command, flag or code change (`commands/*.py`, `rails.py`): plain git in the card, per
  the request ("no CLI tool").
- No automatic mode switch, no chain proposal (`chain <cr> after <cr>`) and no other remedy in the
  ask.
- No check against queued or working CRs, nor against the default branch's own moves (a PR that
  stopped merging with the default branch is already the bullet "A PR ready to merge that stopped
  merging…").
- No check in a `series` or `stack` batch.
- No new allow rule in `skills/chantier/references/hosts/claude-code.md`'s capability table and no P10 sample (see the
  open questions).
- No change to the agent files (`agents/`, `com.github.copilot/agents/`), the hooks, the types or
  the docs' SVGs.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes, with the checks of section 3: no ask without a conflict (section 4),
  one ask and one note for a conflicting pair, no second ask for the same pair, the switch putting
  the earlier ready CR at the bottom, no check in a stack batch, and the Foreman's git limited to
  the listed verbs plus `merge-tree --write-tree`.
- The eval kit's audit stays green with no change: `evals/kit/audit.py`'s `GIT_WRITES`
  (`merge\b(?!-)`) does not match `merge-tree`, so the fast-forward route (J26) is not broken.
  The Driver confirms it by running the audit's tests if they exist, or by reading the regex,
  and says which in the PR.
- No `just mod`: nothing under `hooks/` or `types/` changes.
- Git version: `--write-tree` and `--name-only` need git 2.38 or later. The user's machine runs
  2.56. On an older git the card's "any other exit" line applies, with no fallback.

## Open questions

1. After the user says no to the switch, should a later conflicting pair in the same batch still
   bring a new ask? As specified it does: only a pair already noted is silenced, and the Foreman
   never hears the no.
2. `git merge-tree` is not in Claude Code's capability table. Its run by the Foreman is left to the
   host's classifier, like `git fetch` and `git symbolic-ref` today, and a refusal is a `refused`
   ask. Should P10 name a rule for it (`git merge-tree --write-tree*`) instead? That would be a CLI
   and test change, kept out here.
