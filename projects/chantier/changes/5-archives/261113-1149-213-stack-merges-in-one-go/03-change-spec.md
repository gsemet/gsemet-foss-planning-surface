# Change Specification: a stack is merged in one go; inserting into a ready stack; agents started right the first time

The CR has no tracker issue.

## Goal

In the user's words: "Le mode 'pile mergeable d'un coup' c'est le mode 'stack'." "Je veux une
stack prête à merger d'un coup." The instructions belong in chantier's cards, docs and CLI, not in
a session's memory.

1. **A stack is a native forge stack, merged in one action.** On GitHub a stack is a native
   stacked-PR stack (generally available 2026-10-06): the PRs grouped bottom to top and merged in
   one action from the top PR. A chain of PRs based on each other is not a stack. "Stack ready"
   means: the stack exists on the forge, it is open, it holds every PR of the stack in order,
   none is a draft, the release PR (when the batch has one) is on top, so the release commit
   lands last on `main`. The Foreman and the Chief of Staff check this on the forge before they
   call the stack ready.
2. **Inserting a change into a ready stack** is a use case the cards, the docs and the SVGs
   encode: before anything else every PR that will sit above the new one goes back to draft;
   then insert, restack, update the stack on the forge (re-create it if the forge cannot insert),
   verify, and only then turn the PRs above ready again. The release PR stays on top and its
   release notes name the new change.
3. **Every chantier agent is started right the first time** from what the parent sees at that
   moment: the agent's description shows the first line its prompt must start with, a refusal
   names that line and says a new start is needed, and the Chief of Staff's card makes it a hard
   rule and repeats it at each step that starts an agent.

Batch-15 is the measure: the stack driver left every PR above the bottom one as a draft, to be
merged bottom-up with a restack after each merge, so the user saw 15 drafts and no stack; making
the stack took a whole morning of back and forth, and stack #155 was made by hand
(`gh api -X POST repos/gsemet/chantier/stacks -F "pull_requests[]=<n>"` per PR). The
spec-writer was refused twice in one session for a prompt that did not start with
`chantier spec-writer`, the second time after a corrective message to the stopped agent.

## Where this CR sits

This CR joins batch-15 (`order add`), its PR inserted in stack #155 just below the release PR 154
(CR-212 release-v0-9-0), which the Chief of Staff put back to draft on 2026-11-13. Its branch sits
on CR-211's branch (PR 152, `chantier/batch-15/cr-211-change-specification-parallel-rebase-cos`).
The line numbers below are those of that branch. CR-212 updates its release notes to name this
change (that is CR-212's work, by the insertion rules below, not this CR's).

## Decisions carried from the grill

- D1. Stack mode means a stack the user merges in one go; "stack ready" means mergeable in one
  action from the top PR, none a draft, the release on top, verified on the forge.
- D2. When the user asks for a stack, the Chief of Staff recommends installing the `gh stack`
  extension (github/gh-stack). If the user declines, the stack is made by a new `$CHANTIER`
  command that calls the GitHub REST API (`POST /repos/{owner}/{repo}/stacks` with
  `pull_requests[]`, bottom to top). This is the user's named choice, not a silent fallback: the
  no-fallback rule of `AGENTS.md` holds.
- D3. The stack driver creates the stack on the forge once every PR is ready; the Foreman and the
  Chief of Staff verify it on the forge (`GET /repos/{owner}/{repo}/stacks/{number}`: open, every
  PR in order, none a draft, the release PR on top) before they call it ready.
- D4. The insertion use case, encoded in the stack driver's, the Foreman's and the Chief of
  Staff's cards, the docs and the SVGs, in this order: the PRs above go to draft first; insert at
  the named place; restack the PRs above on it; update the stack on the forge (re-created if the
  forge cannot insert); verify every PR again; only then the PRs above turn ready. The release PR
  stays on top and updates its release notes.
- D5. GitHub only. GitLab's equivalent is a later CR.
- D6. The preflight check for the extension is not here: it goes with `forge-permissions-at-start`
  (P1).
- D7. Each agent's `description`, on both hosts, ends with the first line its prompt must start
  with (e.g. "Prompt starts with: `chantier spec-writer for the Chief of Staff, in the project
  <root>.`").
- D8. The refusal names the expected first line and says a new start is needed (a message to the
  refused agent does not restart it).
- D9. The Chief of Staff's card puts the first-line rule among its hard rules, and each step that
  starts an agent (the spec-writer, the demo-explorer, the Foreman's Drivers) says "copy the first
  line" where it starts it.

## What changes

### 1. Words: a ready stack (`skills/chantier/references/concepts.md`)

- "Ready to merge" (l. 9-12): a PR of a stack batch is ready to merge when it belongs to a stack
  verified on the forge (D3): the user merges the whole stack in one action from its top PR.
  The rule "any other CR's PR is a draft" stays true outside a verified stack (a series, a stack
  not yet made on the forge, a stack being changed).
- Batch modes, **Stack** (l. 91-99): replace "the user merges from the bottom up" with: once every
  PR is ready, the stack driver makes one native stack on the forge (the `gh stack` extension,
  or `$CHANTIER`'s forge-stack command when the user declined it); the user merges it in one
  action from the top PR, the release commit last. A chain of PRs based on each other is not a
  stack. Say that on GitLab the stack stays as it is today (D5).
- Add the insertion use case in a few lines (D4), pointing to the stack driver's card for the
  steps.
- "Starting an agent" (l. 214-277): the refusal sentence (l. 260-261) becomes the new refusal of
  §6; name the first line of every role that starts outside the template, so each description
  can quote it: the Drivers' and workers' (`chantier <role> for <cr> "<title>" of batch <batch>,
  in the project <root>.`), the QA driver's (`chantier qa-driver for <folder> of batch <batch>,
  in the project <root>`, from foreman.md l. 107), the stack driver's (see open question 2), the
  Chief of Staff's subagents' (l. 264) and the Spec-writer's (l. 273).

### 2. The stack driver (`skills/chantier/references/driver.md`, section "Stack driver", l. 290-327)

- The goal first: the stack driver's end is one stack the user merges in one go (D1). Its
  `hand-back ready` is sent only once the stack is made on the forge and the stack driver has read
  it back as ready (the five checks of §4).
- Making the stack: when every PR of the stack is ready (the CRs ordered with `$CHANTIER stack`,
  restacked, pushed, `ship`ped, CI green at the top, as today), create the native stack with the
  means the batch names (the extension, or the `$CHANTIER` command; §5): PRs bottom to top, the
  release PR last. Then turn every PR of the stack ready (`gh pr ready`), not only the bottom one:
  this replaces "on another base, a draft" (l. 300-302) and, for the release PR, "Keep its PR a
  draft until it is the first PR on the default branch" (l. 326-327). A PR stays a draft while
  the stack is being made or changed.
- A means not available as the batch names it (the extension not installed, the command refused
  by the forge, the API missing) is an `anomaly` with the exact text: no other means without the
  user's word (no fallback).
- The hand-back carries the stack's link: `[stack→foreman] hand-back ready <stack link>
  <cr>=<link>…`.
- After a partial merge (l. 315-321): the restack also updates the stack on the forge (or
  re-creates it, as for an insertion) and reads it back before the hand-back.
- **Insertion into a ready stack** (new paragraph, D4), taken with a note that names the new CR
  and its place (`take stack --note "insert: <new cr> below <cr>"`, or the form open question 1
  settles):
  1. Every PR that will sit above the new one goes back to draft first (`gh pr ready --undo`),
     before any other step, so the user cannot merge the stack while it changes (if the Chief
     of Staff already did it, check it on the forge).
  2. Order the stack with the new CR at the place named (`$CHANTIER stack <cr>…`, bottom first;
     the release CR stays last), rebase the new PR on the one under it and each PR above on the
     one under it, push with `--force-with-lease`, `ship` each one moved; the proofs a move
     touched are judged again as today (`verifier`, `inspector`).
  3. Update the stack on the forge: insert the PR at its place where the forge allows it, else
     re-create the stack with the PRs bottom to top.
  4. The release PR: the insertion is a change of content under it, so it is stale (foreman.md
     l. 133-138 already says so): the stack driver leaves it a draft and hands back; the Foreman
     sends the release back (`take <release> --note "redo: <new cr> inserted"`) so that its
     notes name the new change, then takes the stack again.
  5. Verify every PR of the stack again on the forge (the five checks of §4) and only then turn
     the PRs above ready, the release PR last; hand back with the stack's link.

### 3. The Foreman (`skills/chantier/references/foreman.md`)

- Stack batch (l. 142-149): on the stack driver's `hand-back ready`, read the stack on the forge
  (§4) before anything else. All five checks hold: `$CHANTIER asks "stack-ready <stack link>
  <cr>=<link>…"`. One fails: no ask; send it back to a stack driver (`take stack --note "<the
  check that failed>"`).
- The insertion (D4): on the Chief of Staff's order that inserts a CR into a ready stack, the
  sequence is the one of §2 (PRs above to draft first, the new CR's Driver, the stack driver, the
  release redone, the stack driver again, the check, then `stack-ready`). Point to the stack
  driver's card for the steps; the Foreman still edits no PR.
- The asks line (l. 153-156): `stack-ready <stack link> <cr>=<link>…`.
- "To start a Driver" (l. 96-101) and the QA driver's start (l. 106-107): "copy the first line"
  (D9): the prompt starts with the role's first line as "Starting an agent" gives it, unchanged.

### 4. The check of a ready stack (shared words, in the Foreman's and the Chief of Staff's cards)

Read on the forge (`GET /repos/{owner}/{repo}/stacks/{number}`, through the means of §5):

1. the stack is open;
2. it holds every open PR of the batch's stack, and no other;
3. in the order of `take stack` (bottom first);
4. none is a draft;
5. the release PR, when the batch has one with a PR, is on top.

### 5. The new `$CHANTIER` command (`skills/chantier/scripts/cli/`)

A new tool, justified by batch-15's measured cost (a morning of the user's back and forth, the
stack made by hand with `gh api`). Behaviour only; its name and form are the Driver's
(`forge-stack create|show` is a working name, open question 3):

- **Create**: makes the native stack of the batch on GitHub from the batch's record: each stacked
  CR's recorded PR in stack order, bottom first, the release PR last. Refused (exit 2) when a CR
  of the stack has no PR recorded, and when the batch is not a stack. Prints the stack's number
  and link. The same command re-creates the stack when the forge cannot insert (the Driver reads
  what the API offers to add a PR to a stack or to dissolve one; a forge that allows neither is a
  refusal with its exact text, exit 4).
- **Show**: reads the stack on the forge and prints, one line per cause, each of the five checks
  of §4 that fails against the batch's record; exit 0 when all hold. It writes nothing.
- On a remote that is not GitHub it is refused with a line that says GitHub only (D5).
- Dependency-free and portable (POSIX and Windows, UTF-8): today the CLI never calls the forge
  (the agents run `gh`); it runs external tools by subprocess (`git` in `state.py`, `uv` in
  `costs.py`). The command uses the user's own `gh` login (preflight P9), holds no token of its
  own, and fails with `gh`'s exact error (exit 4) when the call fails.
- Its use is the user's choice when they decline the extension, recorded in the batch's brief
  (§6) and passed to the stack driver in its prompt: the stack driver never switches means on its
  own.
- `cli.py` gets its help line; `status` and the board are unchanged.

### 6. The Chief of Staff (`skills/chantier/references/chief-of-staff.md`)

- Hard rules (l. 42-60), new rule (D9): **an agent's prompt starts with its first line, copied**:
  the line `$CHANTIER playbook` prints, or the one "Starting an agent" gives for the role,
  unchanged; a refused start is fixed by a new start with that line, never by a message to the
  refused agent and never by variants.
- Starting a batch, step 2 "Show the plan" (l. 252-256) and the stack entry (l. 26): when the
  user asks for a stack (or the plan proposes one), recommend installing the `gh stack` extension
  (github/gh-stack) and say why; on a no, say that the stack will be made by `$CHANTIER`'s
  command over the REST API, and record the choice in `brief.md` (step 3) so the Foreman passes
  it to the stack driver. GitHub only; on GitLab the stack stays as today.
- New paragraph after "A series batch" (l. 403-407): **a stack batch**: on a `stack-ready` ask,
  read the stack on the forge (§4) yourself before you tell the user; then tell them the stack is
  ready to merge in one action from its top PR (the link), with the release commit last. After
  the user's merge, record `order merged` for each CR of the stack, bottom first (the release
  CR's merge starts the release procedure, as today). A check that fails: no "ready" to the
  user; send it back through the Foreman.
- **Inserting a CR into a ready stack** (new paragraph, D4): on the user's word, the PRs that
  will sit above the new one go back to draft first, at once (see open question 1 for who runs
  it), then `order add --note <folder>` and an `order note` naming the place
  (`insert: <new cr> below <cr>`); say to the user that the stack is not mergeable until the
  Foreman's next `stack-ready`, and that the release notes will name the change.
- Direct mode (l. 600-610 area, "Steering a batch yourself"): the Foreman's check of §4 is
  yours; one check is enough before you tell the user.
- The demo offer (l. 688) stays on the last `stack-ready`.
- The spec-writer's start (l. 140-145) and the demo-explorer's (l. 692): "copy the first line"
  (D9), as `$CHANTIER playbook` prints it or "Starting an agent" gives it.

### 7. Messages (`skills/chantier/references/routing.md`)

- Stack driver → Foreman: `hand-back ready <stack link> <cr>=<link>…`, `anomaly <cr> <text>`.
- Foreman → Chief of Staff: `stack-ready <stack link> <cr>=<link>…`.

### 8. The agent files (24 files, both hosts together, `agents/` and `com.github.copilot/agents/`)

- Every role's `description` (frontmatter, identical on both hosts, as `test_structure.py`
  requires) ends with "Prompt starts with: `<the role's first line>`" (D7), e.g. for the
  spec-writer "Prompt starts with: `chantier spec-writer for the Chief of Staff, in the project
  <root>.`"; for a Driver or a worker the template of "Starting an agent".
- Every body's refusal (the line "A prompt that does not start with `chantier <role>` is not a
  chantier prompt: answer "I run inside a chantier batch only." and stop.") names the expected
  first line and says a new start is needed (D8), e.g. "I run inside a chantier batch only. My
  prompt must start with `chantier spec-writer for the Chief of Staff, in the project <root>.`;
  a message to me does not restart me: start a new agent with that line." Bodies stay identical
  per role on both hosts.
- `agents/stack-driver.md` and `com.github.copilot/agents/chantier-stack-driver.agent.md`: the
  description also says it makes one stack on the forge, merged in one go.
- Bump nothing by hand; the agent version header stays as `just version` keeps it.

### 9. Docs and SVGs that show the stack mode or its lifecycle

Each SVG changes with its `*-texts.md` companion, the same words in both.

- `docs/batch-modes.svg`, `docs/batch-modes-texts.md`: the Stack lane says "you merge from the
  bottom up; the stack driver restacks after each merge" (svg l. 111-112, 140-141): becomes one
  native stack, merged in one action from the top PR, the release last; add the insertion in one
  line (drafts above → insert → restack → stack on the forge → verify → ready).
- `docs/batch-pace.svg` ("one PR stack, one merge", "a stack: one merge at the end, the release
  on top"): already right; check its `<desc>` agrees.
- `docs/cr-lifecycle.svg`, `docs/cr-lifecycle-texts.md` (the "Stack driver" box, "order ·
  restack · ship · heavy CI"): add "one stack on the forge".
- `docs/cr-lifecycle-simple.svg`, `docs/cr-lifecycle-simple-texts.md` ("orders, restacks, ships
  PRs"): same.
- `docs/how-chantier-works.svg`, `docs/how-chantier-works-simple-foreman.svg`,
  `docs/how-chantier-works-simple-direct.svg` and their `-texts.md` ("responsible for PR/MR
  stacks"): check; change only if the words contradict D1.
- `docs/release-driver.svg`, `docs/release-driver-texts.md` ("stack's PRs opened as drafts",
  "merges the stack", "first stack merge to published"): the user merges the stack in one action.
- `README.md` "Batch modes" (l. 104-109) and its table (l. 222): one merge from the top PR; the
  extension recommended; the insertion use case in a sentence.
- `docs/use-cases-foreman.md` "Build a stack of pull requests" (l. 38-62) and the release
  section (l. 114-116): one merge; a new use case "Insert a change into a ready stack"; the
  phrases table gets the user's words for it.
- `docs/use-cases-direct.md` (l. 55-57): same in a sentence.
- `CONTRIBUTING.md` "Release" step 3 (l. 255-258): "merges it by rebase once CI is green, last (in
  a stack, from the bottom up)" becomes: in a stack, the whole stack in one action from the top
  PR, the release commit last; a change inserted into the stack makes the release PR update its
  release notes.
- `docs/release-process.md` "Which batch" (l. 136-143): one sentence on the insertion (the
  version PR stays on top and its notes are updated).

### 10. Scenario and tests

- `scenario/fake_gh.py` answers `gh api` for the stacks endpoint (create, read), from its state
  file, so the scenario can play a stack on the forge.
- `scenario/run_scenario.py`, section 13 "A stack on request" (l. 3108-3207) and the release on
  a stack: steps listed under Evidence.
- `skills/chantier/scripts/cli/tests/test_structure.py`, in
  `test_both_hosts_give_a_role_the_same_body_and_their_own_frontmatter`: each description ends
  with "Prompt starts with: `chantier <role>", and each body's refusal names the first line and
  a new start.

## Out of scope

- GitLab's equivalent of a native stack (a later CR); on GitLab the stack mode stays as today.
- The preflight check that the `gh stack` extension is installed, and allow rules for it in
  `hosts/claude-code.md` (`forge-permissions-at-start`, P1).
- Merging for the user: the user merges the stack; the steering session merges only under a
  release grant, as today.
- Series and parallel batches: unchanged.
- CR-212's own release-notes update: that CR's work.

## Evidence

- `just check` passes (Linux, macOS, Windows), `test_structure.py` included with the new
  assertions on descriptions and refusals.
- `just scenario` passes (the CLI, the cards and the scenario change), with new steps:
  - the forge-stack create on a stack batch with every PR recorded calls the stacks endpoint once
    with the PRs bottom to top and the release PR last (read in `fake_gh`'s call log), and prints
    the stack's link;
  - create is refused (exit 2) on a parallel batch and when a stacked CR has no PR;
  - show exits 0 on a stack that matches; prints one line per failed check and exits non-zero on
    a stack with a draft, a wrong order, the release not on top, or closed;
  - on a GitLab remote the command is refused with "GitHub only";
  - insertion: a CR added to a stack batch and ordered below the release CR with `stack` sits
    there in `take stack`, the release CR still last.
- `just mod` is not required: no change to `hooks/` or `types/`.
- The CR's own delivery: its PR inserted in stack #155 below PR 154, the stack read back on the
  forge with the five checks, recorded in a note.

## Decided by the Chief of Staff (2026-11-13)

The open questions were settled from the user's words, without asking the user (behaviour that
follows from those words) or left to the Driver (implementation detail):

1. The Chief of Staff turns the PRs above to draft at once, on the user's word to insert (as on
   2026-11-13); the stack driver checks it. The same holds when a CR in the middle of a ready
   stack goes back to its Driver for a new round: every PR above it goes to draft first, since
   the stack is changing under it ("mettre en draft le ou les PR qui seront au-dessus").
2. The stack driver's first line: the Driver's choice, written in `concepts.md` with the
   others; the proposal (`chantier stack-driver for the stack of batch <batch>, in the project
   <root>.`) is fine.
3. The command's name: the Driver's choice, kept apart from today's `stack`, which orders CRs.
4. The forge check uses the command's read whether the extension made the stack or not: one
   check everywhere.
5. A release CR of the CLI's release kind, once started, accepts an inserted CR in a stack batch
   on the user's word: the release goes back to `redo:` and updates its notes. The user asked
   exactly that for batch-15.
6. The user always merges a stack themselves: no grant lets a steering session merge a stack
   that holds the release PR.
