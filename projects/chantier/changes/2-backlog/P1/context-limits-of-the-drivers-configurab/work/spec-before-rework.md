# Drivers' context limits: 200k, configurable, listed, warned

The Drivers hand back `blocked context` at a threshold set in `chantier.yaml` and on the board's
Limits tab: 200,000 tokens by default, with the Drivers' agent window raised above it. That window
is measured first. `round`, `note`, `phase` and `stack` print the thresholds they use, and the
cards name no figure. `chantier playbook --context` lists the context limits, each with its value
and source. Incoherent settings warn without blocking, in that list and when a batch opens.

Issue: none (a verbal request; no tracker issue).

## Goal

The owner's words (`intake/request.md`): "ça devrait être 200K pour être tranquilles; ces
settings devraient être configurables, ou au moins documentés pour que je regarde facilement si
elles sont cohérentes." Today the thresholds exist only as figures in card sentences: 130,000 to
hand back, 115,000 for the closing hand-off. Nothing in `chantier.yaml` sets them and no single
list shows them. In batch-31, Drivers handed back `blocked context` five times by 2026-11-25, at
68k to 97k tokens, under a 100k limit the Chief of Staff had asked for (`intake/request.md`).

## Place in the chain, and the facts that depend on CRs not yet written

This CR joins batch-31's stack at its end, after CR-514 and then after `shortcut-commands`
(`1-inbox/shortcut-commands/03-change-spec.md`, not final). It is specified against the newest
head that exists: the worktree `chantier.worktrees/batch-31-CR-507`, head `03f973e`, read
2026-11-25 with uncommitted edits present there (none to the files this CR touches). The new
cards sit there, not yet loaded, in `skills/chantier/cards-next/`. CR-510 to CR-514 and
`shortcut-commands` are not written yet. The facts below come from their specifications. At its
base the Driver checks each one. When one does not hold, it acts as the last column says. There
is no stand-in.

| Fact this specification relies on | From | If it does not hold at the base |
| --- | --- | --- |
| `skills/chantier/references/` holds the swapped `cards-next/`: `cr-driver.md`, `stack-driver.md`, `release-driver.md`, `qa-driver.md`, `topics/closing.md`, `topics/lost-context.md`, `topics/host-compact.md`, `topics.json`. The old `driver.md`, `foreman-lost-driver.md` and their pieces are gone | CR-510 | Stop and say which |
| `references/cr-driver.md` (from `cards-next/cr-driver.md`) has no general rule to hand back at the hand-back threshold. At `03f973e` it names a `context:` threshold only in its closing bullet (line 11), and `topics/closing.md` only during the closing. The old `references/driver.md` had the rule (lines 117 to 124 at `03f973e`: "At 130,000 tokens or more, record your state with `note`, then `handback <cr> blocked context: …`"). It is a rule lost in the rewrite, named here for the CRs that switch to the new cards | CR-510 (the swap), CR-511 (the old-against-new inventory, which restores what was lost) | If the base's `cr-driver.md` holds the rule (restored by CR-511), reword its figure to "the hand-back threshold" (section 6) and add none. Else add it (section 6) |
| The CLI code named below (`context_line` in `commands/driver.py`, `playbook/limits.py`, `limits_check.py`, `board/config_api.py`, `hub/schemas.py` `LIMITS`, `clients/web/js/views/config-limits.js`) is as at `03f973e` | none of CR-510 to CR-514 touches it | Follow the code at the base and list each difference in the PR |
| The history lint (M3) over `references/**/*.md` flags token counts (`\b\d[\d,.]*\s?k?\s?tokens?\b`). The figures `130,000 tokens` and `115,000 tokens` in the cards are either reworded by CR-512 or listed in `references/lint-allow.txt` | CR-512 section 4 | Follow what CR-512 shipped. This CR leaves no token figure in the four Driver cards, `topics/closing.md`, `topics/lost-context.md` and `topics.json`, so it removes every `lint-allow.txt` entry for those figures (a stale entry fails). `topics/host-compact.md` keeps its measure (section 6) |
| `references/budgets.json` freezes each card's size; `rules.json` gives rule ids `[R-nnn]` | CR-512 | Without them, the budget and id steps below fall away |
| M6 (a PR that adds card text quotes the measure or the owner's line) and M11 (`budgets.json` changes only with the owner's approval line) | CR-513 | Same |
| `scenario/run_scenario.py` checks the closing threshold's figure in the Driver cards (at `03f973e`: "driver.md names the 115,000-token closing threshold", line 7169, globbing `references/*driver*.md`) | CR-510 converts it to the new cards | Change that check as section 7 says, wherever it sits at the base |
| `shortcut-commands` changes no file this CR touches (skills, topics `command-*`, `hooks/register.tsx`, `.github/plugin/plugin.json`, `scripts/version.py`) | its specification | Rebase on it and say so |

## Decisions carried from `02-answers.md`

| Answer | Decision | Where here |
| --- | --- | --- |
| 1 | Grilled first; destination confirmed at "grilled enough?" | Answer 6 |
| 2 (Q1) | "200K" means the hand-back threshold at 200,000, with the agents' context window raised above it (for instance 300,000). Nothing proves the model accepts a larger window: the CR measures that first, and comes back to the owner if it cannot | section 0 (the trial, before any code) |
| 3 (Q2) | The thresholds are set in the project's `chantier.yaml`, a command lists each one with its value and source, and they can be edited on the board's Configuration page, Limits tab | sections 1, 3, 5 |
| 4 (Q3) | Incoherent settings warn without blocking, in the list and when a batch opens | section 4 |
| 5 (Q4) | The list holds the context limits only. Rounds, slots, budget, lease, heartbeat, watcher wake and `specifying.parallel` are left out. This narrows the request's "same list" | section 3; Out of scope |
| 6 (Q5) | Specified for the running batch batch-31, after `shortcut-commands`. Accepted defaults: the closing threshold stays 15,000 under the hand-back one (185,000); this applies to the Drivers (CR, stack, QA, release) and to the context thresholds the Foreman applies, and the other agents are unchanged; `chantier` prints the thresholds to the Drivers and the cards name no figure. The exact window is set by the trial. The extra cost of a large context is not measured | sections 0, 1, 2, 6 |
| 6 | A spec critic runs (it changes the Drivers' contract and the board's Configuration page) | the Chief of Staff's, not this specification's |

## Decisions this specification takes on the means

- **D1. Two keys, one derived value.** A new top-level key `context` in `chantier.yaml` holds
  `handback` (the hand-back threshold, a whole number, 1 or more) and `closing_margin` (a whole
  number, 0 or more). The closing threshold is not a key: it is `handback - closing_margin`, so the
  closing margin stays a named value (`intake/request.md`). Shipped defaults: `handback: 200000`,
  `closing_margin: 15000`. The keys resolve through the same layers as `specifying.parallel` and
  `batch.slots`: repository, surface project, surface, then the shipped defaults, with `default`
  as a reset.
- **D2. The window stays in the agent files.** An agent's window is the `autoCompactWindow:` front
  matter of its file under `agents/`. The plugin ships it and no `chantier.yaml` sets it. This CR
  raises it in `agents/cr-driver.md`, `agents/stack-driver.md`, `agents/qa-driver.md` and
  `agents/release-driver.md` to the value the trial proves (section 0). The other agent
  files are unchanged (Answer 6). At `03f973e`, `agents/` holds fifteen files: the four Drivers,
  ten that carry `autoCompactWindow: 200000` (`coder`, `conflict-resolver`, `debugger`,
  `demo-explorer`, `inspector`, `investigator`, `retro-critic`, `spec-critic`, `spec-writer`,
  `verifier`), and `board-griller.md`, which sets no window (the host's own). The list reads the
  window from the file of the role's agent.
- **D3. No new command.** The list is `chantier playbook --context`, a new flag on `playbook`.
  `playbook` already lists the limits, the timing and `events.wake_every` with their layers.
  `rules` and `playbook` without the flag print a single `context:` summary line. The CLI's scope
  (AGENTS.md) gains no tool.
- **D4. Read live.** The thresholds are read from the configuration at each context line, never
  frozen with the batch, the same way `playbook --batch` reads the limits ("live, never frozen
  with the batch"). A change on the board applies at each Driver's next `round`, `note`, `phase`
  or `stack`. (Open question 1.)
- **D5. The CLI prints and never refuses.** The context line says when a threshold is reached;
  no command refuses because of it. The Driver still judges when to hand back, as its card says.

## What changes

Paths are from the repository root. `src/` is `skills/chantier/scripts/cli/src/chantier/`;
`tests/` is `skills/chantier/scripts/cli/tests/`; `references/` is `skills/chantier/references/`
(the swapped cards, CR-510).

### 0. The window trial, first, before any code (Answer 2)

**Unproved:** whether Claude Code honours `autoCompactWindow` in a subagent's file, and whether
`claude-sonnet-5-5` (the Drivers' model, `config/chantier.defaults.yml`) takes an agent window
above 200,000. What is on record (`references/hosts/claude-code.md`, "Compacting",
`docs/proofs/claude-code.md`):

- documented: `autoCompactWindow` takes 100000 to 1000000 and is capped at the model's context
  window;
- measured: agents set to 200000 compacted after a last prompt of 161,951 to 166,684 tokens
  (batch-16, batch-17), and sessions set to 300000 compacted near 165k to 170k.

That second figure points to a cap at 200,000. In that case a 200,000 hand-back can never be
reached.

The trial runs in a scratch folder outside every repository, on Claude Code, with the user's own
install. In that folder, `.claude/agents/window-trial.md` has the front matter `model:
claude-sonnet-5-5`, `tools: Read` and the window under test. A headless `claude -p` asks the main
session to start the `window-trial` agent with this prompt: read whole, one after another, the
files of a fixed list (source files of the chantier repository, by absolute path, enough to pass
the target), then reply `DONE`. The measure comes from the subagent's transcript
(`~/.claude/projects/<slug>/<session>/subagents/agent-*.jsonl`), with the same reading as
`costs/sessions.py` `agent_context`:

- the prompt size of each call;
- the size at the first compaction boundary, if there is one;
- any refusal of the call (for example, a prompt too long).

| Trial | Window in the file | Read until the prompt passes | Pass | Fail |
| --- | --- | --- | --- | --- |
| T1, the key honoured | `autoCompactWindow: 120000` | 130,000 | the first compaction comes below 120,000 | no compaction below 120,000: the key is not honoured for a subagent |
| T2, the window | `autoCompactWindow: 300000` | 215,000 | a call's prompt above 215,000 with no compaction and no refusal before it | a compaction or a refusal below 215,000 |

- The Driver starts the trial in a background shell. If the host refuses `claude -p` there, it
  hands back `blocked question: the window trial needs claude -p in a scratch folder` with
  everything else untouched, and the Chief of Staff runs it.
- Spend cap: $5 for both trials. Sonnet 5.5's prices are in `costs/transcripts.py`.
- **Both pass:** the window is 300000 in the four Driver agent files. Each trial's figures,
  transcript excerpt and spend are recorded in `docs/proofs/claude-code.md`, "Compacting", and in
  the PR. Then sections 1 to 8 follow.
- **Either fails:** no code changes. The Driver hands back `blocked question: agent window: <the
  trial, the figures>`, and the Chief of Staff takes it to the owner. The Driver tries no other
  model, window or setting: the choice is the owner's (AGENTS.md: no fallback).
- **Copilot:** its agent files (`com.github.copilot/agents/*.agent.md`) set no window, and no
  per-agent context is measured there. Untested, and no trial is run there (matrix).

### 1. The configuration: `config/chantier.defaults.yml` and the checks

- **`config/chantier.defaults.yml`** gains, after `batch:`, a comment and the block below. The
  comment says three things: the Drivers' context thresholds; the closing threshold is the
  hand-back minus the margin; the Drivers' window is in their agent files.

  ```yaml
  context:
    handback: 200000        # a Driver hands back `blocked context` from this many tokens
    closing_margin: 15000   # the closing hand-off comes this many tokens before the hand-back
  ```

- **`src/playbook/limits_check.py`:** a `context_key` check. `context` holds `handback` and
  `closing_margin`, each a whole number: `handback` 1 or more, `closing_margin` 0 or more. An
  unknown sub-key or a bad value is a problem line in the form the two limits already use. Wire it
  into `_KEYED` in `src/playbook/config.py`. The `unknown key` message of `check` lists
  `"context"`. `missing_limits` also requires the two context keys in the shipped defaults.
- **`src/playbook/limits.py`:** the limits resolved per key (`_one`, `limits_from`) also cover
  `context.handback` and `context.closing_margin`, each with `{value, layer, src, layers}`. One
  key tuple names the four keys the board edits (`LIMIT_KEYS`, or a second tuple beside it; the
  Driver's choice, said in the PR).
- **Each layer's value is checked alone.** Comparing the two keys never refuses (section 4).

### 2. The context line: `round`, `note`, `phase`, `stack`

`context_line` (`src/commands/driver.py`) is the only function that prints it. It is called by
`round` (`driver.py`), `note` and `phase` (`commands/driver_notes.py`), and `stack` read-only
(`commands/delivery.py`). It reads the two keys live (D4) and adds them to the line it prints
today:

- measured: `context: <n> tokens (agent <id>); hand-back at <h>, closing at <c>`;
- not measured: `context: not measured (<why>); hand-back at <h>, closing at <c>`;
- when either key comes from a user layer: ` [<layer>]` after `<c>` (the layer label, as
  `events_line` prints it). Nothing is added for the shipped defaults;
- when `<n>` ≥ `<c>`: `; closing threshold reached`. When `<n>` ≥ `<h>`: `; hand-back threshold
  reached` instead.

The figures are printed as plain digits, as `<n>` is today. If the configuration cannot be read,
the line ends `; thresholds: not readable: <first problem>`, and the command still succeeds. Each
of these is one line, so the ten-line output rule holds.

### 3. The list: `chantier playbook --context` (Answers 3 and 5)

`declare/rules.py` gives `playbook` the flag `--context`: "the context limits only, each with its
value and source". With it, `playbook` (`src/commands/rules.py`) prints only these lines, for the
host (`--host`, or the detected one):

```
context limits (claude):
hand-back threshold: 200,000 tokens (shipped defaults: config/chantier.defaults.yml)
closing margin: 15,000 tokens (shipped defaults: config/chantier.defaults.yml)
closing threshold: 185,000 tokens (the hand-back threshold minus the closing margin)
window of cr-driver: 300,000 tokens (agents/cr-driver.md, autoCompactWindow; the model's own window may cap it)
window of stack-driver: ...
window of qa-driver: ...
window of release-driver: ...
measured by: round, note, phase and stack, from the agent's transcript
```

- A key set by a user layer shows that layer's label and file path, as the limits view's `src`
  does.
- A Driver role whose agent is the user's own (`agent:` in a `chantier.yaml`): `window of <role>:
  not read (your agent <name>)`.
- On Copilot, each window line reads `window of <role>: not set by the agent file (the host's
  own)`, and the last line is `measured by: none (Copilot gives no per-agent record)`.
- Then the warnings of section 4, one line each, prefixed `warning: `.
- Exit 0 with or without warnings. The ten-line rule does not bind `playbook`: `concepts.md`
  exempts it.
- **Without `--context`:** `playbook` and `rules` print one line after the `limits:` line:
  `context: hand-back at <h>, closing at <c> (margin <m>)`, with each key's layer when it is not
  the default. Then the section 4 warnings. Both commands keep every other line as it is.

### 4. The warnings (Answer 4)

One function (in `src/playbook/lines.py`, beside `timing_warnings`) returns the warning lines:

- **W1**, `closing_margin` ≥ `handback`: `context: the closing margin <m> is not below the
  hand-back threshold <h>: every closing is handed off`.
- **W2**, for each Driver role whose agent is the plugin's on Claude Code: the hand-back threshold
  is above the role's window minus the compaction margin, a named constant in code. The line:
  `context: <role>'s window <w> (agents/<role>.md) is under the hand-back threshold <h> plus <margin>:
  the agent may compact before it hands back (compactions were measured about <margin> under a
  200000 window)`.
- **The compaction margin: 38,000.** Its comment cites both measures of
  `docs/proofs/claude-code.md`, section `compact` (lines 314 to 316 at `03f973e`):
  - agents set to `autoCompactWindow: 200000` on `claude-sonnet-5-5` compacted after a last prompt
    of 161,951 to 166,684 tokens (batch-16, batch-17): 33,316 to 38,049 under the window. 38,000
    is the largest of these gaps, to the thousand. It is measured at a 200000 window only;
  - sessions set to 300000 compacted near 165k to 170k, about 130,000 under the setting. That
    points to a cap at 200,000, not to a margin, and is the case T2 tests.

  **Unproved:** that the gap measured at 200000 holds at 300000. If T2 records a compaction (a
  pass puts it above 215,000), the margin is the larger of 38,000 and 300,000 minus that
  compaction's prompt size, and the comment cites T2's figure as well. With no compaction in T2,
  38,000 stays, and the comment says it was measured at a 200000 window only.

Where they show, never blocking:

- `playbook --context`, and `playbook` and `rules` (section 3);
- `open` (`src/commands/opening.py`): the lines go after the `next:` line and before the CR list,
  in the opening's output, and the opening goes on;
- the board's Limits tab and the reply of a save (section 5).

An invalid key, by contrast, is still refused wherever the configuration is read, as today.

### 5. The board: Configuration page, Limits tab (Answer 3)

- **`clients/web/js/views/config-limits.js`:** `LIMITS` gains
  `{ key: 'context.handback', id: 'handback', min: 1 }` and
  `{ key: 'context.closing_margin', id: 'closing_margin', min: 0 }`. Each row works like the two
  that exist: the input, the value in effect with its layer, "use the inherited value". Below the
  rows, the view's context warnings (section 4) show in the tab's existing note style. No new
  token or component (`DESIGN.md`, read first and kept true).
- **`src/playbook/edit.py` and `edit_text.py`:** `edit_surface_file` and the text edit accept the
  two dotted keys, as they accept `batch.slots`. The view (`config_view`) carries `limits` for the
  four keys and a `context_warnings` list.
- **`src/board/config_api.py`:**
  - `_limit_line` for a context key: `context <name> <old> -> <new>: the Drivers read it at their
    next round, note, phase or stack`;
  - a save that leaves the keys incoherent is written. Its reply's `lines` carry the warnings;
  - each key whose effective value moved appends its `config@1` line, as today.
- **`src/hub/schemas.py`:** `LIMITS` names the two context keys too. `config_text` for a context
  key: `config changed on the board: <key> <old> -> <new>; the Drivers read it at their next
  context line`. The `config@1` model accepts the keys. A context `config@1` line is told and
  never acted on: it applies live (D4), so no order follows it (the cards, section 7).
- **`src/plugin_files.py`:** the `read_limits` docstring ("The two limits") names the four keys.
- **i18n:** `clients/web/js/i18n/en-board.js` and `fr-board.js` gain the labels and texts for the
  two rows, in the existing key form (`config.limits.handback`, `.text`, and so on). In
  `en-help.js` and `fr-help.js`, the help paragraph that says "Two limits are set on this
  board's ... Limits tab" names the four values.

### 6. The cards (Answer 6: the cards name no figure)

Each edit replaces a figure with the threshold's name. The meaning is unchanged. Every rule id
`[R-nnn]` stays on its sentence.

- **`references/cr-driver.md`:**
  - a new bullet, before the closing one, restores the rule lost in the rewrite ("Place in the
    chain"): "At the hand-back threshold the last `context:` line prints, `note` your state, then
    hand back `blocked context:` (`help handback-other`)." Its source, quoted in the PR as M6
    asks: the owner's line in Answers 2 and 6 of `02-answers.md` (Answer 2's facts, "the cards
    hand back at 130,000"; Answer 6, "`chantier` prints the thresholds to the Drivers and the
    cards name no figure"), and the old rule in `references/driver.md`, lines 117 to 124 at
    `03f973e`. With `rules.json` (CR-512), it takes a new rule id `[R-nnn]`. When the base's
    `cr-driver.md` already holds the rule (CR-511), only its figure is reworded;
  - the bullet "At 115,000 tokens on the last `context:` line, at the `VERIFIED` of the pushed head,
    hand off with `context: closing:`" becomes "At the closing threshold the last `context:` line
    prints, ...";
  - the `closing` entry of "Rare cases", "a context near 115,000 tokens", becomes "a context near
    the closing threshold".
- **`references/stack-driver.md`:** "At 130,000 tokens on the `context:` line of `$CHANTIER
  stack`" becomes "At the hand-back threshold the `context:` line of `$CHANTIER stack` prints".
- **`references/topics/closing.md`:** "Below 115,000 tokens", "At 115,000 tokens or more" and the
  two "130,000" become "below the closing threshold", "at the closing threshold or more" and "at
  the hand-back threshold". The line names the thresholds once: "the thresholds are the ones your
  last `context:` line prints".
- **`references/topics/lost-context.md`:** "at 115,000 tokens or more" becomes "at the closing
  threshold or more".
- **`references/topics.json`:** the `closing` trigger "a context near 115,000 tokens" becomes "a
  context near the closing threshold".
- **`references/topics/host-compact.md`:** "(the plugin's agents carry 200000)" becomes "(the
  plugin's Drivers carry the window `playbook --context` prints, the other agents 200000)". The
  rest of the topic stays.
- **`references/release-driver.md`:** if the base has no context rule there, add one bullet:
  "At the hand-back threshold the last `context:` line prints, `note` your state, then hand back
  `blocked context:` (`help handback-other`)". The M6 measure is the owner's line in Answer 6
  ("it applies to the Drivers (CR, stack, QA, release)"). If the base has a context rule there,
  reword its figure as above.
- **`references/qa-driver.md`:** no change. The QA Driver runs no command that prints a context
  line (it holds no CR: no `round`, no `note`), so only its window changes (D2; open question 2).
- **Budgets (CR-512):** each edited file must stay within its limit in `budgets.json`. If a file
  cannot, the Driver leaves `budgets.json` alone and the PR's Known gaps names the file and the
  bytes, for the owner's approval line (M11).
- **The history lint:** no token figure is left in the four Driver cards, `topics/closing.md`,
  `topics/lost-context.md` and `topics.json`. Any `lint-allow.txt` entry for a figure in them is
  removed. `topics/host-compact.md` keeps its measured figure ("165 to 170k tokens", a measure of
  the Chief of Staff's and the Foreman's sessions, not a threshold) and whatever CR-512 gave it
  (its `lint-allow.txt` entry); this CR removes no entry for it.
- **Unchanged:** the Chief of Staff's compacting advice (`topics/compacting-p1.md`, above 100k
  tokens). It is not a Driver's or the Foreman's threshold (Answer 6: the other agents
  unchanged).

### 7. Agent files, docs, eval kit, scenario, AGENTS.md

- **Agent files:** `autoCompactWindow: <the window T2 proved>` in the four Driver files of
  `agents/` (D2). The Copilot files are unchanged. Their bodies are untouched, so the two hosts'
  bodies stay identical.
- **The cards that list the limits** (from `cards-next/`, swapped by CR-510; edited under section
  6's rules on budgets and M6, the owner's line being Answer 3):
  - `topics/watcher-events.md`: after "A `specifying.parallel` or role-key line: one line, no
    action.", the context keys the same way: "A `context.handback` or `context.closing_margin`
    line: one line, no action (it applies at the Drivers' next context line).";
  - `topics/watcher-pull.md`: "act on its merge and two-key `config@1` lines" becomes "act on its
    merge and limit `config@1` lines";
  - `topics/config-p1.md`, its `Keys:` list: after `batch.slots (4 by default, 0 or more)`,
    `context.handback` (200000 by default, 1 or more) and `context.closing_margin` (15000 by
    default, 0 or more).
- **`docs/server-api.md`,** the `config.get` row: "the two limits" becomes "the four limits
  (`specifying.parallel`, `batch.slots`, `context.handback`, `context.closing_margin`)".
- **`docs/web-board.md`,** the signal paragraph (line 70 at `03f973e`): a save that changes the
  effective `context.handback` or `context.closing_margin` writes its `config@1` line too, told as
  `config changed on the board: <key> <old> -> <new>; the Drivers read it at their next context
  line`.
- **Other places checked at `03f973e`:** the i18n help paragraphs (section 5), `AGENTS.md`
  (below) and `plugin_files.py` (section 5). `cards-next/concepts.md` and `init.md` name
  `batch.slots` alone, as a slot rule, not as a list of the limits: unchanged.
- **`docs/agents-and-models.md`,** the paragraph that lists the `chantier.yaml` keys (line 102 at
  `03f973e`): `context` (`handback`, 200,000 by default; `closing_margin`, 15,000), and that
  `playbook --context` lists them with the Drivers' windows.
- **`docs/web-board.md`,** the Limits tab paragraph: four numbers instead of two, when a context
  change applies, and that warnings show without blocking.
- **`docs/tutorial-claude-code.md`:** "The plugin's agents compact at 200,000 tokens" becomes "The
  plugin's Drivers compact at <window>, the other agents at 200,000". The section names
  `playbook --context`.
- **`docs/proofs/claude-code.md`,** "Compacting": the trial's measures, as section 0 says.
- **`evals/kit/audit.py`:** `WINDOW = 200_000` becomes the window read per plugin agent from its
  file (`agents/<role>.md`, `autoCompactWindow`). J17 checks each agent's peak against its own
  window. An agent whose file sets no window (`board-griller.md`, which no batch starts) gets no
  J17 check: no figure stands in for it (AGENTS.md: no fallback).
- **`scenario/run_scenario.py`:**
  - the context-line check (line 6993 at `03f973e`: `out == ["ok", "context: 4240 tokens (agent
    ...)"]`) and the `not measured` checks expect the threshold suffix;
  - the card check that wants "115,000 tokens" in the Driver cards now wants no token figure
    there, and the words "closing threshold" and "hand-back threshold";
  - a new step: the project's `chantier.yaml` sets `context: handback: 50000, closing_margin:
    60000`, then `note` prints `hand-back at 50000, closing at -10000 [<layer>]` and `open` of an
    empty batch prints W1 and opens.
- **AGENTS.md:** "the two limits (`specifying.parallel`, `batch.slots`)" becomes "the limits
  (`specifying.parallel`, `batch.slots`, `context.handback`, `context.closing_margin`)". This
  covers the board's Configuration paragraph and the `config@1` sentence ("the two limits, and
  each role's agent ..."). Nothing else in AGENTS.md changes.

### 8. Tests and the quiz

Every check reads the shipped files at the head under test: the cards, `config/chantier.defaults.yml`
and the agent files. A text the test prepares is used only for a refusal or an incoherent layer.

- **`tests/test_limits.py`** (parametrized):
  - the two keys resolved from each layer and from the shipped file, with a reset;
  - a bad value refused (`handback: 0`, `closing_margin: -1`, an unknown sub-key);
  - `missing_limits` names a shipped file without them.
- **`tests/test_cli_runs.py`:** `note` with no agent prints `context: not measured (no agent
  recorded); hand-back at 200000, closing at 185000`. The two figures are read from the shipped
  defaults file in the test, never typed.
- **A test of the line's suffixes:** an agent transcript prepared at the closing threshold, then at
  the hand-back threshold, gives each "reached" word. A user layer's label shows.
- **`tests/test_playbook_config.py`:** `playbook --context` on the shipped files lists the lines of
  section 3, and each window is equal to that agent file's `autoCompactWindow`. A layer with W1
  gives the warning and exit 0. `rules` prints the summary line.
- **`tests/test_board_config.py`:** a `config.put` of `context.handback` writes the surface file,
  appends a `config@1` line and returns the `_limit_line`. An incoherent save is written and its
  reply carries W1. The view lists four limits.
- **A test of the cards:** the history lint's token-count pattern matches nothing in the four
  Driver cards, `topics/closing.md`, `topics/lost-context.md` and `topics.json` (read as text).
  `topics/host-compact.md` is not among them: it keeps its measure. `cr-driver.md` holds the
  hand-back rule of section 6. Each of them names "closing threshold" or
  "hand-back threshold" where it named a figure.
- **A test of the agent files:** the four Driver files carry the same `autoCompactWindow`; the ten
  other files that set one carry 200000; `board-griller.md` sets none, and the test reads it as no
  window, with no figure in its place.
- **Quiz case (new),** `evals/quiz/cr-driver/context-threshold-from-cli.json`, in the format of
  CR-492's cases. The Driver's last `note` printed `context: 160000 tokens (agent a1); hand-back at
  150000, closing at 135000 [repository]; hand-back threshold reached`, and work remains. A pass:
  `note`, then `handback <cr> blocked context: ...`. A fail: going on, or citing a figure that the
  line does not print. It tests the hand-back rule section 6 adds to `cr-driver.md`: its `rules`
  entry is that rule's id, and its pass cites that bullet.

## Out of scope

- The limits that are not about context (Answer 5): rounds, slots, budget, lease, heartbeat,
  watcher wake, `specifying.parallel`. Their list and their values do not change.
- The model's real window and any model change. Another window, model or host setting if the trial
  fails (that is the owner's choice).
- The windows of the non-Driver agents (Answer 6), and the Chief of Staff's and the Foreman's own
  session windows (`host-compact`).
- A refusal at a threshold (D5). A context measure on Copilot. A context line for the QA Driver
  (open question 2).
- The price of a long context: not measured (Answer 6). The trial's spend is reported only.
- A version bump.

## Host and default matrix

| Host | Defaults | Status and evidence |
| --- | --- | --- |
| Claude Code | shipped (200000 / 15000, window from T2) | The thresholds and the line: tests and scenario. The window: unproved until T1 and T2 pass (section 0). Until then nothing is changed |
| Claude Code | configured (a `chantier.yaml` layer, or the board) | Tests (`test_limits.py`, `test_board_config.py`) and the scenario's step with W1. The board save is in the PR's evidence |
| Copilot | shipped | The keys and the list are the same files, covered by tests. The context line prints `not measured` with the thresholds. The agent files set no window, so the window is untested and not raised. No trial |
| Copilot | configured | Same as shipped. Untested in a real Copilot session |

## Acceptance evidence

Recorded in the PR or under `<CR folder>/evidence/`, from the pushed head.

1. **The trial (section 0):** for T1 and T2, the agent file used, the largest prompt, the first
   compaction's size or none, any refusal, and the spend, with a transcript excerpt. This comes
   before any code. If it fails, it is the only evidence there is.
2. **The measured cost (the request):** from `4-batch/events.jsonl` of batch-31, the count of
   `handback` events whose note starts `context:` (not `context: closing:` and not `context: host
   asked`), each with its last context figure. Expected: five or more, at 68k to 97k.
3. **The CLI at head:** the output of `playbook --context` on the shipped defaults, of `note` on a
   live CR (the suffix), and of `open` with a W1 layer (in a scratch planning folder).
4. **The board:** a save of `context.handback` from the Limits tab on a running board at head. It
   shows the rows, the warning after an incoherent save, and the `config@1` line in
   `forge-journal.jsonl`.
5. **Tests:** `just test` passes, timed at the base and at head on the same machine, both figures
   quoted (expected under +1 s).
6. **The quiz:** `just quiz cr-driver` on the new case, with the spend plan line printed first. The
   score is at least 2 of 3. If the headless host CLI is refused, the Driver hands back with
   everything else done and says so, and the Chief of Staff runs it.
7. **M6:** the PR quotes the owner's line in Answers 2 and 6 and the measure of item 2.
8. **Budgets:** CR-512's tests pass. Each edited card's size is quoted before and after against its
   limit.
9. **Known gaps of the PR** name the inbox item `1-inbox/driver-context-second-cut`. Its done line
   (`intake/request.md`, line 16) reads "with its peak context below 115,000 tokens", a fixed
   figure this CR turns into a setting. The Chief of Staff restates that done line against the
   closing threshold; this CR does not edit the item.

## Gates

- **Before the first push:** `just check`, and `just eval-dry-run` (the CLI's `src/` and
  `evals/kit/` change), at the rebased head. `just mod` is not owed: `hooks/` and `types/` do not
  change.
- **The long gate,** `just scenario (ubuntu-latest)`, green at the PR's head: owed, because the
  CLI and the cards change.
- **The local Windows long gate,** `chantier gate <cr> scenario`, at the head: owed by this CR if
  it is the top of the stack when it joins. The run moves to it from `shortcut-commands`
  (AGENTS.md).
- **The merge:** on the owner's word, after `shortcut-commands`.

## Risk

- **The trial fails** (likely, given the 165k to 170k compactions at a 300000 setting). Then the CR
  stops before any code, and the owner decides (Answer 2).
- **A higher threshold, a larger context:** more tokens per call for a Driver near the end of its
  work. The price above 200,000 is not measured (Answer 6). The trial reports its spend.
- **Live reading (D4):** a board change reaches the running Drivers at their next context line.
  The `config@1` line tells the Chief of Staff.
- **The cards lose their figure:** a Driver must read the line. The quiz case guards that, and
  `context: not measured` keeps today's rule ("go on"; at the closing, hand off).

## Open questions

1. **When a threshold change applies (behaviour).** Default (D4): live, from each Driver's next
   `round`, `note`, `phase` or `stack`. The other choice: frozen when the batch opens, like the
   playbook and the timing, so a change applies only from the next batch. Default if unanswered:
   live.
2. **The QA Driver (scope).** Answer 6 names it among the Drivers, but no command it runs prints a
   context line. Default: its window is raised with the others, and it gets no threshold line and
   no card rule. The other choice: a `context:` line on a command the QA Driver runs (`order qa`
   runs on the steering side, so it would need a new reading). That would be a CLI change. Default
   if unanswered: window only.
