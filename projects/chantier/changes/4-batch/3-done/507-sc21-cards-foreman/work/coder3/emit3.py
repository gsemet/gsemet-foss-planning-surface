import re, sys, json, subprocess, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gen3
from gen3 import CN, REF, EVD, FLOOR_L, lines_of

WT_ROOT = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"

# hand decisions for the rows the script could not place: (file, first line) -> (kind, home, check)
OV = {
    ("chief-of-staff", 39): ("e", "topic config", "help config"),
    ("chief-of-staff", 221): ("e", "topic config; the rule it applies: floor 3, 4", "help config"),
    ("chief-of-staff-steering", 46): ("e", "topic orders; the rule it applies: floor 9", "help orders"),
    ("chief-of-staff-steering", 50): ("e", "topic drop", "help drop"),
    ("chief-of-staff-merge", 206): ("e", "topic steering-reports", "help steering-reports"),
    ("chief-of-staff-batch-end", 111): ("e", "topic batch-close", "help batch-close"),
    ("chief-of-staff-direct", 67): ("e", "topic direct-mode", "help direct-mode"),
    ("chief-of-staff-direct", 186): ("e", "topic recovery", "help recovery"),
    ("chief-of-staff-grill", 43): ("e", "topic grill-backlog", "help grill-backlog"),
    ("chief-of-staff-grill", 88): ("e", "topic grill-options", "help grill-options"),
    ("chief-of-staff-grill", 198): ("e", "topic where-cr-goes", "help where-cr-goes"),
    ("chief-of-staff-grill", 475): ("e", "topic where-cr-goes", "help where-cr-goes"),
    ("chief-of-staff-release", 72): ("e", "topic release-chief-auto", "help release-chief-auto"),
    ("chief-of-staff", 15): ("b", "inferable", "none (a capable model infers it; no protecting rule)"),
    ("griller", 38): ("a", "card griller-skill.md:19", "grep -c 'tracker issue' griller-skill.md"),
    ("chief-of-staff", 25): ("e", "topic grill-specify", "help grill-specify"),
    ("chief-of-staff", 26): ("e", "topic batch-plan-mode", "help batch-plan-mode"),
    ("chief-of-staff", 38): ("e", "topic config", "help config"),
    ("chief-of-staff", 53): ("a", "floor 3, 4", "none (floor)"),
    ("chief-of-staff", 235): ("f", "duplicate: the card's pointers and `help`", "none (duplicate)"),
    ("chief-of-staff", 290): ("e", "topic demo", "help demo"),
    ("chief-of-staff", 315): ("a", "card chief-of-staff.md:24", "grep -c 'close or reopen' chief-of-staff.md"),
    ("chief-of-staff-any", 35): ("e", "topic merge-series-stack", "help merge-series-stack"),
    ("chief-of-staff-batch-start", 26): ("e", "topic trials", "help trials"),
    ("chief-of-staff-batch-start", 54): ("e", "topic batch-plan", "help batch-plan"),
    ("chief-of-staff-batch-start", 112): ("e", "topic batch-plan-mode", "help batch-plan-mode"),
    ("chief-of-staff-batch-start", 117): ("e", "topic batch-plan-mode", "help batch-plan-mode"),
    ("chief-of-staff-batch-start", 133): ("e", "topic batch-plan-mode", "help batch-plan-mode"),
    ("chief-of-staff-steering", 16): ("e", "topic direct-mode-epoch", "help direct-mode-epoch"),
    ("chief-of-staff-steering", 68): ("e", "topic orders", "help orders"),
    ("chief-of-staff-steering", 246): ("e", "topic watcher-events", "help watcher-events"),
    ("chief-of-staff-merge", 26): ("e", "topic merge-words; the rule it applies: floor 1", "help merge-words"),
    ("chief-of-staff-merge", 118): ("e", "topic merge-gaps", "help merge-gaps"),
    ("chief-of-staff-direct", 153): ("a", "card chief-of-staff.md:16", "grep -c 'close --yes' chief-of-staff.md"),
    ("chief-of-staff-direct", 198): ("e", "topic recovery", "help recovery"),
    ("chief-of-staff-direct", 207): ("e", "topic direct-mode-epoch", "help direct-mode-epoch"),
    ("chief-of-staff-grill", 20): ("e", "topic grill-backlog; the rule it applies: card chief-of-staff.md:16", "help grill-backlog"),
    ("chief-of-staff-grill", 143): ("b", "inferable", "none (a capable model infers it; no protecting rule)"),
    ("chief-of-staff-grill", 239): ("a", "floor 8", "none (floor)"),
    ("chief-of-staff-grill", 353): ("e", "topic grill-backlog", "help grill-backlog"),
    ("chief-of-staff-grill", 409): ("e", "topic ticket-summary", "help ticket-summary"),
    ("chief-of-staff-grill", 476): ("e", "topic where-cr-goes", "help where-cr-goes"),
    ("griller", 12): ("e", "topic grill-backlog", "help grill-backlog"),
}

SRC_BYTES = {}


def esc(s):
    return s.replace("|", "\\|")


def clean(t):
    t = re.sub(r"\*\*", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > 240:
        t = t[:239].rstrip() + "…"
    return esc(t)


def src(f, a, b):
    return f"{f}.md:{a}" if a == b else f"{f}.md:{a}-{b}"


def quote(home, card):
    CL = lines_of(CN / card)
    out = [home]
    for m in re.finditer(rf"card {re.escape(card)}:(\d+)(?:-(\d+))?(?:, (\d+))?", home):
        for g in m.groups():
            if g:
                q = CL[int(g) - 1].strip()
                out.append(f"`{card}:{g}` \"{q[:70]}{'…' if len(q) > 70 else ''}\"")
    for m in re.finditer(r"floor ([\d, ]+)", home):
        for k in re.findall(r"\d+", m.group(1)):
            for i, l in enumerate(FLOOR_L, 1):
                if l.startswith(k + ". "):
                    out.append(f"`floor.md:{i}` \"{l[len(k) + 2:]}\"")
    return esc("; ".join(out))


def base_line(f, n):
    key = f
    if key not in SRC_BYTES:
        r = subprocess.run(["git", "-C", WT_ROOT, "show", f"HEAD:skills/chantier/references/{f}.md"], capture_output=True)
        SRC_BYTES[key] = r.stdout.decode("utf-8").split("\n")
    return SRC_BYTES[key][n - 1]


def check_source(items):
    bad = []
    for it in items:
        ok = False
        words = [w for w in re.findall(r"[A-Za-z][A-Za-z-]{3,}", it["t"])][:40] or [it["t"].strip()[:6]]
        for n in range(it["a"], it["b"] + 1):
            line = base_line(it["f"], n).lower()
            if any(w.lower() in line for w in words):
                ok = True
        if not ok:
            bad.append(it["id"])
    return bad


def build(which):
    if which == "chief":
        res = gen3.walk(gen3.CHIEF_FILES, "chief-of-staff", "chief-of-staff.md")
        card, pre, role = "chief-of-staff.md", "C", "chief-of-staff"
        files = gen3.CHIEF_FILES
    else:
        res = gen3.walk(gen3.GRILLER_FILES, "griller", "griller-skill.md", lambda f, a: f == "griller" and 102 <= a <= 136)
        card, pre, role = "griller-skill.md", "G", "griller"
        files = gen3.GRILLER_FILES
    un = []
    for it in res:
        k = (it["f"], it["a"])
        if k in OV:
            it["kind"], it["home"], it["chk"] = OV[k]
        elif it["kind"] == "?":
            un.append(f"{k} {it['t'][:110]}")
    if un:
        print(chr(10).join(un))
        raise SystemExit("unplaced")
    for i, it in enumerate(res, 1):
        it["id"] = f"{pre}-{i:03d}"
    return res, card, pre, role, files


SHARED = {"chief-of-staff-grill", "session-start", "titles", "ticket-summary-example"}


def emit(which):
    res, card, pre, role, files = build(which)
    bad = check_source(res)
    head = "| id | role | trigger | behaviour | source | kind | new home | check |\n| --- | --- | --- | --- | --- | --- | --- | --- |"
    md = []
    title = "the Chief of Staff's rules" if which == "chief" else "the Griller's rules"
    md.append(f"# SC22 evidence: inventory of {title}\n")
    newf = "`chief-of-staff.md`, `topics/`, `topics.json`" if which == "chief" else "`griller-skill.md`, the added line of `griller.md`, `topics/`, `topics.json`"
    md.append(f"Round 3, sentence level. Ids (`{pre}-nnn`) are drafts that child 26 replaces. The new files are in `skills/chantier/cards-next/` ({newf}).\n")
    md.append("## How the sources were walked\n")
    sizes = []
    for f in files:
        n = len(open(REF / (f + ".md"), encoding="utf-8").read().split("\n")) - 1
        sizes.append(f"{f} ({n} lines)")
    if which == "chief":
        md.append("- Sources, `skills/chantier/references/` at the worktree's base: " + ", ".join(sizes) + ". Headings, blank lines and fenced command lines that no sentence carries get no row of their own.")
    else:
        md.append("- Sources, `skills/chantier/references/` at the worktree's base: " + ", ".join(sizes) + ", but the section \"Started from the board\" of `griller.md` (lines 102-136), which is child 19's. Headings and blank lines get no row.")
    md.append("- One row per rule sentence: a sentence ends at a full stop outside a code span; a sentence of more than 190 characters is cut again at a top-level semicolon. A row's `source` is the line, or the two lines, where its sentence sits at the base; no row spans a block. `behaviour` is the sentence itself, cut at 240 characters; `trigger` is the nearest heading above it. The walk was run by a script (`work/coder3/gen3.py` and `emit3.py` in the CR folder, on the part-1 splitter `work/coder/split.py`); a row's home is the best match between its sentence and the new card, the floor and the topics, and a hand table (`OV` in `emit3.py`) settles the rows the match could not place. Every row was then read through the lists at the end of this file.")
    md.append("- Kinds (study-fable section 3): a protects the user or the repository; b inferable by a capable model; c incident or retro patch; d host trial and \"unproved\" bookkeeping; e state or procedure the CLI prints just in time, or a topic carries; f duplicate. A kind a row has a home in the card, the floor or a CLI refusal, never a topic alone (F5), and no protecting row is inferable. A procedure carried by a topic only is kind e (or c), not a; where such a row applies a protecting rule, its `new home` names the topic and, after `the rule it applies:`, the card line or floor rule that holds the rule itself.")
    md.append("- New home vocabulary: `card <file>:<n>`, `floor <n>` (`floor.md`), `refusal <command, message start>`, `next:` line, `topic <name>`, `host row`, `inferable`, `duplicate`.")
    md.append("- Checks: `grep -c '<phrase>' <card>` names a phrase to find in the card; `help <topic>` means `$CHANTIER help <topic>` prints it (`load_topics` loads `topics.json`); `none (<why>)` where the floor owns the rule, or it is dropped.")
    md.append(f"- Roles: the topics of this family carry `{role}`" + (" (some also `griller`, the grill topics)" if which == "chief" else " (the Griller's own topics, and the grill topics it shares with the Chief of Staff)") + f". The role column of a row is `{role}`" + (", or `chief-of-staff, griller` for a sentence of a file both read" if which == "chief" else "") + ".")
    md.append("- Source check: for each row the lines named in `source` were read at the base (`git show HEAD:skills/chantier/references/<file>.md`) and each must hold a word of the row's behaviour: " + ("0 rows failed." if not bad else f"{len(bad)} rows failed: {', '.join(bad[:20])}.") + "\n")

    def rrole(it):
        if which == "chief" and it["f"] in SHARED:
            return "chief-of-staff, griller"
        return role

    for f in files:
        rows = [it for it in res if it["f"] == f]
        md.append(f"## {f}.md\n")
        md.append(head)
        for it in rows:
            md.append(f"| {it['id']} | {rrole(it)} | {esc(it['trig'])} | {clean(it['t'])} | {src(it['f'], it['a'], it['b'])} | {it['kind']} | {esc(it['home'])} | {esc(it['chk'])} |")
        md.append("")
    prot = [it for it in res if it["kind"] == "a"]
    md.append("## Protecting rows and their homes\n")
    md.append(f"Every kind a row ({len(prot)}), with its home quoted: the card's line, the floor's rule or the CLI refusal. None sits in a topic alone and none is inferable.\n")
    md.append("| id | source | home, quoted |\n| --- | --- | --- |")
    for it in prot:
        md.append(f"| {it['id']} | {src(it['f'], it['a'], it['b'])} | {quote(it['home'], card)} |")
    md.append("")
    ap = [it for it in res if it["kind"] == "e" and "the rule it applies" in it["home"]]
    md.append("## Protecting-looking rows a topic carries\n")
    md.append(f"{len(ap)} rows (kind e) say never, only on the user's word or a refusal, and their sentence is carried by a topic as procedure or wording; each names, after `the rule it applies:`, the card line or the floor rule that holds the rule itself, so that the rule's protection does not rest on the topic. They are listed for child 25's review; none is kind a.\n")
    md.append("| id | source | home |\n| --- | --- | --- |")
    for it in ap:
        md.append(f"| {it['id']} | {src(it['f'], it['a'], it['b'])} | {esc(it['home'])} |")
    md.append("")
    inf = [it for it in res if it["kind"] == "b"]
    md.append("## Inferable rows\n")
    md.append(f"Every kind b row ({len(inf)}). None of them is a protecting row (no row is in both lists). Each is dropped from the new card and topics, or never written there, because a capable model infers it or the CLI's line carries it.\n")
    md.append("| id | source | sentence, cut | why inferable |\n| --- | --- | --- | --- |")
    for it in inf:
        md.append(f"| {it['id']} | {src(it['f'], it['a'], it['b'])} | {clean(it['t'])[:110]} | a capable model infers it; no protecting rule |")
    md.append("")
    md.append("## Changed behaviours and rails\n")
    if which == "chief":
        md.append(CHANGED_C)
    else:
        md.append(CHANGED_G)
    kinds = {}
    for it in res:
        kinds[it["kind"]] = kinds.get(it["kind"], 0) + 1
    md.append("## Counts\n")
    md.append(f"{len(res)} rows: " + ", ".join(f"kind {k} {kinds[k]}" for k in sorted(kinds)) + f"; {len(ap)} protecting-looking rows carried by a topic.\n")
    out = EVD / f"cards-inventory-{'chief-of-staff' if which == 'chief' else 'griller'}.md"
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(md))
    print(which, len(res), kinds, "badsrc", len(bad), "ap", len(ap))
    return res


CHANGED_C = """Rows whose behaviour changes on purpose in this round (answer 8), for child 25 to reconcile. This round does not edit `evals/SCORECARD.md`.

- New, with no row at the base: "settles alone" item 3 (a refused `gh pr ready <n>` or `gh pr edit <n> --base <branch>` on a PR the record holds for a CR of this batch: run once alone, note it, say it in the report) and item 4 (a chantier subcommand the host refused in a chain: run again alone). They are in `chief-of-staff.md:8-9` and `help refused-forge-chain`; the old cards name no such route, and a refused `gh` command was a question to the user.
- Unchanged: the rebase route (item 2, `chief-of-staff.md:7`; rows of `chief-of-staff-steering.md` on the refused rebase).
- The refused force push (item 1) keeps the old judgement and the plain `git push --force-with-lease` in the route form; what changes is the wording of the ladder: the Chief of Staff settles alone and says it in the report's Notes, and asks one question only when the host refuses its own run (`chief-of-staff.md:10`).
- Narrower rails in `evals/SCORECARD.md`: J11 describes a ladder ending in "one question to the user and one push on the yes" and names no rebase, no `gh` route and no chained-subcommand route; J22 lists the steering session's exceptions as the cleanup of merged CRs' worktrees, the force push on a Driver's `push` line and the fast-forward of the main checkout, and does not list the refused rebase (`git -C <worktree> rebase`), nor `gh pr ready` and `gh pr edit --base`, which the card now has the session run. Both rails then read narrower than the card (J11 and J22).
- Open question carried: sc22-Q1, whether a non-CR branch is never force-pushed, nor the default branch, even on a yes (the card says never, a yes included, for the default branch and its force push; any other branch: once, on the yes). And sc22-Q2, whether direct mode's `brief foreman --epoch <n>` needs a CLI change (the card writes it as is; none is made).
"""

CHANGED_G = """Rows whose behaviour changes on purpose in this round: none for the Griller's contract. The one added line of `griller.md` ("How you grill is `griller-skill.md`'s `## How you grill`, read by its path; the limits of this section override it where they differ") is new text, not a changed rule: it points a Griller to the new card and ranks the board section above it. The exact line `[griller→board] grilled enough: <next batch|running batch>` stays in `griller.md`; the section "Started from the board" is child 19's and is not inventoried here. No rail of `evals/SCORECARD.md` reads narrower than the Griller's new card.
"""

if __name__ == "__main__":
    emit(sys.argv[1])
