---
title: Foreman heartbeat matches the nested session's prompt cache
description: The Foreman heartbeat assumes a 5-minute prompt cache; a nested session has a 1-hour cache, so the heartbeat moves from 270 s to 600 s.
status: request
date: 2026-11-10
issue: none
---

# Foreman heartbeat matches the nested session's prompt cache

> [!NOTE]
> Owner's request, 2026-11-10 (23:45), during the QA 271 P2 stack run: "Foreman met le tick a
> 10 min", then "Oui corrigé dans une CR". Process guideline only, no product code.

## What was found

The process guideline sets the Foreman heartbeat at 270 seconds "to keep the next heartbeat under
the 5-minute prompt-cache lifetime" (section "Foreman session and its loop", and the Heartbeat
glossary entry). That holds for a sub-agent, not for the Foreman: the Foreman is a nested session,
and a nested session uses a 1-hour prompt cache.

Evidence from the current run's transcripts (Foreman session `6087e976…`):

| Agent | Cache writes, 1 hour | Cache writes, 5 minutes |
| --- | --- | --- |
| Foreman, nested session (1148 requests) | 1.77 M tokens | 0 |
| Its sub-agents (drivers, coders, Inspectors) | 0 | 31.7 M tokens |

The Foreman's own `ScheduleWakeup` tool says the session uses a 1-hour cache and that waking up
only to keep the cache warm is waste. The run made 239 wake-ups at 270 s, most with nothing new,
and each one sent the Chief of Staff a note.

## The request

- The Foreman heartbeat is 600 seconds (10 minutes) when the Foreman is a nested session.
- The reason in the guideline is the right one: a nested session keeps a 1-hour cache, and the
  Foreman wakes at once on a driver's return or a message, so a longer heartbeat misses nothing.
- The fallback without nested sessions (Foreman as a background sub-agent, a background `sleep`)
  keeps 270 seconds: a sub-agent has a 5-minute cache.
