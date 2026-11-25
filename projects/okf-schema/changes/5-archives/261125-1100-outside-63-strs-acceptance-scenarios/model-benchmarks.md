---
title: "Benchmark of 5 Coding LLMs on a Full Multi-Surface Implementation (okf-schema)"
description: >-
  An honest comparison of 5 coding models implementing the same 1,260-line multi-surface
  specification, evaluated on speed, token cost, and real accuracy (mutation testing).
status: published
date: 2026-11-25
---

# Benchmark of 5 Coding LLMs on a Full Implementation

Five coding models implemented **the exact same change specification** end to end on the
open-source `okf-schema` repository (specifically its Python requirements-traceability CLI,
`okfreq`). This report compares their deliverables across three axes — **time**, **token cost**,
and **specification accuracy** — prioritizing measured quality (mutation testing, black-box
execution) over raw volume of code or documentation.

[TOC]

## Executive Summary

::::{grid} 1 1 3 3
:::{grid-item-card} Best Overall Balance
**Claude Sonnet 5.5**
^^^
Fastest run (~29 min active, 42 min including CI), **0 notable spec deviations**, 8/8 mutations
killed, and green CI across all 6 environments.
+++
Time 9.5/10 · Cost 5.5/10 (~$16) · Accuracy 9.0/10
:::
:::{grid-item-card} Quality Surprise
**DeepSeek V4.1 Flash**
^^^
10/10 mutations killed with very few human interventions, but at the cost of a brute-force
approach: **3 h** wall time and **4× more tokens** than the other models.
+++
Time 2.5/10 · Cost 4.0/10 (214M in) · Accuracy 8.5/10
:::
:::{grid-item-card} Key Takeaway
**Coverage ≠ Robustness**
^^^
High coverage (>95%) and a green CI are not enough: Gemini 4 Neon passed CI on the first push with
the best documentation (8/10) and 3× fewer tokens, yet killed only **5/10 mutations**.
+++
Mutation testing and doc deduplication remain essential
:::
::::

## What Was Benchmarked

### The Task: A Multi-Surface Evolution of `okfreq`

`okf-schema` provides JSON Schemas and CLI tools (`okfreq`, `okfkb`) to manage Markdown-based
requirements repositories with YAML front matter. The specification given to all 5 models (~1,260
lines, 9 normative rules, D1–D7 verification matrix) required adding a new coverage mode for
stakeholder requirements (*StRS*):

- **Declared scenarios:** a `scenarios:` front-matter field listing the main paths of an StRS
  (`S1`, `S2`…) and the transitions of an SwRS, with matching headings in the document body.
- **Two traceability verbs:** a new `@accepts_req <StRS>#S<n>` marker for acceptance tests against
  the assembled product, distinct from `@tests_req <ID>#S<n>` for unit/integration tests, producing
  **two independent counters** (*tested* and *accepted*).
- **Diagnostics and waivers:** two actionable warnings (`W003` and `W004`) and a justified waiver
  mechanism requiring a non-empty reason.
- **Strict backward compatibility:** report `format_version` 2, with **unchanged output** in both
  legacy modes (`linked-swrs` and `linked-swrs-and-validation-test`).
- **6 surfaces touched per run (~112 to 115 files):** Python engine and CLI, JSON Schemas, human
  documentation (Diátaxis), agent skills, runnable examples, and migrating the repository's own
  requirements with 12 acceptance tests running against the installed wheel.

### Evaluation Protocol

Rather than judging by lines of code or test count, each deliverable was evaluated with the same
rubric:

1. **Black-box CLI conformance:** running the spec's verification matrix (legacy modes vs. new
   mode, `okfreq new`, `validate`, `trace`, `update-coverage`, `report`) inside isolated temporary
   projects.
2. **Mutation testing:** manually injecting **8 to 10 behavior-breaking defects** one by one into
   the engine (e.g. counting `@tests_req` as accepted, suppressing `W004`, accepting a blank waiver
   reason, `retire` ignoring `@accepts_req`, altering legacy modes) to measure whether each run's
   test suite actually catches regressions.
3. **Qualitative test and documentation audit:** separating behavioral tests from duplicates,
   tautologies, and prose-coupled checks; running documented examples end to end; measuring
   documentation redundancy.
4. **Session metrics:** active duration, LLM calls, token volume (input, cache, output), and cost
   extracted directly from execution logs.

:::{important} Methodological Caveats
1. **Mid-benchmark spec refinement:** GPT-6.1 Terra ran before 5 late clarifications (`U1`–`U5`)
   were added to the specification and received two manual follow-up fixes. MAI-Code-2, Claude
   Sonnet 5.5, DeepSeek V4.1 Flash, and Gemini 4 Neon each ran in a single pass against the updated
   specification.
2. **Pricing:** costs for MAI-Code-2 and DeepSeek V4.1 Flash are estimated using fallback pricing
   rates (DeepSeek V4.1 Flash was billed at $0 on the evaluation provider). For that reason, **raw
   token volume** and **LLM call count** are shown alongside USD cost below.
3. **Mutation testing:** each independent review selected 8 to 10 mutations tailored to the
   inspected implementation; the killed/total ratio is a strong indicator of test robustness, not a
   normalized percentage score.
:::

## Summary Comparison

| Model | Time (/10) | Cost & Tokens (/10) | Accuracy (/10) | Mutations Killed | Tests / Cov. | Docs (/10) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Claude Sonnet 5.5** | **9.5** · ~29 min active (42 min total) | **5.5** · ~$16 · 57M in / 530k out · 498 calls | **9.0** · 0 notable deviations | 8 / 8 | 1,116 · 95.61% | 6.5 |
| **DeepSeek V4.1 Flash** | **2.5** · ~3h03 continuous | **4.0** · $0 billed (~$10.5 est.) · **214M in / 2.1M out** · 2,105 calls | **8.5** · minor deviations | 10 / 10 | 1,141 · 95.60% | 6.0 |
| **Gemini 4 Neon** | **7.5** · ~49 min active (55 min total) | **7.5** · ~$9.47 · **19M in** / 194k out · 170 calls | **7.0** · edge-case test gaps | 5 / 10 | 1,040 · 95.17% | **8.0** |
| **GPT-6.1 Terra** | **5.0** · ~1h43 active (14 msgs) | **8.0** · ~$4.85 · 59M in / 172k out · 426 calls | **6.5** · CLI/skills gaps | 7 / 9 | 1,086 · 95.57% | 6.0 |
| **MAI-Code-2** | **7.0** · ~54 min–1h11 | **9.0** · ~$2.9 est. · 49M in / 97k out · 259 calls | **5.5** · cov. < 95%, deviations | 6 / 9 | 1,040 · 94.96% | 6.0 |

### Scores by Axis

```vega-lite
data:
  values:
    - {model: "Claude Sonnet 5.5", axis: "Time", score: 9.5}
    - {model: "Claude Sonnet 5.5", axis: "Token Cost", score: 5.5}
    - {model: "Claude Sonnet 5.5", axis: "Spec Accuracy", score: 9.0}
    - {model: "DeepSeek V4.1 Flash", axis: "Time", score: 2.5}
    - {model: "DeepSeek V4.1 Flash", axis: "Token Cost", score: 4.0}
    - {model: "DeepSeek V4.1 Flash", axis: "Spec Accuracy", score: 8.5}
    - {model: "Gemini 4 Neon", axis: "Time", score: 7.5}
    - {model: "Gemini 4 Neon", axis: "Token Cost", score: 7.5}
    - {model: "Gemini 4 Neon", axis: "Spec Accuracy", score: 7.0}
    - {model: "GPT-6.1 Terra", axis: "Time", score: 5.0}
    - {model: "GPT-6.1 Terra", axis: "Token Cost", score: 8.0}
    - {model: "GPT-6.1 Terra", axis: "Spec Accuracy", score: 6.5}
    - {model: "MAI-Code-2", axis: "Time", score: 7.0}
    - {model: "MAI-Code-2", axis: "Token Cost", score: 9.0}
    - {model: "MAI-Code-2", axis: "Spec Accuracy", score: 5.5}
mark: bar
encoding:
  y:
    field: model
    type: nominal
    sort: ["Claude Sonnet 5.5", "DeepSeek V4.1 Flash", "Gemini 4 Neon", "GPT-6.1 Terra", "MAI-Code-2"]
    title: null
  x:
    field: score
    type: quantitative
    scale: {domain: [0, 10]}
    title: "Score (/10)"
  yOffset: {field: axis}
  color: {field: axis, type: nominal, title: "Axis"}
config:
  axis: {labelFontSize: 14, titleFontSize: 15, labelLimit: 260}
  legend: {labelFontSize: 14, titleFontSize: 15}
```

### Token Volume, Cost, and Active Time

::::{grid} 1 1 3 3
:::{grid-item-card} Token Volume
```vega-lite
width: container
data:
  values:
    - {model: "Gemini 4 Neon", tokens_m: 19.3, calls: 170}
    - {model: "MAI-Code-2", tokens_m: 48.9, calls: 259}
    - {model: "Sonnet 5.5", tokens_m: 57.4, calls: 498}
    - {model: "GPT-6.1 Terra", tokens_m: 58.6, calls: 426}
    - {model: "DeepSeek V4.1", tokens_m: 214.2, calls: 2105}
mark: bar
encoding:
  y: {field: model, type: nominal, sort: x, title: null}
  x: {field: tokens_m, type: quantitative, title: "Input (M tokens, incl. cache)"}
  tooltip:
    - {field: model, type: nominal}
    - {field: tokens_m, type: quantitative, title: "Input tokens (M)"}
    - {field: calls, type: quantitative, title: "LLM calls"}
config:
  axis: {labelFontSize: 14, titleFontSize: 15, labelLimit: 220}
  legend: {labelFontSize: 14, titleFontSize: 15}
```
+++
Gemini 4 Neon: 3× less than Sonnet, 11× less than DeepSeek
:::
:::{grid-item-card} Cost (USD)
```vega-lite
width: container
data:
  values:
    - {model: "MAI-Code-2", usd: 2.9, source: "Estimated"}
    - {model: "GPT-6.1 Terra", usd: 4.85, source: "Billed"}
    - {model: "Gemini 4 Neon", usd: 9.47, source: "Billed"}
    - {model: "DeepSeek V4.1", usd: 10.46, source: "Estimated ($0 billed)"}
    - {model: "Sonnet 5.5", usd: 16.02, source: "Billed"}
mark: bar
encoding:
  y: {field: model, type: nominal, sort: x, title: null}
  x: {field: usd, type: quantitative, title: "Cost (USD)"}
  color: {field: source, type: nominal, title: null, legend: {orient: bottom, columns: 1}}
  tooltip:
    - {field: model, type: nominal}
    - {field: usd, type: quantitative, title: "USD"}
    - {field: source, type: nominal, title: "Source"}
config:
  axis: {labelFontSize: 14, titleFontSize: 15, labelLimit: 220}
  legend: {labelFontSize: 14, titleFontSize: 15, labelLimit: 240}
```
+++
Fallback pricing for MAI-Code-2 and DeepSeek
:::
:::{grid-item-card} Active Time (minutes)
```vega-lite
width: container
data:
  values:
    - {model: "Sonnet 5.5", min: 29, note: "42 min with CI"}
    - {model: "Gemini 4 Neon", min: 49, note: "55 min with CI"}
    - {model: "MAI-Code-2", min: 54, note: "1h11 total session"}
    - {model: "GPT-6.1 Terra", min: 103, note: "1h43 active, 14 msgs"}
    - {model: "DeepSeek V4.1", min: 173, note: "2h53 active (3h03 wall)"}
mark: bar
encoding:
  y: {field: model, type: nominal, sort: x, title: null}
  x: {field: min, type: quantitative, title: "Active duration (min)"}
  tooltip:
    - {field: model, type: nominal}
    - {field: min, type: quantitative, title: "Active minutes"}
    - {field: note, type: nominal, title: "Details"}
config:
  axis: {labelFontSize: 14, titleFontSize: 15, labelLimit: 220}
  legend: {labelFontSize: 14, titleFontSize: 15}
```
+++
Active agent working time excluding human waits
:::
::::

## Detailed Model Breakdown

::::{tab-set}
:::{tab-item} Claude Sonnet 5.5
**Verdict: best overall deliverable** — Time **9.5/10** · Cost **5.5/10** · Accuracy **9.0/10**

- **Strengths:** fastest execution thanks to parallel subagents (~29 min active work, 42 min
  including CI, zero human wait); **8/8 mutations killed**; no notable deviations from the
  specification (legacy modes preserved, `validate` errors printed in text mode); green CI across
  all 6 jobs (Python 3.10–3.13, macOS, Windows).
- **Weaknesses:** mid-high cost (~$16, 78% of which came from 8 subagents); some duplication
  between library and CLI tests; redundant documentation (same rules repeated across 5–6 pages).
:::
:::{tab-item} DeepSeek V4.1 Flash
**Verdict: very solid, but very slow and verbose** — Time **2.5/10** · Cost **4.0/10** · Accuracy
**8.5/10**

- **Strengths:** qualitative surprise of the benchmark; **10/10 mutations killed**; only 5 user
  interventions; only model to wire the fast acceptance test into `okf-schema`'s own suite
  (`tests/test_acceptance_export.py`).
- **Weaknesses:** compensates through brute force (~3 h continuous run, 2,105 LLM calls, 34
  compactions, 214M input tokens and 2.1M output tokens); very large diff (+7,696 lines); minor
  defects (`<main path title>` placeholder counted as a declared scenario, one empty assert,
  Windows fixes still in flight during the audit); heavily redundant docs (819 lines across two
  pages).
:::
:::{tab-item} Gemini 4 Neon
**Verdict: ultra-lean, top-tier docs, and green CI on first push, but thin edge-case tests** —
Time **7.5/10** · Cost **7.5/10** · Accuracy **7.0/10**

- **Strengths:** undisputed token-efficiency champion (**19.3M in** with 94% cache read, 194k out,
  170 calls — 3× fewer than Sonnet 5.5 and 11× fewer than DeepSeek) for ~$9.47 and ~49 min active
  work (55 min with CI); single clean commit and **green CI on the first push** across all 6
  platforms (Python 3.10–3.13, macOS, Windows); core engine conforms to Rules 1–9 (legacy modes
  preserved); **best documentation in the benchmark (8.0/10)**, clear and accurate.
- **Weaknesses:** only **5/10 mutations killed** — unit tests miss negative edge cases
  (whitespace-only waiver or exemption reasons, deprecated StRS handling, stripping
  `accepted_in_files` in legacy mode); 4 minor spec oversights (stale CLI `--help` text except
  `trace`, unfilled placeholders causing `W002` in `examples/okfreq-examples` due to a stale
  `.replace()` in `justfile`, missing heading-consistency check in `test_project_contract.py`).
:::
:::{tab-item} GPT-6.1 Terra
**Verdict: cost-effective, but incomplete and bumpier** — Time **5.0/10** · Cost **8.0/10** ·
Accuracy **6.5/10**

- **Strengths:** good cost/volume ratio (~$4.85 across 426 calls); conforming core engine; legacy
  modes preserved on `okfreq new`; documented examples verified by tests.
- **Weaknesses:** bumpier session (14 user messages, restarts, and a forgotten push); **1 mutation
  survives** (whitespace-only waiver reason accepted) and another is only caught by a repo-level
  self-test; `trace` alters legacy-mode output; CLI and skills uncovered by tests.
:::
:::{tab-item} MAI-Code-2
**Verdict: cheapest run, but too light on rigor** — Time **7.0/10** · Cost **9.0/10** · Accuracy
**5.5/10**

- **Strengths:** lowest estimated cost (~$2.9 across 259 calls, 48.9M in / 97k out); delivered in
  a single clean commit; legacy modes preserved on `okfreq new`.
- **Weaknesses:** **3 of 9 mutations survive** (`retire`, `okfreq new` pre-filling, empty waiver
  reason helper); coverage at **94.96%** (below the 95% threshold); naming mismatch
  (`tested`/`accepted` instead of `tests`/`accepts`); truncated documentation in `okfreq-cli.md`
  and inaccurate "schema-driven" claim for hard-coded text; out-of-scope edits to `CHANGELOG.md`.
:::
::::

## Lessons Learned & Recommendation

:::{tip} Selected Deliverable: **Claude Sonnet 5.5**
The best balance between proven reliability (8/8 mutations killed, 0 notable spec deviations,
green CI), execution speed (~29 min active), and controlled cost (~$16).
:::

Four takeaways stand out from running a long, multi-surface specification across five coding
models:

1. **Do not confuse volume, coverage, and quality:** all 5 models produced 10–20% weak tests
   (prose-snippet assertions, duplicates) and repeated the same rules across multiple documentation
   files (even Gemini 4 Neon, despite having the best docs at 8/10). Mutation testing was decisive:
   Gemini 4 Neon exceeded 95% coverage and passed CI on the first try, yet killed only 5/10
   edge-case mutations.
2. **Well-orchestrated parallelism drives turnaround time:** Claude Sonnet 5.5 completed all 6
   surfaces in ~29 min of active work (42 min with CI) — 2× to 4× faster than the other runs —
   without sacrificing accuracy.
3. **"Free" or low-cost models can compensate with brute-force volume:** DeepSeek V4.1 Flash
   reached a high functional bar, but consumed ~4× more tokens and 3 h of wall time, increasing
   latency and review burden.
4. **Human post-processing remains necessary for documentation:** regardless of which model's PR is
   merged, a short deduplication pass (one source of truth in the reference docs, cross-links from
   other pages) and cleanup of prose-coupled tests remain worthwhile.
