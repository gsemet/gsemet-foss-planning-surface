"""Price every API request of one Claude Code session (main + subagents) at list prices.

Usage: python3 -I cost2.py <session-base> <out.json>

- Requests are deduplicated by message.id; per id we keep the record with the largest output.
- Input, cache-write and cache-read counts are reliable (known when the stream starts).
- Output: main-session records carry the final count. Most subagent records only carry the
  start-of-stream count, so for those we also estimate output from the stored text and tool-call
  input (chars / 3.6). Thinking text is not stored, so the estimate is a floor.
- Cache writes are priced at the 1-hour rate (this session ran with the 1-hour TTL); the 5-minute
  rate is given as a lower bound.
"""
import json, sys, os, glob, re, collections

base, out = sys.argv[1], sys.argv[2]
PRICES = {  # USD per MTok: input, cw5m, cw1h, cache read, output
    "opus": (4.0, 5.0, 8.0, 0.20, 20.0),
    "sonnet": (2.0, 2.5, 4.0, 0.10, 10.0),
    "haiku": (0.10, 0.125, 0.20, 0.01, 0.50),
    "haiku_long": (0.50, 0.625, 1.0, 0.05, 2.50),
}
CHARS_PER_TOKEN = 3.6


def family(model):
    for f in ("opus", "sonnet", "haiku"):
        if f in model:
            return f
    return None


def read(path):
    recs = {}
    with open(path, errors="replace") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") != "assistant":
                continue
            m = d.get("message") or {}
            u, mid, model = m.get("usage"), m.get("id"), m.get("model", "")
            if not u or not mid or not family(model):
                continue
            chars = 0
            for c in m.get("content") or []:
                if c.get("type") == "text":
                    chars += len(c.get("text") or "")
                elif c.get("type") == "tool_use":
                    chars += len(json.dumps(c.get("input"), ensure_ascii=False))
            r = recs.setdefault(mid, {"model": model, "in": 0, "cw": 0, "cr": 0, "out": 0,
                                      "chars": 0, "final": False, "ts": d.get("timestamp")})
            r["in"] = max(r["in"], int(u.get("input_tokens") or 0))
            r["cw"] = max(r["cw"], int(u.get("cache_creation_input_tokens") or 0))
            r["cr"] = max(r["cr"], int(u.get("cache_read_input_tokens") or 0))
            r["out"] = max(r["out"], int(u.get("output_tokens") or 0))
            r["chars"] += chars  # content blocks of one message are split over records
            r["final"] = r["final"] or m.get("stop_reason") is not None
    return recs


def price(r):
    f = family(r["model"])
    prompt = r["in"] + r["cw"] + r["cr"]
    if f == "haiku" and prompt > 100_000:
        f = "haiku_long"
    pi, cw5, cw1, pcr, po = PRICES[f]
    out_est = r["out"] if r["final"] else max(r["out"], round(r["chars"] / CHARS_PER_TOKEN))
    inp = (r["in"] * pi + r["cr"] * pcr) / 1e6
    return {
        "input_usd": inp + r["cw"] * cw1 / 1e6,
        "input_usd_5m": inp + r["cw"] * cw5 / 1e6,
        "output_usd_recorded": r["out"] * po / 1e6,
        "output_usd_est": out_est * po / 1e6,
        "out_est": out_est,
        "long": f == "haiku_long",
    }


def task_of(desc):
    m = re.search(r"\bT(\d\d)\b", desc or "")
    return f"T{m.group(1)}" if m else None


def role_of(desc):
    d = (desc or "").lower()
    if "review" in d and "visual" not in d:
        return "reviewer"
    if "implement" in d:
        return "implementer"
    if "visual" in d:
        return "visual review"
    if "replay" in d:
        return "replay"
    return "other"


def zero():
    return collections.Counter()


def acc(c, r, p):
    c["requests"] += 1
    c["in"] += r["in"]; c["cw"] += r["cw"]; c["cr"] += r["cr"]
    c["out_recorded"] += r["out"]; c["out_est"] += p["out_est"]
    c["usd_in"] += p["input_usd"]; c["usd_in_5m"] += p["input_usd_5m"]
    c["usd_out_rec"] += p["output_usd_recorded"]; c["usd_out_est"] += p["output_usd_est"]
    c["haiku_long"] += int(p["long"])


by_model = collections.defaultdict(zero)
by_source = collections.defaultdict(zero)
by_role = collections.defaultdict(zero)
agents = []

for mid, r in read(base + ".jsonl").items():
    p = price(r)
    acc(by_model[family(r["model"])], r, p)
    acc(by_source[f"main|{family(r['model'])}"], r, p)

for meta_path in sorted(glob.glob(os.path.join(base, "subagents", "*.meta.json"))):
    meta = json.load(open(meta_path))
    jl = meta_path[: -len(".meta.json")] + ".jsonl"
    if not os.path.exists(jl):
        continue
    tot = zero()
    fams = collections.Counter()
    first = last = None
    for mid, r in read(jl).items():
        p = price(r)
        f = family(r["model"])
        acc(by_model[f], r, p)
        acc(by_source[f"subagent|{f}"], r, p)
        acc(by_role[f"{role_of(meta.get('description'))}|{f}"], r, p)
        acc(tot, r, p)
        fams[f] += 1
        first = min(first or r["ts"], r["ts"])
        last = max(last or r["ts"], r["ts"])
    agents.append({"description": meta.get("description"), "task": task_of(meta.get("description")),
                   "role": role_of(meta.get("description")),
                   "family": fams.most_common(1)[0][0] if fams else None,
                   "first": first, "last": last, **tot})

json.dump({"by_model": by_model, "by_source": by_source, "by_role": by_role, "agents": agents},
          open(out, "w"), indent=1, default=dict)


def show(title, d):
    print(f"\n## {title}")
    print(f"{'key':26} {'req':>6} {'input':>9} {'cw':>11} {'cr':>13} {'out_rec':>10} {'out_est':>10}"
          f" {'$in(1h)':>9} {'$out_est':>9} {'$total':>9}")
    for k, c in sorted(d.items()):
        print(f"{k:26} {c['requests']:>6} {c['in']:>9,} {c['cw']:>11,} {c['cr']:>13,} "
              f"{c['out_recorded']:>10,} {c['out_est']:>10,} {c['usd_in']:>9.2f} {c['usd_out_est']:>9.2f}"
              f" {c['usd_in'] + c['usd_out_est']:>9.2f}")


show("by model", by_model)
show("by source", by_source)
show("by role (subagents)", by_role)
