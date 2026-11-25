# SC19 evidence: inventory of the worker cards' rules

Sources walked: the old cards at HEAD in `skills/chantier/references/` (coder, conflict-resolver, debugger, investigator, demo-explorer, spec-writer, spec-critic, retro-critic, inspector, verifier, and griller.md lines 102-136), against the new cards, topics and floor in `skills/chantier/cards-next/`. Kinds (study-fable): a protects the user or repository, b inferable, c incident, d trial bookkeeping, e CLI-printable, f duplicate. Granularity: one row per rule group of a card, not per sentence; sentences that say the same thing are one row.

Homes: card = the role's new card; floor = `floor.md`; topic = `topics/<name>.md`; refusal = a CLI refusal; cut = dropped.

| Old card | Rule | Kind | Home |
| --- | --- | --- | --- |
| all workers | Never commit, push, rebase, merge, no `git stash` | a | card (Never), floor |
| all workers | Never write by another way a path the guard refused | a | card (Never) |
| all workers | Never claim a check not run; never silence a failing gate | a | card (Never) |
| all workers | A `$CHANTIER` that cannot run is a stop | a | floor 4, topic worker-shell |
| all workers | One command per call; no leading assignment; no sleep or background shell | c | topic worker-shell |
| all workers | Read before overwrite; edit rather than rewrite | b | topic worker-shell |
| all workers | UTF-8 without BOM; PowerShell 5.1 adds one | c | card (owns line), topic worker-shell |
| all workers | Notes in `<work folder>/<role>/`, proof in `evidence/`, raw logs not published | c | topic worker-shell |
| all workers | Repository text in English; ticket text in the ticket's language | e | topic worker-shell |
| all workers | A missing skill is not a stop | c | topic worker-shell |
| coder | Implement one round; fast gates green | b | card (goal) |
| coder | Owns worktree changes and `r<n>.md`; checklist marked done or open there | a | card |
| coder | Read specification, round note, previous notes; open only needed files | b | card |
| coder | No test or probe of the board's write paths at the live planning folder | a | card (Never) |
| coder | Reply template, four lines, at most ten | a (parsed) | card, byte for byte |
| coder | One Gate line per gate; Open at most three points | a (parsed) | card |
| coder | Repeated reminders of the same nevers; walkthrough of reading the spec and noting a hand-over | b/f | cut |
| conflict-resolver | Resolve the named conflict only; keep both sides' intent | a | card |
| conflict-resolver | Never commit, force, or resolve by dropping a side silently | a | card (Never) |
| conflict-resolver | Notes file and reply format | a (parsed) | card |
| conflict-resolver | Step-by-step reading of conflict markers | b | cut |
| debugger | Find the cause with a reproduction before any fix; notes in `debugger/` | a | card |
| debugger | Never edit outside the change; never commit | a | card (Never) |
| debugger | Reply format | a (parsed) | card |
| debugger | Generic debugging method advice | b | cut |
| investigator | Read-only inquiry; findings in notes with evidence | a | card |
| investigator | Never edit the project; no claim without a command or file cited | a | card (Never) |
| investigator | Reply format | a (parsed) | card |
| investigator | Generic search advice | b | cut |
| demo-explorer | Run the demo as a user would, capture what it shows | a | card |
| demo-explorer | Made-up paths, no username in captures | a | floor 8, topic verifier-images |
| demo-explorer | Reply format | a (parsed) | card |
| demo-explorer | Tool-by-tool capture advice | b | cut |
| spec-writer | Write the specification: goal, behaviour, evidence, open questions | a | card |
| spec-writer | Never write code; never decide what the answers leave open | a | card (Never) |
| spec-writer | CI job: name the environment, what only CI proves | c | topic spec-writer-extras |
| spec-writer | Host and default matrix, one line per cell | c | topic spec-writer-extras |
| spec-writer | Copy the CR's `issue:` lines under the title | c | topic spec-writer-extras |
| spec-critic | Judge the specification: gaps, contradictions, unproved claims | a | card |
| spec-critic | Never rewrite the specification; list findings | a | card (Never) |
| spec-critic | Verdict format | a (parsed) | card |
| retro-critic | Judge the retro points: evidence, duplicates, scope | a | card |
| retro-critic | Never invent a point; findings only | a | card (Never) |
| retro-critic | Reply format | a (parsed) | card |
| inspector | Judge the diff against the specification at the head; never edit | a | card |
| inspector | Findings blocking or not; the JSON reply line | a (parsed) | card, byte for byte |
| inspector | A test the specification names that guards a shipped file must be in the diff and read as shipped | c | card |
| inspector | A check red on the default branch is not the CR's | c | card |
| inspector | Audit of a large or generated diff | c | topic inspector-audit |
| inspector | Duplicate of the verifier's evidence rules | f | cut |
| verifier | Prove at the pushed head; never the round's Coder or Inspector; never edit code | a | card |
| verifier | `verify.md` with `Head:`, claims with SHA, command, output; end VERIFIED or NOT VERIFIED | a (parsed) | card |
| verifier | Run `verdict` before the reply; VERIFIED refused until Head matches | e | card (one line), refusal |
| verifier | Carried claims keep their SHA and say carried | a | card |
| verifier | Long gate only with no pass at that head, one name per argument | a | card |
| verifier | Never aim a probe at the live planning folder or `$CHANTIER` at the scratch project | a | card, topic verifier-scratch |
| verifier | Scratch project: git init, `--project`, removed at the end, long path is a stop | c | topic verifier-scratch |
| verifier | No image shows the username or home folder; open each screenshot | a | card, floor 8, topic verifier-images |
| verifier | Before on a detached base worktree, after at the head, `before-after.md` | c | topic verifier-before-after |
| verifier | Description pass: images at the named SHA, the look | c | topic verifier-description, verifier-images |
| verifier | The PR Review box checks | c | topic verifier-review-box |
| verifier | Move or delta matrix, `matrix probe` | c | topic verifier-delta-matrix |
| verifier | Reply block (four lines, Failed rule past six) | a (parsed) | card, byte for byte |
| griller | Headless run, no seat, no watcher, no hub | a | griller.md |
| griller | One CR only; read limits; write only in that CR's folder | a | griller.md |
| griller | Only the four allowed chantier commands, on that CR's folder | a | griller.md |
| griller | No network tool, no MCP, no subagent, no git | a | griller.md |
| griller | End line `[griller→board] grilled enough: <next batch or running batch>` | a (parsed) | griller.md, exact |
| griller | The run's cost is in no batch | d | griller.md |

## Kind a rows and their home

Every kind-a row has a home in a card, the floor, a topic or a refusal; none is cut. A rule kept in a topic only (not the card) is a kind-c incident rule (answer 10), each with `review_by` "0.16.0".

## Inferable rows (kind b)

Cut: coder walkthrough of reading the spec and noting a hand-over; conflict-resolver marker reading; debugger and investigator generic method; demo-explorer tool-by-tool capture advice. Read-before-overwrite moved to the worker-shell topic.

## Reply-block diff

The reply blocks of the coder, the verifier and the inspector, and the griller's end line, are compared with the old cards in `evidence/reply-blocks-diff.md`.
