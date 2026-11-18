"""The Drivers started by each steering session: how long they ran and what a fresh one costs to
start (figures only).

Command: python 06-drivers.py > 06-drivers.csv

For every subagent of a job's steering session whose `agentType` (from its `.meta.json`) ends in
`driver` and whose time range meets the batch's window: the type, first and last record time, calls,
peak context, the context and the cumulative cost at its 15th call (what a restarted Driver pays to
be ready: it re-reads its card, the CR and the branch), and its compactions. Jobs and windows as in
03-steering-calls.py. Message text is not read; the agent ids are the host's own.
"""
import csv, glob, importlib.util, json, os, re, sys

spec = importlib.util.spec_from_file_location("calls03", os.path.join(os.path.dirname(os.path.abspath(__file__)), "03-steering-calls.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(["batch", "steering_session", "agent", "type", "first", "last", "calls", "peak_context", "ctx_at_call_15", "cum_usd_at_call_15", "compactions"])
done = set()
for batch, kind, folder, sid in m.JOBS:
    a, z = (m.when(x + "+00:00") for x in m.WINDOW[batch])
    for meta in sorted(glob.glob(f"{m.B}/{folder}/{sid}/subagents/*.meta.json")):
        try:
            t = json.load(open(meta, encoding="utf-8")).get("agentType", "")
        except ValueError:
            continue
        if not t.endswith("driver"):
            continue
        path = meta[:-len(".meta.json")] + ".jsonl"
        if not os.path.exists(path):
            continue
        seen, n, cum, first, last, peak, comp, c15, u15 = set(), 0, 0.0, None, None, 0, 0, "", ""
        with open(path, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                ts = d.get("timestamp")
                if ts:
                    first, last = first or ts, ts
                if d.get("type") == "system" and d.get("subtype") == "compact_boundary":
                    comp += 1
                msg = d.get("message") if d.get("type") == "assistant" else None
                if not isinstance(msg, dict) or not msg.get("usage") or msg.get("model") == "<synthetic>" or msg.get("id") in seen:
                    continue
                u = msg["usage"]
                cc = u.get("cache_creation") or {}
                tk = (u.get("input_tokens", 0), cc.get("ephemeral_5m_input_tokens", 0), cc.get("ephemeral_1h_input_tokens", 0), u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0))
                if not any(tk):
                    continue
                seen.add(msg["id"])
                n += 1
                rate = m.PRICE.get(re.sub(r"-\d{8}$", "", msg.get("model", "")))
                cum += sum(x * y / 1e6 for x, y in zip(tk, rate)) if rate else 0
                peak = max(peak, sum(tk[:4]))
                if n == 15:
                    c15, u15 = sum(tk[:4]), round(cum, 4)
        if first and m.when(last) >= a and m.when(first) <= z and n:
            w.writerow([f"batch-{batch}", sid[:8], os.path.basename(path)[6:14], t, first, last, n, peak, c15, u15, comp])
