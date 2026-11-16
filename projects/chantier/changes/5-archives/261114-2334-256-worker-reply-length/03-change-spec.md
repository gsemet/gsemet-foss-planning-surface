# Change Specification: workers reply in an exact template, and `verdict` names its words

No issue.

## Goal

Measured on batch-16's transcripts (the spec-writer of CR-236 driver-context-budget, 2026-11-13):
`worker.md` caps a worker's reply at ten lines, yet the Coders' replies ran 93 to 105 lines (about
11,000 to 12,500 characters) and one Verifier's 69. Each long reply lands in the Driver's context
and is paid again on every later turn. Batch-17's retro (draft 6 of
`.agents/changes/batch-17-issue-drafts.md`) adds a second cost: out-of-format Inspector and Verifier
replies (`APPROVED` for `APPROVE`, a missing `head`, extra keys) on CR-228, CR-243, CR-249 and
CR-250 each cost a restart.

Wanted: the Coder, the Inspector and the Verifier know exactly what to reply, so they keep the cap
(details go to their work files and the reply names them); a reply that is only too long is read
and noted, not restarted; the Verifier's `verdict` command, when it refuses a word, says which words
it takes; the gain is measured on batch-18's transcripts.

Decisions (`02-answers.md`, 2026-11-14, WR-Q1):

- The inspector, verifier and coder sections of `worker.md` end with the exact reply template.
- An over-long reply is accepted but noted by the Driver, not restarted.
- The gain is measured on batch-18's transcripts.
- Draft 6 of batch-17's retro joins this CR (choice A): the inspector and verifier sections end with
  the exact reply template, and `verdict`'s refusal names the accepted words.

## What changes

Two cards (`skills/chantier/references/worker.md`, `skills/chantier/references/driver.md`), one CLI
message (`skills/chantier/scripts/cli/src/chantier/commands/delivery.py`) and one scenario check
(`scenario/run_scenario.py`). No hook, no type, no agent file (`agents/`,
`com.github.copilot/agents/`): the agent files name the card, the contract lives in the card.

### 1. `worker.md`, the shared paragraph (line ~20-23)

The sentence "replies in at most ten lines, or in the format its section names" stays, and gains:
details go to the worker's notes or output file, and the reply names that file rather than
repeating it. A role whose section ends with a reply template replies with that template and
nothing else (no greeting, no summary of the work, no list of what was checked and found right).

The sentence after it ("a reply out of that format is a failed worker, which the Driver starts
again") is narrowed: a reply out of format is a failed worker; a reply in format that is only longer
than its cap is read and noted ([driver](driver.md)), not restarted.

### 2. `worker.md`, "Coder": ends with its reply template

Today the section names `r<n>.md` as its output and no reply. Add, as the section's last lines, the
exact reply, at most ten lines:

```text
Round <n>: done | blocked: <one-line reason>
Notes: <work folder>/coder/r<n>.md
Gate: <command as run>: pass | fail: <first failing line>
Open: <one line> | none
```

One `Gate:` line per gate run (the fast gates named in the project's rules); `Open:` names at most
three points in one line each, the rest left to `r<n>.md`. What changed, file by file, and the
hand-over note go in `r<n>.md` only, never in the reply.

### 3. `worker.md`, "Inspector": ends with its exact reply template

The JSON example stays where it is (line ~51-53); the section's last lines restate it as the exact
reply, with the words spelled out so none is guessed:

- The reply is one JSON object and nothing around it (no prose, no code fence), with exactly the
  keys `verdict`, `head`, `blocking`, `minor`, `confidence`, and no other key.
- `verdict` is the word `APPROVE` or the word `FIX-REQUIRED`, nothing else (not `APPROVED`, not
  `FIX REQUIRED`, not lower case).
- `head` is the full 40-character SHA of `git rev-parse HEAD` in the worktree at the review; it is
  always present.
- `blocking` and `minor` are lists of strings (empty lists when there is nothing); `confidence` a
  number from 0 to 1.

The existing cap (300 characters an item, five `minor` items, 3,000 characters in all, from CR-236)
is unchanged. The "Extra review step" section already replies "with the Inspector's JSON": the
template applies to it with no new text.

### 4. `worker.md`, "Verifier": ends with its exact reply template

Today: "Reply with that word and the claims that failed." Replace it with the exact reply, at most
ten lines, as the section's last lines:

```text
VERIFIED | NOT VERIFIED
Head: <full SHA verified>
Proof: <work folder>/verifier/verify.md
Failed: <claim>: <one line why>
```

The first line is exactly one of the two words. One `Failed:` line per failed claim, none when
`VERIFIED`; past six, the sixth says `Failed: and <n> more, in verify.md`. Each claim's command and
output stay in `verify.md`, never in the reply. The section keeps its rule that `$CHANTIER verdict`
runs before the reply, and names the two words it takes: `VERIFIED` and `"NOT VERIFIED"` (quoted,
one argument, or the two words as two arguments).

### 5. `driver.md`, "A reply out of format is a failed worker" (line ~37-64)

The format checks stay as written for the Inspector (parseable JSON alone, `verdict` exactly
`APPROVE` or `FIX-REQUIRED`, `head` a commit SHA) and the other roles, with two changes:

- **Verifier:** the check also reads the reply's first line as exactly `VERIFIED` or
  `NOT VERIFIED`, and its `Head:` line; the rest of the check (`verify.md`, its `Head:` line, each
  claim's SHA, command and output) is unchanged.
- **Coder:** the check also reads the reply's `Notes:` line naming the `r<n>.md` that exists.

A new paragraph, after the restart paragraph: **a long reply is read, not restarted.** A reply in
format that only passes its cap (more than ten lines for a Coder or a Verifier; more than 3,000
characters for an Inspector or an extra review step) is acted on as any other reply, and the Driver
records `$CHANTIER note <cr> "long reply: <role>: <n> lines"` (or `<n> characters` for the JSON).
The long reply is no cause of a restart and counts as no failed worker. The brief of the role's next
start in this CR (the next round's Coder, the next Verifier) says that the last reply passed its
cap and that the details go to the work file. CR-236's line "A reply over the cap is still read"
for the Inspector becomes this general rule.

### 6. `verdict`'s refusal names the accepted words (CLI)

`skills/chantier/scripts/cli/src/chantier/commands/delivery.py`, `verdict()` (line ~32-34). Today a
word that is not a verdict raises `ChantierError('verdict <cr> VERIFIED | "NOT VERIFIED"',
EXIT_USAGE)`, which reads as a usage line and does not say what was wrong. The refusal becomes one
line that quotes the word given and names the accepted words, for example:

```text
verdict: "APPROVED" is not a verdict: the accepted words are VERIFIED and "NOT VERIFIED"
```

The exit code stays `EXIT_USAGE` (1); what is accepted does not change (`VERIFIED`, `NOT VERIFIED`,
any case, one argument or two, as `VERDICTS` and the normalisation at line 32 read them today).
The CLI still knows a verdict, not a role.

### 7. Scenario

`scenario/run_scenario.py`, the check at line ~3720-3721 ("a verdict is VERIFIED or NOT VERIFIED,
nothing else") also checks that the refusal's stderr quotes the word given (`maybe`) and names both
`VERIFIED` and `NOT VERIFIED`. No other scenario step changes.

## Out of scope

- The Investigator, Debugger, Conflict resolver and Demo explorer replies: they keep the cap and the
  format their sections name today, with no new template (see open point Q1).
- What counts as out of format for the Inspector's JSON beyond today's check (see open point Q2).
- Any CLI check of a worker's reply: the Driver judges the reply; the CLI only records `verdict`.
- The Copilot host: the cards are shared by both hosts; the measure reads Claude Code transcripts
  only, since Copilot keeps no per-agent record.
- The Inspector cap's numbers (CR-236's), the Driver's context threshold, the restart rules of
  `concepts.md`.

## Evidence

- `just check` passes (Linux, macOS and Windows in CI).
- `just scenario` passes at the PR's head (`AGENTS.md`: a change to the CLI and the cards), with the
  extended `verdict` check of section 7.
- Before and after: `$CHANTIER verdict <cr> APPROVED` on the scenario's or a scratch batch's CR: the
  before (the CR's base) prints the usage line; the after prints the line of section 6, exit 1 both
  times. `$CHANTIER verdict <cr> verified` still records `VERIFIED` at the head.
- The Verifier quotes, with `git grep -n` at the pushed head: the three templates at the end of
  "Coder", "Inspector" and "Verifier" in `worker.md`; the "long reply" paragraph and the
  `long reply:` note in `driver.md`.
- `git diff --stat <base>..HEAD` lists only `worker.md`, `driver.md`, `delivery.py` and
  `run_scenario.py` (and the CR's archive when the project asks for it).
- Known gaps (in the PR): the gain is not proved by this PR. It is measured on batch-18's
  transcripts, after that batch: the reply length, in lines and characters, of each Coder, Inspector
  and Verifier, read from the steering session's `subagents/agent-<id>.jsonl` (each worker's last
  `assistant` text), compared with batch-16's figures (Coders 93 to 105 lines, a Verifier 69,
  Inspectors 4,307 to 9,343 characters), with the count of `long reply:` notes and of
  `restart: reply out of format:` notes in the batch's record.

## Open questions for the user

- **Q1. The other workers.** The answer names the Coder, Inspector and Verifier. The Investigator,
  Debugger and Conflict resolver keep the ten-line cap with no template (their output is a file, and
  batch-16's measure found no long reply from them). Default: unchanged. Give them a template too?
- **Q2. An extra key in the Inspector's JSON.** The template says "exactly these keys", but the
  Driver's check today restarts only on unparseable JSON, a wrong `verdict` word or a missing
  `head`. Default: an extra key alone is read and noted like a long reply, not restarted (batch-17
  restarted on it). Or is it out of format, and restarted?
- **Q3. Who measures on batch-18, and where it is written.** Default: the Chief of Staff measures in
  batch-18's retro, with the method above, and writes the figures in the retro; no card gains a
  standing measurement step. Should the retro step be written into a card instead?
