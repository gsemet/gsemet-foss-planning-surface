# Change Specification: proof bound to the head

## Goal

Four rules taken from jleechan's `pr-lifecycle` skill, and one point the user settled in the
grill (2026-11-10):

1. Each proof names the SHA it judged. When the head moves (a new round, a rebase, a restack),
   only what the move touched is judged again. The PR says which SHA covers each proof, and a
   stale proof is marked as stale.
2. A claim in the PR with no proof is marked `UNVERIFIED`, or narrowed honestly; never left as a
   plain fact.
3. A cost or a time chantier did not observe is shown as unknown, never as 0.
4. The Driver's card says: while CI runs, do everything else first, then one long wait.
5. For a UI project, the Verifier itself checks that the screenshots show what the PR claims. No
   new role.

## Decisions carried from `02-answers.md`

| # | Decision | Where it lands |
| --- | --- | --- |
| 1 | When the head moves, "only what moved" is judged again; the PR names the SHA of each proof; a stale proof is marked | Areas A, B |
| 2 | The visual check is the Verifier's, no new role | Area E |
| 3 | CI wait: "just the card": other work first, then one long wait; no measure first, no CLI tool | Area D |
| R2 | `UNVERIFIED` or an honest narrowing (restatement, point 2) | Area B |
| R3 | Unknown, never 0, for cost and time (restatement, point 3) | Area C |

## What changes

All the card changes are in `skills/chantier/references/`. The agent files (`agents/`,
`com.github.copilot/agents/`) do not change: the contract lives in the cards.

### A. Each judgment names its SHA, and only what moved is judged again

Words used below: the **head** is the CR branch's commit the judgment covers; a **move** is any
change of the head after a judgment: a new round, a rebase (the `rebase:` note, or the rebase
before the long gate), a restack by the stack driver, a conflict resolution.

**`worker.md`, Inspector.**

- The JSON reply gains one field, `"head"`: the worktree's `git rev-parse HEAD` at the review.
  The verdict covers that commit plus the uncommitted diff it reviewed:
  `{"verdict": …, "head": "<sha>", "blocking": […], "minor": […], "confidence": 0.0}`.
- New paragraph: "Given a move (`<old head>..<new head>` and its kind), review only what the
  move changed in the CR's own patch (`git range-diff <old base>..<old head> <new base>..<new
  head>` for a rebase or a restack; the diff for a resolved conflict), and say in `minor` what
  you carried unchanged."

**`worker.md`, Verifier.**

- `verify.md` holds a `Head: <sha>` line, and each claim names the SHA it was judged at, with its
  command and output. A claim carried from an earlier judgment keeps its own SHA and says why the
  move did not touch it (`carried from <sha7>: <reason>`).
- New paragraph, the delta assessment: "Given the previous `verify.md` and a move, judge again
  each claim the move touched, and the claims that failed; carry the others. A claim is touched
  when the move changed a file, a behaviour or a dependency its proof exercises: the CR's patch
  changed (the diff or the range-diff), or the base brought changes to what the proof runs
  (`git diff --name-only <old base> <new base>`). You judge it; in doubt, judge it again. The
  same holds for the before/after pairs: capture again only a pair the move touched."
- `before-after.md` names, for each pair, the SHA of the before (the base) and of the after.

**`driver.md`, CR driver.**

- After an Inspector's `APPROVE`, the Driver commits with nothing changed in between and records
  `note <cr> "r<n> approved at <head from the JSON>, committed as <sha>"`.
- Every Verifier the Driver starts after the first one is given the previous `verify.md`, the
  move (`<old head>..<new head>`, with the old and new base for a rebase) and its kind.
- After a rebase whose range-diff shows the CR's patch changed (a resolved conflict), an
  `inspector` reviews that change alone (Area A, Inspector), with no `$CHANTIER round` and no
  `coder`, as for a body-only re-inspection; `FIX-REQUIRED` on the code is a round.
- The paragraph on the `rebase: <dependency> merged` note: a clean rebase and green CI still start
  no `coder` round, but a `verifier` given the move judges again what the move touched before
  `handback ready`.
- Before `handback ready`, no proof in the PR is stale (Area B).

**`driver.md`, Stack driver.**

- For each PR it moves: when the move touched a CR's proofs (its patch changed, or the base
  brought changes to what the proofs run), it starts a `verifier` with that CR's previous
  `verify.md` and the move, and an `inspector` when the CR's patch changed; it updates the PR's
  Test plan SHAs (carried, or judged again) with `gh pr edit --body-file` / `glab mr update
  --description`. A touched proof it cannot judge again stays marked stale in the PR and is an
  `anomaly`.

**`concepts.md`, rule 5** ("Evidence is a command run at the pushed head"): add one sentence:
"Every judgment names the SHA it covers; after a move, what the move touched is judged again and
the rest is carried, saying so."

### B. The PR says which SHA covers each proof; stale and unproven are marked

**`pr-template.md`.**

- A new rule, after the Impacts rule: "Each proof names the SHA it covers (seven characters): the
  Test plan items, and the captions of the before/after visuals in Deliverables (before at the
  base's SHA, after at the head's). A proof carried over a move says so (`carried from
  <sha7>`). A proof the head has moved past, not yet judged again, is marked `STALE (judged at
  <sha7>, head now <sha7>)`. A claim in Summary, Deliverables, Changes or Impacts with no proof
  (no test, no gate, no Verifier claim, no evidence) starts with `**UNVERIFIED:**`, or is
  narrowed to what is proven; it is never left as a plain fact."
- The template's Test plan becomes:

  ```markdown
  - [ ] New or changed tests (they fail on the previous code) <!-- or "No behaviour change" -->
  - [ ] Local gates at `<sha7>`: <!-- the commands run and their results -->
  - [ ] Evidence: before at `<sha7>`, after at `<sha7>` <!-- or why there is none -->
  - [ ] Review: approved at `<sha7>`
  - [ ] Verified at `<sha7>` <!-- claims carried from an earlier SHA say so -->
  - [ ] CI green at `<sha7>`
  ```

- The template's HTML comment at the top gains one line: "Name the SHA of each proof; mark a
  stale one STALE and an unproven claim UNVERIFIED."
- The audit list: no new Inspector item (the Inspector reviews before the push, when no proof
  has a SHA yet).

**`worker.md`, Verifier, the description check** (the paragraph on the posted description) gains:
"Each proof in the description names its SHA, which is the head or carried with its reason; a
claim stated as fact with no proof in `verify.md`, the gates or the evidence is `NOT VERIFIED`
(the Driver marks it `UNVERIFIED` or narrows it). A `STALE` mark left at the end is `NOT
VERIFIED`."

**`driver.md`, the CR driver's paragraph** ("then the evidence in Deliverables and the Test plan
boxes updated"): the Test plan boxes and captions carry the SHAs of Area B; a claim the Verifier
could not prove is marked `UNVERIFIED` or narrowed in `pr-body.md` before the description pass.

### C. Unknown, never 0, in metrics

The CLI (`skills/chantier/scripts/cli/src/chantier/`) shows `$0.00` or `0 min` where it observed
nothing. Each place below shows `unknown` (or keeps its existing `-` or `never`) instead:

- `commands.py`, the batch's creation (around line 595): `spent_usd` starts at `None`, not
  `0.0`, until the first priced refresh (`_record_costs`) sets it. A batch file written by an
  earlier version keeps its number.
- `commands.py`, `status` (line ~1119): `spent ${…:.2f}` becomes `spent unknown` while
  `spent_usd` is `None`; the budget part (` of $<budget>`) stays.
- `commands.py`, `_refresh` (line ~1076): `age_minutes(c.get("updated")) or 0` counts a live CR
  with no recorded time as 0 minutes silent. A CR with no time is left out of the "longest silent
  Driver" line, or named with `unknown`; never `0 min`.
- `rails.py`, `over_budget` and `check_budget`: read a `None` spend without failing; the rail
  behaves as today on a spend not priced yet (a Driver may start: see the open question). Its
  message prints `unknown` rather than `$0.00` if it ever names a `None` spend.
- `commands.py`, `order budget`'s refusal message (line ~1678): same.
- `status.py`, `batch_view` (line ~272): `spent_usd` is passed as recorded (`None` allowed), and
  `priced` is false while it is `None`; `batch_markdown` then writes `spent unknown`, as it already
  does after a failed pause.
- `status.py`, `dashboard_markdown` / `_budget`: a batch with no priced spend shows `unknown` (and
  ` of $<budget>` when there is one), not `$0.00`.
- Already right, unchanged: a CR with no figure (`-` in tables, "No figure yet." in its
  `STATUS.md`), `heartbeat never`, `Chief of Staff: not measured`, `Spent: unknown (…)` after a
  failed pricing at the pause, `close` refusing an unpriced final cost, and the `not measured`
  parts of `cost --explain`. A measured zero (`0 compaction calls`, `0 of 0 timed calls`) stays a
  number.

**`status-layout.md`, "The rules of every report":** add a bullet: "A cost or a time chantier did
not observe is written `unknown` (or as the CLI prints it: `-`, `never`, `not measured`), never
0; a 0 is only a measured zero."

### D. One long wait during CI

**`driver.md`, the CI bullet** ("CI: wait with the forge's own watch…"): it starts with: "While
CI runs, do everything that does not need its result first: `pr-body.md` and the description as
far as they can go, the archive's `delivery.md`, your notes. Then one long wait: the forge's
watch in a background shell, end your turn, and let its end wake you; no `gh pr checks` or `glab
ci` look in between." The rest of the bullet (reading the result, the re-run, the 3-hour limit)
is unchanged. No measure, no CLI tool.

### E. The Verifier checks that the screenshots show what the PR claims

**`worker.md`, Verifier**, the evidence paragraph gains: "When the evidence holds screenshots or
videos (a project with a UI), open each one and check that it shows what the PR claims of it: the
screen, the state and the change the Summary, Deliverables and Impacts say, legible, with nothing
that contradicts them. A capture that does not show its claim fails that claim. On the
description pass, check that the images attached are the ones captured at the SHA they name."
No new role, no project option, no second seat. chantier itself has no UI: its own PRs carry no
screenshots, and this changes nothing for them.

## Out of scope

- pr-lifecycle's `Goal:` status line and six stage labels; its two-seat check of a headline UI
  claim; its linked files (`review-routing.md`, `review-recovery.md`, `exceptions.md`,
  `review-records.md`, `six-stage.md`), not read.
- A measure of the tokens a Driver spends waiting on CI, and any CLI tool for the wait.
- A visual review option in `AGENTS.md` or any new role or agent file.
- Recording in the CLI which SHA each proof covers: the cards and the PR carry it; the CLI
  already records the long gate's pass and the PR at a head (`gate`, `ship`).
- Changing what the budget rail does on a spend not priced yet (open question below).
- The order of the steps after the push (the Verifier still runs after CI).

## Evidence

- `just check` passes on Linux, macOS and Windows (the structure tests: links in the cards
  resolve; each role keeps its section; both hosts' agent bodies stay identical).
- `just scenario` passes (the CLI changes), with new checks in `scenario/run_scenario.py`:
  - right after the batch opens, before any priced refresh: `chantier status`'s first line holds
    `spent unknown` and no `spent $0.00`; the batch's `STATUS.md` header says `spent unknown`;
    the dashboard `.agents/changes/STATUS.md` shows `unknown` for that batch;
  - after the first priced `status --refresh`: the three show a dollar figure;
  - the existing checks on `cost --explain` (`0 compaction calls … $0.00`) still pass: a
    measured zero stays a number.
- The Verifier's before/after: `chantier status` and the batch's `STATUS.md` on a fresh batch,
  before (on the base: `spent $0.00`) and after (`spent unknown`); for the cards, the diff of
  `worker.md`, `driver.md`, `pr-template.md`, `concepts.md` and `status-layout.md` is the proof
  (no visual change).
- A grep of the cards for each new rule: the Inspector's `"head"` field, `Head:` in `verify.md`,
  the delta assessment, `STALE`, `UNVERIFIED`, the SHA in each Test plan item, the screenshot
  check, the CI bullet's "one long wait", the unknown-never-0 bullet.

## Open questions

1. **The budget rail on an unknown spend.** Before the first priced refresh, the spend is
   unknown; today the rail reads it as 0 and lets a Driver start. Keep that (the specification's
   default), or refuse a start on a budgeted batch until its spend is priced once?
2. **Recording what wakes a waiting Driver.** The request said the Driver "records what wakes
   it"; the grill's answer ("just the card") and the restatement do not repeat it. Leave it out
   (the specification's default: the existing "say what CI showed in a `note`" stays), or add a
   `note` of what ended the wait?
