# Change Specification: cost-unknown-model

This CR carries three intake items that touch the same `cost` code and the same card
(`status-layout.md`, "Cost"):

- `cost-unknown-model` (`intake/request.md`, `02-answers.md` decisions 1 to 9);
- `report-template` (`intake/report-template-request.md`, `intake/report-template-answers.md`
  answers 1 to 11);
- point 3 of `cr-171-retro-fixes` (`intake/cr-171-retro-fixes-request.md`,
  `intake/cr-171-retro-fixes-answers.md` answers 3 to 5). Point 2 of that item is not here: it went
  to `version-pr-rendered-notes`.

Main read at 24cc7eb. The CLI is `skills/chantier/scripts/cli/src/chantier/` (below: `costs.py`,
`commands.py`, `status.py`, `rails.py`, `playbook.py`).

## Goal

In the user's terms:

1. One call on a model chantier has no price for must not hide the cost of a whole session or
   block a batch's `close`. The known calls are priced; the rest are counted and named, and the
   figure says it is a floor. A project adds a new model's price in its own `chantier.yaml`,
   with no release. Never a guessed price.
2. Every Progress and Completion report follows one fixed skeleton, written in the card, with
   the cost as a table (not raw CLI output) and two named places for free notes. The cost part
   gives the ratio of orchestration: (steering + Drivers) / total.
3. No line that starts with "Driver" ever names the steering session or its own subagents.

Generic: nothing in the cards or the messages names a particular model, project or batch. The
only model ids in the code are the built-in price table's (and the existing `playbook.MODELS`).

## What changes

### 1. The price table and the unpriced calls (`costs.py`)

**Built-in table (decision 1).** `PRICE` gains every model the Claude Code host offers today that
it lacks, `claude-fable-5-2` first, each at the provider's published price ($/MTok: input, 5-min
cache write, 1-h cache write, cache read, output; a long-context tier where the provider
publishes one, as `claude-haiku-5-5>100k` does). The Driver takes each figure from the
provider's public pricing page and cites the page in the PR description. A model whose price it
cannot find published is not added: decision 2 covers it. Never a figure inferred from another
model (decision 3).

**Matching an id.** `_family` matches only the three hardcoded families today. It becomes generic:
a model id is priced by the entry of the same id, or by the entry its id becomes once a trailing
date suffix (`-YYYYMMDD`) is removed. Nothing else: no prefix match, no family match, no "nearest
model" (decision 3). The long-context tier applies when the entry has one and the call's prompt is
above its threshold, as today.

**A model with no price (decisions 2, 3).** `_family` no longer raises "no Claude price for
model ...". `usage()` counts such a call in the row as unpriced, by model id: a new row field
(for example `unpriced: {model_id: calls}`), and adds nothing to `usd` or the dollars-by-kind
fields. Its tokens still count for the context measures (`peak_context`, `wakes`, cache expiry
timing), since they are measured, not priced. `calls` keeps counting priced calls only, so every
"(N calls)" figure stays a priced count; the unpriced ones are always said apart.

**What still fails.** Everything else that refuses today still refuses (unreadable record, no
message id, invalid token counts, missing transcript). A transcript whose calls are all unpriced
is not "no priced calls in ... transcript": `session_costs` treats a row with unpriced calls as
non-empty. The batch-wide refusal stays in `_cost_rows`: when no row of the batch has a single
priced call, it raises as today (decision 6: "nothing at all can be priced").

**Copilot (decision 8).** `copilot_session_costs` is untouched: the host's records carry the
price, and a call without one stays an error there.

### 2. Prices from `chantier.yaml` (decision 7; `playbook.py`, `costs.py`)

`chantier.yaml` gains an optional top-level key `prices`, beside `roles`. `playbook.load` stops
refusing it as an unknown key. Shape, one entry per exact model id, all five prices required, in
$/MTok:

```yaml
prices:
  claude-example-6-0:
    input: 3
    cache_write_5m: 3.75
    cache_write_1h: 6
    cache_read: 0.30
    output: 15
    long_context:          # optional, only when the provider publishes a tier
      above: 200000        # prompt tokens
      input: 6
      cache_write_5m: 7.5
      cache_write_1h: 12
      cache_read: 0.60
      output: 22.5
```

- Validation, with `chantier.yaml:<line>:` as every other problem of the file: an entry missing
  one of the five prices, a value that is not a number or is negative, an unknown key, a
  `long_context` without `above` or without its five prices. No price is derived from another
  (no cache price computed from the input price): that would be a guess (decision 3).
- An entry ranks above the built-in table for the same id. The date-suffix rule of part 1
  applies to it too.
- Read live at each pricing (`cost`, `status --refresh`, `pause`, `close`), not frozen at `open`
  like `roles`: the point is that a price added mid-batch prices the next refresh and the
  `close` without a release.
- With no `chantier.yaml`, or one without `prices`, only the built-in table prices (decision 7).
- A `chantier.yaml` that is not valid makes `cost` refuse with its problems and "run
  `$CHANTIER playbook`", as `open` does: it never prices with the file silently ignored.
- On Copilot the entries are not used (decision 8); `playbook` says so in one line when the
  file has `prices` and the host is Copilot.
- `playbook` prints one line when the file has prices: `prices: <id>, <id> (chantier.yaml, above
  the built-in table)`.
- The comment above `playbook.MODELS` ("A new model reaches the table by a release, like a new
  price in `costs.PRICE`") and the comment above `costs.PRICE` ("Any other model is refused")
  are rewritten to match.

### 3. Floors in every output of `cost` (decisions 2, 4, 5, 6; `commands.py`)

A figure that leaves calls unpriced is a floor and says so; never a plain total, never `$0.00`
for unpriced calls alone (decision 4). Wording, the same everywhere (the exact text is the
Driver's, these are the facts each line carries):

- `cost`'s first line: `<batch>: at least $1.608 over 94 priced model calls; 3 calls of
  claude-example-6-0 not priced`.
- A breakdown line, a `--by cr` line, a `--summary` line, a Chief of Staff line: its priced amount
  with "at least" and its own "N calls of `<model>` not priced" when it holds any.
- One line, once per unpriced model, after the lines of the batch's spend: `<model> has no price:
  add it under prices: in chantier.yaml (exact id: <model>)`. This is the line that gives the user
  the id to add (decision 7).
- `--explain`: the model list names an unpriced model with "(not priced)"; the shares of cost
  (cache reads, writes, output) are of the priced calls and say so.
- `--summary`: `Total: at least $1.61 of a $50 budget; 3 calls of <model> not priced`; the split
  line's shares become `not measured` while any call is unpriced (see part 5).

**Spend, budget, status (decision 5).** `_record_costs` records `spent_usd` as the priced part,
and records the unpriced calls beside it in `batch.json` (a new field, by model). The budget
check (`rails.over_budget`) reads the priced part, unchanged. `take` and `round` are not refused
for an unpriced model. Each place that shows the spend says it is a floor while unpriced calls
exist: the first line of `status` (`spent at least $1.61 of $50`), `rails.spent_text`, the batch's
`STATUS.md` header and the board (`status.py` `_budget`, `batch_markdown`, `dashboard_view`), and
`STATUS.json` (`batch_view` gains the unpriced field; `priced` stays true: a floor is priced). A CR
whose own calls hold unpriced ones: its `cost_usd` is the priced part and its row and page say
"at least" (`_row`, `_rows_markdown`, the CR page's "## Cost" line).

**`pause` and `status --refresh`.** An unpriced model no longer turns the summary into `Spent:
unknown (...)` nor the refresh into `spend not updated`: they record the floor.

**`close` (decision 6).** `_final_rows` no longer refuses for an unpriced model alone: `close`
prints the final cost with the not-priced remainder, and the archived CR pages say "at least"
where it applies. It still refuses, with or without `--yes`, when nothing can be priced: no
steering transcript recorded, or no priced call in the whole batch. The docstrings of `close` and
`_final_rows` ("a batch is never closed on an unknown cost") are rewritten to say exactly that.

### 4. Shares and the ratio of orchestration in `cost` (report-template answers 1, 5, 7, 8, 9)

`cost` (the default breakdown by role) prints, on each line of the batch's spend, its share of
the batch's spend next to its calls, apportioned so the shares add up to 100 as printed (the
existing `_apportion`): `Driver cr-driver: $0.912 (64 calls, 57%)`. The Chief of Staff's lines
outside the budget get no share (answer 6: they are not in the spend).

After the lines of the batch's spend and before the Chief of Staff's lines, one ratio line:
`Orchestration (steering + Drivers): 81% of the batch's spend`. Steering is the steering row as
`cost` prints it today, the batch's window only, grill and specifications already apart (answer
8), with the steering session's own subagents, as `--summary`'s split already groups them (open
question 1): nothing new is designed for the window. The ratio is computed by the CLI from the same
apportioned shares, so the writer copies it (answer 7).

Where a part is not measured, the cell and the ratio say so as the CLI prints (answer 9):

- Copilot, where a Driver cannot be told from a worker: the shares print (the costs are
  billed), the ratio line reads `Orchestration (steering + Drivers): not measured (no parent link
  on this host)`.
- Any unpriced call in the batch: each share reads `share not measured` and the ratio line reads
  `... not measured (calls not priced)`: a share of a floor would mislead as much as a ratio on
  half the data.

`--by cr` and `--summary` get no ratio line (the reports read `cost`); `--summary` keeps its split
line. `--explain` is unchanged in form
(answer 10).

### 5. No "Driver" line for the steering session (cr-171-retro-fixes answers 3 to 5)

The breakdown already labels the steering session's subagents `Foreman's own subagents` or
`Chief of Staff's own subagents` (`OWN_FOREMAN`, `OWN_CHIEF`). What is left (answer 4): in a direct
batch `_cost_groups(..., "driver")` keys the steering session's main row by its type,
`chief-of-staff`, so `_cost_summary` prints `Driver chief-of-staff with its workers: ...`. The
main row of any steering session, Foreman or Chief of Staff, is keyed like the own subagents
(`"foreman"`), so that line goes; its figure is already the steering row's. Check every output of
`cost` (the lines, `--explain`, `--summary`, the summaries of `pause` and `close`, `STATUS.md`'s
"## Cost") for the rule of answer 3: no line that starts with "Driver" names the steering session
or its own subagents, in Foreman and direct mode alike. On Copilot nothing changes: an agent's
line says only its type (answer 5).

### 6. The report template (`skills/chantier/references/status-layout.md`; report-template answers 2 to 7, 10)

The card holds a literal skeleton for each report, read before every report by the Chief of
Staff and by `/chantier:status` (answer 2). No template file elsewhere, no new CLI command. The
existing rules (CR names, icons, `unknown`, MR/PR, the chain line, the force-push line, the demo
offer, the Tips) stay, placed in the skeleton.

Fixed order (answer 3): header line; legend and CR table; **Notes**; cost table and the ratio
line; the second cost table (outside the batch's spend); **Cost notes**; the Completion report's
own parts (not proved, Retro); **For you**; the Tip.

Progress skeleton, as the card writes it (angle brackets are the writer's to fill, from the CLI
as printed):

```markdown
**<batch> <name>** · <who steers> · <shape> · slots <live>/<slots> · <done> CRs done · spent <spent> of <budget>

⚪ not started · 🟡 working · 🟠 waiting · 🔵 to review · 🔴 blocked · ✅ merged

| CR | Subject | State | PR | Cost |
| --- | --- | --- | --- | ---: |
| <CR-n slug> | <a few words> | <icon word> | [PR](<url>) | <cost> |

**Notes**
- <short line>

| Who | Cost | Share | Calls |
| --- | ---: | ---: | ---: |
| <label as printed> | <amount as printed> | <share as printed> | <calls> |
| Total | <total> | 100% | <calls> |

<the ratio line, as printed>

| Outside the batch's spend | Cost | Detail |
| --- | ---: | --- |
| <Chief of Staff line's label> | <amount> | <the rest of its line> |

**Cost notes**
- <short line>

**For you:** <what to review or decide, or "nothing">
💡 <tip>
```

The Completion skeleton is the same with its own header (CRs merged out of how many), its CR
table (CR, subject, result, PR, rounds, cost), then after **Cost notes**: what the batch did not
prove, the **Retro**, **For you**, the Tip.

The card's rules for these parts:

- **Notes and Cost notes are the only places for extra messages (answer 4):** short lines in the
  user's language (explanations, warnings, tips on reading the figures). An empty place is left
  out, not written "none". What the card already asks under the CR table (what a 🟠 or 🔴 CR waits
  for and who unblocks it, a chain and its reason, a force push run for a Driver) goes in
  **Notes**. The CLI's not-priced lines (part 3) and, in the Completion report, the few plain
  lines from `cost --explain` (answer 10) go in **Cost notes**. Nothing but the Tip follows **For
  you**.
- **The cost is a table, never raw output in a code block (answer 5).** Rows in `cost`'s order:
  the steering session, its own subagents, each Driver type, each worker type, then the Total row
  from `cost`'s first line. The Chief of Staff's lines (steering outside the budget, grill and
  specifications, whole session) are the second table (answer 6).
- **The writer copies, computes nothing (answer 7).** Every amount, share, call count and the
  ratio come from `cost` as printed; "at least", `unknown`, `not measured` and `share not
  measured` are copied as such. The current "You group, add and regroup nothing: no
  orchestration, implementation or review lines" becomes: you group, add and regroup nothing;
  the ratio line is the one grouping, and the CLI makes it.
- The "Cost" section's description of each line (who is who from the record, the Chief of Staff's
  lines, Copilot) stays, with "Driver chief-of-staff" gone and the floor rule added: a figure with
  unpriced calls is a floor and is shown as `cost` prints it, never as a plain total.

`skills/status/SKILL.md` keeps its three commands; its last sentence points at the Progress
skeleton. `chief-of-staff.md` lines 288 and 371 keep pointing at `status-layout.md`; reword only
if they describe the cost as raw lines.

### 7. Docs

- `README.md` "Costs and budgets": the sentence "A missing transcript, an unknown model or an
  unpriced call is an error, never a guess" becomes: an unknown model's calls are counted and
  named, the figure is a floor, and a project adds the price in `chantier.yaml`; the reports show
  `cost` as a table with the ratio of orchestration. "The reports show these lines as printed"
  becomes "as a table, the figures as printed".
- `README.md` "Your own agents": one short `prices:` example and a line that the CLI refuses an
  incomplete entry with its line.
- `skills/chantier/references/concepts.md` (playbook part): one line that `chantier.yaml` may also
  carry prices, read by the CLI only.
- No version edited by hand.

## Out of scope

- Fetching any price from the network (decision 7).
- A model in `playbook.MODELS` (role models in `chantier.yaml`): only prices change here.
- Copilot pricing (decision 8).
- The steering window (grill turns, paused time): main already splits grill and specifications
  (answer 8); no new design.
- Point 1 of `cr-171-retro-fixes` (`worker-write-guard-redesign`) and point 2
  (`version-pr-rendered-notes`).
- A template file or a CLI command that prints the report (answer 2).
- `cost --explain` as a table (answer 10).

## Evidence

`just check` passes on Linux, macOS and Windows; `just scenario` passes (this CR touches the CLI
and the cards).

`skills/chantier/scripts/cli/tests/test_costs.py`: the `"unknown-model"` case of
`test_claude_cost_refuses_unpriced_or_unreadable_usage` leaves the refusal list; one test that a
transcript with one priced and one unknown-model call gives the priced amount, `calls == 1` and
the unknown model counted once; one that a dated id of a priced model is priced.

`scenario/run_scenario.py` steps (Claude unless said):

1. The step at about line 1474 ("a batch whose final cost cannot be priced (a model with no
   price)") changes: with one `mystery-model` call added, `close` without `--yes` exits 0 and
   prints the final cost as "at least", with "1 calls of mystery-model not priced" and the
   `chantier.yaml` line naming `mystery-model`. A new refused step: a batch whose every call is
   unpriced is refused with "cannot be priced", nothing deleted.
2. With that call present: `cost`'s first line says "at least" and the not-priced count;
   `status --refresh` records the floor (no "spend not updated"); `status`'s first line,
   the batch's `STATUS.md` and the board say "at least"; `take` on a queued CR is not refused for
   it; each share reads `share not measured` and the ratio line `not measured (calls not priced)`.
3. A `chantier.yaml` with `prices: mystery-model:` and its five prices: `cost` prices the call,
   no "at least", total grown by the expected amount; `playbook` prints the `prices:` line. A
   dated id (`mystery-model-20270101`) is priced by the same entry.
4. `chantier.yaml` refusals, each with its line: a missing price, a non-number, a negative
   value, an unknown key under an entry, a `long_context` without `above`.
5. Section 9 (Cost): each breakdown line of the batch's spend carries a share; the shares add up
   to 100 as printed; the ratio line equals the steering share plus the Drivers' shares; the
   Chief of Staff's lines carry no share.
6. Copilot (`copilot_cost`): shares print, the ratio line reads `not measured (no parent link on
   this host)`.
7. A direct batch: `cost --summary`, `pause`'s summary and `close`'s final cost hold no line that
   starts with "Driver" and names `chief-of-staff`, `Chief of Staff` or `Foreman`; the steering
   row's figure is unchanged. The existing step at about line 1097 (own subagent not on a Driver
   line) still passes.

`tests/test_structure.py` keeps passing; no new structural test unless the card's skeleton needs
one to stay present (the Driver judges).

## Open questions

None. The one raised is settled in `02-answers.md`: the ratio's steering includes the steering
session's own subagents, as `cost --summary`'s split already does.
