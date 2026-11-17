"""Emit the Markdown tables of the cost report from cost2.json, pertask data and the transcripts.

Usage: python3 -I cost_tables.py <scratchpad> <session-base> > tables.md
Run cost2.py first (it writes <scratchpad>/cost2.json).
"""
import json, sys, re, glob, collections, statistics as st

S, base = sys.argv[1], sys.argv[2]
d = json.load(open(f"{S}/cost2.json"))
PLAN = "/Users/az02065/Projects/Nestor/agentic-coding-white-paper/.agents/changes/requests/deep-UX-analysis/fix-plan"
P = {"opus": (4.0, 8.0, 0.20, 20.0), "sonnet": (2.0, 4.0, 0.10, 10.0)}


def money(x):
    return f"${x:,.2f}"


def mtok(x):
    return f"{x / 1e6:,.1f} M"


# 1. By model
print("### Tokens and cost by model\n")
print("| Model | Requests | Input | Cache write | Cache read | Output (recorded) | Output (estimated) | Cost |")
print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
tot = collections.Counter()
for k in ("opus", "sonnet", "haiku"):
    c = d["by_model"].get(k)
    if not c:
        continue
    cost = c["usd_in"] + c["usd_out_est"]
    for f in ("requests", "in", "cw", "cr", "out_recorded", "out_est"):
        tot[f] += c[f]
    tot["cost"] += cost
    tot["cost5"] += c["usd_in_5m"] + c["usd_out_est"]
    print(f"| {k.capitalize()} 5.5 | {c['requests']:,} | {c['in']:,} | {mtok(c['cw'])} | {mtok(c['cr'])} | "
          f"{c['out_recorded']:,} | {c['out_est']:,} | {money(cost)} |")
print(f"| **Total** | {tot['requests']:,} | {tot['in']:,} | {mtok(tot['cw'])} | {mtok(tot['cr'])} | "
      f"{tot['out_recorded']:,} | {tot['out_est']:,} | **{money(tot['cost'])}** |")
print(f"\nWith 5-minute cache writes instead of 1-hour ones, the total would be {money(tot['cost5'])}.\n")

# 2. By source and role
print("### Who spent it\n")
print("| Where | Model | Requests | Cost | Share |")
print("| --- | --- | ---: | ---: | ---: |")
rows = []
for k, c in d["by_source"].items():
    src, fam = k.split("|")
    if src == "main":
        rows.append(("Orchestrator (main session)", fam, c))
for k, c in d["by_role"].items():
    role, fam = k.split("|")
    rows.append((f"Subagents: {role}", fam, c))
for name, fam, c in sorted(rows, key=lambda r: -(r[2]["usd_in"] + r[2]["usd_out_est"])):
    cost = c["usd_in"] + c["usd_out_est"]
    print(f"| {name} | {fam.capitalize()} | {c['requests']:,} | {money(cost)} | {100 * cost / tot['cost']:.0f} % |")
print()

# 3. Main session by phase
seen = {}
for l in open(base + ".jsonl", errors="replace"):
    try:
        j = json.loads(l)
    except Exception:
        continue
    if j.get("type") != "assistant":
        continue
    m = j["message"]
    u = m.get("usage")
    if not u or "opus" not in m.get("model", ""):
        continue
    seen[m["id"]] = (j["timestamp"], u)
phases = [
    ("QA campaign (parts 1 and 2) and the QA skill", "2026-10-08", "2026-10-09T07:39"),
    ("Fix plan writing", "2026-10-09T07:39", "2026-10-09T13:00"),
    ("T00–T06 (Haiku implementers)", "2026-10-09T13:00", "2026-10-10T04:30"),
    ("T07–T39 (Sonnet implementers)", "2026-10-10T04:30", "2026-10-13T07:30"),
    ("T40 final verification", "2026-10-13T07:30", "2026-10-13T08:25"),
    ("T41–T43, T30, T33, T34, final replay, wrap-up", "2026-10-13T08:25", "2027"),
]
print("### Orchestrator (main session, Opus) by phase\n")
print("| Phase | Requests | Cost |")
print("| --- | ---: | ---: |")
for name, a, b in phases:
    n = 0
    c = 0.0
    for ts, u in seen.values():
        if a <= ts < b:
            n += 1
            c += (u.get("input_tokens", 0) * 4 + u.get("cache_creation_input_tokens", 0) * 8
                  + u.get("cache_read_input_tokens", 0) * 0.2 + u.get("output_tokens", 0) * 20) / 1e6
    print(f"| {name} | {n:,} | {money(c)} |")
print()

# 4. Haiku vs Sonnet per task
tasks = collections.defaultdict(lambda: {"impl": 0.0, "rev": 0.0, "rounds": set(), "fam": None,
                                         "first": None, "last": None})
for a in d["agents"]:
    t = a["task"]
    if not t:
        continue
    x = tasks[t]
    usd = a["usd_in"] + a["usd_out_est"]
    if a["role"] == "implementer":
        x["impl"] += usd
        x["fam"] = a["family"]
        m = re.search(r"round (\d)", a["description"] or "")
        x["rounds"].add(m.group(1) if m else "1")
    elif a["role"] == "reviewer":
        x["rev"] += usd
    for k, f in (("first", min), ("last", max)):
        if a[k]:
            x[k] = f(x[k] or a[k], a[k])


def main_cost(a, b):
    return sum((u.get("input_tokens", 0) * 4 + u.get("cache_creation_input_tokens", 0) * 8
                + u.get("cache_read_input_tokens", 0) * 0.2 + u.get("output_tokens", 0) * 20) / 1e6
               for ts, u in seen.values() if a <= ts <= b)


def sev(t):
    c = collections.Counter()
    for p in glob.glob(f"{PLAN}/reviews/{t}-review-r*.md"):
        s = open(p).read()
        for k in ("BLOCKER", "MAJOR"):
            c[k] += len(re.findall(r"\*\*\[%s" % k, s)) + len(re.findall(r"^\d+\. \[%s" % k, s, re.M))
    return c


state = {}
rounds_state = {}
for l in open(f"{PLAN}/STATE.md"):
    cells = [c.strip() for c in l.split("|")]
    if len(cells) > 9 and cells[1].startswith("[T"):
        state[cells[1][1:4]] = cells[4]
        rounds_state[cells[1][1:4]] = int(cells[5]) if cells[5].isdigit() else None

groups = {"haiku": [], "sonnet": []}
for t, x in sorted(tasks.items()):
    if not x["fam"] or state.get(t) != "done":
        continue
    s = sev(t)
    groups[x["fam"]].append({
        "task": t, "rounds": rounds_state.get(t) or len(x["rounds"]), "impl": x["impl"], "rev": x["rev"],
        "main": main_cost(x["first"], x["last"]), "bm": s["BLOCKER"] + s["MAJOR"],
    })
print("### Haiku and Sonnet implementers, per task\n")
print("| | Haiku (T00–T06) | Sonnet (T07–T43) |")
print("| --- | ---: | ---: |")
H, So = groups["haiku"], groups["sonnet"]


def avg(R, k):
    return sum(r[k] for r in R) / len(R)


def med(R, f):
    return st.median([f(r) for r in R])


lines = [
    ("Tasks done", f"{len(H)}", f"{len(So)}"),
    ("Passed review in round 1", f"{sum(r['rounds'] == 1 for r in H)} of {len(H)}",
     f"{sum(r['rounds'] == 1 for r in So)} of {len(So)}"),
    ("Implementation rounds per task", f"{avg(H, 'rounds'):.2f}", f"{avg(So, 'rounds'):.2f}"),
    ("Blocker + major review findings per task", f"{avg(H, 'bm'):.1f}", f"{avg(So, 'bm'):.1f}"),
    ("Implementer cost per task", money(avg(H, "impl")), money(avg(So, "impl"))),
    ("Reviewer (Opus) cost per task", money(avg(H, "rev")), money(avg(So, "rev"))),
    ("Orchestrator cost per task (time window)", money(avg(H, "main")), money(avg(So, "main"))),
    ("**Total per task, mean**", f"**{money(avg(H, 'impl') + avg(H, 'rev') + avg(H, 'main'))}**",
     f"**{money(avg(So, 'impl') + avg(So, 'rev') + avg(So, 'main'))}**"),
    ("Total per task, median", money(med(H, lambda r: r['impl'] + r['rev'] + r['main'])),
     money(med(So, lambda r: r['impl'] + r['rev'] + r['main']))),
]
for a, b, c in lines:
    print(f"| {a} | {b} | {c} |")
print()

impl = {f: [a for a in d["agents"] if a["role"] == "implementer" and a["family"] == f] for f in ("haiku", "sonnet")}
for f, A in impl.items():
    n = len(A)
    print(f"<!-- {f}: agents={n} req/agent={sum(a['requests'] for a in A) / n:.0f} "
          f"cr/agent={sum(a['cr'] for a in A) / n / 1e3:.0f}k $/agent={sum(a['usd_in'] + a['usd_out_est'] for a in A) / n:.3f} "
          f"long-tier-requests={sum(a.get('haiku_long', 0) for a in A)} -->")
A = impl["haiku"]
print(f"<!-- haiku impl tokens priced at Sonnet: "
      f"{(sum(a['in'] for a in A) * 2 + sum(a['cw'] for a in A) * 4 + sum(a['cr'] for a in A) * 0.1 + sum(a['out_est'] for a in A) * 10) / 1e6:.2f}"
      f" vs actual {sum(a['usd_in'] + a['usd_out_est'] for a in A):.2f} -->")
for lo, hi, name in (("2026-10-09", "2026-10-10T00", "normal"), ("2026-10-10T00", "2027", "low")):
    R = [a for a in d["agents"] if a["role"] == "reviewer" and a["first"] and lo <= a["first"] < hi]
    print(f"<!-- reviews effort {name}: n={len(R)} $/review={sum(a['usd_in'] + a['usd_out_est'] for a in R) / len(R):.2f} "
          f"req/review={sum(a['requests'] for a in R) / len(R):.0f} -->")
