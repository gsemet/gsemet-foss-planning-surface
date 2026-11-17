# Token Cost of the Orchestrator, Driver, and Subagent Pattern: Weekly Analysis

Analysis dated 2026-10-26, covering all Claude Code sessions active from October 19 to 26, 2026.
It replaces the shorter version written earlier, several of whose estimates proved incorrect
once measured (see "What the Measurements Correct").

## 1. Summary

- **Total cost for the week at API rates: $1,374,** for 668 agents, including 657 subagents.
- **No uncached input tokens:** 100% of input goes through the prompt cache. The cost breaks down
  as follows: cache reads 49%, cache writes 35% (29% at 5 minutes, 6% at 1 hour), output 16%.
- **Three items account for most of the measurable waste:**
  1. **Full cache rebuilds after waits longer than 5 minutes: $234 (17%).** These mainly involve
     the orchestrator, driver, and coder waiting for CI, a long-running test, or a subagent. For
     the overnight orchestrator, this accounts for 62% of its own cost.
  2. **Long contexts reread on every turn.** Turns with more than 200k tokens of context cost
     $546 (40%). The overnight orchestrator ran with an average context of 263k tokens over
     285 turns.
  3. **Files read through the shell (`cat`, `sed -n`, `grep`) in subagents,** then carried in
     context until the end: approximately $180 in cache reads (+/- 15%).
- **For the same change size, the orchestrator -> coder -> reviewer pattern costs as much as
  the per-CR driver pattern:** a median of approximately $1.0 per 100 lines changed in both
  cases, excluding orchestration. The difference lies in **orchestration overhead,** which ranges
  from 2% to 32% of the subtree cost, depending on how the orchestrator waits.

**Recommendation:** keep the LLM orchestrator, but make it run "short and responsive":

- few turns;
- bounded context, with a handoff as soon as it exceeds 100k tokens;
- no waiting by the LLM: a script waits, then the agent restarts from a summary;
- tool outputs summarized by scripts.

Estimated savings at the same quality level: **30 to 40% of total cost.** Details are in section 6,
where each figure is tied to a measurement.

## 2. Method

**Source:** all `~/.claude/projects/**/*.jsonl` transcripts (main sessions and subagents),
filtered to messages timestamped between 2026-10-19 and 2026-10-26 inclusive.
There are 870 files, of which 668 were active during this window. The `.meta.json` files provide
each subagent's description, model, parent, and depth.

**Counting:**

- assistant messages are deduplicated by `message.id` (a message is written across multiple lines
  when streamed);
- for each message, we retain `input_tokens`, `cache_read_input_tokens`,
  `cache_creation.ephemeral_5m/1h_input_tokens`, and `output_tokens`;
- `<synthetic>` messages are excluded.

**Pricing:** Anthropic first-party rates in $/MTok, taken from the API reference.

| Model | Input | 5-min write (1.25x) | 1-h write (2x) | Cache read | Output |
| --- | --- | --- | --- | --- | --- |
| Opus 5.5 | 4.00 | 5.00 | 8.00 | 0.20 | 20.00 |
| Sonnet 5.5 | 2.00 | 2.50 | 4.00 | 0.20 | 10.00 |
| Haiku 5.5 | 0.10 | 0.125 | 0.20 | 0.01 | 0.50 |

Cost is calculated at API rates, even though these sessions ran through a subscription: that is
the question being asked.

**Classification:**

- **Role** comes from the subagent description (orchestrator, driver, coder or writer,
  reviewer or critic or auditor, analyst or inventory, other), plus the main session.
- **Workstream** comes from the subagent description and those of its ancestors.
- **Cost per CR** groups agents whose description contains "CR NNN". It is matched to the
  GitHub PR (lines added and deleted) by branch name, or by the archived `report.md` for older CRs.

**Context attribution:** each tool result of `n` tokens received on turn `i` of an agent with
`N` turns is reread `N - i` times.

- Token size is estimated at 3.2 characters per token. An image counts as 1,600 tokens.
- This model explains **86%** of measured subagent cache reads ($496 estimated versus $576
  measured). The proportions are therefore reliable to within +/- 15%; dollar amounts are
  rescaled to match the measurement.
- It does not apply to the main session, because compactions reset the context there.

**Cache rebuilds:** we count turns, excluding the first turn, where writes exceed 60% of the
context (with a context of more than 20k tokens). This is a clear signature of an expired cache.
These are cross-checked against the time elapsed since the previous turn.

**$671** cache reads + **$402** 5-min cache writes + **$85** 1-h cache writes + **$216** output


**Limitations:**

- Classification by description is heuristic: approximately 2% of cost remains in "other."
- PR size is a poor measure of difficulty. A CR involving real-window testing or root-cause
  analysis costs more per line.
- Sessions on other machines are not counted.

## 3. Where the Money Goes

The delivery figures below cover PRs merged from October 19 to 26, 2026, in the saved
`prs.tsv` export. They describe repository output, not just the CR sample in section 4.3.

| Delivery metric | Measured output | Scope and interpretation |
| --- | --- | --- |
| Total weekly cost at API rates | **$1,374** | All 668 agents active during the analysis window, including 657 subagents; API-rate equivalent, not the subscription amount paid or a cost attributed only to merged PRs. |
| Cost breakdown | **$671** cache reads + **$402** 5-min cache writes + **$85** 1-h cache writes + **$216** output | Rounded billing-category totals from section 3.3; uncached input costs approximately $0. |
| PRs delivered | **97 merged PRs** | Includes product, tests, documentation, requirements, CI, and dependency work. |
| Lines changed | **262,284**: 206,185 added + 56,099 deleted | Sum of PR diffs across all files, including tests, documentation, requirements, and lock files; not production-code lines or unique lines changed. |
| Bug-fix deliveries | **44 PRs** titled `fix` | PR count, not individual bugs fixed; a PR can address several bugs. |
| Feature deliveries | **14 PRs** titled `feat` | PR count, not individual features; PR #11 alone groups backlog features 007 to 020 and other work. |
| Other deliveries | **39 PRs** | 22 documentation, 8 test, 4 build/dependency, 2 CI, 1 maintenance, 1 refactor, and 1 performance PR. |
| Structural refactor | **101,869 lines changed** in CR 056 / PR #51 | 57,331 added + 44,538 deleted; included in the total above, not classified as corrective rework. |
| Feature rework documented in the analysis | **3 rework rounds** for CR 084 | The CR totals 1,396 changed lines and $21.33; lines attributable only to rework were not measured. |

Delivery categories use PR-title prefixes. These figures do not establish the total number of
individual bugs or features, nor a week-wide rework rate. Summed PR diffs can count the same line
more than once and do not capture intermediate edits within a PR.

### 3.1 By Role

| Role | Agents | Cost | Share | Turns | Cache reads | 5-min writes | 1-h writes | Output |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Coder / writer | 236 | $564.9 | 41.1% | 11,559 | 1,474 M | 55.7 M | 0 | 6.31 M |
| Main session (human) | 11 | $218.2 | 15.9% | 2,703 | 475 M | 0 | 10.6 M | 1.93 M |
| Reviewer / critic / auditor | 248 | $212.1 | 15.4% | 5,050 | 522 M | 23.9 M | 0 | 3.12 M |
| Analyst / inventory | 44 | $185.2 | 13.5% | 2,706 | 539 M | 18.5 M | 0 | 2.88 M |
| Orchestrator | 24 | $99.6 | 7.2% | 1,027 | 188 M | 21.0 M | 0 | 0.70 M |
| Driver | 50 | $67.5 | 4.9% | 1,555 | 99 M | 10.6 M | 0 | 0.36 M |
| Other | 55 | $25.7 | 1.9% | 797 | 56 M | 3.4 M | 0 | 0.42 M |

Opus subagents account for **$369 (27%),** across 109 agents. These are mainly coders from the
"per-CR driver" period (CRs 041 to 051, S stages of CR 056) and the driver for CR 056.

### 3.2 By Workstream

| Workstream | Cost | Agents |
| --- | --- | --- |
| Requirements base (CRs 059 and 060: writers, analysts, critics, reduction) | $665.8 (48%) | 363 |
| CR pipeline, from backlog to PR (overnight stacks, CRs 023 to 104) | $248.3 (18%) | 197 |
| Main session | $218.2 (16%) | 11 |
| CR 056 refactor, stages S1 to S8 (Opus driver) | $152.3 (11%) | 27 |
| Deep-UX correction plan (T#, P#) | $67.2 (5%) | 48 |
| Miscellaneous | Approximately $22 (2%) | 22 |

### 3.3 By Billing Category

| Category | Cost | Share |
| --- | --- | --- |
| Cache reads | $671 | 49% |
| 5-min cache writes | $402 | 29% |
| 1-h cache writes (main session) | $85 | 6% |
| Output | $216 | 16% |
| Uncached input | Approximately $0 | 0% |

The cache is already working: almost no input is paid for at the full rate. The lever is therefore
not "enable caching." It is to **reduce the number of turns multiplied by context size,** and to
**prevent cache expiration.**

### 3.4 By Context Size at the Time of the Turn

| Context | Turns | Approximate cost |
| --- | --- | --- |
| < 50k | 3,089 | $94 |
| 50 to 100k | 8,478 | $275 |
| 100 to 200k | 8,300 | $426 |
| 200 to 400k | 5,020 | $471 |
| > 400k | 463 | $75 |

The 5,483 turns above 200k tokens, or 21% of turns, cost $546, or 40%.

## 4. Measured Findings

### 4.1 The Cache Expires During Waits ($234, 17%)

| Role | Total writes | Cold start | Incremental | Rebuilds | Rebuild cost |
| --- | --- | --- | --- | --- | --- |
| Coder / writer | $178 | $14 | $86 | 147 | $78 |
| Main session | $85 | $4 | $35 | 31 | $45 |
| Reviewer | $70 | $12 | $46 | 30 | $11 |
| Orchestrator | $54 | $2 | $5 | 83 | **$48** |
| Analyst | $48 | $3 | $26 | 25 | $20 |
| Driver | $41 | $4 | $7 | 93 | **$31** |

**The delay before rebuilding confirms the cause:**

- 124 of the 147 coder rebuilds occur 5 to 15 minutes after the previous turn, the time needed
  for a `just preflight` or a real-window test suite.
- Orchestrator and driver rebuilds occur 5 to 60 minutes later, the time needed for CI or a
  subagent.
- Main-session rebuilds occur after more than an hour, while the user is away.

**The overnight orchestrator case ("Orchestrator P1+P2 stacked PRs"):**

- 285 turns, average context of 263k tokens, maximum of 453k, duration of 12.9 h;
- own cost of $40.03, including **$24.7 in rebuilds (62%),** $12.9 in reads, and $1.5 in output.
  $32.5 was spent with a context above 200k.

By contrast, "Orchestrator night run" managed 43 agents ($44.9 subtree cost) in 14 turns, with
an average context of 57k, for **$0.76 in own cost.** This proves that the same role can cost
50 times less depending on how it waits and coordinates.

### 4.2 Orchestration Overhead Ranges from 2% to 32%

| Orchestrator or driver | Own cost | Subtree | Overhead | Turns | Max context | Duration |
| --- | --- | --- | --- | --- | --- | --- |
| Orchestrator P1+P2 stacked PRs (Sonnet) | $40.03 | $123.43 | 32% | 285 | 453k | 12.9 h |
| Orchestrator L: PR #62 reduction (Sonnet) | $25.11 | $109.59 | 23% | 231 | 494k | 3.5 h |
| Driver CR 056 S1..S8 (Opus) | $20.39 | $152.33 | 13% | 96 | 211k | 8.6 h |
| Orchestrator K: requirements batch 3 (Sonnet) | $16.84 | $245.97 | 7% | 139 | 417k | 11.1 h |
| Orchestrator night run (Sonnet) | $0.76 | $44.87 | **1.7%** | 14 | 81k | 7.1 h |
| Orchestrator D: CR 056 (Opus) | $0.73 | $153.06 | **0.5%** | 10 | 57k | 8.6 h |

Low-cost orchestrators delegate entire batches and sleep until notified. Expensive ones run
`git`, `gh`, polls, and reads themselves, and keep everything in their context. For example, the
P1+P2 orchestrator made 208 Bash calls, including 35 shell file reads, 34 git commands, and 18 polls.

### 4.3 Cost per CR at the Same Change Size

| Pattern | CRs | Median cost | Median lines | $ / 100 lines (median) | Total | Total lines |
| --- | --- | --- | --- | --- | --- | --- |
| Per-CR driver (CRs 023 to 060) | 29 | $5.70 | 551 | **$1.06** | $237.4 | 22,414 |
| Overnight stack, orchestrator -> coder -> reviewer (CRs 062 to 103) | 40 | $1.24 | 104 | **$1.02** | $83.4 | 7,793 |

These figures exclude the CR 056 refactor (101,869 lines) and do not include orchestrator overhead.
Adding it brings the overnight stack to approximately $2.2 per CR, including $0.93 in orchestration
for 43 CRs.

At the same change size, the cost per line is the same: **the pattern is not the problem; how it
is operated is.**

- **The per-CR driver costs slightly less than $1 per CR at the median,** but adds a layer of
  context and waiting for each CR.
- **CRs involving real VS Code cost $2 to $6 per 100 lines:** 041 (1.91), 044 (2.18),
  047 (2.14), and 048 (5.77). These involve real-window tests, investigating flaky tests, and
  long waits.
- **The table handle (CR 084) cost $21.33,** for 1,396 lines and 3 rework rounds, because of two
  specification changes along the way: adding `{list-table}` support, then handles outside the
  table.

### 4.4 What Subagent Context Contains

Of the $576 in subagent cache reads:

| Content | Share (model, +/- 15%) | Rescaled amount |
| --- | --- | --- |
| Base prompt: system prompt, tools, brief (approximately 34k tokens at the median on the first turn) | 30% | Approximately $171 |
| Tool results | 49% | Approximately $283 |
| Model-generated text | 21% | Approximately $122 |

**Tool result breakdown** (out of the $283):

| Source | Share | Amount | Calls | Average size |
| --- | --- | --- | --- | --- |
| Bash, file reads (`cat`, `sed -n`, `grep`, `ls`, `find`) | 63.6% | Approximately $180 | 11,000 | 1.5k tokens |
| Bash, other commands | 14.5% | Approximately $41 | 4,770 | 1.1k |
| Read (excluding `src/` and rules) | 6.1% | Approximately $17 | 283 | 5.7k |
| Read `src/` | 3.3% | Approximately $9 | 56 | 7.0k |
| okfreq | 3.2% | Approximately $9 | 1,427 | 1.0k |
| git | 3.0% | Approximately $8 | 1,043 | 1.4k |
| Images | 0.7% | Approximately $2 | 255 | - |
| CI polls | 0.1% | < $1 | 498 | 0.1k |

**Cold starts account for only $40 (3%)** across 657 subagents. However, the 34k-token base prompt
is reread on every turn: multiplied by the number of turns, it accounts for 30%. The lever is
therefore the **number of turns,** not the number of subagents.

**Turns and tool calls per turn** are almost sequential: approximately one call per turn.

| Role | Median turns | p90 turns | Median context per turn | Context growth (last / first) |
| --- | --- | --- | --- | --- |
| Coder / writer | 32 | 110 | 112k | 3.4x |
| Analyst | 52 | 94 | 177k | 6.4x |
| Reviewer | 13 | 49 | 81k | 2.2x |
| Driver | 26 | 67 | 65k | 1.9x |
| Orchestrator | 16 | 39 | 154k | 2.3x |
| Main session | 63 | 272 | 170k | 2.1x |

Coders make 10,921 Bash calls over 11,559 turns; they rarely batch their calls.

### 4.5 The Requirements Base: Write, Then Reduce

This workstream cost **$666 (48% of the week):** $217 for writers, $185 for analysts,
$158 for critics and audits, and $90 for orchestrators. It first produced approximately 1,000
requirements, before the reduction audit retained 440 (76 StRS and 364 SwRS). The reduction alone,
orchestrator L, costs $109.6 for its subtree. This is a one-time setup cost that does not recur.
**It shows that setting granularity before generation avoids paying twice.**

### 4.6 The Main Session ($218, 16%)

- Opus 5.5 with a 1-h cache, 2,703 turns, median context of 170k tokens, maximum of 500k.
- 29 rebuilds after the user was away for more than an hour, costing $41, with an average context
  of 214k at the time of resumption.
- The 1-h cache costs $85 in writes, but avoids rebuilds for absences of 5 to 60 minutes.

### 4.7 Quality: What the Overnight Stack Missed

The overnight stack, the cheapest per CR, let **two regressions** through that only real-window
testing could detect:

1. #87 blocked messages from VS Code to the preview page.
2. #82 broke a test without normal CI detecting it.

Finding them required a bisection with 5 runs of "heavy" CI and an orchestrator restart. Any
savings must preserve this safety net, at minimum the "heavy" job at the top of every stack.

## 5. What the Measurements Correct in the Short Version

| What I wrote | What the measurement says |
| --- | --- |
| Subagent cold starts cost a lot | **False:** $40, 3%. It is the base prompt reread on every turn that matters (30% of subagent cache reads). |
| Grouping small CRs saves 20 to 30% | **Not demonstrated:** cost per line is the same for small and large CRs. Savings would come mainly from fewer waits, not fewer starts. |
| Prompt caching: 40 to 60% on input | **Already achieved:** 100% of input goes through the cache. The real problem is its **expiration** during waits (17% of the total). |
| Haiku for reviews: 10 to 15% | **Measure first:** reviews cost 15%, but they caught errors. There is a risk to accuracy, so use it only for mechanical checks, or better still, replace those with scripts. |

## 6. Recommendations, Ranked by Measured Savings and Without Loss of Accuracy

Each lever keeps the same agents and the same reviews. It changes how they wait, read, and
coordinate, not who makes the judgments.

| # | Lever | Measured baseline | Estimated savings | Risk to accuracy |
| --- | --- | --- | --- | --- |
| 1 | **No waiting by the LLM.** A script starts CI or the long-running test, waits, and hands control back with a 10- to 30-line summary. The waiting agent is either restarted fresh from `STATE.md` or kept warm. In an API harness (Agent SDK), switch to a 1-h cache or send a `max_tokens: 0` keep-alive every 4 min 30 s for waiting agents. | Subagent rebuilds: $189. Total 5-min writes: $402. | **$120 to $170 (9 to 12%)** | None: same work, cache preserved |
| 2 | **A short-running, bounded orchestrator.** It delegates batches, sleeps until notifications, and runs no git, gh, or reads itself (these commands go through scripts with summarized output). It hands off above 100k tokens. | Orchestrators and drivers: $167 in own costs. The "night run" model has 1.7% overhead, versus 32% for the P1+P2 orchestrator. | **$80 to $120 (6 to 9%)** | Low: decisions remain with the LLM, with complete state in files |
| 3 | **Targeted reads in subagents.** `grep -n` with context, `sed -n a,b`, log summaries, and check outputs truncated by script to the relevant error. Batch parallel reads in a single turn. | Shell reads: approximately $180. Other Bash outputs: approximately $41. Coder context growth: 3.4x. | **$70 to $110 (5 to 8%)** | Low if the script keeps the full output on disk for the agent to open |
| 4 | **Fewer turns, with batched calls.** A parallelism instruction and "all-in-one" scripts for routine work: checks, commit, PR, stack. | The base prompt reread on every turn accounts for approximately $171; currently about one call per turn. | **$40 to $80 (3 to 6%)** | None |
| 5 | **A fixed specification before coding features.** For CR 084, the two specification changes cost approximately 3 rework rounds. For requirements, granularity must be set before generation. | CR 084: $21.33. Requirements reduction: $109.6 subtree cost. | One-off, $10 to $100 per workstream | Positive: less rework |
| 6 | **A lightweight main session.** It delegates long reads, compacts or restarts from a summary before a long absence, and keeps Opus for judgment. | $218; $41 in rebuilds after more than an hour. | **$25 to $45 (2 to 3%)** | None |
| 7 | **The right model for each role.** Sonnet for coders and orchestrators. Opus only for root-cause analysis and bisection, and for the human session. Haiku only for mechanical checks, which scripts already do better. | Opus subagents: $369 (27%). At the same change size, the overnight stack (Sonnet) costs as much per line as the Opus-and-driver era. | To be measured: up to 30% of Opus coder cost | **Medium:** validate on 10 CRs before generalizing |

**Total for levers 1 to 4 and 6, without changing models: approximately $335 to $525 out of $1,374,
or 24 to 38%.** These levers partially overlap: fewer turns also mean fewer expirations. I
therefore retain **30 to 40%** as a conservative range with lever 7, and 25 to 30% without it.

## 7. Preserving Orchestrator Flexibility

- **The LLM keeps:** triage, task breakdown, product decisions, root-cause analysis, deviations
  from the plan (a CR removed from the stack, a fix added on top), coding, and review.
- **Scripts take over:** CR and worktree creation, brief assembly, checks with summarized output,
  commits and PR body checks, `gh stack` (without ever renaming an open branch), waiting for and
  summarizing CI (`ci-triage`), the "heavy" job at the top of the stack, and archiving.
- **Each script step can be skipped or rerun by the orchestrator** (`--from`, `--skip`). A script
  failure hands control back with its summary; it never silently fixes anything.
- **For nonstandard work** (research, feature development, bisection), the orchestrator
  coordinates freely, subject only to rules 1 to 3: no LLM waiting, bounded context, summarized
  outputs.

## 8. Rollout and Measurement Plan

1. **Keep this analysis script as a tool.** It is copied into `.agents/changes/cost-analysis/`
   (`analyze.py`, `roles.py`, `deep.py`, `rebuild.py`). Move it into `scripts/` to version it.
   It is sufficient to track weekly cost by role, per CR, and per 100 lines, as well as the
   rebuild rate.
2. **Write the waiting and summary scripts** (`ci-triage`, `cr-gates`, `cr-wait`), then add the
   "no LLM waiting" rule and the handoff at 100k to the change-requests-lifecycle guideline.
3. **Run another stack of 10 CRs and compare it with this week's baseline,** using these metrics:

   | Metric | Baseline | Target |
  | --- | --- | --- |
   | Orchestration overhead | 32% | < 5% |
   | Rebuild cost | 17% of total | < 5% |
   | Cost per 100 lines | $1.02 | Stable or decreasing |
   | Regressions detected by the "heavy" job | 2 | 0 |

4. **Only then test lever 7** (model by role) on a sample, with the same test safety net.
