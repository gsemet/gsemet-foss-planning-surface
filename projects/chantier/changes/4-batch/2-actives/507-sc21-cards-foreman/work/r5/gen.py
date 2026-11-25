"""Build evidence/cards-inventory-host-and-shared.md from the base sources and the hand tables.

Run: uv run --no-sync --project <worktree> python <this file>. It stops, writing nothing, when a
unit is not covered exactly once, a home does not exist, or a kind-a row has no card, floor or
refusal home.
"""

import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from hsplit import REFS, SOURCES, base_text, units  # noqa: E402

CR = HERE.parents[1]
BATCH = CR.parents[1]
CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
OUT = CR / "evidence" / "cards-inventory-host-and-shared.md"

ROLE_CARDS = {
    f"{n}.md"
    for n in (
        "chief-of-staff coder conflict-resolver cr-driver debugger demo-explorer foreman griller "
        "griller-skill inspector investigator qa-driver release-driver retro-critic spec-critic "
        "spec-writer stack-driver verifier review-step"
    ).split()
} | {f"skills/{n}-SKILL.md" for n in ("chantier", "chief-of-staff", "griller", "status")}

ROLE_OF_SOURCE = {
    "concepts.md": "all roles", "pr-template.md": "drivers, inspector, verifier",
    "release-template.md": "release-driver", "status-layout.md": "chief-of-staff, foreman, status",
    "routing.md": "all roles", "init.md": "chief-of-staff", "review-step.md": "review step",
    "sync-checkout.md": "chief-of-staff, foreman", "forges/github.md": "drivers",
    "forges/gitlab.md": "drivers", "hosts/claude-code.md": "all roles",
    "hosts/copilot.md": "all roles", "startup-core.md": "all roles", "role-core.md": "all roles",
    "host-core-claude-code.md": "all roles", "host-core-copilot.md": "all roles",
    "reload-rules.md": "chief-of-staff, foreman, griller", "floor.md": "all roles",
    "skills/chantier/SKILL.md": "router", "skills/chief-of-staff/SKILL.md": "chief-of-staff",
    "skills/griller/SKILL.md": "griller", "skills/status/SKILL.md": "status",
}

# a protecting sentence of a host JSON row: (host, capability, words of the sentence) -> home
ROW_RULES = {
    ("claude-code", "message-session", "never sent another way"): "f:3",
    ("claude-code", "message-limit", "never sent another way"): "f:3",
    ("claude-code", "name-env-holders", "Read-only: never"): "c:skills/chief-of-staff-SKILL.md:25",
    ("claude-code", "stop-session", "on the user's yes"): "c:chief-of-staff.md:14",
    ("copilot", "start-foreman", "refused start is reported"): "f:9",
    ("copilot", "model-ran-on", "stop the agent's work"): "f:3",
    ("copilot", "name-env-holders", "never a stop or a kill"): "c:skills/chief-of-staff-SKILL.md:25",
    ("copilot", "stop-driver", "no other route is used"): "f:3",
    ("copilot", "stop-session", "no other route is used"): "f:3",
    ("copilot", "run-board", "no workaround"): "f:3",
    ("copilot", "run-watcher", "no workaround"): "f:3",
    ("copilot", "workspace-trust", "refused start is reported"): "f:9",
    ("copilot", "move-session", "no other route is used"): "f:3",
    ("copilot", "message-limit", "never sent another way"): "f:3",
}

errors: list[str] = []


def lines_of(rel: str) -> list[str]:
    return (CN / rel).read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")


TOPICS = json.loads((CN / "topics.json").read_text(encoding="utf-8"))["topics"]
ROWS = {}
for host in ("claude-code", "copilot"):
    for row in json.loads((CN / f"hosts/{host}.json").read_text(encoding="utf-8"))["rows"]:
        ROWS.setdefault(row["capability"], []).append(host)


def find_line(rel: str, words: str) -> int:
    hits = [i for i, t in enumerate(lines_of(rel), 1) if words in t]
    if not hits:
        errors.append(f"no line holding {words!r} in {rel}")
        return 1
    return hits[0]


def phrase(rel: str, n: int) -> str:
    """A phrase of line n that `grep -c -F` finds in the file."""
    text = lines_of(rel)[n - 1]
    text = re.sub(r"^\s*(- |\d+\. |#+ )", "", text)
    parts = [p.strip() for p in re.split(r"[`'\"|\[\]()*\\<>$]", text)]
    pick = next((p for p in parts if len(p) >= 18), max(parts, key=len, default=""))
    if len(pick) > 44:
        pick = pick[:44].rsplit(" ", 1)[0]
    return pick


def home_of(code: str, src: str) -> tuple[str, str]:
    """(new home, check) as printed; records an error for a home that does not exist."""
    if code == "B":
        return "inferable", "none (inferable)"
    if code == "P":
        return "proof file", "none (dated proof: `docs/proofs`, child 24)"
    if code == "I":
        return "incidents file", "none (story: child 24's incidents file)"
    if code == "F":
        return "facts", "`$CHANTIER facts` or the brief's facts part"
    if code.startswith("R:"):
        return f"refusal {code[2:]}", "run the command: the CLI refuses"
    if code.startswith("N:"):
        return f"next: line {code[2:]}", "none (the CLI prints it)"
    if code.startswith("f:"):
        n = int(code[2:])
        if not 1 <= n <= 10:
            errors.append(f"{src}: floor {n}")
        return f"floor {n}", f"floor.md:{n + 4} (every brief carries it)"
    if code.startswith("t:"):
        name = code[2:]
        if name not in TOPICS:
            errors.append(f"{src}: no topic {name}")
        return f"topic {name}", f"`help {name}`"
    if code.startswith("r:"):
        cap = code[2:]
        if cap not in ROWS:
            errors.append(f"{src}: no host row {cap}")
        return f"host row {cap}", f"`$CHANTIER host {cap}`"
    if code.startswith("="):
        rel, n = src, int(code[1:])
    elif code.startswith("c:"):
        rel, _, tail = code[2:].rpartition(":")
        if tail == "{work}":
            n = find_line(rel, "scratchpad or temp folder")
        elif tail == "{noimpl}":
            n = find_line(rel, "implement")
        else:
            n = int(tail)
    else:
        errors.append(f"{src}: unknown home {code!r}")
        return code, ""
    if not (CN / rel).is_file():
        errors.append(f"{src}: no file {rel}")
        return f"card {rel}:{n}", ""
    lines = lines_of(rel)
    if not (0 < n <= len(lines)) or not lines[n - 1].strip() or lines[n - 1].startswith("#"):
        errors.append(f"{src}: {rel}:{n} is empty, a heading or past the end")
        return f"card {rel}:{n}", ""
    return f"card {rel}:{n}", f"`grep -c -F '{phrase(rel, n)}' {rel}`"


def a_home_ok(code: str, src: str) -> bool:
    if code.startswith(("f:", "R:")):
        return True
    if code.startswith("="):
        return src in ROLE_CARDS
    if code.startswith("c:"):
        return code[2:].rpartition(":")[0] in ROLE_CARDS
    return False


def cell(text: str, cut: int = 240) -> str:
    text = " ".join(text.split())
    if len(text) > cut:
        text = text[:cut].rsplit(" ", 1)[0] + " ..."
    return text.replace("|", "\\|")


rows: list[dict] = []


def add(role, trigger, behaviour, source, kind, code, src_rel):
    home, check = home_of(code, src_rel)
    if kind == "a" and not a_home_ok(code, src_rel):
        errors.append(f"kind a without card, floor or refusal home: {source} -> {code}")
    if kind not in "abcdef" or len(kind) != 1:
        errors.append(f"{source}: kind {kind!r}")
    if code.startswith("c:"):
        card = home.split()[1].rpartition(":")[0]
        if card in ROLE_CARDS and kind == "a" and not card.startswith("skills/"):
            role = card.removesuffix(".md")
    if code.startswith("r:"):
        found = {r for h in ("claude-code", "copilot") for row in host_rows(h)
                 if row["capability"] == code[2:] for r in row.get("roles", [])}
        role = ", ".join(sorted(found)) or role
    rows.append({"id": f"H-{len(rows) + 1:03d}", "role": role, "trigger": trigger,
                 "behaviour": behaviour, "source": source, "kind": kind, "home": home,
                 "check": check, "file": src_rel})


def host_rows(host: str) -> list[dict]:
    return json.loads((CN / f"hosts/{host}.json").read_text(encoding="utf-8"))["rows"]


def hand(name: str, count: int) -> dict[int, tuple[str, str]]:
    slug = name.replace("/", "-").removesuffix(".md")
    out: dict[int, tuple[str, str]] = {}
    for raw in (HERE / "h" / f"{slug}.hand").read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        span, kind, code = raw.split(" ", 2)
        lo, _, hi = span.partition("-")
        for i in range(int(lo), int(hi or lo) + 1):
            if i in out:
                errors.append(f"{name}: unit {i} twice")
            out[i] = (kind, code.strip())
    if set(out) != set(range(1, count + 1)):
        missing = sorted(set(range(1, count + 1)) - set(out))
        extra = sorted(set(out) - set(range(1, count + 1)))
        errors.append(f"{name}: units not covered {missing[:20]}, beyond the end {extra[:20]}")
    return out


counts: dict[str, int] = {}
for name in SOURCES:
    found = units(name)
    table = hand(name, len(found))
    shown = name if name.startswith("skills/") else name
    # `=N` points into the cards-next file of the same name; a SKILL.md's twin is skills/<n>-SKILL.md
    twin = name
    if name.startswith("skills/"):
        twin = f"skills/{name.split('/')[1]}-SKILL.md"
    counts[shown] = len(found)
    for i, (a, b, text, heading, _) in enumerate(found, 1):
        if i not in table:
            continue
        kind, code = table[i]
        source = f"{shown}:{a}" + (f"-{b}" if b != a else "")
        add(ROLE_OF_SOURCE[name], heading, cell(text), source, kind, code, twin)

# floor.md: one row for the preamble and one per rule
floor = base_text(REFS + "floor.md").replace("\r\n", "\n").split("\n")
counts["floor.md"] = 0
for n, text in enumerate(floor, 1):
    m = re.match(r"(\d+)\. (.*)", text)
    if not text.strip() or text.startswith("#"):
        continue
    counts["floor.md"] += 1
    num = int(m.group(1)) if m else 1
    rows.append({
        "id": f"H-{len(rows) + 1:03d}", "role": "all roles", "trigger": "The floor",
        "behaviour": cell(m.group(2) if m else text), "source": f"floor.md:{n}", "kind": "a",
        "home": f"floor {num}" if m else "floor 1-10 (the preamble, floor.md:3)",
        "check": "`git hash-object` of floor.md equals the base blob (part3-proofs.md)",
        "file": "floor.md",
    })

# hosts/*.json: one row per capability, one more per protecting sentence
for host in ("claude-code", "copilot"):
    raw = base_text(REFS + f"hosts/{host}.json").replace("\r\n", "\n")
    numbered = raw.split("\n")
    name = f"hosts/{host}.json"
    counts[name] = 0
    used = set()
    for row in json.loads(raw)["rows"]:
        cap = row["capability"]
        line = next(i for i, t in enumerate(numbered, 1) if f'"{cap}"' in t)
        plain, protect = [], []
        for sentence in row["means"]:
            key = next((k for k in ROW_RULES if k[:2] == (host, cap) and k[2] in sentence), None)
            if key:
                used.add(key)
                protect.append((sentence, ROW_RULES[key]))
            else:
                plain.append(sentence)
        roles = ", ".join(row.get("roles", []))
        if plain:
            unknown = all(re.search(r"(?i)not (recorded|known)", s) for s in plain)
            add(roles, f"row {cap} [{row.get('mark')}]", cell(" ".join(plain)), f"{name}:{line}",
                "d" if unknown else "e", f"r:{cap}", name)
            counts[name] += 1
        for sentence, code in protect:
            add(roles, f"row {cap} [{row.get('mark')}]", cell(sentence), f"{name}:{line}", "a",
                code, name)
            counts[name] += 1
    for key in ROW_RULES:
        if key[0] == host and key not in used:
            errors.append(f"row rule not found: {key}")


# ---- manifest action table -------------------------------------------------------------------
def t(*names: str) -> str:
    for n in names:
        if n not in TOPICS:
            errors.append(f"manifest table: no topic {n}")
    return ", ".join(f"topic {n}" for n in names)


def c(*cards: str) -> str:
    for n in cards:
        if not (CN / n).is_file():
            errors.append(f"manifest table: no file {n}")
    return ", ".join(f"`{n}`" for n in cards)


def b(role: str) -> str:
    return f"brief part: `brief {role}` carries the card {c(role + '.md')}"


MANIFEST = {
    "route": f"link in a card: {c('routing.md')} is named by {c('foreman.md')}; the router's choice is in {c('skills/chantier-SKILL.md')}",
    "reload": f"{t('reload')}; the role skill runs `brief` again",
    "session-start": f"{t('session-start')}; brief part: the host rows",
    "grill": f"{t('grill')}; brief part: {c('griller-skill.md')} for a Griller",
    "status": f"link in a card: {c('status-layout.md')}, linked by {c('skills/status-SKILL.md')}, named by {c('chief-of-staff.md')}",
    "spec-writer": b("spec-writer"), "spec-critic": b("spec-critic"),
    "retro-critic": b("retro-critic"), "investigator": b("investigator"), "coder": b("coder"),
    "inspector": b("inspector"), "debugger": b("debugger"), "verifier": b("verifier"),
    "conflict-resolver": b("conflict-resolver"), "demo-explorer": b("demo-explorer"),
    "deliver": f"link: {c('pr-template.md')}, linked by {c('concepts.md')} and the topics inspector-audit and verifier-description; topic cr-ship names it as the shipped one with no link (Known gap)",
    "release": f"link: {c('release-template.md')}, named with no link by {t('release-notes')} (Known gap)",
    "board": f"link: {c('concepts.md')}; {t('board', 'board-lines', 'board-restart')}",
    "sync": f"{t('sync')} (reads {c('sync-checkout.md')}), linked by the four SKILL texts",
    "cr-driver:ship": t("cr-ship", "cr-proof"),
    "cr-driver:closing": t("closing", "cr-handback"),
    "cr-driver": b("cr-driver"), "stack-driver": b("stack-driver"), "qa-driver": b("qa-driver"),
    "release-driver": b("release-driver"),
    "driver:restart": t("restart"), "driver:trouble": t("trouble"),
    "driver:conflicts": t("conflicts"), "driver:handback-other": t("handback-other"),
    "driver:pr-extras": t("pr-extras"),
    "driver:session": t("lease", "checkpoints", "steering-messages"),
    "driver:refused": t("refused-push"),
    "driver:end": "brief part: the Drivers' cards (their end and reply)",
    "driver:brief": "brief part: the facts (specification, folders) and the Drivers' cards",
    "driver:start": "brief part: the Drivers' cards and the facts",
    "driver:ship": t("cr-ship", "ci", "long-gate", "refused-push"),
    "cr-driver:retake": t("retake"), "cr-driver:matrix": t("matrix"),
    "stack-driver:restack": t("stack-restack"), "stack-driver:make": t("stack-make"),
    "stack-driver:joins": t("stack-joins"), "stack-driver:changes": t("stack-changes"),
    "release-driver:notes": t("release-notes"), "release-driver:ship": t("release-ship"),
    "release-driver:merged": t("release-merged"), "release-driver:end": t("release-end"),
    "batch:stack": t("stack"),
    "batch": f"brief part: `brief foreman` carries {c('foreman.md')} and the host rows; link: {c('concepts.md')}",
    "foreman:merge": t("merge"), "foreman:hold": t("hold"),
    "foreman:lost-driver": t("lost-driver", "escalation"),
    "foreman:conflict": t("conflict-check"), "foreman:release": t("release"),
    "foreman:refused": t("refused-push", "refused-rebase", "refused-answer"),
    "foreman:pause": t("retro", "retro-critic"),
    "foreman:reference": f"link: {c('concepts.md')} (\"Words\"); brief part: the host rows",
    "host": f"brief part: the host rows (`host <capability>`); {c('hosts/claude-code.md')} for the allow rules; the host-* topics",
    "chief-of-staff": f"brief part: `brief chief-of-staff` carries {c('chief-of-staff.md')}; {t('session-start', 'titles')}",
    "chief-of-staff:grill": t("grill", "writer"),
    "chief-of-staff:batch-start": t("batch-start"),
    "chief-of-staff:steering": t("steering", "refused-push-chief"),
    "chief-of-staff:merge": t("ready-to-merge"),
    "chief-of-staff:batch-end": t("batch-end"),
    "chief-of-staff:direct": f"{t('direct')}; the card {c('foreman.md')} by `brief foreman`",
    "chief-of-staff:release": t("release-procedure"),
    "writer": f"{t('writer')}; link: {c('concepts.md')}",
}
manifest = json.loads(base_text(REFS + "startup-manifest.json"))
actions = manifest["actions"]
if set(actions) != set(MANIFEST):
    errors.append(f"manifest table: missing {sorted(set(actions) - set(MANIFEST))}, "
                  f"not an action {sorted(set(MANIFEST) - set(actions))}")


# ---- completeness table ----------------------------------------------------------------------
FAMILIES = {
    "workers": BATCH / "3-done/505-sc19-cards-workers/evidence/cards-inventory-workers.md",
    "drivers": BATCH / "3-done/505-sc19-cards-workers/evidence/cards-inventory-drivers.md",
    "foreman": CR / "evidence/cards-inventory-foreman.md",
    "chief-and-griller (chief)": CR / "evidence/cards-inventory-chief-of-staff.md",
    "chief-and-griller (griller)": CR / "evidence/cards-inventory-griller.md",
}
claimed: dict[str, dict[str, collections.Counter]] = collections.defaultdict(
    lambda: collections.defaultdict(collections.Counter))
family_rows: dict[str, int] = {}
for family, path in FAMILIES.items():
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not re.match(r"\| [A-Z]{1,3}-?B?\d", line):
            continue
        cells = [x.strip() for x in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) < 8:
            continue
        n += 1
        src = re.search(r"([A-Za-z-]+\.md)", cells[4])
        if not src:
            continue
        got = claimed[src.group(1)][family.split(" (")[0]]
        got["rows"] += 1
        for name in re.findall(r"[a-z0-9][a-z0-9-]*", cells[6]):
            if name in TOPICS and re.search(r"topic", cells[6]):
                got["t:" + name] += 1
        for card in re.findall(r"([a-z][a-z-]*\.md)", cells[6]):
            if card in ROLE_CARDS:
                got["c:" + card] += 1
    family_rows[family] = n

MINE: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
for r in rows:
    src = r["source"].split(":")[0]
    MINE[src]["rows"] += 1
    if r["home"].startswith("topic "):
        MINE[src]["t:" + r["home"][6:]] += 1
    if r["home"].startswith("card "):
        MINE[src]["c:" + r["home"][5:].rpartition(":")[0]] += 1


def parts(counter: collections.Counter) -> tuple[list[str], list[str]]:
    cards = sorted(k[2:] for k in counter if k.startswith("c:"))
    topics = sorted(k[2:] for k in counter if k.startswith("t:"))
    return cards, topics


NOT_CARRIED = "not carried; removed by child 24"
SAME = {
    "concepts.md", "pr-template.md", "release-template.md", "status-layout.md", "routing.md",
    "init.md", "review-step.md", "sync-checkout.md", "forges/github.md", "forges/gitlab.md",
    "floor.md", "coder.md", "conflict-resolver.md", "debugger.md", "investigator.md",
    "demo-explorer.md", "spec-writer.md", "spec-critic.md", "retro-critic.md", "inspector.md",
    "verifier.md", "chief-of-staff.md", "foreman.md", "griller.md", "topics.json",
    "hosts/claude-code.json", "hosts/copilot.json",
}


def fate(name: str, counter: collections.Counter) -> str:
    cards, topics = parts(counter)
    bits = []
    if name.startswith("skills/"):
        twin = f"skills/{name.split('/')[1]}-SKILL.md"
        if not (CN / twin).is_file():
            errors.append(f"completeness: no {twin}")
        return f"carried as `cards-next/{twin}`"
    if name in SAME:
        if not (CN / name).is_file():
            errors.append(f"completeness: no cards-next/{name}")
        bits.append(f"carried as `cards-next/{name}`")
        others = [x for x in cards if x != name]
    elif name == "hosts/claude-code.md":
        bits.append("carried as `cards-next/hosts/claude-code.md` (Allow rules and Capabilities)")
        others = [x for x in cards if x != name]
    elif name == "titles.md":
        bits.append("folded into the topic file `cards-next/topics/titles.md`")
        others = cards
    elif name == "ticket-summary-example.md":
        bits.append("carried as `cards-next/ticket-summary-example.md`")
        others = cards
    else:
        bits.append(NOT_CARRIED)
        others = cards
    if others:
        bits.append("rules in the cards " + ", ".join(others))
    if topics:
        bits.append("split into topics " + ", ".join(topics))
    return "; ".join(bits)


tree = [
    p.removeprefix(REFS)
    for p in __import__("subprocess").run(
        ["git", "-C", str(CN.parents[2]), "ls-tree", "-r", "--name-only", "HEAD", REFS],
        capture_output=True, text=True, check=True).stdout.split()
]
skills = [
    p for p in __import__("subprocess").run(
        ["git", "-C", str(CN.parents[2]), "ls-tree", "-r", "--name-only", "HEAD", "skills"],
        capture_output=True, text=True, check=True).stdout.split()
    if re.fullmatch(r"skills/[^/]+/SKILL\.md", p)
]
EXTRA_NOTE = {
    "startup-manifest.json": "not carried; removed by child 24 (the manifest action table below; `roles.yaml` and `brief` replace its roles and startup lists)",
    "topics.json": "carried as `cards-next/topics.json` (rewritten: triggers and readings, no rule sentence)",
    "titles.md": None,
}
complete = []
findings = []
for name in tree + skills:
    families = dict(claimed.get(name, {}))
    mine = name in counts or name in ("topics.json", "startup-manifest.json")
    inventory = sorted(families) + (["host-and-shared"] if mine else [])
    if not inventory:
        findings.append(name)
        errors.append(f"completeness: no inventory covers {name}")
    if mine and families:
        findings.append(f"{name}: two inventories ({', '.join(inventory)})")
    merged: collections.Counter = collections.Counter()
    for v in families.values():
        merged.update(v)
    merged.update(MINE.get(name, {}))
    text = EXTRA_NOTE.get(name) or fate(name, merged)
    total = ", ".join(f"{f} {families[f]['rows']}" for f in sorted(families))
    if mine:
        total = ", ".join(filter(None, [total, f"host-and-shared {counts.get(name, 0)}"]))
    complete.append((name, ", ".join(inventory), total, text))
# SKILL.md files share one file name; MINE is keyed by the full path, so check them
for path in skills:
    if path not in counts:
        errors.append(f"completeness: {path} not walked")

if errors:
    print("\n".join(errors[:80]))
    print(f"{len(errors)} errors; nothing written")
    sys.exit(1)

# ---- document --------------------------------------------------------------------------------
HEAD = ["id", "role", "trigger", "behaviour", "source", "kind", "new home", "check"]


def table(selected):
    out = ["| " + " | ".join(HEAD) + " |", "| " + " | ".join("---" for _ in HEAD) + " |"]
    for r in selected:
        out.append("| " + " | ".join([
            r["id"], r["role"], cell(r["trigger"], 80), r["behaviour"], r["source"], r["kind"],
            r["home"].replace("|", "\\|"), r["check"].replace("|", "\\|")]) + " |")
    return out


order = list(SOURCES) + ["floor.md", "hosts/claude-code.json", "hosts/copilot.json"]
doc = [
    "# SC21 evidence: inventory of the host and shared sources",
    "",
    "Ids (`H-nnn`) are drafts that child 26 replaces. The new files are in `skills/chantier/cards-next/`. Sources are read at the worktree's base (`git show HEAD:<path>`, head bf4e4c42); homes are read in the working tree. Built by `work/r5/gen.py` from `work/r5/h/*.hand`.",
    "",
    "## How the sources were walked",
    "",
    f"- Sources ({len(order)} files with rows): every \"From today's\" file of the specification's section 1 that no family inventory covers, the five files no family claims (`startup-core.md`, `role-core.md`, `host-core-claude-code.md`, `host-core-copilot.md`, `reload-rules.md`) and the four `skills/*/SKILL.md`. `startup-manifest.json` holds no rule sentence: it has the action table below. `topics.json` holds triggers and readings only: it has a completeness row. `titles.md` and `ticket-summary-example.md` (in section 1's table) are already rows of `cards-inventory-chief-of-staff.md` and are not inventoried twice.",
    "- Markdown: one row per sentence (a full stop outside a code span; a sentence of more than 190 characters is cut again at a top-level semicolon), per table row and per fenced block; headings and blank lines give no row, and the nearest heading is the trigger. A `SKILL.md`'s frontmatter gives no row (kept unchanged). `behaviour` is the source sentence, cut at 240 characters. Script: `work/r5/hsplit.py`.",
    "- `floor.md`: one row for its preamble and one per rule. `hosts/*.json`: one row per capability (its `means`, cut), and one more row per sentence of a `means` that protects the user or the repository; the files are byte-identical copies.",
    "- Kind and home were assigned by hand for each unit, with the best-matching text of the new set beside it (`work/r5/hdump.py`, dumps in `work/r5/h/`). The generator stops when a unit is not covered exactly once, a topic, host row, file or line named as a home does not exist, a home line is empty or a heading, or a kind-a row has no role card, floor or refusal home. It does not judge that the home's words carry the rule: that was read by hand.",
    "- Kinds: a protects the user or the repository; b inferable by a capable model; c incident or retro patch; d host trial and \"unproved\" bookkeeping; e state or procedure the CLI prints, or a topic or file carries; f duplicate.",
    "- New home vocabulary: `card <file>:<line>` is a line of a file of `cards-next/` outside `topics/` (a role card, a `SKILL.md` text, `review-step.md`, or a shared file such as `concepts.md`); `floor <n>`; `refusal <command, message start>`; `topic <name>`; `host row <capability>`; `facts`; `proof file` (`docs/proofs`, child 24); `incidents file` (child 24); `inferable`. A kind-a row's home is only a role card, a `SKILL.md` text, the floor or a refusal, never a shared file or a topic.",
    "- Role column: the home card's role for a kind-a row, the row's roles for a host row, else the readers of the source file.",
    "",
    "Units per source:",
    "",
    "| source | units |",
    "| --- | --- |",
]
doc += [f"| {n} | {counts[n]} |" for n in order]
doc += [f"| total | {sum(counts[n] for n in order)} |", ""]
for n in order:
    selected = [r for r in rows if r["source"].split(":")[0] == n]
    doc += [f"## {n}", ""] + table(selected) + [""]

doc += ["## Manifest action table", "",
        "Each action of `startup-manifest.json` at the base and its new home. The manifest's other keys (`common`, `role_core`, `hosts`, `entries`, `roles`, `startup_sections`, `limit`, `paths`) are replaced by `roles.yaml`, `brief` and `help`.",
        "", "| action | today's readings | new home |", "| --- | --- | --- |"]
for name, readings in actions.items():
    today = ", ".join(x if isinstance(x, str) else "per host: " + ", ".join(x.values())
                      for x in readings)
    doc.append(f"| {name} | {today.replace('|', chr(92) + '|')} | {MANIFEST[name]} |")
doc += ["", f"{len(actions)} actions.", "", "## Completeness table", "",
        "One row per file under `skills/chantier/references/` at the base, recursive, and per `skills/*/SKILL.md`. Inventories: `workers`, `drivers` (both in CR 505's `evidence/`), `foreman`, `chief-and-griller` (two files, in this CR's `evidence/`), `host-and-shared` (this file). The cards and topics of a family-covered file are read from that inventory's `new home` column.",
        "", "| file | inventory | rows | fate |", "| --- | --- | --- | --- |"]
for name, inventory, total, text in complete:
    shown = name if name.startswith("skills/") else f"references/{name}"
    doc.append(f"| {shown} | {inventory} | {total} | {text} |")
doc += ["", f"{len(complete)} files; {sum(1 for x in complete if not x[1])} without an inventory.", "",
        "Family inventory rows read: "
        + ", ".join(f"{k} {v}" for k, v in family_rows.items()) + ".", ""]

a_rows = [r for r in rows if r["kind"] == "a"]
doc += ["## Protecting rows and their homes", "",
        f"{len(a_rows)} kind-a rows, each homed in a role card or `SKILL.md` text, the floor or a refusal. The quoted line is the home's, from the working tree.",
        "", "| id | source | new home | the home line |", "| --- | --- | --- | --- |"]
floor_next = lines_of("floor.md")
for r in a_rows:
    home = r["home"]
    quote = ""
    if home.startswith("card "):
        rel, _, n = home[5:].rpartition(":")
        quote = lines_of(rel)[int(n) - 1]
    elif re.fullmatch(r"floor \d+", home):
        quote = floor_next[int(home.split()[1]) + 3]
    elif home.startswith("floor"):
        quote = floor_next[2]
    doc.append(f"| {r['id']} | {r['source']} | {home} | {cell(quote, 200)} |")

pat = re.compile(r"(?i)\b(never|only on|only with|must not|no one|only the user|nothing else)\b")
loose = [r for r in rows if r["kind"] != "a" and pat.search(r["behaviour"])]
doc += ["", "## Protecting-looking rows not classified a", "",
        f"{len(loose)} rows of kind b to f hold \"never\", \"only on\", \"must not\" or the like; each is listed so a reader can contest its kind.",
        "", "| id | kind | new home | behaviour |", "| --- | --- | --- | --- |"]
doc += [f"| {r['id']} | {r['kind']} | {r['home']} | {cell(r['behaviour'].replace(chr(92) + '|', '|'), 150)} |"
        for r in loose]

inferable = [r for r in rows if r["home"] == "inferable" or r["kind"] == "b"]
if any(r["kind"] == "a" for r in inferable):
    print("an inferable row is kind a")
    sys.exit(1)
doc += ["", "## Inferable rows", "",
        f"{len(inferable)} rows of kind b or homed `inferable`; none is kind a.", "",
        "| id | kind | new home | source | behaviour |", "| --- | --- | --- | --- | --- |"]
doc += [f"| {r['id']} | {r['kind']} | {r['home']} | {r['source']} | {cell(r['behaviour'].replace(chr(92) + '|', '|'), 150)} |"
        for r in inferable]

kinds = collections.Counter(r["kind"] for r in rows)
homes = collections.Counter(
    r["home"].split()[0] if r["home"].split()[0] not in ("host", "proof", "incidents", "next:")
    else " ".join(r["home"].split()[:2]) if r["home"].startswith("host") else r["home"]
    for r in rows)
doc += ["", "## Counts", "", f"{len(rows)} rows.", "",
        "Kinds: " + ", ".join(f"{k} {kinds[k]}" for k in "abcdef") + ".", "",
        "Homes: " + ", ".join(f"{k} {v}" for k, v in homes.most_common()) + ".", ""]

TAIL = HERE / "inventory_tail.md"
if TAIL.exists():
    doc += [TAIL.read_text(encoding="utf-8").rstrip(), ""]

# no home folder in a published file: a quoted source sentence names one
text = re.sub(r"(?i)([A-Z]:[\\/]Users[\\/])[^\\/<>`\s|]+", r"\1<user>", "\n".join(doc))
OUT.write_text(text, encoding="utf-8", newline="\n")
print(f"{len(rows)} rows, kinds {dict(sorted(kinds.items()))}, {len(a_rows)} kind a, "
      f"{len(actions)} actions, {len(complete)} files; findings: {findings}")
print("written", OUT, OUT.stat().st_size, "bytes")
