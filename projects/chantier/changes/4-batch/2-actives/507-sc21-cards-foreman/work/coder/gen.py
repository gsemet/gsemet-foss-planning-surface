import re, sys, os
import split

CARD = open(split.CN + "foreman.md", encoding="utf-8").read()
FLOOR = open(split.CN + "floor.md", encoding="utf-8").read()


def topic_text(n):
    p = split.CN + "topics/" + n + ".md"
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None


STOP = set("""about after again against being between before cannot could every first never other
their there these those under until which while whose would yours""".split())


def words(t):
    return {w for w in re.findall(r"[a-z]{5,}", t.lower()) if w not in STOP}


def ticks(t):
    return {x.strip() for x in re.findall(r"`([^`]+)`", t) if len(x.strip()) > 2}


def score(sent, text):
    if text is None:
        return 0.0
    lo = text.lower()
    w = words(sent)
    tk = ticks(sent)
    s = 0.0
    n = 0.0
    for x in w:
        n += 1
        if x in lo:
            s += 1
    for x in tk:
        n += 2
        if x.lower() in lo:
            s += 2
    return s / n if n else 1.0


# (start, end, trigger, [candidate topics], default kind)
SEG = {
    "foreman": [
        (3, 19, "session start", ["@card"], "e"),
        (20, 30, "the batch's last CR ends", ["@card", "retro"], "e"),
        (31, 46, "the batch's pause: the retro", ["retro-lines", "retro"], "e"),
        (48, 53, "an order that adds work to a paused batch", ["orders-queue", "orders"], "e"),
        (55, 57, "a CR placed in 1-pending", ["orders-queue", "orders"], "e"),
        (61, 65, "B1a: a CR handed back ready (the ask's words)", ["@judge"], "e"),
        (65, 66, "B1b: an ask's icon", ["@inferable"], "b"),
        (66, 67, "B1c: a stack CR ready", ["stack", "stack-asks"], "e"),
        (68, 70, "B1d: a draft's text or `gaps:` in the ask", ["@judge"], "e"),
        (71, 73, "B1e: a hand-back that names an image note", ["pr-images", "@judge"], "e"),
        (73, 75, "B1f: a gap the body lacks", ["take-back", "@card"], "e"),
        (75, 75, "B1g: an order note `evidence: <path>`", ["orders"], "e"),
        (76, 84, "B1h: a hand-back `no long gate: <reason>` (`--no-gate`)", ["long-gate"], "e"),
        (84, 87, "B1i: the stack's top handed back `--no-gate`", ["local-gate", "long-gate"], "e"),
        (88, 97, "B1j: a CR that owes the local run", ["local-gate"], "e"),
        (97, 101, "B1k: `deliver by <time>` and a CR not yet passed", ["local-gate", "stack-deliver"], "e"),
        (102, 104, "B1l: the rules declare a long gate that covers the CR", ["long-gate"], "e"),
        (104, 105, "B1m: the rules say nothing about a long gate", ["long-gate"], "e"),
        (105, 120, "B1n: `long gate waived (O-<k>)`", ["long-gate-waiver", "local-gate"], "e"),
        (120, 124, "B1o: a release PR", ["merge-under-grant", "release-take"], "e"),
        (124, 127, "B1p: a fix CR merged under the grant", ["merge-under-grant", "merge-github", "main-checkout"], "e"),
        (128, 129, "B2: the batch's limits", ["@refusal"], "e"),
        (130, 130, "B2b: a spent budget, a question, an approval", ["escalation", "orders"], "e"),
        (131, 132, "B3: a refusal not understood", ["@inferable"], "b"),
        (133, 137, "B4: the rounds exception", ["orders", "escalation"], "e"),
        (137, 140, "B5a: the open orders", ["orders", "orders-queue"], "e"),
        (140, 144, "B5b: a drop order that cancels a live CR", ["orders", "drop"], "e"),
        (144, 158, "B5c: work for a CR handed back", ["take-back", "@card"], "e"),
        (158, 162, "B5d: a `blocked` CR with typed waits", ["take-back", "wakes-forge"], "e"),
        (162, 164, "B6: the Foreman's own chat", ["@card"], "e"),
        (164, 167, "B7a: what the Foreman never does", ["@card", "refused-push-steering"], "e"),
        (167, 171, "B7b: a dropped CR's PR", ["drop"], "e"),
        (171, 180, "B7c: kept worktrees", ["cleanup"], "e"),
        (180, 182, "B7d: the main checkout after a merge", ["main-checkout", "@card"], "e"),
        (182, 183, "B7e: the early conflict check", ["conflict-check"], "e"),
        (183, 185, "B7d: the fast-forward is the only move", ["@card"], "e"),
        (188, 202, "a moment named in the manifest", ["@help"], "e"),
        (206, 213, "every wake: `status`, `handoff`, `log`", ["wakes", "lost-driver", "lost-silent"], "e"),
        (214, 230, "starting a Driver: `take`, the lease, `agents set`", ["lease-steering", "lost-restart", "take-back", "@card"], "e"),
        (231, 237, "a CR on the critical path with its long gate queued", ["long-gate"], "e"),
        (238, 247, "a CR blocked twice, or a grant of more rounds", ["escalation"], "e"),
        (248, 252, "an `order qa`", ["qa-order"], "e"),
        (253, 255, "a brief to an agent", ["@card"], "e"),
        (256, 261, "a queued CR that `status` shows `waits for …`", ["orders-queue", "chain"], "e"),
        (262, 268, "a queued CR that costs less chained than rebased", ["chain"], "e"),
        (269, 272, "a stack batch", ["stack", "@card"], "e"),
        (273, 275, "a host's event about a CR's PR", ["@card"], "e"),
        (276, 279, "a `writer:` line", ["writer-off"], "e"),
        (280, 293, "the Chief of Staff must hear something", ["@judge", "stack-asks", "orders"], "e"),
        (294, 295, "a `blocked waits: <what>` hand-back", ["take-back", "refused-answer"], "e"),
        (296, 297, "a Driver's refused force push", ["refused-push"], "e"),
        (298, 309, "the heartbeat", ["wakes", "wakes-forge"], "e"),
        (310, 330, "the Foreman's watcher notifies", ["wakes-forge", "wakes"], "e"),
        (331, 333, "a `checks red` line", ["wakes-forge"], "e"),
        (334, 347, "the heartbeat's end", ["wakes", "handover"], "e"),
        (348, 354, "the session's start, before the epoch", ["@card"], "e"),
        (355, 360, "claiming the epoch, then `ready` and `ping`", ["@card"], "e"),
        (361, 363, "a hand-over of the seat", ["handover"], "e"),
        (364, 372, "a switch to direct mode", ["handover", "mode-switch"], "e"),
        (373, 380, "a steering command and `--epoch`", ["@refusal"], "e"),
        (382, 393, "every turn", ["wakes", "@card"], "e"),
    ],
    "foreman-stack": [
        (3, 7, "a stack batch's start", ["@card", "stack"], "f"),
        (9, 19, "a stack batch before its first stack", ["stack"], "e"),
        (23, 28, "a CR's readiness while a stack exists", ["stack", "stack-asks"], "e"),
        (29, 33, "`--outside-stack`", ["stack-outside", "stack"], "e"),
        (34, 39, "a ready CR behind a draft PR", ["stack-outside", "stack"], "e"),
        (40, 43, "an order note `shape: through the stack`", ["stack-outside", "stack"], "e"),
        (44, 49, "the heartbeat's `shape stack:` line", ["stack", "stack-outside"], "e"),
        (53, 60, "the first take of a stack", ["stack-grows"], "e"),
        (61, 66, "a later take of a stack", ["stack-takes", "stack-grows"], "e"),
        (67, 69, "a merge recorded while a stack driver runs", ["stack-takes", "stack-merge"], "e"),
        (70, 73, "a working CR placed on another", ["stack-takes", "stack-grows"], "e"),
        (74, 82, "the final-order take", ["stack-grows", "stack-takes"], "e"),
        (83, 84, "a parked CR in a stack", ["stack-takes", "park"], "e"),
        (85, 96, "an order note `deliver by <time>`", ["stack-deliver", "local-gate"], "e"),
        (100, 111, "starting the stack driver", ["stack-run"], "e"),
        (112, 125, "the stack driver's hand-back", ["stack-asks", "stack-run"], "e"),
        (126, 135, "a stack driver's context end, a lost end or an anomaly", ["stack-ends", "stack-asks"], "e"),
        (136, 146, "a drop in the stack", ["stack-drop"], "e"),
        (147, 151, "heavy CI on a head", ["stack-drop"], "e"),
        (155, 168, "a stack handed back: the checks, an insertion", ["stack-checks"], "e"),
        (169, 174, "the five checks of a stack ready to merge", ["stack-checks"], "e"),
        (178, 197, "after a merge in a stack", ["stack-merge"], "e"),
    ],
    "foreman-merge": [
        (5, 10, "an `order merged <dependency>`", ["merge"], "e"),
        (11, 21, "an `order merged`, parallel batch", ["merge"], "e"),
        (22, 32, "an `order merged`, series batch", ["merge"], "e"),
        (33, 33, "an `order merged`, stack batch", ["@inferable"], "f"),
        (34, 40, "a Driver's line that its CR is merged under it", ["merge", "wakes-forge"], "e"),
        (44, 49, "the main checkout after a merge", ["main-checkout"], "e"),
        (50, 53, "when the fast-forward runs", ["main-checkout"], "e"),
        (54, 57, "which checkout the fast-forward moves", ["main-checkout"], "e"),
        (58, 76, "the fast-forward's steps", ["main-checkout"], "e"),
        (77, 84, "the fast-forward's line on the CR", ["main-checkout"], "e"),
        (85, 87, "after a fast-forward", ["main-checkout"], "e"),
        (91, 94, "a merge on GitHub under the grant", ["merge-under-grant", "merge-github"], "e"),
        (95, 112, "a merge on GitHub: the stacks and the method", ["merge-github", "merge-under-grant"], "e"),
        (116, 139, "a CR taken back from `ready`", ["take-back"], "e"),
    ],
    "foreman-hold": [
        (5, 30, "a held CR", ["hold"], "e"),
        (34, 60, "a CR whose work waits on an outside step", ["park", "park-back"], "e"),
        (64, 87, "an `order mode --note <mode>`", ["mode-switch"], "e"),
    ],
    "foreman-lost-driver": [
        (5, 25, "a Driver waiting on its own work, or woken again", ["lost-driver", "lost-silent"], "e"),
        (26, 42, "a Driver suspected or proved dead", ["lost-driver", "lost-silent"], "e"),
        (43, 58, "a new epoch, a switch to Foreman mode, a restart", ["lost-restart", "lost-driver"], "e"),
        (59, 76, "a `blocked context:` hand-back", ["lost-context"], "e"),
        (77, 103, "a Driver stopped from outside", ["lost-outside", "lost-driver"], "c"),
        (104, 111, "a host failure of a Driver", ["lost-silent", "lost-restart", "lost-driver"], "e"),
        (112, 126, "a Driver that ended with no hand-back recorded", ["lost-silent", "lost-driver"], "e"),
        (127, 130, "a silent end", ["lost-silent", "lost-driver"], "e"),
    ],
    "foreman-conflict": [(5, 45, "a hand-back ready with a PR, parallel batch", ["conflict-check"], "e")],
    "foreman-release": [(5, 48, "the release CR", ["release-take", "release-tag", "release-stale"], "e")],
    "foreman-refused": [
        (5, 11, "a Driver's push or rebase the host refused", ["refused-push", "refused-push-steering"], "e"),
        (12, 19, "the route form of a steering-side push", ["refused-push-run", "refused-push-route", "refused-push-steering"], "e"),
        (20, 23, "step 1: who reads a refused push", ["refused-push", "refused-push-steering"], "e"),
        (24, 56, "step 2: the check and the judgement", ["refused-push-judgement", "refused-push-gate", "refused-push-steering"], "e"),
        (57, 63, "a push of a branch that is not `chantier/*`", ["refused-push-steering", "refused-push-judgement"], "e"),
        (64, 69, "a push the forge rejects as protected", ["refused-push-run", "refused-push-steering"], "e"),
        (70, 89, "step 3: the route rule (P10)", ["refused-push-route"], "e"),
        (90, 95, "step 4: a legitimate push, the rule present", ["refused-push-run"], "e"),
        (96, 99, "step 5: a push that is not legitimate", ["refused-push-judgement", "refused-push-run"], "e"),
        (100, 108, "step 6: the host refuses the Foreman's push", ["refused-push-run", "refused-push-route"], "e"),
        (109, 113, "step 7: a failed lease or a protected branch", ["refused-push-run", "refused-push-route"], "e"),
        (114, 126, "step 8: the answer's way back", ["refused-answer"], "e"),
        (127, 129, "step 9: record each refusal once", ["refused-push-run", "refused-push-steering"], "e"),
        (133, 139, "a Driver's rebase the host refused", ["refused-rebase", "refused-rebase-run"], "e"),
        (141, 145, "rebase step 1: the check", ["refused-rebase"], "e"),
        (146, 150, "rebase step 2: the rule first", ["refused-rebase"], "e"),
        (151, 155, "rebase step 3: run, one command", ["refused-rebase-run"], "e"),
        (156, 160, "rebase step 4: the host refuses the Foreman", ["refused-rebase-run", "refused-rebase"], "e"),
        (161, 163, "rebase step 5: the answer's way back", ["refused-answer", "refused-rebase-run"], "e"),
    ],
    "foreman-pause": [(5, 25, "the batch's pause: the retro critic", ["retro-critic", "retro-critic-write"], "e")],
}


def seg_of(f, ln):
    for a, b, tr, cand, k in SEG[f]:
        if a <= ln <= b:
            return tr, cand, k
    return None


def card_line(rx):
    for i, l in enumerate(CARD.split("\n"), 1):
        if re.search(rx, l):
            return i
    raise SystemExit("card line not found: " + rx)


# protecting homes: (file regex, line range, sentence regex, home, check)
CL = {n: card_line(r) for n, r in dict(
    start7=r"^- `git rev-parse", start8=r"^- `\$CHANTIER foreman set", start9=r"^- Read the rules",
    start10=r"^- A batch starts", own13=r"^- Starting Drivers", own14=r"^- The orders",
    own15=r"^- The asks", own16=r"^- The heartbeat", own17=r"^- The retro", n1=r"^1\. Merge but",
    n2=r"^2\. Drop or invent", n3=r"^3\. Code", n4=r"^4\. Commit, pull", n5=r"^5\. Obey",
    n6=r"^6\. `take --reclaim`", n7=r"^7\. Go on", msg=r"^Messages:", end=r"^End:").items()}


def C(k):
    return f"card foreman.md:{CL[k]}"


REF_FR = 'refusal check_slot/check_budget/check_round (rails.py:57, 222, 305)'
PROT = [
    # (file, (a,b), regex, home, check)
    ("foreman", (61, 65), r"Never merge without|the user merges it|may merge it now", f"floor 1; {C('n1')}", "grep 'Merge but' foreman.md"),
    ("foreman", (61, 65), r"never called mergeable|do not merge", f"floor 1; `judge` words `pr-in-draft`; {C('n1')}", "grep 'Merge but' foreman.md"),
    ("foreman", (71, 73), r"image|username|screenshot", f"floor 8; {C('own15')} (the ask's line is sent unchanged)", "grep 'unchanged' foreman.md"),
    ("foreman", (68, 75), r"invent no gap|drop none|keeps that text|keeps it too|gap you see", f"{C('n2')}", "grep 'invent a gap' foreman.md"),
    ("foreman", (77, 127), r"sends the CR back|send the CR back|goes back|never means|goes only with|not waive|owes no local|does not go back|is not sent back|checked first|checked against|not green|holds when|name a pipeline job|waived|no waiver|A fix CR you merge", f"{C('n2')}", "grep 'local run owed' foreman.md"),
    ("foreman", (120, 127), r"never yours to merge|merge a fix only|only under the grant|an approval never|You merge a fix|order merged", f"floor 1, 6; {C('n1')}; refusal `release go` (release.py: \"no grant for: …; the user merges it\")", "grep 'release grant' foreman.md"),
    ("foreman", (128, 130), r"refusal is a fact|limits are the CLI|past the slots", f"{REF_FR}; floor 9", "none (refusals)"),
    ("foreman", (137, 144), r"user's word|Orders are the user", f"{C('own14')}; floor 7", "grep 'the user's word' foreman.md"),
    ("foreman", (137, 144), r"`pause` waits", "refusal pause (endpause.py:77: \"every CR is merged or cancelled, not paused: …; pause once they are done\")", "none (refusal)"),
    ("foreman", (137, 144), r"you never choose|no destination|cancel", "refusal cancel (release.py:137: \"cancel <cr>: no destination recorded; …\")", "none (refusal)"),
    ("foreman", (144, 158), r"only through|never send it", f"{C('msg')}; refusal take (rails.py:250: \"`--note` saying why\")", "grep 'take-back' foreman.md"),
    ("foreman", (162, 164), r".", f"{C('n5')}", "grep 'stop' foreman.md"),
    ("foreman", (164, 167), r"Never code|never create|exceptions|exception", f"{C('n3')}; floor 2", "grep 'Code, review' foreman.md"),
    ("foreman", (167, 172), r"closed by you|is turned by you|before its", f"{C('n3')} (closing a dropped CR's PR or turning it to draft)", "grep 'dropped CR' foreman.md"),
    ("foreman", (173, 180), r"stay for|stay,|not offered|remove it once", f"{C('n6')}; floor 5", "grep 'trashed' foreman.md"),
    ("foreman", (180, 185), r"fast-forward|moves the main|no other command|merge-tree|moves no ref|second duty|third duty", f"{C('n3')}; floor 5", "grep 'fast-forward' foreman.md"),
    ("foreman", (217, 223), r"exit 3|--reclaim.{0,40}user's word|stays the user's word", f"{C('n6')}; refusal take/lease (core/leases.py, exit 3)", "grep 'reclaim' foreman.md"),
    ("foreman", (214, 217), r"refused|exit 2|agent id", "refusal take (rails.py:255: \"<cr> is working: a new Driver resumes it only with `--note`\"; rails.py:261: \"<cr> still has an agent recorded\")", "none (refusal)"),
    ("foreman", (231, 237), r"Never for another reason|alone", f"{C('own13')} (use every free slot); `gate --first` stays the CLI's", "none"),
    ("foreman", (273, 275), r".", f"{C('n5')}", "grep 'host's event' foreman.md"),
    ("foreman", (276, 279), r"never commit|never", f"{C('n4')}", "grep 'planning surface' foreman.md"),
    ("foreman", (334, 347), r"by its id", "floor 10", "none (floor)"),
    ("foreman", (348, 354), r".", f"{C('start7')}", "grep 'rev-parse' foreman.md"),
    ("foreman", (355, 357), r".", f"{C('start8')}", "grep 'foreman set' foreman.md"),
    ("foreman", (373, 380), r"exit 3|stop at once", f"{C('n7')}; refusal stale Foreman (core/batch.py:261: \"stale Foreman: Foreman n°…; stop now\")", "grep 'exit 3' foreman.md"),
    ("foreman", (373, 380), r"refuses|refuse", "refusal epoch (core/batch.py:248: \"…: the steering session's command; <n> is your number as Foreman…\")", "none (refusal)"),
    ("foreman", (382, 393), r"Stop a task", "floor 10", "none (floor)"),
    ("foreman", (253, 255), r".", f"{C('msg')}", "grep 'past fact' foreman.md"),
    # the pieces
    ("foreman-stack", (23, 28), r"refuses it|the CLI refuses", "refusal shape_refusal (rails_release.py:178-215)", "none (refusal)"),
    ("foreman-stack", (29, 33), r"user's word|open order|Never use it|only on an open|open order", "refusal check_shape (rails_release.py:178-215: \"--outside-stack needs a reason \\\"O-<k>: <why>\\\" naming an open order…\"); floor 7", "none (refusal)"),
    ("foreman-stack", (161, 168), r"edit no PR", f"{C('n3')}", "grep 'edit a PR' foreman.md"),
    ("foreman-stack", (113, 125), r"send it only when|only when it says|failed\s+check|condition of every partial", f"{C('n2')}", "grep 'local run owed' foreman.md"),
    ("foreman-merge", (91, 112), r"Anything else|no other route|no `gh pr merge`|never merged again|do not merge|guards that", f"floor 1, 9; {C('n1')}", "grep 'Merge but' foreman.md"),
    ("foreman-merge", (91, 112), r"under the grant|release go", f"floor 1, 6; {C('n1')}; refusal `release go` (release.py: \"no approval for: …\")", "grep 'release go' foreman.md"),
    ("foreman-merge", (44, 87), r"never `git|only this form|never a gate|Untracked|never list|alone|load-bearing|do nothing more|retry nothing|try no other|never do it|are never listed", f"{C('n3')}; floor 5, 9", "grep 'fast-forward' foreman.md"),
    ("foreman-merge", (44, 49), r"yours alone|never\s+do it", f"{C('n3')}", "grep 'fast-forward' foreman.md"),
    ("foreman-merge", (77, 87), r"planning|never touched", f"{C('n4')}", "grep 'planning surface' foreman.md"),
    ("foreman-merge", (116, 139), r"no new slot|keeps a new CR Driver|needs no\s+`take`", "none", "none"),
    ("foreman-hold", (5, 30), r"Its worktree and branch stay", "floor 5", "none (floor)"),
    ("foreman-lost-driver", (77, 103), r"never restarted by this", "none", "none"),
    ("foreman-conflict", (6, 45), r"moves no ref|no trial merge|no `git merge`|stops no Driver|never switches|changes no order|no rebase note|moves a ref", f"{C('n3')} (your only git: `conflicts` runs `git merge-tree` alone)", "grep 'merge-tree\\|git:' foreman.md"),
    ("foreman-release", (5, 48), r"irreversible|wait for the user's word|run nothing the Driver|never force|try no other way|change nothing", "floor 6, 9", "none (floor)"),
        ("foreman-refused", (5, 63), r"hard refusal|never a plain|nothing, ever|user's yes does not|Else push nothing|push nothing|never pushed", f"floor 2; {C('n3')}", "grep 'chantier/' foreman.md"),
    ("foreman-refused", (96, 99), r"push nothing", f"floor 2; {C('n3')}", "grep 'chantier/' foreman.md"),
    ("foreman-refused", (100, 113), r"Retry nothing|try no other|change no|never retried|nobody waits|never", "floor 9", "none (floor)"),
    ("foreman-refused", (64, 69), r"never retried|not a failed lease|no session reads", "floor 9", "none (floor)"),
    ("foreman-refused", (87, 89), r"push nothing", "floor 9", "none (floor)"),
    ("foreman-refused", (127, 129), r".", "floor 9", "none (floor)"),
    ("foreman-refused", (161, 163), r"Record each refusal once", "floor 9", "none (floor)"),
    ("foreman-conflict", (25, 26), r"host refuses", "floor 9", "none (floor)"),
    ("foreman-refused", (133, 163), r"resolves nothing|rebase nothing|no `--abort`|Never `--exec`|retry nothing|try no other|change no|hard refusal|Else rebase|leave the rebase stopped|only on such a line", "floor 2, 9", "none (floor)"),
    ("foreman-refused", (114, 126), r"never pinged|is never", "none", "none"),
    ("foreman-pause", (5, 25), r"never keep|never your|Follow the verdicts", "none", "none"),
]

# d: host-trial bookkeeping and per-host "unproved"; f: duplicates; b: inferable
RX_D_HOST = re.compile(r"^(the )?Copilot host's path is unproved|^\*\*Marks", re.I)
RX_D_UNPROVED = re.compile(r"unproved|trial: one run|\*\*unproved\*\*", re.I)
RX_F = re.compile(r"^(Read it whole|The rest of the Foreman|Who talks to whom|Its card holds|Next:|Each moment below)")
OVR = [
    ("foreman", r"^A spent budget, a round limit", "e", "topic escalation (the ask goes up once)", "help escalation"),
    ("foreman", r"^A `ping` from the Chief of Staff", "e", "card foreman.md:35 (Reply: `pong <first line of status>`)", "grep -c pong foreman.md"),
    ("foreman", r"^Then the brief and the rules, then", "e", f"{C('start9')}", "grep -c 'ready <batch>' foreman.md"),
    ("foreman-conflict", r"^Never fall back to another command", "a", "floor 3; card foreman.md:22 (your only git)", "none (floor)"),
    ("foreman", r"^At startup read the startup core|^Read the startup sections of", "e", "`brief foreman` (it prints the startup core and the pointer line); card foreman.md:3", "brief foreman builds"),
    ("foreman", r"^`handoff <cr>` and `log <cr>`", "b", "inferable", "none (the commands are named by `next:` and `help`)"),
    ("foreman", r"^add no `writes:` line|^see \[concepts\]", "e", f"card foreman.md:{CL['own13']} (\"copy whole the prompt\")", "grep -c 'copy whole' foreman.md"),
    ("foreman", r"^The host's reference says how it ends", "d", "host row (how the heartbeat ends per host)", "none (host row owns it)"),
    ("foreman", r"^Where ending it is yours", "e", "topic wakes (\"cancel the armed wake as the host row says\")", "help wakes"),
    ("foreman", r"^The merged CRs' cleanup is the CLI's", "e", "topic cleanup (\"At the last CR the CLI removes the merged CRs' worktrees\")", "help cleanup"),
    ("foreman-stack", r"^The CLI reads such a CR", "b", "inferable", "none (no protecting rule; the record is the CLI's)"),
    ("foreman-merge", r"^it rebases once, before its next push|^Conflict or not, its checks", "f", "duplicate: the Driver's card (a rebase note's work)", "none (the Driver card owns it)"),
    ("foreman-merge", r"^the CLI runs no fast-forward", "f", f"duplicate: card foreman.md:{CL['n3']}", "none (duplicate)"),
    ("foreman-merge", r"^\*\*After:\*\* no reload|^The next merge recorded tries", "b", "inferable", "none (no protecting rule; dropped as in r2.md)"),
    ("foreman-merge", r"^the resume steps below do not apply", "b", "inferable", "none (a fragment of the take-back's resume)"),
    ("foreman-hold", r"^Direct mode does this part itself", "b", "inferable", "none (dropped as in r2.md)"),
    ("foreman-hold", r"^If no slot is free, the take is refused", "e", "refusal check_slot (rails.py:57)", "none (refusal)"),
    ("foreman-lost-driver", r"^each of those keeps its own path", "b", "inferable", "none (no protecting rule)"),
    ("foreman-conflict", r"^Each PR stays as its hand-back left it", "b", "inferable", "none (no protecting rule)"),
    ("foreman-release", r"^there is no confirmation to ask", "b", "inferable", "none (the batch's go covers it; card foreman.md:3 asks the fewest questions)"),
]
INFER = [
    ("foreman", r"^A `ping` from the Chief of Staff"),
    ("foreman", r"^(An order's line or a `ping` starts a turn)"),
    ("foreman", r"^(The `take` reopens|It does not stop with the heartbeat)"),
    ("foreman-merge", r"^(Several merges handled|The order of the other steps|The CR's state is unchanged|No ask)"),
    ("foreman-merge", r"^(The `take` comes next)"),
    ("foreman-stack", r"^(Say in your next line|Nothing of the stack left open)"),
    ("foreman-hold", r"^(Then `order done`)"),
]


def build():
    rows = []
    for f in split.FILES:
        for a, b, t in split.sentences(f):
            rows.append((f, a, b, t))
    return rows


if __name__ == "__main__":
    rows = build()
    print(len(rows))
