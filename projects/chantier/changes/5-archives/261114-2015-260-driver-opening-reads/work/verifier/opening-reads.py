"""Opening-read cost of first CR Drivers in a steering session's subagents folder.
Usage: python opening-reads.py <subagents-folder>   (CR-236 method, CR-260 spec "Method")"""
import json, re, statistics, sys, pathlib, datetime

RESTART = re.compile(r"\(resume|\(rebase|\(gate|\(hand-back|\[", re.I)

def prompt(u):
    cc = u.get("cache_creation") or {}
    return (u.get("input_tokens", 0) + cc.get("ephemeral_5m_input_tokens", 0)
            + cc.get("ephemeral_1h_input_tokens", 0) + u.get("cache_read_input_tokens", 0))

def analyse(jl):
    calls = {}      # message.id -> (order, usage)
    first_round_idx = None
    reads = []      # (call index, path, offset, limit)
    order = []
    start = None
    for line in jl.read_text(encoding="utf-8").splitlines():
        try: e = json.loads(line)
        except Exception: continue
        if start is None: start = e.get("timestamp")
        if e.get("type") != "assistant": continue
        m = e.get("message", {})
        if m.get("model") == "<synthetic>": continue
        mid = m.get("id")
        if mid not in calls: order.append(mid)
        calls[mid] = m.get("usage") or {}
        for c in m.get("content", []) if isinstance(m.get("content"), list) else []:
            if c.get("type") != "tool_use": continue
            i = order.index(mid); inp = c.get("input", {})
            if c["name"] == "Read":
                reads.append((i, inp.get("file_path"), inp.get("offset"), inp.get("limit")))
            if first_round_idx is None and (c["name"] == "Agent" or
                    (c["name"] in ("Bash", "PowerShell") and re.search(r"\bround\b", inp.get("command", "")) and "chantier" in inp.get("command", "").lower())):
                first_round_idx = i
    if first_round_idx is None or not order: return None
    cost = prompt(calls[order[first_round_idx]]) - prompt(calls[order[0]])
    rd = [(p, o, l) for i, p, o, l in reads if i <= first_round_idx]
    return start, cost, rd

def main(folder):
    folder = pathlib.Path(folder)
    first, others, pending = [], [], []
    for meta in sorted(folder.glob("agent-*.meta.json")):
        j = json.loads(meta.read_text(encoding="utf-8"))
        if j.get("agentType") != "chantier:cr-driver": continue
        desc = j.get("description", "")
        cr = (re.search(r"CR-\d+", desc) or [desc])[0]
        r = analyse(meta.with_name(meta.name.replace(".meta.json", ".jsonl")))
        aid = meta.name[len("agent-"):-len(".meta.json")]
        if r is None: pending.append((cr, aid, desc)); continue
        start, cost, rd = r
        row = (cr, aid, start, cost, rd)
        (others if RESTART.search(desc) else first).append(row)
    for title, rows in (("FIRST DRIVERS", first), ("OTHER (restarts, not in mean)", others)):
        print(f"== {title}: {len(rows)}")
        for cr, aid, st, cost, rd in sorted(rows, key=lambda x: x[2] or ""):
            print(f"{cr} {aid} {st} opening={cost/1000:.1f}k")
            for p, o, l in rd:
                print(f"    {pathlib.PurePath(p or '?').name}" + (f" offset={o} limit={l}" if o or l else " (whole)"))
        if rows:
            v = [r[3] for r in rows]
            print(f"mean={statistics.mean(v)/1000:.1f}k median={statistics.median(v)/1000:.1f}k n={len(v)}")
    print(f"== no first round yet: {len(pending)}")
    for p in pending: print("  ", *p)

if __name__ == "__main__":
    main(sys.argv[1])
