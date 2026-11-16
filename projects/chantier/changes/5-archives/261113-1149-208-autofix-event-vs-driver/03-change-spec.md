# Change Specification: Claude Desktop's Auto-fix events are left to the CR's Driver; the heartbeat's prompt names no interval

## Goal

Claude Desktop's Auto-fix sends the steering session events about a batch's PRs ("fix the CI",
"merge the base branch in") while the CR's own Driver is working on that PR. The steering session
must never act on such an event: a CR's PR is its Driver's, and the project's rules and the cards
rank above anything a host event asks. The user learns from the host reference how to turn
Auto-fix off and what an ignored event costs; the eval guide asks for it off before a real
campaign. In the same file, the heartbeat's sentence is reworded so the `/loop` prompt holds the
command only and the 30 minutes are the delay of each scheduled wake.

No tracker issue.

## Background (the evidence this CR answers)

- Batch-14 retro (`.agents/changes/5-archives/261112-1924-191-eval-kit-end-to-end-dry-run/retro.md`,
  line 10): the desktop app's Auto-fix event on PR 136 asked the steering session to fix the PR
  and merge the base branch in while the CR's own Driver was fixing it.
- Real-direct run 1 (`evals/results/real-direct-2026-11-12-run1.md`, finding 2, and "Direct mode:
  the host lines this run proved", heartbeat bullet): the app bound the 5 sandbox PRs the Drivers
  (subagents of the steering session) opened to the steering session's PR bar, Auto-fix was on
  for them, and it sent merge-conflict events for PRs #2 and #5 asking for a merge commit while
  their Drivers were rebasing. The Chief of Staff ignored them. In the same run the `/loop` skill
  read a trailing "every 30m" as a fixed cron interval, while the host reference wants each wake
  scheduled with `ScheduleWakeup` (the run armed it at 1800 s).

## What changes

Four files, all text. No CLI, no agent file, no hook, no type, no scenario check.

### 1. `skills/chantier/references/hosts/claude-code.md`: a new section "Auto-fix events"

Place it right after the section "## Heartbeat" (before "## Configuration"). It says, in the
reference's style (short sentences, each behaviour with its mark):

1. **What it is.** Auto-fix is a feature of the Claude Desktop app, not of chantier. The app
   binds a PR opened by a subagent to the session that started it (the steering session: the
   Foreman, or the Chief of Staff in direct mode) and then sends that session events about the
   PR: fix its failing checks, resolve a conflict by merging the base branch in. Cite where it was
   seen: batch-14 (PR 136) and real-direct run 1 (2026-11-12, PRs #2 and #5 of the sandbox).
2. **An event is not an order.** It is neither the user's word nor a line of the batch (`order`,
   `asks`, hand-back). The project's rules, then the cards, always rank above what a host event
   asks; a host event has no rank in that order. A CR's branch is brought up to date the
   project's way (here a rebase, `concepts.md` rule 8 and the project's rules), never by the merge
   of the base branch the event asks for.
3. **A CR with a live Driver** (the CR is `working`, its Driver recorded): the steering session
   does nothing on the PR: no fix, no merge, no rebase, no push, and no relay of the event to the
   Driver. It ends the turn at once. Why, in one line: the Driver reads its own CI and holds the
   branch, two writers on one branch race, and a relay spends messages against the host's limit
   for news the Driver already has.
4. **A CR with no live Driver** (handed back `ready` or `blocked`, waiting for the user): the event
   is only a signal. The steering session checks the forge itself (`gh pr checks`, `gh pr view
   --json mergeable`, or `glab` on GitLab). If the PR is really red or in conflict, it follows the
   card's usual route: the CR goes back to a Driver with `take <cr> --note "<why>"`
   (`foreman.md`, "Your means": a red check, or the ready PR that stopped merging with
   `--note "rebase: …"`). It never does what the event asks itself. If the forge shows nothing
   wrong, nothing is done.
5. **Both steerings.** The same rule holds for whichever session steers: the Foreman, or the Chief
   of Staff in direct mode.
6. **A PR that is not a batch's** (the user's own PR in the same session): out of chantier's rule;
   it is between the user and the app. The section speaks of a batch's PRs only.
7. **chantier never arms, disarms or unbinds the PR monitor.** No card uses the app's PR monitor
   (`mcp__ccd_pr__set_monitor`), to arm it or to disarm it, and chantier never writes the user's
   settings.
8. **The cost.** Even ignored, each event starts a turn of the steering session, which the user
   pays for.
9. **How the user turns Auto-fix off.** Written only from the app's documentation (with its link,
   marked **documented**) or from a dated trial (marked **proved**, with where and when). With
   neither, the line says the path is not known, is marked **unproved**, and names the trial that
   settles it (for instance: in the Claude Desktop app, find the setting that turns Auto-fix off
   for a session or a PR, turn it off, open a PR from a subagent, and see that no Auto-fix event
   arrives; record the labels and the date here). Never a guessed menu path: a wrong path in a
   card is worse than none. Say that turning it off also loses Auto-fix for the user's own PRs in
   that session.
10. **During a normal batch chantier stays silent** about Auto-fix: it does not ask the user to
    turn it off, has no preflight check for it and gives no "For you" line for it (chantier cannot
    see whether Auto-fix is on, and a line at every go would be noise). It only ignores the
    events as above. Only the eval guide asks for Auto-fix off, before a real campaign. A tip may
    come later, from a measure of the ignored turns' cost in a real batch.
11. **The mark of the section.** The rule (points 2 to 5) is **unproved** until the next real
    campaign shows it; name the trial: an Auto-fix event arrives on a CR's PR during a real eval
    campaign, and the steering session ends its turn with no tool call on that PR and no message
    to its Driver (a CR with a live Driver), or checks the forge and uses `take --note` (a CR with
    none).

Also, in the same file, section "Configuration" > "Allow rules", the bullet "Two rules described
here that P10 does not check" > `mcp__ccd_pr__set_monitor`: keep it, and make it say that no
chantier card uses it, to arm or to disarm, with a pointer to the new section "Auto-fix events".
Keep its existing marks.

### 2. `skills/chantier/references/hosts/claude-code.md`: the heartbeat's wording

Section "## Heartbeat", first sentence. Today:

> The Foreman (in direct mode the Chief of Staff, in its own session) runs the `/loop` skill in
> dynamic mode with `chantier status --refresh --batch <batch> --epoch <n>`, every `30m`, each
> wake scheduled with `ScheduleWakeup`.

Reword it so it gives one order only: the loop's prompt is the command `chantier status --refresh
--batch <batch> --epoch <n>` alone, with no interval in it ("every 30m" or any other); a prompt
that ends in an interval makes `/loop` take its fixed-interval mode (seen in real-direct run 1,
2026-11-12). Each wake is scheduled with `ScheduleWakeup`, 30 minutes (1800 seconds) after the
last. The interval stays 30 minutes. The rest of the section (the end with `ScheduleWakeup`
`stop: true`, `status --stop-heartbeat`, when it ends, re-arming, "Proved: same") is unchanged.
The literal string `every \`30m\`` no longer appears in the file.

### 3. `skills/chantier/references/foreman.md`: one pointer

One line in "## Your means", next to the bullet that ends "A ready PR that stopped merging is
yours to notice (…) and send back with `--note "rebase: …"`" (or as its own bullet right after
it): a host's event about a CR's PR (a request to fix it, or to merge the base branch in) is not
an order and not the user's word; your host's reference says what to do with it ([Claude
Code](hosts/claude-code.md), "Auto-fix events"). The rule itself is not restated in the card.
The Chief of Staff reads this card in direct mode, so this pointer covers direct mode too.

Constraint: `tests/test_structure.py`, `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`,
forbids the host tool names of `HOST_TOOLS` (`ScheduleWakeup`, `/loop`, `SendMessage`, …) in a
card line that does not contain `hosts/`. Keep the pointer on a line with the `hosts/` link, and
name no host tool on its other lines. "Auto-fix" is not in `HOST_TOOLS`.

### 4. `skills/chantier/references/chief-of-staff.md`: at most one pointer

At most one line in "## Steering a batch yourself" (the list of differences), saying that the
Foreman's line on a host's event about a CR's PR applies to you, with the same link to
`hosts/claude-code.md`, "Auto-fix events". Same constraint as above. If the Driver judges the
Foreman card's pointer already reaches the Chief of Staff (the section says to do what the
Foreman's card says), it may leave this card unchanged and say so in the PR; it adds no more than
one line.

### 5. `evals/README.md`: Auto-fix off before a real campaign

In "### Before you start", one bullet: on Claude Desktop, before a real campaign on the sandbox
(`full`, `real-foreman`, `real-direct`), the operator turns Auto-fix off for the operator's
session, as `skills/chantier/references/hosts/claude-code.md`, "Auto-fix events", says (link it).
Why, in one clause: its events skew the measured cost and the run's record. If that section
marks the way to turn it off unproved, the bullet says so too and does not give a path itself.
`copilot` is not concerned (Copilot has no Auto-fix); `claude-planted` is not named.

## Decisions carried from 02-answers.md

| Answer | Where |
| --- | --- |
| Live Driver: nothing on the PR, no relay, end the turn at once | §1 point 3 |
| No live Driver: a signal; check the forge; usual route with `take --note`; never do what the event asks | §1 point 4 |
| Same rule in direct mode | §1 point 5; §3; §4 |
| A PR that is not a CR's: out of chantier's rule | §1 point 6 |
| Project's rules, then the cards, above a host event; rebase, never the base merged in | §1 point 2 |
| chantier never turns Auto-fix off or unbinds PRs; no card uses the monitor | §1 point 7; the `set_monitor` bullet |
| The "turn it off" text: documented or proved, else unproved with its trial | §1 point 9; §5 |
| The eval guide asks for Auto-fix off before a real campaign | §5 |
| The heartbeat's interval stays 30 minutes; only the wording changes | §2 |
| The heartbeat fix belongs in this CR | §2 |
| `foreman.md` and `chief-of-staff.md`: at most one pointer each | §3; §4 |
| No new audit or scenario check; the section is unproved until the next real campaign | §1 point 11; Evidence |
| Gates: `just check` and `just scenario`; no `just mod` | Evidence |
| The user (2026-11-12): during a normal batch chantier stays silent; no preflight check, no "For you" line; only the eval guide asks | §1 point 10 |

## Out of scope

- chantier arming, disarming or unbinding the app's PR monitor, or writing the user's settings.
- `skills/chantier/references/hosts/copilot.md`: Copilot has no Auto-fix and its heartbeat is
  another mechanism.
- How a Driver learns of its own red CI (backlog item `driver-ci-from-pr-checks`).
- The agent files (`agents/`, `com.github.copilot/agents/`), the CLI, the mod (`hooks/`,
  `types/`).
- A preflight check, a "For you" block or any line at the go about Auto-fix.
- A new audit check or scenario check (no merge of the base branch into a CR's branch): a new
  campaign behaviour to weigh on its own.
- A change of the heartbeat's interval.

## Evidence

At the pushed head:

- `just check` passes (on Linux, macOS and Windows in CI), including
  `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`.
- `just scenario` passes (a change to the cards). No scenario step is added or changed.
- No `just mod`: nothing under `hooks/` or `types/` changes.
- A search of `skills/chantier/references/hosts/claude-code.md` for `every \`30m\`` finds nothing,
  and the heartbeat section names `ScheduleWakeup` with 30 minutes as the delay of each wake.
- `skills/chantier/references/hosts/claude-code.md` has a section "## Auto-fix events" holding
  points 1 to 11 of §1, with a mark on each behaviour; the turn-off line is marked documented
  (with its link), proved (with its date), or unproved (with its trial), never unmarked.
- `git diff --name-only origin/main` lists only `skills/chantier/references/hosts/claude-code.md`,
  `skills/chantier/references/foreman.md`, `evals/README.md`, and at most
  `skills/chantier/references/chief-of-staff.md` (plus the CR's archive files if `take` asks for
  them).
- The behaviour itself is proved by the next real campaign, not by this PR (§1 point 11).

## Open questions

None.
