# Change Specification: a stack on GitLab behaves as a stack on GitHub

## Goal

The user (2026-11-14): chantier must deliver stacks "dans une variété de cas", on GitHub and on
GitLab, with the skill and the CLI given the tools to do it. On how a stack merges on GitLab:
"C'est exactement le même fonctionnement que les stack github. On peut merger des MR au milieu,
donc je veux le même fonctionnement." And on the proof: "GitLab, on testera plus tard. Fais au
mieux."

So, on GitLab as on GitHub (as CR-244 stack-grows-from-bottom defines GitHub's stack): the stack
made at two ready MRs, each further CR joining on top as a draft as soon as it has its MR, the
ready MRs below and the drafts on top, the same five checks read by `$CHANTIER forge-stack show`,
the same "partial stack mergeable below <commit>" line, the stack made and rebuilt by
`forge-stack`, the user free to merge any MR of the mergeable part at any moment (the bottom one
or one in the middle), and chantier retargeting and restacking what remains, silently. It is
designed from GitLab's public documentation and the existing GitLab forms of the cards, with no
real GitLab run: every GitLab form this CR adds or touches stays marked **unproved** until a real
run on a GitLab project, done later.

What is wrong today (`intake/request.md`, the critic's review of 2026-11-14):

- `forge-stack` refuses any non-GitHub link, `show` included (`GITHUB_ONLY` and `_pr_parts` in
  `skills/chantier/scripts/cli/src/chantier/commands/forge_stack.py`), so the five checks cannot
  run on GitLab (`foreman.md`, "The five checks of a ready stack", "GitHub only").
- `driver.md` ("Making the stack"): on GitLab the stack stays a chain, the first MR ready and the
  others drafts; "stack-ready" is undefined there, and each merge forces a full restack. CR-244
  keeps that for GitLab (its Area 7) and reads its partial-stack line on GitLab by hand
  (`glab mr view`, its Area 9).
- Every GitLab form is "unproved" (`chief-of-staff.md`, "Forge permissions", GitLab;
  `driver.md`, the Push bullet).

## Decisions carried (`02-answers.md` and the request)

| # | Decision | Where in this spec |
| --- | --- | --- |
| 1 | Grilled and specified first, then added at the end of batch-17's stack (one native stack at the end; budget raised to $210) | "Order in batch-17" |
| 2 | Exactly GitHub's stack behaviour on GitLab: the same ready stack, the same checks, any MR merged at any time (bottom or middle), chantier retargeting and restacking the rest. Rejected: bottom-up one by one only; one merge at the top | Areas 1 to 6 |
| 3 | Grilled enough on the restatement: the same five checks, `forge-stack show` on GitLab too, any MR merged at any time with chantier retargeting and restacking the rest; designed from GitLab's docs, the forms "unproved" until a real run later | Areas 1 to 7, "Out of scope" |
| 4 | The spec's defaults accepted: a middle MR merged into the branch below ("folded") has its CR recorded merged at once, the MR below goes back to its Driver, the rest is restacked; nothing blocks a middle merge; `glab stack` (experimental) not used; check 5 reads that no open MR targets the release's branch | Areas 1, 4, "Out of scope" |
| R | The user's word in the request (2026-11-14): no real run now; the forms stay "unproved" until a real GitLab run, done later; lowered to P2 | Area 7, "Out of scope" |

## Words

As CR-244 defines them (`.agents/changes/4-batch/1-pending/244-stack-grows-from-bottom/
03-change-spec.md`, "Words used below"), read on GitLab with "MR" for "PR":

- **The stack (as it stands):** the CRs of `chain()`, bottom first, while each has an MR
  recorded: the ready CRs first, in readiness order, then the CRs with a draft MR.
- **The mergeable part:** the CRs from the bottom while each is `ready` and its MR not a draft.
  **Its commit:** the head of its highest MR (`head` in the record, seven characters).
- **Drafts on top**, **to come** (open CRs with no MR yet), **complete**: as in CR-244.
- **The chain:** what a stack is on GitLab: MR 1 targets the default branch, MR k targets the
  source branch of MR k-1.

## What GitLab's documentation gives (the ground of this design, all unproved here)

Read from GitLab's public docs (REST API "Merge requests", "Projects", "Merge trains"; the user
docs "Merge requests", "Merge request dependencies", "Merge trains", and `glab`'s "Stacked
diffs"). None of it was tried against a real GitLab for this CR; the Driver re-reads the pages it
relies on and names them in the PR.

- **No server-side stack.** GitLab has no object that groups MRs into one stack merged in one
  action. `glab stack` (experimental "stacked diffs") is local metadata in the clone plus a chain
  of MRs. A GitLab stack is therefore the chain. "Unstack, then create" (CR-244's rebuild) has no
  unstack on GitLab: the chain is made by retargeting.
- **An MR read:** `GET /projects/:id/merge_requests/:iid` (`:id` the URL-encoded project path)
  gives `iid`, `state` (`opened`, `closed`, `merged`, `locked`), `draft` (boolean),
  `source_branch`, `target_branch`, `sha`, `web_url`, `detailed_merge_status`.
- **The MRs on a branch:** `GET /projects/:id/merge_requests?state=opened&target_branch=<b>`.
- **Retarget:** `PUT /projects/:id/merge_requests/:iid` with `target_branch=<b>`; nothing stops
  it on an open MR (unlike a stacked GitHub PR).
- **Draft or ready:** `glab mr update <iid> --draft` / `--ready` (already in the cards). GitLab
  does not merge a draft MR, so a draft on top cannot be merged, as on GitHub.
- **Merging an MR merges it into its target branch.** Merging MR k in the middle of the chain
  merges its branch into the branch of MR k-1, not into the default branch: the change rides on
  in MR k-1. When a merged MR's source branch is deleted at the merge, GitLab retargets the open
  MRs that targeted it to the merged MR's target branch ("Update merge requests when target
  branch merges").
- **Merge trains** (Premium and up; the project's `merge_trains_enabled`): merging an MR on the
  default branch adds it to the train; it is `merged` only once its train pipeline passes. Only
  an MR that targets the train's branch can join. "Auto-merge" (merge when the pipeline
  succeeds) is the same: set, not yet merged.
- **`glab api`** takes `--method`, `-f`/`--raw-field`, `--hostname` for a host other than
  gitlab.com, and answers JSON.

What this gives against GitHub, said plainly in the cards: GitLab has no one-action merge of a
stack, nor of an MR "with all those under it" (CR-244's Words). The user's ways on GitHub (one
action from any PR of the mergeable part, or one PR at a time from the bottom) become on GitLab:
**one MR at a time from the bottom, up to any MR of the mergeable part**, each landing on the
default branch; and **an MR merged in the middle directly**, which GitLab folds into the MR below
it (Area 4).

## What changes

The CLI (`forge-stack`), four cards (and one sentence of `chief-of-staff.md`'s "Reports" bullet
as CR-244 writes it), the scenario and its fake `glab`. No agent file (`agents/`,
`com.github.copilot/agents/`), no `hooks/` or `types/` (no `just mod`), no version edit, no CI
job. `status-layout.md`'s partial-stack line (CR-244, Area 9) is unchanged: it now reads the same
on both forges.

### Area 1: `forge-stack` reads and makes the chain on GitLab (`commands/forge_stack.py`)

Written against the module as CR-234 and CR-244 leave it (the stack as it stands, drafts on top,
the status-aware check 4, the partial-stack line, the `to come:` line, `UNSTACK_TRIES`); see
"Order in batch-17".

**The forge, from the links.** A link is a GitHub PR when it matches today's `PR_LINK`
(`…/<owner>/<repo>/pull/<n>`), a GitLab MR when it matches
`^https?://([^/\s]+)/(.+?)/-/merge_requests/(\d+)` (host, the project's full path, subgroups
included, and the iid). The forge is read from the shape of the link, never from the host (a
self-managed GitLab has any host).

- `GITHUB_ONLY` goes. A link of neither shape:
  `forge-stack reads GitHub pull requests and GitLab merge requests: <link> is neither` (exit 2).
- Links of both shapes in one stack, or GitLab MRs of two projects:
  `the stack's PRs are not all in one repository` (the existing text, exit 2).
- `--stack N` on a GitLab stack: `--stack is GitHub only: a GitLab stack is the chain of its MRs`
  (exit 2).
- CR-244's refusal with no PR at the bottom (`no PR at the bottom of the stack: …`) holds on
  GitLab as it is.

**A `_glab` helper** beside `_gh`: `shutil.which("glab")`, else
`glab: not found on PATH (the user's own glab login is needed)` (exit 4); the command is
`glab api <path> [--method <M>] [-f k=v]…`, with `--hostname <host>` when the host is not
`gitlab.com`; `capture_output`, `text`, `encoding="utf-8"`, `errors="replace"`, `check=False`; a
non-zero exit or a non-JSON answer is a `ChantierError` with the exact text, exit 4, as `_gh`
does. The project path is URL-encoded in the API path (`projects/acme%2Fdemo/…`).

**`show` on GitLab: the five checks, read on the chain.** For each MR of the stack as it stands
(the rows, drafts included), one `GET` of the MR; for each source branch of the rows, one `GET`
of the open MRs that target it. The checks keep CR-244's numbers and meaning:

1. **Open:** every MR of the rows reads `state: opened`. Else one line per MR:
   `check 1: !<iid> is <state>`; a merged MR whose target is not the default branch says so:
   `check 1: !<iid> merged into <target>, not <default branch>: folded into <cr below>`.
2. **Every MR of the rows, and no other:** no open MR outside the rows targets a source branch
   of the rows. A foreign MR: `check 2: not in the batch's stack !<iid> (on <branch>)`. An MR of
   the batch's stack left out of the rows (CR-244: its CR placed above one with no MR) that
   targets a branch of the rows: no failure while it is a draft (named in the `to come:` line),
   a failure when it is not: `check 2: not in the stack as it stands !<iid> (<cr>)`.
3. **In the record's order, bottom first:** each MR's `target_branch` is the record's base for
   its CR (`stack_base(…, planned=True)`: the default branch for the first, the branch of the CR
   under it for the others). Else `check 3: !<iid> targets <actual>, expected <base> (bottom
   first)`, one line per MR.
4. **Drafts, against each CR's status** (CR-244's three forms, `!` for `#`):
   `check 4: still a draft !<iid>` (a ready CR's MR still a draft while every MR under it is
   ready: the stack driver turns it ready); `check 4: not a draft !<iid> (<cr> <status>)`;
   `check 4: a draft under a ready MR !<iid>`. A draft on top of a CR not ready is no failure.
5. **The release on top,** when the release is in the stack: no open MR targets the release MR's
   source branch (answer 4). Else `check 5: the release MR !<iid> is not on top (!<x> targets
   it)`.

All hold, one line, CR-244's success line read on the chain: `chain <top MR link> ready: open,
<K> MRs in order, partial stack mergeable below <sha7> (!<m>, <M> MRs)` (`stack complete,
mergeable below <sha7> (!<m>)` once complete), then `, drafts on top !<a> !<b>` when there are,
and `, the release on top`; `<sha7>` is the record's `head` of the highest CR of the mergeable
part, as on GitHub. Then the `to come:` line when drafts are on top or CRs are to come (as CR-244
prints it), exit 0. A failure: the lines, exit 2. `show` writes nothing.

**`create` and `rebuild` on GitLab: the same step** (CR-244's "unstack, then create" has nothing
to unstack). Both retarget, bottom first, each MR of the rows (drafts included) whose
`target_branch` is not the record's base (`PUT … target_branch=<base>`; a done line
`!<iid> target <old> -> <base>` each), then read the chain back with `show`'s checks; `rebuild`
passes the `check 4: still a draft` lines and the `to come:` line through as no failure, as CR-244
does on GitHub. `create` on a chain already in place retargets nothing and exits 0 (no "already in
a stack" refusal on GitLab). An MR left out of the rows (to come) is never retargeted. A forge
refusal stops at once, prints the done lines and the forge's exact text, exit 4 (the existing
handler). The first line on success: `chain <top MR link> (MRs bottom to top: !<a> !<b> …)`.

**Shape of the code.** The GitHub path is unchanged in behaviour. The Driver may put the GitLab
reads and the retarget in a new module (for instance `commands/forge_stack_gitlab.py`) to keep
each function under fifty lines and complexity 10, mypy strict and ruff clean (`just lint` in
`just check`); the dispatch in `forge_stack` picks the path from the rows' forge. The checks'
status logic (check 4, the mergeable part, its commit) is shared by both forges, not copied.

**Help and docstrings.** The `forge-stack` help says, after CR-244's "the stack batch's stack as
it stands (the bottom CRs with a PR, drafts on top)": "on GitHub its native stack, on GitLab the
chain of MRs each targeting the one below; rebuild: GitHub unstacks, retargets and creates again,
GitLab retargets". "GitHub only" leaves the help, except for `--stack`.

### Area 2: making and changing the stack on GitLab (`driver.md`, "Stack driver")

- **The opening** (as CR-233 and CR-244 leave it): add that on GitLab the stack is the chain of
  MRs made by `$CHANTIER forge-stack create`, each MR targeting the one below, the ready MRs below
  and the drafts on top; the user merges it one MR at a time from the bottom (GitLab has no
  one-action merge); a middle MR may be merged directly (Area 4). Unproved; trial: one run on a
  GitLab project.
- **"Making the stack"** (as CR-244 rewrites it: at two ready PRs, drafts on top): its means on
  GitLab is always `$CHANTIER forge-stack create` (no extension); then every MR of the mergeable
  part is turned ready (`glab mr update <iid> --ready`), the drafts on top left drafts. The old
  sentence "On GitLab the stack stays a chain as today: the first PR on the default branch is
  ready, the others drafts" goes.
- **A CR that joins, a draft that turns ready, an insertion, a restack after a merge** (CR-244's
  paragraphs): the same on GitLab, each change ending with `$CHANTIER forge-stack rebuild` (on
  GitLab it retargets; there is nothing to unstack). The rule "never retarget a PR by hand" holds
  on GitLab too (`forge-stack` retargets), though GitLab would allow it. Who moves a branch
  (CR-244, decision 9) is unchanged. A refused `create` or `rebuild` is an `anomaly` with the
  exact text, as today.
- **"The five checks":** read with `forge-stack show` on both forges; add one sentence: on GitLab
  the checks read the chain (each MR's target is the branch below, the first on the default
  branch; no other MR on a branch of the stack but drafts of CRs to come; drafts only on top; the
  release on top).
- **"After a partial merge":** unchanged on GitLab (one restack of what remains on
  `origin/<default branch>`, one `rebuild`, silently). Add: GitLab may already have retargeted
  the next MR to the default branch when the merged MR's source branch was deleted; `rebuild`
  then retargets nothing for it, which is no anomaly. A middle merge: Area 4.
- The Push bullet's GitLab description-file form stays as it is, unproved.

### Area 3: the Foreman (`foreman.md`)

- **"The five checks of a ready stack"** (as CR-244 rewords it): "GitHub only" goes; add "on
  GitLab, read on the chain of MRs (unproved; trial: one run on a GitLab project)".
- **The stack batch paragraph** ("Its end is one native stack …", as CR-233 and CR-244 leave it):
  add "on GitLab, the chain checked by `forge-stack`, merged one MR at a time from the bottom".
  The first take at two ready MRs, each later take, and the `stack-ready` asks (with the commit
  and the `to come:` tail) are the same on GitLab; the asks' `<stack link>` is the top MR's link.
- **"A native stack of the batch is on the forge"** (CR-233's restack-or-rebase choice, as CR-244
  narrows it): on GitLab, a chain made by `forge-stack create` (or `rebuild`) and read back by
  `show`.
- **A folded CR** (Area 4): on the Chief of Staff's `order merged <k>` with the note `folded:
  <k> into <k-1>`, the CR below goes back to a Driver first, `take <k-1> --note "folded: <k>
  merged into its branch"` (a slot, or it waits like a queued CR); the restack of what remains
  (`take stack`) comes after its hand-back.

### Area 4: an MR merged in the middle on GitLab (decisions 2 and 4)

The user may merge any MR of the mergeable part at any time. On GitLab, merging MR k whose
target is the branch of CR k-1 lands it on that branch, not on the default branch. chantier
follows it, with no refusal, no block and no reproach (answer 4: nothing blocks a middle merge):

- **What the user is told beforehand** (`chief-of-staff.md`, Area 5): to bring the MRs up to
  MR k onto the default branch (what one action on MR k does on GitHub), merge them one at a time
  from the bottom up to k; each lands on the default branch (GitLab retargets the next one when
  the merged MR's source branch is deleted, else chantier's restack does). Merging an MR in the
  middle directly folds it into the MR below it: its change reaches the default branch when that
  MR merges.
- **When the user merges a middle MR anyway** (the user says so, or `forge-stack show` prints
  `check 1: !<iid> merged into <target> … folded into <cr below>`): the Chief of Staff records
  `order merged <k>` at once (answer 4; the MR is merged on the forge: the user's merge is a
  fact, as in CR-233), with `order note <k-1> --note "folded: <k> into <k-1>"`, tells the Foreman
  in the same message, and tells the user that CR k's change now rides in CR k-1's MR.
- **CR k-1's Driver** (`driver.md`, beside the `rebase: <cr> merged` paragraph): on a `folded:
  <k> merged into its branch` note, bring the forge's branch into the worktree (`git fetch`, then
  `git merge --ff-only origin/<branch>`; one that cannot fast-forward is a `conflict-resolver`'s,
  never `git reset --hard`), add to `pr-body.md` one line naming the folded CR's change and its
  merged MR (Deliverables, and the Internal references), post the file, then treat it as a move
  that changed the CR's patch: `verifier` given the move, `inspector` on it (its `APPROVE`
  recorded first), the long gate and CI at the new head, the description pass, and hand back as
  before. Unproved; trial: one run on a GitLab project.
- **The stack driver** then restacks what remains as after any merge, silently: CR k+1 now sits
  on CR k-1 (`take stack` prints it, since CR k is merged), and `rebuild` retargets MR k+1 when
  GitLab did not already.
- **On GitHub** nothing changes: CR-233's and CR-244's procedure holds.

### Area 5: what the Chief of Staff does and says (`chief-of-staff.md`)

- **The plan at the go** (step 2, the stack recommendation as CR-244 leaves it; "GitHub only: on
  GitLab the stack stays as it was" goes): on GitLab, say that the stack is made by
  `$CHANTIER forge-stack create` (the chain of MRs, each on the one below; no extension to
  install, nothing to record in `brief.md`), at two ready MRs, growing as CR-244 says, and that
  the user will merge it one MR at a time from the bottom, a middle MR folding into the one
  below; unproved on GitLab (no real run yet).
- **"A stack batch"** (as CR-233 and CR-244 leave it): the `stack-ready` asks are read with
  `forge-stack show` on both forges and name the commit the same way. On GitLab, tell the user
  the stack is mergeable one MR at a time from the bottom up to the MR of the commit named, never
  "in one action from that MR"; that each next MR is mergeable once GitLab shows it so
  (retargeted to the default branch and its pipeline green; when GitLab says it needs a rebase,
  chantier's restack brings it); and the folded case of Area 4 in one sentence. The rest (gaps,
  `order merged` bottom first in one message to the Foreman, a failing check sent back, the
  silent restack) is unchanged.
- **"Reports"** (CR-244, Area 9): its sentence "`$CHANTIER forge-stack show` (GitHub; read only)"
  loses "GitHub;", and its sentence "On GitLab the line names the head of the highest MR of the
  chain that is ready on the forge, read with `glab mr view`" goes: the partial-stack line comes
  from `forge-stack show` on both forges.
- **Merge trains and auto-merge** (GitLab): an MR added to a merge train or set to auto-merge is
  not merged. On the user's "merged", read the MR (`glab mr view <iid>`); record `order merged`
  only once it reads merged, else say that it is recorded once the train (or the pipeline)
  merges it, and read it again at the next report. Only the bottom MR (on the default branch)
  can join the train; the next joins once it is retargeted after that merge. Unproved; trial:
  one run on a GitLab project with merge trains.
- **Inserting a CR into a ready stack:** unchanged (`glab mr update --draft` is already named).

### Area 6: `concepts.md`

- **Stack** (as CR-233 and CR-244 leave it): "On GitHub a stack is the forge's native stacked-PR
  stack; on GitLab the stack stays a chain, as it was" becomes: on GitHub a stack is the forge's
  native stacked-PR stack; on GitLab, which has none, it is the chain of MRs `forge-stack` makes
  and checks, each targeting the one below, the first on the default branch, ready MRs below and
  drafts on top, merged one MR at a time from the bottom (a middle MR merged folds into the one
  below it); unproved on GitLab. **Stack ready** keeps its five checks, read on both forges. The
  sentence "A chain of PRs based on each other is not a stack" gets "on GitHub" (on GitLab the
  checked chain is the stack).
- **Ready to merge** (as CR-233 and CR-244 leave it): merging a PR of the mergeable part "with
  those under it" in one action is GitHub's; on GitLab the MRs under it are merged first, one at
  a time from the bottom.

### Area 7: what stays unproved, and how it is said

Every GitLab form this CR writes in a card carries the cards' existing marker, "unproved; trial:
one run on a GitLab project" (as `chief-of-staff.md`'s GitLab forge permissions and `driver.md`'s
Push bullet do). The CLI's GitLab path is proved only against `scenario/fake_glab.py`, whose
answers follow the documented shapes; the PR's Known gaps say "the GitLab path of `forge-stack`
and the GitLab cards are not run against a real GitLab (unproved, per the user's word of
2026-11-14)". The real run, and the removal of the marker after it, are a later CR.

## What this CR changes on top of CR-233, CR-234 and CR-244

- **CR-233 (merge-any-time, cards):** keeps all of it (any ready PR on the default branch
  mergeable on its own, `you can merge` only after `ready`, the merged-early Driver, the
  restack-or-rebase choice). Adds: the GitLab reading of its merge ways (on GitLab one MR at a
  time from the bottom, plus the folded middle merge); what "a native stack on the forge" means on
  GitLab; the folded CR's handling; merge trains.
- **CR-234 (forge-stack-followups):** keeps `UNSTACK_TRIES`, `_unstack`'s exit-4 text, `_rebuild`'s
  docstring and its scenario steps; none of them applies on GitLab (nothing is unstacked there).
  This CR adds the GitLab path beside them and replaces `GITHUB_ONLY`, so CR-234's checks "on a
  GitLab link `forge-stack …` is refused: GitHub only" change (scenario, item 6).
- **CR-244 (stack-grows-from-bottom):** keeps all its GitHub behaviour: the stack as it stands
  with drafts on top, the first stack at two ready PRs, CRs joining as drafts, rebuild = unstack
  + create, check 4 against the status, the "partial stack mergeable below <commit>" line, the
  silent restack, the asks, "deliver by a time". This CR:
  - replaces its **Area 7** ("On GitLab the stack stays a chain (no `forge-stack`) … the first MR
    on the default branch is ready, the others drafts"): on GitLab the stack is made, grown and
    checked by `forge-stack` as on GitHub, drafts on top of the chain, the mergeable part ready;
  - gives its rebuild a GitLab form (retarget only, no unstack) and its five checks and success
    line a GitLab reading (Area 1), the commit being the head of the highest ready MR;
  - replaces its Area 9 sentence that reads the GitLab line with `glab mr view`, and drops
    "GitHub;" from its "Reports" read (Area 5);
  - its "Out of scope" line on GitLab stack delivery is this CR.

## Out of scope

- A real run on a GitLab project, and dropping "unproved" from the GitLab forms (the user's word:
  later, its own CR).
- `glab stack` (experimental, with its own local metadata beside chantier's record; answer 4:
  not used) and GitLab's "merge request dependencies" (answer 4: nothing blocks a middle merge).
- Any merge by an agent: the user merges, as today; the grant's rules are unchanged.
- A sixth check: CI green at the top stays the stack driver's condition before it turns an MR
  ready or rebuilds the stack, on both forges, as today (decision 3: the same five checks).
- Mergeability (`detailed_merge_status`) as a check of `show`.
- The docs and README sentences on GitLab stacks (`README.md`, `docs/`, the SVGs,
  `CONTRIBUTING.md`) and the eval kit: a docs follow-up, as in CR-233.
- P10's samples (`commands/permissions.py`): the CLI runs `glab api` itself under `$CHANTIER`,
  and the agents' `glab mr update` / `glab mr view` samples already exist.
- `hooks/`, `types/`, the agent files, the CI workflow, any version edit; the board pane and
  `STATUS` files (unchanged, no screenshot due).

## Order in batch-17

CR-233 (PR #173) and CR-234 (PR #175) are not merged yet; CR-244 is pending in batch-17
(`.agents/changes/4-batch/1-pending/244-stack-grows-from-bottom/`). This CR goes on top of
batch-17's stack after the three (`order add`, decision 1) and is written against their merged
text: the same `forge_stack.py` functions (`_plan`, `_checks`, `_show`, `_rebuild`, `_create`,
`register`) and the same card paragraphs. Sharing files is no reason for `depends.json`; its
place in the stack already puts it above them. Its Driver works on CR-244's merged code (or its
branch, in the stack, before the merge); the GitLab path shares CR-244's status logic rather than
copying it. Its card changes reach the running batch only once merged into the main checkout and
reloaded.

## Evidence

**Checks:** `just check` passes (Linux, macOS, Windows), `just lint` within it.

**Scenario** (`just scenario`, both forges; the CLI and cards change), in `run_scenario.py`
section 13a (`forge_stack_cli`), `scenario/fake_glab.py` and `scenario/README.md`, with CR-244's
`record()` statuses:

1. `fake_glab.py` answers, from the state's `mrs` (iid → `state`, `draft`, `source_branch`,
   `target_branch`, `web_url`): `GET projects/<path>/merge_requests/<iid>`;
   `GET projects/<path>/merge_requests?state=opened&target_branch=<b>`;
   `PUT projects/<path>/merge_requests/<iid>` with `-f target_branch=<b>` (it updates the state);
   `retarget_refused` makes the `PUT` fail with a forge text. The calls are logged as today.
2. `--forge gitlab`, CR-244's first steps on the chain: `a`, `b` ready with MRs 201, 202 and the
   release with none: `create` retargets each MR off the record's base, bottom first, passes
   `--hostname gitlab.example.com`, prints `chain <top link> (MRs bottom to top: !201 !202)`, exit
   0; `show` prints `partial stack mergeable below <b's head> (!202` and `to come: <r> …`, exit 0,
   and writes nothing (no `PUT` logged); a second `create` retargets nothing, exit 0.
3. `--forge gitlab`, a CR joins as a draft: `new` working with draft MR 204 ordered on top:
   `rebuild` retargets !204 onto `b`'s branch (no unstack call), `show` prints `mergeable below
   <b's head> (!202`, `drafts on top !204`, `to come: <new> working, <r> queued`, exit 0.
4. `--forge gitlab`, one case each, the line and its cause, exit 2: CR-244's three check 4 forms
   (`still a draft !204` with `new` ready; `not a draft !204 (<new> working)`; `a draft under a
   ready MR !201`); an MR on the wrong target (`check 3`); a foreign open MR on a stack branch
   (`check 2 … not in the batch's stack`); a closed MR (`check 1`); an MR merged into the branch
   below (`check 1 … folded into <cr>`); an open MR targeting the release's branch (`check 5`);
   the complete chain prints `stack complete, mergeable below <r's head>` and no `to come:`.
5. `--forge gitlab`: `rebuild` with `retarget_refused` exits 4, prints the done lines before the
   forge's text; `show --stack 5` is refused naming `GitHub only`.
6. `--forge github`: the existing and CR-244's steps pass; the checks of a GitLab link in a
   GitHub stack (around today's lines 3636-3640 and 3717-3720, as CR-234 and CR-244 leave them)
   now expect `not all in one repository`; a link of neither shape is refused naming `is
   neither`.

**Reading pass**, in the PR's Test plan: `rg -n "GitHub only" skills/chantier/references` finds
none about the stack; `rg -n "stays a chain|glab mr view\`$" skills/chantier/references` finds no
GitLab stack exception; each GitLab stack form in `driver.md`, `foreman.md`, `chief-of-staff.md`
and `concepts.md` carries "unproved"; the four cards tell the same GitLab merge (one MR at a time
from the bottom, a middle MR folding into the one below).

No CI job is added or changed.

## Self-containment for the Driver

Files: `skills/chantier/scripts/cli/src/chantier/commands/forge_stack.py` (and, if the Driver
splits it, a new `commands/forge_stack_gitlab.py`), `skills/chantier/references/driver.md`,
`foreman.md`, `chief-of-staff.md`, `concepts.md`, `scenario/fake_glab.py`,
`scenario/run_scenario.py`, `scenario/README.md`. Read CR-233's and CR-234's specifications in
`.agents/changes/4-batch/2-actives/233-merge-any-time/` and `234-forge-stack-followups/`, and
CR-244's in `.agents/changes/4-batch/1-pending/244-stack-grows-from-bottom/` (or where the batch
moved it), and work on their merged text. Re-read the GitLab doc pages named above before coding
and cite them in the PR.

## Open questions

None: answer 4 settled them.
