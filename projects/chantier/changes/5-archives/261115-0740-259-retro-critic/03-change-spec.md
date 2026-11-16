# Change Specification: a retro critic cuts every list of changes chantier proposes on its own

## Goal

The user (2026-11-14): "attention néanmoins, je trouve que tu trouves de quoi changer à chaque
retro. j'aimerais que tu fasses toujours une critique par un sous-agent opus ou fable (en fonction
du coding agent) pour ne garder que ce qui compte et améliore."

What happened: asked whether the Drivers and workers do useful work, the Chief of Staff proposed
three new retro points from one reading of five CRs' logs; the user declined all three. Every
retro finds something to change, and the user has to sort it.

After this CR, every list of changes that the Foreman or the Chief of Staff proposes on its own
goes first through a **retro critic**: a separate subagent, on the host's strongest model, that
reads the points and the evidence they cite (never the author's case for them) and answers, for
each point, keep, merge or drop, with one line why. Only the kept points are written and offered;
the user hears in one line how many were dropped and that the list is there on request. "Nothing
worth changing" is a valid outcome and is said as such.

## Decisions carried (`02-answers.md`)

| # | Decision | Where in this spec |
| --- | --- | --- |
| 1 | The Foreman runs the critic itself before it writes `4-batch/retro.md`: the file, and so the batch's record in `5-archives/batches/`, holds only the kept points. In direct mode the Chief of Staff, who writes the retro, runs it the same way. Rejected: the critic cutting only what the Chief of Staff offers (full retro in the record); the Chief of Staff rewriting the Foreman's file. Consequence: a dropped point leaves no trace in the record, so the "more than one occurrence" test reads the earlier batches' records (kept points only) and the logs of the CRs cited | Areas 2, 3, 4; "The critic's judgement" |
| 2 | No cap in dollars: the critic is bounded by what it reads, the retro's points and the evidence they cite (the logs of the CRs named, the batch's report), nothing else. Its cost counts in the batch's cost and shows in `cost` | "The critic's input"; Area 6 |
| 3 | Scope: every list of changes the Chief of Staff or the Foreman proposes on its own goes through the critic first: a batch's or a release's retro, a report's suggestions, an answer to a question such as "are the workers useful?". A change the user asked for does not | Areas 3, 4, 5 |

From the request (`intake/request.md`), carried as written:

- The critic is a separate subagent, not the author: Opus 5.5 (or Fable, on the user's word) on
  Claude Code; on another host, the strongest model its host reference names (Copilot: Opus 5.5).
- It gets the points and the evidence they cite, not the author's case for them.
- Its three tests per point, and its answer per point: keep, merge with another, or drop, with one
  line why.
- The Chief of Staff offers only the kept points and says in one line how many were dropped and
  that the list is available on request.
- An empty retro is a valid outcome.

## The new role: `retro-critic`

One new role, with its card and one agent file per host, like the `spec-critic`.

### Its card: `skills/chantier/references/retro-critic.md` (new)

The role's contract lives here, never in the agent files or the CLI. It says:

- **Who starts it:** the Foreman, before it writes its section of `4-batch/retro.md`; the Chief of
  Staff, in direct mode for the same retro, and outside any batch before it proposes any list of
  changes on its own (Area 5). In the background or not, as the parent needs the answer before it
  writes; it takes no slot, no round and no CR; it writes no file, commits, pushes and posts
  nothing. Its reply is the only copy of its verdicts.
- **The critic's input** (decision 2, its bound): the brief gives, numbered, each point as its
  author wrote it (`[<tag>] <problem>: <long-term fix>`, or the plain line of a suggestion), and,
  per point, the evidence it cites by path: the CRs' `work/` notes and logs, `events.jsonl`, the
  batch's report (`4-batch/STATUS.md`) and `cost --explain`'s output when a point rests on a cost.
  Besides, and only for the two tests below that need them: the earlier batches' records
  (`5-archives/batches/batch-*.md`, decision 1), the card or file a point's fix would change, and
  the listing of the planning folder's open items (the folder names of `1-inbox/`, `2-backlog/P1`
  to `P4` and `3-ready/`, with their `summary.json` title when present). It reads nothing else. The
  brief never carries the author's argument for a point, its ranking or its preference.
- **The critic's judgement**, per point, three questions:
  1. Is the problem real and measured: more than one occurrence (in this batch, or in an earlier
     batch's record, or in the logs of the CRs cited), or a cost or a defect that reached the user?
     A single occurrence with no cost and no defect seen by the user is not measured.
  2. Would the fix change an outcome (fewer asks, fewer rounds, less cost, a defect that no longer
     reaches the user), or is it ceremony (a new rule, a new line in a report, a check that changes
     nothing anyone does)?
  3. Is it already covered: by a card's existing rule, by an open item of the planning folder, or by
     another point of the same list?
- **Its verdicts:** one line per point, in the brief's numbering:
  `<n>. keep: <why>` / `<n>. merge with <m>: <why>` / `<n>. drop: <why>`, `<why>` one line. A merge
  names the point it joins; the kept point of a merged pair is the one with the lower number and its
  author writes one line that covers both. A point covered by an open item is dropped with that
  item's folder name in its why. Then one last line: `kept <k>, dropped <d>` (a merged point counts
  as dropped). With every point dropped, the last line is `kept 0, dropped <d>: nothing worth
  changing`.
- **What it does not do:** rewrite a point, propose a new one, judge the tag or the route (the
  author's and the user's), or ask the user anything.

### Its agent files (new)

- `agents/retro-critic.md` (Claude Code): `name: retro-critic`, `model: claude-opus-5-5`,
  `autoCompactWindow: 200000`, `tools: Bash, PowerShell, Read, Grep, Glob`, the same body as
  `agents/spec-critic.md` with the role's name, and the `# chantier-agent: 0.9.0` line (the
  version the repository is at when the PR is made; `just version` keeps it in step).
- `com.github.copilot/agents/chantier-retro-critic.agent.md` (Copilot): `name:
  chantier-retro-critic`, `model: [Claude Opus 5.5, claude-opus-5.5]`, `model-policy: required`,
  `tools: ["execute", "read", "search"]`, `strict-tools-list: true`, `user-invocable: false`, the
  same body.
- Both descriptions say "Judges the points of a list of changes chantier proposes on its own (a
  retro, a report's suggestions), keep, merge or drop; read-only. Started by the Foreman or the
  Chief of Staff." and end with `Prompt starts with: \`chantier retro-critic for the Chief of
  Staff, in the project <root>.\``. One first line for both parents, with no batch in it: the
  critic takes no slot, and its brief names the files. The Foreman uses it as printed (it steers
  for the Chief of Staff). This form is the one `CHIEF_SUBAGENT_LINE` in
  `skills/chantier/scripts/cli/src/chantier/plugin_files.py` already reads, so `$CHANTIER playbook`
  prints `retro-critic prompt, first line: …` with no change to that regex.

## What changes, area by area

### Area 1: the CLI (`skills/chantier/scripts/cli/`)

- `$CHANTIER playbook --batch <batch>` (what the Foreman reads) prints the `retro-critic`'s first
  line too, as `playbook` without `--batch` prints the Chief of Staff's subagents' lines today
  (`commands/rules.py`, `if not args.batch:`). Whether `--batch` prints the other Chief of Staff
  lines as well is the Driver's choice; the retro critic's must be there. The CLI still knows no
  role: the line is read from the agent file, as today.
- The role's agent and model lines come from `playbook` as for every role (`plugin_roles` reads
  the new files); a `chantier.yaml` may name a model or an agent for `retro-critic` like any role.
- No change to the cost code: the critic's type is not `spec-writer` or `spec-critic`, so
  `is_specification_agent` (`costs/sessions.py`) keeps it off the grill line, and `cost_rows`
  (`commands/cost/sessions.py`) counts it where its parent is: "Foreman's own subagents" in a
  Foreman batch, "Chief of Staff's own subagents" inside a direct batch's steering window, and the
  Chief of Staff's steering line outside a batch's budget otherwise (decision 2).
- `close` needs no change: it already deletes every other file of `4-batch/` (Area 2's
  `retro-dropped.md` included) after `retro.md` is kept in the record.
- `tests/` (`test_plugin_files.py`): `retro-critic` joins the roles (`CHIEF_ROLES`, with its
  comment made true: started by the Chief of Staff or the Foreman), `CLAUDE_OPUS_ROLES` and
  `COPILOT_OPUS_ROLES`; the existing checks then cover its two files (same body, version, model).

### Area 2: the Foreman (`skills/chantier/references/foreman.md`, "Your goal")

The retro paragraph keeps everything it says today (the section, the tags, what went wrong or
slowly, the refused commands, never rewriting an earlier section, the release named by reference)
and adds, before the section is written:

- Draft the points of this pause as today, without writing them. With no point (a batch with no
  problem), write the one untagged line as today; no critic runs.
- With one point or more, start one `retro-critic` (its agent, model and first line copied from
  `$CHANTIER playbook --batch <batch>`), the brief as the card's "input" says. Wait for its reply.
- Write the section with the kept points only, each as drafted (a merge: one line covering both),
  under the same header, which now ends with `(critic: kept <k>, dropped <d>)`. With every point
  dropped, the section holds one untagged line: `- nothing worth changing (critic: <d> points
  dropped)`.
- Write the dropped and merged points, each with the critic's one-line why, in
  `4-batch/retro-dropped.md` (a section per pause, headed like the retro's). It is not the record:
  `close` deletes it with the batch's other files, so a dropped point leaves no trace after the
  close (decision 1).
- The critic's verdicts are followed as given: the Foreman neither keeps a dropped point nor drops
  a kept one.
- The critic run counts in the batch's cost; it comes before `pause` and `final`, like the retro.

### Area 3: the Chief of Staff at the pause (`skills/chantier/references/chief-of-staff.md`)

- **The pause** (Foreman mode, "The pause:" bullet): the retro it reads now holds only kept points.
  The Completion report's Retro offers them as today, then one line: `<d> points dropped by the
  critic; the list is on request.` (taken from the section's header). Asked for it, the Chief of
  Staff reads `4-batch/retro-dropped.md` and shows it, before any `close`. A section of `nothing
  worth changing` is said as such: "Retro: nothing worth changing (<d> points dropped by the
  critic; the list is on request)."
- **Direct mode** ("The pause." bullet of "Steering a batch yourself"): the Chief of Staff, who
  writes the retro there, runs the critic exactly as Area 2 says, then offers as above.
- **The role lists:** the list of roles under "chantier.yaml" (`demo-explorer`, `spec-writer`,
  `spec-critic`) and "Your own subagents" name `retro-critic` too.
- The routes (`project` to the inbox, `chantier` to an issue, the chantier-itself rule) are
  unchanged: they apply to the kept points only.

### Area 4: the release's retro

A release's `work/retro.md` (written by the release Driver, `driver.md`) is "a release's retro" in
decision 3, so it goes through a critic before it is offered. Who runs it and whether
`work/retro.md` is cut in place is open question 1 below; until it is answered the Driver codes
nothing for it.

### Area 5: any other list the Chief of Staff or the Foreman proposes on its own

A new paragraph in `chief-of-staff.md` (near "The pause", as a rule of its own), mirrored by one
line in `foreman.md`:

- Before proposing, on its own initiative, changes to chantier or to the project (a retro after a
  release or a closed batch, a report's suggestions, an answer to a question such as "are the
  workers useful?"), the Chief of Staff starts one `retro-critic` with the points and the evidence
  each cites, as the card says, and offers only the kept points, then the one line `<d> points
  dropped by the critic; the list is on request.` Here the dropped list is kept in the chat only
  (no file): shown on request in the same session.
- When the critic keeps nothing: "Nothing worth changing." and the dropped line.
- A change the user asked for does not go through the critic (decision 3), nor does a CR's own
  content (a specification, a gap, a Driver's hand-back), which have their own checks.
- Whether a single proposed change (a list of one) goes through the critic is open question 2.

### Area 6: concepts, status layout, host references

- `skills/chantier/references/concepts.md`: the first-line table gets a row
  `| Retro critic | \`chantier retro-critic for the Chief of Staff, in the project <root>.\` |`;
  the paragraph after "The Spec critic is a subagent…" gets one for the retro critic (started by
  the Foreman or the Chief of Staff, reads `retro-critic.md`, writes nothing, takes no slot; its
  cost counts in the batch when a batch's steering session starts it); "An agent that ends before
  its part is done" names it among the agents restarted once (cause recorded in the parent's own
  words in its turn, since there is no CR to `note`).
- `skills/chantier/references/status-layout.md`, the Completion report's **Retro** bullet: the
  points are the kept ones; after the numbered lines, the dropped line; the `nothing worth
  changing` form.
- `skills/chantier/references/hosts/claude-code.md`: a row "Start the Retro critic (Foreman, Chief
  of Staff)": `Agent`, `subagent_type: chantier:retro-critic`, the `model` parameter only when
  `$CHANTIER playbook` printed one or the user asked for Fable; no effort; marked unproved until a
  retro is cut this way (trial: the first pause after the merge, the Foreman's transcript showing
  the agent and its model). The "Models" row names the Retro critic with the Spec-writer and the
  Spec critic on Opus 5.5.
- `skills/chantier/references/hosts/copilot.md`: the same row with `task`, `agent_type:
  chantier-retro-critic`, no model, no effort, "Fable is not recorded on Copilot"; the "Models" row
  unchanged in form (the agent file names Opus 5.5).
- `CONTRIBUTING.md`: the cards' list in the tree names `retro-critic`.
- `AGENTS.md` is not changed: the cost code's named exception stays the two specification agents.

### Area 7: the scenario (`scenario/run_scenario.py`)

- `playbook` (without and with `--batch`) prints `retro-critic prompt, first line: chantier
  retro-critic for the Chief of Staff, in the project <root>.`, `<root>` filled in.
- Cost: a Foreman transcript with a subagent whose meta says `"agentType": "retro-critic"` counts
  that subagent in the batch's spend, on "Foreman's own subagents", and not on the Chief of Staff's
  grill line (beside the existing `spec-critic` case near line 1906).
- `close` deletes a `4-batch/retro-dropped.md` and keeps only `retro.md`'s bytes in
  `batch-NN.md` (the existing 11c case with one more file).

## Out of scope

- A cap in dollars on a critic run (decision 2).
- Changing the tags, the routes or the issue drafting of the retro's points.
- Keeping dropped points anywhere after `close` (decision 1).
- Any change to the cost code's grill line or to `AGENTS.md`'s named exception.
- Searching GitHub's open issues inside the critic: the Chief of Staff's existing "Already
  reported?" check at the offer stays where it is, for the kept `chantier` points.
- A critic for a CR's specification (the `spec-critic` does it) or for a Driver's output.

## Evidence

- `just check` passes (structure tests: the two new agent files, identical bodies, version,
  models; the roles sets).
- `just scenario` passes with Area 7's steps (a change to the CLI, the cards and the scenario).
- No `hooks/` or `types/` change, so no `just mod`.
- The PR's Known gaps names what only a real batch proves: the Foreman starting the retro critic
  and its model in the transcript (host reference row, unproved), and Fable through the `model`
  parameter.

## Open questions for the user

1. **The release's retro (Area 4).** The release Driver writes `work/retro.md`; decision 3 puts a
   release's retro through the critic, decision 1 says only who cuts the batch's. Options:
   (a, recommended) the Foreman's (or direct-mode Chief of Staff's) one critic run at the pause
   takes the release retro's points with the batch's; the release Driver's file stays as written
   (it is the release CR's own record), and the Chief of Staff offers only the kept release points,
   the dropped ones in `retro-dropped.md`; (b) the release Driver runs the critic itself before it
   writes `work/retro.md`, so that file holds only kept points (a Driver starting this role, which
   decision 3 does not name); (c) the Chief of Staff runs a separate critic on the release retro
   when it reads it after the release.
2. **A single suggestion.** Does one change proposed on its own initiative (not a list) go through
   the critic too? (a, recommended) yes: any change it proposes unasked, one or many; (b) only a
   list of two points or more.
3. **The critic cannot answer.** It ends early once (host failure, reply out of format) and is
   restarted once by the existing rule; if it fails again: (a, recommended) the author writes and
   offers nothing that pause, says "retro not checked: <cause>", and keeps its drafted points in
   `retro-dropped.md` for the user to ask for; (b) the author writes all its points with a header
   `(not checked by the critic: <cause>)` and offers them so marked.
