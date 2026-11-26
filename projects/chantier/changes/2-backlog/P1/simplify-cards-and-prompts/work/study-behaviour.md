# Study: what the roles really do (behaviour side)

Behaviour study for `simplify-cards-and-prompts`, 2026-11-24. Read-only: no transcript, card or
code was changed and no writing `chantier` command was run. The byte measures of the cards are
another study's; this one counts what the agents did.

## 1. Summary

1. **The safety floor holds, and it is held mostly without the cards.** In 681 Driver runs: no
   `gh pr merge`, no `git merge` (one `--ff-only` that git refused), no plain `--force` push, 428
   pushes of which the rewrites use `--force-with-lease`. One Coder commit in 515 runs. The two
   merges of the week (Foreman, Chief of Staff) were made under a recorded grant or the user's word.
2. **The format rules that the CLI or a parent checks are obeyed at 99 %; the prose-only rules
   are obeyed at about half.** Inspector verdict JSON 654/655, Verifier verdict line 679/681,
   first line of a started agent 3,472/3,484. But: `git -C <worktree>` 54 % of the Drivers' git
   commands, "change no shell's folder into a CR folder" broken in 46 % of CR Driver runs, the
   hand-back's printed line copied first in 61 % of runs, `git add -A` or `.` in 8.5 % of runs.
3. **Three CLI stumbles repeat hundreds of times and no card line stops them.** `handoff --lease`
   (about 150 refusals), `phase <cr> "gate <detail>"` as one argument (97 runs), a Driver running
   `take` (39 runs). The card says the right form each time. Each is a one-line CLI fix.
4. **Progressive disclosure already happens, by accident.** A CR Driver reads the 9 common
   sections of `driver.md` (60 to 69 % of runs) and almost never the 16 rare-case sections (7 to
   10 %, about 40 KB). Spec-writers call `summary set --help` in 88 % of their runs with no card
   telling them to. A Foreman reads 110 KB of cards before its first compaction and a median of
   0 KB after each of the next ones, and its stumble rate barely moves (3.8 % against 2.3 %).
5. **The cost is not in the card bytes alone: it is context size times turns.** A Foreman runs at
   a mean context of 182,000 to 186,000 tokens for 470 to 1,175 model calls per batch; its
   heartbeat (`/loop status --refresh`) is 37 to 64 % of its weighted tokens. Each Foreman turn
   end wakes the Chief of Staff, which answers "Noted." 59 % of the time (25 % of its weighted
   tokens in the two sessions measured). A CR takes 2.4 Driver runs on average; 22 % of Driver
   runs end on the context rule and the next Driver boots again.
6. **The host and chantier's own write guard give contradictory orders.** 490 of 577 write-guard
   refusals are scratch writes (the host's scratchpad folder, `/tmp`, `/dev/null`) that the host's
   own prompt recommends.

Section 5 turns these into 14 maintenance rules; the main one: a retro fix lands in the CLI
(accept, refuse, `next:` line, help topic), and a card line is allowed only with an id, a check
and a measured frequency.

## 2. Method and sample sizes

- Source: Claude Code transcripts (JSONL, main sessions and `subagents/`) under
  `C:/Users/gaeta/.claude/projects`, files changed since 2026-11-17, events dated 2026-11-17 to
  2026-11-24. Projects: chantier (and its worktrees), Markdown OKF-Schema Studio ("studio"), the
  planning surface, the eval workspace `real-foreman-2026-11-22`. 3,959 files, 4.26 GB.
- Role of a subagent: its `meta.json` `agentType`, else the first line of its prompt. Role of a
  main session: its title ("Foreman", "CoS", "Griller") or its skill call.
- Every tool call and its result (first 500 and last 400 characters) was indexed; counts below are
  over **all** runs of the window, not a sub-sample, unless "sample" is written. Quotes are at
  most 15 words. A reference `[project] file:line` gives the transcript and the JSONL line.
- Scripts: `index.py`, `runs.py`, `stumble.py`, `wake_tokens.py` and helpers, in the session's
  scratchpad (`.../442a4967-d0b9-4942-95c1-9bdfe82e43d3/scratchpad/behaviour/`), run with
  `python -I`. They are throwaway; rule M7 proposes their permanent form.

| Role | Runs | Tool calls per run (median) | Model calls per run (mean) | Prompt-side tokens per run (mean, cache reads included) |
| --- | --- | --- | --- | --- |
| Verifier | 682 | 10 | 10 | 0.45 M |
| Inspector | 656 | 8 | 7 | 0.24 M |
| CR driver | 576 | 40 | 36 | 2.8 M |
| Coder | 515 | 32 | 42 | 3.5 M |
| Spec-writer | 486 | 30 | 29 | 1.9 M |
| Spec critic | 245 | 27 | 24 | 1.5 M |
| Conflict resolver | 108 | 13 | 14 | 0.57 M |
| Stack driver | 73 | 33 | 30 | 2.2 M |
| Debugger | 50 | 19 | 17 | 0.85 M |
| Investigator | 44 | 24 | 22 | 1.7 M |
| Release driver | 32 | 30 | 26 | 1.8 M |
| Retro critic | 25 | 13 | 11 | 0.41 M |
| Foreman (session = one batch or more) | 12 | 462 | 560 | 100 M |
| Griller (session) | 11 | 39 | 94 | 15 M |
| Chief of Staff (session) | 7 | 810 | not window-filtered | not window-filtered |

Limits of the method are in section 6. The two largest Chief of Staff sessions began on
2026-11-05: their events are filtered to the window, their token totals are not, so no token
figure is given for that role except from the two sessions of 2026-11-22 and later (section 3.5).

## 3. Findings per question

### 3.1 What each role does, in order; what shapes it; what is read and not used

**CR driver** (576 runs). Typical order, with the share of runs that do each step:

1. Reads `startup-core.md` (90 %), `startup-manifest.json` (87 %), `role-core.md` (58 %),
   `host-core-claude-code.md` (54 %), then greps the headings of `driver.md` (62 %) and reads it
   in slices (9.7 card reads, 62 KB per run on average).
2. `rules` (78 %), then reads the project's `AGENTS.md`; `handoff` (77 %, 1.6 calls), `log` (48 %).
3. `round` (54 %), starts a Coder (58 %), an Inspector (63 %), sometimes an Investigator (8 %),
   a Debugger (8 %), a Conflict resolver (12 %).
4. `note` (79 %, 4.3 calls), `phase` (65 %, 2.9 calls).
5. Commit (60 %), rebase (48 %), `just` checks (86 %, 3.5 calls), push (59 %), `gh pr create` or
   `edit` (79 %), `ship` (69 %), `gate` (31 %), CI reads with `gh` (80 %, 4 calls).
6. Verifier (64 %), `handback` (83 %), then the hand-back message.

Card sections of `driver.md` read by CR Drivers (144 runs since 2026-11-22, line map of
`3c29dd7c`; a whole-file read counts for every section):

| Sections | Share of runs | Size |
| --- | --- | --- |
| "Means: the record and the workers", "context and your folder", "the worktree", "rebase and push", "the long gate", "CI", "commits, the PR's state and the evidence", "CR driver", "ship and proof" | 59 to 69 % | 28 KB |
| "Means: the lease", "a Driver started again" | 53 to 55 % | 3 KB |
| "Means: your end", "CR driver: the closing" | 35 to 36 % | 5.6 KB |
| The 16 rare-case "Means:" sections (a worker that fails, escalation, a remote command fails, a force push the host refuses, images, carries, hand-backs out of the ordinary, GitLab forms...) | 7 to 10 % | 40 KB |
| "CR driver: re-takes" | 11 % | 8.9 KB |
| "Stack driver", "QA driver" (other roles' sections) | 7 to 8 % | 33 KB |

Read and not acted on: the `git -C` rule and the "no `cd` into a CR folder" rule sit in "context
and your folder" (read by 62 %) and are followed about half the time (3.3). The lease rule (line
813: "pass `--lease <n>` on `round`, `ship` and `handback`") is read by 55 % and over-applied to
`handoff`, `take`, `verdict`, `rules`, `log`. "Re-takes" is read by 11 % of runs although 70 % of
CRs have a second Driver. `startup-manifest.json` (4.7 KB of JSON) is read by 87 % of Drivers;
what follows is always the same heading grep, so the manifest itself changes nothing visible.

Rules that visibly shape the CR Driver: the reply line (`[driver CR-n→foreman] hand-back ...`),
the context rule (127 runs end `blocked context`, median 117,500 tokens read from the
`context:` line that `note` prints), `--force-with-lease`, commit before the gate, the worker
first lines copied from `round`.

**Stack driver** (73 runs): `stack` (89 %, 2.7 calls), `rules` (81 %), `ship` (63 %, 2.7 calls),
`forge-stack show` (62 %), rebase (62 %, 1.8), push always `--force-with-lease` (56 % of runs,
never plain), Conflict resolver (29 %), Verifier (26 %). It reads "Stack driver" (31 KB) in 81 %
of runs and asks `--help` in 33 % of runs (`stack`, `forge-stack`, `ship`).

**Release driver** (32 runs): `rules`, `handoff`, `release` (47 %), `phase`, `just` (81 %),
`handback` (78 %). It reads "Release driver" (12.6 KB) in 78 % of runs and none of the rare-case
sections (0 %).

**Workers** (studio project only for the CLI figures, so the product under test is not chantier):
each reads its own card in 97 to 100 % of fresh runs and nothing else (Verifier, Inspector, Coder,
Conflict resolver, Debugger, Investigator), then `rules` (57 to 100 %). The Verifier also runs
`log` (66 %) and `verdict` (40 %). The Spec-writer reads its card in 61 % of runs (a resumed
writer does not), runs `summary lint` (95 %) and `summary set` (97 %), and `--help` in 88 %.
The Spec critic reads its card in 73 % of runs. No worker reads `startup-core.md` or the manifest
in more than 19 % of runs.

**Foreman** (12 sessions): per session, 47 CR Driver starts, 6 stack Driver starts, 2 release
Driver starts, 1.3 Retro critics; `agents set` 107 calls, `status` 70, `take` 59, `order done` 31,
`asks` 22, `note` 15, `lease` 13, `SendMessage` 58, `gh` reads 28, `just` 19. It is woken by an
agent's end (878 notifications), by its heartbeat (179 `/loop ... status --refresh`) and by 49
compactions. It reads 110 KB of cards before its first compaction, then a median of 0 KB per
later segment. It reads a rule just in time when an action is rare: before the release merge of
batch-31 it grepped `foreman.md` for "release go|gh pr merge", read 30 lines, ran `release go`,
then merged with `--rebase --match-head-commit` (`[chantier] c095a20c…:753-790`).

**Chief of Staff** (7 sessions): `status` 31 calls per session, `triage` 28, `file` 26, `watch`
24, `order merged` 21, `order add` 16, `summary set` 12, `asks` 11, `seat` 10; 68 Spec-writer and
34 Spec critic starts; 124 `SendMessage`; 57 `AskUserQuestion`; 47 pushes and 40 commits of the
planning surface per session by hand. It is woken 1,494 times by "the session you started
finished a turn".

**Griller** (11 sessions): `preflight` and `seat` (82 %), `summary set` (64 %), `summary lint`
(55 %), `file` and `triage` (36 %). No batch command in any Griller session: the "never opens or
runs a batch" rule holds in the sample.

Not seen in the window: QA driver, demo-explorer, board-griller.

### 3.2 Where agents stumble

Counts over all runs of the window. "CLI refusal" and "usage" count only real `chantier` calls for
the Drivers, the Foreman and the Chief of Staff; for workers of the chantier project the same
words also match the product under test, so worker CLI figures are from the studio project.

| Stumble | CR driver (576) | Stack (73) | Release (32) | Foreman (12) | Chief of Staff (7) | Coder (515) | Verifier (682) | Spec-writer (486) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CLI usage error (argparse) | 229 | 4 | 7 | 24 | 31 | - | 26 | 48 |
| CLI refusal (`error:`) | 184 | 45 | 4 | 98 | 235 | - | - | 446 |
| `--help` calls | 142 | 48 | 9 | 61 | 208 | - | - | 498 |
| `sleep` blocked by the host | 211 | 12 | 4 | 2 | 1 | 13 | 1 | 0 |
| Write guard refusal (chantier's hook) | 113 | 0 | 0 | 0 | 0 | 307 | 93 | 4 |
| Host denial (auto-mode classifier, safety check) | 15 | 6 | 2 | 3 | 21 | 16 | 7 | 2 |
| Tool not in the role's list | 4 | 0 | 0 | 0 | 0 | 22 | 29 | 95 |
| Edit before Read (host rule) | 0 | 0 | 1 | 0 | 1 | 385 | 0 | 0 |
| `gh` command failed | 105 | 10 | 3 | 6 | 35 | 3 | 41 | 3 |
| Compactions per run | 0 | 0 | 0 | 8.2 | 36 | 0.57 | 0.01 | 0.16 |

The repeated ones, with what would have prevented each:

| # | Stumble | Count | Evidence | Prevented by |
| --- | --- | --- | --- | --- |
| S1 | `handoff <cr> --lease <n>` (also `take`, `verdict`, `rules`, `log`): "unrecognized arguments: --lease" | about 150 calls since 2026-11-20 (86 on `handoff` alone), 21 to 69 per day | `[chantier] agent-afc91c82…:43` | CLI: accept `--lease` on every CR command (renew or ignore). No card line: the card already says where it goes. |
| S2 | `phase <cr> "gate preflight"`: "invalid choice: 'gate tests'" | 97 CR Driver runs | `[eval] agent-aea3d63d…:186` | CLI: split a quoted first argument on its first space. |
| S3 | A Driver runs `take`: "the steering session's command" | 39 runs | `[chantier] agent-a6a94ec8…:57` | The Driver's prompt already carries the take's facts; the refusal should add "`handoff <cr>` prints them". |
| S4 | `sleep N; cat <output>` blocked, then a Monitor, then another | 211 refusals in CR Drivers; 15 % of all CR Driver tool calls are waiting calls | `[chantier] 4ead8041…/agent-abadcb52…` (CR-439, `just eval-dry-run`) | A tool: `chantier gate` (or a `wait` form) that runs or follows a long command and returns at its end, so the Driver makes one call. |
| S5 | Scratch writes refused by the write guard: host scratchpad 375, `/tmp` 115, `../x.log` about 60, `/dev/null` 13 | 577 | `[eval] agent-a41f163a…:48`; `[chantier] agent-a2e3ceec…:39` (`2>/dev/null`) | Code: the hook allows `/dev/null` and the session's scratchpad, or the prompt's facts name `<cr>/work/scratch` as "scratch:". The host prompt says to use the scratchpad; the hook refuses it. |
| S6 | Spec-writer: "this is a planning surface with projects ...: p[ass --project]" 70; "CR folder must be inside the planning folder" 43; "not a CR folder: projects/chantier/changes/projects/chantier/changes/..." about 40 | 150+ | `[chantier] agent-a051acf7…:156`, `agent-a2d4dbf4…:137` | The doubled path comes from `cd` into the CR folder plus a relative path. CLI: resolve a path that repeats the planning prefix, or accept the CR's short name. |
| S7 | Spec-writer and Verifier call `Edit`, which their agent file does not give | 95 and 29 | - | Agent frontmatter: add `Edit`, or one line in the prompt facts. Not a card rule. |
| S8 | Spec-writer `summary set --help` | 340 calls (88 % of studio runs) | - | `summary lint`'s gap line could print the exact `summary set` form. Accepted stumbling otherwise: one call, about 300 bytes. |
| S9 | "summary is N characters: the limit is N", "title is N characters" | 52 + 11 | `[chantier] agent-aad9ec6e…:306` | Print the limit in `summary lint` and in `--help`; the refusal already says it, so the retry works. |
| S10 | Foreman: "no free slot" 14, "still has an agent recorded: `agents set CR-N - --epoch <n>` first" 9, `--epoch` put where argparse rejects it 9 | 32 | `[chantier] 1b6c0af3…:1399`, `:5894` | `take` could clear an ended Driver's id itself (the host says it ended); accept `--epoch` in any position. |
| S11 | Chief of Staff: "cannot move CR folder" 36, "no running batch" 23, "triage expects a CR folder" 12, `.venv` `chantier.exe` locked 11 | 82 | `[chantier] 91f1382a…:89257`, `:80319` | Mostly Windows file locks and wrong path forms; the refusals name the cause, retries succeed. A `next:` line with the retry would save the `--help` (208 calls). |
| S12 | Force push denied by the host's classifier | 13 Driver calls | `[chantier] agent-a0c9a049…:151` | Already handled by a route (Driver, Foreman, Chief of Staff). Read by 8 % of runs, yet followed: the refusal text itself says what to do. |
| S13 | Coder: Edit before Read 385, file changed since read 78 | 463 | - | Host behaviour, outside chantier. |

Not found: a repeated question to the user in the same session was not measured (section 6).
Re-reads of the same card slice in one run: under 0.01 per Driver run, 0.33 per Foreman session,
1.4 per Chief of Staff session. Compaction: the Foreman's stumble rate in the 25 tool calls after
a compaction is 3.8 % against 2.3 % elsewhere; the Coder's is lower after than before.

### 3.3 Rules obeyed, ignored, inferred

| Rule (source) | Evidence | Verdict |
| --- | --- | --- |
| Never merge (floor) | 0 `gh pr merge` in 681 Driver runs; 1 `git merge --ff-only`, refused by git (`[chantier] agent-a70a871a…:52`) | Obeyed |
| Merge only on the user's word or grant | Foreman after `release go` (`c095a20c…:775-790`); Chief of Staff: "Je fusionne par rebase, sur votre autorisation de cette nuit." (`[chantier] 9f663e8f…:989`) | Obeyed, 2 of 2 |
| Rebase only; `--force-with-lease`, never plain `--force` | 0 plain force push by a Driver; stack Driver 97 pushes, all with lease | Obeyed |
| The Coder never commits | 1 commit in 515 runs | Obeyed |
| Inspector reply is a JSON verdict | 654 of 655 | Obeyed (the Driver parses it) |
| Verifier reply and `verdict` | 679 of 681 start `VERIFIED` or `NOT VERIFIED` + `Head:` | Obeyed (the CLI refuses a verdict without `verify.md`) |
| Coder reply "Round N: done / Notes:" | 480 of 509 | Obeyed |
| First line of a started agent copied as printed | 3,472 of 3,484; the 12 others are one Foreman passing "Your prompt is the file ..." (`[chantier] bc951dfe…:6235`) | Obeyed |
| Hand-back: the printed line is the first line (`driver.md`, "your end") | first in 343 of 569 runs (61 %); absent though printed in 180 | **Half obeyed**: "CR-355 is handed back ready to merge: https://github.com/…" (`[chantier] agent-aa54b3a9…:86`) |
| "Every git command a Driver runs names its worktree: `git -C`" (`driver.md:131`) | CR Driver: 4,137 with `-C`, 3,502 without (after a `cd`) | **Half obeyed**, no harm seen |
| "Change no shell's folder into a CR folder" (`driver.md:142`) | 709 `cd` into a CR folder in 267 of 576 CR Driver runs | **Ignored**; visible harm only for the Spec-writer (S6) |
| Never `git add -A` or `.` (`driver.md:864`) | 67 times in 49 CR Driver runs (8.5 %) | Mostly obeyed |
| Never discard the worktree's work | Coders: 14 `git checkout -- <files>` in 13 runs (`[chantier] agent-a0342f64…:183`), CR Drivers 4, `reset --hard` 2 | Mostly obeyed; the Coder card has no such line, the Driver card has |
| Never `git stash` (`coder.md:33`) | 1 Coder run with a real `git stash` then `stash apply` (`[studio] agent-aab6a017…:737-747`); several odd `git stash list >/dev/null` | Obeyed but for 1 |
| Never stop a process by name or pattern | Stops seen are by PID (`taskkill //PID 37040`, `Stop-Process -Id`); 1 `Stop-Process` filtered by a command-line pattern, denied by the host (`[chantier] agent-a93ff23f…:243`) | Obeyed; the host is the net |
| `--lease` on `round`, `ship`, `handback` | Over-applied (S1) | Obeyed and over-generalised |
| `phase` before each step, `note` after each step | `phase` in 65 % of runs, `note` in 79 % | Partly obeyed; nothing fails without them |
| Hand back at 130,000 tokens of context | 127 hand-backs `blocked context`, median 117,500, range 64,000 to 145,000 | Obeyed, earlier than the rule asks |

Inferred with no card line: `summary set --help` before `summary set` (Spec-writers); reading the
project's `AGENTS.md` after `rules` prints its path; checking `gh pr checks` before saying a PR is
green; `--match-head-commit` on the two merges; retrying a refused scratch write inside the
folders the refusal names.

The pattern: a rule holds when something reads the result (a parent that parses, a CLI that
refuses, a host that denies). A prose rule about *how to type* a command (`-C`, no `cd`, which
flag where) is followed about half the time whatever the card says, and mostly costs nothing.

### 3.4 CLI outputs: used, ignored, too big

| Output | Use seen | Size and remark |
| --- | --- | --- |
| `handback`'s `[driver CR-n→foreman] hand-back ...` line | Copied in 61 % of hand-backs | 0.4 KB. Used. |
| `note`'s `context: N tokens` line | Drives 127 context hand-backs | Used; printed 4.3 times per run. |
| `rules` | 78 % of Drivers, 57 to 100 % of workers; followed by a read of `AGENTS.md` | 2.4 KB per call. Used. |
| `handoff` | 77 % of Driver runs, 1.6 calls | 2.6 KB per call; piped through `head` or `grep` in 40 % of calls: it is longer than what is wanted. It prints every worker's opening lines each time. |
| `round` | 54 % | 2.2 KB; carries the workers' first lines, which are copied right (99.7 %). |
| `log` | 48 % of Driver runs, 66 % of Verifiers | 2 to 3 KB. |
| `take` (Foreman) | 59 calls per session | 1.5 KB per call, **86 KB per session, the Foreman's largest output**: the Driver's whole prompt skeleton passes through the Foreman's context once per start. |
| `status` (Foreman) | 70 calls per session | 1 KB after pipes; piped through `head`, `tail` or `grep` in 46 % of calls. 70 KB per session. |
| `agents set` (Foreman) | 107 calls per session, 2 per Driver | 35 KB per session for a fact the host already knows. |
| `asks`, `order done` (Foreman) | 22 and 31 calls | 12 KB each per session. |
| `playbook` | 9 % of Driver runs, 2 calls per Foreman session | Rarely read. |
| `lease` | 28 % of Driver runs | Used around long gates. |
| `access` | 2 calls in the window | Almost never used, though the card names it for any refusal not understood. |
| Watcher lines (Chief of Staff) | 113 wakes, 4.7 tool calls per wake, first call `watch` again (88) then `order` (66) | Used. Each wake costs a re-arm call. |
| Refusal texts | A retry follows in the next call in most cases seen | Used; they are the working progressive disclosure today. |

The Foreman's CLI output is 243 KB per session over 214 CLI calls; the Chief of Staff's 176 KB
over 195. These match the Fable study's 184 KB and 173 KB on a smaller sample.

### 3.5 What costs most, and what could be a tool or a message

Weighted tokens below = input + 1.25 × cache write + 0.1 × cache read + 5 × output, per wake kind.

| Session | Model calls | Mean context per call | Heartbeat | Agent ended | Compaction | Other |
| --- | --- | --- | --- | --- | --- | --- |
| Foreman batch-31 (`c095a20c`) | 470 | 186,000 tokens | 64 % (42 wakes, 286 calls) | 26 % | 6 % | 4 % |
| Foreman batch-30 (`4ead8041`) | 1,175 | 182,000 | 37 % (56 wakes, 420 calls) | 44 % | 14 % | 5 % |
| Foreman studio batch-09 (`262338d1`) | 469 | 173,000 | none seen | 82 % | 10 % | 8 % |

| Session | Model calls | Mean context | The user or a peer typed | Foreman's turn ended | Skill load or reload | Watcher |
| --- | --- | --- | --- | --- | --- | --- |
| Chief of Staff chantier (`9f663e8f`) | 656 | 174,000 | 64 % | 25 % (62 wakes) | 5 % | 4 % |
| Chief of Staff studio (`e38fea53`) | 859 | 127,000 | 44 % | 25 % (89 wakes) | 22 % | 10 % |

1. **The Foreman's heartbeat.** One tick is about 7 model calls at 180,000 tokens of context:
   `status`, then `agents`, `take`, a start, `ScheduleWakeup`. A `next` command that answers
   "nothing due" in one call, or a watcher of its own that wakes it only on an event, removes most
   of it. The studio Foreman without heartbeat ticks ran the same number of calls for a batch of
   similar size.
2. **Three to four calls per Driver start** (`take`, the start, `agents set`, sometimes `status`)
   and one more at its end (`agents set <cr> -`), each at full context. One command that prints
   the prompt to a file and records the agent from the hook would make it one call and take 86 KB
   out of the Foreman's context.
3. **The Foreman's context sits at 180,000 tokens** and compacts 8 times per session. What fills
   it is CLI output and hand-back messages more than cards (cards: 110 KB once; CLI: 243 KB).
   `status --since`, a shorter `take`, and hand-backs capped to their line plus a path would lower
   every later call.
4. **Each Foreman turn end wakes the Chief of Staff** (a host message, "finished a turn"). Of
   1,494 such wakes, 881 produced text only, median 234 characters, such as "Noted."
   (`[eval] 63b2e782…:487`), on a context of 127,000 to 174,000 tokens. Fewer Foreman turn ends
   (point 1) cut these too; so would a host setting, if one exists.
5. **Driver restarts.** 231 CRs took 545 Driver runs (2.36 per CR; 30 % of CRs one run, 37 % two,
   33 % three or more). 127 runs end on the context rule. Each new Driver reads about 62 KB of
   cards again plus the specification. A lighter Driver boot is paid 2.4 times per CR; waiting
   outside the Driver's context (S4) would also end fewer runs on context.
6. **Waiting.** 15 % of CR Driver tool calls (3,648) are `sleep`, `until` loops, `Monitor`,
   `TaskStop` and reads of a background output file, each a model call at 80,000 to 110,000
   tokens. See S4.
7. **The Chief of Staff's hand work on the surface**: 47 pushes and 40 commits per session, 53
   `cd` into CR folders, 17 `--help`. The writer already commits and pushes; these calls come from
   sessions where it was not running or not trusted.

### 3.6 Maintenance rules against drift

See section 5.

## 4. What this says about the rewrite

- The rules worth card bytes are the ones a role must know **before** it types: what it owns, what
  it never does, how it ends, its reply format. The sample shows these are short and obeyed.
- Rules about command forms belong to the CLI: it should accept the near-miss (S1, S2, S6, S10)
  or refuse with the next command. Cards did not prevent any of them.
- A rare-case section costs nothing when it is not read and is read just in time when a refusal
  or a grep leads to it (the Foreman's release merge). That is the help-topic design, already
  observed.
- A never-rule with a net (CLI, hook, host classifier) is the safe kind to shorten to one line.
  A never-rule with no net and partial obedience (`git checkout -- <files>` by Coders, `git add
  -A`) is where a hook refusal would add something a card cannot.

## 5. Maintenance rules

Already in the repository (not proposed again): `test_startup_manifest.py` holds the **declared**
boot under 12,544 bytes and the CR Driver's readings under fixed limits; it and
`test_session_start_split.py`, `test_stack_chain_cards.py`, `test_rebase_rules.py`,
`test_command_names.py` pin phrases of the cards; `test_plugin_files.py` holds both hosts' agent
bodies identical, the links, and "the cards hold no host tool"; `evals/SCORECARD.md` lists 50
rails with stable ids and `evals/kit/audit.py` marks some; `test_scenario_coverage.py` ties
coverage bullets to tests; the Retro critic judges retro points (keep, merge, drop); `AGENTS.md`
says "a new CLI tool comes from measured token-costly behaviour". Nothing limits a card's own
size, nothing lints dates or trial marks (today: 70 lines with a date, 49 with a batch name, 45
with a CR id, 258 with "proved" or "unproved", 128 with "trial", in 9,117 lines), nothing ties a
rule to a check, and no target measures behaviour from transcripts.

| # | Rule | What is checked | By what | Who, when | Bypass |
| --- | --- | --- | --- | --- | --- |
| M1 | **A byte budget per card file**, in one data file (`skills/chantier/references/budgets.json`: file, limit, owner) | each card's LF byte count ≤ its limit; every `*.md` under `references/` has a row; the sum of the limits ≤ one constant written in the test | pytest (`test_card_budgets.py`), in `just test` | every PR, CI on three systems | Raising one limit is a diff of `budgets.json`; raising the sum is a diff of the test. Both show in review; M11 asks the owner's line for it. |
| M2 | **A budget on the measured path, not the declared one**: for each role, the bytes of every reading its prompt and its card lead to on the common path | the union of the readings named by the role's prompt and by `next:` lines, per role and host, ≤ the role's limit | pytest, extending `test_startup_manifest.py` (which measures only the manifest's startup sections) | every PR | Same as M1. |
| M3 | **No history in a card**: no date, batch name, CR id, PR number, "proved", "unproved", "trial", "the user's answer", model name, token count | regexes over `references/**/*.md` and `agents/*.md`; a hit fails with the line and "move it to `docs/proofs/` or `docs/incidents.md`" | pytest, in `just lint` | every PR | `references/lint-allow.txt`: one line per exception with the rule id (M4) and a reason; the test fails on an entry that matches nothing (no stale exception). |
| M4 | **A rule has an id and a row**: every sentence of a card with "never", "must", "only", "always" carries `[R-nnn]`; `rules.json` holds id, card, kind (floor, role, format), check, evidence, added by (CR), review by (version) | each id in a card has one row and the reverse; `check` names an existing pytest node, scenario step, scorecard rail or quiz case (resolved as `test_scenario_coverage.py` resolves its bullets); a row with no check has kind `inferred` and a quiz case | pytest | every PR | A row may say `check: none (judgement)` only with a scorecard rail id (`J` row): the rail is then marked in each campaign. |
| M5 | **Where a retro fix may land**, in this order: (1) the CLI accepts or does it, (2) a refusal that names the next command, (3) a `next:` or state line, (4) a help topic, (5) a card line. A point that proposes (5) must carry `count:` (runs seen in the last measure, M7) and say why (1) to (4) cannot hold it | the retro's points have `home:` and, for a card, `count:` and `why not code:`; a point without them is dropped | the Retro critic (its card gets these three fields; it already returns keep, merge or drop) and `chantier validate` on `retro.md` (a read-only check, in the CLI's scope) | the Foreman at each pause; the Chief of Staff before it files a point | The user files the item by hand; M1 and M4 still apply at the PR. |
| M6 | **A frequency floor for prose**: a card line is added only for a stumble seen in at least 5 runs or 2 % of the role's runs in the last measure, or for a rule of kind floor | the PR's body quotes the measure line (`behaviour-<version>.json`, key and count); the Inspector's checklist for a card diff asks for it | Inspector (judgement), with M1 as the net | PRs that touch `references/` | The owner's line in the PR (M11). One-off incidents go to `docs/incidents.md`, which no role loads. |
| M7 | **A periodic measure from transcripts**: `just behaviour [--since <date>]` runs `evals/kit/behaviour.py` and writes `evals/results/behaviour-<version>.json` and `.md`: per role, runs, tool calls, CLI errors by message, `--help` by command, each rule detector's rate (M8), waits, Driver runs per CR, Foreman wake shares | the file exists for the version being released and is newer than the last card change; its "regressions" list (a detector worse by more than 5 points, a new CLI error above 2 % of a role's runs) is empty or each line is answered | a `just` target on the user's machine (transcripts are local: never CI); the release procedure's "claims" step (`evals/README.md`) lists it | before each release, and after a batch that changes cards | The release Driver records "no measure: <reason>" in the claims file; the release notes then say so. |
| M8 | **A detector per checkable rule**: `rules.json` may name `detector: <regex on tool calls>` (for example `gh pr merge`, plain `--force`, `git stash`, `git add -A`, a `cd` into `changes/`) | each detector compiles and matches its own positive example and not its negative one (both in the row) | pytest for the detectors; M7 runs them on transcripts | every PR; each measure | None needed: a rule with no detector is allowed (M4). |
| M9 | **A refusal names what to do next** | every refusal text raised in `rails.py` (and the hook's) contains a backticked command or `help <topic>` | pytest over the refusal table (`test_rail_refusals.py` checks today that a refusal happens, not what it offers) | every PR | An allow-list in the test for refusals that are final ("stop now"). |
| M10 | **An argparse error is a CLI bug, not a card gap**: a usage error or one refusal message seen in more than 2 % of a role's runs | M7 prints the list ("S-list"); each line is filed as an inbox item or answered "accepted stumbling" in `evals/results/behaviour-accepted.md` | M7's output; the Chief of Staff files the items after the release retro (the systematic retro already exists) | each measure | The accepted file; an entry is re-asked when its rate doubles. |
| M11 | **Ownership**: `budgets.json` names one owner role per card; the floor file and `budgets.json` change only with a line "Floor change approved: <user>, <date>" or "Budget change approved: ..." in the PR body | CI job reads the PR's changed files and its body | a step of `ci.yml` (it has the PR context; pytest has not) | PRs that touch the floor or the budgets | The user writes the line. A Driver cannot: it is the user's word, quoted as the cards already require for a merge. |
| M12 | **How a rule is deleted**: in one PR, remove the text and set the row to `retired: <version>, <reason>` (the row stays, as retired rails stay in the scorecard; the id is never reused). A rule is a deletion candidate when its detector shows 0 violations in two measures **and** its quiz case passes 3 of 3 without the text, or when its trigger was not seen in two measures and its kind is not floor | `just behaviour --prune` lists the candidates; the test of M4 accepts a retired row with no text and refuses a retired id still in a card | M7 for the list; pytest for the consistency | after each measure; the owner decides | Kind floor is never a candidate; it leaves only by M11. |
| M13 | **Tests pin ids, not prose**: a test may assert that a rule id is in a card or a refusal, never that a phrase is | no `in card_text` assertion on a literal longer than 40 characters in `tests/` outside the registry test (an AST or regex check) | pytest | every PR | A marked exemption in the test file, counted and printed. Today's phrase tests (`moved rule is where it now lives`) are converted to ids when their card is rewritten. |
| M14 | **A role's tool list follows what it tries**: M7 reports "tool not in the role's list" per role (Spec-writer `Edit`: 95) | a line of the S-list (M10) | M7 | each measure | Accepted file, with the reason the tool is withheld (the Inspector has no `Write` on purpose). |

Review of the set against its own rule: M1, M3, M4, M9 and M13 are pytest and cost nothing per
run; M7 is the only one that needs the user's machine and time (the indexing of 4.3 GB took 7
seconds here, the analyses under a minute). M5 and M6 lean on judgement (Retro critic, Inspector)
and are backed by M1: when the budget is full, a card line can only enter if another leaves.

## 6. What I could not check

- **Small samples for the steering roles**: Foreman 12 sessions, Chief of Staff 7, Griller 11.
  Their rates are counts, not statistics. Token shares (3.5) are from 5 sessions only.
- **Not seen**: QA driver, demo-explorer, board-griller, every Copilot role.
- **Tool results are cut** to their first 500 and last 400 characters in my index: a refusal in
  the middle of a long output is missed, so CLI refusal counts are lower bounds.
- **Workers of the chantier project run chantier as the product under test.** Their "CLI
  refusal" and "usage" counts mix both; I give worker CLI figures from the studio project only
  and left the mixed cells empty in 3.2.
- **Card versions changed during the week** and the checkout is at `3c29dd7c`, behind
  `origin/main` (CR-471's cut by moment). The section map of 3.1 uses that file for runs since
  2026-11-22; line offsets may be off for some runs. No transcript ran on CR-471's cards.
- **Whether a rule was read before it was broken** is not established per run (only shares of
  runs that read a section and shares that break a rule).
- **Repeated questions to the user** and the quality of the grill were not measured; the Chief of
  Staff asked 57 `AskUserQuestion` per session and I did not compare their texts.
- **Quality of the deliverables** (PRs, specifications) was not judged: this study counts
  behaviour, not outcomes. "No harm seen" means none in the tool results.
- **Money**: the weighting of 3.5 is a rough price ratio, not a bill; subagent tokens are not
  attributed to the wake that started them.
- **The hook's rules** were read only through its refusal texts; I did not read
  `hooks/register.tsx`.
- **Regex detectors** (git verbs, `cd`, CLI calls through shell aliases) miss commands built from
  variables (`cd "$F"`), so "ignored" rates for `cd` are lower bounds.
