---
title: Spec, Foreman heartbeat matches the nested session's prompt cache
description: Exact text changes that move the nested-session Foreman heartbeat from 270 s to 600 s.
status: spec
date: 2026-11-10
---

# Spec: Foreman heartbeat at 600 s

Inputs: `01-intent.md`, `02-answers.md`, `task.md`.

## Summary

A nested-session Foreman has a 1-hour prompt cache, so its heartbeat is 600 s (10 minutes). A
driver's return or a message wakes it at once, so a longer heartbeat misses nothing. The fallback
(Foreman as a background sub-agent, background `sleep`) keeps 270 s: a sub-agent has a 5-minute
cache. "Responsiveness" keeps its 5-minute rule for messages.

One file changes: `.agents/guidelines/change-requests-lifecycle.guidelines.md` (4 places).
`AGENTS.md`, `.agents/constitution.md` and the other guidelines were searched on `origin/main` for
`270`, "5-minute", "heartbeat" and "cache": they tie nothing to the 5-minute cache (the only
other "heartbeat" hits are the extension-host file in `ci.guidelines.md`, unrelated). They do not
change.

## Places changed

### 1. Glossary, "Heartbeat" (line 27)

Current:

```text
- **Heartbeat**: the Foreman's periodic wake-up (a `/loop` every 270 seconds while a driver is
  live) to check the drivers and the merged PRs; see "Foreman session and its loop".
```

Replace with:

```text
- **Heartbeat**: the Foreman's periodic wake-up (a `/loop` every 600 seconds while a driver is
  live) to check the drivers and the merged PRs; see "Foreman session and its loop".
```

### 2. Role diagram (lines 172-173)

Current:

```text
 └─ Foreman (nested session) ── one driver per CR, in parallel; /loop heartbeat every
    270 s while a driver is live; landing
```

Replace with:

```text
 └─ Foreman (nested session) ── one driver per CR, in parallel; /loop heartbeat every
    600 s while a driver is live; landing
```

### 3. "Foreman session and its loop", bullet "Loop while a driver is live" (lines 267-272)

Current:

```text
- **Loop while a driver is live**: a driver is live when its background agent has not returned or
  a `STATUS.md` header holds its `driver:` lock with status working or wait-ci. While at least one
  is live, every heartbeat ends with `ScheduleWakeup` at 270 seconds, passing the same loop prompt
  back (`noop: true` when the heartbeat changed nothing). 270 seconds keeps the next heartbeat under the
  5-minute prompt-cache lifetime, so it reads its context from the cache instead of paying
  for it again; it is also the 4–5-minute heartbeat of "Responsiveness".
```

Replace with:

```text
- **Loop while a driver is live**: a driver is live when its background agent has not returned or
  a `STATUS.md` header holds its `driver:` lock with status working or wait-ci. While at least one
  is live, every heartbeat ends with `ScheduleWakeup` at 600 seconds, passing the same loop prompt
  back (`noop: true` when the heartbeat changed nothing). A nested session keeps a 1-hour prompt
  cache, so a 600-second heartbeat still reads its context from the cache, and waking more often
  only to keep the cache warm is waste. The Foreman wakes at once on a driver's return or a
  message, so the longer heartbeat misses nothing.
```

(The sentence "it is also the 4–5-minute heartbeat of Responsiveness" is dropped, as the owner
answered. The "Responsiveness" section itself is not edited.)

### 4. Same section, bullet "Without nested sessions" (lines 284-286)

Current:

```text
- **Without nested sessions** (another harness, or `start_session` unavailable): the Chief of Staff
  starts the Foreman as a background sub-agent, and its heartbeat is a 270-second `sleep` run in
  the background, restarted at the end of every heartbeat.
```

Replace with:

```text
- **Without nested sessions** (another harness, or `start_session` unavailable): the Chief of Staff
  starts the Foreman as a background sub-agent, and its heartbeat is a 270-second `sleep` run in
  the background, restarted at the end of every heartbeat. A sub-agent has a 5-minute prompt
  cache, and 270 seconds keeps the next heartbeat under it.
```

## Unchanged on purpose

- "Responsiveness" (line 240): "a message from its parent is read within 5 minutes" stays; a
  message wakes the Foreman at once. Its Foreman bullet already says "on its `/loop` heartbeat"
  without a value.
- "Foreman heartbeat" step 1 ("within 5 minutes of starting") is a start delay, not the cycle.
- "Supervision" stuck rule (header older than 15 minutes): 600 s leaves one full heartbeat
  inside it. No change.
- Chantier repository: not touched.

## Acceptance checks

Run on the changed file:

- `grep -n "270" .agents/guidelines/change-requests-lifecycle.guidelines.md` returns exactly two
  lines: the "Without nested sessions" bullet (`270-second` and `270 seconds`, in two lines of
  that bullet).
- `grep -n "600" .agents/guidelines/change-requests-lifecycle.guidelines.md` shows the Heartbeat
  glossary entry, the diagram and the "Loop while a driver is live" bullet.
- `grep -n "4–5-minute" .agents/guidelines/change-requests-lifecycle.guidelines.md` returns nothing.
- `grep -n "1-hour" .agents/guidelines/change-requests-lifecycle.guidelines.md` returns the loop bullet.
- `grep -rn "270" AGENTS.md .agents/constitution.md .agents/guidelines/` returns only that bullet
  in the lifecycle guideline.
- `git diff --stat origin/main` lists only the lifecycle guideline file.

## Gates (from task.md)

- `just check`.
- `just preflight`: the static stage is enough for a text change; the report says which stages ran.
- No heavy CI run. No requirements log entry. Blast radius 1: Inspector on Sonnet.
- Commit `docs:` per the commit guidelines. PR opened as a draft (`gh pr create --draft`), `gh pr
  ready <n>` only at `ready`. No issue: no `Fixes`, no issue comment.
