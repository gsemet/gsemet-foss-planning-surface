"""Builds evidence/cards-inventory-workers.md: one row per rule sentence of the old worker cards.
Sources: skills/chantier/references/<card>.md at the base (f7b74e64), line numbers from `cat -n`."""
import io
import os
import sys

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "evidence", "cards-inventory-workers.md")
rows = []  # (role, trigger, behaviour, source, kind, home, check)


def R(role, trig, beh, src, kind, home, check):
    rows.append((role, trig, beh, src, kind, home, check))


FS = "floor.md is a byte copy (cmp); brief carries it"
BR = "brief builds, exit 0 (brief-bytes.md)"


def common(role, f, L):
    """The rule sentences the worker cards share; L maps a key to the old line range."""
    s = lambda k: f"{f}:{L[k]}"
    if "intro" in L:
        R(role, "every run", "Runs in the foreground for a Driver, does one short task and returns; the prompt gives the CR, the CLI, the worktree and its base, the specification, the work folder and the round's note", s("intro"), "e", "facts", BR)
    if "startup" in L:
        R(role, "start", "At startup read the startup core; defer the other sections until an action names them", s("startup"), "e", "facts (the brief's `Read ... whole, first` line)", BR)
    if "only" in L:
        R(role, "start", "Read only this card", s("only"), "e", "facts (the brief's `Read ... whole, first` line)", BR)
    if "rules" in L:
        R(role, "start", "Read the project's rules (`$CHANTIER rules`) before anything else: what touches the task ranks above the card, the card holds where they are silent", s("rules"), "e", "facts (`the project's rules rank above them: rules`)", BR)
    if "english" in L:
        R(role, "writing repository or forge text", "Repository and forge text is in English, except a ticket's comment, plan and demo, in the ticket's language unless the project's rules say otherwise", s("english"), "c", "topic worker-shell (review_by 0.16.0)", "topics.json validates (load_topics)")
    if "worktree" in L:
        R(role, "every run", "Work only in the CR's worktree (`cd` there first)", s("worktree"), "e", "refusal: the plugin's write guard (Write or Edit outside the `writes:` line) and facts (`worktree:`)", "child 25")
    if "never_create" in L:
        R(role, "every run", "The Driver made the worktree: never create one", s("never_create"), "a", f"card {role}.md (Never)", f"grep 'create a worktree' cards-next/{role}.md")
    if "guard" in L:
        R(role, "a Write or Edit refused", "The plugin refuses a Write or Edit outside the folders the `writes:` line names: the path is wrong, so fix it, never retry by another means, a shell write included", s("guard"), "a", f"card {role}.md (Never: write by another way a path the guard refused)", "quiz floor-9-coder-denied-write" if role == "coder" else "child 25")
    if "denied" in L:
        R(role, "a refusal or denied permission", "A denied permission or a refusal is reported to the Driver with its exact text, never worked around", s("denied"), "f", "floor 9", FS)
    if "nofb" in L:
        R(role, "a tool, model, agent or CLI command not available as named", "No fallback: a stop, reported with its error; never a look-alike, a workaround or an estimate", s("nofb"), "f", "floor 3", FS)
    if "free" in L:
        R(role, "every run", "Within what you have, judge freely", s("free"), "b", "inferable", "none: nothing to do")
    if "lacks" in L:
        R(role, "a skill or tool the playbook names is missing", "A skill or tool the playbook says the role needs but the session lacks is not a stop: say so in a note and work without it, never by another means", s("lacks"), "c", "topic worker-shell (review_by 0.16.0)", "topics.json validates")
    if "cli_stop" in L:
        R(role, "`$CHANTIER` cannot run", "Never `$CHANTIER`: a CLI that cannot run is a stop", s("cli_stop"), "f", "floor 4", FS)
    if "notes" in L:
        R(role, "writing notes and proof", L["notes_beh"], s("notes"), "c", "topic worker-shell (review_by 0.16.0)", "topics.json validates")
    if "rawlog" in L:
        R(role, "keeping a raw log", "Keep a raw log in a `*.log` file or `work/gates/`, never in a file published with the CR (reports and evidence are)", s("rawlog"), "c", "topic worker-shell (review_by 0.16.0)", "topics.json validates")
    if "claim" in L:
        R(role, "every claim of a check", "Never claim a check you did not run", s("claim"), "a", f"card {role}.md (Never)", f"grep 'claim a check' cards-next/{role}.md")
    if "commit" in L:
        R(role, "every run", "Never commit, push, rebase or merge", s("commit"), "a", f"card {role}.md (Never)", "quiz floor-5 case of the role" if role in ("coder", "conflict-resolver", "debugger") else "child 25")
    if "sleep" in L:
        R(role, "waiting", "Run no `sleep` and no background shell", s("sleep"), "c", "topic worker-shell (review_by 0.16.0); host row end-turn-background", "topics.json validates")
    if "stash" in L:
        R(role, "every run", "Never run `git stash` (the stash is shared by every worktree)", s("stash"), "a", f"card {role}.md (Never)", f"grep 'git stash' cards-next/{role}.md")
    if "pkill" in L:
        R(role, "every run", "Never stop a process by name or pattern (`pkill`, `killall`)", s("pkill"), "f", "floor 10", FS)
    if "chain" in L:
        R(role, "a shell call", "One command per call when you can: a chain (`a; b`, `a && b`, a pipe) passes the host's allow rules only if every part does", s("chain"), "c", "topic worker-shell (review_by 0.16.0)", "topics.json validates")
        R(role, "a shell call", "No leading assignment before a command (`X=1 cmd`, `$w='...'; cmd`): write the value into the command", s("chain"), "c", "topic worker-shell (review_by 0.16.0)", "topics.json validates")
    if "overwrite" in L:
        R(role, "writing a file", "Read a file before you overwrite it; to change part of a file, edit it rather than rewrite it", s("overwrite"), "e", "refusal: the host's Write tool refuses an overwrite of an unread file; also topic worker-shell", "child 25")
    if "bom" in L:
        R(role, "writing a file", L.get("bom_beh", "Every file you write is UTF-8 without a byte-order mark (on Windows PowerShell 5.1, `Out-File` and `Set-Content -Encoding utf8` add one)"), s("bom"), "c", L.get("bom_home", "topic worker-shell (review_by 0.16.0)"), "topics.json validates")
    if "stop" in L:
        R(role, "blocked", "Stop when blocked and say why", s("stop"), "c", "topic worker-shell (review_by 0.16.0)", "topics.json validates")
    if "failed_worker" in L:
        R(role, "a reply out of format", "A reply out of that format is a failed worker, which the Driver starts again rather than reads; a reply in format that is only longer than its cap is read and noted, not restarted", s("failed_worker"), "b", "inferable (the Driver's own handling; the card keeps `nothing else` and the cap)", "none")


# ---------------------------------------------------------------- coder (references/coder.md)
f = "coder.md"
common("coder", f, dict(intro="3-6", startup="6-7", rules="9-11", english="10-11", worktree="15", never_create="15-16", guard="16-19", denied="18-19", nofb="20-22", free="21", lacks="21-23", cli_stop="23", notes="24-25", notes_beh="Keep your notes in `<work folder>/coder/` and proof in the CR folder's `evidence/`", rawlog="25-26", claim="27", commit="32", sleep="32", stash="32-33", pkill="33-34", chain="35-37", overwrite="37-38", bom="38-40", stop="41", failed_worker="43-45"))
R("coder", "every run", "Run the project's fast gate yourself", f"{f}:27", "a", "card coder.md (goal: fast gates green; Gate: lines)", "quiz floor-3-coder-missing-gate")
R("coder", "a test, smoke run or probe of the board's write paths", "Point it at a scratch planning folder (a fresh temporary folder or one under the worktree's test fixtures), never at the live planning folder, and remove it at its end", f"{f}:28-31", "a", "card coder.md (Never: point a test or probe ... at the live planning folder)", "grep 'live planning folder' cards-next/coder.md")
R("coder", "the reply", "The reply is the template below and nothing else (no greeting, no summary of the work, no list of what was checked and found right): it is the whole of the output to the Driver", f"{f}:41-43", "a", "card coder.md (Reply with this template and nothing else)", "reply-blocks-diff.md")
R("coder", "the round", "Implement one round of the CR, with the fast gates green", f"{f}:49-50", "a", "card coder.md (goal)", "child 25")
R("coder", "the round", "Read the specification, the round's note and the previous notes; open the files the change needs, not whole folders", f"{f}:49-50", "a", "card coder.md (Read the specification ... open only the files the change needs)", "child 25")
R("coder", "a gate fails", "Never silence a failing gate", f"{f}:50-51", "a", "card coder.md (Never: silence a failing gate)", "quiz floor-5-coder-failing-round")
R("coder", "writing a file", "Never add a byte-order mark to a file", f"{f}:51", "a", "card coder.md (Files are UTF-8, no BOM); topic worker-shell", "grep 'no BOM' cards-next/coder.md")
R("coder", "the end of the round", "Output: changes in the worktree, not committed; `r<n>.md`: what changed, the gates run with their results, open points, a hand-over note for the next round", f"{f}:51-52", "a", "card coder.md (You own ...)", "child 25")
R("coder", "the prompt carries a checklist", "`r<n>.md` marks each item `done` or `open: <why>`; the checklist goes in `r<n>.md` only, never in the reply", f"{f}:52-54", "a", "card coder.md (A checklist in your prompt is marked in `r<n>.md` ... never in the reply)", "child 25")
R("coder", "the reply", "Reply with the four-line template (`Round <n>: done | blocked: <one-line reason>`, `Notes: <work folder>/coder/r<n>.md`, `Gate: <command as run>: pass | fail: <first failing line>`, `Open: <one line> | none`), at most ten lines", f"{f}:56-63", "a", "card coder.md (the same block, byte for byte)", "reply-blocks-diff.md")
R("coder", "the reply", "One `Gate:` line per gate run (the fast gates named in the project's rules); `Open:` names at most three points in one line each, the rest left to `r<n>.md`", f"{f}:65-66", "a", "card coder.md (same sentence)", "reply-blocks-diff.md")
R("coder", "the reply", "What changed, file by file, and the hand-over note go in `r<n>.md` only, never in the reply", f"{f}:66-67", "f", "card coder.md (the owns line puts them in `r<n>.md`)", "child 25")

# ---------------------------------------------------------------- conflict-resolver
f = "conflict-resolver.md"
common("conflict-resolver", f, dict(intro="3-5", only="5-6", rules="8-10", english="9-10", worktree="14", never_create="14-15", guard="15-18", denied="17-18", nofb="19-21", free="20-21", lacks="21-22", cli_stop="22", notes="23", notes_beh="Keep your notes in `<work folder>/conflict-resolver/`", rawlog="23-24", claim="25", stash="26-27", pkill="28-29", sleep="28", chain="30-32", overwrite="32-33", bom="33-34", stop="35"))
R("conflict-resolver", "every run", "Run the project's fast gate yourself", f"{f}:25", "a", "card conflict-resolver.md (Run the fast gate after the rebase)", "quiz floor-5-conflict-resolver-rebase")
R("conflict-resolver", "every run", "You never commit, push or merge", f"{f}:26", "a", "card conflict-resolver.md (Never: push ... merge; the rebase stays a rebase)", "quiz floor-5-conflict-resolver-rebase")
R("conflict-resolver", "staging", "You may stage and continue the rebase; stage with explicit paths (`git add -- <path>`, never `-A`)", f"{f}:26-28", "a", "card conflict-resolver.md (You may stage with explicit paths ...)", "grep 'never `-A`' cards-next/conflict-resolver.md")
R("conflict-resolver", "the reply", "Reply in at most ten lines; details go to `conflicts.md`, and the reply names that file rather than repeating it", f"{f}:35-36", "a", "card conflict-resolver.md (Reply in at most ten lines, naming `conflicts.md`)", "reply-blocks-diff.md")
R("conflict-resolver", "the task", "Rebase the CR's branch on its base and resolve the conflicts so both sides' intent survives", f"{f}:40-41", "a", "card conflict-resolver.md (goal)", "child 25")
R("conflict-resolver", "resolving", "The rebase stays a rebase: never resolve by merging the base in (`git merge`, `git pull` without `--rebase`), and never use `--rebase-merges`", f"{f}:41-43", "a", "card conflict-resolver.md (Never: merge ... or use `--rebase-merges`)", "quiz floor-5-conflict-resolver-rebase")
R("conflict-resolver", "a merge commit in the branch", "A merge commit left in the branch shows up as the Driver's `ship` refusal (`concepts.md` rule 8)", f"{f}:42-43", "e", "refusal: `ship` (merge commit in the branch); card conflict-resolver.md names it", "child 25")
R("conflict-resolver", "continuing", "Never `git rebase --exec` or `-x`; never push", f"{f}:44", "a", "card conflict-resolver.md (Never: push ... `--exec` or `-x`)", "grep -- '--exec' cards-next/conflict-resolver.md")
R("conflict-resolver", "every git command", "Every git command you run is `git -C <worktree>`; never run git in the main checkout", f"{f}:44-45", "a", "card conflict-resolver.md (Never: run git in the main checkout)", "grep 'git -C' cards-next/conflict-resolver.md")
R("conflict-resolver", "choosing a side", "Never resolve with a whole side (`-X ours`, `checkout --theirs`); two product intents in conflict are a question: stop and say so", f"{f}:45-46", "a", "card conflict-resolver.md (Never: resolve with a whole side)", "child 25")
R("conflict-resolver", "before `git rebase --continue`", "Add no byte-order mark: check that each resolved file starts as it did before the conflict (a mark it already had is kept)", f"{f}:46-48", "a", "card conflict-resolver.md (Never: add a BOM ...)", "grep 'BOM' cards-next/conflict-resolver.md")
R("conflict-resolver", "after resolving", "Run the fast gate after", f"{f}:48-49", "a", "card conflict-resolver.md (Run the fast gate after the rebase)", "child 25")
R("conflict-resolver", "the output", "`conflicts.md`: each conflicted hunk and the choice made, and the fast gate's command, as run, and its result (the pass or the failing lines)", f"{f}:49-50", "a", "card conflict-resolver.md (You own ...)", "child 25")
R("conflict-resolver", "the project names no fast gate", "With no fast gate in the project's rules, one line says so", f"{f}:50-51", "a", "card conflict-resolver.md (or one line saying the project's rules name none)", "child 25")
R("conflict-resolver", "the output", "A `conflicts.md` without this line is a reply out of format", f"{f}:51", "a", "card conflict-resolver.md (A `conflicts.md` without that line is out of format)", "child 25")

# ---------------------------------------------------------------- debugger
f = "debugger.md"
common("debugger", f, dict(intro="3-5", only="5-6", rules="8-10", english="9-10", worktree="14", never_create="14-15", guard="15-18", denied="17-18", nofb="19-21", free="20-21", lacks="21-22", cli_stop="22", notes="23", notes_beh="Keep your notes in `<work folder>/debugger/` and proof in the CR folder's `evidence/`", rawlog="24-25", claim="33", commit="33", sleep="33-34", stash="34", pkill="34-35", chain="36-38", overwrite="38-39", bom="39-41", stop="42"))
R("debugger", "a CI artifact is downloaded", "It goes under `<CR folder>/work/scratch/artifacts-<run id>/`, never under `<work folder>/debugger/` or `evidence/`: it stays on this machine, never published; copy into `evidence/` only the small part that proves the finding", f"{f}:25-28", "a", "card debugger.md (a CI artifact goes under ... never published)", "child 25")
R("debugger", "a test, smoke run or probe of the board's write paths", "Point it at a scratch planning folder, never at the live planning folder, and remove it at its end", f"{f}:29-32", "a", "card debugger.md (Never: point a test or probe ... at the live planning folder)", "grep 'live planning folder' cards-next/debugger.md")
R("debugger", "every run", "Run the project's fast gate yourself", f"{f}:33", "a", "card debugger.md (Never: claim a check you did not run: run the project's fast gate yourself)", "quiz floor-5-debugger-uncommitted")
R("debugger", "the reply", "Reply in at most ten lines; details go to your notes, and the reply names that file rather than repeating it", f"{f}:42-43", "a", "card debugger.md (Reply in at most ten lines, naming `diagnosis.md`)", "reply-blocks-diff.md")
R("debugger", "the task", "Find why a check is red or a behavior is wrong, and prove it", f"{f}:47", "a", "card debugger.md (goal)", "child 25")
R("debugger", "the task", "A diagnosis, not a fix: probe with commands and scripts in your notes folder, and change no file of the worktree", f"{f}:47-48", "a", "card debugger.md (You own ... You change no file of the worktree)", "child 25")
R("debugger", "the output", "`diagnosis.md`: the reproduction command, the cause with its evidence, the place to fix", f"{f}:49-50", "a", "card debugger.md (diagnosis.md: the reproduction command, the cause with its evidence, the place to fix)", "child 25")
R("debugger", "two fixes failed", "After two failed fixes on one premise, test the premise", f"{f}:50", "a", "card debugger.md (same sentence)", "child 25")

# ---------------------------------------------------------------- investigator
f = "investigator.md"
common("investigator", f, dict(intro="3-5", only="5-6", rules="8-10", english="9-10", worktree="14", never_create="14-15", guard="15-18", denied="17-18", nofb="19-21", free="20-21", lacks="21-22", cli_stop="22", notes="23", notes_beh="Keep your notes in `<work folder>/investigator/` and proof in the CR folder's `evidence/`", rawlog="24-25", claim="26", commit="26", sleep="26-27", stash="27", pkill="27-28", chain="29-31", overwrite="31-32", bom="32-34", stop="35"))
R("investigator", "the reply", "Reply in at most ten lines; details go to your notes, and the reply names that file rather than repeating it", f"{f}:35-36", "a", "card investigator.md (Reply in at most ten lines, naming `investigation.md`)", "reply-blocks-diff.md")
R("investigator", "before the first round", "Map the code the CR touches and name the smallest change that meets the specification", f"{f}:40-41", "a", "card investigator.md (goal)", "child 25")
R("investigator", "the task", "Read only", f"{f}:41", "a", "card investigator.md (Read only: you write no worktree file)", "child 25")
R("investigator", "the output", "`investigation.md`: files and entry points, the smallest change, risks, the questions only the user can answer, and to end an evidence plan", f"{f}:41-45", "a", "card investigator.md (You own `investigation.md`: ...)", "child 25")
R("investigator", "a change alters a size or a value other code measures from", "Risks include every value derived from it, found by searching for the old value", f"{f}:42-44", "a", "card investigator.md (risks: ... found by searching for the old value)", "child 25")
R("investigator", "the evidence plan", "The kind of change, what shows it before and after (a screenshot, a command's output, a log, a generated file), the technique, reusing the project's e2e or test environment when it has one, and what cannot be shown", f"{f}:44-47", "a", "card investigator.md (to end, an evidence plan ...)", "child 25")
R("investigator", "nothing to see", "A change with nothing to see says so in one line", f"{f}:47", "a", "card investigator.md (same sentence)", "child 25")
R("investigator", "the project's rules speak of evidence", "What the project's rules say of the evidence a kind of change needs, and how to capture it, ranks above the plan; where they are silent the plan decides, never a question to the user", f"{f}:47-49", "a", "card investigator.md (same sentence)", "child 25")

# ---------------------------------------------------------------- demo-explorer
f = "demo-explorer.md"
common("demo-explorer", f, dict(startup="5-6", rules="8-10", english="9-10", nofb="17-19", free="18-19", lacks="19-20", cli_stop="20", claim="21", sleep="21", stash="21-22", pkill="22", chain="23-26", overwrite="26-27", bom="27", stop="28"))
R("demo-explorer", "start", "Started by the Chief of Staff in the foreground; the prompt names the batch, its folder and the language of the user; it has no CR and no round", f"{f}:3-5", "e", "facts", BR)
R("demo-explorer", "the demo's language", "The demo is in the batch's language", f"{f}:10", "b", "inferable (the prompt names the language; card: in the user's language)", "none")
R("demo-explorer", "every run", "You work in no CR's worktree and you never commit, push, comment or open a PR", f"{f}:14-15", "a", "card demo-explorer.md (Never: work in a CR's worktree ...; commit, push, comment or open a PR)", "grep 'open a PR' cards-next/demo-explorer.md")
R("demo-explorer", "every run", "You never create a worktree except the detached one of step 3", f"{f}:15-16", "a", "card demo-explorer.md (Never: create a worktree but that detached one)", "grep 'detached' cards-next/demo-explorer.md")
R("demo-explorer", "a refusal", "A denied permission or a refusal is reported with its exact text, never worked around", f"{f}:15-16", "f", "floor 9", FS)
R("demo-explorer", "the reply", "Reply in at most ten lines", f"{f}:28", "a", "card demo-explorer.md (Reply: ... at most ten lines)", "reply-blocks-diff.md")
R("demo-explorer", "the task", "Study a stack that is ready to merge and write the demo of what it delivers", f"{f}:3", "a", "card demo-explorer.md (goal)", "child 25")
R("demo-explorer", "reading", "Read in this order and stop as soon as you can write: 1. the PRs or MRs with `gh` or `glab` (description, diff, comments, attached images and videos); 2. the batch's CRs (specification, `02-answers.md`, `work/`, the Verifier's `evidence/`); 3. the code, only if these leave a question", f"{f}:32-39", "a", "card demo-explorer.md (Read in this order, stop as soon as you can write)", "child 25")
R("demo-explorer", "reading the code", "The stack's highest worktree if it still exists, else a detached worktree at the top of the stack, made clean and outside the repository, which you remove at your end", f"{f}:37-39", "a", "card demo-explorer.md (the stack's highest worktree, else a detached worktree ..., removed at the end)", "child 25")
R("demo-explorer", "reading the code", "Read only; run nothing that writes in a CR's worktree", f"{f}:39", "a", "card demo-explorer.md (Never: work in a CR's worktree or write in one)", "grep 'write in one' cards-next/demo-explorer.md")
R("demo-explorer", "the output", "`demo/demo.md` in `4-batch/`, in the user's language", f"{f}:41", "a", "card demo-explorer.md (You own `demo/demo.md` in `4-batch/`, in the user's language)", "child 25")
R("demo-explorer", "the output", "What is delivered, by feature; the bugs fixed; the architectural impact that matters", f"{f}:43", "a", "card demo-explorer.md (what is delivered by feature, the bugs fixed, the architectural impact)", "child 25")
R("demo-explorer", "the output", "The evidence for each, with its link or path; before and after screenshots when there are some; say what has none; invent nothing", f"{f}:44-45", "a", "card demo-explorer.md (the evidence for each ... say what has none, invent nothing)", "quiz floor-8-demo-explorer-capture")
R("demo-explorer", "the output", "For each change, a walkthrough: the setup, where to click or what to run, what was there before, what the user should see now", f"{f}:46-47", "a", "card demo-explorer.md (a walkthrough per change)", "child 25")
R("demo-explorer", "the output", "What the walkthroughs need: a fixture or a small ephemeral environment, and how to remove it", f"{f}:48", "a", "card demo-explorer.md (what they need ... and its removal)", "child 25")
R("demo-explorer", "running the project", "How to run the project comes from its `AGENTS.md`; what it does not say is a question in your reply, not a guess", f"{f}:48-50", "a", "card demo-explorer.md (same sentence)", "child 25")
R("demo-explorer", "the reply", "Reply with the path of `demo/demo.md` and the open questions, in at most ten lines", f"{f}:52", "a", "card demo-explorer.md (Reply: the path of `demo/demo.md` and the open questions)", "reply-blocks-diff.md")

# ---------------------------------------------------------------- spec-writer
f = "spec-writer.md"
R("spec-writer", "start", "Write one CR's Change Specification from its grill", f"{f}:3", "a", "card spec-writer.md (goal)", "child 25")
R("spec-writer", "start", "Started by the Chief of Staff or a Griller in the background, only on the user's word that the CR is grilled enough, outside any batch; the prompt names the CR's folder; no worktree, no round, no slot", f"{f}:3-6", "a", "card spec-writer.md (The Chief of Staff or a Griller starts you ... only on the user's word ...)", "child 25")
R("spec-writer", "every run", "You never commit, push or open a PR", f"{f}:5-6", "a", "card spec-writer.md (Never: commit, push or open a PR)", "grep 'open a PR' cards-next/spec-writer.md")
R("spec-writer", "reading", "Read the CR's folder (`intake/request.md`, `01-intent.md`, `02-answers.md`, any reference file) and the project's rules (what touches the CR ranks above the card)", f"{f}:10-12", "a", "card spec-writer.md (Read the CR's folder ...); the rank of the rules is in facts", "child 25")
R("spec-writer", "reading", "Read the code the CR touches, read-only, to name real files, functions and commands", f"{f}:12", "a", "card spec-writer.md (read-only, the code the CR touches)", "child 25")
R("spec-writer", "the CR adds or changes a CI job", "Read the project's CI files, read-only, to name the environment the job runs in; what the CI files and the answers do not give goes in the open questions", f"{f}:12-14", "c", "topic spec-writer-extras (review_by 0.16.0)", "topics.json validates")
R("spec-writer", "spec-critic fixes in the brief", "Apply each, or say in your reply why it does not hold; never against `02-answers.md`", f"{f}:15-16", "a", "card spec-writer.md (apply each, or say why not; never against `02-answers.md`)", "child 25")
R("spec-writer", "the output", "`03-change-spec.md` in the CR's folder and the CR's summary refreshed (`summary lint`, then `summary set`), and nothing else written anywhere", f"{f}:20-22", "a", "card spec-writer.md (You own `03-change-spec.md` and the CR's summary ...; nothing else is written)", "child 25")
R("spec-writer", "the output", "The specification's `#` heading and the summary's title are short (at most 72 characters), the description below them", f"{f}:24-25", "a", "card spec-writer.md (Heading and summary title: at most 72 characters)", "grep '72' cards-next/spec-writer.md")
R("spec-writer", "the specification", "Holds the goal in the user's terms; what changes, area by area, naming files, commands, messages and cards", f"{f}:29-30", "a", "card spec-writer.md (It holds: the goal ...; what changes ...)", "child 25")
R("spec-writer", "the specification", "Each decision of `02-answers.md` carried into it: none dropped, none invented", f"{f}:31", "a", "card spec-writer.md (each decision of `02-answers.md`, none dropped, none invented)", "child 25")
R("spec-writer", "the specification", "What is out of scope", f"{f}:32", "a", "card spec-writer.md (what is out of scope)", "child 25")
R("spec-writer", "the CR has an issue", "The CR's `issue:` line(s), copied under the specification's title as `concepts.md` places it", f"{f}:33-34", "c", "topic spec-writer-extras (review_by 0.16.0)", "topics.json validates")
R("spec-writer", "a CI job is added or changed", "The environment the job runs in (system, what is absent that the local machine has), the evidence that proves the job before the push as the project's rules ask, and which differences only the first CI run can prove", f"{f}:35-38", "c", "topic spec-writer-extras (review_by 0.16.0)", "topics.json validates")
R("spec-writer", "what the CR changes depends on the host or a default", "Its host and default matrix (`concepts.md`, \"Words\") in the evidence, one line per cell; name no matrix when there is no such dependency", f"{f}:39-41", "c", "topic spec-writer-extras (review_by 0.16.0)", "topics.json validates")
R("spec-writer", "a check guards a shipped file", "The evidence says the check reads that file from the repository as it ships, at the head under test, not a copy or a text the test prepares", f"{f}:42-45", "a", "card spec-writer.md (A check that guards a shipped file reads that file at the head under test, not a copy)", "child 25")
R("spec-writer", "a check on a shipped file", "A prepared text is only for a case the shipped file cannot hold (a refusal, a broken input), named as such and paired with a check on the shipped file", f"{f}:45-46", "c", "topic spec-writer-extras (added in round 2; review_by 0.16.0)", "topics.json validates")
R("spec-writer", "the specification", "The evidence that proves it: the checks and the scenario steps", f"{f}:47", "a", "card spec-writer.md (the evidence that proves it)", "child 25")
R("spec-writer", "the specification", "Self-containment: a Driver needs nothing else to implement it", f"{f}:48", "a", "card spec-writer.md (self-contained)", "child 25")
R("spec-writer", "an answer is left open", "Not yours to decide: end the specification with a list of questions, which the Chief of Staff takes to the user", f"{f}:50-51", "a", "card spec-writer.md (An open point is a question ...; Never: decide what the answers leave open)", "child 25")
R("spec-writer", "the reply", "Reply in a few lines: the path of the specification, and the open questions if any; with spec-critic fixes, the fixes applied and those not, with why", f"{f}:55-56", "a", "card spec-writer.md (Reply: ...)", "reply-blocks-diff.md")

# ---------------------------------------------------------------- spec-critic
f = "spec-critic.md"
R("spec-critic", "start", "Check one CR's Change Specification before it is final; started by the one who grills (the Chief of Staff or a Griller) in the background, outside any batch; no worktree, round or slot", f"{f}:3-5", "a", "card spec-critic.md (goal; The one who grills starts you in the background)", "child 25")
R("spec-critic", "every run", "You write no file, commit nothing, push nothing", f"{f}:4-5", "a", "card spec-critic.md (You write no file, commit nothing, push nothing)", "grep 'commit nothing' cards-next/spec-critic.md")
R("spec-critic", "reading", "Read in the CR's folder `intake/`, `02-answers.md` and `03-change-spec.md`", f"{f}:9-10", "a", "card spec-critic.md (Read in the CR's folder ...)", "child 25")
R("spec-critic", "reading", "You get no summary of the grill and no case for the specification: judge the spirit of the request from the user's own words", f"{f}:10-12", "a", "card spec-critic.md (judge the request's spirit by the user's words)", "child 25")
R("spec-critic", "reading", "Then read the repository, read-only: the project's rules first (they rank above the card), the files the specification names, and the cards, code, docs and tests around them", f"{f}:12-14", "a", "card spec-critic.md (Then, read-only: the project's rules ..., the files the specification names ...)", "child 25")
R("spec-critic", "reading", "The other items not yet merged (`1-inbox/`, `2-backlog/`, `3-ready/`, `4-batch/1-pending/`, `4-batch/2-actives/`) that touch the same files: request, answers and specification, whichever exist", f"{f}:14-16", "a", "card spec-critic.md (the unmerged items (`1-inbox/` to `4-batch/2-actives/`) on the same files)", "child 25")
R("spec-critic", "an inbox item", "An inbox item often has no specification", f"{f}:16", "b", "inferable", "none")
R("spec-critic", "judging", "Only four things: intent, inconsistency, claim, bundle", f"{f}:20", "a", "card spec-critic.md (Four kinds only)", "child 25")
R("spec-critic", "intent", "A gap with the request's intent: something asked that the specification drops, narrows or bends; something added that nobody asked for; a decision of `02-answers.md` lost or changed", f"{f}:22-24", "a", "card spec-critic.md (1. intent)", "child 25")
R("spec-critic", "intent", "Evidence that does not prove what is asked counts too: a check that guards a shipped file but reads a copy or a prepared text where the shipped file would do; this is about evidence, not an implementation detail", f"{f}:24-27", "a", "card spec-critic.md (a check on a shipped file reading a copy counts)", "child 25")
R("spec-critic", "inconsistency", "With a card, the CLI, the hooks, the docs, the tests or the scenario (an old rule the specification leaves standing against it included), or with another pending item on the same files", f"{f}:27-30", "a", "card spec-critic.md (2. inconsistency)", "child 25")
R("spec-critic", "claim", "An unproved claim about the real world: a statement about a host, a tool, a forge, a model or an outside service that the repository does not prove (the host references' marks: proved, documented, unproved) and that the specification treats as a fact", f"{f}:31-33", "a", "card spec-critic.md (3. claim: ... the repository does not prove, taken as fact)", "child 25")
R("spec-critic", "claim", "The host references' marks: proved, documented, unproved", f"{f}:32-33", "b", "inferable (the claim kind says the repository does not prove it)", "none")
R("spec-critic", "bundle", "The specification joins work that would ship more cheaply as separate CRs (a refactor or feature with a lint, format or type cleanup across files the change does not need; several views, screens or commands that each deliver alone); name the parts and the cut", f"{f}:34-37", "a", "card spec-critic.md (4. bundle: work cheaper as separate CRs; name the parts and the cut)", "child 25")
R("spec-critic", "bundle", "A bundle always touches behaviour (scope): its draft question offers the split first (the parts named), then keeping it whole", f"{f}:37-38", "a", "card spec-critic.md (the draft question offers the split first)", "child 25")
R("spec-critic", "never", "Edit the specification or any file; restyle its prose", f"{f}:42", "a", "card spec-critic.md (Never: edit the specification)", "child 25")
R("spec-critic", "never", "Propose an implementation detail the specification leaves to its Driver", f"{f}:43", "a", "card spec-critic.md (Never: propose implementation details)", "child 25")
R("spec-critic", "never", "Re-ask a question `02-answers.md` already settled, unless its answer rests on an unproved claim or on an inconsistency the user did not see", f"{f}:44-45", "a", "card spec-critic.md (re-ask what `02-answers.md` settled, unless ...)", "child 25")
R("spec-critic", "never", "Repeat or answer the specification's own open questions (raise one only if it is itself wrong, e.g. it rests on an unproved claim)", f"{f}:46-47", "a", "card spec-critic.md (answer the specification's own open questions)", "child 25")
R("spec-critic", "the reply", "One numbered list of findings, each with its kind, where (section; file and line), the evidence in one or two lines, and whether it touches behaviour", f"{f}:51-57", "a", "card spec-critic.md (Reply, numbered: kind; where; evidence; touches behaviour or not)", "reply-blocks-diff.md")
R("spec-critic", "a finding touches behaviour", "Add a draft question for the user with at most 4 options, the recommended one first, so the one who grills can ask it", f"{f}:59-60", "a", "card spec-critic.md (a draft question, at most 4 options, recommended first)", "reply-blocks-diff.md")
R("spec-critic", "a finding does not touch behaviour", "Add the fix in one line", f"{f}:60-61", "a", "card spec-critic.md (Otherwise: the fix in one line)", "reply-blocks-diff.md")
R("spec-critic", "nothing found", "Say \"no finding\"", f"{f}:61", "a", "card spec-critic.md (None: \"no finding\")", "reply-blocks-diff.md")
R("spec-critic", "the reply", "Nothing else: no summary of the specification, no praise; this reply is the only copy of the list", f"{f}:61-62", "a", "card spec-critic.md (No summary, no praise; your reply is the only copy of your list)", "reply-blocks-diff.md")

# ---------------------------------------------------------------- retro-critic
f = "retro-critic.md"
R("retro-critic", "start", "Judge the points of one list of changes that chantier proposes on its own: a batch's retro, a release's retro points, a report's suggestions, an answer such as \"are the workers useful?\"", f"{f}:3-5", "a", "card retro-critic.md (goal)", "child 25")
R("retro-critic", "start", "The Foreman starts you before it writes its section of `4-batch/retro.md`; the Chief of Staff starts you in direct mode for the same retro, and outside any batch before it proposes any list of changes on its own", f"{f}:5-7", "a", "card retro-critic.md (The Foreman or the Chief of Staff starts you before it writes)", "child 25")
R("retro-critic", "start", "Started in the background or not, as the parent needs your answer before it writes", f"{f}:7-8", "b", "inferable", "none")
R("retro-critic", "every run", "You take no slot, no round and no CR; you write no file, commit nothing, push nothing and post nothing", f"{f}:8-9", "a", "card retro-critic.md (you take no slot, round or CR; you write no file, commit nothing, push nothing, post nothing)", "grep 'post nothing' cards-next/retro-critic.md")
R("retro-critic", "every run", "Your reply is the only copy of your verdicts", f"{f}:9", "a", "card retro-critic.md (your reply is the only copy of your verdicts)", "child 25")
R("retro-critic", "reading", "The brief gives, numbered, each point as its author wrote it and, per point, the evidence it cites by path (the CRs' `work/` notes and logs, `events.jsonl`, the batch's report, `cost --explain`'s output)", f"{f}:13-16", "e", "facts (the brief); card retro-critic.md (Your brief numbers each point ... with the evidence it cites by path)", "child 25")
R("retro-critic", "a question needs it", "Read the earlier batches' records (`5-archives/batches/batch-*.md`; kept points only), the card or file a point's fix would change, the listing of the planning folder's open items (folder names and `summary.json` title)", f"{f}:18-23", "a", "card retro-critic.md (Read only what a question needs: ...)", "child 25")
R("retro-critic", "reading", "Read nothing else", f"{f}:22", "a", "card retro-critic.md (Read only what a question needs)", "child 25")
R("retro-critic", "judging", "You get no argument for a point, no ranking and no preference of its author: judge the evidence", f"{f}:22-23", "a", "card retro-critic.md (Judge the evidence, not an author's argument or preference)", "child 25")
R("retro-critic", "a point", "Is the problem real and measured? More than one occurrence (this batch, an earlier batch's record, the logs of the CRs cited), or a cost or a defect that reached the user; a single occurrence with neither is not measured", f"{f}:29-31", "a", "card retro-critic.md (question 1)", "child 25")
R("retro-critic", "a point", "Would the fix change an outcome (fewer asks, fewer rounds, less cost, a defect that no longer reaches the user), or is it ceremony (a new rule, a new line in a report, a check that changes nothing anyone does)?", f"{f}:32-35", "a", "card retro-critic.md (question 2)", "child 25")
R("retro-critic", "a point", "Is it already covered by a card's existing rule, an open item of the planning folder, or another point of the same list?", f"{f}:35-37", "a", "card retro-critic.md (question 3)", "child 25")
R("retro-critic", "the reply", "One line per point, in the brief's numbering: `<n>. keep: <why>`, `<n>. merge with <m>: <why>`, `<n>. drop: <why>`, `<why>` being one line", f"{f}:40-44", "a", "card retro-critic.md (the three line forms)", "reply-blocks-diff.md")
R("retro-critic", "a merge", "A merge names the point it joins; the kept point of a merged pair is the one with the lower number, and its author writes one line that covers both", f"{f}:46-47", "a", "card retro-critic.md (the lower number is kept; a merge counts as dropped); the clause that the author writes one line is cut (the author's act, not the critic's reply)", "reply-blocks-diff.md")
R("retro-critic", "a point covered by an open item", "It is dropped with that item's folder name in its why", f"{f}:47-48", "a", "card retro-critic.md (covered by an open item: its folder name in the why)", "reply-blocks-diff.md")
R("retro-critic", "the last line", "`kept <k>, dropped <d>` (a merged point counts as dropped); with every point dropped, `kept 0, dropped <d>: nothing worth changing`", f"{f}:48-50", "a", "card retro-critic.md (Then `kept <k>, dropped <d>`; all dropped: ...)", "reply-blocks-diff.md")
R("retro-critic", "the reply", "Nothing else", f"{f}:50", "a", "card retro-critic.md (Nothing else.)", "reply-blocks-diff.md")
R("retro-critic", "never", "Rewrite a point, or propose a new one", f"{f}:54", "a", "card retro-critic.md (Never: rewrite a point or propose one)", "child 25")
R("retro-critic", "never", "Judge the tag or the route of a point (the author's and the user's)", f"{f}:55", "a", "card retro-critic.md (judge a point's tag or route)", "child 25")
R("retro-critic", "never", "Ask the user anything", f"{f}:56", "a", "card retro-critic.md (ask the user anything)", "child 25")

# ---------------------------------------------------------------- inspector
f = "inspector.md"
common("inspector", f, dict(intro="3-5", startup="6-7", rules="9-11", english="10-11", nofb="18-20", free="19-20", lacks="20-21", cli_stop="21", claim="27", commit="27", sleep="27-28", stash="28-29", pkill="29-30", chain="30-32", stop="33", failed_worker="34-36"))
R("inspector", "every run", "Work only in the CR's worktree (`cd` there first; the Driver made it, never create one)", f"{f}:15-16", "a", "card inspector.md (Never: create a worktree); facts (`worktree:`)", "child 25")
R("inspector", "every run", "You write nothing: your reply is your output", f"{f}:16-17", "a", "card inspector.md (You write nothing: your reply is your output)", "grep 'You write nothing' cards-next/inspector.md")
R("inspector", "a refusal", "A denied permission or a refusal is reported to the Driver with its exact text, never worked around", f"{f}:16-17", "f", "floor 9", FS)
R("inspector", "evidence", "Evidence is a command run at the pushed head, with its output; notes and green CI are not proof", f"{f}:22-23", "a", "card inspector.md (Evidence is a command run there, with its output; notes and green CI are not proof)", "child 25")
R("inspector", "a check is red on the default branch", "It is not the CR's: report it, do not fix it there", f"{f}:23-24", "a", "card inspector.md (A check red on the default branch is not the CR's); \"report it, do not fix it there\" cut: you write nothing", "child 25")
R("inspector", "every judgment", "Every judgment names the SHA it covers", f"{f}:24-25", "a", "card inspector.md (Judge at the pushed head, naming its SHA)", "child 25")
R("inspector", "a move", "A move is any change of the head after a judgment (a new round, a rebase, a restack, a conflict resolution); after a move, what the move touched is judged again and the rest is carried, saying so", f"{f}:24-26", "a", "card inspector.md (After a move ..., judge only what it touched and say in `minor` what you carried)", "child 25")
R("inspector", "the task", "Review the round's diff (the worktree against its base, uncommitted and untracked files included) against the project's rules, the specification and the Coder's notes", f"{f}:40-41", "a", "card inspector.md (Review the round's diff ...)", "child 25")
R("inspector", "the task", "Read only; you may run the fast gate to check a claim", f"{f}:41-42", "b", "inferable (a command run at the head is evidence: the card says so)", "none")
R("inspector", "the reply", "Reply with JSON only: `{\"verdict\": \"APPROVE | FIX-REQUIRED\", \"head\": \"<sha>\", \"blocking\": [...], \"minor\": [...], \"confidence\": 0.0}`", f"{f}:42-45", "a", "card inspector.md (the same line)", "reply-blocks-diff.md")
R("inspector", "the reply", "`head` is the worktree's `git rev-parse HEAD` at the review: the verdict covers that commit plus the uncommitted diff reviewed", f"{f}:48-49", "a", "card inspector.md (`head` is the full 40-character `git rev-parse HEAD` of the worktree, always present); \"plus the uncommitted diff\" is cut (inferable from the task line)", "reply-blocks-diff.md")
R("inspector", "a move was given", "Review only what the move changed in the CR's own patch (`git range-diff` for a rebase or a restack; the diff for a resolved conflict), and say in `minor` what you carried unchanged", f"{f}:49-52", "c", "topic inspector-audit (Carry); card inspector.md (After a move ...)", "topics.json validates")
R("inspector", "the reply's cap", "Each item in `blocking` and `minor` is one sentence of at most 300 characters, starting with `file:line:` or `pr-body.md: <section>:` when it has a place", f"{f}:56-57", "a", "card inspector.md (An item is one sentence of at most 300 characters, starting `file:line:` or `pr-body.md: <section>:`)", "reply-blocks-diff.md")
R("inspector", "the reply's cap", "`minor` holds at most five items; the fifth says `and <n> more of the same kind` and names the kind", f"{f}:58-59", "a", "card inspector.md (`minor` holds at most five ...)", "reply-blocks-diff.md")
R("inspector", "the reply's cap", "An item states a defect; what was checked and found right does not go in the reply", f"{f}:60", "a", "card inspector.md (stating a defect)", "reply-blocks-diff.md")
R("inspector", "the reply's cap", "The whole reply stays under 3,000 characters", f"{f}:61", "a", "card inspector.md (Reply under 3,000 characters)", "reply-blocks-diff.md")
R("inspector", "the reply's cap", "`blocking` is not limited in number: each item there is worth a round, and keeps the 300-character limit", f"{f}:62-63", "b", "inferable (the 300-character limit is kept; nothing caps the count)", "none")
R("inspector", "the diff touches `hooks/`", "It is checked for the CR's gate record holding `just mod` (CI does not run it): a missing one is `blocking`", f"{f}:65-66", "a", "card inspector.md (A diff touching `hooks/` needs `just mod` in the gate record, else blocking)", "grep 'just mod' cards-next/inspector.md")
R("inspector", "classifying", "`blocking` holds only defects worth another round: a project rule broken, wrong behavior, a missing test, a broken gate, a part of the specification missed; style the project has no rule on goes to `minor`", f"{f}:68-70", "a", "card inspector.md (`blocking` holds only defects worth another round ...)", "child 25")
R("inspector", "you cannot judge", "`FIX-REQUIRED` with one blocking item saying so", f"{f}:70", "a", "card inspector.md (You cannot judge: `FIX-REQUIRED` with one blocking item)", "child 25")
R("inspector", "a host and default matrix is named", "Each cell needs a test or a check in the diff that runs its real flow; a cell with none, or one tested only on a record or configuration shape built by hand, is `blocking`", f"{f}:72-74", "c", "topic inspector-audit (Matrix)", "topics.json validates")
R("inspector", "from round 1", "Each test the specification names that guards a shipped file must read that file as it ships, at the head under test; a named test missing from the diff, or one that checks only a prepared text where the shipped file would do, is `blocking`", f"{f}:76-78", "a", "card inspector.md (A test the specification names that guards a shipped file must be in the diff and read it as shipped ... else blocking)", "child 25")
R("inspector", "a CR's round", "Read `<work folder>/pr-body.md` with the diff and audit it against the project's PR template and rules, else against `pr-template.md` (its audit list); when the CR was grilled, also read its `02-answers.md` for the Human decisions item", f"{f}:80-83", "c", "topic inspector-audit (pr-body.md)", "topics.json validates")
R("inspector", "a CR's round", "A missing `pr-body.md` or a failed audit item is `blocking`, written `pr-body.md: <section>: ...`", f"{f}:83-84", "c", "topic inspector-audit (pr-body.md); card inspector.md names `pr-body.md: <section>:` as an item start", "topics.json validates")
R("inspector", "the exact reply", "One JSON object and nothing around it (no prose, no code fence), with exactly the keys `verdict`, `head`, `blocking`, `minor`, `confidence`", f"{f}:88-89", "a", "card inspector.md (Reply with JSON only, no prose, no code fence, exactly these keys)", "reply-blocks-diff.md")
R("inspector", "the exact reply", "`verdict` is the word `APPROVE` or `FIX-REQUIRED`, nothing else (not `APPROVED`, not `FIX REQUIRED`, not lower case)", f"{f}:90-91", "a", "card inspector.md (`verdict` is `APPROVE` or `FIX-REQUIRED`, nothing else)", "reply-blocks-diff.md")
R("inspector", "the exact reply", "`head` is the full 40-character SHA, always present", f"{f}:92-93", "a", "card inspector.md (same sentence)", "reply-blocks-diff.md")
R("inspector", "the exact reply", "`blocking` and `minor` are lists of strings (empty lists when nothing); `confidence` is a number from 0 to 1", f"{f}:94-95", "a", "card inspector.md (same sentence)", "reply-blocks-diff.md")

# ---------------------------------------------------------------- verifier
f = "verifier.md"
common("verifier", f, dict(intro="3-5", startup="6-7", rules="9-11", english="10-11", worktree="15", never_create="15-16", guard="16-19", denied="18-19", nofb="20-22", free="21-22", lacks="22-23", cli_stop="23", notes="24-26", notes_beh="Keep your notes in `<work folder>/verifier/` and proof in the CR folder's `evidence/` (the before and after in `<work folder>/verifier/evidence/`, `verify.md` at `<work folder>/verify.md`)", rawlog="26-27", claim="38", commit="56", sleep="56", stash="56-57", pkill="57-58", chain="59-61", overwrite="61-62", bom="62-63", stop="64", failed_worker="65-68"))
R("verifier", "a CI artifact is downloaded", "It goes under the `scratch:` folder (`<CR folder>/work/scratch/artifacts-<run id>/`), never under `<work folder>/verifier/` or `evidence/`: it stays on this machine, never published; copy into the evidence only the small part that proves a claim", f"{f}:27-30", "a", "card verifier.md (A CI artifact goes under `scratch:` ..., never published)", "child 25")
R("verifier", "evidence", "Evidence is a command run at the pushed head, with its output (except a matrix probe, run at the committed head before the CR's first push); notes and green CI are not proof", f"{f}:31-32", "a", "card verifier.md (Prove, at the pushed head ...; their notes and green CI are not proof); topic verifier-delta-matrix (matrix probe)", "child 25")
R("verifier", "a check is red on the default branch", "It is not the CR's: report it, do not fix it there", f"{f}:33-34", "a", "card verifier.md (A check red on the default branch is not the CR's); \"report it\" cut in round 2 for size: you never edit code, so \"do not fix it there\" is inferable", "child 25")
R("verifier", "every judgment", "Every judgment names the SHA it covers; after a move, what the move touched is judged again and the rest is carried, saying so", f"{f}:34-36", "a", "card verifier.md (each claim with the SHA it was judged at; carried claims keep their SHA and say so); topic verifier-delta-matrix", "child 25")
R("verifier", "a clean rebase", "A clean rebase that leaves the CR's patch unchanged, proved by git's exact patch-ids, recorded at `ship`, touches no judgment; CI at the new head still runs", f"{f}:36-37", "e", "topic verifier-delta-matrix (the `carry` event, `ship`)", "topics.json validates")
R("verifier", "a probe of the board's write paths", "It never points at the project's live planning folder; the project's own tests keep their fixtures and tmp folders as they are", f"{f}:38-41", "a", "card verifier.md (Never: aim a test, smoke run or probe ... at the live planning folder); topic verifier-scratch (the project's own tests keep their fixtures)", "grep 'live planning folder' cards-next/verifier.md")
R("verifier", "a throwaway project", "A scratch planning folder, a probe project or a hand-run smoke run goes under the `scratch:` folder the brief gives, never a temporary folder or a path outside the `writes:` folders, and you remove it at your end", f"{f}:41-45", "c", "topic verifier-scratch (review_by 0.16.0); facts (`scratch:`)", "topics.json validates")
R("verifier", "the scratch project", "It is its own git repository: run `git init <scratch project>` before anything else there and before any chantier command", f"{f}:45-46", "c", "topic verifier-scratch (review_by 0.16.0)", "topics.json validates")
R("verifier", "a chantier call aimed at the scratch project", "It names it: `--project <scratch project's folder>`, or runs with the scratch repository as working folder and no `--project` and no `CHANTIER_ROOT` that points elsewhere", f"{f}:46-49", "c", "topic verifier-scratch (review_by 0.16.0)", "topics.json validates")
R("verifier", "a chantier call aimed at the scratch project", "Never use the prompt's `$CHANTIER` line as printed there: it names the live project", f"{f}:49-50", "a", "card verifier.md (Never: aim ... the prompt's `$CHANTIER` at the scratch project (`help verifier-scratch`))", "grep 'scratch' cards-next/verifier.md")
R("verifier", "a scratch path too long for Windows", "A write, a `git` command or a tool failing on its length is a stop: report it to the Driver with the exact error text; no shorter folder outside the `writes:` folders, no other workaround; the claim is then not proved", f"{f}:51-55", "c", "topic verifier-scratch (review_by 0.16.0); floor 9", "topics.json validates")
R("verifier", "the reply", "The reply is the template at the end and nothing else (no greeting, no summary, no list of what was checked and found right): the whole of the output to the Driver", f"{f}:64-66", "a", "card verifier.md (Reply in at most ten lines, after `verdict` has run; the block)", "reply-blocks-diff.md")
R("verifier", "the task", "Prove, at the pushed head, that the CR does what its specification says", f"{f}:72-73", "a", "card verifier.md (goal)", "child 25")
R("verifier", "the task", "You are never the round's Coder or Inspector; their notes and green CI are not proof", f"{f}:73-74", "a", "card verifier.md (You are never the round's Coder or Inspector)", "child 25")
R("verifier", "the task", "Never edit code", f"{f}:74", "a", "card verifier.md (Never edit code)", "grep 'Never edit code' cards-next/verifier.md")
R("verifier", "the gate pass", "You cite the pass in `verify.md` by the gate log's first line (the CR and the full SHA it ran at) and `handoff`'s checklist, at the full SHA verified; the CLI is what refuses a hand-back without a gate pass", f"{f}:74-76", "e", "card verifier.md (Cite the gate pass by its log's first line and `handoff`); refusal: `handback` without a gate pass", "child 25")
R("verifier", "no gate pass at that head", "Run `$CHANTIER gate <cr> <name>` (one name per argument, from `long_gate.commands`, never a `;` or `&&` chain) only when no pass exists at that head and a claim only the long suite proves, and only for the project's long gate; a short check you run directly and cite", f"{f}:76-79", "a", "card verifier.md (Run `$CHANTIER gate <cr> <name>` ... only for the long gate with no pass at that head; run a short check directly)", "child 25")
R("verifier", "the gate", "`gate` is refused on a dirty tree", f"{f}:77", "e", "refusal: `gate` (dirty tree)", "child 25")
R("verifier", "the output", "`<work folder>/verify.md` (the work folder's root, the one file the CLI reads): a `Head: <full SHA>` line, each claim with the SHA it was judged at, the command and the output that prove it, and `VERIFIED` or `NOT VERIFIED`", f"{f}:79-81", "a", "card verifier.md (`verify.md` holds a `Head: <full SHA>` line, then each claim ...)", "child 25")
R("verifier", "a claim that something is refused, absent or unchanged", "Its proof is the command that shows it and that command's output; a claim without them is out of format", f"{f}:81-83", "a", "card verifier.md (also for a claim that something is refused, absent or unchanged; a claim without them is out of format)", "child 25")
R("verifier", "after `verify.md`", "Run `$CHANTIER verdict <cr> VERIFIED` or `$CHANTIER verdict <cr> \"NOT VERIFIED\"` from the worktree at the head verified, before you reply (the last verdict at a head decides)", f"{f}:83-85", "a", "card verifier.md (run `$CHANTIER verdict <cr> VERIFIED` or ... before you reply); \"the last verdict decides\" is the CLI's semantics (e)", "child 25")
R("verifier", "`verdict VERIFIED` is refused (exit 2)", "It is refused until `verify.md` has a `Head:` line naming that full SHA: write or fix the note and run `verdict` again, in the same run, before you reply", f"{f}:85", "e", "refusal: `verdict` (Head: line); card verifier.md (`VERIFIED` is refused (exit 2) until ...: fix the note, run it again)", "child 25")
R("verifier", "a claim carried", "It keeps its own SHA and says why the move did not touch it (`carried from <sha7>: <reason>`)", f"{f}:85-86", "a", "card verifier.md (A claim carried ... says `carried from <sha7>: <reason>`)", "child 25")
R("verifier", "evidence cannot be captured", "It does not alone change the verdict; if the project's rules require it, its absence is `NOT VERIFIED`", f"{f}:86-87", "a", "card verifier.md (same sentence)", "child 25")
R("verifier", "the description", "The PR's description, as posted on the forge, is one of the claims: it must render, be consistent with the diff at the pushed head, and no attached image shows the user's username or home folder; a failure of any is `NOT VERIFIED`", f"{f}:90-94", "c", "topic verifier-description (review_by 0.16.0); card verifier.md (The PR's description is a claim too); floor 8", "topics.json validates")
R("verifier", "the description", "Each proof in the description names its SHA (the head, or `carried from <sha7>` with its reason); a claim stated as fact with no proof is `NOT VERIFIED` (the Driver marks it `UNVERIFIED` or narrows it); a `STALE` mark left at the end is `NOT VERIFIED`", f"{f}:94-98", "c", "topic verifier-description (review_by 0.16.0)", "topics.json validates")
R("verifier", "the description's Known gaps", "It holds a bullet for each `**UNVERIFIED:**` claim, each evidence pair `before-after.md` says was not captured, and each failed claim accepted rather than fixed; a missing one, or \"None\" while one exists, is `NOT VERIFIED`", f"{f}:98-102", "c", "topic verifier-description (review_by 0.16.0)", "topics.json validates")
R("verifier", "a role name in the description", "It is judged by `pr-template.md`, \"The rules\" (internal references): a product term of a change to that role is not a failure, the doer of the work outside Internal references is", f"{f}:102-104", "c", "topic verifier-description (review_by 0.16.0)", "topics.json validates")
R("verifier", "given only the description", "Check only it, and record its verdict the same way; a description found `NOT VERIFIED` cancels an earlier `VERIFIED` at that head until a later pass says `VERIFIED`", f"{f}:104-106", "c", "topic verifier-description (review_by 0.16.0)", "topics.json validates")
R("verifier", "the Review box", "`Review: approved at <sha7>` is judged against the Driver's note of the pass, read with `$CHANTIER log <cr>` (complete; `handoff` shows only the last ten)", f"{f}:108-110", "c", "topic verifier-review-box (review_by 0.16.0)", "topics.json validates")
R("verifier", "the Review box", "A note of an approved pass whose SHA is the one the box cites (the reviewed `head`, the round's `committed as <sha>`, the move's head; for `carried from <sha7>` that `<sha7>`) proves the claim; no such note, or another SHA, is `NOT VERIFIED`; it proves that a review happened, not the code", f"{f}:110-114", "c", "topic verifier-review-box (review_by 0.16.0)", "topics.json validates")
R("verifier", "started after a move", "A Verifier is not started for a clean rebase that leaves the patch unchanged (a `carry` event)", f"{f}:116-117", "e", "topic verifier-delta-matrix; the `carry` event of `ship`", "topics.json validates")
R("verifier", "started after a move", "Given the previous `verify.md` (or `matrix-r<n>.md`) and a move, judge again each claim the move touched and the claims that failed; carry the others", f"{f}:118-121", "c", "topic verifier-delta-matrix (review_by 0.16.0)", "topics.json validates")
R("verifier", "a claim is touched", "When the move changed a file, a behaviour or a dependency its proof exercises: the CR's patch changed (the diff or the range-diff), or the base brought changes to what the proof runs (`git diff --name-only <old base> <new base>`); in doubt, judge it again", f"{f}:121-124", "c", "topic verifier-delta-matrix (review_by 0.16.0)", "topics.json validates")
R("verifier", "before and after pairs after a move", "Capture again only a pair the move touched", f"{f}:124-125", "c", "topic verifier-delta-matrix (review_by 0.16.0)", "topics.json validates")
R("verifier", "`matrix probe` in the note", "Prove each cell of the matrix the prompt gives, at the worktree's committed head (not pushed)", f"{f}:127-128", "c", "topic verifier-delta-matrix (review_by 0.16.0)", "topics.json validates")
R("verifier", "a matrix probe", "Use each cell's real flow from a real state: the CLI's own commands on a scratch project or the project's test fixtures, under the scratch rules, with no user file for a shipped-default cell; a hand-built shape proves no cell", f"{f}:128-131", "c", "topic verifier-delta-matrix (review_by 0.16.0)", "topics.json validates")
R("verifier", "a matrix probe", "Write `<work folder>/verifier/matrix-r<n>.md`, with a `Head:` line and each cell as a claim (SHA, command, output); run no `verdict` and no gate, capture no before/after, check no PR description; reply with the template, `Proof:` naming that file", f"{f}:131-133", "c", "topic verifier-delta-matrix (review_by 0.16.0)", "topics.json validates")
R("verifier", "the end", "Capture the before on a detached worktree of the CR's base (`git worktree add --detach <path> <base>`, the one worktree you create; remove it at your end) and the after at the pushed head, so the two compare", f"{f}:135-138", "a", "card verifier.md (Never: ... create a worktree (but the detached base of the before and after)); topic verifier-before-after", "child 25")
R("verifier", "the end", "The files go to `<work folder>/verifier/evidence/`, with a `before-after.md` listing each pair, what it shows and how to reproduce it, and the SHA of the before and of the after; evidence you cannot capture: `before-after.md` says why", f"{f}:138-141", "c", "topic verifier-before-after (review_by 0.16.0); card verifier.md (owns your before and after in `<work folder>/verifier/evidence/`)", "topics.json validates")
R("verifier", "screenshots or videos", "Open each one and check that it shows what the PR claims of it: the screen, the state and the change the Summary, Deliverables and Impacts say, legible, with nothing that contradicts them; a capture that does not show its claim fails that claim", f"{f}:141-144", "c", "topic verifier-before-after (review_by 0.16.0)", "topics.json validates")
R("verifier", "the description pass", "Check that the images attached are the ones captured at the SHA they name, and give each the look; `verify.md` names an image that fails (which one, what shows), so the Driver replaces it", f"{f}:144-146", "c", "topic verifier-description and verifier-images (review_by 0.16.0)", "topics.json validates")
R("verifier", "an image of a capture", "Every before and after image you capture shows made-up paths and no username (the username is the login name of the machine and the last part of the home folder's path; the home folder is its full path in any form on screen)", f"{f}:148-153", "a", "card verifier.md (Never: keep an image that shows the username or the home folder); floor 8; terms in topic verifier-images", "quiz floor-8-verifier-screenshot")
R("verifier", "an image of a capture", "A made-up path holds neither the username nor the home folder, wherever the image shows a local path; how you get it is yours (a made-up folder name, `~`, `user`)", f"{f}:153-155", "c", "topic verifier-images (review_by 0.16.0); floor 8", "quiz floor-8-verifier-screenshot")
R("verifier", "a capture of the scratch project", "It sits under the user's home folder, so a capture shows the user's paths: rewrite them to made-up paths in the capture", f"{f}:155-157", "c", "topic verifier-images and verifier-scratch (review_by 0.16.0)", "topics.json validates")
R("verifier", "an image", "The look: open the image as an image and look for both; it passes once neither shows; give each capture the look; one that fails is captured again with made-up paths before it is kept in `<work folder>/verifier/evidence/`; one you cannot capture that way is not kept and `before-after.md` names it with why", f"{f}:157-161", "a", "card verifier.md (open every screenshot you capture or the PR carries); topic verifier-images (the look)", "quiz floor-8-verifier-screenshot")
R("verifier", "the reply", "The exact reply, at most ten lines, after `verdict` has run: `VERIFIED | NOT VERIFIED`, `Head: <full SHA verified>`, `Proof: <work folder>/verify.md`, `Failed: <claim>: <one line why>`", f"{f}:163-170", "a", "card verifier.md (the same block, byte for byte)", "reply-blocks-diff.md")
R("verifier", "the reply", "The first line is exactly one of the two words; one `Failed:` line per failed claim, none when `VERIFIED`; past six, the sixth says `Failed: and <n> more, in verify.md`", f"{f}:172-173", "a", "card verifier.md (same sentence)", "reply-blocks-diff.md")
R("verifier", "the reply", "Each claim's command and output stay in `verify.md`, never in the reply", f"{f}:173-174", "a", "card verifier.md (Each claim's command and output stay in `verify.md`)", "reply-blocks-diff.md")

# ---------------------------------------------------------------- griller (## Started from the board, griller.md:102-136)
f = "griller.md"
G = lambda a, b=None: f"{f}:{a}" + (f"-{b}" if b else "")
R("board-griller", "started by the board", "Started by the surface server, headless, one run per message typed in the web board, resumed from the run before", G(104, 105), "a", "card griller.md (The surface server starts you headless ...)", BR)
R("board-griller", "started by the board", "The conversation is shared by every holder of the private key, so the words may come from more than one person", G(105, 106), "a", "card griller.md (same sentence)", BR)
R("board-griller", "started by the board", "You take no seat (skip `session-start.md`'s seat reading and title), start no watcher, server or hub", G(106, 108), "a", "card griller.md (You take no seat and start no watcher, server or hub)", BR)
R("board-griller", "started by the board", "Never open, pause, order or steer anything (\"Never\" holds)", G(108, 108), "a", "card griller.md (You never: open, pause, order or steer anything ...)", BR)
R("board-griller", "the brief", "The brief names the CR's folder: you grill that CR only; \"From the files\" holds: re-read the folder at each run", G(110, 111), "a", "card griller.md (Your brief names the CR's folder ...: you grill that CR only, and re-read its folder at each run)", BR)
R("board-griller", "a planning surface", "\"In a planning surface\" holds but its `seat` reading: skip it (the server has checked the writer before the run)", G(111, 113), "e", "inferable from the server (it checks the writer before the run); card keeps no seat", "none")
R("board-griller", "reading", "You may read the project, the planning folder and the plugin's skill folder (your card, the startup core, your host's reference), nothing else", G(113, 114), "a", "card griller.md (You may read the project, the planning folder and the plugin's skill folder, nothing else)", BR)
R("board-griller", "grilling", "Grill as \"What you do\" says, for that CR: questions in the user's language, each answer recorded in `02-answers.md` at once, the restatement before \"grilled enough?\"", G(116, 118), "a", "card griller.md (round 2: You grill that CR: questions in the user's language, each answer recorded in `02-answers.md` at once, a restatement before ...)", BR)
R("board-griller", "grilled enough", "At \"grilled enough?\" the destination is asked and recorded as the Chief of Staff's \"Where the CR goes\" (`chief-of-staff-grill.md`) says", G(118, 119), "a", "card griller.md (you ask and record the destination (next batch or running batch)); the pointer to `chief-of-staff-grill.md` is cut (that card is not this CR's)", BR)
R("board-griller", "never", "You do not start a spec-writer or a spec-critic, run `file`, `triage`, `abandon` or `restore`, or set a label or a group; you tell the user that the Chief of Staff (or a desktop Griller) specifies and places the CR", G(120, 122), "a", "card griller.md (You never: start a spec-writer ..., tell the user that the Chief of Staff ... specifies and places the CR)", BR)
R("board-griller", "an `issue:` line", "You write no issue drafts: the Chief of Staff drafts them when it starts the spec-writer", G(122, 124), "a", "card griller.md (write issue drafts: the Chief of Staff drafts them)", BR)
R("board-griller", "a question for the Chief of Staff", "You send no `[griller→chief-of-staff]` line: tell the user to put the question or request to it", G(124, 125), "a", "card griller.md (send a `[griller→chief-of-staff]` line ...)", BR)
R("board-griller", "writing", "You write only in the CR's folder (prototypes included, as \"A CR's folder holds its work\" says)", G(127, 127), "a", "card griller.md (You write only in that CR's folder); \"prototypes included\" cut (inferable: a prototype is a file in the folder)", BR)
R("board-griller", "commands", "You run only these commands: `$CHANTIER rules`, `$CHANTIER access`, `$CHANTIER summary lint <the CR's folder>` and `$CHANTIER summary set <the CR's folder> ...`, and no other `chantier` command", G(128, 130), "a", "card griller.md (You run only these commands ...)", BR)
R("board-griller", "the summary", "(the summary rule of this card holds)", G(129, 130), "f", "the rest of griller.md, which child 22 rewrites (a pointer to another section, not a rule)", "child 25")
R("board-griller", "a tool refused by the limits", "Say it in one line; never another way", G(130, 131), "a", "card griller.md (A tool your limits refuse: say it in one line, never go another way)", BR)
R("board-griller", "the end", "When the user has said \"grilled enough\" and the destination is recorded, end the reply with the line `[griller→board] grilled enough: <next batch|running batch>`", G(133, 134), "a", "card griller.md (same line, \"the exact line\")", "reply-blocks-diff.md")
R("board-griller", "the cost", "Your cost is in no batch", G(136, 136), "d", "card griller.md (Your cost is in no batch) (kept: it is one line of the old section)", BR)


# ---------------------------------------------------------------- output
def esc(x):
    return x.replace("|", "\\|")


lines = []
lines.append("# SC19 evidence: inventory of the worker cards' rules")
lines.append("")
lines.append("Round 2 rebuild. The draft is the seed of child 25; its ids (`W-nnn`) are drafts that child 26 replaces.")
lines.append("")
lines.append("## How the sources were walked")
lines.append("")
lines.append("- The sources are the ten worker cards at the base (`f7b74e64`), `skills/chantier/references/{coder,conflict-resolver,debugger,investigator,demo-explorer,spec-writer,spec-critic,retro-critic,inspector,verifier}.md`, and the `## Started from the board` section of `griller.md` (lines 102-136), each read with `cat -n`, top to bottom, one card at a time.")
lines.append("- One row per sentence that states a behaviour, a never, a path, a format or an exception. Pure transitions get no row. A sentence repeated word for word on several cards (the ground rules that all workers share) gets one row per card, with that card's own line numbers. Two short sentences that state one rule in one breath are one row.")
lines.append("- `source` is `file:line` (or a range) in the old card at the base, so each row can be checked against `git show f7b74e64:skills/chantier/references/<file>`; a row whose behaviour is not in the old text says so in `source` (`none`) and is kept only to show where a rule now lives.")
lines.append("- `kind` is study-fable's a to f: a protects the user or the repository, b inferable, c incident, d trial bookkeeping, e CLI-printable, f duplicate. Kind c rows kept in a topic carry `review_by` 0.16.0 (answer 10). When unsure, the row is a.")
lines.append("- `new home` uses the spec's words: `card <file>`, `floor <n>`, `refusal ...`, `topic <name>`, `facts`, `host row <id>`, `inferable`. The new cards are `skills/chantier/cards-next/<role>.md`; the board-griller's section is `griller.md`.")
lines.append("- `check` names what proves the row: a quiz case id under `evals/quiz/<role>/`, a `grep` on the new card, a script check, or `child 25` (the committed inventory and its tests).")
lines.append("- Round 2 corrected round 1: rows that were not in the old text were removed or flagged (conflict-resolver \"Never commit, force\" and \"Step-by-step reading of conflict markers\", demo-explorer \"Run the demo as a user would\", debugger \"Never edit outside the change\"); the old text says instead: conflict-resolver:26 \"You never commit, push or merge\", conflict-resolver:44 \"never `git rebase --exec` or `-x`\", debugger:47-48 \"change no file of the worktree\", demo-explorer:14-15 \"you never commit, push, comment or open a PR\".")
lines.append("")
lines.append("| id | role | trigger | behaviour | source | kind | new home | check |")
lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
for i, (role, trig, beh, src, kind, home, chk) in enumerate(rows, 1):
    lines.append(f"| W-{i:03d} | {role} | {esc(trig)} | {esc(beh)} | {esc(src)} | {kind} | {esc(home)} | {esc(chk)} |")
lines.append("")
ka = [(i, r) for i, r in enumerate(rows, 1) if r[4] == "a"]
lines.append("## Kind a rows and their home")
lines.append("")
lines.append(f"{len(ka)} rows. Each home is a card, the floor or a refusal (F5); none is a topic alone.")
lines.append("")
lines.append("| id | role | behaviour | home |")
lines.append("| --- | --- | --- | --- |")
bad = []
for i, r in ka:
    h = r[5]
    if not (h.startswith("card ") or h.startswith("floor") or h.startswith("refusal")):
        bad.append((i, h))
    lines.append(f"| W-{i:03d} | {r[0]} | {esc(r[2][:110])} | {esc(h)} |")
lines.append("")
kb = [(i, r) for i, r in enumerate(rows, 1) if r[4] == "b"]
lines.append("## Inferable rows (kind b)")
lines.append("")
lines.append(f"{len(kb)} rows. None is kind a.")
lines.append("")
lines.append("| id | role | behaviour | why inferable |")
lines.append("| --- | --- | --- | --- |")
for i, r in kb:
    lines.append(f"| W-{i:03d} | {r[0]} | {esc(r[2][:110])} | {esc(r[5])} |")
lines.append("")
kc = sum(1 for r in rows if r[4] == "c")
lines.append("## Counts and notes")
lines.append("")
from collections import Counter
cnt = Counter(r[4] for r in rows)
lines.append("- Rows: " + str(len(rows)) + "; by kind: " + ", ".join(f"{k} {cnt[k]}" for k in sorted(cnt)) + ".")
lines.append("- Kind c rows are the answer-10 rules (topics with `review_by` 0.16.0).")
lines.append("- No `new home` is empty. Every kind-a home is a card, the floor or a refusal. No kind-b row is kind a.")
lines.append("- Rules cut for size, kept visible: the verifier's \"report it\" after \"A check red on the default branch is not the CR's\" (the Verifier never edits code); the inspector's \"report it, do not fix it there\" (the Inspector writes nothing); both are in the rows above.")
lines.append("- Griller rows point to the rest of the old griller card (\"What you do\", \"From the files\", \"the summary rule\"), which child 22 rewrites: the section now states the grilling it needs on its own.")
with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")
print(len(rows), dict(cnt), "bad kind-a homes:", bad)
