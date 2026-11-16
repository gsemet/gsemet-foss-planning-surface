# Change Specification: CR-248 "ready locally", "PR in draft" and "ready to merge"

## Goal

The user (2026-11-14), reading the `ready` asks of batch-17's stack while each of those PRs was
still a draft on the CR under it: "Il faut revoir le vocabulaire: "prêt" alors que la PR est en
draft." The user reads "ready" as "I can merge it". Later, reading "draft and mergeable" in a
report: "Si une PR est mergeable elle ne peut pas être en draft, c'est donc que quelque chose ne
va pas."

Today one word, `ready`, covers every CR whose work is done and proven (long gate, CI green,
Verifier `VERIFIED`), whether its PR is a draft (on an unmerged CR) or open on the default branch,
and one icon, 🔵 ("to review" in `status-layout.md`), marks it. After this CR, every place the
user or an agent reads a CR's readiness says one of three states (decisions 8 to 12):

- **ready locally** ("prête localement"), 🟣: the work is done and proven, and there is no PR yet
  (rare: in today's flow the PR is opened before the long gate);
- **PR in draft** ("PR en draft"), 🟤: the PR is open, a draft, and waits for what is under it;
- **ready to merge** ("prête à merger"), 🟢 (green, the "go" light): the PR is out of draft on the
  forge and the user can merge it, everything under it being ready to merge too.

✅ stays merged (decision 13), distinct from 🟢 by its shape; the other icons keep their meaning
(decision 14). 🔵 marks no state any more (decision 12). The forge's word "mergeable" (no
conflict) is never said to the user of a draft PR.

## Decisions carried (`02-answers.md`)

| # | Decision | Where in this spec |
| --- | --- | --- |
| 1 | The words: **ready locally** and **ready to merge** (PR out of draft, mergeable now). Rejected: verified/mergeable, done/ready to merge, stacked/mergeable. Replaced by 8 where they differ (ready locally) | Words; every area |
| 2 | Everywhere, one vocabulary: what the Chief of Staff tells the user, the Foreman's asks, the STATUS tables, the board and the CLI's output. Rejected: the user-facing text only | Areas 2 to 7 |
| 3 | A stacked PR turns ready to merge when every PR under it is ready to merge too; the top of the stack ready to merge means the whole stack is mergeable. Rejected: when its PR is out of draft on the forge, whatever is under it | Words; Area 1 |
| 4 | Grilled enough; specified, then P2 at the end of batch-17's stack | "Order in batch-17" |
| 5 | The stack's own words renamed too: `stack-ready` becomes `stack-ready-to-merge`, `forge-stack`'s `stack #N ready:` becomes `stack #N ready to merge:`, `concepts.md`'s **Stack ready** becomes **Stack ready to merge**. Rejected: keeping them | Areas 2, 4, 6 |
| 6 | 🟣 for ready locally; 🟠 stays queued (a CR that waits). Its "🔵 stays ready to merge" is replaced by 12 (🟢) | Areas 3, 5 |
| 7 | Board, pane and status aligned: the web board (CR-222 and the views of CR-225 to CR-228, as they stand below this CR), the Claude Code pane (`hooks/register.tsx`) and the STATUS files and `status` output show the same words and icons, none on `ready` alone; the PR shows each one side by side. Its icons as amended by 10 and 12: 🟣 ready locally, 🟢 ready to merge, 🟠 waits | Area 3; Evidence |
| 8 | Three states, not two: **ready locally** (done and proven, no PR yet), **PR in draft** (PR open, waits for what is under it), **ready to merge** (out of draft, the user can merge it, everything under it ready to merge; its icon 🟢 by 12). 🟠 stays waits. The forge's "mergeable" is never said to the user of a draft PR | Words; every area |
| 9 | Today's flow stays (the PR opened before the long gate; `handback ready` needs one). Rejected: opening the PR only when the CR joins the stack. 🟣 ready locally stays in the vocabulary and is rare | Words; Area 1 |
| 10 | 🟤 for PR in draft (⚪ already marks not started or dropped); replaces answer 8's ⚪ | Areas 3, 5 |
| 11 | Ready to merge follows the forge: shown (🟢 by 12) only once the PR is really out of draft on the forge, never ahead of it; the CLI records the forge's draft state. Answer 3's rule holds as well. Rejected: deriving it from answer 3 alone | "How the record holds it"; Areas 1, 2 |
| 12 | 🟢 (green) for ready to merge, replacing 🔵: the "go" light. 🔵 no longer marks any state. Rejected: keeping 🔵 | Goal; Areas 3, 5, 7; "Where 🔵 is today"; Evidence |
| 13 | ✅ stays merged: the checked square means done, the green dot means go. Rejected: 🏁 | Areas 3, 5 |
| 14 | The other icons unchanged: ⚪ not started or dropped, 🟡 working, 🟠 waiting for a named thing on its way, 🔴 blocked, 🟣 ready locally, 🟤 PR in draft. Rejected: changing one | Areas 3, 5; Out of scope |
| 15 | The icon beside a PR or a CR is always its current state, as `label` gives it; what it will become is said in words, never with an icon | Areas 4, 5; Evidence |
| 16 | Every PR in draft named to the user says "do not merge" ("ne pas merger") and what blocks it (its base, what it waits for) | Areas 4, 5; Evidence |
| 17 | "You can merge it" is said only of a PR ready to merge (🟢); never "mergeable" or "ready" of a draft | Area 5; Evidence |
| 18 | A draft's icon is its CR's state from the refreshed `STATUS.md`, never "draft" by default: 🟤 only when the CR has nothing left to do; a draft whose CR is rebasing or running CI or a Verifier is 🟡, waiting for another CR's work (not its merge) 🟠, blocked 🔴 | Areas 4, 5; Evidence |

## Words used below

- **Ready (the status):** the CR's status value `ready` in `batch.json`, unchanged: a Driver
  handed it back ready (`handback <cr> ready <link>`). It is a stored token, read by the rails,
  the eval kit and old records; no person reads it alone any more.
- **The recorded draft:** the CR's new field `pr_draft`, whether its PR is a draft on the forge,
  as the agent that opened it or turned it ready or back to draft recorded it.
- **Ready to merge:** a CR whose status is `ready`, with a PR recorded whose `pr_draft` is false
  (decision 11), and:
  - outside a stack batch, its PR's base is the default branch;
  - in a stack batch, every CR under it in the stack (`chain()`) is ready to merge too
    (decision 3), the bottom one standing on the default branch.
- **PR in draft:** a CR whose status is `ready`, with a PR recorded, that is not ready to merge:
  its PR waits for what is under it (a CR below in the stack, the dependency it is based on, or,
  for a prepared release, the top it sits on) or for its turn out of draft.
- **Ready locally:** a CR whose status is `ready` and with no PR recorded. Today's rails do not
  produce it (`ready means a PR recorded`, decision 9): the word and its icon stay in the
  vocabulary for a rare case.
- A CR not `ready` keeps its state as today (a working CR with a draft PR is 🟡 working).
- The three words are **derived** by the CLI from the record; none is a status of its own.
- **Mergeable**, in what the user reads, names only PRs ready to merge (as CR-244's **mergeable
  part** does); never a draft, whatever the forge's own `mergeable` field says.
- **The icons** (decisions 6, 10, 12 to 14): ⚪ not started or dropped · 🟡 working · 🟠 waiting ·
  🟣 ready locally · 🟤 PR in draft · 🟢 ready to merge · 🔴 blocked · ✅ merged. 🔵 is none of
  them.

## How the record holds it (the choice, and why)

**The status `ready` stays as it is; one field, `pr_draft`, records the forge's draft state; the
three words are derived from the record.**

Why not rename the status (`ready` into three statuses):

- `ready` is a lifecycle state the CLI's refusals read in many places (`rails.py`: `take`'s
  rule, the waits of a release and of a stack or series, `closing.py`'s `pause` refusal,
  `rails_release.py`, `orders_apply.py`, `lifecycle/convert.py`, `driver_checks.py`), and so do
  the eval kit (`evals/kit/audit.py`: `status in ("ready", "merged")`, `result == "ready"`) and
  every old `batch.json`, `events.jsonl` and `STATUS.json`. A rename would touch every one of
  them and need a migration of old records, for no change in behaviour: the three states share
  every rule but the user's merge.
- The word changes with no act of the CR's own Driver: a stacked CR turns ready to merge when the
  CRs under it do and the stack driver turns its PR ready. A status written at hand-back would go
  stale.

Why a recorded draft (decision 11): the word must never lead the forge. Answer 3 alone would
read a stacked CR ready to merge as soon as everything under it is `ready`, one stack-driver take
before its PR leaves draft. So the CLI holds what the forge holds, written by whoever changes it:

- **`pr_draft: bool | None`** on `CrEntry` (`core/records.py`), `None` when nothing recorded it.
- **`ship <cr> <pr> [--draft]`**: the Driver records its PR with its draft state (`--draft` when
  it opened or left it a draft). A Driver that turns its PR ready (the hand-back on the default
  branch, `driver.md`) runs `ship <cr> <pr>` again after `gh pr ready` / `glab mr update
  --ready`, before `handback`; one that turns it back to a draft ships again with `--draft`.
- **`stack --out-of-draft <cr>…` / `stack --draft <cr>…`** (`commands/delivery.py`): the stack
  driver (CR-244, CR-245, CR-246) records the PRs it turned ready, right after the forge command,
  and those it turned back to a draft (CR-246's drop, an insertion into a stack). `--out-of-draft`
  is refused (exit 2, nothing written) for a CR not `ready` (`only a CR handed back ready leaves
  draft`) and for a CR with a draft under it (`under it is a draft: <cr>`), the same rule as
  CR-244's check 4 (`a draft under a ready PR`). Each prints `<cr> ready to merge` / `<cr> PR in
  draft` per CR named and logs one event.
- **`forge-stack show`** (CR-244's check 4) also names a PR whose recorded draft differs from the
  forge's (`check 4: recorded <draft|out of draft> #n, the forge says <…>`), so a record that
  drifted is caught where the forge is already read.

Old records stay readable: `pr_draft` is optional with `None` as default (no migration, no schema
break). `None` reads as a draft, so a CR from before this CR shows **PR in draft** until a `ship`
or `stack --out-of-draft` records otherwise: never ahead of the forge.

## What changes

The CLI (the recorded draft, the derived word, the icons, the views, the printed lines), the pane
(`hooks/register.tsx`), its test (`hooks/register.test.tsx`) and its row type
(`types/index.d.ts`), the cards, the docs, one agent file on both hosts, the scenario. The
`hooks/` and `types/` change passes `just mod` before the PR (`AGENTS.md`); a Driver that cannot
run it stops and says so. No version edit, no CI job.

### Area 1: the recorded draft and the derived word (`core/records.py`, `commands/delivery.py`, `status/words.py`, `commands/facts.py`)

- **`pr_draft`**, `ship --draft`, `stack --out-of-draft` / `--draft`: as in "How the record
  holds it".
- **`ready_word(d, c, default_branch) -> str | None`**, one function, the only place the rule
  lives: `None` unless `c.status == "ready"`; `"ready locally"` when `c.pr` is empty; `"ready to
  merge"` when `c.pr_draft is False` and, in a stack batch, every CR of `chain()` under `c` is
  ready to merge, in any other batch its PR's base (`stack_base(d, c, repo)`) is the default
  branch; else `"PR in draft"`. A prepared release (its PR a draft on the top) is `"PR in
  draft"`. Where it sits is the Driver's choice within the layers (`status/` may not import
  `commands/`: move `chain()`/`stack_base()` down to a layer both read, or give `status/` what it
  needs).
- `handback <cr> ready <link>` keeps its input and its rail (`ready means a PR recorded`,
  decision 9): `ready` is the Driver's word that the work is done; the CLI says which state it is.

### Area 2: the CLI's output

Every line the CLI prints about a CR's readiness says the derived word; `ready` alone names no
state any more:

- `handback`: the line to send becomes `[driver <cr>→foreman] hand-back ready to merge <note>`
  or `hand-back PR in draft <note>` (`hand-back ready to merge, no long gate: <reason> <note>`
  and `hand-back PR in draft, no long gate: <reason> <note>` with `--no-gate`); the last line
  `<cr> ready to merge` or `<cr> PR in draft: it waits on <base>`; for a prepared release,
  `<cr> PR in draft: the release PR <pr> waits on <base>` (or `<cr> ready to merge: the release
  PR <pr> waits for its merge` when it is out of draft on the default branch). The cards that
  match the prefix `hand-back ready` match these forms instead.
- `ship`: `recorded <pr> (base <base>, head <sha7>, draft)` or `(…, out of draft)`.
- `status` (`commands/batch_status.py`, `_cr_row`): the state after the CR id is the word
  (`CR-3 ready to merge r1/3 <pr> …`, `CR-4 PR in draft r1/3 <pr> …`).
- `handoff` (`commands/facts.py`, `cr_facts`, first line) and `take stack` / `stack`
  (`stack_lines`, one row per CR): the word in place of `ready`.
- The texts that name the status as a condition say so plainly: `opening.py` (lines 177 and
  334), `orders_release.py` (line 51) and `rails.py`'s waits (lines 230-232): "once every other
  CR is ready (stack, series)" becomes "once every other CR is handed back ready (stack,
  series)"; "ready or merged" becomes "handed back ready or merged".
- `forge-stack` (as CR-244 and CR-245 leave it): the status it prints for a CR (`check 4: not a
  draft #n (<cr> <status>)`, the `to come: <cr> <status>…` line) uses the word for a ready CR
  (`PR in draft` for a draft on top); the recorded-draft line of "How the record holds it". Its
  success line `stack #N ready: …` becomes `stack #N ready to merge: …` (decision 5), the rest of
  the line as CR-244 writes it (`stack complete, mergeable below …` or `partial stack mergeable
  below …`, which names the PRs ready to merge only); on GitLab (CR-245) `chain <top MR link>
  ready:` becomes `chain <top MR link> ready to merge:`. The help of `forge-stack` says "ready to
  merge" where it says the stack is ready.

### Area 3: STATUS files, the board and the pane (decisions 7, 12 to 14)

One source for all of them: `label` and `readiness`, written by `status` in `STATUS.json`. The
board, the pane, `STATUS.md` and `status` show the same word with the same icon for every CR.

- **`icon`** (`status/words.py`, line 73 today: `"ready": "🔵"`): a ready CR's icon follows its
  derived word: 🟢 ready to merge, 🟤 PR in draft, 🟣 ready locally. `"🔵"` leaves the function
  and the CLI entirely (decision 12). ✅ merged, 🟡 working, ⚪ queued with a free slot or
  dropped, 🟠 and 🔴 as today (decisions 13, 14).
- **`label`** (`status/words.py`): a ready CR reads `🟢 ready to merge Notify 1/3`, `🟤 PR in
  draft, waits for <what is under it>` (the CR below, the dependency, the top, or its turn out of
  draft, in the `waits for` form a queued CR already has) or `🟣 ready locally Notify 1/3`. 🟣,
  🟤 and 🟢 are new; 🟠 keeps its meaning (a CR that waits for a thing on its way); ⚪ stays not
  started or dropped. `severity` stays `green` for the three.
- **`STATUS.json`** (`cr_view`, `_row`): `state` stays the status value (`ready`); one added
  field `readiness`: `"ready locally"`, `"PR in draft"`, `"ready to merge"` or `null`. Additive:
  `SCHEMA` stays 3.
- **`_now_next`**, the row of a ready CR: ready to merge, `Ready to merge: <pr> waits for the
  user's merge.` / `The merge, then the archive.`; PR in draft, `PR in draft: <pr> on <base>,
  waits for <what>.` / `Ready to merge once what is under it is and the PR is out of draft.`;
  ready locally, `Ready locally: no PR yet.` / `Its PR.`
- **`STATUS.md`** follows the label and the lines above (it renders them).
- **The board** (`chantier board`, CR-222 and the views CR-225 to CR-228 add, as they stand
  below this CR): wherever it shows a CR's state (tables, stack view, any card or filter it
  holds), it shows `label`, the same icon and word, never `ready` alone and never 🔵; a filter or
  group of ready CRs groups by the three words. If any of those views draws an icon or a colour
  of its own for a ready CR (rather than copying `label`), it draws 🟢 / green for ready to merge.
- **The pane** (`hooks/register.tsx`, `types/index.d.ts`): it draws `label` as today, so the
  words and icons follow (🟢 in place of 🔵). `ChantierRow` gains `readiness: string | null`.
  `isWaiting` (line 115) puts a ready CR in "Waiting for you" only when `readiness` is `"ready to
  merge"`; a PR in draft or a CR ready locally waits for nothing of the user's and goes in "In
  progress" (decision 8: a draft waits for what is under it). `hooks/register.test.tsx` (line 567,
  `'🔵 ready Notify 1/3'`) expects `'🟢 ready to merge Notify 1/3'`, with rows for `🟤 PR in
  draft…` and `🟣 ready locally…` beside it. `just mod` passes.
- **The screenshot** (still required): what the pane draws changes (its words and the 🟢 icon),
  so the PR's Deliverables carry one screenshot of the pane from a real Claude Code session at the
  PR's head, captioned with the head's SHA (seven characters); until then its Known gaps say "no
  screenshot of the pane from a real session" (`AGENTS.md`), and the Chief of Staff asks the user
  for one. Beside it (decision 7), the same batch's CRs on the web board, in `STATUS.md` and in
  `status`'s output, so the three states and their icons read the same in each.

### Area 4: the asks (`foreman.md`)

- The ask of a ready CR (`foreman.md` lines 44-56 and the line list at 189-191) is written with
  the word the CLI printed at the hand-back: `ready-to-merge <cr> <link> [gaps: …]` or
  `pr-in-draft <cr> <link> on <base>: waits for <what> [gaps: …]`; the `no long gate:` form
  likewise. The rest of each rule (gaps kept as written, the long-gate check) is unchanged.
- The stack's ask: `stack-ready` becomes `stack-ready-to-merge` (decision 5) in both forms CR-244
  gives it (`stack-ready-to-merge <stack link> partial stack mergeable below <sha7> <cr>=<link>…
  to come: …` and `stack-ready-to-merge <stack link> mergeable below <sha7> <cr>=<link>…`), in the
  `asks` line list and wherever a card names it (`chief-of-staff.md`, `driver.md`, and the
  mentions CR-245 and CR-246 add).
- Every other mention of a ready CR, PR or hand-back in `foreman.md` says which state it means
  (for instance CR-244's "a CR of the stack handed back `ready` (decision 10): no ask" becomes
  "handed back, ready to merge or PR in draft").
- An ask never calls a draft PR mergeable, whatever the forge's `mergeable` field says.
- An ask's icon, when it carries one, is the CR's state at the ask (decision 15): a `pr-in-draft`
  ask is 🟤, never 🟢 for the state it will reach. The `pr-in-draft` ask names what blocks the
  merge (its base), so the Chief of Staff can relay "do not merge" (decision 16).

### Area 5: the Chief of Staff (`chief-of-staff.md`, `status-layout.md`)

- **To the user**, in the user's language: "ready to merge" / "prête à merger" only for a PR the
  user can merge now; "PR in draft" / "PR en draft" for a draft, with what it waits for; "ready
  locally" / "prête localement" for done work with no PR yet. "Ready" / "prête" alone is never
  said of a CR or a PR, and "mergeable" never of a draft (decision 8). When the Chief of Staff
  writes an icon beside a CR, it copies it from `label` (🟢 for ready to merge), never 🔵.
- **The icon is the present** (decision 15): the icon beside a PR or a CR is its state at the
  time of writing, never the state it is expected to reach; the future is said in words. Wrong:
  "the next PR ready to merge will be 🟢 #171 CR-237" while #171 is a draft. Right: "🟤 #171
  CR-237, do not merge: it waits for its gate; it will be the next ready to merge".
- **A draft says "do not merge"** (decision 16): every PR in draft the Chief of Staff names to
  the user carries, in the user's language, "do not merge" / "ne pas merger" and what blocks it:
  "🟤 #174 CR-222: ne pas merger, base = branche de CR-237". A PR in draft based on another CR's
  branch is never called "prête", even of its own work: merging it lands it in that branch, not
  in the default branch.
- **"You can merge it"** (decision 17) / "tu peux la merger": only for a PR ready to merge (🟢:
  out of draft, CI green, no conflict, on the default branch or with everything under it ready to
  merge).
- **"A plain `ready <cr> <link> gaps: …` ask"** (line 538, as CR-233 left it) becomes the
  `ready-to-merge` ask (offered as mergeable now) and the `pr-in-draft` ask (what it waits for,
  not offered to merge). CR-233's rule "you can merge only after its `ready` line" reads "only
  after its `ready-to-merge` line (or the `stack-ready-to-merge` line for a stack)".
- **`status-layout.md`**: the icons (lines 23-24, today `… 🔵 to review, 🔴 blocked, ✅ merged`,
  and the legend at line 38, today `⚪ not started · 🟡 working · 🟠 waiting · 🔵 to review · 🔴
  blocked · ✅ merged`) become `⚪ not started or dropped · 🟡 working · 🟠 waiting · 🟣 ready
  locally · 🟤 PR in draft · 🟢 ready to merge · 🔴 blocked · ✅ merged` (decisions 6, 10, 12 to
  14), each icon copied from `label` as today; line 83 (today "🔵 to review is a ready PR only
  …") becomes "🟢 ready to merge is a PR out of draft whose CR is ready to merge; a PR in draft is
  🟤 and says what it waits for; **For you** asks the user to merge only a PR ready to merge";
  line 32 ("On a CR ready or merged") and line 95 ("On the Foreman's `ready` that is the last of
  a stack") name the words. The words "to review" leave the legend: the state is "ready to merge".
- In direct mode the same, the Chief of Staff steering.

### Area 6: the other cards (`driver.md`, `concepts.md`, `routing.md`, `init.md`, `worker.md`, `griller.md`, `hosts/*.md`)

- **`concepts.md`, Words:** **Ready to merge** (lines 9-16, as CR-233, CR-244, CR-245 and
  CR-246 leave it) is restated from "Words used below", decisions 3 and 11 included (out of draft
  on the forge; the top of a stack ready to merge means the whole stack is mergeable); new words
  **PR in draft** and **Ready locally** beside it. The status `ready` is named as the stored
  token the three come from, and "mergeable" as said of PRs ready to merge only. CR-244's
  **mergeable part** is "the CRs of the stack ready to merge, from the bottom"; **drafts on top**
  "the CRs above it (PR in draft, or not ready)". **Stack ready** (as CR-244 words it) becomes
  **Stack ready to merge** (decision 5), its five checks unchanged. Where a card gives an icon
  for one of these words, it is the icon of "Words used below" (🟢 ready to merge).
- **`driver.md`:** `ship` with `--draft` while its PR is a draft; the hand-back (lines 247-267):
  on the default branch, turn the PR ready, `ship` again without `--draft`, then `handback`; the
  CLI prints which state the CR is. The stack driver ("Stack driver", as CR-244, CR-245 and
  CR-246 leave it) runs `$CHANTIER stack --out-of-draft <cr>…` right after it turns PRs of the
  mergeable part ready, and `$CHANTIER stack --draft <cr>…` right after it turns any back to a
  draft (CR-246's drop, an insertion into a stack); its other mentions of a ready PR or CR say
  which word.
- Every other card's mention of a ready CR or PR says which word. Untouched: the `3-ready`
  stage and `triage --ready`, `handback <cr> ready` as typed, the forge commands (`gh pr ready`,
  `glab mr update --ready`), and "ready" in other senses (a worktree, a file, a grill).

### Area 7: the docs and the agent files

- `README.md`, `docs/*.md` (use cases, boards, gates, planning folder, tutorial, the
  `*-texts.md` of the diagrams) and the SVGs whose text names a CR's or PR's state as `ready`
  (`docs/batch-modes.svg`, `cr-lifecycle.svg`, `cr-lifecycle-simple.svg`,
  `cr-folder-lifecycle.svg`, `release-driver.svg`, `how-chantier-works.svg`, `batch-pace.svg`):
  the three words, each SVG kept in line with its `-texts.md`. Where a doc or an SVG gives the
  icon of a state, it is the icon of "Words used below" (🟢 ready to merge, never 🔵); none does
  today (see "Where 🔵 is today"). `CONTRIBUTING.md` likewise. The board's docs and screenshots
  (CR-228, as it stands below this CR) show the new labels and icons.
- `agents/demo-explorer.md` and `com.github.copilot/agents/chantier-demo-explorer.agent.md`:
  "Studies a ready stack" becomes "Studies a stack ready to merge", both bodies kept identical.
- Not edited (records of what was): `docs/release-notes/`, `evals/results/`,
  `scenario/results/`, the archives.

## Where 🔵 is today (decision 12)

`rg -n "🔵" skills hooks docs README.md scenario tests CONTRIBUTING.md agents com.github.copilot`
on the main checkout (2026-11-14, at `ff701a9`) finds 🔵 in these places, each meaning a ready CR
("to review" / "ready"); each changes:

| File | Line today | Becomes |
| --- | --- | --- |
| `skills/chantier/scripts/cli/src/chantier/status/words.py` | 73, `icon`: `"ready": "🔵"` | the icon of the derived word (🟢 / 🟤 / 🟣), Area 3 |
| `skills/chantier/references/status-layout.md` | 24, `🔵 to review, 🔴 blocked, ✅ merged` | the full icon list of Area 5 |
| `skills/chantier/references/status-layout.md` | 38, the legend `… · 🔵 to review · …` | the legend of Area 5 |
| `skills/chantier/references/status-layout.md` | 83, `🔵 to review is a ready PR only …` | `🟢 ready to merge is a PR out of draft …`, Area 5 |
| `hooks/register.test.tsx` | 567, `'🔵 ready Notify 1/3'` | `'🟢 ready to merge Notify 1/3'` and the two other rows, Area 3 |
| `scenario/run_scenario.py` | 1735, `"🔵 ready Notify 1/3" in board and … in batch` | `🟢 ready to merge Notify 1/3` (or the draft label the step's CR really has), Evidence |
| `scenario/run_scenario.py` | 4919, `icon_is(w, c1, "🔵", "a ready CR")` | `icon_is(w, c1, "🟢", "a CR ready to merge")` after a ship out of draft, and a 🟤 check for a draft, Evidence |

None today in `README.md`, `docs/` (its SVGs' blue strokes and `arrow-blue` markers are arrows,
not a state, and stay), `tests/`, `CONTRIBUTING.md` or the agent files. The planning folder holds
🔵 only in records (the CR-225 QA prototype's `data.js` copies old `label`s; CR-223's evidence); records are not edited. CR-252's specification draws 🟢 (its answer 10).

## What this CR changes on top of CR-233, CR-244, CR-245 and CR-246

All four are kept in behaviour; this CR changes their words and adds the recorded draft.

- **CR-233 (merge-any-time):** its "a PR whose CR was handed back `ready` and whose base is the
  default branch" is a CR ready to merge (its PR recorded out of draft); its "`ready … draft on
  <base>: waits for <cr>` ask" is the `pr-in-draft` ask; "you can merge only after the `ready`
  line" names the `ready-to-merge` line.
- **CR-244 (stack-grows-from-bottom):** its **mergeable part** ("from the bottom while each is
  `ready` and its PR not a draft") is the CRs ready to merge, now named by the CLI from the
  record (`ready_word`, decisions 3 and 11); its stack driver records with `stack --out-of-draft`
  each PR it turns ready and with `stack --draft` each it turns back. Its check 4 also compares
  the recorded draft with the forge's. **Drafts on top** are the CRs with a PR in draft or not
  ready; **to come** (no PR yet) keeps its word. The status its checks print for a ready CR is
  the word. Its `stack-ready` ask becomes `stack-ready-to-merge`, its `forge-stack` line `stack
  #N ready to merge:`, its **Stack ready** **Stack ready to merge** (decision 5). Its partial
  stack line ("partial stack mergeable below <sha7>") is unchanged: it is decision 8 of CR-244 in
  the user's words and names only PRs ready to merge.
- **CR-245 (gitlab-stack-delivery):** the same words on GitLab ("the ready MRs below" becomes
  "the MRs ready to merge below"; `chain <top MR link> ready to merge:`); `stack --out-of-draft`
  follows `glab mr update --ready` as it follows `gh pr ready`.
- **CR-246 (stack-robustness):** after its drop's "turn every PR above the dropped one back to a
  draft first", the stack driver records `stack --draft <cr>…`; its Chief of Staff bullet ("the
  PRs above it are drafts, not mergeable") says they are PRs in draft until the next report shows
  them ready to merge again; its `stack-ready` mentions become `stack-ready-to-merge`.

## Out of scope

- Renaming the status value `ready`, the `handback <cr> ready` argument, the `3-ready` stage or
  `triage --ready`.
- Lifting the rail `ready means a PR recorded`, or opening the PR later (decision 9).
- Reading the forge to derive the word (the STATUS files never call the forge); `forge-stack
  show` stays the forge check.
- Any icon change beyond 🟣 for ready locally, 🟤 for PR in draft and 🟢 for ready to merge in
  place of 🔵 (decisions 12 to 14): ✅, ⚪, 🟡, 🟠 and 🔴 keep their meaning.
- The blue colour of arrows and markers in the docs' SVGs (not a state).
- CR-252's own specification: amended on its own to 🟢 ready to merge (its answer 10); this CR does not edit it.
- Any change to who merges, when a stack is made, or the checks beyond check 4's recorded-draft
  line.
- Historical records (release notes, eval and scenario results, archives).

## Order in batch-17

P2, at the end of batch-17's stack (decision 4), above CR-233 (`4-batch/2-actives/233-merge-any-time`),
CR-244 (`4-batch/2-actives/244-stack-grows-from-bottom`), CR-245
(`4-batch/1-pending/245-gitlab-stack-delivery`) and CR-246 (`4-batch/1-pending/246-stack-robustness`),
and written against their merged text (the same card paragraphs, `forge_stack.py`'s printed
lines, `stack` in `delivery.py`). It also reads the board as CR-222 and CR-225 to CR-228 leave
it, whichever of them stand below it (decision 7). Sharing files is no reason for
`depends.json`; its place at the top of the stack is enough. Its card changes reach a running
batch only once merged into the main checkout and reloaded; its pane change once merged and
reloaded too.

## Evidence

**Checks:** `just check` passes (Linux, macOS, Windows), `just lint` within it (each function
under fifty lines; the rule in one function). `just mod` passes (`hooks/`, `types/`), with
`hooks/register.test.tsx` expecting the 🟢, 🟤 and 🟣 labels.

**Scenario** (`just scenario`, both forges; the CLI and cards change), in
`scenario/run_scenario.py` and its `README.md` list; the existing checks that read a printed
`<cr> ready` line, `stack-ready`, `stack #N ready:` or a 🔵 label (lines 1735 and 4919 today)
expect the new words and icons:

1. Parallel batch, a CR on the default branch: `ship <cr> <link>` (no `--draft`) then `handback
   <cr> ready <link>` prints `hand-back ready to merge` and `<cr> ready to merge`; its
   `STATUS.json` has `state: "ready"`, `readiness: "ready to merge"`, `label` starting `🟢 ready
   to merge`; `status` shows `ready to merge`. The same CR shipped with `--draft`: `PR in draft`,
   🟤.
2. Parallel batch, a CR `after` an open CR, its PR shipped `--draft` on that branch: `handback …
   draft on <base>: waits for <cr>` prints `PR in draft`; `readiness: "PR in draft"`, `label`
   starts `🟤 PR in draft, waits for <cr>`.
3. Stack batch, `a` (bottom), `b`, `c`, each shipped `--draft`, all handed back ready: all read
   PR in draft (none out of draft yet: never ahead of the forge); `stack --out-of-draft c` is
   refused naming `b`, nothing written; `stack --out-of-draft a b c` passes, all ready to merge
   (🟢); `take b --note …` (back to working): `c` reads PR in draft; `stack --draft c` records it
   back; `stack --out-of-draft` on a working CR is refused.
4. A prepared release (`handback <r> ready <link> draft on <top>: waits for the merge`): PR in
   draft, `the release PR … waits on <top>`.
5. An old record (a `batch.json` with ready CRs and no `pr_draft`) reads with no error; its ready
   CRs read PR in draft (🟤).
6. `handoff` and `stack` rows print the word; `forge-stack show` prints `stack #N ready to merge:`
   and, in its `to come:` line, `PR in draft` for a ready draft (with CR-244's steps); a CR
   recorded out of draft whose PR is a draft on the fake forge gives the check 4 recorded-draft
   line.
7. A `ready` CR with no `pr` in a hand-edited record: `readiness: "ready locally"`, `label`
   starts `🟣 ready locally`.
8. The icon step (line 4919 today): a CR shipped out of draft and handed back ready gives
   `icon_is(…, "🟢", "a CR ready to merge")`; merged, `✅`; no `STATUS.json` of the scenario holds
   🔵.

**Reading pass**, in the PR's Test plan: `rg -n -w "ready" skills/chantier/references README.md
docs CONTRIBUTING.md --glob "!docs/release-notes/**"` leaves only the stored token
(`handback <cr> ready`, the status `ready`), the forge commands, `3-ready`/`triage --ready`, and
other senses, each read by eye; `rg -n -i "mergeable"` on the same paths finds it only of PRs
ready to merge; `rg -n "stack-ready |stack-ready\`|Stack ready\*\*" skills/chantier/references`
finds none; `rg -n "🔵" skills hooks docs README.md scenario tests CONTRIBUTING.md agents
com.github.copilot --glob "!docs/release-notes/**" --glob "!scenario/results/**"` finds none;
`rg -n "to review" skills/chantier/references/status-layout.md` no longer finds the legend's
state; `chief-of-staff.md` gives the French words "prête localement", "PR en draft" and "prête à
merger"; `status-layout.md` names 🟣 ready locally, 🟤 PR in draft and 🟢 ready to merge;
`chief-of-staff.md` states decisions 15 to 17 (the icon is the present state, the future in
words; a draft named to the user says "ne pas merger" with its base; "tu peux la merger" only of
🟢), with the wrong and right examples of Area 5; the two
agent files' bodies are identical.

**Side by side** (decision 7), in the PR's Deliverables: the pane screenshot of Area 3 (or the
Known gaps line), the web board, `STATUS.md` and `status`'s output for one batch holding a CR in
each state shown (at least PR in draft 🟤 and ready to merge 🟢), the same word and icon in each.

No CI job is added or changed.

## Self-containment for the Driver

Files: `skills/chantier/scripts/cli/src/chantier/core/records.py` (`CrEntry`),
`commands/delivery.py` (`ship`, `stack`, `register`), `commands/driver.py` (`handback`'s lines),
`commands/facts.py` (`cr_facts`, `stack_lines`, and `chain`/`stack_base` if moved),
`commands/batch_status.py` (`_cr_row`), `commands/forge_stack.py` (the printed lines, check 4,
the help), `commands/opening.py`, `commands/orders_release.py`, `rails.py` (texts only),
`status/words.py` (`label`, `icon`, `ready_word`), `status/views.py` (`_now_next`, `cr_view`,
`_row`), `board/` (`render.py` and the views CR-222 and CR-225 to CR-228 leave);
`hooks/register.tsx` (`isWaiting`), `hooks/register.test.tsx` (the labels), `types/index.d.ts`
(`ChantierRow`); `skills/chantier/references/*.md`; `README.md`, `docs/`, `CONTRIBUTING.md`;
`agents/demo-explorer.md`, `com.github.copilot/agents/chantier-demo-explorer.agent.md`;
`scenario/run_scenario.py`, `scenario/README.md`, `scenario/fake_gh.py` (and its GitLab twin)
for the drafts. Read the specifications of CR-233, CR-244, CR-245, CR-246 and CR-222, CR-225 to
CR-228 (folders above) and work on their merged text.

## Open questions

None. (CR-252 follows the 🟢: recorded as its answer 10, its specification amended.)
