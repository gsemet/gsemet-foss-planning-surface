# Cost report: deep UX review and fix campaign

This report covers the Claude Code session "Studio: Analyse UX et QA, puis fix"
(`dd375646…`, from 2026-10-08 to 2026-10-14). It includes the session's
146 subagents. Three short side sessions about this work are counted separately at the end.

## How the numbers were obtained, and their limits

- **Source.** The token counts come from the session transcripts in
  `~/.claude/projects/<project>/`, which contain the main session and one file per subagent.
  - Each API request is counted once, by message id. A streamed answer is stored as several
    records with the same id.
- **Prices.** The official Anthropic list prices on 2026-10-14
  ([pricing page](https://platform.claude.com/docs/en/about-claude/pricing)), in USD per million
  tokens:

  | Model | Input | Cache write (1 h) | Cache read | Output |
  | --- | ---: | ---: | ---: | ---: |
  | Opus 5.5 | 4 | 8 | 0.20 | 20 |
  | Sonnet 5.5 | 2 | 4 | 0.10 | 10 |
  | Haiku 5.5, prompt ≤ 100k tokens | 0.10 | 0.20 | 0.01 | 0.50 |
  | Haiku 5.5, prompt > 100k tokens | 0.50 | 1 | 0.05 | 2.50 |

  The amounts are **API-equivalent costs**. On a subscription plan the actual bill is different:
  usage counts against the plan's limits instead. The limit was hit once during this work, which
  caused a pause of about 2 hours.
- **Cache writes** are priced at the 1-hour rate, because this session ran with the 1-hour cache
  lifetime. The 5-minute rate gives a lower bound, shown under the first table.
- **Output tokens of subagents are under-recorded.** Most subagent records keep the token count
  from the start of the stream, not the final one. We therefore also estimate output from the
  stored text and tool-call arguments, at 3.6 characters per token.
  - Thinking text is not stored, so this estimate is a floor.
  - The main session's records hold final counts.
  - Output is a small share of the total (see below), so this uncertainty moves the total by a
    few percent at most.
- The input, cache-write and cache-read counts are exact.

## Totals

| Model | Requests | Input | Cache write | Cache read | Output (recorded) | Output (estimated) | Cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Opus 5.5 | 3,379 | 6,940 | 13.1 M | 605.1 M | 1,731,629 | 2,000,255 | $266.14 |
| Sonnet 5.5 | 2,062 | 4,188 | 11.3 M | 217.5 M | 56,173 | 534,560 | $72.14 |
| Haiku 5.5 | 482 | 964 | 1.7 M | 44.5 M | 113,031 | 209,199 | $2.33 |
| **Total** | 5,923 | 12,092 | 26.1 M | 867.1 M | 1,900,833 | 2,744,014 | **$340.61** |

With 5-minute cache writes instead of 1-hour ones, the total would be $284.08.

**Where the money goes.** Most of the cost is context, not generated text:
cache writes about $151 (44 %), cache reads about $144 (42 %), generated output about $46 (13 %). Agentic work re-reads its whole context on every tool call. In this session that
meant 867 million cache-read tokens, against 2.7 million generated tokens.

| Where | Model | Requests | Cost | Share |
| --- | --- | ---: | ---: | ---: |
| Orchestrator (main session) | Opus | 1,705 | $163.06 | 48 % |
| Subagents: reviewer | Opus | 1,150 | $73.69 | 22 % |
| Subagents: implementer | Sonnet | 2,046 | $71.77 | 21 % |
| Subagents: replay | Opus | 364 | $17.98 | 5 % |
| Subagents: visual review | Opus | 107 | $9.21 | 3 % |
| Subagents: implementer | Haiku | 482 | $2.33 | 1 % |
| Subagents: other | Opus | 53 | $2.21 | 1 % |
| Subagents: replay | Sonnet | 16 | $0.37 | 0 % |

The orchestrator is the main session, running Opus. It ran the QA campaign itself, wrote the plan,
gated every task, and is half of the cost.

Orchestrator cost by phase (Opus):

| Phase | Requests | Cost |
| --- | ---: | ---: |
| QA campaign (parts 1 and 2) and the QA skill | 370 | $45.61 |
| Fix plan writing | 126 | $22.64 |
| T00–T06 (Haiku implementers) | 183 | $11.86 |
| T07–T39 (Sonnet implementers) | 685 | $54.88 |
| T40 final verification | 73 | $4.83 |
| T41–T43, T30, T33, T34, final replay, wrap-up | 268 | $23.06 |

## Haiku or Sonnet as implementer: what this campaign shows

T00–T06 were implemented by **Haiku**, which was the user's initial choice. After T06 the user
switched to **Sonnet** for T07 onwards (decision D-12). The reviewer was Opus throughout.

| | Haiku (T00–T06) | Sonnet (T07–T43) |
| --- | ---: | ---: |
| Tasks done | 7 | 35 |
| Passed review in round 1 | 1 of 7 | 22 of 35 |
| Implementation rounds per task | 2.14 | 1.49 |
| Blocker + major review findings per task | 2.0 | 0.5 |
| Implementer cost per task | $0.33 | $1.89 |
| Reviewer (Opus) cost per task | $5.61 | $0.93 |
| Orchestrator cost per task (time window) | $1.09 | $1.99 |
| **Total per task, mean** | **$7.03** | **$4.81** |
| Total per task, median | $8.07 | $2.52 |

Median working time per task, with idle and limit pauses removed: Haiku about **42 min**, Sonnet
about **21 min**.

### What is clearly due to the model

- **Quality on the first try.**
  - Haiku passed review in round 1 on 1 task of 7; Sonnet did so on 22 of 35.
  - Haiku needed 2.1 rounds per task on average; Sonnet needed 1.5.
  - Haiku's code drew 2.0 blocker or major findings per task; Sonnet's drew 0.5.
- **The kind of defects.** Haiku's blockers were silent data-corruption edge cases:
  - a YAML comment duplicated, or a block-scalar header comment deleted (T05);
  - a stray `\r` written into CRLF documents (T05);
  - a new field inserted between a field and its own comment lines, or, after removing the only
    field, an empty frontmatter block that the extension itself rejects (T06);
  - in tables without leading or trailing pipes, an empty first or last cell losing its
    delimiter, so the row no longer split back into the same cells (T04).

  Opus caught every one of them in review. Without a strong reviewer they would have shipped.
- **Token volume per agent was similar.** Haiku used 32 requests and 3.0 M cache-read tokens per
  implementer agent; Sonnet used 41 and 4.3 M.
  - The Haiku agents are cheap mainly because Haiku's price is about 20 times lower.
  - Priced at Sonnet rates, the same Haiku tokens would have cost $13.45 instead of $2.33.
  - 185 of the 482 Haiku requests went over 100k prompt tokens, so they paid Haiku's
    long-context price.

### What is not a fair comparison

- **Reviewer effort changed at the same time.**
  - The Haiku-phase reviews ran at normal effort: $2.46 and 41 requests per review.
  - The Sonnet-phase reviews ran at low effort: $0.66 and 10 requests per review.
  - Most of the gap in reviewer cost per task ($5.61 against $0.93) therefore comes from this
    switch, not from the implementer.
  - Re-pricing the 16 Haiku-phase reviews at the low-effort rate gives about **$1.5 for reviews
    per task**, so about **$2.9 per task** in total. That is close to Sonnet's median of $2.52.
- **The tasks differ.**
  - T00–T06 were the test infrastructure and the two hardest correctness tasks (minimal patches of
    Markdown tables and YAML).
  - Sonnet also struggled on its hardest tasks. T29 was blocked after 3 rounds; its design was
    later replaced (T43). T32, T34 and T39 needed 2–3 rounds.
- **Seven tasks is a small sample**, and the orchestrator's process was still settling during the
  first tasks.

### Verdict

- **On cost, Haiku saves little once the whole loop is counted.** Its implementer saving is about
  $1.6 per task (Haiku $0.33, Sonnet $1.89). The extra review rounds and orchestrator time it
  causes eat that saving: with the same reviewer effort, a Haiku task costs about as much as a
  Sonnet task.
- **On quality and time, Sonnet is clearly better here.**
  - It passed review in round 1 three times as often.
  - It had four times fewer serious findings.
  - It needed half the working time per task.
- **Haiku is only safe with a strong reviewer.** Its defects were the dangerous kind: they lose
  user data silently. For serialization and editing code, the review is what made Haiku usable,
  and the review is where the money went.
- **What worked best: Sonnet implementer and Opus reviewer at low effort.** That setup ran from
  T07 onwards: a median of about $2.5 and 21 minutes per task, with 0.5 serious findings per task,
  all fixed before commit.
- **The larger lever is the orchestrator.** It is about half of the total. Delegating more of the
  orchestration, such as gate runs and log triage, to a cheaper model would save more than any
  choice of implementer model.

## Side sessions about this work

| Session | Purpose | Model | Cost |
| --- | --- | --- | ---: |
| `5ca05972` | Read-only check: "is this long session worth it?" | Opus | $5.49 |
| `c18fdbeb` | Check that the orchestrator does not review its own work | Sonnet | $0.28 |
| `6b417e0a` | Plan how to archive the analysis after the merge | Opus | $1.76 |

**Grand total, all sessions: about $348** at API list prices.

## Reproduce

The scripts are `cost2.py` (pricing per request) and `cost_tables.py` (these tables). They read
only the local transcripts. Run:
`python3 -I cost2.py <session> out.json && python3 -I cost_tables.py <dir> <session>`.
