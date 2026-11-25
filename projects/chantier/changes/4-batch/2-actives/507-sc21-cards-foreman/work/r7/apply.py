"""Round 7: apply the judged homes, labels and lists to the Foreman, Chief of Staff and Griller
inventories (CRLF and UTF-8 without a byte-order mark kept). Run once, with the worktree path."""

import re
import sys
from collections import Counter
from pathlib import Path

import cos_rules
import inv

CN = Path(sys.argv[1]) / "skills/chantier/cards-next"
DRY = "--dry" in sys.argv
STRONG = re.compile(
    r"\b(never|not without|only on the user|only with the user|user's (?:own )?(?:word|yes|answer)|"
    r"only after the user|must not|refus\w*|no guess|without the user)\b",
    re.I,
)
KEYS = ("id", "role", "trigger", "behaviour", "source", "kind", "home", "check")


def load(name):
    path = inv.EV / f"cards-inventory-{name}.md"
    raw = path.read_bytes().decode("utf-8")
    assert not raw.startswith("﻿")
    nl = "\r\n" if "\r\n" in raw else "\n"
    return path, raw.split(nl), nl


def save(path, lines, nl):
    if not DRY:
        path.write_bytes(nl.join(lines).encode("utf-8"))


def join(cells):
    assert all(len(inv.cells(f"| {x} |")) == 1 for x in cells), cells
    return "| " + " | ".join(cells) + " |"


def parse(lines, prefix):
    """id -> (index, cells) of the rule rows."""
    out = {}
    for i, line in enumerate(lines):
        if line.startswith(f"| {prefix}"):
            c = inv.cells(line)
            if len(c) == 8:
                assert join(c) == line, line
                assert c[0] not in out, c[0]
                out[c[0]] = (i, c)
    return out


def card_line(rel, n):
    return (CN / rel).read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")[n - 1]


def quoted(home):
    """The home, then each card line and floor rule it names, quoted."""
    refs = []
    for m in re.finditer(r"([\w-]+(?:/[\w-]+)?\.md):(\d+(?:, \d+)*)", home):
        refs += [(m[1], int(n)) for n in m[2].split(", ")]
    for m in re.finditer(r"\bfloor (\d+(?:, \d+)*)", home):
        refs += [("floor.md", int(n) + 4) for n in m[1].split(", ")]
    out = [home]
    for rel, n in dict.fromkeys(refs):
        line = card_line(rel, n).strip()
        assert line, (rel, n, home)
        if rel != "floor.md" and len(line) > 70:
            line = line[:70].rstrip() + "…"
        line = line.replace("|", "\\|")
        out.append(f'`{rel}:{n}` "{line}"')
    return "; ".join(out)


def protecting(lines, rows_in_order):
    """Rewrite the table of "Protecting rows and their homes" from the rows."""
    s = lines.index("## Protecting rows and their homes")
    head = next(i for i in range(s, len(lines)) if lines[i].startswith("| id |"))
    end = head + 2
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    a = [c for c in rows_in_order if c[5] == "a"]
    lines[head + 2 : end] = [join([c[0], c[4], quoted(c[6])]) for c in a]
    intro = next(i for i in range(s, head) if lines[i].startswith("Every kind a row ("))
    lines[intro] = re.sub(r"\(\d+\)", f"({len(a)})", lines[intro], count=1)
    return len(a)


def base_home(home):
    return re.split(r"; (?:the rule it applies:|no rule:|gap:)", home)[0]


def listing(name, lines, rows, rules):
    """Set each listed row's home, and return the section's lines."""
    order = sorted(rules, key=lambda k: rows[k][0])
    table = []
    for key in order:
        i, c = rows[key]
        assert c[5] == "e" and "topic " in c[6], (key, c[5], c[6])
        c[6] = f"{base_home(c[6])}; {rules[key]}"
        lines[i] = join(c)
        table.append(join([key, c[4], c[6]]))
    kinds = Counter(
        "rule" if r.startswith("the rule") else "gap" if r.startswith("gap") else "none"
        for r in rules.values()
    )
    gaps = [k for k in order if rules[k].startswith("gap")]
    intro = (
        f"{len(order)} rows (kind e) say never, only on the user's word or a refusal, or were "
        "listed as such by an earlier round, and their sentence is carried by a topic as procedure "
        f"or wording. {kinds['rule']} name, after `the rule it applies:`, the card line, floor rule "
        "or CLI refusal that holds the rule itself, so that its protection does not rest on the "
        f"topic; {kinds['none']} hold no rule of their own and say `no rule:` and why; "
        f"{kinds['gap']} are held by no card, floor or refusal (`gap:`"
        + (f": {', '.join(gaps)}" if gaps else "")
        + "). They are listed for child 25's review; none is kind a."
    )
    if not order:
        intro = "0 rows."
    section = ["## Protecting-looking rows a topic carries", "", intro, ""]
    section += ["| id | source | home |", "| --- | --- | --- |", *table, ""]
    return section, len(order), kinds


def replace_section(lines, section):
    s = lines.index("## Protecting-looking rows a topic carries")
    e = next(i for i in range(s + 1, len(lines)) if lines[i].startswith("## "))
    lines[s:e] = section


def sub_line(lines, pattern, repl):
    hits = [i for i, x in enumerate(lines) if re.search(pattern, x)]
    assert len(hits) == 1, (pattern, hits)
    lines[hits[0]] = re.sub(pattern, repl, lines[hits[0]])


# ---------------------------------------------------------------- Foreman
LABELS = {
    "B1a": "a CR handed back ready (the ask's words)",
    "B1b": "an ask's icon",
    "B1c": "a stack CR's readiness",
    "B1d": "a draft's text or `gaps:` in the ask",
    "B1e": "a hand-back that names an image note",
    "B1f": "a gap the body lacks",
    "B1g": "an order note `evidence: <path>`",
    "B1h": "a hand-back `no long gate: <reason>` (`--no-gate`)",
    "B1i": "the stack's top handed back `--no-gate`",
    "B1j": "a CR that owes the local run",
    "B1k": "`deliver by <time>` and a CR not yet passed",
    "B1l": "the rules declare a long gate that covers the CR",
    "B1m": "the rules say nothing about a long gate",
    "B1n": "`long gate waived (O-<k>)`",
    "B1o": "a release PR",
    "B1p": "a fix PR",
    "B2": "the batch's limits",
    "B2b": "a spent budget, a limit, a question, an approval, a failure",
    "B3": "a refusal not understood",
    "B4": "the rounds exception",
    "B5a": "the open orders",
    "B5b": "a drop order that cancels a live CR",
    "B5c": "work for a CR handed back",
    "B5d": "a `blocked` CR with typed waits",
    "B6": "the Foreman's own chat",
    "B7a": "code, review, commit, rebase, push, PR, worktree",
    "B7b": "a dropped CR's PR",
    "B7c": "kept worktrees",
    "B7d": "the main checkout after a merge",
    "B7e": "the early conflict check",
    "B7f": "a Driver's refused force push or rebase",
}
BY_LABEL = {
    "B1a": "001 003", "B1b": "002", "B1c": "063", "B1d": "004 005", "B1e": "006", "B1f": "007",
    "B1g": "008", "B1h": "009 010 013", "B1i": "011 012 014", "B1j": "015 016 017 019 022",
    "B1k": "020 021", "B1l": "023", "B1m": "024",
    "B1n": "025 026 027 028 029 030 031 032", "B1o": "033 034", "B1p": "018 035",
    "B2": "036 037", "B2b": "038", "B3": "039", "B4": "040 041 042", "B5a": "043 044",
    "B5b": "045", "B5c": "046 047 048 049 050 051", "B5d": "052", "B6": "053 054",
    "B7a": "055", "B7b": "056 065", "B7c": "057 058 059", "B7d": "060 062", "B7e": "061",
    "B7f": "064",
}


def ids(text):
    return [f"FM-{x}" for x in text.split()]


EDITS: dict[str, dict[str, str]] = {}


def edit(which, **kw):
    for k in ids(which):
        EDITS.setdefault(k, {}).update(kw)


def grep(phrase, card="foreman.md"):
    return f"grep -c '{phrase}' {card}"


C21 = "card foreman.md:21"
edit("B001", home="floor 1; card foreman.md:15, 20")
edit("B002", behaviour="An ask's icon, when it carries one, is the CR's state at the ask, never "
     "the state it will reach;")
edit("B003", kind="a", home="floor 1; card foreman.md:20", check=grep("Merge but"))
edit("B004 B005", home="card foreman.md:15, 21; `judge` copies them (status/judge_words.py:99)",
     check=grep("unchanged"))
edit("B006", home="floor 8; card foreman.md:15 (an image note goes in it; `judge` does not "
     "carry it: Known gap)", check=grep("image note"))
edit("B008", home="topic orders", check="help orders")
edit("B009", kind="a", home=f"{C21}; topic long-gate", check=grep("does not hold"))
edit("B010 B011 B014 B015 B016 B023 B024 B025 B026 B027 B028 B029 B031", home=C21,
     check=grep("local run owed"))
edit("B018", home="card foreman.md:20, 21; refusal check_granted_fix (rails_release.py:108, a "
     "fix without the grant is not started)")
edit("B019 B030", home="card foreman.md:15, 21; `judge --local-gate` adds the clause "
     "(status/judge_words.py:33)", check=grep("local run owed"))
edit("B020", kind="e", home="topic local-gate; card foreman.md:21 points to it",
     check="help local-gate")
RELEASE = ("floor 1, 6; card foreman.md:20; refusal `release go` (commands/release.py:81 "
           "\"no grant for: …; the user merges it\", :84 \"no approval for: …\")")
edit("B033 B034", home=RELEASE)
edit("B035", home=RELEASE + "; refusal check_granted_fix (rails_release.py:108)")
edit("B037", kind="a", home="refusal check_slot (rails.py:57, the batch's own slots); floor 9",
     check="none (refusal)")
edit("B044", home="refusal pause (commands/closing.py:95: \"cannot pause <batch>: live …, "
     "orders pending …\")")
edit("B045", home="refusal cancel (commands/release.py:137: \"cancel <cr>: no destination "
     "recorded; …\")")
edit("B046", home="card foreman.md:29; refusal take (rails.py:249: \"<cr> is <status>: a "
     "Driver takes it back only with `--note` saying why\")")
edit("B053 B054", home="card foreman.md:24", check=grep("Obey your chat"))
edit("B055", behaviour="Never code, review, commit, rebase, push or edit a PR, never create a "
     "worktree.", source="foreman.md:164", home="card foreman.md:22",
     check=grep("Code, review, commit"))
edit("B056", home="card foreman.md:22 (closing or drafting a dropped CR's PR)",
     check=grep("dropped CR"))
edit("B058", home="card foreman.md:22; floor 5", check=grep("kept merged"))
edit("B059", home="card foreman.md:25; floor 5")
edit("B060 B062", home="card foreman.md:22; floor 5")
edit("B061", home="card foreman.md:22; floor 5; `chantier conflicts` runs the check "
     "(commands/conflicts.py)", check=grep("Your only git"))

LEASE = "card foreman.md:25; refusal check_free (core/leases.py:255, exit 3)"
edit("053 058", home=LEASE)
edit("054", home="refusal check_free (core/leases.py:255); topic lease", check="help lease")
edit("071", home="card foreman.md:13", check=grep("not on a Driver"))
edit("095", home="card foreman.md:24; topic host-auto-fix",
     check=grep("event about a PR is no order"))
edit("131 160", home="card foreman.md:16", check=grep("stray background"))
edit("138", home="card foreman.md:7 (the user-words worktree override dropped per sc21-Q1, "
     "default, to confirm by the owner)")
edit("153", home="card foreman.md:26; refusal stale Foreman (core/batch.py:264: \"stale "
     "Foreman: Foreman n°…\")")
SHAPE = "refusal check_shape/shape_refusal (rails_release.py:178, 192)"
edit("172", home=SHAPE)
edit("174 176 177", home=SHAPE + "; floor 7")
edit("286 308", home="card foreman.md:22; floor 3, 5, 9")
edit("287", home="card foreman.md:22; chief-of-staff.md:22; cr-driver.md:14; "
     "stack-driver.md:14; release-driver.md:13; conflict-resolver.md:12")
edit("302", home="card foreman.md:22; floor 5")
edit("317", home="floor 1, 6; card foreman.md:20; refusal `release go` "
     "(commands/release.py:84: \"no approval for: …\")")
edit("322 328 330", home="floor 1; card foreman.md:20")
edit("329", home="floor 1, 3, 9; card foreman.md:20")
edit("485", home="card foreman.md:14, 22; `chantier conflicts` (commands/conflicts.py: records "
     "no ask, switches no mode, starts no rebase)")
edit("546", home="card foreman.md:22", check=grep("branch protection unread"))
edit("558", home="card foreman.md:22; floor 2")
edit("566", home="card foreman.md:22; floor 9",
     check=grep("no failed or protected push retried"))
edit("568", home="card chief-of-staff.md:10",
     check=grep("told at once", "chief-of-staff.md"))
edit("582 584", home="card foreman.md:22; floor 2", check=grep("chantier/*"))
edit("583 589", home="card foreman.md:22", check=grep("a conflict stays stopped"))
edit("585", home="card foreman.md:22", check=grep("checked"))
edit("590", home="card foreman.md:22", check=grep("--exec"))
edit("586", home="floor 9; card foreman.md:22 (checked; steps in topic refused-rebase)")
edit("593", home="floor 3, 9")

NEW = {
    "FM-002": [
        ("FM-B063", "B1c",
         "(except a CR of a stack on the forge: its readiness reaches the user through the "
         "stack, [foreman-stack](foreman-stack.md));", "foreman.md:67",
         SHAPE + "; next: `judge` prints `no ask:` (commands/judge.py:58); card foreman.md:15; "
         "topic stack", "grep -c -F 'no ask:' foreman.md"),
    ],
    "FM-055": [
        ("FM-B064", "B7f",
         "Two named exceptions (and a third, the push of a Driver's refused force push and the "
         "rebase of a Driver's refused rebase, by [A Driver's refused force push](foreman-"
         "refused.md#a-drivers-refused-force-push) and [A Driver's refused rebase](…",
         "foreman.md:164-167", "card foreman.md:22; topic refused-push; topic refused-rebase",
         grep("refused push or rebase")),
        ("FM-B065", "B7b",
         "a drop order whose line ends `close its PR <link>` (a trash drop outside a stack; "
         "after `cancel` for a live CR) is closed by you (`gh pr close <n>`, `glab mr close "
         "<n>`, no `--delete-branch`, no comment) before its `order done`;",
         "foreman.md:167-169", "card foreman.md:22; topic drop", grep("branch kept")),
    ],
}
AFTER = {"FM-B002": NEW["FM-002"], "FM-B055": NEW["FM-055"]}


def foreman():
    path, lines, nl = load("foreman")
    rows = parse(lines, "FM-")
    assert "FM-B063" not in rows, "already applied"
    labels = {f"FM-B{n}": lab for lab, text in BY_LABEL.items() for n in text.split()}
    assert set(labels) == {k for k in rows if k.startswith("FM-B")} | {
        "FM-B063", "FM-B064", "FM-B065"
    }
    edits = {k.replace("FM-0", "FM-0"): v for k, v in EDITS.items()}
    unknown = set(edits) - set(rows)
    assert not unknown, unknown
    for key, (i, c) in rows.items():
        new = dict(zip(KEYS, c))
        if key in labels:
            new["trigger"] = f"{labels[key]}: {LABELS[labels[key]]}"
        new.update(edits.get(key, {}))
        c[:] = [new[k] for k in KEYS]
        if key == "FM-152":
            assert "core/batch.py:248" in c[6]
            c[6] = c[6].replace("core/batch.py:248", "core/batch.py:249")
        lines[i] = join(c)
    for after in sorted(AFTER, key=lambda k: rows[k][0], reverse=True):
        add = [
            join([key, "foreman", f"{lab}: {LABELS[lab]}", behaviour, source, "a", home, check])
            for key, lab, behaviour, source, home, check in AFTER[after]
        ]
        at = rows[after][0] + 1
        lines[at:at] = add
    rows = parse(lines, "FM-")
    walked = next(i for i, x in enumerate(lines) if x.startswith("- The B rows"))
    lines.insert(
        walked + 1,
        "- Round 7: FM-B003, FM-B009 and FM-B037 are now kind a (their label protects and the "
        "sentence carries it); FM-B020 is now kind e (B1k does not protect). FM-B063 to FM-B065 "
        "are sentences the earlier rounds left inside FM-B002 and FM-B055. The label to final "
        "home table is `boundaries-split.md`.",
    )
    rows = parse(lines, "FM-")
    cand = {
        k for k, (_, c) in rows.items()
        if c[5] == "e" and "topic " in c[6] and STRONG.search(c[3])
    }
    assert cand == set(cos_rules.FM), (cand - set(cos_rules.FM), set(cos_rules.FM) - cand)
    section, n, kinds = listing("foreman", lines, rows, cos_rules.FM)
    at = lines.index("## Inferable rows")
    lines[at:at] = section
    rows = parse(lines, "FM-")
    ordered = [c for _, c in sorted(rows.values())]
    na = protecting(lines, ordered)
    count = Counter(c[5] for c in ordered)
    nb = sum(c[0].startswith("FM-B") for c in ordered)
    total = ", ".join(f"kind {k} {count[k]}" for k in sorted(count))
    sub_line(
        lines, r"^\d+ rows: kind a .*B rows\.$",
        f"{len(ordered)} rows: {total}; {nb} B rows; {n} protecting-looking rows carried by "
        "a topic.",
    )
    save(path, lines, nl)
    print("foreman", len(ordered), dict(count), "B", nb, "a", na, "list", n, dict(kinds))


# ---------------------------------------------------------------- Chief of Staff
COS_EDITS = {
    "C-051": ("card chief-of-staff.md:33; floor 9",
              grep("Meet a refusal", "chief-of-staff.md")),
    "C-056": ("floor 7; card chief-of-staff.md:3",
              grep("start one Foreman per batch", "chief-of-staff.md")),
    "C-058": ("floor 1; card foreman.md:20", grep("Merge but")),
    "C-201": ("card chief-of-staff.md:31; floor 1, 7", None),
    "C-211": ("card chief-of-staff.md:29", grep("delivery time", "chief-of-staff.md")),
    "C-1161": ("floor 8; card chief-of-staff.md:27; card griller-skill.md:24; topic "
               "grill-backlog-p2", grep("only in chat", "chief-of-staff.md")),
}


def chief():
    path, lines, nl = load("chief-of-staff")
    rows = parse(lines, "C-")
    for key, (home, check) in COS_EDITS.items():
        i, c = rows[key]
        assert c[5] == "a", key
        c[6] = home
        if check:
            c[7] = check
        lines[i] = join(c)
    for key, (i, c) in rows.items():
        if "Stopping a process you" in c[7]:
            c[7] = c[7].replace("Stopping a process you", "Stopping a Foreman or a process")
            lines[i] = join(c)
    cand = {
        k for k, (_, c) in rows.items()
        if c[5] == "e" and "topic " in c[6] and STRONG.search(c[3])
    }
    assert cand <= set(cos_rules.COS), cand - set(cos_rules.COS)
    section, n, kinds = listing("chief-of-staff", lines, rows, cos_rules.COS)
    replace_section(lines, section)
    rows = parse(lines, "C-")
    na = protecting(lines, [c for _, c in sorted(rows.values())])
    sub_line(
        lines, r"\d+ protecting-looking rows carried by a topic\.",
        f"{n} protecting-looking rows carried by a topic.",
    )
    save(path, lines, nl)
    print("chief-of-staff", len(rows), "a", na, "list", n, dict(kinds))


# ---------------------------------------------------------------- Griller
GRILLER = {
    "G-006": "the rule it applies: card griller-skill.md:5; refusal file "
             "(lifecycle/backlog.py:70 \"the request has no short title…\")",
    "G-017": "the rule it applies: card griller-skill.md:5",
    "G-044": "the rule it applies: card griller-skill.md:25",
}


def griller():
    path, lines, nl = load("griller")
    rows = parse(lines, "G-")
    cand = {
        k for k, (_, c) in rows.items()
        if c[5] == "e" and "topic " in c[6] and STRONG.search(c[3])
    }
    assert cand <= set(GRILLER), cand - set(GRILLER)
    section, n, kinds = listing("griller", lines, rows, GRILLER)
    replace_section(lines, section)
    rows = parse(lines, "G-")
    na = protecting(lines, [c for _, c in sorted(rows.values())])
    sub_line(
        lines, r"\d+ protecting-looking rows carried by a topic\.",
        f"{n} protecting-looking rows carried by a topic.",
    )
    save(path, lines, nl)
    print("griller", len(rows), "a", na, "list", n, dict(kinds))


foreman()
chief()
griller()
