import re, sys
from out import *

EV = "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/507-sc21-cards-foreman/evidence/cards-inventory-foreman.md"
CARD_L = CARD.split("\n")
FLOOR_L = FLOOR.split("\n")


def fname(f):
    return f + ".md"


def src(f, a, b):
    return f"{fname(f)}:{a}" if a == b else f"{fname(f)}:{a}-{b}"


def clean(t):
    t = re.sub(r"\*\*", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > 240:
        t = t[:239].rstrip() + "…"
    return esc(t)


def expand(home):
    """The home with each card line and floor rule quoted, for the end list."""
    out = [home]
    for m in re.finditer(r"card foreman\.md:(\d+)", home):
        n = int(m.group(1))
        q = CARD_L[n - 1].strip()
        out.append(f"`foreman.md:{n}` \"{q[:70]}{'…' if len(q) > 70 else ''}\"")
    seen = set()
    for m in re.finditer(r"floor ([\d, ]+)", home):
        for k in re.findall(r"\d+", m.group(1)):
            if k in seen:
                continue
            seen.add(k)
            for i, l in enumerate(FLOOR_L, 1):
                if l.startswith(k + ". "):
                    out.append(f"`floor.md:{i}` \"{l[len(k) + 2:]}\"")
    return esc("; ".join(out))


def main():
    rows = build()
    items = []  # dicts
    nb = 0
    nn = 0
    for f, a, b, t in rows:
        r = classify(f, a, b, t)
        trig, kind, home, chk, sc = r
        isb = f == "foreman" and 59 <= a <= 184
        if isb:
            nb += 1
            rid = f"FM-B{nb:03d}"
        else:
            nn += 1
            rid = f"FM-{nn:03d}"
        items.append(dict(id=rid, f=f, a=a, b=b, t=t, trig=trig, kind=kind, home=home, chk=chk, b_=isb))

    def row(it):
        return (f"| {it['id']} | foreman | {esc(it['trig'])} | {clean(it['t'])} | {src(it['f'], it['a'], it['b'])} | "
                f"{it['kind']} | {esc(it['home'])} | {esc(it['chk'])} |")

    head = "| id | role | trigger | behaviour | source | kind | new home | check |\n| --- | --- | --- | --- | --- | --- | --- | --- |"
    md = []
    md.append("# SC21 evidence: inventory of the Foreman's rules\n")
    md.append("Round 2, sentence level. Ids (`FM-nnn`, `FM-Bnnn`) are drafts that child 26 replaces. The new card and topics are in `skills/chantier/cards-next/` (`foreman.md`, `topics/`, `topics.json`).\n")
    md.append("## How the sources were walked\n")
    md.append("- Sources: `skills/chantier/references/foreman.md` (393 lines) and its eight pieces at the worktree's base: foreman-stack (197 lines), foreman-merge (139), foreman-hold (87), foreman-lost-driver (130), foreman-conflict (45), foreman-release (48), foreman-refused (163), foreman-pause (25). Headings and blank lines carry no rule and get no row.")
    md.append("- One row per rule sentence: a sentence ends at a full stop outside a code span; a sentence of more than 190 characters is cut again at a top-level semicolon. A row's `source` is the line, or the two lines, where its sentence sits; no row spans a block. `behaviour` is the sentence itself, cut at 240 characters. The walk was run by a script (`work/coder/split.py`, `gen.py`, `out.py`, `doc.py`, in the CR folder) and every row was then read through the three review lists below.")
    md.append("- The B rows (`FM-B###`) are the sentences of \"The user's boundaries\" (`foreman.md:59-184`, specification section 4); their `trigger` starts with the specification's label (B1a to B7f).")
    md.append("- Kinds (study-fable section 3): a protects the user or the repository; b inferable by a capable model; c incident or retro patch; d host trial and \"unproved\" bookkeeping; e state or procedure the CLI prints just in time, or a topic carries; f duplicate. A kind a row has a home in the card, the floor or a CLI refusal, never a topic alone (F5), and no protecting row is inferable. A procedure carried by a topic only is kind e (or c), not a.")
    md.append("- New home vocabulary: `card foreman.md:<n>`, `floor <n>` (`floor.md`), `refusal <command, message start>`, `next:` line (the line the CLI prints), `topic <name>`, `host row`, `inferable`, `duplicate`.")
    md.append("- Checks: `grep -c '<phrase>' foreman.md` names a phrase to find in the card; `help <topic>` means `$CHANTIER help <topic>` prints it (`load_topics` loads `topics.json`); `none (<why>)` where a refusal or the floor owns the rule, or it is dropped.")
    md.append("- Roles: every topic row carries `foreman` and `chief-of-staff` (the Chief of Staff steers a direct batch with this card). The role column of a row is `foreman`: the card's reader.\n")

    def section(title, sel):
        md.append(f"## {title}\n")
        md.append(head)
        for it in items:
            if sel(it):
                md.append(row(it))
        md.append("")

    section("foreman.md, outside \"The user's boundaries\"", lambda it: it["f"] == "foreman" and not it["b_"])
    section("\"The user's boundaries\" (the B rows of the specification, section 4)", lambda it: it["b_"])
    for f, ttl in [("foreman-stack", "foreman-stack.md"), ("foreman-merge", "foreman-merge.md"), ("foreman-hold", "foreman-hold.md"),
                   ("foreman-lost-driver", "foreman-lost-driver.md"), ("foreman-conflict", "foreman-conflict.md"),
                   ("foreman-release", "foreman-release.md"), ("foreman-refused", "foreman-refused.md"), ("foreman-pause", "foreman-pause.md")]:
        section(ttl, lambda it, f=f: it["f"] == f)

    prot = [it for it in items if it["kind"] == "a"]
    md.append("## Protecting rows and their homes\n")
    md.append(f"Every kind a row ({len(prot)}), with its home quoted: the card's line (file and line, then its start), the floor's rule, or the CLI refusal's message start with its source line. None sits in a topic alone and none is inferable.\n")
    md.append("| id | source | home, quoted |\n| --- | --- | --- |")
    for it in prot:
        md.append(f"| {it['id']} | {src(it['f'], it['a'], it['b'])} | {expand(it['home'])} |")
    md.append("")
    inf = [it for it in items if it["kind"] == "b"]
    md.append("## Inferable rows\n")
    md.append(f"Every kind b row ({len(inf)}). None of them is a protecting row (no row is in both lists; a protecting rule is never inferable). Each is dropped from the new card and topics, or never written there, because a capable model infers it or the CLI's line carries it.\n")
    md.append("| id | source | sentence, cut | why inferable |\n| --- | --- | --- | --- |")
    for it in inf:
        why = it["chk"].replace("none (", "").rstrip(")")
        md.append(f"| {it['id']} | {src(it['f'], it['a'], it['b'])} | {clean(it['t'])[:110]} | {esc(why)} |")
    md.append("")
    kinds = {}
    for it in items:
        kinds[it["kind"]] = kinds.get(it["kind"], 0) + 1
    md.append("## Counts\n")
    md.append(f"{len(items)} rows: " + ", ".join(f"kind {k} {kinds[k]}" for k in sorted(kinds)) + f"; {nb} B rows.\n")
    md.append(TAIL)
    open(EV, "w", encoding="utf-8", newline="\n").write("\n".join(md))
    print(len(items), kinds, nb)


TAIL = """## Check candidates for child 25

- Chat obeys only "stop" and "hold" (FM-B rows of `foreman.md:162-163`).
- A note does not wake; only `anomaly` and `blocked` do (`wakes`, card Messages).
- `judge` then send unchanged, no merge (card Own, Never 1).
- The `--no-gate` check against the rules (B1h rows).
- A release PR is not merged without the grant (B1o rows).
- A refused push of a branch not `chantier/*` is never pushed, a yes included (card Never 3, floor 2).
- A session in a worktree takes no CR (card Start).
- `next` against a refusal: a refusal is the rule (card own heartbeat bullet).

## For child 24: the stack line (no CLI change in this round)

Section 7's text for the stack line:

`shape: stack: read `$CHANTIER help stack` now and after each compaction`

Child 24 changes `src/stack_shape.py`, `shape_line()`, and converts these tests: `test_came_back.py`, `test_stack_shape.py`, `test_reload_rules.py`, `test_role_cards_split.py`, `test_startup_manifest.py`, `test_stack_chain_cards.py`, `test_rebase_rules.py`, `test_release_tag.py` and `moved_rules.tsv`.
"""

if __name__ == "__main__":
    main()
