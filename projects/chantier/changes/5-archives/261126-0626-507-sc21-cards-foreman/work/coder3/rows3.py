import json, pathlib
CRF = pathlib.Path(r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/507-sc21-cards-foreman/work/coder3")
TJ = pathlib.Path(r"C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next/topics.json")
pj = json.load(open(CRF / "parts.json"))
parts = pj["parts"]
C, G, CG = ["chief-of-staff"], ["griller"], ["chief-of-staff", "griller"]
R = "0.16.0"
# name: (roles, trigger, review_by)
T = {
 "grill-series": (CG, "a series of questions to the user, a CR's answers", None),
 "grill-options": (CG, "the options of a question, a recommended answer", None),
 "grill-backlog": (CG, "filing, moving, triaging or grouping a CR; the backlog's labels", None),
 "grill-restate": (CG, "before asking 'grilled enough?', a restatement", None),
 "grill-specify": (CG, "the spec-writer or the spec-critic to start, a specification to apply", None),
 "grill-critic": (CG, "an impactful CR's specification", None),
 "grill-critic-steps": (CG, "a spec-critic's report to apply", None),
 "where-cr-goes": (CG, "'grilled enough': the destination of a CR", None),
 "grill-surface": (CG, "a CR of another project of the surface, a relay", None),
 "grill-outside-pr": (CG, "'archive <link>', a PR follow-up on a ticket", R),
 "ticket-summary": (CG, "a CR with an `issue:` line, a summary for a ticket", None),
 "ticket-summary-post": (C, "the user's yes to post a drafted text on a ticket", None),
 "session-start": (CG, "a session's first turn, a failed P6 or P7", None),
 "session-start-surface": (CG, "no `--project`, a `planning:` pointer in AGENTS.md", None),
 "seat": (CG, "`seat` output, a role question, 'become chief of staff' or 'griller'", None),
 "first-turn": (CG, "a session's first message to the user", None),
 "reload": (CG, "'chantier reload', a skill argument `reload`, a host reload", None),
 "titles": (CG, "a role set or changed, a session to rename", None),
 "writer": (CG, "a `writer:` line, a journal `sync-*` line", None),
 "griller-worktree": (G, "a Griller in a worktree", None),
 "griller-cost": (G, "the cost of a Griller", None),
 "board": (C, "the board, the surface server, `serve`, a `board` line", None),
 "board-lines": (C, "a `board on`, `board already running` or `error: board not started` line", None),
 "board-restart": (C, "`board runs another build`, a new key, a restart", None),
 "watcher": (C, "a `watch: not running` line, the session's first yes", None),
 "watcher-lines": (C, "a `watch:` start or end line", None),
 "watcher-events": (C, "a watcher's notification or end, a `forge saw` line", None),
 "watcher-board": (C, "a `board wrote (...)` line", None),
 "watcher-pull": (C, "no watcher can wake the session, `watch --once`", None),
 "remote-login": (C, "'board on my phone', `webui`, `chantier login`", R),
 "allow-rules": (C, "a P10 warn line, the allow-rules question", None),
 "allow-rules-more": (C, "a broad or stale rule, a no, a refused settings edit", R),
 "forge-permissions": (C, "P9 at a first turn or step 1 of a batch (GitHub)", None),
 "forge-permissions-say": (C, "what the first message says of the forge", None),
 "forge-permissions-gitlab": (C, "P9 on a GitLab remote", None),
 "config": (C, "`chantier.yaml`, `playbook`, a role's agent or model", None),
 "project-rules": (C, "a session's start, a long gate to name", None),
 "options": (C, "an option to offer the user", None),
 "refusals-to-say": (C, "the user asks for what the CLI will refuse", None),
 "refusals-to-say-more": (C, "a release word, a CR with no specification, rounds, an unpriced model", None),
 "compacting": (C, "context above 100k tokens, a tip moment", R),
 "delivery-time": (C, "a plan, a report, a sentence that says when work will be done", None),
 "trials": (C, "step 1 of a batch, a permission trial", None),
 "batch-plan": (C, "the user's go to run CRs, up to `open`", None),
 "batch-plan-show": (C, "the plan shown at the go, an empty batch, a waiver", None),
 "batch-plan-mode": (C, "the mode question, the steering mode, a forced `foreman` or `direct`", None),
 "batch-plan-cut": (C, "a time given by the user, a wait between CRs", None),
 "foreman-start": (C, "`open`, the Foreman to start", None),
 "foreman-start-more": (C, "a Foreman to reuse, a Foreman in a worktree, `ready <batch>`", None),
 "steering-reports": (C, "`status`, a Progress report, a delivery slip", None),
 "refused-push-chief": (C, "`[foreman→chief-of-staff] push <branch> ...`, a Driver's `push` line in direct mode", None),
 "refused-push-chief-more": (C, "a push judged not legitimate, a host refusal of your push", None),
 "refused-rebase-chief": (C, "`[foreman→chief-of-staff] rebase <branch> <base>`", None),
 "refused-forge-chain": (C, "a refused `gh pr ready`, `gh pr edit --base`, or a chained subcommand", R),
 "asks": (C, "`asks`, a report's unread asks", None),
 "cost": (C, "the cost table, `cost --explain`", None),
 "chain-conflict": (C, "`chain <cr> after <cr>`, `conflict <cr> with <cr>`", None),
 "rounds-exception": (C, "a CR blocked `rounds:` on a red the batch caused", None),
 "driver-question": (C, "`ask ... blocked <cr> question`, `fix:`, `refused <cr>`, a typed wait, `parked`", None),
 "merge-words": (C, "a PR to name to the user, a `handed back:` line", None),
 "merge-gaps": (C, "a `ready-to-merge` ask with gaps, a local gate clause, a screenshot gap", None),
 "merge-recorded": (C, "a `forge saw merged` line, 'I merged #n'", None),
 "merge-series-stack": (C, "a series or stack batch's merge, `order mode`, a mismatched ask", None),
 "merge-stack-ready": (C, "`stack-ready-to-merge`, a refused `forge-stack rebuild`", None),
 "merge-stack-gitlab": (C, "a stack of MRs on GitLab", None),
 "stack-changes-chief": (C, "a drop from a stack, a hold, an insert into a stack ready to merge", None),
 "batch-pause": (C, "`final <STATUS.md path>`, the last CR ended", None),
 "retro-route": (C, "the retro to offer, a point's route, a list of changes of your own", None),
 "retro-route-chantier": (C, "a `chantier` point the user wants posted as an issue", None),
 "batch-close": (C, "'close the batch', the close offer", None),
 "batch-close-stopped": (C, "`close` refused for a held agent, `--stopped`", R),
 "recovery": (C, "a stale heartbeat, an app restart, a Foreman not answering", R),
 "direct-mode": (C, "`open --direct`, a switch to direct mode", None),
 "direct-mode-epoch": (C, "a claim of your number as Foreman, `--epoch`", None),
 "direct-mode-accept": (C, "a request while a direct batch runs, the pause in direct mode", None),
 "release-chief": (C, "a release CR to file or join, `order add --release`", None),
 "release-chief-approve": (C, "a `ready-to-merge` ask of a release PR, `order approve`", None),
 "release-chief-auto": (C, "'auto' during a release, `order grant`", None),
 "release-chief-after": (C, "a refused publication, a refused main-checkout step, `release published`", None),
 "seat-handover": (C, "'hand the batch to another session', `your turn, you are the Chief of Staff`", R),
 "demo": (C, "the last PR of a stack ready to merge, 'demo'", R),
 "pr-template-own": (C, "the user's own PR template", R),
}
d = json.load(open(TJ, encoding="utf-8"))
tp = d["topics"]
missing = [n for n in pj["names"] if n not in T]
extra = [n for n in T if n not in pj["names"]]
print("missing", missing, "extra", extra)
for n in pj["names"]:
    roles, trig, rb = T[n]
    rd = [f"topics/{p}.md" for p in parts[n]] if n in parts else [f"topics/{n}.md"]
    row = {"readings": rd, "roles": roles, "trigger": trig}
    if rb:
        row["review_by"] = rb
    tp[n] = row
json.dump(d, open(TJ, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
open(TJ, "a", encoding="utf-8", newline="\n").write("\n")
print(len(tp), "rows")
