---
type: cr-answers
description: The user's answers to the grill of a Driver stopped from outside.
---

# Answers

## driver-resume-Q1: does the steering session restart it alone

2026-11-17, the user chose the recommended answer: yes, covered by the batch's go: a fresh Driver by `take <cr> --note "resume: <cause>"` with no question to the user, said in the report; the heartbeat detects a Driver recorded but stopped.

Spec critic: yes, it lets the steering session start a Driver without asking and changes the heartbeat.

## Spec questions (2026-11-17)

- resume-stop-Q2 (counting): a stop from outside does not count toward `driver ended twice` nor toward "blocked twice"; it is the host's doing; the Driver is restarted at each such stop.
- resume-stop-Q3 (which stops): only a stop the steering session did not make itself; its own `TaskStop` (a switch to Foreman mode, a drop, the user's stop or hold) is never restarted by this rule.
- resume-stop-Q4 (what is detected): the stops a compaction snapshot reports (`task_status` `killed`), plus the host's refusal of a message; the card and the host row say so. A trial records what a stop made by the user in the app leaves in the transcript.
