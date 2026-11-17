---
title: Grill answers, Foreman heartbeat
date: 2026-11-10
---

# Grill answers

Owner's answers, 2026-11-10.

| Question | Answer |
| --- | --- |
| Heartbeat of a nested-session Foreman | 600 seconds ("Foreman met le tick a 10 min"), already applied to the running Foreman through the brief. |
| Encode it | In a CR ("Oui corrigé dans une CR"). |
| Fallback without nested sessions | Unchanged, 270 s: a background sub-agent has a 5-minute cache (Chief of Staff, from the same evidence). |
| Responsiveness | Unchanged: "a message from its parent is read within 5 minutes" still holds, since a message wakes the Foreman at once. Drop only the sentence that ties the 270 s heartbeat to it. |
| Chantier | Not touched by this CR. The same rule in Chantier goes in an issue there, opened by the Chief of Staff after the owner approves its text. |
| Tracker issue | none. |
| Run | Independent of the P2 stack (no shared file): its own PR from `origin/main`, outside the stack. Open-PR cap raised to 7 for it. |

## Scope

- One file: `.agents/guidelines/change-requests-lifecycle.guidelines.md` (Heartbeat entry,
  "Foreman session and its loop", the 270 s mention tied to "Responsiveness"). Plus `AGENTS.md` only
  if it names the 270 s (it does not today).
- Process text only; no product code, no requirements change, no heavy CI run. Blast radius 1:
  Inspector on Sonnet.
