# A clear batch lifecycle, ending in a pause

## Goal

In the user's words: "tu mets le batch en pause quand tout est fini", and "quand un batch est
complet, il est mis en pause. Et les coûts sont quand même affichés". When every CR of a batch is
merged or cancelled, the steering session removes the merged CRs' worktrees and branches, then
**pauses** the batch with `chantier pause`: it is not closed. At the pause the full cost to date
is computed and shown. A paused batch takes new CRs, which set it **running** again. A batch is
closed only on the user's own word ("close the batch"). This is the same in Foreman mode and in
direct mode.

A batch has three states, and only three words for them: **running**, **paused**, **closed**.
"landed", `land` and "open" as a state go away. "Pause" names only the batch state: the hold on
new Drivers (`order slots --note 0`) is called **hold**.

Today the cards contradict each other: `chief-of-staff.md`, "Steering a batch yourself", says in
"The pause" that a landed batch is paused and takes new CRs, but its "The end" goes straight to
the `close` flow, and the Completion report ends with "**For you:** closing the batch". The
landing's cost is marked "not final" and only `close` prints the cost. This CR states the
lifecycle once, in `concepts.md`, and makes every card, the CLI, the STATUS files, the board, the
docs and the scenario say the same thing.

## The lifecycle (the text to state once)

`concepts.md` gets one entry, **Batch lifecycle**, placed right after the **Batch** entry. Every
other card points to it and does not restate it. Its content:

1. **Running:** `open` creates the batch, running. Its CRs are taken by Drivers on the free
   slots, worked, handed back, merged by the user, or dropped.
2. **Complete:** every CR is merged or cancelled. The steering session (the Foreman, or the
   Chief of Staff in direct mode) removes each merged CR's worktree and branch, from the main
   checkout, as `foreman.md` says today. Then it runs `pause`, and the batch is **paused**.
3. **Paused:** nothing runs. The cost to date has been computed and shown. The batch is not
   closed (one batch at a time, so `open` still refuses a new batch). It takes new CRs:
   `order add` (or `order qa`) sets it running again, and it pauses again at the end with the
   cost to date, which has grown.
4. **Closed:** only on the user's word ("close the batch"): the `close` flow, as today (the check
   and the final cost from `close` without `--yes`, then `close --yes` on the user's yes in that
   turn). Until then, a paused batch stays paused, however long.

The same in both steerings. The one difference stays as it is: a *running* direct batch is
strict (`order add` and `order qa` refused, except a release CR); a *paused* batch, of either
steering, takes new CRs.

## What changes

### 1. The command: `pause` replaces `land`

The command `land` becomes `pause`; `land` goes away (no alias). Its behaviour is unchanged
except as section 3 says (it prints the cost to date). It still takes `--epoch` and `--batch`.

- `skills/chantier/scripts/cli/src/chantier/cli.py` line 151: `cmd("pause", commands.pause, …)`,
  `epoch=True`; help: "pause the batch once its work is done: refused while anything is live or
  already paused; prints the cost to date". `pause` is added to `FULL_OUTPUT` (section 3).
- `commands.py`: `land()` (line ~1514) is renamed `pause()`. The event it logs is `pause`
  (`b.log("pause", None)`, line ~1545), not `land`. Past `events.jsonl` records keep their `land`
  events: no code reads that kind (only the scenario's list of kinds, line ~743, which expects
  `pause`).
- Every message naming the command says `chantier pause`: `cancel()` (line ~1217, ~1511),
  `rails.py` `archive_merged()` (line 190), the `order()` reopen line, `_close_target()` /
  `close()` refusals, the docstrings of `close` (line ~1552), the cost window (line ~1629: "`pause`
  ends no window") and line ~1867.
- `evals/kit/audit.py`: `EPOCH_COMMANDS` (line 28) lists `pause` instead of `land`; the check
  message (line 194) "cancel and pause carries its epoch"; line 204 "before the pause".
- `CONTRIBUTING.md` line 20: the command list names `pause`.
- Every card, doc and runbook that names the command (sections 4 to 8) says `pause`.

### 2. The state words: running, paused, closed

`batch.json` records `status: "running"` (not `"open"`) or `status: "paused"` (not `"landed"`),
and the pause time under the key `paused` (not `landed`). A closed batch has no folder, as today.

CLI (`skills/chantier/scripts/cli/src/chantier/`):

- `commands.py`, `open_batch()` (line 496): creates `"status": "running"`.
- `commands.py`, `pause()`: writes `status="paused"`, `paused=<time>`, `summary=…` (line ~1544).
  The refusal on a second run: `<batch> is already paused (at <time>): \`order add\` sets it
  running again, then \`pause\` runs again`. The refusal while something runs:
  `cannot pause <batch>: live …`.
- `commands.py`, `order()` (lines ~844-858): the strict-direct refusal says "add the CR once the
  batch is paused (`pause`), or switch to Foreman mode"; the reopen sets `status = "running"`,
  clears `paused` (and `summary`, as today) and prints
  `<batch> was paused: running again; \`pause\` runs again at the end`.
- `commands.py`, `status()` (line ~951-957): the first line prints the state word (`running` or
  `paused`); the suffix ` (landed, cost not final)` becomes ` (paused, cost to date)`.
- `commands.py`, `_refresh()` (line ~923): the summary refreshed on a paused batch.
- `commands.py`, `_close_target()` and `close()` (lines ~1552-1566): "the only landed one"
  becomes "the only paused one"; the refusal on a running batch says
  `it is running, not paused; \`pause\` comes first. Nothing was deleted.` `close` itself is
  unchanged otherwise.
- `rails.py`, `check_no_open_batch()` (line 20-25): `<batch> is not closed (a paused batch stays
  until \`close\`): \`order add\` joins new work to it`; its docstring says the same.
- `state.py`: the comment "A batch is open or landed" (line ~98) names running and paused;
  `open_batches()` (line 246) and `find_cr_batch()` (line 400) test `"paused"`; their messages
  that mean the state say "running" ("no running batch holds <cr>", "several running batches");
  their behaviour is unchanged. The message "no open batch: run `chantier open` first" (line 371)
  says "no running batch".
- `lifecycle.py`, `ensure_unclaimed()` (line 85): tests `"paused"`.
- `status.py`, `batch_view()` (line 274): the key `landed` becomes `paused`; `state` carries
  `running` or `paused`. `batch_markdown()` (line 286-293): the title reads
  `# <folder>: running` or `# <folder>: paused`; the `## Landed` section becomes `## Paused` with
  `- Paused: <time>`.
- Any other test of `"open"` as a batch state in the CLI reads `"running"`.

**An old batch recorded `landed` or `open`.** The CLI reads a `batch.json` with
`status: "landed"` as paused and one with `status: "open"` as running, and rewrites it at its
next write (batch-08 in this repository is running when this CR merges). One helper in
`state.py`, used by every reader of a `batch.json` (`Batch.__enter__`, `read_batch`,
`open_batches`, `find_cr_batch`, `lifecycle.ensure_unclaimed`, `commands._close_target`,
`status.py` `dashboard_view`), maps `status: "landed"` to `"paused"` (moving the key `landed` to
`paused`) and `status: "open"` to `"running"`, with a comment saying why. A read-only command
does not write; the next write through `Batch` stores the new words. No other old word is
translated.

Board and types:

- `hooks/register.tsx` line 452: a live batch is `b.state === 'running'`; line 455: a **paused**
  batch is folded, its cost still on its title line (`b.state !== 'paused'`, comment "a paused
  batch is folded …").
- `hooks/register.test.tsx`: the fixture's `state: 'open'` (line 50) becomes `'running'`; the test
  at line 351 is named "a paused batch is folded, with its cost on its title line" and uses
  `state: 'paused'`.

### 3. The cost at the pause: computed and shown, to date

Today `land` records a summary marked `NOT_FINAL` ("Not final: it runs until `close`, which
prices the final cost") and prints only two lines. The user wants the full cost to date computed
and shown at the pause, the cost table by role and its explanation, as the final report shows
today; it grows if the batch runs again.

- `commands.py`, `NOT_FINAL` is replaced by a line that says the cost is to date, for example
  `To date: it grows if the batch runs again; \`close\` prices the final cost`. Every use of
  `NOT_FINAL` takes it.
- `pause()` prints, after its first line (`paused <batch>: cost to date below`) and the report
  path, the cost summary it already computes (`_cost_summary(...)`: total and budget, the split,
  the costliest CRs, the wakes, each Driver with its workers, the `Chief of Staff:` line, what is
  not counted), followed by the to-date line. `pause` is in `FULL_OUTPUT` in `cli.py`, and in the
  list of commands exempt from the ten-line limit in `concepts.md` ("Output is ten lines at most,
  except …").
- When the cost cannot be priced, the pause still happens, as today: the summary is
  `Spent: unknown (<cause>)`, printed too, never a false $0.00.
- `status.py`, `batch_markdown()`: the header's ` (not final)` becomes ` (to date)` on a paused
  batch; the `## Cost` section ends with the to-date line.
- `close` keeps the word "final": the final cost is the one `close` prints.

### 4. "Hold" for `order slots 0`; "Merged" for the archive list

So that "pause" names only the batch state:

- `commands.py` line 756: `order slots --note <n> (0 holds: no new Driver starts)`.
- `chief-of-staff.md` line 208: `$CHANTIER order slots --note 0              # 0 holds; a number
  resumes`.
- `foreman.md` line 42: the Foreman's own chat obeys "stop", "hold" (no new Driver: the batch
  still runs), and the user's line allowing a refused action.
- `docs/use-cases.md` line 66: `| "Hold." · "Resume." | slots 0: no new CR starts; a number
  resumes |`.
- `chief-of-staff.md` line 310, "After a pause, a restart or a stale heartbeat": a session's
  pause, not the batch's; reworded "After a break, a restart or a stale heartbeat".

The CR board's archive list, today "Landed (n of m)", names the merged CRs of `4-archives/`:

- `hooks/register.tsx` line 587-588: the section is `Merged (${index.merged.length} of
  ${index.merged_total})`, its key `merged`, its table `merged-table`.
- `status.py`, `dashboard_view()` (line 372-377): the index keys `landed` / `landed_total` become
  `merged` / `merged_total` (local names too).
- `types/index.d.ts`: line 46 "A merged or trashed CR."; lines 66-67 `merged: ChantierPast[]`,
  `merged_total: number`.
- `hooks/register.test.tsx` lines 61-62, 312, 399-433: the keys, the test name ("Backlog, Merged
  and Trashed are folded …"), `fold-merged` and `Merged (1 of 12)`.
- `scenario/run_scenario.py` lines ~1005-1035: the index checks read `merged` / `merged_total`
  and say "merged CRs".

### 5. The reports at the pause (`chief-of-staff.md`)

- **Completion report**, on the `final` message (Foreman mode) or right after your own `pause`
  (direct mode): header line, the CR table, then the cost table (the lines of `$CHANTIER cost`)
  and its explanation (`$CHANTIER cost --explain`), both run **at the pause**, the cost to date;
  it no longer takes them from `close` without `--yes`. What the batch did not prove. Its last
  line, **For you:**, says the batch is **paused**, lists the inbox ideas ready for a grill (the
  items of `1-inbox/`, each by its slug), and may invite the user to add other CRs to this same
  batch later or to close the batch ("close the batch"). It no longer says "closing the batch, with
  what `close` lists". Only a Tips line can follow it, as today.
- **Cost** bullet: "at landing" becomes "at the pause".
- **Landing** bullet becomes **The pause**: on `[foreman→chief-of-staff] final <STATUS.md path>`,
  that file is the exit report with the cost to date; the Foreman has removed the merged CRs'
  worktrees and branches, paused the batch, and stays idle. Give the Completion report. New work
  for the paused batch is `order add`: it sets the batch running again, you start the Foreman's
  work again by the usual order, and it pauses again at the end. The heartbeat sentence says
  "at the pause" instead of "at landing".
- **Closing** (a new short bullet, from the rest of the old Landing bullet): only on the user's
  word ("close the batch"): `$CHANTIER close --batch <batch>` without `--yes` is the check and
  prices the final cost; all its refusals stay as written today (anything running, an unpriceable
  cost, a running batch: it names what runs or says `pause` comes first). Report a refusal with
  its cause, never retry in a loop. When it passes, show the bilan, the final Cost section and
  what goes, and ask; only on their yes, in that turn: `close --yes`, then the dropped CRs'
  worktrees and branches, as today.
- **Starting a batch**, step 2 ("whatever its state until `close`") keeps its meaning: a paused
  batch is still the batch.
- **Steering a batch yourself**: "The running batch is strict" ends "Once the batch is paused it
  takes new CRs (below)". "The pause" says: once every CR is merged or cancelled, remove the
  merged CRs' worktrees and branches (your Foreman's work in direct mode), run `$CHANTIER pause
  --epoch <n>`, and the batch is paused; give the Completion report; grill the inbox ideas with
  the user and, on their word, `order add --note <folder>`: it runs again and pauses again at the
  end. "The end" is removed (its content is "The pause" plus the Closing bullet, which `close` in
  direct mode follows: it still counts only your Drivers' session files, not your own).
- Line ~322, the CLI's scope: `(open, slots, rounds, budget, orders, pause, close)`.
- Every other "landed"/"landing"/`land` of a batch in this card says "paused"/"the pause"/`pause`;
  "lands again" says "pauses again".

### 6. `foreman.md`

- Opening line: "You run one batch until it is paused" (not "until it lands").
- **Goal**: every CR merged or cancelled; then the merged CRs' cleanup, `$CHANTIER pause`, and
  the `final` line; the batch is paused. After `final` you stay idle (no Driver, no worker, no
  tool call), so that a later `close` finds nothing running. Remove "`land`'s cost is not final":
  the cost at the pause is the cost to date. An order that adds work to the paused batch sets it
  running again; you start again and pause it again at the end (a second `pause` on a paused
  batch is refused).
- Line 38: "`pause` waits for both". Line 45: "Your git is the merged CRs' cleanup before
  `pause`" (the step before the pause).
- Line 42: "hold", as section 4 says.
- Every other `land`/"lands" says `pause`/"pauses".

### 7. `concepts.md`, the other cards and the skill

- The new **Batch lifecycle** entry (above).
- **Batch** entry: "One batch is open at a time, until the user's `close`" becomes "One batch at a
  time, from `open` to the user's `close`"; the parenthesis about `order add` refers to the
  lifecycle and says "paused" for "landed" ("`order add` sets a paused batch running again:
  `pause` runs again at the end, and is refused on a batch already paused"; "a paused batch, of
  either steering, takes new CRs, which set it running again"). "`close` refuses … on a reopened
  batch too" stays.
- **Slots** entry: no change of meaning; if it names slots 0, it calls it "hold".
- **STATUS** entry: "A paused batch's `STATUS.md` is the exit report, its cost to date: `close`
  prices the batch up to now and prints the final cost." ("with no end date taken from `pause`").
  The rest (the refusals of `close` when it cannot price) stays.
- **`$CHANTIER`** entry: `pause` joins the commands exempt from the ten-line limit.
- `skills/chantier/SKILL.md`, Entry points: the row "the batch landed (\"close it\", the `final`
  message)" (line 64) splits into two rows: "the `final` message, the batch paused" → the
  Completion report (the cost to date from `cost` and `cost --explain`), section While it runs;
  and "close the batch" → `$CHANTIER close` (refused while anything runs; it prices the final
  cost), show the bilan and that cost, ask; `close --yes` only on the user's yes. Row 65 ("more
  rounds, slots or budget") is unchanged.
- `skills/chantier/references/init.md` line 42-43: "once it has landed, it is paused" becomes
  "once it is paused".
- `skills/chantier/references/hosts/claude-code.md` line 42: "right after `pause`". Its other
  "lands" (lines 65, 79, 129) are about a session's directory, not a batch: unchanged.
- `skills/chantier/references/hosts/copilot.md` line 32: "at the pause the Chief of Staff tells
  the user to delete the `/every`".
- `skills/chantier/references/driver.md` line 70 ("when that thing lands") is not a batch:
  unchanged.
- The agent files (`agents/`, `com.github.copilot/agents/`) hold no lifecycle text: unchanged.

### 8. Docs and evals

- `README.md` (lines ~56, ~189, ~208-219): the paused batch, `pause`, the cost to date shown at
  the pause, new work setting it running again, and closing only on your word ("close the
  batch").
- `docs/tutorial-claude-code.md` line ~147: "pauses the batch (its `STATUS.md` is the exit
  report, its cost to date)".
- `docs/use-cases.md` lines ~66 (hold), ~71-72 (`pause` waits; `order done` lets `pause` pass),
  ~151-162: the same words.
- `docs/cr-lifecycle-texts.md` ("LANDING", "## Landing", `chantier land`) and
  `docs/cr-lifecycle.svg`, `docs/cr-lifecycle-simple-texts.md` ("LAND", "## Land") and
  `docs/cr-lifecycle-simple.svg`, and `docs/how-chantier-works-texts.md` line 134 (`open, take,
  ship, land`) / `.svg`: the stage is the pause (`PAUSE`, `chantier pause`); closing is shown as
  the user's later word, not the next step. Keep each `-texts.md` and its SVG in step. Line 6 of
  `cr-lifecycle-texts.md` ("Every Change Request (CR) lands in one Markdown file") is not a batch:
  unchanged.
- `evals/kit/audit.py` line 278: the check reads `status == "paused"` ("the batch paused");
  lines 28, 194, 204 as section 1 says. `evals/README.md` line 82: "When the batch is paused".
  `evals/claude-smoke/RUNBOOK.md` line ~32 and `evals/copilot/RUNBOOK.md` line ~36: "the batch
  `paused`", `pause`. `evals/results/*` are records: not edited.
- `scenario/README.md` lines 20, 31, 39-40, 47, 60-61, 66: `pause`, paused, running, the cost to
  date, and the old `landed` / `open` batch read and rewritten.

## Out of scope

- What `close` checks, refuses and deletes, and its `--yes` confirmation: unchanged.
- Opening a second batch while one is paused: `open` still refuses (one batch at a time).
- The CR lifecycle and its stages (`1-inbox/` … `5-trash/`), and the CR states (`queued`,
  `working`, `ready`, `blocked`, `merged`, `cancelled`).
- The `open` command's name.
- The past records under `.agents/changes/` and `evals/results/`, and past `events.jsonl` lines:
  never rewritten by hand (only the CLI's own next write of an old `landed` or `open` batch,
  section 2).
- "lands"/"landed" that do not name a batch (a session's directory, a CR "landing in" a file, a
  waited-for thing that lands).

## Evidence

- `just check` passes (structure tests; `tests/test_structure.py` needs no new test).
- `claude plugin test .` passes with the board tests updated: a running batch, a paused batch
  folded, the "Merged (1 of 12)" section (`CONTRIBUTING.md` line 90).
- `just scenario` passes, on both forges, with its steps updated in
  `scenario/run_scenario.py` and `scenario/README.md` (the helper `self.landed` becomes
  `self.paused`, `w.landed_total` becomes `w.paused_total`):
  - a new batch is `status == "running"` (lines ~651, 881, 1138, 1488, 1499 read `"running"`);
  - `pause` refused while PRs are not merged (line ~650); the Foreman's `pause` at the last merge
    leaves `status == "paused"` and a `paused` timestamp (lines ~362-366, 676-691, 847, 892,
    1508-1511, 1666-1669, 1733, 1899-1904, 2119); `STATUS.md` holds `# <folder>: paused` and a
    `## Paused` section;
  - the event kinds include `pause`, not `land` (line ~743);
  - `close_refusals` (line ~1095): `status` shows `(paused, cost to date)`; the summary ends with
    the to-date line and holds no "Not final"; `pause`'s own output prints the cost summary
    (`Total: $…` among its lines, more than ten lines not cut); a second `pause` is refused with
    "already paused" and changes nothing; `STATUS.md` shows one total in its header and its Cost
    section, marked `(to date)`; `order add` sets it running again (`status == "running"`),
    clears `paused` and prints "was paused: running again"; `close` on a running batch where
    nothing runs says "not paused" and "`pause` comes first"; the second `pause` pauses again and
    its total counts the later call; `close` still prints the final cost, with a call made after
    the last pause in it;
  - the direct batch (lines ~847-892): it runs from `open` to the pause, `order add` on the paused
    direct batch reopens it (running), and it pauses again;
  - a new step, the old words: a batch whose `batch.json` is written by hand with
    `status: "landed"` and a `landed` timestamp is reported paused by `status` (and `close`
    treats it as paused), and after the next write through the CLI (e.g. `order add`, or
    `status --refresh`) its `batch.json` holds no `landed` key and no `"landed"` status; a batch
    written by hand with `status: "open"` is reported running by `status`, is taken by `take` and
    paused by `pause` as a running batch, and after the next write its `batch.json` holds
    `"running"`, no `"open"`;
  - `land` is no longer a command (exit 1, usage);
  - `order slots --note 0` still holds new Drivers; the usage line says "0 holds";
  - the index checks (lines ~1005-1035) read `merged` / `merged_total`.
- A grep proof in the PR body: `rg -n -i "\bland(ed|ing|s)?\b|not final" skills/ hooks/ types/
  README.md CONTRIBUTING.md docs/ evals/kit evals/README.md evals/*/RUNBOOK.md scenario/` returns
  only the non-batch uses listed in Out of scope and the compatibility helper of section 2, each
  hit named; and `rg -n "'open'|\"open\"" skills/chantier/scripts hooks/ scenario/` shows no batch
  state `open` left, except the compatibility helper and the scenario's old-words step (the
  `open` command and its event kind stay).

## Open questions

None.
