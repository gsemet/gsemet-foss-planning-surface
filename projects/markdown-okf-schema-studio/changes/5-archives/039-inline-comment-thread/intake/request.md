# 039 — inline-comment-thread

From backlog `P3/inline-comment-thread` (files copied here as `backlog-*` / images).

## Problem

There is no inline discussion thread anchored at a point of the document (existing chips: TODO, comment).

## Decisions (user grill, 2026-10-22 night plan)

1. Format (from the backlog intent): `<!-- THREAD` / `User (YYYY-MM-DD HH:MM):` / indented lines / ... / `-->`.
2. Decision: renders as a green chip with a speech-bubble icon; expanding it shows an admonition-like callout with the messages. Interactions: read, reply (author = git user.name, date in the same format), delete the thread. Created from the slash menu or palette at block level. Hidden with the other chips (chip toggle).
3. Existing comment/TODO chips and review threads unchanged; parsing tolerant of CRLF and trailing spaces; replying preserves the rest of the file byte for byte.

Night rules: blocked on a real product decision → apply the driver's recommendation and list it in the PR under "Décisions prises en autonomie" (Autonomous decisions).
