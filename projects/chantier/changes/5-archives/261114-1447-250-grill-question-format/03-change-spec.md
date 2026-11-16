# Change Specification: grill questions with a reference, context, examples and a recommendation, the same in the text and in the tool

## Goal

The user, 2026-11-14 (`intake/request.md`, in French): a grill series asks independent questions,
which is good, but jumping from one subject to the next is hard. They want, for each question, a
little more context and above all clear examples; a reference on each question; a text before the
question tool with the context, the options with examples and the recommendation, because the tool
is small, has no formatting and is long to read; and the questions and options shown the same way
on both sides: the same question, in the same order, each option starting with the same words. The
text may be richer.

This CR changes the cards only (the contract of the Chief of Staff and the Griller, and the two
host references). No CLI, no hook, no agent file, no test.

## Decisions carried from `02-answers.md`

1. **Who follows the format** (answer 1): the Chief of Staff and the Griller, for every grill and
   specification question (a specification's open questions taken to the user included). The
   Release driver keeps its short yes/no confirmations before an irreversible action.
2. **The reference** (answer 2): `<short name>-Q<n>`, the item's short name plus the question's
   number, e.g. `ready-wording-Q3`, `grill-format-Q1`; always the short name, even when the CR
   already has a number (never `CR248-Q3`). The reference names a question, not the CR: wherever
   the CR itself is named (the text's context, status, PR, `depends.json`), it keeps its name as
   `skills/chantier/references/concepts.md` gives it, number and slug, e.g.
   "CR-250 grill-question-format".
3. **One item per call** (answers 3 and 6): never two CRs in the same call of the question tool.
   One call is about one CR or backlog item; questions about another item go in a separate call.
   A series may touch any facet of its item (scope, words, icons).
4. **Independent questions, at most 5** (answer 3): the questions of one series are independent of
   one another.
5. **The host's limit** (answers 5, 10, 11): a series holds as many questions as the host's
   question tool takes, never more than 5. The figure for each host lives in the host's reference,
   not in the general card: the user's statements are 4 on Claude Code, Remote Control included
   (it relays Claude Code's tool), and 5 on Copilot, both unproved until a trial.
6. **Without a question tool** (answers 4 and 11): only for a host or surface that truly has none
   (none is known today): the same text, and the user answers by reference in one message, e.g.
   "Q1 A, Q2 B". Not one question per message.
7. **The reference in the record** (answer 8): each answer recorded in `02-answers.md` starts with
   its reference, e.g. `9. grill-format-Q9: **Numbering.** ...`.
8. **Numbering** (answer 9): the question numbers keep counting across one item's series (a second
   series after Q1 to Q7 starts at Q8), so each reference is unique for the item's life. The list
   number of an answer in `02-answers.md` and its Q number need not match (older files, answers
   given outside a grill).
9. **The short name** (answer 12): a short name the asker picks once for the item and keeps for
   its life, not necessarily the item's folder name (this item, folder `250-grill-question-format`:
   `grill-format`). It is written at the head of `02-answers.md` as the line
   ``Short name: `<name>` ``. It is used only inside question references, never as the CR's name.
10. **At most 4 options** (answer 13): at most 4 options per question, on both sides; the asker
    keeps the 4 most plausible; the tool's own free answer ("Other") covers the rest, and the text
    says so.
11. **The recommendation is A** (answer 14): the recommended option is always option A, on both
    sides, marked "(recommended)" in the user's language.
12. **One asker per item** (answer 15): one session grills an item at a time; another session
    waits or takes another item. This is what keeps the numbering unique.
13. **"Grilled enough?"** (answer 16): the closing question follows the same format: a reference,
    options (specify, backlog, not yet) and a recommendation, after the complete restatement.
14. **The text before is always written** (answer 17, observed 2026-11-14 and corrected by the
    user): every call of the question tool is preceded by its text, without exception: each
    question's reference, its context, its options with their examples, and the recommendation.
    The user does see that text on Remote Control from a phone, by scrolling up; the fault observed
    was the asker's, who wrote it with its references for some series and not for others ("Des fois
    tu l'as bien fait (je voyais les références), des fois pas"). The form stays the short mirror
    of that text.

Derived from the request, not a new decision: the text before the tool and the tool show the same
questions in the same order with the same reference; each option starts with the same words on
both sides (`A. <words>`); the text may say more. With decision 14: the text is the full question,
the form its short mirror.

## What changes

### 1. `skills/chantier/references/chief-of-staff.md`, section "Backlog and grill"

Replace the sentence "Grill at any stage, once for all the CRs of a batch: each question carries
your recommended answer; skip the ones whose answer would not change the specification." with a
short paragraph and a subsection (e.g. "Asking the user: a series") that says, in the card's style,
with no host figure (no 4, no 5: it points to the host's reference):

- Grill at any stage, once for all the CRs of a batch, item by item: skip a question whose answer
  would not change the specification.
- **Who:** the Chief of Staff and the Griller, for every grill and specification question,
  including a specification's open questions and the closing "grilled enough?". Not the Release
  driver's yes/no confirmation before an irreversible action, nor the card's other questions (a
  release approval with "auto", a force-push question, "looks stopped"): those keep their shapes.
- **One asker per item:** one session grills an item at a time; another session waits or takes
  another item. (Grillers take no lock, `griller.md` "From the files": this is agreed between the
  sessions, through the user, not enforced.)
- **One item per call:** never two CRs in the same call of the question tool. One call is about
  one CR or backlog item; questions about another item go in a separate call. A series may touch
  any facet of its item.
- **The series:** independent questions only, as many as the host's question tool takes, never
  more than 5; the host's reference gives its figure.
- **The short name:** before an item's first series, read the head of its `02-answers.md`. With no
  ``Short name: `<name>` `` line there, pick a short name (a few words, e.g. `grill-format` for
  `250-grill-question-format`; it need not be the folder's name) and write that line at the head
  of `02-answers.md` (creating the file if needed) before the series is shown. With the line there,
  use it unchanged: the name is kept for the item's life, whoever asks next.
- **The reference:** each question carries `<short name>-Q<n>`, e.g. `grill-format-Q3`, even when
  the CR has a number. `<n>` keeps counting across the item's series: read the last reference in
  its `02-answers.md` before a new series. The list number of an answer there need not match its Q
  number. The reference names the question only: the context, and anything else that names the CR
  (status, PR, `depends.json`), names it by number and slug as [concepts](concepts.md) says
  ("CR-250 grill-question-format").
- **The text first, every time:** every call of the question tool is preceded by its text,
  without exception: the first series of an item and every later one, a single question, the
  closing "grilled enough?", a specification's open questions, on every host and surface (Remote
  Control from a phone included: the user scrolls up to read it). That message gives, for each
  question in order: its reference and the question; a short context (two or three lines: the CR
  by its name, why this point matters); the options, lettered `A.` to at most `D.`, each with a
  clear, concrete example of what it would mean in use (examples help the user most); and the
  reason for the recommendation. No call goes out without it, and never with the references left
  out of it.
- **The options:** at most 4 per question, the 4 most plausible; the text says the tool's own free
  answer ("Other", whatever the host calls it) is there for anything else. The recommended option
  is always `A.`, marked "(recommended)" in the user's language (e.g. "(recommandé)"), on both
  sides.
- **The same on both sides:** the tool then shows the same questions, in the same order, each
  starting with its reference, and the same options in the same order, each starting with the same
  words as in the text (`A. <words> (recommended)`). The form is the short mirror of the text: the
  text says more than the tool (the context, the examples, the reason); never other words, another
  order or another option.
- **No question tool** (a host or surface that truly has none; none is known today): the same
  text, ending with how to answer: by reference, in one message, e.g. "Q1 A, Q2 B" (a free answer
  is accepted as ever).
- **The record:** each answer goes into `02-answers.md` at once (as "Record at once" says),
  starting with its reference, e.g. `9. grill-format-Q9: **Numbering.** <the answer, with the
  user's words>`.
- **"Grilled enough?"** After the complete restatement ("Shared understanding", unchanged), the
  question is asked in the same format: its reference, its options (specify, backlog, not yet), the recommended one first as
  `A.` as for any question (e.g. `A. Specify (recommended)`, `B. Back to the backlog`, `C. Not yet`). The paragraph "Shared
  understanding" points to this.
- A short worked example (one item, two questions), written in English in the card, showing the
  text and the matching tool call side by side. The example's wording is the Driver's.

The rest of the section ("Record at once", the restatement before "grilled enough?") is unchanged
in substance.

### 2. `skills/chantier/references/griller.md`

- "What you do": the list of what the Griller takes from chief-of-staff's "Backlog and grill"
  names the shape of a series of questions too (one short mention); the format is not copied there.
- "In a worktree": one sentence. The Griller reads the item's short name and last reference from
  the planning folder's `02-answers.md` (the main checkout's CR folder, which it reads, as the
  section says), and writes its answers, continuing that numbering, in its worktree's
  `02-answers.md` under the same relative path, which goes to the Chief of Staff as today. If the
  item has no short name yet, the Griller picks one and writes the line in its worktree's copy.

### 3. `skills/chantier/references/hosts/claude-code.md`

- **Tools table:** a new row "Ask the user a series of questions (grill, specification)": the
  host's question tool (`AskUserQuestion`), at most 4 questions per call, at most 4 options per
  question, plus the tool's own free answer ("Other"); the reference opens each question's text
  (the tool's short header field, if used, does not need to hold it). Remote Control relays the
  same tool: the user sees the same 4-question form on the phone. Mark: the user's statements
  (2026-11-14, CR-250 answers 5 and 11), unproved; trials: one call with 4 questions shown and a
  fifth refused; the same series from the phone under Remote Control, all 4 shown. Under Remote
  Control the form shows above the conversation and the text written before it is read by
  scrolling up (CR-250 answer 17, observed): the text is written before every call all the same.
- The "Surfaces and options" table is not changed: it maps one to one to chief-of-staff.md's
  checklist of options offered to the user, and the question tool is not such an option.

### 4. `skills/chantier/references/hosts/copilot.md`

- **Preamble:** the paragraph saying the lines below moved unchanged, with no new Copilot finding,
  admits one exception: the question tool's row, a user's statement dated 2026-11-14 (CR-250
  answer 10), unproved like the rest.
- **Tools table:** a new row "Ask the user a series of questions (grill, specification)": the
  host's question tool, at most 5 questions per call, at most 4 options per question (the
  general rule), the reference opening each question's text. The tool's exact name and whether it
  has its own free answer are not recorded in this repository: the Driver names them only if a
  Copilot session or Copilot's documentation shows them, else writes "the host's question tool".
  Mark: the user's statement (2026-11-14, CR-250 answer 10), unproved; trial: one call with 5
  questions on Copilot, all 5 shown, the tool's name and its free answer recorded.

### Not changed

- `agents/` and `com.github.copilot/agents/`: a role's contract lives in the cards.
- `skills/chantier/references/driver.md` and the Release driver's confirmations.
- `skills/chantier/references/spec-writer.md`: it lists open questions; the Chief of Staff or the
  Griller asks them in this format.
- `skills/chantier/references/concepts.md`: the CR's name stays number and slug.
- `SKILL.md`'s router question (which role), session-start questions, release approvals.
- The CLI, the hooks, the tests, the scenario.

## Out of scope

- Other roles' questions to the user (answer 1).
- Grouping several items in one call (answers 3 and 6).
- A CLI tool, a hook or a lock that checks the format or the one asker per item.
- The docs and other places that mention the grill's "recommended answers":
  `docs/tutorial-claude-code.md` (lines 100-101), `docs/use-cases.md` (lines 72-73),
  `skills/chantier/references/init.md` (line 38), `docs/cr-lifecycle.svg` (line 146). They stay
  true (each question still carries a recommendation) and are not changed; none describes the
  reference, the text before the tool or the options' shape.

## Evidence

- `just check` passes (Linux, macOS, Windows), per `AGENTS.md`.
- `just scenario` passes before the PR: `AGENTS.md` asks it for a change to the cards.
- No `just mod`: nothing in `hooks/` or `types/`.
- Review checklist for the PR: every decision above (1 to 14) appears in `chief-of-staff.md`, with
  no host figure there; "The text first, every time" says the text precedes every call without
  exception and the form is its short mirror; `griller.md` points to it without copying and says which `02-answers.md`
  a Griller in a worktree reads and writes; each host reference has its Tools row with its mark
  and trials; copilot.md's preamble admits the dated statement; the "Surfaces and options" table
  of claude-code.md is unchanged; the agent files are untouched.

## Open questions for the user

None.
