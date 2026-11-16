# Change Specification: a CR's new readiness ask supersedes its earlier one

## Goal

When the Foreman records a new readiness ask for a CR, the CLI marks the earlier unread readiness
ask of that same CR as read, so the Chief of Staff relays only the latest one. In batch-18 each
restack sent a second `ready-to-merge` ask for the same CR (six pairs: A-10/A-15, A-11/A-18,
A-12/A-17, A-13/A-20, A-14/A-19, A-16/A-21), and 17 asks were left unread (45 in batch-17).

Source: batch-18's retro, kept by the retro critic and by a Fable review. The fix is the user's
choice ("oui les 6", then "lance le tout dans le batch actuel").

## Decisions carried from `02-answers.md`

1. The fix is the one in `intake/request.md`: a CLI change to `asks` (`batch_status.py`, and
   `record_ask`) plus one line in `foreman.md`.
2. It works the same on both hosts (Claude Code, GitHub Copilot) and both forges (GitHub,
   GitLab). Any card line that describes a path not proved on Copilot or on a real GitLab carries
   the mark "unproved". This change has no host path and no forge path: the CLI reads only the
   ask's text and the batch record, and the Foreman's card line is the same on both hosts. So the
   `foreman.md` line carries no "unproved" mark. A Driver who finds a host or forge dependency adds
   the mark.
3. Place in the stack: fifth, beside early-conflicts. This is the Foreman's to apply when it
   takes the CR. It changes nothing in the code.
4. `question` and `blocked` asks are never superseded. Rule 1 below goes further: they never
   supersede another ask either, because only a readiness word triggers the rule.

## What changes

### 1. The rule (CLI)

These are the readiness words. They are the first word of an ask's text, as `foreman.md` lists
them:

- Per-CR family: `ready-to-merge`, `pr-in-draft`, `ready-locally`. The ask's key is the CR named by
  the second word: `ready-to-merge CR-261 board-cr-step <link> …`. The word goes through
  `chantier.core.ids.normalize_cr`, so `CR-261`, `cr-261` and `261` give the same key. It counts
  only when the result is the id of a CR in the batch record (`b.record.crs`).
- Stack family: `stack-ready-to-merge`. Its key is the batch, because a batch has one stack at a
  time ("after a partial merge, what remains is another stack of the same batch", `foreman.md`). It
  does not take the CRs in its `<cr>=<link>` pairs as keys (see open question 1).

When `chantier asks "<text>"` records a new ask whose first word is a readiness word and whose key
resolves, every earlier ask that meets all three conditions below is marked read:

- it is unread (`read` is null);
- its first word is in the same family as the new ask's first word (a `pr-in-draft` replaces an
  earlier `ready-to-merge` of the same CR, and the other way round);
- it has the same key.

Marking it read works as it does for `asks --read` today: `read = now()`.

Nothing else is superseded:
- an ask whose first word is not a readiness word (`question`, `blocked`, `refused`, `budget`,
  `merged`, `released`, `heavy-ci`, `autosync …`, free text) neither supersedes nor is superseded;
- a readiness ask whose key does not resolve (no CR word, or a CR not in the batch) supersedes
  nothing and is recorded as it is today;
- an ask that is already read is never touched.

The rule matches on the first word exactly. Case-folding and stripping of a leading icon are left
to the Driver's judgment (asks start with the word today; `foreman.md` says an ask's icon, when it
has one, is the CR's state). If the Driver allows a leading icon, a scenario check covers it.

### 2. Code

- `skills/chantier/scripts/cli/src/chantier/rails_release.py`, `record_ask(b, text)`:
  - Work out the new ask's family and key with a small pure helper, for example
    `readiness_key(text, crs) -> tuple[str, str] | None`, which returns `("cr", "CR-261")`,
    `("stack", "")` or None. It can live beside `record_ask` or in a module of the Driver's
    choice. The CLI stays free of roles: the helper reads words, not agents.
  - Before it appends the new ask, find the earlier unread asks with the same family and key, and
    set `read = now()` on each.
  - Log the new ask with its CR: `b.log("ask", <the CR id or None>, ask=aid, text=text)`. Today the
    CR is always None, which is why every ask event carries `"cr": null`. A per-CR readiness ask now
    carries its CR, and the board's events (`board/state.py`, kind `ask`) can tie it to the CR.
  - When it superseded anything, log
    `b.log("asks-read", <cr or None>, asks=[<ids>], superseded_by=aid)`. This is the "superseded by
    A-n" line of the request. The event's actor is the Foreman (the batch is opened with
    `actor="foreman"` when there is text).
  - Return the new id and the superseded ids, so the command can print them.
- `skills/chantier/scripts/cli/src/chantier/commands/batch_status.py`, `asks()`: the printed line
  `[foreman→chief-of-staff] ask A-n: <text>` stays exactly as it is, as the first line (the
  scenario's regex and the Foreman's send depend on it). When asks were superseded, a second line
  follows: `A-k superseded by A-n (marked read)`, one line per superseded ask or one line that
  lists them all, as the Driver chooses. This second line is for the Foreman. It is not sent.
- `AskRecord` (`core/records.py`) gets no new field: the state of a superseded ask is `read`, and
  the reason is in `events.jsonl`. `status`, `STATUS.json`/`STATUS.md` (`asks_unread`) and the
  board's count follow on their own, because they count `read`.
- `declare/batch_status.py`: the `asks` help text ("the Foreman's asks still unread; with text,
  record one") gains a clause such as "; a readiness ask marks the CR's earlier unread one read".
  This is optional, if it fits the help's style and length.
- Keep the functions under the project's size limits (recent commits had to split functions after
  a rebase). `just check` says where they stand.

### 3. Card: one line in `skills/chantier/references/foreman.md`

Add this to the `$CHANTIER asks "<text>"` bullet (around line 319), after the list of plain lines:

> A readiness ask (`ready-to-merge`, `pr-in-draft`, `ready-locally` for a CR, `stack-ready-to-merge`
> for the stack) marks the earlier unread one of the same CR (of the stack) read, logged
> "superseded by A-n": send the line it prints first, never the earlier ask again; `question` and
> `blocked` asks are never superseded.

The Driver may adjust the wording, but the meaning stays. No other card changes. `chief-of-staff.md`'s
"Asks" bullet already lists only what is still unread, and that stays true.

## Out of scope

- No change to how the Foreman decides to send an ask, or to the restack's own behaviour (why a
  restack re-sends `ready-to-merge`). This CR only makes the duplicate harmless.
- No supersession across families: a `stack-ready-to-merge` does not mark the per-CR readiness asks
  of the CRs it lists (open question 1), and a `blocked` or `merged` ask marks nothing.
- No new field on `AskRecord`, no new command, no change to `asks --read`, and no change to the
  board pane or the web board's drawing. The pane's `asks_unread` field keeps its meaning, so the
  AGENTS.md screenshot rule does not apply.
- No change to `chief-of-staff.md`, `routing.md`, the agent files in `agents/` or
  `com.github.copilot/agents/`, or the hooks.

## Evidence

- `just check` passes (lint, types, `just test`) on Linux, macOS and Windows. CI covers the two
  other systems.
- `just scenario` passes, because this is a change to the CLI and a card. Add scenario checks in
  `scenario/run_scenario.py`, next to the existing asks checks (around lines 6118 to 6135, the
  "the Foreman's own ask is recorded and printed" block), with `w.chantier("asks", …)`:
  1. Record `ready-to-merge <cr> <link> gaps: a`, then `ready-to-merge <cr> <link> gaps: b`. The
     second call's first output line is the usual `[foreman→chief-of-staff] ask A-n: …` line. A
     second line names the first id as superseded. `asks` lists the second ask and not the first.
  2. The `asks-read` event in `events.jsonl` names the first id with `superseded_by` equal to the
     second id. The `ask` event of the second ask carries `"cr": "<cr>"`.
  3. Record a `pr-in-draft <cr> …` after an unread `ready-to-merge <cr> …`: the earlier one is
     superseded (same family).
  4. Record `question <cr> …` and then `blocked <cr> …`, both unread, then a `ready-to-merge <cr> …`:
     both stay unread. Then a `question <cr> …` after an unread `ready-to-merge <cr> …`: the
     `ready-to-merge` stays unread.
  5. Record unread `ready-to-merge` asks for two different CRs: a new ask for one leaves the other
     unread.
  6. An earlier ask already marked read (`asks --read A-k`) is not touched again: its `read` time
     does not change.
  7. Record two `stack-ready-to-merge …` asks: the second supersedes the first.
  Make sure the existing checks still hold. In particular, "`asks` gives every ask still unread"
  expects `A-1: ready-to-merge {one} …` to be the first unread ask. If the scripted Foreman sends
  a second readiness ask for `one` before that point, adjust the check to the new behaviour; never
  weaken it.
- Optional: a small parametrized test in `tests/` for the helper `readiness_key` (word in or out of
  the families, a CR in or out of the batch, `normalize_cr` forms). It stays fast and in-process.
- Replay against batch-18's record (read-only, by hand or in a scratch copy, never in the live
  `.agents/changes/4-batch/`): with the rule, A-10, A-11, A-12, A-13, A-14 and A-16 would have
  been marked read by A-15, A-18, A-17, A-20, A-19 and A-21. Quote this in the PR's Deliverables
  as a check of the request's numbers, if the Driver can run it cheaply.

## Self-containment notes for the Driver

- Ask texts look like this in batch-18's `batch.json`:
  `ready-to-merge CR-261 board-cr-step https://github.com/gsemet/chantier/pull/208 gaps: …` and
  `stack-ready-to-merge <stack link> partial stack mergeable below <sha7> <cr>=<link> … to come: …`.
- `Batch.log(kind, cr=None, **fields)` is in `core/batch.py`. Records keep unknown keys
  (`extra="allow"`), so the event's new `superseded_by` key needs no schema change.
- The scenario's scripted Foreman records asks through `Foreman.ask` (`run_scenario.py` around
  line 440: `self.w.chantier("asks", "--", *text.split(" "))`).

## Open questions

1. Should a `stack-ready-to-merge` also mark as read the earlier unread per-CR readiness asks
   (`ready-to-merge`, `pr-in-draft`) of the CRs it lists in its `<cr>=<link>` pairs? The request
   says "same CR and word family". This spec reads that as two families (per-CR and stack) that do
   not cross. In a stack batch, before the first stack exists, each CR handed back ready gets its
   own `ready-to-merge`, and the first `stack-ready-to-merge` then covers those CRs again.
   Default here: no crossing.
2. Is the key of `stack-ready-to-merge` the batch (this spec: one stack per batch at a time) or the
   stack's link (`<stack link>`, the second word)? They give different results only if a batch
   could hold two stacks with different top links whose asks are both unread. Default here: the
   batch.
